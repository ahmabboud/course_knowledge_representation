"""Session 3: the lab (AGENTS.md 2e: individual, not collected or graded) and the wrap."""
from common import slide, divider, defbox, callout, figure, placeholder
from kit import head

SLIDES = []
IMG = "../assets/img/"
VIDEO = "https://www.youtube.com/watch?v=CduRWyyL3q8&list=PLNohRKRAHaszTV3puqFM9yXDXnEqjS6Fd"

SLIDES.append(divider("Lab · Find the bug, fix it, write your own", "Lab",
    "Lab · about 70 minutes · on your own machine",
    "Our ontology has a real mistake in it. Can you make the reasoner show you where?",
    "Then watch the fixed file classify real shipments, and write three axioms of your own."))

# ---------------------------------------------------------------- Lab brief
SLIDES.append(slide("Lab brief", "Lab", 3,
    head("Hands-on lab · about 70 minutes", "A buggy file, a reasoner, and three axioms of your own.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <ol class="lu-list lu-list--num">
      <li><b>Build and observe.</b> Open <code>scro-extension-v0.ttl</code>, run ELK, find the red class, read why, run HermiT, see the fix, watch <code>sample-shipments.ttl</code> classify two shipments.</li>
      <li><b>Write your own.</b> Three axioms in <code>my_axioms.ttl</code>; <code>check_my_axioms.py</code> says right or not yet.</li>
      <li><b>Think.</b> Three questions, one about your own team's data, for the discussion.</li>
    </ol>
    <div class="lu-stack">
      ''' + callout("Nothing to hand in", "The lab is for understanding. The README in <code>demos/session-03-ontology/</code> says what to expect at each step and what to take to your project.", "concept") + '''
      ''' + callout("If Protégé fails", "Do not debug in the room: <code>python local_reasoner.py workspace/scro-extension-v0.ttl</code> finds the same red classes from the terminal.", "neutral") + '''
    </div>
  </div>''', '''<p>Three minutes, then walk the room. Most common blocker: opening the file from <code>demos/session-03-ontology/</code> instead of <code>workspace/</code>, so the imports do not resolve (next slide, point 1). Second: <code>python fetch_ontologies.py</code> never run.</p>'''))

# ---------------------------------------------------------------- The tool: Protégé on our files
cells = [
    ("1 · Open the copy in workspace/", figure(IMG + "s3-protege-16-sample-imports.png", "Protégé imports panel: the course ontology resolved to the local file in workspace",
        "Imports resolve to local files only when the file sits next to <code>catalog-v001.xml</code>.")),
    ("2 · Asserted or Inferred", figure(IMG + "s3-protege-06-asserted-inferred-dropdown.png", "Protégé class hierarchy dropdown: Asserted and Inferred",
        "After the reasoner runs, switch to <b>Inferred</b>: that is what it added.")),
    ("3 · The ? button", figure(IMG + "s3-protege-09b-explanation-1.png", "Protégé explanation window for the red class",
        "Next to a red class: the axioms that cause it.")),
]
grid = "".join(f'<div class="lu-callout lu-callout--neutral"><span class="lu-callout__label">{t}</span>{f}</div>' for t, f in cells)
SLIDES.append(slide("The tool: Protégé on our files", "Lab", 3,
    head("One slide for the tool", "Learn Protégé from the video series. These four things it does not show, and our lab needs.") + f'''
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:var(--lu-s3)">{grid}</div>
  ''' + callout("4 · Never save over v0", "Save your fixed version as a new file. v0 is the lab's starting point for everyone, including you next week.") + '''
  <p class="lu-caption">Video series: <a href="''' + VIDEO + '''">Protégé fundamentals on YouTube</a>, the Protégé videos in that playlist, also linked in the lab README.</p>''',
    '''<p>Three minutes. Protégé is a complex GUI tool, so it gets a video plus this one slide (AGENTS.md 2c rule 5). Every capture is real, from the instructor's Protégé 5.6 on these files.</p>'''))

# ---------------------------------------------------------------- Lab time
SLIDES.append(slide("Lab time", "Lab", 55,
    head("Lab · 55 minutes", "Each student on their own machine. Checkpoints keep you on time.") + '''
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:var(--lu-s4)">
    <div class="lu-card"><span class="lu-card__label">By minute 30 · Part A</span><p class="lu-sub">Red class found and explained. HermiT shows a second one. The fixed file has none. Two shipments of V444_1 classified as at risk.</p></div>
    <div class="lu-card"><span class="lu-card__label">By minute 45 · Part B</span><p class="lu-sub"><code>python check_my_axioms.py</code> says 3 of 3. Stuck? The hints name the missing word.</p></div>
    <div class="lu-card"><span class="lu-card__label">By minute 55 · Part C</span><p class="lu-sub">Answers to the three questions, one of them about your own team's data.</p></div>
  </div>
  ''' + callout("For your team project", "Your project ontology will reuse a published one too. Before you borrow a property, open its definition and check its domain and range.", "concept"),
    '''<p>Fifty five minutes. At minute 30, anyone still without a red class runs <code>python local_reasoner.py workspace/scro-extension-v0.ttl</code> and continues from the explanation.</p>
<ul><li>Most common wrong answer in Part B: Y3 without the <code>someValuesFrom</code> part, the only trap from Part 2. The checker names it.</li>
<li>HermiT through the checker takes about 20 seconds; tell them it is not frozen.</li></ul>'''))

# ---------------------------------------------------------------- Licensing exercise
SLIDES.append(slide("The licensing exercise", "Lab", 10, '''  <div class="lu-eyebrow">Inside the lab · 10 minutes, as a room</div>
  <div class="lu-split">
    <div class="lu-stack">
      <h2 class="lu-h2">Licence literacy is part of reuse, not an administrative detail</h2>
      <ol class="lu-list lu-list--num">
        <li>Open the SCORVoc repository, <code>vocol/scor</code>, on GitHub.</li>
        <li>Find the <b>ODC PDDL</b> licence declared inside <code>scor.ttl</code>.</li>
        <li>Find the <b>all rights reserved</b> notice in the same repository's README.</li>
        <li>Decide which governs. Write why, in two sentences.</li>
      </ol>
      ''' + callout("Why it is here", "It is one reason this course builds on IOF SCRO (MIT licence), not SCORVoc. An ambiguous licence is itself the finding.") + '''
    </div>
    ''' + placeholder("Screenshot: the two contradictory licence statements, side by side",
        "Capture both notices from the same repository at the same commit, crop to the licence text, and save as <code>assets/img/s3-licence-conflict.png</code>. Date the capture in the caption: this may be fixed upstream.",
        "Same repository, same commit, two incompatible claims.") + '''
  </div>''', '''<p>Ten minutes, run as a whole-room pause. Do it live if the network holds. Check upstream before teaching: if the conflict has been resolved, the exercise still works but the caption must say so.</p>
<p>Say the full version: every third-party ontology, vocabulary and dataset in the team's final report must be listed with its licence. <code>workspace/LICENCES.md</code> records the licences for what this lab reuses.</p>'''))

# ---------------------------------------------------------------- Discussion
SLIDES.append(slide("Discussion: what did the reasoner tell us?", "Wrap", 8, '''  <div class="lu-eyebrow">Discussion · as a room, from Part C</div>
  <h2 class="lu-h2">Three questions, the last one about your own data</h2>
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <ol class="lu-list lu-list--num">
      <li><code>ul:CancelledShipment</code> answers no competency question. Keep it or delete it, and what question would earn it a place?</li>
      <li>Why did ELK miss the second red class, and when is that acceptable?</li>
      <li>Name the three main kinds of thing in your team's data. Which are continuants, which occurrents, and which published class would each subclass?</li>
    </ol>
    ''' + callout("Outcome", "Each team leaves knowing where its own classes will attach, and one property it must not borrow for its name alone.", "concept") + '''
  </div>''', '''<p>Eight minutes. Question 3 is the one to spend time on: two or three teams answer it out loud. The usual weak answer puts a business event (a delivery, a payment) under a continuant.</p>'''))

# ---------------------------------------------------------------- Glossary
GLOSS = [
    ("Ontology", "A machine readable description of kinds of things and how they relate."),
    ("Class · individual", "A kind of thing · one particular thing."),
    ("Object · datatype property", "A link to a thing · a link to a value."),
    ("TBox · ABox", "The rules · the data."),
    ("Restriction", "A class described by a condition on a property."),
    ("some · only", "At least one link · every link, if any."),
    ("Cardinality", "A rule that counts links: exactly, min, max."),
    ("Domain · range", "What a property's subject and object are inferred to be."),
    ("Primitive · defined class", "SubClassOf only · EquivalentTo, so the reasoner fills it."),
    ("Reasoner · inference", "The program · a fact it derived."),
    ("Unsatisfiable", "A class that can never have a member; red in Protégé."),
    ("Inconsistent", "An ontology that contradicts itself."),
    ("Justification", "The smallest set of axioms behind an inference."),
    ("BFO · IOF · SCRO", "The upper ontology · the industrial layers we build on."),
    ("Continuant · occurrent", "A thing that lasts · something that happens."),
    ("OWL profile", "A part of OWL chosen so reasoning stays fast: EL, QL, RL."),
    ("ELK · HermiT", "Fast EL reasoner · complete DL reasoner."),
    ("Competency question", "A question the ontology must answer; it sets the scope."),
]
half = (len(GLOSS) + 1) // 2
SLIDES.append(slide("Glossary for this session", "Wrap", 1,
    head("Glossary", "The main words this session introduced. Every one is clickable on the slides.") +
    '<div class="lu-split" style="margin-top:var(--lu-s2)">' +
    "".join('<dl class="lu-defs">' + "".join(f"<dt>{t}</dt><dd>{d}</dd>" for t, d in part) + "</dl>"
            for part in (GLOSS[:half], GLOSS[half:])) + '</div>',
    '''<p>One minute, or skip in class: it is for revision. The full list, with every BFO term, is in <code>GLOSSARY.md</code>.</p>'''))

# ---------------------------------------------------------------- Wrap
SLIDES.append(slide("Wrap and next session", "Wrap", 2, '''  <div class="lu-eyebrow">Wrap</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">One sentence to leave with.</h2>
      <p class="lu-statement">A reasoner believes everything you write. That is exactly why it can show you what you did not mean.</p>
      ''' + callout("Before Session 4", "Hogan et al., Chapter 4, Deductive Knowledge. Allemang, Hendler and Gandon: Basic OWL, Counting and sets in OWL. Bring the Session 1 business rules: next week each one becomes a SHACL shape.") + '''
    </div>
    <div class="lu-stack">
      <div class="lu-card">
        <span class="lu-card__label">Next session</span>
        <h3 class="lu-h3">Session 4 · Constraints, quality and provenance: SHACL</h3>
        <p class="lu-sub">Today OWL inferred rather than complained. Next week SHACL complains: closed world checks over the same graph.</p>
      </div>
      <div class="lu-row"><span class="lu-tag lu-tag--green">For your team</span><span class="lu-caption" style="flex:1">Pick the published ontology your project will extend, and check its licence.</span></div>
    </div>
  </div>''', '''<p>Two minutes. End on the sentence. Milestone 1 is due at the end of Session 4.</p>''', kind="tint"))

# ---------------------------------------------------------------- Self-check
SLIDES.append(slide("Self-check", "Wrap", 1, '''  <div class="lu-eyebrow">Self-check</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">How you did on this session's questions</h2>
      <div data-score></div>
    </div>
    <div class="lu-stack">
      ''' + callout("Studying alone?", "Press <kbd>S</kbd> for study mode: every definition shows inline, every reveal opens, every diagram shows its last step.", "concept") + '''
      <p class="lu-caption"><kbd>O</kbd> contents · <kbd>/</kbd> search · <kbd>?</kbd> all shortcuts. Answers are stored in this browser only.</p>
    </div>
  </div>''', '''<p>Close here so students know where the self study tools are.</p>'''))
