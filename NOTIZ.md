Segelflug 2.9 — ein Modus, der nur fragt: Was ist das für eine Wolke?

Bis 2.7 standen die Fotos unter den Zeichnungen, unter der Überschrift der
Wolke, die sie zeigen. Das erklärt gut und übt nichts: Wer unter
„Cumulus humilis“ drei Bilder von Cumulus humilis sieht, hat nichts zu
entscheiden. Am Himmel steht aber keine Überschrift.

**Der neue Modus dreht es um.** Ein Foto, sonst nichts auf der Seite, und
zwei Fragen dazu:

1. **Was für eine Wolke ist das?** Zur Auswahl stehen vier — und zwar
   nicht irgendwelche, sondern die, mit denen diese wirklich verwechselt
   wird (`verwechselt` in `erkennen.py`). Zwischen Cirrus und Stratus zu
   unterscheiden übt niemand; zwischen mediocris und congestus hängt der
   Tag davon ab.
2. **Und was heißt sie fürs Segelfliegen?** Hier ist die Auswahl immer
   dieselbe kurze Liste von neun Bedeutungen — von „schwache Thermik“ über
   „Welle“ bis „schirmt ab“. Das hält die Autorenarbeit bei den zwölf
   Klassen statt bei den einundachtzig Fotos.

Nach jedem Tipp steht da, woran man es hätte sehen können, und erst dann
geht es weiter. Bei der Einstufung wäre das falsch — dort wird gemessen —,
hier ist es der ganze Zweck.

Am Ende: wie viele Wolken erkannt, wie viele Bedeutungen gewusst, und
welche Klassen danebengingen, jede mit dem Satz, woran sie zu erkennen
gewesen wäre.

## Die Bilder

**153 Fotos in zwölf Klassen** (2.8 hatte 81), 131 Dateien eigens dafür;
die siebenundzwanzig aus den Lektionen werden mitbenutzt, nicht ein
zweites Mal geholt:

| Klasse | Fotos | heißt |
|---|---|---|
| Cumulus humilis | 18 | schwache Thermik |
| Cumulus mediocris | 14 | der Tag trägt |
| Cumulus congestus | 12 | Überentwicklung |
| Cumulonimbus | 16 | Gewitter |
| Wolkenstraße | 5 | Strecke geradeaus |
| Stratocumulus | 13 | schirmt ab |
| Altocumulus castellanus | 3 | Überentwicklung |
| Lenticularis | 22 | Welle |
| Altocumulus | 10 | schirmt ab |
| Cirrus | 19 | Warmfront |
| Cirrostratus | 9 | Warmfront |
| Stratus | 12 | kein Flugwetter |

Zwei Klassen bleiben dünn, und das ist keine Nachlässigkeit: Von einer
**Wolkenstraße** gibt es auf Commons fast nur Satellitenbilder — vom Boden
aus fotografiert sie kaum jemand, weil man sie dort erst erkennt, wenn man
weiß, wonach man sucht. Und **Altocumulus castellanus** ist selbst am
Himmel selten und wird meist falsch beschriftet; von fünfzig Kandidaten
blieben drei. Lieber drei richtige als zehn, bei denen die Übung das
Falsche beibringt.

**Eine Runde sind zwanzig Bilder**, reihum über die Klassen gemischt.
Hundertdreiundfünfzig Bilder mal zwei Fragen wären vierhundert Antworten
am Stück; wer mehr will, tippt noch einmal, und im Menü (Sailfish) bzw.
unter der Taste (N9) steht der ganze Stapel.

Gesucht hat `tools/sammeln.py` — Commons-Kategorien, deren
Unterkategorien, Volltextsuche und, wo nötig, eine Liste von Titeln.
Ausgewählt habe ich mit den Augen: Aus den Kandidaten werden Kontaktbögen
gezeichnet, und jedes Bild, bei dem man selbst zögert, ist für eine
Erkennungsübung ein schlechtes Bild. Aus rund tausend Kandidaten sind
hundertdreiundfünfzig geblieben. Draußen geblieben sind Satelliten- und
Flugzeugbilder (so sieht niemand Wolken vom Platz aus) — darunter ein
ganzer Schwung Apollo-Aufnahmen, die in der Congestus-Kategorie liegen —,
Sonnenuntergänge (die Farbe verrät mehr als die Form), Nachtbilder und
alles mit Masten und Leitungen quer durchs Bild.

Zwei Dinge, die beim Hinsehen auffielen und ohne das Hinsehen falsch
gelernt worden wären: ein Floccus-Feld unter „castellanus“, wo der
Erklärsatz von Türmchen spricht, und ein Strandbild unter „Altocumulus“.
Beide sitzen jetzt richtig oder gar nicht.

## Ein Fehler, der nur beim Hinsehen auffällt

Unter „Wolkenstraßen“ stand seit 2.6 ein Foto aus der Commons-Kategorie
**„Cloud Street, Austral“** — und das ist eine Wohnstraße namens Cloud
Street in New South Wales. Ausgewählt nach dem Dateinamen, nie angesehen.
Jetzt steht dort eine wirkliche Wolkenstraße, und der Kontaktbogen über
alle siebenundzwanzig Lektionsfotos ist der Grund, warum es aufgefallen
ist.

## Prüfungen

* `c-lehrer/tools/build-erkennentest.sh` — der Ablauf ohne Gerät: dass die
  richtige Antwort wandert statt vorne zu stehen, dass die verwechselbare
  Wolke zur Wahl steht, dass nicht zwei Bilder derselben Klasse
  hintereinander kommen.
* `segelflug/bin/segelflug --qml-pruefen` — **am Gerät**, ohne Fenster:
  jede QML-Datei einmal übersetzen. Der Prüfer auf dem Rechner kennt
  `com.nokia.meego` nicht, und gerade dessen Fallen fallen sonst erst beim
  Antippen auf. 19 Dateien, 0 Fehler.
* `harbour-lehrer/tools/qml-laden.sh` — dasselbe für Silica: 18 Dateien,
  0 Fehler.

Nicht geprüft: wie es aussieht. Das N950 hängt hinter dem Sicherheitscode,
und der gehört nicht mir.

## Pakete

* **N9 / N950:** `segelflug_2.9_armel.deb` (7,3 MB)
* **Sailfish OS:** `harbour-segelflug-1.15.0-1.aarch64.rpm` bzw. `…armv7hl.rpm`

Das Harmattan-Binär und die Lehrer-Oberfläche mussten neu gebaut werden:
Der Modus steckt in `Erkennen.{h,cpp}` und in `Course`, nicht im Kurs.
Die anderen drei Kurse tragen keinen Schlüssel `erkennen` — dort bleibt
die Taste weg.
