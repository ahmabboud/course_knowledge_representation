"""Session 3, Part 3: what a reasoner does.

Every screenshot is a real capture from the instructor's Protégé 5.6
(2026-09-22); every reasoner result is a recorded run in
demos/session-03-ontology/reference-outputs/.
"""
from common import slide, divider, defbox, callout, figure
from kit import flow, node, edge, defnote

SLIDES = []
IMG = "../assets/img/"

SLIDES.append(divider("Part 3 · What a reasoner does", "The reasoner",
    "Part 3 of 5 · about 27 minutes",
    "Our file carries 4,819 axioms. Who checks that none of them contradict each other?",
    "Nobody, by hand. A reasoner does, in seconds, and tells you exactly which axioms are to blame."))

# ---------------------------------------------------------------- 4,819 axioms
SLIDES.append(slide("Nobody checks 4,819 axioms by hand", "The reasoner", 4, '''  <div class="lu-eyebrow">Why a reasoner</div>
  <h2 class="lu-h2">Our small extension imports SCRO, IOF Core and BFO: 4,819 axioms, 254 classes</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + figure(IMG + "s3-protege-02-active-ontology.png", "Protégé Active ontology tab: metrics 4,819 axioms, 254 classes, imports SupplyChain and BFO",
                 "Real capture: Protégé 5.6, the lab file <code>scro-extension-v0.ttl</code>, Active ontology tab. Right: the metrics. Bottom: what it imports.") + '''
    <div class="lu-stack">
      ''' + defnote([
          ("Reasoner", "a program that works out every fact that follows from an ontology's axioms."),
          ("Inference", "a fact the reasoner derived that nobody wrote down."),
      ]) + '''
      ''' + callout("Open world, one more time", "The reasoner never assumes a missing fact is false. No carrier recorded means <b>unknown</b>, not <b>none</b>.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. Our own file is small (about 40 of our classes and properties); the 4,819 come from what it imports. Nobody reads that by hand, and a single wrong axiom anywhere can change the meaning of ours.</p>
<ul><li>The open world callout is Session 1's point, repeated because every reasoner result today depends on it.</li></ul>'''))

# ---------------------------------------------------------------- Three jobs
def job(kind):
    if kind == "consistency":
        n = [node("a", "Late shipment", 110, 30, 200, 48, kind="ours"),
             node("b", "Cancelled shipment", 350, 30, 230, 48, kind="ours"),
             node("x", "one shipment in both", 230, 118, 260, 48, kind="individual", flag="right")]
        e = [edge("d", "a", "b", "disjoint", both=True, kind="conflict"),
             edge("p", "x", "a", "is a"), edge("q", "x", "b", "is a")]
        s = {"x": "impossible"}
    elif kind == "classification":
        n = [node("a", "At-risk shipment", 230, 118, 240, 48, kind="ours", flag="right"),
             node("b", "Shipment", 230, 30, 200, 48, kind="reused")]
        e = [edge("p", "a", "b", "subclass of (inferred)", kind="inferred")]
        s = {"a": "inferred"}
    else:
        n = [node("a", "shipment 1447291369.7", 230, 118, 280, 48, kind="individual", flag="right"),
             node("b", "At-risk shipment", 230, 30, 240, 48, kind="ours")]
        e = [edge("p", "a", "b", "is a (inferred)", kind="inferred")]
        s = {"a": "inferred"}
    return flow(kind, 460, 150, n, e, [{"show": [x["id"] for x in n] + [x["id"] for x in e], "set": s}])


jobs = [("consistency", "Consistency", "Can this ontology have any model at all? One thing in two disjoint classes: no."),
        ("classification", "Classification", "Compute the full tree, including subclass links nobody wrote."),
        ("realization", "Realization", "For every individual, compute every class it belongs to.")]
cells = "".join(f'<div class="lu-callout lu-callout--concept"><span class="lu-callout__label">{t}</span>{job(k)}<p class="lu-sub">{d}</p></div>'
                for k, t, d in jobs)
SLIDES.append(slide("Three jobs", "The reasoner", 5, '''  <div class="lu-eyebrow">What a reasoner actually does for you</div>
  <h2 class="lu-h2">Three jobs, each finding a different kind of mistake</h2>
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr))">''' + cells + '''</div>
  ''' + defbox([
      ("Subsumption", "The &ldquo;is a subclass of&rdquo; relation, stated or inferred."),
      ("Consistency check", "The test that the ontology does not contradict itself."),
  ]), '''<p>Five minutes. Walk the three cards left to right. The middle one is real: At-risk shipment is defined as "Shipment and handled by some Sanctioned carrier", so the reasoner concludes it is a subclass of Shipment although nobody wrote that line. The right one is the lab's realization result (<code>reference-outputs/realized-sample.txt</code>).</p>
<ul><li>Amber means inferred: Protégé shows the same thing with a yellow background. Red means impossible.</li></ul>'''))

# ---------------------------------------------------------------- The red class
SLIDES.append(slide("The red class", "The reasoner", 4, '''  <div class="lu-eyebrow">What an error looks like</div>
  <h2 class="lu-h2">A class that can never have a member turns red, under owl:Nothing</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + figure(IMG + "s3-protege-08-red-class-selected.png", "Protégé inferred class tree with Order for a sole-sourced good in red, equivalent to owl:Nothing",
                 "Real capture: ELK on <code>scro-extension-v0.ttl</code>. <b>Order for a sole-sourced good</b> is red.") + '''
    <div class="lu-stack">
      ''' + defnote([
          ("Satisfiable class", "a class that could have at least one member without contradiction."),
          ("Unsatisfiable class", "a class that can never have a member. Protégé shows it red."),
          ("owl:Nothing", "the empty class. An unsatisfiable class is equivalent to it."),
      ]) + '''
      ''' + callout("Not a crash, a finding", "Nothing failed. The reasoner proved that our own definition asks for something impossible. The lab finds out why.") + '''
    </div>
  </div>''', '''<p>Four minutes. This is the moment of the lab, shown now so nobody panics when it happens on their screen. ELK finds one red class in v0; HermiT finds two (Part 5 explains why).</p>
<ul><li>An unsatisfiable class is not the same as an inconsistent ontology: one class is empty, the rest still works. The next slide shows the other case.</li></ul>'''))

# ---------------------------------------------------------------- Walkthrough: a domain mistake
n = [
    node("po", "purchase order po88", 220, 40, 280, 56, kind="individual", flag="bottom"),
    node("c", "carrier V444_1", 720, 40, 250, 56, kind="individual"),
    node("ship", "Shipment", 220, 165, 220, 56, kind="reused", flag="right"),
    node("ic", "independent\ncontinuant", 220, 290, 250, 68, kind="upper"),
    node("pord", "Purchase order", 720, 165, 240, 56, kind="reused"),
    node("gdc", "generically dependent\ncontinuant", 720, 290, 300, 68, kind="upper"),
]
e = [
    edge("a", "po", "c", "handled by"),
    edge("b", "po", "ship", "is a (domain)", kind="inferred"),
    edge("c1", "ship", "ic", "is a"),
    edge("d", "po", "pord", "is a", route="elbow", sides=["right", "top"]),
    edge("f", "pord", "gdc", "is a"),
    edge("g", "ic", "gdc", "disjoint", both=True, kind="conflict"),
]
steps = [
    {"show": ["po", "c", "a"], "run": ["a"], "set": {"po": "active"}},
    {"show": ["ship", "b"], "run": ["b"], "set": {"ship": "inferred"}},
    {"show": ["ic", "c1", "pord", "gdc", "d", "f"], "run": ["c1", "d", "f"], "set": {"ship": "idle", "po": "active"}},
    {"show": ["g"], "run": ["g"], "set": {"po": "impossible", "ic": "impossible", "gdc": "impossible"}},
]
caps = [
    ("One careless fact", "<b>Step 1.</b> A mapping says purchase order po88 is <b>handled by</b> carrier V444_1. In SQL a foreign key would refuse it. Here, nothing complains."),
    ("The domain infers", "<b>Step 2.</b> The domain of <b>handled by</b> is Shipment, so the reasoner concludes po88 is a Shipment."),
    ("What SCRO already says", "<b>Step 3.</b> In SCRO a Shipment is a physical thing (an independent continuant) and a purchase order is information (a generically dependent continuant)."),
    ("Inconsistent", "<b>Step 4.</b> BFO says nothing can be both. So the whole ontology is <b>inconsistent</b>, and the reasoner refuses to answer anything."),
]
walk = flow("A domain mistake, found by the reasoner", 1000, 330, n, e, steps, caps, legend={
    "reused": "Reused, IOF SCRO", "upper": "BFO, upper ontology", "individual": "Individual"})
SLIDES.append(slide("Walkthrough: a domain mistake", "The reasoner", 5, '''  <div class="lu-eyebrow">Diagnostic walkthrough</div>
  <h2 class="lu-h2">One careless fact, four steps, and the reasoner stops everything</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + walk + '''
    <div class="lu-stack">
      ''' + callout("Real run", "<code>python local_reasoner.py workspace/domain-mistake.ttl</code> answers: the ontology is inconsistent.", "neutral") + '''
      ''' + callout("The lesson", "A domain is a promise about every subject. Attach the property to the wrong kind of thing and the reasoner believes you, all the way to a contradiction.") + '''
    </div>
  </div>''', '''<p>Five minutes. Step through with the arrow keys; ask the room at step 2 what they expect before showing step 3.</p>
<ul><li>This is a real HermiT run on <code>demos/session-03-ontology/domain-mistake.ttl</code> (<code>reference-outputs/domain-mistake.txt</code>). po88 is a purchase order from the Session 5 ERP seed data.</li>
<li>Inconsistent is stronger than unsatisfiable: one impossible <i>individual</i> breaks the whole ontology, while an impossible <i>class</i> only empties that class. Protégé says "inconsistent ontology" and stops.</li>
<li>Continuant and the two kinds of dependent continuant are defined properly in Part 4; here the plain words are enough.</li></ul>'''))

# ---------------------------------------------------------------- Reading an explanation
SLIDES.append(slide("Reading an explanation", "The reasoner", 5, '''  <div class="lu-eyebrow">Why is the class red?</div>
  <h2 class="lu-h2">Click the <b>?</b> next to a red class: Protégé lists the few axioms that together cause it</h2>
  ''' + figure(IMG + "s3-protege-09b-explanation-1.png", "Protégé explanation: six axioms that make Order for a sole-sourced good equivalent to owl:Nothing",
               "Real capture: Protégé's first explanation for <b>Order for a sole-sourced good</b>, six lines. Line 1 is ours; lines 2 to 6 come from SCRO and BFO.") + '''
  <div class="lu-split">
    ''' + defbox([("Justification", "The smallest set of axioms that together cause an inference. Remove any one and the inference goes away.")]) + '''
    ''' + callout("How to read it", "Line 1 is the only line we wrote. Lines 2 to 6 were imported. So the mistake is in how line 1 <b>uses</b> SCRO. Part 4 decodes lines 2 to 6.") + '''
  </div>''', '''<p>Five minutes. Read the six lines aloud, but do not explain the BFO words yet: they are Part 4. The point now is the method: find the line that is ours.</p>
<ul><li>ROBOT's <code>explain</code> finds a different justification for the same class (<code>reference-outputs/explain_v0_ELK.md</code>): there can be more than one. Any single one is enough to fix.</li></ul>'''))

# ---------------------------------------------------------------- Check
SLIDES.append(slide("Check: which job finds which bug", "The reasoner", 3, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-mcq" data-qid="s3-q2" data-answer="b" data-label="Which reasoning task surfaces an unintended subclass"
       data-fb-correct=" Classification computes subsumption, so an unintended subclass link shows up in the inferred tree."
       data-fb-wrong=" Consistency only asks whether any model exists; a surprising subclass link is a tree question.">
    <p class="lu-mcq__q">After the reasoner runs, <b>Late shipment</b> appears under <b>At-risk shipment</b>, which nobody intended. Which job surfaced it?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">Consistency checking<span class="lu-mcq__why" hidden>An ontology with a surprising subclass link can be perfectly consistent.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">Classification<span class="lu-mcq__why" hidden>Correct: it computes every subclass link, stated or not, and this one was not stated.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">Realization<span class="lu-mcq__why" hidden>Realization places individuals in classes; this is a link between two classes.</span></button>
    </div>
  </div>''', '''<p>Three minutes. The scenario is hypothetical (it does not happen in our file): read the inferred tree as a claim about what you said. When it disagrees with what you meant, the model is wrong, not the reasoner.</p>''', kind="tint"))
