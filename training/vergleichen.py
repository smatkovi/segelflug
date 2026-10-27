# -*- coding: utf-8 -*-
"""Logits des C++-Pruefstands gegen referenz/referenz.json stellen.

  python3 training/vergleichen.py referenz/ --pruefstand ./klassifizierertest modell.bin
      ruft fuer jede Referenz `<pruefstand> modell.bin referenz/<name>.rgb`
      auf und liest 14 Zeilen Logits von dessen Standardausgabe.
  python3 training/vergleichen.py referenz/ --ausgaben ORDNER
      liest statt dessen ORDNER/<name>.txt (14 Zeilen je Datei).

Bestanden, wenn max |Delta| < 0.01 ueber alle Referenzen (Rueckgabe 0)."""

import argparse
import json
import os
import subprocess
import sys

SCHWELLE = 0.01


def logits_aus_text(text, name):
    # Der Pruefstand nennt vor den Logits den Dateinamen; alles, was keine
    # Zahl ist, wird ueberlesen.
    werte = []
    for z in text.split():
        try:
            werte.append(float(z))
        except ValueError:
            pass
    if len(werte) != 14:
        raise SystemExit("%s: %d statt 14 Werte" % (name, len(werte)))
    return werte


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("referenz")
    p.add_argument("--pruefstand", nargs=2, metavar=("PROGRAMM", "MODELL"))
    p.add_argument("--ausgaben")
    args = p.parse_args()
    if not args.pruefstand and not args.ausgaben:
        p.error("--pruefstand oder --ausgaben angeben")

    with open(os.path.join(args.referenz, "referenz.json")) as f:
        referenz = json.load(f)
    schlimmste = 0.0
    fehler = 0
    for name, eintrag in sorted(referenz.items()):
        if args.pruefstand:
            lauf = subprocess.run([args.pruefstand[0], args.pruefstand[1],
                                   os.path.join(args.referenz, name)],
                                  capture_output=True, text=True)
            if lauf.returncode != 0:
                print("%s: Pruefstand scheiterte: %s" % (name, lauf.stderr.strip()))
                fehler += 1
                continue
            werte = logits_aus_text(lauf.stdout, name)
        else:
            with open(os.path.join(args.ausgaben, name[:-4] + ".txt")) as f:
                werte = logits_aus_text(f.read(), name)
        delta = max(abs(a - b) for a, b in zip(werte, eintrag["logits"]))
        schlimmste = max(schlimmste, delta)
        treffer = max(range(14), key=lambda i: werte[i]) == max(range(14), key=lambda i: eintrag["logits"][i])
        print("%-28s max|Delta| %.5f  %s" % (name, delta, "" if treffer else "TOP-1 WEICHT AB"))
    print("Gesamt: max|Delta| %.5f  %s" % (schlimmste, "bestanden" if schlimmste < SCHWELLE and not fehler else "DURCHGEFALLEN"))
    sys.exit(0 if schlimmste < SCHWELLE and not fehler else 1)


if __name__ == "__main__":
    main()
