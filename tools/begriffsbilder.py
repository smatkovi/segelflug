#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zeichnet die Bilder zum Glossar (bilder/begriff-*.png).

Das Glossar erklaert jedes Fachwort in zwei Saetzen. Zwei Saetze reichen
fuer eine Definition, aber nicht fuer eine Vorstellung: Wer "Rotor" liest,
weiss hinterher, dass es dreht, und nicht, wo es liegt. Genau das kann ein
Bild in einem Blick, und deshalb bekommt jeder Begriff eines, der sich
zeichnen laesst -- die Lage im Gelaende, die Abfolge am Himmel, die Kurve.

Gezeichnet wird wie in tools/skizzen.py: dunkler Grund, dieselben Farben,
dieselben Striche, 440x300 bei dreifacher Aufloesung. Die Masse sind nicht
frei waehlbar -- Bild.qml rechnet die Hoehe aus dem festen Verhaeltnis
300/440 aus, ein anderes Format passte nur mit Rand hinein.

Die Hilfsfunktionen kommen aus skizzen.py und clouds.py, damit es zweimal
dieselben Striche sind und nicht zweimal aehnliche. Beide Module werden
nur gelesen, nie geaendert, und keine vorhandene PNG wird angefasst: alles
hier heisst begriff-*.

Beschriftete Bilder gibt es zweimal, begriff-x.png und begriff-x.en.png --
die Beschriftung steckt im Bild, also braucht die englische Fassung ein
eigenes. Bilder ohne Text (die reinen Wolkenbilder) gibt es nur einmal;
Bild.qml faellt von selbst auf die deutsche Fassung zurueck.

    python3 tools/begriffsbilder.py        # -> bilder/begriff-*.png
"""
from __future__ import division

import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import clouds as wo        # noqa: E402  (erst nach sys.path)
import skizzen as sk       # noqa: E402

W, H, S = sk.W, sk.H, sk.S

GRUND = sk.GRUND
LINIE = sk.LINIE
DUENN = sk.DUENN
TEXT = sk.TEXT
BETONT = sk.BETONT
WARN = sk.WARN
GUT = sk.GUT
ROT = sk.ROT
KOERPER = sk.KOERPER

WOLKE = (226, 230, 240)          # wie die Wolken in skizze-wolkenbasis
WOLKE_SCHATTEN = (150, 158, 176)
EIS = (238, 242, 250)
ERDE = (86, 108, 68)             # clouds.GROUND, damit der Boden ueberall gleich ist
FELD = (104, 86, 58)
DUNST = (62, 66, 78)
FELS = (72, 78, 70)

BODEN_Y = 228                    # darunter ist Platz fuer die Unterschrift
TEXT_BREITE = 400                # von x=20 bis x=420


# ---------------------------------------------------------------------------
# Handgriffe
# ---------------------------------------------------------------------------

def beschrift(draw, x, y, de, en, groesse=11, farbe=TEXT, mitte=False,
              rechts=False):
    """Zweisprachiger Text. skizzen.text uebersetzt ueber seine eigene
    Tabelle; hier steht die Uebersetzung an Ort und Stelle, weil fast jedes
    Wort nur einmal vorkommt und eine zweite Tabelle nur auseinanderliefe.

    Jede Beschriftung wird nachgemessen. Die englische Fassung ist fast
    immer laenger als die deutsche, und eine Beschriftung, die rechts aus
    dem Bild laeuft, sieht man nur, wenn man genau dieses eine Bild
    anschaut -- das Messen findet sie in jedem.
    """
    inhalt = de if sk.SPRACHE == "de" else en
    breite = textbreite(inhalt, groesse)
    links = x - breite if rechts else (x - breite / 2.0 if mitte else x)
    if links < 1 or links + breite > W - 1 or y + groesse * 1.25 > H - 1:
        UEBER_RAND.append("%s: %r bei x=%d y=%d" % (sk.SPRACHE, inhalt,
                                                    int(links), int(y)))
    sk.text(draw, x, y, inhalt, groesse, farbe, mitte, rechts)


_MESSER = ImageDraw.Draw(Image.new("RGB", (4, 4)))

# Zu lange Unterschriften sammeln sich hier und brechen den Lauf am Ende ab.
# Sammeln statt sofort abbrechen: sonst findet man sie eine nach der
# anderen, und das sind bei fuenfzig Bildern fuenfzig Laeufe.
ZU_LANG = []
UEBER_RAND = []


def textbreite(inhalt, groesse):
    """Breite in Zeicheneinheiten -- die Schrift ist S-fach gross."""
    kasten = _MESSER.textbbox((0, 0), inhalt, font=sk.schrift(groesse * S))
    return (kasten[2] - kasten[0]) / float(S)


def umbrechen(inhalt, groesse, breite):
    zeilen, zeile = [], ""
    for wort in inhalt.split():
        probe = (zeile + " " + wort).strip()
        if zeile and textbreite(probe, groesse) > breite:
            zeilen.append(zeile)
            zeile = wort
        else:
            zeile = probe
    if zeile:
        zeilen.append(zeile)
    return zeilen


def unterschrift(draw, de, en, de2=None, en2=None):
    """Die ein bis drei Zeilen unter dem Bild: der Satz, den das Bild zeigt.

    Umgebrochen wird gemessen und nicht geschaetzt, und wenn es mehr als
    drei Zeilen werden, bricht der Lauf ab. Ein stillschweigend am rechten
    Rand abgeschnittener Satz faellt beim Durchsehen von hundert Bildern
    genau einmal auf -- naemlich gar nicht.
    """
    zeilen = [(z, TEXT) for z in umbrechen(
        de if sk.SPRACHE == "de" else en, 11, TEXT_BREITE)]
    if de2:
        zeilen += [(z, GUT) for z in umbrechen(
            de2 if sk.SPRACHE == "de" else en2, 11, TEXT_BREITE)]
    if len(zeilen) > 3:
        ZU_LANG.append("%d Zeilen: %s ..." % (len(zeilen), zeilen[0][0][:52]))
        zeilen = zeilen[:3]
    y = 246 + (3 - len(zeilen)) * 8
    for inhalt, farbe in zeilen:
        sk.text(draw, 20, y, inhalt, 11, farbe)
        y += 16


def loeschen(draw, x0, y0, x1, y1, hintergrund=GRUND):
    """Ein Stueck Bild wieder auf den Grund setzen. So bekommt eine Wolke
    ihre schnurgerade Basis: nicht durch einen Balken darunter, sondern
    indem verschwindet, was unter die Basis ragt.

    `hintergrund` ist noetig, wo nicht der schwarze Grund hinter der Wolke
    steht, sondern etwa die graue Dunstschicht -- sonst schneidet der
    Schnitt ein schwarzes Loch hinein."""
    draw.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=hintergrund)


def kreis(draw, x, y, r, farbe):
    draw.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S],
                 fill=farbe)


def haufen(draw, cx, basis, breite, hoehe, farbe=WOLKE, seed=0, turm=False,
           zerfallen=False, hintergrund=GRUND):
    """Eine Quellwolke von der Seite: Kugelreihen auf einer flachen Basis.

    Die unterste Reihe liegt genau auf der Basis und wird dort abgeschnitten
    -- die messerscharfe Unterkante ist das Merkmal, an dem man eine
    Thermikwolke von allem anderen unterscheidet. `turm` laesst die Reihen
    nach oben nur langsam schmaler werden (congestus), `zerfallen` laesst
    den Schnitt weg: eine Wolke ohne Basis traegt nicht mehr.

    Die Breite je Reihe folgt einem Viertelkreis und nicht einer Geraden --
    eine linear schmaler werdende Wolke sieht aus wie ein Tannenbaum.
    """
    rng = random.Random(seed)
    r = max(4.0, breite * 0.17)
    reihen = max(1, int(round(hoehe / (r * 0.78))))
    for i in range(reihen):
        t = i / float(reihen - 1) if reihen > 1 else 0.0
        schmal = (1.0 - t ** (4.0 if turm else 2.2)) ** (0.35 if turm else 0.5)
        w = breite * schmal
        y = basis - (hoehe - r) * t
        n = max(1, int(round(w / (r * 1.15))))
        for k in range(n):
            x = cx - w / 2 + (k + 0.5) * w / n
            rr = r * rng.uniform(0.82, 1.08) * (0.8 if t > 0.9 else 1.0)
            kreis(draw, x + rng.uniform(-r * 0.18, r * 0.18),
                  y + rng.uniform(-r * 0.16, r * 0.16), rr, farbe)
    if not zerfallen:
        # Nur so breit wie die Wolke wirklich ist: ein zu breiter Schnitt
        # radiert den Nachbarn oder den Hintergrund daneben mit weg.
        loeschen(draw, cx - breite * 0.72, basis + 1, cx + breite * 0.72,
                 basis + r + 6, hintergrund)


def schicht(draw, x0, x1, y, dicke, farbe=WOLKE, seed=0, buckel=True,
            hintergrund=GRUND):
    """Eine Schichtwolke: ein Band, oben gebuckelt, unten glatt."""
    rng = random.Random(seed)
    draw.rectangle([x0 * S, y * S, x1 * S, (y + dicke) * S], fill=farbe)
    if buckel:
        x = x0
        while x < x1:
            r = dicke * rng.uniform(0.45, 0.8)
            kreis(draw, x, y + dicke * 0.35, r, farbe)
            x += r * 1.25
        loeschen(draw, x0 - dicke, y + dicke + 1, x1 + dicke, y + 2.2 * dicke,
                 hintergrund)


def boden(draw, y=BODEN_Y, x0=0, x1=W, farbe=ERDE, dicke=5):
    draw.rectangle([x0 * S, y * S, x1 * S, (y + dicke) * S], fill=farbe)


def berg(draw, punkte, farbe=FELS, rand=LINIE):
    draw.polygon([(x * S, y * S) for x, y in punkte], fill=farbe, outline=rand,
                 width=1 * S)


def segler(draw, x, y, winkel=0.0, laenge=24, farbe=KOERPER):
    """Ein Segelflugzeug von der Seite: Rumpf, Fluegel, Seitenleitwerk."""
    c, s = math.cos(math.radians(winkel)), math.sin(math.radians(winkel))
    sk.strich(draw, x - laenge / 2 * c, y - laenge / 2 * s,
              x + laenge / 2 * c, y + laenge / 2 * s, farbe, 2)
    qx, qy = -s, c
    sk.strich(draw, x - 6 * qx, y - 6 * qy, x + 6 * qx, y + 6 * qy, farbe, 2)
    sk.strich(draw, x - laenge / 2 * c, y - laenge / 2 * s,
              x - laenge / 2 * c, y - laenge / 2 * s - 6, farbe, 2)


def segler_oben(draw, x, y, winkel=0.0, spanne=22, farbe=KOERPER):
    """Von oben: Rumpf in Flugrichtung, Fluegel vorn, Leitwerk hinten.

    Ohne das kurze Leitwerk sind Bug und Heck nicht zu unterscheiden -- und
    ein Kreuz ohne Richtung taugt in einer Platzrunde nichts."""
    c, s = math.cos(math.radians(winkel)), math.sin(math.radians(winkel))
    qx, qy = -s, c
    sk.strich(draw, x - 10 * c, y - 10 * s, x + 10 * c, y + 10 * s, farbe, 2)
    fx, fy = x + 2 * c, y + 2 * s
    sk.strich(draw, fx - spanne / 2 * qx, fy - spanne / 2 * qy,
              fx + spanne / 2 * qx, fy + spanne / 2 * qy, farbe, 2)
    hx, hy = x - 9 * c, y - 9 * s
    sk.strich(draw, hx - spanne / 5 * qx, hy - spanne / 5 * qy,
              hx + spanne / 5 * qx, hy + spanne / 5 * qy, farbe, 2)


def sonne(draw, x, y, r=11, strahlen=True, farbe=(255, 222, 120)):
    kreis(draw, x, y, r, farbe)
    if strahlen:
        for i in range(8):
            a = math.radians(i * 45 + 11)
            sk.strich(draw, x + math.cos(a) * (r + 4), y + math.sin(a) * (r + 4),
                      x + math.cos(a) * (r + 10), y + math.sin(a) * (r + 10),
                      farbe, 1)


def regen(draw, x0, x1, y0, y1, anzahl=26, seed=5, farbe=(120, 130, 150)):
    rng = random.Random(seed)
    for _ in range(anzahl):
        x = rng.uniform(x0, x1)
        y = y0 + rng.uniform(0, max(1.0, (y1 - y0) * 0.5))
        sk.strich(draw, x, y, x - 3, y + 9, farbe, 1)


def wirbel(draw, cx, cy, r, farbe=WARN, dicke=2, drehsinn=1, offen=70):
    """Ein Kreispfeil -- die Spitze gibt den Drehsinn."""
    von = -90 + offen / 2.0
    bis = 270 - offen / 2.0
    sk.bogen(draw, cx, cy, r, von, bis, farbe, dicke)
    a = math.radians(bis if drehsinn > 0 else von)
    x, y = cx + r * math.cos(a), cy + r * math.sin(a)
    t = a + (math.pi / 2 if drehsinn > 0 else -math.pi / 2)
    sk.pfeil(draw, x, y, x + math.cos(t) * 7, y + math.sin(t) * 7, farbe,
             dicke, 6)


def linse(draw, cx, cy, breite, hoehe, farbe=WOLKE, lagen=3):
    """Eine Linsenwolke: flache Teller uebereinander. Ein einzelner Teller
    sieht nach Untertasse aus, erst der Stapel nach Lenticularis."""
    for i in range(lagen):
        t = i / float(max(1, lagen - 1))
        b, h = breite * (1.0 - 0.42 * t), hoehe * (1.0 - 0.3 * t)
        y = cy - i * hoehe * 0.95
        draw.ellipse([(cx - b / 2) * S, (y - h / 2) * S,
                      (cx + b / 2) * S, (y + h / 2) * S], fill=farbe)


def stromlinie(draw, y0, amp, lam, x0, farbe=BETONT, dicke=1, x_von=20,
               x_bis=420, daempfung=400.0, schritt=3):
    """Eine Stromlinie ueber einem Hindernis.

    Vor dem Berg hebt sie sich glockenfoermig an, dahinter schwingt sie
    aus: genau das ist die Leewelle. Beide Haelften treffen sich bei x0 auf
    demselben Wert, sonst hat die Linie am Gipfel einen Knick.
    """
    punkte = []
    x = x_von
    while x <= x_bis:
        d = x - x0
        if d < 0:
            h = amp * math.exp(-(d / 58.0) ** 2)
        else:
            h = amp * math.cos(2 * math.pi * d / lam) * math.exp(-d / daempfung)
        punkte.append((x * S, (y0 - h) * S))
        x += schritt
    draw.line(punkte, fill=farbe, width=dicke * S, joint="curve")


def baum(draw, x, fuss, hoehe=16, farbe=(52, 84, 54)):
    draw.polygon([(x * S, (fuss - hoehe) * S), ((x - hoehe * 0.42) * S, fuss * S),
                  ((x + hoehe * 0.42) * S, fuss * S)], fill=farbe)


def welle_wasser(draw, x0, x1, y, farbe=(58, 86, 124)):
    draw.rectangle([x0 * S, y * S, x1 * S, (y + 5) * S], fill=farbe)
    x = x0 + 6
    while x < x1 - 6:
        sk.bogen(draw, x, y + 1, 4, 180, 360, (110, 150, 190), 1)
        x += 14


def ring_strichelt(draw, cx, cy, r, farbe=DUENN, dicke=1, stuecke=16):
    """Ein gestrichelter Kreis -- fuer das, was man gerade nicht tun soll."""
    for i in range(stuecke):
        if i % 2:
            continue
        sk.bogen(draw, cx, cy, r, i * 360.0 / stuecke,
                 (i + 1) * 360.0 / stuecke, farbe, dicke)


def achsen(draw, x0, y0, x1, y1, unten_de, unten_en, links_de, links_en):
    """Ein Achsenkreuz: die eine Groesse nach rechts, die andere nach oben."""
    sk.strich(draw, x0, y0, x0, y1, DUENN, 1)
    sk.strich(draw, x0, y0, x1, y0, DUENN, 1)
    beschrift(draw, x1, y0 + 7, unten_de, unten_en, 10, DUENN, rechts=True)
    beschrift(draw, x0 + 6, y1 - 2, links_de, links_en, 10, DUENN)


# ---------------------------------------------------------------------------
# Thermik und Schichtung
# ---------------------------------------------------------------------------

def durchschiessen():
    bild, draw = sk.leinwand()
    inv = 112

    # Links laeuft die Blase gegen die Sperrschicht und legt sich darunter
    # breit; rechts dieselbe Wolke, nur kraeftiger -- sie stoesst hindurch.
    # Erst der Deckel, dann die Wolke darunter: der flache Teller schneidet
    # beim Zeichnen seine Unterkante frei und wuerde sonst den Kopf der
    # Quellwolke wegradieren.
    haufen(draw, 116, inv + 18, 160, 15, seed=7)
    haufen(draw, 112, 196, 74, 80, seed=3)
    haufen(draw, 316, 196, 72, 158, seed=11, turm=True)

    sk.gestrichelt(draw, 18, inv, 422, inv, WARN, 1, 7)
    beschrift(draw, 420, inv - 18, "Inversion", "inversion", 11, WARN,
              rechts=True)

    boden(draw)
    beschrift(draw, 124, 208, "breitet sich darunter aus",
              "spreads out underneath", 11, ROT, mitte=True)
    beschrift(draw, 320, 208, "schießt durch", "shoots through", 11, GUT,
              mitte=True)

    unterschrift(draw,
                 "Die Sperrschicht hält die Blase — bis eine kommt, die "
                 "kräftig genug ist.",
                 "The lid holds the bubble down — until one comes up strong "
                 "enough.",
                 "Darüber wächst sie frei weiter: aus humilis wird congestus.",
                 "Above it the cloud grows on freely: humilis becomes "
                 "congestus.")
    sk.sichern(bild, "begriff-durchschiessen")


def basis():
    bild, draw = sk.leinwand()
    hoehe = 108

    for cx, br, ho, seed in ((104, 64, 40, 2), (182, 50, 30, 4),
                             (268, 74, 46, 6), (352, 56, 34, 8)):
        haufen(draw, cx, hoehe, br, ho, seed=seed)
    sk.gestrichelt(draw, 34, hoehe, 420, hoehe, GUT, 1, 7)
    beschrift(draw, 420, hoehe + 7, "alle Basen gleich hoch",
              "all bases level", 11, GUT, rechts=True)

    boden(draw)
    # Der Schlauch unter der mittleren Wolke steht ueber einem dunklen Feld:
    # die Wolke ist sein Kopf, das Feld seine Quelle.
    draw.rectangle([242 * S, BODEN_Y * S, 294 * S, (BODEN_Y + 5) * S], fill=FELD)
    sk.gestrichelt(draw, 242, BODEN_Y, 254, hoehe + 4, BETONT, 1, 6)
    sk.gestrichelt(draw, 294, BODEN_Y, 282, hoehe + 4, BETONT, 1, 6)
    for y in (216, 186, 156):
        sk.pfeil(draw, 268, y, 268, y - 20, BETONT, 2, 6)
    beschrift(draw, 302, 178, "Thermikschlauch", "thermal", 11, BETONT)

    sk.pfeil(draw, 40, BODEN_Y, 40, hoehe, TEXT, 1)
    sk.pfeil(draw, 40, hoehe, 40, BODEN_Y, TEXT, 1)
    beschrift(draw, 48, 160, "Basishöhe", "base height", 11, TEXT)
    beschrift(draw, 48, 176, "≈ 1800 m", "≈ 1800 m", 11, TEXT)

    unterschrift(draw,
                 "Die Basis ist das Kondensationsniveau — in einer Luftmasse "
                 "für jede Wolke dieselbe Höhe.",
                 "The base is the condensation level — the same height for "
                 "every cloud in one air mass.",
                 "Darum liest man an einer Wolke ab, wie hoch alle anderen "
                 "tragen.",
                 "So one cloud tells you how high all the others will carry "
                 "you.")
    sk.sichern(bild, "begriff-basis")


def inversion():
    bild, draw = sk.leinwand()
    inv_o, inv_u = 118, 144

    # Links das Temperaturprofil, rechts der Himmel dazu, beide auf
    # derselben Hoehe: der Knick und der Dunstdeckel sind eine Zeile.
    achsen(draw, 52, 222, 206, 42, "Temperatur →", "temperature →",
           "Höhe", "height")
    sk.strich(draw, 164, 222, 122, inv_u, WARN, 2)
    sk.strich(draw, 122, inv_u, 172, inv_o, WARN, 2)
    sk.strich(draw, 172, inv_o, 128, 52, WARN, 2)
    beschrift(draw, 168, 204, "T", "T", 12, WARN)
    beschrift(draw, 178, inv_o - 16, "wärmer", "warmer", 10, BETONT)

    # Rechts der Himmel dazu, durch einen Strich als zweite Tafel kenntlich.
    sk.strich(draw, 232, 36, 232, BODEN_Y, DUENN, 1)
    draw.rectangle([236 * S, inv_u * S, 424 * S, BODEN_Y * S], fill=DUNST)
    haufen(draw, 316, 192, 76, 48, WOLKE_SCHATTEN, seed=4, hintergrund=DUNST)
    sonne(draw, 392, 68, 10)
    boden(draw, x0=236)
    beschrift(draw, 242, 200, "Dunst, Sicht schlecht",
              "haze, poor visibility", 10, TEXT)
    beschrift(draw, 420, inv_o - 32, "darüber klar", "clear above", 10, TEXT,
              rechts=True)

    sk.gestrichelt(draw, 52, inv_u, 424, inv_u, DUENN, 1, 7)
    sk.gestrichelt(draw, 52, inv_o, 424, inv_o, DUENN, 1, 7)
    beschrift(draw, 330, inv_o + 4, "Inversion", "inversion", 11, BETONT,
              mitte=True)

    unterschrift(draw,
                 "In der Inversion nimmt die Temperatur mit der Höhe zu.",
                 "In an inversion the temperature increases with height.",
                 "Die Blase ist dort nicht mehr wärmer als ihre Umgebung und "
                 "bleibt stehen — mit ihr Dunst, Rauch und die Basis.",
                 "The bubble is no longer warmer than its surroundings and "
                 "stops — and with it haze, smoke and the cloud base.")
    sk.sichern(bild, "begriff-inversion")


def labilitaet():
    bild, draw = sk.leinwand()
    achsen(draw, 56, 228, 408, 36, "Temperatur →", "temperature →",
           "Höhe", "height")
    fx, fy = 266, 226                      # beide Luftmassen starten am Boden
    # Das Paket kuehlt immer gleich ab (1 °C je 100 m). Ob es weitersteigt,
    # entscheidet allein, wie schnell die Umgebung abkuehlt.
    sk.strich(draw, fx, fy, 208, 70, BETONT, 2)
    beschrift(draw, 208, 36, "Paket", "parcel", 11, BETONT, mitte=True)
    beschrift(draw, 208, 51, "1 °C je 100 m", "1 °C per 100 m", 10, BETONT,
              mitte=True)

    sk.strich(draw, fx, fy, 146, 104, WARN, 2)
    beschrift(draw, 138, 90, "labile", "unstable", 11, WARN, rechts=True)
    beschrift(draw, 138, 105, "Umgebung", "environment", 11, WARN, rechts=True)

    sk.strich(draw, fx, fy, 344, 104, GUT, 2)
    beschrift(draw, 352, 90, "stabile", "stable", 11, GUT)
    beschrift(draw, 352, 105, "Umgebung", "environment", 11, GUT)

    y = 150
    t = (fy - y) / float(fy - 104)
    lx = fx + (146 - fx) * t
    sx = fx + (344 - fx) * t
    px = fx + (208 - fx) * (fy - y) / float(fy - 70)
    sk.gestrichelt(draw, lx, y, sx, y, DUENN, 1, 6)
    kreis(draw, px, y, 3, TEXT)
    sk.pfeil(draw, px, y - 6, px, y - 34, WARN, 2, 6)
    beschrift(draw, px + 8, y - 32, "wärmer → steigt weiter",
              "warmer → keeps rising", 10, WARN)
    sk.pfeil(draw, px, y + 6, px, y + 34, GUT, 2, 6)
    beschrift(draw, px + 8, y + 20, "kälter → sinkt zurück",
              "colder → sinks back", 10, GUT)

    unterschrift(draw,
                 "Labil heißt nicht „warm“, sondern: die Umgebung kühlt "
                 "schneller ab als das steigende Paket.",
                 "Unstable does not mean “warm” but: the environment cools "
                 "faster than the rising parcel.",
                 "Dann bleibt das Paket wärmer und steigt ohne weiteres Zutun.",
                 "Then the parcel stays warmer and rises with no further help.")
    sk.sichern(bild, "begriff-labilitaet")


def spread():
    bild, draw = sk.leinwand()
    # Links die beiden Zahlen am Boden, rechts, was sie ueber den Himmel
    # sagen: die Spreizung ist eine Bodenmessung mit einer Aussage oben.
    y = 176
    sk.strich(draw, 26, y, 196, y, DUENN, 1)
    beschrift(draw, 26, y + 8, "Temperatur am Boden",
              "temperature at the ground", 10, DUENN)
    for x, farbe in ((62, BETONT), (170, WARN)):
        sk.strich(draw, x, y - 7, x, y + 7, farbe, 2)
    beschrift(draw, 62, y - 44, "Taupunkt", "dew point", 11, BETONT, mitte=True)
    beschrift(draw, 62, y - 29, "9 °C", "9 °C", 11, BETONT, mitte=True)
    beschrift(draw, 170, y - 44, "Temperatur", "temperature", 11, WARN,
              mitte=True)
    beschrift(draw, 170, y - 29, "24 °C", "24 °C", 11, WARN, mitte=True)

    sk.strich(draw, 62, y + 26, 170, y + 26, GUT, 1)
    sk.strich(draw, 62, y + 22, 62, y + 30, GUT, 1)
    sk.strich(draw, 170, y + 22, 170, y + 30, GUT, 1)
    beschrift(draw, 116, y + 32, "Spreizung 15 K", "spread 15 K", 11, GUT,
              mitte=True)

    hoehe = 76
    boden(draw, x0=244)
    haufen(draw, 340, hoehe, 70, 42, seed=12)
    sk.gestrichelt(draw, 250, hoehe, 420, hoehe, GUT, 1, 7)
    sk.pfeil(draw, 262, BODEN_Y, 262, hoehe, TEXT, 1)
    sk.pfeil(draw, 262, hoehe, 262, BODEN_Y, TEXT, 1)
    beschrift(draw, 270, 142, "≈ 1900 m", "≈ 1900 m", 11, TEXT)

    beschrift(draw, 116, y + 48, "× 125 m je Kelvin", "× 125 m per kelvin",
              11, GUT, mitte=True)
    sk.strich(draw, 228, 36, 228, BODEN_Y, DUENN, 1)

    unterschrift(draw,
                 "Spreizung = Temperatur minus Taupunkt, gemessen am Boden.",
                 "Spread = temperature minus dew point, measured at the ground.",
                 "Rund 125 m Basishöhe je Kelvin — und zu viel Spreizung heißt "
                 "Blauthermik.",
                 "About 125 m of cloud base per kelvin — and too much spread "
                 "means blue thermals.")
    sk.sichern(bild, "begriff-spread")


def taupunkt():
    bild, draw = sk.leinwand()
    basis_y = 72
    # Dieselbe Luft auf drei Hoehen: die beiden Zahlen laufen aufeinander
    # zu, weil T fuenfmal schneller faellt als T_d. Wo sie sich treffen,
    # steht die Wolke.
    sk.gestrichelt(draw, 146, 212, 160, basis_y, DUENN, 1, 6)
    sk.gestrichelt(draw, 198, 212, 184, basis_y, DUENN, 1, 6)
    for yy in (206, 164, 122):
        sk.pfeil(draw, 172, yy, 172, yy - 24, BETONT, 2, 6)

    haufen(draw, 172, basis_y, 62, 36, seed=14)
    sk.gestrichelt(draw, 212, basis_y, 292, basis_y, GUT, 1, 7)

    for yy, h, t1, t2, treffer in ((212, "0 m", "T 24 °C", "T_d 9 °C", False),
                                   (146, "1000 m", "T 14 °C", "T_d 7 °C", False),
                                   (basis_y + 2, "1900 m", "T 5 °C", "T_d 5 °C",
                                    True)):
        beschrift(draw, 138, yy - 7, h, h, 10, DUENN, rechts=True)
        sk.strich(draw, 142, yy, 204, yy, DUENN, 1)
        beschrift(draw, 218, yy - 15, t1, t1, 11, WARN)
        beschrift(draw, 218, yy + 1, t2, t2, 11, BETONT)
        if treffer:
            beschrift(draw, 302, yy - 7, "→ gesättigt", "→ saturated", 11, GUT)

    boden(draw)
    unterschrift(draw,
                 "Der Taupunkt ist die Temperatur, bei der die Luft gesättigt "
                 "wäre.",
                 "The dew point is the temperature at which the air would be "
                 "saturated.",
                 "Beim Steigen fällt T um 1 °C, T_d nur um 0,2 °C je 100 m — "
                 "treffen sie sich, beginnt die Wolke.",
                 "On the way up T falls 1 °C, T_d only 0.2 °C per 100 m — "
                 "where they meet, the cloud begins.")
    sk.sichern(bild, "begriff-taupunkt")


def kondensationsniveau():
    bild, draw = sk.leinwand()
    achsen(draw, 96, 224, 404, 40, "Temperatur →", "temperature →",
           "Höhe", "height")
    tx, dx = 336, 244
    mx, my = 198, 92
    sk.strich(draw, tx, 224, mx, my, WARN, 2)
    sk.strich(draw, dx, 224, mx, my, BETONT, 2)
    beschrift(draw, tx + 4, 206, "T", "T", 12, WARN)
    beschrift(draw, dx - 4, 206, "T_d", "T_d", 12, BETONT, rechts=True)

    sk.gestrichelt(draw, 96, my, 404, my, GUT, 1, 7)
    draw.ellipse([(mx - 8) * S, (my - 8) * S, (mx + 8) * S, (my + 8) * S],
                 outline=GUT, width=2 * S)
    haufen(draw, 320, my, 68, 40, seed=16)
    beschrift(draw, 402, my + 8, "Kondensationsniveau = Basis",
              "condensation level = cloud base", 11, GUT, rechts=True)
    beschrift(draw, 106, my - 22, "hier ist die Luft gesättigt",
              "here the air is saturated", 10, TEXT)

    unterschrift(draw,
                 "Das Kondensationsniveau ist die Höhe, in der die steigende "
                 "Luft ihren Taupunkt erreicht.",
                 "The condensation level is the height at which rising air "
                 "reaches its dew point.",
                 "Es gehört der Luftmasse, nicht der einzelnen Wolke.",
                 "It belongs to the air mass, not to the single cloud.")
    sk.sichern(bild, "begriff-kondensationsniveau")


def ausloesung():
    bild, draw = sk.leinwand()
    grund = 206
    # Drei Untergruende nebeneinander: nur einer heizt. Die Blase haengt so
    # lange am Boden, bis sie leicht genug ist -- das ist die Ausloesung.
    boden(draw, grund, 20, 150, (52, 84, 54))
    boden(draw, grund, 150, 292, FELD)
    welle_wasser(draw, 292, 420, grund)
    for x in (44, 70, 96, 122):
        baum(draw, x, grund)

    beschrift(draw, 85, 214, "Wald, kühl", "forest, cool", 10, DUENN, mitte=True)
    beschrift(draw, 221, 214, "trockener Acker, heiß",
              "dry field, hot", 10, WARN, mitte=True)
    beschrift(draw, 356, 214, "See, kühl", "lake, cool", 10, DUENN, mitte=True)

    # Die warme Luft sammelt sich erst flach an und loest sich dann als Ganzes
    draw.arc([155 * S, (grund - 30) * S, 287 * S, (grund + 30) * S],
             180, 360, fill=WARN, width=2 * S)
    beschrift(draw, 221, grund - 26, "warme Luft sammelt sich",
              "warm air pools", 10, WARN, mitte=True)

    kreis(draw, 228, 110, 26, GRUND)
    sk.bogen(draw, 228, 110, 26, 0, 360, WARN, 2)
    sk.pfeil(draw, 228, 128, 228, 84, WARN, 2)
    sk.gestrichelt(draw, 224, grund - 32, 228, 140, WARN, 1, 6)
    beschrift(draw, 268, 96, "die Blase löst sich", "the bubble breaks away",
              11, WARN)
    sonne(draw, 62, 54, 12)
    beschrift(draw, 62, 82, "Einstrahlung", "sunshine", 10, DUENN, mitte=True)

    unterschrift(draw,
                 "Die Luft über dem heißen Feld wird so leicht, dass sie als "
                 "Blase abreißt.",
                 "The air over the hot field gets light enough to break away.",
                 "Die Auslösetemperatur ist die Bodentemperatur, bei der das "
                 "zum ersten Mal gelingt.",
                 "The trigger temperature is where that first works.")
    sk.sichern(bild, "begriff-ausloesung")


def ueberentwicklung():
    bild, draw = sk.leinwand()
    basis_y = 182
    # Derselbe Tag dreimal. Die Basis bleibt, der Kopf waechst -- und mit
    # dem Kopf verschwindet das Steigen darunter.
    haufen(draw, 76, basis_y, 60, 34, seed=21)
    haufen(draw, 200, basis_y, 68, 110, seed=23, turm=True)
    haufen(draw, 338, basis_y, 84, 152, seed=25, turm=True)
    # Der Amboss liegt dem Kopf auf und zieht mit dem Wind nach rechts aus.
    draw.polygon([(282 * S, 58 * S), (320 * S, 40 * S), (434 * S, 36 * S),
                  (434 * S, 50 * S), (330 * S, 62 * S)], fill=EIS)
    regen(draw, 312, 372, basis_y + 4, 196, 30, seed=29)
    sk.gestrichelt(draw, 24, basis_y, 420, basis_y, DUENN, 1, 7)

    boden(draw)
    for x, de, en, farbe in ((76, "10 Uhr: humilis", "10:00: humilis", GUT),
                             (200, "13 Uhr: congestus", "13:00: congestus",
                              WARN),
                             (338, "15 Uhr: Schauer", "15:00: showers", ROT)):
        beschrift(draw, x, 210, de, en, 10, farbe, mitte=True)

    unterschrift(draw,
                 "Überentwicklung: Die Quellwolke wächst über das gute Maß "
                 "hinaus, bis sie regnet.",
                 "Overdevelopment: the cumulus grows past the useful stage.",
                 "Ihr Schatten nimmt der Umgebung die Thermik.",
                 "Its shadow takes the lift from the area.")
    sk.sichern(bild, "begriff-ueberentwicklung")


def ausbreitung():
    bild, draw = sk.leinwand()
    basis_y = 150
    sonne(draw, 60, 48, 12)

    haufen(draw, 110, basis_y, 70, 54, seed=31)
    beschrift(draw, 110, 164, "scharf, trägt", "crisp, works", 11, GUT,
              mitte=True)

    sk.pfeil(draw, 170, 120, 212, 120, DUENN, 2)
    haufen(draw, 330, basis_y, 180, 26, WOLKE_SCHATTEN, seed=33)
    beschrift(draw, 330, 164, "ausgebreitet, trägt nicht mehr",
              "spread out, no longer works", 11, ROT, mitte=True)

    boden(draw)
    # Was oben zugeht, fehlt unten: der Schatten ist der eigentliche Schaden.
    draw.rectangle([244 * S, (BODEN_Y - 8) * S, 420 * S, BODEN_Y * S],
                   fill=(40, 42, 50))
    for x in (70, 110, 150):
        sk.gestrichelt(draw, x, 182, x + 8, 204, (255, 222, 120), 1, 6)
    beschrift(draw, 332, BODEN_Y - 20, "Schatten", "shadow", 10, DUENN,
              mitte=True)
    beschrift(draw, 110, 208, "Sonne am Boden", "sun on the ground",
              10, DUENN, mitte=True)

    unterschrift(draw,
                 "Ausbreitung: Der Wolkenkopf läuft unter einer Sperrschicht "
                 "seitlich aus und wird zu einer Schicht.",
                 "Spreading out: the cloud top runs sideways under a lid and "
                 "turns into a layer.",
                 "Die Basis bleibt, aber der Boden bekommt keine Sonne mehr.",
                 "The base stays, but the ground gets no more sun.")
    sk.sichern(bild, "begriff-ausbreitung")


def abschirmung():
    bild, draw = sk.leinwand()
    # Die hohe Schicht kommt von weit her und hat mit der Thermik darunter
    # nichts zu tun -- sie nimmt ihr nur das Licht.
    schicht(draw, 0, 440, 44, 22, (186, 194, 208), seed=35)
    kreis(draw, 330, 60, 13, (214, 212, 200))
    beschrift(draw, 24, 76, "Cirrostratus / Altostratus",
              "cirrostratus / altostratus", 10, DUENN)
    beschrift(draw, 330, 76, "Sonne nur noch matt", "sun only dim", 10, DUENN,
              mitte=True)

    for x, seed in ((120, 37), (250, 39), (360, 41)):
        haufen(draw, x, 152, 56, 26, WOLKE_SCHATTEN, seed=seed, zerfallen=True)
    beschrift(draw, 250, 170, "Reste ohne Basis", "remnants without a base",
              10, ROT, mitte=True)

    for x in (56, 118, 332, 394):
        sk.pfeil(draw, x, 190, x, 216, ROT, 2, 6)
    boden(draw, farbe=(52, 58, 52))
    beschrift(draw, 225, 196, "keine Einstrahlung", "no sunshine", 11, ROT,
              mitte=True)

    unterschrift(draw,
                 "Abschirmung: Eine hohe Schicht legt sich vor die Sonne, "
                 "meist vor einer Warmfront.",
                 "Shading out: a high layer moves in front of the sun, usually "
                 "ahead of a warm front.",
                 "Ohne Sonne heizt der Boden nicht — die Thermik hört auf.",
                 "With no sun the ground stops heating — the lift dies.")
    sk.sichern(bild, "begriff-abschirmung")


def blauthermik():
    bild, draw = sk.leinwand()
    sonne(draw, 66, 52, 12)
    niveau = 92
    # Der Schlauch ist da, nur die Quittung oben fehlt: die Spreizung ist zu
    # gross, das Kondensationsniveau liegt ueber der Obergrenze.
    sk.gestrichelt(draw, 40, niveau, 400, niveau, DUENN, 1, 7)
    beschrift(draw, 398, niveau - 20, "Kondensationsniveau zu hoch",
              "condensation level too high", 10, DUENN, rechts=True)
    sk.gestrichelt(draw, 40, 134, 420, 134, WARN, 1, 7)
    beschrift(draw, 420, 138, "Obergrenze des Steigens", "top of the lift", 10,
              WARN, rechts=True)

    for x in (130, 250):
        sk.gestrichelt(draw, x - 24, BODEN_Y, x - 12, 140, BETONT, 1, 6)
        sk.gestrichelt(draw, x + 24, BODEN_Y, x + 12, 140, BETONT, 1, 6)
        for y in (212, 184, 156):
            sk.pfeil(draw, x, y, x, y - 20, BETONT, 2, 6)
    beschrift(draw, 130, 108, "kein Zeichen am Himmel", "no sign in the sky",
              10, TEXT, mitte=True)

    segler(draw, 356, 112, -8)
    boden(draw)
    draw.rectangle([106 * S, BODEN_Y * S, 154 * S, (BODEN_Y + 5) * S], fill=FELD)
    draw.rectangle([226 * S, BODEN_Y * S, 274 * S, (BODEN_Y + 5) * S], fill=FELD)

    unterschrift(draw,
                 "Blauthermik: Es steigt, aber die Luft ist zu trocken für "
                 "eine Wolke.",
                 "Blue thermals: the air rises, but it is too dry to make a "
                 "cloud.",
                 "Gesucht wird am Boden — Felder, Hänge, Ortschaften — und am "
                 "Variometer.",
                 "You search on the ground — fields, slopes, villages — and on "
                 "the vario.")
    sk.sichern(bild, "begriff-blauthermik")


def dunstglocke():
    bild, draw = sk.leinwand()
    deckel = 128
    # Die Dunstobergrenze ist eine sichtbare Linie: so hoch reicht die
    # Durchmischung, und genau so hoch traegt es.
    draw.rectangle([0, deckel * S, 440 * S, BODEN_Y * S], fill=DUNST)
    for i in range(7):
        y = deckel + 12 + i * 13
        sk.strich(draw, 10 + (i % 3) * 20, y, 410 - (i % 2) * 40, y,
                  (86, 90, 104), 1)
    sk.strich(draw, 0, deckel, 440, deckel, (150, 158, 176), 2)
    beschrift(draw, 420, deckel - 20, "Dunstobergrenze", "top of the haze",
              11, TEXT, rechts=True)
    beschrift(draw, 20, deckel + 12, "trübe, Sicht 5 km",
              "murky, visibility 5 km", 10, TEXT)
    beschrift(draw, 20, 58, "darüber klar, Sicht 50 km",
              "clear above, visibility 50 km", 10, TEXT)

    sonne(draw, 376, 56, 11)
    segler(draw, 150, 92, -6)
    # Weiter rechts als die Sichtangabe endet: "murky, visibility 5 km" ist
    # laenger als "trübe, Sicht 5 km", und der Pfeil stand mitten darin.
    sk.pfeil(draw, 160, 180, 160, 140, BETONT, 2, 6)
    beschrift(draw, 168, 160, "Thermik endet hier", "lift ends here", 10,
              BETONT)

    for x, h in ((230, 24), (268, 34), (306, 20)):
        draw.rectangle([x * S, (BODEN_Y - h) * S, (x + 16) * S, BODEN_Y * S],
                       fill=(58, 62, 74))
    boden(draw)

    unterschrift(draw,
                 "Dunstglocke: Dunst sammelt sich unter einer Inversion und "
                 "hört an ihr scharf auf.",
                 "Haze collects under an inversion and stops sharply at it.",
                 "Ihre Obergrenze zeigt, wie hoch die Durchmischung reicht.",
                 "Its top shows how far the mixing reaches.")
    sk.sichern(bild, "begriff-dunstglocke")


def welle():
    bild, draw = sk.leinwand()
    gipfel_x = 136
    berg(draw, [(52, BODEN_Y), (gipfel_x, 118), (216, BODEN_Y)])
    # Drei Stromlinien, dieselbe Welle in drei Hoehen: nur so sieht man,
    # dass die ganze Luftschicht schwingt und nicht nur eine Linie.
    for y0, amp, dicke in ((176, 30, 1), (124, 26, 1), (78, 20, 2)):
        stromlinie(draw, y0, amp, 118, gipfel_x, BETONT, dicke, 24, 424)

    linse(draw, 254, 52, 86, 15)
    linse(draw, 372, 58, 70, 13)
    beschrift(draw, 150, 28, "Lenticularis", "lenticularis", 11, TEXT,
              rechts=True)

    haufen(draw, 252, 196, 74, 34, WOLKE_SCHATTEN, seed=43, zerfallen=True)
    wirbel(draw, 252, 186, 22, WARN, 2, -1)
    beschrift(draw, 252, 212, "Rotor", "rotor", 11, WARN, mitte=True)

    sk.pfeil(draw, 24, 214, 60, 206, GUT, 2)
    # Links vom Hang stehen lassen: "windward" ist dreimal so breit wie
    # "Luv" und lief sonst in die graue Flanke.
    beschrift(draw, 22, 188, "Luv", "windward", 11, GUT)
    beschrift(draw, 196, 160, "Lee", "lee", 11, TEXT)
    sk.pfeil(draw, 300, 124, 300, 88, GUT, 2, 6)
    beschrift(draw, 424, 120, "Steigen vor der Wolke",
              "lift ahead of the cloud", 10, GUT, rechts=True)
    boden(draw)

    unterschrift(draw,
                 "Leewelle: Die Luft schwingt hinter dem Berg wie Wasser "
                 "hinter einem Stein.",
                 "Lee wave: behind the hill the air oscillates like water "
                 "behind a stone.",
                 "Gestiegen wird im Aufwindteil vor der Linsenwolke, nicht in "
                 "ihr.",
                 "You climb in the rising part ahead of the lens cloud, not "
                 "inside it.")
    sk.sichern(bild, "begriff-welle")


def rotor():
    bild, draw = sk.leinwand()
    berg(draw, [(14, BODEN_Y), (84, 134), (152, BODEN_Y)])
    for y0, amp in ((150, 26), (96, 20)):
        stromlinie(draw, y0, amp, 150, 84, BETONT, 1, 14, 424)
    linse(draw, 236, 58, 92, 16)
    beschrift(draw, 146, 26, "Linsenwolke oben", "lens cloud above", 10, DUENN,
              rechts=True)

    # Der Rotor steht unter dem ersten Wellenberg, nicht hinter dem Gipfel.
    haufen(draw, 232, 200, 110, 46, WOLKE_SCHATTEN, seed=45, zerfallen=True)
    wirbel(draw, 232, 182, 34, WARN, 2, -1)
    wirbel(draw, 340, 192, 22, WARN, 2, -1)
    beschrift(draw, 232, 150, "Rotor", "rotor", 12, WARN, mitte=True)
    segler(draw, 300, 140, 16)
    sk.pfeil(draw, 300, 158, 300, 176, ROT, 2, 6)
    beschrift(draw, 312, 142, "hier wird es grob", "this gets rough", 10, ROT)
    boden(draw)

    unterschrift(draw,
                 "Rotor: die walzenförmige Turbulenz unter dem ersten "
                 "Wellenberg im Lee.",
                 "Rotor: the roll of turbulence under the first wave crest in "
                 "the lee.",
                 "Durch ihn führt der Weg in die Welle — langsam und nie tief.",
                 "The way into the wave leads through it — slow and never low.")
    sk.sichern(bild, "begriff-rotor")


def hangaufwind():
    bild, draw = sk.leinwand()
    berg(draw, [(96, BODEN_Y), (236, 92), (396, BODEN_Y)])
    # Der Wind kann nicht durch den Hang, also geht er darueber -- und nimmt
    # mit, wer nah genug und hoch genug daneben fliegt.
    for y in (210, 178, 146, 114):
        x = 96 + (236 - 96) * (BODEN_Y - y) / float(BODEN_Y - 92)
        sk.pfeil(draw, x - 76, y + 10, x - 16, y - 2, GUT, 2)
    for y in (120, 152, 184):
        x = 236 + (396 - 236) * (y - 92) / float(BODEN_Y - 92)
        sk.pfeil(draw, x + 10, y - 14, x + 30, y + 14, ROT, 2)
    wirbel(draw, 352, 174, 18, ROT, 1, -1)

    # Tiefer und weiter rechts: "this is where you fly" reicht weiter als
    # "hier wird geflogen" und stiess sonst an den Segler.
    segler(draw, 162, 146, -14)
    sk.gestrichelt(draw, 162, 146, 190, 172, DUENN, 1, 6)
    beschrift(draw, 30, 108, "Luv: Hangaufwind", "windward: ridge lift", 11,
              GUT)
    beschrift(draw, 30, 124, "hier wird geflogen", "this is where you fly",
              10, GUT)
    beschrift(draw, 418, 108, "Lee: Abwind", "lee: sink", 11, ROT, rechts=True)
    beschrift(draw, 418, 124, "und Turbulenz", "and turbulence", 10, ROT,
              rechts=True)
    boden(draw)

    unterschrift(draw,
                 "Hangaufwind: Der Wind wird am Hang nach oben abgelenkt.",
                 "Ridge lift: the wind is deflected upwards by the slope.",
                 "Geflogen wird parallel zum Hang im Luv — mit Abstand und "
                 "Ausweg.",
                 "You fly parallel to the slope in the windward side, with a "
                 "margin.")
    sk.sichern(bild, "begriff-hangaufwind")


def luv_lee():
    bild, draw = sk.leinwand()
    berg(draw, [(130, BODEN_Y), (220, 104), (320, BODEN_Y)])
    for y in (126, 160, 194):
        sk.pfeil(draw, 24, y, 110, y, BETONT, 2)
    sk.pfeil(draw, 150, 196, 206, 122, GUT, 2)
    sk.pfeil(draw, 238, 118, 300, 196, ROT, 2)
    for x, y in ((330, 180), (372, 196)):
        wirbel(draw, x, y, 16, ROT, 1, -1)

    beschrift(draw, 24, 104, "Wind", "wind", 11, BETONT)
    # In die Luecke zwischen den Pfeilen bei y=126 und y=160 -- vorher lag
    # der mittlere Pfeil quer durch das zweite Wort.
    beschrift(draw, 120, 128, "Luv", "windward", 13, GUT, rechts=True)
    beschrift(draw, 120, 144, "zugewandt", "facing the wind", 10, GUT,
              rechts=True)
    beschrift(draw, 330, 130, "Lee", "lee", 13, ROT)
    beschrift(draw, 330, 146, "abgewandt", "away from the wind", 10, ROT)
    boden(draw)

    unterschrift(draw,
                 "Luv ist die dem Wind zugewandte Seite, Lee die abgewandte.",
                 "Windward is the side facing the wind, lee the side away "
                 "from it.",
                 "Im Luv steigt es, im Lee sinkt es und wirbelt — das gilt für "
                 "Berge, Hänge und Wolken.",
                 "Windward it rises, in the lee it sinks and tumbles — true "
                 "for hills, slopes and clouds.")
    sk.sichern(bild, "begriff-luv-lee")


def foehn():
    bild, draw = sk.leinwand()
    gipfel = 100
    berg(draw, [(120, BODEN_Y), (228, gipfel), (344, BODEN_Y)])
    # Links Steigregen, rechts trockenes Absinken: dieselbe Luft, und
    # trotzdem ist sie unten rechts waermer als unten links.
    haufen(draw, 180, 150, 120, 46, seed=47)
    regen(draw, 140, 216, 154, 212, 34, seed=49)
    sk.pfeil(draw, 40, 168, 110, 142, BETONT, 2)
    sk.pfeil(draw, 252, 120, 340, 192, WARN, 2)

    beschrift(draw, 34, 174, "feucht, kühl", "moist, cool", 10, BETONT)
    beschrift(draw, 34, 190, "10 °C", "10 °C", 11, BETONT)
    beschrift(draw, 228, 76, "0 °C am Gipfel", "0 °C at the summit", 10, TEXT,
              mitte=True)
    beschrift(draw, 418, 180, "trocken, warm", "dry, warm", 10, WARN,
              rechts=True)
    beschrift(draw, 418, 196, "18 °C", "18 °C", 11, WARN, rechts=True)
    draw.polygon([(236 * S, 120 * S), (254 * S, 120 * S), (248 * S, 192 * S),
                  (240 * S, 192 * S)], fill=(214, 220, 232))
    beschrift(draw, 262, 100, "Föhnmauer", "föhn wall", 10, TEXT)
    boden(draw)

    unterschrift(draw,
                 "Föhn: Die Luft regnet sich im Luv aus und sinkt im Lee "
                 "trocken wieder herab.",
                 "Föhn: the air rains out on the windward side and sinks down "
                 "dry in the lee.",
                 "Trocken erwärmt sie sich schneller, als sie feucht abkühlte.",
                 "Dry, it warms faster than it cooled moist.")
    sk.sichern(bild, "begriff-foehn")


def thermikschlauch():
    bild, draw = sk.leinwand()
    basis_y = 92
    # Der Schlauch steht nicht senkrecht: der Wind legt ihn um. Die Wolke
    # liegt im Lee ihrer Quelle, und deshalb faengt man sie luvseitig ab.
    sk.gestrichelt(draw, 118, BODEN_Y, 218, basis_y, BETONT, 1, 6)
    sk.gestrichelt(draw, 162, BODEN_Y, 266, basis_y, BETONT, 1, 6)
    for xy in ((140, 212), (170, 176), (200, 140), (226, 110)):
        sk.pfeil(draw, xy[0], xy[1], xy[0] + 10, xy[1] - 26, BETONT, 2, 6)
    haufen(draw, 242, basis_y, 76, 44, seed=51)

    sk.pfeil(draw, 24, 56, 92, 56, TEXT, 2)
    beschrift(draw, 24, 38, "Wind", "wind", 11, TEXT)

    boden(draw)
    draw.rectangle([116 * S, BODEN_Y * S, 164 * S, (BODEN_Y + 5) * S], fill=FELD)
    beschrift(draw, 140, 210, "Quelle", "source", 10, WARN, mitte=True)

    segler(draw, 344, 128, 176)
    sk.pfeil(draw, 330, 128, 286, 118, GUT, 2)
    beschrift(draw, 420, 146, "luvseitig anfliegen",
              "approach on the windward side", 10, GUT, rechts=True)

    unterschrift(draw,
                 "Der Thermikschlauch steht schräg: unten die warme Quelle, "
                 "oben im Lee die Wolke.",
                 "The thermal leans: the warm source at the bottom, the cloud "
                 "downwind at the top.",
                 "Angeflogen wird die Luvseite, nicht die Wolke selbst.",
                 "Aim for the windward side, not the cloud itself.")
    sk.sichern(bild, "begriff-thermikschlauch")


def anflug():
    bild, draw = sk.leinwand()
    basis_y = 140
    # Eine Wolke hat zwei Seiten: die wachsende und die zerfallende. Beide
    # sehen von weitem gleich aus, und nur eine traegt.
    haufen(draw, 160, basis_y, 110, 76, seed=53)
    haufen(draw, 350, basis_y, 90, 38, WOLKE_SCHATTEN, seed=55, zerfallen=True)
    sk.strich(draw, 106, basis_y, 214, basis_y, (110, 118, 138), 2)

    beschrift(draw, 160, 56, "scharfer Rand, wächst",
              "crisp edge, growing", 10, GUT, mitte=True)
    beschrift(draw, 222, 148, "dunkle Basis", "dark base", 10, GUT)
    beschrift(draw, 350, 82, "ausgefranst, zerfällt",
              "ragged, falling apart", 10, ROT, mitte=True)

    sk.pfeil(draw, 160, 196, 160, 160, GUT, 2)
    beschrift(draw, 160, 200, "hier steigt es", "lift here", 11, GUT,
              mitte=True)
    sk.pfeil(draw, 350, 166, 350, 196, ROT, 2)
    beschrift(draw, 350, 200, "hier nicht mehr", "not any more", 11, ROT,
              mitte=True)

    segler(draw, 58, 182, -12)
    sk.gestrichelt(draw, 70, 178, 140, 160, DUENN, 1, 6)
    boden(draw)

    unterschrift(draw,
                 "Beim Anflug zählt nicht die Wolke, sondern ihre Seite: "
                 "scharfer Rand und dunkle Basis bedeuten Steigen.",
                 "On the approach what counts is not the cloud but its side: "
                 "a crisp edge and a dark base mean lift.",
                 "Ausgefranste Ränder sind die Vergangenheit der Wolke.",
                 "Ragged edges are the cloud's past.")
    sk.sichern(bild, "begriff-anflug")


def _wolkenband(draw, x0, x1, unterkante, dicke, farbe, schritt=4):
    """Ein Wolkenband laengs einer schraegen Flaeche.

    Die Wolken einer Front liegen nicht nebeneinander, sondern uebereinander
    auf der Frontflaeche: ein Keil, vorne duenn und hoch, hinten dick und
    tief. Als Vieleck gezeichnet, Stuetzpunkt fuer Stuetzpunkt, damit die
    Unterkante genau auf der Frontflaeche sitzt.
    """
    oben, unten = [], []
    x = x0
    while x <= x1:
        y = unterkante(x)
        oben.append((x * S, (y - dicke(x)) * S))
        unten.append((x * S, y * S))
        x += schritt
    draw.polygon(oben + list(reversed(unten)), fill=farbe)


def warmfront():
    bild, draw = sk.leinwand()
    # Die Warmfront ist flach, etwa 1:150. Deshalb steht ihre Wolkendecke
    # schon am Himmel, wenn der Regen noch einen Tag entfernt ist -- und
    # deshalb liest man sie von rechts nach links: Cirrus zuerst.
    x0, x1 = 118, 430
    y0, y1 = 226, 44

    def kante(x):
        return y0 + (y1 - y0) * (x - x0) / float(x1 - x0)

    def dick(x):
        return 62 + (16 - 62) * (x - x0) / float(x1 - x0)

    for a, b, farbe in ((x0, 196, (150, 158, 176)),
                        (196, 290, (182, 190, 204)),
                        (290, x1, (212, 218, 230))):
        _wolkenband(draw, a, b, kante, dick, farbe)
    for i in range(9):
        x = 364 + i * 8
        for k in range(9):
            kreis(draw, x + k * 2.4, kante(x) - dick(x) - 6 - k * 0.9
                  + k * k * 0.05, 2.0, EIS)

    sk.strich(draw, x0, y0, x1, y1, ROT, 2)
    regen(draw, 126, 236, 196, 224, 46, seed=63)

    for x, de, en in ((158, "Nimbostratus", "nimbostratus"),
                      (244, "Altostratus", "altostratus"),
                      (326, "Cirrostratus", "cirrostratus"),
                      (398, "Cirrus", "cirrus")):
        beschrift(draw, x, kante(x) - dick(x) - 32, de, en, 10, DUENN,
                  mitte=True)

    beschrift(draw, 24, 104, "Warmluft gleitet auf", "warm air glides up", 10,
              ROT)
    sk.pfeil(draw, 24, 148, 96, 124, ROT, 2)
    beschrift(draw, 330, 196, "Kaltluft", "cold air", 11, BETONT, mitte=True)
    sk.pfeil(draw, 332, 218, 404, 218, TEXT, 2)
    beschrift(draw, 326, 212, "Zugrichtung", "direction of travel", 10, TEXT,
              rechts=True)
    boden(draw)

    unterschrift(draw,
                 "Warmfront: Die warme Luft gleitet flach über die kalte und "
                 "schiebt ihre Wolken voraus.",
                 "Warm front: the warm air glides up over the cold and pushes "
                 "its clouds ahead.",
                 "Cirrus, Halo, Altostratus, Regen — die Abfolge ist die "
                 "Vorhersage.",
                 "Cirrus, halo, altostratus, rain — the sequence is the "
                 "forecast.")
    sk.sichern(bild, "begriff-warmfront")


def kaltfront():
    bild, draw = sk.leinwand()
    kalt = (26, 36, 58)
    # Die Kaltluft schiebt sich als Keil unter die Warmluft: steil, schmal,
    # in einer Stunde vorbei. Was dahinter kommt, ist der bessere Tag.
    draw.polygon([(0, 226 * S), (0, 104 * S), (210 * S, 226 * S)], fill=kalt)
    sk.strich(draw, 0, 104, 210, 226, BETONT, 2)
    beschrift(draw, 40, 182, "Kaltluft", "cold air", 11, BETONT)
    beschrift(draw, 356, 150, "Warmluft", "warm air", 11, WARN, mitte=True)
    sk.pfeil(draw, 262, 188, 312, 124, WARN, 2)
    beschrift(draw, 282, 112, "wird gehoben", "is lifted", 10, WARN)

    haufen(draw, 218, 172, 84, 126, seed=71, turm=True)
    draw.polygon([(190 * S, 62 * S), (228 * S, 44 * S), (342 * S, 40 * S),
                  (342 * S, 54 * S), (238 * S, 66 * S)], fill=EIS)
    regen(draw, 188, 252, 176, 222, 42, seed=73)
    for x, seed in ((46, 75), (104, 77)):
        haufen(draw, x, 136, 44, 24, seed=seed, zerfallen=True)
    beschrift(draw, 76, 96, "dahinter: Cumulus", "behind it: cumulus", 10,
              GUT, mitte=True)
    beschrift(draw, 186, 210, "Schauer, Böen", "showers, squalls", 10, ROT,
              mitte=True)
    sk.pfeil(draw, 344, 196, 412, 196, TEXT, 2)
    beschrift(draw, 338, 190, "Zugrichtung", "direction of travel", 10, TEXT,
              rechts=True)
    boden(draw)

    unterschrift(draw,
                 "Kaltfront: Die Kaltluft schiebt sich als Keil unter die "
                 "Warmluft.",
                 "Cold front: the cold air pushes in as a wedge under the warm "
                 "air.",
                 "Schmal, heftig, schnell vorbei — dahinter gute Sicht.",
                 "Narrow, violent, quickly past — behind it good visibility.")
    sk.sichern(bild, "begriff-kaltfront")


def ring(draw, cx, cy, rx, ry, farbe=DUENN, dicke=1):
    draw.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S],
                 outline=farbe, width=dicke * S)


def _druckgebilde(draw, cx, cy, zeichen, farbe, drehsinn, einwaerts):
    """Isobaren mit Wind: der Drehsinn ist die halbe Aussage, das Ein- oder
    Auswaerts die andere. Nordhalbkugel -- auf der Suedhalbkugel andersherum."""
    for i in range(1, 5):
        ring(draw, cx, cy, 20 * i, 16 * i, DUENN, 1)
    sk.text(draw, cx - 9, cy - 16, zeichen, 26, farbe)
    for i in range(6):
        a = math.radians(i * 60 + 20)
        r = 56
        x, y = cx + math.cos(a) * r * 1.25, cy + math.sin(a) * r
        t = a + drehsinn * math.pi / 2 + einwaerts * drehsinn * 0.5
        sk.pfeil(draw, x, y, x + math.cos(t) * 24, y + math.sin(t) * 22,
                 farbe, 2, 6)


def hochdruck():
    bild, draw = sk.leinwand()
    _druckgebilde(draw, 116, 118, "H", GUT, +1, -1)
    beschrift(draw, 116, 206, "Wind im Uhrzeigersinn, auswärts",
              "wind clockwise, outwards", 10, GUT, mitte=True)
    sk.strich(draw, 236, 24, 236, 220, DUENN, 1)

    for x in (278, 320, 362, 404):
        sk.pfeil(draw, x, 40, x, 104, WARN, 2, 6)
    beschrift(draw, 340, 24, "absinkende Luft", "subsiding air", 10, WARN,
              mitte=True)
    sk.gestrichelt(draw, 252, 128, 428, 128, WARN, 1, 7)
    beschrift(draw, 256, 110, "Inversion", "inversion", 10, WARN)
    draw.rectangle([252 * S, 130 * S, 428 * S, BODEN_Y * S], fill=DUNST)
    haufen(draw, 368, 194, 68, 62, WOLKE_SCHATTEN, seed=81, hintergrund=DUNST)
    beschrift(draw, 258, 150, "Dunst,", "haze,", 10, TEXT)
    beschrift(draw, 258, 165, "flache Basis", "low base", 10, TEXT)
    boden(draw, x0=240)

    unterschrift(draw,
                 "Hoch: Die Luft sinkt groß­räumig ab und erwärmt sich dabei.",
                 "High: the air subsides over a large area and warms as it "
                 "does.",
                 "Das gibt eine Absinkinversion — schönes Wetter, aber tiefe "
                 "Basis und viel Dunst.",
                 "That makes a subsidence inversion — fine weather, but a low "
                 "base and a lot of haze.")
    sk.sichern(bild, "begriff-hochdruck")


def tiefdruck():
    bild, draw = sk.leinwand()
    _druckgebilde(draw, 116, 118, "T", BETONT, -1, +1)
    beschrift(draw, 116, 206, "Wind gegen den Uhrzeigersinn, einwärts",
              "wind anticlockwise, inwards", 10, BETONT, mitte=True)
    sk.strich(draw, 236, 24, 236, 220, DUENN, 1)

    schicht(draw, 244, 436, 36, 32, (158, 166, 182), seed=83)
    for x in (266, 300):
        sk.pfeil(draw, x, 198, x, 98, BETONT, 2, 6)
    regen(draw, 330, 424, 76, 150, 46, seed=85)
    beschrift(draw, 252, 206, "aufsteigende Luft", "rising air", 10, BETONT)
    beschrift(draw, 376, 170, "Wolken und Regen", "cloud and rain", 10, TEXT,
              mitte=True)
    boden(draw, x0=240)

    unterschrift(draw,
                 "Tief: Die Luft strömt zusammen und muss nach oben "
                 "ausweichen.",
                 "Low: the air converges and has nowhere to go but up.",
                 "Aufsteigen heißt Abkühlen heißt Wolken — dazu Fronten und "
                 "viel Wind.",
                 "Rising means cooling means cloud — plus fronts and plenty "
                 "of wind.")
    sk.sichern(bild, "begriff-tiefdruck")


def amboss():
    bild, draw = sk.leinwand()
    tropo = 54
    sk.gestrichelt(draw, 16, tropo, 424, tropo, DUENN, 1, 7)
    beschrift(draw, 20, tropo - 18, "Tropopause", "tropopause", 10, DUENN)

    haufen(draw, 150, 196, 96, 150, seed=87, turm=True)
    # Oben ist Schluss: der Kopf laeuft unter der Tropopause nach Lee aus
    # und gefriert dabei -- faserig statt knubbelig, das ist der Amboss.
    draw.polygon([(104 * S, 76 * S), (156 * S, tropo * S), (400 * S, 58 * S),
                  (396 * S, 74 * S), (180 * S, 92 * S)], fill=EIS)
    for i in range(26):
        y = 60 + (i % 5) * 4
        x = 200 + i * 7.6
        sk.strich(draw, x, y, x + 16, y - 2, (210, 220, 236), 1)
    sk.pfeil(draw, 300, 102, 376, 102, TEXT, 2)
    beschrift(draw, 300, 108, "Höhenwind", "wind aloft", 10, TEXT)
    beschrift(draw, 330, 40, "Eis, faserig", "ice, fibrous", 10, TEXT,
              mitte=True)
    regen(draw, 112, 192, 200, 226, 40, seed=89)
    beschrift(draw, 208, 206, "Hagel, Böen", "hail, squalls", 10, ROT)
    boden(draw)

    unterschrift(draw,
                 "Der Amboss ist der vereiste Kopf eines Cumulonimbus unter "
                 "der Tropopause.",
                 "The anvil is the frozen top of a cumulonimbus under the "
                 "tropopause.",
                 "Wohin er ausläuft, zieht die Zelle.",
                 "The cell travels the way the anvil points.")
    sk.sichern(bild, "begriff-amboss")


def boeenfront():
    bild, draw = sk.leinwand()
    haufen(draw, 338, 150, 100, 110, WOLKE_SCHATTEN, seed=91, turm=True)
    regen(draw, 296, 380, 154, 222, 44, seed=93)
    # Die kalte Luft faellt heraus, schlaegt unten auf und laeuft voraus.
    sk.pfeil(draw, 318, 160, 300, 214, BETONT, 2)
    for x in (260, 210, 160):
        sk.pfeil(draw, x + 34, 216, x, 216, BETONT, 2, 6)
    haufen(draw, 150, 186, 110, 30, WOLKE_SCHATTEN, seed=95, zerfallen=True)
    wirbel(draw, 150, 196, 20, WARN, 2, 1)
    beschrift(draw, 150, 144, "Böenwalze", "roll cloud", 10, WARN, mitte=True)
    beschrift(draw, 98, 212, "10–20 km voraus", "10–20 km ahead", 10, ROT,
              mitte=True)
    segler(draw, 56, 120, -10)
    sk.gestrichelt(draw, 70, 126, 118, 160, DUENN, 1, 6)
    beschrift(draw, 20, 96, "Wind dreht und frischt auf",
              "wind veers and gets up", 10, TEXT)
    boden(draw, 232)

    unterschrift(draw,
                 "Böenfront: Der Kaltluftausfluss eines Gewitters läuft als "
                 "Wall über den Boden.",
                 "Gust front: a thunderstorm's cold outflow runs across the "
                 "ground as a wall.",
                 "Sie kommt vor der Zelle an — der Platz ist dann schon "
                 "unbrauchbar.",
                 "It arrives before the cell — by then the airfield is "
                 "already unusable.")
    sk.sichern(bild, "begriff-boeenfront")


def halo():
    bild, draw = sk.leinwand()
    cx, cy = 180, 120
    # Der Ring hat immer denselben Radius: 22°. Er kommt nicht von der
    # Wolke, sondern von der Form der Eiskristalle darin.
    for i in range(72):
        y = 24 + (i % 12) * 16
        x = 6 + ((i * 97) % 410)
        sk.strich(draw, x, y, x + 38, y - 3, (92, 100, 120), 1)
    ring(draw, cx, cy, 78, 78, (246, 240, 210), 2)
    sonne(draw, cx, cy, 13, True)
    sk.gestrichelt(draw, cx, cy, cx + 78, cy, DUENN, 1, 6)
    beschrift(draw, cx + 40, cy - 18, "22°", "22°", 12, TEXT, mitte=True)
    beschrift(draw, 286, 60, "Cirrostratus", "cirrostratus", 10, TEXT)
    sk.pfeil(draw, 300, 72, 262, 92, DUENN, 1)
    beschrift(draw, 420, 182, "Warmfront im Anzug", "warm front on the way",
              11, WARN, rechts=True)
    sk.pfeil(draw, 320, 204, 392, 204, WARN, 2)
    boden(draw)

    unterschrift(draw,
                 "Halo: der 22°-Ring um Sonne oder Mond, gebrochen an "
                 "Eiskristallen im Cirrostratus.",
                 "Halo: the 22° ring around sun or moon, refracted by ice "
                 "crystals in cirrostratus.",
                 "Er ist das erste sichere Zeichen einer anrückenden "
                 "Warmfront.",
                 "It is the first reliable sign of an approaching warm front.")
    sk.sichern(bild, "begriff-halo")


def nebel():
    bild, draw = sk.leinwand()
    deckel = 168
    berg(draw, [(0, BODEN_Y), (74, 104), (164, BODEN_Y)])
    berg(draw, [(290, BODEN_Y), (380, 96), (440, BODEN_Y)])
    # Die Kaltluft sammelt sich im Tal, nicht am Hang: deshalb steht der
    # Nebel unten und die Haenge ragen heraus.
    draw.rectangle([0, deckel * S, 440 * S, BODEN_Y * S], fill=(176, 182, 196))
    schicht(draw, -20, 460, deckel - 8, 10, (206, 212, 224), seed=97)
    sonne(draw, 372, 56, 12)
    sk.gestrichelt(draw, 10, deckel - 26, 430, deckel - 26, WARN, 1, 7)
    beschrift(draw, 424, deckel - 44, "Inversion", "inversion", 10, WARN,
              rechts=True)
    beschrift(draw, 150, deckel + 18, "Nebel im Tal", "fog in the valley", 11,
              (40, 44, 54), mitte=True)
    beschrift(draw, 20, 70, "oben klar und sonnig", "clear and sunny above",
              10, TEXT)
    beschrift(draw, 20, 200, "Sicht unter 1 km", "visibility below 1 km", 10,
              (40, 44, 54))
    beschrift(draw, 80, 86, "Hänge ragen heraus", "slopes stick out", 10,
              TEXT, mitte=True)
    boden(draw)

    unterschrift(draw,
                 "Nebel ist eine Wolke am Boden: die klare, windstille Nacht "
                 "kühlt die Luft bis zum Taupunkt.",
                 "Fog is a cloud on the ground: a clear, calm night cools the "
                 "air to its dew point.",
                 "Hebt der Wind ihn an, wird Hochnebel daraus.",
                 "If wind lifts it, it becomes low stratus.")
    sk.sichern(bild, "begriff-nebel")


# ---------------------------------------------------------------------------
# Fliegen
# ---------------------------------------------------------------------------

def sinken(v):
    """Die Polare eines mittleren Segelflugzeugs: v in km/h, Sinken in m/s.

    Eine Parabel ist nicht die Wahrheit, trifft aber die beiden Punkte, auf
    die es ankommt -- geringstes Sinken bei 75 km/h, bestes Gleiten E 38 --
    und bleibt nachrechenbar."""
    return 0.60 + 0.000263 * (v - 75.0) ** 2


def polarfeld(draw, x0=76, y0=80, sv=1.75, sw=30.0, v_bis=172):
    """Das Achsenkreuz der Polare samt Kurve.

    Der Nullpunkt liegt bei v = 0, obwohl die Kurve erst bei 55 km/h
    anfaengt: nur von dort aus ist die Tangente die Gleitzahl, und genau
    diese Konstruktion soll das Bild zeigen. Die Zahlen an der Fahrtachse
    stehen darueber, weil darunter die Kurve liegt.
    """
    def px(v):
        return x0 + v * sv

    def py(w):
        return y0 + w * sw

    sk.strich(draw, x0, y0, px(v_bis) + 8, y0, DUENN, 1)
    sk.strich(draw, x0, y0 - 6, x0, py(4.0), DUENN, 1)
    for v in (60, 90, 120, 150):
        sk.strich(draw, px(v), y0 - 4, px(v), y0 + 4, DUENN, 1)
        sk.text(draw, px(v), y0 - 17, "%d" % v, 9, DUENN, True)
    for w in (1, 2, 3):
        sk.strich(draw, x0 - 4, py(w), x0 + 4, py(w), DUENN, 1)
        sk.text(draw, x0 - 8, py(w) - 6, "%d" % w, 9, DUENN, False, True)
    punkte = []
    v = 55.0
    while v <= v_bis:
        punkte.append((px(v) * S, py(sinken(v)) * S))
        v += 1.0
    draw.line(punkte, fill=WOLKE, width=2 * S, joint="curve")
    return px, py


def _strahl(draw, x0, y0, x1, y1, farbe, dicke=1, ueber=1.22):
    """Die Tangente, ueber ihren Beruehrpunkt hinaus verlaengert."""
    sk.strich(draw, x0, y0, x0 + (x1 - x0) * ueber, y0 + (y1 - y0) * ueber,
              farbe, dicke)


def polare():
    bild, draw = sk.leinwand()
    px, py = polarfeld(draw)
    beschrift(draw, 418, 92, "Fahrt [km/h]", "airspeed [km/h]", 10, DUENN,
              rechts=True)
    beschrift(draw, 40, 216, "Sinken [m/s]", "sink [m/s]", 10, DUENN)

    vs = 75.0
    vg = min(range(56, 172), key=lambda v: sinken(v) / v)
    _strahl(draw, 76, 80, px(vg), py(sinken(vg)), WARN, 1, 1.30)
    sk.gestrichelt(draw, 76, py(sinken(vs)), px(vs), py(sinken(vs)), GUT, 1, 6)
    kreis(draw, px(vs), py(sinken(vs)), 4, GUT)
    kreis(draw, px(vg), py(sinken(vg)), 4, WARN)

    # Die Beschriftung steht links unten, wo die Kurve nicht hinkommt.
    sk.gestrichelt(draw, 150, 146, px(vs) - 5, py(sinken(vs)) + 5, GUT, 1, 5)
    beschrift(draw, 84, 150, "geringstes Sinken", "minimum sink", 10, GUT)
    beschrift(draw, 84, 165, "75 km/h, 0,60 m/s", "75 km/h, 0.60 m/s", 10, GUT)
    sk.gestrichelt(draw, 176, 190, px(vg) - 5, py(sinken(vg)) + 6, WARN, 1, 5)
    beschrift(draw, 84, 186, "bestes Gleiten", "best glide", 10, WARN)
    beschrift(draw, 84, 201, "%d km/h, E = 38" % vg, "%d km/h, E = 38" % vg,
              10, WARN)

    unterschrift(draw,
                 "Die Polare sagt für jede Fahrt, wie schnell man dabei "
                 "sinkt.",
                 "The polar gives the sink rate for every airspeed.",
                 "Der tiefste Punkt ist das geringste Sinken, die Tangente "
                 "vom Nullpunkt das beste Gleiten.",
                 "The lowest point is minimum sink, the tangent from the "
                 "origin is best glide.")
    sk.sichern(bild, "begriff-polare")


def mccready():
    bild, draw = sk.leinwand()
    px, py = polarfeld(draw, y0=112, sw=26.0)
    steigen = 2.0
    oben = py(-steigen)
    beschrift(draw, 418, 124, "Fahrt [km/h]", "airspeed [km/h]", 10, DUENN,
              rechts=True)

    sk.strich(draw, 70, oben, 82, oben, BETONT, 2)
    kreis(draw, 76, oben, 4, BETONT)
    beschrift(draw, 88, oben - 8, "erwartetes Steigen 2 m/s",
              "expected climb 2 m/s", 10, BETONT)

    vg = min(range(56, 172), key=lambda v: sinken(v) / v)
    _strahl(draw, 76, 112, px(vg), py(sinken(vg)), DUENN, 1, 1.26)
    vm = min(range(56, 172), key=lambda v: (sinken(v) + steigen) / v)
    _strahl(draw, 76, oben, px(vm), py(sinken(vm)), GUT, 2, 1.14)
    kreis(draw, px(vm), py(sinken(vm)), 4, GUT)
    sk.gestrichelt(draw, px(vm), py(sinken(vm)), px(vm), 112, GUT, 1, 6)
    beschrift(draw, px(vm) + 10, 136, "Sollfahrt %d km/h" % vm,
              "speed to fly %d km/h" % vm, 10, GUT)
    beschrift(draw, 84, 190, "ohne Steigen: bestes Gleiten",
              "with no climb: best glide", 10, DUENN)
    beschrift(draw, 84, 205, "mehr Steigen → schneller fliegen",
              "more climb → fly faster", 10, TEXT)

    unterschrift(draw,
                 "McCready: Die Tangente kommt vom erwarteten Steigen, nicht "
                 "vom Nullpunkt.",
                 "McCready: the tangent starts at the expected climb, not at "
                 "the origin.",
                 "Wer stark steigt, darf schnell fliegen.",
                 "Strong climbs allow high speeds.")
    sk.sichern(bild, "begriff-mccready")


def wasserballast():
    bild, draw = sk.leinwand()
    px, py = polarfeld(draw)
    beschrift(draw, 418, 92, "Fahrt [km/h]", "airspeed [km/h]", 10, DUENN,
              rechts=True)
    # Ballast verschiebt jeden Punkt auf seinem Strahl nach rechts unten:
    # schneller und schneller sinkend, aber im selben Winkel.
    f = 1.18
    punkte = []
    v = 55.0 * f
    while v <= 172:
        punkte.append((px(v) * S, py(sinken(v / f) * f) * S))
        v += 1.0
    draw.line(punkte, fill=BETONT, width=2 * S, joint="curve")

    kreis(draw, px(75), py(0.60), 4, WOLKE)
    kreis(draw, px(75 * f), py(0.60 * f), 4, BETONT)
    _strahl(draw, 76, 80, px(75 * f), py(0.60 * f), DUENN, 1, 1.12)
    sk.pfeil(draw, px(75) + 6, py(0.60) + 3, px(75 * f) - 7, py(0.60 * f) - 3,
             TEXT, 1, 5)

    beschrift(draw, 84, 150, "leer: 75 km/h", "empty: 75 km/h", 10, WOLKE)
    beschrift(draw, 84, 166, "mit Ballast: 89 km/h", "ballasted: 89 km/h", 10,
              BETONT)
    beschrift(draw, 84, 190, "derselbe Gleitwinkel,", "the same glide angle,",
              10, TEXT)
    beschrift(draw, 84, 205, "nur schneller", "only faster", 10, TEXT)

    unterschrift(draw,
                 "Wasserballast macht schwerer: jeder Punkt der Polare rückt "
                 "zu höherer Fahrt.",
                 "Ballast makes the glider heavier: every point of the polar "
                 "moves faster.",
                 "Die Gleitzahl bleibt, schwache Thermik wird mühsam.",
                 "The glide ratio stays, weak climbs get worse.")
    sk.sichern(bild, "begriff-wasserballast")


def endanflug():
    bild, draw = sk.leinwand()
    # Der Endanflug ist eine Rechnung mit drei Summanden, und das Bild
    # zeigt sie als drei Strecken uebereinander.
    boden(draw)
    for x in (300, 320, 340, 360):
        sk.strich(draw, x, BODEN_Y - 2, x + 10, BODEN_Y - 2, (210, 216, 228), 2)
    beschrift(draw, 330, 210, "Ziel", "goal", 10, TEXT, mitte=True)

    hoch = 86
    segler(draw, 76, hoch, 0)
    sk.strich(draw, 90, hoch + 6, 330, BODEN_Y - 6, GUT, 2)
    beschrift(draw, 186, 118, "Gleitpfad E = 30", "glide path E = 30", 10, GUT,
              mitte=True)

    sk.pfeil(draw, 52, BODEN_Y, 52, hoch, TEXT, 1)
    sk.pfeil(draw, 52, hoch, 52, BODEN_Y, TEXT, 1)
    beschrift(draw, 60, 136, "benötigte Höhe", "height required", 10, TEXT)
    beschrift(draw, 60, 151, "870 m", "870 m", 11, TEXT)
    sk.pfeil(draw, 110, 212, 300, 212, DUENN, 1, 6)
    sk.pfeil(draw, 300, 212, 110, 212, DUENN, 1, 6)
    beschrift(draw, 205, 194, "20 km", "20 km", 10, DUENN, mitte=True)

    sk.gestrichelt(draw, 300, 190, 424, 190, WARN, 1, 6)
    sk.pfeil(draw, 400, BODEN_Y, 400, 190, WARN, 1)
    sk.pfeil(draw, 400, 190, 400, BODEN_Y, WARN, 1)
    beschrift(draw, 424, 170, "+ Sicherheitshöhe 200 m",
              "+ safety height 200 m", 10, WARN, rechts=True)
    beschrift(draw, 418, 60, "20 km ÷ 30 = 667 m", "20 km ÷ 30 = 667 m", 11,
              TEXT, rechts=True)

    unterschrift(draw,
                 "Endanflug: Strecke durch Gleitzahl, plus Sicherheitshöhe — "
                 "und Gegenwind frisst mit.",
                 "Final glide: distance divided by glide ratio, plus a safety "
                 "height — and headwind eats into it.",
                 "Erst wenn die Höhe sicher reicht, wird der letzte Bart "
                 "verlassen.",
                 "Only when the height is safely there do you leave the last "
                 "thermal.")
    sk.sichern(bild, "begriff-endanflug")


def profil(draw, cx, cy, laenge, winkel, farbe=KOERPER):
    """Ein Fluegelschnitt. Vorne rund, hinten spitz, oben gewoelbt -- und um
    `winkel` gedreht, denn genau darum geht es bei diesen Bildern."""
    form = [(0.00, 0.00), (0.06, -0.055), (0.18, -0.082), (0.36, -0.086),
            (0.60, -0.066), (0.82, -0.036), (1.00, 0.00), (0.80, 0.008),
            (0.55, 0.018), (0.32, 0.022), (0.14, 0.014), (0.04, 0.004)]
    c, s2 = math.cos(math.radians(winkel)), math.sin(math.radians(winkel))
    punkte = []
    for fx, fy in form:
        x = (fx - 0.35) * laenge
        y = fy * laenge
        punkte.append(((cx + x * c - y * s2) * S, (cy + x * s2 + y * c) * S))
    draw.polygon(punkte, fill=farbe)


def profilpunkte(cx, cy, laenge, winkel):
    """Nase und Hinterkante eines gedrehten Profils -- fuer Sehne und Bogen.

    Positiver Winkel heisst Nase hoch: in Bildkoordinaten zeigt y nach
    unten, deshalb liegt die Nase bei positivem Winkel beim kleineren y.
    """
    c, s2 = math.cos(math.radians(winkel)), math.sin(math.radians(winkel))
    nase = (cx - 0.35 * laenge * c, cy - 0.35 * laenge * s2)
    kante = (cx + 0.65 * laenge * c, cy + 0.65 * laenge * s2)
    return nase, kante


def anstellwinkel():
    bild, draw = sk.leinwand()
    alpha = 12.0
    cx, cy = 214, 126
    nase, kante = profilpunkte(cx, cy, 160, alpha)

    sk.gestrichelt(draw, 60, nase[1], 400, nase[1], DUENN, 1, 6)
    for y in (nase[1] - 48, nase[1] - 24, nase[1] + 30, nase[1] + 54):
        sk.pfeil(draw, 64, y, 142, y, BETONT, 1, 5)
    beschrift(draw, 64, nase[1] - 76, "Anströmung", "airflow", 10, BETONT)

    profil(draw, cx, cy, 160, alpha)
    # Die Sehne, ueber beide Enden hinaus gezogen, damit der Winkel steht.
    rx, ry = kante[0] - nase[0], kante[1] - nase[1]
    sk.strich(draw, nase[0] - 0.08 * rx, nase[1] - 0.08 * ry,
              nase[0] + 1.5 * rx, nase[1] + 1.5 * ry, WARN, 1)
    sk.bogen(draw, nase[0], nase[1], 104, 0, alpha, WARN, 1)
    beschrift(draw, nase[0] + 112, nase[1] + 2, "α", "α", 14, WARN)
    beschrift(draw, nase[0] + 128, nase[1] + 6, "Anstellwinkel",
              "angle of attack", 10, WARN)
    beschrift(draw, 346, 166, "Sehne", "chord", 10, WARN)

    sk.pfeil(draw, 70, 214, 170, 214, TEXT, 2)
    beschrift(draw, 178, 208, "die Flugbahn zählt, nicht der Horizont",
              "the flight path counts, not the horizon", 10, TEXT)

    unterschrift(draw,
                 "Der Anstellwinkel liegt zwischen Flügelsehne und "
                 "Anströmung.",
                 "The angle of attack lies between chord and airflow.",
                 "Nicht zwischen Nase und Horizont — und er allein "
                 "bestimmt den Auftrieb.",
                 "Not between nose and horizon — and it alone sets the "
                 "lift.")
    sk.sichern(bild, "begriff-anstellwinkel")


def ueberziehen():
    bild, draw = sk.leinwand()
    # Links zweimal derselbe Fluegel, nur anders angestellt.
    for cy, a, farbe, de, en in (
            (84, 4.0, GUT, "kleiner Winkel: die Strömung liegt an",
             "small angle: the flow stays attached"),
            (176, 18.0, ROT, "zu großer Winkel: sie reißt ab",
             "too large: it separates")):
        nase, kante = profilpunkte(130, cy, 112, a)
        sk.gestrichelt(draw, 28, nase[1], 240, nase[1], DUENN, 1, 6)
        profil(draw, 130, cy, 112, a)
        beschrift(draw, 28, cy + 30, de, en, 10, farbe)

    for dy in (18, 28):
        punkte = [(x * S, (84 - dy - 9 * math.exp(-((x - 130) / 46.0) ** 2)) * S)
                  for x in range(32, 240, 3)]
        draw.line(punkte, fill=BETONT, width=1 * S, joint="curve")
    sk.pfeil(draw, 32, 150, 96, 156, BETONT, 1, 5)
    for x, y in ((140, 158), (166, 150), (192, 156), (216, 148)):
        wirbel(draw, x, y, 9, ROT, 1, -1)

    sk.strich(draw, 258, 32, 258, 220, DUENN, 1)
    achsen(draw, 286, 200, 418, 62, "α →", "α →", "", "")
    beschrift(draw, 292, 62, "Auftrieb", "lift", 10, DUENN)
    punkte = []
    for a in range(0, 23):
        ca = 0.11 * a if a <= 16 else 0.11 * 16 - 0.055 * (a - 16)
        punkte.append(((286 + a * 5.6) * S, (200 - ca * 64) * S))
    draw.line(punkte, fill=WOLKE, width=2 * S, joint="curve")
    spitze = (286 + 16 * 5.6, 200 - 0.11 * 16 * 64)
    kreis(draw, spitze[0], spitze[1], 4, ROT)
    beschrift(draw, 424, 36, "kritischer Winkel ≈ 16°",
              "critical angle ≈ 16°", 10, ROT, rechts=True)
    sk.gestrichelt(draw, 356, 52, spitze[0] + 2, spitze[1] - 8, ROT, 1, 5)

    unterschrift(draw,
                 "Überziehen heißt: der Anstellwinkel wurde zu "
                 "groß, die Strömung reißt ab.",
                 "A stall means the angle of attack grew too large and the "
                 "flow separated.",
                 "Das hängt nicht an der Fahrt, nur am Winkel.",
                 "It depends on the angle, not on the speed.")
    sk.sichern(bild, "begriff-ueberziehen")


def trudeln():
    bild, draw = sk.leinwand()
    # Links, warum es anfaengt: eine Flaeche stroemt ab, die andere traegt.
    beschrift(draw, 106, 20, "eine Fläche strömt ab", "one wing stalls", 10,
              TEXT, mitte=True)
    sk.strich(draw, 40, 84, 172, 68, KOERPER, 3)
    kreis(draw, 106, 76, 5, KOERPER)
    for x, y in ((56, 92), (72, 90)):
        wirbel(draw, x, y, 8, ROT, 1, -1)
    beschrift(draw, 34, 114, "abgerissen", "stalled", 10, ROT)
    sk.pfeil(draw, 150, 56, 168, 48, GUT, 1, 5)
    beschrift(draw, 168, 56, "trägt", "flying", 10, GUT)
    wirbel(draw, 106, 76, 36, WARN, 2, -1)
    beschrift(draw, 106, 120, "Autorotation", "autorotation", 10, WARN,
              mitte=True)

    # Rechts die Bahn: eine enge, steile Schraube.
    sk.strich(draw, 268, 32, 268, 220, DUENN, 1)
    for i in range(6):
        y = 48 + i * 24
        ring(draw, 342, y, 44 - i * 2, 11, BETONT, 1)
    segler_oben(draw, 342, 48, 0, 26)
    beschrift(draw, 424, 186, "steil, eng,", "steep, tight,", 10, BETONT,
              rechts=True)
    beschrift(draw, 424, 201, "hoher Höhenverlust", "big height loss", 10,
              BETONT, rechts=True)

    unterschrift(draw,
                 "Trudeln: Eine Fläche ist abgerissen, die andere trägt.",
                 "A spin: one wing is stalled, the other still flies.",
                 "Ausleiten: Querruder neutral, Seitenruder gegen, Knüppel "
                 "nach vorn.",
                 "Recovery: ailerons neutral, full opposite rudder, stick "
                 "forward.")
    sk.sichern(bild, "begriff-trudeln")


def kurbeln():
    bild, draw = sk.leinwand()
    # Von oben. Der Kern ist klein; wer ihn nicht trifft, kurbelt im
    # schwachen Rand und wundert sich.
    cx, cy = 180, 120
    for r, farbe in ((74, (34, 46, 66)), (50, (44, 64, 94)), (26, (58, 92, 140))):
        kreis(draw, cx, cy, r, farbe)
    beschrift(draw, cx, cy - 8, "Kern", "core", 10, TEXT, mitte=True)
    beschrift(draw, cx, cy + 8, "3 m/s", "3 m/s", 10, TEXT, mitte=True)

    ring_strichelt(draw, cx + 44, cy + 30, 58, DUENN, 1)
    segler_oben(draw, cx + 102, cy + 30, 90, 24, DUENN)
    beschrift(draw, 298, 198, "daneben: 1 m/s", "off centre: 1 m/s", 10, DUENN)

    ring(draw, cx, cy, 36, 36, GUT, 2)
    segler_oben(draw, cx + 36, cy, 90, 24, GUT)
    sk.pfeil(draw, cx + 30, cy + 40, cx + 8, cy + 22, GUT, 2, 6)
    beschrift(draw, 20, 46, "versetzen, bis das Steigen stimmt",
              "shift until the climb is right", 10, GUT)
    beschrift(draw, 20, 206, "45° Querlage, Ø ≈ 150 m",
              "45° bank, Ø ≈ 150 m", 10, TEXT)
    sk.pfeil(draw, 300, 60, 364, 84, BETONT, 2)
    beschrift(draw, 310, 42, "Wind versetzt mit",
              "the wind drifts you along", 10, BETONT)

    unterschrift(draw,
                 "Kurbeln heißt kreisen, bis die Wolke erreicht ist — eng "
                 "genug, um im Kern zu bleiben.",
                 "Circling means turning until the cloud is reached — tight "
                 "enough to stay in the core.",
                 "Wo es weniger steigt, wird der Kreis versetzt, nicht "
                 "vergrößert.",
                 "Where the climb is weaker you shift the circle, not enlarge "
                 "it.")
    sk.sichern(bild, "begriff-kurbeln")


def dichtehoehe():
    bild, draw = sk.leinwand()
    grund, oben = 206, 56          # 0 m und 2000 m auf der Skala rechts
    sx = 318

    def hy(h):
        return grund - (grund - oben) * h / 2000.0

    draw.rectangle([30 * S, (grund - 6) * S, 286 * S, grund * S],
                   fill=(96, 102, 112))
    sk.pfeil(draw, 40, grund - 20, 146, grund - 20, GUT, 2)
    beschrift(draw, 40, grund - 40, "15 °C: kurze Startstrecke",
              "15 °C: short take-off run", 10, GUT)
    sk.pfeil(draw, 40, grund + 14, 236, grund + 14, ROT, 2)
    beschrift(draw, 40, grund + 18, "35 °C: längere Startstrecke",
              "35 °C: longer take-off run", 10, ROT)

    # Die Skala: dieselbe Druckhoehe, zwei verschiedene Dichtehoehen.
    sk.strich(draw, sx, grund, sx, oben - 6, DUENN, 1)
    for h in (0, 500, 1000, 1500, 2000):
        sk.strich(draw, sx - 4, hy(h), sx + 4, hy(h), DUENN, 1)
        sk.text(draw, sx - 8, hy(h) - 6, "%d" % h, 9, DUENN, False, True)
    beschrift(draw, sx - 30, oben - 22, "Höhe [m]", "height [m]", 10, DUENN)

    sk.gestrichelt(draw, 250, hy(400), sx, hy(400), BETONT, 1, 6)
    kreis(draw, sx, hy(400), 4, BETONT)
    beschrift(draw, sx + 10, hy(400) - 14, "Druckhöhe",
              "pressure altitude", 10, BETONT)
    beschrift(draw, sx + 10, hy(400) + 1, "400 m", "400 m", 10, BETONT)
    sk.gestrichelt(draw, 236, hy(1100), sx, hy(1100), ROT, 1, 6)
    kreis(draw, sx, hy(1100), 4, ROT)
    beschrift(draw, sx + 10, hy(1100) - 14, "Dichtehöhe",
              "density altitude", 10, ROT)
    beschrift(draw, sx + 10, hy(1100) + 1, "1100 m", "1100 m", 10, ROT)
    sk.pfeil(draw, sx - 22, hy(430), sx - 22, hy(1070), ROT, 2, 6)
    beschrift(draw, sx - 28, hy(750) - 7, "+ 20 °C", "+ 20 °C", 10,
              ROT, rechts=True)

    unterschrift(draw,
                 "Die Dichtehöhe ist die Höhe, in der die Luft bei "
                 "Normbedingungen so dünn wäre wie hier und heute.",
                 "Density altitude is the height at which standard air would "
                 "be as thin as the air here today.",
                 "Warm heißt dünn heißt: längere Startstrecke, schlechteres "
                 "Steigen.",
                 "Warm means thin means: longer take-off run, poorer climb.")
    sk.sichern(bild, "begriff-dichtehoehe")


def hoehenbezuege():
    bild, draw = sk.leinwand()
    # Drei Nullpunkte uebereinander. Welcher gilt, sagt allein die
    # Einstellung am Hoehenmesser -- die Hoehe selbst aendert sich nicht.
    # Die Reihenfolge ist nicht frei: der QNH liegt um 1013 herum, also
    # liegt die 1013er Flaeche dicht bei NN -- nie ueber dem Platz. Hier ein
    # Hochdrucktag mit QNH 1030, da liegt sie 141 m ueber NN.
    nn, platz, fl = 200, 148, 178
    for y, farbe, de, en in ((fl, WARN, "FL: Flugfläche", "FL: flight level"),
                             (platz, GUT, "QFE: 0 am Platz",
                              "QFE: 0 at the field"),
                             (nn, BETONT, "QNH: über NN", "QNH: above MSL")):
        sk.strich(draw, 86, y, 300, y, farbe, 2)
        beschrift(draw, 308, y - 7, de, en, 10, farbe)
    beschrift(draw, 82, fl - 7, "1013", "1013", 10, WARN, rechts=True)
    beschrift(draw, 82, platz - 7, "Platz", "field", 10, GUT, rechts=True)
    beschrift(draw, 82, nn - 7, "NN", "MSL", 10, BETONT, rechts=True)

    boden(draw, platz, 86, 300, ERDE, 4)
    segler(draw, 200, 66, 0)
    sk.gestrichelt(draw, 86, 58, 300, 58, DUENN, 1, 6)
    beschrift(draw, 86, 38, "dieselbe Höhe, drei Zahlen",
              "one height, three numbers", 10, TEXT)

    # Die drei Zahlen gehoeren zusammen: Platz 450 m ueber NN, Segler
    # 1050 m ueber NN, also 600 m ueber dem Platz. Ueber der 1013er Flaeche
    # (141 m ueber NN) bleiben 909 m = 2982 ft, das ist FL 30.
    sk.pfeil(draw, 118, 62, 118, nn, BETONT, 1)
    beschrift(draw, 124, 120, "1050 m", "1050 m", 10, BETONT)
    sk.pfeil(draw, 250, 62, 250, platz, GUT, 1)
    beschrift(draw, 256, 100, "600 m", "600 m", 10, GUT)
    sk.pfeil(draw, 184, 62, 184, fl, WARN, 1)
    beschrift(draw, 190, 128, "FL 30", "FL 30", 10, WARN)

    unterschrift(draw,
                 "Der Höhenmesser zählt von dem Druck an, den man ihm "
                 "einstellt.",
                 "The altimeter counts from whatever pressure you set on it.",
                 "QNH über NN, QFE über dem Platz, 1013 hPa als Flugfläche.",
                 "QNH above sea level, QFE above the field, 1013 hPa as a "
                 "flight level.")
    sk.sichern(bild, "begriff-hoehenbezuege")


def platzrunde():
    bild, draw = sk.leinwand()
    # Von oben. Gelandet wird nach unten (gegen den Wind), also liegt die
    # linke Platzrunde rechts der Bahn: alle drei Kurven gehen nach links.
    draw.rectangle([186 * S, 86 * S, 208 * S, 198 * S], fill=(96, 102, 112))
    sk.strich(draw, 197, 94, 197, 190, (226, 230, 240), 1)
    beschrift(draw, 180, 150, "Landebahn", "runway", 10, TEXT, rechts=True)

    sk.pfeil(draw, 80, 196, 80, 140, BETONT, 2)
    beschrift(draw, 80, 206, "Wind", "wind", 10, BETONT, mitte=True)

    bahn = [(292, 204), (292, 86), (197, 86), (197, 184)]
    for i in range(len(bahn) - 1):
        sk.pfeil(draw, bahn[i][0], bahn[i][1], bahn[i + 1][0], bahn[i + 1][1],
                 GUT, 2)
    segler_oben(draw, 292, 150, -90, 22, GUT)
    beschrift(draw, 302, 150, "Gegenanflug", "downwind", 10, GUT)
    beschrift(draw, 244, 64, "Queranflug", "base", 10, GUT, mitte=True)
    beschrift(draw, 212, 150, "Endanflug", "final", 10, GUT)
    beschrift(draw, 302, 200, "Einteilung ab 300 m", "join at 300 m", 10, TEXT,
              rechts=True)

    beschrift(draw, 24, 48, "linke Platzrunde:", "left-hand circuit:", 10, TEXT)
    beschrift(draw, 24, 63, "alle Kurven nach links", "all turns to the left",
              10, TEXT)
    wirbel(draw, 72, 110, 24, TEXT, 2, -1)

    unterschrift(draw,
                 "Die Platzrunde ist ein festes Rechteck: Gegenanflug, "
                 "Queranflug, Endanflug.",
                 "The circuit is a fixed rectangle: downwind, base, final.",
                 "Gelandet wird gegen den Wind, eingeteilt in fester Höhe.",
                 "You land into wind and join at a fixed height.")
    sk.sichern(bild, "begriff-platzrunde")


def aussenlandung():
    bild, draw = sk.leinwand()
    # Von oben: vier Felder, und nur eines taugt. Gesucht wird lang, eben,
    # frei und gegen den Wind.
    sk.pfeil(draw, 30, 40, 92, 40, BETONT, 2)
    beschrift(draw, 98, 32, "Wind", "wind", 10, BETONT)

    draw.rectangle([30 * S, 72 * S, 194 * S, 140 * S], fill=(62, 78, 52))
    sk.strich(draw, 30, 72, 194, 72, GUT, 2)
    sk.strich(draw, 30, 140, 194, 140, GUT, 2)
    sk.pfeil(draw, 180, 106, 44, 106, GUT, 2)
    beschrift(draw, 112, 84, "lang, eben, frei", "long, flat, clear", 10, GUT,
              mitte=True)
    beschrift(draw, 112, 118, "gegen den Wind", "into wind", 10, GUT,
              mitte=True)

    draw.rectangle([226 * S, 72 * S, 410 * S, 126 * S], fill=(58, 58, 48))
    for x in range(232, 406, 18):
        sk.strich(draw, x, 100, x + 10, 100, (120, 120, 100), 2)
    sk.strich(draw, 226, 86, 410, 86, ROT, 2)
    for x in (250, 310, 370):
        sk.strich(draw, x, 78, x, 94, ROT, 2)
    beschrift(draw, 318, 60, "Leitung, hohe Frucht", "wires, tall crop", 10,
              ROT, mitte=True)

    draw.rectangle([226 * S, 150 * S, 410 * S, 212 * S], fill=(58, 58, 48))
    for i in range(5):
        sk.strich(draw, 236 + i * 4, 206 - i * 10, 400 - i * 6, 196 - i * 10,
                  (92, 92, 78), 1)
    beschrift(draw, 318, 160, "Hang und Gräben", "slope and ditches", 10, ROT,
              mitte=True)

    draw.rectangle([30 * S, 158 * S, 132 * S, 212 * S], fill=(58, 58, 48))
    beschrift(draw, 82, 178, "zu kurz", "too short", 10, ROT, mitte=True)
    segler_oben(draw, 170, 180, -62, 24, TEXT)

    unterschrift(draw,
                 "Außenlandung: Das Feld wird nach Größe, Neigung, Oberfläche "
                 "und Hindernissen gewählt.",
                 "Field landing: choose by size, slope, surface and "
                 "obstacles.",
                 "Früh entscheiden, bei 300 m steht das Feld fest.",
                 "Decide early — by 300 m the field is settled.")
    sk.sichern(bild, "begriff-aussenlandung")


def seilriss():
    bild, draw = sk.leinwand()
    boden(draw)
    entscheid = 150
    sk.gestrichelt(draw, 24, entscheid, 420, entscheid, WARN, 1, 7)
    beschrift(draw, 24, entscheid - 18, "Entscheidungshöhe",
              "decision height", 10, WARN)

    punkte = []
    for i in range(41):
        t = i / 40.0
        x = 40 + t * 150
        y = BODEN_Y - 6 - (1 - math.cos(t * math.pi / 2)) * 160
        punkte.append((x * S, y * S))
    draw.line(punkte, fill=KOERPER, width=2 * S, joint="curve")
    beschrift(draw, 76, 200, "Windenstart", "winch launch", 10, TEXT,
              rechts=True)

    # Zwei Rissstellen, zwei verschiedene Antworten.
    for y, farbe, de, en in ((196, ROT, "tief: geradeaus landen",
                              "low: land straight ahead"),
                             (104, GUT, "hoch: verkürzte Platzrunde",
                              "high: abbreviated circuit")):
        x = 40 + 150 * (2 / math.pi) * math.acos(
            1 - (BODEN_Y - 6 - y) / 160.0)
        sk.strich(draw, x - 7, y - 7, x + 7, y + 7, ROT, 2)
        sk.strich(draw, x - 7, y + 7, x + 7, y - 7, ROT, 2)
        if farbe is ROT:
            sk.strich(draw, x, y, 300, BODEN_Y - 6, ROT, 2)
            beschrift(draw, 40, 62, de, en, 10, farbe)
        else:
            sk.strich(draw, x, y, 296, 72, GUT, 2)
            sk.strich(draw, 296, 72, 376, 146, GUT, 2)
            sk.strich(draw, 376, 146, 300, BODEN_Y - 6, GUT, 2)
            beschrift(draw, 40, 42, de, en, 10, farbe)
        sk.strich(draw, 26, 48 + (20 if farbe is ROT else 0),
                  34, 48 + (20 if farbe is ROT else 0), farbe, 2)

    unterschrift(draw,
                 "Seilriss: Zuerst nachdrücken, dann entscheiden.",
                 "Cable break: lower the nose first, then decide.",
                 "Unter der Entscheidungshöhe wird geradeaus gelandet, "
                 "darüber eine verkürzte Platzrunde geflogen.",
                 "Below the decision height you land ahead, above it you fly "
                 "an abbreviated circuit.")
    sk.sichern(bild, "begriff-seilriss")


def staudruck():
    bild, draw = sk.leinwand()
    # Der Rumpf im Schnitt: vorne der Staurohr-Anschluss, seitlich die
    # statischen Bohrungen. Was die beiden unterscheidet, ist der Staudruck.
    # Der Rumpf endet vor dem Kasten des Fahrtmessers (ab x=252). Reichte
    # er wie zuvor bis x=348, lief die Spitze quer durch die ersten
    # Buchstaben von "Gesamtdruck" und "statischer Druck".
    draw.polygon([(60 * S, 120 * S), (96 * S, 102 * S), (200 * S, 102 * S),
                  (244 * S, 112 * S), (200 * S, 140 * S), (96 * S, 140 * S)],
                 fill=(60, 66, 80), outline=LINIE, width=1 * S)
    sk.strich(draw, 34, 121, 60, 121, KOERPER, 3)
    kreis(draw, 34, 121, 4, KOERPER)
    for y in (84, 96, 146, 158):
        sk.pfeil(draw, 12, y, 54, y, BETONT, 1, 5)
    beschrift(draw, 56, 36, "Anströmung v", "airflow v", 10, BETONT)
    beschrift(draw, 56, 176, "Staurohr", "pitot tube", 10, WARN)
    sk.pfeil(draw, 54, 176, 38, 130, WARN, 1, 5)

    for x in (176, 190):
        kreis(draw, x, 139, 3, TEXT)
    beschrift(draw, 183, 84, "statische Bohrungen", "static ports", 10, GUT,
              mitte=True)
    sk.pfeil(draw, 183, 98, 183, 132, GUT, 1, 5)

    sk.strich(draw, 34, 118, 34, 56, WARN, 1)
    sk.strich(draw, 34, 56, 252, 56, WARN, 1)
    sk.strich(draw, 190, 144, 190, 196, GUT, 1)
    sk.strich(draw, 190, 196, 252, 196, GUT, 1)
    draw.rectangle([252 * S, 44 * S, 400 * S, 208 * S], outline=LINIE,
                   width=1 * S)
    beschrift(draw, 326, 56, "Fahrtmesser", "airspeed indicator", 11, TEXT,
              mitte=True)
    beschrift(draw, 326, 100, "Gesamtdruck", "total pressure", 10, WARN,
              mitte=True)
    beschrift(draw, 326, 118, "−  statischer Druck", "−  static pressure", 10,
              GUT, mitte=True)
    sk.strich(draw, 266, 136, 386, 136, DUENN, 1)
    beschrift(draw, 326, 142, "=  Staudruck q", "=  dynamic pressure q", 10,
              TEXT, mitte=True)
    beschrift(draw, 326, 170, "q = ½ · ρ · v²", "q = ½ · ρ · v²", 12, GUT,
              mitte=True)

    unterschrift(draw,
                 "Vorn misst das Staurohr den Gesamtdruck, seitlich messen "
                 "die Bohrungen den statischen Druck.",
                 "The pitot tube at the front measures total pressure, the "
                 "ports on the side measure static pressure.",
                 "Die Differenz ist der Staudruck — daraus kommt die Fahrt.",
                 "The difference is the dynamic pressure — and from it the "
                 "airspeed.")
    sk.sichern(bild, "begriff-staudruck")


def variometer():
    bild, draw = sk.leinwand()
    # Eine Flasche, ein Loch nach draussen, und dazwischen misst etwas den
    # Durchzug. Mehr ist ein Variometer nicht.
    draw.rounded_rectangle([60 * S, 104 * S, 150 * S, 196 * S], 8 * S,
                           fill=(46, 52, 66), outline=LINIE, width=1 * S)
    beschrift(draw, 105, 136, "Ausgleichs-", "reference", 10, TEXT, mitte=True)
    beschrift(draw, 105, 151, "gefäß", "flask", 10, TEXT, mitte=True)
    sk.strich(draw, 150, 128, 206, 128, LINIE, 2)
    draw.rectangle([206 * S, 110 * S, 254 * S, 146 * S], fill=(60, 66, 80),
                   outline=LINIE, width=1 * S)
    beschrift(draw, 230, 92, "Messglied", "flow sensor", 10, GUT, mitte=True)
    sk.strich(draw, 254, 128, 330, 128, LINIE, 2)
    sk.strich(draw, 330, 128, 330, 104, LINIE, 2)
    kreis(draw, 330, 100, 5, KOERPER)
    beschrift(draw, 424, 72, "Düse: statischer Druck",
              "nozzle: static pressure", 10, TEXT, rechts=True)

    sk.pfeil(draw, 160, 118, 300, 118, BETONT, 2)
    beschrift(draw, 230, 60, "Steigen: Luft strömt heraus",
              "climbing: air flows out", 10, BETONT, mitte=True)
    sk.pfeil(draw, 300, 160, 160, 160, WARN, 2)
    beschrift(draw, 230, 176, "Sinken: Luft strömt hinein",
              "sinking: air flows in", 10, WARN, mitte=True)

    unterschrift(draw,
                 "Das Variometer misst den Luftstrom zwischen Gefäß und "
                 "Außendruck.",
                 "The vario measures the airflow between flask and outside "
                 "pressure.",
                 "Beim Steigen fällt der Außendruck, das Gefäß bläst aus.",
                 "Climbing lowers the outside pressure and the flask blows "
                 "out.")
    sk.sichern(bild, "begriff-variometer")


# ---------------------------------------------------------------------------
# Noch ein paar Lagen am Himmel und am Platz
# ---------------------------------------------------------------------------

def abwind():
    bild, draw = sk.leinwand()
    basis_y = 104
    # Was in den Schlaeuchen hochgeht, kommt daneben wieder herunter. Das
    # Bild soll zeigen, dass das Sinken dazwischen die Regel ist, nicht das
    # Pech.
    for x in (92, 350):
        haufen(draw, x, basis_y, 70, 44, seed=211 + x)
        for y in (206, 176, 146):
            sk.pfeil(draw, x, y, x, y - 22, GUT, 2, 6)
    for x in (178, 222, 266):
        for y in (130, 170):
            sk.pfeil(draw, x, y, x, y + 26, ROT, 2, 6)
    beschrift(draw, 222, 108, "Abwind", "sink", 11, ROT, mitte=True)
    beschrift(draw, 92, 216, "Steigen", "lift", 10, GUT, mitte=True)
    beschrift(draw, 350, 216, "Steigen", "lift", 10, GUT, mitte=True)

    segler(draw, 286, 210, -4)
    sk.pfeil(draw, 268, 210, 150, 210, TEXT, 2)
    beschrift(draw, 222, 192, "schnell durchfliegen", "fly through fast", 10,
              TEXT, mitte=True)
    boden(draw)

    unterschrift(draw,
                 "Was im Bart aufsteigt, sinkt daneben wieder ab — der "
                 "Abwind gehört zur Thermik dazu.",
                 "What rises in the thermal comes down beside it — sink is "
                 "part of the deal.",
                 "Darum wird er mit Fahrt durchflogen, nicht langsam "
                 "ausgesessen.",
                 "So you fly through it with speed instead of sitting it out "
                 "slowly.")
    sk.sichern(bild, "begriff-abwind")


def tagesgang():
    bild, draw = sk.leinwand()
    x0, y0 = 60, 206
    achsen(draw, x0, y0, 412, 40, "", "", "", "")
    # Unter die Achse, nicht daneben: rechts oben faellt die Basiskurve
    # genau durch die Stelle, an der die Achsenbeschriftung stand.
    beschrift(draw, 412, 226, "Uhrzeit", "time of day", 10, DUENN,
              rechts=True)
    for std in (8, 10, 12, 14, 16, 18, 20):
        x = x0 + (std - 8) * 28
        sk.strich(draw, x, y0 - 4, x, y0 + 4, DUENN, 1)
        sk.text(draw, x, y0 + 8, "%d" % std, 9, DUENN, True)

    def kurve(hoehe, versatz, farbe, dicke=2):
        punkte = []
        t = 8.0
        while t <= 20.0:
            w = max(0.0, math.sin((t - 9.5 + versatz) / 9.0 * math.pi))
            punkte.append(((x0 + (t - 8) * 28) * S,
                           (y0 - w ** 0.8 * hoehe) * S))
            t += 0.25
        draw.line(punkte, fill=farbe, width=dicke * S, joint="curve")

    kurve(126, 0.0, GUT)
    kurve(96, -1.5, BETONT)
    # "climb rate" ist breiter als "Steigen" und stiess an "best hours";
    # darum weiter links. Die Basisbeschriftung haengt jetzt unter ihrer
    # Kurve, vorher lag sie darauf.
    beschrift(draw, 150, 52, "Steigen", "climb rate", 10, GUT)
    beschrift(draw, 300, 130, "Basishöhe", "cloud base", 10, BETONT,
              rechts=True)

    sk.gestrichelt(draw, x0 + 56, 60, x0 + 56, y0, DUENN, 1, 6)
    beschrift(draw, x0 + 50, 70, "Auslösung", "trigger", 10, TEXT, rechts=True)
    sk.gestrichelt(draw, x0 + 168, 60, x0 + 168, y0, DUENN, 1, 6)
    beschrift(draw, x0 + 176, 50, "beste Zeit", "best hours", 10, TEXT)
    beschrift(draw, 336, 176, "abends weich", "soft in the evening", 10, TEXT,
              rechts=True)

    unterschrift(draw,
                 "Der Tag hat einen Gang: Auslösung am Vormittag, das Beste "
                 "zwischen 13 und 16 Uhr.",
                 "The day has a rhythm: trigger in the morning, the best of "
                 "it between 13:00 and 16:00.",
                 "Die Basis steigt noch, wenn das Steigen schon nachlässt.",
                 "The base is still rising when the climbs already weaken.")
    sk.sichern(bild, "begriff-tagesgang")


def windenstart():
    bild, draw = sk.leinwand()
    boden(draw)
    # Winde rechts, Flugzeug links: das Seil zieht nach unten vorn, und
    # deshalb steigt es steil und endet in 400 m.
    draw.rectangle([380 * S, (BODEN_Y - 20) * S, 414 * S, BODEN_Y * S],
                   fill=(70, 76, 90), outline=LINIE, width=1 * S)
    beschrift(draw, 362, 200, "Winde", "winch", 10, TEXT, rechts=True)

    punkte = []
    for i in range(49):
        t = i / 48.0
        x = 44 + t * 240
        y = BODEN_Y - 6 - (1 - math.cos(t * math.pi / 2)) * 158
        punkte.append((x * S, y * S))
    draw.line(punkte, fill=KOERPER, width=2 * S, joint="curve")
    # Die Bahn steigt nach rechts weg, also liegt links von ihr alles frei.
    # Jede Beschriftung endet dort, wo die Bahn noch tiefer verlaeuft als
    # ihre Unterkante -- vorher lief die weisse Bahn quer durch die weisse
    # Schrift. Die Stuetzlinie fuehrt vom Punkt auf der Bahn zum Wort.
    for t, de, en, lx, ly, tx, ty in (
            (0.06, "Anrollen", "ground run", 74, 200, 124, 186),
            (0.32, "Übergangsbogen", "transition", 140, 168, 170, 150),
            (0.66, "Steigflug", "full climb", 186, 134, 182, 118)):
        x = 44 + t * 240
        y = BODEN_Y - 6 - (1 - math.cos(t * math.pi / 2)) * 158
        sk.strich(draw, x, y, lx, ly, DUENN, 1)
        beschrift(draw, tx, ty, de, en, 10, TEXT, rechts=True)

    segler(draw, 284, 64, -52)
    sk.strich(draw, 284, 70, 384, BODEN_Y - 14, WARN, 1)
    beschrift(draw, 330, 120, "Seil", "cable", 10, WARN)
    sk.pfeil(draw, 284, 56, 318, 44, GUT, 2)
    beschrift(draw, 324, 36, "ausklinken", "release", 10, GUT)
    sk.pfeil(draw, 16, BODEN_Y, 16, 64, TEXT, 1)
    beschrift(draw, 22, 140, "≈ 400 m", "≈ 400 m", 10, TEXT)

    unterschrift(draw,
                 "Der Windenstart zieht das Flugzeug in gut einer Minute auf "
                 "rund 400 Meter.",
                 "The winch launch pulls the glider to about 400 metres in a "
                 "little over a minute.",
                 "Erst flach anrollen, dann im Bogen in den steilen "
                 "Steigflug.",
                 "First a shallow ground run, then a curve into the steep "
                 "climb.")
    sk.sichern(bild, "begriff-windenstart")


def flugzeugschlepp():
    bild, draw = sk.leinwand()
    boden(draw)
    # Das Gespann steigt flach. Der Segler haelt sich ueber dem Nachlauf
    # des Schleppers -- dort ist die Luft ruhig und die Sicht frei.
    sk.gestrichelt(draw, 60, 200, 380, 72, DUENN, 1, 8)
    segler(draw, 330, 86, -14, 30)
    kreis(draw, 342, 83, 3, KOERPER)
    beschrift(draw, 300, 50, "Schleppflugzeug", "tug", 10, TEXT, mitte=True)
    segler(draw, 196, 136, -14, 26, GUT)
    beschrift(draw, 196, 158, "Segelflugzeug", "glider", 10, GUT, mitte=True)
    sk.strich(draw, 210, 132, 318, 90, WARN, 1)
    beschrift(draw, 252, 96, "Seil 40–60 m", "rope 40–60 m", 10, WARN,
              mitte=True)

    sk.gestrichelt(draw, 200, 108, 360, 62, DUENN, 1, 6)
    beschrift(draw, 150, 100, "über dem Nachlauf bleiben",
              "stay above the wake", 10, TEXT, rechts=True)
    sk.pfeil(draw, 196, 120, 196, 102, TEXT, 1, 5)
    sk.pfeil(draw, 182, 136, 150, 160, GUT, 2)
    beschrift(draw, 146, 162, "ausklinken und wegdrehen",
              "release and turn away", 10, GUT, rechts=True)

    unterschrift(draw,
                 "Im Flugzeugschlepp hängt der Segler an 40 bis 60 Metern "
                 "Seil hinter dem Schlepper.",
                 "On aerotow the glider hangs 40 to 60 metres behind the tug.",
                 "Ausgeklinkt wird nach rechts, der Schlepper geht links weg.",
                 "It stays above the wake; the glider turns right after "
                 "release, the tug goes left.")
    sk.sichern(bild, "begriff-flugzeugschlepp")


# ---------------------------------------------------------------------------
# Wolkenbilder ohne Beschriftung
#
# Hier gibt es nichts zu beschriften -- eine Wolke sieht aus, wie sie
# aussieht. Also nur eine Datei je Bild; Bild.qml nimmt fuer Englisch
# dieselbe. Gezeichnet wird mit den Mitteln aus clouds.py, damit diese
# Wolken dieselben sind wie die im Erkennungsteil.
# ---------------------------------------------------------------------------

def _himmel(oben=wo.SKY_TOP, unten=wo.SKY_BOTTOM, horizont=0.86):
    return wo.zelle(W * S, H * S, horizont, oben, unten)


def wolke_mediocris():
    rng = random.Random(201)
    bild, draw = _himmel()
    basis = int(H * S * 0.66)
    bild = wo.cumulus(bild, W * S * 0.50, basis, W * S * 0.26, H * S * 0.30, rng)
    bild = wo.cumulus(bild, W * S * 0.18, basis, W * S * 0.17, H * S * 0.17, rng)
    bild = wo.cumulus(bild, W * S * 0.82, basis, W * S * 0.19, H * S * 0.22, rng)
    wo.save(wo.soften(bild, 1.4), "begriff-cu-mediocris")


def _decke(bild, draw, rng, unterkante, farbe, zotteln=0.06):
    """Eine geschlossene Schicht mit zerfaserter Unterkante.

    Scharf ist die Unterkante nur bei Thermikwolken; eine Schichtwolke
    franst aus, und genau daran erkennt man sie von unten."""
    draw.rectangle([0, 0, bild.size[0], int(unterkante)], fill=farbe)
    for _ in range(340):
        x = rng.uniform(-20, bild.size[0] + 20)
        y = unterkante + rng.uniform(-bild.size[1] * zotteln,
                                     bild.size[1] * zotteln * 0.4)
        wo.blob(draw, x, y, bild.size[1] * rng.uniform(0.018, 0.045), farbe)


def wolke_stratus():
    rng = random.Random(203)
    bild, draw = _himmel((150, 158, 172), (196, 200, 208))
    _decke(bild, draw, rng, H * S * 0.50, (120, 126, 142))
    for _ in range(30):
        wo.blob(draw, rng.uniform(0, W * S), H * S * rng.uniform(0.52, 0.64),
                H * S * rng.uniform(0.012, 0.028), (146, 152, 166))
    wo.save(wo.soften(bild, 2.4), "begriff-stratus")


def wolke_nimbostratus():
    rng = random.Random(205)
    bild, draw = _himmel((96, 102, 116), (158, 164, 176))
    _decke(bild, draw, rng, H * S * 0.40, (86, 92, 106), 0.07)
    bild = wo.soften(bild, 2.6)
    for teil in range(7):
        bild = wo.regen(bild, rng, 0.0, 1.0,
                        int(H * S * (0.42 + teil * 0.062)), 150)
    wo.save(bild, "begriff-nimbostratus")


def wolke_altostratus():
    rng = random.Random(207)
    bild, draw = _himmel((104, 118, 144), (172, 180, 194))
    bild = Image.blend(bild, Image.new("RGB", bild.size, (186, 192, 204)), 0.45)
    bild = wo.schleier(bild, rng, 0.9, (204, 210, 220), 0.0, 0.62)
    bild = wo.sonne(bild, W * S * 0.70, H * S * 0.28, H * S * 0.052, False,
                    True)
    bild = wo.schleier(bild, rng, 0.5, (204, 210, 220), 0.10, 0.54)
    wo.save(wo.soften(bild, 2.0), "begriff-altostratus")


def wolke_cirrostratus():
    rng = random.Random(209)
    bild, draw = _himmel((72, 126, 186), (176, 204, 230))
    # Milchglas statt Streifen: Cirrostratus hat keine Struktur, nur einen
    # Schleier -- und den Ring, an dem man ihn sicher erkennt.
    bild = Image.blend(bild, Image.new("RGB", bild.size, (236, 240, 248)), 0.38)
    bild = wo.schleier(bild, rng, 0.22, wo.ICE, 0.0, 0.66)
    bild = wo.soften(bild, 2.2)
    bild = wo.sonne(bild, W * S * 0.52, H * S * 0.34, H * S * 0.05, True)
    wo.save(bild, "begriff-cirrostratus")


def wolke_cirrocumulus():
    rng = random.Random(211)
    bild, draw = _himmel((56, 112, 180), (164, 198, 228))
    # Koerner in Reihen: klein, weiss, ohne Schatten -- das unterscheidet
    # Cirrocumulus von Altocumulus. Unregelmaessig gesetzt, sonst sieht es
    # nach Tapete aus.
    for reihe in range(7):
        y = H * S * (0.12 + reihe * 0.05)
        r = H * S * (0.019 - reihe * 0.0011)
        x = W * S * 0.03 + rng.uniform(0, r * 2)
        while x < W * S * 0.99:
            if rng.random() > 0.22:
                wo.blob(draw, x + rng.uniform(-r, r), y + rng.uniform(-r, r),
                        r * rng.uniform(0.6, 1.1), wo.CLOUD_LIT)
            x += r * rng.uniform(2.4, 3.8)
    wo.save(wo.soften(bild, 1.1), "begriff-cirrocumulus")


def wolke_altocumulus():
    rng = random.Random(213)
    bild, draw = _himmel((58, 116, 184), (168, 200, 228))
    # Groesser als Cirrocumulus und mit Schatten an der Unterseite: das ist
    # der Unterschied, an dem die Hoehe haengt.
    for reihe in range(5):
        y = H * S * (0.20 + reihe * 0.088)
        r = H * S * (0.054 - reihe * 0.006)
        x = W * S * 0.02 + rng.uniform(0, r)
        while x < W * S * 1.02:
            if rng.random() > 0.18:
                wo.puff(draw, x, y + rng.uniform(-r * 0.3, r * 0.3),
                        r * rng.uniform(0.8, 1.2), rng,
                        wo.CLOUD_DARK, wo.CLOUD_MID, wo.CLOUD_LIT, 8, 1.1)
            x += r * rng.uniform(2.2, 3.4)
    wo.save(wo.soften(bild, 1.5), "begriff-altocumulus")


def wolke_kondensstreifen():
    rng = random.Random(215)
    bild, draw = _himmel((54, 110, 178), (166, 200, 228))
    # Schnurgerade und in grosser Hoehe: nur Menschenwerk zieht solche
    # Linien. Ob sie stehen bleiben, sagt etwas ueber die Feuchte oben.
    for x0, y0, x1, y1, dicke in ((0.02, 0.10, 0.98, 0.26, 2.2),
                                  (0.06, 0.40, 0.94, 0.22, 1.6),
                                  (0.10, 0.30, 0.70, 0.52, 1.2)):
        draw.line([(W * S * x0, H * S * y0), (W * S * x1, H * S * y1)],
                  fill=wo.ICE, width=int(dicke * S))
    # Der aelteste faechert auf, statt zu verschwinden: feuchte Hoehenluft.
    for _ in range(420):
        t = rng.random()
        x = W * S * (0.02 + t * 0.96)
        y = H * S * (0.10 + t * 0.16) \
            + rng.gauss(0, H * S * 0.012) * (0.3 + t)
        wo.blob(draw, x, y, H * S * rng.uniform(0.004, 0.009), wo.ICE)
    wo.save(wo.soften(bild, 1.6), "begriff-kondensstreifen")


# ---------------------------------------------------------------------------
# Rund um den Flug: Atmosphaere, Luftraum, Kompass, Vorrang
# ---------------------------------------------------------------------------

def isa():
    bild, draw = sk.leinwand()
    # Die Normatmosphaere ist eine Vereinbarung, keine Messung: eine Gerade
    # durch 15 °C am Boden, 0,65 °C weniger je 100 m. Der Druck steht
    # daneben, denn der Hoehenmesser misst Druck und zeigt Hoehe -- die
    # Umrechnung dazwischen ist genau diese Tabelle.
    x0, y0, x1, y1 = 92, 206, 300, 44
    # Die Hoehenbeschriftung nicht aus achsen(): sie saesse an der Achse und
    # damit genau auf der obersten Strichlinie. Sie steht hier links ueber
    # den Zahlen, wo nichts anderes liegt.
    achsen(draw, x0, y0, x1, y1, "Temperatur →", "temperature →", "", "")
    beschrift(draw, x0 - 6, 32, "Höhe [m]", "height [m]", 10, DUENN,
              rechts=True)

    # 1000 m sind 52 Pixel, 1 °C sind 4 Pixel, 15 °C stehen bei x=280.
    for hoehe, grad, druck in ((0, "15 °C", "1013 hPa"),
                               (1000, "8,5 °C", "899 hPa"),
                               (2000, "2 °C", "795 hPa"),
                               (3000, "−4,5 °C", "701 hPa")):
        y = y0 - hoehe * 0.052
        sk.gestrichelt(draw, x0, y, 304, y, DUENN, 1, 5)
        sk.text(draw, x0 - 6, y - 6, "%d" % hoehe, 9, DUENN, rechts=True)
        beschrift(draw, 312, y - 6, grad + " · " + druck,
                  grad.replace(",", ".") + " · " + druck, 10, TEXT)

    sk.strich(draw, 280, y0, 202, y1, WARN, 2)
    kreis(draw, 280, y0, 3, WARN)
    beschrift(draw, 110, 112, "0,65 °C je 100 m", "0.65 °C per 100 m", 10,
              WARN)
    beschrift(draw, 110, 170, "1 hPa je 8 m", "1 hPa per 8 m", 10, BETONT)

    unterschrift(draw,
                 "Die Standardatmosphäre: 15 °C und 1013 hPa in Meereshöhe, "
                 "0,65 °C weniger je 100 m.",
                 "The standard atmosphere: 15 °C and 1013 hPa at sea level, "
                 "0.65 °C less per 100 m.",
                 "Auf ihr rechnen Höhenmesser, Flugflächen und jede "
                 "Leistungsangabe.",
                 "Altimeters, flight levels and every performance figure are "
                 "based on it.")
    sk.sichern(bild, "begriff-isa")


def luftraum():
    bild, draw = sk.leinwand()
    # Im Schnitt, und nach oben immer weiter ausgreifend: so liegt die
    # kontrollierte Luft ueber einem Verkehrsflughafen. Links davon bleibt
    # die Luft frei -- dort fliegt der Segler ohne zu fragen.
    boden(draw)
    deckel, grenze = 62, 176
    for x_von, oben, unten in ((230, deckel, 110), (280, 110, 150),
                               (330, 150, BODEN_Y)):
        draw.rectangle([x_von * S, oben * S, 420 * S, unten * S],
                       fill=(46, 52, 70), outline=LINIE, width=1 * S)
    sk.strich(draw, 350, 224, 402, 224, DUENN, 3)

    sk.gestrichelt(draw, 20, deckel, 228, deckel, WARN, 1, 6)
    beschrift(draw, 24, 44, "Obergrenze: siehe Karte",
              "upper limit: see the chart", 10, WARN)
    sk.gestrichelt(draw, 20, grenze, 328, grenze, DUENN, 1, 6)
    beschrift(draw, 24, 180, "meist 2500 ft über Grund",
              "usually 2500 ft above ground", 10, DUENN)

    segler(draw, 136, 128, -4)
    beschrift(draw, 30, 96, "E: ohne Freigabe", "E: no clearance", 11, GUT)
    beschrift(draw, 30, 196, "G: unkontrolliert", "G: uncontrolled", 11, TEXT)
    beschrift(draw, 325, 74, "C / D", "C / D", 13, WARN, mitte=True)
    beschrift(draw, 325, 92, "Freigabe und Funk", "clearance and radio", 10,
              WARN, mitte=True)

    unterschrift(draw,
                 "Der Luftraum ist in Klassen geteilt, über den "
                 "Verkehrsflughäfen gestapelt.",
                 "Airspace is divided into classes, stacked over the airline "
                 "airports.",
                 "In C und D nur mit Freigabe und Funk, in E und G ohne.",
                 "In C and D only with clearance and radio, in E and G "
                 "without.")
    sk.sichern(bild, "begriff-luftraum")


def missweisung():
    bild, draw = sk.leinwand()
    cx, cy, r = 126, 128, 62
    # Zwei Nadeln aus einem Punkt. Der Winkel dazwischen ist in
    # Mitteleuropa so klein, dass er gezeichnet verschwaende -- deshalb
    # steht er ueberhoeht da, und darunter, dass er ueberhoeht ist.
    draw.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
                 outline=DUENN, width=1 * S)
    for grad in range(0, 360, 15):
        aussen = r
        innen = r - (7 if grad % 90 == 0 else 4)
        b = math.radians(grad - 90)
        sk.strich(draw, cx + innen * math.sin(b + math.pi / 2),
                  cy - innen * math.cos(b + math.pi / 2),
                  cx + aussen * math.sin(b + math.pi / 2),
                  cy - aussen * math.cos(b + math.pi / 2), DUENN, 1)
    beschrift(draw, cx, cy + r + 6, "S", "S", 10, DUENN, mitte=True)
    beschrift(draw, cx - r - 14, cy - 6, "W", "W", 10, DUENN)
    beschrift(draw, cx + r + 6, cy - 6, "O", "E", 10, DUENN)

    sk.pfeil(draw, cx, cy, cx, cy - r + 8, TEXT, 2)
    schraeg = math.radians(16)
    sk.pfeil(draw, cx, cy, cx + (r - 8) * math.sin(schraeg),
             cy - (r - 8) * math.cos(schraeg), WARN, 2)
    sk.bogen(draw, cx, cy, 34, -90, -74, WARN, 1)

    beschrift(draw, cx - 6, cy - r - 20, "rw N", "true N", 10, TEXT,
              rechts=True)
    beschrift(draw, cx + 22, cy - r - 2, "mw N", "magnetic N", 10, WARN)
    beschrift(draw, 212, 108, "Missweisung 2–5° Ost",
              "variation 2–5° east", 10, WARN)
    beschrift(draw, 212, 124, "(hier überhöht)", "(exaggerated here)", 9,
              DUENN)
    beschrift(draw, 212, 156, "Karte → Kompass:", "chart → compass:", 10,
              TEXT)
    beschrift(draw, 212, 174, "östliche abziehen", "easterly: subtract", 10,
              GUT)
    beschrift(draw, 212, 190, "westliche addieren", "westerly: add", 10, GUT)

    unterschrift(draw,
                 "Missweisung: der Winkel zwischen geographisch und "
                 "magnetisch Nord, bei uns 2–5° Ost.",
                 "Variation: the angle between true and magnetic north, here "
                 "2–5° east.",
                 "Die Karte zeigt rechtweisend, der Kompass missweisend.",
                 "The chart shows true, the compass shows magnetic.")
    sk.sichern(bild, "begriff-missweisung")


def ausweichen():
    bild, draw = sk.leinwand()
    # Von oben, drei Faelle nebeneinander. "Rechts" ist immer das Rechts
    # des Flugzeugs, nicht das des Betrachters -- darum zeigt der Pfeil
    # beim entgegenkommenden Segler im Bild nach links.
    for x in (150, 290):
        sk.strich(draw, x, 28, x, 206, DUENN, 1)

    beschrift(draw, 80, 32, "Gegenkurs", "head-on", 11, TEXT, mitte=True)
    segler_oben(draw, 80, 82, 90, 22, TEXT)
    sk.pfeil(draw, 80, 98, 54, 112, GUT, 2)
    segler_oben(draw, 80, 150, -90, 22, TEXT)
    sk.pfeil(draw, 80, 134, 106, 120, GUT, 2)
    beschrift(draw, 80, 184, "beide nach rechts", "both turn right", 10, GUT,
              mitte=True)

    beschrift(draw, 220, 32, "Kreuzen", "crossing", 11, TEXT, mitte=True)
    segler_oben(draw, 196, 152, -90, 22, ROT)
    sk.pfeil(draw, 196, 136, 220, 118, ROT, 2)
    segler_oben(draw, 258, 92, 180, 22, GUT)
    sk.pfeil(draw, 240, 92, 212, 92, GUT, 2)
    beschrift(draw, 220, 184, "rechts hat Vorrang", "right has priority", 10,
              GUT, mitte=True)

    beschrift(draw, 360, 32, "Überholen", "overtaking", 11, TEXT, mitte=True)
    segler_oben(draw, 368, 86, -90, 22, TEXT)
    segler_oben(draw, 350, 158, -90, 22, GUT)
    sk.pfeil(draw, 350, 142, 392, 104, GUT, 2)
    beschrift(draw, 360, 184, "rechts vorbei", "pass on the right", 10, GUT,
              mitte=True)

    unterschrift(draw,
                 "Bei Gegenkurs weichen beide nach rechts aus, sonst hat "
                 "Vorrang, wer von rechts kommt.",
                 "Head-on both turn right; otherwise the one coming from the "
                 "right has priority.",
                 "Überholt wird rechts — und beim Landen hat Vorrang, wer "
                 "tiefer ist.",
                 "Overtake on the right — and on landing the lower aircraft "
                 "has priority.")
    sk.sichern(bild, "begriff-ausweichen")


# ---------------------------------------------------------------------------
# Was gezeichnet wird
# ---------------------------------------------------------------------------

BESCHRIFTET = [
    durchschiessen,
    basis,
    inversion,
    labilitaet,
    spread,
    taupunkt,
    kondensationsniveau,
    ausloesung,
    ueberentwicklung,
    ausbreitung,
    abschirmung,
    blauthermik,
    dunstglocke,
    welle,
    rotor,
    hangaufwind,
    luv_lee,
    foehn,
    thermikschlauch,
    anflug,
    warmfront,
    kaltfront,
    hochdruck,
    tiefdruck,
    amboss,
    boeenfront,
    halo,
    nebel,
    polare,
    mccready,
    wasserballast,
    endanflug,
    anstellwinkel,
    ueberziehen,
    trudeln,
    kurbeln,
    dichtehoehe,
    hoehenbezuege,
    platzrunde,
    aussenlandung,
    seilriss,
    staudruck,
    variometer,
    abwind,
    tagesgang,
    windenstart,
    flugzeugschlepp,
    isa,
    luftraum,
    missweisung,
    ausweichen,
]

OHNE_TEXT = [
    wolke_mediocris,
    wolke_stratus,
    wolke_nimbostratus,
    wolke_altostratus,
    wolke_cirrostratus,
    wolke_cirrocumulus,
    wolke_altocumulus,
    wolke_kondensstreifen,
]



def main():
    for sprache in ("de", "en"):
        sk.SPRACHE = sprache
        print("Begriffsbilder (%s):" % sprache)
        for zeichnung in BESCHRIFTET:
            zeichnung()
    sk.SPRACHE = "de"
    if OHNE_TEXT:
        print("Begriffsbilder (ohne Beschriftung):")
        for zeichnung in OHNE_TEXT:
            zeichnung()
    schlecht = 0
    if ZU_LANG:
        print("Unterschriften passen nicht in drei Zeilen:", file=sys.stderr)
        for eintrag in sorted(set(ZU_LANG)):
            print("  " + eintrag, file=sys.stderr)
        schlecht = 1
    if UEBER_RAND:
        print("Beschriftungen laufen aus dem Bild:", file=sys.stderr)
        for eintrag in sorted(set(UEBER_RAND)):
            print("  " + eintrag, file=sys.stderr)
        schlecht = 1
    return schlecht


if __name__ == "__main__":
    raise SystemExit(main())
