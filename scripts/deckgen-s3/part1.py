"""Session 3: opening and Part 1, what an ontology is.

The cast is the course's one cast (AGENTS.md 2c rule 4): real Brunel orders
and carriers from Sessions 1 and 2. Carrier V444_1 carries a labelled teaching
flag, "sanctioned", which nothing in the data says. Colours follow lu-flow:
blue ours (ul:), teal reused (ioc:, IOF SCRO), green individuals, grey values.
"""
from common import slide, divider, defbox, callout
from kit import flow, node, edge
from svgkit import svg, text, line, dot, rect, box, FULL, WL, INK, INK3, LINE, BLUE, BLUE_BG, GREEN, GREEN_BG

SLIDES = []
LEGEND = {"ours": "Our ontology (ul:)", "reused": "Reused, IOF SCRO (ioc:)", "individual": "Individual",
          "literal": "Value"}

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
      <div class="lu-eyebrow">Knowledge Representation · Session 3 of 8</div>
      <h1 class="lu-display" style="max-width:24ch">Ontology Engineering: Description Logic, OWL, and Reuse</h1>
      <p class="lu-lead" style="max-width:46ch">Today you write down what our supply chain words mean, in a form a machine can reason with. Then a reasoner finds a real mistake in our own ontology, and you fix it.</p>
    </div>
    <div class="lu-row" style="justify-content:space-between;font-size:var(--lu-t-caption);color:var(--lu-on-night-2)">
      <span>About 230 minutes · lecture, lab in Protégé and Python, wrap</span>
      <span>Press <kbd>&rarr;</kbd> to begin · <kbd>?</kbd> for shortcuts</span>
    </div>
  </div>
  <template data-notes>
    <p>This session runs long on purpose (about 230 minutes, agreed with the instructor on 2026-09-22): it carries the ontology the rest of the course builds on.</p>
    <ul>
      <li>Before minute one: every student has Protégé 5.6 open and has run <code>python fetch_ontologies.py</code> once in <code>demos/session-03-ontology/</code>. If not, they do it during Part 1; the lab needs it.</li>
      <li>Nothing here assumes logic or semantic web background. Every term is defined on the slide where it first appears, in a green "Defined on this slide" box, and later uses are clickable.</li>
    </ul>
  </template>
</section>
''')

# ---------------------------------------------------------------- Recap
SLIDES.append(slide("Where we are in the architecture", "Opening", 3, '''  <div class="lu-eyebrow">Recap</div>
  <h2 class="lu-h1" style="max-width:40ch">Sessions 1 and 2 put the data in a graph. Nothing yet says what it <em style="font-style:italic;color:var(--lu-red-700)">means</em>.</h2>
  <ul class="lu-pipeline" style="margin-top:var(--lu-s5)">
    <li data-state="done"><span class="lu-pipeline__n">01</span><span class="lu-pipeline__t">Sources</span><span class="lu-pipeline__d">DataCo, Brunel</span></li>
    <li data-state="done"><span class="lu-pipeline__n">02</span><span class="lu-pipeline__t">Profiling</span><span class="lu-pipeline__d">Business rules</span></li>
    <li data-state="done"><span class="lu-pipeline__n">03</span><span class="lu-pipeline__t">Graph</span><span class="lu-pipeline__d">RDF, SPARQL</span></li>
    <li data-state="active"><span class="lu-pipeline__n">04</span><span class="lu-pipeline__t">Ontology</span><span class="lu-pipeline__d">You are here</span></li>
    <li data-state="muted"><span class="lu-pipeline__n">05</span><span class="lu-pipeline__t">Constraints</span><span class="lu-pipeline__d">SHACL · 4</span></li>
    <li data-state="muted"><span class="lu-pipeline__n">06</span><span class="lu-pipeline__t">Mappings</span><span class="lu-pipeline__d">RML · 5</span></li>
    <li data-state="muted"><span class="lu-pipeline__n">07</span><span class="lu-pipeline__t">Learning</span><span class="lu-pipeline__d">GNN · 6</span></li>
    <li data-state="muted"><span class="lu-pipeline__n">08</span><span class="lu-pipeline__t">Access</span><span class="lu-pipeline__d">Questions · 7</span></li>
  </ul>
  <div class="lu-split" style="margin-top:var(--lu-s5)">
    ''' + callout("What you have", "The 9,215 Brunel orders as a graph you can query (Session 2), and a list of business rules found in the data (Session 1).", "neutral") + '''
    ''' + callout("What is missing", "Nothing tells a machine what <b>late</b>, <b>carrier</b> or <b>at risk</b> mean. Every system still guesses.") + '''
  </div>''', '''<p>Three minutes. Point at stage 04: this is where the course stops storing data and starts describing what it means.</p>'''))

# ---------------------------------------------------------------- Objective
SLIDES.append(slide("Session objective and shape", "Opening", 3, '''  <div class="lu-eyebrow">Objective</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <p class="lu-statement">By the end you can read and write the rules of an ontology, run a reasoner, understand what it reports, and fix a real mistake it finds in our own supply chain ontology.</p>
      ''' + callout("Open these now", "Protégé 5.6 · the folder <code>demos/session-03-ontology/</code> · its <code>workspace/</code>, created by <code>python fetch_ontologies.py</code>.", "concept") + '''
    </div>
    <div class="lu-card">
      <span class="lu-card__label">How the ~230 minutes are spent</span>
      <ul class="lu-layers">
        <li><span class="lu-layers__name">Lecture · ~140 min</span><span class="lu-layers__note">What an ontology is, writing rules, the reasoner, reuse and BFO, profiles</span></li>
        <li><span class="lu-layers__name">Lab · ~75 min</span><span class="lu-layers__note">Find the bug, fix it, let the reasoner classify, write three axioms of your own</span></li>
        <li><span class="lu-layers__name">Wrap · ~15 min</span><span class="lu-layers__note">Discussion, glossary, self-check</span></li>
      </ul>
    </div>
  </div>''', '''<p>Name the payoff early: in the lab the reasoner turns one of <i>our</i> classes red, and before the end of the session everyone knows exactly why and has seen it fixed.</p>''', kind="tint"))

# ---------------------------------------------------------------- Part 1 divider
SLIDES.append(divider("Part 1 · What an ontology is", "What an ontology is",
    "Part 1 of 5 · about 25 minutes",
    "One dataset. Three honest answers to &ldquo;how many orders were late?&rdquo;",
    "The disagreement is not in the data. It is in the word."))

# ---------------------------------------------------------------- One word, three numbers
SLIDES.append(slide("One word, three numbers", "What an ontology is", 4, '''  <div class="lu-eyebrow">Why this session exists</div>
  <h2 class="lu-h2">Same 65,752 DataCo orders. Three definitions of &ldquo;late&rdquo;. Three different answers.</h2>
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr))">
    <div class="lu-card"><span class="lu-card__label">Late means: any delay</span><div class="lu-display" style="color:var(--lu-ink)">57.3%</div><p class="lu-sub">Real shipping days greater than the scheduled days.</p></div>
    <div class="lu-card"><span class="lu-card__label">Late means: the label says so</span><div class="lu-display" style="color:var(--lu-ink)">54.8%</div><p class="lu-sub">The dataset's own column <code>Delivery Status</code> says &ldquo;Late delivery&rdquo;.</p></div>
    <div class="lu-card"><span class="lu-card__label">Late means: more than a day</span><div class="lu-display" style="color:var(--lu-ink)">23.7%</div><p class="lu-sub">Real shipping days more than one day over schedule.</p></div>
  </div>
  <div class="lu-split">
    ''' + callout("The problem", "Every number is correct. A dashboard, a model and a report can each pick a different one, and nobody notices.", "neutral") + '''
    ''' + callout("The fix this session builds", "Write the meaning down <b>once</b>, precisely, in a form every program reads the same way.") + '''
  </div>''', '''<p>Four minutes. All three numbers were computed on 2026-09-22 from the real file <code>demos/data/dataco/DataCoSupplyChainDataset.csv</code>: 65,752 distinct orders; 37,698 with real days &gt; scheduled (57.3%); 36,048 labelled "Late delivery" (54.8%); 15,578 more than one day late (23.7%).</p>
<ul><li>Ask the room first: which one is right? Every answer is defensible. That is the point: the meaning lives in people's heads, not in the data.</li></ul>'''))

# ---------------------------------------------------------------- An ontology in one picture
n = [
    node("ship", "Shipment", 300, 35, 240, 56, kind="reused"),
    node("atrisk", "At-risk shipment", 300, 125, 260, 56, kind="ours"),
    node("carrier", "Carrier", 1130, 35, 240, 56, kind="reused"),
    node("sanct", "Sanctioned carrier", 1130, 125, 280, 56, kind="ours"),
    node("s1", "shipment of order 1447291369.7", 470, 225, 400, 56, kind="individual"),
    node("c1", "carrier V444_1", 960, 225, 250, 56, kind="individual"),
]
e = [
    edge("a", "atrisk", "ship", "subclass of"),
    edge("b", "sanct", "carrier", "subclass of"),
    edge("c", "s1", "ship", "is a", route="elbow", sides=["top", "right"]),
    edge("d", "c1", "sanct", "is a", route="elbow", sides=["top", "left"]),
    edge("f", "s1", "c1", "handled by"),
]
pic = flow("An ontology in one picture", FULL, 260, n, e,
           [{"show": [x["id"] for x in n] + [x["id"] for x in e]}], legend=LEGEND)
SLIDES.append(slide("An ontology in one picture", "What an ontology is", 5, f'''  <div class="lu-eyebrow">The idea, drawn</div>
  <h2 class="lu-h2">An ontology names the kinds of things, and how things connect</h2>
  {pic}
  ''' + defbox([
    ("Ontology", "A machine readable description of the kinds of things in a domain and how they relate."),
    ("Class", "A named kind of thing, a square box: <b>Shipment</b>."),
    ("Individual", "One particular thing, a green pill: <b>carrier V444_1</b>."),
    ("Property", "A named connection, an arrow: <b>handled by</b>."),
  ]), '''<p>Five minutes. Walk the picture in plain words: "this shipment is a shipment; it is handled by carrier V444_1; V444_1 is a sanctioned carrier; every sanctioned carrier is a carrier".</p>
<ul><li>These are the real Brunel order and carrier from Sessions 1 and 2. <b>Sanctioned is a teaching flag</b>: nothing in the data says so, and V444_1 is an anonymised code, not a company. Say it out loud once.</li>
<li>Colour is meaning: blue is ours, teal is reused from IOF SCRO (Part 4 explains), green is one thing. The lab file <code>sample-shipments.ttl</code> holds exactly these individuals.</li></ul>'''))

# ---------------------------------------------------------------- The class tree
rows = [("owl:Thing", 0, "ink"), ("Shipment (reused)", 1, "reused"), ("Late shipment", 2, "ours"),
        ("Cancelled shipment", 2, "ours"), ("At-risk shipment", 2, "ours"), ("Carrier (reused)", 1, "reused"),
        ("Sanctioned carrier", 2, "ours"), ("Multi-route carrier", 2, "ours")]
g, pos = "", []
y0, dy, ind = 26, 44, 60
for i, (name, lvl, col) in enumerate(rows):
    pos.append((30 + lvl * ind, y0 + i * dy, lvl))
for i, (x, y, lvl) in enumerate(pos):
    if lvl == 0:
        continue
    for j in range(i - 1, -1, -1):
        if pos[j][2] == lvl - 1:
            px, py = pos[j][0], pos[j][1]
            break
    g += line(px, py + 12, px, y, LINE, 2)
    g += line(px, y, x - 12, y, LINE, 2)
for (name, lvl, col), (x, y, _) in zip(rows, pos):
    g += dot(x, y, None, col)
    g += text(x + 22, y, name, anchor="start", color=INK, weight=600 if lvl < 2 else None)
g += text(470, y0 + 3 * dy, "every late shipment", "s-label", anchor="start", color=INK3)
g += text(470, y0 + 3 * dy + 26, "is a shipment", "s-label", anchor="start", color=INK3)
tree = svg(WL, 350, g, "A class tree: owl:Thing, Shipment with three subclasses, Carrier with two")
SLIDES.append(slide("The class tree", "What an ontology is", 4, f'''  <div class="lu-eyebrow">Kinds of things, arranged from general to specific</div>
  <h2 class="lu-h2">Classes form a tree. Read each line as &ldquo;every &hellip; is a &hellip;&rdquo;</h2>
  <div class="lu-split lu-split--wide-left">
    {tree}
    <div class="lu-stack">
      ''' + defbox([
        ("Subclass", "A is a subclass of B when every member of A is also a member of B."),
        ("owl:Thing", "The class of everything. Every class sits somewhere below it."),
      ]) + '''
      ''' + callout("Why a tree, not a list", "A fact stated about <b>Shipment</b> is automatically true of every late, cancelled and at-risk shipment. You write it once.") + '''
    </div>
  </div>''', '''<p>Four minutes. Protégé draws the same tree; students see it in the lab. Read two lines aloud as sentences: "every late shipment is a shipment", "every sanctioned carrier is a carrier". Then the inheritance point in the callout: that is the whole reason for a tree.</p>
<p>All six of our classes are real classes in <code>scro-extension-reference.ttl</code>; Shipment and Carrier come from IOF SCRO.</p>'''))

# ---------------------------------------------------------------- Two kinds of arrow
n = [
    node("s1", "shipment of order\n1447291369.7", 600, 110, 290, 72, kind="individual"),
    node("c1", "carrier V444_1", 1200, 35, 250, 56, kind="individual"),
    node("w", "11.8", 1200, 185, 150, 56, kind="literal"),
    node("lab", '"shipment of order 1447291369.7"', 180, 110, 330, 56, kind="builtin"),
]
e = [
    edge("a", "s1", "c1", "handled by (to a thing)"),
    edge("b", "s1", "w", "weight in kg (to a value)"),
    edge("c", "s1", "lab", "label (a note)"),
]
pic = flow("Two kinds of arrow, plus notes", FULL, 220, n, e,
           [{"show": [x["id"] for x in n] + [x["id"] for x in e]}])
SLIDES.append(slide("Two kinds of arrow, plus notes", "What an ontology is", 4, f'''  <div class="lu-eyebrow">Properties</div>
  <h2 class="lu-h2">An arrow points to a thing, or to a value. Notes are for humans only.</h2>
  {pic}
  ''' + defbox([
    ("Object property", "Links a thing to a thing: <b>handled by</b>."),
    ("Datatype property", "Links a thing to a value (number, date, text): <b>weight in kg</b>."),
    ("Annotation property", "A note for humans. The reasoner ignores it."),
  ]), '''<p>Four minutes. The practical reason this matters: in Protégé, object and datatype properties live in two different tabs, and a value cannot be the start of another arrow.</p>
<ul><li>11.8 kg is this order's real weight in Brunel's OrderList (Session 2 stored it as <code>ul:weight</code>). Session 1 met the same order in the rate band gap.</li>
<li>Annotation properties in our file: <code>rdfs:label</code>, <code>skos:definition</code>, and the course's own <code>ul:answersCQ</code>.</li></ul>'''))

# ---------------------------------------------------------------- TBox and ABox
g = ""
g += rect(0, 4, FULL, 110, BLUE_BG, BLUE)
g += text(30, 34, "TBox · the rules", anchor="start", color=BLUE, weight=600)
g += text(FULL - 24, 34, "scro-extension-reference.ttl", "s-mono", anchor="end", color=INK3)
g += box(390, 76, 600, 46, "Every At-risk shipment is a Shipment", "plain")
g += box(1070, 76, 620, 46, "handled by: from a Shipment to a Carrier", "plain")
g += rect(0, 126, FULL, 110, GREEN_BG, GREEN)
g += text(30, 156, "ABox · the data", anchor="start", color=GREEN, weight=600)
g += text(FULL - 24, 156, "sample-shipments.ttl", "s-mono", anchor="end", color=INK3)
g += box(390, 198, 600, 46, "the shipment of 1447291369.7 is a Shipment", "plain")
g += box(1070, 198, 620, 46, "it is handled by carrier V444_1", "plain")
pic = svg(FULL, 240, g, "Two layers: rules about classes above, facts about individuals below")
SLIDES.append(slide("Two layers: rules and data", "What an ontology is", 4, f'''  <div class="lu-eyebrow">How an ontology file is organised</div>
  <h2 class="lu-h2">Rules about kinds of things above. Facts about particular things below.</h2>
  {pic}
  <div class="lu-split lu-split--wide-left">
    ''' + defbox([
      ("Axiom", "One statement in an ontology. Each white box above is one axiom."),
      ("TBox", "The rules part: axioms about classes and properties."),
      ("ABox", "The data part: axioms about individuals."),
    ]) + '''
    ''' + callout("Why keep them apart", "You can change the rules without touching the data, and load new data without touching the rules. The lab keeps them in two files.") + '''
  </div>''', '''<p>Four minutes. T is for terminology, A is for assertions: say it once, it helps them remember.</p>
<ul><li>In Session 5 the ABox will come from the database automatically; the TBox stays hand written. That is why the split matters beyond neatness.</li></ul>'''))

# ---------------------------------------------------------------- Check
SLIDES.append(slide("Check: rules or data?", "What an ontology is", 3, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-mcq" data-qid="s3-q1" data-answer="b" data-label="Which statement is an ABox axiom"
       data-fb-correct=" Correct. It is about one particular shipment and one particular carrier, so it belongs to the data."
       data-fb-wrong=" Not quite. Ask: is it about one particular thing, or about a whole kind of thing?">
    <p class="lu-mcq__q">Which of these is an <b>ABox</b> axiom, a fact about particular things?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">Every late shipment is a shipment<span class="lu-mcq__why" hidden>A rule about a whole class: TBox.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">The shipment of order 1447291369.7 is handled by carrier V444_1<span class="lu-mcq__why" hidden>Correct: two individuals and one property between them.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">&ldquo;Handled by&rdquo; goes from a shipment to a carrier<span class="lu-mcq__why" hidden>A rule about what the property connects: TBox.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="d">Sanctioned carrier is a subclass of Carrier<span class="lu-mcq__why" hidden>A relationship between two classes: TBox.</span></button>
    </div>
  </div>''', '''<p>Three minutes. If anyone picks c, that is the most useful wrong answer: it is about a property, not a particular thing, so it is a rule.</p>''', kind="tint"))
