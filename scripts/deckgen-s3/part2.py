from common import slide, divider, defbox, callout, code
from svgkit import *

SLIDES = []

SLIDES.append(divider("Part 2 · Writing rules a machine can use", "Writing rules",
    "Part two of five · about 34 minutes",
    "How do you tell a machine what &ldquo;at risk&rdquo; means?",
    "With a handful of words: some, only, and, or, not, exactly. Protégé shows them on every screen."))

# ---------------------------------------------------------------- Classes are sets
g = ""
g += circle(300, 120, 112, "Shipment", "red")
g += circle(338, 140, 66, None, "red")
g += line(385, 186, 420, 214, INK3, 1.5) + text(426, 218, "At-risk shipment", anchor="start", color=RED, weight=600)
g += dot(235, 110, "4471", lx=235, ly=136, anchor="middle")
g += dot(320, 120, "4472")
g += dot(320, 168, "4473")
g += circle(960, 120, 112, "Carrier", "green")
g += circle(998, 140, 66, None, "green")
g += line(1045, 186, 1080, 214, INK3, 1.5) + text(1086, 218, "Sanctioned carrier", anchor="start", color=GREEN, weight=600)
g += dot(895, 110, "DHL", lx=895, ly=136, anchor="middle")
g += dot(990, 130, "Blackline", lx=990, ly=156, anchor="middle")
pic = svg(FULL, 240, g, "Venn diagram: Shipment contains At-risk shipment; Carrier contains Sanctioned carrier; dots are individuals")
SLIDES.append(slide("Classes are sets", "Writing rules", 4, f'''  <div class="lu-eyebrow">The picture behind every rule</div>
  <h2 class="lu-h2">Draw a class as a circle and its members as dots. Every rule says which dots may sit where.</h2>
  {pic}
  <p class="lu-caption">Circle = class · dot = individual · a circle inside a circle = a subclass.</p>
  ''' + defbox([
    ("Member", "An individual inside a class: a dot inside a circle."),
    ("Class as a set", "OWL treats a class as exactly the set of its members."),
  ]), '''<p>Four minutes. "Every at-risk shipment is a shipment" just says one circle sits inside the other; the next slides add rules the same way.</p>
<p>4472 and 4473 are drawn inside At-risk shipment already. In the lab the reasoner puts them there, because of the rule on the slide "SubClassOf and EquivalentTo". Say: hold that thought.</p>'''))

# ---------------------------------------------------------------- some
def some_only(which):
    g = ""
    g += circle(530, 95, 88, "Sanctioned carrier", "green", ly=28)
    g += dot(90, 70, "4472", lx=90, ly=44, anchor="middle")
    g += dot(520, 92, "Blackline", lx=520, ly=118, anchor="middle")
    g += arrow(100, 71, 506, 91, "handled by", ly=64)
    g += dot(90, 200, "4471", lx=90, ly=174, anchor="middle")
    g += dot(520, 215, "DHL", lx=548, ly=215)
    g += arrow(100, 201, 506, 214, "handled by", ly=192)
    g += tick(30, 70, True)
    g += tick(30, 200, False)
    if which == "only":
        g += dot(90, 272, "4480", lx=90, ly=248, anchor="middle")
        g += text(125, 274, "no carrier recorded", "s-label", anchor="start", color=INK3)
        g += tick(30, 272, True)
    return svg(HALF, 292 if which == "only" else 236, g, f"Which shipments satisfy 'handled by {which} Sanctioned carrier'")

three_some = '''<table class="lu-table"><tbody>
<tr><td>English</td><td>at least one carrier of this shipment is sanctioned</td></tr>
<tr><td>Protégé</td><td><code>'handled by' some 'Sanctioned carrier'</code></td></tr>
<tr><td>Turtle</td><td><code>owl:someValuesFrom ul:SanctionedCarrier</code></td></tr>
</tbody></table>'''
SLIDES.append(slide("some: at least one", "Writing rules", 5, f'''  <div class="lu-eyebrow">The most used rule in OWL</div>
  <h2 class="lu-h2"><code>some</code> means: at least one arrow of this kind lands in that circle</h2>
  <div class="lu-split">
    {some_only("some")}
    {three_some}
  </div>
  ''' + defbox([
      ("Restriction", "A class described by a condition on a property."),
      ("some", "Existential restriction: at least one link goes to a member of the class."),
      ("Manchester syntax", "The readable way Protégé writes rules, with the words some, only, and, or, not."),
    ]), '''<p>Five minutes. Read the Protégé line aloud slowly, it is exactly what they will see in the Description panel in the lab: <code>'handled by' some 'Sanctioned carrier'</code>. The quotes appear because the names contain spaces.</p>
<ul><li>4472 passes (one arrow into the circle). 4471 fails (its only carrier is outside).</li></ul>'''))

three_only = '''<table class="lu-table"><tbody>
<tr><td>English</td><td>every carrier of this shipment, if any, is sanctioned</td></tr>
<tr><td>Protégé</td><td><code>'handled by' only 'Sanctioned carrier'</code></td></tr>
<tr><td>Turtle</td><td><code>owl:allValuesFrom ul:SanctionedCarrier</code></td></tr>
</tbody></table>'''
SLIDES.append(slide("only: every one, if any", "Writing rules", 4, f'''  <div class="lu-eyebrow">The rule people misread</div>
  <h2 class="lu-h2"><code>only</code> means: no arrow of this kind lands outside that circle</h2>
  <div class="lu-split">
    <div class="lu-stack">{some_only("only")}
    ''' + callout("The trap", "Shipment 4480 has <b>no</b> carrier and still passes. <code>only</code> never says an arrow exists. To say both, write <code>some</code> and <code>only</code>.") + f'''</div>
    <div class="lu-stack">{three_only}
    ''' + defbox([("only", "Universal restriction: every link of this kind, if there is any, goes to a member of the class.")]) + '''</div>
  </div>''', '''<p>Four minutes. Ask the room first: does 4480 satisfy it? Most say no. The answer is yes, there is nothing that breaks the rule. This is the single most common OWL misreading.</p>'''))

# ---------------------------------------------------------------- and / or / not / disjoint
def mini(kind):
    W, H = 270, 150
    g = f'<defs><clipPath id="clip-{kind}"><circle cx="105" cy="75" r="62"/></clipPath></defs>'
    if kind == "and":
        g += circle(105, 75, 62, None, "muted", fill=False) + circle(165, 75, 62, None, "muted", fill=False)
        g += f'<circle cx="165" cy="75" r="62" clip-path="url(#clip-{kind})" style="fill:{RED_BG2};stroke:{RED};stroke-width:2"/>'
    elif kind == "or":
        g += circle(105, 75, 62, None, "red") + circle(165, 75, 62, None, "red")
    elif kind == "not":
        g += rect(6, 6, W - 12, H - 12, RED_BG2, RED, rx=8)
        g += circle(135, 75, 58, None, "muted")
    else:
        g += circle(75, 75, 55, None, "red") + circle(195, 75, 55, None, "green")
    return svg(W, H, g, f"Venn picture for {kind}")

cards = [
    ("and · intersection", "and", "Members of <b>both</b> classes.", "Shipment and ('handled by' some 'Sanctioned carrier')"),
    ("or · union", "or", "Members of <b>either</b> class.", "Plant or Port"),
    ("not · complement", "not", "Everything <b>outside</b> the class.", "Carrier and not 'Sanctioned carrier'"),
    ("disjoint", "disjoint", "Classes that share <b>no</b> member.", "'Late shipment' DisjointWith 'Cancelled shipment'"),
]
cells = "".join(
    f'<div class="lu-callout lu-callout--concept" style="padding:var(--lu-s4)"><span class="lu-callout__label">{t}</span>{mini(k)}'
    f'<p class="lu-sub">{d}</p><p class="lu-sub"><code>{e}</code></p></div>' for t, k, d, e in cards)
SLIDES.append(slide("and, or, not, disjoint", "Writing rules", 5, f'''  <div class="lu-eyebrow">Combining classes</div>
  <h2 class="lu-h2">Four ways to combine circles. The shaded area is the new class.</h2>
  <div class="lu-cards" style="grid-template-columns:repeat(4,minmax(0,1fr))">{cells}</div>
  <p class="lu-caption">Every example is written the way Protégé shows it. The disjoint one is a real axiom in our lab file.</p>''',
  '''<p>Five minutes. Disjointness is the one that makes errors findable: if one individual lands in both circles, the reasoner reports a contradiction instead of silently accepting it. Session 3's walkthrough and the lab's bug both depend on disjointness.</p>'''))

# ---------------------------------------------------------------- counting
g = ""
g += dot(160, 80, "brake disc", lx=160, ly=50, anchor="middle")
g += dot(560, 80, "Acme Logistics", lx=560, ly=50, anchor="middle")
g += arrow(172, 80, 546, 80, "supplied by", ly=104)
g += text(360, 160, "'supplied by' exactly 1 Supplier", "s-mono", color=RED)
g += text(360, 192, "exactly one: a sole-sourced component", "s-label", color=INK3)
g += dot(880, 100, "DHL", lx=880, ly=70, anchor="middle")
g += dot(1300, 40, "Hamburg to Bremen", lx=1180, ly=40, anchor="end")
g += dot(1300, 150, "Beirut to Hamburg", lx=1180, ly=150, anchor="end")
g += arrow(892, 95, 1286, 43, None)
g += arrow(892, 105, 1286, 147, None)
g += text(1316, 95, "handles route", "s-mono", anchor="start", color=INK2)
g += text(1090, 205, "'handles route' min 2 'Shipping route'", "s-mono", color=RED)
g += text(1090, 237, "two or more: a multi-route carrier", "s-label", color=INK3)
pic = svg(FULL, 252, g, "Counting links: exactly one supplier, at least two routes")
SLIDES.append(slide("Counting: exactly, min, max", "Writing rules", 4, f'''  <div class="lu-eyebrow">Rules that count</div>
  <h2 class="lu-h2">Some questions need a number: exactly one supplier, at least two routes</h2>
  {pic}
  <div class="lu-split">''' + defbox([("Cardinality restriction", "A rule that counts links: exactly 1, min 2, max 3.")]) +
  callout("Remember this for Part 5", "Counting is slow to reason about. The fast reasoner used first in the lab, ELK, <b>ignores</b> these rules. That matters at minute 150.") + '''
  </div>''', '''<p>Four minutes. Both rules are real classes in the lab file: <code>ul:SoleSourcedComponent</code> (exactly 1) and <code>ul:MultiRouteCarrier</code> (min 2). Acme Logistics is one of the course's supplier names from Session 5. The words are exactly, min (at least), max (at most).</p>'''))

# ---------------------------------------------------------------- domain and range
g = ""
g += box(150, 60, 230, 48, "shipment 4473", "ind")
g += box(560, 60, 250, 48, "Blackline Freight", "ind")
g += arrow(265, 60, 433, 60, "handled by", ly=40)
g += box(150, 205, 200, 48, "Shipment", "class")
g += arrow(150, 86, 150, 179, "is a (inferred)", "infer", lx=165, ly=132, label_anchor="start")
g += text(420, 205, "why: the domain of", "s-label", color=GREEN, anchor="start")
g += text(420, 230, "handled by is Shipment", "s-label", color=GREEN, anchor="start")
owl_pic = svg(HALF, 240, g, "OWL infers that shipment 4473 is a Shipment")
sql = code("SQLite 3.45.1 · real run", '''<span class="tok-kw">INSERT INTO</span> handled_by
  <span class="tok-kw">VALUES</span> (<span class="tok-num">4473</span>, <span class="tok-str">'blackline'</span>);

<span class="tok-com">IntegrityError: FOREIGN KEY constraint failed</span>''')
SLIDES.append(slide("Domain and range infer, they do not reject", "Writing rules", 5, f'''  <div class="lu-eyebrow">The biggest surprise for database people</div>
  <h2 class="lu-h2">The same fact: a database rejects it, OWL learns from it</h2>
  <div class="lu-split">
    <div class="lu-stack">
      <p class="lu-sub"><b>Database:</b> 4473 is not in the shipment table, so the row is refused.</p>
      {sql}
      ''' + defbox([
        ("Domain", "Class every <b>subject</b> is inferred to be in."),
        ("Range", "Class every <b>object</b> is inferred to be in."),
      ]) + f'''
    </div>
    <div class="lu-stack">
      <p class="lu-sub"><b>OWL:</b> nothing is refused. The reasoner concludes 4473 is a Shipment.</p>
      {owl_pic}
      ''' + defbox([("Entailment", "A fact that follows from stated facts and rules, though nobody wrote it.")], label="Also defined here") + '''
    </div>
  </div>''', '''<p>Five minutes. Both sides are real runs. The database error: SQLite 3.45.1 with foreign keys on (<code>demos/session-03-ontology/closed_world_demo.py</code>). The OWL side: ROBOT 1.9.10 with ELK on <code>sample-shipments.ttl</code>, output in <code>reference-outputs/</code>: shipment 4473 has no type in the file, and the reasoner gives it Shipment.</p>
<ul><li>For <code>handled by</code>: domain Shipment, range Carrier.</li><li>Say the sentence: <b>OWL infers rather than complains.</b> Session 4 (SHACL) is the tool that complains.</li></ul>'''))

# ---------------------------------------------------------------- SubClassOf vs EquivalentTo
def door(two_way):
    g = ""
    g += box(300, 24, 240, 42, "At-risk shipment", "class")
    g += box(300, 108, 560, 42, "Shipment and handled by some Sanctioned carrier", "plain")
    g += arrow(300, 47, 300, 85, None, "strong", both=two_way)
    g += text(318, 66, "both ways" if two_way else "one way only", "s-label", anchor="start", color=GREEN if two_way else INK3)
    return svg(600, 132, g, "EquivalentTo, two way" if two_way else "SubClassOf, one way")

table = '''<table class="lu-table">
<thead><tr><th>Real reasoner result (ELK)</th><th>4471 · DHL</th><th>4472 · Blackline</th><th>4473 · Blackline</th></tr></thead>
<tbody>
<tr><td>At-risk as <b>SubClassOf</b></td><td>no</td><td>no</td><td>no</td></tr>
<tr><td>At-risk as <b>EquivalentTo</b></td><td>no</td><td><b>at risk</b></td><td><b>at risk</b></td></tr>
</tbody></table>'''
def dcard(label, svgpic, term, d):
    return (f'<div class="lu-callout lu-callout--concept" style="padding:var(--lu-s4) var(--lu-s5)"><span class="lu-callout__label">{label}</span>{svgpic}'
            f'<dl class="lu-defs"><dt>{term}</dt><dd>{d}</dd></dl></div>')
SLIDES.append(slide("SubClassOf and EquivalentTo", "Writing rules", 6, f'''  <div class="lu-eyebrow">Why the reasoner sometimes does nothing</div>
  <h2 class="lu-h2">A one way door, or a two way door. Only the two way door lets the reasoner classify data.</h2>
  <div class="lu-split">
    {dcard("SubClassOf · one way", door(False), "Primitive class", "Meeting the conditions does not make you a member.")}
    {dcard("EquivalentTo · two way", door(True), "Defined class", "Meeting the conditions makes you a member.")}
  </div>
  {table}''', '''<p>Six minutes. This is the slide that answers "what did the reasoner add?". With a primitive class, nothing: no shipment is ever placed in it. With a defined class, the reasoner does the classifying.</p>
<ul><li>The table is real: ROBOT 1.9.10, ELK, on <code>sample-shipments.ttl</code>, once with the reference file as shipped (EquivalentTo) and once with that one axiom changed back to SubClassOf. Both outputs are in <code>reference-outputs/</code>.</li>
<li>The original v0 file had At-risk shipment as SubClassOf only, which is why nothing visible happened when the reasoner first ran on it.</li></ul>'''))

# ---------------------------------------------------------------- property characteristics
def pc(kind):
    g = ""
    if kind == "transitive":
        g += dot(40, 50, "bolt", lx=40, ly=22, anchor="middle")
        g += dot(200, 50, "wheel", lx=200, ly=22, anchor="middle")
        g += dot(360, 50, "truck", lx=360, ly=22, anchor="middle")
        g += arrow(52, 50, 188, 50, None)
        g += arrow(212, 50, 348, 50, None)
        g += text(120, 76, "part of", "s-mono", color=INK2) + text(280, 76, "part of", "s-mono", color=INK2)
        g += '<path d="M 40 62 Q 200 190 356 64" style="fill:none;stroke:var(--lu-green-700);stroke-width:2.5" stroke-dasharray="8 6"/>'
        g += text(200, 152, "part of (inferred)", "s-label", color=GREEN)
    elif kind == "functional":
        g += dot(40, 80, "4472", lx=40, ly=52, anchor="middle")
        g += box(300, 34, 150, 40, "2026-03-01", "lit")
        g += box(300, 124, 150, 40, "2026-03-03", "lit")
        g += arrow(52, 76, 223, 40, None)
        g += arrow(52, 84, 223, 118, None, "red")
        g += text(200, 162, "two different dates: contradiction", "s-label", color=RED)
    else:
        g += dot(40, 80, "4472", lx=40, ly=52, anchor="middle")
        g += dot(360, 80, "Blackline", lx=360, ly=52, anchor="middle")
        g += arrow(52, 74, 348, 74, None)
        g += arrow(348, 90, 52, 90, None)
        g += text(200, 58, "handled by", "s-mono", color=INK2) + text(200, 116, "handles", "s-mono", color=INK2)
    return svg(400, 170, g, kind)

pcs = [("transitive", "Transitive", "If A is part of B and B is part of C, then A is part of C."),
       ("functional", "Functional", "At most one value per subject: one committed date per shipment."),
       ("inverse", "Inverse", "The same link read backwards: <b>handled by</b> and <b>handles</b>.")]
cells = "".join(f'<div class="lu-callout lu-callout--concept"><span class="lu-callout__label">{t}</span>{pc(k)}<p class="lu-sub">{d}</p></div>' for k, t, d in pcs)
SLIDES.append(slide("Property characteristics", "Writing rules", 4, f'''  <div class="lu-eyebrow">Rules about the arrows themselves</div>
  <h2 class="lu-h2">A property can carry its own rules, and the reasoner uses them</h2>
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr))">{cells}</div>
  ''' + callout("Also: punning", "Using one name as both a class and an individual. OWL 2 allows it, but it confuses people and tools. Avoid it unless you truly need it.", "neutral"),
  '''<p>Four minutes. Our file declares <code>ul:deliveredAfter</code> as the inverse of <code>ul:committedBefore</code>, a real example. Transitivity is how "which products contain a part from this plant" works at any depth (Session 1's sanction question).</p>
<p>Precision for the functional card: two different <i>literal</i> values (dates) make the ontology inconsistent. If the two values were individuals, OWL would instead conclude they are the same thing, the open world again.</p>'''))

# ---------------------------------------------------------------- drill
SLIDES.append(slide("Drill: the rule words", "Writing rules", 3, '''  <div class="lu-eyebrow">Drill · complete the statements</div>
  <div class="lu-blanks" data-qid="s3-blanks1" data-label="OWL rule words">
    <p class="lu-h3" style="margin-bottom:var(--lu-s4)">Fill in the blanks</p>
    <ol class="lu-list lu-list--num">
      <li>&ldquo;At least one link goes to that class&rdquo; is written with <input class="lu-blank" data-answer="some" data-label="Blank 1" placeholder="…">.</li>
      <li>&ldquo;Every link, if any, goes to that class&rdquo; is written with <input class="lu-blank" data-answer="only" data-label="Blank 2" placeholder="…">.</li>
      <li>For the reasoner to put data into a class by itself, the class needs an <input class="lu-blank" data-answer="EquivalentTo|equivalent to|equivalence|equivalentClass" data-label="Blank 3" placeholder="…"> axiom.</li>
      <li>In OWL, a domain never rejects data. It <input class="lu-blank" data-answer="infers|entails|adds|derives" data-label="Blank 4" placeholder="…"> a type.</li>
    </ol>
  </div>''', '''<p>Three minutes. Blank 3 is the one that matters for the lab.</p>''', kind="tint"))
