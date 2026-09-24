Segelflug 2.4 — die Formeln auf den Karteikarten sind hergeleitet

Sechs Karten rechnen: Wolkenbasis, Gleitzahl, Lastvielfaches und
Überziehgeschwindigkeit in der Kurve, Schwerpunkt, Vorhaltewinkel und
Missweisung. In der Lösung stand bisher nur die Rechnung — also eine Zahl zum
Auswendiglernen, die im Cockpit genau so lange hilft, wie die Lage zur Aufgabe
passt.

**Jede dieser Karten trägt jetzt ihre Herleitung:** woher die Formel kommt,
welche Annahme sie macht, und was passiert, wenn die Annahme nicht stimmt.

* Die **125 m je Grad Spreizung** sind `100 / 0,8` — Trockenadiabate 1 K/100 m
  minus Taupunktgradient 0,2 K/100 m. Die Annahme dahinter: die aufsteigende
  Luft ist dieselbe, die unten gemessen wurde.
* Die **60 der 1-in-60-Regel** ist ein gerundetes Bogenmaß (`180/π ≈ 57,3`).
  Bei `v_q/v_e = 0,5` ist das Ergebnis zufällig exakt, bei 0,9 sagt die Regel
  54° und gebraucht werden 64°.
* Das **Lastvielfache** ist `1 / cos φ`, die Überziehgeschwindigkeit steigt
  aber nur mit `√n`, weil der Auftrieb quadratisch mit der Geschwindigkeit
  geht. Bei 45° Schräglage sind das 41 % Last, aber 19 % Geschwindigkeit — wer
  beides verwechselt, rechnet sich eine Reserve herbei, die es nicht gibt.
* Der **Schwerpunkt** ist ein mit den Massen gewichteter Mittelwert der
  Hebelarme; deshalb darf man Momente addieren, Hebelarme aber nicht.
* Die **Missweisung** ist keine Formel, sondern Buchhaltung mit zwei
  Nordrichtungen — die Karte leitet das Vorzeichen her, statt eine Merkregel
  hinzustellen.

Fünf der sechs bekommen die Skizze dazu, die schon im Lehrtext an derselben
Herleitung hängt. Sie steht **in der Lösung** und nicht über der Frage — davor
wäre sie die Antwort.

Alles zweisprachig.

## Pakete

* **N9 / N950:** `segelflug_2.4_armel.deb`
* **Sailfish OS:** `harbour-segelflug-1.11.0-1.aarch64.rpm` bzw. `…armv7hl.rpm`
