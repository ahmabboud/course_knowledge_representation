"""Session 7: opening and Part 1, why text to SPARQL is hard.

Every slide stands on its own (instructor rule, 2026-09-25). Counts come from
Session 2's brunel.ttl and demos/session-07-access-layer/reference-outputs/.
"""
from common import slide, divider, defbox, callout, code
from kit import flow, node, edge, head, bar

SLIDES = []
S, C, E = '<span class="tok-str">', '<span class="tok-com">', '</span>'

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
      <div class="lu-tag lu-tag--red" style="background:transparent;color:#FF9AA7;border-color:#96122B">Module 5 · Access</div>
    </div>
    <div class="lu-stack">
      <div class="lu-eyebrow">Knowledge Representation · Session 7 of 8</div>
      <h1 class="lu-display" style="max-width:24ch">The Access Layer</h1>
      <p class="lu-lead" style="max-width:50ch">A manager asks the Brunel graph a question in plain English. A language model writes the SPARQL, the graph's own description keeps it honest, and when the graph cannot answer, it says so. Then: running it for real, and what the field has not solved.</p>
    </div>
    <div class="lu-row" style="justify-content:space-between;font-size:var(--lu-t-caption);color:var(--lu-on-night-2)">
      <span>About 180 minutes · lecture, lab in Python, open problems, wrap</span>
      <span>Press <kbd>&rarr;</kbd> to begin · <kbd>?</kbd> for shortcuts</span>
    </div>
  </div>
  <template data-notes>
    <p>Before minute one: every student has a Gemini key in <code>demos/.env</code> (from <code>demos/.env.example</code>), and Session 2's <code>brunel.ttl</code> exists. A student without a working key runs the lab with <code>LLM_MODE=replay</code>.</p>
    <ul><li>The model's scores on these slides are the instructor's recorded run (<code>reference-outputs/evaluate.txt</code>). Students' live runs will differ a little; that difference is part of the lesson.</li></ul>
  </template>
</section>
''')

SLIDES.append(slide("Where we are in the architecture", "Opening", 3, '''  <div class="lu-eyebrow">Recap</div>
  <h2 class="lu-h1" style="max-width:40ch">Everything so far needed SPARQL. The people with the questions do not <em style="font-style:italic;color:var(--lu-red-700)">speak</em> it.</h2>
  <ul class="lu-pipeline" style="margin-top:var(--lu-s5)">
    <li data-state="done"><span class="lu-pipeline__n">01</span><span class="lu-pipeline__t">Sources</span><span class="lu-pipeline__d">DataCo, Brunel</span></li>
    <li data-state="done"><span class="lu-pipeline__n">02</span><span class="lu-pipeline__t">Profiling</span><span class="lu-pipeline__d">Business rules</span></li>
    <li data-state="done"><span class="lu-pipeline__n">03</span><span class="lu-pipeline__t">Graph</span><span class="lu-pipeline__d">RDF, SPARQL</span></li>
    <li data-state="done"><span class="lu-pipeline__n">04</span><span class="lu-pipeline__t">Ontology</span><span class="lu-pipeline__d">OWL, reasoner</span></li>
    <li data-state="done"><span class="lu-pipeline__n">05</span><span class="lu-pipeline__t">Constraints</span><span class="lu-pipeline__d">SHACL</span></li>
    <li data-state="done"><span class="lu-pipeline__n">06</span><span class="lu-pipeline__t">Mappings</span><span class="lu-pipeline__d">R2RML</span></li>
    <li data-state="done"><span class="lu-pipeline__n">07</span><span class="lu-pipeline__t">Learning</span><span class="lu-pipeline__d">GNN, KGE</span></li>
    <li data-state="active"><span class="lu-pipeline__n">08</span><span class="lu-pipeline__t">Access</span><span class="lu-pipeline__d">You are here</span></li>
  </ul>
  <div class="lu-split" style="margin-top:var(--lu-s5)">
    ''' + callout("What you have", "A checked, mapped graph behind a SPARQL endpoint (Session 2's Fuseki), and Session 6's lesson: a number means nothing without a fair test.", "neutral") + '''
    ''' + callout("What is new", "A layer that turns a question in English into a query, shows its evidence, refuses what it cannot answer, and is measured like any other model.") + '''
  </div>''', '''<p>Three minutes. This is the last layer of the architecture, and the one a stakeholder actually touches. Session 8's stack puts it in front of each team's graph.</p>'''))

SLIDES.append(slide("Session objective and shape", "Opening", 3, '''  <div class="lu-eyebrow">Objective</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <p class="lu-statement">By the end you can build a question answering layer over a graph, make it check and repair its own queries, make it refuse, and measure it on a test set.</p>
      ''' + callout("Open these now", "<code>demos/session-07-access-layer/</code>, starting with its <code>OVERVIEW.md</code> · your key in <code>demos/.env</code> · a terminal with <code>demos/.venv</code> active.", "concept") + '''
    </div>
    <div class="lu-card">
      <span class="lu-card__label">How the ~180 minutes are spent</span>
      <ul class="lu-layers">
        <li><span class="lu-layers__name">Lecture · ~85 min</span><span class="lu-layers__note">Why it is hard, grounding, check and repair, measuring, deployment</span></li>
        <li><span class="lu-layers__name">Lab · ~50 min</span><span class="lu-layers__note">VoID, prompt, ask, check, evaluate, serve; three improvements</span></li>
        <li><span class="lu-layers__name">Open problems · ~22 min</span><span class="lu-layers__note">Six unsolved questions; each team picks one</span></li>
        <li><span class="lu-layers__name">Wrap · ~11 min</span><span class="lu-layers__note">Scores against the leaderboard, the Session 8 checklist</span></li>
      </ul>
    </div>
  </div>''', '''<p>Name the stance now: the model is the least trustworthy part of this system, so everything around it is built to check it.</p>''', kind="tint"))

SLIDES.append(divider("Part 1 · Why it is hard", "Why it is hard",
    "Part 1 of 5 · about 15 minutes",
    "A language model writes SQL and SPARQL fluently. Why not just ask it?",
    "Because it writes about the graph it imagines, not the one you have."))

q = (f'''SELECT (COUNT(?order) AS ?n) WHERE {{
  ?order ul:carriedBy
    &lt;https://ul.edu.lb/kr/id/carrier/brunel/V44_3&gt; .
}}''')
SLIDES.append(slide("The question and the query", "Why it is hard", 4, '''  <div class="lu-eyebrow">The gap this session closes</div>
  <h2 class="lu-h2">The manager's sentence and the query that answers it share almost no words</h2>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <p class="lu-statement" style="font-size:var(--lu-t-h3)">&ldquo;How many orders did carrier V44_3 carry?&rdquo;</p>
      ''' + code("the query that answers it · 854", q) + '''
    </div>
    <div class="lu-stack">
      ''' + defbox([("Text to SPARQL", "Turning a question in plain language into a SPARQL query."),
                    ("Large language model", "A model trained on huge amounts of text that writes text, and code, one piece at a time.")]) + '''
      ''' + callout("What the writer must know", "The property is <code>ul:carriedBy</code>, not &ldquo;carry&rdquo;. The carrier is an IRI built from its code. Neither is in the question.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. 854 is the real answer (Session 2's Q1; test question 4 of the lab). Ask the room: what does a writer need to know that the question does not say? The vocabulary, and the naming rule.</p>'''))

cards = [
    ("It invents a property", "<code>ul:shippedBy</code> sounds right. The graph says <code>ul:carriedBy</code>. The query runs and answers nothing."),
    ("It misses a subclass", "<code>?o a ul:Order</code> finds 9,023 orders. The graph has 9,215: 192 are typed <code>ul:LateOrder</code> only."),
    ("It answers the unanswerable", "&ldquo;Which customers are in Beirut?&rdquo; The graph has no places at all, but a query can still be written."),
]
grid = "".join(f'<div class="lu-card"><span class="lu-card__label">{t}</span><p class="lu-sub">{d}</p></div>' for t, d in cards)
SLIDES.append(slide("Three ways a model goes wrong", "Why it is hard", 5,
    head("Three failures, each real on the Brunel graph", "Only the first one produces an error you would notice") + f'''
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:var(--lu-s3)">{grid}</div>
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    <div class="lu-stack" style="gap:var(--lu-s2)"><span class="lu-card__label">Orders found by <code>?o a ul:Order</code></span>''' + bar(9023, 9215, "9,023", "red") + '''<span class="lu-card__label">All orders</span>''' + bar(9215, 9215, "9,215") + '''</div>
    ''' + defbox([("Hallucination", "A model stating something fluent that is not true: here, a property or an answer the graph does not have.")]) + '''
  </div>''', '''<p>Five minutes. The counts are Session 2's (Q5: 9,023 with the plain type, 9,215 with subclasses). The invented property is the lab's <code>broken.sparql</code>; the Beirut question is test question 13.</p>
<ul><li>The dangerous one is the second: a wrong number that looks right. Keep it in mind; Part 3 shows the check cannot catch it.</li></ul>'''))

nodes = [
    node("q", "question", 110, 60, 180, 56, kind="literal"),
    node("s", "schema + 3 examples", 420, 60, 300, 56, kind="builtin"),
    node("m", "language model", 760, 60, 250, 56, kind="builtin"),
    node("c", "check the query", 1100, 60, 270, 56, kind="builtin"),
    node("g", "run on the graph", 1100, 190, 270, 56, kind="builtin"),
    node("r", "rows: answer + evidence", 700, 190, 340, 56, kind="literal"),
    node("x", "REFUSE: what is missing", 300, 190, 360, 56, kind="literal"),
]
edges = [edge("a", "q", "s", ""), edge("b", "s", "m", "prompt"), edge("c1", "m", "c", "query"),
         edge("d", "c", "m", "problems", route="elbow", sides=["top", "top"]),
         edge("e", "c", "g", "valid"), edge("f", "g", "r", ""),
         edge("h", "m", "x", "cannot", route="elbow", sides=["bottom", "top"])]
steps = [
    {"show": ["q", "s", "a"], "run": ["a"], "set": {"s": "active"}},
    {"show": ["m", "b"], "run": ["b"], "set": {"s": "idle", "m": "active"}},
    {"show": ["c", "c1"], "run": ["c1"], "set": {"m": "idle", "c": "active"}},
    {"show": ["d"], "run": ["d"], "set": {"c": "impossible"}},
    {"show": ["g", "r", "e", "f"], "run": ["e", "f"], "set": {"c": "active", "r": "inferred"}},
    {"show": ["x", "h"], "run": ["h"], "set": {"c": "idle", "x": "inferred"}},
]
caps = [
    ("Ground it", "<b>Step 1.</b> The question is sent with what the graph holds (its schema) and the three closest worked examples. Part 2."),
    ("Ask", "<b>Step 2.</b> The model writes one query, or says it cannot."),
    ("Check", "<b>Step 3.</b> Before anything runs: is it SPARQL, and does every property exist? Part 3."),
    ("Repair", "<b>Step 4.</b> If not, the problems go back to the model as hints, up to twice."),
    ("Answer", "<b>Step 5.</b> A valid query runs on the graph. The rows are the answer and its evidence."),
    ("Refuse", "<b>Step 6.</b> If the graph cannot answer, the right output is a refusal that says what is missing."),
]
walk = flow("The access layer", 1448, 240, nodes, edges, steps, caps,
            flags={"impossible": "problems", "inferred": "output"},
            legend={"builtin": "A step", "literal": "What goes in or out", "impossible": "Check failed", "inferred": "Output"})
SLIDES.append(slide("The access layer, step by step", "Why it is hard", 5, '''  <div class="lu-eyebrow">Walkthrough · the design of this session</div>
  <h2 class="lu-h2">The model is one step of six. The other five are there to keep it honest.</h2>
  ''' + walk, '''<p>Five minutes. This is the whole session on one slide: Part 2 is step 1, Part 3 is steps 3, 4 and 6, Part 4 measures the lot. The lab's <code>access_layer.py</code> is these six steps in about 260 lines.</p>'''))
