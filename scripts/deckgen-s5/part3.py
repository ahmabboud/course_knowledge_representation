"""Session 5, Part 3: materialize with Morph-KGC, compare, validate.

Numbers: reference-outputs/materialize-and-compare.txt, validate-mapped.txt,
validate-mapped-without-vocabulary.txt (2026-09-25, SQLite source, the same
tables as PostgreSQL).
"""
from common import slide, divider, defbox, callout
from kit import flow, node, edge, head, table

SLIDES = []

SLIDES.append(divider("Part 3 · Materialize", "Materialize",
    "Part 3 of 5 · about 18 minutes",
    "Did the mapping build the same graph as Session 2's program?",
    "Check it triple by triple, then run Session 4's shapes on it."))

rows = [
    ("Session 2's graph", "135,841"),
    ("minus its vocabulary (class and property descriptions)", "&minus; 49"),
    ("plus the 7 carriers the mapping now types", "+ 7"),
    ("<b>the mapped graph, Morph-KGC</b>", "<b>135,799</b>"),
]
SLIDES.append(slide("Morph-KGC builds the same graph", "Materialize", 5, '''  <div class="lu-eyebrow">A real run, 2.3 seconds</div>
  <h2 class="lu-h2">Every triple of Session 2's data, and 7 more: nothing else differs</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + table(["Triples", "Count"], rows) + '''
    <div class="lu-stack">
      ''' + defbox([("Morph-KGC", "The open source tool that runs a mapping and writes the whole graph.")]) + '''
      ''' + callout("Compared one by one", "0 triples only in Session 2's graph, 7 only in the mapped graph (the new carrier types), all 1,540 rate bands equal.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. Real run of <code>materialize.py</code> and <code>compare_with_session2.py</code> (<code>reference-outputs/materialize-and-compare.txt</code>).</p>
<ul><li>Decimals are compared as numbers. Session 2 read the CSV with pandas' fast number parser, which misreads some long decimals by one unit in the last digit (1.462970094059406 for the file's 1.4629700940594061); the database keeps the file's digits exactly. Say it only if asked: it is a real, tiny finding.</li>
<li>A mapping produces data only; the 49 vocabulary triples live in <code>vocabulary.ttl</code>.</li></ul>'''))

rows = [
    ("Violations: weight not above 0", "2", "2"),
    ("Warnings: weight in no band of a priced lane", "1,370", "1,370"),
    ("Warnings: band carrier is not a Carrier", "1,209", "<b>0</b>"),
]
SLIDES.append(slide("Session 4's shapes on the mapped graph", "Materialize", 4, '''  <div class="lu-eyebrow">The same shapes, unchanged</div>
  <h2 class="lu-h2">The data problems stay. The conversion problem is gone.</h2>
  ''' + table(["Result", "Session 2 graph", "Mapped graph"], rows) + '''
  <div class="lu-split">
    ''' + callout("Right to stay", "The two zero weight orders and the rate table's gap are in the source tables. No mapping should hide them.", "neutral") + '''
    ''' + callout("Right to go", "The 1,209 were the converter's fault. Session 4 said: fix it in the mapping. Done.") + '''
  </div>''', '''<p>Four minutes. Real runs of Session 4's <code>validate.py</code> with <code>brunel-shapes.ttl</code> (Session 4's <code>validate-triaged.txt</code>, and here <code>validate-mapped.txt</code>). This is the first time a triage decision has been closed.</p>'''))

n = [
    node("m", "mapped data\n135,799 triples", 190, 55, 300, 70, kind="builtin"),
    node("f1", "9,023 focus nodes:\n192 late orders unchecked", 640, 55, 420, 70, kind="builtin", flag="right"),
    node("v", "+ vocabulary.ttl:\nlate order ⊑ order", 190, 195, 300, 70, kind="builtin"),
    node("f2", "9,215 focus nodes:\nevery order checked", 640, 195, 420, 70, kind="builtin"),
]
e = [edge("a", "m", "f1", "validate"), edge("b", "v", "f2", "validate")]
steps = [
    {"show": ["m", "f1", "a"], "run": ["a"], "set": {"f1": "impossible"}},
    {"show": ["v", "f2", "b"], "run": ["b"], "set": {"f2": "active"}},
]
caps = [
    ("No error, still wrong", "<b>Step 1.</b> The order shapes target <code>ul:Order</code>. The late orders are typed <code>ul:LateOrder</code> only, and nothing in the data says a late order is an order. 192 orders are silently not checked."),
    ("Data plus vocabulary", "<b>Step 2.</b> Validate the data <b>together with</b> the vocabulary. Its rule, every late order is an order, brings the focus nodes back to 9,215."),
]
walk = flow("A mapping bug that raises no error", 1100, 250, n, e, steps, caps, flags={"impossible": "unchecked"},
            legend={"builtin": "Step", "impossible": "Silently unchecked"})
SLIDES.append(slide("The bug that raised no error", "Materialize", 5, '''  <div class="lu-eyebrow">Found by accident, building this lab</div>
  <h2 class="lu-h2">The first validation reported 6 fewer warnings. Nothing had improved.</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + walk + '''
    ''' + callout("Session 4's rule, again", "Read the focus node count before the result. 9,023 instead of 9,215 was the only sign that 192 orders had not been looked at.") + '''
  </div>''', '''<p>Five minutes. Real: without <code>vocabulary.ttl</code> the weight in band shape reported 1,364 warnings instead of 1,370; the 6 missing are all late orders (<code>reference-outputs/validate-mapped-without-vocabulary.txt</code>).</p>
<ul><li>Session 2's graph never had the problem because its converter wrote the vocabulary into the same file.</li></ul>'''))

SLIDES.append(slide("Check: why no join?", "Materialize", 3, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-mcq" data-qid="s5-q2" data-answer="c" data-label="Why the order to carrier link needs no join"
       data-fb-correct=" Both maps build the carrier's IRI with the same template from the same key."
       data-fb-wrong=" Look at how each map builds the IRI of carrier V44_3.">
    <p class="lu-mcq__q">The orders map links each order to its carrier without joining the orders table to anything. Why does that work?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">Morph-KGC joins the tables by itself<span class="lu-mcq__why" hidden>It does not; no join is written or needed.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">The carrier column holds the carrier's IRI<span class="lu-mcq__why" hidden>It holds the code V44_3, not an IRI.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">Both maps build the IRI from the same key with the same template<span class="lu-mcq__why" hidden>Right: same kind, same source, same key, same IRI.</span></button>
    </div>
  </div>''', '''<p>Three minutes. Answer c is Session 2's naming rule paying off.</p>''', kind="tint"))
