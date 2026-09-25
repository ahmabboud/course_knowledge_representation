#!/usr/bin/env python3
"""List acronyms used on the slides that GLOSSARY.md does not define.

Run before finishing any deck:  python3 scripts/check-glossary.py
Add each real term it prints to GLOSSARY.md, rebuild with
scripts/build-glossary.py, and run this again until it prints nothing new.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = (ROOT / "assets" / "glossary.js").read_text(encoding="utf-8")
entries = json.loads(data[data.index("["):data.rindex("]") + 1])
known = set()
for e in entries:
    known.add(e["term"].lower())
    for f in e.get("forms", []):
        known.add(f["text"].lower())
    for part in re.findall(r"\(([^)]+)\)", e["term"]):
        known.add(part.lower())
# Not jargon: units, course labels, file types students never have to understand.
IGNORE = set("LU MSC ID OK PM AM UTC TODO HTML CSS JS PDF PNG URL API UI TL DR KR IT USA UK EU Q1 Q2 Q3 Q4 I II III IV WH BY EL QL RL DL FOL ODC PDDL EPCIS-SHACL AIR EE UU US PROJECT-REDESIGN Q5 Q6 Q7 Y1 Y2 Y3 CND9".split())  # AIR, EE. UU., CND9: real data values; Y1 to Y3: lab task labels

decks = sorted(d for d in (ROOT / "lectures").glob("*.html") if not d.name.startswith(("_", "proto")))
missing = {}
for deck in decks:
    html = deck.read_text(encoding="utf-8")
    html = re.sub(r"<template data-notes>.*?</template>", " ", html, flags=re.S)
    html = re.sub(r"<(script|style|code|pre|svg)[^>]*>.*?</\1>", " ", html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", html)
    for word in re.findall(r"(?<![\w:/.-])([A-Z][A-Z0-9]{1,}(?:-[A-Z0-9]+)?)(?![\w:/-])", text):
        if word in IGNORE or word.lower() in known or re.search(r"\d{2,}", word):
            continue
        missing.setdefault(word, set()).add(deck.stem)
for w in sorted(missing):
    print(f"{w:14} {', '.join(sorted(missing[w]))}")
sys.exit(1 if missing else 0)
