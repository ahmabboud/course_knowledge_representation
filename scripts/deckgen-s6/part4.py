"""Session 6, Part 4: leakage, and the split that tells the truth.

Numbers: reference-outputs/baseline.txt and gnn.txt; the late orders per
customer are counted on Session 5's brunel-mapped.nt (the notes say so).
"""
from common import slide, divider, defbox, callout, code
from kit import head, table, bar
from svgkit import svg, text, circle, rect, line, FULL, INK2, INK3, RED, GREEN, LINE, BLUE, BLUE_BG, PAPER2

SLIDES = []
S, C, E = '<span class="tok-str">', '<span class="tok-com">', '</span>'

SLIDES.append(divider("Part 4 · Leakage", "Leakage",
    "Part 4 of 4 · about 25 minutes",
    "The model scores 0.88. Did it learn about late orders, or about the test?",
    "Three ways a test can let the model cheat, all found in this graph."))

# ---------------------------------------------------------------- the label, twice
tt = (f'''order:1447135386.7
    a ul:LateOrder ;          {C}# the label{E}
    ul:lateDays 1 ;           {C}# the label again{E}
    ul:weight 3.0977760466629154 ;
    ul:serviceLevel {S}"DTP"{E} ;
    ul:orderedBy customer:V555_15 .''')
SLIDES.append(slide("The label is in the graph twice", "Leakage", 4, '''  <div class="lu-eyebrow">Leak 1 · the answer among the features</div>
  <h2 class="lu-h2">The graph says &ldquo;late&rdquo; twice: as a class and as a number</h2>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      ''' + code("brunel-mapped.nt · the order from Part 1, as Turtle, prefixes shortened", tt) + '''
      ''' + table(["Logistic regression, random split", "PR-AUC", "Accuracy"],
                  [("with lateDays kept as a column", "<b>1.000</b>", "1.000")]) + '''
    </div>
    <div class="lu-stack">
      ''' + defbox([("Leakage", "When the test lets the model see the answer, or something that gives it away.")]) + '''
      ''' + callout("A perfect score is a warning", "Nothing predicts the future perfectly. <code>build_graph.py</code> removes both the class and <code>lateDays</code> before any model sees the order.") + '''
    </div>
  </div>''', '''<p>Four minutes. Real run, line 1 of <code>reference-outputs/baseline.txt</code>. The graph is right to hold these facts: they are what Session 1 profiled. They are the answer, so the model must not see them.</p>
<ul><li>Ask: where else could the label hide in your own project's graph? A status field, a "delivered on" date, a class assigned after the fact.</li></ul>'''))

# ---------------------------------------------------------------- accuracy trap
SLIDES.append(slide("Accuracy is the wrong score", "Leakage", 3,
    head("When 2% are late, saying &ldquo;never late&rdquo; is 97.9% accurate", "Score the ranking of the rare class instead") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <div class="lu-stack" style="gap:var(--lu-s4)">
      <div class="lu-stack" style="gap:var(--lu-s2)"><span class="lu-card__label">Accuracy · always say &ldquo;not late&rdquo;</span>''' + bar(0.979, 1, "0.979") + '''</div>
      <div class="lu-stack" style="gap:var(--lu-s2)"><span class="lu-card__label">Accuracy · logistic regression, random split</span>''' + bar(0.944, 1, "0.944") + '''</div>
      <div class="lu-stack" style="gap:var(--lu-s2)"><span class="lu-card__label">PR-AUC · guessing</span>''' + bar(0.021, 1, "0.021", "red") + '''</div>
      <div class="lu-stack" style="gap:var(--lu-s2)"><span class="lu-card__label">PR-AUC · logistic regression, random split</span>''' + bar(0.788, 1, "0.788", "red") + '''</div>
    </div>
    ''' + defbox([("PR-AUC", "How well the late orders are ranked above the rest; guessing scores their share, 0.021."),
                  ("Precision@k", "Of the k orders ranked most at risk, the share that are late: 0.48 at k = 100 here.")]) + '''
  </div>''', '''<p>Three minutes. <code>reference-outputs/baseline.txt</code>, lines 2 and the header. The model is less accurate than saying "never", and far more useful: it finds late orders. Accuracy cannot tell those apart; PR-AUC can.</p>'''))

# ---------------------------------------------------------------- random against by customer
rows = [
    ("Guessing", "0.021", "about 0.02"),
    ("Logistic regression", "0.788", "0.002 to 0.019"),
    ("GraphSAGE", "<b>0.857 to 0.879</b>", "<b>0.004 to 0.045</b>"),
]
SLIDES.append(slide("Random split against split by customer", "Leakage", 5, '''  <div class="lu-eyebrow">Leak 2 · the same customer on both sides</div>
  <h2 class="lu-h2">The graph model wins the random split, and both fall to guessing on new customers</h2>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      ''' + table(["PR-AUC on late orders", "Random split", "Split by customer"], rows) + '''
      <div class="lu-stack" style="gap:var(--lu-s2)"><span class="lu-card__label">GraphSAGE, seed 0</span>''' + bar(0.857, 1, "0.857 random", "red") + bar(0.045, 1, "0.045 by customer", "red") + '''</div>
    </div>
    <div class="lu-stack">
      ''' + defbox([("Random split", "Test orders drawn at random, so the same customers are in training too."),
                    ("Split by group", "Every order of a customer on the same side, so the test customers are new.")]) + '''
      ''' + callout("What each one measures", "Random: can it recognise customers it knows? By customer: can it predict for one it does not? Only the second is the company's question.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. Real runs: <code>baseline.txt</code> and <code>gnn.txt</code>. The random split is the same 30% for both models; GraphSAGE's range is three training seeds; the split by customer is five split seeds, of which one has no late order in its test set.</p>
<ul><li>This is the honest headline of the session: the graph model's advantage exists only where it can remember.</li></ul>'''))

# ---------------------------------------------------------------- the four customers, drawn
LATE = {4: ("V555_15", "110 of 110 late"), 16: ("V555555555555555_44", "9 of 9 late"),
        28: ("V555555555_27", "69 of 521 late"), 40: ("V555555555_14", "4 of 351 late")}
g = ""
x0, step = 36, (FULL - 72) / 45
for i in range(46):
    cx = x0 + i * step
    g += circle(round(cx, 1), 40, 12, None, "red" if i in LATE else "muted")
for i, (cid, share) in LATE.items():
    cx = round(x0 + i * step, 1)
    g += line(cx, 56, cx, 88, RED, 2)
    g += text(cx, 108, cid, "s-mono", color=RED)
    g += text(cx, 136, share, "s-label", color=INK2)
pic = svg(FULL, 150, g, "Brunel's 46 customers; only 4 ever have a late order.")
SLIDES.append(slide("Why the random split flatters", "Leakage", 3,
    head("Brunel's 46 customers. Only four ever have a late order.", "Late orders are almost entirely &ldquo;which customer&rdquo;") + '''
  ''' + pic + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    <div class="lu-card"><span class="lu-card__label">Random split</span><p class="lu-sub">All four have orders in training. The model learns four names, and the test asks about the same four.</p></div>
    <div class="lu-card"><span class="lu-card__label">Split by customer · 14 held out</span><p class="lu-sub">The test holds 0, 1 or 2 of the four, never seen in training. Nothing learned applies.</p></div>
  </div>''', '''<p>Three minutes. Counted on <code>brunel-mapped.nt</code>: late orders per customer. The dots' order is arbitrary; the counts are real. 30% of 46 customers is 14 (<code>split_by_customer</code> in <code>learning_utils.py</code>).</p>'''))

# ---------------------------------------------------------------- seeds
rows = [("0", "69", "0.019", "0.045"), ("1", "13", "0.004", "0.004"), ("2", "4", "0.002", "0.005"),
        ("3", "78", "0.015", "0.017"), ("4", "0", "<i>nothing to measure</i>", "<i>nothing to measure</i>")]
SLIDES.append(slide("One split is not evidence", "Leakage", 3,
    head("Five splits by customer, five different tests", "Which customers land in the test decides the number") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    ''' + table(["Split seed", "Late orders in test", "Logistic regression", "GraphSAGE"], rows) + '''
    <div class="lu-stack">
      ''' + callout("Report the spread", "Run several seeds and give the range, not the best run. Seed 0 alone would say the GNN is twice as good; seed 1 says they tie.") + '''
      ''' + callout("An empty test", "Seed 4 put none of the four customers in the test: no late order at all, so PR-AUC is undefined.", "neutral") + '''
    </div>
  </div>''', '''<p>Three minutes. <code>baseline.txt</code> and <code>gnn.txt</code>, the split by customer rows. With 4 positive customers this is noisy by nature; a real project with this shape would say so in its limits.</p>'''))

# ---------------------------------------------------------------- the rule for data with dates
g = rect(40, 60, 900, 70, BLUE_BG, BLUE, rx=8) + text(490, 95, "train: orders before the cut", color=BLUE, weight=600)
g += rect(960, 60, 448, 70, PAPER2, INK2, rx=8) + text(1184, 95, "test: orders after", color=INK2, weight=600)
g += line(950, 30, 950, 160, RED, 3, dashed=True) + text(950, 18, "cut date", "s-label", color=RED)
g += line(40, 170, 1408, 170, LINE, 2) + text(40, 196, "time", "s-label", anchor="start", color=INK3)
pic = svg(FULL, 210, g, "A split by time: train on everything before a cut date, test on everything after it.")
SLIDES.append(slide("With dates, split by time", "Leakage", 4,
    head("The rule for your project: train on the past, test on the future", "Brunel cannot do this: all 9,215 orders are dated 2013-05-26") + '''
  ''' + pic + '''
  <div class="lu-split">
    <ol class="lu-list lu-list--num">
      <li>Pick a cut date. Everything after it is the test.</li>
      <li>Build the training <b>graph</b> from before the cut only: a link created later is the future too.</li>
      <li>If the same customers appear on both sides, also report a split by customer.</li>
    </ol>
    ''' + defbox([("Temporal split", "Training on everything before a cut date and testing on everything after it."),
                  ("Temporal leakage", "Letting information from after the cut into training.")]) + '''
  </div>''', '''<p>Four minutes. The single order date was counted on <code>brunel-mapped.nt</code> (one value, 9,215 times). This is why the lab splits by customer instead, and why Milestone 2 asks for a split by time where the data has dates.</p>
<ul><li>Rule 2 is the graph specific trap: a random split of orders still leaves future links (a customer's later orders) in the graph the model trains on.</li></ul>'''))

SLIDES.append(slide("Poll: which number do you report?", "Leakage", 3, '''  <div class="lu-eyebrow">Room poll · 45 seconds</div>
  <div class="lu-poll" data-qid="s6-poll" data-seconds="45" data-answer="b" data-label="Which late order score to report to the company">
    <p class="lu-mcq__q">Next month, many orders come from customers never served before. Which PR-AUC should the company expect?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">About 0.87 (random split)<span class="lu-mcq__why" hidden>It measures recognising known customers.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">About 0.02 (split by customer)<span class="lu-mcq__why" hidden>Yes, for new customers: as good as guessing.</span></button>
    </div>
  </div>''', '''<p>Forty five seconds, then discuss. Known customers would still see the random split's quality, so an honest report gives both numbers and says which question each answers. If someone suggests averaging them: an average of two different questions answers neither.</p>''', kind="tint", extra_attr=' style="--lu-s5:12px"'))
