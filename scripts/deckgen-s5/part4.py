"""Session 5, Part 4: virtualize with Ontop, and when to choose which route.

The answers are Session 2's own run of the same query (its
reference-outputs/query-timings-oxigraph.txt); the SQL shown is written by
hand and labelled so: the lab prints the SQL Ontop itself writes.
"""
from common import slide, divider, defbox, callout, code
from kit import flow, node, edge, head, table

SLIDES = []
K, S, V, E = '<span class="tok-kw">', '<span class="tok-str">', '<span class="tok-var">', '</span>'

SLIDES.append(divider("Part 4 · Virtualize", "Virtualize",
    "Part 4 of 5 · about 15 minutes",
    "Can we ask SPARQL questions of a database that has no graph at all?",
    "Yes: translate each question into SQL, on the fly."))

n = [
    node("q", "SPARQL: orders and late\norders per carrier", 190, 55, 340, 70, kind="builtin"),
    node("o", "Ontop reads\nbrunel-mapping.ttl", 620, 55, 320, 70, kind="builtin"),
    node("s", "SQL on the orders table", 1070, 55, 380, 56, kind="builtin"),
    node("db", "PostgreSQL: rows", 1070, 185, 300, 56, kind="builtin"),
    node("a", "answers, as if from a graph", 620, 185, 400, 56, kind="builtin"),
]
e = [edge("x", "q", "o", ""), edge("y", "o", "s", "rewrite"), edge("z", "s", "db", "run"), edge("w", "db", "a", "rows to answers")]
steps = [
    {"show": ["q"], "set": {"q": "active"}},
    {"show": ["o", "x"], "run": ["x"], "set": {"q": "idle", "o": "active"}},
    {"show": ["s", "y"], "run": ["y"], "set": {"o": "idle", "s": "active"}},
    {"show": ["db", "z", "a", "w"], "run": ["z", "w"], "set": {"s": "idle", "a": "active"}},
]
caps = [
    ("A SPARQL question", "<b>Step 1.</b> Session 2's Q2, unchanged: orders and late orders per carrier."),
    ("The mapping, read backwards", "<b>Step 2.</b> Ontop finds which triples map produces <code>ul:carriedBy</code> and <code>ul:lateDays</code>: columns <code>carrier</code> and <code>ship_late_day_count</code> of <code>orders</code>."),
    ("SQL", "<b>Step 3.</b> It writes one SQL query that groups the orders table by carrier."),
    ("Answers", "<b>Step 4.</b> PostgreSQL returns rows; Ontop turns them back into SPARQL answers. No triple was ever stored."),
]
walk = flow("How Ontop answers", 1448, 230, n, e, steps, caps, legend=False)
SLIDES.append(slide("Ontop: SPARQL in, SQL out", "Virtualize", 5, '''  <div class="lu-eyebrow">Walkthrough</div>
  <h2 class="lu-h2">The same mapping, used the other way round</h2>
  ''' + walk + '''
  ''' + defbox([("Ontop", "The open source engine that answers SPARQL over a relational database, through a mapping."),
                ("OBDA", "Ontology based data access: querying a database through an ontology, by virtualization.")]),
    '''<p>Five minutes. Ontop 5.5.0 (February 2026) reads R2RML directly; in the lab <code>ontop/run_ontop.py</code> prints the SQL it generated.</p>
<ul><li>Ontop does not support <code>*</code> and <code>+</code> property paths; it uses the vocabulary instead (<code>-t vocabulary.ttl</code>), so <code>?o a ul:Order</code> also finds the late orders, without storing that inference.</li></ul>'''))

sp = (f'''{K}SELECT{E} {V}?carrier{E} ({K}COUNT{E}({V}?order{E}) {K}AS{E} {V}?orders{E})
  ({K}SUM{E}({K}IF{E}({V}?late{E} &gt; 0, 1, 0)) {K}AS{E} {V}?lateOrders{E})
{K}WHERE{E} {{ {V}?order{E} ul:carriedBy {V}?carrier{E} ;
               ul:lateDays {V}?late{E} . }}
{K}GROUP BY{E} {V}?carrier{E}''')
sq = (f'''{K}SELECT{E} carrier, {K}COUNT{E}(*) {K}AS{E} orders,
  {K}SUM{E}({K}CASE WHEN{E} ship_late_day_count &gt; 0
      {K}THEN{E} 1 {K}ELSE{E} 0 {K}END{E}) {K}AS{E} late_orders
{K}FROM{E} orders {K}GROUP BY{E} carrier''')
rows = [("V444_0", "6,264", "183"), ("V444_1", "2,097", "9"), ("V44_3", "854", "0")]
SLIDES.append(slide("The same question, two languages", "Virtualize", 4, '''  <div class="lu-eyebrow">What Ontop has to produce</div>
  <h2 class="lu-h2">A SPARQL question about triples becomes an SQL question about rows</h2>
  <div class="lu-split">
    <div class="lu-stack">
      ''' + code("SPARQL · Session 2's Q2", sp) + '''
      ''' + code("SQL · the same question, written by hand", sq) + '''
    </div>
    <div class="lu-stack">
      ''' + table(["Carrier", "Orders", "Late"], rows) + '''
      <p class="lu-caption">The answer both must give: Session 2's run of Q2 on its graph.</p>
      ''' + callout("In the lab", "<code>ontop/run_ontop.py</code> prints the SQL Ontop really wrote. Compare it with this one: longer, but the same question.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. The hand-written SQL is ours, labelled as such; the generated SQL is recorded in <code>reference-outputs/ontop-q2.txt</code> once the run on the instructor's machine is done.</p>'''))

rows = [
    ("Answers are current", "no: a snapshot, until the next run", "yes: every query asks the live tables"),
    ("Query speed", "fast: the graph is stored", "depends on the database and the SQL"),
    ("SHACL validation", "yes: the shapes need a graph to read", "no: nothing is stored to check"),
    ("Space", "a second copy of the data", "nothing extra"),
    ("Changes to the mapping", "run it again", "effective at the next query"),
]
SLIDES.append(slide("Materialize or virtualize?", "Virtualize", 5,
    head("Choosing a route", "Neither wins: each gives up something the other keeps") +
    table(["", "Materialize · Morph-KGC", "Virtualize · Ontop"], rows) + '''
  ''' + callout("A common answer", "Virtualize for live questions, and materialize on a schedule for validation and for Session 6's learning, from the same mapping.", "concept"),
    '''<p>Five minutes. Tie it to Part C question 1 and the project clinic: every team names its route and why.</p>'''))
