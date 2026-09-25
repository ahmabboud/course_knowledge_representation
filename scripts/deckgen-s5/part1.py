"""Session 5: opening and Part 1, the integration problem.

Every slide stands on its own (instructor rule, 2026-09-25): the examples are
complete here, the lab repeats them. Numbers come from
demos/session-05-integration/reference-outputs/.
"""
from common import slide, divider, defbox, callout
from kit import flow, node, edge

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
      <div class="lu-tag lu-tag--red" style="background:transparent;color:#FF9AA7;border-color:#96122B">Module 3 · Integration</div>
    </div>
    <div class="lu-stack">
      <div class="lu-eyebrow">Knowledge Representation · Session 5 of 8</div>
      <h1 class="lu-display" style="max-width:24ch">Integrating Operational Data</h1>
      <p class="lu-lead" style="max-width:48ch">The Brunel data moves into a live database. A mapping, not a script, turns it into the same graph as Session 2, two ways. Then two systems disagree on how to write a customer, and we measure how well a matcher sorts it out.</p>
    </div>
    <div class="lu-row" style="justify-content:space-between;font-size:var(--lu-t-caption);color:var(--lu-on-night-2)">
      <span>About 185 minutes · lecture, lab in Python, wrap</span>
      <span>Press <kbd>&rarr;</kbd> to begin · <kbd>?</kbd> for shortcuts</span>
    </div>
  </div>
  <template data-notes>
    <p>Before minute one: every student's <code>demos/.venv</code> has both install lines of <code>demos/README.md</code> (the second adds Morph-KGC), and Docker Desktop is running. Without Docker the whole lab except Ontop runs on a database file (<code>--sqlite</code>).</p>
    <ul><li>Every number on these slides is a real run, recorded in <code>demos/session-05-integration/reference-outputs/</code> on 2026-09-25. The customer matching data is teaching data, built on purpose; its slides say so.</li></ul>
  </template>
</section>
''')

SLIDES.append(slide("Where we are in the architecture", "Opening", 3, '''  <div class="lu-eyebrow">Recap</div>
  <h2 class="lu-h1" style="max-width:40ch">The graph came from files. A company keeps its data in a <em style="font-style:italic;color:var(--lu-red-700)">database</em> that changes every day.</h2>
  <ul class="lu-pipeline" style="margin-top:var(--lu-s5)">
    <li data-state="done"><span class="lu-pipeline__n">01</span><span class="lu-pipeline__t">Sources</span><span class="lu-pipeline__d">DataCo, Brunel</span></li>
    <li data-state="done"><span class="lu-pipeline__n">02</span><span class="lu-pipeline__t">Profiling</span><span class="lu-pipeline__d">Business rules</span></li>
    <li data-state="done"><span class="lu-pipeline__n">03</span><span class="lu-pipeline__t">Graph</span><span class="lu-pipeline__d">RDF, SPARQL</span></li>
    <li data-state="done"><span class="lu-pipeline__n">04</span><span class="lu-pipeline__t">Ontology</span><span class="lu-pipeline__d">OWL, reasoner</span></li>
    <li data-state="done"><span class="lu-pipeline__n">05</span><span class="lu-pipeline__t">Constraints</span><span class="lu-pipeline__d">SHACL</span></li>
    <li data-state="active"><span class="lu-pipeline__n">06</span><span class="lu-pipeline__t">Mappings</span><span class="lu-pipeline__d">You are here</span></li>
    <li data-state="muted"><span class="lu-pipeline__n">07</span><span class="lu-pipeline__t">Learning</span><span class="lu-pipeline__d">GNN</span></li>
    <li data-state="muted"><span class="lu-pipeline__n">08</span><span class="lu-pipeline__t">Access</span><span class="lu-pipeline__d">Questions</span></li>
  </ul>
  <div class="lu-split" style="margin-top:var(--lu-s5)">
    ''' + callout("What you have", "Session 2's converter, a Python script that read four Brunel CSV files once. Session 4's shapes, and its note: 1,209 rate bands point at carriers nobody typed. Fix it in the mapping.", "neutral") + '''
    ''' + callout("What is missing", "A way to rebuild the graph from a <b>live</b> database, whenever it changes, without writing the converter again.") + '''
  </div>''', '''<p>Three minutes. Stage 06 is where the graph stops being a one-time export.</p>'''))

SLIDES.append(slide("Session objective and shape", "Opening", 3, '''  <div class="lu-eyebrow">Objective</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <p class="lu-statement">By the end you can read and extend a mapping from a database to the graph, choose between materializing and virtualizing, and say how often a record matcher is wrong.</p>
      ''' + callout("Open these now", "<code>demos/session-05-integration/</code>, starting with its <code>OVERVIEW.md</code> · Docker Desktop · a terminal with <code>demos/.venv</code> active.", "concept") + '''
    </div>
    <div class="lu-card">
      <span class="lu-card__label">How the ~185 minutes are spent</span>
      <ul class="lu-layers">
        <li><span class="lu-layers__name">Lecture · ~115 min</span><span class="lu-layers__note">The problem, R2RML, materialize, virtualize, entity resolution</span></li>
        <li><span class="lu-layers__name">Lab · ~55 min</span><span class="lu-layers__note">Load, map, compare, validate, ask Ontop, match customers, extend a mapping</span></li>
        <li><span class="lu-layers__name">Wrap · ~15 min</span><span class="lu-layers__note">Discussion, project clinic, glossary, self-check</span></li>
      </ul>
    </div>
  </div>''', '''<p>Name the payoff: one small file of rules rebuilds all 135,799 triples of the Brunel graph, identical to Session 2's except for the 7 carriers it now types correctly.</p>''', kind="tint"))

SLIDES.append(divider("Part 1 · The integration problem", "Integration problem",
    "Part 1 of 5 · about 14 minutes",
    "The database changed overnight. Do we rewrite the converter?",
    "No. We describe once how rows become triples, and let a tool do it."))

# ---------------------------------------------------------------- program vs declaration
n = [
    node("csv", "four CSV files", 170, 45, 250, 56, kind="builtin"),
    node("py", "convert_to_rdf.py\n(a program)", 540, 45, 300, 70, kind="builtin"),
    node("g1", "graph", 860, 45, 170, 56, kind="builtin"),
    node("db", "PostgreSQL:\nthe same four tables", 170, 175, 290, 70, kind="builtin"),
    node("map", "brunel-mapping.ttl\n(rules, not code)", 540, 175, 300, 70, kind="builtin"),
    node("g2", "graph", 860, 175, 170, 56, kind="builtin"),
]
e = [edge("a", "csv", "py", ""), edge("b", "py", "g1", ""), edge("c", "db", "map", ""), edge("d", "map", "g2", "")]
steps = [
    {"show": ["csv", "py", "g1", "a", "b"], "run": ["a", "b"], "set": {"py": "active"}},
    {"show": ["db", "map", "g2", "c", "d"], "run": ["c", "d"], "set": {"py": "idle", "map": "active"}},
]
caps = [
    ("Session 2", "<b>Step 1.</b> A Python script read the files once, row by row, and wrote triples. To change what it produces, you change the program."),
    ("Today", "<b>Step 2.</b> The tables are in a database. A <b>mapping</b> says, for each table, which triples a row becomes. A tool reads the mapping and does the work, as often as needed."),
]
walk = flow("A program against a mapping", 1000, 220, n, e, steps, caps, legend=False)
SLIDES.append(slide("A converter is a program; a mapping is a set of rules", "Integration problem", 5, '''  <div class="lu-eyebrow">The idea</div>
  <h2 class="lu-h2">Same tables, same graph. The difference is who does the work.</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + walk + '''
    <div class="lu-stack">
      ''' + defbox([("Mapping", "Rules that turn rows of a table into triples."),
                    ("R2RML", "The W3C language for mappings from relational databases to RDF (2012).")]) + '''
      ''' + callout("Why it matters", "A mapping is a file any R2RML tool can run, and anyone can read. A converter is code only its author knows.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. Sizes are similar (the mapping: 11 triples maps in 155 lines, many of them comments; Session 2's converter: 150 lines of Python). The difference is not length: the mapping says <i>what</i>, and any R2RML tool decides <i>how</i>.</p>'''))

# ---------------------------------------------------------------- two routes
n = [
    node("map", "one mapping", 170, 125, 230, 56, kind="builtin"),
    node("mk", "Morph-KGC", 520, 45, 240, 56, kind="builtin"),
    node("file", "brunel-mapped.nt\n135,799 triples, stored", 950, 45, 380, 70, kind="builtin"),
    node("on", "Ontop", 520, 205, 240, 56, kind="builtin"),
    node("sql", "SPARQL in, SQL to the\ndatabase, answers out", 950, 205, 380, 70, kind="builtin"),
]
e = [edge("a", "map", "mk", "", route="elbow"), edge("b", "mk", "file", "materialize"),
     edge("c", "map", "on", "", route="elbow"), edge("d", "on", "sql", "virtualize")]
steps = [
    {"show": ["map"], "set": {"map": "active"}},
    {"show": ["mk", "file", "a", "b"], "run": ["a", "b"], "set": {"map": "idle", "file": "active"}},
    {"show": ["on", "sql", "c", "d"], "run": ["c", "d"], "set": {"file": "idle", "sql": "active"}},
]
caps = [
    ("One mapping", "<b>Step 1.</b> The same R2RML file serves both routes."),
    ("Materialize", "<b>Step 2.</b> Morph-KGC reads every table now and stores the whole graph in a file. Fast to query, but a snapshot: run it again when the data changes."),
    ("Virtualize", "<b>Step 3.</b> Ontop stores nothing. Each SPARQL question becomes SQL on the live database, so every answer is current."),
]
walk = flow("Two routes from one mapping", 1448, 250, n, e, steps, caps, legend=False)
SLIDES.append(slide("Two routes from one mapping", "Integration problem", 5, '''  <div class="lu-eyebrow">Materialize or virtualize</div>
  <h2 class="lu-h2">Store the graph, or translate every question. One mapping does both.</h2>
  ''' + walk + '''
  <div class="lu-split">
    ''' + defbox([("Materialization", "Converting the data to triples once and storing them.")]) + '''
    ''' + defbox([("Virtualization", "Leaving the data in its database and translating each SPARQL query into SQL.")], label="Also defined here") + '''
  </div>''', '''<p>Five minutes. Parts 3 and 4 take one route each; Part 4 ends with when to choose which.</p>'''))

SLIDES.append(slide("Check: which route?", "Integration problem", 3, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-mcq" data-qid="s5-q1" data-answer="b" data-label="Which route gives always-current answers"
       data-fb-correct=" Ontop asks the live database for every question, so nothing can be out of date."
       data-fb-wrong=" Ask where the answer comes from at the moment the question is asked.">
    <p class="lu-mcq__q">Orders change every minute. A dashboard must always show the current number of late orders per carrier. Which route?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">Materialize once a day with Morph-KGC<span class="lu-mcq__why" hidden>Up to a day out of date.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">Virtualize with Ontop<span class="lu-mcq__why" hidden>Right: each query runs as SQL on the live tables.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">Rerun Session 2's converter<span class="lu-mcq__why" hidden>Still a snapshot, and a program to maintain.</span></button>
    </div>
  </div>''', '''<p>Three minutes. The honest counterpoint comes in Part 4: SHACL needs a graph to check, so a team that validates every change materializes too.</p>''', kind="tint"))
