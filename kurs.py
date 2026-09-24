# -*- coding: utf-8 -*-
"""Segelflug- und PPL-Theorie, deutsch und englisch.

Every string a person reads is a pair, so the language switch changes the
whole course and not just the menus. Written with t("deutsch", "english").

The cloud chapter comes first because that is the part of the theory that
is answered in the sky rather than in the book: a glider pilot reads the
clouds continuously, and everything else -- where to fly, when to start,
when to go home -- follows from that reading.
"""
from __future__ import unicode_literals

from herleitungen import HERLEITUNGEN
from kursformeln import KURSFORMELN


def t(de, en):
    return {"de": de, "en": en}


def mc(q, options, answer, why, bild="", code=""):
    return {"kind": "mc", "q": q, "optionen": options, "antwort": answer,
            "warum": why, "bild": bild, "code": code}


def zahl(q, answer, einheit, why, toleranz=0.1, bild=""):
    """A number to work out -- cloud base, glide, time. Compared with a
    tolerance, because nobody does mental arithmetic to four digits."""
    return {"kind": "zahl", "q": q, "antwort": answer, "einheit": einheit,
            "warum": why, "toleranz": toleranz, "bild": bild}


def formel(zeile, tex, untertitel, erklaerung):
    """Eine Formel zweimal: wie sie im Text steht und wie sie gesetzt aussieht.

    `zeile` ist genau die Zeile, die im Lehrtext oder in der Herleitung
    vorkommt -- eine dritte Schreibweise waere eine Huerde mehr, keine
    weniger. `tex` ist dieselbe Sache in TeX-Schreibweise; gesetzt wird sie
    beim Bauen (tools/formeln.py), das Geraet zeigt nur ein Bild.

    `untertitel` sagt in einer halben Zeile, was dasteht, `erklaerung`
    beantwortet die Frage, die beim Hinsehen entsteht: woher der Faktor
    kommt und wo er aufhoert zu gelten. Beide sind Sprachpaare, die Formel
    selbst nicht -- die ist in jeder Sprache dieselbe.
    """
    return {"code": zeile, "tex": tex, "untertitel": untertitel,
            "erklaerung": erklaerung}


def lektion(ident, titel, begriffe, text, bild, aufgaben, formeln=None):
    # Die Herleitung haengt hinten an, in beiden Sprachen. Sie steht nicht
    # im Lektionstext selbst, damit sie an einer Stelle zu ueberblicken
    # ist und keine Formel ohne Begruendung durchrutscht.
    h = HERLEITUNGEN.get(ident)
    if h:
        text = {"de": text["de"] + "\n\n" + h["de"],
                "en": text["en"] + "\n\n" + h["en"]}
    return {"id": ident, "titel": titel, "begriffe": begriffe, "text": text,
            "bild": bild, "aufgaben": aufgaben,
            "formeln": formeln or KURSFORMELN.get(ident, [])}


def kapitel(ident, titel, stufe, blurb, lektionen):
    return {"id": ident, "titel": titel, "stufe": stufe, "text": blurb,
            "lektionen": lektionen}



# ===========================================================================
# Wolken lesen
# ===========================================================================

K_WOLKEN = kapitel(
    "wolken", t("Wolken lesen", "Reading the sky"), 1,
    t("Die Wolke ist das Messgerät, das immer mitfliegt. Sie zeigt, wo "
      "gestiegen wird, wie hoch es geht, wie lange der Tag noch trägt und "
      "wann es gefährlich wird.",
      "A cloud is the one instrument that is always there. It shows where "
      "the lift is, how high it goes, how much longer the day will carry, "
      "and when it is turning dangerous."), [

    # -- 0 -------------------------------------------------------------
    lektion("w-namen",
        t("Woher die Wolken ihre Namen haben",
          "Where clouds get their names"),
        ["namen", "systematik"],
        t("Die Namen wirken willkürlich, bis man merkt: sie **beschreiben** "
          "die Wolke. Luke Howard hat das System 1802 aufgestellt, mit "
          "lateinischen Wörtern, die man zusammensetzt wie Bausteine.\n\n"
          "**Die vier Grundwörter:**\n\n"
          "**cumulus** – der Haufen. Alles, was sich aufquellend nach oben "
          "türmt.\n\n"
          "**stratus** – die Schicht, von *sternere*, ausbreiten. Alles, was "
          "flach liegt.\n\n"
          "**cirrus** – die Haarlocke. Die dünnen, gefaserten Eiswolken ganz "
          "oben.\n\n"
          "**nimbus** – die Regenwolke. Steckt als Vor- oder Nachsilbe drin, "
          "wo es niederschlägt.\n\n"
          "**Dazu die Stockwerke:** *alto-* heißt hoch (von *altus*) und "
          "meint das **mittlere** Stockwerk, etwa 2 bis 7 km — das verwirrt "
          "anfangs jeden. Ohne Vorsilbe liegt die Wolke tief, mit *cirro-* "
          "ganz oben.\n\n"
          "**Und die Beinamen**, die sagen, wie die Wolke aussieht:\n\n"
          "*humilis* – niedrig, bescheiden\n"
          "*mediocris* – mittelmäßig, also mittelhoch\n"
          "*congestus* – aufgehäuft, angeschwollen\n"
          "*castellanus* – wie eine Burg, mit Zinnen\n"
          "*lenticularis* – linsenförmig\n"
          "*fractus* – zerbrochen, zerfetzt\n\n"
          "Damit liest sich jeder Name von selbst: **Cumulonimbus** ist die "
          "Haufen-Regen-Wolke. **Altocumulus castellanus** ist die "
          "mittelhohe Haufenwolke mit Zinnen. **Stratocumulus** ist der "
          "breitgelaufene Haufen, der zur Schicht geworden ist.",
          "The names look arbitrary until you notice that they **describe** "
          "the cloud. Luke Howard set the system up in 1802, out of Latin "
          "words that combine like building blocks.\n\n"
          "**The four root words:**\n\n"
          "**cumulus** – a heap. Anything welling upwards.\n\n"
          "**stratus** – a layer, from *sternere*, to spread out. Anything "
          "lying flat.\n\n"
          "**cirrus** – a curl of hair. The thin, fibrous ice clouds at the "
          "top.\n\n"
          "**nimbus** – a rain cloud. It appears as a prefix or suffix "
          "wherever precipitation falls.\n\n"
          "**Then the storeys:** *alto-* means high (from *altus*) but marks "
          "the **middle** level, roughly 2 to 7 km — which confuses everyone "
          "at first. With no prefix the cloud is low; with *cirro-* it is at "
          "the top.\n\n"
          "**And the epithets**, which say what the cloud looks like:\n\n"
          "*humilis* – low, humble\n"
          "*mediocris* – middling, so medium height\n"
          "*congestus* – piled up, swollen\n"
          "*castellanus* – like a castle, with battlements\n"
          "*lenticularis* – lens-shaped\n"
          "*fractus* – broken, ragged\n\n"
          "Every name then reads itself: **cumulonimbus** is the heap rain "
          "cloud. **Altocumulus castellanus** is the mid-level heap cloud "
          "with turrets. **Stratocumulus** is the heap that has spread out "
          "into a layer."),
        "cu-humilis",
        [
            mc(t("Was heißt „Cumulonimbus\" wörtlich?",
                 "What does \"cumulonimbus\" mean literally?"),
               [t("Haufen-Regen-Wolke", "Heap rain cloud"),
                t("Hohe Schichtwolke", "High layer cloud"),
                t("Gelockte Wolke", "Curled cloud"),
                t("Linsenwolke", "Lens cloud")], 0,
               t("*cumulus* = Haufen, *nimbus* = Regen. Der Name sagt genau, "
                 "was sie ist: ein Haufen, aus dem es regnet — und bei dieser "
                 "Größe eben auch blitzt.",
                 "*cumulus* = heap, *nimbus* = rain. The name says exactly "
                 "what it is: a heap that rains — and at that size, one that "
                 "also produces lightning."),
               bild="cumulonimbus"),
            mc(t("In welchem Stockwerk steht eine Wolke mit der Vorsilbe "
                 "„alto-\"?",
                 "Which level does a cloud with the prefix \"alto-\" sit at?"),
               [t("im mittleren, etwa 2 bis 7 km",
                  "the middle one, roughly 2 to 7 km"),
                t("im höchsten, über 7 km", "the highest, above 7 km"),
                t("im tiefsten, unter 2 km", "the lowest, below 2 km"),
                t("Das sagt die Vorsilbe nicht.",
                  "The prefix says nothing about that.")], 0,
               t("Das ist die eine Stelle, an der die Wortbedeutung in die "
                 "Irre führt: *altus* heißt hoch, gemeint ist aber das "
                 "**mittlere** Stockwerk. Ganz oben steht *cirro-*.",
                 "This is the one place where the literal meaning misleads: "
                 "*altus* means high, but it marks the **middle** level. The "
                 "top one is *cirro-*."),
               bild="ac-castellanus"),
            mc(t("Eine Wolke heißt *Cumulus fractus*. Wie sieht sie aus?",
                 "A cloud is called *cumulus fractus*. What does it look "
                 "like?"),
               [t("Ein zerfetzter Haufen ohne klare Form und ohne flache "
                  "Basis.",
                  "A ragged heap with no clear shape and no flat base."),
                t("Ein besonders großer Haufen.",
                  "An especially large heap."),
                t("Eine Schicht in Bruchstücken.",
                  "A layer in fragments."),
                t("Eine gefrorene Wolke.", "A frozen cloud.")], 0,
               t("*fractus* heißt zerbrochen. Für den Segelflug ist das ein "
                 "Zeichen: Eine zerfetzte Quellwolke ist entweder am "
                 "Zerfallen oder steht in zu feuchter, zu böiger Luft — unter "
                 "ihr ist selten etwas zu holen.",
                 "*fractus* means broken. For soaring that is a signal: a "
                 "ragged cumulus is either decaying or sitting in air too "
                 "damp and too gusty — there is rarely anything to be had "
                 "under it."),
               bild="cu-zyklus"),
        ]),

    # -- 1 -------------------------------------------------------------
    lektion("w-basis",
        t("Die flache Basis", "The flat base"),
        ["cu-humilis", "basis", "spread"],
        t("**Cumulus humilis** – wörtlich der *bescheidene Haufen*, und genau "
          "so sieht er aus: breiter als hoch, scharf umrissen, und vor "
          "allem **unten schnurgerade**.\n\n"
          "Diese gerade Linie ist kein Zufall und kein Zeichenfehler. Ein "
          "Thermikschlauch steigt auf, kühlt sich dabei um rund 1 °C je "
          "100 m ab, und in genau der Höhe, in der er seinen Taupunkt "
          "erreicht, kondensiert der Wasserdampf. Darunter ist die Luft "
          "nicht gesättigt, also ist dort nichts zu sehen. Deshalb der "
          "Schnitt.\n\n"
          "Für dich heißt das dreierlei:\n\n"
          "**Erstens:** Die Basis ist die Obergrenze des nutzbaren Steigens. "
          "In die Wolke darfst du nicht, und über ihr ist ohnehin Schluss.\n\n"
          "**Zweitens:** Alle Wolken derselben Luftmasse haben dieselbe "
          "Basishöhe. Sieht eine tiefer aus, ist sie weiter weg.\n\n"
          "**Drittens:** Du kannst die Basishöhe vorher ausrechnen. Die "
          "**Spreizung** ist die Differenz zwischen Temperatur und Taupunkt "
          "am Boden. Pro Grad Spreizung liegt die Basis etwa **125 m** "
          "höher:\n\n"
          "    Basis über Grund [m] ≈ 125 × (T − Taupunkt) [°C]\n\n"
          "22 °C bei 8 °C Taupunkt sind 14 Grad Spreizung, also rund "
          "1750 m über Grund.",
          "**Cumulus humilis** – literally the *humble heap*, and that is just "
          "how it looks: wider than tall, sharply outlined, and above all "
          "**dead flat underneath**.\n\n"
          "That straight line is neither a coincidence nor a drawing error. "
          "A thermal rises, cools at about 1 °C per 100 m, and at exactly "
          "the height where it reaches its dew point the vapour condenses. "
          "Below that the air is not saturated, so there is nothing to see. "
          "Hence the cut.\n\n"
          "Three things follow.\n\n"
          "**One:** the base is the ceiling of usable lift. You may not "
          "enter the cloud, and above it there is nothing anyway.\n\n"
          "**Two:** every cloud in the same air mass has the same base "
          "height. One that looks lower is simply further away.\n\n"
          "**Three:** you can work the base out beforehand. The **spread** "
          "is the difference between temperature and dew point at the "
          "ground. Each degree of spread puts the base about **125 m** "
          "higher:\n\n"
          "    base above ground [m] ≈ 125 × (T − dew point) [°C]\n\n"
          "22 °C with a dew point of 8 °C is 14 degrees of spread, so about "
          "1750 m above the ground."),
        "cu-humilis",
        [
            zahl(t("Am Morgen meldet der Platz 24 °C und 9 °C Taupunkt. In "
                   "welcher Höhe über Grund ist die Basis zu erwarten?",
                   "The field reports 24 °C and a dew point of 9 °C. What "
                   "cloud base above ground do you expect?"),
                 1875, t("m über Grund", "m above ground"),
                 t("15 Grad Spreizung × 125 m = 1875 m. Die Faustformel ist "
                   "gut genug fürs Cockpit; sie unterstellt trockenadiabatisches "
                   "Steigen und einen Taupunktrückgang von etwa 0,2 °C je 100 m.",
                   "15 degrees of spread × 125 m = 1875 m. The rule of thumb "
                   "is good enough in the cockpit; it assumes dry adiabatic "
                   "ascent and a dew point falling about 0.2 °C per 100 m."),
                 toleranz=0.08),
            mc(t("Eine Wolke am Horizont hat eine sichtbar tiefere Basis als "
                 "die über dir. Was ist die wahrscheinlichste Erklärung?",
                 "A cloud on the horizon has a visibly lower base than the "
                 "one above you. What is the most likely explanation?"),
               [t("Sie ist einfach weiter weg – die Perspektive drückt sie "
                  "nach unten.", "It is simply further away – perspective "
                  "pushes it down."),
                t("Dort ist die Thermik schwächer.", "The thermal is weaker "
                  "there."),
                t("Dort ist eine andere Luftmasse.", "A different air mass "
                  "is there."),
                t("Sie löst sich gerade auf.", "It is dissolving.")], 0,
               t("In derselben Luftmasse liegt die Basis überall gleich hoch. "
                 "Was tiefer aussieht, ist weiter weg. Erst wenn eine "
                 "**Reihe** von Wolken systematisch tiefer steht, ist "
                 "tatsächlich eine andere Luftmasse im Spiel – dann lohnt der "
                 "Blick auf die Front.",
                 "Within one air mass the base is at the same height "
                 "everywhere. What looks lower is further away. Only when a "
                 "**row** of clouds sits systematically lower is a different "
                 "air mass really involved – then look for the front."),
               bild="cu-humilis"),
        ]),

    # -- 2 -------------------------------------------------------------
    lektion("w-zyklus",
        t("Der Lebenslauf einer Thermikwolke",
          "The life of a thermal cloud"),
        ["zyklus", "anflug"],
        t("Eine Quellwolke lebt etwa **15 bis 20 Minuten**. Das ist die "
          "wichtigste Zahl des Streckenflugs, denn sie entscheidet, welche "
          "Wolke du anfliegst.\n\n"
          "**Wachsend** (links im Bild): klein, scharf umrissen, die Ränder "
          "wirken fest, die Oberseite quillt sichtbar nach oben. Unter ihr "
          "steigt es.\n\n"
          "**Reif** (Mitte): am größten, Basis am dunkelsten und am "
          "flächigsten, oben Blumenkohl. Hier ist das stärkste Steigen – "
          "aber es ist schon fast vorbei.\n\n"
          "**Zerfallend** (rechts): die Ränder franst aus, die Wolke wird "
          "durchsichtig, die flache Basis löst sich in Fetzen auf. Darunter "
          "sinkt es, oft kräftig.\n\n"
          "Die Regel lautet deshalb: **Flieg nicht die größte Wolke an, "
          "sondern die, die gerade wächst.** Bis du dort bist, ist sie reif. "
          "Fliegst du die reife an, ist sie bei deiner Ankunft tot und du "
          "stehst im Abwind.\n\n"
          "Dazu passt die zweite Regel: Der Aufwind steht **nicht unter der "
          "Wolke**, sondern schräg davor, denn der Wind versetzt die Wolke "
          "gegenüber ihrer Quelle. Such den Schlauch auf der Luvseite.",
          "A cumulus lives about **15 to 20 minutes**. That is the most "
          "important number in cross-country flying, because it decides "
          "which cloud you head for.\n\n"
          "**Growing** (left): small, sharply outlined, edges looking solid, "
          "the top visibly welling upwards. There is lift underneath.\n\n"
          "**Mature** (middle): biggest, base darkest and broadest, "
          "cauliflower on top. The strongest lift is here – and it is nearly "
          "over.\n\n"
          "**Decaying** (right): edges fraying, the cloud going "
          "translucent, the flat base breaking into shreds. Underneath it "
          "sinks, often hard.\n\n"
          "Hence the rule: **do not fly to the biggest cloud, fly to the one "
          "that is growing.** By the time you arrive it will be mature. Fly "
          "to the mature one and it is dead when you get there, leaving you "
          "in the sink.\n\n"
          "And the second rule: the thermal is **not under the cloud** but "
          "ahead of it, because the wind displaces the cloud from its "
          "source. Look for the core on the upwind side."),
        "cu-zyklus",
        [
            mc(t("Du bist auf halber Höhe und hast zwei Wolken zur Auswahl: "
                 "eine große mit dunkler, breiter Basis in 8 km, und eine "
                 "kleine, scharf umrissene, sichtbar wachsende in 10 km. "
                 "Wohin?",
                 "You are at half height with two clouds to choose from: a "
                 "big one with a dark, broad base 8 km away, and a small, "
                 "sharply outlined, visibly growing one 10 km away. Which?"),
               [t("Die kleine wachsende – sie ist bei der Ankunft reif.",
                  "The small growing one – it will be mature when you get "
                  "there."),
                t("Die große – dort ist jetzt das stärkste Steigen.",
                  "The big one – the strongest lift is there now."),
                t("Die große, weil sie näher ist.",
                  "The big one, because it is closer."),
                t("Keine von beiden, lieber geradeaus.",
                  "Neither, better to press on straight.")], 0,
               t("Rechne mit der Flugzeit. Bei 100 km/h brauchst du für 10 km "
                 "sechs Minuten – in denen die große Wolke ihren Zyklus "
                 "beendet und die kleine ihren Höhepunkt erreicht. Wer nach "
                 "dem aktuellen Bild entscheidet statt nach dem Bild bei "
                 "Ankunft, fliegt systematisch in den Abwind.",
                 "Work with your travel time. At 100 km/h, 10 km takes six "
                 "minutes – in which the big cloud finishes its cycle and "
                 "the small one peaks. Deciding by the picture now instead "
                 "of the picture on arrival puts you in the sink "
                 "systematically."),
               bild="cu-zyklus"),
            mc(t("Es weht mit 20 km/h aus Westen. Wo suchst du unter einer "
                 "reifen Wolke den Schlauch?",
                 "The wind is 20 km/h from the west. Where do you look for "
                 "the core under a mature cloud?"),
               [t("Am Westrand, also auf der Luvseite.",
                  "At the western edge, that is, upwind."),
                t("Genau in der Mitte unter der Wolke.",
                  "Exactly in the middle under the cloud."),
                t("Am Ostrand, auf der Leeseite.",
                  "At the eastern edge, downwind."),
                t("Das hängt nur von der Sonne ab.",
                  "That depends only on the sun.")], 0,
               t("Der Schlauch wird mit der Höhe verweht, die Wolke steht "
                 "also versetzt über ihrer Quelle. Von unten heißt das: der "
                 "Einstieg liegt auf der Luvseite, oft ein Stück vor der "
                 "sichtbaren Wolkenkante. Je stärker der Wind und je höher "
                 "die Basis, desto größer der Versatz.",
                 "The column is blown downwind as it rises, so the cloud "
                 "sits displaced from its source. From below that means the "
                 "entry is on the upwind side, often a little ahead of the "
                 "visible edge. The stronger the wind and the higher the "
                 "base, the bigger the offset.")),
        ]),
])


# -- weitere Lektionen des Wolkenkapitels -----------------------------------

K_WOLKEN["lektionen"].extend([

    lektion("w-ueberentwicklung",
        t("Wenn es zu gut läuft", "When it gets too good"),
        ["congestus", "cumulonimbus", "ueberentwicklung"],
        t("**Cumulus congestus** – der *aufgehäufte* Haufen: höher als breit, "
          "oben quellend wie Blumenkohl, Basis dunkel und breit. Darunter steigt es stark – "
          "3 bis 5 m/s sind keine Seltenheit. Es ist die beste und die "
          "letzte gute Wolke des Tages.\n\n"
          "Denn was danach kommt, ist der **Cumulonimbus**. Das "
          "Erkennungszeichen ist nicht die Größe, sondern die **Oberseite**: "
          "sobald der Blumenkohl oben weich, faserig, verwaschen wird, ist "
          "die Wolke oben vereist. Von da an ist sie kein Aufwind mehr, "
          "sondern ein Gewitter im Bau. Der Amboss breitet sich mit dem "
          "Höhenwind aus und zeigt, wohin es zieht.\n\n"
          "**Die Gefahren, der Reihe nach:**\n\n"
          "Unter der Basis kann der Aufwind so stark werden, dass er auch "
          "mit gezogenen Bremsen nicht mehr zu verlassen ist – "
          "Wolkeneinflug gegen den eigenen Willen.\n\n"
          "Die **Böenfront** läuft dem Gewitter bis 20 km voraus, oft bei "
          "noch blauem Himmel: plötzlicher Windsprung, Scherung, "
          "Turbulenz – gefährlich vor allem im Landeanflug.\n\n"
          "Der **Abwind** im Niederschlagsbereich erreicht Werte, die kein "
          "Segelflugzeug wegsteigt.\n\n"
          "Die praktische Regel: Sobald ein Cu oben faserig wird, hältst du "
          "Abstand und planst die Landung. Nicht, wenn es blitzt – dann ist "
          "es zu spät.",
          "**Cumulus congestus** – the *piled-up* heap: taller than it is "
          "wide, welling up like cauliflower on top, base dark and broad. There is strong lift "
          "underneath – 3 to 5 m/s is common. It is the best and the last "
          "good cloud of the day.\n\n"
          "Because what comes next is the **cumulonimbus**. The giveaway is "
          "not the size but the **top**: as soon as the cauliflower turns "
          "soft, fibrous and washed-out, the cloud has glaciated. From then "
          "on it is not a thermal but a thunderstorm under construction. The "
          "anvil spreads with the upper wind and shows where it is going.\n\n"
          "**The dangers, in order:**\n\n"
          "Under the base the lift can become strong enough that you cannot "
          "leave it even with the brakes out – entering cloud against your "
          "will.\n\n"
          "The **gust front** runs up to 20 km ahead of the storm, often "
          "under a still-blue sky: sudden wind shift, shear, turbulence – "
          "dangerous above all on final approach.\n\n"
          "The **downdraught** in the rain area reaches values no glider "
          "climbs out of.\n\n"
          "The practical rule: as soon as a cumulus goes fibrous on top, "
          "keep your distance and plan the landing. Not when it starts to "
          "flash – by then it is too late."),
        "cu-congestus",
        [
            mc(t("Woran erkennst du, dass ein Cumulus congestus zum "
                 "Cumulonimbus geworden ist?",
                 "How do you tell that a cumulus congestus has become a "
                 "cumulonimbus?"),
               [t("Die Oberseite wird weich und faserig statt scharf und "
                  "knollig.", "The top turns soft and fibrous instead of "
                  "sharp and knobbly."),
                t("Die Wolke wird dunkler.", "The cloud gets darker."),
                t("Die Basis sinkt.", "The base drops."),
                t("Es beginnt zu blitzen.", "It starts to lightning.")], 0,
               t("Der Übergang ist die Vereisung der Oberseite – sie macht "
                 "aus knolligen Wassertröpfchen faserige Eiskristalle. Das "
                 "ist sichtbar, lange bevor es blitzt, und es ist der "
                 "Zeitpunkt für die Entscheidung. Dunkler wird die Basis "
                 "auch bei harmlosen Wolken, und sinken tut sie gar nicht.",
                 "The transition is glaciation of the top – it turns knobbly "
                 "water droplets into fibrous ice crystals. That is visible "
                 "long before any lightning, and it is the moment to decide. "
                 "A base darkens under harmless clouds too, and it does not "
                 "drop at all."),
               bild="cumulonimbus"),
            mc(t("Der Himmel über dem Platz ist blau, aber 15 km westlich "
                 "steht ein Gewitter. Du bist im Anflug. Was erwartest du?",
                 "The sky over the field is blue, but there is a "
                 "thunderstorm 15 km to the west. You are on approach. What "
                 "do you expect?"),
               [t("Eine Böenfront kann dich vor dem Regen erreichen: "
                  "Windsprung und Scherung im Endteil.",
                  "A gust front may reach you ahead of the rain: wind shift "
                  "and shear on final."),
                t("Nichts, solange es nicht regnet.",
                  "Nothing, as long as it is not raining."),
                t("Nur etwas mehr Thermik.", "Just a little more thermal."),
                t("Rückenwind aus Osten.", "A tailwind from the east.")], 0,
               t("Die ausfließende Kaltluft läuft dem Gewitter weit voraus, "
                 "bei blauem Himmel und ohne Vorwarnung außer einem "
                 "aufziehenden Staubrand oder einer Böenwalze. Genau in der "
                 "Landephase ist das der gefährlichste Teil des ganzen "
                 "Gewitters.",
                 "The outflowing cold air runs far ahead of the storm, under "
                 "a blue sky and with no warning beyond a line of dust or a "
                 "roll cloud. In the landing phase that is the most "
                 "dangerous part of the whole storm."),
               bild="cumulonimbus"),
        ]),

    lektion("w-zumachen",
        t("Wenn der Tag zumacht", "When the day closes down"),
        ["stratocumulus", "cirrus", "abschirmung"],
        t("Thermik braucht Sonne am Boden. Zwei Wolkenarten nehmen sie weg, "
          "auf ganz verschiedene Weise – und beide sind früh zu sehen.\n\n"
          "**Stratocumulus** – wörtlich die *Schicht aus Haufen*, und der Name "
          "beschreibt genau, was passiert ist: die Quellwolken sind "
          "breitgelaufen und "
          "zusammengewachsen. Keine Lücken mehr, keine scharfe Basis, kein "
          "Blumenkohl. Das passiert typisch dann, wenn eine Inversion den "
          "Wolken den Weg nach oben versperrt: sie können nur noch in die "
          "Breite. Der Boden liegt im Schatten, die Thermik erstickt sich "
          "selbst. Manchmal reißt es nachmittags wieder auf, oft nicht.\n\n"
          "**Cirrus** – die *Haarlocke*: dünne Eisfedern in 8 bis 12 km Höhe, "
          "mit Haken am "
          "Kopf. Für sich harmlos – aber Cirrus, der von Westen aufzieht und "
          "dichter wird, ist die Ankündigung einer **Warmfront**, meist 12 "
          "bis 24 Stunden im Voraus. Erst wird er zu Cirrostratus, dann "
          "erscheint der Halo um die Sonne, dann ist der Tag gelaufen: Die "
          "hohe Schicht nimmt der Einstrahlung so viel weg, dass die Thermik "
          "einschläft, lange bevor der Regen kommt.\n\n"
          "Wichtig ist die **Richtung der Entwicklung**. Aufreißender Cirrus "
          "am Abend ist bedeutungslos. Cirrus, der morgens dünn beginnt und "
          "mittags den halben Himmel deckt, beendet den Streckenflug.",
          "Thermals need sun on the ground. Two cloud types take it away, in "
          "quite different ways – and both are visible early.\n\n"
          "**Stratocumulus** – literally a *layer of heaps*, and the name "
          "describes exactly what happened: the heap clouds have spread out "
          "and merged. No "
          "gaps left, no sharp base, no cauliflower. Typically this happens "
          "when an inversion blocks the way up: the clouds can only grow "
          "sideways. The ground lies in shadow and the thermal suffocates "
          "itself. Sometimes it breaks up again in the afternoon, often "
          "not.\n\n"
          "**Cirrus** – the *curl of hair*: thin ice feathers at 8 to 12 km "
          "with hooks at the "
          "head. Harmless in itself – but cirrus moving in from the west and "
          "thickening announces a **warm front**, usually 12 to 24 hours "
          "ahead. First it becomes cirrostratus, then a halo appears round "
          "the sun, and then the day is over: the high layer takes so much "
          "out of the sunshine that the thermals die long before any rain.\n\n"
          "What matters is the **direction of the trend**. Cirrus breaking "
          "up in the evening means nothing. Cirrus that starts thin in the "
          "morning and covers half the sky by midday ends the cross-country "
          "flight."),
        "stratocumulus",
        [
            mc(t("Die Cumuluswolken sind seit einer Stunde breitgelaufen und "
                 "berühren sich. Was ist die wahrscheinlichste Ursache?",
                 "For an hour the cumulus have been spreading out and now "
                 "touch each other. What is the most likely cause?"),
               [t("Eine Inversion deckelt sie – sie können nur noch in die "
                  "Breite wachsen.",
                  "An inversion is capping them – they can only grow "
                  "sideways."),
                t("Die Sonne ist zu stark.", "The sun is too strong."),
                t("Der Wind hat gedreht.", "The wind has shifted."),
                t("Die Luft ist zu trocken.", "The air is too dry.")], 0,
               t("Breitlaufen statt Wachsen heißt: oben ist eine Sperre. Die "
                 "Folge ist Abschirmung, und damit endet die Thermik von "
                 "selbst. Wer das früh sieht, dreht rechtzeitig um oder "
                 "sucht die Kante der Abschirmung, wo die Sonne noch "
                 "hinkommt.",
                 "Spreading instead of growing means a lid above. The result "
                 "is shading, and the thermals end by themselves. Seeing it "
                 "early means turning back in time, or heading for the edge "
                 "of the shading where the sun still reaches."),
               bild="stratocumulus"),
            mc(t("Um 9 Uhr stehen dünne Eisfedern im Westen, um 12 Uhr "
                 "decken sie ein Drittel des Himmels. Was planst du?",
                 "At 9 o'clock there are thin ice feathers in the west; by "
                 "noon they cover a third of the sky. What do you plan?"),
               [t("Die Strecke kürzen – die Warmfront schirmt ab, bevor sie "
                  "Regen bringt.",
                  "Shorten the task – the warm front shades the ground long "
                  "before it brings rain."),
                t("Nichts ändern, Cirrus ist zu hoch, um zu stören.",
                  "Change nothing, cirrus is too high to matter."),
                t("Die Strecke verlängern, vor der Front wird es besser.",
                  "Extend the task, it gets better ahead of a front."),
                t("Auf Wellenflug umstellen.",
                  "Switch to wave soaring.")], 0,
               t("Cirrus in dieser Entwicklung ist die Vorhut einer "
                 "Warmfront. Die Einstrahlung geht zurück, bevor irgendetwas "
                 "am Boden zu spüren ist – der Tag endet zwei bis drei "
                 "Stunden früher als gedacht. Gerechnet wird mit dem, was in "
                 "drei Stunden ist, nicht mit dem, was jetzt ist.",
                 "Cirrus developing like that is the vanguard of a warm "
                 "front. The sunshine drops off before anything is "
                 "noticeable at ground level – the day ends two or three "
                 "hours earlier than planned. You plan for what the sky will "
                 "be in three hours, not what it is now."),
               bild="cirrus"),
        ]),

    lektion("w-strassen",
        t("Wolkenstraßen und Wellen", "Cloud streets and wave"),
        ["wolkenstrasse", "lenticularis", "rotor"],
        t("**Wolkenstraßen** entstehen, wenn die Thermik in einem Wind von "
          "etwa 20 bis 40 km/h aufsteigt, der mit der Höhe wenig dreht. Die "
          "Thermik ordnet sich dann in lange Walzen parallel zum Wind. Über "
          "den aufsteigenden Ästen stehen die Wolken, dazwischen liegt "
          "Abwind.\n\n"
          "Für dich ist das die freie Autobahn: Unter einer Straße kannst du "
          "**geradeaus im Steigen fliegen**, ohne zu kreisen – schneller "
          "geht Streckenflug nicht. Der Preis: quer zu den Straßen zu fliegen "
          "kostet doppelt, weil jeder Übergang durch das Sinken zwischen den "
          "Walzen führt.\n\n"
          "**Lenticularis** – *linsenförmig* – ist etwas völlig anderes. Glatt, "
          "oft mehrfach übereinander gestapelt – und vor allem: **sie steht "
          "still**, während der Wind mit 60 km/h hindurchbläst. Das ist "
          "keine Thermik, sondern eine **Leewelle**: Luft, die über einen "
          "Bergrücken gedrückt wurde und dahinter schwingt. Die Wolke "
          "markiert den Wellenberg.\n\n"
          "Wellenflug ist ruhig, gleichmäßig und geht sehr hoch – die "
          "Höhenrekorde des Segelflugs stammen alle daher.\n\n"
          "**Aber:** unter der Welle, im Lee des Bergs, liegt der **Rotor** – "
          "die zerrissene, dunkle Walze im Bild unten. Dort herrscht "
          "Turbulenz, die Segelflugzeuge strukturell überfordert hat. Der "
          "Rotor ist zu durchfliegen, um in die Welle zu kommen, und er ist "
          "der gefährlichste Teil des Wellenflugs.",
          "**Cloud streets** form when thermals rise in a wind of roughly 20 "
          "to 40 km/h that changes little with height. The convection then "
          "organises into long rolls parallel to the wind. The clouds sit "
          "over the rising branches, with sink in between.\n\n"
          "For you that is the free motorway: under a street you can "
          "**fly straight ahead and still climb**, without circling – "
          "cross-country does not get faster. The price: crossing the "
          "streets costs double, because every transition goes through the "
          "sink between the rolls.\n\n"
          "**Lenticularis** – *lens-shaped* – is something else entirely. Smooth, "
          "often stacked several deep – and above all: **it stands still** "
          "while the wind blows through it at 60 km/h. That is not a thermal "
          "but a **lee wave**: air forced over a ridge and oscillating "
          "behind it. The cloud marks the crest.\n\n"
          "Wave flying is smooth, steady and goes very high – every glider "
          "altitude record comes from it.\n\n"
          "**But:** below the wave, in the lee of the ridge, lies the "
          "**rotor** – the torn, dark roll at the bottom of the picture. The "
          "turbulence there has broken gliders structurally. The rotor has "
          "to be flown through to reach the wave, and it is the most "
          "dangerous part of wave flying."),
        "wolkenstrasse",
        [
            mc(t("Du fliegst unter einer Wolkenstraße nach Norden, dein Ziel "
                 "liegt aber nordöstlich. Was ist meist schneller?",
                 "You are flying north under a cloud street, but your goal "
                 "is to the north-east. What is usually faster?"),
               [t("Der Straße folgen und erst am Ende quer versetzen.",
                  "Follow the street and only cross over at the end."),
                t("Direkt auf dem kürzesten Weg zum Ziel.",
                  "Straight along the shortest track to the goal."),
                t("Abwechselnd kurz quer und kurz längs.",
                  "Alternating short crossings and short runs."),
                t("Das macht keinen Unterschied.",
                  "It makes no difference.")], 0,
               t("Unter der Straße fliegst du im Steigen geradeaus; quer "
                 "dazu verlierst du bei jedem Übergang Höhe im Sinken "
                 "zwischen den Walzen. Der scheinbare Umweg ist fast immer "
                 "der schnellere Weg – die Geometrie zahlt sich aus, solange "
                 "der Winkel unter etwa 45 Grad bleibt.",
                 "Under the street you fly straight ahead climbing; across "
                 "it you lose height in the sink between the rolls at every "
                 "transition. The apparent detour is almost always the "
                 "faster route – the geometry pays as long as the angle "
                 "stays under about 45 degrees."),
               bild="wolkenstrasse"),
            mc(t("Eine linsenförmige Wolke steht seit zwanzig Minuten "
                 "unbewegt über dem Bergrücken, obwohl es kräftig weht. Was "
                 "bedeutet das – und was liegt darunter?",
                 "A lens-shaped cloud has stood motionless over the ridge "
                 "for twenty minutes although the wind is strong. What does "
                 "that mean – and what lies beneath it?"),
               [t("Leewelle; darunter im Lee liegt der Rotor mit schwerer "
                  "Turbulenz.",
                  "Lee wave; below it, in the lee, lies the rotor with "
                  "severe turbulence."),
                t("Eine besonders starke Thermikquelle.",
                  "A particularly strong thermal source."),
                t("Eine Inversion.", "An inversion."),
                t("Beginnende Gewitterbildung.",
                  "A thunderstorm beginning to form.")], 0,
               t("Eine stehende Wolke im starken Wind heißt: die Luft strömt "
                 "hindurch, kondensiert im aufsteigenden Ast und löst sich "
                 "im absteigenden wieder auf. Das ist die Signatur der "
                 "Welle. Der Rotor darunter ist der Teil, der Menschen "
                 "umgebracht hat – ruhige Welle oben, zerrissene Walze "
                 "unten.",
                 "A cloud standing still in a strong wind means the air is "
                 "flowing through it, condensing in the rising branch and "
                 "evaporating in the descending one. That is the signature "
                 "of wave. The rotor below is the part that has killed "
                 "people – smooth wave above, torn roll underneath."),
               bild="lenticularis"),
        ]),

    lektion("w-castellanus",
        t("Warnzeichen aus der Höhe", "Warnings from above"),
        ["castellanus", "labilitaet"],
        t("**Altocumulus castellanus** – der mittelhohe Haufen *mit Zinnen*, "
          "und mehr steht nicht im Namen: kleine Türmchen, die auf einer "
          "gemeinsamen Basis in mittlerer Höhe stehen – wie Zinnen auf einer "
          "Mauer. Sie sehen harmlos aus und sind die wichtigste Frühwarnung, "
          "die der Morgenhimmel hergibt.\n\n"
          "Türmchen bedeuten: **auch in der Höhe ist die Luft labil.** Da "
          "oben fängt es schon an zu quellen, ohne dass die Bodenthermik "
          "überhaupt eingesetzt hat.\n\n"
          "Was daraus folgt, ist zweischneidig:\n\n"
          "**Gut:** Die Thermik setzt früher ein und wird kräftig, weil "
          "nichts sie deckelt.\n\n"
          "**Schlecht:** Genau deshalb entwickelt der Tag auch früh über – "
          "Gewitter am frühen Nachmittag statt am Abend. Castellanus am "
          "Morgen heißt in der Praxis: früh starten, früh zurück sein, und "
          "die Rückkehr nicht auf den späten Nachmittag legen.\n\n"
          "Der Unterschied zum harmlosen Altocumulus ist die Höhe der "
          "einzelnen Elemente. Flache Schäfchen: stabil. Türmchen, die höher "
          "als breit sind: labil.",
          "**Altocumulus castellanus** – the mid-level heap *with battlements*, "
          "and the name says no more than that: little turrets on a common "
          "base at middle levels – like battlements on a wall. They look "
          "harmless and are the most valuable early warning the morning sky "
          "offers.\n\n"
          "Turrets mean: **the air is unstable up there as well.** It is "
          "already welling up at that height before the surface thermals "
          "have even started.\n\n"
          "What follows cuts both ways.\n\n"
          "**Good:** thermals start earlier and become strong, because "
          "nothing caps them.\n\n"
          "**Bad:** for exactly that reason the day also overdevelops "
          "early – thunderstorms in the early afternoon instead of the "
          "evening. Castellanus in the morning means in practice: start "
          "early, be back early, and do not schedule the return for late "
          "afternoon.\n\n"
          "What separates it from harmless altocumulus is the height of the "
          "individual elements. Flat little sheep: stable. Turrets taller "
          "than they are wide: unstable."),
        "ac-castellanus",
        [
            mc(t("Beim Briefing um 8 Uhr stehen Altocumulus castellanus im "
                 "Süden. Wie planst du den Tag?",
                 "At the 8 o'clock briefing there is altocumulus castellanus "
                 "to the south. How do you plan the day?"),
               [t("Früher starten und früher zurück sein – der Tag wird gut, "
                  "aber kurz.",
                  "Start earlier and be back earlier – the day will be good "
                  "but short."),
                t("Später starten, die Thermik braucht länger.",
                  "Start later, the thermals will take longer."),
                t("Wie immer, Castellanus sagt nichts über den Boden.",
                  "As usual, castellanus says nothing about the surface."),
                t("Gar nicht fliegen.", "Do not fly at all.")], 0,
               t("Labilität in der Höhe beschleunigt beides: den Beginn der "
                 "Thermik und die Überentwicklung. Der Fehler wäre, die gute "
                 "Frühthermik als Zeichen für einen langen Tag zu nehmen – "
                 "es ist das Gegenteil.",
                 "Instability aloft speeds up both the start of the thermals "
                 "and the overdevelopment. The mistake would be to read the "
                 "good early lift as a sign of a long day – it is the "
                 "opposite."),
               bild="ac-castellanus"),
        ]),
])

# ===========================================================================
# Thermik und Wetter
# ===========================================================================

K_THERMIK = kapitel(
    "thermik", t("Thermik und Wetter", "Thermals and weather"), 2,
    t("Woher die Thermik kommt, wann sie einsetzt, wie hoch sie trägt und "
      "woran sie stirbt. Dazu die Wetterlagen, die einen Segelflugtag "
      "machen oder beenden.",
      "Where thermals come from, when they start, how high they go and what "
      "kills them. Plus the weather patterns that make or end a soaring "
      "day."), [

    lektion("t-entstehung",
        t("Wie ein Aufwind entsteht", "How a thermal forms"),
        ["thermik", "ausloesung", "inversion"],
        t("Die Sonne heizt nicht die Luft, sondern den **Boden**. Der Boden "
          "heizt die Luft darüber. Und weil Böden verschieden schnell warm "
          "werden, entsteht ein Flickenteppich aus wärmeren und kühleren "
          "Luftpaketen.\n\n"
          "Ein warmes Paket steigt nicht sofort. Es klebt am Boden, wächst, "
          "und löst sich erst ab, wenn es genug Auftrieb hat oder etwas es "
          "anstößt: eine Geländekante, ein Waldrand, ein Windstoß, ein "
          "vorbeifahrender Zug. Das ist die **Auslösung** — und deshalb "
          "kommt Thermik in Schüben und nicht als gleichmäßiger Strom.\n\n"
          "**Gute Auslöser** sind Grenzen: Feld an Wald, Ort an Wiese, "
          "Sonnenhang an Schatten. Besonders zuverlässig sind trockene, "
          "dunkle, der Sonne zugeneigte Flächen — abgeerntete Felder, "
          "Industrieanlagen, Fels. **Schlecht** sind Wasser, Wald im "
          "Vollbestand und frisch gepflügte nasse Erde.\n\n"
          "Nach oben steigt das Paket, bis seine Temperatur der Umgebung "
          "gleicht. Liegt darüber eine **Inversion** — eine Schicht, in der "
          "es nach oben wärmer statt kälter wird — ist Schluss, auch wenn es "
          "unten noch so gut geht. Die Inversion ist der Deckel des Tages.",
          "The sun does not heat the air, it heats the **ground**. The "
          "ground heats the air above it. And because different surfaces "
          "warm at different rates, a patchwork of warmer and cooler parcels "
          "forms.\n\n"
          "A warm parcel does not rise at once. It clings to the ground, "
          "grows, and only breaks away when it has enough buoyancy or "
          "something nudges it: a break in the terrain, a treeline, a gust, "
          "a passing train. That is **triggering** — and it is why thermals "
          "come in pulses rather than as a steady stream.\n\n"
          "**Good triggers** are boundaries: field against forest, village "
          "against meadow, sunlit slope against shade. Dry, dark, sun-facing "
          "surfaces are the most reliable — harvested fields, industrial "
          "sites, rock. **Poor** ones are water, dense forest and freshly "
          "ploughed wet soil.\n\n"
          "The parcel rises until its temperature matches its surroundings. "
          "If an **inversion** lies above — a layer where it gets warmer "
          "instead of colder with height — that is the end, however good it "
          "is lower down. The inversion is the lid on the day."),
        "cu-humilis",
        [
            mc(t("Du suchst über flachem Land einen Aufwind. Wo ist er am "
                 "wahrscheinlichsten?",
                 "You are looking for a thermal over flat country. Where is "
                 "it most likely?"),
               [t("An der Grenze zwischen zwei verschiedenen Flächen, etwa "
                  "Feld und Wald.",
                  "At the boundary between two different surfaces, such as "
                  "field and forest."),
                t("Über dem größten zusammenhängenden Wald.",
                  "Over the largest continuous forest."),
                t("Über einem See.", "Over a lake."),
                t("Über frisch bewässerten Feldern.",
                  "Over freshly irrigated fields.")], 0,
               t("Kanten lösen aus. Eine gleichförmige Fläche heizt zwar "
                 "auf, aber die warme Luft bleibt liegen, bis etwas sie "
                 "anstößt — und genau das tut eine Grenze.",
                 "Edges trigger. A uniform surface heats up all right, but "
                 "the warm air sits there until something nudges it — and "
                 "that is exactly what a boundary does.")),
            mc(t("Die Cumuluswolken stehen alle in derselben Höhe und werden "
                 "nicht höher. Was begrenzt sie?",
                 "The cumulus all sit at the same height and grow no taller. "
                 "What limits them?"),
               [t("Eine Inversion über der Basis.",
                  "An inversion above the base."),
                t("Zu wenig Sonne.", "Too little sun."),
                t("Zu viel Wind.", "Too much wind."),
                t("Zu trockene Luft.", "Air that is too dry.")], 0,
               t("Über der Inversion wird die Umgebungsluft wärmer statt "
                 "kälter; das aufsteigende Paket verliert seinen Auftrieb "
                 "schlagartig. Die Wolken können dann nur noch in die "
                 "Breite — und genau daraus wird später Stratocumulus.",
                 "Above an inversion the surrounding air gets warmer instead "
                 "of colder; the rising parcel loses its buoyancy at once. "
                 "The clouds can then only spread sideways — which is how "
                 "stratocumulus comes about."),
               bild="stratocumulus"),
        ]),

    lektion("t-tagesgang",
        t("Der Tagesgang", "The course of the day"),
        ["tagesgang", "planung"],
        t("Thermik folgt der Sonne mit Verzögerung. Ein mitteleuropäischer "
          "Sommertag läuft ungefähr so:\n\n"
          "**Morgens** steht eine Bodeninversion von der Nacht. Erst wenn "
          "die Sonne sie weggeheizt hat, beginnt überhaupt etwas — "
          "typischerweise zwei bis vier Stunden nach Sonnenaufgang.\n\n"
          "**Vormittags** setzt die Thermik ein, schwach und mit tiefer "
          "Basis. Die Basis steigt im Lauf des Tages, weil sich die "
          "Bodenluft erwärmt und die Spreizung zunimmt.\n\n"
          "**Mittags bis Nachmittag** ist das Optimum: stärkstes Steigen, "
          "höchste Basis. Das stärkste Steigen liegt oft nicht zur "
          "Sonnenhöchststand, sondern ein bis zwei Stunden danach — der "
          "Boden braucht Zeit.\n\n"
          "**Spätnachmittag** wird es schwächer und weicher, die Abstände "
          "zwischen den Aufwinden werden größer. Die letzte Stunde ist "
          "trügerisch: Die Basis steht noch hoch, aber es steigt kaum noch.\n\n"
          "Für die Planung heißt das: Die **Rückkehr** wird nicht nach der "
          "Basishöhe berechnet, sondern nach dem, was in einer Stunde noch "
          "trägt. Wer den Wendepunkt auf die letzte gute Stunde legt, "
          "landet auswärts.",
          "Thermals follow the sun with a delay. A central European summer "
          "day runs roughly like this.\n\n"
          "**Morning**: a ground inversion left from the night. Only once "
          "the sun has burned it off does anything start at all — typically "
          "two to four hours after sunrise.\n\n"
          "**Late morning**: thermals begin, weak and with a low base. The "
          "base climbs through the day as the surface air warms and the "
          "spread increases.\n\n"
          "**Midday to afternoon** is the optimum: strongest climbs, highest "
          "base. The best lift often comes not at the sun's highest point "
          "but one or two hours later — the ground needs time.\n\n"
          "**Late afternoon** it weakens and softens, and the spacing "
          "between thermals grows. The last hour is deceptive: the base is "
          "still high but there is hardly any lift left.\n\n"
          "For planning that means the **return** is not computed from the "
          "base height but from what will still carry in an hour's time. "
          "Put the turnpoint in the last good hour and you land out."),
        "wolkenstrasse",
        [
            zahl(t("Sonnenaufgang war um 5:30. Wann ist mit der ersten "
                   "nutzbaren Thermik zu rechnen? Gib die volle Stunde an "
                   "(z. B. 9 für 9 Uhr).",
                   "Sunrise was at 05:30. When can the first usable thermal "
                   "be expected? Give the whole hour (e.g. 9 for 09:00)."),
                 8.5, t("Uhr", "o'clock"),
                 t("Zwei bis vier Stunden nach Sonnenaufgang, je nach "
                   "Jahreszeit, Bewölkung und Bodenfeuchte — hier also "
                   "zwischen 7:30 und 9:30. Wer früher aufrüstet, wartet am "
                   "Start.",
                   "Two to four hours after sunrise, depending on season, "
                   "cloud and ground moisture — here between 07:30 and "
                   "09:30. Rig earlier and you wait on the grid."),
                 toleranz=0.14),
            mc(t("Um 17 Uhr steht die Basis noch bei 1800 m, aber das "
                 "Steigen ist auf 0,5 m/s gefallen. Was bedeutet das für den "
                 "Rückflug?",
                 "At 17:00 the base is still at 1800 m but the climbs are "
                 "down to 0.5 m/s. What does that mean for the run home?"),
               [t("Jetzt heimfliegen – die Höhe täuscht, der Tag ist fast "
                  "vorbei.",
                  "Head home now – the height is deceptive, the day is "
                  "nearly over."),
                t("Noch ein Schenkel geht sicher.",
                  "One more leg will certainly work."),
                t("Die Basis ist entscheidend, also alles gut.",
                  "The base is what counts, so all is well."),
                t("Tiefer fliegen, dort ist es stärker.",
                  "Fly lower, it is stronger there.")], 0,
               t("Die Basis bleibt am Abend oft lange stehen, während das "
                 "Steigen längst zusammengebrochen ist. Entscheidend ist "
                 "nicht, wie hoch man noch kommt, sondern ob man **wieder** "
                 "hochkommt.",
                 "The base often stays put into the evening long after the "
                 "climbs have collapsed. What matters is not how high you "
                 "can get but whether you can get up **again**.")),
        ]),

    lektion("t-fronten",
        t("Fronten und was sie bringen", "Fronts and what they bring"),
        ["kaltfront", "warmfront", "hochdruck"],
        t("**Kaltfront**: Kalte Luft schiebt sich unter warme und hebt sie "
          "an. Das geht schnell und steil — Schauer, Gewitter, Böen, "
          "manchmal eine Böenlinie weit voraus. **Dahinter** aber kommt oft "
          "der beste Segelflugtag des Monats: labile, klare Rückseitenluft "
          "mit hoher Basis und kräftigem Steigen.\n\n"
          "**Warmfront**: Warme Luft gleitet flach auf kalte auf. Das geht "
          "langsam und über hunderte Kilometer: erst Cirrus, dann "
          "Cirrostratus mit Halo, dann Altostratus, dann Regen. Für den "
          "Segelflug ist die Warmfront schon einen Tag vorher erledigt — die "
          "hohe Schicht nimmt der Sonne die Kraft.\n\n"
          "**Hochdruck** ist nicht automatisch gut. Absinkende Luft "
          "erwärmt sich und baut eine **Absinkinversion** — der Deckel liegt "
          "dann tief, die Basis bleibt niedrig, und bei anhaltendem Hoch "
          "wird die Luft unter der Inversion diesig. Ein frisches Hoch nach "
          "einer Kaltfront ist gut; ein altes Hoch nach fünf Tagen ist es "
          "nicht.\n\n"
          "Die brauchbarste Faustregel: Es geht nicht um Sonne, sondern um "
          "**Labilität**. Ein Tag mit Sonne und stabiler Luft bringt nichts; "
          "ein Tag mit Quellwolken und labiler Luft trägt auch bei mäßiger "
          "Einstrahlung.",
          "**Cold front**: cold air pushes under warm and lifts it. That "
          "happens fast and steeply — showers, thunderstorms, gusts, "
          "sometimes a squall line far ahead. **Behind** it, though, often "
          "comes the best soaring day of the month: unstable, clear air with "
          "a high base and strong climbs.\n\n"
          "**Warm front**: warm air slides gently up over cold. That happens "
          "slowly and over hundreds of kilometres: first cirrus, then "
          "cirrostratus with a halo, then altostratus, then rain. For "
          "soaring a warm front is finished a day in advance — the high "
          "layer takes the strength out of the sun.\n\n"
          "**High pressure** is not automatically good. Subsiding air warms "
          "and builds a **subsidence inversion** — the lid then sits low, "
          "the base stays down, and in a persistent high the air below the "
          "inversion turns hazy. A fresh high behind a cold front is good; "
          "an old high on its fifth day is not.\n\n"
          "The most useful rule of thumb: it is not about sunshine but about "
          "**instability**. A sunny day in stable air gives nothing; a day "
          "with cumulus in unstable air carries even with moderate "
          "sunshine."),
        "cirrus",
        [
            mc(t("Wann ist mit dem besten Segelflugwetter zu rechnen?",
                 "When is the best soaring weather to be expected?"),
               [t("Am Tag nach dem Durchzug einer Kaltfront.",
                  "The day after a cold front has passed."),
                t("Beim Aufziehen einer Warmfront.",
                  "As a warm front moves in."),
                t("Am fünften Tag einer Hochdrucklage.",
                  "On the fifth day of a high."),
                t("Bei Nebel am Morgen.", "With fog in the morning.")], 0,
               t("Die Rückseitenluft ist kalt, labil und trocken: hohe "
                 "Basis, kräftiges Steigen, gute Sicht. Das ist der "
                 "klassische Streckenflugtag.",
                 "The air behind is cold, unstable and dry: high base, "
                 "strong climbs, good visibility. That is the classic "
                 "cross-country day.")),
            mc(t("Ein Halo um die Sonne. Was folgt daraus für morgen?",
                 "A halo around the sun. What follows for tomorrow?"),
               [t("Eine Warmfront zieht auf; der Tag wird abschirmen.",
                  "A warm front is moving in; the day will be shaded out."),
                t("Es wird besonders gut.", "It will be especially good."),
                t("Gewittergefahr.", "Thunderstorm risk."),
                t("Nichts Bestimmtes.", "Nothing in particular.")], 0,
               t("Der Halo entsteht an Eiskristallen im Cirrostratus — der "
                 "zweiten Stufe einer aufziehenden Warmfront. Der Regen "
                 "kommt noch lange nicht, die Abschirmung aber bald.",
                 "The halo forms on ice crystals in cirrostratus — the "
                 "second stage of an approaching warm front. The rain is "
                 "still far off, but the shading is not."),
               bild="cirrus"),
        ]),
])


# ===========================================================================
# Aerodynamik und Flugmechanik
# ===========================================================================

K_AERO = kapitel(
    "aero", t("Aerodynamik und Flugmechanik",
              "Aerodynamics and flight mechanics"), 3,
    t("Warum ein Segelflugzeug fliegt, warum es überzieht, und warum die "
      "Kurve alles ändert. Das ist der Stoff, der in der Prüfung am meisten "
      "Punkte bringt und im Flug am meisten Leben rettet.",
      "Why a glider flies, why it stalls, and why a turn changes "
      "everything. This is the material that scores most in the exam and "
      "saves most lives in the air."), [

    lektion("a-polare",
        t("Die Polare", "The polar curve"),
        ["polare", "gleitzahl", "geringstes-sinken"],
        t("Die **Geschwindigkeitspolare** zeigt das Sinken über der "
          "Fluggeschwindigkeit. Aus ihr liest man zwei ganz verschiedene "
          "Punkte ab:\n\n"
          "**Geringstes Sinken** – die Geschwindigkeit, bei der man am "
          "längsten oben bleibt. Das ist die Kurbelgeschwindigkeit: im "
          "Aufwind zählt Zeit, nicht Strecke.\n\n"
          "**Bestes Gleiten** – die Geschwindigkeit, bei der man am "
          "weitesten kommt. Sie liegt **schneller** als das geringste "
          "Sinken. Grafisch: die Tangente vom Ursprung an die Polare.\n\n"
          "Zwei Dinge verschieben das:\n\n"
          "**Wasserballast** macht schwerer, also schneller — die ganze "
          "Polare verschiebt sich nach rechts. Die Gleitzahl bleibt fast "
          "gleich, aber man erreicht sie schneller. Deshalb Ballast bei "
          "starker Thermik und keiner bei schwacher.\n\n"
          "**Gegenwind** verschiebt den Tangentenpunkt zu höherer "
          "Geschwindigkeit: Gegen den Wind fliegt man schneller, mit dem "
          "Wind langsamer. Wer im Gegenwind auf bestem Gleiten bleibt, "
          "verliert Strecke.",
          "The **speed polar** plots sink against airspeed. Two quite "
          "different points are read from it.\n\n"
          "**Minimum sink** – the speed at which you stay up longest. That "
          "is the circling speed: in a thermal, time counts, not "
          "distance.\n\n"
          "**Best glide** – the speed at which you get furthest. It is "
          "**faster** than minimum sink. Graphically: the tangent from the "
          "origin to the polar.\n\n"
          "Two things shift this.\n\n"
          "**Water ballast** makes the glider heavier, hence faster — the "
          "whole polar moves right. The glide ratio stays almost the same "
          "but you reach it faster. Hence ballast in strong conditions and "
          "none in weak.\n\n"
          "**Headwind** moves the tangent point to a higher speed: into "
          "wind you fly faster, downwind slower. Staying at best glide into "
          "a headwind loses distance."),
        "",
        [
            mc(t("Du kurbelst in einem schwachen Aufwind. Welche "
                 "Geschwindigkeit?",
                 "You are circling in a weak thermal. Which speed?"),
               [t("Nahe dem geringsten Sinken.",
                  "Close to minimum sink."),
                t("Bestes Gleiten.", "Best glide."),
                t("So langsam wie möglich.", "As slow as possible."),
                t("Möglichst schnell.", "As fast as possible.")], 0,
               t("Im Aufwind geht es darum, möglichst lange zu steigen, "
                 "nicht weit zu kommen. „So langsam wie möglich\" wäre "
                 "falsch: unterhalb des geringsten Sinkens steigt das Sinken "
                 "wieder an, und die Überziehreserve schrumpft.",
                 "In a thermal the point is to climb as long as possible, "
                 "not to travel far. \"As slow as possible\" would be wrong: "
                 "below minimum sink the sink rate rises again and the "
                 "stall margin shrinks.")),
            mc(t("Du fliegst mit 25 kt Gegenwind zum Platz. Wie änderst du "
                 "gegenüber bestem Gleiten?",
                 "You are heading home into a 25 kt headwind. How do you "
                 "change from best glide?"),
               [t("Schneller fliegen.", "Fly faster."),
                t("Langsamer fliegen.", "Fly slower."),
                t("Gleich bleiben.", "Stay the same."),
                t("Das hängt nur vom Ballast ab.",
                  "That depends only on the ballast.")], 0,
               t("Gegen den Wind zählt jede Sekunde doppelt: Man verliert "
                 "über Grund, solange man in der Luft steht. Der "
                 "Tangentenpunkt wandert um etwa die Hälfte der "
                 "Windgeschwindigkeit nach rechts.",
                 "Into wind every second counts double: you lose ground "
                 "while you hang in the air. The tangent point moves right "
                 "by roughly half the wind speed.")),
            zahl(t("Gleitzahl 38, Ankunftshöhe 300 m soll übrig bleiben. Du "
                   "bist 1200 m über Platzhöhe. Wie weit darfst du dich "
                   "höchstens entfernen? (Windstille, in km)",
                   "Glide ratio 38, you want 300 m to spare on arrival. You "
                   "are 1200 m above field elevation. How far may you go at "
                   "most? (Still air, in km)"),
                 34.2, t("km", "km"),
                 t("Nutzbar sind 1200 − 300 = 900 m. 900 m × 38 = 34,2 km. "
                   "In der Praxis rechnet man mit einer schlechteren "
                   "Gleitzahl als im Prospekt: Mücken, Regen und ein "
                   "ungenaues Höhenmesserbezugsniveau kosten leicht zehn "
                   "Prozent.",
                   "Usable height is 1200 − 300 = 900 m. 900 m × 38 = "
                   "34.2 km. In practice you reckon with a worse glide ratio "
                   "than the brochure: flies, rain and an imprecise altimeter "
                   "setting easily cost ten per cent."),
                 toleranz=0.06),
        ]),

    lektion("a-ueberziehen",
        t("Überziehen und Trudeln", "Stalling and spinning"),
        ["ueberziehen", "lastvielfaches", "trudeln"],
        t("Ein Flügel trägt, solange die Strömung anliegt. Sie reißt ab, "
          "wenn der **Anstellwinkel** zu groß wird — nicht, wenn die "
          "Geschwindigkeit zu klein wird. Das ist derselbe Satz aus zwei "
          "Richtungen, aber der Unterschied rettet Leben: **man kann bei "
          "jeder Geschwindigkeit überziehen.**\n\n"
          "In der Kurve wird es kritisch. Mit der Schräglage steigt das "
          "**Lastvielfache** n, und die Überziehgeschwindigkeit steigt mit "
          "der Wurzel daraus:\n\n"
          "    30° Schräglage: n = 1,15 → + 7 %\n"
          "    45° Schräglage: n = 1,41 → + 19 %\n"
          "    60° Schräglage: n = 2,00 → + 41 %\n\n"
          "Wer eng kurbelt und dabei „ein bisschen zieht\", ist der "
          "Überziehgrenze näher, als der Fahrtmesser vermuten lässt.\n\n"
          "**Trudeln** entsteht, wenn beim Überziehen ein Flügel früher "
          "abreißt als der andere — typisch beim Ziehen im Schiebeflug, also "
          "in der überzogenen, schiebenden Kurve. Das klassische Szenario "
          "ist die **Platzrunde**: zu langsam, zu eng in den Endanflug "
          "gezogen, mit dem Seitenruder nachgeholfen. Genau daraus entsteht "
          "der Trudelunfall, aus dem in Platzrundenhöhe kein Ausleiten mehr "
          "hilft.\n\n"
          "**Ausleiten** in dieser Reihenfolge: Querruder neutral, "
          "Seitenruder **gegen** die Drehung, Knüppel nach vorn, und wenn "
          "die Drehung steht, Seitenruder neutral und sanft abfangen.",
          "A wing lifts as long as the flow stays attached. It separates "
          "when the **angle of attack** gets too large — not when the speed "
          "gets too low. That is the same statement from two directions, but "
          "the difference saves lives: **you can stall at any speed.**\n\n"
          "In a turn it gets critical. Bank raises the **load factor** n, "
          "and the stall speed rises with its square root:\n\n"
          "    30° of bank: n = 1.15 → + 7 %\n"
          "    45° of bank: n = 1.41 → + 19 %\n"
          "    60° of bank: n = 2.00 → + 41 %\n\n"
          "Circle tightly while \"pulling a little\" and you are closer to "
          "the stall than the airspeed indicator suggests.\n\n"
          "**Spinning** happens when, at the stall, one wing drops before "
          "the other — typically from pulling while slipping, that is, in a "
          "stalled, skidding turn. The classic scenario is the "
          "**circuit**: too slow, pulled too tight onto final, helped along "
          "with rudder. That is exactly how the spin accident happens, and "
          "at circuit height no recovery helps.\n\n"
          "**Recovery** in this order: ailerons neutral, rudder **against** "
          "the rotation, stick forward, and once the rotation stops, rudder "
          "neutral and pull out gently."),
        "",
        [
            mc(t("Wovon hängt es ab, ob ein Flügel die Strömung verliert?",
                 "What decides whether a wing loses its airflow?"),
               [t("Vom Anstellwinkel.", "The angle of attack."),
                t("Nur von der Geschwindigkeit.", "Only the speed."),
                t("Vom Gewicht.", "The weight."),
                t("Von der Flughöhe.", "The altitude.")], 0,
               t("Der kritische Anstellwinkel ist eine Eigenschaft des "
                 "Profils und immer derselbe — bei 60 km/h wie bei 200. "
                 "Deshalb kann man auch im Sturzflug überziehen, wenn man "
                 "hart genug zieht.",
                 "The critical angle of attack is a property of the aerofoil "
                 "and always the same — at 60 km/h as at 200. That is why "
                 "you can stall even in a dive if you pull hard enough.")),
            mc(t("Du kurbelst mit 45 Grad Schräglage. Um wie viel steigt die "
                 "Überziehgeschwindigkeit gegenüber dem Geradeausflug?",
                 "You circle at 45 degrees of bank. By how much does the "
                 "stall speed rise compared with straight flight?"),
               [t("um etwa 19 Prozent", "by about 19 per cent"),
                t("gar nicht", "not at all"),
                t("um etwa 41 Prozent", "by about 41 per cent"),
                t("um etwa 100 Prozent", "by about 100 per cent")], 0,
               t("n = 1/cos(45°) = 1,41, und die Überziehgeschwindigkeit "
                 "steigt mit der Wurzel: √1,41 ≈ 1,19. Die 41 Prozent "
                 "gehören zu 60 Grad.",
                 "n = 1/cos(45°) = 1.41, and the stall speed rises with its "
                 "square root: √1.41 ≈ 1.19. The 41 per cent belongs to 60 "
                 "degrees.")),
            mc(t("Ein Flügel kippt beim Überziehen weg und das Flugzeug geht "
                 "ins Trudeln. Was tust du zuerst?",
                 "A wing drops at the stall and the glider enters a spin. "
                 "What do you do first?"),
               [t("Querruder neutral und Seitenruder gegen die Drehung.",
                  "Ailerons neutral and rudder against the rotation."),
                t("Mit dem Querruder gegenhalten.",
                  "Pick the wing up with aileron."),
                t("Ziehen, um die Nase zu heben.",
                  "Pull, to raise the nose."),
                t("Bremsklappen ausfahren.", "Open the airbrakes.")], 0,
               t("Querruder gegen die Drehung vergrößert den Anstellwinkel "
                 "am ohnehin abgerissenen Flügel und verschlimmert alles — "
                 "der häufigste Reflex und der falscheste. Erst Seitenruder "
                 "gegen die Drehung, dann Knüppel nach vorn.",
                 "Aileron against the rotation increases the angle of attack "
                 "on the already stalled wing and makes everything worse — "
                 "the commonest reflex and the most wrong. Rudder against "
                 "the rotation first, then stick forward.")),
        ]),
])

# ===========================================================================
# Flugleistung und Flugplanung
# ===========================================================================

K_LEISTUNG = kapitel(
    "leistung", t("Flugleistung und Flugplanung",
                  "Performance and flight planning"), 4,
    t("Rechnen, bevor man fliegt: Startstrecke, Gleitwinkel, "
      "Sicherheitshöhe, Schwerpunkt. Die Zahlen sind einfach — der Fehler "
      "liegt fast immer darin, sie gar nicht gerechnet zu haben.",
      "Arithmetic before flight: take-off run, glide angle, safety height, "
      "centre of gravity. The numbers are simple — the mistake is almost "
      "always not having done them at all."), [

    lektion("l-schwerpunkt",
        t("Schwerpunkt und Beladung", "Centre of gravity and loading"),
        ["schwerpunkt", "beladung"],
        t("Jedes Segelflugzeug hat einen zugelassenen **Schwerpunktbereich**. "
          "Er steht im Flughandbuch, und er ist keine Empfehlung.\n\n"
          "**Zu weit vorn** (schwerer Pilot, kein Heckballast): Das Flugzeug "
          "ist stabil, aber schwerfällig. Es überzieht bei höherer "
          "Geschwindigkeit, das Höhenruder reicht beim Ausschweben "
          "womöglich nicht, und im Landeanflug fehlt die Wirkung.\n\n"
          "**Zu weit hinten** (leichter Pilot ohne Bugballast): Das ist die "
          "gefährliche Seite. Das Flugzeug wird instabil, reagiert "
          "überempfindlich, und beim Überziehen geht es leicht ins Trudeln — "
          "aus dem es sich unter Umständen **nicht mehr ausleiten lässt**.\n\n"
          "Deshalb steht im Cockpit die **Mindestzuladung**: Wiegt der Pilot "
          "weniger, muss Blei zugeladen werden, und zwar dort, wo es das "
          "Handbuch vorschreibt.\n\n"
          "Die Rechnung selbst ist eine Momentenbilanz: Jede Masse wird mit "
          "ihrem Hebelarm zum Bezugspunkt multipliziert, alles addiert und "
          "durch die Gesamtmasse geteilt. Das Ergebnis muss zwischen "
          "vorderer und hinterer Grenze liegen.",
          "Every glider has an approved **centre-of-gravity range**. It is "
          "in the flight manual, and it is not a recommendation.\n\n"
          "**Too far forward** (heavy pilot, no tail ballast): the glider is "
          "stable but sluggish. It stalls at a higher speed, the elevator "
          "may not suffice in the flare, and the approach lacks authority.\n\n"
          "**Too far aft** (light pilot without nose ballast): this is the "
          "dangerous side. The glider becomes unstable, over-responsive, and "
          "at the stall it readily enters a spin — from which, in some "
          "cases, **it cannot be recovered**.\n\n"
          "Hence the **minimum cockpit load** placard: a lighter pilot must "
          "carry lead, and exactly where the manual says.\n\n"
          "The calculation is a moment balance: every mass times its arm to "
          "the datum, summed, divided by the total mass. The result must lie "
          "between the forward and aft limits."),
        "",
        [
            mc(t("Ein leichter Pilot fliegt ohne die vorgeschriebene "
                 "Zuladung. Was ist die Gefahr?",
                 "A light pilot flies without the required ballast. What is "
                 "the danger?"),
               [t("Schwerpunkt zu weit hinten: instabil und im schlimmsten "
                  "Fall nicht ausleitbares Trudeln.",
                  "CG too far aft: unstable, and in the worst case a spin "
                  "that cannot be recovered."),
                t("Schwerpunkt zu weit vorn, das Flugzeug wird träge.",
                  "CG too far forward, the glider gets sluggish."),
                t("Nur die Gleitzahl leidet.",
                  "Only the glide ratio suffers."),
                t("Nichts, solange die Höchstmasse eingehalten wird.",
                  "Nothing, as long as the maximum mass is respected.")], 0,
               t("Die hintere Grenze ist die kritische. Zwischen „fliegt "
                 "spitz\" und „trudelt flach und bleibt drin\" liegen oft nur "
                 "wenige Zentimeter Schwerpunktlage.",
                 "The aft limit is the critical one. Between \"handles "
                 "sharply\" and \"spins flat and stays there\" there are "
                 "often only a few centimetres of CG travel.")),
            zahl(t("Leermasse 250 kg mit Moment 75 000 kg·mm, Pilot 70 kg "
                   "bei Hebelarm 100 mm. Wo liegt der Schwerpunkt in mm "
                   "hinter dem Bezugspunkt?",
                   "Empty mass 250 kg with a moment of 75 000 kg·mm, pilot "
                   "70 kg at an arm of 100 mm. Where is the CG, in mm aft of "
                   "the datum?"),
                 256.25, t("mm", "mm"),
                 t("(75 000 + 70 × 100) / (250 + 70) = 82 000 / 320 = "
                   "256,25 mm. Das Ergebnis muss dann gegen die Grenzen im "
                   "Handbuch geprüft werden — die Zahl allein sagt noch "
                   "nichts.",
                   "(75 000 + 70 × 100) / (250 + 70) = 82 000 / 320 = "
                   "256.25 mm. The result must then be checked against the "
                   "manual's limits — the number alone says nothing."),
                 toleranz=0.02),
        ]),

    lektion("l-startstrecke",
        t("Start, Dichtehöhe und Sicherheitshöhe",
          "Take-off, density altitude and safety height"),
        ["dichtehoehe", "startstrecke", "sicherheitshoehe"],
        t("Die **Dichtehöhe** ist die Höhe, die das Flugzeug *spürt*. Heiße "
          "Luft, hoher Platz und tiefer Luftdruck lassen die Dichte sinken — "
          "der Flügel trägt weniger, der Schlepp zieht schwächer, die "
          "Startstrecke wächst. Faustregel: **je 10 °C über Standard etwa "
          "10 Prozent mehr Startstrecke**, dazu rund 10 Prozent je 1000 ft "
          "Platzhöhe.\n\n"
          "Im Gebirge an einem heißen Nachmittag summiert sich das schnell "
          "auf das Doppelte der Handbuchzahl bei Standardbedingungen.\n\n"
          "Die **Sicherheitshöhe** ist die Höhe, unter der nur noch gelandet "
          "und nicht mehr gesucht wird. Ihre Zahl ist weniger wichtig als "
          "ihre Verbindlichkeit: Wer sie auf 300 m über Grund festlegt und "
          "dann doch „nur noch den einen Aufwind\" probiert, hat sie nicht.\n\n"
          "Beim Windenstart gibt es zusätzlich die **Entscheidungshöhe** für "
          "den Seilriss. Darunter wird geradeaus gelandet, darüber eine "
          "verkürzte Platzrunde geflogen — und welche Höhe das ist, gehört "
          "**vor** dem Start durchgesprochen, nicht währenddessen "
          "ausgerechnet.",
          "**Density altitude** is the height the aircraft *feels*. Hot air, "
          "a high field and low pressure all reduce the density — the wing "
          "lifts less, the tow pulls weaker, the take-off run grows. Rule of "
          "thumb: **about 10 per cent more take-off run per 10 °C above "
          "standard**, plus roughly 10 per cent per 1000 ft of field "
          "elevation.\n\n"
          "In the mountains on a hot afternoon that quickly adds up to twice "
          "the manual figure for standard conditions.\n\n"
          "**Safety height** is the height below which you only land and no "
          "longer search. Its exact value matters less than its being "
          "binding: set it at 300 m above ground and then try \"just this one "
          "more thermal\" and you have not set it at all.\n\n"
          "On a winch launch there is also the **decision height** for a "
          "cable break. Below it you land ahead, above it you fly an "
          "abbreviated circuit — and which height that is belongs in the "
          "briefing **before** the launch, not in a calculation during it."),
        "",
        [
            mc(t("Platz auf 1000 m Höhe, 32 °C. Wie wirkt sich das auf den "
                 "Start aus?",
                 "Field at 1000 m elevation, 32 °C. How does that affect the "
                 "take-off?"),
               [t("Die Startstrecke wird deutlich länger, das Steigen "
                  "schwächer.",
                  "The take-off run gets considerably longer and the climb "
                  "weaker."),
                t("Kein Unterschied, das Segelflugzeug ist leicht.",
                  "No difference, a glider is light."),
                t("Der Start wird kürzer, weil warme Luft besser trägt.",
                  "The run gets shorter, because warm air carries better."),
                t("Nur die Landung ist betroffen.",
                  "Only the landing is affected.")], 0,
               t("Beides wirkt in dieselbe Richtung: Höhe und Wärme senken "
                 "die Luftdichte. Rund 10 Prozent je 1000 ft und je 10 °C — "
                 "hier zusammen leicht 40 Prozent mehr Strecke als im "
                 "Handbuch.",
                 "Both act the same way: altitude and heat lower the air "
                 "density. Roughly 10 per cent per 1000 ft and per 10 °C — "
                 "here easily 40 per cent more run than the manual says.")),
            mc(t("Seilriss beim Windenstart, knapp unter der "
                 "Entscheidungshöhe. Was tust du?",
                 "Cable break on a winch launch, just below the decision "
                 "height. What do you do?"),
               [t("Nachdrücken, Fahrt aufnehmen, geradeaus landen.",
                  "Push over, get the speed back, land ahead."),
                t("Sofort die Platzrunde einleiten.",
                  "Start the circuit immediately."),
                t("Umkehrkurve zum Startpunkt.",
                  "Turn back to the launch point."),
                t("Bremsklappen sofort voll ausfahren.",
                  "Full airbrakes at once.")], 0,
               t("Das Erste ist immer **nachdrücken**: Nach dem Riss steht "
                 "die Nase hoch und die Fahrt fällt in Sekunden. Erst wenn "
                 "die Fahrt wieder stimmt, wird entschieden — und unter der "
                 "Entscheidungshöhe heißt das geradeaus.",
                 "The first action is always to **push**: after the break "
                 "the nose is high and the speed falls within seconds. Only "
                 "with the speed back is the decision made — and below the "
                 "decision height that means landing ahead.")),
        ]),
])


# ===========================================================================
# Luftrecht
# ===========================================================================

K_RECHT = kapitel(
    "recht", t("Luftrecht (EASA)", "Air law (EASA)"), 5,
    t("Lufträume, Ausweichregeln, Höhenmessereinstellung und was die Lizenz "
      "erlaubt. Trocken, aber es ist der Stoff, bei dem ein Fehler am "
      "schnellsten teuer wird.",
      "Airspaces, right of way, altimeter settings and what the licence "
      "allows. Dry, but it is the material where a mistake turns expensive "
      "fastest."), [

    lektion("r-lufträume",
        t("Lufträume", "Airspace classes"),
        ["luftraum", "freigabe"],
        t("Europa kennt die Klassen A bis G. Für den Segelflug zählen "
          "praktisch:\n\n"
          "**C** – kontrolliert, Freigabe **nötig**, auch für Sichtflug. "
          "Liegt meist als Deckel über großen Flughäfen.\n\n"
          "**D** – kontrolliert, Freigabe nötig; die klassische Kontrollzone "
          "um einen Verkehrsflughafen.\n\n"
          "**E** – kontrolliert, aber Sichtflug **ohne** Freigabe erlaubt "
          "und ohne Funkpflicht. Der Zusammenstoßschutz liegt beim Piloten. "
          "In Mitteleuropa beginnt E meist bei 2500 ft GND oder FL100.\n\n"
          "**G** – unkontrolliert. Hier spielt sich der meiste Segelflug "
          "ab.\n\n"
          "Dazu kommen **Gebiete mit Beschränkungen**: D (Gefahrengebiet), "
          "R (Beschränkungsgebiet), P (Sperrgebiet), TMZ (Transponderpflicht) "
          "und RMZ (Funkpflicht).\n\n"
          "Die Sichtflugmindestbedingungen sind das andere Bein: unterhalb "
          "FL100 in G mindestens **5 km Sicht**, frei von Wolken und mit "
          "Erdsicht; in E zusätzlich **1,5 km horizontal und 300 m vertikal** "
          "Abstand zu Wolken. Genau deshalb darf man nicht in die "
          "Wolkenbasis einsteigen, auch wenn es dort am besten steigt.",
          "Europe has classes A to G. For gliding the ones that matter are:\n\n"
          "**C** – controlled, clearance **required**, VFR included. Usually "
          "sits as a lid above major airports.\n\n"
          "**D** – controlled, clearance required; the classic control zone "
          "around an airport.\n\n"
          "**E** – controlled, but VFR is allowed **without** clearance and "
          "without a radio requirement. Collision avoidance is the pilot's "
          "own. In central Europe E usually starts at 2500 ft AGL or "
          "FL100.\n\n"
          "**G** – uncontrolled. Most gliding happens here.\n\n"
          "Then there are **areas with restrictions**: D (danger), R "
          "(restricted), P (prohibited), TMZ (transponder mandatory) and RMZ "
          "(radio mandatory).\n\n"
          "VFR minima are the other leg: below FL100 in G at least **5 km "
          "visibility**, clear of cloud and in sight of the surface; in E "
          "additionally **1.5 km horizontally and 300 m vertically** from "
          "cloud. That is precisely why you may not climb into the cloud "
          "base, however well it goes up there."),
        "cu-humilis",
        [
            mc(t("Du kurbelst in Luftraum E unter einer Wolke und steigst "
                 "weiter. Welcher Abstand zur Wolke ist einzuhalten?",
                 "You are circling in class E under a cloud and still "
                 "climbing. What separation from the cloud must you keep?"),
               [t("1,5 km horizontal, 300 m vertikal.",
                  "1.5 km horizontally, 300 m vertically."),
                t("Keiner, solange man Erdsicht hat.",
                  "None, as long as you have the surface in sight."),
                t("50 m genügen.", "50 m is enough."),
                t("Nur seitlich, nach oben egal.",
                  "Sideways only, upwards does not matter.")], 0,
               t("Das ist die Regel, an der sich jeder Segelflieger einmal "
                 "stößt: Der letzte, beste Teil des Aufwinds liegt "
                 "rechtlich außer Reichweite. Wer trotzdem einsteigt, "
                 "fliegt blind in einem Raum, in dem Instrumentenflüge "
                 "unterwegs sind.",
                 "This is the rule every glider pilot runs into once: the "
                 "last and best part of the climb is legally out of reach. "
                 "Climb in anyway and you are flying blind in airspace where "
                 "IFR traffic is about.")),
            mc(t("Was bedeutet TMZ?", "What does TMZ mean?"),
               [t("Transponderpflicht.", "Transponder mandatory zone."),
                t("Sperrgebiet.", "Prohibited area."),
                t("Zone ohne Funk.", "Radio-free zone."),
                t("Zeitlich begrenzte Militärzone.",
                  "Temporary military zone.")], 0,
               t("Transponder Mandatory Zone. Ohne eingeschalteten "
                 "Transponder mit korrektem Code ist das Durchfliegen "
                 "unzulässig — für Segelflugzeuge oft der Grund, eine "
                 "Strecke umzuplanen.",
                 "Transponder Mandatory Zone. Without a transponder switched "
                 "on and squawking correctly, transit is not permitted — "
                 "often the reason a glider task has to be replanned.")),
        ]),

    lektion("r-hoehenmesser",
        t("Höhenmesser und Ausweichregeln",
          "Altimeter settings and right of way"),
        ["qnh", "flugflaeche", "ausweichen"],
        t("**Höhenmessereinstellung** — drei Werte, drei Zwecke:\n\n"
          "**QNH**: Der Höhenmesser zeigt die Höhe über dem Meer. Das ist "
          "die Einstellung für den Streckenflug, weil Luftraumgrenzen und "
          "Geländehöhen in MSL angegeben sind.\n\n"
          "**QFE**: Null über dem Platz. Praktisch für die Platzrunde, aber "
          "unbrauchbar, sobald man den Platz verlässt.\n\n"
          "**Standard 1013,25 hPa**: Oberhalb der Übergangshöhe. Angezeigt "
          "werden dann **Flugflächen** (FL), keine Höhen. FL100 ist nicht "
          "10 000 ft über dem Meer, sondern 10 000 ft in der Standard­"
          "atmosphäre.\n\n"
          "Die Falle: Bei tiefem Luftdruck liegt die wahre Höhe **unter** "
          "der angezeigten. „From high to low, look out below.\"\n\n"
          "**Ausweichregeln**, nach Manövrierfähigkeit geordnet — wer "
          "weniger ausweichen kann, hat Vorrang:\n\n"
          "    Ballon → Segelflugzeug → Luftschiff → Motorflugzeug\n\n"
          "Dazu: Bei **Gegenkurs** weichen beide nach rechts aus. Beim "
          "**Überholen** wird rechts überholt. Am **Hang** weicht der aus, "
          "der den Hang zur Linken hat — der andere kann nicht ausweichen, "
          "ohne in den Berg zu fliegen. Beim **Kurbeln** im selben Aufwind "
          "wird in derselben Richtung gekreist wie der, der zuerst da war.",
          "**Altimeter setting** — three values, three purposes.\n\n"
          "**QNH**: the altimeter reads height above mean sea level. That is "
          "the cross-country setting, because airspace boundaries and "
          "terrain are given in MSL.\n\n"
          "**QFE**: zero over the airfield. Handy for the circuit, useless "
          "as soon as you leave it.\n\n"
          "**Standard 1013.25 hPa**: above the transition altitude. What is "
          "shown are then **flight levels**, not altitudes. FL100 is not "
          "10 000 ft above the sea but 10 000 ft in the standard "
          "atmosphere.\n\n"
          "The trap: with low pressure the true height is **below** the "
          "indicated one. \"From high to low, look out below.\"\n\n"
          "**Right of way**, ordered by manoeuvrability — whoever can "
          "manoeuvre least has priority:\n\n"
          "    balloon → glider → airship → aeroplane\n\n"
          "Also: **head-on**, both give way to the right. **Overtaking** is "
          "done on the right. On a **ridge**, the one with the slope on its "
          "left gives way — the other cannot turn away without flying into "
          "the hill. **Thermalling** in the same lift, you circle the same "
          "way as whoever was there first."),
        "",
        [
            mc(t("Du fliegst mit QNH 995 hPa, der Höhenmesser zeigt 1500 m. "
                 "Wo bist du wirklich?",
                 "You fly with QNH 995 hPa and the altimeter reads 1500 m. "
                 "Where are you really?"),
               [t("Auf 1500 m über dem Meer – QNH ist richtig eingestellt.",
                  "At 1500 m above sea level – QNH is set correctly."),
                t("Deutlich höher.", "Considerably higher."),
                t("Deutlich tiefer.", "Considerably lower."),
                t("Das lässt sich nicht sagen.",
                  "That cannot be said.")], 0,
               t("Mit korrekt eingestelltem QNH stimmt die Anzeige. Die "
                 "Falle „from high to low\" betrifft den Fall, dass man das "
                 "QNH **nicht** nachstellt und in ein Tiefdruckgebiet "
                 "einfliegt — dann ist man tiefer, als angezeigt wird.",
                 "With QNH set correctly the reading is right. The \"high to "
                 "low\" trap applies when you do **not** update the QNH and "
                 "fly into lower pressure — then you are lower than "
                 "indicated.")),
            mc(t("Du kommst an einen Hang, an dem schon ein Segelflugzeug "
                 "fliegt, den Hang zu seiner Rechten. Du fliegst ihm "
                 "entgegen. Wer weicht aus?",
                 "You arrive at a ridge where a glider is already flying "
                 "with the slope on its right. You are heading towards it. "
                 "Who gives way?"),
               [t("Du – du hast den Hang zur Linken.",
                  "You – you have the slope on your left."),
                t("Der andere, er war zuerst da.",
                  "The other one, he was there first."),
                t("Beide nach rechts.", "Both to the right."),
                t("Der Höhere weicht aus.", "The higher one gives way.")], 0,
               t("Die Regel ist geometrisch, nicht höflich: Wer den Hang "
                 "rechts hat, kann nach rechts nicht ausweichen. Also weicht "
                 "der andere aus — auch wenn er später gekommen ist.",
                 "The rule is geometric, not polite: with the slope on your "
                 "right you cannot turn right. So the other one gives way — "
                 "even if he arrived later.")),
        ]),
])


# ===========================================================================
# Navigation
# ===========================================================================

K_NAV = kapitel(
    "navigation", t("Navigation", "Navigation"), 6,
    t("Karte, Kurs, Wind und Zeit. Auch mit Satellitennavigation im Cockpit "
      "bleibt das Rechnen Prüfungsstoff — und der Tag, an dem das Gerät "
      "ausfällt, kommt.",
      "Map, track, wind and time. Even with satellite navigation in the "
      "cockpit the arithmetic stays exam material — and the day the box "
      "quits does come."), [

    lektion("n-kurse",
        t("Rechtweisend, missweisend, Steuerkurs",
          "True, magnetic and compass heading"),
        ["missweisung", "steuerkurs"],
        t("Drei Kurse, die sich um zwei Korrekturen unterscheiden:\n\n"
          "**Rechtweisend (true)** – gegenüber dem geografischen Nordpol, so "
          "wie die Karte gezeichnet ist.\n\n"
          "**Missweisend (magnetic)** – gegenüber dem magnetischen Nordpol. "
          "Der Unterschied ist die **Missweisung** (Variation), auf der "
          "Karte eingetragen. Ost wird abgezogen, West addiert: „Ost ist "
          "Mist, West ist best.\"\n\n"
          "**Steuerkurs (compass)** – was der Kompass im Flugzeug zeigt. Der "
          "Unterschied ist die **Deviation**, verursacht vom Eisen und vom "
          "Strom an Bord; sie steht auf einem Schildchen am Kompass.\n\n"
          "Dazu kommt der **Vorhaltewinkel**: Der Wind versetzt. Um über "
          "Grund die gewünschte Linie zu fliegen, muss man in den Wind "
          "hinein vorhalten. Faustformel für kleine Winkel:\n\n"
          "    Vorhaltewinkel ≈ (Querwindanteil / Eigengeschwindigkeit) × 60\n\n"
          "Bei 20 kt Querwind und 60 kt Eigengeschwindigkeit sind das rund "
          "20 Grad — kein kleiner Wert, und er ist der Grund, warum ein "
          "Segelflug bei Wind ohne Vorhalten schnell zehn Kilometer neben "
          "dem Ziel herauskommt.",
          "Three courses, differing by two corrections.\n\n"
          "**True** – relative to the geographic pole, as the chart is "
          "drawn.\n\n"
          "**Magnetic** – relative to the magnetic pole. The difference is "
          "**variation**, marked on the chart. East is subtracted, west "
          "added: \"east is least, west is best.\"\n\n"
          "**Compass** – what the instrument in the aircraft shows. The "
          "difference is **deviation**, caused by iron and current on board; "
          "it is on a card beside the compass.\n\n"
          "Then the **drift correction**: the wind pushes you sideways. To "
          "make good the intended line over the ground you must head into "
          "the wind. Rule of thumb for small angles:\n\n"
          "    drift angle ≈ (crosswind component / airspeed) × 60\n\n"
          "At 20 kt of crosswind and 60 kt airspeed that is about 20 "
          "degrees — not a small number, and the reason a glider flown "
          "without drift correction ends up ten kilometres beside the goal."),
        "",
        [
            zahl(t("Rechtweisender Kurs 120°, Missweisung 4° West. Welcher "
                   "missweisende Kurs?",
                   "True track 120°, variation 4° West. What is the magnetic "
                   "track?"),
                 124, t("Grad", "degrees"),
                 t("West wird addiert: 120 + 4 = 124. Bei Ost-Missweisung "
                   "würde man abziehen.",
                   "West is added: 120 + 4 = 124. With easterly variation "
                   "you would subtract."),
                 toleranz=0.01),
            zahl(t("Eigengeschwindigkeit 90 km/h, Querwindanteil 15 km/h. "
                   "Wie groß ist der Vorhaltewinkel etwa?",
                   "Airspeed 90 km/h, crosswind component 15 km/h. Roughly "
                   "what is the drift angle?"),
                 10, t("Grad", "degrees"),
                 t("(15 / 90) × 60 = 10 Grad. Die Formel gilt gut bis etwa "
                   "20 Grad; darüber wird sie ungenau.",
                   "(15 / 90) × 60 = 10 degrees. The formula holds well to "
                   "about 20 degrees; beyond that it loses accuracy."),
                 toleranz=0.12),
        ]),

    lektion("n-karte",
        t("Karte und Gelände", "Chart and terrain"),
        ["karte", "orientierung"],
        t("Die ICAO-Karte 1:500 000 ist das Handwerkszeug: 1 cm entspricht "
          "5 km. Wichtiger als die Rechnerei ist das **Kartenlesen im "
          "Flug** — man orientiert sich an Linien, nicht an Punkten.\n\n"
          "**Gute Marken** sind lang und eindeutig: Autobahnen, Flüsse, "
          "Bahnlinien, Seeufer, Waldkanten, Hochspannungstrassen. **Schlechte "
          "Marken** sind Dörfer — aus 1000 m sehen sie alle gleich aus.\n\n"
          "Die verlässlichste Technik ist das **Auffanglinien-Verfahren**: "
          "Man peilt nicht das Ziel an, sondern eine lange Linie dahinter "
          "(Fluss, Autobahn), und zwar bewusst schief. Trifft man die Linie, "
          "weiß man sicher, **auf welcher Seite** des Ziels man ist, und "
          "fliegt daran entlang. Wer genau anpeilt, weiß bei Abweichung "
          "nicht, ob links oder rechts.\n\n"
          "Für den Segelflug kommt die **Außenlandeplanung** dazu: Beim "
          "Kartenlesen achtet man mit auf die Felder, nicht nur auf den Kurs. "
          "Ein Feld beurteilt man nach den vier S: **Size** (groß genug), "
          "**Shape** (Anflug möglich), **Slope** (möglichst eben, notfalls "
          "bergauf landen), **Surface** (abgeerntet, kurz, keine "
          "Hochkulturen) — und Stromleitungen an den Rändern.",
          "The 1:500 000 ICAO chart is the tool: 1 cm is 5 km. More "
          "important than the arithmetic is **reading the chart in "
          "flight** — you navigate by lines, not by points.\n\n"
          "**Good features** are long and unambiguous: motorways, rivers, "
          "railways, lake shores, forest edges, power lines. **Poor "
          "features** are villages — from 1000 m they all look alike.\n\n"
          "The most reliable technique is **aiming off**: you do not steer "
          "at the goal but at a long line behind it (a river, a motorway), "
          "and deliberately to one side. When you reach the line you know "
          "for certain **which side** of the goal you are on, and follow it "
          "in. Steer exactly at the goal and a deviation leaves you not "
          "knowing whether to turn left or right.\n\n"
          "For gliding there is **field selection** on top: while reading "
          "the chart you watch the fields, not only the track. A field is "
          "judged by four S: **size** (big enough), **shape** (an approach "
          "is possible), **slope** (as level as possible, uphill if "
          "necessary), **surface** (harvested, short, no tall crops) — and "
          "the power lines along its edges."),
        "",
        [
            mc(t("Du bist unsicher, wo genau du bist, und suchst deinen "
                 "Platz. Was ist die bessere Technik?",
                 "You are unsure of your position and looking for your "
                 "field. Which is the better technique?"),
               [t("Bewusst neben das Ziel peilen und eine lange Linie "
                  "dahinter anfliegen.",
                  "Deliberately aim off and fly to a long line behind the "
                  "goal."),
                t("Genau auf den Platz zufliegen.",
                  "Fly straight at the field."),
                t("Kreisen, bis man etwas erkennt.",
                  "Circle until something is recognisable."),
                t("Dem nächsten Dorf folgen.",
                  "Follow the nearest village.")], 0,
               t("Wer genau anpeilt und danebenliegt, weiß nicht, in welche "
                 "Richtung er suchen soll. Wer bewusst daneben peilt, weiß "
                 "es immer.",
                 "Aim exactly and miss, and you do not know which way to "
                 "search. Aim off deliberately and you always do.")),
            mc(t("Welches Feld nimmst du für eine Außenlandung?",
                 "Which field do you take for an outlanding?"),
               [t("Ein großes, abgeerntetes, ebenes Feld ohne Leitungen am "
                  "Anflug.",
                  "A large, harvested, level field with no wires on the "
                  "approach."),
                t("Das nächstgelegene, egal wie.",
                  "The nearest one, whatever it is like."),
                t("Ein leuchtend grünes, weiches Feld.",
                  "A bright green, soft field."),
                t("Ein Feld mit hohem Bewuchs, das bremst.",
                  "A field with tall crops, they slow you down.")], 0,
               t("Leuchtend grün heißt meist hoher oder nasser Bewuchs — "
                 "beides bremst so abrupt, dass sich das Flugzeug überschlägt. "
                 "Die Reihenfolge ist: erst Größe und Hindernisfreiheit, dann "
                 "Oberfläche, und die Leitungen sieht man fast nie, sondern "
                 "schließt sie aus den Masten.",
                 "Bright green usually means tall or wet growth — both brake "
                 "so abruptly that the glider tips over. The order is: size "
                 "and obstacle clearance first, then surface, and the wires "
                 "are almost never visible — you infer them from the "
                 "poles.")),
        ]),
])

# ===========================================================================
# Menschliches Leistungsvermoegen
# ===========================================================================

K_MENSCH = kapitel(
    "mensch", t("Menschliches Leistungsvermögen", "Human performance"), 7,
    t("Der Pilot ist das unzuverlässigste Bauteil im Flugzeug. Dieses "
      "Kapitel handelt davon, wie er ausfällt und woran man es rechtzeitig "
      "merkt.",
      "The pilot is the least reliable component in the aircraft. This "
      "chapter is about how he fails and how to notice in time."), [

    lektion("m-koerper",
        t("Was die Höhe mit dem Körper macht",
          "What altitude does to the body"),
        ["hypoxie", "hyperventilation", "druckausgleich"],
        t("**Hypoxie** – Sauerstoffmangel. Ab etwa 3000 m spürbar, ab 4000 m "
          "gefährlich. Das Tückische ist, dass sie sich **gut** anfühlt: "
          "Euphorie, Sorglosigkeit, dann Sehstörungen und langsamere "
          "Entscheidungen — und der Betroffene hält sich die ganze Zeit für "
          "voll leistungsfähig. Deshalb gibt es feste Grenzen statt "
          "Selbsteinschätzung: über 4000 m Sauerstoff.\n\n"
          "**Hyperventilation** – zu schnelles Atmen aus Angst oder Stress. "
          "Es fehlt nicht Sauerstoff, sondern **Kohlendioxid**. Symptome: "
          "Kribbeln in Fingern und um den Mund, Schwindel, Krämpfe. Abhilfe: "
          "bewusst langsam atmen, sprechen. Die Symptome ähneln der "
          "Hypoxie — im Zweifel **zuerst Sauerstoff geben**, denn Hypoxie "
          "tötet schneller.\n\n"
          "**Druckausgleich**: Beim Sinken muss die Luft im Mittelohr "
          "nachströmen. Bei Erkältung geht das nicht, und es wird sehr "
          "schmerzhaft bis zum Trommelfellriss. Mit Schnupfen fliegt man "
          "nicht.\n\n"
          "**Räumliche Desorientierung**: Das Gleichgewichtsorgan meldet "
          "Beschleunigungen, nicht Lagen. Eine langsame, gleichmäßige Kurve "
          "fühlt sich nach kurzer Zeit wie Geradeausflug an; beim Ausleiten "
          "meint man, in die Gegenrichtung zu kurven. In Wolken oder über "
          "Wasser ohne Horizont ist das tödlich — und nach etwa 30 Sekunden "
          "unvermeidlich.",
          "**Hypoxia** – lack of oxygen. Noticeable from about 3000 m, "
          "dangerous from 4000 m. The treacherous part is that it feels "
          "**good**: euphoria, unconcern, then visual disturbance and slower "
          "decisions — while the sufferer believes himself fully capable "
          "throughout. Hence fixed limits rather than self-assessment: "
          "oxygen above 4000 m.\n\n"
          "**Hyperventilation** – breathing too fast from fear or stress. "
          "What is missing is not oxygen but **carbon dioxide**. Symptoms: "
          "tingling in the fingers and round the mouth, dizziness, cramp. "
          "Remedy: breathe slowly and deliberately, talk. The symptoms "
          "resemble hypoxia — when in doubt **give oxygen first**, because "
          "hypoxia kills faster.\n\n"
          "**Pressure equalisation**: on descent air must flow back into "
          "the middle ear. With a cold it cannot, and it becomes very "
          "painful, up to a ruptured eardrum. You do not fly with a head "
          "cold.\n\n"
          "**Spatial disorientation**: the balance organ reports "
          "accelerations, not attitudes. A slow, steady turn feels like "
          "straight flight after a short while; on rolling out you believe "
          "you are turning the other way. In cloud, or over water without a "
          "horizon, that is fatal — and after about 30 seconds it is "
          "unavoidable."),
        "",
        [
            mc(t("Warum ist Hypoxie besonders gefährlich?",
                 "Why is hypoxia especially dangerous?"),
               [t("Weil sie sich gut anfühlt und das Urteilsvermögen als "
                  "Erstes ausfällt.",
                  "Because it feels good and judgement is the first thing to "
                  "go."),
                t("Weil sie sofort bewusstlos macht.",
                  "Because it causes immediate unconsciousness."),
                t("Weil sie Schmerzen verursacht.",
                  "Because it is painful."),
                t("Weil sie erst am Boden wirkt.",
                  "Because it only takes effect on the ground.")], 0,
               t("Wer betroffen ist, merkt es gerade nicht — er fühlt sich "
                 "eher besonders gut. Deshalb helfen nur feste Regeln und "
                 "ein Blick auf den Höhenmesser, keine Selbstprüfung.",
                 "Whoever is affected is precisely the one who does not "
                 "notice — he rather feels unusually well. So only firm "
                 "rules and a look at the altimeter help, not "
                 "self-assessment.")),
            mc(t("Nach 40 Sekunden in einer Wolke meinst du, geradeaus zu "
                 "fliegen, das Variometer zeigt aber starkes Sinken. Wem "
                 "glaubst du?",
                 "After 40 seconds in cloud you believe you are flying "
                 "straight, but the variometer shows heavy sink. Which do "
                 "you believe?"),
               [t("Den Instrumenten – das Gefühl ist nach so kurzer Zeit "
                  "schon unbrauchbar.",
                  "The instruments – the seat of the pants is already "
                  "useless after that short a time."),
                t("Dem Gefühl, es ist unmittelbarer.",
                  "The feeling, it is more immediate."),
                t("Beiden gleich viel.", "Both equally."),
                t("Erst ausleiten, dann entscheiden.",
                  "Roll out first, decide afterwards.")], 0,
               t("Das Gleichgewichtsorgan gewöhnt sich an gleichförmige "
                 "Drehungen binnen Sekunden. Die Spirale, in die man dabei "
                 "gerät, fühlt sich völlig normal an — bis das Flugzeug die "
                 "zulässige Geschwindigkeit überschreitet.",
                 "The balance organ adapts to a steady rotation within "
                 "seconds. The spiral dive you end up in feels perfectly "
                 "normal — until the aircraft exceeds its limiting "
                 "speed.")),
        ]),

    lektion("m-entscheiden",
        t("Entscheiden unter Druck", "Deciding under pressure"),
        ["entscheidung", "risiko"],
        t("Die meisten Segelflugunfälle haben keine technische Ursache. Sie "
          "entstehen aus einer Kette kleiner Entscheidungen, von denen jede "
          "für sich vertretbar aussah.\n\n"
          "Die bekannteste Falle heißt **get-home-itis**: Der Wunsch "
          "anzukommen verdrängt die Einsicht, dass es nicht mehr reicht. Sie "
          "wirkt am stärksten, wenn jemand wartet, wenn der Anhänger weit "
          "weg ist, oder wenn man schon einmal knapp durchgekommen ist.\n\n"
          "Zwei Gegenmittel, beide unspektakulär:\n\n"
          "**Grenzen vorher festlegen.** Die Sicherheitshöhe, die "
          "Umkehrzeit, die Mindestankunftshöhe gehören vor dem Start "
          "bestimmt — in der Luft ist man nicht mehr derselbe "
          "Entscheider.\n\n"
          "**Die Entscheidung früh treffen.** Eine Außenlandung aus 500 m "
          "ist Routine, aus 150 m ein Notfall. Der Unterschied liegt nicht "
          "im Feld, sondern in der Zeit, die man hatte.\n\n"
          "Dazu die Merkhilfe **IMSAFE** für die Selbstprüfung vor dem "
          "Flug: Illness, Medication, Stress, Alcohol, Fatigue, Emotion. "
          "Jeder Punkt allein macht nicht flugunfähig; zwei oder drei "
          "zusammen schon.",
          "Most gliding accidents have no technical cause. They come from a "
          "chain of small decisions, each of which looked defensible on its "
          "own.\n\n"
          "The best-known trap is **get-home-itis**: the wish to arrive "
          "crowds out the recognition that it will not work. It bites "
          "hardest when someone is waiting, when the trailer is far away, or "
          "when you have scraped through once before.\n\n"
          "Two remedies, both unspectacular.\n\n"
          "**Set the limits beforehand.** The safety height, the turnaround "
          "time, the minimum arrival height belong to the pre-flight "
          "briefing — in the air you are no longer the same decision "
          "maker.\n\n"
          "**Decide early.** An outlanding from 500 m is routine; from "
          "150 m it is an emergency. The difference is not the field but the "
          "time you had.\n\n"
          "Plus the **IMSAFE** check before flight: illness, medication, "
          "stress, alcohol, fatigue, emotion. No single item grounds you; "
          "two or three together do."),
        "",
        [
            mc(t("Du bist auf 400 m über Grund, 15 km vom Platz, die "
                 "Thermik ist weg. Was ist richtig?",
                 "You are at 400 m above ground, 15 km from the field, and "
                 "the lift has gone. What is right?"),
               [t("Jetzt ein Feld wählen und die Landung planen.",
                  "Choose a field now and plan the landing."),
                t("Auf den Platz zuhalten und hoffen.",
                  "Press on towards the field and hope."),
                t("Noch einmal kurbeln, wo es zuletzt ging.",
                  "Circle once more where it last worked."),
                t("Tiefer gehen, dort ist mehr Thermik.",
                  "Go lower, there is more lift down there.")], 0,
               t("15 km aus 400 m verlangen Gleitzahl 37 ohne jede Reserve, "
                 "ohne Gegenwind und ohne Sinken dazwischen — das geht "
                 "nicht. Die Entscheidung ist längst gefallen; es geht nur "
                 "noch darum, ob man sie rechtzeitig trifft.",
                 "15 km from 400 m needs a glide ratio of 37 with no "
                 "reserve, no headwind and no sink on the way — it will not "
                 "work. The decision has long been made; the only question "
                 "is whether you make it in time.")),
            mc(t("Was beschreibt „get-home-itis\" am besten?",
                 "What describes \"get-home-itis\" best?"),
               [t("Der Wunsch anzukommen verdrängt die nüchterne "
                  "Beurteilung.",
                  "The wish to arrive displaces sober judgement."),
                t("Eine Erkrankung durch langes Sitzen.",
                  "An illness from sitting too long."),
                t("Zu frühes Aufgeben.", "Giving up too early."),
                t("Navigationsfehler nahe am Ziel.",
                  "A navigation error near the goal.")], 0,
               t("Sie wirkt genau dann am stärksten, wenn die Lage schon eng "
                 "ist — deshalb hilft nur, die Grenze vorher zu ziehen, "
                 "solange man sie noch nüchtern ziehen kann.",
                 "It bites hardest exactly when the situation is already "
                 "tight — so the only help is to draw the line beforehand, "
                 "while you can still draw it soberly.")),
        ]),
])


# ===========================================================================
# Technik und Instrumente
# ===========================================================================

K_TECHNIK = kapitel(
    "technik", t("Technik und Instrumente", "Aircraft general knowledge"), 8,
    t("Was im Flugzeug steckt und was die Instrumente wirklich messen. Wer "
      "weiß, woher eine Anzeige kommt, erkennt auch, wann sie lügt.",
      "What is in the aircraft and what the instruments actually measure. "
      "Knowing where a reading comes from is what lets you spot it "
      "lying."), [

    lektion("k-instrumente",
        t("Fahrtmesser, Höhenmesser, Variometer",
          "ASI, altimeter, variometer"),
        ["staudruck", "statik", "variometer"],
        t("Alle drei hängen an denselben zwei Drücken.\n\n"
          "**Statischer Druck** – der Umgebungsdruck, abgenommen an Öffnungen "
          "seitlich am Rumpf. **Staudruck** – der Druck, den die "
          "anströmende Luft im Pitotrohr aufbaut.\n\n"
          "**Höhenmesser**: nur statisch. Je höher, desto weniger Druck.\n\n"
          "**Fahrtmesser**: die **Differenz** von Staudruck und statischem "
          "Druck. Er zeigt die **angezeigte** Geschwindigkeit (IAS), nicht "
          "die wahre. In großer Höhe ist die wahre Geschwindigkeit höher als "
          "die angezeigte — was für die Strukturgrenzen zählt, ist aber "
          "meist die angezeigte.\n\n"
          "**Variometer**: die zeitliche Änderung des statischen Drucks. Es "
          "misst also Steigen, und zwar mit Verzögerung.\n\n"
          "**Die Verstopfungsfälle** sind beliebter Prüfungsstoff:\n\n"
          "*Pitot verstopft, Statik frei*: Der Fahrtmesser wird zum "
          "Höhenmesser verkehrt herum — im Steigflug zeigt er zu viel, im "
          "Sinkflug zu wenig.\n\n"
          "*Statik verstopft*: Der Höhenmesser bleibt stehen, das Variometer "
          "zeigt null, und der Fahrtmesser zeigt im Sinkflug zu viel, im "
          "Steigflug zu wenig.\n\n"
          "Das **TE-Variometer** (total energy) rechnet die "
          "Geschwindigkeitsänderung heraus: Ohne sie würde jedes Ziehen als "
          "Steigen erscheinen. Die TE-Düse sitzt meist am Seitenleitwerk. "
          "Ist sie verstopft, zeigt das Vario jedes Abfangen als kräftigen "
          "Aufwind — der „Knüppelthermik\" heißt.",
          "All three hang on the same two pressures.\n\n"
          "**Static pressure** – ambient pressure, taken from ports on the "
          "side of the fuselage. **Pitot pressure** – the pressure the "
          "oncoming air builds up in the pitot tube.\n\n"
          "**Altimeter**: static only. The higher, the less pressure.\n\n"
          "**Airspeed indicator**: the **difference** between pitot and "
          "static. It shows **indicated** airspeed, not true. High up the "
          "true speed is greater than the indicated one — but what the "
          "structural limits refer to is usually the indicated value.\n\n"
          "**Variometer**: the rate of change of static pressure. So it "
          "measures climb, and with a lag.\n\n"
          "**The blockage cases** are favourite exam material.\n\n"
          "*Pitot blocked, static clear*: the ASI becomes a reversed "
          "altimeter — reading high in a climb and low in a descent.\n\n"
          "*Static blocked*: the altimeter freezes, the variometer reads "
          "zero, and the ASI reads high in a descent and low in a climb.\n\n"
          "The **total energy variometer** cancels out speed changes: "
          "without it every pull-up would look like a climb. The TE probe "
          "usually sits on the fin. Blocked, the vario shows every recovery "
          "as strong lift — what pilots call \"stick thermal\"."),
        "",
        [
            mc(t("Die Statikanschlüsse sind verklebt. Was zeigt der "
                 "Höhenmesser im Sinkflug?",
                 "The static ports are taped over. What does the altimeter "
                 "show in a descent?"),
               [t("Er bleibt auf dem Wert stehen, bei dem die Verstopfung "
                  "eintrat.",
                  "It sticks at the value where the blockage occurred."),
                t("Er zeigt zu viel.", "It reads too high."),
                t("Er zeigt zu wenig.", "It reads too low."),
                t("Er fällt auf null.", "It drops to zero.")], 0,
               t("Ohne Verbindung zur Außenwelt bleibt der eingeschlossene "
                 "Druck gleich — und damit die Anzeige. Das Variometer zeigt "
                 "aus demselben Grund null.",
                 "With no connection to the outside the trapped pressure "
                 "stays constant — and so does the reading. For the same "
                 "reason the variometer shows zero.")),
            mc(t("Das Variometer schlägt jedes Mal kräftig aus, wenn du "
                 "abfängst. Was ist der Verdacht?",
                 "The variometer swings strongly every time you pull out of "
                 "a dive. What do you suspect?"),
               [t("Die TE-Düse ist verstopft oder undicht.",
                  "The TE probe is blocked or leaking."),
                t("Das ist normale Thermik.", "That is ordinary lift."),
                t("Der Höhenmesser ist falsch eingestellt.",
                  "The altimeter is set wrongly."),
                t("Der Fahrtmesser ist defekt.",
                  "The ASI is faulty.")], 0,
               t("Genau das soll die Totalenergie-Kompensation verhindern. "
                 "Zeigt das Vario „Knüppelthermik\", ist die Düse hin — und "
                 "dann führt jeder Aufwind, den man so findet, ins Leere.",
                 "That is exactly what total energy compensation is for. If "
                 "the vario shows \"stick thermal\", the probe has failed — "
                 "and every climb found that way leads nowhere.")),
        ]),
])


# ===========================================================================
# Betriebliche Verfahren und Notfaelle
# ===========================================================================

K_BETRIEB = kapitel(
    "betrieb", t("Betriebliche Verfahren und Notfälle",
                 "Operational procedures and emergencies"), 9,
    t("Start, Platzrunde, Außenlandung und die Fälle, in denen es schnell "
      "gehen muss. Hier zählt nicht Wissen, sondern eine Reihenfolge, die "
      "sitzt.",
      "Launch, circuit, outlanding and the cases where it has to be quick. "
      "What counts here is not knowledge but an order of actions that is "
      "second nature."), [

    lektion("b-seilriss",
        t("Seilriss und Startunterbrechung",
          "Cable break and aborted launch"),
        ["seilriss", "entscheidungshoehe"],
        t("Der Seilriss ist der am häufigsten geübte Notfall, weil die "
          "richtige Reaktion nicht naheliegt.\n\n"
          "**Erstens und immer: nachdrücken.** Beim Windenstart steht die "
          "Nase steil; reißt das Seil, fällt die Fahrt binnen zwei bis drei "
          "Sekunden unter die Überziehgeschwindigkeit. Der Reflex, die Nase "
          "oben zu halten, tötet.\n\n"
          "**Zweitens: Fahrt prüfen, Seil ausklinken.**\n\n"
          "**Drittens: entscheiden**, und zwar nach der Höhe:\n\n"
          "*Unter der Entscheidungshöhe* (oft 50–100 m, platzabhängig): "
          "geradeaus landen, notfalls mit kleinen Richtungsänderungen. Die "
          "Umkehrkurve aus dieser Höhe ist der klassische tödliche "
          "Fehler.\n\n"
          "*Darüber*: verkürzte Platzrunde, auf die verbleibende Höhe "
          "angepasst.\n\n"
          "Beim **Flugzeugschlepp** kommt der Fall „Schleppflugzeug hat "
          "Motorschaden\" dazu: Dann klinkt der Segelflieger **sofort** aus, "
          "damit beide handlungsfähig werden — und beide weichen "
          "voneinander weg, der Segler nach rechts.\n\n"
          "Das Abbruchzeichen des Schleppiloten (Seitenruder wedeln) heißt "
          "**sofort ausklinken**. Das Zeichen des Seglers (Schlängeln) heißt "
          "„ich kann nicht ausklinken\".",
          "The cable break is the most practised emergency because the "
          "correct response is not the obvious one.\n\n"
          "**First and always: push.** On a winch launch the nose is steep; "
          "if the cable breaks the speed falls below the stall within two or "
          "three seconds. The reflex to hold the nose up kills.\n\n"
          "**Second: check the speed, release the cable.**\n\n"
          "**Third: decide**, by height.\n\n"
          "*Below the decision height* (often 50–100 m, field dependent): "
          "land ahead, with small changes of direction if needed. Turning "
          "back from that height is the classic fatal mistake.\n\n"
          "*Above it*: an abbreviated circuit, matched to the height "
          "left.\n\n"
          "On **aerotow** there is also the case of the tug losing its "
          "engine: the glider releases **immediately** so that both are free "
          "to act — and both turn away from each other, the glider to the "
          "right.\n\n"
          "The tug pilot's abort signal (rudder waggle) means **release "
          "now**. The glider's signal (yawing from side to side) means \"I "
          "cannot release\"."),
        "",
        [
            mc(t("Seilriss in 60 m über Grund, Entscheidungshöhe ist 80 m. "
                 "Was tust du nach dem Nachdrücken?",
                 "Cable break at 60 m above ground, decision height is 80 m. "
                 "What do you do after pushing over?"),
               [t("Geradeaus landen, notfalls mit kleinen "
                  "Richtungsänderungen.",
                  "Land ahead, with small changes of direction if needed."),
                t("Umkehrkurve zur Startstelle.",
                  "Turn back to the launch point."),
                t("Volle Platzrunde.", "A full circuit."),
                t("Steigflug fortsetzen.", "Continue the climb.")], 0,
               t("Die Umkehrkurve braucht mehr Höhe, als man bei 60 m hat — "
                 "und sie wird meist zu eng und zu langsam geflogen, also "
                 "genau in die überzogene Kurve hinein. Geradeaus in ein "
                 "schlechtes Feld ist fast immer überlebbar.",
                 "The turnback needs more height than 60 m provides — and it "
                 "is usually flown too tight and too slow, straight into the "
                 "stalled turn. Ahead into a poor field is almost always "
                 "survivable.")),
            mc(t("Der Schlepppilot wedelt mit dem Seitenruder. Was heißt "
                 "das?",
                 "The tug pilot waggles his rudder. What does that mean?"),
               [t("Sofort ausklinken.", "Release immediately."),
                t("Du fliegst zu hoch.", "You are flying too high."),
                t("Bremsklappen einfahren.", "Close your airbrakes."),
                t("Alles in Ordnung.", "Everything is fine.")], 0,
               t("Das Seitenruderwedeln des Schleppflugzeugs ist das "
                 "Ausklinkzeichen. Nicht zu verwechseln mit dem "
                 "Querruderwackeln, das „Bremsklappen ausgefahren\" meldet.",
                 "The tug's rudder waggle is the release signal. Not to be "
                 "confused with the rocking of wings, which reports "
                 "\"airbrakes out\".")),
        ]),
])


# ===========================================================================
# Sprechfunk
# ===========================================================================

K_FUNK = kapitel(
    "funk", t("Sprechfunk", "Communications"), 10,
    t("Wenig Stoff, klare Regeln — und ein Notruf, der sitzen muss, weil "
      "man ihn genau einmal braucht.",
      "Not much material, clear rules — and a distress call that has to be "
      "right, because you need it exactly once."), [

    lektion("f-grundlagen",
        t("Sprechgruppen und Notruf", "Phraseology and the distress call"),
        ["funk", "notruf"],
        t("Der Aufbau jeder Meldung ist immer gleich: **wen rufe ich, wer "
          "bin ich, was will ich.**\n\n"
          "    „Innsbruck Information, OE-1234, Position …\"\n\n"
          "Zahlen werden einzeln gesprochen, die Buchstabiertafel gilt "
          "(Alfa, Bravo, Charlie …). **Ja/Nein** heißt affirm und negativ, "
          "**verstanden** heißt roger, **wiederholen Sie** heißt say again. "
          "„Roger\" bestätigt nur den Empfang, nicht die Befolgung — dafür "
          "steht **wilco**.\n\n"
          "**Die drei Dringlichkeitsstufen:**\n\n"
          "**MAYDAY** (dreimal) – Lebensgefahr. Höchste Priorität, alle "
          "anderen schweigen.\n\n"
          "**PAN PAN** (dreimal) – dringlich, aber keine unmittelbare "
          "Lebensgefahr. Zum Beispiel eine Außenlandung, die sicher "
          "durchführbar ist, über die aber jemand Bescheid wissen soll.\n\n"
          "Dazu die Frequenzen, die man auswendig kann: **121,5 MHz** ist "
          "die internationale Notfrequenz, **7700** der Transpondercode für "
          "Notlage, **7600** für Funkausfall, **7500** für unrechtmäßige "
          "Einmischung.\n\n"
          "Der Notruf selbst folgt einem Muster, das man einmal auswendig "
          "lernt und dann hat: **wer, wo, was, wie viele, was ich vorhabe.** "
          "Wer im Ernstfall nachdenken muss, funkt gar nicht.",
          "Every transmission has the same structure: **whom I am calling, "
          "who I am, what I want.**\n\n"
          "    \"Innsbruck Information, OE-1234, position …\"\n\n"
          "Numbers are spoken digit by digit and the phonetic alphabet "
          "applies (Alfa, Bravo, Charlie …). **Yes/no** are affirm and "
          "negative, **understood** is roger, **repeat** is say again. "
          "\"Roger\" only confirms reception, not compliance — that is "
          "**wilco**.\n\n"
          "**The three urgency levels:**\n\n"
          "**MAYDAY** (three times) – grave and imminent danger. Highest "
          "priority, everyone else keeps quiet.\n\n"
          "**PAN PAN** (three times) – urgent but no immediate danger to "
          "life. An outlanding that can be carried out safely but which "
          "somebody should know about, for instance.\n\n"
          "Then the frequencies worth knowing by heart: **121.5 MHz** is the "
          "international distress frequency, **7700** the transponder code "
          "for an emergency, **7600** for radio failure, **7500** for "
          "unlawful interference.\n\n"
          "The distress call follows a pattern you learn once and then have: "
          "**who, where, what, how many on board, what I intend.** Anyone "
          "who has to think about it in earnest does not transmit at all."),
        "",
        [
            mc(t("Du musst außen landen, die Lage ist beherrscht, aber "
                 "jemand soll es wissen. Welcher Anruf?",
                 "You have to land out; the situation is under control but "
                 "somebody should know. Which call?"),
               [t("PAN PAN", "PAN PAN"), t("MAYDAY", "MAYDAY"),
                t("Ein normaler Positionsbericht.",
                  "An ordinary position report."),
                t("Gar keiner.", "None at all.")], 0,
               t("MAYDAY ist der Lebensgefahr vorbehalten. Eine geplante, "
                 "beherrschte Außenlandung ist dringlich, aber nicht "
                 "lebensbedrohend — dafür gibt es PAN PAN.",
                 "MAYDAY is reserved for danger to life. A planned, "
                 "controlled outlanding is urgent but not life-threatening — "
                 "that is what PAN PAN is for.")),
            mc(t("Was bedeutet „wilco\"?", "What does \"wilco\" mean?"),
               [t("Verstanden und ich werde danach handeln.",
                  "Understood and I will comply."),
                t("Nur: verstanden.", "Merely: understood."),
                t("Wiederholen Sie.", "Say again."),
                t("Ich warte.", "Standing by.")], 0,
               t("„Roger\" bestätigt nur, dass die Meldung angekommen ist. "
                 "Wer eine Anweisung befolgen will, sagt „wilco\" — will "
                 "comply.",
                 "\"Roger\" only confirms that the message was received. To "
                 "say you will act on an instruction you say \"wilco\" — will "
                 "comply.")),
            zahl(t("Auf welcher Frequenz in MHz sendet man einen Notruf, "
                   "wenn keine andere erreichbar ist?",
                   "On which frequency in MHz do you make a distress call if "
                   "no other is available?"),
                 121.5, t("MHz", "MHz"),
                 t("121,5 MHz wird international abgehört, auch von "
                   "Verkehrsflugzeugen in der Nähe. Der zugehörige "
                   "Transpondercode ist 7700.",
                   "121.5 MHz is monitored internationally, including by "
                   "airliners nearby. The matching transponder code is "
                   "7700."),
                 toleranz=0.01),
        ]),
])


# ===========================================================================
# Kapitelplan -- die Faecher der EASA-Theorie fuer SPL und PPL
# ===========================================================================

KAPITEL = [K_WOLKEN, K_THERMIK, K_AERO, K_LEISTUNG, K_RECHT, K_NAV,
           K_MENSCH, K_TECHNIK, K_BETRIEB, K_FUNK]

# Alle geplanten Kapitel sind geschrieben.
PLAN = []

THEMEN = {
    "wolken": t("Wolken und Thermik", "Clouds and thermals"),
    "wetter": t("Wetter und Fronten", "Weather and fronts"),
    "aero": t("Aerodynamik", "Aerodynamics"),
    "leistung": t("Flugleistung", "Performance"),
    "recht": t("Luftrecht", "Air law"),
    "navigation": t("Navigation", "Navigation"),
    "mensch": t("Menschliches Leistungsvermögen", "Human performance"),
    "technik": t("Technik", "Aircraft knowledge"),
    "betrieb": t("Verfahren und Notfälle", "Procedures and emergencies"),
}


def frage(ident, stufe, thema, q, optionen, antwort, warum, bild=""):
    return {"id": ident, "stufe": stufe, "thema": thema, "q": q,
            "optionen": optionen, "antwort": antwort, "warum": warum,
            "bild": bild}


EINSTUFUNG = [
    # -- Stufe 1 -----------------------------------------------------------
    frage("e-basis", 1, "wolken",
          t("Was sagt dir die flache Unterseite einer Quellwolke?",
            "What does the flat bottom of a cumulus tell you?"),
          [t("Bis dorthin trägt der Aufwind, darüber nicht mehr.",
             "Lift goes up to there and no further."),
           t("Dort ist der stärkste Abwind.",
             "The strongest sink is there."),
           t("Sie zeigt die Windrichtung an.",
             "It shows the wind direction."),
           t("Nichts Bestimmtes.", "Nothing in particular.")], 0,
          t("Die Basis ist das Kondensationsniveau: Bis dorthin steigt der "
            "Thermikschlauch, dort wird der Wasserdampf sichtbar, und dort "
            "hört das nutzbare Steigen auf.",
            "The base is the condensation level: the thermal rises to there, "
            "the vapour becomes visible there, and that is where usable lift "
            "ends."),
          bild="cu-humilis"),
    frage("e-wind", 1, "wetter",
          t("Eine Windangabe „270/15\" bedeutet:",
            "A wind given as \"270/15\" means:"),
          [t("Wind aus 270 Grad mit 15 Knoten.",
             "Wind from 270 degrees at 15 knots."),
           t("Wind nach 270 Grad mit 15 Knoten.",
             "Wind towards 270 degrees at 15 knots."),
           t("270 Meter Höhe, 15 Grad warm.",
             "270 metres altitude, 15 degrees warm."),
           t("Windscherung von 15 Grad.",
             "Wind shear of 15 degrees.")], 0,
          t("Wind wird immer nach der Richtung benannt, **aus der** er weht, "
            "und in Knoten angegeben. 270 Grad ist West.",
            "Wind is always named by the direction it comes **from**, and "
            "given in knots. 270 degrees is west.")),

    # -- Stufe 3 -----------------------------------------------------------
    frage("e-zyklus", 3, "wolken",
          t("Zwei Wolken zur Auswahl: eine große mit dunkler Basis, eine "
            "kleine, die sichtbar wächst. Welche fliegst du an?",
            "Two clouds to choose from: a big one with a dark base, and a "
            "small one visibly growing. Which do you head for?"),
          [t("Die wachsende – sie ist bei der Ankunft reif.",
             "The growing one – it will be mature when you arrive."),
           t("Die große – dort steigt es jetzt am besten.",
             "The big one – the best lift is there now."),
           t("Die nähere von beiden.", "Whichever is closer."),
           t("Egal, das gleicht sich aus.",
             "It makes no difference.")], 0,
          t("Eine Quellwolke lebt 15 bis 20 Minuten. Entscheidend ist, wie "
            "sie bei deiner **Ankunft** aussieht, nicht jetzt.",
            "A cumulus lives 15 to 20 minutes. What matters is how it looks "
            "when you **arrive**, not now."),
          bild="cu-zyklus"),
    frage("e-spread", 3, "wetter",
          t("Am Boden 25 °C, Taupunkt 10 °C. In welcher Höhe über Grund "
            "liegt die Basis etwa?",
            "25 °C at the ground, dew point 10 °C. Roughly what height "
            "above ground is the cloud base?"),
          [t("etwa 1900 m", "about 1900 m"),
           t("etwa 600 m", "about 600 m"),
           t("etwa 3500 m", "about 3500 m"),
           t("Das lässt sich nicht abschätzen.",
             "That cannot be estimated.")], 0,
          t("Faustformel: 125 m je Grad Spreizung. 15 × 125 = 1875 m.",
            "Rule of thumb: 125 m per degree of spread. 15 × 125 = 1875 m.")),

    # -- Stufe 4 -----------------------------------------------------------
    frage("e-cb", 4, "wolken",
          t("Woran erkennst du, dass aus einer Quellwolke ein Gewitter wird?",
            "How do you recognise a cumulus turning into a thunderstorm?"),
          [t("Die Oberseite wird faserig statt knollig.",
             "The top turns fibrous instead of knobbly."),
           t("Die Wolke wird breiter als hoch.",
             "The cloud becomes wider than tall."),
           t("Die Basis steigt an.", "The base rises."),
           t("Erst am Blitz.", "Only by the lightning.")], 0,
          t("Faserig heißt vereist – ab da ist es kein Aufwind mehr, sondern "
            "ein Gewitter im Bau, mit Böenfront weit voraus.",
            "Fibrous means glaciated – from then on it is not lift but a "
            "thunderstorm under construction, with a gust front far ahead."),
          bild="cumulonimbus"),
    frage("e-ueberziehen", 4, "aero",
          t("Wovon hängt die Überziehgeschwindigkeit in der Kurve ab?",
            "What does the stall speed in a turn depend on?"),
          [t("Sie steigt mit dem Lastvielfachen, also mit der Schräglage.",
             "It rises with the load factor, that is, with the bank angle."),
           t("Sie bleibt immer gleich.", "It stays the same."),
           t("Sie sinkt in der Kurve.", "It drops in a turn."),
           t("Nur vom Gewicht.", "Only on the weight.")], 0,
          t("Mit der Wurzel aus dem Lastvielfachen: bei 60 Grad Schräglage "
            "(n = 2) ist sie rund 41 Prozent höher. Deshalb überzieht man "
            "im engen Kreisen schneller als gedacht.",
            "With the square root of the load factor: at 60 degrees of bank "
            "(n = 2) it is about 41 per cent higher. That is why tight "
            "circling stalls sooner than expected.")),

    # -- Stufe 5 -----------------------------------------------------------
    frage("e-gleitzahl", 5, "leistung",
          t("Gleitzahl 40, du bist 1000 m über Grund. Wie weit kommst du bei "
            "Windstille, ohne Sicherheitsreserve?",
            "Glide ratio 40, you are 1000 m above ground. How far do you get "
            "in still air, with no safety margin?"),
          [t("40 km", "40 km"), t("4 km", "4 km"),
           t("14 km", "14 km"), t("400 km", "400 km")], 0,
          t("Gleitzahl 40 heißt 40 m vorwärts je Meter Höhe: 1000 m × 40 = "
            "40 km. Mit Gegenwind und Reserve deutlich weniger.",
            "A glide ratio of 40 means 40 m forward per metre of height: "
            "1000 m × 40 = 40 km. Considerably less with headwind and "
            "reserve.")),
    frage("e-luftraum", 5, "recht",
          t("Luftraum C beginnt über deinem Flugplatz bei FL100. Was gilt "
            "darunter, in Luftraum E?",
            "Airspace C begins above your field at FL100. What applies "
            "below, in airspace E?"),
          [t("Sichtflug ohne Freigabe erlaubt, Funk nicht zwingend.",
             "VFR without clearance, radio not mandatory."),
           t("Freigabe der Flugsicherung nötig.",
             "ATC clearance required."),
           t("Segelflug verboten.", "Gliding prohibited."),
           t("Nur mit Transponder.", "Only with a transponder.")], 0,
          t("Luftraum E ist kontrolliert, aber Sichtflüge brauchen keine "
            "Freigabe. Der Zusammenstoßschutz liegt beim Piloten – Augen "
            "auf.",
            "Airspace E is controlled, but VFR flights need no clearance. "
            "Collision avoidance is the pilot's own job – keep a lookout.")),

    # -- Stufe 6 -----------------------------------------------------------
    frage("e-strasse", 6, "wolken",
          t("Wolkenstraßen stehen quer zu deinem Kurs. Was ist meist "
            "schneller?",
            "Cloud streets run across your track. What is usually faster?"),
          [t("Der Straße folgen und später versetzen.",
             "Follow the street and cross over later."),
           t("Auf dem kürzesten Weg direkt zum Ziel.",
             "Straight along the shortest track."),
           t("Ständig abwechseln.", "Alternate constantly."),
           t("Kein Unterschied.", "No difference.")], 0,
          t("Unter der Straße fliegst du geradeaus im Steigen; quer dazu "
            "führt jeder Übergang durch das Sinken zwischen den Walzen.",
            "Under the street you fly straight ahead climbing; across it "
            "every transition goes through the sink between the rolls."),
          bild="wolkenstrasse"),
    frage("e-kurs", 6, "navigation",
          t("Rechtweisender Kurs 090, Missweisung 3 Grad Ost. Welcher "
            "missweisende Kurs?",
            "True track 090, variation 3 degrees east. What is the magnetic "
            "track?"),
          [t("087", "087"), t("093", "093"),
           t("090", "090"), t("084", "084")], 0,
          t("Ost-Missweisung wird abgezogen, West addiert – die alte Regel "
            "„Ost ist Mist, West ist best\" bezieht sich genau darauf.",
            "Easterly variation is subtracted, westerly added – the old "
            "mnemonic \"east is least, west is best\" says exactly that.")),

    # -- Stufe 7 -----------------------------------------------------------
    frage("e-hyperventilation", 7, "mensch",
          t("Ein Flugschüler atmet nach einem Schreck schnell und flach und "
            "klagt über Kribbeln in den Fingern. Was ist das?",
            "After a fright a student breathes fast and shallow and reports "
            "tingling fingers. What is it?"),
          [t("Hyperventilation – zu viel CO₂ abgeatmet.",
             "Hyperventilation – too much CO₂ breathed off."),
           t("Sauerstoffmangel.", "Lack of oxygen."),
           t("Unterzuckerung.", "Low blood sugar."),
           t("Beginnende Luftkrankheit.", "Onset of airsickness.")], 0,
          t("Der CO₂-Mangel, nicht der Sauerstoffmangel, macht die Symptome. "
            "Abhilfe: ruhig und langsam atmen, sprechen lassen.",
            "The shortage of CO₂, not of oxygen, causes the symptoms. "
            "Remedy: breathe slowly and calmly, get them talking.")),
    frage("e-rotor", 7, "wolken",
          t("Unter einer stehenden Linsenwolke im Lee eines Bergs liegt eine "
            "zerrissene, dunkle Walze. Was ist das?",
            "Under a stationary lenticular in the lee of a ridge lies a "
            "torn, dark roll. What is it?"),
          [t("Der Rotor – schwere Turbulenz, gefährlichster Teil des "
             "Wellenflugs.",
             "The rotor – severe turbulence, the most dangerous part of wave "
             "flying."),
           t("Eine gewöhnliche Quellwolke.",
             "An ordinary cumulus."),
           t("Hangaufwind.", "Ridge lift."),
           t("Bodennebel.", "Ground fog.")], 0,
          t("Die Welle oben ist glatt und trägt hoch; der Rotor darunter hat "
            "schon Segelflugzeuge strukturell überfordert.",
            "The wave above is smooth and goes high; the rotor below has "
            "broken gliders structurally."),
          bild="lenticularis"),

    # -- Stufe 8 -----------------------------------------------------------
    frage("e-fahrtmesser", 8, "technik",
          t("Die Staudrucksonde vereist. Was zeigt der Fahrtmesser beim "
            "Sinkflug?",
            "The pitot tube ices up. What does the airspeed indicator show "
            "in a descent?"),
          [t("Er zeigt zu wenig an, weil der Staudruck eingefroren bleibt "
             "und der statische Druck steigt.",
             "Too little, because the trapped pressure stays while static "
             "pressure rises."),
           t("Er zeigt weiter richtig.", "It keeps reading correctly."),
           t("Er zeigt zu viel an.", "It reads too much."),
           t("Er fällt sofort auf null.", "It drops straight to zero.")], 0,
          t("Bei blockierter Sonde verhält sich der Fahrtmesser wie ein "
            "Höhenmesser verkehrt herum: im Sinkflug zu wenig, im Steigflug "
            "zu viel.",
            "With the pitot blocked the ASI behaves like an altimeter in "
            "reverse: too little in a descent, too much in a climb.")),
    frage("e-vorflug", 8, "leistung",
          t("Nach MacCready: Wie fliegst du zwischen zwei Aufwinden, wenn "
            "die Steigwerte hoch sind?",
            "Per MacCready: how do you fly between thermals when the climb "
            "rates are high?"),
          [t("Schneller – die verlorene Höhe ist billig zu ersetzen.",
             "Faster – the height lost is cheap to replace."),
           t("Langsamer, um Höhe zu sparen.",
             "Slower, to save height."),
           t("Immer mit bestem Gleiten.",
             "Always at best glide."),
           t("Das hängt nur vom Wind ab.",
             "That depends only on the wind.")], 0,
          t("Je stärker das erwartete Steigen, desto höher die optimale "
            "Reisegeschwindigkeit. Bei schwacher Thermik dagegen lohnt "
            "langsames, sparsames Fliegen.",
            "The stronger the expected climb, the higher the optimal "
            "cruising speed. In weak conditions slow, economical flying "
            "pays instead.")),

    # -- Stufe 9 -----------------------------------------------------------
    frage("e-aussenlandung", 9, "betrieb",
          t("Du entscheidest dich für eine Außenlandung. Wann triffst du "
            "diese Entscheidung?",
            "You decide on a field landing. When do you make that decision?"),
          [t("Früh genug, um in Ruhe ein Feld auszuwählen und eine "
             "vollständige Platzrunde zu fliegen.",
             "Early enough to choose a field calmly and fly a complete "
             "circuit."),
           t("Wenn das letzte Steigen ausbleibt.",
             "When the last climb fails to appear."),
           t("Auf 100 m über Grund.", "At 100 m above ground."),
           t("Erst wenn der Platz sicher unerreichbar ist.",
             "Only once the airfield is definitely unreachable.")], 0,
          t("Die Entscheidung gehört in eine Höhe, in der sie noch eine "
            "Entscheidung ist – üblich ist, ab etwa 300 m über Grund nur "
            "noch die Landung zu fliegen und nicht mehr zu kurbeln.",
            "The decision belongs at a height where it is still a decision – "
            "the common rule is to stop thermalling and fly the landing from "
            "about 300 m above ground.")),
    frage("e-vorfahrt", 9, "recht",
          t("Ein Segelflugzeug und ein Motorflugzeug fliegen aufeinander zu. "
            "Wer weicht aus?",
            "A glider and a powered aeroplane are converging. Who gives "
            "way?"),
          [t("Das Motorflugzeug weicht dem Segelflugzeug aus.",
             "The powered aeroplane gives way to the glider."),
           t("Das Segelflugzeug weicht aus.",
             "The glider gives way."),
           t("Beide nach rechts.", "Both to the right."),
           t("Der Langsamere weicht aus.", "The slower one gives way.")], 0,
          t("Die Rangfolge geht nach Manövrierfähigkeit: Ballon vor "
            "Segelflugzeug vor Luftschiff vor Motorflugzeug. Bei "
            "Segelflugzeugen untereinander im Hangflug weicht der aus, der "
            "den Hang zur Linken hat.",
            "The order follows manoeuvrability: balloon before glider "
            "before airship before aeroplane. Between gliders on a ridge, "
            "the one with the slope on its left gives way.")),

    # -- Stufe 10 ----------------------------------------------------------
    frage("e-castellanus", 10, "wetter",
          t("Morgens stehen Altocumulus castellanus am Himmel. Was heißt das "
            "für die Tagesplanung?",
            "Altocumulus castellanus in the morning sky. What does that mean "
            "for the day's planning?"),
          [t("Früh starten und früh zurück – gut, aber kurz.",
             "Start early and be back early – good but short."),
           t("Später Start, die Thermik braucht länger.",
             "Later start, thermals need longer."),
           t("Ein ruhiger, langer Tag.", "A calm, long day."),
           t("Keine Aussage möglich.", "No conclusion possible.")], 0,
          t("Türmchen heißen Labilität auch in der Höhe: Die Thermik setzt "
            "früher ein und wird stark, aber der Tag entwickelt ebenso früh "
            "über.",
            "Turrets mean instability aloft as well: thermals start earlier "
            "and become strong, but the day also overdevelops just as "
            "early."),
          bild="ac-castellanus"),
    frage("e-boeenfront", 10, "betrieb",
          t("15 km westlich steht ein Gewitter, über dem Platz ist es blau. "
            "Du bist im Anflug. Womit rechnest du?",
            "A thunderstorm 15 km west, blue sky over the field. You are on "
            "approach. What do you expect?"),
          [t("Böenfront: plötzlicher Windsprung und Scherung im Endteil.",
             "Gust front: sudden wind shift and shear on final."),
           t("Nichts, solange es nicht regnet.",
             "Nothing while it is not raining."),
           t("Nur etwas mehr Thermik.", "Just a little more lift."),
           t("Gleichmäßigen Rückenwind.", "Steady tailwind.")], 0,
          t("Die ausfließende Kaltluft läuft dem Gewitter bis 20 km voraus – "
            "genau in der Landephase der gefährlichste Teil.",
            "The outflowing cold air runs up to 20 km ahead of the storm – "
            "in the landing phase the most dangerous part of it."),
          bild="cumulonimbus"),
]
