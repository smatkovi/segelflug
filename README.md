# Segelflug

Theorie für den **Segelflug- und PPL-Schein**, deutsch oder englisch, auf dem
Nokia N9 und N950 (MeeGo 1.2 Harmattan) und auf Sailfish OS.

Zehn Kapitel, 23 Lektionen: Aerodynamik und Flugmechanik, Flugleistung und
Flugplanung, Luftrecht nach EASA, Navigation, menschliches
Leistungsvermögen, Technik und Instrumente, Verfahren und Notfälle,
Sprechfunk — und als Schwerpunkt sieben Lektionen **Wolken lesen**: was
Cumulus, Stratocumulus, Lenticularis, Cumulonimbus und die Bewölkung einer
Kaltfront über Thermik, Streckenflug und Sicherheit verraten.

Die Sprache lässt sich jederzeit umschalten; Kurstexte, Aufgaben und
Begriffe liegen zweisprachig vor.

## Die Wolkenbilder

Alle neun Wolkenbilder sind gezeichnet, nicht fotografiert
(`tools/clouds.py`, Pillow). Die Wolkenbasis wird dabei **ausgeschnitten**
statt hell unterlegt — eine unterlegte Basis sieht auf dem OLED des N9 wie
Dunst aus, ein sauberer Schnitt wie eine Basis.

## Wie das gebaut ist

Das Programm ist [C-Lehrer](https://github.com/smatkovi/c-lehrer)
beziehungsweise dessen Sailfish-Fassung
[harbour-lehrer](https://github.com/smatkovi/harbour-lehrer), unverändert:
Die App liest ihren ganzen Kurs aus `data/kurs.json` und weiß nichts vom
Thema. Ein zweiter Kurs ist deshalb ein zweites Paket, kein zweites Programm.

Dieses Repo ist der Kurs:

```
kurs.py            Kapitel, Lektionen, Aufgaben, beides zweisprachig
tools/make-kurs.py schreibt data/kurs.json
tools/clouds.py    zeichnet bilder/*.png
tools/build-deb.sh packt das Harmattan-.deb
```

Die richtige Antwort steht beim Schreiben immer vorne; `make-kurs.py` mischt
deterministisch und zählt danach nach, damit kein Muster entsteht.

## Bauen

```sh
python3 tools/clouds.py          # Wolkenbilder zeichnen
python3 tools/make-kurs.py       # data/kurs.json erzeugen
tools/build-deb.sh 1.5           # braucht ~/ps/c-lehrer/build/c-lehrer
```

Die Sailfish-RPMs entstehen im Baum von `harbour-lehrer`
(`cmake -DKURS=segelflug`), wo `kurs.json` und die Bilder als
`kurse/segelflug/` liegen.

## Installieren

* **N9 / N950:** `dpkg -i segelflug_1.5_armel.deb`
* **Sailfish OS:** `pkcon install-local harbour-segelflug-1.0.0-1.<arch>.rpm`

Die Pakete für beide Systeme hängen an den
[Releases](https://github.com/smatkovi/segelflug/releases).

## Kein Ersatz für die Schulung

Der Kurs deckt den Theoriestoff ab, ersetzt aber weder die Ausbildung noch
die amtlichen Fragenkataloge.
