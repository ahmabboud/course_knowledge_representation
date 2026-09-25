"""Session 6: opening and Part 1, why learn on a graph.

Every slide stands on its own (instructor rule, 2026-09-25): the examples are
complete here, the lab repeats them. Numbers come from
demos/session-06-learning/reference-outputs/ and from counts on Session 5's
brunel-mapped.nt, stated in the notes.
"""
from common import slide, divider, defbox, callout
from kit import flow, node, edge, head, table, bar

SLIDES = []

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
      <div class="lu-tag lu-tag--red" style="background:transparent;color:#FF9AA7;border-color:#96122B">Module 4 · Learning</div>
    </div>
    <div class="lu-stack">
      <div class="lu-eyebrow">Knowledge Representation · Session 6 of 8</div>
      <h1 class="lu-display" style="max-width:24ch">Learning Over the Graph</h1>
      <p class="lu-lead" style="max-width:50ch">Two models learn from the Brunel graph: one predicts late orders, one predicts which plant makes a product. Each is compared with the simplest model that could do the job, and tested so that it cannot cheat.</p>
    </div>
    <div class="lu-row" style="justify-content:space-between;font-size:var(--lu-t-caption);color:var(--lu-on-night-2)">
      <span>About 180 minutes · lecture, lab in Python, wrap</span>
      <span>Press <kbd>&rarr;</kbd> to begin · <kbd>?</kbd> for shortcuts</span>
    </div>
  </div>
  <template data-notes>
    <p>Before minute one: every student's <code>demos/.venv</code> has both install lines of <code>demos/README.md</code> run again, since Session 6 adds PyTorch, PyTorch Geometric, PyKEEN and scikit-learn (about 400 MB). On Linux the CPU build of PyTorch goes first; the command is in that README.</p>
    <ul><li>Every result on these slides is a real run, recorded in <code>demos/session-06-learning/reference-outputs/</code> on 2026-09-25. The honest outcome is the lesson: the graph models do not beat the simple ones once the test is fair.</li></ul>
  </template>
</section>
''')

SLIDES.append(slide("Where we are in the architecture", "Opening", 3, '''  <div class="lu-eyebrow">Recap</div>
  <h2 class="lu-h1" style="max-width:40ch">The graph is built, checked and mapped. Now a model <em style="font-style:italic;color:var(--lu-red-700)">learns</em> from it.</h2>
  <ul class="lu-pipeline" style="margin-top:var(--lu-s5)">
    <li data-state="done"><span class="lu-pipeline__n">01</span><span class="lu-pipeline__t">Sources</span><span class="lu-pipeline__d">DataCo, Brunel</span></li>
    <li data-state="done"><span class="lu-pipeline__n">02</span><span class="lu-pipeline__t">Profiling</span><span class="lu-pipeline__d">Business rules</span></li>
    <li data-state="done"><span class="lu-pipeline__n">03</span><span class="lu-pipeline__t">Graph</span><span class="lu-pipeline__d">RDF, SPARQL</span></li>
    <li data-state="done"><span class="lu-pipeline__n">04</span><span class="lu-pipeline__t">Ontology</span><span class="lu-pipeline__d">OWL, reasoner</span></li>
    <li data-state="done"><span class="lu-pipeline__n">05</span><span class="lu-pipeline__t">Constraints</span><span class="lu-pipeline__d">SHACL</span></li>
    <li data-state="done"><span class="lu-pipeline__n">06</span><span class="lu-pipeline__t">Mappings</span><span class="lu-pipeline__d">R2RML</span></li>
    <li data-state="active"><span class="lu-pipeline__n">07</span><span class="lu-pipeline__t">Learning</span><span class="lu-pipeline__d">You are here</span></li>
    <li data-state="muted"><span class="lu-pipeline__n">08</span><span class="lu-pipeline__t">Access</span><span class="lu-pipeline__d">Questions</span></li>
  </ul>
  <div class="lu-split" style="margin-top:var(--lu-s5)">
    ''' + callout("What you have", "Session 5's graph: 9,215 orders, each linked to its customer, carrier, plant, port and product, rebuilt from the database by a mapping.", "neutral") + '''
    ''' + callout("What is new", "Questions the graph does not answer by itself: <b>will</b> this order be late? <b>Which</b> plant is missing from this product?") + '''
  </div>''', '''<p>Three minutes. Every earlier stage wrote down what is known. This one guesses what is not, and so it needs a way to measure how often the guess is right.</p>'''))

SLIDES.append(slide("Session objective and shape", "Opening", 3, '''  <div class="lu-eyebrow">Objective</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <p class="lu-statement">By the end you can train a graph model and an embedding on a knowledge graph, compare each with a baseline, and say whether the test let it cheat.</p>
      ''' + callout("Open these now", "<code>demos/session-06-learning/</code>, starting with its <code>OVERVIEW.md</code> · a terminal with <code>demos/.venv</code> active.", "concept") + '''
    </div>
    <div class="lu-card">
      <span class="lu-card__label">How the ~180 minutes are spent</span>
      <ul class="lu-layers">
        <li><span class="lu-layers__name">Lecture · ~110 min</span><span class="lu-layers__note">Why a graph, embeddings, message passing, leakage</span></li>
        <li><span class="lu-layers__name">Lab · ~55 min</span><span class="lu-layers__note">Convert the graph, run a baseline, a GNN and TransE, write three functions</span></li>
        <li><span class="lu-layers__name">Wrap · ~15 min</span><span class="lu-layers__note">Discussion, project clinic, Milestone 2, self-check</span></li>
      </ul>
    </div>
  </div>''', '''<p>Name the surprise now, so nobody feels cheated later: on Brunel, the fair test shows the graph models learn almost nothing that a count or a logistic regression does not. Finding that out properly is the skill.</p>''', kind="tint"))

SLIDES.append(divider("Part 1 · Why learn on a graph", "Why a graph",
    "Part 1 of 4 · about 15 minutes",
    "A table row already names the customer. What more can a graph give a model?",
    "The things around the order: its customer's other orders, its plant's products."))

# ---------------------------------------------------------------- a row against a graph
n = [
    node("o", "order 1447135386.7", 724, 150, 330, 60, kind="individual"),
    node("x", "3.1 kg · 1,045 units · DTP", 724, 40, 420, 56, kind="literal"),
    node("c", "customer V555_15", 250, 150, 300, 56, kind="individual"),
    node("k", "carrier V444_0", 1200, 150, 280, 56, kind="individual"),
    node("p", "PLANT08", 500, 270, 200, 56, kind="individual"),
    node("q", "PORT04", 724, 270, 200, 56, kind="individual"),
    node("d", "product 1681878", 990, 270, 280, 56, kind="individual"),
    node("oo", "109 other orders\nof V555_15", 200, 280, 300, 70, kind="individual"),
]
e = [edge("a", "o", "x", ""), edge("b", "o", "c", "orderedBy"), edge("c1", "o", "k", "carriedBy"),
     edge("d1", "o", "p", "", route="elbow"), edge("e1", "o", "q", ""), edge("f", "o", "d", "", route="elbow"),
     edge("g", "c", "oo", "")]
steps = [
    {"show": ["o", "x", "a"], "run": ["a"], "set": {"o": "active"}},
    {"show": ["c", "k", "p", "q", "d", "b", "c1", "d1", "e1", "f"], "run": ["b", "c1", "d1", "e1", "f"]},
    {"show": ["oo", "g"], "run": ["g"], "set": {"o": "idle", "oo": "inferred"}},
]
caps = [
    ("The row", "<b>Step 1.</b> A late order, and the three numbers a table model knows about it: weight, quantity, service level."),
    ("Its neighbours", "<b>Step 2.</b> In the graph it is linked to five things. A table has these too, as columns holding names."),
    ("Their neighbours", "<b>Step 3.</b> What a table does not show: this customer's 109 other orders. <b>Every one of them is late.</b> A graph model can read that."),
]
walk = flow("A row against a graph", 1448, 330, n, e, steps, caps,
            flags={"inferred": "all late"},
            legend={"individual": "Thing in the graph", "literal": "Value", "inferred": "What the neighbours show"})
SLIDES.append(slide("A row against a graph", "Why a graph", 5, '''  <div class="lu-eyebrow">Walkthrough · a real order</div>
  <h2 class="lu-h2">A row describes one order. The graph also describes everything around it.</h2>
  ''' + walk, '''<p>Five minutes. The order and all its links are real (<code>brunel-mapped.nt</code>). V555_15 has 110 orders and all 110 are late: counted on Session 5's graph.</p>
<ul><li>Plant this now, it pays off in Part 4: a signal this strong is also a trap. A model that remembers "V555_15 means late" has learned about one customer, not about lateness.</li></ul>'''))

# ---------------------------------------------------------------- two tasks
SLIDES.append(slide("Two questions for a model", "Why a graph", 5,
    head("The two tasks of this session, on Brunel", "Predict a label for a node, or predict a missing link") + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    <div class="lu-card">
      <span class="lu-card__label">Node classification · will this order be late?</span>
      <div class="lu-stack" style="gap:var(--lu-s3)">''' + bar(9215, 9215, "9,215 orders") + bar(192, 9215, "192 late", "red") + '''</div>
      <p class="lu-sub">2.1% are late. Only <b>4 of the 46 customers</b> ever have a late order.</p>
    </div>
    <div class="lu-card">
      <span class="lu-card__label">Link prediction · which plant makes this product?</span>
      <div class="lu-stack" style="gap:var(--lu-s3)">''' + bar(2036, 2036, "2,036 links") + bar(781, 2036, "781 PLANT03", "red") + '''</div>
      <p class="lu-sub">Hide some links, ask the model to find them. One plant, PLANT03, makes 781 of them.</p>
    </div>
  </div>
  ''' + defbox([("Node classification", "Predicting a label for each node: here, late or not for each order."),
                ("Link prediction", "Predicting a missing edge: here, which plant makes a product.")]),
    '''<p>Five minutes. Counts from <code>reference-outputs/build-graph.txt</code> and <code>link-prediction.txt</code>; PLANT03's 781 counted on <code>brunel-mapped.nt</code>. Ask the room: which of these two numbers already worries you? Both: one class is rare, one plant dominates.</p>'''))

# ---------------------------------------------------------------- baselines first
rows = [
    ("Late orders", "Logistic regression", "the row, with customer, carrier, plant as columns"),
    ("Late orders", "GraphSAGE", "the same, plus its neighbours (Part 3)"),
    ("Which plant", "Popularity", "how many products each plant makes"),
    ("Which plant", "TransE", "every link but the hidden ones (Part 2)"),
]
SLIDES.append(slide("The baseline comes first", "Why a graph", 5,
    head("Every model today has a simple rival", "A graph model is only interesting if it beats the simple one, on a fair test") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    ''' + table(["Task", "Model", "What it sees"], rows) + '''
    <div class="lu-stack">
      ''' + defbox([("Baseline", "The simplest reasonable model; every new model is compared with it.")]) + '''
      ''' + callout("Losing is a result", "If the graph model does not beat the baseline, that is worth reporting: it says the graph's shape adds nothing for this task.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. XGBoost is the usual stronger table baseline; for your project it is a good second one. Today logistic regression is enough, because it already ties the graph model.</p>'''))
