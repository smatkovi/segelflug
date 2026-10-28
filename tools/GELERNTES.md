# gelerntes.bin — was die App dazugelernt hat

Das Faltungsnetz in `data/modell.bin` ist fest; weitertrainiert wird auf
dem Gerät nur seine **letzte Schicht**, und dazu kommt ein Gedächtnis.
Beides lebt in einer zweiten, kleinen Datei, die der Leser mitnehmen kann:
`gelerntes.bin`. Sie enthält die Fotos, die er deuten ließ, samt der Klasse,
auf die sich Claude und er geeinigt haben — und aus diesen Beispielen wird
das Urteil des Netzes für **neue** Fotos besser (gemessen, unten).

Dieses Blatt ist der Vertrag zwischen `Nachlernen.cpp` (beide Bäume) und
`training/nachlernen_versuch.py`. Wer eine Seite ändert, ändert zuerst hier.

## Warum nur die letzte Schicht

Rückwärtsrechnung durch 53 Faltungsschichten braucht Gradienten, Speicher
und Minuten — auf einer N950 mit 50 MB freiem Speicher gibt es das nicht.
Gelernt wird darum im **Merkmalsraum**: Die 1280 Zahlen, die das Netz vor
seiner letzten Schicht ausgibt (der `mittel`-Tensor, siehe `MODELL.md`),
sind der Fingerabdruck eines Bildes. Ähnliche Himmel liegen dort nah
beieinander, auch wenn die letzte Schicht sie verwechselt. Die letzte
Schicht selbst ist klein (17 920 Gewichte) und lässt sich auf einem
Telefon in Sekunden nachtrainieren.

Zu jedem gemerkten Foto wird dieser Abdruck gespeichert. Daraus werden zwei
Dinge: die nachtrainierte letzte Schicht, und je Klasse das Mittel der
Abdrücke, mit dem ein neues Foto verglichen wird — 14 Skalarprodukte über
1280 Zahlen, also nichts.

**Der Fachbegriff ist nicht „Reinforcement Learning".** Dort lernt ein
System aus einer Belohnung, die es sich durch Ausprobieren selbst holt.
Hier gibt Claude eine **Klasse** vor, also eine Beschriftung: Das ist
Lernen mit Lehrer (Destillation), und das braucht viel weniger Beispiele
als Lernen aus Belohnung. Für die App ist das der Glücksfall — fünfzig
Fotos genügen, fünfzigtausend hätte niemand.

## Was gemerkt wird

Nur, worauf sich **zwei Stimmen einigen**: Claudes Urteil und der eigene
Tipp des Lesers. Das halbiert die Zahl der Einträge und verdoppelt ihren
Wert (gemessen, siehe unten). Weichen sie voneinander ab, merkt die App von
sich aus nichts; der Leser kann dann ausdrücklich entscheiden, wessen
Urteil gespeichert wird.

Dazu kommt, was der Leser selbst richtigstellt („das war doch ein
Stratocumulus") — das ist die stärkste Stimme und wird immer gemerkt.

Auf Wunsch zählt Claude allein: Mit dem Schalter „Von Claude lernen,
unabhängig von meinem Tipp" (Gelerntes-Seite) merkt die App Claudes Klasse
von selbst, sobald er seine Sicherheit mit „hoch" angibt — auch gegen den
eigenen Tipp (Quelle 1; stimmen beide überein, bleibt es Quelle 0). Die
Schwelle „hoch" ist bewusst gesetzt: Ein Lehrer mit 80 % Trefferquote hat
dem Netz im Versuch kaum geholfen (Tabelle unten), bei „hoch" liegt Claude
deutlich über seinem Mittel. Bei „mittel" und „niedrig" bleibt es beim
ausdrücklichen Knopf. Der Lehrer ist seit 2.15 Fable (claude-fable-5-1),
mit Rückfall auf Opus (claude-opus-5), wenn Fable nicht verfügbar ist;
welches Modell geantwortet hat, steht in jeder Karte (`modell`); das Urteil
kommt als structured output nach Schema (seit 2.16, Fable lehnt erzwungene
Werkzeugwahl ab). Von selbst
gemerkt wird nur, was Fable gesagt hat — auch die Übereinstimmung mit dem
eigenen Tipp; antwortet Opus, bleibt es beim Knopf „Claude glauben".

## Datei

    "WOLKENG1"            8 Byte Kennung
    uint32 LE             Länge N des Kopfes in Byte
    N Byte                Kopf, JSON (UTF-8)
    Einträge              hintereinander, Aufbau unten

Der Kopf:

```json
{
  "format": 2,
  "klassen": ["cu-humilis", "...", "kondensstreifen"],
  "modell": "a3f1c0…",
  "abdruck": 1280,
  "eintraege": 47,
  "geschrieben": "2026-10-27"
}
```

`klassen` ist die Klassenliste des Netzes, mit dem die Abdrücke gerechnet
wurden; `modell` ihr Fingerabdruck (SHA-1 über den Gewichtsblob von
`modell.bin`, als Hexadezimalzahl). Beim Laden gilt:

- **Gleiche Klassenliste, gleicher Fingerabdruck:** Die Abdrücke werden
  übernommen, nichts wird gerechnet.
- **Gleiche Klassenliste, anderer Fingerabdruck** (neue Fassung der App):
  Die Abdrücke sind wertlos, aber jeder Eintrag trägt sein Bild mit — die
  App rechnet sie beim ersten Start mit dem neuen Netz neu und schreibt die
  Datei zurück. Darum ist sie übertragbar, auch über Fassungen hinweg.
- **Andere Klassenliste:** Nur die Einträge, deren Klasse die neue Liste
  kennt, werden übernommen; die anderen bleiben in der Datei stehen und
  werden übersprungen (eine spätere Fassung mag sie wieder kennen).

Ein Eintrag:

    uint16 LE   Länge der Kennung der Klasse in Byte
    …           die Kennung (UTF-8, z.B. "stratocumulus")
    uint8       Quelle: 0 = beide einig, 1 = Claude allein,
                        2 = Leser allein (Richtigstellung)
    uint8       Sicherheit, die Claude genannt hat: 0 keine,
                        1 niedrig, 2 mittel, 3 hoch
    int64 LE    Zeitpunkt (Unix-Sekunden, UTC)
    uint32 LE   Länge des Bildes in Byte
    …           das Bild: JPEG, genau eingabe × eingabe, RGB — der Puffer,
                den das Netz gesehen hat (gestaucht, nicht beschnitten)
    uint8       1 = Abdruck folgt, 0 = keiner (dann wird er gerechnet)
    …           bei 1: abdruck × int8, dazu float32 LE Maßstab und
                float32 LE Länge; der Abdruck ist auf Länge 1 normiert,
                dann mit 127/max|x| quantisiert; die Länge ist die vor dem
                Normieren (das Nachtrainieren braucht sie, siehe unten)

Die Bildkante steht nicht im Kopf; sie ist die des gespeicherten JPEGs
(die Eingabekante des Netzes, mit dem gemerkt wurde).

**Fassungen.** `format` 2 ist die oben beschriebene. Fassung 1 (Segelflug
2.11, Sailfish 1.18.x) schrieb den Abdruck ohne die Länge; die App liest
sie weiterhin, verwirft dabei aber die Abdrücke und rechnet sie aus den
Bildern nach, wie bei einem neuen Netz — beim nächsten Schreiben ist die
Datei Fassung 2. Eine höhere Fassung als 2 wird abgelehnt, nicht geraten.

Ein Eintrag ist damit etwa 10 kB (JPEG Güte 85) plus 1,3 kB Abdruck. 50
gemerkte Fotos sind eine halbe Megabyte — klein genug für die 2-GB-Partition
der N950 und für den Versand per Mail.

Die Datei liegt neben dem Fortschritt (`fortschritt.json`), also auf
Sailfish in `~/.local/share/harbour-segelflug/harbour-segelflug/`, auf
Harmattan in `~/.config/segelflug/`. Übertragen wird sie, indem man sie
kopiert; die App bietet dafür „Gelerntes sichern" (nach Dokumente bzw.
MyDocs) und „Gelerntes laden" an, und beim Laden werden Einträge
**zusammengeführt**, nicht ersetzt — zwei Geräte lassen sich so vereinen.
Doppelte Einträge erkennt sie am Bild (gleiche Bytes) und behält einen.

**Was in der Datei steht, sind Bilder.** Klein (160 × 160), aber es sind
die Fotos des Lesers. Wer die Datei weitergibt, gibt sie mit. Die App sagt
das beim Sichern, und auf der Seite „Gelerntes" ist jeder Eintrag zu sehen
und einzeln zu löschen.

## Die Korrektur

Zwei Stufen, beide gemessen (unten), zusammen das Beste.

### 1. Die letzte Schicht nachtrainieren — das Netz wird wirklich besser

Die letzte Schicht des Netzes (`linear`, 1280 × 14 = 17 920 Gewichte) wird
auf den gemerkten Abdrücken weitertrainiert: Start bei der ausgelieferten
Schicht, 200 Schritte Gradientenabstieg mit Lernrate 1, dazu ein Zug von
0,01 zurück zur ausgelieferten Schicht gegen das Auswendiglernen. Gerechnet
wird auf den **normierten** Abdrücken; die ausgelieferte Schicht erwartet
die rohen, zehn- bis zwanzigmal so langen, und wird dafür einmal mit der
mittleren Länge der gemerkten Abdrücke skaliert (darum steht die Länge in
der Datei). Ein paar hundert Matrixprodukte — auf dem Jolla eine Sekunde,
auf der N950 mehrere, darum in einem Arbeitsfaden, nach jeder Änderung.

**Erst ab 40 Einträgen.** Darunter lernt die Schicht die Irrtümer des
Lehrers mit (bei 50 Einträgen und einem 80-%-Lehrer im Versuch noch leicht
negativ, ab 80 deutlich positiv).

Die neue Schicht ersetzt die Wahrscheinlichkeiten des Netzes; das Netz
selbst in `modell.bin` bleibt, wie es ist.

### 2. Das Gedächtnis darüber

Für ein neues Foto mit Abdruck `x` (normiert) und Wahrscheinlichkeiten `p`
(aus der nachtrainierten Schicht, sonst aus dem Netz):

1. Je Klasse `c`, zu der Einträge vorliegen: `ähnlich[c]` = Kosinus
   zwischen `x` und dem normierten Mittel der Abdrücke dieser Klasse.
   Klassen ohne Einträge: `ähnlich[c] = -1`.
2. `p_gedächtnis = softmax(8 · ähnlich)`.
3. `w = n / (n + 30)`, wobei `n` die Zahl aller Einträge ist.
4. `p_neu = (1 − w) · p + w · p_gedächtnis`, daraus die Reihenfolge.

**Unter 20 Einträgen bleibt die Korrektur aus** — so wenige Beispiele sind
Rauschen, und im Versuch haben sie das Ergebnis eher verschlechtert. Die
Seite sagt dann, wie viele noch fehlen.

Die Konstanten (8, 30, 20; 40, 200, 1, 0,01) stehen in `Nachlernen.cpp` an
einer Stelle und sind in `training/nachlernen_versuch.py` dieselben; wer
sie ändert, misst vorher.

## Was es bringt — gemessen

`training/nachlernen_versuch.py` spielt es auf den 136 kuratierten Fotos
durch, mit einem Modell, das keines davon im Training hatte (58,8 % Top-1).
Der Lehrer ist nicht unfehlbar; weil Claudes Trefferquote auf diesen
Bildern nicht bekannt ist (kein Schlüssel auf dem Rechner), wird sie
durchgespielt, und falsche Lehrerangaben folgen der Verwechslungsmatrix des
Netzes — also genau den Fehlern, die ein Lehrer wirklich macht.

Alles merken, was Claude sagt:

| Lehrer | 30 gemerkt | 50 gemerkt | 80 gemerkt |
|---|---|---|---|
| 100 % | +3,9 | +6,5 | +9,1 |
| 90 % | +2,0 | +3,3 | +5,7 |
| 80 % | +0,4 | +3,0 | +2,3 |
| 70 % | −1,0 | +0,5 | +1,9 |

Nur merken, was Claude und der Leser gleich sehen (Leser 60 % richtig):

| Lehrer | 25 gemerkt | 40 gemerkt | 55 gemerkt |
|---|---|---|---|
| 80 % | +1,5 | +1,8 | +6,7 |
| 70 % | −0,1 | +0,9 | +4,4 |

Je Eintrag ist der gefilterte Weg deutlich besser: 52 gefilterte Einträge
bei einem 70-%-Lehrer bringen +4,4, während 50 ungefilterte nur +0,5
bringen. Dafür braucht es doppelt so viele gedeutete Fotos — was im
Gebrauch kein Verlust ist, weil der Leser ohnehin weiterfotografiert.

Die letzte Schicht nachtrainieren, allein und zusammen mit dem Gedächtnis
(„beides"), Lehrer 90 % und 80 %, gemessen auf neuen Fotos, die nicht
gemerkt wurden:

| | 50 gemerkt | 79 gemerkt | 109 gemerkt |
|---|---|---|---|
| nur Gedächtnis, Lehrer 90 % | +2,6 | +3,5 | +5,4 |
| nur Schicht, Lehrer 90 % | +2,9 | +4,7 | +8,5 |
| **beides, Lehrer 90 %** | **+4,3** | **+7,7** | **+12,6** |
| nur Gedächtnis, Lehrer 80 % | +1,6 | +2,5 | +1,7 |
| nur Schicht, Lehrer 80 % | −0,9 | +2,6 | +1,1 |
| **beides, Lehrer 80 %** | **+0,3** | **+4,6** | **+3,7** |

Das Nachtrainieren verdoppelt den Gewinn des Gedächtnisses, sobald genug
Einträge da sind, und bleibt bei wenigen darunter — darum die Schwelle 40.
Ein erster Lauf mit den rohen, unnormierten Abdrücken fiel um bis zu 40
Punkte: dieselbe Lernrate war für kurze Abdrücke zu klein und für lange so
groß, dass der Abstieg auseinanderflog. Darum die Normierung.

Zum Vergleich getestet und verworfen: Ähnlichkeit über die k nächsten
Nachbarn statt über das Klassenmittel (durchweg 1–3 Punkte schlechter), und
eine Korrektur, die nur Klassen mit Einträgen anhebt (schützt bei wenigen
Fotos nicht besser, verschenkt aber bei vielen 3 Punkte).
