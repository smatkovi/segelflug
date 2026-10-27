Segelflug 2.11 — ein eigenes Foto vom Himmel, und die App sagt, was es ist

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
| gesamt (136) | 60 % | 90 % |
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

## Prüfungen

- `c-lehrer/tools/build-klassifizierertest.sh`: Winzigmodell aus reinem
  Python nachgerechnet (Δ 5·10⁻⁸), kaputte Dateien scheitern sauber,
  EXIF-Drehung.
- `training/vergleichen.py` gegen 33 Referenzpuffer des echten Modells:
  max |Δ Logit| 2·10⁻⁵.
- `c-lehrer/tools/build-onlinedeutertest.sh`: „alles gut“.
- `harbour-lehrer/tools/qml-laden.sh`: 20 QML-Dateien, 0 Fehler.
- Harmattan: Cross-Build mit GCC 14 gegen Qt 4.7 fehlerfrei; auf dem Gerät
  noch nicht gestartet (N950 nicht erreichbar).

## Pakete

- MeeGo Harmattan (N9/N950): `segelflug_2.11_armel.deb`, 9,2 MB
- Sailfish OS: `harbour-segelflug-1.17.0-1.{aarch64,armv7hl}.rpm`
