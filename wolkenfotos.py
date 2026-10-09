# -*- coding: utf-8 -*-
"""Echte Wolkenfotos zu den Zeichnungen.

Die Zeichnung zeigt das Merkmal und sonst nichts -- deshalb steht sie
weiter oben auf der Seite und bleibt das Hauptbild (tools/clouds.py sagt,
warum). Was sie nicht leisten kann, ist das, worum es am Himmel geht:
dasselbe Merkmal in einem Bild wiederzufinden, in dem noch zwanzig andere
Dinge stehen -- Dunst, Gegenlicht, drei Wolkenstockwerke uebereinander,
ein Baum im Weg. Dafuer stehen unter der Zeichnung zwei bis drei Fotos.

Jedes Foto traegt **einen Satz, der sagt, wohin zu schauen ist**. Ohne den
waere es nur ein huebscher Himmel; mit ihm ist es eine Uebung.

Die Dateien kommen von Wikimedia Commons und sind frei lizenziert
(CC0, gemeinfrei, CC BY, CC BY-SA). `tools/fotos.py` holt sie, verkleinert
sie und schreibt Urheber und Lizenz zu jedem Bild in bilder/fotos.json;
die App zeigt beides unter dem Foto, und CREDITS listet alles noch einmal.

Der Schluessel ist der Name der Zeichnung. Eine Lektion bekommt damit
genau die Fotos, die zu ihrem Bild gehoeren -- und ueber ZUSATZ auch die
zu einer Wolke, die sie bespricht, ohne sie als Bild zu fuehren.
"""
from __future__ import unicode_literals


def t(de, en):
    return {"de": de, "en": en}


def foto(commons, hinweis):
    return {"commons": commons, "hinweis": hinweis}


WOLKENFOTOS = {

    # -- Cumulus humilis: die flache Basis ----------------------------------
    "cu-humilis": [
        foto("File:Cumulus humilis clouds.jpg",
             t("Alle Basen liegen auf derselben Höhe. Das ist kein Zufall "
               "und kein Zeichenfehler: Dort kondensiert die Luft, und tiefer "
               "fängt keine Wolke an.",
               "Every base sits at the same height. That is neither chance "
               "nor a flaw in the drawing: that is where the air condenses, "
               "and no cloud starts any lower.")),
        foto("File:Cumulus humilis.jpg",
             t("Breiter als hoch, mit viel Blau dazwischen — kleine Blasen, "
               "schwaches Steigen. Zum Vergleich: der Congestus in der "
               "Lektion „Wenn es zu gut läuft“ ist höher als breit.",
               "Wider than tall, with plenty of blue in between — small "
               "bubbles, weak lift. For contrast: the congestus in \"When it "
               "goes too well\" is taller than it is wide.")),
        foto("File:Cumulus cloud above Lechtaler Alps at tannheim, Austria.jpg",
             t("Eine einzelne Wolke von der Seite: oben Blumenkohl, unten wie "
               "mit dem Lineal gezogen. Genau diese Kante trägt die Rechnung "
               "zur Basishöhe.",
               "A single cloud from the side: cauliflower on top, ruler-"
               "straight underneath. That edge is what the cloud-base "
               "calculation is about.")),
    ],

    # -- Der Lebenslauf: wachsend gegen zerfallend --------------------------
    "cu-zyklus": [
        foto("File:Lockinge Kiln Farm - geograph.org.uk - 937836.jpg",
             t("Wachsend: harte, scharf gezeichnete Ränder und ein praller "
               "Blumenkohl. Unter so einer Wolke steht der Bart noch.",
               "Growing: hard, sharply drawn edges and a firm cauliflower "
               "top. There is still lift under a cloud like this.")),
        foto("File:Cumulus fractus in Altus, Oklahoma III.jpg",
             t("Zerfallend: die Ränder fasern aus, die flache Basis ist weg. "
               "*fractus* heißt zerbrochen — der Aufwind, der sie gebaut hat, "
               "ist schon aus.",
               "Decaying: the edges go fibrous, the flat base is gone. "
               "*fractus* means broken — the updraught that built it has "
               "already stopped.")),
        foto("File:Cumulus fractus in Altus, Oklahoma.jpg",
             t("Dasselbe ein paar Minuten später: nur noch Fetzen. Wer das "
               "für eine Wolke hält und hinfliegt, findet das Loch.",
               "The same a few minutes later: shreds. Mistake this for a "
               "cloud, fly to it, and what you find is the hole.")),
    ],

    # -- Cumulus congestus: Ueberentwicklung --------------------------------
    "cu-congestus": [
        foto("File:2016 Chmura Cumulus congestus 02.jpg",
             t("Höher als breit, der Blumenkohl quillt nach oben. Die Ränder "
               "sind noch scharf — also noch Wasser, noch kein Eis, noch kein "
               "Cumulonimbus.",
               "Taller than wide, the cauliflower boiling upwards. The edges "
               "are still sharp — still water, no ice yet, not a "
               "cumulonimbus yet.")),
        foto("File:Cumulus congestus cloud.jpg",
             t("Ein Turm steht deutlich über seinen Nachbarn. Dort geht die "
               "Entwicklung weiter, während die anderen stehenbleiben.",
               "One turret clearly outgrows its neighbours. That is where "
               "development continues while the rest stall.")),
        foto("File:Cumulus congestus bei Limburg.jpg",
             t("Von unten: die Basis ist dunkel geworden. Das ist kein "
               "Schatten, sondern Dicke — die Wolke lässt kaum noch Licht "
               "durch, und am Boden hört die Thermik gleich auf.",
               "From below: the base has gone dark. That is not shadow but "
               "depth — hardly any light gets through, and the thermals "
               "beneath are about to stop.")),
    ],

    # -- Cumulonimbus -------------------------------------------------------
    "cumulonimbus": [
        foto("File:Cumulonimbus incus over Warsaw, Poland.jpg",
             t("Der Amboss (*incus*): oben läuft die Wolke flach aus und wird "
               "faserig statt knubbelig. Faserig heißt vereist — der Deckel "
               "ist drauf.",
               "The anvil (*incus*): the top spreads out flat and turns "
               "fibrous instead of lumpy. Fibrous means frozen — the lid is "
               "on.")),
        foto("File:20200607 Chmura cumulonimbus incus nad Krakowem 1407 0252.jpg",
             t("Von weit weg ist die ganze Gestalt zu sehen: Fuß, Turm, "
               "Amboss. Aus der Nähe sieht man nur noch eine graue Wand — "
               "deshalb wird sie von unten so oft zu spät erkannt.",
               "From far away the whole shape is visible: foot, tower, anvil. "
               "Close up there is only a grey wall — which is why it is so "
               "often recognised too late from underneath.")),
        foto("File:Cumulonimbus cloud over the Sundarbans, West Bengal, India 01.jpg",
             t("Unter der Basis hängt der Schauer als graue Schliere bis zum "
               "Boden. Dort ist Abwind, keine Thermik, und die Böenfront "
               "läuft voraus.",
               "The shower hangs under the base as a grey streak down to the "
               "ground. That is downdraught, not lift — and the gust front "
               "runs out ahead of it.")),
    ],

    # -- Stratocumulus: der Tag macht zu ------------------------------------
    "stratocumulus": [
        foto("File:2018 Front chłodny w Kotlinie Kłodzkiej 2.jpg",
             t("Die Quellwolken sind oben zusammengelaufen und zu einer Decke "
               "geworden. Am Rand sind die einzelnen Ballen noch zu erkennen "
               "— dort reißt es wieder auf.",
               "The heaps have run together into a sheet. At its edge the "
               "individual lumps are still visible — that is where it breaks "
               "up again.")),
        foto("File:Stratocumulus lacunosus.jpg",
             t("Geschlossene graue Decke mit Löchern. Durch die Löcher kommt "
               "noch etwas Sonne an den Boden, sonst nirgends — die Thermik "
               "lebt nur noch dort.",
               "A closed grey sheet with holes in it. Sun reaches the ground "
               "through the holes and nowhere else — the thermals live only "
               "there.")),
        foto("File:Stratocumulus stratiformis asperitas am Rand eines Regengebiets V.jpg",
             t("Flache, zerflossene Ballen ohne Quellung nach oben: aus "
               "Haufen ist Schicht geworden. Für heute war es das.",
               "Flat, smeared lumps with no upward growth: heap has become "
               "layer. That is the day finished.")),
    ],

    # -- Wolkenstrassen -----------------------------------------------------
    "wolkenstrasse": [
        foto("File:Cloud Street, Austral 025.jpg",
             t("Die Wolken stehen in einer Reihe bis zum Horizont, längs des "
               "Windes. Darunter lässt sich geradeaus fliegen, ohne zu "
               "kreisen.",
               "The clouds line up to the horizon, along the wind. Under that "
               "line you can fly straight ahead without circling.")),
        foto("File:HorizontalConvectiveRollsClouds1.jpg",
             t("Mehrere Reihen nebeneinander, dazwischen blaue Gassen. In den "
               "Gassen liegt der Abwind — querab der Straße wird es teuer.",
               "Several rows side by side with blue lanes between them. The "
               "lanes are the downdraught — crossing a street costs height.")),
        foto("File:Cloud streets 2.jpg",
             t("Von oben, aus dem Satelliten: dasselbe Muster, das vom Boden "
               "aus nur als Reihe zu ahnen ist. So weit reicht eine Straße "
               "wirklich.",
               "From above, by satellite: the same pattern that is only "
               "guessable as a line from the ground. That is how far a street "
               "really runs.")),
    ],

    # -- Altocumulus castellanus: die Warnung aus der Hoehe ------------------
    "ac-castellanus": [
        foto("File:Altocumulus castellanus undulatus, Altocumulus floccus and Cirrocumulus floccus.jpg",
             t("Aus den Ballen wachsen kleine Türmchen nach oben — *castellum* "
               "ist die Burg. Türmchen in der Höhe heißen: dort oben ist die "
               "Luft labil.",
               "Little turrets grow upward out of the lumps — *castellum* is "
               "a castle. Turrets up there mean the air up there is "
               "unstable.")),
        foto("File:Altocumulus-Castellanus.jpg",
             t("Hier sind die Türmchen am deutlichsten: Aus einer flachen "
               "Reihe wächst jeder Ballen einzeln nach oben. Darunter "
               "stehen gewöhnliche Cumuli — zwei Stockwerke, zwei "
               "Geschichten.",
               "Here the turrets are clearest: out of a flat row each lump "
               "grows upward on its own. Ordinary cumulus sit below — two "
               "levels, two different stories.")),
        foto("File:Cirrocumulus, Altocumulus castellanus, and Altocumulus lenticularis.jpg",
             t("Drei Sorten auf einmal: feinkörniger Cirrocumulus, Zinnen und "
               "eine Linse. So viel Bewegung in der Höhe gehört zu keinem "
               "ruhigen Tag.",
               "Three kinds at once: fine-grained cirrocumulus, battlements "
               "and a lens. That much going on aloft belongs to no quiet "
               "day.")),
    ],

    # -- Cirrus: die Front kuendigt sich an ---------------------------------
    "cirrus": [
        foto("File:Cirrus front over Austnesfjorden, Austvågøya, Lofoten, Norway, 2015 April.jpg",
             t("*cirrus* ist die Haarlocke. Die Haken hängen nach unten: "
               "Eiskristalle fallen aus der Wolke und werden vom langsameren "
               "Wind darunter nachgezogen.",
               "*cirrus* is a lock of hair. The hooks hang downward: ice "
               "crystals fall out of the cloud and are dragged back by the "
               "slower wind beneath.")),
        foto("File:Cirrus uncinus clouds in the morning sky.jpg",
             t("Einzelne Haken am Morgen. Entscheidend ist, was daraus wird: "
               "Werden sie im Lauf des Tages mehr und dichter, kommt eine "
               "Warmfront.",
               "Scattered hooks in the morning. What matters is what becomes "
               "of them: if they thicken through the day, a warm front is on "
               "its way.")),
        foto("File:22°-Halo in Cirrostratus fibratus bei Limburg II.jpg",
             t("Der Ring um die Sonne entsteht an Eiskristallen. Er heißt: "
               "Aus dem Cirrus ist eine geschlossene Schicht geworden — die "
               "Front ist nah, die Thermik geht aus.",
               "The ring around the sun forms on ice crystals. It says the "
               "cirrus has closed into a sheet — the front is near and the "
               "thermals are going.")),
    ],

    # -- Lenticularis: Welle --------------------------------------------------
    "lenticularis": [
        foto("File:PXL 20211221 223638171.jpg",
             t("Glatt wie geschliffen und ortsfest: die Wolke bleibt über dem "
               "Berg stehen, während die Luft durch sie hindurchzieht. Nur "
               "deshalb ist die Form so sauber.",
               "Smooth as if polished, and standing still: the cloud stays "
               "over the mountain while the air moves through it. That is the "
               "only reason the shape is so clean.")),
        foto("File:Âne du Mont-Blanc vu du col du Petit-Saint-Bernard (août 2019).JPG",
             t("Dieselbe Welle als Kappe direkt über dem Gipfel. Wo die Kappe "
               "sitzt, steigt die Luft — und im Lee dahinter liegt der Rotor.",
               "The same wave as a cap right over the summit. Where the cap "
               "sits the air rises — and the rotor lies in the lee behind "
               "it.")),
        foto("File:Lenticularis MWP.jpg",
             t("Aus dem Segelflugzeug: so sieht die Linse aus, wenn man im "
               "Steigen davor steht. Angeflogen wird die Vorderkante, nicht "
               "die Wolke selbst.",
               "From a glider: this is the lens seen from the lift in front "
               "of it. You fly to the leading edge, not into the cloud.")),
    ],
}


# Zwei Wolken werden besprochen, ohne das Bild der Lektion zu sein:
# der Cumulonimbus in der Ueberentwicklung, die Linse bei den Wellen.
# Ihre Fotos haengen deshalb an der Lektion, nicht am Bildnamen.
ZUSATZ = {
    "w-ueberentwicklung": ["cumulonimbus"],
    "w-strassen": ["lenticularis"],
}
