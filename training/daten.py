# -*- coding: utf-8 -*-
"""Datenbestand fuer das Wolkennetz: Trainings- und Pruefmenge zusammenstellen.

Alles, was train.py und export.py gemeinsam brauchen, steht hier, damit die
Vorverarbeitung beim Pruefen, beim Export und bei den Referenzpuffern
garantiert dieselbe ist (MODELL.md: stauchen, nicht beschneiden).

Laeuft auf arch in ~/wolken-train/ (Wurzel = Elternordner dieses Skripts)."""

import glob
import hashlib
import json
import os
import random

import numpy as np
from PIL import Image, ImageOps

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EINGABE = 160
MITTEL = [0.485, 0.456, 0.406]
STREUUNG = [0.229, 0.224, 0.225]

# Die Reihenfolge ist der Vertrag (MODELL.md), nicht aendern.
KLASSEN = ["cu-humilis", "cu-mediocris", "cu-congestus", "cumulonimbus",
           "stratocumulus", "stratus", "nimbostratus", "altocumulus",
           "ac-lenticularis", "altostratus", "cirrus", "cirrostratus",
           "cirrocumulus", "kondensstreifen"]
INDEX = {k: i for i, k in enumerate(KLASSEN)}
CUMULUS = ["cu-humilis", "cu-mediocris", "cu-congestus"]

# CCSN-Kuerzel -> Kennung; Cu bekommt ein weiches Ziel ueber drei Stufen.
CCSN = {"Ac": "altocumulus", "As": "altostratus", "Cb": "cumulonimbus",
        "Cc": "cirrocumulus", "Ci": "cirrus", "Cs": "cirrostratus",
        "Ct": "kondensstreifen", "Cu": "cu-zyklus", "Ns": "nimbostratus",
        "Sc": "stratocumulus", "St": "stratus"}

# Kandidatenordner -> Kennung.  Die "-such"-Ordner sind Suchergebnisse ohne
# Kategorie und entsprechend verrauschter; die Wolkenstrassen bleiben draussen
# (MODELL.md).  None = ueberspringen.
KANDIDATEN = {
    "cu-humilis": "cu-humilis", "cu-mediocris": "cu-mediocris",
    "med-such": "cu-mediocris", "cu-congestus": "cu-congestus",
    "cumulonimbus": "cumulonimbus", "stratocumulus": "stratocumulus",
    "stratus": "stratus", "stratus-hochnebel": "stratus",
    "stratus-neb": "stratus", "altocumulus": "altocumulus",
    "ac-castellanus": "altocumulus", "cast-such": "altocumulus",
    "ac-lenticularis": "ac-lenticularis", "cirrus": "cirrus",
    "cirrostratus": "cirrostratus",
    "wolkenstrasse": None, "strasse-roll": None, "strasse-such": None,
    "strasse2": None,
}

# Schluessel aus bilder/fotos.json und erkennen.json -> Kennung.
KURATIERT = {"ac-castellanus": "altocumulus", "lenticularis": "ac-lenticularis",
             "wolkenstrasse": None, "cu-zyklus": "cu-zyklus"}

# Klassen, die nur CCSN liefert: davon halten wir beim Messen 10 % zurueck,
# sonst gaebe es fuer sie gar keine Zahl.
NUR_CCSN = ["nimbostratus", "altostratus", "cirrocumulus", "kondensstreifen"]


def ziel(kennung):
    """Zielvektor (14 Wahrscheinlichkeiten) fuer eine Kennung."""
    z = np.zeros(len(KLASSEN), dtype=np.float32)
    if kennung == "cu-zyklus":
        for k in CUMULUS:
            z[INDEX[k]] = 1.0 / 3
    else:
        z[INDEX[kennung]] = 1.0
    return z


def titel_norm(t):
    if t.startswith("File:"):
        t = t[5:]
    return t.replace("_", " ").strip()


def kuratierte_titel():
    """Commons-Titel aller kuratierten Bilder -- die duerfen beim Messen nicht
    im Training stecken."""
    titel = set()
    with open(os.path.join(WURZEL, "bilder", "erkennen.json")) as f:
        for e in json.load(f):
            titel.add(titel_norm(e["titel"]))
    with open(os.path.join(WURZEL, "bilder", "fotos.json")) as f:
        for liste in json.load(f).values():
            for e in liste:
                titel.add(titel_norm(e["titel"]))
    return titel


def pruefmenge():
    """[(pfad, kennung)] der kuratierten Bilder; kennung kann 'cu-zyklus' sein."""
    gesehen = set()
    aus = []

    def nimm(datei, klasse):
        klasse = KURATIERT.get(klasse, klasse)
        if klasse is None or datei in gesehen:
            return
        gesehen.add(datei)
        aus.append((os.path.join(WURZEL, "bilder", datei), klasse))

    with open(os.path.join(WURZEL, "bilder", "erkennen.json")) as f:
        for e in json.load(f):
            nimm(e["datei"], e["klasse"])
    with open(os.path.join(WURZEL, "bilder", "fotos.json")) as f:
        for schluessel, liste in json.load(f).items():
            for e in liste:
                nimm(e["datei"], schluessel)
    return aus


def trainingsmenge(leck_vermeiden, ausschluss=(), ccsn_rueckhalt=False, saat=1):
    """Trainingsbilder als [(pfad, zielvektor, herkunft)], herkunft in
    {"ccsn", "kandidat"}.  Dazu die zurueckgehaltenen CCSN-Bilder
    [(pfad, kennung)] der Nur-CCSN-Klassen (leer, wenn nicht verlangt).

    leck_vermeiden: Kandidaten mit kuratiertem Commons-Titel weglassen.
    ausschluss: Pfade (oder md5-Dateinamen) aus der Saeuberungsrunde."""
    ausschluss = set(os.path.basename(a) for a in ausschluss)
    zufall = random.Random(saat)
    bilder = []
    rueckhalt = []

    for kuerzel, kennung in sorted(CCSN.items()):
        pfade = sorted(glob.glob(os.path.join(WURZEL, "ccsn", "CCSN_v2", kuerzel, "*.jpg")))
        zufall.shuffle(pfade)
        if ccsn_rueckhalt and kennung in NUR_CCSN:
            n = len(pfade) // 10
            rueckhalt += [(p, kennung) for p in pfade[:n]]
            pfade = pfade[n:]
        bilder += [(p, ziel(kennung), "ccsn") for p in pfade]

    tabu = kuratierte_titel() if leck_vermeiden else set()
    # Dieselbe md5-Datei kann in mehreren Ordnern liegen: Ziele mitteln.
    je_md5 = {}
    gelecht = 0
    for ordner, kennung in KANDIDATEN.items():
        if kennung is None:
            continue
        index = os.path.join(WURZEL, "kandidaten", ordner, "index.json")
        if not os.path.exists(index):
            continue
        with open(index) as f:
            eintraege = json.load(f)["dateien"]
        for e in eintraege:
            name = os.path.basename(e["vorschaudatei"])
            pfad = os.path.join(WURZEL, "kandidaten", ordner, name)
            if not os.path.exists(pfad):
                continue
            if titel_norm(e["titel"]) in tabu:
                gelecht += 1
                continue
            if name in ausschluss:
                continue
            je_md5.setdefault(name, (pfad, []))[1].append(ziel(kennung))
    for name, (pfad, ziele) in sorted(je_md5.items()):
        bilder.append((pfad, np.mean(ziele, axis=0).astype(np.float32), "kandidat"))

    zufall.shuffle(bilder)
    return bilder, rueckhalt, gelecht


def zaehlung(bilder):
    """Weiche Bildzahl je Klasse (Summe der Zielvektoren)."""
    summe = np.zeros(len(KLASSEN))
    for _, z, _ in bilder:
        summe += z
    return summe


def bild_oeffnen(pfad):
    """RGB-PIL-Bild mit angewandter EXIF-Drehung."""
    bild = Image.open(pfad)
    bild = ImageOps.exif_transpose(bild)
    return bild.convert("RGB")


def gestaucht(bild):
    """Der Puffer, den das Netz sieht: HWC uint8, EINGABE x EINGABE.

    **Flaechenmittelung (BOX), nicht BILINEAR.** Die App staucht mit
    QImage::scaled(Qt::SmoothTransformation), und das ist beim Verkleinern
    eine Flaechenmittelung -- PILs BILINEAR glaettet staerker. Der
    Unterschied ist klein, aber gross genug: Auf 2 von 33 Referenzbildern
    kamen die beiden Wege zu verschiedenen Klassen (gemessen 27.10.2026).
    Beide Seiten rechnen jetzt dasselbe; MODELL.md sagt es auch so."""
    bild = bild.resize((EINGABE, EINGABE), Image.BOX)
    return np.asarray(bild, dtype=np.uint8)


def normalisiert(hwc):
    """HWC uint8 -> CHW float32 nach MODELL.md."""
    x = hwc.astype(np.float32) / 255.0
    x = (x - np.array(MITTEL, dtype=np.float32)) / np.array(STREUUNG, dtype=np.float32)
    return np.ascontiguousarray(x.transpose(2, 0, 1))


def eingabe(pfad):
    return normalisiert(gestaucht(bild_oeffnen(pfad)))
