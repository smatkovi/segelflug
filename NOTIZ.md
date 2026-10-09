Segelflug 2.7 — unter jeder Zeichnung steht jetzt der wirkliche Himmel

Die Zeichnungen bleiben, wo sie sind, und bleiben das Hauptbild: Sie zeigen
das Merkmal und sonst nichts. Genau das ist aber auch ihre Grenze. Am
Himmel steht das Merkmal nie allein, sondern zwischen Dunst, Gegenlicht,
drei Wolkenstockwerken übereinander und einem Baum im Weg — und wer nur die
Zeichnung kennt, erkennt die Wolke im Bild wieder, nicht draußen.

**Unter jeder der neun Zeichnungen stehen deshalb zwei bis drei Fotos
derselben Wolke**, und zu jedem Foto ein Satz, der sagt, wohin zu schauen
ist. Ohne den Satz wäre es ein hübscher Himmel; mit ihm ist es eine Übung:

* **Cumulus humilis:** dass alle Basen auf derselben Höhe liegen — das ist
  die Kondensationshöhe, kein Zeichenfehler.
* **Lebenslauf:** harte Ränder gegen ausgefranste. Dasselbe Bildpaar, das
  im Text „wachsend“ und „zerfallend“ heißt, einmal fotografiert.
* **Congestus:** höher als breit, Ränder noch scharf — noch kein Eis.
* **Cumulonimbus:** der Amboss von weitem, und der Regenschauer unter der
  Basis von nahem.
* **Stratocumulus:** wie aus Haufen Schicht wird und der Tag zumacht.
* **Wolkenstraße:** von unten die Reihe, von oben (Satellit) das Muster.
* **Castellanus:** die Türmchen, an denen die Warnung hängt.
* **Cirrus:** die Haken, und der 22°-Ring, wenn daraus eine Schicht wird.
* **Lenticularis:** ortsfest über dem Berg, und dieselbe Linse aus dem
  Segelflugzeug.

Cumulonimbus und Lenticularis sind in keiner Lektion das Bild, werden aber
in einer besprochen; ihre Fotos hängen deshalb an „Wenn es zu gut läuft“
und an „Wolkenstraßen und Wellen“.

## Woher die Fotos kommen

Von Wikimedia Commons, 27 Stück, jedes frei lizenziert (CC BY, CC BY-SA,
gemeinfrei). Urheber und Lizenz stehen **unter jedem Bild in der App** und
noch einmal in `CREDITS` — beide Lizenzen verlangen das. `tools/fotos.py`
prüft das vor dem Holen und bricht ab, statt ein Bild ohne Urheber oder
unter GFDL stillschweigend mitzunehmen.

Geholt wird auf 640 Punkte Breite und höchstens 520 Punkte Höhe, als JPEG
mit Qualität 82: 1,1 MB für siebenundzwanzig Fotos. Ohne die Höhengrenze
stünde ein Hochformat 850 Punkte hoch auf einem 854 Punkte hohen
Bildschirm, und die Zeichnung darüber liefe aus dem Bild.

## Auch bei den Aufgaben

Nicht nur in den Lektionen: Jede Aufgabe und jede Karteikarte, die eine
Zeichnung führt, zeigt die Fotos **zweimal** — über der Frage neben der
Zeichnung, wo sie beim Nachdenken helfen, und noch einmal in der Lösung,
wo nach der Antwort Zeit ist, wirklich hinzusehen. Verraten wird damit
nichts, was die Zeichnung über der Frage nicht schon zeigt. Vierzehn der
neunundvierzig Aufgaben haben eine Zeichnung, macht zweiundvierzig
Fotoplätze.

## Pakete

* **N9 / N950:** `segelflug_2.7_armel.deb`
* **Sailfish OS:** `harbour-segelflug-1.13.0-1.aarch64.rpm` bzw. `…armv7hl.rpm`

Die Oberfläche dafür liegt in C-Lehrer und harbour-lehrer (`Foto.qml`,
`Fotos.qml`); das Harmattan-Binär musste neu gebaut werden, weil die
Lektion ihre Felder einzeln durchreicht und `fotos` dazugekommen ist.
