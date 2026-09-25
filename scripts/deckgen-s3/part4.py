"""Session 3, Part 4: reuse, and BFO in plain words.

The reuse trap flow is the real Protégé explanation of the lab's red class
(assets/img/s3-protege-09b-explanation-1.png), drawn step by step; the spec
is the one prototyped in scripts/proto-diagrams/spec.json.
"""
import json
from pathlib import Path

from common import slide, divider, defbox, callout
from kit import flow, node, edge, defnote

SLIDES = []

SLIDES.append(divider("Part 4 · Reuse, and BFO in plain words", "Reuse and BFO",
    "Part 4 of 5 · about 30 minutes",
    "Industrial ontologies for supply chain already exist. Why build your own?",
    "Not reusing them is a decision, not a default. And reusing them has a price: you inherit their rules."))

# ---------------------------------------------------------------- The stack
n = [
    node("bfo", "BFO 2020\nthings, happenings, qualities", 250, 345, 420, 68, kind="upper"),
    node("core", "IOF Core\nproducts, processes, agents", 250, 240, 420, 68, kind="reused"),
    node("scro", "IOF SCRO\nshipments, carriers, orders", 250, 135, 420, 68, kind="reused"),
    node("ul", "ul: our extension\nonly what our questions need", 250, 35, 420, 64, kind="ours"),
    node("gs1", "GS1 Web\nVocabulary", 700, 135, 200, 68, kind="builtin"),
]
e = [edge("a", "ul", "scro", "builds on"), edge("b", "scro", "core", "builds on"),
     edge("c", "core", "bfo", "builds on"), edge("d", "scro", "gs1", "aligned with", both=True)]
stack = flow("The ontology stack our file sits on", 820, 385, n, e,
             [{"show": [x["id"] for x in n] + [x["id"] for x in e]}],
             legend={"ours": "Our ontology (ul:)", "reused": "Reused, IOF", "upper": "BFO, upper ontology"})
SLIDES.append(slide("Why reuse: the stack", "Reuse and BFO", 4, '''  <div class="lu-eyebrow">Where our classes attach</div>
  <h2 class="lu-h2">Three published layers under us. We only write what they do not already say.</h2>
  <div class="lu-split lu-split--wide-left">
  ''' + stack + defnote([
      ("Upper ontology", "a very general ontology of basic categories that domain ontologies build on. <b>BFO</b> is an ISO standard one."),
      ("IOF · SCRO", "the Industrial Ontologies Foundry's core layer, and its Supply Chain Reference Ontology, the base we extend."),
      ("Alignment", "linking our classes to classes in another ontology."),
  ]) + '''
  </div>''', '''<p>Four minutes. Build the stack from the bottom in words: BFO says what kinds of thing exist at all; IOF Core adds industry; SCRO adds supply chain; we add only what our competency questions need.</p>
<ul><li>Why reuse: someone else's shipment is then the same shipment as ours, and their tools and data work with our file. The GS1 check found no term for "port" or "freight rate band", an honest result of reuse first.</li>
<li>All three are real downloads in <code>workspace/</code> (IOF release 202603, MIT licence).</li></ul>'''))

# ---------------------------------------------------------------- Things and happenings
n = [
    node("cont", "continuant: persists through time", 300, 35, 400, 56, kind="upper"),
    node("occ", "occurrent: unfolds in time", 1000, 35, 360, 56, kind="upper"),
    node("truck", "a truck of carrier V444_1", 300, 150, 320, 56, kind="individual"),
    node("del", "the delivery of order 1447291369.7", 1000, 150, 420, 56, kind="individual"),
]
e = [edge("a", "truck", "cont", "is a"), edge("b", "del", "occ", "is a"),
     edge("c", "truck", "del", "participates in")]
pic = flow("Things and happenings", 1300, 190, n, e, [{"show": [x["id"] for x in n] + [x["id"] for x in e]}])
SLIDES.append(slide("Things and happenings", "Reuse and BFO", 4, '''  <div class="lu-eyebrow">BFO's first split</div>
  <h2 class="lu-h2">Everything is either a thing that lasts, or something that happens</h2>
  ''' + pic + '''
  ''' + defbox([
      ("Continuant", "Something that persists through time: a truck, a warehouse, a purchase order."),
      ("Occurrent", "Something that happens and unfolds in time: a delivery."),
      ("Process", "An occurrent with parts that happen one after another: loading, then shipping."),
  ]), '''<p>Four minutes. The test to give students: can you ask "how long did it take?" If yes, occurrent. Can you ask "where is it now?" If yes, continuant.</p>
<ul><li>The truck is an illustration: Brunel records carriers, not their trucks. The order is real.</li></ul>'''))

# ---------------------------------------------------------------- A truck, its colour, its role, its paperwork
n = [
    node("truck", "the truck\nmaterial entity", 260, 135, 270, 64, kind="individual"),
    node("colour", "its colour\nquality", 700, 36, 240, 64, kind="individual"),
    node("role", "its role as carrier\nrole", 700, 135, 280, 64, kind="individual"),
    node("po", "the purchase order text\ninformation", 700, 234, 330, 64, kind="individual"),
    node("ic", "independent\ncontinuant", 260, 36, 250, 64, kind="upper"),
    node("sdc", "specifically dependent\ncontinuant", 1150, 85, 320, 64, kind="upper"),
    node("gdc", "generically dependent\ncontinuant", 1150, 234, 320, 64, kind="upper"),
]
e = [edge("a", "colour", "truck", "inheres in"), edge("b", "role", "truck", "inheres in"),
     edge("c", "truck", "ic", "is a"), edge("d", "colour", "sdc", "is a"), edge("f", "role", "sdc", "is a"),
     edge("g", "po", "gdc", "is a")]
pic = flow("A truck, its colour, its role, its paperwork", 1448, 270, n, e,
           [{"show": [x["id"] for x in n] + [x["id"] for x in e]}])
SLIDES.append(slide("A truck, its colour, its role, its paperwork", "Reuse and BFO", 5, '''  <div class="lu-eyebrow">Three kinds of continuant</div>
  <h2 class="lu-h2">Some things stand on their own. Some exist only in one bearer. Some can be copied.</h2>
  ''' + pic + '''
  <div class="lu-split">
  ''' + defnote([
      ("Independent continuant", "exists on its own; a <b>material entity</b> is made of matter."),
      ("Specifically dependent continuant", "exists only in one bearer: a <b>quality</b>, a <b>role</b>."),
  ]) + defnote([
      ("Generically dependent continuant", "information that can be copied between bearers."),
  ], label="Also defined here") + '''
  </div>''', '''<p>Five minutes. The one rule that matters for the lab: <b>BFO says these three kinds share no member</b>. A physical thing is never a role, and never a document. Remember this for the next slide.</p>
<ul><li>Walk the two arrows "inheres in": the colour and the role cannot exist without the truck. Destroy the truck and both are gone; the purchase order text survives in its copies.</li></ul>'''))

# ---------------------------------------------------------------- The reuse trap (the real explanation, drawn)
spec = json.loads((Path(__file__).resolve().parent.parent / "proto-diagrams" / "spec.json").read_text(encoding="utf-8"))
caps = [
    ("Our class", "<b>Step 1.</b> Our class: an order for a sole-sourced good <b>orders some</b> product that <b>depends on product</b> some sole-sourced component. Line 1 of the explanation, the only line we wrote."),
    ("The domain", "<b>Step 2.</b> In SCRO, <b>depends on product</b> has domain SupplyRelationship. So the product is inferred to be a supply relationship."),
    ("What that is in BFO", "<b>Step 3.</b> SCRO says a supply relationship is a <b>specifically dependent continuant</b>: something that exists only in a bearer."),
    ("What the product also is", "<b>Step 4.</b> But the product is a MaterialProduct, a material entity: an <b>independent continuant</b>."),
    ("The clash", "<b>Step 5.</b> BFO says the two are <b>disjoint</b>. No product can be both, so the product is impossible."),
    ("The red class", "<b>Step 6.</b> So our class can never have a member: it is equivalent to <b>owl:Nothing</b>. That is the red class in Protégé."),
]
trap = flow("The reuse trap, drawn from the real explanation", spec["width"], spec["height"],
            spec["nodes"], spec["edges"], spec["steps"], caps, legend=spec["legend"])
SLIDES.append(slide("The reuse trap: our real bug", "Reuse and BFO", 6, '''  <div class="lu-eyebrow">The lab's red class, explained</div>
  <h2 class="lu-h2">We borrowed a SCRO property for its name, and inherited a rule we did not know about</h2>
  ''' + trap + '''
  ''' + callout("The fix", "Do not reuse a property for its name. Use our own, <code>ul:hasComponent</code> and <code>ul:suppliedBy</code>, which say exactly what we mean. The reference file does; the lab applies it.", "concept"),
  '''<p>Six minutes, the most important slide of Part 4. Step through slowly; at step 5 ask the room why the product cannot be both, and let them use the previous slide.</p>
<ul><li>The six steps are the six lines of Protégé's real explanation (the screenshot on "Reading an explanation"). ROBOT's explain finds a second, equally valid chain through BFO's <i>specifically depends on</i> (<code>reference-outputs/explain_v0_ELK.md</code>).</li>
<li>In plain words: SCRO's "depends on product" means one dependent thing (a supply relationship) depends on a product. We used it to mean a product needs a component. The name fit; the meaning did not.</li></ul>'''))

# ---------------------------------------------------------------- Competency questions (sort)
SLIDES.append(slide("Competency questions decide scope", "Reuse and BFO", 5, '''  <div class="lu-eyebrow">Method · drag or use the arrow buttons</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-sort" data-qid="s3-sort" data-label="Order the ontology-building method">
      <p class="lu-h3" style="margin-bottom:var(--lu-s3)">Put the method in the order you will actually work in.</p>
      <ul class="lu-sort__list">
        <li class="lu-sort__item" data-rank="3"><span>Extend SCRO only where a question needs a class it lacks</span></li>
        <li class="lu-sort__item" data-rank="1"><span>Write the competency questions the organisation actually asks</span></li>
        <li class="lu-sort__item" data-rank="5"><span>Read the inferred tree and fix the model, not the output</span></li>
        <li class="lu-sort__item" data-rank="2"><span>Search for a published ontology that already answers them</span></li>
        <li class="lu-sort__item" data-rank="4"><span>Run ELK, then HermiT</span></li>
      </ul>
    </div>
    <div class="lu-stack">
      ''' + defbox([("Competency question", "A question the ontology must be able to answer. It decides what belongs in the ontology.")]) + '''
      ''' + callout("In our file", "Every class carries the question it answers, as a <code>ul:answersCQ</code> note. Eight questions, listed in <code>competency_questions.md</code>.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. Let them argue about whether the search comes before or after writing the questions. It comes after: you cannot judge whether SCRO covers you until you know what you are asking.</p>
<p>The rule that decides scope: a class earns its place by answering a question the organisation actually asks. If you cannot name the question, delete the class.</p>''', kind="tint"))

# ---------------------------------------------------------------- Poll
SLIDES.append(slide("Poll: does this class earn its place?", "Reuse and BFO", 4, '''  <div class="lu-eyebrow">Room poll · 45 seconds</div>
  <div class="lu-poll" data-qid="s3-poll" data-seconds="45" data-answer="b" data-label="Does a class per service level earn its place?">
    <p class="lu-mcq__q">Someone adds a class <code>ul:DTPShipment</code> for Brunel's <code>Service Level</code> column. Keep it?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">Keep it: the data has the column<span class="lu-mcq__why" hidden>The source schema is not an argument for a class.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">Delete it unless a competency question needs it<span class="lu-mcq__why" hidden>Correct. Questions set the scope, not columns. A plain value can carry the level.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">Replace it with a GS1 term<span class="lu-mcq__why" hidden>Reusing a term you do not need is still an unearned class.</span></button>
    </div>
  </div>''', '''<p>Forty five seconds, then reveal and tally with the plus buttons. Spend the rest on whoever picked a: the schema first instinct this course exists to dislodge.</p>
<p>Session 1 found that CRF orders are exactly the V44_3 orders and have no freight rate: that <i>is</i> a question worth asking, and it could earn a class. Ask the room to name the question first.</p>''', kind="tint", extra_attr=' style="--lu-s5:12px"'))

# ---------------------------------------------------------------- Alignment hazards
n = [
    node("a", "carrier V444_1\n(Brunel)", 220, 70, 260, 76, kind="individual"),
    node("b", "the same carrier\nin another source", 760, 70, 280, 76, kind="individual"),
    node("c", "Carrier", 220, 220, 200, 60, kind="reused"),
    node("d", "an organisation class\nin another ontology", 760, 220, 320, 76, kind="builtin"),
]
e = [edge("x", "a", "b", "owl:sameAs: one thing, merged", both=True),
     edge("y", "c", "d", "owl:equivalentClass: same members", both=True)]
pic = flow("Two alignment axioms with side effects", 1000, 290, n, e, [{"show": [x["id"] for x in n] + [x["id"] for x in e]}])
SLIDES.append(slide("Alignment hazards", "Reuse and BFO", 4, '''  <div class="lu-eyebrow">Linking to other ontologies</div>
  <h2 class="lu-h2">Two linking axioms that look harmless and are not</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + pic + '''
    <div class="lu-stack">
      ''' + defnote([
          ("owl:sameAs", "two names for exactly the same individual. The reasoner merges everything said about them."),
          ("owl:equivalentClass", "two classes with exactly the same members. Every rule on one applies to the other."),
      ]) + '''
      ''' + callout("Safer", "Prefer <code>rdfs:subClassOf</code> until you can defend the equivalence. Keep &ldquo;probably the same&rdquo; for Session 5's entity resolution, with a confidence.") + '''
    </div>
  </div>''', '''<p>Four minutes. sameAs is routinely misused for "these records probably refer to the same carrier". That is a similarity claim, and it belongs in Session 5 with a reported confidence, not as a logical identity the reasoner propagates everywhere.</p>
<p>equivalentClass imports every axiom on the other side, which is exactly how the reuse trap on the previous slides happened, one level down.</p>'''))
