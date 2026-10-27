# data/modell.bin — das Wolkennetz im Paket

Ein Faltungsnetz (MobileNetV2 1.0, Eingabe 160×160), das ein Himmelsfoto
einer von 14 Wolkenklassen zuordnet. Trainiert wird auf arch
(`segelflug/training/`), gerechnet wird in der App ohne Fremdbibliothek
(`c-lehrer/src/Klassifizierer.cpp`, derselbe Text in `harbour-lehrer/src`).
Dieses Blatt ist der Vertrag zwischen beiden: Wer eine Seite ändert,
ändert zuerst hier.

## Datei

    "WOLKEN01"            8 Byte Kennung
    uint32 LE             Länge N des Kopfes in Byte
    N Byte                Kopf, JSON (UTF-8), ohne Nullbyte
    Blob                  die Gewichte, Offsets im Kopf zählen ab hier (Byte 12+N)

Der Blob beginnt an einer durch 4 teilbaren Dateiposition — der Exporter
polstert den Kopf mit Leerzeichen auf. Jeder Tensor im Blob beginnt an
einem durch 4 teilbaren Offset.

## Kopf

```json
{
  "format": 1,
  "eingabe": 160,
  "mittel":   [0.485, 0.456, 0.406],
  "streuung": [0.229, 0.224, 0.225],
  "klassen": ["cu-humilis", "cu-mediocris", "cu-congestus", "cumulonimbus",
              "stratocumulus", "stratus", "nimbostratus", "altocumulus",
              "ac-lenticularis", "altostratus", "cirrus", "cirrostratus",
              "cirrocumulus", "kondensstreifen"],
  "bytes": 2344240,
  "schichten": [ ... ]
}
```

`klassen` ist die Reihenfolge der Ausgabe; die App ordnet den Kurs-Einträgen
über die Kennung zu, nicht über die Stelle. `bytes` ist die Länge des Blobs
(Prüfung beim Laden). `mittel`/`streuung` sind die ImageNet-Werte, in RGB.

## Vorverarbeitung (gilt für Training, Export und App gleich)

1. Das ganze Bild auf `eingabe`×`eingabe` **stauchen**, nicht beschneiden —
   der Rand eines Himmelsfotos gehört dazu. Gestaucht wird durch
   **Flächenmittelung** (`QImage::scaled` mit `Qt::SmoothTransformation`,
   in Python `Image.BOX`), nicht bilinear: PILs BILINEAR glättet stärker,
   und auf 2 von 33 Referenzbildern kamen die beiden Wege zu verschiedenen
   Klassen.
2. RGB, Werte 0..255 → `x/255`, dann je Kanal `(x - mittel[c]) / streuung[c]`.
3. Tensor 0 = Eingabe, Layout **CHW** float32, Index `c*E*E + y*E + x`.

Im Training werden Ausschnitte gezogen (RandomResizedCrop mit kleiner
Mindestfläche), beim Prüfen wird nur gestaucht — genau wie in der App.

## Schichten

Der Graph ist flach: Schicht `i` (ab 0) erzeugt Tensor `i+1`. Jede Schicht
nennt ihre Quelle(n) als Tensorindex. Arten:

### `conv`

```json
{"art": "conv", "quelle": 0,
 "ein": 3, "aus": 32, "kern": 3, "schritt": 2, "rand": 1, "gruppen": 1,
 "relu6": true,
 "gewichte": 0, "skalen": 896, "bias": 1024}
```

- Faltung mit symmetrischem Rand `rand` (torchvision: `(kern-1)/2`), Schrittweite
  `schritt`, `gruppen` Gruppen (`gruppen == ein == aus` ist die tiefenweise
  Faltung). Keine Dilatation.
- BatchNorm ist **eingefaltet**: `gewichte` und `bias` sind schon die
  Werte nach der Faltung von Gamma/Beta/Mittel/Varianz (eps 1e-5).
- `gewichte`: int8, Layout `[aus][ein/gruppen][kern][kern]`, zeilenweise.
- `skalen`: float32 `[aus]`, symmetrische Quantisierung je Ausgabekanal:
  `w = q * skalen[o]`, `skalen[o] = max|w[o]| / 127`.
- `bias`: float32 `[aus]`.
- `relu6`: nach Faltung + Bias `min(max(x,0),6)`; bei `false` nichts
  (die Projektion im Block ist linear).

### `add`

```json
{"art": "add", "quellen": [5, 8]}
```

Elementweise Summe zweier gleich großer Tensoren (der Rest-Pfad der
InvertedResidual-Blöcke).

### `mittel`

```json
{"art": "mittel", "quelle": 52}
```

Mittel über die Fläche je Kanal: aus `[C][H][W]` wird `[C]`.

### `linear`

```json
{"art": "linear", "quelle": 53, "ein": 1280, "aus": 14,
 "gewichte": 3480000, "skalen": 3497920, "bias": 3497976}
```

`gewichte` int8 `[aus][ein]`, `skalen` und `bias` float32 `[aus]`, gleiche
Quantisierung wie bei `conv`. Ausgabe sind die Logits; die App rechnet
Softmax selbst.

Das Dropout aus dem Training kommt nicht in die Datei.

## Speicher auf dem Gerät

Die N950 hat oft nur 50 MB frei. Die App hält die dequantisierten Gewichte
als float32 — bei diesem Modell 8,8 MB plus 0,1 MB Bias und Skalen — und
gibt Zwischentensoren frei, sobald keine spätere Schicht sie mehr nennt
(Letztverwendung aus dem Graphen berechnen). Der größte Zwischentensor ist
96×80×80 float = 2,4 MB; gemessen braucht die Rechnung rund 17 MB über dem
Grundbedarf der App.

## Prüfung gegen die Referenz

Der Exporter legt neben `modell.bin` den Ordner `referenz/` an:

- `referenz/<name>.rgb`: die gestauchte 160×160-Eingabe als rohe Bytes,
  **HWC**, RGB, 76 800 Byte, genau der Puffer, den das Netz gesehen hat.
- `referenz/referenz.json`: `{"<name>.rgb": {"datei": "...", "klasse": "...",
  "logits": [14 float]}}`, gerechnet mit dem **dequantisierten** Modell in
  float32, damit nur die Rechenreihenfolge abweichen kann.

`c-lehrer/tools/build-klassifizierertest.sh` baut den Prüfstand lokal; er
liest `modell.bin` und ein `.rgb`, gibt die Logits aus, und
`training/vergleichen.py` vergleicht: `max |Δ| < 0.01` über alle Referenzen
ist bestanden.

Die Referenzpuffer beginnen beim fertigen 160-px-Bild. Den Weg davor — Datei
öffnen, EXIF-Drehung, Stauchen — prüft `training/stauchung_pruefen.py`
getrennt: derselbe Prüfstand mit `--bild` über die kuratierten Fotos auf dem
Gerät, der Python-Weg (`daten.eingabe`) auf dem Rechner, bestanden ab 95 %
gleicher Top-1-Klasse. Ganz gleich werden die beiden nie (andere
JPEG-Dekoder, in der App eine Zwischenstufe auf 640 Pixel); gemessen sind
95,5 % bei gleicher Trefferzahl.

## Klassen und ihre Quellen

| Kennung           | CCSN v2 | Commons-Kandidaten (`kandidaten/<ordner>`) |
|-------------------|---------|---------------------------------------------|
| cu-humilis        | Cu (⅓)  | cu-humilis                                  |
| cu-mediocris      | Cu (⅓)  | cu-mediocris                                |
| cu-congestus      | Cu (⅓)  | cu-congestus                                |
| cumulonimbus      | Cb      | cumulonimbus                                |
| stratocumulus     | Sc      | stratocumulus                               |
| stratus           | St      | stratus                                     |
| nimbostratus      | Ns      | —                                           |
| altocumulus       | Ac      | altocumulus, ac-castellanus                 |
| ac-lenticularis   | —       | ac-lenticularis                             |
| altostratus       | As      | —                                           |
| cirrus            | Ci      | cirrus                                      |
| cirrostratus      | Cs      | cirrostratus                                |
| cirrocumulus      | Cc      | —                                           |
| kondensstreifen   | Ct      | —                                           |

`wolkenstrasse` aus den Kandidaten wird nicht trainiert (drei Bilder, und
die Reihen sieht man auf einem Handyfoto ohnehin nicht). CCSN "Cu" ist
nicht nach Humilis/Mediocris/Congestus getrennt und bekommt ein weiches
Ziel von je ⅓.

Prüfmenge: die kuratierten Bilder des Kurses (`bilder/erkennen.json` und
`bilder/fotos.json`, Zuordnung über den Commons-Titel). Dieselben Titel
werden beim Messen aus den Kandidaten ausgeschlossen; das ausgelieferte
Modell wird danach noch einmal auf allem trainiert.
