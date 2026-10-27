# -*- coding: utf-8 -*-
"""Den ganzen Weg vom Foto bis zur Klasse zwischen App und Training vergleichen.

vergleichen.py prueft nur die zweite Haelfte (fertiger 160-px-Puffer ->
Logits). Hier geht es um die erste: Datei oeffnen, EXIF-Drehung, Stauchen
auf 160 x 160. Die App macht das in C++ (Klassifizierer::bildLaden, erst auf
640 Kante, dann QImage::scaled), das Training in PIL (daten.eingabe, BOX in
einem Schritt). Stimmen die beiden nicht ueberein, gilt jede auf der
Python-Seite gemessene Genauigkeit nicht fuer die App.

  python3 training/stauchung_pruefen.py --pruefstand BIN MODELL AUS.json
      laeuft `BIN --bild MODELL foto` ueber alle kuratierten Fotos
      (daten.pruefmenge) -- auf dem Telefon oder dem Rechner, nur Qt noetig.
  python3 training/stauchung_pruefen.py --python MODELL AUS.json
      derselbe Satz ueber daten.eingabe + export.vorwaerts (braucht torch).
  python3 training/stauchung_pruefen.py --vergleich A.json B.json
      Top-1-Uebereinstimmung und groesste Abweichung der Wahrscheinlichkeit;
      bestanden ab 95 % Uebereinstimmung (Rueckgabe 0).

Jede Ausgabedatei: {datei: {"klasse": Kennung, "oben": [[klasse, p], ...]}}."""

import json
import os
import subprocess
import sys

import daten

SCHWELLE = 0.95


def pruefstand(bin_, modell, aus):
    ergebnis = {}
    for pfad, kennung in daten.pruefmenge():
        text = subprocess.run([bin_, "--bild", modell, pfad], capture_output=True,
                              text=True, check=True).stdout
        oben = []
        for zeile in text.splitlines():
            teile = zeile.split()
            if len(teile) == 3 and teile[0] in ("1.", "2.", "3."):
                oben.append([teile[1], float(teile[2])])
        if len(oben) != 3:
            raise SystemExit("%s: keine drei Raenge in:\n%s" % (pfad, text))
        ergebnis[os.path.relpath(pfad, daten.WURZEL)] = {"klasse": kennung, "oben": oben}
        sys.stderr.write(".")
    sys.stderr.write("\n")
    schreiben(aus, ergebnis)


def python(modell, aus):
    import numpy as np
    import torch
    import export
    kopf, gewichte = export.lesen(modell)
    ergebnis = {}
    for pfad, kennung in daten.pruefmenge():
        x = torch.from_numpy(daten.eingabe(pfad)[None])
        with torch.no_grad():
            lg = export.vorwaerts(kopf, gewichte, x)[0].numpy().astype(np.float64)
        p = np.exp(lg - lg.max())
        p /= p.sum()
        reihen = np.argsort(-p)[:3]
        oben = [[daten.KLASSEN[int(i)], float(p[i])] for i in reihen]
        ergebnis[os.path.relpath(pfad, daten.WURZEL)] = {"klasse": kennung, "oben": oben}
        sys.stderr.write(".")
    sys.stderr.write("\n")
    schreiben(aus, ergebnis)


def schreiben(aus, ergebnis):
    with open(aus, "w") as f:
        json.dump(ergebnis, f, indent=1, ensure_ascii=False, sort_keys=True)
    print("%d Fotos -> %s" % (len(ergebnis), aus))


def vergleich(a_pfad, b_pfad):
    with open(a_pfad) as f:
        a = json.load(f)
    with open(b_pfad) as f:
        b = json.load(f)
    gemeinsam = sorted(set(a) & set(b))
    if not gemeinsam:
        raise SystemExit("keine gemeinsamen Fotos")
    gleich = 0
    abweichung = 0.0
    anders = []
    richtig_a = richtig_b = 0
    for datei in gemeinsam:
        oa, ob = a[datei]["oben"], b[datei]["oben"]
        soll = a[datei]["klasse"]

        def trifft(klasse):
            return klasse in daten.CUMULUS if soll == "cu-zyklus" else klasse == soll

        richtig_a += trifft(oa[0][0])
        richtig_b += trifft(ob[0][0])
        if oa[0][0] == ob[0][0]:
            gleich += 1
            abweichung = max(abweichung, abs(oa[0][1] - ob[0][1]))
        else:
            anders.append((datei, oa[0], ob[0]))
    n = len(gemeinsam)
    print("%d Fotos; Top-1 gleich bei %d (%.1f %%); groesste Abweichung der "
          "Top-1-Wahrscheinlichkeit %.4f" % (n, gleich, 100.0 * gleich / n, abweichung))
    print("Top-1 richtig: A %d (%.1f %%), B %d (%.1f %%)"
          % (richtig_a, 100.0 * richtig_a / n, richtig_b, 100.0 * richtig_b / n))
    for datei, oa, ob in anders:
        print("  %s: A %s %.3f / B %s %.3f" % (datei, oa[0], oa[1], ob[0], ob[1]))
    if gleich < SCHWELLE * n:
        print("NICHT bestanden: unter %d %%" % int(100 * SCHWELLE))
        return 1
    print("bestanden")
    return 0


def main():
    a = sys.argv[1:]
    if len(a) == 4 and a[0] == "--pruefstand":
        pruefstand(a[1], a[2], a[3])
    elif len(a) == 3 and a[0] == "--python":
        python(a[1], a[2])
    elif len(a) == 3 and a[0] == "--vergleich":
        sys.exit(vergleich(a[1], a[2]))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
