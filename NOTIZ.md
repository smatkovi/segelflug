Segelflug 2.12 — ein eigenes Foto vom Himmel, und die App lernt daraus

Bis 2.10 kamen alle Wolken aus dem Paket: gezeichnet in den Lektionen,
fotografiert im Erkennungsmodus. Jetzt geht es andersherum: Ein Foto, das
man gerade selbst gemacht hat (oder eines aus der Galerie), wird im Gerät
eingeordnet — ohne Netz — und bekommt dazu, was es fürs Segelfliegen
heißt. Wer mag, holt sich als zweites Urteil Claude dazu; beide bleiben
nebeneinander stehen.

**Erst der eigene Tipp.** Das Netz ist meist schon fertig, bevor man die
Ratetafel gelesen hat; stünde sein Ergebnis da, tippte niemand mehr selbst.
Also bleibt es verborgen, bis ein Tipp steht (oder „Weiß nicht“), und erst
dann erscheinen die drei wahrscheinlichsten Klassen mit Prozentbalken, die
Bedeutung für den Tag beim ersten, und aufklappbar, woran man es erkennt.

## Das Netz

MobileNetV2 (ImageNet-vortrainiert), Eingabe 160 × 160, 14 Klassen: die
zwölf Übungsklassen ohne Wolkenstraße und Castellanus, dazu Altostratus,
Nimbostratus, Cirrocumulus und Kondensstreifen — die vier haben jetzt auch
Bedeutungstexte im Kurs. Die Gewichte liegen als int8 je Ausgabekanal in
`data/modell.bin` (2,35 MB; Format in `tools/MODELL.md`), gerechnet wird in
`Klassifizierer.cpp` ohne jede Fremdbibliothek, aus demselben Text für Qt 4.7
und Qt 5. Auf dem Jolla dauert ein Bild 97 ms; die N950 ist noch nicht
gemessen.

**Woher die Bilder kommen.** CCSN v2 (Harvard Dataverse, CC0; 2543 Bilder
in elf Klassen, „Cu“ als weiches Ziel auf humilis/mediocris/congestus),
die unkuratierten Wikimedia-Commons-Kandidaten aus der Sammlung für den
Erkennungsmodus (etwa 1500), und die 136 kuratierten Kursfotos.

**Wie gut es ist — ehrlich gemessen.** Fünffache Kreuzprobe über die 136
kuratierten Fotos (jedes genau einmal geprüft, nie im eigenen Training):

| | Top-1 | Top-3 |
|---|---|---|
| gesamt (136) | 64 % | 90 % |
| Cirrus (20) | 95 % | 100 % |
| Lenticularis (22) | 82 % | 100 % |
| Altocumulus (12) | 75 % | 100 % |
| Cumulonimbus (14) | 71 % | 100 % |
| Cu mediocris (11) | 55 % | 91 % |
| Cu congestus (13) | 46 % | 100 % |
| Stratus (9) | 44 % | 89 % |
| Cu humilis (15) | 40 % | 87 % |
| Cirrostratus (7) | 29 % | 43 % |
| Stratocumulus (10) | 10 % | 40 % |

Die Cumulus-Stufen verwechselt es untereinander (das ist auch für Menschen
die schwere Frage), Stratocumulus hält es für Altocumulus. Darum zeigt die
Seite drei Klassen, nicht eine, und darum gibt es den zweiten Blick.

**Was beim Training schiefging.** Das erste Rezept — alle Gewichte, Lernrate
2·10⁻⁴, dreißig Epochen — war nach der ersten Epoche am besten (54 %) und
wurde dann schlechter, während es auf zurückgehaltenen CCSN-Bildern besser
wurde: Es lernte die CCSN-Bilder (256 px, beschnittene Webfotos) auswendig
und verlor die Verteilung der Handyfotos. Geholfen hat: frühe Blöcke
eingefroren, Rückgrat mit kleiner Lernrate, Mixup, stärkere Augmentierung,
die Commons- und Kursfotos häufiger gezogen, und die Kursfotos per
Kreuzprobe mit ins Training (`training/train.py`).

## Der zweite Blick

„Claude fragen“ schickt das Foto (auf 1024 px verkleinert) mit der
Klassenliste an die Anthropic-API (claude-sonnet-5) und bekommt Kennung,
Sicherheit und zwei Sätze Begründung zurück — in der Sprache der App. Der
Schlüssel wird auf der Seite eingetragen und neben dem Fortschritt
gespeichert (0600); auf den Nokias wird er aus `~/.profile` übernommen. Auf
Sailfish geht die Anfrage über QNetworkAccessManager, auf Harmattan (Qt
4.7, TLS zu alt) über den wget-Helfer aus wunderw — der Schlüssel steht nie
in argv, sondern in einer wgetrc, die nur `WGETRC` benennt. Geprüft gegen
einen Scheinserver (`tests/scheinserver.py`): Kopfzeilen, Rumpf, Fehlerfall
401, Abbruch. Live noch nicht: Hier auf dem Jolla gibt es keinen Schlüssel,
und die N950 war nicht erreichbar.

## So gelingt das Foto

Sechs Hinweise stehen auf der Seite, solange kein Foto gewählt ist: Sonne
im Rücken, Wolke ganz ins Bild mit Basis und Oberseite, schräg nach oben
statt in den Zenit, auf die Wolke belichten, nicht durch Scheiben, bei
Tageslicht.

## Neue Lektion: Tagesverläufe

Acht Verläufe, wie ein Flugtag laufen kann — der klassische Cumulus-Tag,
Blauthermik, Überentwicklung, Zumachen, Fronttag, Rückseitenwetter, Welle,
Hochnebel — jeweils Morgen, Vormittag, Nachmittag, Abend und die
Entscheidung für den Piloten; am Ende eine Tafel „Was ich um 9 Uhr sehe“.
Mit einer Zeichnung (vier Verläufe × vier Uhrzeiten) und vier Fotos.

## Dazulernen

Wer Claude fragt, bringt der App etwas bei. Stimmen Claudes Urteil und der
eigene Tipp überein, merkt sie sich das Foto; gehen sie auseinander,
entscheidet der Leser, wessen Urteil gelernt wird. Dazu kommt
„Es ist etwas anderes" — die eigene Richtigstellung, die immer zählt.

**Das Faltungsnetz bleibt, die letzte Schicht lernt.** Rückwärtsrechnung
durch 53 Faltungsschichten gibt es auf einer N950 nicht; die letzte Schicht
aber ist klein (17 920 Gewichte) und wird ab 40 gemerkten Fotos auf dem
Gerät nachtrainiert — in einem Arbeitsfaden, in Sekunden. Dazu kommt ein
Gedächtnis: Die 1280 Zahlen vor der letzten Schicht sind der Fingerabdruck
eines Bildes, und die App vergleicht ein neues Foto mit dem Mittel der
gemerkten Abdrücke je Klasse. Das Format steht in `tools/GELERNTES.md`.

Der Fachbegriff ist nicht „Reinforcement Learning". Dort lernt ein System
aus einer Belohnung, die es sich selbst holt. Hier gibt Claude eine Klasse
vor, also eine Beschriftung: Lernen mit Lehrer. Das ist der Glücksfall —
fünfzig Fotos genügen, fünfzigtausend hätte niemand.

**Was es bringt, gemessen** (`training/nachlernen_versuch.py`, auf den 136
kuratierten Fotos mit einem Modell, das keines davon im Training hatte;
Claudes Trefferquote ist hier nicht bekannt, also durchgespielt):

| Lehrer trifft | 50 gemerkt | 79 gemerkt | 109 gemerkt |
|---|---|---|---|
| 90 %, nur Gedächtnis | +2,6 | +3,5 | +5,4 |
| 90 %, Gedächtnis und nachtrainierte Schicht | **+4,3** | **+7,7** | **+12,6** |
| 80 %, nur Gedächtnis | +1,6 | +2,5 | +1,7 |
| 80 %, Gedächtnis und nachtrainierte Schicht | **+0,3** | **+4,6** | **+3,7** |

Gemessen auf Fotos, die **nicht** gemerkt wurden — es geht um das Erkennen
neuer Fotos, nicht um das Wiedererkennen alter. Das Nachtrainieren der
letzten Schicht verdoppelt den Gewinn des Gedächtnisses, sobald genug
Einträge da sind; darunter lernt es die Irrtümer des Lehrers mit, darum die
Schwelle 40. Nur zu merken, worauf sich Claude und der Leser einigen,
halbiert die Zahl der Einträge und verdoppelt ihren Wert. Unter zwanzig
Einträgen bleibt jede Korrektur aus — so wenige sind Rauschen.

**Die Datei ist übertragbar.** `gelerntes.bin` trägt zu jedem Eintrag das
160-Pixel-Bild mit, das das Netz gesehen hat. Darum kann eine spätere
Fassung der App die Fingerabdrücke mit ihrem eigenen Netz neu rechnen, und
zwei Geräte lassen sich zusammenführen (geladen wird dazu, nicht ersetzt;
Doppelte erkennt sie am Bild). „Sichern" legt sie nach MyDocs bzw.
Dokumente. Was drin ist, sind Fotos — klein, aber Fotos; wer die Datei
weitergibt, gibt sie mit, und die App sagt das beim Sichern.

Auf der Seite „Gelerntes" steht jeder Eintrag mit Bild, Klasse und Quelle
und lässt sich einzeln löschen.

## Glossar

Alle Fachwörter der App mit Definition: 98 Stichwörter von Abschirmung bis
Wolkenstraße, jedes mit zwei bis fünf Sätzen, Verweisen auf verwandte
Begriffe und, wo es hilft, einer Zeichnung. Im Lektionstext ist jedes Wort
beim ersten Vorkommen verlinkt.

## Prüfungen

- `c-lehrer/tools/build-klassifizierertest.sh`: Winzigmodell aus reinem
  Python nachgerechnet (Δ 5·10⁻⁸), kaputte Dateien scheitern sauber,
  EXIF-Drehung.
- `training/vergleichen.py` gegen 33 Referenzpuffer des echten Modells:
  max |Δ Logit| 2·10⁻⁵.
- `training/stauchung_pruefen.py` prüft die andere Hälfte des Weges — Datei
  öffnen, EXIF, Stauchen —, die die Referenzpuffer auslassen: der C++-Prüfstand
  auf dem Jolla und der Python-Weg auf arch über dieselben 134 kuratierten
  Fotos. Top-1 gleich bei 128 (95,5 %), beide Wege 112 richtig; die sechs
  Abweichungen sind knappe Entscheidungen (größte Abweichung der
  Top-1-Wahrscheinlichkeit 0,064, verschiedene JPEG-Dekoder und die
  Zwischenstufe auf 640 Pixel). Die 64 % gelten also für die App, nicht nur
  für das Training.
- `c-lehrer/tools/build-onlinedeutertest.sh`: „alles gut“.
- `harbour-lehrer/tools/qml-laden.sh`: 23 QML-Dateien, 0 Fehler (Methodenaufrufe prüft es nicht — siehe Kamera unten).
- `c-lehrer/tools/build-nachlernentest.sh`: Datei schreiben und lesen,
  Korrektur, Modellwechsel, unbekannte Klassen, zwei Geräte zusammenführen,
  kaputte Dateien — „alles gut".
- Harmattan: Cross-Build mit GCC 14 gegen Qt 4.7 fehlerfrei, und zum ersten
  Mal laden alle QML-Seiten **gegen das echte Qt 4.7 samt com.nokia.meego**
  — die ARM-Binärdatei läuft dafür unter qemu mit dem MADDE-Sysroot
  (`c-lehrer/tools/qml-pruefen-qemu.sh`, 24 Dateien, 0 Fehler). Auf dem
  Gerät selbst noch nicht gestartet (N950 nicht erreichbar).

## Was die Gegenprüfung gefunden hat

Drei Prüfläufe über den neuen Code (Qt-4.7-Verträglichkeit, Numerik und
Speicher, Schlüssel und Privatsphäre). Die wichtigsten Funde, alle behoben:

- **Text aus der Antwort wurde als Auszeichnung gedeutet.** Qt zeigt Text
  ohne `textFormat` als AutoText; ein `<img src="http://…">` in Claudes
  Begründung wäre wirklich abgeholt worden — ein zweiter Weg nach draußen
  neben der einen Anfrage. Jetzt steht überall `Text.PlainText`.
- **Das Foto wäre auf Harmattan unsichtbar gewesen.** Qt 4.7.4 gibt
  `sourceSize.height` als 0 zurück, wenn nur die Breite gesetzt ist — der
  Rahmen wäre 0 Pixel hoch. Jetzt ein fester Kasten im Verhältnis 4:3.
- Hochkant geschossene Fotos lagen in der Anzeige quer, obwohl das Netz sie
  gedreht sah: Qt 4 dreht QML-Bilder nicht nach EXIF. Die Seite dreht jetzt
  selbst.
- Ein falscher Schlüssel meldete „Keine Verbindung (6)" statt „Schlüssel?" —
  wget nennt eine abgelehnte Beglaubigung mit 6, nicht mit 8.
- Die Umgebungsvariablen für Adresse und Hilfsprogramm waren auch in der
  ausgelieferten App wirksam; sie stehen jetzt hinter einem Baukennzeichen,
  das nur der Prüfstand setzt.
- Schlüssel- und Rumpfdatei lagen in `/tmp` und wurden nur vom Destruktor
  weggeräumt; stirbt die App dazwischen, blieb der Schlüssel liegen. Jetzt
  feste Namen im eigenen Ordner, 0600, und der nächste Lauf überschreibt.
- Der Hilfsprozess erbte `ANTHROPIC_API_KEY` aus der Umgebung; er bekommt
  sie jetzt ohne.
- Zwei Fotos nacheinander starteten zwei Netzdurchläufe nebeneinander — auf
  der N950 ein Speichertod. Jetzt wartet das zweite.
- Der EXIF-Leser konnte bei einem Versatz nahe 2³² über den Puffer hinaus
  lesen.

Nach 1.19.0 noch vier, darum 1.19.1:

- **Die Gelerntes-Datei aus 1.18.x wäre verworfen worden.** 1.18.0 und 1.18.1
  schrieben die Einträge noch ohne die Abdrucklänge, unter derselben
  Formatnummer; 1.19.0 hätte sie als kaputt gemeldet, alles vergessen und die
  Datei beim nächsten Merken überschrieben. Auf dem Jolla lag genau so eine
  Datei (zwei Einträge). Jetzt schreibt die App Fassung 2, liest Fassung 1
  weiter und rechnet deren Abdrücke aus den gespeicherten Bildern nach
  (`GELERNTES.md`, „Fassungen"; Test im Nachlernen-Prüfstand, auch gegen die
  echte Gerätedatei).
- **„Sichern" schrieb auf Sailfish ins Leere.** Sailjail zeigte der App
  `~/Documents` nicht (nur `Internet;Pictures;Camera` erlaubt), also fiel die
  Datei in die Wurzel des Sandkasten-Home. Jetzt `Documents` dazu.
- **Der Lernfaden las im lebenden Gedächtnis.** Er hielt Zeiger auf die
  Abdrücke, während die Oberfläche „Vergessen" oder ein neues Foto
  zulassen konnte. Jetzt zieht er im Oberflächenfaden eine Abschrift
  (`Nachlernen::Lernstoff`) und rechnet nur darauf.
- **Die Kamera stellte auf Tippen nicht scharf.** Der Nutzer hat es auf dem
  Jolla bestätigt. Drei Prüfer am Quelltext des Sailfish-Forks von
  QtMultimedia und von gst-droid haben die Ursache gefunden: Die Seite rief
  `exposure.isMeteringModeSupported()` auf, und die Methode gibt es im
  QML-Typ nicht — der TypeError brach die Funktion ab, bevor
  `searchAndLock()` kam. Der Hinweis „die Belichtung ist gesetzt" war nur
  Text; eine eigene Belichtungsstelle kennt der Fork gar nicht, die
  Messfläche kommt über die Fokusregion mit (gst-droid setzt daraus
  focus-areas und metering-areas). Dazu zwei Dinge, die auch nach dem Abbruch
  falsch gewesen wären: der Tipp-Punkt muss wie in der Jolla-Kamera um
  `camera.orientation` in die Sensorlage gedreht werden (dafür QtMultimedia
  5.4), und ein Rückfall auf `FocusPointAuto` setzt die Messfläche mit
  zurück. Die neue Seite: kann die Kamera `FocusInfinity`, bleibt die Schärfe
  im Unendlichen (Wolken liegen dort, und ein Kontrast-Autofokus auf weichen
  Rändern scheitert oft) und der Tipp setzt nur die Messfläche; sonst der
  Weg der Jolla-Kamera mit Auto-Fokus und eigenem Punkt. Unter dem Hinweis
  steht in Worten, was die Kamera tut, samt Sucherquelle und Sensorlage. Am
  Gerät noch nicht bestätigt — das kann nur der Nutzer; die Prüfung mit
  `qml-laden.sh` sieht fehlende Methoden nicht, weil sie erst zur Laufzeit
  aufgelöst werden.

## Nachtrag 2.13 / 1.19.2: „Antwort nicht lesbar"

Der Nutzer bekam bei „Claude fragen" manchmal „Antwort nicht lesbar" — nicht
immer, am selben Morgen hatte es zweimal funktioniert. Die App bat um „JSON
only" und suchte dann im Text nach der ersten `{` und der letzten `}`; kam
Prosa, ein halbes Objekt (400 Token Platz waren knapp) oder ein erfundenes
Wort für die Sicherheit, blieb nichts übrig. Jetzt stellt die Anfrage ein
Werkzeug `urteil` mit Schema (Klasse aus der Liste, Sicherheit hoch, mittel
oder niedrig, Begründung) und erzwingt den Aufruf mit `tool_choice`; die API
liefert die Eingabe als geprüftes JSON-Objekt. Der alte Textweg bleibt als
Rückfall. Platz 800 Token. Lässt sich eine Antwort trotzdem nicht deuten,
nennt die Meldung ihren Anfang („abgeschnitten", „leer" oder die ersten
Wörter) und der Rumpf liegt unter `letzte-antwort.json` im Datenordner der
App zum Nachlesen. Scheinserver und Prüfstand kennen die vier Fälle
(Werkzeug, Text, Prosa, abgeschnitten) — „alles gut".

Dazu auf Sailfish: „Foto wählen" zeigte keine Bilder. Der Bildwähler
(`Sailfish.Pickers`) liest den Tracker-Index, und dafür braucht die App das
Sailjail-Recht `MediaIndexing`; `Pictures` allein gibt nur den Ordner frei.
Jetzt `MediaIndexing` und `RemovableMedia` (Speicherkarte) in der
Desktop-Datei, wie bei Fernschreiber und Sag's Wien.

## Pakete

- MeeGo Harmattan (N9/N950): `segelflug_2.13_armel.deb` (2.12 ohne den Nachtrag)
- Sailfish OS: `harbour-segelflug-1.19.2-1.{aarch64,armv7hl}.rpm` (1.19.1 ohne den Nachtrag)
