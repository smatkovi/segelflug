# Wolkennetz trainieren

Rechnet auf arch (GPU) in `~/wolken-train/`, dort liegen `ccsn/`, `kandidaten/`,
`bilder/`; dieser Ordner wird nach `~/wolken-train/training/` gespielt:

    rsync -av ~/ps/segelflug/training/ arch:~/wolken-train/training/
    ssh arch 'tmux new -d -s wolken ~/wolken-train/training/lauf.sh'

`lauf.sh` erledigt alles und legt am Ende `training/FERTIG` an (`FEHLER` bei
Abbruch); Verlauf in `training/lauf.log`.

- `daten.py` — Klassen (Reihenfolge = MODELL.md), Quellen und Zuordnung,
  Vorverarbeitung (stauchen auf 160×160, ImageNet-Normierung). Leck-Schutz:
  Kandidaten mit kuratiertem Commons-Titel fliegen beim Messen raus. Dieselbe
  md5-Datei in mehreren Ordnern: Ziele gemittelt. `cast-such` → altocumulus,
  `med-such` → cu-mediocris, `stratus-*` → stratus, `strasse*` weg.
- `train.py messen` — MobileNetV2 (ImageNet-Start), 3 Epochen nur Kopf, dann
  30 Epochen alles (AdamW 2e-4, Cosine, Batch 64), Ziehen ~ 1/√Häufigkeit,
  weiche Ziele + Glättung 0.05. Prüfmenge = kuratierte Bilder (+ 10 % CCSN
  der vier Klassen ohne kuratierte Bilder). Schreibt `<ausgabe>.json`
  (Genauigkeiten, Verwechslungsmatrix, beste Epoche) und
  `<ausgabe>.saeubern.txt` (Kandidaten, die das Netz mit > 0,9 anders sieht).
- `train.py endmodell --epochen N` — alle Bilder inkl. kuratierte, N = beste
  Epoche des Messlaufs.
- `export.py` — BatchNorm einfalten, int8 je Ausgabekanal, `modell.bin` nach
  MODELL.md schreiben, mit numpy zurücklesen und prüfen, Genauigkeit der Datei
  gegen das Float-Modell, `referenz/*.rgb` + `referenz.json`.
- `vergleichen.py referenz/ --pruefstand ./klassifizierertest modell.bin` —
  C++-Logits gegen die Referenz, bestanden bei max |Δ| < 0,01.
- `stauchung_pruefen.py` — die erste Hälfte des Weges (Datei öffnen, EXIF,
  Stauchen), die die Referenzpuffer auslassen: `--pruefstand BIN modell.bin
  aus.json` auf dem Telefon, `--python modell.bin aus.json` hier, dann
  `--vergleich a.json b.json`; bestanden ab 95 % gleicher Top-1-Klasse über
  die kuratierten Fotos (27.10.2026: 95,5 %, beide Wege gleich treffsicher).

Ergebnis zurück: `modell.bin` → `segelflug/data/modell.bin`, `referenz/` und
`*.log` hierher (beide gitignored).
