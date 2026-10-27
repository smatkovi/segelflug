# -*- coding: utf-8 -*-
"""Taugt das Nachlernen am Geraet etwas? -- gemessen, bevor es gebaut wird.

Die Frage: Wenn der Leser ein Foto von Claude deuten laesst und die App sich
das Urteil merkt, wird die Einordnung auf dem Geraet dann besser? Und wie
viele Fotos braucht es dafuer?

Das Netz selbst wird dabei NICHT weitertrainiert -- auf einem N950 gibt es
keine Rueckwaertsrechnung. Gelernt wird nur im Merkmalsraum: Die 1280 Zahlen
vor der letzten Schicht (der `mittel`-Tensor, MODELL.md) sind der
Fingerabdruck eines Bildes. Zu jedem gemerkten Foto wird dieser Abdruck samt
Klasse gespeichert; bei einem neuen Foto zaehlt, wie aehnlich es den
gemerkten ist. Das ist eine Handvoll Skalarprodukte, also auch auf dem
alten Geraet nichts.

Zwei Regeln werden verglichen:
  "klassenmittel" -- je Klasse der Mittelwert der Abdruecke (Prototyp),
      Aehnlichkeit = Kosinus zum Prototyp.
  "knn" -- Aehnlichkeit = Mittel der k besten Treffer je Klasse.
Beides wird mit der Netzausgabe gemischt; das Gewicht waechst mit der Zahl
der gemerkten Fotos: w = n / (n + n0).

Der Lehrer ist nicht unfehlbar. Claudes Trefferquote auf diesen Bildern ist
hier nicht bekannt (kein Schluessel auf diesem Rechner), also wird sie
durchgespielt: 100 %, 90 %, 80 %, 70 % -- falsche Lehrerangaben folgen der
Verwechslungsmatrix des Netzes, nicht dem Zufall, denn genau die
Verwechslungen macht auch ein Lehrer.

  python3 training/nachlernen_versuch.py --modell training/ohne-kuratiert.pt

Das Modell muss eines sein, das die kuratierten Bilder NICHT im Training
hatte (train.py messen --falten 1), sonst misst der Versuch sich selbst."""

import argparse
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daten  # noqa: E402
import train  # noqa: E402


@torch.no_grad()
def abdruecke(modell, bilder, geraet, batch=64):
    """(Abdruecke [n,1280], Logits [n,14]) fuer eine Liste von Pfaden."""
    modell.eval()
    merkmale, logits = [], []
    for i in range(0, len(bilder), batch):
        x = torch.from_numpy(np.stack([daten.eingabe(p) for p in bilder[i:i + batch]]))
        x = x.to(geraet)
        # Dasselbe wie mobilenet_v2.forward, nur mit dem Zwischenstand:
        # features -> globales Mittel -> classifier.
        f = modell.features(x)
        m = torch.nn.functional.adaptive_avg_pool2d(f, 1).flatten(1)
        merkmale.append(m.float().cpu())
        logits.append(modell.classifier(m).float().cpu())
    return torch.cat(merkmale), torch.cat(logits)


def einheit(v):
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-6)


def lehrerurteil(wahr, matrix_zeile, treffer, zufall):
    """Was der Lehrer sagt: mit Wahrscheinlichkeit `treffer` die richtige
    Klasse, sonst eine, die zu dieser Klasse wirklich verwechselt wird."""
    if zufall.random() < treffer:
        return wahr
    gewichte = np.array(matrix_zeile, dtype=np.float64)
    gewichte[daten.INDEX[wahr]] = 0.0
    if gewichte.sum() <= 0:
        return wahr
    return daten.KLASSEN[int(zufall.choice(len(gewichte), p=gewichte / gewichte.sum()))]


def ziel_vektor(wahr, gesagt):
    """Das Ziel fuer das Nachtrainieren: was der Lehrer gesagt hat."""
    z = np.zeros(len(daten.KLASSEN))
    z[daten.INDEX[gesagt]] = 1.0
    return z


def bewerten(logits, kennungen):
    """Top-1 ueber die uebliche Regel (cu-zyklus gilt fuer jede Cumulusstufe)."""
    richtig = 0
    for l, k in zip(logits, kennungen):
        ordnung = np.argsort(-l).tolist()
        richtig += train.richtig(k, ordnung, 1)
    return richtig / max(len(kennungen), 1)


def mischen(p_netz, aehnlich, n_gemerkt, n0, scharf):
    """Netzausgabe und Gedaechtnis mischen -- die ganze Verteilung ersetzen.

    Aus den Kosinus-Werten wird eine Wahrscheinlichkeit, und das Gewicht des
    Gedaechtnisses waechst mit der Zahl der gemerkten Fotos. Nachteil, im
    Versuch gemessen: Klassen, zu denen nichts gemerkt ist, werden dabei
    heruntergedrueckt -- bei wenigen Fotos oder schlechtem Lehrer schadet
    das mehr, als die gemerkten helfen."""
    w = n_gemerkt / float(n_gemerkt + n0)
    roh = np.where(np.isfinite(aehnlich), aehnlich, -1.0)
    e = np.exp(scharf * (roh - roh.max()))
    p_ged = e / max(e.sum(), 1e-9)
    p = (1.0 - w) * p_netz + w * p_ged
    return np.log(np.maximum(p, 1e-12))


def mischen_klassenweise(p_netz, aehnlich, je_klasse, n0, scharf):
    """Nur die Klassen anheben oder senken, zu denen etwas gemerkt ist.

    Je Klasse ein Zuschlag auf das Logit: wie aehnlich ist dieses Foto den
    gemerkten dieser Klasse, verglichen mit dem Mittel ueber alle Klassen,
    zu denen etwas liegt. Das Gewicht waechst je Klasse mit ihrer eigenen
    Zahl -- eine Klasse, von der nichts gemerkt ist, bleibt unberuehrt.
    Damit kann ein einzelnes gemerktes Foto nichts kaputt machen."""
    logits = np.log(np.maximum(p_netz, 1e-12))
    da = [i for i in range(len(aehnlich)) if je_klasse.get(daten.KLASSEN[i], 0) > 0]
    if not da:
        return logits
    mittel = float(np.mean([aehnlich[i] for i in da]))
    aus = logits.copy()
    for i in da:
        n = je_klasse[daten.KLASSEN[i]]
        w = n / float(n + n0)
        aus[i] += scharf * w * (aehnlich[i] - mittel)
    return aus


def letzte_schicht(modell):
    """Die ausgelieferte letzte Schicht (W0, b0) als numpy."""
    w = modell.classifier[1].weight.detach().cpu().numpy().astype(np.float64)
    b = modell.classifier[1].bias.detach().cpu().numpy().astype(np.float64)
    return w, b


def kopf_nachtrainieren(w0, b0, abdruecke, ziele, schritte, lr, zug, skala,
                        glaetten=0.0):
    """Die LETZTE SCHICHT wirklich nachtrainieren -- das Netz wird besser,
    nicht nur korrigiert. Nur 1280x14 = 17 920 Gewichte, also ein paar
    Matrixprodukte; das geht auch auf einem alten Telefon.

    Gerechnet wird mit den auf Laenge 1 normierten Abdruecken, nicht mit den
    rohen: Die rohen sind je nach Bild zehn- bis zwanzigmal so lang, und
    dieselbe Lernrate ist dann einmal zu klein und einmal so gross, dass der
    Lauf auseinanderfliegt (im ersten Versuch gemessen: -40 Punkte). Die
    ausgelieferte Schicht wird dafuer einmal mitskaliert.

    Zwei Vorkehrungen gegen das Auswendiglernen weniger Beispiele:
      * Start bei der ausgelieferten Schicht, nicht bei Null.
      * Ein Zug zurueck zu ihr (`zug`), damit sie sich nur so weit entfernt,
        wie die Beispiele es tragen.
    `glaetten` traegt dem Rechnung, dass der Lehrer irrt: Das Ziel ist nicht
    ganz 1, sondern 1-glaetten, der Rest gleichmaessig verteilt."""
    w0 = w0 * skala
    w = w0.copy()
    b = b0.copy()
    x = np.stack(abdruecke)
    y = np.stack(ziele)
    if glaetten > 0:
        y = (1.0 - glaetten) * y + glaetten / y.shape[1]
    n = len(x)
    for _ in range(schritte):
        logits = x @ w.T + b
        logits -= logits.max(axis=1, keepdims=True)
        p = np.exp(logits)
        p /= p.sum(axis=1, keepdims=True)
        fehler = (p - y) / n
        w -= lr * (fehler.T @ x + zug * (w - w0))
        b -= lr * (fehler.sum(axis=0) + zug * (b - b0))
    return w, b


def aehnlichkeiten(abdruck, gemerkt, regel, k):
    """Kosinus-Aehnlichkeit je Klasse; -1, wo zu einer Klasse nichts liegt."""
    aus = np.full(len(daten.KLASSEN), -1.0)
    for i, kennung in enumerate(daten.KLASSEN):
        v = gemerkt.get(kennung)
        if not v:
            continue
        m = np.stack(v)
        if regel == "klassenmittel":
            aus[i] = float(einheit(m.mean(axis=0)) @ abdruck)
        else:
            treffer = np.sort(m @ abdruck)[::-1][:k]
            aus[i] = float(treffer.mean())
    return aus


def lauf(args):
    geraet = torch.device("cpu" if args.cpu or not torch.cuda.is_available() else "cuda")
    modell = train.netz().to(geraet)
    modell.load_state_dict(torch.load(args.modell, map_location=geraet))

    kuratiert = daten.pruefmenge()
    pfade = [p for p, _ in kuratiert]
    kennungen = [k for _, k in kuratiert]
    print("Modell: %s;  %d kuratierte Bilder" % (os.path.basename(args.modell), len(pfade)))

    M, L = abdruecke(modell, pfade, geraet)
    M_roh = M.numpy()
    M = einheit(M_roh)
    L = L.numpy()
    P = np.exp(L - L.max(axis=1, keepdims=True))
    P /= P.sum(axis=1, keepdims=True)

    grund = bewerten(L, kennungen)
    print("Ohne Gedaechtnis: Top-1 %.1f %%" % (100 * grund))

    # Verwechslungsmatrix des Netzes -- sie liefert die Fehler des Lehrers.
    matrix = {k: [0] * len(daten.KLASSEN) for k in set(kennungen)}
    for l, k in zip(L, kennungen):
        matrix[k][int(np.argmax(l))] += 1
    for k in matrix:
        if sum(matrix[k]) == 0:
            matrix[k][daten.INDEX.get(k, 0)] = 1

    # Nur Klassen, die das Netz kennt, koennen gemerkt werden; cu-zyklus
    # (Cumulus allgemein) taugt nicht als Lehrerangabe und bleibt Pruefstoff.
    lehrbar = [i for i, k in enumerate(kennungen) if k in daten.INDEX]
    ergebnisse = []
    w0, b0 = letzte_schicht(modell)
    # Wie lang ein Abdruck im Mittel wirklich ist (vor dem Normieren).
    skala = float(np.mean(np.linalg.norm(M_roh, axis=1)))
    for regel in args.regeln:
        for treffer in args.lehrer:
            for je_klasse in args.anzahl:
                werte = []
                behalten = []
                for saat in range(args.wiederholungen):
                    zufall = np.random.default_rng(1000 * saat + int(100 * treffer) + je_klasse)
                    # Wer wird gelehrt: je Klasse bis zu `je_klasse` Bilder,
                    # zufaellig gezogen; der Rest ist Pruefmenge.
                    gelehrt = []
                    for kennung in sorted(set(kennungen)):
                        kandidaten = [i for i in lehrbar if kennungen[i] == kennung]
                        zufall.shuffle(kandidaten)
                        gelehrt += kandidaten[:je_klasse]
                    gelehrt = set(gelehrt)
                    gemerkt = {}
                    gesagt_je = {}
                    verworfen = 0
                    for i in gelehrt:
                        gesagt = lehrerurteil(kennungen[i], matrix[kennungen[i]], treffer, zufall)
                        if args.nutzer is not None:
                            # Zweistimmigkeit: gemerkt wird nur, was Claude
                            # und der eigene Tipp gleich sehen.
                            getippt = lehrerurteil(kennungen[i], matrix[kennungen[i]],
                                                   args.nutzer, zufall)
                            if getippt != gesagt:
                                verworfen += 1
                                continue
                        gemerkt.setdefault(gesagt, []).append(M[i])
                        gesagt_je[i] = gesagt
                    pruef = [i for i in range(len(pfade)) if i not in gelehrt]
                    behalten.append(sum(len(v) for v in gemerkt.values()))
                    zahl = dict((k, len(v)) for k, v in gemerkt.items())
                    n_ged = sum(zahl.values())
                    if regel == "kopf":
                        # Die letzte Schicht nachtrainieren. 
                        pass
                    if regel in ("kopf", "beides"):
                        proben = [(M[i], ziel_vektor(kennungen[i], gesagt_je[i]))
                                  for i in sorted(gelehrt) if i in gesagt_je]
                        if len(proben) < 2:
                            neu = L[pruef]
                        else:
                            w, b = kopf_nachtrainieren(
                                w0, b0, [a for a, _ in proben], [z for _, z in proben],
                                args.schritte, args.lr, args.zug, skala, args.glaetten)
                            neu = M[pruef] @ w.T + b
                            if regel == "beides":
                                # Erst die nachtrainierte Schicht, dann
                                #   darueber noch das Gedaechtnis. 
                                pn = np.exp(neu - neu.max(axis=1, keepdims=True))
                                pn /= pn.sum(axis=1, keepdims=True)
                                neu = np.stack([
                                    mischen(pn[j],
                                            aehnlichkeiten(M[i], gemerkt, "klassenmittel", args.k),
                                            n_ged, args.n0, args.scharf)
                                    for j, i in enumerate(pruef)])
                    elif regel == "klassenweise":
                        neu = np.stack([mischen_klassenweise(
                            P[i], aehnlichkeiten(M[i], gemerkt, "klassenmittel", args.k),
                            zahl, args.n0k, args.scharfk) for i in pruef])
                    else:
                        neu = np.stack([mischen(P[i], aehnlichkeiten(M[i], gemerkt, regel, args.k),
                                                n_ged, args.n0, args.scharf) for i in pruef])
                    vorher = bewerten(L[pruef], [kennungen[i] for i in pruef])
                    nachher = bewerten(neu, [kennungen[i] for i in pruef])
                    werte.append((vorher, nachher))
                v = 100 * np.mean([a for a, _ in werte])
                n = 100 * np.mean([b for _, b in werte])
                print("%-14s Lehrer %3.0f %%  %2d je Klasse (%3d gezeigt, %3.0f gemerkt)  "
                      "Top-1 %.1f %% -> %.1f %%  (%+.1f)"
                      % (regel, 100 * treffer, je_klasse,
                         je_klasse * len(set(kennungen)), np.mean(behalten), v, n, n - v))
                ergebnisse.append({"regel": regel, "lehrer": treffer, "je_klasse": je_klasse,
                                   "vorher": v, "nachher": n})
    if args.ausgabe:
        with open(args.ausgabe, "w") as f:
            json.dump({"modell": args.modell, "grund": grund, "n0": args.n0,
                       "scharf": args.scharf, "k": args.k,
                       "ergebnisse": ergebnisse}, f, indent=1)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--modell", required=True)
    p.add_argument("--anzahl", type=int, nargs="+", default=[1, 2, 3, 5, 8])
    p.add_argument("--lehrer", type=float, nargs="+", default=[1.0, 0.9, 0.8, 0.7])
    p.add_argument("--wiederholungen", type=int, default=20)
    p.add_argument("--n0", type=float, default=30.0)
    p.add_argument("--lr", type=float, default=0.5)
    p.add_argument("--scharf", type=float, default=8.0)
    p.add_argument("--k", type=int, default=3)
    p.add_argument("--n0k", type=float, default=3.0)
    p.add_argument("--scharfk", type=float, default=6.0)
    # Trefferquote des Lesers; gesetzt heisst: nur merken, was er und der
    # Lehrer gleich sehen.
    p.add_argument("--nutzer", type=float)
    p.add_argument("--regeln", nargs="+",
                   default=["klassenmittel", "knn", "klassenweise", "kopf"])
    # Fuer die Regel "kopf": Schritte, Lernrate, Zug zur ausgelieferten Schicht.
    p.add_argument("--schritte", type=int, default=200)
    p.add_argument("--zug", type=float, default=0.02)
    p.add_argument("--glaetten", type=float, default=0.0)
    p.add_argument("--ausgabe")
    p.add_argument("--cpu", action="store_true")
    lauf(p.parse_args())


if __name__ == "__main__":
    main()
