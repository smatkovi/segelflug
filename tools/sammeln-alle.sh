#!/bin/sh
# Alle Klassen des Erkennungsmodus einsammeln (siehe tools/sammeln.py).
#
# Die Namen sind nachgeprueft: "Category:Stratocumulus" und "Category:Cirrus"
# sind auf Commons leer -- die Bilder liegen in "... clouds". Und fuer die
# Wolkenstrasse gibt es gar keine brauchbare Kategorie ("Cloud streets" ist
# leer, "Cloud Street, Austral" ist eine Wohnstrasse), also eine Suche.
cd "$(dirname "$0")/.." || exit 1
set -- \
  "cu-humilis:Cumulus humilis clouds" \
  "cu-mediocris:Cumulus mediocris clouds" \
  "cu-congestus:Cumulus congestus clouds" \
  "cumulonimbus:Cumulonimbus incus" \
  "stratocumulus:Stratocumulus clouds" \
  "ac-castellanus:Altocumulus castellanus clouds" \
  "ac-lenticularis:Altocumulus lenticularis clouds" \
  "altocumulus:Altocumulus clouds" \
  "cirrus:Cirrus uncinus clouds" \
  "cirrostratus:Cirrostratus clouds" \
  "stratus:Stratus clouds"
for paar in "$@"; do
  klasse=${paar%%:*}; kat=${paar#*:}
  echo "== $klasse"
  tools/sammeln.py --klasse "$klasse" --kategorie "$kat" --grenze "${GRENZE:-40}" || echo "  FEHLER"
done
echo "== wolkenstrasse"
tools/sammeln.py --klasse wolkenstrasse --suche 'intitle:"cloud streets"' \
                 --grenze "${GRENZE:-40}" || echo "  FEHLER"
