"""Session 2, Part 5 (RDF against the property graph), the lab, and the wrap. About 85 minutes, 60 of them lab."""
from kit import slide, divider, head, defbox, defnote, callout, table, figure, flow, node, edge
from part_a import code

SLIDES = []

SLIDES.append(divider("Part 5 · RDF against the property graph", "Graph models",
    "Part 5 of 5 · about 10 minutes",
    "Neo4j is the most used graph database. Why does this course use RDF?",
    "The same orders, loaded into both. The difference shows up in one question."))

SLIDES.append(slide("The same order in Neo4j", "Graph models", 4,
    head("The property graph", "In Neo4j, nodes have labels and key value properties, and edges have types.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s2)">
    ''' + figure("../assets/img/s2-neo4j-browser.png", "Neo4j Browser showing order 1447296446.7 linked to PLANT16, PORT09 and carrier V44_3",
                 "Real run: Neo4j 5.26 Community, Neo4j Browser, loaded by neo4j_comparison.py.") + '''
    <div class="lu-stack">
      ''' + code("Cypher, Neo4j's query language", "MATCH (o:Order {id: '1447296446.7'})\n      -[r]->(n)\nRETURN o, r, n") + '''
      ''' + defnote([
          ("Property graph", "nodes and edges that carry labels and properties, as in Neo4j."),
          ("Cypher", "the query language of Neo4j: patterns drawn with brackets and arrows."),
      ]) + '''
    </div>
  </div>''',
    '''<p>Four minutes. This is also the one slide for the Neo4j tool: the Browser is at localhost:7474 in the lab. Same four things and three links as the RDF picture in Part 1.</p>'''))

SLIDES.append(slide("What each model gives up", "Graph models", 3,
    head("One question shows the difference", "How many orders are there, counting late orders as orders?") + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    <div class="lu-stack">
      ''' + code("SPARQL · the hierarchy is data", "?o a/rdfs:subClassOf* ul:Order") + '''
      <p class="lu-sub">Answer <b>9,215</b>. The fact that a late order is an order lives in the graph, once, for every query.</p>
    </div>
    <div class="lu-stack">
      ''' + code("Cypher · the hierarchy is in each query", "MATCH (o:Order) ...                  // 9,023\nMATCH (o) WHERE o:Order OR o:LateOrder  // 9,215") + '''
      <p class="lu-sub">A label is a string. Neo4j has no subclass, so every query must list the kinds itself.</p>
    </div>
  </div>
  ''' + table(["RDF gives you", "The property graph gives you"], [
      ["Global names: graphs from two companies merge without a meeting", "Properties on edges without extra ceremony"],
      ["A schema you can query and reason over (RDFS, OWL, SHACL)", "A friendlier query language, and wide industry use"],
    ]),
    '''<p>Three minutes. Real counts from neo4j_comparison.py. Be fair: Neo4j is excellent and common in industry. We use RDF because the next three sessions need a schema a machine can reason over, and the concepts carry over to property graphs, not the other way.</p>'''))

SLIDES.append(slide("Poll: which model for this job?", "Graph models", 2, '''  <div class="lu-eyebrow">Room poll · 45 seconds</div>
  <div class="lu-poll" data-qid="s2-poll" data-seconds="45" data-answer="b" data-label="Which graph model fits a traceability graph shared by three companies?">
    <p class="lu-mcq__q">Three companies want one traceability graph: parts, plants, shipments, each company adding its own data. Which model fits better?</p>
    <div class="lu-mcq__opts" style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr))">
      <button class="lu-mcq__opt" type="button" data-key="a">A property graph, for its simpler queries<span class="lu-mcq__why" hidden>Simpler for one team; three companies would still need to agree every label by hand.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">RDF, for its global names<span class="lu-mcq__why" hidden>Correct. IRIs let each company add triples without renaming anyone else's things.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">Three relational databases and nightly exports<span class="lu-mcq__why" hidden>That is today's problem, not a solution to it.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="d">It makes no difference<span class="lu-mcq__why" hidden>For one team, maybe. Across companies, naming is the whole problem.</span></button>
    </div>
  </div>''', '''<p>Two minutes. Ask one person who chose a to defend it; the defence is reasonable for a single team.</p>''', kind="tint"))

# ================================================================== Lab
SLIDES.append(divider("Lab · Build the first graph", "Lab",
    "Hands-on lab · about 60 minutes",
    "Lab: turn Brunel into a graph, load it, and answer seven questions with timings.",
    "Convert with rdflib, load into Fuseki, query, then compare with Neo4j. Each student on their own machine.",
    notes="<p>Ten seconds. The lab clock starts on the next slide.</p>"))

SLIDES.append(slide("Lab brief", "Lab", 3,
    head("Hands-on lab · 60 minutes", "Tables to triples, triples to answers.", "h1", 34) + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <ol class="lu-list lu-list--num">
      <li><b>Build and query.</b> <code>docker compose up -d</code>, then <code>convert_to_rdf.py</code>, <code>load_fuseki.py</code>, <code>run_queries.py</code>, <code>neo4j_comparison.py</code>.</li>
      <li><b>Write your own.</b> Three questions in <code>my_queries.sparql</code>; <code>check_my_queries.py</code> says right or not yet.</li>
      <li><b>Think about names.</b> Test the course IRI scheme, then sketch one for your project's own data.</li>
    </ol>
    <div class="lu-stack">
      ''' + callout("Nothing to hand in", "The lab is for understanding. The README says what to expect at each step and what to take to your project.", "concept") + '''
      ''' + callout("If Docker fails", "Do not debug in the room: <code>python run_queries.py oxigraph</code> runs everything inside Python.") + '''
    </div>
  </div>''',
    '''<p>Three minutes, then walk the room. Folder: <code>demos/session-02-rdf-sparql/</code>; its README has the steps, the expected answers and the questions to think about. Not graded: say so.</p>
    <ul><li>Most common blocker: Docker Desktop not running. Second: port 3030 or 7474 already in use.</li></ul>'''))

SLIDES.append(slide("The tool: the Fuseki query page", "Lab", 2,
    head("One slide for the tool", "<b>Apache Jena Fuseki</b> stores the graph (TDB2) and answers SPARQL over the web.") + '''
  ''' + figure("../assets/img/s2-fuseki-query.png", "Fuseki query page with Q2 and its three result rows",
                 "Real run: Fuseki 5.5, dataset kr, Q2, 3 results in 0.061 seconds.") + '''
  <p class="lu-sub">Open <b>localhost:3030</b>, dataset <b>kr</b>, tab <b>query</b>. Paste a query from <code>queries.sparql</code>, press the run arrow, read the table.</p>''',
    '''<p>Two minutes. rdflib and Docker get no slide: a Python library and a common tool, both in the README.</p>'''))

SLIDES.append(slide("Lab time", "Lab", 55,
    head("Lab · 55 minutes", "Each student on their own machine. Checkpoints keep you on time.") + '''
  <div class="lu-grid" style="margin-top:var(--lu-s3)">
    <div class="lu-card lu-col-4"><span class="lu-card__label">By minute 25</span><p class="lu-sub">Graph loaded (135,841 triples), seven questions run, Neo4j compared.</p></div>
    <div class="lu-card lu-col-4"><span class="lu-card__label">By minute 45</span><p class="lu-sub">Your own three queries checked. Stuck? Try them in the Fuseki page first.</p></div>
    <div class="lu-card lu-col-4"><span class="lu-card__label">By minute 55</span><p class="lu-sub">IRI scheme sketched for your own project data, ready for the discussion.</p></div>
  </div>
  ''' + callout("For your team project", "Sketch the IRI scheme for your own database now. The discussion next tests it against a second source.", "neutral"),
    '''<p>Fifty five minutes. At minute 25, anyone without a loaded graph switches to <code>run_queries.py oxigraph</code>. At minute 45, ask two students to read out their answer to the third question; the usual wrong one is 44 (no DISTINCT).</p>''', kind="tint"))

# ================================================================== Wrap
SLIDES.append(slide("Discussion: test the IRI convention", "Wrap", 8,
    head("Discussion · as a room", "Which IRI schemes break when a second source arrives?") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <ol class="lu-list lu-list--num">
      <li>Three volunteers show the scheme they sketched for their project data.</li>
      <li>The room attacks each one: a second source, a renamed supplier, two merged companies.</li>
      <li>Compare each with the course convention in <code>common/iri.py</code>.</li>
    </ol>
    ''' + callout("Outcome", "Each team leaves with a naming scheme for its own data that survives a second source. The course keeps <code>common/iri.py</code>; Session 5 depends on it.", "concept") + '''
  </div>''',
    '''<p>Eight minutes. The usual weak spot: a scheme that puts a name or a country in the IRI. Ask what happens the day the supplier renames itself.</p>'''))

GLOSS = [
    ("RDF", "A graph written as three part statements."),
    ("Triple", "Subject, predicate, object: one edge."),
    ("IRI", "A globally unique name for a thing."),
    ("Literal · datatype", "A plain value; its kind (integer, date)."),
    ("Blank node", "A node with no global name."),
    ("Named graph", "Triples with a name, to track their source."),
    ("Turtle, N-Triples, JSON-LD", "Three ways to write the same triples."),
    ("RDFS", "Classes, subclasses, domain, range."),
    ("Entailment", "A fact that follows, though nobody wrote it."),
    ("SPARQL", "The query language for RDF graphs."),
    ("Property path", "Follow links in sequence or any number of times."),
    ("Property graph", "Labelled nodes and edges with properties."),
]
half = (len(GLOSS) + 1) // 2
SLIDES.append(slide("Glossary for this session", "Wrap", 1,
    head("Glossary", "The words this session introduced.") +
    '<div class="lu-split" style="margin-top:var(--lu-s2)">' +
    "".join('<dl class="lu-defs">' + "".join(f"<dt>{t}</dt><dd>{d}</dd>" for t, d in part) + "</dl>"
            for part in (GLOSS[:half], GLOSS[half:])) + '</div>',
    '''<p>One minute, or skip in class: it is for revision.</p>'''))

SLIDES.append(slide("Wrap and next session", "Wrap", 2, '''  <div class="lu-eyebrow">Wrap</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">One sentence to leave with.</h2>
      <p class="lu-statement">In a graph, joining is not something you run. It is what happens when two facts use the same name.</p>
      ''' + callout("Before Session 3", "Read Hogan et al., Chapters 2 and 3, and the RDF and SPARQL chapters of Allemang, Hendler and Gandon. Install Protégé 5.6 and watch the first videos of the Protégé series linked in the Session 3 lab README.") + '''
    </div>
    <div class="lu-stack">
      <div class="lu-card">
        <span class="lu-card__label">Next session</span>
        <h3 class="lu-h3">Session 3 · Ontology engineering: description logic, OWL, and reuse</h3>
        <p class="lu-sub">Say what an order <i>is</i>, precisely enough that a reasoner finds a real mistake in our own model.</p>
      </div>
      <div class="lu-row"><span class="lu-tag lu-tag--green">For your team</span><span class="lu-caption" style="flex:1">Share your IRI sketch with your team and agree one scheme for your project.</span></div>
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
