#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kandidaten fuer den Erkennungsmodus von Commons holen und anschauen.

    tools/sammeln.py --kategorie "Cumulus humilis clouds" --klasse cu-humilis
    tools/sammeln.py --bogen cu-humilis      # Kontaktbogen neu zeichnen

Nicht die Fotos fuer das Paket -- das macht tools/fotos.py aus
erkennen.py. Hier wird gesucht: aus einer Commons-Kategorie werden die
Dateien aufgelistet, die Lizenz geprueft und kleine Vorschauen geholt,
und daraus ein Kontaktbogen mit Nummern gezeichnet. Ausgewaehlt wird
danach mit den Augen, nicht mit einem Filter: fuer eine Erkennungsuebung
ist ein Bild, bei dem man selbst zoegert, ein schlechtes Bild.

Alles landet unter kandidaten/ und gehoert nicht ins Repository.
"""
from __future__ import unicode_literals

import argparse
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(HIER)
KAND = os.path.join(WURZEL, "kandidaten")

API = "https://commons.wikimedia.org/w/api.php"
KENNUNG = "segelflug-kurs/1.0 (https://github.com/smatkovi/segelflug)"

ERLAUBT = re.compile(r"cc0|public domain|cc by|cc-by|pd-", re.I)
VERBOTEN = re.compile(r"gfdl|non-?free|fair use|nc\b|nd\b", re.I)
# Aus der Luft oder vom Satelliten sieht man Wolken von oben. Geuebt wird
# der Blick aus dem Cockpit und vom Platz, also von unten und von der Seite.
VONOBEN = re.compile(r"satellit|from space|iss\b|modis|aqua|terra modis|"
                     r"aerial|from the air|from above|von oben|airplane window|"
                     r"flight|window seat|a380|boeing|airbus", re.I)
VORSCHAU = 300


def hole(url, versuche=4):
    """Holen, und bei einem abgerissenen Strang noch einmal.

    Commons wirft bei ein paar hundert Anfragen hintereinander regelmaessig
    eine Verbindung weg (Errno 104). Das ist kein Fehler im Sinne von "das
    Bild gibt es nicht", sondern eine Bitte, langsamer zu machen -- also
    kurz warten und noch einmal, statt den ganzen Lauf abzubrechen.
    """
    import time
    bitte = urllib.request.Request(url, headers={"User-Agent": KENNUNG})
    for versuch in range(versuche):
        try:
            return urllib.request.urlopen(bitte, timeout=120).read()
        except Exception as fehler:
            if versuch == versuche - 1:
                raise
            print("     noch einmal (%s)" % fehler, file=sys.stderr)
            time.sleep(2 * (versuch + 1))


def frage(**werte):
    werte.setdefault("action", "query")
    werte.setdefault("format", "json")
    return json.loads(hole(API + "?" + urllib.parse.urlencode(werte)))


def klartext(html):
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = (text.replace("&amp;", "&").replace("&nbsp;", " ")
                .replace("&quot;", "\"").replace("&#039;", "'"))
    return " ".join(text.split())[:80].strip()


def unterkategorien(kategorie, wieviele=12):
    """Die Unterkategorien einer Kategorie.

    Manche Oberbegriffe auf Commons tragen selbst keine Bilder, sondern nur
    Unterkategorien -- "Stratocumulus" etwa haelt alles in "Stratocumulus
    stratiformis clouds in Germany" und zwanzig aehnlichen. Wer nur die
    Kategorie selbst abfragt, bekommt null Dateien und glaubt, es gebe
    keine Bilder.
    """
    antwort = frage(list="categorymembers", cmtitle="Category:" + kategorie,
                    cmtype="subcat", cmlimit=str(wieviele))
    return [e["title"][len("Category:"):]
            for e in (antwort.get("query") or {}).get("categorymembers", [])]


def dateien(kategorie, grenze):
    """Alle Bilddateien einer Kategorie, mit Lizenz und Vorschau-Adresse."""
    aus = []
    weiter = {}
    while len(aus) < grenze:
        antwort = frage(generator="categorymembers",
                        gcmtitle="Category:" + kategorie,
                        gcmtype="file", gcmlimit="50",
                        prop="imageinfo",
                        iiprop="url|size|extmetadata|mime",
                        iiurlwidth=str(VORSCHAU), **weiter)
        seiten = (antwort.get("query") or {}).get("pages") or {}
        if not seiten:
            break
        for seite in seiten.values():
            bilder = seite.get("imageinfo")
            if not bilder:
                continue
            bild = bilder[0]
            if bild.get("mime") not in ("image/jpeg", "image/png"):
                continue
            meta = bild.get("extmetadata", {})
            aus.append({
                "titel": seite["title"],
                "lizenz": klartext(meta.get("LicenseShortName", {}).get("value")),
                "lizenzurl": meta.get("LicenseUrl", {}).get("value") or "",
                "autor": (klartext(meta.get("Artist", {}).get("value"))
                          or klartext(meta.get("Credit", {}).get("value"))),
                "breite": bild.get("width"), "hoehe": bild.get("height"),
                "vorschau": bild.get("thumburl"),
                "seite": bild.get("descriptionurl", ""),
            })
        weiter = (antwort.get("continue") or {})
        weiter.pop("continue", None)
        if not weiter:
            break
    return aus


def suchdateien(suche, grenze):
    """Dateien ueber die Volltextsuche statt ueber eine Kategorie.

    Fuer "Wolkenstrasse" gibt es keine brauchbare Kategorie -- Commons
    kennt "Category:Cloud streets", aber sie ist leer. Gesucht wird
    deshalb in den Dateinamen und Beschreibungen.
    """
    aus = []
    weiter = {}
    while len(aus) < grenze:
        antwort = frage(generator="search", gsrsearch=suche,
                        gsrnamespace="6", gsrlimit="50",
                        prop="imageinfo",
                        iiprop="url|size|extmetadata|mime",
                        iiurlwidth=str(VORSCHAU), **weiter)
        seiten = (antwort.get("query") or {}).get("pages") or {}
        if not seiten:
            break
        for seite in seiten.values():
            bilder = seite.get("imageinfo")
            if not bilder or bilder[0].get("mime") not in ("image/jpeg",
                                                           "image/png"):
                continue
            bild = bilder[0]
            meta = bild.get("extmetadata", {})
            aus.append({
                "titel": seite["title"],
                "lizenz": klartext(meta.get("LicenseShortName", {}).get("value")),
                "lizenzurl": meta.get("LicenseUrl", {}).get("value") or "",
                "autor": (klartext(meta.get("Artist", {}).get("value"))
                          or klartext(meta.get("Credit", {}).get("value"))),
                "breite": bild.get("width"), "hoehe": bild.get("height"),
                "vorschau": bild.get("thumburl"),
                "seite": bild.get("descriptionurl", ""),
            })
        weiter = (antwort.get("continue") or {})
        weiter.pop("continue", None)
        if not weiter:
            break
    return aus


def titeldateien(titel):
    """Genau diese Dateien, ohne Suche -- fuer das, was weder Kategorie
    noch Suche ordentlich findet (die Wolkenstrasse etwa)."""
    aus = []
    for i in range(0, len(titel), 30):
        antwort = frage(titles="|".join(titel[i:i + 30]), prop="imageinfo",
                        iiprop="url|size|extmetadata|mime",
                        iiurlwidth=str(VORSCHAU))
        for seite in ((antwort.get("query") or {}).get("pages") or {}).values():
            bilder = seite.get("imageinfo")
            if not bilder:
                continue
            bild = bilder[0]
            meta = bild.get("extmetadata", {})
            aus.append({
                "titel": seite["title"],
                "lizenz": klartext(meta.get("LicenseShortName", {}).get("value")),
                "lizenzurl": meta.get("LicenseUrl", {}).get("value") or "",
                "autor": (klartext(meta.get("Artist", {}).get("value"))
                          or klartext(meta.get("Credit", {}).get("value"))),
                "breite": bild.get("width"), "hoehe": bild.get("height"),
                "vorschau": bild.get("thumburl"),
                "seite": bild.get("descriptionurl", ""),
            })
    return aus


def brauchbar(d):
    if not d["vorschau"]:
        return "ohne Vorschau"
    if VERBOTEN.search(d["lizenz"]) or not ERLAUBT.search(d["lizenz"]):
        return "Lizenz %r" % (d["lizenz"] or "?")
    if not d["autor"]:
        return "kein Urheber"
    if VONOBEN.search(d["titel"]):
        return "von oben"
    if min(d["breite"] or 0, d["hoehe"] or 0) < 480:
        return "zu klein"
    return None


def laden(klasse, kategorie, grenze, suche=None, titel=None):
    os.makedirs(os.path.join(KAND, klasse), exist_ok=True)
    if titel:
        liste = titeldateien(titel)
    elif suche:
        liste = suchdateien(suche, grenze)
    else:
        liste = dateien(kategorie, grenze)
    if len(liste) < grenze and not suche and not titel:
        gesehen = set(d["titel"] for d in liste)
        for unter in unterkategorien(kategorie):
            if len(liste) >= grenze:
                break
            print("     auch aus: %s" % unter)
            for d in dateien(unter, grenze - len(liste)):
                if d["titel"] not in gesehen:
                    gesehen.add(d["titel"])
                    liste.append(d)
    gut, weg = [], {}
    for d in liste:
        grund = brauchbar(d)
        if grund:
            weg[grund] = weg.get(grund, 0) + 1
            continue
        gut.append(d)
    print("  %s: %d Dateien, %d brauchbar"
          % (suche or kategorie, len(liste), len(gut)))
    for grund, wieviel in sorted(weg.items()):
        print("     weg: %-16s %d" % (grund, wieviel))

    from PIL import Image
    for nummer, d in enumerate(gut):
        ziel = os.path.join(KAND, klasse, "%03d.jpg" % nummer)
        if not os.path.exists(ziel):
            bild = Image.open(io.BytesIO(hole(d["vorschau"]))).convert("RGB")
            bild.save(ziel, "JPEG", quality=78)
        d["nummer"] = nummer
        d["vorschaudatei"] = ziel
    with open(os.path.join(KAND, klasse, "index.json"), "w",
              encoding="utf-8") as fh:
        fh.write(json.dumps({"kategorie": kategorie, "dateien": gut},
                            ensure_ascii=False, indent=1))
    return gut


def bogen(klasse, spalten=4, zeilen=4):
    """Kontaktboegen zeichnen: Nummern gross drauf, damit ich sie nennen kann."""
    from PIL import Image, ImageDraw
    with open(os.path.join(KAND, klasse, "index.json"), encoding="utf-8") as fh:
        gut = json.load(fh)["dateien"]
    kasten = 300
    pro = spalten * zeilen
    namen = []
    for seite in range((len(gut) + pro - 1) // pro):
        teil = gut[seite * pro:(seite + 1) * pro]
        blatt = Image.new("RGB", (spalten * kasten, zeilen * kasten), "white")
        mal = ImageDraw.Draw(blatt)
        for i, d in enumerate(teil):
            x, y = (i % spalten) * kasten, (i // spalten) * kasten
            bild = Image.open(d["vorschaudatei"]).convert("RGB")
            bild.thumbnail((kasten - 4, kasten - 24), Image.LANCZOS)
            blatt.paste(bild, (x + 2, y + 22))
            mal.rectangle([x, y, x + kasten - 1, y + 19], fill="black")
            mal.text((x + 4, y + 4), "%d  %dx%d" % (d["nummer"], d["breite"],
                                                    d["hoehe"]), fill="white")
        name = os.path.join(KAND, "bogen-%s-%d.png" % (klasse, seite))
        blatt.save(name)
        namen.append(name)
        print("  %s (%d Bilder)" % (name, len(teil)))
    return namen


def main():
    teiler = argparse.ArgumentParser(description=__doc__)
    teiler.add_argument("--kategorie")
    teiler.add_argument("--suche", help="Volltextsuche statt Kategorie")
    teiler.add_argument("--titel", help="Datei mit Commons-Titeln, einer je Zeile")
    teiler.add_argument("--klasse", required=True)
    teiler.add_argument("--grenze", type=int, default=60)
    teiler.add_argument("--bogen", action="store_true")
    args = teiler.parse_args()
    if args.kategorie or args.suche or args.titel:
        titel = None
        if args.titel:
            with open(args.titel, encoding="utf-8") as fh:
                titel = [z.strip() for z in fh if z.strip()]
        laden(args.klasse, args.kategorie, args.grenze, args.suche, titel)
    bogen(args.klasse)
    return 0


if __name__ == "__main__":
    sys.exit(main())
