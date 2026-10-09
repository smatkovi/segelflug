#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Holt die echten Wolkenfotos von Wikimedia Commons und legt sie daneben.

    tools/fotos.py            # alle Fotos aus wolkenfotos.py holen
    tools/fotos.py --pruefen  # nur nachsehen, ob alles da und frei ist

Welche Fotos es sind und wohin bei jedem zu schauen ist, steht in
wolkenfotos.py. Hier steht nur, wie sie ins Paket kommen.

Drei Dinge entscheidet dieses Werkzeug, und alle drei aus demselben Grund
-- das Ziel ist ein Telefon mit 480 oder 540 Punkten Breite:

* **Groesse.** Commons liefert auf Wunsch jede Breite; geholt werden 640
  Punkte. Das ist auf dem N9 ueber die volle Breite noch scharf und kostet
  rund 80 kB statt 5 MB.
* **Format.** JPEG, nicht PNG. Ein Foto in PNG ist viermal so gross und
  sieht gleich aus. Die Zeichnungen bleiben PNG -- bei Flaechen und harten
  Kanten ist es umgekehrt.
* **Herkunft.** Zu jedem Bild werden Urheber, Lizenz und Fundstelle
  mitgeschrieben, nach bilder/fotos.json und nach CREDITS. Die Lizenzen
  verlangen das, und die App zeigt die Zeile unter dem Foto.

Nicht jedes freie Bild ist gleich frei: CC0, gemeinfrei, CC BY und CC BY-SA
sind in Ordnung, GFDL-nur nicht (unvertraeglich mit dem Rest und fuer ein
Telefonpaket unbrauchbar). Faellt ein Bild durch, bricht der Lauf ab,
statt es stillschweigend wegzulassen.

Die Bilder und bilder/fotos.json gehoeren ins Repository: der Kurs soll
sich auch ohne Netz bauen lassen.
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
sys.path.insert(0, WURZEL)

from wolkenfotos import WOLKENFOTOS          # noqa: E402

BILDER = os.path.join(WURZEL, "bilder")
INDEX = os.path.join(BILDER, "fotos.json")
CREDITS = os.path.join(WURZEL, "CREDITS")

API = "https://commons.wikimedia.org/w/api.php"
# Wikimedia weist Anfragen ohne eigene Kennung ab, und zwar zu Recht.
KENNUNG = "segelflug-kurs/1.0 (https://github.com/smatkovi/segelflug)"

BREITE = 640                 # Zielbreite in Punkten
HOEHE = 520                  # und so hoch darf ein Hochformat hoechstens werden
ERLAUBT = re.compile(r"cc0|public domain|cc by|cc-by|pd-", re.I)
VERBOTEN = re.compile(r"gfdl|non-?free|fair use|nc\b|nd\b", re.I)


def klartext(html):
    """Aus dem Urheberfeld von Commons einen Namen machen.

    Das Feld ist roher HTML und reicht von "<a …>Glg</a>" bis zu einem
    kompletten Lizenzkasten mit Tabelle. Tags raus, Leerraum glaetten,
    und falls dann noch ein Absatz uebrig ist, die erste Zeile nehmen --
    unter dem Foto ist Platz fuer einen Namen, nicht fuer einen Kasten.
    """
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = (text.replace("&amp;", "&").replace("&nbsp;", " ")
                .replace("&quot;", "\"").replace("&#039;", "'"))
    text = " ".join(text.split())
    return text[:80].strip()


def hole(url):
    bitte = urllib.request.Request(url, headers={"User-Agent": KENNUNG})
    return urllib.request.urlopen(bitte, timeout=120).read()


def auskunft(titel):
    """Urheber, Lizenz und eine 640 Punkte breite Fassung -- in einem Zug."""
    frage = urllib.parse.urlencode({
        "action": "query", "format": "json", "titles": "|".join(titel),
        "prop": "imageinfo", "iiprop": "url|size|extmetadata",
        "iiurlwidth": str(BREITE),
    })
    antwort = json.loads(hole(API + "?" + frage))
    seiten = (antwort.get("query") or {}).get("pages") or {}
    # Commons normalisiert Titel (Unterstriche, Grossbuchstaben); ohne die
    # Rueckuebersetzung findet sich das angefragte Bild nicht wieder.
    zurueck = {}
    for eintrag in (antwort.get("query") or {}).get("normalized", []):
        zurueck[eintrag["to"]] = eintrag["from"]
    aus = {}
    for seite in seiten.values():
        name = zurueck.get(seite["title"], seite["title"])
        bilder = seite.get("imageinfo")
        if not bilder:
            aus[name] = None
            continue
        bild = bilder[0]
        meta = bild.get("extmetadata", {})
        aus[name] = {
            "lizenz": klartext(meta.get("LicenseShortName", {}).get("value")),
            "lizenzurl": (meta.get("LicenseUrl", {}).get("value") or ""),
            "autor": (klartext(meta.get("Artist", {}).get("value"))
                      or klartext(meta.get("Credit", {}).get("value"))),
            "seite": bild.get("descriptionurl", ""),
            "url": bild.get("thumburl") or bild.get("url"),
            "breite": bild.get("thumbwidth") or bild.get("width"),
            "hoehe": bild.get("thumbheight") or bild.get("height"),
        }
    return aus


def dateiname(art, nummer):
    return "foto-%s-%d.jpg" % (art, nummer + 1)


def pruefen(art, titel, daten):
    if daten is None:
        return "%s: %s gibt es auf Commons nicht" % (art, titel)
    if not daten["url"]:
        return "%s: %s liefert kein Bild" % (art, titel)
    lizenz = daten["lizenz"]
    if VERBOTEN.search(lizenz) or not ERLAUBT.search(lizenz):
        return "%s: %s steht unter %r -- nicht verwendbar" % (art, titel,
                                                              lizenz or "?")
    if not daten["autor"]:
        # CC BY und BY-SA verlangen die Nennung. Ohne Namen laesst sich die
        # Bedingung nicht erfuellen, also kommt das Bild nicht ins Paket.
        return "%s: %s nennt keinen Urheber" % (art, titel)
    return None


def speichern(daten, ziel):
    """Das geholte Bild als JPEG ablegen -- neu gerechnet, nicht durchgereicht.

    Commons liefert die Vorschau in Studioqualitaet; auf einem Telefon ist
    das halbe Megabyte je Foto, das niemand sieht. Also wird jedes Bild hier
    noch einmal gerechnet: Qualitaet 82 und, wichtiger, eine Grenze auch
    fuer die Hoehe. Ohne sie steht ein Hochformat 850 Punkte hoch auf einem
    854 Punkte hohen Bildschirm -- ein Foto, fuer das man scrollen muss,
    waehrend die Zeichnung darueber aus dem Bild laeuft.

    Die wirkliche Groesse wird zurueckgegeben, nicht die angefragte: Die App
    rechnet die Rahmenhoehe daraus aus.
    """
    roh = hole(daten["url"])
    from PIL import Image
    bild = Image.open(io.BytesIO(roh)).convert("RGB")
    bild.thumbnail((BREITE, HOEHE), Image.LANCZOS)
    bild.save(ziel, "JPEG", quality=82, optimize=True, progressive=False)
    daten["breite"], daten["hoehe"] = bild.size
    return os.path.getsize(ziel)


def credits_schreiben(index):
    zeilen = [
        "Fotos",
        "=====",
        "",
        "Die Zeichnungen (bilder/*.png) sind eigene Arbeit und stehen unter",
        "derselben Lizenz wie der Kurs; die Fotos sind die JPEG-Dateien.",
        "",
        "Die Fotos stammen von Wikimedia Commons. Jedes ist frei lizenziert;",
        "Urheber und Lizenz stehen hier und in der App unter dem Bild.",
        "",
    ]
    for art in sorted(index):
        zeilen.append(art)
        zeilen.append("-" * len(art))
        for foto in index[art]:
            zeilen.append("  %s" % foto["datei"])
            zeilen.append("    %s" % foto["titel"])
            zeilen.append("    %s -- %s" % (foto["autor"], foto["lizenz"]))
            zeilen.append("    %s" % foto["seite"])
        zeilen.append("")
    with open(CREDITS, "w", encoding="utf-8") as fh:
        fh.write("\n".join(zeilen))


def main():
    teiler = argparse.ArgumentParser(description=__doc__)
    teiler.add_argument("--pruefen", action="store_true",
                        help="nur nachsehen, nichts holen")
    args = teiler.parse_args()

    titel = [f["commons"] for liste in WOLKENFOTOS.values() for f in liste]
    auskuenfte = {}
    for i in range(0, len(titel), 40):       # die API nimmt 50 auf einmal
        auskuenfte.update(auskunft(titel[i:i + 40]))

    maengel = []
    for art, liste in sorted(WOLKENFOTOS.items()):
        for foto in liste:
            fehler = pruefen(art, foto["commons"],
                             auskuenfte.get(foto["commons"]))
            if fehler:
                maengel.append(fehler)
    if maengel:
        for fehler in maengel:
            print("  FEHLER " + fehler, file=sys.stderr)
        return 1
    if args.pruefen:
        print("%d Fotos, alle frei und mit Urheber" % len(titel))
        return 0

    os.makedirs(BILDER, exist_ok=True)
    index = {}
    gesamt = 0
    for art, liste in sorted(WOLKENFOTOS.items()):
        index[art] = []
        for nummer, foto in enumerate(liste):
            daten = auskuenfte[foto["commons"]]
            datei = dateiname(art, nummer)
            groesse = speichern(daten, os.path.join(BILDER, datei))
            gesamt += groesse
            index[art].append({
                "datei": datei,
                "breite": daten["breite"], "hoehe": daten["hoehe"],
                "hinweis": foto["hinweis"],
                "titel": foto["commons"][5:],     # ohne "File:"
                "autor": daten["autor"], "lizenz": daten["lizenz"],
                "lizenzurl": daten["lizenzurl"], "seite": daten["seite"],
            })
            print("  %-22s %4d x %-4d %6d B  %s"
                  % (datei, daten["breite"], daten["hoehe"], groesse,
                     daten["lizenz"]))

    with open(INDEX, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(index, ensure_ascii=False, indent=1,
                            sort_keys=True))
    credits_schreiben(index)
    print("%d Fotos, %d kB -- bilder/fotos.json und CREDITS geschrieben"
          % (len(titel), gesamt // 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
