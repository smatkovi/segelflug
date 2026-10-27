# -*- coding: utf-8 -*-
"""Der Erkennungsmodus: viele Fotos, und zu jedem zwei Fragen.

Die Lektionen zeigen eine Zeichnung und darunter zwei, drei Fotos derselben
Wolke (wolkenfotos.py). Das erklaert. Es uebt aber nicht -- wer unter der
Ueberschrift "Cumulus humilis" drei Bilder von Cumulus humilis sieht, hat
nichts zu entscheiden.

Hier ist es umgekehrt: ein Foto, sonst nichts auf der Seite, und zwei
Fragen dazu.

1. **Was ist das fuer eine Wolke?** Die Auswahl sind andere Wolken -- und
   zwar nicht irgendwelche, sondern die, mit denen diese wirklich
   verwechselt wird (`verwechselt`). Zwischen Cirrus und Stratus zu
   unterscheiden, uebt niemand; zwischen Cumulus mediocris und congestus
   haengt der Tag davon ab.
2. **Was heisst das fuers Segelfliegen?** Die Auswahl ist immer dieselbe
   kurze Liste von Bedeutungen (BEDEUTUNGEN). Das haelt die Autorenarbeit
   bei den Klassen statt bei den Fotos: zweihundert Fotos brauchen keine
   zweihundert Antworttexte, sondern vierzehn.

Die Fotos kommen von Wikimedia Commons, frei lizenziert und mit Urheber;
tools/sammeln.py sucht Kandidaten in den Kategorien, ausgewaehlt wird mit
den Augen (ein Bild, bei dem man selbst zoegert, taugt nicht zur Uebung),
und tools/fotos.py holt die ausgewaehlten ins Paket.
"""
from __future__ import unicode_literals

from wolkenfotos import t


# -- Was eine Wolke fuers Fliegen heisst -------------------------------------
#
# Eine feste, kurze Liste. Sie ist die Antwortauswahl der zweiten Frage und
# steht deshalb in der Reihenfolge, in der ein Tag ablaeuft: von "noch
# nichts" ueber "jetzt" bis "vorbei".
BEDEUTUNGEN = [
    ("thermik-schwach", t("Schwache Thermik, niedrige Basis",
                          "Weak lift, low cloud base")),
    ("thermik-gut", t("Gute Thermik — der Tag trägt",
                      "Good lift — the day works")),
    ("strasse", t("Aufwind in Reihen — Strecke geradeaus",
                  "Lift in rows — straight-line cross-country")),
    ("welle", t("Welle: ortsfestes Steigen, viel Wind",
                "Wave: steady lift fixed in place, strong wind")),
    ("ueberentwicklung", t("Überentwicklung — es schießt durch",
                           "Overdevelopment — it is shooting through")),
    ("gewitter", t("Gewitter: Böen und Hagel, Abstand halten",
                   "Thunderstorm: gusts and hail, keep away")),
    ("abschirmung", t("Schirmt ab — die Thermik stirbt",
                      "Shades the ground — the lift dies")),
    ("front", t("Warmfront zieht auf — Wetterwechsel",
                "Warm front moving in — weather is changing")),
    ("kein-flug", t("Tief und nass — nichts zu holen",
                    "Low and wet — nothing to be had")),
]


# Wie die Uebung heisst. Sie steht im Kurs und nicht in der Oberflaeche:
# Dieselbe App traegt vier Kurse, und "Wolken erkennen" waere in einem
# C-Kurs eine seltsame Taste.
TITEL = t("Wolken erkennen", "Recognise clouds")
UNTERZEILE = t("Ein Foto nach dem anderen. Zu jedem zwei Fragen: Was für "
               "eine Wolke ist das — und was heißt sie fürs Fliegen?",
               "One photo after another. Two questions about each: what "
               "cloud is that — and what does it mean for flying?")


def klasse(id, name, bedeutung, erkennen, bedeutet, verwechselt, fotos):
    """Eine Wolkenart, wie der Uebungsmodus sie kennt.

    `erkennen` ist der Satz, der nach der ersten Frage erscheint: woran man
    es haette sehen koennen. `bedeutet` begruendet die zweite Antwort.
    """
    return {"id": id, "name": name, "bedeutung": bedeutung,
            "erkennen": erkennen, "bedeutet": bedeutet,
            "verwechselt": verwechselt, "fotos": fotos}


KLASSEN = [

    klasse(
        "cu-humilis",
        t("Cumulus humilis (Schönwetterwolke)", "Cumulus humilis (fair-weather cumulus)"),
        "thermik-schwach",
        t("Flach, breiter als hoch — und alle Basen liegen auf derselben "
          "Höhe. Dazwischen steht viel Blau.",
          "Flat, wider than tall — and every base sits at the same height, "
          "with plenty of blue in between."),
        t("Die Blasen reichen nur knapp über die Kondensationshöhe: Thermik "
          "ja, aber schwach, und die Basis bleibt niedrig.",
          "The bubbles barely reach above the condensation level: there is "
          "lift, but weak, and the base stays low."),
        ["cu-mediocris", "stratocumulus", "wolkenstrasse"],
        [
            "File:Cumulus humilis clouds.jpg",
            "File:Cumulus humilis.jpg",
            "File:Cumulus cloud above Lechtaler Alps at tannheim, Austria.jpg",
            "File:- panoramio (2117).jpg",
            "File:. - panoramio (238).jpg",
            "File:18769784 112894445907318 6589379670662184960 n (34627606460).jpg",
            "File:2013-05-19 15-03-51-nuages.jpg",
            "File:2013-05-25 13-20-11-nuages.jpg",
            "File:2014-02-17 12-45-02 paysage-champey.jpg",
            "File:20190406 141726 le barrage de damouni tiaret.jpg",
            "File:5 stainless steel grain bins.jpg",
            "File:500px photo (152124903).jpeg",
            "File:500px photo (47206606).jpeg",
            "File:A high country landscape.jpg",
            "File:AcrosstheHills.jpg",
        ]),

    klasse(
        "cu-mediocris",
        t("Cumulus mediocris", "Cumulus mediocris"),
        "thermik-gut",
        t("Etwa so hoch wie breit: oben schon Blumenkohl, unten noch die "
          "scharfe flache Basis.",
          "About as tall as it is wide: cauliflower on top, still a sharp "
          "flat base underneath."),
        t("Die Wolke wächst, ohne durchzuschießen — der Normalfall eines "
          "brauchbaren Streckentags.",
          "The cloud is growing without shooting through — an ordinary "
          "workable cross-country day."),
        ["cu-humilis", "cu-congestus", "stratocumulus"],
        [
            "File:2013-06-05 17-25-10-nuages.jpg",
            "File:2013-06-07 15-54-46-cumulus.jpg",
            "File:500px photo (79660815).jpeg",
            "File:Above the Valais of Mabayi there are clouds.jpg",
            "File:Bar Harbor distant view.jpg",
            "File:Beau nuage le 18 mai 2008 près de Châteauneuf-du-Pape.JPG",
            "File:Belleza puntana.JPG",
            "File:Bilbao - Parque Doña Casilda - Farola 01.jpg",
            "File:Carretera en el Altiplano - Bolivia.jpg",
            "File:Chapel of Our Lady of Sorrows on Svatý kopeček in Mikulov 2020.jpg",
            "File:Chicago skyline 2013.JPG",
        ]),

    klasse(
        "cu-congestus",
        t("Cumulus congestus (Blumenkohl)", "Cumulus congestus (towering cumulus)"),
        "ueberentwicklung",
        t("Deutlich höher als breit, die Türme noch scharf umrissen — der "
          "Kopf ist weiß und hart, nicht faserig.",
          "Clearly taller than wide, the towers still sharply outlined — the "
          "top is white and hard, not fibrous."),
        t("So viel Steigen, dass es gleich zu viel wird: Unter dem Congestus "
          "regnet es bald, und der nächste Schritt ist der Cumulonimbus.",
          "So much lift that it is about to become too much: rain starts "
          "under a congestus soon, and the next step is a cumulonimbus."),
        ["cu-mediocris", "cumulonimbus", "stratocumulus"],
        [
            "File:2016 Chmura Cumulus congestus 02.jpg",
            "File:Cumulus congestus cloud.jpg",
            "File:Cumulus congestus bei Limburg.jpg",
            "File:2013-05-25 19-49-39-nuages.jpg",
            "File:2016 Chmura Cumulus congestus 01.jpg",
            "File:2019-05-25 09-51-19 cumulus.jpg",
            "File:2022-08-05 18 40 16 View of towering cumulus from Mercer County Route 526 (Robbinsville-Edinburg Road) in Robbinsville Township, Mercer County, New Jersey.jpg",
            "File:2022-08-05 19 37 17 View of towering cumulus near sunset from Mercer County Route 526 (Robbinsville-Edinburg Road) in Robbinsville Township, Mercer County, New Jersey.jpg",
            "File:A Dutch polder.jpg",
            "File:Amazonas peruano 1980 08.jpg",
            "File:Big cu congestus 1.JPG",
            "File:Cayo Blanco (1983) 01.jpg",
            "File:Cloud formations over Mumbai.jpg",
        ]),

    klasse(
        "cumulonimbus",
        t("Cumulonimbus (Gewitterwolke)", "Cumulonimbus (thunderstorm cloud)"),
        "gewitter",
        t("Der Kopf ist nicht mehr scharf, sondern faserig — das ist Eis — "
          "und oben läuft er flach aus wie ein Amboss.",
          "The top is no longer sharp but fibrous — that is ice — and it "
          "spreads out flat like an anvil."),
        t("Böenfront, Hagel, Abwind, und unter der Basis Regen. Auch der "
          "harmlos aussehende Rand gehört noch dazu.",
          "Gust front, hail, sink, and rain under the base. The "
          "harmless-looking edge is part of it too."),
        ["cu-congestus", "stratocumulus", "cirrostratus"],
        [
            "File:Cumulonimbus incus over Warsaw, Poland.jpg",
            "File:20200607 Chmura cumulonimbus incus nad Krakowem 1407 0252.jpg",
            "File:Cumulonimbus cloud over the Sundarbans, West Bengal, India 01.jpg",
            "File:08-30-2020 Cumululonimbus cloud.jpg",
            "File:2016-07-19 14 30 41 Thundestorm with a large cumulonimbus anvil and mammatus hanging from it over the Blue Ridge Mountains of Shenandoah National Park, viewed from U.S. Route 211 (Lee Highway) just east of Collins Avenue in Luray, Virginia.jpg",
            "File:2016-07-19 15 42 26 View of a thunderstorm cumulonimbus east of the Blue Ridge Mountains in Shenandoah National Park from U.S. Route 340 south of Newport in western Page County, Virginia.jpg",
            "File:2023-07-04 17 55 29 View of a distant line of thunderstorms from Ann M. Banchoff Park in the Mountainview section of Ewing Township, Mercer County, New Jersey.jpg",
            "File:Alasiga rünksajupilv (Cumulonimbus incus) .jpg",
            "File:Anvil cloud 1.jpg",
            "File:Anvil cloud, St. Simons, GA, US.jpg",
            "File:Chasing the rain, Masai Mara.jpg",
            "File:Chmura burzowa na północny-wschód od Krakowa, widok spod Wawelu, 20201005 1657 1653.jpg",
            "File:2023-09-08 13 53 22 View of a cumulonimbus anvil from Aquetong Lane in the Mountainview section of Ewing Township, Mercer County, New Jersey.jpg",
            "File:2025-06-19 17 21 52 An approaching severe thunderstorm (about 40 minutes out) viewed from the Ewing Branch of the Mercer County Library System in Ewing Township, Mercer County, New Jersey.jpg",
        ]),

    klasse(
        "wolkenstrasse",
        t("Wolkenstraße", "Cloud street"),
        "strasse",
        t("Die Wolken stehen nicht verstreut, sondern in Reihen, die zum "
          "Horizont zusammenlaufen — immer längs des Windes.",
          "The clouds are not scattered but lined up in rows converging "
          "towards the horizon — always along the wind."),
        t("Unter der Reihe steigt es fast durchgehend: geradeaus fliegen "
          "statt kreisen. Schneller geht Strecke nicht.",
          "Under the row it goes up almost continuously: fly straight "
          "instead of circling. Cross-country gets no faster than this."),
        ["cu-humilis", "altocumulus", "stratocumulus"],
        [
            "File:HorizontalConvectiveRollsClouds1.jpg",
            "File:Cloud-street (11802049514).jpg",
            "File:Roll clouds, grand junction, co 20250710.jpg",
        ]),

    klasse(
        "stratocumulus",
        t("Stratocumulus (Haufenschichtwolke)", "Stratocumulus"),
        "abschirmung",
        t("Eine zusammenhängende tiefe Schicht aus Ballen und Walzen, "
          "zwischen denen kaum noch Blau steht.",
          "A connected low layer of rolls and lumps with hardly any blue "
          "left between them."),
        t("Wo die Sonne nicht mehr auf den Boden kommt, entsteht keine "
          "Thermik mehr — der Tag macht zu.",
          "Where the sun no longer reaches the ground, no new thermals "
          "form — the day is closing down."),
        ["altocumulus", "stratus", "cu-humilis"],
        [
            "File:Stratocumulus lacunosus.jpg",
            "File:Stratocumulus stratiformis asperitas am Rand eines Regengebiets V.jpg",
            "File:2018 Central Chernozem Zapovednik 11 34 26 010000.jpeg",
            "File:Bayern Erlangen Naturschutzgebiet Exerzierplatz Frühling 1.jpg",
            "File:Blue Sky in Montreal, Quebec.jpg",
            "File:BlueSkyWhiteClouds.jpg",
            "File:Brosen clouds lake2.jpg",
            "File:Burnished (8583935661).jpg",
            "File:Chapel of Saint Sebastian in Mikulov - west side 2020 crop.jpg",
        ]),

    klasse(
        "ac-castellanus",
        t("Altocumulus castellanus (Zinnenwolke)", "Altocumulus castellanus"),
        "ueberentwicklung",
        t("Mittelhoch, und auf einer gemeinsamen Grundlinie sitzen kleine "
          "Türmchen wie Zinnen auf einer Mauer.",
          "At middle level, with small turrets sitting on a common base "
          "line like battlements on a wall."),
        t("Schon in der Höhe ist die Luft labil. Am Morgen gesehen heißt "
          "das: am Nachmittag Gewitter.",
          "The air is already unstable aloft. Seen in the morning this "
          "means thunderstorms in the afternoon."),
        ["altocumulus", "cu-humilis", "cirrus"],
        [
            "File:Altocumulus castellanus undulatus, Altocumulus floccus and Cirrocumulus floccus.jpg",
            "File:Altocumulus-Castellanus.jpg",
        ]),

    klasse(
        "ac-lenticularis",
        t("Lenticularis (Linsenwolke)", "Lenticularis (lens cloud)"),
        "welle",
        t("Glatt, linsenförmig, mit scharfem Rand, oft gestapelt — und sie "
          "steht still, während der Wind durch sie hindurchzieht.",
          "Smooth, lens-shaped, sharp-edged, often stacked — and it stands "
          "still while the wind blows through it."),
        t("Im Lee eines Berges steht eine Welle. Vor der Linse trägt es "
          "gleichmäßig und sehr hoch, dahinter sinkt es ebenso.",
          "There is a wave in the lee of a mountain. Ahead of the lens the "
          "lift is smooth and goes very high; behind it the sink is just "
          "as steady."),
        ["altocumulus", "cirrus", "stratocumulus"],
        [
            "File:PXL 20211221 223638171.jpg",
            "File:Âne du Mont-Blanc vu du col du Petit-Saint-Bernard (août 2019).JPG",
            "File:Lenticularis MWP.jpg",
            "File:01 Altocumulus lenticulaire au-dessus de Nyons.jpg",
            "File:A late afternoon hike from the Dewdrop to Red Plateau - colourful clouds at sunset (13657822665).jpg",
            "File:Altocumulus duplicatus over Wellington.jpg",
            "File:Altocumulus lenticolaris.jpg",
            "File:Altocumulus lenticularis - Andøy, Norway 2023-07-12.jpg",
            "File:Altocumulus lenticularis Arctowski Station HD.JPG",
            "File:Flickr - Nicholas T - Saucer.jpg",
            "File:Flickr - Nicholas T - Shape-Shifters.jpg",
            "File:Garaio - Embalse de Ullíbarri-Gamboa - Camino 02.jpg",
            "File:Isolated Altocumulus lenticularis.jpg",
            "File:Lago de Coatepeque, Occidente El Salvador.jpg",
            "File:Lake Argentino northern arm Lago Argentino Brazo Norte Patagonia Argentina Luca Galuzzi 2005.JPG",
            "File:Lenticular clouds and cumulus over flat New Braunfels.jpg",
            "File:Lenticular clouds and Mount Hotaka from Mount Otensho 1994-06-25.jpg",
            "File:Lenticular Clouds around Fitz Roy (3259963875).jpg",
            "File:Lenticular clouds Scotland (5844541910).jpg",
            "File:Lenticular-La Serrota.jpeg",
            "File:Lenticular4.jpeg",
            "File:LenticularCloud-Madeira 20150221©KarlheinzEssl.JPG",
        ]),

    klasse(
        "altocumulus",
        t("Altocumulus (Schäfchenwolken)", "Altocumulus"),
        "abschirmung",
        t("Mittelhoch: viele kleine Ballen, fast gleich groß, in Reihen "
          "geordnet — und jeder davon hat noch einen Schatten.",
          "Middle level: many small lumps of nearly equal size, arranged in "
          "rows — and each one still has a shadow."),
        t("Allein ist es harmlos. Dichter werdend legt es sich als Schirm "
          "über die Thermik, lange bevor etwas davon unten ankommt.",
          "On its own it is harmless. As it thickens it screens off the "
          "thermals, long before anything of it reaches the ground."),
        ["ac-castellanus", "stratocumulus", "cirrus"],
        [
            "File:2025-07-30 08 46 36 Altocumulus clouds viewed from Aquetong Lane in the Mountainview section of Ewing Township, Mercer County, New Jersey.jpg",
            "File:Clouds over Nuthurst, West Sussex, England.jpg",
            "File:2025-07-29 08 15 46 \"Mackerel sky\" Altocumulus clouds viewed from Aquetong Lane in the Mountainview section of Ewing Township, Mercer County, New Jersey.jpg",
            "File:2025-11-09 Igreja de São Sebastião, Cesaredas, Reguengo Grande.jpg",
            "File:2026-05-26 19 02 02 Altocumulus clouds viewed from Mountain View Road in the Mountainview section of Ewing Township, Mercer County, New Jersey.jpg",
            "File:2026-05-26 19 06 43 Altocumulus clouds viewed from Mountain View Road in the Mountainview section of Ewing Township, Mercer County, New Jersey.jpg",
            "File:Altocumulus (11773580033).jpg",
            "File:Altocumulus 1 August 2021 Galley Common.jpg",
            "File:Altocumulus and cumulus over Gåseberg.jpg",
        ]),

    klasse(
        "cirrus",
        t("Cirrus (Federwolke)", "Cirrus"),
        "front",
        t("Ganz oben, dünn und faserig, ohne eigenen Schatten; die Haken "
          "zeigen, woher der Wind in der Höhe kommt.",
          "Highest of all, thin and fibrous, casting no shadow of its own; "
          "the hooks show where the wind up there comes from."),
        t("Der Vorbote einer Warmfront. Heute ist der Tag noch gut, in "
          "zwölf bis vierundzwanzig Stunden ist er vorbei.",
          "The herald of a warm front. Today is still good; in twelve to "
          "twenty-four hours it is over."),
        ["cirrostratus", "altocumulus", "ac-lenticularis"],
        [
            "File:Cirrus front over Austnesfjorden, Austvågøya, Lofoten, Norway, 2015 April.jpg",
            "File:Cirrus uncinus clouds in the morning sky.jpg",
            "File:- panoramio (2677).jpg",
            "File:2019-08-04 12 52 41 Cirrus and cumulus clouds viewed from Franklin Farm Park in the Franklin Farm section of Oak Hill, Fairfax County, Virginia.jpg",
            "File:2019-11-26 14 46 30 Cirrus uncinus clouds viewed from Kinross Circle in the Chantilly Highlands section of Oak Hill, Fairfax County, Virginia.jpg",
            "File:2026-09-10 16 20 38 Cirrus uncinus clouds viewed from Aquetong Lane in the Mountainview section of Ewing Township, Mercer County, New Jersey.jpg",
            "File:2026-09-10 16 45 51 Cirrus uncinus clouds viewed from Aquetong Lane in the Mountainview section of Ewing Township, Mercer County, New Jersey.jpg",
            "File:2026-10-10 12 07 54 Cirrus uncinus clouds viewed from Klockner Road in Hamilton Township, Mercer County, New Jersey.jpg",
            "File:Clouds - Mendocino, California - DSC01699.JPG",
            "File:Clouds - Mendocino, California - DSC01703.JPG",
            "File:Dancing blue clouds and skies.jpg",
            "File:El cielo muy azul y....JPG",
            "File:Mares' tails, St Andrews Park - geograph.org.uk - 6266391.jpg",
            "File:Mattupetty Dam reservoir, Munnar,Kerala, India.jpg",
            "File:Mila Young 2017-05-21 (Unsplash).jpg",
            "File:Nuages 3.jpg",
            "File:Nuages 6.jpg",
            "File:Nuvole 2.jpg",
            "File:Nuvole.jpg",
            "File:02162008 Interstate80NWUtah.JPG",
        ]),

    klasse(
        "cirrostratus",
        t("Cirrostratus (Schleier mit Halo)", "Cirrostratus (veil with halo)"),
        "front",
        t("Ein milchiger Schleier über dem ganzen Himmel. Die Sonne bleibt "
          "sichtbar, bekommt aber einen Ring im Abstand von 22°.",
          "A milky veil over the whole sky. The sun stays visible but "
          "picks up a ring at 22° from it."),
        t("Aus dem Cirrus ist eine Schicht geworden: Die Front ist näher, "
          "die Einstrahlung geht zurück, die Thermik wird flau.",
          "The cirrus has become a layer: the front is closer, the sunshine "
          "is cut back, and the lift goes soft."),
        ["cirrus", "altocumulus", "stratus"],
        [
            "File:22°-Halo in Cirrostratus fibratus bei Limburg II.jpg",
            "File:(139) Cirrostratus.jpg",
            "File:2015 04 09 23 23 20 2 Jpg (112274519).jpeg",
            "File:2020-02-20 09 12 22 Sun dimly visible through cirrostratus along Old Ox Road in the Dulles section of Sterling, Loudoun County, Virginia.jpg",
            "File:2021-07-13 12 20 22 Cirrostratus clouds viewed from Thompson Road in the Franklin Farm section of Oak Hill, Fairfax County, Virginia.jpg",
            "File:2021-07-13 12 52 40 A halo around the sun within cirrus and cirrostratus clouds viewed from Franklin Farm Park in the Franklin Farm section of Oak Hill, Fairfax County, Virginia.jpg",
            "File:2021-07-13 12 52 48 Cirrostratus clouds viewed from Franklin Farm Park in the Franklin Farm section of Oak Hill, Fairfax County, Virginia.jpg",
        ]),

    klasse(
        "stratus",
        t("Stratus (Hochnebel)", "Stratus"),
        "kein-flug",
        t("Eine tiefe, strukturlose graue Decke ohne erkennbare Ballen — "
          "Nebel, der nicht ganz am Boden liegt, oft an Hängen klebend.",
          "A low, featureless grey blanket with no discernible lumps — fog "
          "that is not quite on the ground, often clinging to slopes."),
        t("Keine Sonne, kein Steigen, dazu schlechte Sicht und eine Basis, "
          "unter der nichts mehr geht.",
          "No sun, no lift, poor visibility and a base below which nothing "
          "works any more."),
        ["stratocumulus", "cirrostratus", "cumulonimbus"],
        [
            "File:\"Valley of Tranquility, Where the Clouds Descend and the Pines Stand Tall\" 🌫️🏞️🌲.jpg",
            "File:\"Whispers of the Clouds, A Symphony in the Silent Mountains\" 🌫️🌲⛰️.jpg",
            "File:2015-01-14 11 44 01 View west under some low clouds from Nevada State Route 487 (Baker Road) north of Baker, Nevada.JPG",
            "File:2019-11-30 12 58 13 Stratus clouds over a field along Old Ox Road in the Dulles section of Sterling, Loudoun County, Virginia.jpg",
            "File:2019-10-13 13 58 40 Stratus over a field along Old Ox Road in the Dulles section of Sterling, Loudoun County, Virginia.jpg",
            "File:2024-12-20 09 31 08 Stratus clouds viewed from Interstate 295 in Ewing Township, Mercer County, New Jersey.jpg",
            "File:2024-12-20 09 39 41 Stratus clouds viewed from Suburban Square Shopping Center in Ewing Township, Mercer County, New Jersey.jpg",
            "File:2025-11-21 10 40 58 Stratus clouds viewed from Mountain View Road in the Mountainview section of Ewing Township, Mercer County, New Jersey.jpg",
            "File:Hochnebel Wismat 005.jpg",
        ]),
]
