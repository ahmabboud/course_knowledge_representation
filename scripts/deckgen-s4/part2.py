"""Session 4, Part 2: SHACL core, on the Session 2 graph.

Numbers: reference-outputs/validate-v0.txt, validate-triaged.txt,
targeting-trap.txt, shape-timings.txt (pySHACL 0.40.1, 2026-09-25).
"""
from common import slide, divider, defbox, callout, code
from kit import flow, node, edge, head, table

SLIDES = []

K = '<span class="tok-kw">'
S = '<span class="tok-str">'
C = '<span class="tok-com">'
N = '<span class="tok-num">'
E = '</span>'

SLIDES.append(divider("Part 2 · Shapes on the real graph", "SHACL core",
    "Part 2 of 5 · about 30 minutes",
    "How do you tell a machine: every order has exactly one carrier?",
    "You describe the shape the data must have, and let it compare."))

# ---------------------------------------------------------------- Shape, target, focus nodes, report
n = [
    node("sh", "Order shape", 130, 45, 220, 60, kind="builtin"),
    node("t", "target:\nevery ul:Order", 440, 45, 250, 66, kind="builtin"),
    node("f", "9,215 focus nodes\n(192 late orders too)", 790, 45, 320, 66, kind="individual"),
    node("c", "7 property\nchecks each", 1110, 45, 210, 66, kind="builtin"),
    node("r", "report:\n2 results", 1340, 45, 190, 66, kind="builtin", flag="bottom"),
]
e = [edge("a", "sh", "t", ""), edge("b", "t", "f", "selects"), edge("c1", "f", "c", ""), edge("d", "c", "r", "")]
steps = [
    {"show": ["sh", "t", "a"], "run": ["a"], "set": {"t": "active"}},
    {"show": ["f", "b"], "run": ["b"], "set": {"t": "idle", "f": "active"}},
    {"show": ["c", "c1"], "run": ["c1"], "set": {"f": "idle", "c": "active"}},
    {"show": ["r", "d"], "run": ["d"], "set": {"c": "idle", "r": "impossible"}},
]
caps = [
    ("A shape and its target", "<b>Step 1.</b> A shape names its target: here every member of <b>ul:Order</b>."),
    ("Focus nodes", "<b>Step 2.</b> The target selects 9,215 focus nodes: 9,023 orders, plus the 192 late orders, because the graph says every late order is an order (rdfs:subClassOf)."),
    ("Checks", "<b>Step 3.</b> Each focus node is checked against the shape's rules: one carrier, one date, a weight above 0, and four more."),
    ("The report", "<b>Step 4.</b> One result per broken rule per node. On the real graph: 2 results, the two orders that weigh 0 kg. It took 2.6 seconds."),
]
walk = flow("How one shape runs", 1448, 112, n, e, steps, caps, flags={"impossible": "2 violations"},
            legend={"builtin": "SHACL", "individual": "Our data", "impossible": "Violation"})
SLIDES.append(slide("A shape, a target, a report", "SHACL core", 5, '''  <div class="lu-eyebrow">How validation works</div>
  <h2 class="lu-h2">A shape picks its nodes, checks each one, and writes one line per broken rule</h2>
  ''' + walk + '''
  <div class="lu-split">
    ''' + defbox([
      ("Shape", "A named set of rules that some nodes of the graph must obey."),
      ("Target", "Which nodes a shape checks, for example every member of a class."),
    ]) + defbox([
      ("Focus node", "The node being checked when a shape runs."),
      ("Validation report", "SHACL's output: conforms or not, and one result per broken rule."),
    ], label="Also defined here") + '''
  </div>''', '''<p>Five minutes. The numbers are real: <code>python validate.py</code> on the 135,841 triple Session 2 graph (<code>reference-outputs/validate-triaged.txt</code>) and the order shape timed alone (<code>shape-timings.txt</code>, 2.6 s).</p>
<ul><li>Step 2 is worth a sentence: SHACL follows rdfs:subClassOf <i>in the data graph</i> when it resolves a target class. That is why the 192 late orders, typed only ul:LateOrder, are still checked.</li></ul>'''))

# ---------------------------------------------------------------- Node shape and property shapes in Turtle
ttl = (f'''uls:OrderShape {K}a{E} sh:NodeShape ;
    sh:targetClass ul:Order ;
    sh:property [
        sh:path ul:carriedBy ; sh:minCount {N}1{E} ; sh:maxCount {N}1{E} ;
        sh:class ul:Carrier ] ;
    sh:property [
        sh:path ul:serviceLevel ; sh:in ( {S}"CRF"{E} {S}"DTD"{E} {S}"DTP"{E} ) ] ;
    sh:property [
        sh:path ul:weight ; sh:datatype xsd:decimal ;
        sh:minExclusive {N}0{E} ] .           {C}# four more in the file{E}''')
SLIDES.append(slide("Node shapes and property shapes", "SHACL core", 5, '''  <div class="lu-eyebrow">Writing a shape</div>
  <h2 class="lu-h2">One node shape for &ldquo;every order&rdquo;, one property shape per rule</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code("brunel-shapes.ttl · uls:OrderShape, shortened", ttl, small=False) + '''
    <div class="lu-stack">
      ''' + defbox([
        ("Node shape", "A shape about a whole node: every order."),
        ("Property shape", "A shape about one property of that node: exactly one carrier."),
      ]) + '''
      ''' + callout("Which SHACL", "SHACL 1.0, a W3C Recommendation since 2017. SHACL 1.2 Core is still a Working Draft (3 August 2026): build on 1.0.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. Read the shape aloud as English: every order has exactly one carrier, and it is a Carrier; a service level from this list; a decimal weight above 0.</p>
<ul><li>A shapes file is ordinary Turtle, so it can live in the same repository, be diffed and reviewed like code. The full file is <code>demos/session-04-shacl/brunel-shapes.ttl</code>.</li>
<li>Standards status checked on w3.org on 2026-09-25: SHACL 1.2 Core is a Working Draft dated 3 August 2026.</li></ul>'''))

# ---------------------------------------------------------------- The targeting trap
out = (f'''$ python validate.py --shapes shapes_template.ttl
  focus nodes      0  PurchaseOrderShape   {C}&lt;- targets nothing{E}
validated in 0.6 s. conforms (SHACL): {K}True{E}
GATE: PASS, no violations.''')
SLIDES.append(slide("The targeting trap", "SHACL core", 4, '''  <div class="lu-eyebrow">The most common SHACL bug</div>
  <h2 class="lu-h2">A shape that targets nothing checks nothing, and the report still says &ldquo;conforms&rdquo;</h2>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      ''' + code("a real run: the old Session 4 template on the Brunel graph", out, small=False) + '''
      <p class="lu-caption">The template targets <code>ul:PurchaseOrder</code>. Our graph has 9,215 <code>ul:Order</code> nodes and not one <code>ul:PurchaseOrder</code>.</p>
    </div>
    <div class="lu-stack">
      ''' + callout("Green is not proof", "A clean report on zero focus nodes means nothing was looked at. <b>Read the focus node count before the result.</b>") + '''
      ''' + callout("Our tools print it first", "<code>validate.py</code> lists every shape's focus nodes before validating. shacl-play warns &ldquo;Shapes did not match anything!&rdquo;", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. This is a real run on 2026-09-25 (<code>reference-outputs/targeting-trap.txt</code>): the course's own old template shape, written before the Session 2 graph existed, silently passes.</p>
<ul><li>Ask: what would a CI gate have done with this? Passed every commit, forever. Part B's checker refuses a shape with no focus nodes for exactly this reason.</li></ul>'''))

# ---------------------------------------------------------------- Constraint types
rows = [
    ("<code>sh:minCount</code> · <code>sh:maxCount</code>", "how many values", "exactly one carrier", "0"),
    ("<code>sh:datatype</code>", "the kind of value", "weight is an <code>xsd:decimal</code>", "0"),
    ("<code>sh:in</code>", "one of a list", "service level CRF, DTD or DTP", "0"),
    ("<code>sh:pattern</code>", "text matches a pattern", "order id: digits, a dot, one digit", "0"),
    ("<code>sh:minExclusive</code>", "above a bound", "weight above 0 kg", "<b style=\"color:var(--lu-red-700)\">2</b>"),
    ("<code>sh:class</code>", "the value's type", "a band's carrier is a <code>ul:Carrier</code>", "<b style=\"color:var(--lu-red-700)\">1,209</b>"),
    ("<code>sh:lessThanOrEquals</code>", "two values compared", "a band's lower bound &le; its upper bound", "0"),
]
SLIDES.append(slide("Seven kinds of rule", "SHACL core", 5,
    head("Core SHACL, on our graph", "Seven kinds of rule cover most of Session 1's list. Two of them already find problems.") +
    table(["Constraint", "Says", "Our rule", "Results on Brunel"], rows) + '''
  <p class="lu-caption">First draft of <code>brunel-shapes.ttl</code>, run on the 9,215 orders and 1,540 rate bands of the Session 2 graph.</p>''',
    '''<p>Five minutes. Go down the last column: five rules hold on every order. The two that do not are the next two slides and Part 3.</p>
<ul><li>All counts from <code>reference-outputs/validate-v0.txt</code>. The 1,209 are rate bands whose carrier is not typed ul:Carrier; Part 3 explains why, and whose fault it is.</li></ul>'''))

# ---------------------------------------------------------------- Two orders that weigh nothing
rows = [
    ("1447336276.7", "361", "<b style=\"color:var(--lu-red-700)\">0 kg</b>", "V444_0", "DTP"),
    ("1447215484.7", "348", "<b style=\"color:var(--lu-red-700)\">0 kg</b>", "V444_0", "DTP"),
    ("next lightest order", "", "0.0026 kg", "", ""),
]
SLIDES.append(slide("Two orders that weigh nothing", "SHACL core", 4, '''  <div class="lu-eyebrow">A real finding</div>
  <h2 class="lu-h2">The first run found two orders that Session 1's profiling missed</h2>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      ''' + table(["Order", "Units", "Weight", "Carrier", "Service"], rows) + '''
      <p class="lu-caption">From the Session 2 graph. Every other order weighs more than 0.0026 kg.</p>
    </div>
    <div class="lu-stack">
      ''' + callout("Why nobody saw them", "A profile reports the weight column's minimum, 0, among dozens of other numbers: easy to read past. A rule that says <b>above 0</b> cannot overlook it.") + '''
      ''' + callout("Rule wrong, or data wrong?", "Hundreds of units cannot weigh nothing. The rule is right; the two rows are wrong. Part 3 names this decision: triage.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. This is the value of writing rules down: profiling shows you what the data is; a rule says what it must be, and runs every time.</p>
<ul><li>Checked on 2026-09-25 with pyoxigraph on <code>brunel.ttl</code>: exactly two orders have weight 0; the smallest non-zero weight is 0.0026 kg.</li></ul>'''))

# ---------------------------------------------------------------- Severity and conforms
rows = [
    ("<b>Violation</b>", "the default: the data breaks the rule", "2 (weight 0 kg)"),
    ("<b>Warning</b>", "worth a look, not an error", "2,579 (Part 3)"),
    ("<b>Info</b>", "for the record", "0"),
]
SLIDES.append(slide("Severity, and what conforms means", "SHACL core", 4, '''  <div class="lu-eyebrow">Reading the top of a report</div>
  <h2 class="lu-h2">Any result at all makes conforms false. A gate decides which results block.</h2>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      ''' + table(["Severity", "Meaning", "Our triaged run"], rows) + '''
      ''' + defbox([("Severity", "How serious a broken rule is: Violation, Warning or Info, set per rule with <code>sh:severity</code>.")]) + '''
    </div>
    <div class="lu-stack">
      ''' + callout("The rule in SHACL 1.0", "<code>sh:conforms</code> is true only when there are <b>no results of any severity</b>. Our triaged run: conforms false.") + '''
      ''' + callout("The rule in our gate", "<code>validate.py</code> fails only on a Violation. Warnings are printed and pass. pySHACL's own switch for this is <code>allow_warnings</code>.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. Many people believe a Warning leaves conforms true. It does not: checked with pySHACL 0.40.1 on 2026-09-25, a report with only Warnings has conforms False unless you pass <code>allow_warnings=True</code>.</p>
<ul><li>So "does it conform?" and "may this change go in?" are two different questions. SHACL answers the first; the team decides the second, and writes it into the gate.</li></ul>'''))

# ---------------------------------------------------------------- Drill
SLIDES.append(slide("Drill: core SHACL words", "SHACL core", 3, '''  <div class="lu-eyebrow">Drill · type the missing word</div>
  <div class="lu-blanks" data-qid="s4-blanks1" data-label="Core SHACL words">
    <p class="lu-h3" style="margin-bottom:var(--lu-s4)">Fill in the blanks</p>
    <ol class="lu-list lu-list--num">
      <li>To check every member of <code>ul:Order</code>, a shape uses <input class="lu-blank lu-blank--wide" data-answer="sh:targetClass|targetClass" data-label="Blank 1" placeholder="…">.</li>
      <li>&ldquo;Exactly one carrier&rdquo; needs both <code>sh:minCount 1</code> and <input class="lu-blank lu-blank--wide" data-answer="sh:maxCount 1|sh:maxCount|maxCount 1|maxCount" data-label="Blank 2" placeholder="…">.</li>
      <li>&ldquo;Service level is CRF, DTD or DTP&rdquo; is written with <input class="lu-blank" data-answer="sh:in|in" data-label="Blank 3" placeholder="…">.</li>
      <li>A shape with 0 focus nodes reports conforms <input class="lu-blank" data-answer="true" data-label="Blank 4" placeholder="…">, and has checked nothing.</li>
    </ol>
  </div>''', '''<p>Three minutes. Blank 4 is the one to discuss: it is the targeting trap in one line.</p>''', kind="tint"))
