#!/bin/sh
# Nachschub fuer die duennen Klassen -- dort, wo die Kategorie allein
# nicht genug hergibt.
#
# Stratus: die Kategorie "Stratus clouds" ist zur Haelfte eine einzige
# Autofahrt durch Nevada. Auf Deutsch heisst dieselbe Wolke Hochnebel,
# und darunter liegt ganz anderes Material.
# Wolkenstrasse: es gibt keine brauchbare Kategorie, nur Suchen.
cd "$(dirname "$0")/.." || exit 1
G=${GRENZE:-60}
tools/sammeln.py --klasse stratus-hochnebel --suche 'Hochnebel'                    --grenze "$G"
tools/sammeln.py --klasse stratus-neb       --suche 'intitle:"Stratus nebulosus"'  --grenze "$G"
tools/sammeln.py --klasse strasse-roll      --suche 'horizontal convective rolls clouds' --grenze "$G"
tools/sammeln.py --klasse strasse-such      --suche 'intitle:"cloud street"'       --grenze "$G"
tools/sammeln.py --klasse cast-such         --suche 'intitle:castellanus'          --grenze "$G"
tools/sammeln.py --klasse med-such          --suche 'intitle:"Cumulus mediocris"'  --grenze "$G"
