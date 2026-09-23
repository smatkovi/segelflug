#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draws the cloud types a glider pilot has to recognise.

Drawings rather than photographs, on purpose. A photograph shows one
particular sky on one particular day, with the diagnostic feature -- the
sharp flat base, the fibrous top, the tilt -- buried among everything else
that happened to be in frame. A drawing can show the feature and nothing
else, which is what recognition has to be learned from. The photographs
come later, in the sky.

Everything is drawn at 3x and scaled down, so the soft edges stay soft.

    tools/clouds.py            # -> bilder/*.png
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

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


if __name__ == "__main__":
    main()
