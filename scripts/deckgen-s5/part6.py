"""Session 5: the lab (AGENTS.md 2e: individual, not collected or graded;
2026-09-25 rule: every Part B task is the twin of a rule already shown),
the discussion and project clinic, and the wrap."""
from common import slide, divider, callout
from kit import head

SLIDES = []

SLIDES.append(divider("Lab · Map, compare, ask, match", "Lab", "Lab · about 55 minutes · on your own machine",
    "One mapping, two routes, one graph. Does it hold up?",
    "Then add three rules to a mapping, each a copy of one you have already seen."))

SLIDES.append(slide("Lab brief", "Lab", 3,
    head("Hands-on lab · about 55 minutes", "The Brunel tables in a database, and the mapping that turns them into the graph.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <ol class="lu-list lu-list--num">
      <li><b>Build and observe.</b> Start PostgreSQL, load the tables, materialize (135,799 triples), compare with Session 2, validate with Session 4's shapes, ask Ontop Q2, match the TMS customers.</li>
      <li><b>Extend a mapping.</b> Three rules in <code>my_mapping.ttl</code>, each the twin of one already there; <code>check_my_mapping.py</code> says right or not yet.</li>
      <li><b>Think.</b> Three questions, one about your own team's database.</li>
    </ol>
    <div class="lu-stack">
      ''' + callout("Nothing to hand in", "The lab is for understanding. Start with <code>OVERVIEW.md</code> in <code>demos/session-05-integration/</code>: what the data is, and why each step exists.", "concept") + '''
      ''' + callout("No Docker?", "Add <code>--sqlite</code> to the load and materialize steps: the same tables in a file. Only Ontop needs Docker; read its recorded output instead.", "neutral") + '''
    </div>
  </div>''', '''<p>Three minutes, then walk the room. Most common blocker: Morph-KGC missing, because the second install line of <code>demos/README.md</code> was not run; <code>materialize.py</code> prints the exact command.</p>
<ul><li>Second: an old PostgreSQL volume from an earlier course version. The compose file uses a new volume name, so <code>docker compose up -d</code> in this folder starts clean.</li></ul>'''))

SLIDES.append(slide("Lab time", "Lab", 50,
    head("Lab · 50 minutes", "Each student on their own machine. Checkpoints keep you on time.") + '''
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:var(--lu-s4)">
    <div class="lu-card"><span class="lu-card__label">By minute 30 · Part A</span><p class="lu-sub">135,799 triples; compare says 0 and 7; shapes say 2 Violations and 1,370 Warnings; matcher precision 0.878 and 1.000.</p></div>
    <div class="lu-card"><span class="lu-card__label">By minute 42 · Part B</span><p class="lu-sub"><code>python check_my_mapping.py</code> says 3 of 3. Each hint names the rule to copy.</p></div>
    <div class="lu-card"><span class="lu-card__label">By minute 50 · Part C</span><p class="lu-sub">Answers to the three questions, one of them about your own team's database.</p></div>
  </div>
  ''' + callout("For your team project", "Your project's database needs a mapping like this one: one triples map per table, templates from your naming rule, validated with your Session 4 shapes.", "concept"),
    '''<p>Fifty minutes. The validation step takes about two minutes; let it run while students read <code>brunel-mapping.ttl</code>.</p>
<ul><li>Most common wrong answer in Part B: Y2 written with <code>rr:column</code>, which makes text instead of a link. The checker shows the text it made.</li></ul>'''))

SLIDES.append(slide("Discussion and project clinic", "Wrap", 10, '''  <div class="lu-eyebrow">Discussion · as a room, from Part C</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">Where does each check belong?</h2>
      <ol class="lu-list lu-list--num">
        <li>A late order is an order: in the vocabulary, the shapes, or the mapping? Which of them caught the 192 unchecked orders?</li>
        <li>Session 4 checked the graph; today a mapping made it. Should the gate check the mapping's output, the database, or both?</li>
        <li>Materialize or virtualize, for your team's database, and why?</li>
      </ol>
    </div>
    <div class="lu-card">
      <span class="lu-card__label">Project clinic · 5 minutes</span>
      <p class="lu-sub">Each team says in one sentence which route it chooses for its own database, and names one thing blocking its mapping.</p>
      <p class="lu-caption">Milestone 2, a checkpoint for feedback, not graded, is pushed at the end of Session 6.</p>
    </div>
  </div>''', '''<p>Ten minutes. Question 1 has a clear answer: the rule lives in the vocabulary (a reasoner or SHACL's target resolution uses it); the mapping only produces data; the focus node count exposed the gap.</p>'''))

GLOSS = [
    ("Mapping · R2RML", "Rows to triples · the W3C language."),
    ("RML", "R2RML for CSV, JSON, XML too."),
    ("Triples map", "One table, one kind of subject."),
    ("IRI template", "An IRI built from a column."),
    ("Logical view", "An SQL query as the source."),
    ("Materialize", "Build and store the graph now."),
    ("Virtualize", "Store nothing; SPARQL to SQL."),
    ("Morph-KGC · Ontop", "Materializes · virtualizes."),
    ("OBDA", "A database queried through an ontology."),
    ("Entity resolution", "Same real thing, two records?"),
    ("Blocking", "Compare only likely pairs."),
    ("Match weight", "log2(m / u), evidence per field."),
    ("Precision · recall", "Right among found · found among right."),
]
half = (len(GLOSS) + 1) // 2
SLIDES.append(slide("Glossary for this session", "Wrap", 1,
    head("Glossary", "The main words this session introduced. Every one is clickable on the slides.") +
    '<div class="lu-split" style="margin-top:var(--lu-s2)">' +
    "".join('<dl class="lu-defs">' + "".join(f"<dt>{t}</dt><dd>{d}</dd>" for t, d in part) + "</dl>"
            for part in (GLOSS[:half], GLOSS[half:])) + '</div>',
    '''<p>One minute, or skip in class: it is for revision. The full list is in <code>GLOSSARY.md</code>.</p>'''))

SLIDES.append(slide("Wrap and next session", "Wrap", 2, '''  <div class="lu-eyebrow">Wrap</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">One sentence to leave with.</h2>
      <p class="lu-statement">Write down once what a row means, and every tool can rebuild the graph, or answer from the rows directly.</p>
      ''' + callout("Before Session 6", "Read the Session 6 lab's <code>README.md</code> and <code>OVERVIEW.md</code>. The graph learning of Session 6 starts from a graph like today's materialized one.") + '''
    </div>
    <div class="lu-stack">
      <div class="lu-card">
        <span class="lu-card__label">Next session</span>
        <h3 class="lu-h3">Session 6 · Learning over the graph</h3>
        <p class="lu-sub">Today the graph was rebuilt from the database. Next week a model learns from it: embeddings and graph neural networks.</p>
      </div>
      <div class="lu-row"><span class="lu-tag lu-tag--green">For your team</span><span class="lu-caption" style="flex:1">Write your project's first triples map, for its most important table.</span></div>
    </div>
  </div>''', '''<p>Two minutes. End on the sentence.</p>''', kind="tint"))

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
