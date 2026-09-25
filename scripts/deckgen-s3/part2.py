"""Session 3, Part 2: writing rules a machine can use.

Set pictures (circles of members) stay inline SVG, route 2, because the
geometry is the idea; every arrow diagram is an lu-flow. Blue is ours, teal
reused, green an individual, amber inferred, red only refused or impossible.
"""
from common import slide, divider, defbox, callout, code
from kit import flow, node, edge
from svgkit import svg, text, line, circle, dot, arrow, rect, tick, FULL, HALF, INK3, BLUE, TEAL, BLUE_BG, INK2

SLIDES = []
SHIP_A, SHIP_B, SHIP_C = "1447291369.7", "1447385217.7", "1447311670.7"

SLIDES.append(divider("Part 2 · Writing rules a machine can use", "Writing rules",
    "Part 2 of 5 · about 40 minutes",
    "How do you tell a machine what &ldquo;at risk&rdquo; means?",
    "With a handful of words: some, only, and, or, not, exactly. Protégé shows them on every screen."))


def still(label, w, h, nodes, edges, legend=False):
    """A flow with no steps to click through: everything shown at once."""
    return flow(label, w, h, nodes, edges,
                [{"show": [x["id"] for x in nodes] + [x["id"] for x in edges]}], legend=legend)


# ---------------------------------------------------------------- Classes are sets
g = ""
g += circle(300, 120, 112, "Shipment", "reused")
g += circle(338, 146, 64, None, "ours")
g += line(385, 190, 420, 214, INK3, 1.5) + text(426, 218, "At-risk shipment", anchor="start", color=BLUE, weight=600)
g += dot(222, 104, SHIP_B, lx=222, ly=132, anchor="middle")
g += dot(318, 128, None) + dot(352, 170, None)
g += text(470, 128, f"{SHIP_A} and {SHIP_C}", "s-label", anchor="start", color=INK2)
g += line(330, 128, 462, 128, INK3, 1.2)
g += circle(1060, 120, 112, "Carrier", "reused")
g += circle(1098, 146, 64, None, "ours")
g += line(1145, 190, 1180, 214, INK3, 1.5) + text(1186, 218, "Sanctioned carrier", anchor="start", color=BLUE, weight=600)
g += dot(995, 104, "V444_0", lx=995, ly=132, anchor="middle")
g += dot(1098, 150, "V444_1", lx=1098, ly=176, anchor="middle")
pic = svg(FULL, 240, g, "Venn diagram: Shipment contains At-risk shipment; Carrier contains Sanctioned carrier; dots are individuals")
SLIDES.append(slide("Classes are sets", "Writing rules", 4, f'''  <div class="lu-eyebrow">The picture behind every rule</div>
  <h2 class="lu-h2">Draw a class as a circle and its members as dots. Every rule says which dots may sit where.</h2>
  {pic}
  <p class="lu-caption">Circle = class · dot = individual · a circle inside a circle = a subclass.</p>
  ''' + defbox([
    ("Member", "An individual inside a class: a dot inside a circle."),
    ("Class as a set", "OWL treats a class as exactly the set of its members."),
  ]), f'''<p>Four minutes. "Every at-risk shipment is a shipment" just says one circle sits inside the other; the next slides add rules the same way.</p>
<p>The shipments of orders {SHIP_A} and {SHIP_C} are drawn inside At-risk shipment already. In the lab the reasoner puts them there, because of the rule on the slide "SubClassOf and EquivalentTo". Say: hold that thought.</p>'''))


# ---------------------------------------------------------------- some
def some_only(which):
    g = ""
    g += circle(540, 100, 88, "Sanctioned carrier", "ours", ly=32)
    g += dot(90, 72, SHIP_A, lx=90, ly=46, anchor="middle")
    g += dot(540, 104, "V444_1", lx=540, ly=130, anchor="middle")
    g += arrow(102, 73, 526, 103, "handled by", ly=66)
    g += dot(90, 206, SHIP_B, lx=90, ly=180, anchor="middle")
    g += dot(540, 222, "V444_0", lx=570, ly=222)
    g += arrow(102, 207, 526, 221, "handled by", ly=198)
    g += tick(30, 72, True)
    g += tick(30, 206, False)
    if which == "only":
        g += dot(90, 280, None)
        g += text(110, 282, "a shipment with no carrier recorded", "s-label", anchor="start", color=INK3)
        g += tick(30, 280, True)
    return svg(HALF, 300 if which == "only" else 244, g, f"Which shipments satisfy 'handled by {which} Sanctioned carrier'")


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
    ]), f'''<p>Five minutes. Read the Protégé line aloud slowly, it is exactly what they will see in the Description panel in the lab: <code>'handled by' some 'Sanctioned carrier'</code>. The quotes appear because the names contain spaces.</p>
<ul><li>The shipment of {SHIP_A} passes (one arrow into the circle). The shipment of {SHIP_B} fails (its only carrier, V444_0, is outside).</li></ul>'''))

three_only = '''<table class="lu-table"><tbody>
<tr><td>English</td><td>every carrier of this shipment, if any, is sanctioned</td></tr>
<tr><td>Protégé</td><td><code>'handled by' only 'Sanctioned carrier'</code></td></tr>
<tr><td>Turtle</td><td><code>owl:allValuesFrom ul:SanctionedCarrier</code></td></tr>
</tbody></table>'''
SLIDES.append(slide("only: every one, if any", "Writing rules", 4, f'''  <div class="lu-eyebrow">The rule people misread</div>
  <h2 class="lu-h2"><code>only</code> means: no arrow of this kind lands outside that circle</h2>
  <div class="lu-split">
    <div class="lu-stack">{some_only("only")}
    ''' + callout("The trap", "A shipment with <b>no</b> carrier recorded still passes. <code>only</code> never says an arrow exists. To say both, write <code>some</code> and <code>only</code>.") + f'''</div>
    <div class="lu-stack">{three_only}
    ''' + defbox([("only", "Universal restriction: every link of this kind, if there is any, goes to a member of the class.")]) + '''</div>
  </div>''', '''<p>Four minutes. Ask the room first: does the shipment with no carrier satisfy it? Most say no. The answer is yes, nothing breaks the rule. This is the single most common OWL misreading, and Part B of the lab asks them to write <code>some</code> plus <code>only</code> correctly.</p>
<p>Every Brunel order has a carrier, so the third dot is a hypothetical shipment, not a row from the data. Say so.</p>'''))


# ---------------------------------------------------------------- and / or / not / disjoint
def mini(kind):
    W, H = 270, 150
    g = f'<defs><clipPath id="s3clip-{kind}"><circle cx="105" cy="75" r="62"/></clipPath></defs>'
    if kind == "and":
        g += circle(105, 75, 62, None, "muted", fill=False) + circle(165, 75, 62, None, "muted", fill=False)
        g += (f'<circle cx="165" cy="75" r="62" clip-path="url(#s3clip-{kind})" '
              f'style="fill:{BLUE_BG};stroke:{BLUE};stroke-width:2"/>')
    elif kind == "or":
        g += circle(105, 75, 62, None, "ours") + circle(165, 75, 62, None, "ours")
    elif kind == "not":
        g += rect(6, 6, W - 12, H - 12, BLUE_BG, BLUE, rx=8)
        g += circle(135, 75, 58, None, "muted")
    else:
        g += circle(75, 75, 55, None, "ours") + circle(195, 75, 55, None, "ours")
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
  '''<p>Five minutes. Disjointness is the one that makes errors findable: if one individual lands in both circles, the reasoner reports a contradiction instead of silently accepting it. The lab's bug is found by a disjointness axiom in BFO.</p>'''))

# ---------------------------------------------------------------- counting
n = [
    node("comp", "Sole-sourced component", 200, 45, 320, 56, kind="ours"),
    node("sup", "Supplier", 740, 45, 200, 56, kind="reused"),
    node("mrc", "Multi-route carrier", 200, 170, 300, 56, kind="ours"),
    node("route", "Shipping route", 740, 170, 240, 56, kind="reused"),
]
e = [edge("a", "comp", "sup", "supplied by · exactly 1"),
     edge("b", "mrc", "route", "handles route · min 2")]
pic = still("Two counting rules in our ontology", 900, 230, n, e)
SLIDES.append(slide("Counting: exactly, min, max", "Writing rules", 4, f'''  <div class="lu-eyebrow">Rules that count</div>
  <h2 class="lu-h2">Some questions need a number: exactly one supplier, at least two routes</h2>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">{pic}
    ''' + callout("In the Brunel data", "V444_0 ships on 2 lanes, V44_3 on 3, V444_1 on 1. Two of the three carriers would count as multi-route.", "neutral") + '''</div>
    <div class="lu-stack">''' + defbox([("Cardinality restriction", "A rule that counts links: exactly 1, min 2, max 3.")]) +
    callout("Remember this for Part 5", "The fast reasoner used first in the lab, ELK, <b>ignores</b> counting rules. That is why it misses one of the lab's two errors.") + '''
    </div>
  </div>''', '''<p>Four minutes. Both classes are real in <code>scro-extension-reference.ttl</code>: <code>ul:SoleSourcedComponent</code> (<code>'supplied by' exactly 1 Supplier</code>) and <code>ul:MultiRouteCarrier</code> (<code>'handles route' min 2 'Shipping route'</code>).</p>
<ul><li>Lane counts are from Brunel's OrderList (origin and destination port per order): V444_0 PORT04 and PORT09 to PORT09; V444_1 PORT04 to PORT09 only; V44_3 PORT04, PORT05 and PORT09 to PORT09.</li>
<li>If asked: a reasoner cannot conclude "min 2" from two port names alone, because OWL does not assume two names are two things. That is the open world again; Session 4 is where counting is checked.</li></ul>'''))

# ---------------------------------------------------------------- domain and range
n = [
    node("s", f"shipment of order\n{SHIP_C}", 220, 70, 290, 76, kind="individual"),
    node("c", "carrier V444_1", 700, 70, 250, 60, kind="individual"),
    node("S", "Shipment", 220, 220, 220, 60, kind="reused", flag="right"),
]
e = [edge("a", "s", "c", "handled by"),
     edge("b", "s", "S", "is a", kind="inferred")]
steps = [{"show": ["s", "c", "a"], "run": ["a"], "set": {"s": "active"}},
         {"show": ["S", "b"], "run": ["b"], "set": {"s": "idle", "S": "inferred"}}]
caps = [("What the file says", f"<b>Step 1.</b> The file only says the shipment of {SHIP_C} is handled by carrier V444_1. It gives the shipment no type at all."),
        ("What OWL concludes", "<b>Step 2.</b> The domain of <b>handled by</b> is Shipment, so the reasoner concludes it is a Shipment. Nothing is refused.")]
owl_pic = flow("OWL infers the type", 820, 270, n, e, steps, caps)
sql = code("Database · SQLite 3.37.2, real run of closed_world_demo.py", f'''<span class="tok-kw">INSERT INTO</span> handled_by
  <span class="tok-kw">VALUES</span> (<span class="tok-str">'{SHIP_C}'</span>, <span class="tok-str">'V444_1'</span>);

<span class="tok-com">IntegrityError: FOREIGN KEY constraint failed</span>''')
SLIDES.append(slide("Domain and range infer, they do not reject", "Writing rules", 5, f'''  <div class="lu-eyebrow">The biggest surprise for database people</div>
  <h2 class="lu-h2">The same fact: a database rejects it, OWL learns from it</h2>
  <div class="lu-split">
    <div class="lu-stack">
      {sql}
      ''' + defbox([
        ("Domain", "Class every <b>subject</b> of a property is inferred to be in."),
        ("Range", "Class every <b>object</b> is inferred to be in."),
        ("Entailment", "A fact that follows from stated facts and rules, though nobody wrote it."),
      ]) + f'''
    </div>
    {owl_pic}
  </div>''', '''<p>Five minutes. Left, the database: the shipment is not in the shipment table, so the row is refused. Right, OWL: nothing is refused, the reasoner concludes a type. Both sides are real. The database error: <code>demos/session-03-ontology/closed_world_demo.py</code> (output in <code>reference-outputs/closed-world-demo.txt</code>). The OWL side is the lab file <code>sample-shipments.ttl</code>, reasoned with ELK in the lab.</p>
<ul><li>For <code>handled by</code>: domain Shipment, range Carrier.</li><li>Say the sentence: <b>OWL infers rather than complains.</b> Session 4 (SHACL) is the tool that complains.</li></ul>'''))


# ---------------------------------------------------------------- SubClassOf vs EquivalentTo
def door(two_way):
    n = [node("c", "At-risk shipment", 300, 32, 280, 52, kind="ours"),
         node("x", "Shipment and handled by some Sanctioned carrier", 300, 118, 560, 52, kind="builtin")]
    e = [edge("a", "c", "x", "both ways" if two_way else "one way only", both=two_way)]
    return still("EquivalentTo, two way" if two_way else "SubClassOf, one way", 600, 150, n, e)


table = f'''<table class="lu-table">
<thead><tr><th>Real reasoner result (ELK)</th><th>{SHIP_B} · V444_0</th><th>{SHIP_A} · V444_1</th><th>{SHIP_C} · V444_1</th></tr></thead>
<tbody>
<tr><td>At-risk as <b>SubClassOf</b></td><td>no</td><td>no</td><td>no</td></tr>
<tr><td>At-risk as <b>EquivalentTo</b></td><td>no</td><td><b>at risk</b></td><td><b>at risk</b></td></tr>
</tbody></table>'''


def dcard(label, pic, term, d):
    return (f'<div class="lu-callout lu-callout--concept" style="padding:var(--lu-s4) var(--lu-s5)"><span class="lu-callout__label">{label}</span>{pic}'
            f'<dl class="lu-defs"><dt>{term}</dt><dd>{d}</dd></dl></div>')


SLIDES.append(slide("SubClassOf and EquivalentTo", "Writing rules", 6, f'''  <div class="lu-eyebrow">Why the reasoner sometimes does nothing</div>
  <h2 class="lu-h2">A one way door, or a two way door. Only the two way door lets the reasoner classify data.</h2>
  <div class="lu-split">
    {dcard("SubClassOf · one way", door(False), "Primitive class", "Meeting the conditions does not make you a member.")}
    {dcard("EquivalentTo · two way", door(True), "Defined class", "Meeting the conditions makes you a member.")}
  </div>
  {table}''', '''<p>Six minutes. This is the slide that answers "what did the reasoner add?". With a primitive class, nothing: no shipment is ever placed in it. With a defined class, the reasoner does the classifying.</p>
<ul><li>The table is a real ELK run: <code>python realize_sample.py</code> runs ROBOT on <code>sample-shipments.ttl</code> twice, once as shipped (EquivalentTo) and once with that one axiom turned into SubClassOf; output in <code>reference-outputs/realized-sample.txt</code>.</li>
<li>The v0 file had At-risk shipment as SubClassOf only, which is why nothing visible happened when the reasoner first ran on it.</li></ul>'''))


# ---------------------------------------------------------------- property characteristics
def pc(kind):
    if kind == "transitive":
        n = [node("a", "bolt", 70, 140, 110, 50, kind="individual"),
             node("b", "wheel", 235, 40, 120, 50, kind="individual"),
             node("c", "truck", 400, 140, 120, 50, kind="individual")]
        e = [edge("x", "a", "b", "part of"), edge("y", "b", "c", "part of"),
             edge("z", "a", "c", "part of (inferred)", kind="inferred")]
    elif kind == "functional":
        n = [node("o", "order\n1447291369.7", 110, 90, 200, 70, kind="individual"),
             node("d1", "2013-05-26", 380, 35, 160, 50, kind="literal"),
             node("d2", "2013-05-27", 380, 150, 160, 50, kind="literal", flag="right")]
        e = [edge("x", "o", "d1", "order date"), edge("y", "o", "d2", "order date", kind="conflict")]
    else:
        n = [node("s", "shipment", 90, 90, 150, 56, kind="individual"),
             node("c", "V444_1", 390, 90, 150, 56, kind="individual")]
        e = [edge("x", "s", "c", "handled by / handles", both=True)]
    return still(kind, 470, 190, n, e)


pcs = [("transitive", "Transitive", "If A is part of B and B is part of C, then A is part of C."),
       ("functional", "Functional", "At most one value per subject: one order date per order."),
       ("inverse", "Inverse", "The same link read backwards: <b>handled by</b> and <b>handles</b>.")]
cells = "".join(f'<div class="lu-callout lu-callout--concept"><span class="lu-callout__label">{t}</span>{pc(k)}<p class="lu-sub">{d}</p></div>' for k, t, d in pcs)
SLIDES.append(slide("Property characteristics", "Writing rules", 4, f'''  <div class="lu-eyebrow">Rules about the arrows themselves</div>
  <h2 class="lu-h2">A property can carry its own rules, and the reasoner uses them</h2>
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr))">{cells}</div>
  ''' + callout("Also: punning", "Using one name as both a class and an individual. OWL 2 allows it, but it confuses people and tools. Avoid it unless you truly need it.", "neutral"),
  '''<p>Four minutes. Our file declares <code>ul:deliveredAfter</code> as the inverse of <code>ul:committedBefore</code>, a real example. Transitivity is how "which products contain a part from this plant" works at any depth (Session 1's sanction question); Brunel has no parts list, so the bolt and wheel are a generic picture, not course data.</p>
<p>The functional card: order 1447291369.7 really was ordered on 2013-05-26; the second date is what a careless second source might send. Two different <i>literal</i> values make the ontology inconsistent. If the two values were individuals, OWL would instead conclude they are the same thing, the open world again.</p>'''))

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
