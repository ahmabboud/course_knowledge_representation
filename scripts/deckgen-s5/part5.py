"""Session 5, Part 5: entity resolution, on a labelled teaching set.

Numbers: reference-outputs/match-customers.txt; the records are
er/tms-customers.csv and er/truth.csv (teaching data, built by
er/make_teaching_set.py from Brunel's 46 real customers).
"""
import math

from common import slide, divider, defbox, callout
from kit import head, table, bar

SLIDES = []

SLIDES.append(divider("Part 5 · Entity resolution", "Entity resolution",
    "Part 5 of 5 · about 24 minutes",
    "Two systems list the same customer under two different codes. Which records match?",
    "A matcher decides, and it will be wrong sometimes. The question is how often, and which way."))

rows = [
    ("<code>v555555555555555555_42</code>", "lower case", "<code>V555555555555555555_42</code>"),
    ("<code>V555555555555555555-45</code>", "a dash", "<code>V555555555555555555_45</code>"),
    ("<code>V555555555555555_023</code>", "a padded number", "<code>V555555555555555_23</code>"),
    ("<code>555555555555555_44</code>", "the V lost", "<code>V555555555555555_44</code>"),
    ("<code>V5555555555555_8</code>", "one 5 lost", "<code>V55555555555555_8</code>"),
    ("<code>V555555555555_13</code>", "two digits swapped", "<code>V555555555555_31</code>"),
]
SLIDES.append(slide("Same customer, two systems", "Entity resolution", 5, '''  <div class="lu-eyebrow">Teaching data, built on purpose</div>
  <h2 class="lu-h2">A second system writes Brunel's customers the way real systems drift</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + table(["TMS export", "What drifted", "Brunel"], rows) + '''
    <div class="lu-stack">
      ''' + defbox([("Entity resolution", "Deciding which records in different sources describe the same real thing.")]) + '''
      ''' + callout("Teaching data", "Brunel has no second system. A script wrote this TMS list from Brunel's 46 real customers, plus 6 that are not in Brunel. So the truth is known, and errors can be counted.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. Say clearly: this is teaching data, like Session 3's sanctioned flag. The customers are real; the second system is not. <code>er/make_teaching_set.py</code> shows exactly how each record was made.</p>
<ul><li>Checked first: DataCo and Brunel share no entities, Brunel's codes are anonymised and unique, and DataCo's names are personal data we never show.</li></ul>'''))

SLIDES.append(slide("Clean first, then block", "Entity resolution", 4, '''  <div class="lu-eyebrow">Two cheap steps before any scoring</div>
  <h2 class="lu-h2">Cleaning fixes the easy drift. Blocking skips pairs that cannot match.</h2>
  <div class="lu-split">
    <div class="lu-card">
      <span class="lu-card__label">1 · Clean both sides the same way</span>
      <ul class="lu-list"><li>upper case, spaces off</li><li>dash to underscore</li><li>put the V back</li><li><code>_023</code> to <code>_23</code></li></ul>
      <p class="lu-sub">4 of the 6 drifts above now match exactly. A lost 5 and swapped digits do not.</p>
    </div>
    <div class="lu-card">
      <span class="lu-card__label">2 · Block on the home plant</span>
      <div class="lu-stack" style="gap:var(--lu-s3)">''' + bar(2392, 2392, "2,392 pairs") + bar(1818, 2392, "1,818 pairs") + '''</div>
      <p class="lu-sub">52 &times; 46 = 2,392 possible pairs; comparing only records with the same home plant leaves 1,818.</p>
    </div>
  </div>
  ''' + defbox([("Blocking", "Only comparing records that share a cheap key, so the matcher does not compare every pair.")]),
    '''<p>Four minutes. Blocking saves little here, because 41 of the 46 customers have the same home plant, PLANT03. At DataCo's 180,519 order lines, comparing every pair is impossible without it.</p>'''))

W = [("code, exact after cleaning", 0.60, 0.001), ("code, close (Jaro-Winkler &ge; 0.93)", 0.35, 0.02),
     ("code, different", 0.05, 0.979), ("same home plant", 0.95, 0.80), ("same main service", 0.90, 0.40)]
rows = [(n, f"{m}", f"{u}", f"{math.log2(m / u):+.1f}") for n, m, u in W]
SLIDES.append(slide("Evidence adds up: match weights", "Entity resolution", 5, '''  <div class="lu-eyebrow">Fellegi and Sunter, 1969</div>
  <h2 class="lu-h2">Each comparison adds evidence for &ldquo;same customer&rdquo;, or against it</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + table(["Outcome", "m", "u", "Weight"], rows) + '''
    <div class="lu-stack">
      ''' + defbox([("Match weight", "log2(m / u): m is how often the outcome happens for a true match, u for two different customers.")]) + '''
      ''' + callout("Read one row", "Same home plant: true matches share it 95% of the time, different customers 80%. Weak evidence: +0.2. An exact code: +9.2.", "neutral") + '''
      ''' + callout("At scale", "These weights are stated in <code>er/match_customers.py</code>. Splink, the tool named in the syllabus, estimates them from the data, for the same model.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. A pair's score is the sum of its weights. Exact code, same plant, same service: 9.2 + 0.2 + 1.2, about 10.6. A close code with both the same: 4.1 + 0.2 + 1.2 = 5.5.</p>'''))

rows = [("4", "49", "43", "0.878", "0.935"), ("8", "40", "40", "1.000", "0.870")]
SLIDES.append(slide("One threshold, two kinds of error", "Entity resolution", 5, '''  <div class="lu-eyebrow">A real run on the teaching set</div>
  <h2 class="lu-h2">Lower the threshold: more found, more wrong. Raise it: fewer wrong, more missed.</h2>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      ''' + table(["Threshold", "Matches", "Right", "Precision", "Recall"], rows) + '''
      ''' + callout("A wrong match at 4", "<code>V555555555555555555_18</code>, not a Brunel customer, matched to a real one: its code is close to several.") + '''
      ''' + callout("A miss at 8", "<code>V555555555555_13</code> (digits swapped) scored 5.5, below 8: the true customer is <code>V555555555555_31</code>.", "neutral") + '''
    </div>
    ''' + defbox([("Precision", "Of the matches we reported, the share that are correct."),
                  ("Recall", "Of the true matches, the share we found.")]) + '''
  </div>''', '''<p>Five minutes. Real run of <code>er/match_customers.py</code> (<code>reference-outputs/match-customers.txt</code>). No threshold gives both at 1.000 on this data: a lost 5 makes a code equally close to two customers.</p>'''))

SLIDES.append(slide("Poll: which error costs more?", "Entity resolution", 4, '''  <div class="lu-eyebrow">Room poll · 45 seconds</div>
  <div class="lu-poll" data-qid="s5-poll" data-seconds="45" data-answer="a" data-label="Which matching error costs more when merging customer records">
    <p class="lu-mcq__q">The matched customers will be merged: their orders, prices and credit limits become one record. Which error costs more?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">A wrong match: two customers merged<span class="lu-mcq__why" hidden>Usually, yes: one customer sees another's orders and prices, and undoing a merge is hard.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">A miss: one customer kept twice<span class="lu-mcq__why" hidden>Annoying and costly in reports, but nothing is mixed up, and it can be merged later.</span></button>
    </div>
  </div>''', '''<p>Forty five seconds, then discuss. For merging, favour precision (threshold 8). For finding possible duplicates for a person to review, favour recall (threshold 4). The use decides the threshold.</p>''', kind="tint", extra_attr=' style="--lu-s5:12px"'))
