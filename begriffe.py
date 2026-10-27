# -*- coding: utf-8 -*-
"""Das Glossar: jedes Fachwort der App mit Definition, Zeichnung und Verweisen.

Die Lektionen fuehren unter `begriffe` Kennungen -- bisher nur fuer den
Wiederholungsplan (Engine.cpp merkt sich je Kennung, wann sie faellig ist).
Hier bekommt jede Kennung ihre Definition, und dazu kommen die Woerter, die
in den Texten vorkommen, ohne eine eigene Lektion zu haben: Spreizung,
Durchschiessen, Luv und Lee, Vorhalt ...

Ein Eintrag:
    begriff("basis", t("Wolkenbasis", "Cloud base"),
            t("...", "..."),            # Definition, Markdown wie die Lektionen
            bild="skizze-wolkenbasis",  # Dateiname in bilder/ ohne .png, oder ""
            siehe=["spread", "kondensationsniveau"],
            formen=["Basis", "Wolkenbasis", "cloud base", "base"])

`formen` sind die Wortformen (deutsch und englisch), mit denen das Wort in
den Lektionstexten steht; tools/make-kurs.py verlinkt das erste Vorkommen
je Lektion damit auf den Eintrag. Nur ganze Woerter -- ein trennbares Verb
("schiesst ... durch") findet die Suche nicht, also stehen die Hauptwoerter.

Die Kennungen der Lektionen (kurs.py, `begriffe`) muessen hier alle
vorkommen; make-kurs.py meldet, was fehlt. Die Reihenfolge hier ist egal,
die App sortiert nach dem uebersetzten Wort.
"""
from __future__ import unicode_literals

from wolkenfotos import t


def begriff(id, wort, definition, bild="", siehe=None, formen=None):
    return {"id": id, "wort": wort, "definition": definition, "bild": bild,
            "siehe": list(siehe or []), "formen": list(formen or [])}


BEGRIFFE = [
    # -- Wolken -------------------------------------------------------------
    begriff("namen", t("Wolkennamen (Gattungen)", "Cloud names (genera)"),
            t("Die zehn **Gattungen** nach Howard: vier Grundwörter — *Cumulus* "
              "(Haufen), *Stratus* (Schicht), *Cirrus* (Haar, Eis), *Nimbus* "
              "(Regen) — und die Stockwerke *Alto-* (mittel, 2–7 km) und "
              "*Cirro-* (hoch, über 6 km). Daraus werden Cumulonimbus, "
              "Altocumulus, Cirrostratus und so fort.\n\n"
              "Für den Segelflieger zählt weniger der Name als das Stockwerk "
              "und die Form: Haufen heißt Aufwind, Schicht heißt keiner.",
              "The ten **genera** after Howard: four root words — *cumulus* "
              "(heap), *stratus* (layer), *cirrus* (hair, ice), *nimbus* "
              "(rain) — and the storeys *alto-* (middle, 2–7 km) and "
              "*cirro-* (high, above 6 km). From these come cumulonimbus, "
              "altocumulus, cirrostratus and so on.\n\n"
              "For the glider pilot the storey and the shape matter more than "
              "the name: heaps mean lift, layers mean none."),
            siehe=["systematik", "cu-humilis", "stratus", "cirrus"],
            formen=["Gattungen", "Wolkennamen", "genera", "cloud names"]),

    begriff("systematik", t("Wolkensystematik (Arten und Beinamen)",
                            "Cloud classification (species and varieties)"),
            t("Unter der Gattung steht die **Art** — bei Cumulus *humilis* "
              "(flach), *mediocris* (mittel), *congestus* (hochragend) — und "
              "der **Beiname** wie *lenticularis* (linsenförmig) oder "
              "*castellanus* (mit Türmchen). Die Art sagt, wie weit die "
              "Entwicklung schon ist; der Beiname, welcher Vorgang sie formt.",
              "Below the genus comes the **species** — for cumulus *humilis* "
              "(flat), *mediocris* (medium), *congestus* (towering) — and the "
              "**variety** such as *lenticularis* (lens-shaped) or "
              "*castellanus* (turreted). The species tells how far the "
              "development has gone; the variety, which process shapes it."),
            siehe=["namen", "cu-humilis", "congestus", "castellanus", "lenticularis"],
            formen=["Systematik", "Arten", "Beinamen", "species", "varieties"]),

    begriff("cu-humilis", t("Cumulus humilis", "Cumulus humilis"),
            t("Die flache Schönwetter-Quellwolke: breiter als hoch, scharfer "
              "Rand, flache gemeinsame Basis. Sie markiert den Kopf eines "
              "Thermikschlauchs und ist der erste Beleg, dass der Tag trägt.\n\n"
              "Steigen unter ihr: schwach bis mittel, oft 1–2 m/s. Wächst sie "
              "im Lauf des Vormittags zu *mediocris*, wird der Tag gut.",
              "The flat fair-weather cumulus: wider than tall, crisp edges, a "
              "flat common base. It marks the top of a thermal and is the "
              "first proof that the day works.\n\n"
              "Lift beneath it: weak to moderate, often 1–2 m/s. If it grows "
              "into *mediocris* during the morning, the day becomes good."),
            bild="cu-humilis",
            siehe=["cu-mediocris", "basis", "thermik"],
            formen=["Cumulus humilis", "Humilis", "humilis"]),

    begriff("cu-mediocris", t("Cumulus mediocris", "Cumulus mediocris"),
            t("Die Quellwolke in mittlerer Entwicklung: etwa so hoch wie "
              "breit, Oberseite mit deutlichen Blumenkohl-Ballen, Basis dunkel "
              "und flächig. Unter ihr steht das stärkste Steigen des "
              "Normaltags, 2–4 m/s.\n\n"
              "Sie ist die Wolke, die man anfliegt — solange sie noch wächst.",
              "The cumulus in mid development: about as tall as wide, top "
              "with clear cauliflower lumps, base dark and broad. Beneath it "
              "lies the strongest lift of a normal day, 2–4 m/s.\n\n"
              "It is the cloud you fly to — as long as it is still growing."),
            bild="begriff-cu-mediocris",
            siehe=["cu-humilis", "congestus", "zyklus"],
            formen=["Cumulus mediocris", "Mediocris", "mediocris"]),

    begriff("congestus", t("Cumulus congestus", "Cumulus congestus"),
            t("Die hochragende Quellwolke: deutlich höher als breit, Türme mit "
              "scharfen Ballen, noch ohne Eisschirm. Sie zeigt starke Thermik "
              "(4–6 m/s), aber auch, dass die Luft bis weit hinauf labil ist.\n\n"
              "Für den Tag heißt das: **Überentwicklung** droht. Wird die "
              "Oberseite faserig, ist es ein Cumulonimbus.",
              "The towering cumulus: clearly taller than wide, towers with "
              "crisp lumps, still without an ice cap. It shows strong lift "
              "(4–6 m/s) but also that the air is unstable a long way up.\n\n"
              "For the day that means **overdevelopment** is looming. Once the "
              "top turns fibrous it is a cumulonimbus."),
            bild="cu-congestus",
            siehe=["cu-mediocris", "cumulonimbus", "ueberentwicklung"],
            formen=["Cumulus congestus", "Congestus", "congestus"]),

    begriff("cumulonimbus", t("Cumulonimbus", "Cumulonimbus"),
            t("Die Gewitterwolke: Basis in 1–2 km, Oberseite bis in die "
              "Tropopause (10–12 km), oben vereist und als **Amboss** vom "
              "Höhenwind verweht. Unter und neben ihr: Böen, Hagel, Blitz, "
              "Abwinde von 10 m/s und mehr, die den Aufwind am Rand "
              "übertreffen.\n\n"
              "Abstand halten — mindestens 10 km — und nie unter die Basis "
              "oder in den Amboss. Ein Segelflugzeug hat keinen Reserve­rahmen "
              "für Hagel und Böen.",
              "The thunderstorm cloud: base at 1–2 km, top up to the "
              "tropopause (10–12 km), iced over and blown out into an "
              "**anvil** by the upper wind. Beneath and beside it: gusts, "
              "hail, lightning, downdraughts of 10 m/s and more that exceed "
              "the lift at its edge.\n\n"
              "Keep your distance — at least 10 km — and never go under the "
              "base or into the anvil. A glider has no margin for hail and "
              "gusts."),
            bild="cumulonimbus",
            siehe=["congestus", "amboss", "boeenfront", "ueberentwicklung"],
            formen=["Cumulonimbus", "Cumulonimben", "Cb", "cumulonimbus"]),

    begriff("stratocumulus", t("Stratocumulus", "Stratocumulus"),
            t("Die tiefe Ballen-Schicht: graue, zusammengewachsene Walzen "
              "oder Felder mit schmalen Lücken, Basis unter 2 km, keine "
              "Türme. Meist entsteht sie, wenn Cumuli unter einer Inversion "
              "nicht weiterkommen und sich seitlich **ausbreiten**.\n\n"
              "Sie schirmt die Sonne ab, und damit stirbt die Thermik; durch "
              "die Lücken geht oft noch etwas, aber der Tag ist zu Ende.",
              "The low lumpy layer: grey, merged rolls or fields with narrow "
              "gaps, base below 2 km, no towers. It usually forms when cumuli "
              "cannot get past an inversion and **spread out** sideways.\n\n"
              "It shades the sun, and with that the lift dies; something "
              "often still works through the gaps, but the day is over."),
            bild="stratocumulus",
            siehe=["ausbreitung", "abschirmung", "inversion"],
            formen=["Stratocumulus", "Sc", "stratocumulus"]),

    begriff("stratus", t("Stratus (Hochnebel)", "Stratus"),
            t("Die tiefe, strukturlose graue Decke — Nebel, der nicht ganz am "
              "Boden liegt. Keine Ballen, keine Sonne, oft an Hängen klebend "
              "und mit Nieseln.\n\n"
              "Kein Steigen, schlechte Sicht, Basis manchmal unter "
              "Platzrundenhöhe: nichts geht, bis er sich auflöst — ob er das "
              "tut, verrät seine Dicke (Sonne als Scheibe sichtbar: ja).",
              "The low, featureless grey blanket — fog that is not quite on "
              "the ground. No lumps, no sun, often clinging to slopes and "
              "drizzling.\n\n"
              "No lift, poor visibility, base sometimes below circuit height: "
              "nothing works until it breaks up — whether it will is told by "
              "its thickness (sun visible as a disc: yes)."),
            bild="begriff-stratus",
            siehe=["nebel", "nimbostratus"],
            formen=["Stratus", "Hochnebel", "stratus", "low stratus"]),

    begriff("nimbostratus", t("Nimbostratus", "Nimbostratus"),
            t("Die dunkle, dicke Regenschicht ohne Form, aus der es anhaltend "
              "regnet oder schneit; Basis tief und zerfasert, oft mit Fetzen "
              "darunter. Das Ende der Warmfront-Abfolge.\n\n"
              "Dauerregen, tiefe Basis, schlechte Sicht: für Stunden nichts. "
              "Das Flugzeug bleibt in der Halle.",
              "The dark, thick, shapeless rain layer with steady rain or snow "
              "falling from it; base low and ragged, often with shreds "
              "beneath. The end of the warm-front sequence.\n\n"
              "Steady rain, low base, poor visibility: nothing for hours. The "
              "glider stays in the hangar."),
            bild="begriff-nimbostratus",
            siehe=["warmfront", "altostratus", "stratus"],
            formen=["Nimbostratus", "Ns", "nimbostratus"]),

    begriff("altocumulus", t("Altocumulus", "Altocumulus"),
            t("Die Ballenwolke des mittleren Stockwerks (2–7 km): weiße oder "
              "graue Flocken und Walzen mit Eigenschatten, in Feldern, oft als "
              "**Schäfchenwolken** bezeichnet. Größer als Cirrocumulus, höher "
              "als Stratocumulus.\n\n"
              "Sie sagt, dass in der Höhe Feuchte und leichte Labilität "
              "sitzen. Als dünnes Feld harmlos; verdichtet sie sich von Westen "
              "her, kommt oft eine Front.",
              "The lumpy cloud of the middle storey (2–7 km): white or grey "
              "flakes and rolls with shading, in patches, often called a "
              "**mackerel sky**. Larger than cirrocumulus, higher than "
              "stratocumulus.\n\n"
              "It says that moisture and slight instability sit aloft. As a "
              "thin patch harmless; if it thickens from the west, a front is "
              "often on its way."),
            bild="begriff-altocumulus",
            siehe=["castellanus", "lenticularis", "cirrocumulus", "stratocumulus"],
            formen=["Altocumulus", "Ac", "Schäfchenwolken", "altocumulus"]),

    begriff("castellanus", t("Altocumulus castellanus", "Altocumulus castellanus"),
            t("Altocumulus mit **Türmchen**, die aus einer gemeinsamen Basis "
              "in einer Reihe aufsteigen, wie Zinnen. Er zeigt, dass die Luft "
              "in mittlerer Höhe labil ist — nicht nur am Boden.\n\n"
              "Am Morgen gesehen heißt er: Heute wird es gewittrig. Der "
              "Nachmittag bringt Cumulonimben, auch wenn der Vormittag gut "
              "aussieht.",
              "Altocumulus with **turrets** rising from a common base in a "
              "row, like battlements. It shows that the air is unstable at "
              "mid level — not only near the ground.\n\n"
              "Seen in the morning it means: today will turn thundery. The "
              "afternoon brings cumulonimbus even if the morning looks good."),
            bild="ac-castellanus",
            siehe=["altocumulus", "labilitaet", "cumulonimbus"],
            formen=["Castellanus", "Altocumulus castellanus", "castellanus"]),

    begriff("lenticularis", t("Lenticularis (Linsenwolke)", "Lenticularis (lens cloud)"),
            t("Die linsen- oder mandelförmige Wolke mit glatten Rändern, die "
              "**ortsfest** über dem Gebirge steht, obwohl starker Wind weht: "
              "Die Luft strömt hindurch, kondensiert im Wellenberg und löst "
              "sich im Tal wieder auf.\n\n"
              "Sie zeigt die **Leewelle** an: ortsfestes Steigen vor (luvseitig) "
              "der Linse, oft 3–8 m/s bis in große Höhe — dazu Rotoren "
              "darunter, die ernst zu nehmen sind.",
              "The lens- or almond-shaped cloud with smooth edges that stands "
              "**still** over the mountains despite a strong wind: the air "
              "flows through it, condensing in the wave crest and clearing "
              "again in the trough.\n\n"
              "It marks the **lee wave**: steady lift upwind of the lens, "
              "often 3–8 m/s up to great height — with rotors beneath that "
              "must be taken seriously."),
            bild="lenticularis",
            siehe=["welle", "rotor", "foehn"],
            formen=["Lenticularis", "Linsenwolke", "Linsen", "lenticularis", "lens cloud", "lenses"]),

    begriff("cirrus", t("Cirrus", "Cirrus"),
            t("Die hohe Eiswolke (über 6 km): weiße Fasern, Haken, Federn, "
              "ohne Schatten, die Sonne scheint hindurch. Ein paar Haken sind "
              "harmlos.\n\n"
              "**Haken, die dichter werden** und von Westen her zu einem "
              "Schleier zusammenwachsen, sind der erste Bote einer Warmfront — "
              "innerhalb von 12 bis 24 Stunden ändert sich das Wetter, und "
              "schon am Nachmittag dämpft der Schleier die Thermik.",
              "The high ice cloud (above 6 km): white fibres, hooks, feathers, "
              "without shadow, the sun shining through. A few hooks are "
              "harmless.\n\n"
              "**Hooks thickening** and merging into a veil from the west are "
              "the first messenger of a warm front — the weather changes "
              "within 12 to 24 hours, and the veil already damps the lift in "
              "the afternoon."),
            bild="cirrus",
            siehe=["cirrostratus", "warmfront", "abschirmung", "kondensstreifen"],
            formen=["Cirrus", "Cirren", "Ci", "Cirrus-Haken", "cirrus", "cirrus hooks"]),

    begriff("cirrostratus", t("Cirrostratus", "Cirrostratus"),
            t("Der hohe, dünne Eisschleier, der den ganzen Himmel milchig "
              "macht; die Sonne bleibt sichtbar und bekommt einen **Halo**. "
              "Er folgt auf die Cirrushaken und geht dem Altostratus voraus.\n\n"
              "Die Einstrahlung sinkt um ein Drittel und mehr: Die Thermik "
              "wird weich, die Basis bleibt tief. Die Front ist ein halber Tag "
              "entfernt.",
              "The high, thin ice veil that turns the whole sky milky; the "
              "sun stays visible and gets a **halo**. It follows the cirrus "
              "hooks and precedes the altostratus.\n\n"
              "Insolation drops by a third and more: the lift turns soft, the "
              "base stays low. The front is half a day away."),
            bild="begriff-cirrostratus",
            siehe=["cirrus", "halo", "altostratus", "abschirmung"],
            formen=["Cirrostratus", "Cs", "Cirrostratus-Schleier", "cirrostratus", "cirrostratus veil"]),

    begriff("cirrocumulus", t("Cirrocumulus", "Cirrocumulus"),
            t("Sehr kleine weiße Körnchen oder Rippel hoch oben, ohne "
              "Schatten, oft in Feldern — viel feiner als Altocumulus. Er "
              "zeigt feuchte, labile Höhenluft.\n\n"
              "Meist ein Vorbote: Innerhalb eines Tages kommt die Front. Heute "
              "meist noch fliegbar, morgen eher nicht.",
              "Very small white grains or ripples high up, without shading, "
              "often in patches — much finer than altocumulus. It shows "
              "moist, unstable air aloft.\n\n"
              "Usually a harbinger: the front arrives within a day. Today "
              "mostly still flyable, tomorrow probably not."),
            bild="begriff-cirrocumulus",
            siehe=["altocumulus", "cirrus", "warmfront"],
            formen=["Cirrocumulus", "Cc", "cirrocumulus"]),

    begriff("altostratus", t("Altostratus", "Altostratus"),
            t("Die graue bis bläuliche Schicht in mittlerer Höhe, die den "
              "Himmel weitgehend bedeckt; die Sonne scheint wie durch "
              "**Milchglas**, ohne Halo, und wirft keinen Schatten mehr.\n\n"
              "Die Warmfront ist da: Die Decke dickt von Westen her ein, die "
              "Thermik ist weg, als Nächstes kommt Regen.",
              "The grey to bluish sheet at mid level covering most of the "
              "sky; the sun shows as if through **frosted glass**, without a "
              "halo, and no longer casts a shadow.\n\n"
              "The warm front has arrived: the sheet thickens from the west, "
              "the lift is gone, rain comes next."),
            bild="begriff-altostratus",
            siehe=["cirrostratus", "nimbostratus", "warmfront"],
            formen=["Altostratus", "As", "altostratus"]),

    begriff("kondensstreifen", t("Kondensstreifen", "Contrails"),
            t("Gerade weiße Linien hoch am Himmel, hinter Flugzeugen "
              "entstanden. Lösen sie sich sofort auf, ist die Höhe trocken — "
              "gut. Bleiben sie, werden breiter und fasern zu Cirrus aus, ist "
              "die Höhe feucht.\n\n"
              "Bleibende Streifen wachsen im Lauf des Tages zu einem Schleier, "
              "der die Thermik dämpft, und oft kündigen sie eine Front an.",
              "Straight white lines high in the sky, left by aircraft. If "
              "they dissolve at once the upper air is dry — good. If they "
              "persist, widen and fray into cirrus, the upper air is moist.\n\n"
              "Persistent trails grow into a veil during the day that damps "
              "the lift, and often they announce a front."),
            bild="begriff-kondensstreifen",
            siehe=["cirrus", "cirrostratus"],
            formen=["Kondensstreifen", "contrails", "contrail"]),

    begriff("wolkenstrasse", t("Wolkenstraße", "Cloud street"),
            t("Cumuli in **Reihen** längs des Windes, mit wolkenfreien Gassen "
              "dazwischen. Sie entstehen, wenn der Wind in der Thermikschicht "
              "gleichmäßig und mäßig stark ist und die Schicht eine Inversion "
              "deckelt: Die Thermik ordnet sich in Walzen.\n\n"
              "Unter der Reihe steigt es fast durchgehend — Strecke geradeaus "
              "ohne Kurbeln, mit 100 km/h und mehr über Grund. Die Gassen "
              "daneben sinken; nicht querab fliegen.",
              "Cumuli in **rows** along the wind, with cloud-free lanes between "
              "them. They form when the wind in the convective layer is "
              "steady and moderate and an inversion caps the layer: the "
              "thermals line up into rolls.\n\n"
              "Beneath the row the lift is nearly continuous — straight-line "
              "cross-country without circling, at 100 km/h and more over the "
              "ground. The lanes beside it sink; do not fly across."),
            bild="wolkenstrasse",
            siehe=["inversion", "thermik", "cu-humilis"],
            formen=["Wolkenstraße", "Wolkenstraßen", "Reihe", "cloud street", "cloud streets"]),

    begriff("zyklus", t("Lebenslauf einer Quellwolke", "Life cycle of a cumulus"),
            t("Eine Quellwolke lebt etwa **15 bis 20 Minuten**: wachsend "
              "(klein, scharf, quillt), reif (am größten, Basis am dunkelsten, "
              "stärkstes Steigen — aber fast vorbei), zerfallend (Ränder "
              "fransen, durchsichtig, darunter sinkt es).\n\n"
              "Regel: Nicht die größte Wolke anfliegen, sondern die, die "
              "gerade wächst — bis man dort ist, ist sie reif.",
              "A cumulus lives about **15 to 20 minutes**: growing (small, "
              "crisp, bulging), mature (largest, base darkest, strongest lift "
              "— but nearly over), decaying (edges fraying, translucent, "
              "sink beneath).\n\n"
              "Rule: do not fly to the biggest cloud but to the one that is "
              "growing — by the time you arrive it is mature."),
            bild="cu-zyklus",
            siehe=["anflug", "cu-mediocris", "thermik"],
            formen=["Lebenslauf", "Zyklus", "life cycle"]),

    begriff("anflug", t("Anflug einer Wolke", "Approaching a cloud"),
            t("Der Aufwind steht **nicht unter der Wolke**, sondern schräg "
              "davor: Der Wind versetzt die Wolke gegenüber ihrer Quelle am "
              "Boden. Gesucht wird der Schlauch auf der **Luvseite**, und "
              "zwar bei der Wolke, die noch wächst.\n\n"
              "Unterwegs die Fahrt nach McCready wählen und an der dunkelsten, "
              "flachsten Stelle der Basis mit dem Kurbeln beginnen.",
              "The lift is **not under the cloud** but ahead of it at an "
              "angle: the wind displaces the cloud from its source on the "
              "ground. Look for the thermal on the **upwind side**, and at the "
              "cloud that is still growing.\n\n"
              "On the way choose the speed by MacCready and start circling at "
              "the darkest, flattest part of the base."),
            bild="begriff-anflug",
            siehe=["zyklus", "luv-lee", "thermikschlauch", "mccready"],
            formen=["Anflug", "anfliegen", "approach"]),

    # -- Thermik und Schichtung ------------------------------------------------
    begriff("thermik", t("Thermik", "Thermals"),
            t("Aufsteigende Warmluftblasen oder -schläuche über Boden, den die "
              "Sonne stärker erwärmt hat als die Umgebung: dunkle Äcker, "
              "Südhänge, Städte. Die Luft steigt, solange sie wärmer ist als "
              "die Umgebung — bis zur Inversion oder bis sie kondensiert und "
              "eine Quellwolke bildet.\n\n"
              "Typische Stärke in Mitteleuropa 1–4 m/s, im Sommer bis 2 km "
              "Basis. Sie ist der Motor des Segelflugs.",
              "Rising bubbles or columns of warm air over ground the sun has "
              "heated more than its surroundings: dark fields, south-facing "
              "slopes, towns. The air rises as long as it is warmer than its "
              "surroundings — up to the inversion or until it condenses and "
              "forms a cumulus.\n\n"
              "Typical strength in central Europe 1–4 m/s, base up to 2 km in "
              "summer. It is the engine of soaring."),
            bild="begriff-ausloesung",
            siehe=["ausloesung", "thermikschlauch", "labilitaet", "inversion", "tagesgang"],
            formen=["Thermik", "thermals", "thermal"]),

    begriff("thermikschlauch", t("Thermikschlauch (Bart)", "Thermal core"),
            t("Der zusammenhängende Aufwindschlauch zwischen Auslösestelle am "
              "Boden und Wolke, im Flieger­deutsch der **Bart**. Durchmesser "
              "einige hundert Meter, im Kern am stärksten, am Rand von "
              "Abwind gesäumt.\n\n"
              "Der Wind neigt ihn: Die Wolke steht im Lee ihrer Quelle, also "
              "unter der Wolke luvseitig suchen. Im Schlauch wird gekurbelt — "
              "eng, wenn er eng ist.",
              "The continuous column of lift between the trigger point on the "
              "ground and the cloud — in pilots' slang the **core**. A few "
              "hundred metres across, strongest in the centre, fringed by "
              "sink at the edge.\n\n"
              "The wind tilts it: the cloud stands downwind of its source, so "
              "search upwind beneath the cloud. In the core you circle — "
              "tightly if it is narrow."),
            bild="begriff-thermikschlauch",
            siehe=["thermik", "kurbeln", "anflug", "abwind"],
            formen=["Thermikschlauch", "Bart", "Schlauch", "thermal core", "core"]),

    begriff("ausloesung", t("Auslösung", "Triggering"),
            t("Der Moment, in dem eine Warmluftblase sich vom Boden löst. Sie "
              "braucht einen **Auslöser**: eine Kante im Gelände, einen "
              "Windstoß, eine Erntemaschine, einen Waldrand. Die "
              "**Auslösetemperatur** ist die Bodentemperatur, ab der die "
              "Blasen bis zur Kondensation steigen können — sie wird aus dem "
              "Temperaturprofil des Morgens gerechnet.\n\n"
              "Ist sie erreicht, geht der Tag los; typischerweise zwei bis vier "
              "Stunden nach Sonnenaufgang.",
              "The moment a bubble of warm air detaches from the ground. It "
              "needs a **trigger**: an edge in the terrain, a gust, a "
              "harvester, a forest edge. The **trigger temperature** is the "
              "ground temperature from which bubbles can rise to "
              "condensation — it is calculated from the morning sounding.\n\n"
              "Once reached, the day starts; typically two to four hours "
              "after sunrise."),
            bild="begriff-ausloesung",
            siehe=["thermik", "inversion", "tagesgang"],
            formen=["Auslösung", "Auslösetemperatur", "Auslöser", "triggering", "trigger temperature", "triggers"]),

    begriff("inversion", t("Inversion", "Inversion"),
            t("Eine Schicht, in der die Temperatur mit der Höhe **zunimmt** "
              "statt abzunehmen. Darunter ist die Luft gefangen — Dunst, "
              "Rauch und Thermik enden an ihr wie an einer Decke.\n\n"
              "Die **Bodeninversion** der Nacht muss die Sonne erst wegheizen, "
              "bevor die Thermik beginnt; die **Absinkinversion** eines Hochs "
              "deckelt den Tag auf 1 500 m und verwandelt Cumuli in "
              "Stratocumulus.",
              "A layer in which the temperature **rises** with height instead "
              "of falling. Beneath it the air is trapped — haze, smoke and "
              "thermals stop at it as at a ceiling.\n\n"
              "The night's **surface inversion** must be burnt off by the sun "
              "before the lift starts; the **subsidence inversion** of a high "
              "caps the day at 1,500 m and turns cumuli into stratocumulus."),
            bild="begriff-inversion",
            siehe=["labilitaet", "hochdruck", "ausbreitung", "durchschiessen"],
            formen=["Inversion", "Bodeninversion", "Absinkinversion", "inversion", "subsidence inversion"]),

    begriff("labilitaet", t("Labilität", "Instability"),
            t("Die Luft ist **labil**, wenn ein angehobenes Luftpaket wärmer "
              "bleibt als seine Umgebung und darum weitersteigt — die "
              "Temperatur der Umgebung nimmt dann schneller mit der Höhe ab "
              "als die des Pakets (trocken etwa 1 °C je 100 m, in der Wolke "
              "etwa 0,6 °C). **Stabil** ist sie, wenn das Paket kälter wird "
              "als die Umgebung und zurücksinkt.\n\n"
              "Labilität am Boden macht Thermik; Labilität in der Höhe macht "
              "Türme, Castellanus und Gewitter.",
              "The air is **unstable** when a lifted parcel stays warmer than "
              "its surroundings and therefore keeps rising — the environment "
              "then cools faster with height than the parcel does (dry about "
              "1 °C per 100 m, inside cloud about 0.6 °C). It is **stable** "
              "when the parcel becomes colder than its surroundings and sinks "
              "back.\n\n"
              "Instability near the ground makes thermals; instability aloft "
              "makes towers, castellanus and thunderstorms."),
            bild="begriff-labilitaet",
            siehe=["inversion", "castellanus", "ueberentwicklung", "thermik"],
            formen=["Labilität", "labil", "Stabilität", "stabil", "instability", "unstable", "stable"]),

    begriff("spread", t("Spreizung", "Spread"),
            t("Der Abstand zwischen **Temperatur und Taupunkt** am Boden, in "
              "Grad. Je größer die Spreizung, desto trockener die Luft und "
              "desto höher muss ein Luftpaket steigen, bis es kondensiert.\n\n"
              "Faustformel für die Basis: **Spreizung × 125 m**. Bei 20 °C "
              "und 8 °C Taupunkt (12 K) liegt die Basis etwa 1 500 m über "
              "Grund. Über 15 K Spreizung bleibt der Himmel oft blau.",
              "The gap between **temperature and dew point** at the ground, in "
              "degrees. The larger the spread, the drier the air and the "
              "higher a parcel must rise before it condenses.\n\n"
              "Rule of thumb for the base: **spread × 125 m** (about 400 ft "
              "per °C). At 20 °C and a dew point of 8 °C (12 K) the base is "
              "roughly 1,500 m above ground. Above 15 K of spread the sky "
              "often stays blue."),
            bild="begriff-spread",
            siehe=["basis", "taupunkt", "kondensationsniveau", "blauthermik"],
            formen=["Spreizung", "spread"]),

    begriff("taupunkt", t("Taupunkt", "Dew point"),
            t("Die Temperatur, auf die Luft abgekühlt werden muss, damit ihr "
              "Wasserdampf zu kondensieren beginnt. Er ist ein Maß für die "
              "absolute Feuchte: hoher Taupunkt, viel Wasser in der Luft.\n\n"
              "Taupunkt und Temperatur zusammen geben die Spreizung — und damit "
              "die Wolkenbasis.",
              "The temperature to which air must be cooled for its water "
              "vapour to start condensing. It measures the absolute humidity: "
              "a high dew point, much water in the air.\n\n"
              "Dew point and temperature together give the spread — and with "
              "it the cloud base."),
            bild="begriff-taupunkt",
            siehe=["spread", "basis"],
            formen=["Taupunkt", "dew point"]),

    begriff("basis", t("Wolkenbasis", "Cloud base"),
            t("Die Unterseite der Quellwolken — die Höhe, in der die "
              "aufsteigende Luft ihren Taupunkt erreicht und kondensiert "
              "(Kondensationsniveau). Darum liegen alle Basen eines Tages auf "
              "**derselben Höhe**, und darum steigt sie im Lauf des Tages mit "
              "der Spreizung.\n\n"
              "Für den Piloten ist sie die Arbeitshöhe: Bis dorthin trägt es, "
              "darüber nicht. Eine flache, dunkle Basis heißt kräftiges "
              "Steigen; eine zerfaserte, dass die Wolke stirbt.",
              "The underside of the cumuli — the height at which rising air "
              "reaches its dew point and condenses (condensation level). That "
              "is why every base of a day sits at **the same height**, and why "
              "it rises with the spread during the day.\n\n"
              "For the pilot it is the working height: lift up to there, none "
              "above. A flat, dark base means strong lift; a ragged one, that "
              "the cloud is dying."),
            bild="begriff-basis",
            siehe=["spread", "kondensationsniveau", "cu-humilis", "taupunkt"],
            formen=["Wolkenbasis", "Basis", "Basishöhe", "Basen", "cloud base", "base", "bases"]),

    begriff("kondensationsniveau", t("Kondensationsniveau", "Condensation level"),
            t("Die Höhe, in der ein vom Boden aufsteigendes Luftpaket so weit "
              "abgekühlt ist (etwa 1 °C je 100 m), dass es seinen Taupunkt "
              "erreicht — dort beginnt die Wolke. Für Thermik ist es das "
              "**Cumulus-Kondensationsniveau**, gerechnet aus Temperatur und "
              "Taupunkt des Nachmittags.\n\n"
              "In der Praxis: Spreizung × 125 m über Grund.",
              "The height at which a parcel rising from the ground has cooled "
              "(about 1 °C per 100 m) to its dew point — there the cloud "
              "begins. For thermals it is the **cumulus condensation level**, "
              "worked out from the afternoon's temperature and dew point.\n\n"
              "In practice: spread × 125 m above ground."),
            bild="begriff-kondensationsniveau",
            siehe=["basis", "spread", "taupunkt"],
            formen=["Kondensationsniveau", "condensation level"]),

    begriff("durchschiessen", t("Durchschießen", "Shooting through"),
            t("Eine Quellwolke **schießt durch**, wenn ihr Aufwind die "
              "deckelnde Inversion durchbricht und der Turm weiterwächst, "
              "statt sich seitlich auszubreiten. Die Luft darüber ist dann "
              "ebenfalls labil, und aus Cumulus wird Congestus, aus Congestus "
              "Cumulonimbus.\n\n"
              "Das Zeichen: Türme, die höher als breit werden und oben scharf "
              "bleiben. Dann heißt es **Überentwicklung** — früh starten, "
              "mittags Abstand, nachmittags Vorsicht.",
              "A cumulus **shoots through** when its updraught breaks the "
              "capping inversion and the tower keeps growing instead of "
              "spreading out sideways. The air above is then unstable too, and "
              "cumulus becomes congestus, congestus becomes cumulonimbus.\n\n"
              "The sign: towers growing taller than wide and staying crisp on "
              "top. That means **overdevelopment** — launch early, keep away "
              "at noon, take care in the afternoon."),
            bild="begriff-durchschiessen",
            siehe=["inversion", "ueberentwicklung", "congestus", "labilitaet"],
            formen=["Durchschießen", "durchschießt", "schießt durch", "shooting through", "shoots through"]),

    begriff("ueberentwicklung", t("Überentwicklung", "Overdevelopment"),
            t("Der Tag, an dem die Quellwolken zu groß werden: Schon am "
              "Vormittag Congestus, mittags Türme, nachmittags Schauer und "
              "Gewitter, dazwischen breite Abschattung, in der die Thermik "
              "erstirbt.\n\n"
              "Zu erkennen am Morgen an Castellanus, an feuchter Luft (kleine "
              "Spreizung) und an Cumuli, die um 10 Uhr schon höher als breit "
              "sind. Fliegen: früh und kurz, Wendepunkte nach Hause legen.",
              "The day on which the cumuli grow too big: congestus already in "
              "the morning, towers at noon, showers and thunderstorms in the "
              "afternoon, between them broad shading in which the lift dies.\n\n"
              "Recognised in the morning by castellanus, by moist air (small "
              "spread) and by cumuli that are taller than wide by 10 o'clock. "
              "Flying: early and short, turn points towards home."),
            bild="begriff-ueberentwicklung",
            siehe=["durchschiessen", "congestus", "cumulonimbus", "castellanus"],
            formen=["Überentwicklung", "overdevelopment"]),

    begriff("ausbreitung", t("Ausbreitung", "Spreading out"),
            t("Quellwolken, die an einer Inversion nicht weiterkommen, "
              "breiten sich seitlich aus und wachsen zu einer Decke aus "
              "Stratocumulus zusammen — das **Zumachen**. Je feuchter die "
              "Luft unter der Inversion, desto schneller.\n\n"
              "Die Decke schirmt die Sonne ab, die Thermik stirbt oft schon "
              "um 14 Uhr. Am Morgen zu ahnen an einer tiefen Inversion mit "
              "feuchter Luft darunter.",
              "Cumuli that cannot get past an inversion spread out sideways "
              "and merge into a sheet of stratocumulus — the sky **closing "
              "in**. The moister the air below the inversion, the faster.\n\n"
              "The sheet shades the sun; the lift often dies by 14:00. Hinted "
              "at in the morning by a low inversion with moist air beneath."),
            bild="begriff-ausbreitung",
            siehe=["stratocumulus", "inversion", "abschirmung"],
            formen=["Ausbreitung", "Zumachen", "ausbreiten", "spreading out", "closing in"]),

    begriff("abschirmung", t("Abschirmung", "Shading"),
            t("Alles, was sich zwischen Sonne und Boden schiebt, nimmt der "
              "Thermik den Antrieb: ein Cirrostratus-Schleier von Westen, eine "
              "Stratocumulus-Decke aus Ausbreitung, der Amboss eines "
              "Gewitters. Schon ein dünner Schleier senkt die Einstrahlung um "
              "ein Drittel.\n\n"
              "Erkennbar als **weißer Saum im Westen, der bleibt**: Dann endet "
              "der Tag Stunden früher als die Basis verspricht.",
              "Anything that slides between sun and ground takes away the "
              "thermals' drive: a cirrostratus veil from the west, a "
              "stratocumulus sheet from spreading out, a thunderstorm's anvil. "
              "Even a thin veil cuts the insolation by a third.\n\n"
              "Recognisable as **a white fringe in the west that stays**: then "
              "the day ends hours earlier than the base promises."),
            bild="begriff-abschirmung",
            siehe=["cirrostratus", "ausbreitung", "stratocumulus", "amboss"],
            formen=["Abschirmung", "abschirmen", "schirmt ab", "shading", "shades"]),

    begriff("blauthermik", t("Blauthermik", "Blue thermals"),
            t("Thermik ohne Wolken: Die Luft ist so trocken (Spreizung über "
              "15 K), dass die Blasen die Inversion erreichen, bevor sie "
              "kondensieren. Oft stark, aber blind.\n\n"
              "Marken statt Wolken: die **Dunstglocke** (Obergrenze des "
              "Dunstes = Obergrenze der Thermik), **Staubteufel**, kreisende "
              "**Greifvögel**, andere Segelflugzeuge, Kumulusfetzen, die nur "
              "Sekunden leben. Die Arbeitshöhe muss gerechnet werden.",
              "Thermals without clouds: the air is so dry (spread above 15 K) "
              "that the bubbles reach the inversion before they condense. "
              "Often strong, but blind.\n\n"
              "Markers instead of clouds: the **haze dome** (top of the haze = "
              "top of the lift), **dust devils**, circling **birds of prey**, "
              "other gliders, cumulus wisps that live only seconds. The "
              "working height has to be calculated."),
            bild="begriff-blauthermik",
            siehe=["spread", "dunstglocke", "inversion", "thermik"],
            formen=["Blauthermik", "blue thermals", "blue day"]),

    begriff("dunstglocke", t("Dunstglocke", "Haze dome"),
            t("Die Dunstschicht unter der Inversion, von oben als scharfe "
              "Obergrenze zu sehen, über einer Stadt oft als Kuppel. Sie "
              "zeigt bei Blauthermik, wie hoch die Thermik reicht: Bis zur "
              "Dunstobergrenze trägt es, darüber ist die Luft glatt.\n\n"
              "Beulen in der Dunstobergrenze markieren einzelne Schläuche.",
              "The haze layer beneath the inversion, seen from above as a "
              "sharp top, over a town often as a dome. On a blue day it shows "
              "how high the lift goes: it carries up to the top of the haze, "
              "above it the air is smooth.\n\n"
              "Bumps in the haze top mark individual thermals."),
            bild="begriff-dunstglocke",
            siehe=["blauthermik", "inversion"],
            formen=["Dunstglocke", "Dunst", "haze dome", "haze"]),

    begriff("tagesgang", t("Tagesgang der Thermik", "Daily cycle of thermals"),
            t("Thermik folgt der Sonne mit Verzögerung: Beginn zwei bis vier "
              "Stunden nach Sonnenaufgang, wenn die Bodeninversion weggeheizt "
              "ist; Optimum ein bis zwei Stunden nach dem Sonnenhöchststand; "
              "spätnachmittags weich, die letzte Stunde trügerisch.\n\n"
              "Die Rückkehr wird nach dem gerechnet, was in einer Stunde noch "
              "trägt — nicht nach der Basis.",
              "Thermals follow the sun with a delay: start two to four hours "
              "after sunrise once the surface inversion is burnt off; optimum "
              "one to two hours after the sun's peak; soft in the late "
              "afternoon, the last hour deceptive.\n\n"
              "The return is planned by what still carries in an hour — not "
              "by the base."),
            bild="begriff-tagesgang",
            siehe=["ausloesung", "inversion", "tagesverlauf", "planung"],
            formen=["Tagesgang", "daily cycle"]),

    begriff("tagesverlauf", t("Tagesverläufe", "How a day can go"),
            t("Nicht jeder Tag ist der Normaltag: Cumulus-Tag, Blauthermik, "
              "Überentwicklung, Zumachen, Fronttag, Rückseitenwetter, Welle, "
              "Hochnebel — acht Verläufe, und jeder ist am Morgen an den "
              "Wolken zu erkennen.\n\n"
              "Die Frage um 9 Uhr: Was steht im Westen, wie groß ist die "
              "Spreizung, sind die ersten Cumuli flach oder schon Türme?",
              "Not every day is the normal day: cumulus day, blue thermals, "
              "overdevelopment, closing in, front day, post-frontal air, wave, "
              "low stratus — eight courses, and each shows itself in the "
              "morning clouds.\n\n"
              "The question at 9 o'clock: what stands in the west, how large "
              "is the spread, are the first cumuli flat or already towers?"),
            bild="tagesverlaeufe",
            siehe=["tagesgang", "ueberentwicklung", "ausbreitung", "warmfront", "rueckseitenwetter"],
            formen=["Tagesverläufe", "Tagesverlauf", "how a day can go"]),

    begriff("rueckseitenwetter", t("Rückseitenwetter", "Post-frontal air"),
            t("Die kalte, klare Luft **hinter einer Kaltfront**: Sicht 50 km, "
              "scharfe Cumuli mit hoher Basis, oft Schauer und Böen. Die "
              "Thermik ist kräftig, weil die Luft kalt und labil ist, aber "
              "ruppig.\n\n"
              "Oft der beste Streckentag des Monats — und der, an dem man "
              "die Schauer im Auge behalten muss.",
              "The cold, clear air **behind a cold front**: visibility 50 km, "
              "crisp cumuli with a high base, often showers and gusts. The "
              "lift is strong because the air is cold and unstable, but "
              "rough.\n\n"
              "Often the best cross-country day of the month — and the one "
              "on which the showers need watching."),
            bild="begriff-kaltfront",
            siehe=["kaltfront", "labilitaet", "tagesverlauf"],
            formen=["Rückseitenwetter", "post-frontal air", "post-frontal"]),

    # -- Wind, Welle, Hang -----------------------------------------------------
    begriff("luv-lee", t("Luv und Lee", "Windward and lee"),
            t("**Luv** ist die dem Wind zugewandte Seite, **Lee** die "
              "abgewandte. Am Hang steigt es im Luv und sinkt im Lee; hinter "
              "einem Berg entstehen im Lee Welle und Rotor; und eine Wolke "
              "steht im Lee ihrer Quelle.\n\n"
              "Merkhilfe: Lee ist dort, wo der Wind hin**weht** — leer von "
              "Wind.",
              "**Windward** is the side facing the wind, **lee** the sheltered "
              "side. On a ridge the lift is on the windward side and the sink "
              "in the lee; behind a mountain wave and rotor form in the lee; "
              "and a cloud stands in the lee of its source.\n\n"
              "Memory aid: the lee is where the wind blows **to**."),
            bild="begriff-luv-lee",
            siehe=["hangaufwind", "welle", "rotor", "anflug"],
            formen=["Luv", "Lee", "Luvseite", "Leeseite", "windward", "lee", "upwind side", "downwind"]),

    begriff("hangaufwind", t("Hangaufwind", "Ridge lift"),
            t("Wind, der auf einen Hang trifft, wird nach oben abgelenkt: Vor "
              "dem Hang (luvseitig) entsteht eine Aufwindzone, die mit "
              "Windstärke und Hanghöhe wächst. Fliegbar ab etwa 20 km/h Wind "
              "senkrecht zum Hang.\n\n"
              "Geflogen wird in Achten entlang des Hangs, nie mit dem Hang im "
              "Rücken kurvend; und nie ins Lee, wo es ebenso stark sinkt.",
              "Wind hitting a slope is deflected upward: in front of the "
              "slope (windward) a zone of lift forms that grows with wind "
              "strength and slope height. Flyable from about 20 km/h of wind "
              "perpendicular to the ridge.\n\n"
              "Fly figures of eight along the ridge, never turning with the "
              "ridge at your back; and never into the lee, where the sink is "
              "just as strong."),
            bild="begriff-hangaufwind",
            siehe=["luv-lee", "welle", "rotor"],
            formen=["Hangaufwind", "Hangwind", "Hang", "ridge lift", "slope lift", "ridge"]),

    begriff("welle", t("Leewelle", "Lee wave"),
            t("Hinter einem Gebirge schwingt die Strömung bei starkem Wind "
              "und stabiler Schichtung auf und ab wie Wasser hinter einem "
              "Stein — ortsfest, oft bis 10 km Höhe und mehr. Im Wellenberg "
              "steigt es gleichmäßig, 2–8 m/s, in glatter Luft.\n\n"
              "Sichtbar an **Lenticularis** auf den Wellenbergen und "
              "**Rotorwolken** darunter; bei Föhn am **Föhnfenster**. Mit "
              "Sauerstoff und Flugplanrecht wird daraus der Höhenflug.",
              "Behind a mountain range, with strong wind and stable layering, "
              "the flow oscillates up and down like water behind a stone — "
              "fixed in place, often up to 10 km and more. In the wave crest "
              "the lift is steady, 2–8 m/s, in smooth air.\n\n"
              "Visible as **lenticularis** on the crests and **rotor clouds** "
              "beneath; with foehn at the **foehn gap**. With oxygen and the "
              "right airspace it becomes a high-altitude flight."),
            bild="begriff-welle",
            siehe=["lenticularis", "rotor", "foehn", "luv-lee"],
            formen=["Leewelle", "Welle", "Wellen", "lee wave", "wave"]),

    begriff("rotor", t("Rotor", "Rotor"),
            t("Die Walze aus turbulenter Luft **unter** dem ersten Wellenberg, "
              "im Lee des Gebirges: Die Strömung rollt sich hier wie eine "
              "Brandung ein. Oft markiert durch zerfetzte, kochende "
              "**Rotorwolken** in Hanghöhe.\n\n"
              "Der gefährlichste Teil der Welle — Böen, die ein Flugzeug "
              "überlasten können. Hindurch nur mit Fahrt, Gurten fest, und "
              "nicht nahe am Hang; darüber beginnt die glatte Welle.",
              "The roll of turbulent air **beneath** the first wave crest, in "
              "the lee of the mountains: the flow curls over here like surf. "
              "Often marked by ragged, boiling **rotor clouds** at ridge "
              "height.\n\n"
              "The most dangerous part of the wave — gusts that can overload "
              "an aircraft. Through it only with speed, straps tight, and not "
              "close to the slope; above it the smooth wave begins."),
            bild="begriff-rotor",
            siehe=["welle", "lenticularis", "lastvielfaches"],
            formen=["Rotor", "Rotoren", "Rotorwolken", "rotor", "rotor clouds", "rotors"]),

    begriff("foehn", t("Föhn", "Foehn"),
            t("Warmer, trockener Fallwind im Lee eines Gebirges: Die Luft "
              "regnet sich im Luv aus und erwärmt sich beim Absinken "
              "trockenadiabatisch (1 °C je 100 m). Im Lee: klare Sicht, "
              "Föhnmauer über dem Kamm, **Föhnfenster** dahinter, Lenticularis "
              "darüber.\n\n"
              "Föhn heißt Welle — und Böen am Boden, die Starts und Landungen "
              "schwierig machen.",
              "A warm, dry downslope wind in the lee of a mountain range: the "
              "air rains out on the windward side and warms dry-adiabatically "
              "(1 °C per 100 m) as it descends. In the lee: clear visibility, "
              "a foehn wall over the crest, the **foehn gap** behind it, "
              "lenticularis above.\n\n"
              "Foehn means wave — and gusts on the ground that make launches "
              "and landings difficult."),
            bild="begriff-foehn",
            siehe=["welle", "lenticularis", "rotor"],
            formen=["Föhn", "Föhnfenster", "foehn", "foehn gap"]),

    begriff("abwind", t("Abwind", "Sink"),
            t("Die absinkende Luft, die jeden Aufwind ausgleicht: am Rand "
              "jedes Thermikschlauchs, zwischen Wolkenstraßen, unter "
              "zerfallenden Wolken, im Lee von Hängen, unter dem Amboss. Oft "
              "ebenso stark wie das Steigen daneben.\n\n"
              "Im Abwind nicht trödeln: Fahrt aufnehmen und durch — das sagt "
              "die Sollfahrt nach McCready.",
              "The descending air that balances every updraught: at the edge "
              "of every thermal, between cloud streets, under decaying clouds, "
              "in the lee of slopes, under the anvil. Often as strong as the "
              "lift next to it.\n\n"
              "Do not dawdle in sink: pick up speed and get through — that is "
              "what MacCready's speed-to-fly says."),
            bild="begriff-abwind",
            siehe=["thermikschlauch", "mccready", "wolkenstrasse"],
            formen=["Abwind", "Abwinde", "sink", "downdraught", "downdraughts"]),

    # -- Fronten und Druck -----------------------------------------------------
    begriff("warmfront", t("Warmfront", "Warm front"),
            t("Warme Luft schiebt sich flach über kalte und gleitet an ihr "
              "auf — die Wolken kommen in fester Reihenfolge von oben herab: "
              "**Cirrus**-Haken, **Cirrostratus** mit Halo, **Altostratus** "
              "(Sonne als Scheibe), **Nimbostratus** mit Dauerregen. Vom "
              "ersten Haken bis zum Regen vergehen 12 bis 24 Stunden.\n\n"
              "Für den Piloten: Der Tag mit den ersten Haken ist noch gut, "
              "wird aber nachmittags weich; der nächste fällt aus.",
              "Warm air slides up and over cold air at a shallow angle — the "
              "clouds arrive in a fixed sequence from above: **cirrus** hooks, "
              "**cirrostratus** with halo, **altostratus** (sun as a disc), "
              "**nimbostratus** with steady rain. From the first hook to the "
              "rain 12 to 24 hours pass.\n\n"
              "For the pilot: the day with the first hooks is still good but "
              "turns soft in the afternoon; the next one is lost."),
            bild="begriff-warmfront",
            siehe=["cirrus", "cirrostratus", "altostratus", "nimbostratus", "kaltfront"],
            formen=["Warmfront", "warm front"]),

    begriff("kaltfront", t("Kaltfront", "Cold front"),
            t("Kalte Luft schiebt sich steil unter warme und hebt sie ruckartig: "
              "eine schmale Linie aus **Cumulonimben**, Böenfront, "
              "Platzregen, dann in ein, zwei Stunden Aufklaren mit kalter, "
              "klarer Luft. Am Himmel vorher: Druckfall, zunehmender Südwind, "
              "eine dunkle Wand im Westen.\n\n"
              "Vor der Front landen; dahinter kommt das Rückseitenwetter — "
              "oft der beste Thermiktag.",
              "Cold air pushes steeply under warm air and lifts it abruptly: a "
              "narrow line of **cumulonimbus**, gust front, downpour, then "
              "within an hour or two clearing with cold, clear air. In the sky "
              "beforehand: falling pressure, rising southerly wind, a dark "
              "wall in the west.\n\n"
              "Land before the front; behind it comes the post-frontal air — "
              "often the best thermal day."),
            bild="begriff-kaltfront",
            siehe=["cumulonimbus", "boeenfront", "rueckseitenwetter", "warmfront"],
            formen=["Kaltfront", "cold front"]),

    begriff("boeenfront", t("Böenfront", "Gust front"),
            t("Die Kaltluft, die aus einem Gewitter oder einer Schauerzelle "
              "herausfällt und sich am Boden ausbreitet, mit einer scharfen "
              "Vorderkante: plötzlicher Winddreher, 50–100 km/h Böen, oft "
              "eine Walzenwolke davor. Sie läuft dem Regen 5–15 km voraus.\n\n"
              "Am Boden: Flugzeug verzurren oder wegräumen. In der Luft: "
              "Landung vorher oder weit nachher, nie hinein.",
              "The cold air falling out of a thunderstorm or shower cell and "
              "spreading along the ground with a sharp leading edge: sudden "
              "wind shift, 50–100 km/h gusts, often a roll cloud ahead of it. "
              "It runs 5–15 km ahead of the rain.\n\n"
              "On the ground: tie down or hangar the glider. In the air: land "
              "before it or well after, never into it."),
            bild="begriff-boeenfront",
            siehe=["cumulonimbus", "kaltfront"],
            formen=["Böenfront", "Böen", "gust front", "gusts"]),

    begriff("amboss", t("Amboss", "Anvil"),
            t("Die vereiste, flach auseinanderlaufende Oberseite eines "
              "Cumulonimbus, vom Höhenwind in Zugrichtung verweht. Unter ihm "
              "Abschattung und Abwind über viele Kilometer; aus ihm fällt "
              "Hagel weit vor der Zelle.\n\n"
              "Die Richtung, in die der Amboss zeigt, ist die Zugrichtung "
              "des Gewitters — dort nicht hin.",
              "The iced-over, flat spreading top of a cumulonimbus, blown out "
              "by the upper wind in the direction of travel. Beneath it "
              "shading and sink over many kilometres; from it hail falls well "
              "ahead of the cell.\n\n"
              "The direction the anvil points is the storm's direction of "
              "travel — do not go there."),
            bild="begriff-amboss",
            siehe=["cumulonimbus", "abschirmung"],
            formen=["Amboss", "anvil"]),

    begriff("hochdruck", t("Hochdruck", "High pressure"),
            t("Ein Gebiet hohen Luftdrucks: absinkende Luft, die sich erwärmt "
              "und trocknet — klarer Himmel, schwacher Wind, am Rand im "
              "Uhrzeigersinn ausströmend (Nordhalbkugel). Das Absinken baut "
              "die **Absinkinversion**, die den Thermiktag deckelt.\n\n"
              "Sommerhoch: gute, aber niedrige Thermik, Dunst, Blauthermik. "
              "Winterhoch: Hochnebel, der tagelang liegen bleibt.",
              "An area of high air pressure: descending air that warms and "
              "dries — clear sky, light wind, flowing out clockwise at the "
              "edge (northern hemisphere). The descent builds the "
              "**subsidence inversion** that caps the thermal day.\n\n"
              "Summer high: good but low thermals, haze, blue days. Winter "
              "high: low stratus lying for days."),
            bild="begriff-hochdruck",
            siehe=["inversion", "tiefdruck", "blauthermik"],
            formen=["Hochdruck", "Hoch", "Hochdruckgebiet", "high pressure", "high"]),

    begriff("tiefdruck", t("Tiefdruck", "Low pressure"),
            t("Ein Gebiet tiefen Luftdrucks: Luft strömt gegen den Uhrzeigersinn "
              "hinein und steigt auf — Wolken, Fronten, Regen, Wind. Die "
              "Fronten hängen an ihm: vorn die Warmfront, hinten die "
              "Kaltfront, dazwischen der Warmsektor.\n\n"
              "Fliegbar sind meist nur die Rückseite und der Warmsektor "
              "mit seiner Blauthermik unter Dunst.",
              "An area of low air pressure: air flows in anticlockwise and "
              "rises — cloud, fronts, rain, wind. The fronts hang from it: the "
              "warm front ahead, the cold front behind, the warm sector "
              "between.\n\n"
              "Usually only the rear side and the warm sector with its hazy "
              "blue thermals are flyable."),
            bild="begriff-tiefdruck",
            siehe=["hochdruck", "warmfront", "kaltfront"],
            formen=["Tiefdruck", "Tief", "Tiefdruckgebiet", "low pressure", "low"]),

    begriff("halo", t("Halo", "Halo"),
            t("Der Ring um Sonne oder Mond im Abstand von 22 Grad, entstanden "
              "durch Brechung in den Eiskristallen eines **Cirrostratus**. Wer "
              "ihn sieht, sieht den Eisschleier, auch wenn der Himmel noch "
              "blau wirkt.\n\n"
              "Alte Regel: Halo heute, Regen morgen — die Warmfront ist "
              "unterwegs.",
              "The ring around the sun or moon at 22 degrees, made by "
              "refraction in the ice crystals of a **cirrostratus**. Whoever "
              "sees it sees the ice veil even if the sky still looks blue.\n\n"
              "Old rule: halo today, rain tomorrow — the warm front is on its "
              "way."),
            bild="begriff-halo",
            siehe=["cirrostratus", "warmfront"],
            formen=["Halo", "halo"]),

    begriff("nebel", t("Nebel und Hochnebel", "Fog and low stratus"),
            t("Nebel ist eine Wolke am Boden (Sicht unter 1 km), Hochnebel "
              "dieselbe Schicht ein paar hundert Meter höher — Stratus. Beide "
              "entstehen in klaren Nächten durch Abkühlung oder unter einer "
              "Winterinversion.\n\n"
              "Ob er sich auflöst, verrät die Dicke: Sonne als Scheibe sichtbar "
              "und erste Löcher bis 11 Uhr — ja, dann wird es ein guter Tag; "
              "gleichmäßig grau und windstill — nein.",
              "Fog is a cloud on the ground (visibility under 1 km), low "
              "stratus the same layer a few hundred metres higher. Both form "
              "on clear nights by cooling or beneath a winter inversion.\n\n"
              "Whether it breaks up is told by its thickness: sun visible as a "
              "disc and first holes by 11 o'clock — yes, and a good day "
              "follows; uniformly grey and calm — no."),
            bild="begriff-nebel",
            siehe=["stratus", "inversion", "tagesverlauf"],
            formen=["Nebel", "Hochnebel", "fog", "low stratus"]),

    # -- Aerodynamik und Leistung ----------------------------------------------
    begriff("polare", t("Geschwindigkeitspolare", "Speed polar"),
            t("Die Kurve, die jeder Fluggeschwindigkeit das zugehörige Sinken "
              "zuordnet — die Leistungsbeschreibung des Flugzeugs. Ihr "
              "höchster Punkt ist das **geringste Sinken**, die Tangente vom "
              "Ursprung das **beste Gleiten**; bei mehr Fahrt fällt sie steil "
              "ab.\n\n"
              "Mit Wasserballast verschiebt sie sich nach rechts (schneller "
              "bei gleichem Gleiten), im Abwind oder Gegenwind nach unten "
              "bzw. links — daraus folgt die Sollfahrt.",
              "The curve that assigns to every airspeed its rate of sink — the "
              "performance description of the aircraft. Its highest point is "
              "**minimum sink**, the tangent from the origin **best glide**; at "
              "higher speed it drops away steeply.\n\n"
              "With water ballast it shifts right (faster at the same glide), "
              "in sink or headwind down or left — from that follows the "
              "speed to fly."),
            bild="begriff-polare",
            siehe=["gleitzahl", "geringstes-sinken", "bestes-gleiten", "mccready"],
            formen=["Polare", "Geschwindigkeitspolare", "speed polar", "polar"]),

    begriff("gleitzahl", t("Gleitzahl", "Glide ratio"),
            t("Das Verhältnis von zurückgelegter Strecke zu verlorener Höhe im "
              "ruhigen Gleitflug: 40 heißt 40 km aus 1 000 m. Sie ist gleich "
              "dem Verhältnis von Auftrieb zu Widerstand und hängt nicht vom "
              "Gewicht ab — nur die Fahrt, bei der sie erreicht wird.\n\n"
              "Im Wind ändert sie sich über Grund: Gegenwind frisst, "
              "Rückenwind schenkt. Für den Endanflug mit Sicherheitsreserve "
              "rechnen.",
              "The ratio of distance covered to height lost in a still-air "
              "glide: 40 means 40 km from 1,000 m. It equals the ratio of lift "
              "to drag and does not depend on weight — only the speed at which "
              "it is achieved does.\n\n"
              "In wind it changes over the ground: headwind eats it, tailwind "
              "gives. For the final glide calculate with a safety margin."),
            bild="skizze-gleitflug",
            siehe=["polare", "bestes-gleiten", "endanflug"],
            formen=["Gleitzahl", "glide ratio", "glide angle"]),

    begriff("geringstes-sinken", t("Geringstes Sinken", "Minimum sink"),
            t("Die Fahrt, bei der das Flugzeug am langsamsten Höhe verliert — "
              "der höchste Punkt der Polare, meist knapp über der "
              "Überziehgeschwindigkeit. Sie ist die Fahrt zum **Kurbeln** in "
              "der Thermik, zuzüglich des Zuschlags für die Kurve.\n\n"
              "Zum Gleiten ist sie zu langsam: Dort gilt das beste Gleiten.",
              "The speed at which the aircraft loses height most slowly — the "
              "highest point of the polar, usually just above the stall speed. "
              "It is the speed for **circling** in a thermal, plus the "
              "allowance for the bank.\n\n"
              "For gliding it is too slow: there, best glide applies."),
            bild="begriff-polare",
            siehe=["polare", "bestes-gleiten", "kurbeln"],
            formen=["Geringstes Sinken", "geringstes Sinken", "minimum sink"]),

    begriff("bestes-gleiten", t("Bestes Gleiten", "Best glide"),
            t("Die Fahrt, bei der die Gleitzahl am größten ist — die Tangente "
              "vom Ursprung an die Polare. In ruhiger Luft und ohne Wind die "
              "Fahrt, mit der man am weitesten kommt.\n\n"
              "Mit Gegenwind oder Abwind schneller fliegen, mit Rückenwind "
              "oder Aufwind langsamer: Die Tangente wandert.",
              "The speed at which the glide ratio is greatest — the tangent "
              "from the origin to the polar. In still air without wind the "
              "speed that takes you furthest.\n\n"
              "Fly faster in headwind or sink, slower in tailwind or lift: the "
              "tangent moves."),
            bild="begriff-polare",
            siehe=["gleitzahl", "polare", "mccready"],
            formen=["Bestes Gleiten", "bestes Gleiten", "best glide"]),

    begriff("mccready", t("McCready-Sollfahrt", "MacCready speed to fly"),
            t("Die Fahrt zwischen zwei Aufwinden, die die Reisegeschwindigkeit "
              "über den Tag am größten macht: Je stärker das Steigen, das man "
              "im nächsten Bart erwartet (der **McCready-Wert**), desto "
              "schneller fliegt man dazwischen — und im Abwind noch schneller.\n\n"
              "Der Sollfahrtgeber am Variometer zeigt es an; der Wert wird "
              "nach dem tatsächlichen Mittelsteigen gesetzt, nicht nach dem "
              "Wunsch.",
              "The speed between two thermals that maximises the cruising "
              "speed over the day: the stronger the climb you expect in the "
              "next thermal (the **MacCready setting**), the faster you fly "
              "between them — and faster still in sink.\n\n"
              "The speed director on the variometer shows it; the setting "
              "follows the actual average climb, not wishful thinking."),
            bild="begriff-mccready",
            siehe=["polare", "abwind", "variometer", "endanflug"],
            formen=["McCready", "MacCready", "Sollfahrt", "speed to fly"]),

    begriff("endanflug", t("Endanflug", "Final glide"),
            t("Der letzte Gleitflug zum Ziel ohne weiteres Kurbeln. Aus "
              "Entfernung, Gleitzahl, Wind und Sicherheitshöhe ergibt sich die "
              "nötige Abflughöhe; die Rechnung macht der Endanflugrechner, "
              "die Kontrolle das Auge: Wandert das Ziel in der Haube nach "
              "oben, reicht es nicht.\n\n"
              "Reserve einplanen — Abwind und Gegenwind sind nie ganz "
              "bekannt, und tief über fremdem Gelände ist kein Ort zum Suchen.",
              "The last glide to the goal without further circling. From "
              "distance, glide ratio, wind and safety height follows the "
              "required departure height; the final-glide computer does the "
              "sum, the eye does the check: if the goal climbs in the canopy, "
              "it will not be enough.\n\n"
              "Plan a reserve — sink and headwind are never fully known, and "
              "low over strange ground is no place to search."),
            bild="begriff-endanflug",
            siehe=["gleitzahl", "mccready", "sicherheitshoehe", "aussenlandung"],
            formen=["Endanflug", "final glide"]),

    begriff("ueberziehen", t("Überziehen", "Stall"),
            t("Der Strömungsabriss: Wird der **Anstellwinkel** zu groß, löst "
              "sich die Strömung von der Flügeloberseite, der Auftrieb bricht "
              "ein, die Nase fällt. Es passiert bei jeder Fahrt, wenn der "
              "Anstellwinkel stimmt — in der Kurve und beim Abfangen auch "
              "mit viel Fahrt.\n\n"
              "Vorzeichen: weiche Ruder, Schütteln, Stille. Ausleiten: "
              "**nachdrücken**, Fahrt aufnehmen, dann abfangen. Nie zuerst "
              "ziehen.",
              "The flow separation: if the **angle of attack** becomes too "
              "large, the flow detaches from the upper wing surface, lift "
              "collapses, the nose drops. It happens at any speed when the "
              "angle of attack is right — in a turn and in a pull-up even at "
              "high speed.\n\n"
              "Warning signs: soft controls, buffeting, silence. Recovery: "
              "**push**, gain speed, then pull out. Never pull first."),
            bild="begriff-ueberziehen",
            siehe=["anstellwinkel", "trudeln", "lastvielfaches"],
            formen=["Überziehen", "überzogen", "stall", "stalling"]),

    begriff("anstellwinkel", t("Anstellwinkel", "Angle of attack"),
            t("Der Winkel zwischen Flügelprofil und anströmender Luft. Er "
              "bestimmt den Auftrieb, nicht die Fahrt: Bei etwa 15 Grad reißt "
              "die Strömung ab, egal wie schnell man fliegt.\n\n"
              "Beim Abfangen und in der steilen Kurve wird er groß — darum "
              "kann man bei jeder Fahrt überziehen.",
              "The angle between the wing section and the oncoming air. It "
              "determines the lift, not the speed: at about 15 degrees the "
              "flow separates, however fast you fly.\n\n"
              "In a pull-up and in a steep turn it becomes large — which is "
              "why you can stall at any speed."),
            bild="begriff-anstellwinkel",
            siehe=["ueberziehen", "lastvielfaches"],
            formen=["Anstellwinkel", "angle of attack"]),

    begriff("lastvielfaches", t("Lastvielfaches", "Load factor"),
            t("Das Verhältnis von Auftrieb zu Gewicht, in **g**. Im "
              "Geradeausflug 1; in der Kurve 1/cos(Querlage): bei 45 Grad "
              "1,4 g, bei 60 Grad 2 g. Mit dem Lastvielfachen steigt die "
              "Überziehgeschwindigkeit um die Wurzel daraus — bei 60 Grad um "
              "41 Prozent.\n\n"
              "Böen und ruppiges Abfangen bringen ein Vielfaches davon; die "
              "Manövergeschwindigkeit setzt die Grenze.",
              "The ratio of lift to weight, in **g**. In straight flight 1; in "
              "a turn 1/cos(bank): at 45 degrees 1.4 g, at 60 degrees 2 g. "
              "The stall speed rises with the square root of the load factor "
              "— by 41 per cent at 60 degrees.\n\n"
              "Gusts and rough pull-ups bring a multiple of it; the "
              "manoeuvring speed sets the limit."),
            bild="skizze-kurvenlast",
            siehe=["ueberziehen", "rotor"],
            formen=["Lastvielfaches", "Lastvielfache", "load factor"]),

    begriff("trudeln", t("Trudeln", "Spin"),
            t("Der Zustand nach einem einseitigen Strömungsabriss: Ein Flügel "
              "hängt tiefer, das Flugzeug dreht steil um die Hochachse und "
              "verliert je Umdrehung 50–100 m. Es entsteht aus überzogenem "
              "Flug mit Schiebewinkel — klassisch in der langsamen, "
              "schmierigen Kurve nahe am Boden.\n\n"
              "Ausleiten: Querruder neutral, **Seitenruder gegen die "
              "Drehung**, nachdrücken, nach dem Stillstand abfangen. Tief "
              "unten gibt es kein Ausleiten — darum dort Fahrt und saubere "
              "Kurven.",
              "The state after a one-sided stall: one wing drops, the aircraft "
              "rotates steeply about the vertical axis and loses 50–100 m per "
              "turn. It arises from stalled flight with sideslip — "
              "classically in the slow, skidding turn close to the ground.\n\n"
              "Recovery: ailerons neutral, **rudder against the rotation**, "
              "push, pull out once the rotation stops. Low down there is no "
              "recovery — hence speed and clean turns there."),
            bild="begriff-trudeln",
            siehe=["ueberziehen", "anstellwinkel"],
            formen=["Trudeln", "trudelt", "spin", "spinning"]),

    begriff("kurbeln", t("Kurbeln", "Thermalling"),
            t("Das Kreisen im Aufwind: Querlage 30–45 Grad, Fahrt nahe dem "
              "geringsten Sinken plus Kurvenzuschlag, Kreis so eng wie der "
              "Schlauch. Zentriert wird nach dem Variometer: Dort, wo es am "
              "stärksten steigt, die Kurve öffnen und zur Mitte versetzen.\n\n"
              "Im Pulk: alle in dieselbe Richtung, der Erste gibt sie vor.",
              "Circling in lift: bank 30–45 degrees, speed near minimum sink "
              "plus the turn allowance, circle as tight as the core. Centre by "
              "the variometer: where it climbs strongest, open the turn and "
              "shift towards the middle.\n\n"
              "In a gaggle: everyone the same way round, the first one sets "
              "it."),
            bild="begriff-kurbeln",
            siehe=["thermikschlauch", "geringstes-sinken", "variometer"],
            formen=["Kurbeln", "kurbeln", "thermalling", "circling"]),

    # -- Beladung und Planung --------------------------------------------------
    begriff("schwerpunkt", t("Schwerpunkt", "Centre of gravity"),
            t("Der Punkt, in dem das Flugzeug im Gleichgewicht hängt. Er muss "
              "im zugelassenen **Schwerpunktbereich** liegen: zu weit vorn "
              "heißt schwer zu ziehen, hohe Überziehgeschwindigkeit, viel "
              "Trimmwiderstand; zu weit hinten heißt instabil, leicht "
              "überziehbar, Trudeln nicht ausleitbar.\n\n"
              "Verschoben wird er mit Pilotengewicht, Trimmballast, "
              "Wasserballast — vor jedem Flug nachrechnen.",
              "The point at which the aircraft balances. It must lie within the "
              "approved **CG range**: too far forward means heavy to pull, "
              "high stall speed, much trim drag; too far aft means unstable, "
              "easily stalled, a spin that cannot be recovered.\n\n"
              "It moves with pilot weight, trim ballast, water ballast — "
              "check before every flight."),
            bild="skizze-schwerpunkt",
            siehe=["beladung", "trudeln", "wasserballast"],
            formen=["Schwerpunkt", "Schwerpunktbereich", "centre of gravity", "CG"]),

    begriff("beladung", t("Beladung", "Loading"),
            t("Was im Flugzeug sitzt und liegt: Pilot, Fallschirm, Ballast, "
              "Wasser. Zwei Grenzen gelten: die **maximale Abflugmasse** und "
              "die **Mindestzuladung** im Sitz — darunter wandert der "
              "Schwerpunkt nach hinten, und der Trimmballast muss dazu.\n\n"
              "Die Zahlen stehen im Cockpit und im Flughandbuch; der Tipp am "
              "Flugplatz ersetzt sie nicht.",
              "What sits and lies in the aircraft: pilot, parachute, ballast, "
              "water. Two limits apply: the **maximum take-off mass** and the "
              "**minimum cockpit load** — below it the CG moves aft and trim "
              "ballast must be added.\n\n"
              "The figures are in the cockpit and the flight manual; the tip "
              "at the airfield does not replace them."),
            bild="skizze-schwerpunkt",
            siehe=["schwerpunkt", "wasserballast"],
            formen=["Beladung", "Mindestzuladung", "loading", "minimum cockpit load"]),

    begriff("wasserballast", t("Wasserballast", "Water ballast"),
            t("Wasser in den Flügeltanks, bis zu 200 Liter: Es erhöht die "
              "Flächenbelastung und verschiebt die Polare nach rechts — "
              "gleiche Gleitzahl bei höherer Fahrt, also schneller über die "
              "Strecke. Dafür schlechteres Steigen in schwacher Thermik.\n\n"
              "An starken Tagen voll, an schwachen leer; vor der Landung "
              "ablassen, bei Frost gar nicht erst einfüllen.",
              "Water in the wing tanks, up to 200 litres: it raises the wing "
              "loading and shifts the polar to the right — the same glide "
              "ratio at higher speed, so faster around the course. In return, "
              "poorer climb in weak lift.\n\n"
              "Full on strong days, empty on weak ones; dump before landing, "
              "and do not fill at all in frost."),
            bild="begriff-wasserballast",
            siehe=["polare", "schwerpunkt", "beladung"],
            formen=["Wasserballast", "water ballast", "ballast"]),

    begriff("dichtehoehe", t("Dichtehöhe", "Density altitude"),
            t("Die Höhe der Standardatmosphäre, in der die Luft dieselbe "
              "Dichte hätte wie heute hier. Warm, hoch gelegen und feucht "
              "heißt dünne Luft: weniger Auftrieb, weniger Schleppleistung, "
              "**längere Startstrecke** — bei 30 °C auf 1 000 m Platzhöhe "
              "liegt die Dichtehöhe über 2 000 m.\n\n"
              "Faustformel: je 1 °C über ISA etwa 36 m höher.",
              "The altitude in the standard atmosphere at which the air would "
              "have the same density as here today. Warm, high and humid means "
              "thin air: less lift, less tow power, **longer take-off run** — "
              "at 30 °C on a 1,000 m airfield the density altitude is above "
              "2,000 m.\n\n"
              "Rule of thumb: about 36 m (120 ft) higher per 1 °C above ISA."),
            bild="begriff-dichtehoehe",
            siehe=["startstrecke", "isa"],
            formen=["Dichtehöhe", "density altitude"]),

    begriff("isa", t("Standardatmosphäre (ISA)", "Standard atmosphere (ISA)"),
            t("Die vereinbarte Mittelatmosphäre: 15 °C und 1013,25 hPa in "
              "Meereshöhe, Abnahme um 2 °C je 300 m (0,65 °C je 100 m) und "
              "etwa 1 hPa je 8 m in Bodennähe. Auf ihr beruhen Höhenmesser, "
              "Flugflächen und Leistungstabellen.\n\n"
              "Die wirkliche Atmosphäre weicht davon ab — daraus folgen "
              "Dichtehöhe und Höhenmesserfehler.",
              "The agreed mean atmosphere: 15 °C and 1013.25 hPa at sea "
              "level, falling 2 °C per 1,000 ft (0.65 °C per 100 m) and about "
              "1 hPa per 8 m near the ground. Altimeters, flight levels and "
              "performance tables are based on it.\n\n"
              "The real atmosphere departs from it — hence density altitude "
              "and altimeter errors."),
            bild="begriff-isa",
            siehe=["dichtehoehe", "qnh", "flugflaeche"],
            formen=["ISA", "Standardatmosphäre", "standard atmosphere"]),

    begriff("startstrecke", t("Startstrecke", "Take-off distance"),
            t("Die Strecke vom Stillstand bis zum Überfliegen eines "
              "15-m-Hindernisses, aus dem Flughandbuch für Standardbedingungen. "
              "Sie wächst mit Masse, Dichtehöhe, Rückenwind, nassem oder "
              "hohem Gras und Gefälle — die Zuschläge multiplizieren sich.\n\n"
              "Im Windenstart zählt die Seillänge, im Flugzeugschlepp die "
              "Leistung des Schleppflugzeugs an diesem Tag.",
              "The distance from standstill to clearing a 15 m obstacle, from "
              "the flight manual for standard conditions. It grows with mass, "
              "density altitude, tailwind, wet or long grass and upslope — "
              "the factors multiply.\n\n"
              "On a winch launch the cable length counts; on an aerotow the "
              "tug's power on this day."),
            bild="begriff-dichtehoehe",
            siehe=["dichtehoehe", "sicherheitshoehe", "flugzeugschlepp"],
            formen=["Startstrecke", "take-off distance", "take-off run"]),

    begriff("sicherheitshoehe", t("Sicherheitshöhe", "Safety height"),
            t("Die Höhe, die man zur gerechneten Höhe addiert, um Unbekanntes "
              "abzudecken: Abwind, Gegenwind, Hindernisse, den eigenen "
              "Fehler. Für den Endanflug üblich 200–300 m über Platzhöhe; über "
              "Gelände ohne Landemöglichkeit mehr.\n\n"
              "Sie ist keine Reserve zum Verbrauchen, sondern die Grenze, ab "
              "der die Entscheidung fällt.",
              "The height added to the calculated height to cover the unknown: "
              "sink, headwind, obstacles, your own error. For the final glide "
              "usually 200–300 m above airfield elevation; more over terrain "
              "with no landing options.\n\n"
              "It is not a reserve to use up but the limit at which the "
              "decision is made."),
            bild="begriff-endanflug",
            siehe=["endanflug", "aussenlandung", "entscheidungshoehe"],
            formen=["Sicherheitshöhe", "safety height", "safety margin"]),

    begriff("planung", t("Flugplanung", "Flight planning"),
            t("Vor dem Streckenflug: Wetter (Thermikbeginn, Basis, "
              "Abschirmung, Front), Aufgabe und Wendepunkte, Lufträume und "
              "Freigaben, Außenlandefelder entlang der Strecke, Wasserballast "
              "und Beladung, und die **Rückkehr** nach dem, was in der letzten "
              "Stunde noch trägt.\n\n"
              "Die Entscheidung über Weiterflug oder Umkehr fällt an "
              "vorher festgelegten Grenzen, nicht unterwegs aus dem Bauch.",
              "Before the cross-country: weather (start of thermals, base, "
              "shading, front), task and turn points, airspace and clearances, "
              "landable fields along the route, water ballast and loading, "
              "and the **return** by what still carries in the last hour.\n\n"
              "The decision to continue or turn back is made at limits set "
              "beforehand, not from the gut en route."),
            siehe=["tagesgang", "luftraum", "aussenlandung", "entscheidung"],
            formen=["Flugplanung", "Planung", "flight planning", "planning"]),

    begriff("aussenlandung", t("Außenlandung", "Field landing"),
            t("Die Landung auf einem Feld, wenn die Thermik ausbleibt. Die "
              "Wahl beginnt in 600 m: **Größe, Hang, Oberfläche, Hindernisse, "
              "Wind** — ein großes, ebenes, kurz gemähtes Feld gegen den Wind, "
              "ohne Leitungen am Anflug. Entschieden wird spätestens in "
              "300 m, danach wird nur noch geflogen.\n\n"
              "Eine saubere Außenlandung ist Teil des Streckenflugs, kein "
              "Versagen; das Zögern ist das Risiko.",
              "Landing in a field when the lift fails. The choice begins at "
              "600 m: **size, slope, surface, obstacles, wind** — a large, "
              "level, short-mown field into wind, with no wires on the "
              "approach. Decide by 300 m at the latest; after that you only "
              "fly.\n\n"
              "A clean field landing is part of cross-country flying, not a "
              "failure; the hesitation is the risk."),
            bild="begriff-aussenlandung",
            siehe=["endanflug", "sicherheitshoehe", "entscheidung"],
            formen=["Außenlandung", "Außenlandeplanung", "field landing", "field selection"]),

    begriff("platzrunde", t("Platzrunde", "Circuit"),
            t("Der feste Weg zur Landung: Position (Gegenanflug neben der "
              "Bahn in 200–300 m), Queranflug, Endanflug. Sie macht den "
              "Verkehr am Platz vorhersehbar und gibt dem Piloten feste "
              "Punkte für Höhe und Fahrt.\n\n"
              "Lieber eine verkürzte Platzrunde mit Höhe als eine volle ohne.",
              "The fixed path to landing: downwind (beside the runway at "
              "200–300 m), base leg, final. It makes the traffic at the "
              "airfield predictable and gives the pilot fixed points for "
              "height and speed.\n\n"
              "Better a shortened circuit with height than a full one "
              "without."),
            bild="begriff-platzrunde",
            siehe=["aussenlandung", "ausweichen"],
            formen=["Platzrunde", "circuit"]),

    begriff("flugzeugschlepp", t("Flugzeugschlepp", "Aerotow"),
            t("Der Start hinter einem Motorflugzeug am 40–60 m langen Seil "
              "bis in Ausklinkhöhe, meist 500 m. Der Segelflieger hält die "
              "Position hinter dem Schlepper (Hochschlepp oder Tiefschlepp) "
              "und klinkt erst aus, wenn das Seil straff ist.\n\n"
              "Gefährdungen: Seilriss tief, Überholen des Schleppers bei "
              "Böen, und das Vergessen der Bremsklappen.",
              "The launch behind a powered aircraft on a 40–60 m rope to "
              "release height, usually 500 m. The glider holds position behind "
              "the tug (high or low tow) and releases only with the rope "
              "taut.\n\n"
              "Hazards: a rope break low down, overtaking the tug in gusts, "
              "and forgetting the airbrakes."),
            bild="begriff-flugzeugschlepp",
            siehe=["seilriss", "windenstart", "startstrecke"],
            formen=["Flugzeugschlepp", "F-Schlepp", "aerotow", "tug"]),

    begriff("windenstart", t("Windenstart", "Winch launch"),
            t("Der Start an einem bis zu 1 500 m langen Seil, das eine "
              "Motorwinde am Bahnende einzieht: steiler Steigflug mit "
              "100–120 km/h, Ausklinken in 300–450 m, wenn das Seil "
              "steil nach unten zeigt. Dauer unter eine Minute.\n\n"
              "Der kritische Moment ist der **Seilriss** im steilen Steigflug: "
              "sofort nachdrücken.",
              "The launch on a cable up to 1,500 m long, hauled in by a motor "
              "winch at the end of the runway: steep climb at 100–120 km/h, "
              "release at 300–450 m when the cable points steeply down. Under "
              "a minute.\n\n"
              "The critical moment is a **cable break** in the steep climb: "
              "push immediately."),
            bild="begriff-windenstart",
            siehe=["seilriss", "flugzeugschlepp"],
            formen=["Windenstart", "Winde", "winch launch", "winch"]),

    # -- Luftrecht und Höhenmessung -------------------------------------------
    begriff("luftraum", t("Luftraum", "Airspace"),
            t("Der Himmel ist in **Klassen** geteilt: Im Luftraum C und D "
              "(um Verkehrsflughäfen) braucht ein Segelflugzeug eine Freigabe "
              "und Funk, im Luftraum E darf es ohne fliegen, solange es "
              "Sichtflugbedingungen einhält, im Luftraum G ebenso. Dazu "
              "**Gebiete mit Beschränkungen**: Sperrgebiete, Gefahrengebiete, "
              "Segelflugsektoren, die nur auf Anfrage offen sind.\n\n"
              "Die Grenzen stehen in der Karte und im Rechner — und sie "
              "gelten auch in der Thermik.",
              "The sky is divided into **classes**: in airspace C and D "
              "(around airports) a glider needs a clearance and radio, in "
              "airspace E it may fly without as long as it keeps visual "
              "flight rules, in airspace G likewise. Plus **areas with "
              "restrictions**: prohibited and danger areas, gliding sectors "
              "open only on request.\n\n"
              "The boundaries are on the chart and in the computer — and they "
              "apply in a thermal too."),
            bild="begriff-luftraum",
            siehe=["freigabe", "flugflaeche", "karte"],
            formen=["Luftraum", "Lufträume", "Luftraumklassen", "airspace", "airspaces"]),

    begriff("freigabe", t("Freigabe", "Clearance"),
            t("Die Erlaubnis der Flugsicherung, einen kontrollierten Luftraum "
              "zu nutzen — erfragt über Funk mit Kennung, Position, Höhe und "
              "Absicht, bestätigt mit **wilco** oder durch Zurücklesen. Ohne "
              "sie bleibt der Luftraum C oder D zu, auch wenn die Thermik "
              "hineinträgt.\n\n"
              "Eine Freigabe gilt genau so, wie sie erteilt wurde: Höhe, "
              "Ort, Zeit.",
              "Air traffic control's permission to use controlled airspace — "
              "requested by radio with callsign, position, altitude and "
              "intention, acknowledged with **wilco** or by reading back. "
              "Without it airspace C or D stays closed, even if the thermal "
              "carries you in.\n\n"
              "A clearance applies exactly as given: altitude, place, time."),
            siehe=["luftraum", "funk"],
            formen=["Freigabe", "clearance", "wilco"]),

    begriff("qnh", t("QNH", "QNH"),
            t("Der auf Meereshöhe reduzierte Luftdruck des Platzes, in hPa. "
              "Mit QNH am Höhenmesser zeigt dieser die **Höhe über dem "
              "Meer**; am Platz steht dann die Platzhöhe. Daneben **QFE**: der "
              "Druck auf Platzhöhe, mit dem der Höhenmesser am Platz 0 zeigt.\n\n"
              "Unterwegs wird das QNH der Region gesetzt; das Standard-QNH "
              "1013,25 hPa gilt für Flugflächen.",
              "The airfield's pressure reduced to sea level, in hPa. With the "
              "QNH set, the altimeter shows **altitude above sea level**; on "
              "the ground it reads the airfield elevation. Also **QFE**: the "
              "pressure at airfield level, with which the altimeter reads 0 on "
              "the ground.\n\n"
              "En route the regional QNH is set; the standard setting "
              "1013.25 hPa applies to flight levels."),
            bild="begriff-hoehenbezuege",
            siehe=["flugflaeche", "hoehenmesser", "isa"],
            formen=["QNH", "QFE", "Höhenmessereinstellung", "altimeter setting"]),

    begriff("flugflaeche", t("Flugfläche", "Flight level"),
            t("Eine Höhe, gemessen mit dem Standarddruck **1013,25 hPa** am "
              "Höhenmesser, in Hundert Fuß: FL 100 sind 10 000 ft Standardhöhe. "
              "Oberhalb der **Übergangshöhe** (in Mitteleuropa meist 5 000 ft) "
              "fliegen alle nach Flugflächen, damit die Abstände stimmen, egal "
              "wie das Wetter ist.\n\n"
              "Luftraumgrenzen wie „FL 100“ gelten mit 1013 am Höhenmesser — "
              "mit QNH gerechnet kann man darüber sein, ohne es zu merken.",
              "An altitude measured with the standard setting **1013.25 hPa**, "
              "in hundreds of feet: FL 100 is 10,000 ft standard altitude. "
              "Above the **transition altitude** (usually 5,000 ft in central "
              "Europe) everyone flies by flight levels so the separation "
              "holds whatever the weather.\n\n"
              "Airspace limits like “FL 100” apply with 1013 set — reckoned "
              "with QNH you can be above it without noticing."),
            bild="begriff-hoehenbezuege",
            siehe=["qnh", "luftraum", "isa"],
            formen=["Flugfläche", "Flugflächen", "flight level", "flight levels", "transition altitude", "Übergangshöhe"]),

    begriff("hoehenmesser", t("Höhenmesser", "Altimeter"),
            t("Ein Barometer mit Höhenskala: Er misst den statischen Druck und "
              "zeigt die Höhe nach der Standardatmosphäre, bezogen auf den "
              "eingestellten Druck (QNH, QFE oder 1013). Bei warmer Luft zeigt "
              "er zu wenig, bei kalter zu viel — „vom Hoch ins Tief geht's "
              "schief“.\n\n"
              "Im Segelflug meist mit QNH, für den Endanflug zur Platzhöhe "
              "gerechnet.",
              "A barometer with a height scale: it measures static pressure "
              "and shows altitude by the standard atmosphere, referenced to "
              "the set pressure (QNH, QFE or 1013). In warm air it reads low, "
              "in cold air high — “from high to low, look out below”.\n\n"
              "In gliding usually set to QNH, with the final glide calculated "
              "to airfield elevation."),
            bild="skizze-luftsaeule",
            siehe=["qnh", "flugflaeche", "statik"],
            formen=["Höhenmesser", "altimeter"]),

    begriff("ausweichen", t("Ausweichregeln", "Right of way"),
            t("Wer wem ausweicht: Bei **Gegenkurs** beide nach rechts; wer "
              "den anderen **rechts** hat, weicht aus; **Überholen** nur "
              "rechts; wer tiefer ist, hat beim Landen Vorrang; am Hang hat "
              "Vorrang, wer den Hang rechts hat, und im Aufwind drehen alle "
              "wie der Erste.\n\n"
              "Die Regel gilt — aber das Segelflugzeug, das nicht weicht, "
              "wird vom anderen vielleicht nicht gesehen.",
              "Who gives way to whom: **head-on**, both turn right; the one "
              "who has the other on the **right** gives way; **overtaking** "
              "only on the right; the lower aircraft has priority when "
              "landing; on a ridge the one with the slope on its right has "
              "priority, and in a thermal everyone turns like the first.\n\n"
              "The rule applies — but the glider that does not give way may "
              "not be seen by the other."),
            bild="begriff-ausweichen",
            siehe=["platzrunde", "hangaufwind", "kurbeln"],
            formen=["Ausweichregeln", "Ausweichen", "ausweichen", "right of way", "give way"]),

    # -- Navigation ----------------------------------------------------------
    begriff("missweisung", t("Missweisung", "Variation"),
            t("Der Winkel zwischen geographisch Nord und magnetisch Nord am "
              "jeweiligen Ort — in Mitteleuropa derzeit 2–5 Grad Ost. "
              "**Rechtweisend** (Karte) plus westliche Missweisung = "
              "**missweisend** (Kompass); östliche wird abgezogen. Dazu kommt "
              "die **Deviation**, der Fehler des eingebauten Kompasses.\n\n"
              "Für den Segelflug mit GPS fast vergessen — bis das GPS ausfällt.",
              "The angle between true north and magnetic north at a place — "
              "in central Europe currently 2–5 degrees east. **True** (chart) "
              "plus westerly variation = **magnetic** (compass); easterly is "
              "subtracted. Add **deviation**, the error of the installed "
              "compass.\n\n"
              "Nearly forgotten in gliding with GPS — until the GPS fails."),
            bild="begriff-missweisung",
            siehe=["steuerkurs", "karte"],
            formen=["Missweisung", "Deviation", "variation", "deviation", "magnetic", "true"]),

    begriff("steuerkurs", t("Steuerkurs und Vorhalt", "Heading and drift correction"),
            t("Der **Kurs** ist die Richtung über Grund, die man fliegen "
              "will; der **Steuerkurs** die Richtung, in die die Nase zeigt. "
              "Bei Seitenwind unterscheiden sie sich um den **Vorhaltewinkel**: "
              "Man hält gegen den Wind vor, damit die Abdrift ausgeglichen "
              "wird.\n\n"
              "Faustformel: Vorhaltewinkel in Grad ≈ Windkomponente quer "
              "(km/h) × 60 / Fahrt (km/h).",
              "The **track** is the direction over the ground you want to "
              "fly; the **heading** the direction the nose points. In a "
              "crosswind they differ by the **drift correction angle**: you "
              "aim off into the wind to cancel the drift.\n\n"
              "Rule of thumb: drift angle in degrees ≈ crosswind component "
              "(km/h) × 60 / airspeed (km/h)."),
            bild="skizze-vorhalt",
            siehe=["missweisung", "karte"],
            formen=["Steuerkurs", "Vorhalt", "Vorhaltewinkel", "Kurs", "heading", "drift correction", "aiming off", "track"]),

    begriff("karte", t("Luftfahrtkarte", "Aeronautical chart"),
            t("Die ICAO-Karte 1:500 000: Gelände, Lufträume mit Grenzen in "
              "Fuß und Flugflächen, Hindernisse, Flugplätze, Funkfrequenzen. "
              "Im Segelflug ergänzt durch die Segelflugkarte mit Sektoren und "
              "Außenlandefeldern.\n\n"
              "Gelesen wird vom Großen zum Kleinen: Flusslauf, Stadt, "
              "Autobahn, dann der Platz. Das GPS ergänzt die Karte, es "
              "ersetzt sie nicht.",
              "The ICAO chart 1:500,000: terrain, airspace with limits in feet "
              "and flight levels, obstacles, airfields, radio frequencies. In "
              "gliding supplemented by the gliding chart with sectors and "
              "landable fields.\n\n"
              "Read from large to small: river, town, motorway, then the "
              "airfield. GPS supplements the chart; it does not replace it."),
            siehe=["orientierung", "luftraum", "missweisung"],
            formen=["Luftfahrtkarte", "Karte", "ICAO-Karte", "chart", "aeronautical chart"]),

    begriff("orientierung", t("Orientierung", "Orientation"),
            t("Zu wissen, wo man ist — mit Karte, Uhr und Blick: markante "
              "Linien (Flüsse, Bahnen, Autobahnen) als **Auffanglinien**, "
              "deren Richtung man nicht verfehlen kann, und Punkte an ihnen. "
              "Bei Zweifel: Höhe halten, nach bekannten Linien suchen, nicht "
              "raten.\n\n"
              "Die **räumliche Desorientierung** in Wolken ist etwas anderes: "
              "der Verlust des Oben und Unten — darum bleibt das "
              "Segelflugzeug draußen.",
              "Knowing where you are — with chart, clock and eyes: prominent "
              "lines (rivers, railways, motorways) as **catching lines** whose "
              "direction you cannot miss, and points along them. In doubt: "
              "hold height, look for known lines, do not guess.\n\n"
              "**Spatial disorientation** in cloud is something else: losing "
              "up and down — which is why the glider stays outside."),
            siehe=["karte", "steuerkurs"],
            formen=["Orientierung", "Auffanglinien", "Desorientierung", "orientation", "catching lines", "disorientation"]),

    # -- Mensch -----------------------------------------------------------------
    begriff("hypoxie", t("Hypoxie", "Hypoxia"),
            t("Sauerstoffmangel im Gewebe, weil der Luftdruck in der Höhe "
              "sinkt: ab etwa 3 000 m lassen Nachtsicht und Urteil nach, ab "
              "4 000 m Rechnen, Reaktion, Einsicht — und zwar ohne dass man "
              "es merkt, oft mit guter Laune. Über 3 000 m (10 000 ft) länger "
              "als 30 Minuten: Sauerstoff.\n\n"
              "In der Welle ist sie die stille Gefahr; die Regel heißt "
              "**zuerst Sauerstoff geben**, dann alles andere.",
              "Oxygen shortage in the tissues because the air pressure falls "
              "with height: from about 3,000 m night vision and judgement "
              "decline, from 4,000 m arithmetic, reaction, insight — without "
              "noticing, often in a good mood. Above 3,000 m (10,000 ft) for "
              "more than 30 minutes: oxygen.\n\n"
              "In wave it is the silent danger; the rule is **give oxygen "
              "first**, then everything else."),
            siehe=["hyperventilation", "welle", "druckausgleich"],
            formen=["Hypoxie", "hypoxia"]),

    begriff("hyperventilation", t("Hyperventilation", "Hyperventilation"),
            t("Zu schnelles, zu tiefes Atmen — aus Angst oder Anstrengung —, "
              "das zu viel **Kohlendioxid** abatmet: Kribbeln in Händen und "
              "Lippen, Schwindel, Krämpfe, im Extrem Ohnmacht. Die Symptome "
              "ähneln der Hypoxie, die Ursache ist das Gegenteil.\n\n"
              "Abhilfe: bewusst langsam atmen, sprechen, zählen. Bei "
              "Unsicherheit in der Höhe trotzdem zuerst Sauerstoff.",
              "Breathing too fast and too deep — from fear or exertion — "
              "blowing off too much **carbon dioxide**: tingling in hands and "
              "lips, dizziness, cramps, in the extreme fainting. The symptoms "
              "resemble hypoxia; the cause is the opposite.\n\n"
              "Remedy: breathe slowly and deliberately, talk, count. If in "
              "doubt at altitude, give oxygen first anyway."),
            siehe=["hypoxie"],
            formen=["Hyperventilation", "hyperventilation"]),

    begriff("druckausgleich", t("Druckausgleich", "Pressure equalisation"),
            t("Der Ausgleich zwischen Mittelohr und Außendruck über die "
              "Ohrtrompete: beim Steigen von selbst, beim Sinken nur durch "
              "Schlucken, Gähnen oder Valsalva (Nase zu, vorsichtig pressen). "
              "Mit Schnupfen bleibt die Trompete zu — Schmerz, Trommelfell "
              "in Gefahr.\n\n"
              "Erkältet nicht fliegen; im schnellen Sinkflug früh und oft "
              "ausgleichen.",
              "Equalising the middle ear with the outside pressure through the "
              "Eustachian tube: automatic when climbing, when descending only "
              "by swallowing, yawning or Valsalva (nose closed, press gently). "
              "With a cold the tube stays shut — pain, eardrum at risk.\n\n"
              "Do not fly with a cold; in a fast descent equalise early and "
              "often."),
            siehe=["hypoxie"],
            formen=["Druckausgleich", "pressure equalisation"]),

    begriff("entscheidung", t("Entscheiden im Cockpit", "Decision making"),
            t("Die Entscheidungen, die Flüge sicher machen, fallen früh und "
              "an vorher gesetzten Grenzen: Abflughöhe, Umkehrzeit, "
              "Außenlandehöhe, Wetterzeichen. Wer unterwegs erst abwägt, "
              "wägt unter Druck — und die **Get-home-itis** gewinnt.\n\n"
              "Werkzeug: Grenzen vorher festlegen, bei Erreichen handeln, "
              "nicht verhandeln. Und **IMSAFE** vor dem Flug: Illness, "
              "Medication, Stress, Alcohol, Fatigue, Eating.",
              "The decisions that make flights safe are made early and at "
              "limits set beforehand: departure height, turn-back time, field "
              "landing height, weather signs. Whoever weighs things up en "
              "route weighs them under pressure — and **get-home-itis** "
              "wins.\n\n"
              "Tools: set the limits beforehand, act when reached, do not "
              "negotiate. And **IMSAFE** before the flight: illness, "
              "medication, stress, alcohol, fatigue, eating."),
            siehe=["risiko", "planung", "aussenlandung"],
            formen=["Entscheidung", "Entscheidungen", "entscheiden", "IMSAFE", "Get-home-itis", "decision", "decide"]),

    begriff("risiko", t("Risiko", "Risk"),
            t("Risiko ist Wahrscheinlichkeit mal Folge. Im Segelflug sind die "
              "großen Folgen bekannt — Überziehen tief, Außenlandung zu spät, "
              "Gewitter, Zusammenstoß im Pulk — und ihre Wahrscheinlichkeit "
              "hängt fast immer von einer früheren Entscheidung ab.\n\n"
              "Die Gefahren, der Reihe nach: tief und langsam, spät "
              "entschieden, Wetter unterschätzt, nicht hinausgeschaut.",
              "Risk is probability times consequence. In gliding the big "
              "consequences are known — stall low down, field landing too "
              "late, thunderstorm, collision in the gaggle — and their "
              "probability almost always depends on an earlier decision.\n\n"
              "The dangers, in order: low and slow, decided late, weather "
              "underestimated, not looking out."),
            siehe=["entscheidung", "ueberziehen", "cumulonimbus"],
            formen=["Risiko", "Gefahren", "risk", "dangers"]),

    # -- Instrumente ----------------------------------------------------------
    begriff("staudruck", t("Staudruck", "Pitot pressure"),
            t("Der Druck, den die anströmende Luft im Staurohr aufbaut — er "
              "wächst mit dem Quadrat der Fahrt und mit der Luftdichte. Der "
              "**Fahrtmesser** vergleicht ihn mit dem statischen Druck und "
              "zeigt die **angezeigte** Fahrt (IAS), die in dünner Luft "
              "kleiner ist als die wahre.\n\n"
              "Gut so: Überziehen und Grenzen gelten nach der angezeigten Fahrt.",
              "The pressure the oncoming air builds up in the pitot tube — it "
              "grows with the square of the speed and with air density. The "
              "**airspeed indicator** compares it with static pressure and "
              "shows **indicated** airspeed (IAS), which in thin air is lower "
              "than true.\n\n"
              "Just as well: stalling and limits go by indicated airspeed."),
            bild="begriff-staudruck",
            siehe=["statik", "fahrtmesser", "variometer"],
            formen=["Staudruck", "pitot pressure", "dynamic pressure"]),

    begriff("statik", t("Statischer Druck", "Static pressure"),
            t("Der Luftdruck der umgebenden Luft, abgenommen an Öffnungen "
              "seitlich am Rumpf, wo die Strömung weder staut noch saugt. Er "
              "speist Höhenmesser und Variometer und ist die Bezugsgröße des "
              "Fahrtmessers.\n\n"
              "Eine verstopfte Statik lässt den Höhenmesser stehen und den "
              "Fahrtmesser im Steigflug zu viel zeigen — die "
              "**Verstopfungsfälle** gehören zum Instrumentenwissen.",
              "The pressure of the surrounding air, taken at ports on the side "
              "of the fuselage where the flow neither piles up nor sucks. It "
              "feeds altimeter and variometer and is the reference for the "
              "airspeed indicator.\n\n"
              "A blocked static leaves the altimeter stuck and makes the "
              "airspeed indicator over-read in a climb — the **blockage "
              "cases** belong to instrument knowledge."),
            bild="begriff-staudruck",
            siehe=["staudruck", "hoehenmesser", "variometer"],
            formen=["Statik", "Statischer Druck", "statischer Druck", "static pressure", "static"]),

    begriff("fahrtmesser", t("Fahrtmesser", "Airspeed indicator"),
            t("Zeigt die Fahrt aus der Differenz von Staudruck und statischem "
              "Druck. Die Markierungen: grüner Bogen normal, gelber nur in "
              "ruhiger Luft, roter Strich nie überschreiten, und die "
              "**Manövergeschwindigkeit** als Grenze für volle Ruderausschläge.\n\n"
              "In der Thermik ist er der wichtigste Blick nach dem "
              "Horizont: Fahrt ist Leben, besonders tief.",
              "Shows airspeed from the difference between pitot and static "
              "pressure. The markings: green arc normal, yellow only in smooth "
              "air, red line never to be exceeded, and the **manoeuvring "
              "speed** as the limit for full control deflection.\n\n"
              "In a thermal it is the most important glance after the "
              "horizon: speed is life, especially low down."),
            bild="begriff-staudruck",
            siehe=["staudruck", "statik", "ueberziehen"],
            formen=["Fahrtmesser", "airspeed indicator", "ASI"]),

    begriff("variometer", t("Variometer", "Variometer"),
            t("Das Steig- und Sinkmessgerät: Es zeigt die Änderung des "
              "statischen Drucks als Vertikalgeschwindigkeit in m/s. Das "
              "einfache Variometer zeigt beim Hochziehen Steigen an, das nur "
              "aus der Fahrt kommt; das **TE-Variometer** (Totalenergie) "
              "rechnet das heraus und zeigt nur das Steigen der Luft.\n\n"
              "Im Segelflug das Instrument, nach dem zentriert und die "
              "Sollfahrt gewählt wird — mit Ton, damit der Blick draußen "
              "bleibt.",
              "The climb and sink instrument: it shows the change of static "
              "pressure as vertical speed in m/s. The simple variometer shows "
              "a climb when you pull up that comes only from speed; the "
              "**total energy variometer** removes that and shows only the "
              "air's climb.\n\n"
              "In gliding the instrument you centre by and choose the speed "
              "to fly with — with audio, so the eyes stay outside."),
            bild="begriff-variometer",
            siehe=["statik", "kurbeln", "mccready"],
            formen=["Variometer", "TE-Variometer", "Vario", "variometer", "total energy variometer"]),

    # -- Betrieb und Funk -----------------------------------------------------
    begriff("seilriss", t("Seilriss", "Cable break"),
            t("Das Reißen des Schleppseils im Windenstart oder Flugzeugschlepp "
              "— der am meisten geübte Notfall. **Erstens und immer: "
              "nachdrücken**, aus dem steilen Steigflug in die Normalfluglage; "
              "zweitens Fahrt prüfen, Seilrest ausklinken; drittens "
              "entscheiden: geradeaus landen (unter der Entscheidungshöhe) "
              "oder verkürzte Platzrunde.\n\n"
              "Entschieden wird nach Höhe, nicht nach Hoffnung.",
              "The breaking of the launch cable on a winch launch or aerotow — "
              "the most practised emergency. **First and always: push**, from "
              "the steep climb into the normal attitude; second check speed, "
              "release the cable remnant; third decide: land straight ahead "
              "(below decision height) or a shortened circuit.\n\n"
              "The decision follows height, not hope."),
            bild="begriff-seilriss",
            siehe=["entscheidungshoehe", "windenstart", "flugzeugschlepp"],
            formen=["Seilriss", "cable break", "rope break"]),

    begriff("entscheidungshoehe", t("Entscheidungshöhe", "Decision height"),
            t("Die vor dem Start festgelegte Höhe, unter der nach einem "
              "Seilriss nur geradeaus gelandet wird und über der eine "
              "verkürzte Platzrunde oder ein Gegenanflug möglich ist — "
              "je nach Platz und Wind, oft um 100 m im Windenstart.\n\n"
              "Sie ist vorher zu wissen: Nach dem Riss bleibt keine Zeit "
              "zum Rechnen.",
              "The height fixed before launch below which, after a cable "
              "break, you only land straight ahead and above which a "
              "shortened circuit or a downwind landing is possible — "
              "depending on airfield and wind, often around 100 m on a winch "
              "launch.\n\n"
              "It must be known beforehand: after the break there is no time "
              "for sums."),
            bild="begriff-seilriss",
            siehe=["seilriss", "sicherheitshoehe"],
            formen=["Entscheidungshöhe", "decision height"]),

    begriff("funk", t("Sprechfunk", "Radio telephony"),
            t("Der Sprechfunk nach festen Regeln: zuerst die Gegenstelle, dann "
              "die eigene Kennung, dann die Nachricht — kurz, in "
              "Standardphrasen, mit dem ICAO-Alphabet für Buchstaben. "
              "**verstanden** (roger) heißt gehört, **wilco** heißt "
              "ausführen, **wiederholen Sie** (say again) heißt nicht gehört.\n\n"
              "Vor dem Senden hören, nach dem Senden auf die Antwort warten; "
              "und bei Zweifel lieber fragen als raten.",
              "Radio telephony by fixed rules: the station called first, then "
              "your own callsign, then the message — short, in standard "
              "phrases, with the ICAO alphabet for letters. **Roger** means "
              "heard, **wilco** means will comply, **say again** means not "
              "heard.\n\n"
              "Listen before transmitting, wait for the reply after; and in "
              "doubt ask rather than guess."),
            siehe=["notruf", "freigabe"],
            formen=["Sprechfunk", "Funk", "radio", "radio telephony"]),

    begriff("notruf", t("Notruf", "Distress call"),
            t("Die drei Dringlichkeitsstufen: **MAYDAY** (dreimal) bei "
              "unmittelbarer Lebensgefahr, **PAN PAN** (dreimal) bei "
              "Dringlichkeit ohne unmittelbare Gefahr, sonst normaler Funk. "
              "Dazu Kennung, Lage, Position, Absicht — auf der aktuellen "
              "Frequenz oder 121,5 MHz.\n\n"
              "Transponder: **7700** Notfall, **7600** Funkausfall, **7500** "
              "Entführung. Wer ruft, bekommt Vorrang auf der Frequenz.",
              "The three urgency levels: **MAYDAY** (three times) for "
              "immediate danger to life, **PAN PAN** (three times) for urgency "
              "without immediate danger, otherwise normal radio. Then "
              "callsign, situation, position, intention — on the current "
              "frequency or 121.5 MHz.\n\n"
              "Transponder: **7700** emergency, **7600** radio failure, "
              "**7500** hijack. Whoever calls gets priority on the frequency."),
            siehe=["funk"],
            formen=["Notruf", "MAYDAY", "PAN PAN", "distress call", "distress"]),
]
