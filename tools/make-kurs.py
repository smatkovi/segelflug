#!/usr/bin/env python3
"""Turns the authored glider course into the data file the app reads.

Same engine as C-Lehrer: it reads <app>/data/kurs.json and knows nothing
about the subject. What differs here is that every readable string is a
{"de": ..., "en": ...} pair and that lessons carry pictures instead of code.

    tools/make-kurs.py        # -> data/kurs.json
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import formeln as formelsatz
import kartenherleitungen
import kurs
import erkennen as erkennungsmodus
import wolkenfotos


def mischen(optionen, antwort, saat):
    """Die Antwortmöglichkeiten durchmischen und den Index nachführen.

    Beim Schreiben steht die richtige Antwort bequem an erster Stelle. Bliebe
    sie dort, wäre der ganze Kurs mit einem Fingertipp lösbar, ohne eine
    einzige Frage gelesen zu haben -- und genau so ist es aufgefallen: "es
    wird immer die erste Antwort ausgewählt".

    Gemischt wird deterministisch aus der Fragenkennung, nicht zufällig: Die
    Reihenfolge muss über Neubauten hinweg gleich bleiben, sonst sitzt eine
    gemerkte Position beim nächsten Update woanders.

    Die Streuung ist FNV-1a mit Nachmischung. Ein einfaches "mal 131 plus
    Zeichen" genügt hier nicht: Die Saatwerte unterscheiden sich oft nur in
    der letzten Ziffer, und dann liefern aufeinanderfolgende Fragen
    systematisch verwandte Reihenfolgen -- im ersten Versuch landete die
    richtige Antwort dadurch in der Hälfte aller Fälle wieder vorne.
    """
    zustand = 2166136261
    for zeichen in saat:
        zustand = ((zustand ^ ord(zeichen)) * 16777619) & 0xffffffff
    zustand ^= zustand >> 15
    zustand = (zustand * 2246822519) & 0xffffffff
    zustand ^= zustand >> 13
    zustand = (zustand * 3266489917) & 0xffffffff
    zustand ^= zustand >> 16

    def naechste():
        nonlocal zustand
        zustand ^= (zustand << 13) & 0xffffffff
        zustand ^= zustand >> 17
        zustand ^= (zustand << 5) & 0xffffffff
        return zustand

    reihen = list(range(len(optionen)))
    for i in range(len(reihen) - 1, 0, -1):
        j = naechste() % (i + 1)
        reihen[i], reihen[j] = reihen[j], reihen[i]
    return [optionen[k] for k in reihen], reihen.index(antwort)



def aufgabe(task, saat):
    """Rename the authoring keys to the ones the engine reads."""
    out = {"kind": task["kind"], "q": task["q"], "warum": task["warum"],
           "bild": task.get("bild", ""),
           # Dieselbe Wolke wie ueber der Frage, nur echt. Sie steht auf der
           # Aufgabenseite zweimal: ueber der Frage neben der Zeichnung und
           # noch einmal in der Loesung, wo man nach der Antwort Zeit hat,
           # hinzusehen. Verraten wird damit nichts, was die Zeichnung
           # darueber nicht schon zeigt.
           "fotos": fotos_fuer([task.get("bild", "")])}
    # Die Herleitung liegt daneben (kartenherleitungen.py) und wird ueber
    # den deutschen Fragetext zugeordnet, damit die Aufgaben selbst
    # unberuehrt bleiben. Sie steht in der Loesung; die Skizze dazu auch,
    # und ausdruecklich nicht in "bild" -- das steht ueber der Frage und
    # wuerde die Antwort verraten.
    frage = task["q"]
    schluessel = frage["de"] if isinstance(frage, dict) else frage
    herleitung = kartenherleitungen.HERLEITUNGEN.get(schluessel)
    if herleitung:
        out["herleitung"] = herleitung
        out["skizze"] = kartenherleitungen.SKIZZEN.get(schluessel, "")
    if task["kind"] == "mc":
        optionen, antwort = mischen(task["optionen"], task["antwort"], saat)
        out["options"] = optionen
        out["answer"] = antwort
        out["code"] = task.get("code", "")
    elif task["kind"] == "zahl":
        out["antwort"] = task["antwort"]
        out["einheit"] = task["einheit"]
        out["toleranz"] = task.get("toleranz", 0.1)
    return out


def fotos_fuer(arten):
    """Die Fotos zu einer Liste von Zeichnungsnamen, in dieser Reihenfolge.

    Masse und Herkunft stehen in bilder/fotos.json, das tools/fotos.py
    geschrieben hat. Fehlt die Datei, gibt es eben keine Fotos -- der Kurs
    soll sich auch ohne Netz bauen lassen.
    """
    pfad = os.path.join(ROOT, "bilder", "fotos.json")
    if not os.path.exists(pfad):
        return []
    with open(pfad, encoding="utf-8") as fh:
        geholt = json.load(fh)
    aus = []
    for art in arten:
        for eintrag in geholt.get(art, []):
            aus.append({
                "datei": eintrag["datei"],
                "breite": eintrag["breite"], "hoehe": eintrag["hoehe"],
                "hinweis": eintrag["hinweis"],
                "autor": eintrag["autor"], "lizenz": eintrag["lizenz"],
            })
    return aus


def fotos_zu(lektion):
    """Die Fotos, die unter die Zeichnung dieser Lektion gehoeren.

    Sie haengen am Namen der Zeichnung, nicht an der Lektion: Dieselbe
    Wolke in zwei Lektionen bekommt zweimal dieselben Fotos, und das ist
    richtig so -- wer in "Die flache Basis" einsteigt, hat die Bilder aus
    "Woher die Wolken ihre Namen haben" vielleicht nie gesehen.

    Zwei Wolken werden besprochen, ohne das Bild der Lektion zu sein (der
    Cumulonimbus in der Ueberentwicklung, die Linse bei den Wellen); die
    haengen ueber wolkenfotos.ZUSATZ an der Lektionskennung.

    Die Masse und die Herkunft stehen in bilder/fotos.json, das
    tools/fotos.py geschrieben hat. Fehlt die Datei, gibt es eben keine
    Fotos -- der Kurs soll sich auch ohne Netz bauen lassen.
    """
    arten = [lektion.get("bild", "")]
    arten += wolkenfotos.ZUSATZ.get(lektion["id"], [])
    return fotos_fuer(arten)


def erkennung():
    """Der Erkennungsmodus, so wie die App ihn liest.

    Die Klassen und ihre Texte stehen in erkennen.py, die Masse und die
    Herkunft der Bilder in bilder/erkennen.json (tools/fotos.py). Fehlt
    die Datei, bleibt der Modus leer -- und die App laesst die Taste dann
    weg, statt eine leere Seite anzubieten.
    """
    pfad = os.path.join(ROOT, "bilder", "erkennen.json")
    if not os.path.exists(pfad):
        print("Ohne bilder/erkennen.json: kein Erkennungsmodus",
              file=sys.stderr)
        return {}
    with open(pfad, encoding="utf-8") as fh:
        fotos = json.load(fh)
    klassen = [{"id": k["id"], "name": k["name"],
                "bedeutung": k["bedeutung"], "erkennen": k["erkennen"],
                "bedeutet": k["bedeutet"], "verwechselt": k["verwechselt"]}
               for k in erkennungsmodus.KLASSEN]
    bekannt = set(k["id"] for k in klassen)
    for foto in fotos:
        if foto["klasse"] not in bekannt:
            print("Foto ohne Klasse: " + foto["datei"], file=sys.stderr)
            return {}
    return {
        "titel": erkennungsmodus.TITEL,
        "unterzeile": erkennungsmodus.UNTERZEILE,
        "bedeutungen": [{"id": i, "text": text}
                        for i, text in erkennungsmodus.BEDEUTUNGEN],
        "klassen": klassen,
        "fotos": [{"datei": f["datei"], "klasse": f["klasse"],
                   "breite": f["breite"], "hoehe": f["hoehe"],
                   "autor": f["autor"], "lizenz": f["lizenz"]}
                  for f in fotos],
    }


def klassifizierer():
    """Foto deuten, so wie die App es liest.

    Die Klassentafel fuer das Netz in data/modell.bin (tools/MODELL.md):
    dieselben Texte wie im Erkennungsmodus, plus die vier Klassen ohne
    Uebungsfotos. Das Netz selbst nennt seine Klassen im Dateikopf; die
    App ordnet ueber die Kennung zu, nicht ueber die Stelle.
    """
    klassen = [{"id": k["id"], "name": k["name"],
                "bedeutung": k["bedeutung"], "erkennen": k["erkennen"],
                "bedeutet": k["bedeutet"]}
               for k in erkennungsmodus.klassifizierer_klassen()]
    bekannt = set(i for i, _ in erkennungsmodus.BEDEUTUNGEN)
    for k in klassen:
        if k["bedeutung"] not in bekannt:
            raise SystemExit("Klasse ohne Bedeutung: " + k["id"])
    return {
        "titel": erkennungsmodus.FOTO_TITEL,
        "unterzeile": erkennungsmodus.FOTO_UNTERZEILE,
        "tipps": erkennungsmodus.FOTO_TIPPS,
        "bedeutungen": [{"id": i, "text": text}
                        for i, text in erkennungsmodus.BEDEUTUNGEN],
        "klassen": klassen,
    }


def glossar(chapters):
    """Das Glossar: jedes Fachwort der App mit Definition und Zeichnung.

    Die Eintraege stehen in begriffe.py (BEGRIFFE, je {id, wort, definition,
    bild, siehe}). Die Kennungen sind dieselben wie in den `begriffe` der
    Lektionen, damit die Lektion ihre Woerter verlinken kann; Woerter, die
    nur im Text vorkommen, bekommen eigene Kennungen. Fehlt das Modul,
    bleibt das Glossar leer und die App laesst die Taste weg.
    """
    try:
        import begriffe as glossarmodul
    except ImportError:
        print("Ohne begriffe.py: kein Glossar", file=sys.stderr)
        return []
    eintraege = list(glossarmodul.BEGRIFFE)
    ids = [b["id"] for b in eintraege]
    if len(ids) != len(set(ids)):
        raise SystemExit("Glossar: doppelte Kennung")
    bekannt = set(ids)
    for b in eintraege:
        for s in b.get("siehe", []):
            if s not in bekannt:
                raise SystemExit("Glossar: siehe-Verweis ins Leere: %s -> %s"
                                 % (b["id"], s))
        if b.get("bild"):
            pfad = os.path.join(ROOT, "bilder", b["bild"] + ".png")
            if not os.path.exists(pfad):
                raise SystemExit("Glossar: Bild fehlt: " + pfad)
    fehlend = set()
    for chapter in chapters:
        for lesson in chapter["lektionen"]:
            for kennung in lesson["begriffe"]:
                if kennung not in bekannt:
                    fehlend.add(kennung)
    if fehlend:
        print("Lektionsbegriffe ohne Glossareintrag: " + ", ".join(sorted(fehlend)),
              file=sys.stderr)
    return [{"id": b["id"], "wort": b["wort"], "definition": b["definition"],
             "bild": b.get("bild", ""), "siehe": list(b.get("siehe", []))}
            for b in eintraege]


def verlinken(text, begriffe):
    """Die Fachwoerter eines Lektionstextes zu Glossarverweisen machen.

    Aus jeder Wortform (begriffe.py, `formen`) wird beim ERSTEN Vorkommen
    je Begriff der Marker [[begriff:<id>|<Wortform>]]. style.js und
    stil.js machen daraus in rich()/reich() einen Link, und die
    Lektionsseite oeffnet damit den Glossareintrag.

    Nur das erste Vorkommen, weil ein Text, in dem jedes zweite Wort
    unterstrichen ist, nicht mehr zu lesen ist: der Verweis wird einmal
    angeboten, nicht in jedem Satz.

    Nicht angetastet wird, was schon ausgezeichnet ist -- **Fettungen**
    (dort fuehrt die Lektion ihre eigenen Begriffe ein und erklaert sie
    gleich, ein Verweis waere dort ein Umweg), `Programmtext` und
    vorhandene [[...]]-Marker. Sonst stuende ein Marker im Marker und
    rich() zeigte ihn woertlich.

    Gesucht wird mit Lookarounds und nicht mit \\b: Formen wie "Alto-"
    enden auf einem Zeichen, das selbst keine Wortgrenze bildet, und \\b
    griffe dort ins Leere. Gross- und Kleinschreibung zaehlt, damit das
    englische "As" am Satzanfang nicht zum Altostratus wird -- Latein
    steht in beiden Sprachen gleich, deshalb kommen alle Formen in jeden
    Text.
    """
    if not text:
        return text

    def regel(formen):
        """Eine Alternative aus allen Formen, die laengste zuerst.

        Die Reihenfolge in der Alternative entscheidet bei gleichem
        Anfang: ohne sie faende "Cumulus" schon in "Cumulus humilis" sein
        Ende, und der Verweis haengte am halben Namen.
        """
        teile = sorted([f for f in formen if f.strip()], key=len, reverse=True)
        if not teile:
            return None
        return re.compile(r"(?<!\w)(?:"
                          + "|".join(re.escape(f) for f in teile)
                          + r")(?!\w)")

    def sperren(quelle):
        return [(m.start(), m.end()) for m in
                re.finditer(r"\*\*[^*]+\*\*|`[^`]+`|\[\[[^\]]+\]\]", quelle)]

    # Die Begriffe der Reihe nach, der mit der laengsten Form zuerst: so
    # belegt "Cumulus humilis" die Stelle, bevor der Begriff "Cumulus"
    # ueberhaupt sucht.
    sortiert = sorted(
        begriffe,
        key=lambda b: max([len(f) for f in b.get("formen", [])] or [0]),
        reverse=True)
    for b in sortiert:
        muster = regel(b.get("formen", []))
        if muster is None:
            continue
        verboten = sperren(text)
        for treffer in muster.finditer(text):
            if any(treffer.start() < ende and treffer.end() > anfang
                   for anfang, ende in verboten):
                continue
            text = (text[:treffer.start()]
                    + "[[begriff:" + b["id"] + "|" + treffer.group(0) + "]]"
                    + text[treffer.end():])
            break
    return text


def fotos_pruefen():
    """Jede Zeichnung, die als Lektionsbild vorkommt, soll Fotos haben.

    Sonst faellt es erst am Geraet auf, und dort nur dem, der zufaellig
    diese eine Lektion aufschlaegt.
    """
    gezeichnet = set()
    for kap in kurs.KAPITEL:
        for lek in kap["lektionen"]:
            if lek.get("bild"):
                gezeichnet.add(lek["bild"])
    ohne = sorted(gezeichnet - set(wolkenfotos.WOLKENFOTOS))
    for name in ohne:
        print("Zeichnung ohne Fotos: " + name, file=sys.stderr)
    return not ohne


def pruefen(chapters, sprachen):
    """Faellt, bevor ein halbfertiger Kurs ausgeliefert wird.

    Zwei Dinge sind im Feld schon schiefgegangen und beide fallen im
    Alltag nicht auf: eine Lektion, die nur auf Deutsch uebersetzt ist
    (die App zeigt dann stillschweigend die andere Sprache), und eine
    Formel ohne Herleitung. Also hier, beim Erzeugen, und nicht spaeter.
    """
    fehler = []

    def zwei(wert, wo):
        if isinstance(wert, dict):
            for code in sprachen:
                if not wert.get(code, "").strip():
                    fehler.append("%s: %s fehlt" % (wo, code))
        elif isinstance(wert, str) and wert.strip():
            fehler.append("%s: nur einsprachig" % wo)

    for c in chapters:
        zwei(c.get("titel"), "Kapitel %s Titel" % c["id"])
        zwei(c.get("text"), "Kapitel %s Text" % c["id"])
        for l in c["lektionen"]:
            zwei(l.get("titel"), "%s Titel" % l["id"])
            zwei(l.get("text"), "%s Text" % l["id"])
            for i, a in enumerate(l.get("aufgaben", [])):
                zwei(a.get("q"), "%s Aufgabe %d Frage" % (l["id"], i))
                zwei(a.get("warum"), "%s Aufgabe %d Begruendung" % (l["id"], i))
                for j, o in enumerate(a.get("optionen", []) or []):
                    zwei(o, "%s Aufgabe %d Antwort %d" % (l["id"], i, j))
    return fehler


def herleitungen_pruefen():
    """Jeder Schluessel muss auf eine wirkliche Frage zeigen.

    Ein Tippfehler waere sonst unsichtbar: die Herleitung faende ihre Karte
    nicht, und die Karte bliebe ohne Herleitung -- genau der Zustand, den
    es hier abzustellen gilt.
    """
    alle = set()
    for kapitel in kurs.KAPITEL:
        for lektion in kapitel["lektionen"]:
            for t in lektion["aufgaben"]:
                frage = t["q"]
                alle.add(frage["de"] if isinstance(frage, dict) else frage)
    verwaist = sorted(set(kartenherleitungen.HERLEITUNGEN) - alle) \
             + sorted(set(kartenherleitungen.SKIZZEN) - alle)
    for q in verwaist:
        print("Herleitung zeigt ins Leere: " + q, file=sys.stderr)
    return not verwaist


def main():
    if not herleitungen_pruefen():
        return 1
    if not fotos_pruefen():
        return 1
    chapters = []
    for chapter in kurs.KAPITEL:
        lessons = []
        for lesson in chapter["lektionen"]:
            lessons.append({
                "id": lesson["id"],
                "titel": lesson["titel"],
                "begriffe": lesson["begriffe"],
                "text": lesson["text"],
                "bild": lesson.get("bild", ""),
                "fotos": fotos_zu(lesson),
                "formeln": [dict(f) for f in lesson.get("formeln", [])],
                # No runnable example here -- the app hides the whole block
                # when it is empty, which is what a theory course wants.
                "beispiel": "",
                "ausgabe": "",
                "aufgaben": [aufgabe(t, lesson["id"] + "#" + str(i))
                             for i, t in enumerate(lesson["aufgaben"])],
            })
        chapters.append({
            "id": chapter["id"], "titel": chapter["titel"],
            "stufe": chapter["stufe"], "sprache": "-",
            "text": chapter["text"], "lektionen": lessons,
        })

    # ---- Glossarverweise in die Lektionstexte ---------------------------
    # Die Wortformen stehen in begriffe.py und nicht in kurs.json: die App
    # braucht sie nicht, verlinkt wird hier beim Bauen. Fehlt das Modul,
    # bleibt der Kurs ohne Verweise -- genau wie er ohne Glossar bleibt.
    try:
        import begriffe as glossarmodul
        glossarbegriffe = list(glossarmodul.BEGRIFFE)
    except ImportError:
        glossarbegriffe = []
    titelmuster = {}
    for b in glossarbegriffe:
        formen = sorted([f for f in b.get("formen", []) if f.strip()],
                        key=len, reverse=True)
        if formen:
            titelmuster[b["id"]] = re.compile(
                r"(?<!\w)(?:" + "|".join(re.escape(f) for f in formen)
                + r")(?!\w)", re.I)
    verweise = {"de": 0, "en": 0}
    for kap in chapters:
        for lek in kap["lektionen"]:
            texte = {}
            for code in ("de", "en"):
                titel = lek["titel"].get(code, "")
                # Die Lektion, die den Begriff selbst erklaert, verlinkt ihn
                # nicht: ein Verweis von der Ueberschrift "Cumulus humilis"
                # auf den Eintrag "Cumulus humilis" fuehrt im Kreis.
                dran = [b for b in glossarbegriffe
                        if b["id"] in titelmuster
                        and not titelmuster[b["id"]].search(titel)]
                texte[code] = verlinken(lek["text"].get(code, ""), dran)
                verweise[code] += texte[code].count("[[begriff:")
            # Ein neues Wortverzeichnis, nicht das aus kurs.py: die
            # Lektionen teilen ihre Textwoerterbuecher mit dem Modul, und
            # ein zweiter Lauf im selben Prozess verlinkte sonst doppelt.
            lek["text"] = texte
    print("Glossarverweise: de %d, en %d" % (verweise["de"], verweise["en"]))

    # Zu jeder Formel das Bild dazulegen, das tools/formeln.py gesetzt hat.
    # Fehlt eines, bleibt die Textzeile stehen und nur das Gesetzte fehlt --
    # matplotlib gibt es nur auf dem Baurechner, der Kurs soll sich ueberall
    # bauen lassen.
    bilder = formelsatz.gesetzte()
    ohne_bild = []
    for kap in chapters:
        for lek in kap["lektionen"]:
            for eintrag in lek.get("formeln", []):
                name = formelsatz.kennung(eintrag["tex"])
                daten = bilder.get(name)
                if not daten:
                    ohne_bild.append(eintrag["tex"])
                    continue
                eintrag["bild"] = name
                eintrag["breite"] = daten["breite"]
                eintrag["hoehe"] = daten["hoehe"]
    if ohne_bild:
        print("%d Formeln ohne Bild -- tools/formeln.py auf dem Baurechner "
              "laufen lassen:" % len(ohne_bild), file=sys.stderr)
        for tex in ohne_bild:
            print("   " + tex, file=sys.stderr)

    plan = [{"id": c["id"], "titel": c["titel"], "stufe": c["stufe"],
             "sprache": "-", "fertig": True} for c in chapters]
    for ident, titel, stufe in kurs.PLAN:
        plan.append({"id": ident, "titel": titel, "stufe": stufe,
                     "sprache": "-", "fertig": False})

    items = []
    for entry in kurs.EINSTUFUNG:
        e_optionen, e_antwort = mischen(entry["optionen"], entry["antwort"],
                                        entry["id"])
        items.append({
            "id": entry["id"], "stufe": entry["stufe"],
            "thema": entry["thema"], "frage": entry["q"],
            "code": "", "bild": entry.get("bild", ""),
            "optionen": e_optionen, "antwort": e_antwort,
            "warum": entry["warum"],
        })

    fehler = pruefen(chapters, ["de", "en"])
    if fehler:
        for f in fehler[:25]:
            print("  FEHLER " + f, file=sys.stderr)
        print("%d Maengel -- kein kurs.json geschrieben" % len(fehler),
              file=sys.stderr)
        return 1
    print("Zweisprachigkeit: vollstaendig")

    out = {
        "titel": {"de": "Segelflug", "en": "Soaring"},
        "untertitel": {
            "de": ("Segelflug- und PPL-Theorie. Schwerpunkt: an den Wolken "
                   "ablesen, was der Himmel hergibt."),
            "en": ("Glider and PPL theory. The focus: reading from the "
                   "clouds what the sky has to offer."),
        },
        "ausfuehrbar": False,
        "sprachen": ["de", "en"],
        "kapitel": chapters,
        "plan": plan,
        "einstufung": {"themen": kurs.THEMEN, "fragen": items},
        "erkennen": erkennung(),
        "klassifizierer": klassifizierer(),
        "begriffe": glossar(chapters),
    }
    path = os.path.join(ROOT, "data", "kurs.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
    bildzahl = sum(len(l["fotos"]) for c in chapters for l in c["lektionen"])
    uebung = out["erkennen"].get("fotos", [])
    print("data/kurs.json: %d Kapitel, %d Lektionen, %d Aufgaben, "
          "%d Einstufungsfragen, %d Fotos, %d Uebungsbilder in %d Klassen, "
          "%d B"
          % (len(chapters), sum(len(c["lektionen"]) for c in chapters),
             sum(len(l["aufgaben"]) for c in chapters for l in c["lektionen"]),
             len(items), bildzahl, len(uebung),
             len(out["erkennen"].get("klassen", [])), os.path.getsize(path)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
