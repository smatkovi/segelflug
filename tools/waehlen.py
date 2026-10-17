#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Die auf dem Kontaktbogen genannten Nummern in Commons-Titel uebersetzen.

    tools/waehlen.py cu-humilis 4 9 23 28

Gibt die Zeilen so aus, wie sie in erkennen.py stehen.
"""
import json
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
KAND = os.path.join(os.path.dirname(HIER), "kandidaten")

klasse = sys.argv[1]
mit = os.path.join(KAND, klasse, "index.json")
nach = {d["nummer"]: d for d in json.load(open(mit, encoding="utf-8"))["dateien"]}
for arg in sys.argv[2:]:
    d = nach[int(arg)]
    print('    "%s",   # %s, %s' % (d["titel"], d["autor"][:28], d["lizenz"]))
