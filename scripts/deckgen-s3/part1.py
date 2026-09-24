from common import slide, divider, defbox, callout
from svgkit import *

SLIDES = []

# ---------------------------------------------------------------- 01 Title
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
      <span>About 230 minutes · lecture, guided lab in Protégé, wrap</span>
      <span>Press <kbd>&rarr;</kbd> to begin · <kbd>?</kbd> for shortcuts</span>
    </div>
  </div>
  <template data-notes>
    <p>This session was rebuilt on 2026-09-22 to the course's visual first standard (AGENTS.md, section 2c). It runs long on purpose, like Sessions 4 to 6.</p>
    <ul>
      <li>Before minute one: every student has Protégé 5.6 open and has run <code>python fetch_ontologies.py</code> once. If not, they do it during Part 1; the lab needs it at minute 120.</li>
      <li>Nothing in this deck assumes logic or semantic web background. Every term is defined on the slide where it first appears, in a green "Defined on this slide" box.</li>
    </ul>
  </template>
</section>
''')

# ---------------------------------------------------------------- 02 Recap
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
    ''' + callout("What you have", "Real orders as a graph you can query (Session 2), and a list of business rules found in the data (Session 1).", "neutral") + '''
    ''' + callout("What is missing", "Nothing tells a machine what <b>late</b>, <b>carrier</b> or <b>at risk</b> mean. Every system still guesses.") + '''
  </div>''', '''<p>Three minutes. Point at stage 04: this is where the course stops storing data and starts describing what it means.</p>''', ))

# ---------------------------------------------------------------- 03 Objective
SLIDES.append(slide("Session objective and shape", "Opening", 3, '''  <div class="lu-eyebrow">Objective</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <p class="lu-statement">By the end you can read and write the rules of an ontology, run a reasoner, understand what it reports, and fix a real mistake it finds in our own supply chain ontology.</p>
      ''' + callout("Open these now", "Protégé 5.6 · the Protégé guide, <code>lectures/guide-protege.html</code> · the folder <code>demos/session-03-ontology/workspace/</code> (created by <code>python fetch_ontologies.py</code>).", "concept") + '''
    </div>
    <div class="lu-card">
      <span class="lu-card__label">How the ~230 minutes are spent</span>
      <ul class="lu-layers">
        <li><span class="lu-layers__name">Lecture · ~120 min</span><span class="lu-layers__note">What an ontology is, writing rules, reasoners, reuse and BFO, profiles</span></li>
        <li><span class="lu-layers__name">Guided lab · ~90 min</span><span class="lu-layers__note">Find the bug, fix it, let the reasoner classify, read a real report</span></li>
        <li><span class="lu-layers__name">Wrap · ~20 min</span><span class="lu-layers__note">Discussion, glossary, self-check</span></li>
      </ul>
    </div>
  </div>''', '''<p>Name the payoff early: at minute 130 the reasoner will turn one of <i>our</i> classes red, and by minute 160 they will know exactly why and have fixed it.</p>''', kind="tint"))

# ---------------------------------------------------------------- 04 Divider
SLIDES.append(divider("Part 1 · What an ontology is", "What an ontology is",
    "Part one of five · about 22 minutes",
    "One dataset. Three honest answers to &ldquo;how many orders were late?&rdquo;",
    "The disagreement is not in the data. It is in the word."))

# ---------------------------------------------------------------- 05 Why: one word, three numbers
SLIDES.append(slide("One word, three numbers", "What an ontology is", 4, '''  <div class="lu-eyebrow">Why this session exists</div>
  <h2 class="lu-h2">Same 65,752 DataCo orders. Three definitions of &ldquo;late&rdquo;. Three different answers.</h2>
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr))">
    <div class="lu-card"><span class="lu-card__label">Late means: any delay</span><div class="lu-display" style="color:var(--lu-red-700)">57.3%</div><p class="lu-sub">Real shipping days greater than the scheduled days.</p></div>
    <div class="lu-card"><span class="lu-card__label">Late means: the label says so</span><div class="lu-display" style="color:var(--lu-red-700)">54.8%</div><p class="lu-sub">The dataset's own column <code>Delivery Status</code> says &ldquo;Late delivery&rdquo;.</p></div>
    <div class="lu-card"><span class="lu-card__label">Late means: more than a day</span><div class="lu-display" style="color:var(--lu-red-700)">23.7%</div><p class="lu-sub">Real shipping days more than one day over schedule.</p></div>
  </div>
  <div class="lu-split">
    ''' + callout("The problem", "Every number is correct. A dashboard, a model and a report can each pick a different one, and nobody notices.", "neutral") + '''
    ''' + callout("The fix this session builds", "Write the meaning down <b>once</b>, precisely, in a form every program reads the same way.") + '''
  </div>''', '''<p>Four minutes. All three numbers were computed on 2026-09-22 from the real file <code>demos/data/dataco/DataCoSupplyChainDataset.csv</code>: 65,752 distinct orders; 37,698 with real days &gt; scheduled (57.3%); 36,048 labelled "Late delivery" (54.8%); 15,578 more than one day late (23.7%).</p>
<ul><li>Ask the room: which one is right? Every answer is defensible. That is the point: the meaning lives in people's heads, not in the data.</li>
<li>Session 1's failure gallery had the same story as a case study (12% against 30%). Here it is on the course's own data.</li></ul>'''))

# ---------------------------------------------------------------- 06 Ontology in one picture
g = ""
g += box(330, 28, 260, 46, "Shipment", "class")
g += box(330, 108, 260, 46, "At-risk shipment", "class")
g += arrow(330, 85, 330, 53, "subclass of", lx=315, ly=69, label_anchor="end")
g += box(1110, 28, 260, 46, "Carrier", "class")
g += box(1110, 108, 260, 46, "Sanctioned carrier", "class")
g += arrow(1110, 85, 1110, 53, "subclass of", lx=1125, ly=69, label_anchor="start")
g += box(520, 192, 230, 46, "shipment 4472", "ind")
g += box(960, 192, 250, 46, "Blackline Freight", "ind")
g += arrow(635, 192, 833, 192, "handled by", ly=172)
g += arrow(520, 169, 452, 53, "is a", lx=500, ly=112, label_anchor="start")
g += arrow(960, 169, 1000, 133, "is a", lx=996, ly=160, label_anchor="start")
pic = svg(FULL, 220, g, "Four classes, two individuals, and the arrows between them")
SLIDES.append(slide("An ontology in one picture", "What an ontology is", 5, f'''  <div class="lu-eyebrow">The idea, drawn</div>
  <h2 class="lu-h2">An ontology names the kinds of things, and how things connect</h2>
  {pic}
  <div class="lu-split">
  ''' + defbox([
    ("Ontology", "A precise, machine readable description of the kinds of things in a domain and how they relate."),
    ("Class", "A named kind of thing, drawn as a red box: <b>Shipment</b>."),
  ]) + defbox([
    ("Individual", "One particular thing, drawn as a green pill: <b>shipment 4472</b>."),
    ("Property", "A named connection, drawn as an arrow: <b>handled by</b>."),
  ], label="Also defined here") + '''
  </div>''', '''<p>Five minutes. Walk the picture in plain words: "shipment 4472 is a shipment; it is handled by Blackline Freight; Blackline is a sanctioned carrier; every sanctioned carrier is a carrier."</p>
<ul><li>Blackline Freight is fictional. Never label a real company as sanctioned in teaching material.</li>
<li>These exact entities are in the lab file <code>sample-shipments.ttl</code>; students meet them again in Protégé.</li></ul>'''))

# ---------------------------------------------------------------- 07 Class tree
rows = [("owl:Thing", 0, "ink"), ("Shipment", 1, "red"), ("Late shipment", 2, "red"),
        ("Cancelled shipment", 2, "red"), ("At-risk shipment", 2, "red"), ("Carrier", 1, "red"),
        ("Sanctioned carrier", 2, "red"), ("Multi-route carrier", 2, "red")]
g = ""
y0, dy, ind = 26, 44, 60
pos = []
for i, (name, lvl, col) in enumerate(rows):
    x = 30 + lvl * ind
    y = y0 + i * dy
    pos.append((x, y, lvl))
# connectors
for i, (x, y, lvl) in enumerate(pos):
    if lvl == 0:
        continue
    # parent: nearest previous row with lvl-1
    for j in range(i - 1, -1, -1):
        if pos[j][2] == lvl - 1:
            px, py = pos[j][0], pos[j][1]
            break
    g += line(px, py + 12, px, y, LINE, 2)
    g += line(px, y, x - 12, y, LINE, 2)
for (name, lvl, col), (x, y, _) in zip(rows, pos):
    g += dot(x, y, None, "red" if col == "red" else "ink")
    g += text(x + 22, y, name, anchor="start", color=INK, weight=600 if lvl < 2 else None)
g += text(470, y0 + 3 * dy, "every late shipment", "s-label", anchor="start", color=INK3)
g += text(470, y0 + 3 * dy + 26, "is a shipment", "s-label", anchor="start", color=INK3)
g += arrow(460, y0 + 3 * dy + 6, 420, y0 + 2 * dy + 8, None, "muted")
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
  </div>''', '''<p>Four minutes. Protégé draws the same tree; students see it in the lab. Read two lines aloud as sentences: "every late shipment is a shipment", "every sanctioned carrier is a carrier". Then the inheritance point in the callout: that is the whole reason for a tree.</p>'''))

# ---------------------------------------------------------------- 08 Two kinds of arrow
g = ""
g += box(560, 115, 240, 52, "shipment 4472", "ind")
g += box(1100, 40, 280, 52, "Blackline Freight", "ind")
g += arrow(680, 104, 958, 50, "handled by", lx=820, ly=58)
g += box(1100, 190, 160, 52, "420", "lit")
g += arrow(680, 126, 1018, 182, "weight in kg", lx=850, ly=180)
g += box(170, 115, 300, 52, '"shipment 4472"', "note")
g += arrow(440, 115, 322, 115, "label", "muted", ly=95)
g += text(1270, 40, "a thing", "s-label", color=GREEN, anchor="start")
g += text(1200, 190, "a value", "s-label", color=INK3, anchor="start")
g += text(170, 160, "a note for humans", "s-label", color=INK3)
pic = svg(FULL, 230, g, "Three arrows from shipment 4472: to a thing, to a value, to a note for humans")
SLIDES.append(slide("Two kinds of arrow, plus notes", "What an ontology is", 4, f'''  <div class="lu-eyebrow">Properties</div>
  <h2 class="lu-h2">An arrow points to a thing, or to a value. Notes are for humans only.</h2>
  {pic}
  ''' + defbox([
    ("Object property", "Connects a thing to another thing: <b>handled by</b>."),
    ("Datatype property", "Connects a thing to a value (number, date, text): <b>weight in kg</b>."),
    ("Annotation property", "A note for humans (label, definition, comment). The reasoner ignores it."),
  ]), '''<p>Four minutes. The practical reason this matters: in Protégé, object and datatype properties live in two different tabs, and a value cannot be the start of another arrow.</p>
<ul><li>The weight is illustrative, the same pattern as <code>ul:weightKg</code> in Session 2's sandbox data.</li>
<li>Annotation properties in our file: <code>rdfs:label</code>, <code>skos:definition</code>, and the course's own <code>ul:answersCQ</code>.</li></ul>'''))

# ---------------------------------------------------------------- 09 TBox / ABox
g = ""
g += rect(0, 4, FULL, 110, RED_BG, RED)
g += text(30, 34, "TBox · the rules", anchor="start", color=RED, weight=600)
g += text(FULL - 24, 34, "scro-extension-reference.ttl", "s-mono", anchor="end", color=INK3)
g += box(430, 76, 560, 46, "Every At-risk shipment is a Shipment", "plain")
g += box(1080, 76, 600, 46, "handled by: from a Shipment to a Carrier", "plain")
g += rect(0, 126, FULL, 110, GREEN_BG, GREEN)
g += text(30, 156, "ABox · the data", anchor="start", color=GREEN, weight=600)
g += text(FULL - 24, 156, "sample-shipments.ttl", "s-mono", anchor="end", color=INK3)
g += box(430, 198, 560, 46, "shipment 4472 is a Shipment", "plain")
g += box(1080, 198, 600, 46, "shipment 4472 is handled by Blackline", "plain")
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

# ---------------------------------------------------------------- 10 Check
SLIDES.append(slide("Check: rules or data?", "What an ontology is", 3, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-mcq" data-qid="s3-q1" data-answer="b" data-label="Which statement is an ABox axiom"
       data-fb-correct=" Correct. It is about one particular shipment and one particular carrier, so it belongs to the data."
       data-fb-wrong=" Not quite. Ask: is it about one particular thing, or about a whole kind of thing?">
    <p class="lu-mcq__q">Which of these is an <b>ABox</b> axiom, a fact about particular things?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">Every late shipment is a shipment<span class="lu-mcq__why" hidden>A rule about a whole class: TBox.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">Shipment 4472 is handled by Blackline Freight<span class="lu-mcq__why" hidden>Correct: two individuals and one property between them.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">&ldquo;Handled by&rdquo; goes from a shipment to a carrier<span class="lu-mcq__why" hidden>A rule about what the property connects: TBox.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="d">Sanctioned carrier is a subclass of Carrier<span class="lu-mcq__why" hidden>A relationship between two classes: TBox.</span></button>
    </div>
  </div>''', '''<p>Three minutes. If anyone picks c, that is the most useful wrong answer: it is about a property, not a particular thing, so it is a rule.</p>''', kind="tint"))
