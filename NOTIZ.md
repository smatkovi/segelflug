Segelflug 2.10 — ein Modus, der nur fragt: Was ist das für eine Wolke?

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

**134 Fotos in zwölf Klassen**, 113 Dateien eigens dafür; die
siebenundzwanzig aus den Lektionen werden mitbenutzt, nicht ein zweites
Mal geholt:

| Klasse | Fotos | heißt |
|---|---|---|
| Cumulus humilis | 15 | schwache Thermik |
| Cumulus mediocris | 11 | der Tag trägt |
| Cumulus congestus | 13 | Überentwicklung |
| Cumulonimbus | 14 | Gewitter |
| Wolkenstraße | 3 | Strecke geradeaus |
| Stratocumulus | 9 | schirmt ab |
| Altocumulus castellanus | 2 | Überentwicklung |
| Lenticularis | 22 | Welle |
| Altocumulus | 9 | schirmt ab |
| Cirrus | 20 | Warmfront |
| Cirrostratus | 7 | Warmfront |
| Stratus | 9 | kein Flugwetter |

2.9 hatte 153. Der Nutzer war sich nicht sicher, ob die Bezeichnungen
stimmen, und er hatte recht, nachzufragen: Beim zweiten Durchgang —
klassenweise, in größerer Ansicht, mit der Frage „würde ein Meteorologe
das unterschreiben?“ — flogen **neunzehn** wieder raus und **drei**
wechselten die Klasse. Die Muster dahinter:

* **Zu groß für seine Klasse.** Drei „humilis“ waren schon mediocris,
  zwei „mediocris“ und ein Cumulonimbus ohne Amboss waren congestus. Die
  Grenze zwischen den Cumulus-Stufen ist genau das, was der Modus lehren
  soll — ein Bild auf der falschen Seite der Grenze lehrt das Gegenteil.
* **Blau zwischen den Haufen.** Zwei „Stratocumulus“ zeigten verstreute
  Cumulus mit viel Himmel dazwischen; zwei weitere eine Frontwolkenbank am
  Horizont. Stratocumulus heißt: eine Schicht, kaum Lücken.
* **Die falsche Höhe.** Die beiden „Wolkenstraßen“ aus Monterrey sind
  fächerförmige Cirrus-Bänder, die zum Horizont zusammenlaufen — ja, in
  Reihen, aber ohne einen einzigen Cumulus darunter, und damit ohne das
  Steigen, um das es geht. Eines davon war seit 2.8 das **Lektionsfoto**;
  jetzt steht dort ein Bild mit niedrigen Rollen in Reihen.
* **Zu wenig zu sehen.** Dämmerung, Zinnen ohne Zinnen, ein Cirrus unter
  „Cirrostratus“, ein Zwilling derselben Minute.

Zwei Klassen sind danach sehr dünn: Wolkenstraße drei, Castellanus zwei.
Von beiden gibt es auf Commons kaum brauchbare Bodenaufnahmen; die
Kandidaten, die noch da wären, hätten den Fehler wiederholt. Lieber zwei
richtige als zehn, bei denen die Übung das Falsche beibringt.

**Eine Runde sind zwanzig Bilder**, reihum über die Klassen gemischt.
Wer mehr will, tippt noch einmal; im Menü (Sailfish) bzw. unter der Taste
(N9) steht der ganze Stapel.

Gesucht hat `tools/sammeln.py` — Commons-Kategorien, deren
Unterkategorien, Volltextsuche und, wo nötig, eine Liste von Titeln.
Ausgewählt wurde mit den Augen über Kontaktbögen. Draußen geblieben sind
Satelliten- und Flugzeugbilder (darunter ein ganzer Schwung
Apollo-Aufnahmen, die in der Congestus-Kategorie liegen), Sonnenuntergänge
(die Farbe verrät mehr als die Form), Nachtbilder und alles mit Masten und
Leitungen quer durchs Bild.

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

* **N9 / N950:** `segelflug_2.10_armel.deb` (6,7 MB)
* **Sailfish OS:** `harbour-segelflug-1.16.0-1.aarch64.rpm` bzw. `…armv7hl.rpm`

Das Harmattan-Binär und die Lehrer-Oberfläche mussten neu gebaut werden:
Der Modus steckt in `Erkennen.{h,cpp}` und in `Course`, nicht im Kurs.
Die anderen drei Kurse tragen keinen Schlüssel `erkennen` — dort bleibt
die Taste weg.
