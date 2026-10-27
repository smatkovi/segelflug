# -*- coding: utf-8 -*-
"""Trainiertes Netz als data/modell.bin schreiben (Format: tools/MODELL.md).

  python3 training/export.py training/endmodell.pt --ausgabe training/modell.bin \
      --referenz training/referenz

Schritte: BatchNorm einfalten, int8 je Ausgabekanal, Datei schreiben, Datei
mit numpy zurueckladen und streng pruefen, Vorwaertsrechnung aus der Datei
gegen das Float-Modell stellen (Genauigkeit auf der Pruefmenge), und die
Referenzpuffer samt referenz.json aus dem dequantisierten Modell erzeugen."""

import argparse
import json
import os
import struct
import sys

import numpy as np
import torch
import torch.nn.functional as F
import torchvision
from torchvision.ops.misc import Conv2dNormActivation
from torchvision.models.mobilenetv2 import InvertedResidual

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daten  # noqa: E402

KENNUNG = b"WOLKEN01"


def modell_laden(pfad):
    m = torchvision.models.mobilenet_v2(weights=None)
    m.classifier[1] = torch.nn.Linear(m.last_channel, len(daten.KLASSEN))
    m.load_state_dict(torch.load(pfad, map_location="cpu"))
    return m.eval()


def einfalten(conv, bn):
    """Faltung + BatchNorm -> Gewichte und Bias einer Faltung mit Bias."""
    w = conv.weight.detach().double()
    g = bn.weight.detach().double() / torch.sqrt(bn.running_var.detach().double() + bn.eps)
    b = bn.bias.detach().double() - bn.running_mean.detach().double() * g
    if conv.bias is not None:
        b = b + conv.bias.detach().double() * g
    return (w * g.view(-1, *([1] * (w.dim() - 1)))).float().numpy(), b.float().numpy()


def quantisieren(w):
    """Symmetrisch je Ausgabekanal (erste Achse): q int8, skalen float32."""
    flach = w.reshape(w.shape[0], -1)
    skalen = np.abs(flach).max(axis=1) / 127.0
    skalen = np.where(skalen > 0, skalen, 1.0).astype(np.float32)
    q = np.clip(np.rint(flach / skalen[:, None]), -127, 127).astype(np.int8)
    return q.reshape(w.shape), skalen


class Blob:
    def __init__(self):
        self.teile = []
        self.laenge = 0

    def anhaengen(self, arr):
        """Tensor anhaengen, Beginn auf 4 Byte ausgerichtet; gibt den Offset."""
        roh = np.ascontiguousarray(arr).tobytes()
        offset = self.laenge
        polster = (-len(roh)) % 4
        self.teile.append(roh + b"\0" * polster)
        self.laenge += len(roh) + polster
        return offset

    def bytes(self):
        return b"".join(self.teile)


def exportieren(modell):
    """Schichtenliste und Blob aus dem torchvision-Graphen."""
    schichten = []
    blob = Blob()

    def neu(schicht):
        schichten.append(schicht)
        return len(schichten)  # Index des erzeugten Tensors

    def faltung(conv, bn, relu6, quelle):
        w, b = einfalten(conv, bn)
        q, s = quantisieren(w)
        return neu({"art": "conv", "quelle": quelle,
                    "ein": conv.in_channels, "aus": conv.out_channels,
                    "kern": conv.kernel_size[0], "schritt": conv.stride[0],
                    "rand": conv.padding[0], "gruppen": conv.groups, "relu6": relu6,
                    "gewichte": blob.anhaengen(q), "skalen": blob.anhaengen(s),
                    "bias": blob.anhaengen(b.astype(np.float32))})

    aktuell = 0
    for block in modell.features:
        if isinstance(block, Conv2dNormActivation):
            aktuell = faltung(block[0], block[1], True, aktuell)
        elif isinstance(block, InvertedResidual):
            eingang = aktuell
            conv_offen = None
            for teil in block.conv:
                if isinstance(teil, Conv2dNormActivation):
                    aktuell = faltung(teil[0], teil[1], True, aktuell)
                elif isinstance(teil, torch.nn.Conv2d):
                    conv_offen = teil
                elif isinstance(teil, torch.nn.BatchNorm2d):
                    aktuell = faltung(conv_offen, teil, False, aktuell)
                    conv_offen = None
                else:
                    raise RuntimeError("unbekannter Teil %r" % teil)
            if block.use_res_connect:
                aktuell = neu({"art": "add", "quellen": [eingang, aktuell]})
        else:
            raise RuntimeError("unbekannter Block %r" % block)
    aktuell = neu({"art": "mittel", "quelle": aktuell})
    lin = modell.classifier[1]
    q, s = quantisieren(lin.weight.detach().numpy())
    neu({"art": "linear", "quelle": aktuell, "ein": lin.in_features, "aus": lin.out_features,
         "gewichte": blob.anhaengen(q), "skalen": blob.anhaengen(s),
         "bias": blob.anhaengen(lin.bias.detach().numpy().astype(np.float32))})
    return schichten, blob.bytes()


def schreiben(pfad, schichten, blob):
    kopf = {"format": 1, "eingabe": daten.EINGABE, "mittel": daten.MITTEL,
            "streuung": daten.STREUUNG, "klassen": daten.KLASSEN,
            "bytes": len(blob), "schichten": schichten}
    text = json.dumps(kopf, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    text += b" " * ((-(12 + len(text))) % 4)
    with open(pfad, "wb") as f:
        f.write(KENNUNG)
        f.write(struct.pack("<I", len(text)))
        f.write(text)
        f.write(blob)


# ---- Zurueckladen, nur mit numpy, und streng pruefen ------------------------

def lesen(pfad):
    with open(pfad, "rb") as f:
        roh = f.read()
    assert roh[:8] == KENNUNG, "Kennung fehlt"
    n = struct.unpack("<I", roh[8:12])[0]
    assert (12 + n) % 4 == 0, "Blob nicht ausgerichtet"
    kopf = json.loads(roh[12:12 + n].decode("utf-8"))
    assert b"\0" not in roh[12:12 + n]
    blob = roh[12 + n:]
    assert len(blob) == kopf["bytes"], "bytes stimmt nicht: %d != %d" % (len(blob), kopf["bytes"])
    assert kopf["klassen"] == daten.KLASSEN and kopf["eingabe"] == daten.EINGABE

    def tensor(offset, dtype, anzahl):
        assert offset % 4 == 0, "Tensor nicht ausgerichtet"
        groesse = anzahl * np.dtype(dtype).itemsize
        assert offset + groesse <= len(blob), "Tensor ragt aus dem Blob"
        return np.frombuffer(blob, dtype=dtype, count=anzahl, offset=offset)

    # Kanalzahl je Tensor mitfuehren, damit die Kette stimmt.
    kanaele = {0: 3}
    gewichte = {}
    for i, s in enumerate(kopf["schichten"]):
        aus = i + 1
        if s["art"] == "conv":
            assert s["quelle"] < aus and kanaele[s["quelle"]] == s["ein"], "conv %d: Kette" % i
            n_w = s["aus"] * (s["ein"] // s["gruppen"]) * s["kern"] * s["kern"]
            q = tensor(s["gewichte"], np.int8, n_w).reshape(s["aus"], s["ein"] // s["gruppen"], s["kern"], s["kern"])
            sk = tensor(s["skalen"], "<f4", s["aus"])
            b = tensor(s["bias"], "<f4", s["aus"])
            gewichte[i] = (q.astype(np.float32) * sk[:, None, None, None], b.copy())
            kanaele[aus] = s["aus"]
        elif s["art"] == "add":
            a, c = s["quellen"]
            assert a < aus and c < aus and kanaele[a] == kanaele[c], "add %d: Kette" % i
            kanaele[aus] = kanaele[a]
        elif s["art"] == "mittel":
            assert s["quelle"] < aus
            kanaele[aus] = kanaele[s["quelle"]]
        elif s["art"] == "linear":
            assert s["quelle"] < aus and kanaele[s["quelle"]] == s["ein"], "linear: Kette"
            q = tensor(s["gewichte"], np.int8, s["aus"] * s["ein"]).reshape(s["aus"], s["ein"])
            sk = tensor(s["skalen"], "<f4", s["aus"])
            b = tensor(s["bias"], "<f4", s["aus"])
            gewichte[i] = (q.astype(np.float32) * sk[:, None], b.copy())
            kanaele[aus] = s["aus"]
        else:
            raise AssertionError("unbekannte Art %r" % s["art"])
    assert kopf["schichten"][-1]["art"] == "linear" and kanaele[len(kopf["schichten"])] == len(daten.KLASSEN)
    return kopf, gewichte


@torch.no_grad()
def vorwaerts(kopf, gewichte, x):
    """Die Datei durchrechnen (float32, CPU) -- das dequantisierte Modell.
    x: [N,3,E,E] float32-Tensor."""
    t = {0: x}
    for i, s in enumerate(kopf["schichten"]):
        if s["art"] == "conv":
            w, b = gewichte[i]
            y = F.conv2d(t[s["quelle"]], torch.from_numpy(w), torch.from_numpy(b),
                         stride=s["schritt"], padding=s["rand"], groups=s["gruppen"])
            if s["relu6"]:
                y = torch.clamp(y, 0.0, 6.0)
        elif s["art"] == "add":
            y = t[s["quellen"][0]] + t[s["quellen"][1]]
        elif s["art"] == "mittel":
            y = t[s["quelle"]].mean(dim=(2, 3))
        else:
            w, b = gewichte[i]
            y = F.linear(t[s["quelle"]], torch.from_numpy(w), torch.from_numpy(b))
        t[i + 1] = y
    return t[len(kopf["schichten"])]


def genauigkeit(lg, kennungen):
    r = 0
    for l, k in zip(lg, kennungen):
        oben = daten.KLASSEN[int(torch.argmax(l))]
        r += (oben in daten.CUMULUS) if k == "cu-zyklus" else (oben == k)
    return r / max(len(kennungen), 1)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("modell")
    p.add_argument("--ausgabe", default="modell.bin")
    p.add_argument("--referenz", default="referenz")
    p.add_argument("--je-klasse", type=int, default=3)
    args = p.parse_args()
    torch.set_num_threads(8)

    modell = modell_laden(args.modell)
    schichten, blob = exportieren(modell)
    schreiben(args.ausgabe, schichten, blob)
    groesse = os.path.getsize(args.ausgabe)
    arten = {}
    for s in schichten:
        arten[s["art"]] = arten.get(s["art"], 0) + 1
    print("Geschrieben: %s  %d Byte (%.2f MB), Blob %d Byte, Schichten %s" % (
        args.ausgabe, groesse, groesse / 1e6, len(blob), arten))
    assert groesse <= 4 * 1024 * 1024, "Datei groesser als 4 MB"

    kopf, gewichte = lesen(args.ausgabe)
    print("Zurueckgeladen: %d Schichten, Kopf %d Byte, Blob ok" % (len(kopf["schichten"]), len(json.dumps(kopf))))

    # Pruefmenge: Float-Modell gegen die Datei.
    pruef = daten.pruefmenge()
    x = torch.from_numpy(np.stack([daten.eingabe(pf) for pf, _ in pruef]))
    kennungen = [k for _, k in pruef]
    with torch.no_grad():
        lg_float = modell(x)
    lg_datei = vorwaerts(kopf, gewichte, x)
    g_float, g_datei = genauigkeit(lg_float, kennungen), genauigkeit(lg_datei, kennungen)
    print("Top-1 auf %d Pruefbildern: Float %.1f %%  Datei (int8 dequantisiert) %.1f %%  max|dLogit| %.3f" % (
        len(pruef), 100 * g_float, 100 * g_datei, float((lg_float - lg_datei).abs().max())))
    if g_datei < g_float - 0.015:
        print("WARNUNG: Quantisierung kostet mehr als ~1 Punkt")

    # Referenzen: je Klasse ein paar Bilder, aus genau dem .rgb-Puffer gerechnet.
    os.makedirs(args.referenz, exist_ok=True)
    for alt in os.listdir(args.referenz):
        os.remove(os.path.join(args.referenz, alt))
    referenz = {}
    je = {}
    for pfad, k in pruef:
        je.setdefault(k, 0)
        if je[k] >= args.je_klasse:
            continue
        je[k] += 1
        name = "%s-%d.rgb" % (k, je[k])
        puffer = daten.gestaucht(daten.bild_oeffnen(pfad))
        assert puffer.shape == (daten.EINGABE, daten.EINGABE, 3) and puffer.dtype == np.uint8
        with open(os.path.join(args.referenz, name), "wb") as f:
            f.write(puffer.tobytes())
        lg = vorwaerts(kopf, gewichte, torch.from_numpy(daten.normalisiert(puffer))[None])[0]
        referenz[name] = {"datei": os.path.relpath(pfad, daten.WURZEL), "klasse": k,
                          "logits": [float(v) for v in lg]}
    with open(os.path.join(args.referenz, "referenz.json"), "w") as f:
        json.dump(referenz, f, indent=1, ensure_ascii=False)
    print("Referenz: %d Puffer in %s" % (len(referenz), args.referenz))


if __name__ == "__main__":
    main()
