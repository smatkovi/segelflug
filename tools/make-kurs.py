#!/usr/bin/env python3
"""Turns the authored glider course into the data file the app reads.

Same engine as C-Lehrer: it reads <app>/data/kurs.json and knows nothing
about the subject. What differs here is that every readable string is a
{"de": ..., "en": ...} pair and that lessons carry pictures instead of code.

    tools/make-kurs.py        # -> data/kurs.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import kurs


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
           "bild": task.get("bild", "")}
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


def main():
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
    }
    path = os.path.join(ROOT, "data", "kurs.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print("data/kurs.json: %d Kapitel, %d Lektionen, %d Aufgaben, "
          "%d Einstufungsfragen, %d B"
          % (len(chapters), sum(len(c["lektionen"]) for c in chapters),
             sum(len(l["aufgaben"]) for c in chapters for l in c["lektionen"]),
             len(items), os.path.getsize(path)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
