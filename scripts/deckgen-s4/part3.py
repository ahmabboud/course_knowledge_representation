"""Session 4, Part 3: the Session 1 business rules as shapes, SPARQL
constraints, and triage of the first real report.

Numbers: reference-outputs/validate-v0.txt (3,435 violations),
validate-triaged.txt (2 violations, 2,579 warnings), shape-timings.txt;
the 854 / 1,370 split is Session 1's (s1-facts.txt) and Session 2's Q6.
"""
from common import slide, divider, defbox, callout, code
from kit import flow, node, edge, head, table, bar

SLIDES = []

K = '<span class="tok-kw">'
S = '<span class="tok-str">'
C = '<span class="tok-com">'
V = '<span class="tok-var">'
E = '</span>'

SLIDES.append(divider("Part 3 · The rules as shapes", "Rules as shapes",
    "Part 3 of 5 · about 30 minutes",
    "Session 1 wrote the rules in English. The first run says 3,435 are broken. Are they?",
    "A report is a list of work. Some of the work is fixing the rule."))

# ---------------------------------------------------------------- From the inventory to shapes
rows = [
    ("One carrier, one plant, one date, one service level per order", "core", "0"),
    ("An order weighs more than 0 kg", "core", "<b style=\"color:var(--lu-red-700)\">2</b>"),
    ("A band's lower bound is not above its upper bound", "core, two values", "0"),
    ("A rate band belongs to a carrier", "core", "<b style=\"color:var(--lu-red-700)\">1,209</b>"),
    ("A plant ships only through ports it is linked to", "SPARQL", "0"),
    ("A plant ships only products it makes", "SPARQL", "0"),
    ("An order's weight falls in a rate band of its lane", "SPARQL", "<b style=\"color:var(--lu-red-700)\">2,224</b>"),
    ("CRF orders are carried by V44_3", "SPARQL", "you write it (Part B)"),
]
SLIDES.append(slide("From the inventory to shapes", "Rules as shapes", 5,
    head("Session 1's list, as a first draft", "Each business rule becomes one shape. Four need SPARQL: they compare an order with other nodes.") +
    table(["Business rule (Session 1)", "Kind of shape", "First draft, results"], rows) + '''
  <p class="lu-caption"><code>brunel-shapes-v0.ttl</code> on the Session 2 graph: <b>3,435 Violations</b> in 90 seconds. Every rule was written as a Violation.</p>''',
    '''<p>Five minutes. The first draft is what anyone writes from the English list: every rule, all Violations. Real run, <code>reference-outputs/validate-v0.txt</code>.</p>
<ul><li>The two SPARQL rules with 0 results confirm Session 1's evidence on all 9,215 orders: no order leaves through an unlinked port, none ships a product its plant does not make.</li>
<li>The weight rule is new: Session 1 had no rule for it. Adding a rule you did not think of is normal; the gate keeps it from then on.</li></ul>'''))

# ---------------------------------------------------------------- sh:sparql
q = (f'''uls:LinkedPortShape {K}a{E} sh:NodeShape ;
    sh:targetClass ul:Order ;
    sh:sparql [
        sh:message {S}"Order leaves through {{?port}}, which its plant does not ship through."{E} ;
        sh:prefixes &lt;https://ul.edu.lb/kr/shapes&gt; ;
        sh:select """
            {K}SELECT{E} {V}$this{E} {V}?plant{E} {V}?port{E} {K}WHERE{E} {{
                {V}$this{E} ul:fromPlant {V}?plant{E} ; ul:shipsFrom {V}?port{E} .
                {K}FILTER NOT EXISTS{E} {{ {V}?plant{E} ul:servesPort {V}?port{E} }}
            }}""" ] .''')
SLIDES.append(slide("sh:sparql, the escape hatch", "Rules as shapes", 5, '''  <div class="lu-eyebrow">When core SHACL cannot say it</div>
  <h2 class="lu-h2">The rule compares the order's port with its plant's ports. That needs a query.</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code("brunel-shapes.ttl · uls:LinkedPortShape", q, small=False) + '''
    <div class="lu-stack">
      ''' + defbox([
        ("SHACL-SPARQL", "A SHACL rule written as a SPARQL query. Each row the query returns is one result."),
        ("$this", "The focus node being checked, filled in for every order in turn."),
      ]) + '''
      ''' + callout("Result on Brunel", "0 of 9,215 orders. Session 1's rule holds on every order, now checked by a machine.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. Read the query as a sentence: find this order's plant and port, and return the order if the plant has no link to that port.</p>
<ul><li>A query returns problems, not matches: an empty result is good news. That surprises people who write SELECT to find what they want.</li>
<li>Prefixes: <code>sh:prefixes</code> points at the ontology node that declares <code>ul:</code> with <code>sh:declare</code>. The old template's <code>sh:prefixes ul:</code> is not standard and fails in pySHACL.</li></ul>'''))

# ---------------------------------------------------------------- Walkthrough: triage
n = [
    node("d", "first draft\n3,435 violations", 140, 165, 240, 78, kind="builtin"),
    node("g1", "2,224 · weight in\nno rate band", 520, 73, 300, 70, kind="builtin"),
    node("g2", "1,209 · band carrier\nnot a Carrier", 520, 200, 300, 70, kind="builtin"),
    node("g3", "2 · weight 0 kg", 520, 298, 300, 56, kind="builtin"),
    node("h1", "854 CRF orders, never priced:\nfix the shape, priced lanes only", 1135, 34, 570, 62, kind="builtin"),
    node("h2", "1,370 in the rate table's gap:\nkeep, as a Warning", 1135, 112, 570, 62, kind="builtin", flag="right"),
    node("k2", "typed only if it carries an order:\na Warning until Session 5", 1135, 200, 570, 62, kind="builtin", flag="right"),
    node("k3", "361 units cannot weigh 0:\nstays a Violation", 1135, 298, 570, 56, kind="builtin", flag="right"),
]
e = [
    edge("e1", "d", "g1", "", route="elbow"), edge("e2", "d", "g2", ""), edge("e3", "d", "g3", "", route="elbow"),
    edge("f1", "g1", "h1", "shape wrong", route="elbow"), edge("f2", "g1", "h2", "data wrong", route="elbow"),
    edge("f3", "g2", "k2", "conversion"), edge("f4", "g3", "k3", "data wrong"),
]
steps = [
    {"show": ["d", "g1", "g2", "g3", "e1", "e2", "e3"], "run": ["e1", "e2", "e3"],
     "set": {"g1": "impossible", "g2": "impossible", "g3": "impossible"}},
    {"show": ["h1", "f1"], "run": ["f1"], "set": {"g1": "active"}},
    {"show": ["h2", "f2"], "run": ["f2"], "set": {"h2": "inferred"}},
    {"show": ["k2", "f3"], "run": ["f3"], "set": {"g1": "idle", "g2": "active", "k2": "inferred"}},
    {"show": ["k3", "f4"], "run": ["f4"], "set": {"g2": "idle", "g3": "active", "k3": "impossible"}},
]
caps = [
    ("The first report", "<b>Step 1.</b> Three groups of results, all Violations: 2,224, 1,209 and 2."),
    ("Shape wrong", "<b>Step 2.</b> 854 of the 2,224 are the CRF orders, all carrier V44_3. Session 1 found CRF is <b>not in the rate table at all</b>. The rule only means something on a priced lane: the shape was wrong."),
    ("Data wrong, elsewhere", "<b>Step 3.</b> The other 1,370 are all on one lane, V444_1 · PORT04 · DTD, 1,364 in one hole between 2.5 and 70.51 kg. The orders are fine; the <b>rate table</b> has a gap."),
    ("The conversion's fault", "<b>Step 4.</b> 1,209 bands belong to 7 carriers that carry no order. Session 2's converter types a carrier only when an order uses it. Fix the mapping in Session 5."),
    ("Data wrong", "<b>Step 5.</b> The 2 zero weight orders are simply wrong. After triage: <b>2 Violations, 2,579 Warnings</b>."),
]
walk = flow("Triage of the first report", 1448, 330, n, e, steps, caps,
            flags={"impossible": "violation", "inferred": "warning"},
            legend={"builtin": "SHACL result", "impossible": "Violation", "inferred": "Warning"})
SLIDES.append(slide("Walkthrough: triage of the first report", "Rules as shapes", 6, '''  <div class="lu-eyebrow">Diagnostic walkthrough</div>
  <h2 class="lu-h2">3,435 Violations. Only 2 are the orders' fault.</h2>
  ''' + walk, '''<p>Six minutes, the most important slide of the session. At step 2 ask the room before showing it: the 854 all have carrier V44_3; what did Session 1 say about V44_3?</p>
<ul><li>Every split is real: 854 = the CRF orders (Session 1); 1,370 = Session 2's Q6 answer; 2,224 = Q6 without its priced-lane filter. The triaged file adds exactly that filter.</li>
<li>Amber here means Warning, not inferred: this diagram has no reasoner in it. Red is the only thing that blocks.</li>
<li>The 1,209: the 7 carriers are V444_2 and V444_4 to V444_9, present only in FreightRates.</li></ul>'''))

# ---------------------------------------------------------------- Recording the decision
rec = (f'''sh:property [
    sh:path ul:bandCarrier ; sh:class ul:Carrier ;
    sh:severity sh:Warning ;
    rdfs:comment {S}"TRIAGE: data incomplete, the conversion's fault.
      The Session 2 converter types a carrier ul:Carrier only
      when it carries an order, so the 7 carriers that appear
      only in FreightRates are untyped, 1,209 bands. Fix it in
      the mapping (Session 5); a Warning until then."{E} ] .''')
SLIDES.append(slide("Triage: rule wrong, or data wrong?", "Rules as shapes", 4, '''  <div class="lu-eyebrow">Writing the decision down</div>
  <h2 class="lu-h2">Every triage decision lives next to its rule, with the evidence</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code("brunel-shapes.ttl · the band carrier rule, after triage", rec, small=False) + '''
    <div class="lu-stack">
      ''' + defbox([("Triage", "Going through a report result by result, and deciding for each whether the rule or the data is wrong, and what to do.")]) + '''
      ''' + callout("Three honest answers", "<b>Rule wrong:</b> change the rule. <b>Data wrong:</b> fix the source, keep the rule. <b>Known and accepted for now:</b> lower the severity, and say until when.") + '''
    </div>
  </div>''', '''<p>Four minutes. The comment is the real text in <code>brunel-shapes.ttl</code>; every triaged rule has one starting TRIAGE.</p>
<ul><li>Never delete a rule to make a report green. Deleting the weight in band rule would hide the rate table's gap from everyone after you.</li></ul>'''))

# ---------------------------------------------------------------- Poll
SLIDES.append(slide("Poll: violation or warning?", "Rules as shapes", 4, '''  <div class="lu-eyebrow">Room poll · 45 seconds</div>
  <div class="lu-poll" data-qid="s4-poll" data-seconds="45" data-answer="b" data-label="How to treat the 1,370 orders in the rate table's gap">
    <p class="lu-mcq__q">1,370 orders weigh an amount no rate band of their lane covers, because the rate table has a gap. What should the rule say?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">Keep it a Violation: the gate must stop them<span class="lu-mcq__why" hidden>The orders are correct; blocking every change until someone else fixes a price table stops all work.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">Make it a Warning, with a note on who fixes the table<span class="lu-mcq__why" hidden>Correct. The problem stays visible in every report, and work is not blocked.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">Delete the rule: the orders are fine<span class="lu-mcq__why" hidden>Then nobody ever sees the gap again, including whoever owns the rate table.</span></button>
    </div>
  </div>''', '''<p>Forty five seconds, then reveal and tally. Spend the rest on a and c: both are common in practice, and both are wrong for opposite reasons.</p>''', kind="tint", extra_attr=' style="--lu-s5:12px"'))

# ---------------------------------------------------------------- The cost of SPARQL
tim = [("Order shape", "core, 7 rules", 2.6), ("Rate band shape", "core, 2 rules", 1.2),
       ("Linked port", "SPARQL", 15.8), ("Plant makes product", "SPARQL", 16.1),
       ("Weight in a rate band", "SPARQL", 73.1)]
rows = "".join(
    f'<div class="lu-row" style="gap:var(--lu-s4);align-items:center">'
    f'<span style="width:15ch"><b>{nm}</b><br><span class="lu-caption">{kd}</span></span>'
    f'<span style="flex:1">{bar(sec, 73.1, f"{sec:.1f} s", "red" if kd == "SPARQL" else "ink")}</span></div>'
    for nm, kd, sec in tim)
SLIDES.append(slide("The cost of reaching for SPARQL too early", "Rules as shapes", 4,
    head("Each shape timed alone, on the 9,215 orders", "One SPARQL rule costs 28 times the whole core order shape") + f'''
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack" style="gap:var(--lu-s3)">{rows}</div>
    <div class="lu-stack">
      ''' + callout("Why", "pySHACL runs a SPARQL rule once per focus node: 9,215 small queries. Session 2 answered the same weight question as one query in under 3 seconds.") + '''
      ''' + callout("The rule of thumb", "Write it in core SHACL if you can. Reach for SPARQL only when a rule compares a node with other nodes.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. Real timings, pySHACL 0.40.1 in the course workspace (<code>reference-outputs/shape-timings.txt</code>); students' laptops will differ, the ratio will not.</p>
<ul><li>GS1's EPCIS shapes, 1,138 lines (Part 5), contain no SPARQL rule at all.</li></ul>'''))

# ---------------------------------------------------------------- Check
SLIDES.append(slide("Check: which rule needs SPARQL?", "Rules as shapes", 3, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-mcq" data-qid="s4-q2" data-answer="c" data-label="Which Brunel rule needs a SPARQL constraint"
       data-fb-correct=" Correct. It compares the order with rate band nodes elsewhere in the graph."
       data-fb-wrong=" Not quite. Ask whether the rule looks only at the order's own values, or at other nodes.">
    <p class="lu-mcq__q">Which of these rules <b>needs</b> a SPARQL constraint?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">Every order has exactly one carrier<span class="lu-mcq__why" hidden>Counting values: sh:minCount and sh:maxCount.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">A band's lower bound is not above its upper bound<span class="lu-mcq__why" hidden>Two values of the same node: core, sh:lessThanOrEquals.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">An order's weight falls in a rate band of its lane<span class="lu-mcq__why" hidden>Correct: it has to find the bands of the lane, other nodes of the graph.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="d">The service level is CRF, DTD or DTP<span class="lu-mcq__why" hidden>A list of values: sh:in.</span></button>
    </div>
  </div>''', '''<p>Three minutes. Option b is the trap: comparing two numbers sounds like it needs a query, but both are values of the same node.</p>''', kind="tint"))
