#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draws the cloud types a glider pilot has to recognise.

Drawings first, photographs under them. A photograph shows one particular
sky on one particular day, with the diagnostic feature -- the sharp flat
base, the fibrous top, the tilt -- buried among everything else that
happened to be in frame. A drawing can show the feature and nothing else,
and that is what recognition starts from. Finding the same feature again
in a crowded frame is the second half, and that is what the real photos
under each drawing are for (wolkenfotos.py, tools/fotos.py).

Everything is drawn at 3x and scaled down, so the soft edges stay soft.

    tools/clouds.py            # -> bilder/*.png
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "bilder")

W, H = 440, 300          # final size
S = 3                    # oversampling

SKY_TOP = (58, 118, 186)
SKY_BOTTOM = (168, 202, 232)
GROUND = (86, 108, 68)
CLOUD_LIT = (252, 252, 255)
CLOUD_MID = (226, 230, 240)
CLOUD_DARK = (150, 158, 176)
CLOUD_BASE = (110, 118, 138)
ICE = (238, 242, 250)


def canvas(horizon=0.86):
    image = Image.new("RGB", (W * S, H * S))
    draw = ImageDraw.Draw(image)
    top = int(H * S * horizon)
    for y in range(top):
        t = y / float(max(1, top - 1))
        draw.line([(0, y), (W * S, y)],
                  fill=tuple(int(SKY_TOP[i] + (SKY_BOTTOM[i] - SKY_TOP[i]) * t)
                             for i in range(3)))
    draw.rectangle([0, top, W * S, H * S], fill=GROUND)
    return image, draw


def blob(draw, cx, cy, r, colour):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)


def puff(draw, cx, cy, r, rng, colour_dark, colour_mid, colour_lit,
         density=14, spread=1.0):
    """One rounded cloud mass, built from many overlapping circles.

    A single ellipse reads as a shape; a cloud has to read as a *lump of
    lumps*. Three passes -- shadowed, middle, lit -- put the light where the
    sun is, at the top left.
    """
    for _ in range(density):
        a = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(0, r * 0.55 * spread)
        blob(draw, cx + math.cos(a) * d, cy + math.sin(a) * d * 0.62,
             r * rng.uniform(0.45, 0.72), colour_dark)
    for _ in range(density):
        a = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(0, r * 0.50 * spread)
        blob(draw, cx + math.cos(a) * d, cy + math.sin(a) * d * 0.62 - r * 0.10,
             r * rng.uniform(0.40, 0.64), colour_mid)
    for _ in range(density):
        a = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(0, r * 0.42 * spread)
        blob(draw, cx + math.cos(a) * d - r * 0.08,
             cy + math.sin(a) * d * 0.62 - r * 0.26,
             r * rng.uniform(0.32, 0.55), colour_lit)


def model(mask, lumps, base_y, base_strength=1.0):
    """Paint the inside of a cloud: vertical shading plus lump modelling.

    The vertical gradient alone gives a smooth silhouette, which is exactly
    what a cumulus is not. The light on each separate mass -- bright on its
    upper left, shadow under its lower right -- is what makes it read as a
    heap of lumps rather than a blob, and heaps of lumps is the whole
    recognition cue.
    """
    box = mask.getbbox()
    if box is None:
        return None
    top, bottom = box[1], box[3]

    body = Image.new("RGB", mask.size)
    painter = ImageDraw.Draw(body)
    for y in range(top, bottom):
        t = (y - top) / float(max(1, bottom - top - 1))
        t = min(1.0, t * base_strength) ** 1.5
        painter.line([(0, y), (mask.size[0], y)],
                     fill=tuple(int(CLOUD_LIT[i] + (CLOUD_BASE[i] - CLOUD_LIT[i]) * t)
                                for i in range(3)))

    light = Image.new("L", mask.size, 0)
    shade = Image.new("L", mask.size, 0)
    lightPainter = ImageDraw.Draw(light)
    shadePainter = ImageDraw.Draw(shade)
    for x, y, r in lumps:
        lightPainter.ellipse([x - r * 0.62 - r * 0.20, y - r * 0.62 - r * 0.26,
                              x + r * 0.62 - r * 0.20, y + r * 0.62 - r * 0.26],
                             fill=150)
        shadePainter.ellipse([x - r * 0.80, y - r * 0.10,
                              x + r * 0.80, y + r * 0.95], fill=120)
    light = light.filter(ImageFilter.GaussianBlur(5 * S))
    shade = shade.filter(ImageFilter.GaussianBlur(6 * S))

    body = Image.composite(Image.new("RGB", mask.size, CLOUD_LIT), body, light)
    body = Image.composite(Image.new("RGB", mask.size, CLOUD_DARK), body, shade)
    return body


def cumulus(image, cx, base_y, width, height, rng, flat_base=True,
            ragged=False, cauliflower=False):
    """A heap cloud: rounded masses sitting on a flat base.

    That base is the condensation level and the single most useful line in
    the sky -- the same height for every thermal cloud in the same air mass,
    and the height at which the lift stops. It is made by *cutting* the
    cloud off there rather than by drawing a bar underneath: below that
    height the air is simply not saturated, so nothing is there, and only a
    cut looks as razor-straight as the real thing.
    """
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    white = (255, 255, 255, 255)
    lumps = []

    count = max(3, int(width / 34))
    for i in range(count):
        t = (i + 0.5) / count
        x = cx - width / 2 + t * width
        fat = 1.0 - abs(t - 0.5) * 1.5
        r = height * (0.34 + 0.40 * max(0.10, fat)) * rng.uniform(0.85, 1.12)
        y = base_y - r * rng.uniform(0.80, 1.00)
        if cauliflower:
            y -= height * 0.34 * max(0.0, fat) ** 0.7
        lumps.append((x, y, r))
        for _ in range(int(8 + r / (4 * S))):
            a = rng.uniform(0, 2 * math.pi)
            d = rng.uniform(0, r * 0.50)
            sub = r * rng.uniform(0.44, 0.70)
            blob(draw, x + math.cos(a) * d, y + math.sin(a) * d * 0.66, sub, white)
            lumps.append((x + math.cos(a) * d, y + math.sin(a) * d * 0.66, sub))
        if not ragged:
            draw.rectangle([x - r * 0.72, y, x + r * 0.72, base_y], fill=white)

    alpha = layer.split()[3].filter(ImageFilter.GaussianBlur(1.3 * S))
    alpha = alpha.point(lambda v: 0 if v < 120 else 255)
    if not ragged:
        cut = Image.new("L", alpha.size, 255)
        ImageDraw.Draw(cut).rectangle([0, int(base_y), alpha.size[0], alpha.size[1]],
                                      fill=0)
        alpha = Image.composite(alpha, Image.new("L", alpha.size, 0), cut)

    body = model(alpha, lumps, base_y, 1.15 if flat_base else 0.7)
    if body is None:
        return image
    return Image.composite(body, image, alpha)


def save(image, name):
    os.makedirs(OUT, exist_ok=True)
    small = image.resize((W, H), Image.LANCZOS)
    path = os.path.join(OUT, name + ".png")
    small.save(path)
    print("%-26s %s" % (name, path))


def soften(image, radius=2.2):
    return image.filter(ImageFilter.GaussianBlur(radius * S * 0.4))


# ---------------------------------------------------------------------------

def cumulus_humilis():
    rng = random.Random(11)
    image, draw = canvas()
    base = int(H * S * 0.52)
    for cx, w, h in ((W * S * 0.22, W * S * 0.22, H * S * 0.13),
                     (W * S * 0.52, W * S * 0.26, H * S * 0.15),
                     (W * S * 0.82, W * S * 0.20, H * S * 0.12)):
        image = cumulus(image, cx, base, w, h, rng)
    image = soften(image, 1.4)
    save(image, "cu-humilis")


def cumulus_congestus():
    rng = random.Random(23)
    image, draw = canvas()
    base = int(H * S * 0.62)
    image = cumulus(image, W * S * 0.50, base, W * S * 0.30, H * S * 0.46,
                    rng, cauliflower=True)
    image = cumulus(image, W * S * 0.16, base, W * S * 0.16, H * S * 0.11, rng)
    image = soften(image, 1.5)
    save(image, "cu-congestus")


def cumulonimbus():
    rng = random.Random(31)
    image, draw = canvas()
    base = int(H * S * 0.74)
    image = cumulus(image, W * S * 0.44, base, W * S * 0.30, H * S * 0.34,
                    rng, cauliflower=True)
    draw = ImageDraw.Draw(image)
    # the anvil: ice, blown downwind, fibrous rather than lumpy
    # The anvil is the diagnosis: once the top glaciates it stops being
    # knobbly water and becomes fibrous ice, spreading downwind under the
    # tropopause. Drawn as many soft streaks, never as a plate.
    top = int(H * S * 0.10)
    anvil = Image.new("RGBA", image.size, (0, 0, 0, 0))
    painter = ImageDraw.Draw(anvil)
    for _ in range(420):
        t = rng.random() ** 0.7
        x0 = W * S * (0.22 + t * 0.70)
        thickness = (1.0 - t) * H * S * 0.060 + H * S * 0.016
        y = top + H * S * 0.070 + rng.uniform(-thickness, thickness) \
            - t * H * S * 0.030
        length = W * S * rng.uniform(0.06, 0.20) * (0.4 + t)
        painter.line([(x0, y), (x0 + length, y - H * S * rng.uniform(0.0, 0.015))],
                     fill=(255, 255, 255, int(rng.uniform(90, 190))),
                     width=int(rng.uniform(1.5, 4.0) * S))
    anvil = anvil.filter(ImageFilter.GaussianBlur(1.8 * S))
    image = Image.alpha_composite(image.convert("RGBA"), anvil).convert("RGB")
    draw = ImageDraw.Draw(image)
    # rain shaft
    for i in range(70):
        x = W * S * rng.uniform(0.36, 0.60)
        y = base + rng.uniform(0, H * S * 0.14)
        draw.line([(x, y), (x - 3 * S, y + 9 * S)], fill=(120, 130, 150),
                  width=int(1 * S))
    image = soften(image, 1.6)
    save(image, "cumulonimbus")


def stratocumulus():
    """A lid of merged lumps: no gaps, no sharp base, and no more sun."""
    rng = random.Random(43)
    image, draw = canvas()
    base = int(H * S * 0.46)
    for i in range(22):
        x = W * S * (i / 21.0) + rng.uniform(-10 * S, 10 * S)
        r = H * S * rng.uniform(0.055, 0.095)
        puff(draw, x, base - r * 0.9, r, rng,
             CLOUD_DARK, CLOUD_MID, CLOUD_LIT, density=10, spread=1.3)
    # underside: shaded and uneven, the way a closing layer looks
    for _ in range(220):
        x = rng.uniform(0, W * S)
        blob(draw, x, base - H * S * rng.uniform(0.0, 0.028),
             H * S * rng.uniform(0.014, 0.030), CLOUD_BASE)
    image = soften(image, 2.0)
    save(image, "stratocumulus")


def cirrus():
    """Ice cloud, drawn out by the wind into hooks and feathers."""
    rng = random.Random(57)
    image, draw = canvas()
    for _ in range(11):
        y0 = H * S * rng.uniform(0.08, 0.40)
        x0 = W * S * rng.uniform(0.00, 0.60)
        length = W * S * rng.uniform(0.22, 0.42)
        droop = H * S * rng.uniform(0.04, 0.09)
        # the head of the feather is denser, the tail thins out
        steps = 44
        for k in range(steps):
            t = k / float(steps - 1)
            x = x0 + length * t
            y = y0 - droop * math.sin(t * 1.3) + H * S * 0.012 * math.sin(t * 9)
            thickness = (1.0 - t) ** 1.4 * 3.4 * S + 0.5 * S
            for j in range(3):
                jitter = rng.uniform(-1.0, 1.0) * S
                blob(draw, x + jitter, y + jitter * 1.6, thickness, ICE)
        # the hook at the head
        for k in range(10):
            t = k / 9.0
            blob(draw, x0 + length * 0.02 - t * W * S * 0.02,
                 y0 + t * H * S * 0.025, (1.0 - t) * 3.0 * S + S, ICE)
    image = soften(image, 1.1)
    save(image, "cirrus")


def altocumulus_castellanus():
    """Turrets on a common base: the air is unstable up there as well.

    The diagnostic is the ratio -- an element taller than it is wide means
    convection at that level, and that is what separates this from the
    harmless flat sheep of ordinary altocumulus.
    """
    rng = random.Random(67)
    image, draw = canvas()
    base = int(H * S * 0.42)
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    painter = ImageDraw.Draw(layer)
    white = (255, 255, 255, 255)
    lumps = []

    # the common base: a continuous, slightly uneven band
    for i in range(70):
        x = W * S * (0.05 + 0.90 * i / 69.0)
        r = H * S * rng.uniform(0.026, 0.040)
        painter.ellipse([x - r * 2.0, base - r * 2.0, x + r * 2.0, base],
                        fill=white)
        lumps.append((x, base - r * 0.9, r * 1.6))

    # the turrets: taller than wide, of differing heights
    for i in range(9):
        x = W * S * (0.10 + i * 0.096) + rng.uniform(-5 * S, 5 * S)
        h = H * S * rng.uniform(0.070, 0.130)
        r = H * S * rng.uniform(0.034, 0.046)
        steps = max(2, int(h / (r * 0.8)))
        for k in range(steps):
            y = base - r * 0.8 - k * (h / steps)
            rr = r * (1.0 - 0.18 * k / steps)
            for _ in range(7):
                a = rng.uniform(0, 2 * math.pi)
                d = rng.uniform(0, rr * 0.40)
                painter.ellipse([x + math.cos(a) * d - rr,
                                 y + math.sin(a) * d - rr,
                                 x + math.cos(a) * d + rr,
                                 y + math.sin(a) * d + rr], fill=white)
            lumps.append((x, y, rr))

    alpha = layer.split()[3].filter(ImageFilter.GaussianBlur(1.1 * S))
    alpha = alpha.point(lambda v: 0 if v < 120 else 255)
    body = model(alpha, lumps, base, 0.9)
    if body is not None:
        image = Image.composite(body, image, alpha)
    image = image.filter(ImageFilter.GaussianBlur(0.8 * S))
    save(image, "ac-castellanus")


def lenticularis():
    rng = random.Random(71)
    image, draw = canvas()
    # mountain
    draw.polygon([(0, H * S * 0.86), (W * S * 0.22, H * S * 0.52),
                  (W * S * 0.44, H * S * 0.86)], fill=(64, 76, 62))
    # stacked lenses, standing still while the wind goes through them
    for k in range(3):
        cy = H * S * (0.22 + k * 0.10)
        rx = W * S * (0.20 - k * 0.02)
        ry = H * S * 0.035
        cx = W * S * (0.58 + k * 0.03)
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=CLOUD_LIT)
        draw.ellipse([cx - rx * 0.95, cy, cx + rx * 0.95, cy + ry * 1.2],
                     fill=CLOUD_MID)
    # rotor cloud under the lee: ragged, turning, and the dangerous one
    for i in range(9):
        x = W * S * (0.44 + i * 0.045)
        puff(draw, x, H * S * (0.64 + rng.uniform(-0.02, 0.02)),
             H * S * rng.uniform(0.045, 0.065), rng,
             (96, 104, 122), (150, 158, 176), (198, 204, 218),
             density=9, spread=1.2)
    image = soften(image, 1.5)
    save(image, "lenticularis")


def wolkenstrasse():
    rng = random.Random(83)
    image, draw = canvas(horizon=0.80)
    base = int(H * S * 0.42)
    # two rows running to the horizon -- the free motorway of a soaring day
    for row, (y0, scale) in enumerate(((0.42, 1.0), (0.33, 0.62))):
        for i in range(9):
            t = i / 8.0
            x = W * S * (0.02 + t * 0.96)
            w = W * S * 0.10 * scale * (1.0 - 0.45 * t)
            h = H * S * 0.075 * scale * (1.0 - 0.4 * t)
            image = cumulus(image, x, H * S * y0 - row * H * S * 0.02,
                            w, h, rng)
    image = soften(image, 1.5)
    save(image, "wolkenstrasse")


def zyklus():
    """One cumulus through its life: growing, mature, falling apart."""
    rng = random.Random(97)
    image, draw = canvas()
    base = int(H * S * 0.58)
    # growing: small, sharp, dark base
    image = cumulus(image, W * S * 0.18, base, W * S * 0.15, H * S * 0.16, rng)
    # mature: biggest, sharpest, darkest base
    image = cumulus(image, W * S * 0.50, base, W * S * 0.22, H * S * 0.28,
                    rng, cauliflower=True)
    draw = ImageDraw.Draw(image)
    # dying: no base left, edges coming apart into separate shreds
    for i in range(11):
        x = W * S * (0.78 + rng.uniform(-0.08, 0.10))
        y = base - H * S * rng.uniform(0.02, 0.22)
        puff(draw, x, y, H * S * rng.uniform(0.025, 0.050), rng,
             CLOUD_MID, CLOUD_LIT, CLOUD_LIT, density=6, spread=1.5)
    image = soften(image, 1.8)
    save(image, "cu-zyklus")


# ---------------------------------------------------------------------------
# w-tagesverlaeufe: vier Tage nebeneinander, vier Uhrzeiten untereinander
# ---------------------------------------------------------------------------

GRUND_TAFEL = (14, 14, 18)
TEXT_TAFEL = (226, 230, 240)
HAZE = (214, 222, 232)
VEIL = (236, 240, 246)
AS_GREY = (176, 184, 198)
NS_GREY = (118, 126, 142)

SPRACHE_TAFEL = "de"
EN_TAFEL = {
    "Cumulus-Tag": "cumulus day",
    "Überentwicklung": "overdevelopment",
    "Abschirmung": "shading out",
    "Warmfront": "warm front",
    "9 Uhr": "09:00", "12 Uhr": "12:00", "15 Uhr": "15:00", "18 Uhr": "18:00",
}


def schrift(groesse):
    for pfad in ("/usr/share/fonts/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/TTF/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(pfad):
            return ImageFont.truetype(pfad, groesse)
    return ImageFont.load_default()


def zelle(w, h, horizon=0.84, top=SKY_TOP, bottom=SKY_BOTTOM):
    """Ein kleiner Himmel fuer eine Tafelzelle -- canvas() in frei waehlbarer
    Groesse und mit waehlbaren Himmelsfarben, denn ein Tag unter Altostratus
    ist nicht blau."""
    image = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(image)
    oben = int(h * horizon)
    for y in range(oben):
        t = y / float(max(1, oben - 1))
        draw.line([(0, y), (w, y)],
                  fill=tuple(int(top[i] + (bottom[i] - top[i]) * t)
                             for i in range(3)))
    draw.rectangle([0, oben, w, h], fill=GROUND)
    return image, draw


def schleier(image, rng, dichte, farbe=VEIL, y0=0.0, y1=0.55):
    """Cirrostratus oder Altostratus: eine Schicht ohne Gestalt. Je dichter,
    desto mehr verschwindet das Blau -- genau das ist das Merkmal."""
    w, h = image.size
    lage = Image.new("RGBA", image.size, (0, 0, 0, 0))
    painter = ImageDraw.Draw(lage)
    for _ in range(int(140 * dichte)):
        x = rng.uniform(-w * 0.1, w * 1.1)
        y = h * rng.uniform(y0, y1)
        laenge = w * rng.uniform(0.15, 0.45)
        painter.line([(x, y), (x + laenge, y - h * rng.uniform(0.0, 0.02))],
                     fill=farbe + (int(60 + 120 * dichte),),
                     width=int(rng.uniform(2, 5) * S))
    lage = lage.filter(ImageFilter.GaussianBlur(2.5 * S))
    return Image.alpha_composite(image.convert("RGBA"), lage).convert("RGB")


def cirrusfaeden(image, rng, anzahl, x0=0.0, x1=0.6):
    w, h = image.size
    draw = ImageDraw.Draw(image)
    for _ in range(anzahl):
        y = h * rng.uniform(0.06, 0.32)
        x = w * rng.uniform(x0, x1)
        laenge = w * rng.uniform(0.18, 0.36)
        for k in range(24):
            t = k / 23.0
            dicke = (1.0 - t) ** 1.4 * 2.2 * S + 0.5 * S
            blob(draw, x + laenge * t, y - h * 0.05 * math.sin(t * 1.3),
                 dicke, ICE)
    return image


def sonne(image, cx, cy, r, halo=False, matt=False):
    draw = ImageDraw.Draw(image)
    if halo:
        draw.ellipse([cx - r * 3.2, cy - r * 3.2, cx + r * 3.2, cy + r * 3.2],
                     outline=(252, 250, 240), width=int(1.2 * S))
    farbe = (236, 236, 228) if matt else (255, 250, 214)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=farbe)
    return image


def fetzen(image, rng, anzahl, y_von, y_bis, hell=True):
    """Zerfallende Reste ohne Basis -- wie der Abend des Cumulus-Tags."""
    w, h = image.size
    draw = ImageDraw.Draw(image)
    for _ in range(anzahl):
        x = w * rng.uniform(0.05, 0.95)
        y = h * rng.uniform(y_von, y_bis)
        puff(draw, x, y, h * rng.uniform(0.05, 0.09), rng,
             CLOUD_MID if hell else CLOUD_DARK, CLOUD_LIT if hell else CLOUD_MID,
             CLOUD_LIT, density=5, spread=1.5)
    return image


def regen(image, rng, x0, x1, y0, anzahl=40):
    w, h = image.size
    draw = ImageDraw.Draw(image)
    for _ in range(anzahl):
        x = w * rng.uniform(x0, x1)
        y = y0 + rng.uniform(0, h * 0.10)
        draw.line([(x, y), (x - 2 * S, y + 7 * S)], fill=(120, 130, 150),
                  width=int(1 * S))
    return image


def tafel_text(draw, x, y, inhalt, groesse, mitte=False):
    if SPRACHE_TAFEL != "de":
        inhalt = EN_TAFEL.get(inhalt, inhalt)
    f = schrift(groesse * S)
    kasten = draw.textbbox((0, 0), inhalt, font=f)
    breite = (kasten[2] - kasten[0]) / float(S)
    if mitte:
        x -= breite / 2.0
    draw.text((x * S, y * S), inhalt, font=f, fill=TEXT_TAFEL)


def tagesverlaeufe():
    """Vier Tage, je um 9, 12, 15 und 18 Uhr.

    Die Lektion sagt, dass ein Flugtag auf sehr verschiedene Arten laufen
    kann und dass der Morgen schon verraet, welche. Dazu gehoert ein Bild,
    in dem die Zeilen die Tage und die Spalten die Stunden sind: Man liest
    eine Zeile von links nach rechts und sieht den Tag werden, und man liest
    die erste Spalte von oben nach unten und sieht, wie wenig sich vier
    Morgen unterscheiden, die vier verschiedene Tage werden.
    """
    global SPRACHE_TAFEL
    for SPRACHE_TAFEL in ("de", "en"):
        rng = random.Random(113)
        image = Image.new("RGB", (W * S, H * S), GRUND_TAFEL)
        draw = ImageDraw.Draw(image)
        links, oben, luecke = 88, 18, 4
        cw = (W - links - luecke * 5) // 4
        ch = (H - oben - luecke * 5) // 4
        stunden = ("9 Uhr", "12 Uhr", "15 Uhr", "18 Uhr")
        zeilen = ("Cumulus-Tag", "Überentwicklung", "Abschirmung", "Warmfront")

        for spalte, stunde in enumerate(stunden):
            x = links + luecke + spalte * (cw + luecke)
            tafel_text(draw, x + cw / 2.0, 3, stunde, 10, mitte=True)
        for zeile, name in enumerate(zeilen):
            y = oben + luecke + zeile * (ch + luecke)
            tafel_text(draw, 4, y + ch / 2.0 - 7, name, 9)

        w, h = cw * S, ch * S
        szenen = {}

        # -- Zeile 1: der klassische Cumulus-Tag ------------------------------
        bild, _ = zelle(w, h)
        bild = sonne(bild, w * 0.80, h * 0.20, h * 0.05)
        szenen[(0, 0)] = bild                                  # blau, nichts
        bild, _ = zelle(w, h)
        basis = int(h * 0.58)
        for cx, bw in ((0.22, 0.16), (0.52, 0.18), (0.80, 0.15)):
            bild = cumulus(bild, w * cx, basis, w * bw, h * 0.09, rng)
        szenen[(0, 1)] = bild                                  # erste Humilis
        bild, _ = zelle(w, h)
        basis = int(h * 0.40)
        for cx, bw in ((0.20, 0.22), (0.58, 0.28), (0.88, 0.18)):
            bild = cumulus(bild, w * cx, basis, w * bw, h * 0.20, rng,
                           cauliflower=True)
        szenen[(0, 2)] = bild                                  # Mediocris, hoch
        bild, _ = zelle(w, h, top=(70, 120, 180), bottom=(220, 200, 180))
        bild = fetzen(bild, rng, 7, 0.22, 0.42)
        szenen[(0, 3)] = bild                                  # Zerfall

        # -- Zeile 2: Ueberentwicklung ----------------------------------------
        bild, _ = zelle(w, h)
        basis = int(h * 0.56)
        for cx, bw in ((0.18, 0.18), (0.50, 0.22), (0.82, 0.18)):
            bild = cumulus(bild, w * cx, basis, w * bw, h * 0.26, rng,
                           cauliflower=True)
        szenen[(1, 0)] = bild                                  # schon um 9
        bild, _ = zelle(w, h)
        basis = int(h * 0.62)
        bild = cumulus(bild, w * 0.50, basis, w * 0.34, h * 0.48, rng,
                       cauliflower=True)
        bild = cumulus(bild, w * 0.14, basis, w * 0.16, h * 0.14, rng)
        szenen[(1, 1)] = bild                                  # Congestus
        bild, _ = zelle(w, h)
        basis = int(h * 0.70)
        bild = cumulus(bild, w * 0.46, basis, w * 0.32, h * 0.44, rng,
                       cauliflower=True)
        bild = schleier(bild, rng, 0.6, farbe=ICE, y0=0.04, y1=0.22)
        bild = regen(bild, rng, 0.36, 0.60, basis)
        szenen[(1, 2)] = bild                                  # Cb mit Amboss
        bild, _ = zelle(w, h, top=(90, 100, 120), bottom=(150, 156, 170))
        bild = schleier(bild, rng, 1.0, farbe=AS_GREY, y0=0.0, y1=0.5)
        bild = fetzen(bild, rng, 6, 0.30, 0.55, hell=False)
        bild = regen(bild, rng, 0.55, 0.95, int(h * 0.55), 30)
        szenen[(1, 3)] = bild                                  # ausgebreitet, Schauer

        # -- Zeile 3: Abschirmung von Westen ----------------------------------
        bild, _ = zelle(w, h)
        bild = cirrusfaeden(bild, rng, 4, 0.0, 0.3)            # links = Westen
        basis = int(h * 0.60)
        bild = cumulus(bild, w * 0.70, basis, w * 0.14, h * 0.08, rng)
        szenen[(2, 0)] = bild
        bild, _ = zelle(w, h)
        bild = schleier(bild, rng, 0.5, y0=0.0, y1=0.45)
        bild = sonne(bild, w * 0.74, h * 0.18, h * 0.045, halo=True)
        basis = int(h * 0.52)
        for cx, bw in ((0.22, 0.18), (0.56, 0.16)):
            bild = cumulus(bild, w * cx, basis, w * bw, h * 0.10, rng)
        szenen[(2, 1)] = bild                                  # Halo, Cu darunter
        bild, _ = zelle(w, h, top=(150, 168, 190), bottom=(200, 208, 220))
        bild = schleier(bild, rng, 0.9, y0=0.0, y1=0.5)
        bild = sonne(bild, w * 0.70, h * 0.20, h * 0.045, matt=True)
        bild = fetzen(bild, rng, 4, 0.40, 0.55)
        szenen[(2, 2)] = bild                                  # milchig, Cu sterben
        bild, _ = zelle(w, h, top=(140, 150, 168), bottom=(190, 196, 206))
        bild = schleier(bild, rng, 1.0, farbe=AS_GREY, y0=0.0, y1=0.55)
        szenen[(2, 3)] = bild                                  # grau, nichts

        # -- Zeile 4: Warmfront -----------------------------------------------
        bild, _ = zelle(w, h)
        bild = cirrusfaeden(bild, rng, 6, 0.0, 0.6)
        szenen[(3, 0)] = bild                                  # Cirrus-Haken
        bild, _ = zelle(w, h)
        bild = schleier(bild, rng, 0.7, y0=0.0, y1=0.5)
        bild = sonne(bild, w * 0.52, h * 0.24, h * 0.05, halo=True)
        szenen[(3, 1)] = bild                                  # Cirrostratus, Halo
        bild, _ = zelle(w, h, top=(128, 138, 156), bottom=(176, 182, 194))
        bild = schleier(bild, rng, 1.0, farbe=AS_GREY, y0=0.0, y1=0.6)
        bild = sonne(bild, w * 0.52, h * 0.24, h * 0.045, matt=True)
        szenen[(3, 2)] = bild                                  # Altostratus
        bild, _ = zelle(w, h, top=(92, 100, 116), bottom=(140, 146, 158))
        bild = schleier(bild, rng, 1.2, farbe=NS_GREY, y0=0.0, y1=0.7)
        bild = regen(bild, rng, 0.05, 0.95, int(h * 0.40), 90)
        szenen[(3, 3)] = bild                                  # Nimbostratus

        for (zeile, spalte), szene in szenen.items():
            szene = szene.filter(ImageFilter.GaussianBlur(0.5 * S))
            x = (links + luecke + spalte * (cw + luecke)) * S
            y = (oben + luecke + zeile * (ch + luecke)) * S
            image.paste(szene, (x, y))

        name = "tagesverlaeufe" + ("" if SPRACHE_TAFEL == "de" else ".en")
        save(image, name)


def main():
    cumulus_humilis()
    cumulus_congestus()
    cumulonimbus()
    stratocumulus()
    cirrus()
    altocumulus_castellanus()
    lenticularis()
    wolkenstrasse()
    zyklus()
    tagesverlaeufe()


if __name__ == "__main__":
    main()
