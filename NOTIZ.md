Segelflug 2.8 — ein Modus, der nur fragt: Was ist das für eine Wolke?

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

**81 Fotoplätze in zwölf Klassen**, 59 Dateien neu dazu (die
siebenundzwanzig aus den Lektionen werden mitbenutzt, nicht ein zweites
Mal geholt):

| Klasse | Fotos | heißt |
|---|---|---|
| Cumulus humilis | 10 | schwache Thermik |
| Cumulus mediocris | 6 | der Tag trägt |
| Cumulus congestus | 8 | Überentwicklung |
| Cumulonimbus | 7 | Gewitter |
| Wolkenstraße | 4 | Strecke geradeaus |
| Stratocumulus | 7 | schirmt ab |
| Altocumulus castellanus | 4 | Überentwicklung |
| Lenticularis | 9 | Welle |
| Altocumulus | 6 | schirmt ab |
| Cirrus | 8 | Warmfront |
| Cirrostratus | 6 | Warmfront |
| Stratus | 6 | kein Flugwetter |

Gesucht hat `tools/sammeln.py` (Commons-Kategorien, Unterkategorien,
Volltextsuche), ausgewählt habe ich mit den Augen: Aus den Kandidaten
wurden Kontaktbögen gezeichnet, und jedes Bild, bei dem man selbst zögert,
ist für eine Erkennungsübung ein schlechtes Bild. Von rund fünfhundert
Kandidaten sind einundachtzig geblieben. Draußen geblieben sind
Satelliten- und Flugzeugbilder (so sieht niemand Wolken vom Platz aus),
Sonnenuntergänge (die Farbe verrät mehr als die Form), Nachtbilder und
alles mit Masten und Leitungen quer durchs Bild.

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

* **N9 / N950:** `segelflug_2.8_armel.deb` (4,4 MB)
* **Sailfish OS:** `harbour-segelflug-1.14.0-1.aarch64.rpm` bzw. `…armv7hl.rpm`

Das Harmattan-Binär und die Lehrer-Oberfläche mussten neu gebaut werden:
Der Modus steckt in `Erkennen.{h,cpp}` und in `Course`, nicht im Kurs.
Die anderen drei Kurse tragen keinen Schlüssel `erkennen` — dort bleibt
die Taste weg.
