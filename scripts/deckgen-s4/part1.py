"""Session 4: opening and Part 1, why OWL cannot check data.

The cast is the course's one cast (AGENTS.md 2c rule 4): real Brunel orders
and carriers from Sessions 1 to 3, in the Session 2 graph. Every number comes
from demos/session-04-shacl/reference-outputs/. Colours follow lu-flow: green
an individual, grey a value or a SHACL term; amber something inferred; red a
Violation, the only thing that is refused.
"""
from common import slide, divider, defbox, callout
from kit import flow, node, edge, head
from svgkit import svg, text, rect, circle, dot, FULL, INK2, INK3, RED, GREEN, LINE

SLIDES = []

# ---------------------------------------------------------------- Title
SLIDES.append('''<section class="slide slide--night" data-chrome="none" data-label="Title" data-section="Opening" data-minutes="2">
  <div class="slide__body" style="justify-content:space-between">
    <div class="lu-row" style="justify-content:space-between;align-items:flex-start">
      <div class="lu-lockup">
        <span class="lu-lockup__mark">LU</span>
        <span class="lu-lockup__text">
          <span class="lu-lockup__name">Lebanese University</span>
          <span class="lu-lockup__unit">Faculty of Sciences · MSc Computer Science</span>
        </span>
      </div>
      <div class="lu-tag lu-tag--red" style="background:transparent;color:#FF9AA7;border-color:#96122B">Module 2 · Ontology and constraints</div>
    </div>
    <div class="lu-stack">
      <div class="lu-eyebrow">Knowledge Representation · Session 4 of 8</div>
      <h1 class="lu-display" style="max-width:24ch">Constraints, Quality, and Provenance: SHACL</h1>
      <p class="lu-lead" style="max-width:48ch">Session 1 wrote the business rules down in English. Today they become checks a machine runs on every order, every time the data changes, and the first real report tells us what is wrong.</p>
    </div>
    <div class="lu-row" style="justify-content:space-between;font-size:var(--lu-t-caption);color:var(--lu-on-night-2)">
      <span>About 190 minutes · lecture, lab in Python, wrap</span>
      <span>Press <kbd>&rarr;</kbd> to begin · <kbd>?</kbd> for shortcuts</span>
    </div>
  </div>
  <template data-notes>
    <p>Before minute one: every student has the Session 2 graph (<code>demos/session-02-rdf-sparql/brunel.ttl</code>, from <code>convert_to_rdf.py</code>) and pySHACL installed (it is in <code>demos/requirements.txt</code>). The lab needs both.</p>
    <ul>
      <li>Milestone 1 of the team project is due at the end of this session. The lab is not part of it: it is the shared case, done once, so the team can do the same on its own data.</li>
      <li>Every number on these slides is a real run on the Session 2 graph, recorded in <code>demos/session-04-shacl/reference-outputs/</code> on 2026-09-25.</li>
    </ul>
  </template>
</section>
''')

# ---------------------------------------------------------------- Recap
SLIDES.append(slide("Where we are in the architecture", "Opening", 3, '''  <div class="lu-eyebrow">Recap</div>
  <h2 class="lu-h1" style="max-width:40ch">We have the data and what it means. Nothing yet <em style="font-style:italic;color:var(--lu-red-700)">checks</em> it.</h2>
  <ul class="lu-pipeline" style="margin-top:var(--lu-s5)">
    <li data-state="done"><span class="lu-pipeline__n">01</span><span class="lu-pipeline__t">Sources</span><span class="lu-pipeline__d">DataCo, Brunel</span></li>
    <li data-state="done"><span class="lu-pipeline__n">02</span><span class="lu-pipeline__t">Profiling</span><span class="lu-pipeline__d">Business rules</span></li>
    <li data-state="done"><span class="lu-pipeline__n">03</span><span class="lu-pipeline__t">Graph</span><span class="lu-pipeline__d">RDF, SPARQL</span></li>
    <li data-state="done"><span class="lu-pipeline__n">04</span><span class="lu-pipeline__t">Ontology</span><span class="lu-pipeline__d">OWL, reasoner</span></li>
    <li data-state="active"><span class="lu-pipeline__n">05</span><span class="lu-pipeline__t">Constraints</span><span class="lu-pipeline__d">You are here</span></li>
    <li data-state="muted"><span class="lu-pipeline__n">06</span><span class="lu-pipeline__t">Mappings</span><span class="lu-pipeline__d">RML · 5</span></li>
    <li data-state="muted"><span class="lu-pipeline__n">07</span><span class="lu-pipeline__t">Learning</span><span class="lu-pipeline__d">GNN · 6</span></li>
    <li data-state="muted"><span class="lu-pipeline__n">08</span><span class="lu-pipeline__t">Access</span><span class="lu-pipeline__d">Questions · 7</span></li>
  </ul>
  <div class="lu-split" style="margin-top:var(--lu-s5)">
    ''' + callout("What you have", "The 9,215 Brunel orders as a graph (Session 2), an ontology that says what the words mean (Session 3), and Session 1's list of business rules, in English.", "neutral") + '''
    ''' + callout("What is missing", "Nothing runs those rules. Session 3 showed why OWL will not: it <b>infers</b> rather than complains. Today's tool complains.") + '''
  </div>''', '''<p>Three minutes. Point at stage 05. The one line to say: Session 3 taught the machine what things mean; today teaches it what the data must look like.</p>'''))

# ---------------------------------------------------------------- Objective
SLIDES.append(slide("Session objective and shape", "Opening", 3, '''  <div class="lu-eyebrow">Objective</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <p class="lu-statement">By the end you can turn a business rule into a check, run it on the real graph, read the report as a list of work, and put the check where every change has to pass it.</p>
      ''' + callout("Open these now", "The folder <code>demos/session-04-shacl/</code> · the Session 2 graph <code>brunel.ttl</code> · a terminal with <code>demos/.venv</code> active.", "concept") + '''
    </div>
    <div class="lu-card">
      <span class="lu-card__label">How the ~190 minutes are spent</span>
      <ul class="lu-layers">
        <li><span class="lu-layers__name">Lecture · ~120 min</span><span class="lu-layers__note">Why OWL cannot check, SHACL core, the rules as shapes, provenance and versions, reuse and the gate</span></li>
        <li><span class="lu-layers__name">Lab · ~55 min</span><span class="lu-layers__note">Validate, triage, record provenance, watch the gate fail, write three shapes of your own</span></li>
        <li><span class="lu-layers__name">Wrap · ~15 min</span><span class="lu-layers__note">Discussion, Milestone 1, glossary, self-check</span></li>
      </ul>
    </div>
  </div>''', '''<p>Name the payoff: the first real report on our graph has 3,435 problems. By the lab, the room knows which of them are ours to fix and which are the data's.</p>''', kind="tint"))

# ---------------------------------------------------------------- Part 1 divider
SLIDES.append(divider("Part 1 · The gap OWL leaves open", "Why OWL cannot check",
    "Part 1 of 5 · about 18 minutes",
    "An order has lost its carrier. Does the reasoner complain?",
    "No. And by OWL's own rules, it is right not to."))

# ---------------------------------------------------------------- OWL infers, SHACL checks
n = [
    node("o", "order 1447291369.7", 230, 50, 300, 60, kind="individual"),
    node("u", "some carrier,\nname unknown", 760, 50, 260, 70, kind="builtin"),
    node("s", "rule: exactly one carrier", 230, 190, 330, 60, kind="builtin"),
    node("r", "report: MinCount\non carried by", 700, 190, 280, 70, kind="builtin", flag="right"),
]
e = [
    edge("a", "o", "u", "carried by", kind="inferred"),
    edge("b", "s", "o", "checks"),
    edge("c", "s", "r", "result"),
]
steps = [
    {"show": ["o"], "set": {"o": "active"}},
    {"show": ["u", "a"], "run": ["a"], "set": {"u": "inferred"}},
    {"show": ["s", "b"], "run": ["b"], "set": {"u": "idle", "o": "active"}},
    {"show": ["r", "c"], "run": ["c"], "set": {"r": "impossible"}},
]
caps = [
    ("The data", "<b>Step 1.</b> Suppose the conversion lost the <b>carried by</b> line of order 1447291369.7 (Part B plants exactly this fault)."),
    ("OWL, open world", "<b>Step 2.</b> If the ontology says every order is carried by some carrier, the reasoner concludes a carrier exists that nobody named. No error: missing is not false."),
    ("SHACL, closed world", "<b>Step 3.</b> A SHACL rule looks only at the triples in front of it: this order has zero <b>carried by</b> values."),
    ("A Violation", "<b>Step 4.</b> Zero is fewer than one, so the report says: Violation, MinCount on <b>carried by</b>, for this order."),
]
walk = flow("OWL infers, SHACL checks", 1000, 240, n, e, steps, caps,
            flags={"impossible": "violation"},
            legend={"individual": "Individual", "builtin": "Value or rule", "inferred": "Inferred", "impossible": "Violation"})
SLIDES.append(slide("OWL infers, SHACL checks", "Why OWL cannot check", 5, '''  <div class="lu-eyebrow">The same missing fact, two tools</div>
  <h2 class="lu-h2">A reasoner fills the gap with an unknown. A validator reports the gap.</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + walk + '''
    <div class="lu-stack">
      ''' + defbox([("SHACL", "Shapes Constraint Language: the W3C standard for checking that graph data obeys rules, looking only at the data it is given.")]) + '''
      ''' + callout("Session 3 did this too", "The untyped shipment of order 1447311670.7 was not refused: OWL concluded it was a Shipment. Inferring is what OWL is for; checking is not.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. Step through slowly and ask at step 2: is the reasoner wrong? No. OWL was designed for the web, where a missing fact usually means nobody wrote it down yet.</p>
<ul><li>The order is real; the lost carrier is not. Part B's test file plants exactly this fault on this order, and its header says so.</li>
<li>Our Session 3 ontology does not actually say "every order is carried by some carrier"; step 2 is the conditional. The point holds either way: without such an axiom OWL says nothing at all.</li></ul>'''))

# ---------------------------------------------------------------- Open and closed world, drawn
g = ""
W = FULL // 2 - 20
for i, (x0, title, sub) in enumerate([(0, "Open world · OWL", "not in the graph: unknown"),
                                     (W + 40, "Closed world · SHACL", "not in the graph: false")]):
    g += rect(x0, 4, W, 240, "var(--lu-paper)", LINE)
    g += text(x0 + 24, 34, title, anchor="start", color=INK2, weight=600)
    g += text(x0 + W - 24, 34, sub, "s-label", anchor="end", color=INK3)
    cx = x0 + W / 2
    if i == 0:
        g += circle(cx - 60, 140, 92, None, "muted", fill=False, dashed=True)
        g += text(cx - 60, 72, "true in the world", "s-label", color=INK3)
        g += circle(cx - 80, 158, 52, None, "green")
        g += text(cx - 80, 146, "what the", "s-label", color=GREEN)
        g += text(cx - 80, 170, "graph says", "s-label", color=GREEN)
        g += dot(cx - 2, 112, None, "ink")
        g += text(cx + 16, 112, "a carrier?", "s-label", anchor="start", color=INK2)
        g += text(cx + 16, 138, "maybe: unknown", "s-label", anchor="start", color=INK3)
    else:
        g += circle(cx - 60, 140, 92, None, "green")
        g += text(cx - 60, 128, "what the graph says", "s-label", color=GREEN)
        g += text(cx - 60, 152, "is the whole world", "s-label", color=GREEN)
        g += dot(cx + 62, 88, None, "red")
        g += text(cx + 80, 88, "a carrier?", "s-label", anchor="start", color=RED)
        g += text(cx + 80, 114, "not here: false", "s-label", anchor="start", color=RED)
pic = svg(FULL, 250, g, "Open world: the graph is part of what is true. Closed world: the graph is all that is true.")
SLIDES.append(slide("Open world and closed world", "Why OWL cannot check", 5, f'''  <div class="lu-eyebrow">The one idea behind this session</div>
  <h2 class="lu-h2">OWL treats the graph as part of the truth. SHACL treats it as the whole truth.</h2>
  {pic}
  <div class="lu-split">
    ''' + defbox([
      ("Open world assumption", "If a fact is missing, it is unknown, not false."),
      ("Closed world assumption", "If a fact is missing, it is false. How SQL databases behave."),
    ]) + '''
    ''' + callout("Two tools, two jobs", "Use OWL to <b>add</b> what follows from the data. Use SHACL to <b>check</b> the data you actually hold. A real system runs both, on the same graph.") + '''
  </div>''', '''<p>Five minutes. Both terms were previewed in Session 1 (the open world surprise) and used in Session 3; here they finally do opposite jobs side by side.</p>
<ul><li>The question students ask: can't I just close the world in OWL? Partly (owl:FunctionalProperty, cardinalities), but OWL then infers equalities or declares the whole ontology inconsistent; it never produces a list of the orders to fix. That list is what SHACL gives.</li></ul>'''))

# ---------------------------------------------------------------- Four things a reasoner will never catch
cards = [
    ("A missing value", "Order 1447291369.7 with no carrier.", "Some carrier exists, name unknown.", "MinCount: Violation."),
    ("One value too many", "An order carried by both V444_0 and V444_1.", "If carried by is functional: the two carriers are the same carrier.", "MaxCount: Violation."),
    ("A value outside the list", 'Service level <code>"DTX"</code>, a typo for DTD.', "A string, like any other.", "In ( CRF DTD DTP ): Violation."),
    ("A value outside the range", "Orders 1447336276.7 and 1447215484.7 weigh 0 kg.", "0 is a decimal: nothing to say.", "MinExclusive 0: Violation, on the real data."),
]
grid = "".join(
    f'<div class="lu-card"><span class="lu-card__label">{t}</span><p class="lu-sub">{ex}</p>'
    f'<p class="lu-sub"><b>OWL:</b> {owl}</p><p class="lu-sub" style="color:var(--lu-red-700)"><b>SHACL:</b> {sh}</p></div>'
    for t, ex, owl, sh in cards)
SLIDES.append(slide("Four things a reasoner will never catch", "Why OWL cannot check", 4,
    head("What goes wrong in real data", "Four everyday data errors. OWL accepts all four. SHACL reports all four.") + f'''
  <div class="lu-cards" style="grid-template-columns:repeat(2,minmax(0,1fr));margin-top:var(--lu-s3)">{grid}</div>''',
    '''<p>Four minutes. Card 2 surprises people most: declaring a property functional does not stop two carriers; the reasoner merges them into one carrier (or, if they are declared different, declares the ontology inconsistent). Neither is a list of orders to fix.</p>
<ul><li>Card 4 is not an example: it is the real Brunel data. Two orders of 361 and 348 units have weight 0 kg. Session 1 did not catch them; the first shape run did (Part 2).</li>
<li>Cards 1 to 3 are the faults Part B's test file plants on real orders.</li></ul>'''))

# ---------------------------------------------------------------- Check
SLIDES.append(slide("Check: what does the reasoner say?", "Why OWL cannot check", 3, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-mcq" data-qid="s4-q1" data-answer="c" data-label="What a reasoner reports for a missing required value"
       data-fb-correct=" Open world: missing is unknown, so it assumes a carrier it cannot name."
       data-fb-wrong=" Ask what the open world assumption says about a fact that is simply not there.">
    <p class="lu-mcq__q">Every order is carried by <b>some</b> carrier. Order 1447291369.7 has none. What does HermiT report?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">The ontology is inconsistent<span class="lu-mcq__why" hidden>A missing value contradicts nothing.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">The class Order is unsatisfiable<span class="lu-mcq__why" hidden>Orders can still exist; this one has an unnamed carrier.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">Nothing: it assumes a carrier exists that it cannot name<span class="lu-mcq__why" hidden>Correct. That is the open world assumption at work.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="d">A MinCount Violation for that order<span class="lu-mcq__why" hidden>That is SHACL's answer. A reasoner writes no report of broken rules.</span></button>
    </div>
  </div>''', '''<p>Three minutes. Answer d is the useful wrong answer: it shows the student already expects the tool of this session.</p>''', kind="tint"))
