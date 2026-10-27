# -*- coding: utf-8 -*-
"""Wolkennetz trainieren (MobileNetV2, 160x160, 14 Klassen).

Aufrufe (auf arch, in ~/wolken-train):
  python3 training/train.py messen --falten 5 --ausgabe training/messen.pt
      Fuenffache Kreuzprobe ueber die kuratierten Bilder: je Falte stecken
      vier Fuenftel davon im Training, ein Fuenftel ist Pruefmenge; dazu
      immer 10 % Rueckhalt der Nur-CCSN-Klassen.  Gemessen wird mit fester
      Epochenzahl (keine Auswahl auf der Pruefmenge), berichtet wird die
      Summe ueber alle Falten.  Schreibt <ausgabe>.json (Genauigkeiten,
      Verlauf je Epoche ueber die Falten gemittelt, Verwechslungsmatrix)
      und <ausgabe>.saeubern.txt (Kandidaten, die das Netz mit > 0.9 anders
      sieht als beschriftet; aus der letzten Falte).
  python3 training/train.py messen --falten 1 --ausgabe ...
      Wie frueher: Training ohne die kuratierten Bilder, alle 136 pruefen.
  python3 training/train.py endmodell --epochen N --ausgabe training/endmodell.pt
      Alles (auch die kuratierten Bilder), keine Pruefmenge, N Epochen.

Rezept: Das erste Rezept (alles mit 2e-4, 30 Epochen) wurde von Epoche zu
Epoche schlechter auf den kuratierten Fotos, waehrend es auf dem
CCSN-Rueckhalt besser wurde -- es lernte die CCSN-Bilder (256 px,
beschnittene Webfotos) auswendig und verlor die Handyfoto-Verteilung.
Darum jetzt: fruehe Bloecke eingefroren, Rueckgrat mit kleiner Lernrate,
Mixup, staerkere Augmentierung, und die Commons-/kuratierten Bilder (die
der Handyverteilung am naechsten sind) werden haeufiger gezogen.

Optionen: --ausschluss DATEI (eine Zeile je Pfad, aus der Saeuberung),
          --cpu (Ausweichen, wenn ROCm ausfaellt), --batch, --kopf-epochen,
          --lr (Kopf), --lr-rueckgrat, --einfrieren N (features[:N]),
          --mixup ALPHA, --quelle-kandidat F, --quelle-kuratiert F."""

import argparse
import hashlib
import json
import os
import random
import sys
import time

import numpy as np
import torch
import torch.nn.functional as F
import torchvision
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler
from torchvision import transforms

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daten  # noqa: E402

GLAETTUNG = 0.05


def netz():
    m = torchvision.models.mobilenet_v2(weights=torchvision.models.MobileNet_V2_Weights.IMAGENET1K_V1)
    # Der vorgefertigte Kopf ist schon Dropout(0.2)+Linear; nur die Breite tauschen.
    m.classifier[1] = torch.nn.Linear(m.last_channel, len(daten.KLASSEN))
    return m


class Trainingsdaten(Dataset):
    def __init__(self, bilder):
        self.bilder = bilder
        self.wandel = transforms.Compose([
            transforms.RandomResizedCrop(daten.EINGABE, scale=(0.35, 1.0), ratio=(0.75, 1.33)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(12),
            transforms.ColorJitter(0.3, 0.3, 0.25, 0.03),
            transforms.RandomApply([transforms.GaussianBlur(3, sigma=(0.1, 1.5))], p=0.2),
            transforms.RandomGrayscale(p=0.03),
            transforms.ToTensor(),
            transforms.Normalize(daten.MITTEL, daten.STREUUNG),
        ])

    def __len__(self):
        return len(self.bilder)

    def __getitem__(self, i):
        pfad, z, _ = self.bilder[i]
        x = self.wandel(daten.bild_oeffnen(pfad))
        z = (1 - GLAETTUNG) * z + GLAETTUNG / len(daten.KLASSEN)
        return x, torch.from_numpy(z)


def pruefpuffer(liste):
    """Pruefbilder einmal stauchen und als Tensor halten (wenige hundert)."""
    if not liste:
        return torch.zeros(0, 3, daten.EINGABE, daten.EINGABE), []
    x = np.stack([daten.eingabe(p) for p, _ in liste])
    return torch.from_numpy(x), [k for _, k in liste]


@torch.no_grad()
def logits_von(modell, x, geraet, batch=64):
    modell.eval()
    aus = []
    for i in range(0, len(x), batch):
        aus.append(modell(x[i:i + batch].to(geraet)).float().cpu())
    return torch.cat(aus) if aus else torch.zeros(0, len(daten.KLASSEN))


def richtig(kennung, reihenfolge, n):
    """Steckt die Kennung in den ersten n vorhergesagten Klassen?  cu-zyklus
    (Cumulus allgemein) gilt bei jeder der drei Stufen."""
    kopf = [daten.KLASSEN[i] for i in reihenfolge[:n]]
    if kennung == "cu-zyklus":
        return any(k in daten.CUMULUS for k in kopf)
    return kennung in kopf


def bewertung(lg, kennungen):
    """Top-1/Top-3 gesamt und je Klasse plus Verwechslungsmatrix (Zeile =
    beschriftet, Spalte = vorhergesagt; cu-zyklus als eigene Zeile)."""
    reihen = sorted(set(kennungen), key=lambda k: (daten.INDEX.get(k, 99), k))
    je = {k: {"n": 0, "top1": 0, "top3": 0} for k in reihen}
    matrix = {k: [0] * len(daten.KLASSEN) for k in reihen}
    t1 = t3 = 0
    for l, k in zip(lg, kennungen):
        ordnung = torch.argsort(l, descending=True).tolist()
        r1, r3 = richtig(k, ordnung, 1), richtig(k, ordnung, 3)
        je[k]["n"] += 1
        je[k]["top1"] += r1
        je[k]["top3"] += r3
        matrix[k][ordnung[0]] += 1
        t1 += r1
        t3 += r3
    n = max(len(kennungen), 1)
    return {"n": len(kennungen), "top1": t1 / n, "top3": t3 / n,
            "je_klasse": je, "matrix": matrix}


def matrix_text(matrix):
    kurz = [k[:5] for k in daten.KLASSEN]
    zeilen = ["%-16s " % "" + " ".join("%5s" % s for s in kurz)]
    for k, z in matrix.items():
        zeilen.append("%-16s " % k + " ".join("%5d" % v for v in z))
    return "\n".join(zeilen)


def bericht(name, erg):
    print("== %s: n=%d  Top-1 %.1f %%  Top-3 %.1f %%" % (
        name, erg["n"], 100 * erg["top1"], 100 * erg["top3"]))
    for k, v in erg["je_klasse"].items():
        print("   %-16s n=%3d  Top-1 %5.1f %%  Top-3 %5.1f %%" % (
            k, v["n"], 100 * v["top1"] / max(v["n"], 1), 100 * v["top3"] / max(v["n"], 1)))
    print(matrix_text(erg["matrix"]))


def falte_von(pfad, falten):
    """Stabile Zuordnung eines kuratierten Bildes zu einer Falte -- ueber den
    Dateinamen, nicht ueber die Reihenfolge, damit jeder Lauf dieselbe
    Aufteilung sieht."""
    h = hashlib.md5(os.path.basename(pfad).encode("utf-8")).hexdigest()
    return int(h[:8], 16) % falten


def trainieren(args, geraet, bilder, zaehl, pruef=None, kennung_pruef=None, pruef_r=None, kennung_r=None):
    """Ein Trainingslauf: Kopf, dann Feinabstimmung.  Gibt (modell, verlauf)
    zurueck; verlauf enthaelt je Epoche Verlust und -- wenn eine Pruefmenge
    da ist -- Top-1/Top-3 darauf."""
    quell = {"ccsn": 1.0, "kandidat": args.quelle_kandidat, "kuratiert": args.quelle_kuratiert}
    # Ziehwahrscheinlichkeit ~ Herkunft / sqrt(Haeufigkeit), ueber weiche Ziele gemittelt
    gewichte = [quell[h] * float(np.sum(z / np.sqrt(np.maximum(zaehl, 1)))) for _, z, h in bilder]
    sampler = WeightedRandomSampler(gewichte, num_samples=len(bilder), replacement=True)
    lader = DataLoader(Trainingsdaten(bilder), batch_size=args.batch, sampler=sampler,
                       num_workers=args.arbeiter, drop_last=True, persistent_workers=True)

    modell = netz().to(geraet)
    verlauf = []
    start = time.time()

    def eingefroren():
        # Die ersten Bloecke bleiben, wie ImageNet sie gelernt hat -- auch
        # ihre BatchNorm-Statistik (eval), sonst wandert sie doch.
        for i in range(min(args.einfrieren, len(modell.features))):
            modell.features[i].eval()

    def epoche_laufen(opt, sched):
        modell.train()
        eingefroren()
        summe = 0.0
        n = 0
        for x, z in lader:
            x, z = x.to(geraet, non_blocking=True), z.to(geraet, non_blocking=True)
            if args.mixup > 0 and random.random() < 0.5:
                lam = float(np.random.beta(args.mixup, args.mixup))
                perm = torch.randperm(x.size(0), device=geraet)
                x = lam * x + (1 - lam) * x[perm]
                z = lam * z + (1 - lam) * z[perm]
            v = F.cross_entropy(modell(x), z)
            if not torch.isfinite(v):
                raise RuntimeError("Verlust nicht endlich -- auf --cpu ausweichen")
            opt.zero_grad(set_to_none=True)
            v.backward()
            opt.step()
            summe += v.item() * len(x)
            n += len(x)
        if sched:
            sched.step()
        return summe / max(n, 1)

    def messung(e, v):
        zeile = {"epoche": e, "verlust": v}
        if pruef is not None and len(kennung_pruef):
            erg = bewertung(logits_von(modell, pruef, geraet), kennung_pruef)
            zeile.update({"top1": erg["top1"], "top3": erg["top3"]})
        if pruef_r is not None and len(kennung_r):
            erg_r = bewertung(logits_von(modell, pruef_r, geraet), kennung_r)
            zeile["rueckhalt_top1"] = erg_r["top1"]
        text = "Epoche %2d/%d  Verlust %.3f" % (e, args.epochen, v)
        if "top1" in zeile:
            text += "  Top-1 %.1f %%  Top-3 %.1f %%" % (100 * zeile["top1"], 100 * zeile["top3"])
        if "rueckhalt_top1" in zeile:
            text += "  Rueckhalt %.1f %%" % (100 * zeile["rueckhalt_top1"])
        print(text + "  %.0f s" % (time.time() - start), flush=True)
        verlauf.append(zeile)

    # Phase 1: nur der Kopf, das Rueckgrat bleibt eingefroren.
    for p in modell.features.parameters():
        p.requires_grad_(False)
    opt = torch.optim.AdamW(modell.classifier.parameters(), lr=1e-3, weight_decay=args.wd)
    for e in range(args.kopf_epochen):
        v = epoche_laufen(opt, None)
        print("Kopf %d/%d  Verlust %.3f  %.0f s" % (e + 1, args.kopf_epochen, v, time.time() - start), flush=True)

    # Phase 2: spaete Bloecke und Kopf, zwei Lernraten, Cosine.
    for i, block in enumerate(modell.features):
        for p in block.parameters():
            p.requires_grad_(i >= args.einfrieren)
    opt = torch.optim.AdamW([
        {"params": [p for p in modell.features.parameters() if p.requires_grad], "lr": args.lr_rueckgrat},
        {"params": list(modell.classifier.parameters()), "lr": args.lr},
    ], weight_decay=args.wd)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=args.epochen)
    for e in range(1, args.epochen + 1):
        v = epoche_laufen(opt, sched)
        messung(e, v)
    return modell, verlauf


def saeuberungsliste(modell, bilder, geraet, pfad):
    kandidaten = [b for b in bilder if b[2] == "kandidat"]
    verdaechtig = []
    for i in range(0, len(kandidaten), 256):
        stueck = kandidaten[i:i + 256]
        x = torch.from_numpy(np.stack([daten.eingabe(p) for p, _, _ in stueck]))
        wahr = torch.softmax(logits_von(modell, x, geraet), dim=1)
        for (p, z, _), w in zip(stueck, wahr):
            j = int(torch.argmax(w))
            if w[j] > 0.9 and z[j] < 0.1:
                beschriftet = ",".join(daten.KLASSEN[k] for k in np.nonzero(z > 0.1)[0])
                verdaechtig.append((p, beschriftet, daten.KLASSEN[j], float(w[j])))
    with open(pfad, "w") as f:
        for p, b, v, w in verdaechtig:
            f.write("%s\t%s\t%s\t%.3f\n" % (os.path.relpath(p, daten.WURZEL), b, v, w))
    print("Verdaechtige Kandidaten (> 0.9 anders als beschriftet): %d" % len(verdaechtig))
    for p, b, v, w in verdaechtig:
        print("   %-50s %-16s -> %-16s %.2f" % (os.path.relpath(p, daten.WURZEL), b, v, w))
    return len(verdaechtig)


def lauf(args):
    geraet = torch.device("cpu" if args.cpu or not torch.cuda.is_available() else "cuda")
    torch.manual_seed(args.saat)
    random.seed(args.saat)
    np.random.seed(args.saat)
    messen = args.modus == "messen"

    ausschluss = []
    if args.ausschluss:
        with open(args.ausschluss) as f:
            ausschluss = [z.strip() for z in f if z.strip()]

    bilder, rueckhalt, gelecht = daten.trainingsmenge(
        leck_vermeiden=messen, ausschluss=ausschluss, ccsn_rueckhalt=messen, saat=args.saat)
    kuratiert = daten.pruefmenge()
    print("Geraet:", geraet)
    print("Grundmenge: %d (davon %d Kandidaten, %d wegen Titel-Leck ausgelassen, %d per Ausschluss); kuratiert: %d" % (
        len(bilder), sum(1 for b in bilder if b[2] == "kandidat"), gelecht, len(ausschluss), len(kuratiert)))
    x_r, k_r = pruefpuffer(rueckhalt)
    start = time.time()

    if not messen:
        bilder = bilder + [(p, daten.ziel(k), "kuratiert") for p, k in kuratiert]
        zaehl = daten.zaehlung(bilder)
        for k, n in zip(daten.KLASSEN, zaehl):
            print("   %-16s %7.1f" % (k, n))
        modell, verlauf = trainieren(args, geraet, bilder, zaehl)
        torch.save(modell.state_dict(), args.ausgabe)
        with open(args.ausgabe + ".json", "w") as f:
            json.dump({"modus": "endmodell", "epochen": args.epochen, "dauer_s": time.time() - start,
                       "bilder": len(bilder), "je_klasse": dict(zip(daten.KLASSEN, zaehl.tolist())),
                       "rezept": vars(args), "verlauf": verlauf}, f, indent=1)
        print("Fertig: %s  (%.0f s)" % (args.ausgabe, time.time() - start))
        return

    # Messen: Kreuzprobe ueber die kuratierten Bilder (--falten 1 = alle
    # kuratierten pruefen, keine im Training).
    alle_logits = []
    alle_kennungen = []
    verlaeufe = []
    letztes = None
    for falte in range(args.falten):
        if args.falten == 1:
            pruef = kuratiert
            dazu = []
        else:
            pruef = [(p, k) for p, k in kuratiert if falte_von(p, args.falten) == falte]
            dazu = [(p, daten.ziel(k), "kuratiert") for p, k in kuratiert if falte_von(p, args.falten) != falte]
        menge = bilder + dazu
        zaehl = daten.zaehlung(menge)
        print("== Falte %d/%d: %d Trainingsbilder (%d kuratiert), %d Pruefbilder, %d CCSN-Rueckhalt" % (
            falte + 1, args.falten, len(menge), len(dazu), len(pruef), len(k_r)), flush=True)
        if falte == 0:
            for k, n in zip(daten.KLASSEN, zaehl):
                print("   %-16s %7.1f" % (k, n))
        x_k, k_k = pruefpuffer(pruef)
        modell, verlauf = trainieren(args, geraet, menge, zaehl, x_k, k_k, x_r, k_r)
        alle_logits.append(logits_von(modell, x_k, geraet))
        alle_kennungen += k_k
        verlaeufe.append(verlauf)
        letztes = (modell, menge)

    erg = bewertung(torch.cat(alle_logits), alle_kennungen)
    erg_r = bewertung(logits_von(letztes[0], x_r, geraet), k_r)
    print("== Ergebnis ueber %d Falte(n), feste %d Epochen" % (args.falten, args.epochen))
    bericht("kuratiert", erg)
    bericht("CCSN-Rueckhalt (letzte Falte)", erg_r)

    # Verlauf ueber die Falten mitteln: sagt, wie viele Epochen das Endmodell
    # bekommen soll.
    mittel = []
    for e in range(args.epochen):
        zeilen = [v[e] for v in verlaeufe if e < len(v)]
        mittel.append({"epoche": e + 1,
                       "verlust": float(np.mean([z["verlust"] for z in zeilen])),
                       "top1": float(np.mean([z.get("top1", 0) for z in zeilen])),
                       "top3": float(np.mean([z.get("top3", 0) for z in zeilen]))})
    beste = max(mittel, key=lambda z: z["top1"])
    print("Verlauf (Mittel ueber Falten):")
    for z in mittel:
        print("   Epoche %2d  Top-1 %.1f %%  Top-3 %.1f %%" % (z["epoche"], 100 * z["top1"], 100 * z["top3"]))
    print("Beste Epoche im Mittel: %d (%.1f %%)" % (beste["epoche"], 100 * beste["top1"]))

    verdaechtig = saeuberungsliste(letztes[0], letztes[1], geraet, args.ausgabe + ".saeubern.txt")
    torch.save(letztes[0].state_dict(), args.ausgabe)
    with open(args.ausgabe + ".json", "w") as f:
        json.dump({"modus": "messen", "falten": args.falten, "beste_epoche": beste["epoche"],
                   "epochen": args.epochen, "dauer_s": time.time() - start,
                   "pruef_kuratiert": len(alle_kennungen), "pruef_rueckhalt": len(k_r),
                   "kuratiert": erg, "rueckhalt": erg_r, "verdaechtig": verdaechtig,
                   "rezept": vars(args), "verlauf": mittel, "verlaeufe": verlaeufe}, f, indent=1)
    print("Fertig: %s  (%.0f s)" % (args.ausgabe, time.time() - start))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("modus", choices=["messen", "endmodell"])
    p.add_argument("--ausgabe", required=True)
    p.add_argument("--epochen", type=int, default=15)
    p.add_argument("--kopf-epochen", type=int, default=3)
    p.add_argument("--falten", type=int, default=5)
    p.add_argument("--lr", type=float, default=5e-4)
    p.add_argument("--lr-rueckgrat", type=float, default=3e-5)
    p.add_argument("--einfrieren", type=int, default=7)
    p.add_argument("--wd", type=float, default=0.02)
    p.add_argument("--mixup", type=float, default=0.2)
    p.add_argument("--quelle-kandidat", type=float, default=2.0)
    p.add_argument("--quelle-kuratiert", type=float, default=3.0)
    p.add_argument("--batch", type=int, default=64)
    p.add_argument("--arbeiter", type=int, default=8)
    p.add_argument("--ausschluss")
    p.add_argument("--cpu", action="store_true")
    p.add_argument("--saat", type=int, default=1)
    lauf(p.parse_args())


if __name__ == "__main__":
    main()
