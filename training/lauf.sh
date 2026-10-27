#!/bin/bash
# Der ganze Ablauf auf arch, in tmux: messen -> saeubern -> (erneut messen)
# -> Endmodell -> Export.  Marker FERTIG am Ende, FEHLER bei Abbruch.
set -u
cd "$(dirname "$0")/.." || exit 1
T=training
rm -f $T/FERTIG $T/FEHLER
P="python3 -u"
{
  echo "== Messlauf 1 $(date)"
  $P $T/train.py messen --ausgabe $T/messen1.pt || { touch $T/FEHLER; exit 1; }
  N=$(wc -l < $T/messen1.pt.saeubern.txt)
  BESTES=$T/messen1.pt
  if [ "$N" -gt 50 ]; then
    echo "== Saeuberung: $N Kandidaten raus, Messlauf 2 $(date)"
    cut -f1 $T/messen1.pt.saeubern.txt > $T/ausschluss.txt
    $P $T/train.py messen --ausgabe $T/messen2.pt --ausschluss $T/ausschluss.txt || { touch $T/FEHLER; exit 1; }
    BESTES=$T/messen2.pt
    AUSSCHLUSS="--ausschluss $T/ausschluss.txt"
  else
    echo "== Saeuberung: nur $N verdaechtig, bleibt"
    AUSSCHLUSS=""
  fi
  E=$(python3 -c "import json;print(json.load(open('$BESTES.json'))['beste_epoche'])")
  echo "== Endmodell mit $E Epochen $(date)"
  $P $T/train.py endmodell --epochen "$E" --ausgabe $T/endmodell.pt $AUSSCHLUSS || { touch $T/FEHLER; exit 1; }
  echo "== Export $(date)"
  $P $T/export.py $T/endmodell.pt --ausgabe $T/modell.bin --referenz $T/referenz || { touch $T/FEHLER; exit 1; }
  echo "== Fertig $(date)"
} 2>&1 | tee $T/lauf.log
touch $T/FERTIG
