#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zeichnet die Skizzen zu den Herleitungen.

Eine Herleitung ist eine Kette von Saetzen, und an genau einer Stelle
haengt sie an einem Bild: dem Kraeftedreieck, der schiefen Ebene, der
Luftsaeule. Wer das Bild vor sich hat, liest die Rechnung als Beschreibung
dessen, was er sieht; wer es nicht hat, muss es sich nebenher bauen -- und
verliert dabei den Faden.

Gezeichnet wird schematisch, nicht abbildend: Ein Segelflugzeug ist hier
ein Strich mit Fluegel, weil es auf die Winkel ankommt und nicht auf den
Rumpf. Alles bei 3x und am Ende verkleinert, sonst treppen die Schraegen.

Die Beschriftung steckt im Bild, also gibt es jede Skizze zweimal:
<name>.png und <name>.en.png. Welche gezeigt wird, entscheidet die App.

    tools/skizzen.py            # -> bilder/skizze-*.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "bilder")

W, H = 440, 300
S = 3

GRUND = (14, 14, 18)
LINIE = (120, 130, 150)
DUENN = (70, 78, 94)
TEXT = (226, 230, 240)
BETONT = (90, 169, 255)
WARN = (255, 177, 78)
GUT = (126, 231, 135)
ROT = (226, 74, 74)
KOERPER = (232, 236, 244)

SPRACHE = "de"

EN = {
    "Strecke": "distance",
    "Höhe": "height",
    "Gleitwinkel": "glide angle",
    "Auftrieb": "lift",
    "Widerstand": "drag",
    "Gewicht": "weight",
    "Fahrt": "airspeed",
    "Sinken": "sink",
    "Querlage": "bank",
    "Auftrieb in der Kurve": "lift in the turn",
    "trägt das Gewicht": "carries the weight",
    "zieht in die Kurve": "pulls into the turn",
    "Bezugspunkt": "datum",
    "Pilot": "pilot",
    "Flugzeug": "aircraft",
    "Schwerpunkt": "centre of gravity",
    "Hebelarm": "lever arm",
    "Temperatur": "temperature",
    "Taupunkt": "dew point",
    "Wolkenbasis": "cloud base",
    "Spreizung am Boden": "spread at the ground",
    "Boden": "ground",
    "Wind": "wind",
    "gewollter Kurs": "intended track",
    "Vorhalt": "drift correction",
    "Kurs über Grund": "track over the ground",
    "Luftsäule": "column of air",
    "1 hPa": "1 hPa",
    "8,3 m": "8.3 m",
    "Druck oben": "pressure above",
    "Druck unten": "pressure below",
    "je 100 m": "per 100 m",
}


def schrift(groesse):
    for pfad in ("/usr/share/fonts/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/TTF/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(pfad):
            return ImageFont.truetype(pfad, groesse)
    return ImageFont.load_default()


def leinwand():
    bild = Image.new("RGB", (W * S, H * S), GRUND)
    return bild, ImageDraw.Draw(bild)


def sichern(bild, name):
    os.makedirs(OUT, exist_ok=True)
    if SPRACHE != "de":
        name = name + "." + SPRACHE
    bild.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, name + ".png"))
    print("  %s" % name)


def text(draw, x, y, inhalt, groesse=13, farbe=TEXT, mitte=False, rechts=False):
    if SPRACHE != "de":
        inhalt = EN.get(inhalt, inhalt)
    f = schrift(groesse * S)
    # Die Breite kommt in Geraetepunkten (die Schrift ist S-fach gross),
    # x und y sind in Zeicheneinheiten -- also erst umrechnen, sonst rueckt
    # der Text dreimal zu weit nach links und faellt aus dem Bild.
    kasten = draw.textbbox((0, 0), inhalt, font=f)
    breite = (kasten[2] - kasten[0]) / float(S)
    if mitte:
        x -= breite / 2.0
    elif rechts:
        x -= breite
    draw.text((x * S, y * S), inhalt, font=f, fill=farbe)


def strich(draw, x1, y1, x2, y2, farbe=LINIE, dicke=2):
    draw.line([(x1 * S, y1 * S), (x2 * S, y2 * S)], fill=farbe, width=dicke * S)


def gestrichelt(draw, x1, y1, x2, y2, farbe=DUENN, dicke=1, laenge=6):
    weite = math.hypot(x2 - x1, y2 - y1)
    if weite <= 0:
        return
    schritte = max(1, int(weite / laenge))
    for i in range(schritte):
        if i % 2:
            continue
        a, b = i / float(schritte), min(1.0, (i + 1) / float(schritte))
        strich(draw, x1 + (x2 - x1) * a, y1 + (y2 - y1) * a,
               x1 + (x2 - x1) * b, y1 + (y2 - y1) * b, farbe, dicke)


def pfeil(draw, x1, y1, x2, y2, farbe=BETONT, dicke=2, spitze=7):
    strich(draw, x1, y1, x2, y2, farbe, dicke)
    winkel = math.atan2(y2 - y1, x2 - x1)
    for seite in (+1, -1):
        a = winkel + seite * 2.6
        strich(draw, x2, y2, x2 + spitze * math.cos(a), y2 + spitze * math.sin(a),
               farbe, dicke)


def bogen(draw, cx, cy, r, von, bis, farbe=DUENN, dicke=1):
    """Winkelbogen; die Winkel in Grad, 0 ist rechts, positiv im Uhrzeigersinn."""
    draw.arc([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
             von, bis, fill=farbe, width=dicke * S)


def flugzeug_seite(draw, x, y, winkel, laenge=34, farbe=KOERPER):
    """Ein Segelflugzeug von der Seite: Rumpf als Strich, Fluegel als Punkt."""
    c, s = math.cos(math.radians(winkel)), math.sin(math.radians(winkel))
    strich(draw, x - laenge / 2 * c, y - laenge / 2 * s,
           x + laenge / 2 * c, y + laenge / 2 * s, farbe, 3)
    # Fluegel quer, kurz
    qx, qy = -s, c
    strich(draw, x - 7 * qx, y - 7 * qy, x + 7 * qx, y + 7 * qy, farbe, 3)
    # Leitwerk am hinteren Ende
    hx, hy = x - laenge / 2 * c, y - laenge / 2 * s
    strich(draw, hx, hy, hx - 6 * qx * 0 - 6 * s * 0 + 0, hy - 7, farbe, 2)


# ---------------------------------------------------------------------------
# a-polare: das Kraeftedreieck im stationaeren Gleitflug
# ---------------------------------------------------------------------------
def gleitflug():
    bild, draw = leinwand()
    # Die Bahn: von links oben nach rechts unten, uebertrieben steil
    # gezeichnet -- bei einer echten Gleitzahl von 40 saehe man den Winkel
    # sonst gar nicht.
    x1, y1 = 70, 78
    x2, y2 = 350, 188
    strich(draw, x1, y1, x2, y2, LINIE, 2)
    gestrichelt(draw, x1, y1, x2, y1)                 # Waagrechte
    gestrichelt(draw, x2, y1, x2, y2)                 # Hoehe
    bogen(draw, x1, y1, 54, 0, math.degrees(math.atan2(y2 - y1, x2 - x1)),
          WARN, 1)
    text(draw, x1 + 60, y1 + 4, "γ", 14, WARN)
    text(draw, x1 + (x2 - x1) * 0.82, y1 - 20, "Strecke", 12, TEXT,
         mitte=True)
    text(draw, x2 + 8, (y1 + y2) / 2 - 8, "Höhe", 12, TEXT)

    # Das Flugzeug sitzt auf der Bahn
    mx, my = x1 + (x2 - x1) * 0.30, y1 + (y2 - y1) * 0.30
    bahn = math.degrees(math.atan2(y2 - y1, x2 - x1))
    draw.ellipse([(mx - 4) * S, (my - 4) * S, (mx + 4) * S, (my + 4) * S],
                 fill=KOERPER)

    # Kraefte: Gewicht senkrecht, Auftrieb quer zur Bahn, Widerstand entgegen
    pfeil(draw, mx, my, mx, my + 62, ROT)
    text(draw, mx + 6, my + 46, "G", 13, ROT)
    text(draw, mx + 6, my + 62, "Gewicht", 11, ROT)
    qx = -math.sin(math.radians(bahn))
    qy = math.cos(math.radians(bahn))
    pfeil(draw, mx, my, mx - 58 * qx, my - 58 * qy, BETONT)
    text(draw, mx - 58 * qx - 4, my - 58 * qy - 18, "L", 13, BETONT)
    text(draw, mx - 58 * qx + 12, my - 58 * qy - 4, "Auftrieb", 11, BETONT)
    lx = math.cos(math.radians(bahn))
    ly = math.sin(math.radians(bahn))
    pfeil(draw, mx, my, mx - 42 * lx, my - 42 * ly, WARN)
    text(draw, mx - 42 * lx - 14, my - 42 * ly - 22, "D", 13, WARN)
    text(draw, mx - 42 * lx - 14, my - 42 * ly - 6, "Widerstand", 11, WARN,
         rechts=True)

    text(draw, 30, 236, "Strecke / Höhe  =  L / D  =  v / w  =  E", 14, GUT)
    text(draw, 30, 258, "Gleitwinkel γ:  tan γ = D / L", 12, TEXT)
    sichern(bild, "skizze-gleitflug")


# ---------------------------------------------------------------------------
# a-ueberziehen: warum n = 1 / cos φ
# ---------------------------------------------------------------------------
def kurvenlast():
    bild, draw = leinwand()
    cx, cy = 218, 196          # Schwerpunkt des Flugzeugs, von hinten gesehen
    phi = 45.0

    # Flugzeug von hinten: Fluegel als Strich, um phi gekippt
    c, s = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    strich(draw, cx - 62 * c, cy + 62 * s, cx + 62 * c, cy - 62 * s, KOERPER, 3)
    draw.ellipse([(cx - 5) * S, (cy - 5) * S, (cx + 5) * S, (cy + 5) * S],
                 fill=KOERPER)

    # Auftrieb steht senkrecht auf dem Fluegel
    lx, ly = math.sin(math.radians(phi)), -math.cos(math.radians(phi))
    laenge = 120
    pfeil(draw, cx, cy, cx + laenge * lx, cy + laenge * ly, BETONT, 2)
    text(draw, cx + laenge * lx + 6, cy + laenge * ly - 6, "L", 14, BETONT)
    text(draw, cx + laenge * lx + 6, cy + laenge * ly + 12,
         "Auftrieb", 11, BETONT)

    # Senkrechte Komponente = Gewicht, waagrechte zieht in die Kurve
    hoehe = laenge * math.cos(math.radians(phi))
    gestrichelt(draw, cx, cy, cx, cy - hoehe)
    gestrichelt(draw, cx, cy - hoehe, cx + laenge * lx, cy + laenge * ly)
    pfeil(draw, cx, cy, cx, cy - hoehe, GUT, 2)
    text(draw, cx - 8, cy - hoehe - 4, "L·cos φ = G", 12, GUT, rechts=True)
    text(draw, cx - 8, cy - hoehe + 12, "trägt das Gewicht", 11, GUT, rechts=True)
    breite = laenge * math.sin(math.radians(phi))
    pfeil(draw, cx, cy, cx + breite, cy, WARN, 2)
    text(draw, cx + breite + 6, cy + 4, "zieht in die Kurve", 11, WARN)

    # Querlage
    gestrichelt(draw, cx, cy, cx, cy + 50)
    bogen(draw, cx, cy, 40, -90, -90 + phi, DUENN)
    text(draw, cx + 16, cy - 44, "φ", 13, WARN)
    text(draw, cx + 34, cy - 24, "Querlage", 10, WARN)

    text(draw, 24, 250, "L = G / cos φ    →    n = 1 / cos φ", 14, GUT)
    text(draw, 24, 272, "45°: n = 1,41      60°: n = 2", 12, TEXT)
    sichern(bild, "skizze-kurvenlast")


# ---------------------------------------------------------------------------
# l-schwerpunkt: Momente um einen Bezugspunkt
# ---------------------------------------------------------------------------
def schwerpunkt():
    bild, draw = leinwand()
    y = 150
    x0, x1 = 60, 400
    strich(draw, x0, y, x1, y, LINIE, 2)
    # Bezugspunkt
    strich(draw, x0, y - 30, x0, y + 30, DUENN, 1)
    text(draw, x0 + 4, y + 56, "Bezugspunkt", 11, DUENN, mitte=True)

    # Zwei Massen
    def masse(x, r, beschriftung, wert, farbe):
        draw.ellipse([(x - r) * S, (y - r - 10) * S, (x + r) * S, (y + r - 10) * S],
                     fill=farbe)
        text(draw, x, y - r - 34, beschriftung, 12, farbe, mitte=True)
        text(draw, x, y + 16, wert, 11, TEXT, mitte=True)
        gestrichelt(draw, x0, y + 34, x, y + 34)
        strich(draw, x, y + 30, x, y + 38, DUENN, 1)

    masse(150, 16, "Pilot", "m₁ · x₁", BETONT)
    masse(330, 22, "Flugzeug", "m₂ · x₂", KOERPER)

    # Schwerpunkt als Dreieck unter dem Balken
    xs = (150 * 80 + 330 * 260) / float(80 + 260)
    draw.polygon([((xs) * S, (y + 6) * S), ((xs - 12) * S, (y + 30) * S),
                  ((xs + 12) * S, (y + 30) * S)], fill=GUT)
    text(draw, xs, y - 78, "Schwerpunkt", 12, GUT, mitte=True)
    gestrichelt(draw, xs, y - 62, xs, y + 6, GUT)

    text(draw, 40, 226, "(m₁ + m₂) · x_S  =  m₁·x₁ + m₂·x₂", 14, GUT)
    text(draw, 40, 250, "x_S = Σ(m·x) / Σm  —  Gesamtmoment durch Gesamtmasse",
         11, TEXT)
    sichern(bild, "skizze-schwerpunkt")


# ---------------------------------------------------------------------------
# w-basis: wo sich Temperatur und Taupunkt treffen
# ---------------------------------------------------------------------------
def wolkenbasis():
    bild, draw = leinwand()
    # Hoehe nach oben, Temperatur nach rechts. Beide Geraden laufen nach
    # links oben: Es wird kaelter, je hoeher man kommt.
    x0, y0 = 118, 214          # Ecke: Boden links
    strich(draw, x0, y0, x0, 44, DUENN, 1)
    strich(draw, x0, y0, 408, y0, DUENN, 1)
    text(draw, x0 - 8, y0 - 12, "Boden", 10, DUENN, rechts=True)
    text(draw, 406, y0 - 40, "Temperatur →", 10, DUENN, rechts=True)
    text(draw, x0 + 6, 46, "Höhe", 10, DUENN)

    tx, dx = 352, 268          # Werte am Boden: T rechts, Taupunkt links
    treff_x, treff_y = 176, 92
    strich(draw, tx, y0, treff_x, treff_y, WARN, 2)
    strich(draw, dx, y0, treff_x, treff_y, BETONT, 2)
    text(draw, tx + 4, y0 - 18, "T", 13, WARN)
    text(draw, dx - 4, y0 - 18, "T_d", 13, BETONT, rechts=True)
    # Steigung je Gerade, an ihrer Mitte
    text(draw, (tx + treff_x) / 2 + 16, (y0 + treff_y) / 2 - 6,
         "1,0 °C je 100 m", 10, WARN)
    text(draw, (dx + treff_x) / 2 - 12, (y0 + treff_y) / 2 + 10,
         "0,2 °C je 100 m", 10, BETONT, rechts=True)

    # Spreizung am Boden, als Mass ueber der Achse
    strich(draw, dx, y0 + 14, tx, y0 + 14, GUT, 1)
    strich(draw, dx, y0 + 10, dx, y0 + 18, GUT, 1)
    strich(draw, tx, y0 + 10, tx, y0 + 18, GUT, 1)
    text(draw, (dx + tx) / 2, y0 + 20, "Spreizung am Boden", 10, GUT, mitte=True)

    # Die Basis liegt dort, wo sich beide treffen
    gestrichelt(draw, x0, treff_y, 404, treff_y, GUT)
    for (wx, wr) in ((214, 20), (242, 26), (272, 18), (296, 22)):
        draw.ellipse([(wx - wr) * S, (treff_y - 2 * wr) * S,
                      (wx + wr) * S, treff_y * S], fill=(226, 230, 240))
    text(draw, 404, treff_y + 8, "Wolkenbasis", 11, GUT, rechts=True)

    pfeil(draw, x0 - 26, y0, x0 - 26, treff_y, TEXT, 1)
    text(draw, x0 - 34, (y0 + treff_y) / 2 - 8, "h", 13, TEXT, rechts=True)

    text(draw, 22, 254, "Die Spreizung schließt sich mit 0,8 °C je 100 m", 11, TEXT)
    text(draw, 22, 274, "h = Spreizung ÷ 0,8 = Spreizung × 125 m/°C", 13, GUT)
    sichern(bild, "skizze-wolkenbasis")


# ---------------------------------------------------------------------------
# n-kurse: das Geschwindigkeitsdreieck beim Vorhalten
# ---------------------------------------------------------------------------
def vorhalt():
    bild, draw = leinwand()
    # Der gewollte Kurs ist die Waagrechte. Das Flugzeug zeigt um alpha
    # daneben; was der Wind zur Seite schiebt, bringt es genau dorthin
    # zurueck -- deshalb liegt der Kurs ueber Grund wieder auf der Linie.
    ax, ay = 70, 150
    zx = 370
    gestrichelt(draw, ax, ay, zx, ay, DUENN, 1)
    text(draw, ax, ay + 12, "gewollter Kurs = Kurs über Grund", 11, DUENN)

    alpha = 17.0
    laenge = 260
    ex = ax + laenge * math.cos(math.radians(alpha))
    ey = ay - laenge * math.sin(math.radians(alpha))
    pfeil(draw, ax, ay, ex, ey, BETONT, 2)
    text(draw, ax + 120, ay - 76, "v", 13, BETONT)
    text(draw, ax + 134, ay - 74, "(wohin die Nase zeigt)", 10, BETONT)

    # Der Wind schiebt vom Kopf des Vektors senkrecht zurueck auf die Linie
    pfeil(draw, ex, ey, ex, ay, WARN, 2)
    text(draw, ex + 8, (ey + ay) / 2 - 8, "v_q", 13, WARN)
    text(draw, ex + 8, (ey + ay) / 2 + 8, "Wind", 11, WARN)

    # Das Ergebnis liegt auf der gewollten Linie
    pfeil(draw, ax, ay, ex, ay, GUT, 2)
    draw.ellipse([(ex - 4) * S, (ay - 4) * S, (ex + 4) * S, (ay + 4) * S], fill=GUT)

    bogen(draw, ax, ay, 66, -alpha, 0, WARN, 1)
    text(draw, ax + 74, ay - 20, "α", 13, WARN)

    text(draw, 22, 210, "sin α = v_q / v", 12, TEXT)
    text(draw, 22, 232, "kleine Winkel: sin α ≈ α im Bogenmaß, 1 rad = 57,3°",
         11, TEXT)
    text(draw, 22, 258, "α [°] ≈ (v_q / v) × 57,3   —  im Kopf: × 60", 13, GUT)
    sichern(bild, "skizze-vorhalt")


# ---------------------------------------------------------------------------
# r-hoehenmesser: die Luftsaeule ueber einem Hektopascal
# ---------------------------------------------------------------------------
def luftsaeule():
    bild, draw = leinwand()
    x0, x1 = 140, 250
    yo, yu = 70, 230
    draw.rectangle([x0 * S, yo * S, x1 * S, yu * S], outline=LINIE, width=2 * S)
    for i in range(1, 7):
        y = yo + (yu - yo) * i / 7.0
        gestrichelt(draw, x0 + 4, y, x1 - 4, y, DUENN)
    text(draw, (x0 + x1) / 2, yu - 34, "Luftsäule", 12, TEXT, mitte=True)

    pfeil(draw, x0 - 30, yo, x0 - 30, yu, BETONT, 2)
    pfeil(draw, x0 - 30, yu, x0 - 30, yo, BETONT, 2)
    text(draw, x0 - 38, (yo + yu) / 2 - 16, "Δh", 13, BETONT, rechts=True)
    text(draw, x0 - 38, (yo + yu) / 2 + 2, "8,3 m", 11, BETONT, rechts=True)

    strich(draw, x0, yo, x1 + 60, yo, DUENN, 1)
    strich(draw, x0, yu, x1 + 60, yu, DUENN, 1)
    text(draw, x1 + 66, yo - 8, "Druck oben", 11, DUENN)
    text(draw, x1 + 66, yu - 8, "Druck unten", 11, DUENN)
    text(draw, x1 + 66, yu + 10, "Δp = 1 hPa", 12, GUT)

    # Gewicht der Saeule
    pfeil(draw, (x0 + x1) / 2, yo + 30, (x0 + x1) / 2, yo + 78, ROT, 2)
    text(draw, (x0 + x1) / 2 + 8, yo + 52, "ρ·g·Δh", 12, ROT)

    text(draw, 24, 256, "Δp = ρ · g · Δh    →    Δh = Δp / (ρ·g)", 13, GUT)
    text(draw, 24, 276, "100 Pa ÷ (1,225 × 9,81) ≈ 8,3 m je Hektopascal", 11, TEXT)
    sichern(bild, "skizze-luftsaeule")


def main():
    global SPRACHE
    for SPRACHE in ("de", "en"):
        print("Skizzen (%s):" % SPRACHE)
        gleitflug()
        kurvenlast()
        schwerpunkt()
        wolkenbasis()
        vorhalt()
        luftsaeule()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
