"""Session 4: the lab (AGENTS.md 2e: individual, not collected or graded),
the discussion with Milestone 1 of the team project, and the wrap."""
from common import slide, divider, callout
from kit import head

SLIDES = []

SLIDES.append(divider("Lab · Validate, triage, gate, write your own", "Lab", "Lab · about 55 minutes · on your own machine",
    "Our graph has 3,435 problems. Which ones are yours to fix?",
    "Then write three shapes of your own, and watch a gate stop a typo."))

# ---------------------------------------------------------------- Lab brief
SLIDES.append(slide("Lab brief", "Lab", 3,
    head("Hands-on lab · about 55 minutes", "The real graph, the real report, and three shapes of your own.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <ol class="lu-list lu-list--num">
      <li><b>Build and observe.</b> Validate the first draft (3,435), then the triaged shapes (2 Violations). Record provenance, release the ontology as 1.0.0, run the gate on the sample and on the broken sample, read GS1's shapes.</li>
      <li><b>Write your own.</b> Three shapes in <code>my_shapes.ttl</code>; <code>check_my_shapes.py</code> says right or not yet.</li>
      <li><b>Think.</b> Three questions, one about your own team's data, for the discussion.</li>
    </ol>
    <div class="lu-stack">
      ''' + callout("Nothing to hand in", "The lab is for understanding. The README in <code>demos/session-04-shacl/</code> says what to expect at each step and what to take to your project.", "concept") + '''
      ''' + callout("If the big graph is slow", "Each full run takes about two minutes. Short of time? Use <code>--data ci/sample-orders.ttl</code>: the same shapes on six real orders, in a second.", "neutral") + '''
    </div>
  </div>''', '''<p>Three minutes, then walk the room. Most common blocker: <code>brunel.ttl</code> missing, because Session 2's <code>convert_to_rdf.py</code> was never run on this laptop; <code>validate.py</code> says so in one line.</p>
<ul><li>Second blocker: the old Session 2 virtual environment without pySHACL. <code>pip install -r demos/requirements.txt</code> fixes it.</li></ul>'''))

# ---------------------------------------------------------------- Lab time
SLIDES.append(slide("Lab time", "Lab", 50,
    head("Lab · 50 minutes", "Each student on their own machine. Checkpoints keep you on time.") + '''
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:var(--lu-s4)">
    <div class="lu-card"><span class="lu-card__label">By minute 25 · Part A</span><p class="lu-sub">First draft 3,435 Violations; triaged 2 Violations and 2,579 Warnings. The gate passes the sample and fails the broken one, exit code 1.</p></div>
    <div class="lu-card"><span class="lu-card__label">By minute 40 · Part B</span><p class="lu-sub"><code>python check_my_shapes.py</code> says 3 of 3. Stuck? The hints name the missing piece.</p></div>
    <div class="lu-card"><span class="lu-card__label">By minute 50 · Part C</span><p class="lu-sub">Answers to the three questions, one of them about your own team's data.</p></div>
  </div>
  ''' + callout("For your team project", "Milestone 1 asks for the same pipeline on your own data: shapes for your rules, a triaged report, provenance, a version IRI, and a gate that blocks a bad commit.", "concept"),
    '''<p>Fifty minutes. At minute 25, anyone still waiting on the full graph switches to <code>--data ci/sample-orders.ttl</code> and continues.</p>
<ul><li>Most common wrong answer in Part B: Y2 with the dates written as plain text. Every order then fails, and the checker's hint says why.</li>
<li>Second: Y3 comparing the carrier with the text "V44_3" instead of its IRI, which flags the one correct CRF order.</li></ul>'''))

# ---------------------------------------------------------------- Discussion and Milestone 1
SLIDES.append(slide("Discussion and Milestone 1", "Wrap", 10, '''  <div class="lu-eyebrow">Discussion · as a room, from Part C</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">Three questions, the last one about your own data</h2>
      <ol class="lu-list lu-list--num">
        <li>Pick one Session 1 rule OWL could state as an axiom. Should it live in the ontology, in the shapes, or both?</li>
        <li>The 1,370 orders in the rate table's gap: who fixes what, and how would the report show it is fixed?</li>
        <li>Name two rules in your team's data: which are core, which need SPARQL, and what severity each gets.</li>
      </ol>
    </div>
    <div class="lu-card">
      <span class="lu-card__label">Milestone 1 · a checkpoint, not graded · push at the end of this session</span>
      <ul class="lu-list">
        <li>Your ontology, with a version IRI</li>
        <li>A shapes file covering your rule list</li>
        <li>A triaged validation report</li>
        <li>Provenance for your data</li>
        <li>A gate that blocks a bad commit</li>
      </ul>
      <p class="lu-caption">For feedback only: the project is graded once, at the end. Read before you push: Allemang, Hendler and Gandon on RDFS and SHACL, and on good and bad modeling practices; Hogan et al., Chapter 7.</p>
    </div>
  </div>''', '''<p>Ten minutes: five on the questions, five on Milestone 1. Question 1 has no single answer: a rule that must hold for reasoning (a domain) belongs in OWL; a rule about what the data must contain belongs in the shapes. Many teams will say both, and should say why.</p>
<ul><li>Milestone 1 is a checkpoint for feedback, not graded (instructor, 2026-09-26): the team project is scored once, before Session 8. Point teams at <code>.github/workflows/shacl-gate.yml</code> and <code>validate.py</code> as templates.</li></ul>'''))

# ---------------------------------------------------------------- Glossary
GLOSS = [
    ("SHACL", "Rules the data must obey, checked."),
    ("Shape · target", "A set of rules · the nodes it checks."),
    ("Focus node", "The node being checked."),
    ("Node · property shape", "About a node · about one property."),
    ("Validation report", "One result per broken rule."),
    ("Severity", "Violation, Warning or Info."),
    ("SHACL-SPARQL", "A rule written as a query."),
    ("Triage", "Rule wrong, or data wrong?"),
    ("Provenance · PROV-O", "Where data came from · as triples."),
    ("Version IRI", "The name of one release."),
    ("Validation gate", "No Violation, or no merge."),
    ("CI · GitHub Actions", "Checks on every push · GitHub's."),
    ("EPCIS", "GS1's supply chain event standard."),
    ("Open · closed world", "Missing is unknown · missing is false."),
]
half = (len(GLOSS) + 1) // 2
SLIDES.append(slide("Glossary for this session", "Wrap", 1,
    head("Glossary", "The main words this session introduced. Every one is clickable on the slides.") +
    '<div class="lu-split" style="margin-top:var(--lu-s2)">' +
    "".join('<dl class="lu-defs">' + "".join(f"<dt>{t}</dt><dd>{d}</dd>" for t, d in part) + "</dl>"
            for part in (GLOSS[:half], GLOSS[half:])) + '</div>',
    '''<p>One minute, or skip in class: it is for revision. The full list is in <code>GLOSSARY.md</code>.</p>'''))

# ---------------------------------------------------------------- Wrap
SLIDES.append(slide("Wrap and next session", "Wrap", 2, '''  <div class="lu-eyebrow">Wrap</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">One sentence to leave with.</h2>
      <p class="lu-statement">A rule nobody runs is a wish. A shape in a gate is a rule that holds.</p>
      ''' + callout("Before Session 5", "Sequeda and Lassila, Chapters 2 and 3 (designing enterprise knowledge graphs, mapping design patterns); Kejriwal et al., Chapter 8. Bring the 1,209 untyped bands: Session 5's mapping is where they get fixed.") + '''
    </div>
    <div class="lu-stack">
      <div class="lu-card">
        <span class="lu-card__label">Next session</span>
        <h3 class="lu-h3">Session 5 · Integrating operational data</h3>
        <p class="lu-sub">Today the graph came from files. Next week it comes from a live database, through mappings, and today's shapes check what the mappings produce.</p>
      </div>
      <div class="lu-row"><span class="lu-tag lu-tag--green">For your team</span><span class="lu-caption" style="flex:1">Milestone 1 is due at the end of today. Copy the gate first; it catches the rest.</span></div>
    </div>
  </div>''', '''<p>Two minutes. End on the sentence.</p>''', kind="tint"))

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
  </div>''', '''<p>Close here so students know where the self study tools are.</p>''',
    extra_attr=' style="--lu-s3:4px;--lu-s2:2px;--lu-s5:14px"'))
