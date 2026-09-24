# -*- coding: utf-8 -*-
"""Herleitungen zu den Karteikarten.

Auf einigen Karten steht eine Rechnung, und eine Rechnung ohne Herleitung
ist eine Zahl zum Auswendiglernen. Im Cockpit hilft das genau so lange, wie
die Lage zur Aufgabe passt -- und dann nicht mehr.

Deshalb haengt an jeder solchen Karte hier die Herleitung: woher die Formel
kommt, welche Annahme sie macht, und was passiert, wenn die Annahme nicht
stimmt. Sie steht **in der Loesung**, nicht in der Frage; vorher waere sie
die Antwort. Die Skizze daneben ist dieselbe, die auch an der Herleitung im
Lehrtext haengt (tools/skizzen.py).

Der Schluessel ist der deutsche Fragetext. tools/make-kurs.py bricht ab,
wenn ein Schluessel ins Leere zeigt.

Die Texte stehen zweisprachig direkt hier, wie der ganze Kurs -- segelflug
hat keine Uebersetzungstabelle daneben.
"""
from __future__ import unicode_literals

from kurs import t


BASIS = t(
 "## Woher die 125 Meter je Grad kommen\n\n"
 "`ϑ` Temperatur am Boden, °C. `ϑ_d` Taupunkt am Boden, °C. "
 "`h` Höhe der Wolkenbasis über Grund, m. `Γ_d` "
 "Trockenadiabate, K/100 m. `Γ_t` Taupunktgradient, K/100 m.\n\n"
 "Ein Luftpaket, das aufsteigt, kühlt sich ab, weil es sich gegen den "
 "fallenden Druck ausdehnt und dabei Arbeit leistet. Solange nichts "
 "kondensiert, ist das die **Trockenadiabate**: `Γ_d = g / c_p = "
 "9,81 / 1005 ≈ 0,00976 K/m`, also rund **1 K je 100 m**.\n\n"
 "Der Taupunkt fällt beim Aufsteigen auch, aber viel langsamer: das "
 "Paket behält seinen Wasserdampf, nur die Dichte nimmt ab. Gemessen sind "
 "das rund **0,2 K je 100 m**.\n\n"
 "Die Wolke entsteht, wo sich beide treffen, also wo die anfängliche "
 "Spreizung `ϑ − ϑ_d` aufgebraucht ist. Je 100 m schliesst "
 "sich die Lücke um `1 − 0,2 = 0,8 K`:\n\n"
 "`h = (ϑ − ϑ_d) / 0,8 · 100 m = (ϑ − ϑ_d) · 125 m`\n\n"
 "Die 125 sind also nichts Gemessenes, sondern `100 / 0,8`. Mit 24 °C "
 "und 9 °C: `15 · 125 = 1875 m`.\n\n"
 "Die Annahme dahinter ist, dass die aufsteigende Luft dieselbe ist, die "
 "unten gemessen wurde. Bei Advektion, nach einem Schauer oder über "
 "nassem Boden stimmt das nicht — dann liegt die Basis tiefer als "
 "gerechnet.",

 "## Where the 125 metres per degree come from\n\n"
 "`ϑ` temperature at the ground, °C. `ϑ_d` dew point at the "
 "ground, °C. `h` height of the cloud base above ground, m. "
 "`Γ_d` dry adiabatic lapse rate, K/100 m. `Γ_t` dew point "
 "lapse rate, K/100 m.\n\n"
 "A parcel of air that rises cools down, because it expands against the "
 "falling pressure and does work in doing so. As long as nothing "
 "condenses, that is the **dry adiabatic lapse rate**: `Γ_d = g / c_p "
 "= 9.81 / 1005 ≈ 0.00976 K/m`, so about **1 K per 100 m**.\n\n"
 "The dew point falls as the parcel rises as well, but much more slowly: "
 "the parcel keeps its water vapour, only the density drops. Measurements "
 "give about **0.2 K per 100 m**.\n\n"
 "The cloud forms where the two meet, that is where the initial spread "
 "`ϑ − ϑ_d` has been used up. Every 100 m the gap closes by "
 "`1 − 0.2 = 0.8 K`:\n\n"
 "`h = (ϑ − ϑ_d) / 0.8 · 100 m = (ϑ − ϑ_d) · 125 m`\n\n"
 "So the 125 are not measured, they are `100 / 0.8`. With 24 °C and "
 "9 °C: `15 · 125 = 1875 m`.\n\n"
 "The assumption behind it is that the rising air is the same air that was "
 "measured at the ground. With advection, after a shower or over wet "
 "ground that does not hold — and then the base is lower than the sum "
 "says.")

GLEITZAHL = t(
 "## Was die Gleitzahl überhaupt ist\n\n"
 "`E` Gleitzahl, dimensionslos. `s` zurückgelegte Strecke über Grund, "
 "m. `h` dabei verlorene Höhe, m. `A` Auftrieb, N. `W` Widerstand, N.\n\n"
 "Im stationären Gleitflug hängt das Flugzeug an nichts als der "
 "Schwerkraft; sie zerlegt sich in eine Komponente, die den Widerstand "
 "überwindet, und eine, die den Auftrieb trägt. Aus dem ähnlichen "
 "Dreieck von Kräften und Wegen folgt unmittelbar\n\n"
 "`E = s / h = A / W`\n\n"
 "Die Gleitzahl ist also zweierlei in einem: das Verhältnis von Strecke "
 "zu Höhe **und** das Verhältnis von Auftrieb zu Widerstand. Deshalb "
 "steht sie im Handbuch und nicht der Gleitwinkel.\n\n"
 "Umgestellt: `s = E · h`. Nutzbar ist nur die Höhe über der "
 "Ankunftshöhe, also `1200 − 300 = 900 m`, und damit "
 "`s = 38 · 900 m = 34,2 km`.\n\n"
 "Die Annahme ist ruhige Luft und ein sauberes Flugzeug. Mücken, Regen "
 "und jedes Grad Abweichung von der besten Geschwindigkeit drücken `E`; "
 "Gegenwind auch, weil `s` über Grund zählt und die Höhe in der Zeit "
 "verbraucht wird. Deshalb rechnet man mit einer schlechteren Zahl als im "
 "Prospekt.",

 "## What the glide ratio actually is\n\n"
 "`E` glide ratio, dimensionless. `s` distance covered over the ground, m. "
 "`h` height lost while doing so, m. `A` lift, N. `W` drag, N.\n\n"
 "In a steady glide the aircraft hangs on nothing but gravity; that force "
 "splits into one component overcoming the drag and one carrying the lift. "
 "From the similar triangle of forces and distances it follows at once "
 "that\n\n"
 "`E = s / h = A / W`\n\n"
 "So the glide ratio is two things at once: the ratio of distance to "
 "height **and** the ratio of lift to drag. That is why the handbook gives "
 "it rather than the glide angle.\n\n"
 "Rearranged: `s = E · h`. Only the height above the arrival height is "
 "usable, so `1200 − 300 = 900 m`, and therefore "
 "`s = 38 · 900 m = 34.2 km`.\n\n"
 "The assumption is still air and a clean aircraft. Flies, rain and every "
 "degree away from the best speed push `E` down; so does a headwind, "
 "because `s` counts over the ground while the height is spent in time. "
 "That is why you reckon with a worse number than the brochure's.")

KURVENLAST = t(
 "## Warum die Wurzel und nicht der Faktor selbst\n\n"
 "`n` Lastvielfaches, dimensionslos. `φ` Schräglage, Grad. "
 "`v_s` Überziehgeschwindigkeit, km/h. `A` Auftrieb, N. `m` Masse, kg. "
 "`g` Fallbeschleunigung, m/s². `ρ` Luftdichte, kg/m³. "
 "`S` Flügelfläche, m². `c_A` Auftriebsbeiwert, dimensionslos.\n\n"
 "**Erstens das Lastvielfache.** Im sauberen Kurvenflug steht der Auftrieb "
 "senkrecht auf den Flügeln, also um `φ` gekippt. Seine senkrechte "
 "Komponente `A · cos φ` muss das Gewicht `m · g` tragen, sonst "
 "sinkt das Flugzeug:\n\n"
 "`A · cos φ = m · g`  →  `n = A / (m · g) = 1 / cos φ`\n\n"
 "Bei 45°: `1 / cos 45° = 1,41`. (Die bekannten 2,0 gehören zu "
 "60°, denn `cos 60° = 0,5`.)\n\n"
 "**Zweitens die Geschwindigkeit.** Der Auftrieb wächst mit dem Quadrat "
 "der Geschwindigkeit: `A = c_A · ½ ρ v² · S`. Überzogen wird "
 "bei höchstem `c_A`; gebraucht wird jetzt der `n`-fache Auftrieb, also "
 "muss `v²` das `n`-fache sein und `v` selbst das `√n`-fache:\n\n"
 "`v_s(φ) = v_s · √n = v_s / √(cos φ)`\n\n"
 "Bei 45°: `√1,41 ≈ 1,19`, also **rund 19 Prozent mehr**. Die 41 "
 "Prozent sind das Lastvielfache und nicht die Geschwindigkeit — wer "
 "beides verwechselt, rechnet sich in der Platzrunde eine Reserve herbei, "
 "die es nicht gibt.",

 "## Why the square root and not the factor itself\n\n"
 "`n` load factor, dimensionless. `φ` angle of bank, degrees. "
 "`v_s` stall speed, km/h. `A` lift, N. `m` mass, kg. `g` acceleration of "
 "gravity, m/s². `ρ` air density, kg/m³. `S` wing area, m². "
 "`c_A` lift coefficient, dimensionless.\n\n"
 "**First the load factor.** In a clean turn the lift stands square to the "
 "wings, so it is tilted by `φ`. Its vertical component "
 "`A · cos φ` has to carry the weight `m · g`, otherwise the "
 "aircraft descends:\n\n"
 "`A · cos φ = m · g`  →  `n = A / (m · g) = 1 / cos φ`\n\n"
 "At 45°: `1 / cos 45° = 1.41`. (The familiar 2.0 belongs to 60°, "
 "because `cos 60° = 0.5`.)\n\n"
 "**Then the speed.** Lift grows with the square of the speed: "
 "`A = c_A · ½ ρ v² · S`. You stall at the highest `c_A`; what "
 "is needed now is `n` times the lift, so `v²` must be `n` times as big "
 "and `v` itself `√n` times:\n\n"
 "`v_s(φ) = v_s · √n = v_s / √(cos φ)`\n\n"
 "At 45°: `√1.41 ≈ 1.19`, so **about 19 per cent more**. The 41 "
 "per cent are the load factor and not the speed — confuse the two and "
 "you talk yourself into a margin in the circuit that is not there.")

SCHWERPUNKT = t(
 "## Warum man Momente addiert und nicht Massen\n\n"
 "`mᵢ` Einzelmasse, kg. `xᵢ` Hebelarm dieser Masse hinter dem "
 "Bezugspunkt, mm. `Mᵢ = mᵢ · xᵢ` ihr Moment, kg·mm. "
 "`x_S` Lage des Gesamtschwerpunkts hinter dem Bezugspunkt, mm.\n\n"
 "Der Schwerpunkt ist der Punkt, um den sich alle Drehwirkungen aufheben. "
 "Ein Gewicht `mᵢ` im Abstand `xᵢ` dreht mit dem Moment "
 "`mᵢ · xᵢ`; ersetzt man alle Gewichte durch ein einziges im "
 "Schwerpunkt, muss dieselbe Drehwirkung herauskommen:\n\n"
 "`(Σ mᵢ) · x_S = Σ (mᵢ · xᵢ)`  →  "
 "`x_S = Σ Mᵢ / Σ mᵢ`\n\n"
 "Der Schwerpunkt ist also ein **mit den Massen gewichteter Mittelwert der "
 "Hebelarme** — und deshalb darf man Momente addieren, Hebelarme aber "
 "nicht: der Mittelwert zweier Arme wäre nur dann richtig, wenn beide "
 "Massen gleich gross wären.\n\n"
 "`x_S = (75 000 + 70 · 100) / (250 + 70) = 82 000 / 320 = 256,25 mm`\n\n"
 "Die Zahl allein sagt noch nichts. Sie muss gegen die Grenzen im Handbuch "
 "geprüft werden, und die gelten fuer die Gesamtmasse, die dabei "
 "herauskommt — zu weit hinten heisst träges Abfangen und schlechtes "
 "Trudelverhalten, zu weit vorn heisst Ruderweg, der nicht reicht.",

 "## Why you add moments and not masses\n\n"
 "`mᵢ` individual mass, kg. `xᵢ` arm of that mass behind the datum, "
 "mm. `Mᵢ = mᵢ · xᵢ` its moment, kg·mm. `x_S` position of "
 "the overall centre of gravity behind the datum, mm.\n\n"
 "The centre of gravity is the point about which all turning effects "
 "cancel. A weight `mᵢ` at a distance `xᵢ` turns with the moment "
 "`mᵢ · xᵢ`; replace all the weights by a single one at the centre "
 "of gravity and the same turning effect must come out:\n\n"
 "`(Σ mᵢ) · x_S = Σ (mᵢ · xᵢ)`  →  "
 "`x_S = Σ Mᵢ / Σ mᵢ`\n\n"
 "So the centre of gravity is a **mass-weighted mean of the arms** — and "
 "that is why moments may be added but arms may not: the mean of two arms "
 "would only be right if both masses were equal.\n\n"
 "`x_S = (75,000 + 70 · 100) / (250 + 70) = 82,000 / 320 = 256.25 mm`\n\n"
 "The number by itself says nothing yet. It has to be checked against the "
 "limits in the handbook, and those apply to the total mass that comes out "
 "with it — too far aft means sluggish recovery and poor spin behaviour, "
 "too far forward means running out of elevator.")

VORHALT = t(
 "## Woher die Sechzig in der 1-in-60-Regel kommt\n\n"
 "`α` Vorhaltewinkel, Grad. `v_q` Querwindanteil, km/h. "
 "`v_e` Eigengeschwindigkeit, km/h.\n\n"
 "Der Vorhaltewinkel ist der Winkel, dessen Sinus das Verhältnis von "
 "Querwind zu Eigengeschwindigkeit ist: `sin α = v_q / v_e`. Das ist "
 "exakt — aber im Cockpit unbrauchbar.\n\n"
 "Für kleine Winkel gilt `sin α ≈ α` **im Bogenmass**, und ein "
 "Bogenmass sind `180° / π ≈ 57,3°`. Auf 60 gerundet:\n\n"
 "`α [°] ≈ (v_q / v_e) · 57,3 ≈ (v_q / v_e) · 60`\n\n"
 "Die Sechzig ist also nichts weiter als ein gerundetes Bogenmass — "
 "dieselbe Sechzig wie in der 1-in-60-Regel der Navigation, wo eine "
 "Seemeile Versatz auf 60 Seemeilen einem Grad entspricht.\n\n"
 "`(15 / 90) · 60 = 10°`\n\n"
 "Die Rundung von 57,3 auf 60 macht den Winkel rund 5 % zu gross; die "
 "Näherung `sin α ≈ α` macht ihn zu klein, und die beiden "
 "heben sich eine Weile gegenseitig auf. Bei `v_q / v_e = 0,5` ist das "
 "Ergebnis sogar zufällig genau richtig: Regel 30°, gerechnet 30,0°. "
 "Danach läuft die Regel weg, und zwar nach unten — bei "
 "`v_q / v_e = 0,9` sagt sie 54°, gebraucht werden 64°. Bis etwa 20° "
 "Vorhalt ist sie gut, darüber verlässt man sich besser auf den "
 "Rechner.",

 "## Where the sixty in the 1-in-60 rule comes from\n\n"
 "`α` wind correction angle, degrees. `v_q` crosswind component, km/h. "
 "`v_e` airspeed, km/h.\n\n"
 "The wind correction angle is the angle whose sine is the ratio of "
 "crosswind to airspeed: `sin α = v_q / v_e`. That is exact — and "
 "useless in the cockpit.\n\n"
 "For small angles `sin α ≈ α` **in radians**, and one radian is "
 "`180° / π ≈ 57.3°`. Rounded to 60:\n\n"
 "`α [°] ≈ (v_q / v_e) · 57.3 ≈ (v_q / v_e) · 60`\n\n"
 "So the sixty is nothing but a rounded radian — the same sixty as in "
 "the 1-in-60 rule of navigation, where one nautical mile off track in "
 "sixty corresponds to one degree.\n\n"
 "`(15 / 90) · 60 = 10°`\n\n"
 "Rounding 57.3 up to 60 makes the angle about 5 % too large; the "
 "approximation `sin α ≈ α` makes it too small, and for a while the two "
 "cancel. At `v_q / v_e = 0.5` the result is even exactly right by "
 "coincidence: rule 30°, worked out 30.0°. After that the rule drifts, "
 "and downwards — at `v_q / v_e = 0.9` it says 54° where 64° are "
 "needed. Up to about 20° of correction it is good; beyond that you are "
 "better off trusting the computer.")

MISSWEISUNG = t(
 "## Warum West addiert wird\n\n"
 "`rwK` rechtweisender Kurs (gegen geografisch Nord), Grad. `mωK` "
 "missweisender Kurs (gegen magnetisch Nord), Grad. `MW` Missweisung "
 "(Ortsmissweisung), Grad, West positiv gezählt.\n\n"
 "Das ist keine Formel aus der Physik, sondern eine **Buchhaltung mit zwei "
 "Nordrichtungen**, und man kann sie sich herleiten statt sie zu merken.\n\n"
 "Bei westlicher Missweisung zeigt der Kompass nach **links** von "
 "geografisch Nord, also auf eine kleinere Gradzahl. Alle Kurse werden "
 "dann von dieser verdrehten Skala aus gemessen, und ein Kurs, der "
 "gegenüber Nord gleich bleibt, bekommt deshalb eine **grössere** "
 "Zahl — die Skala ist ja nach links gerutscht.\n\n"
 "`mωK = rwK + MW`  (West), `mωK = rwK − MW`  (Ost)\n\n"
 "`120° + 4° = 124°`\n\n"
 "Kurz: **West dazu, Ost weg** — und das gilt nur in dieser Richtung: "
 "**vom rechtweisenden zum missweisenden Kurs**. Rückwärts, von der Karte zur Nadel, kehren "
 "sich die Vorzeichen um. Wer nicht mehr weiss, in welche Richtung er "
 "gerade rechnet, zeichnet die beiden Nordpfeile hin — das dauert fünf "
 "Sekunden und ist nie falsch.",

 "## Why westerly variation is added\n\n"
 "`rwK` true course (against geographic north), degrees. `mωK` magnetic "
 "course (against magnetic north), degrees. `MW` magnetic variation, "
 "degrees, counted positive west.\n\n"
 "This is not a law of physics but **bookkeeping with two norths**, and "
 "you can derive it instead of memorising it.\n\n"
 "With westerly variation the compass points to the **left** of geographic "
 "north, that is at a smaller number of degrees. All courses are then "
 "measured from this rotated scale, and a course that stays the same "
 "relative to north therefore gets a **larger** number — the scale has "
 "slid to the left.\n\n"
 "`mωK = rwK + MW`  (west), `mωK = rwK − MW`  (east)\n\n"
 "`120° + 4° = 124°`\n\n"
 "Short: **west added, east taken off** — and that holds in this "
 "direction only: **from the true to the magnetic course**. The other way round, from the chart to the needle, "
 "the signs reverse. If you lose track of which way you are working, draw "
 "the two north arrows — it takes five seconds and is never wrong.")


HERLEITUNGEN = {
 "Am Morgen meldet der Platz 24 °C und 9 °C Taupunkt. In welcher "
 "Höhe über Grund ist die Basis zu erwarten?": BASIS,
 "Gleitzahl 38, Ankunftshöhe 300 m soll übrig bleiben. Du bist 1200 m "
 "über Platzhöhe. Wie weit darfst du dich höchstens entfernen? "
 "(Windstille, in km)": GLEITZAHL,
 "Du kurbelst mit 45 Grad Schräglage. Um wie viel steigt die "
 "Überziehgeschwindigkeit gegenüber dem Geradeausflug?": KURVENLAST,
 "Leermasse 250 kg mit Moment 75 000 kg·mm, Pilot 70 kg bei Hebelarm "
 "100 mm. Wo liegt der Schwerpunkt in mm hinter dem Bezugspunkt?":
   SCHWERPUNKT,
 "Eigengeschwindigkeit 90 km/h, Querwindanteil 15 km/h. Wie groß ist "
 "der Vorhaltewinkel etwa?": VORHALT,
 "Rechtweisender Kurs 120°, Missweisung 4° West. Welcher missweisende "
 "Kurs?": MISSWEISUNG,
}


SKIZZEN = {
 "Am Morgen meldet der Platz 24 °C und 9 °C Taupunkt. In welcher "
 "Höhe über Grund ist die Basis zu erwarten?": "skizze-luftsaeule",
 "Gleitzahl 38, Ankunftshöhe 300 m soll übrig bleiben. Du bist 1200 m "
 "über Platzhöhe. Wie weit darfst du dich höchstens entfernen? "
 "(Windstille, in km)": "skizze-gleitflug",
 "Du kurbelst mit 45 Grad Schräglage. Um wie viel steigt die "
 "Überziehgeschwindigkeit gegenüber dem Geradeausflug?": "skizze-kurvenlast",
 "Leermasse 250 kg mit Moment 75 000 kg·mm, Pilot 70 kg bei Hebelarm "
 "100 mm. Wo liegt der Schwerpunkt in mm hinter dem Bezugspunkt?":
   "skizze-schwerpunkt",
 "Eigengeschwindigkeit 90 km/h, Querwindanteil 15 km/h. Wie groß ist "
 "der Vorhaltewinkel etwa?": "skizze-vorhalt",
}
