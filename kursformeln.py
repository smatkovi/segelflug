# -*- coding: utf-8 -*-
"""Die Formeln des Kurses, zweimal aufgeschrieben.

Oben steht die Zeile so, wie sie im Lehrtext oder in der Herleitung
vorkommt, darunter dieselbe Sache gesetzt. Beides zusammen, weil das eine
ohne das andere nur halb hilft: Die gesetzte Formel zeigt die Struktur auf
einen Blick, die Textzeile ist die, die man im Kurs wiederfindet.

Zu jeder Formel steht, woher sie kommt und wo sie aufhoert zu gelten. Eine
Faustformel, die man nur auswendig kann, hilft genau so lange, wie die Lage
zum Lehrbuch passt.

Gesetzt werden die Formeln beim Bauen, siehe tools/formeln.py.
"""
from __future__ import unicode_literals


def t(de, en):
    return {"de": de, "en": en}


def formel(zeile, tex, untertitel, erklaerung):
    return {"code": zeile, "tex": tex, "untertitel": untertitel,
            "erklaerung": erklaerung}


KURSFORMELN = {

    "w-basis": [
        formel(
            "Höhe = Spreizung × 125 m/°C",
            r"$h \approx (T - T_d)\cdot 125\,\frac{\mathrm{m}}{\mathrm{K}}$",
            t("Die Basis aus Temperatur und Taupunkt",
              "Cloud base from temperature and dew point"),
            t("Trockene Luft kühlt beim Steigen um rund 1 °C je 100 m, der "
              "Taupunkt sinkt dabei nur um etwa 0,2 °C je 100 m. Die "
              "Spreizung schließt sich also mit 0,8 °C je 100 m, und "
              "100 ÷ 0,8 sind die 125 m je Grad. **Wo sie bricht:** Sie "
              "unterstellt, dass das Luftpaket vom Boden aufsteigt und "
              "unterwegs nichts dazumischt. Unter einer Inversion, bei "
              "Advektion feuchter Luft oder über Wasser stimmt sie nicht.",
              "Dry air cools by about 1 °C per 100 m as it rises, while the "
              "dew point falls by only some 0.2 °C per 100 m. The spread "
              "therefore closes at 0.8 °C per 100 m, and 100 ÷ 0.8 gives the "
              "125 m per degree. **Where it breaks:** it assumes a parcel "
              "rising from the ground with nothing mixing in on the way. "
              "Under an inversion, with moist air advected in, or over "
              "water, it does not hold.")),
    ],

    "a-polare": [
        formel(
            "Strecke / Höhe = L / D = E",
            r"$E = \frac{L}{D} = \frac{v}{w}$",
            t("Gleitzahl: dieselbe Zahl aus Kräften und aus Geschwindigkeiten",
              "Glide ratio: the same number from forces and from speeds"),
            t("Im stationären Gleitflug halten sich die Kräfte das "
              "Gleichgewicht: längs der Bahn `G·sin γ = D`, quer dazu "
              "`G·cos γ = L`. Geteilt ergibt das `tan γ = D/L`, und Strecke "
              "durch Höhe ist `1/tan γ`, also `L/D`. Weil das Dreieck aus "
              "Vorwärts- und Sinkgeschwindigkeit denselben Winkel hat, ist "
              "dieselbe Zahl auch `v/w` -- deshalb liest man die Gleitzahl "
              "aus der Polare ab und muss keine Kräfte messen. **Gilt für "
              "ruhige Luft:** Im Steigen oder Sinken der Luftmasse zählt die "
              "Bewegung über Grund, nicht die durch die Luft.",
              "In steady gliding flight the forces balance: along the path "
              "`G·sin γ = D`, across it `G·cos γ = L`. Dividing gives "
              "`tan γ = D/L`, and distance over height is `1/tan γ`, that is "
              "`L/D`. Because the triangle of forward and sinking speed has "
              "the same angle, the same number is also `v/w` -- which is why "
              "the glide ratio is read off the polar and no force has to be "
              "measured. **Holds for still air:** in rising or sinking air "
              "what counts is the movement over the ground, not through the "
              "air.")),
    ],

    "a-ueberziehen": [
        formel(
            "q = ½·ρ·v²",
            r"$q = \frac{1}{2}\rho v^{2}$",
            t("Der Staudruck steckt in jeder Luftkraft",
              "Dynamic pressure is in every aerodynamic force"),
            t("Je Sekunde trifft die Masse `ρ·A·v` auf die Fläche `A`, und "
              "jedes Kilogramm davon bringt `½v²` an Bewegungsenergie mit. "
              "Leistung durch Geschwindigkeit ist Kraft, Kraft durch Fläche "
              "ist Druck -- übrig bleibt `½ρv²`. Die Einheitenprobe: "
              "kg/m³ · m²/s² = N/m² = Pa. Entscheidend ist das Quadrat: "
              "doppelte Fahrt, vierfache Kraft.",
              "Each second the mass `ρ·A·v` arrives at the area `A`, and "
              "every kilogram of it brings `½v²` of kinetic energy. Power "
              "divided by speed is force, force divided by area is pressure "
              "-- what remains is `½ρv²`. The unit check: "
              "kg/m³ · m²/s² = N/m² = Pa. The square is what matters: twice "
              "the speed, four times the force.")),
        formel(
            "n = 1 / cos φ",
            r"$n = \frac{1}{\cos\varphi}$",
            t("Lastvielfaches in der Kurve",
              "Load factor in a turn"),
            t("In der stationären Kurve muss die senkrechte Komponente des "
              "Auftriebs weiter das ganze Gewicht tragen: `L·cos φ = G`, "
              "also `L = G / cos φ`. Bei 45° Querlage sind das 1,41 G, bei "
              "60° schon 2 G. Das Lastvielfache hängt **nur** von der "
              "Querlage ab -- nicht vom Radius, nicht von der "
              "Geschwindigkeit und nicht vom Gewicht.",
              "In a steady turn the vertical component of the lift must "
              "still carry the whole weight: `L·cos φ = G`, so "
              "`L = G / cos φ`. At 45° of bank that is 1.41 G, at 60° "
              "already 2 G. The load factor depends **only** on the bank "
              "angle -- not on the radius, not on the speed and not on the "
              "weight.")),
        formel(
            "v_kurve = v_s · √n",
            r"$v_{S,\varphi} = v_S\sqrt{n} = \frac{v_S}{\sqrt{\cos\varphi}}$",
            t("Überziehgeschwindigkeit in der Kurve",
              "Stalling speed in a turn"),
            t("Der Auftrieb wächst mit `v²`, also verlangt das n-fache "
              "Gewicht die √n-fache Geschwindigkeit. Bei 60° Querlage ist "
              "n = 2, die Überziehgeschwindigkeit damit 1,41-mal so hoch. "
              "Deshalb ist eng und langsam die gefährliche Kombination, und "
              "deshalb steht der Fahrtmesser in der Platzrunde nie am "
              "unteren Anschlag.",
              "Lift grows with `v²`, so n times the weight needs √n times "
              "the speed. At 60° of bank n = 2 and the stalling speed is "
              "1.41 times as high. That is why tight and slow is the "
              "dangerous combination, and why the airspeed indicator never "
              "sits at its lower limit in the circuit.")),
    ],

    "l-schwerpunkt": [
        formel(
            "x_s = Σ (m_i · x_i) / Σ m_i",
            r"$x_S = \frac{\sum m_i x_i}{\sum m_i}$",
            t("Der Schwerpunkt ist ein gewogener Mittelwert",
              "The centre of gravity is a weighted mean"),
            t("Ein Moment ist Kraft mal Hebelarm. Der Schwerpunkt ist der "
              "Punkt, an dem alle Massen zusammengefasst dasselbe Moment "
              "erzeugen wie einzeln: `(Σm)·x_S = Σ(m·x)`. Ein schwerer Pilot "
              "zieht ihn weit nach vorn, Wasserballast im Flügel kaum -- der "
              "sitzt nahe am Schwerpunkt. **Warum es beide Grenzen gibt:** "
              "zu weit vorn heißt schwer abfangbar, zu weit hinten heißt "
              "nicht mehr abfangbar.",
              "A moment is force times lever arm. The centre of gravity is "
              "the point at which all masses taken together produce the same "
              "moment as they do separately: `(Σm)·x_S = Σ(m·x)`. A heavy "
              "pilot pulls it far forward, water ballast in the wing hardly "
              "at all -- it sits close to the centre of gravity. **Why there "
              "are two limits:** too far forward means hard to flare, too "
              "far aft means impossible to recover.")),
    ],

    "l-startstrecke": [
        formel(
            "v = √( 2G / (ρ · S · c_A) )",
            r"$v = \sqrt{\frac{2G}{\rho\,S\,c_A}}$",
            t("Abhebegeschwindigkeit, und warum sie mit der Höhe steigt",
              "Lift-off speed, and why it rises with altitude"),
            t("Abgehoben wird, wenn der Auftrieb das Gewicht erreicht: "
              "`½ρv²·S·c_A = G`. Nach `v` aufgelöst steht dort `v ∝ 1/√ρ`. "
              "An einem heißen Tag auf 1000 m ist die Dichte rund 10 % "
              "kleiner, die **wahre** Geschwindigkeit also etwa 5 % höher -- "
              "und weil die Strecke mit `v²` geht, wird der Start gut 10 % "
              "länger. Der Fahrtmesser zeigt davon nichts: Er misst "
              "denselben Staudruck und damit dieselbe angezeigte Zahl.",
              "You lift off when the lift reaches the weight: "
              "`½ρv²·S·c_A = G`. Solved for `v` this says `v ∝ 1/√ρ`. On a "
              "hot day at 1000 m the density is some 10 % lower, so the "
              "**true** speed is about 5 % higher -- and because the "
              "distance goes with `v²`, the take-off run grows by a good "
              "10 %. The airspeed indicator shows none of this: it measures "
              "the same dynamic pressure and thus the same indicated "
              "number.")),
    ],

    "n-kurse": [
        formel(
            "α [°] ≈ (v_q / v) × 57,3",
            r"$\alpha \approx \frac{v_q}{v}\cdot 57{,}3^{\circ}$",
            t("Vorhaltewinkel gegen den Querwind",
              "Drift correction angle for a crosswind"),
            t("Für kleine Winkel ist `sin α ≈ α` im Bogenmaß, und ein "
              "Bogenmaß sind 57,3°. Also Querwindanteil durch "
              "Eigengeschwindigkeit, mal 57,3 -- in der Praxis mal 60, das "
              "rechnet sich im Kopf und liegt nur 5 % daneben. Gut bis etwa "
              "20°; darüber wird der Sinus merklich kleiner als der Winkel "
              "und die Faustformel hält zuwenig vor.",
              "For small angles `sin α ≈ α` in radians, and one radian is "
              "57.3°. So crosswind component divided by airspeed, times 57.3 "
              "-- in practice times 60, which can be done in the head and is "
              "only 5 % off. Good up to about 20°; beyond that the sine "
              "becomes noticeably smaller than the angle and the rule of "
              "thumb under-corrects.")),
    ],

    "r-hoehenmesser": [
        formel(
            "dh = dp / (ρ·g) ≈ 8,3 m je hPa",
            r"$\Delta h = \frac{\Delta p}{\rho\,g} \approx 8{,}3\ \mathrm{m/hPa}$",
            t("Warum ein Hektopascal acht Meter sind",
              "Why one hectopascal is eight metres"),
            t("Eine Luftsäule drückt mit `ρ·g·h`. Ein Hektopascal sind "
              "100 Pa; geteilt durch 1,225 kg/m³ × 9,81 m/s² ergibt 8,3 m. "
              "Das gilt **in Bodennähe**: Oben ist die Luft dünner, und "
              "dasselbe Hektopascal entspricht dort einer größeren Höhe. "
              "Ein um 10 hPa falsch gestellter Höhenmesser zeigt unten 83 m "
              "falsch -- in der Höhe mehr, und immer in die unangenehme "
              "Richtung, wenn der Druck unterwegs gefallen ist.",
              "A column of air presses with `ρ·g·h`. One hectopascal is "
              "100 Pa; divided by 1.225 kg/m³ × 9.81 m/s² that gives 8.3 m. "
              "This holds **near the ground**: higher up the air is thinner "
              "and the same hectopascal corresponds to a greater height. An "
              "altimeter set 10 hPa wrong reads 83 m wrong down low -- more "
              "up high, and always in the unpleasant direction if the "
              "pressure has fallen on the way.")),
    ],
}
