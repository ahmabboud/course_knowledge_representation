import importlib, sys
sys.path.insert(0, "/tmp/s3deck")

PARTS = [p for p in sys.argv[2:]] or ["part1"]
out = sys.argv[1]

HEAD = '''<!DOCTYPE html>
<html lang="en" class="lu-deck-page">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ontology Engineering: Description Logic, OWL, and Reuse · Knowledge Representation, Session 3</title>
<meta name="description" content="Session 3 of Knowledge Representation, MSc, Lebanese University. What an ontology is, OWL restrictions drawn as sets, what a reasoner does, reuse on BFO and IOF SCRO, OWL profiles, and a guided Protégé lab that finds and fixes a real modelling error.">
<meta name="theme-color" content="#96122B">
<link rel="manifest" href="../manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;1,8..60,400&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/lu.css?v=1.1.0">
</head>

<body
  data-deck-id="kr-s03"
  data-course="Knowledge Representation"
  data-session="Session 3 of 8"
  data-duration="DURATION"
  data-app-root="../"
  data-unit="Lebanese University · MSc">

<a class="lu-skip" href="#slide-2">Skip to the first content slide</a>

<div class="deck">
<div class="deck__stage">

'''
TAIL = '''
</div><!-- /stage -->
</div><!-- /deck -->

<script src="../assets/lu-deck.js?v=1.1.0" defer></script>
</body>
</html>
'''
slides = []
for p in PARTS:
    m = importlib.import_module(p)
    slides += m.SLIDES
import re
total = sum(int(x) for s in slides for x in re.findall(r'data-minutes="(\d+)"', s)[:1])
html = HEAD.replace("DURATION", str(total)) + "\n".join(
    f"<!-- {'=' * 68} {i:02d} -->\n{s}" for i, s in enumerate(slides, 1)) + TAIL
open(out, "w").write(html)
print(f"{out}: {len(slides)} slides, {total} minutes")
