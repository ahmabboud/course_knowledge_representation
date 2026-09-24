"""Session 2, opening and Part 1 (from a table row to triples). About 38 minutes.

Numbers come from demos/session-02-rdf-sparql/reference-outputs/ and sample/.
"""
import html
from kit import slide, divider, head, defbox, defnote, callout, table, flow, node, edge

SLIDES = []


def code(name, text, build=None):
    b = f' data-build="{build}"' if build else ""
    return (f'<div class="lu-code lu-code--sm" data-name="{html.escape(name)}"{b}>'
            f'<pre><code>{html.escape(text)}</code></pre></div>')


# ------------------------------------------------------------------ Title
SLIDES.append('''<section class="slide slide--night" data-chrome="none" data-label="Title" data-section="Opening" data-minutes="1">
  <div class="slide__body" style="justify-content:space-between">
    <div class="lu-row" style="justify-content:space-between;align-items:flex-start">
      <div class="lu-lockup">
        <span class="lu-lockup__mark">LU</span>
        <span class="lu-lockup__text">
          <span class="lu-lockup__name">Lebanese University</span>
          <span class="lu-lockup__unit">Faculty of Sciences · MSc Computer Science</span>
        </span>
      </div>
      <div class="lu-tag lu-tag--red" style="background:transparent;color:#FF9AA7;border-color:#96122B">Module 1 · Representation and integration</div>
    </div>
    <div class="lu-stack">
      <div class="lu-eyebrow">Knowledge Representation · Session 2 of 8</div>
      <h1 class="lu-display" style="max-width:24ch">RDF, SPARQL, and the Graph as a Data Model</h1>
      <p class="lu-lead" style="max-width:46ch">Last week you measured Brunel's tables. Today they become a graph of 135,841 statements, and you ask it questions that follow links.</p>
    </div>
    <div class="lu-row" style="justify-content:space-between;font-size:var(--lu-t-caption);color:var(--lu-on-night-2)">
      <span>About 180 minutes · about 105 of lecture, 60 of lab, 15 of discussion</span>
      <span>Press <kbd>&rarr;</kbd> to begin · <kbd>?</kbd> for shortcuts</span>
    </div>
  </div>
  <template data-notes>
    <p>Rebuilt on 2026-09-24 to the course standard (AGENTS.md 2c). Every number and every code sample is real output of the lab scripts in <code>demos/session-02-rdf-sparql/</code>, recorded in its <code>reference-outputs/</code> and <code>sample/</code> folders.</p>
    <ul>
      <li>Before minute one: <code>docker compose up -d</code> from <code>demos/</code> on every laptop. Fuseki and Neo4j take a minute to start.</li>
      <li>Teams and topics were due before today. Collect any missing ones at the break.</li>
    </ul>
  </template>
</section>
''')

# ------------------------------------------------------------------ Where we are
w_nodes = [
    node("src", "Sources\nSession 1", 130, 70, 210, 80),
    node("prof", "Profiling\nSession 1", 400, 70, 210, 80),
    node("graph", "Graph\nToday", 670, 70, 210, 80),
    node("ont", "Ontology\nSession 3", 940, 70, 210, 80),
    node("shp", "Shapes\nSession 4", 1210, 70, 210, 80),
]
w_edges = [edge("a", "src", "prof"), edge("b", "prof", "graph"), edge("c", "graph", "ont"), edge("d", "ont", "shp")]
w_steps = [{"show": [n["id"] for n in w_nodes] + [e["id"] for e in w_edges], "run": ["b"], "set": {"graph": "active"}}]
SLIDES.append(slide("Where we are in the architecture", "Opening", 3,
    head("Recap", "Session 1 measured the data and wrote rules. Today the data becomes a graph.") +
    flow("Where Session 2 sits", 1448, 140, w_nodes, w_edges, w_steps) + '''
  <div class="lu-split" style="margin-top:var(--lu-s4)">
    ''' + callout("What you have", "Brunel's seven tables, profiled, and a constraint inventory. For example: a plant ships only through ports it is linked to, 0 exceptions in 9,215 orders.", "neutral") + '''
    ''' + callout("What is missing", "The tables still do not join to anything outside themselves, and the rules live in a spreadsheet. A graph gives every thing a name the whole world can point at.") + '''
  </div>''',
    '''<p>Three minutes. Point at the ring on "Graph": this session's stage. Remind them the plant and port rule from last week comes back today as a one line question.</p>'''))

# ------------------------------------------------------------------ Objective
SLIDES.append(slide("Today: objective and time plan", "Opening", 2, '''  <div class="lu-eyebrow">Objective</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <p class="lu-statement">By the end you can turn a table into triples, design names that survive a second source, and ask a graph questions that follow links.</p>
      ''' + callout("What you leave with", "A graph of Brunel you can query, three queries you wrote yourself, and a naming scheme sketched for your own project. Nothing to hand in.", "concept") + '''
    </div>
    ''' + table(["Part", "Minutes"], [
        ["1 · From a table row to triples", "30"], ["2 · Naming things: IRI design", "8"],
        ["3 · RDFS, the first meaning", "12"], ["4 · Asking questions: SPARQL", "34"],
        ["5 · RDF against the property graph", "10"], ["Lab", "60"], ["Discussion and wrap", "15"]],
        "About 180 minutes in all.") + '''
  </div>''',
    '''<p>Two minutes. Say it plainly: the lab is not graded; it is where the concepts become real and where the team project starts. One query in the set is slow on purpose.</p>''', kind="tint"))

# ================================================================== Part 1
SLIDES.append(divider("Part 1 · From a table row to triples", "The data model",
    "Part 1 of 5 · about 30 minutes",
    "A table stores rows. A graph stores statements. What is the difference, and why pay for it?",
    "One real Brunel order, taken apart into statements, one step at a time."))

# ------------------------------------------------------------------ Why a graph
y_nodes = [
    node("row", "OrderList row\nOrder ID · Plant Code · Origin Port ·\nCarrier · Customer · Weight ...", 250, 180, 440, 130),
    node("o", "Order\n1447296446.7", 900, 180, 250, 90),
    node("pl", "PLANT16", 1250, 50, 190, 64),
    node("po", "PORT09", 1300, 180, 190, 64),
    node("ca", "V44_3", 1250, 310, 190, 64),
]
y_edges = [
    edge("t", "row", "o", "same facts"),
    edge("a", "o", "pl", "fromPlant"), edge("b", "o", "po", "shipsFrom"), edge("c", "o", "ca", "carriedBy"),
    edge("d", "pl", "po", "servesPort", kind="inferred", route="elbow", sides=["right", "right"]),
]
y_steps = [
    {"show": ["row"], "set": {"row": "active"}},
    {"show": ["o", "t", "pl", "po", "ca", "a", "b", "c"], "run": ["t", "a", "b", "c"], "set": {"row": "idle", "o": "active"}},
    {"show": ["d"], "run": ["d"], "set": {"o": "idle", "pl": "active"}},
]
y_caps = [
    ("A row", "<b>Step 1.</b> In a table, an order is one row. Its links to plants and ports are codes in columns, matched only when someone writes a JOIN."),
    ("Things and links", "<b>Step 2.</b> In a graph, the order, the plant, the port and the carrier are each a thing, and each link has a name."),
    ("Links from another table", "<b>Step 3.</b> A link that came from another table, PlantPorts, attaches to the same plant. No JOIN was written: the shared name did it."),
]
SLIDES.append(slide("Why a graph", "The data model", 3,
    head("The problem", "Session 1's question follows links: plant, port, carrier, customer. Tables hide links in columns.") +
    flow("The same order as a row and as a graph", 1448, 370, y_nodes, y_edges, y_steps, y_caps,
         flags={"inferred": "joined"}),
    '''<p>Three minutes. The idea to land: in a graph, joining is not an operation you run, it is a consequence of using the same name.</p>
    <ul><li>The dashed arrow is amber because it came from another table, not because anything was inferred. Say so if asked.</li></ul>'''))

# ------------------------------------------------------------------ The triple
t_nodes = [
    node("s", "order 1447296446.7", 250, 110, 360, 80),
    node("o", "plant PLANT16", 1150, 110, 330, 80),
]
t_edges = [edge("p", "s", "o", "ul:fromPlant")]
t_steps = [
    {"show": ["s"], "set": {"s": "active"}},
    {"show": ["p"], "run": ["p"], "set": {"s": "idle"}},
    {"show": ["o"], "set": {"o": "active"}},
]
t_caps = [
    ("Subject", "<b>Subject</b>: the thing the statement is about. Here, one real Brunel order."),
    ("Predicate", "<b>Predicate</b>: the named relationship. It is the label on the arrow."),
    ("Object", "<b>Object</b>: what the relationship points to: another thing, or a plain value."),
]
SLIDES.append(slide("The triple", "The data model", 4,
    head("The smallest unit", "Every fact in RDF has the same three parts. One fact is one <b>triple</b>.") +
    flow("One real triple from brunel.ttl", 1448, 220, t_nodes, t_edges, t_steps, t_caps) + '''
  <div class="lu-split" style="margin-top:var(--lu-s2)">
    ''' + code("the same triple, as written in brunel.ttl (N-Triples)",
               "<https://ul.edu.lb/kr/id/order/brunel/1447296446.7>\n  <https://ul.edu.lb/kr/scm#fromPlant>\n  <https://ul.edu.lb/kr/id/plant/brunel/PLANT16> .") + '''
    ''' + defnote([
        ("RDF", "Resource Description Framework: a graph written as a list of three part statements."),
        ("Triple", "one statement: subject, predicate, object. One edge of the graph."),
    ]) + '''
  </div>''',
    '''<p>Four minutes. Our whole Brunel graph is 135,841 of these, and nothing else. Tables, columns and keys are gone; only statements remain.</p>'''))

# ------------------------------------------------------------------ IRI, namespace, prefix
i_nodes = [
    node("ns", "https://ul.edu.lb/kr/id/", 260, 80, 420, 70, kind="literal"),
    node("ty", "order/", 620, 80, 180, 70, kind="literal"),
    node("src", "brunel/", 860, 80, 190, 70, kind="literal"),
    node("key", "1447296446.7", 1150, 80, 300, 70, kind="literal"),
]
i_edges = [edge("a", "ns", "ty"), edge("b", "ty", "src"), edge("c", "src", "key")]
i_steps = [
    {"show": ["ns"], "set": {"ns": "active"}},
    {"show": ["ty", "a"], "set": {"ns": "idle", "ty": "active"}},
    {"show": ["src", "b"], "set": {"ty": "idle", "src": "active"}},
    {"show": ["key", "c"], "set": {"src": "idle", "key": "active"}},
]
i_caps = [
    ("Namespace", "<b>Namespace</b>: the shared first part. Every thing we mint starts with it."),
    ("What kind", "The kind of thing: order, plant, port, carrier."),
    ("Which system", "The system that gave us the key. A second source gets its own space."),
    ("The source key", "The key exactly as the source wrote it, decimal point included. Never a row number."),
]
SLIDES.append(slide("IRIs, namespaces and prefixes", "The data model", 4,
    head("Names for things", "Every thing gets a globally unique name, an <b>IRI</b>, built from parts you choose.") +
    flow("The parts of one real IRI", 1448, 160, i_nodes, i_edges, i_steps, i_caps) + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    ''' + code("a prefix is a nickname for a namespace",
               "@prefix ul:    <https://ul.edu.lb/kr/scm#> .\n@prefix order: <https://ul.edu.lb/kr/id/order/brunel/> .\n\norder:1447296446.7  ul:fromPlant  plant:PLANT16 .") + '''
    ''' + defnote([
        ("IRI", "Internationalised Resource Identifier: a globally unique name, written like a web address."),
        ("Namespace", "the shared first part of a group of IRIs."),
        ("Prefix", "a short nickname for a namespace, such as <code>ul:</code>."),
    ]) + '''
  </div>''',
    '''<p>Four minutes. Two namespaces on purpose: <code>ul:</code> (ending in #) for the words, classes and properties; <code>https://ul.edu.lb/kr/id/</code> (ending in /) for the things. Part 2 argues why.</p>'''))

# ------------------------------------------------------------------ Literals and datatypes
SLIDES.append(slide("Literals and datatypes", "The data model", 3,
    head("Plain values", "Not everything is a thing. A weight or a date is a <b>literal</b>, and it has a <b>datatype</b>.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    ''' + table(["Brunel column", "Value in brunel.ttl", "Datatype"], [
        ["Order Date", '"2013-05-26"', "xsd:date"],
        ["Unit quantity", "808", "xsd:integer"],
        ["Weight", "14.3", "xsd:decimal"],
        ["Service Level", '"CRF"', "plain text"],
        ["Order ID", '"1447296446.7"', "plain text, on purpose"],
      ], "Real values of order 1447296446.7.", cls="lu-table lu-table--mono") + '''
    <div class="lu-stack">
      ''' + defnote([
        ("Literal", "a plain value in a triple: a number, a date, a piece of text."),
        ("Datatype", "the kind of a literal, such as integer or date."),
      ]) + '''
      ''' + callout("Why the ID is text", "Read as a number, 1447296446.7 is a decimal to be rounded and summed. It is a name. Text keeps it exact.", build="1") + '''
    </div>
  </div>''',
    '''<p>Three minutes. The datatype decides what comparisons mean: 14.3 as a decimal sorts after 9.5; as text it sorts before. Q6 later compares weights, so this matters.</p>'''))

# ------------------------------------------------------------------ One row to triples, step by step
r_nodes = [
    node("o", "order\n1447296446.7", 260, 205, 280, 96),
    node("ty", "ul:Order", 720, 40, 220, 56),
    node("pl", "plant PLANT16", 720, 125, 260, 56),
    node("po", "port PORT09", 720, 210, 260, 56),
    node("ca", "carrier V44_3", 720, 295, 260, 56),
    node("cu", "customer V55555_53", 720, 380, 300, 56),
    node("dt", '"2013-05-26"', 1200, 60, 260, 56, kind="literal"),
    node("wt", "14.3", 1200, 150, 260, 56, kind="literal"),
    node("qt", "808", 1200, 240, 260, 56, kind="literal"),
    node("sv", '"CRF"', 1200, 330, 260, 56, kind="literal"),
]
r_edges = [
    edge("e1", "o", "ty", "a"), edge("e2", "o", "pl"), edge("e3", "o", "po"), edge("e4", "o", "ca"), edge("e5", "o", "cu"),
    edge("e6", "o", "dt", route="elbow", sides=["top", "left"]),
    edge("e7", "o", "wt", route="elbow", sides=["top", "left"]),
    edge("e8", "o", "qt", route="elbow", sides=["bottom", "left"]),
    edge("e9", "o", "sv", route="elbow", sides=["bottom", "left"]),
]
r_steps = [
    {"show": ["o"], "set": {"o": "active"}},
    {"show": ["ty", "e1"], "run": ["e1"]},
    {"show": ["pl", "po", "ca", "cu", "e2", "e3", "e4", "e5"], "run": ["e2", "e3", "e4", "e5"], "set": {"o": "idle"}},
    {"show": ["dt", "wt", "qt", "sv", "e6", "e7", "e8", "e9"], "run": ["e6", "e7", "e8", "e9"]},
]
r_caps = [
    ("Mint one IRI", "<b>Step 1.</b> Mint one IRI for the order, from its source key."),
    ("Say what it is", "<b>Step 2.</b> One triple says what it is: <code>a ul:Order</code>. (<code>a</code> is short for <code>rdf:type</code>.)"),
    ("Codes become links", "<b>Step 3.</b> Each code column becomes a link to a thing with its own IRI: plant, port, carrier, customer."),
    ("Values stay values", "<b>Step 4.</b> Dates, weights, quantities and codes stay literals. In all, this one row gives <b>13 triples</b>."),
]
SLIDES.append(slide("One real row, converted step by step", "The data model", 5,
    head("Worked example", "The first row of OrderList becomes 13 triples. This is what <code>convert_to_rdf.py</code> does 9,215 times.") +
    flow("Order 1447296446.7 as triples", 1448, 420, r_nodes, r_edges, r_steps, r_caps),
    '''<p>Five minutes. Step slowly; this is the lab's conversion, drawn. Not every column is shown: the file has 13 triples for this order, including the destination port and product.</p>
    <ul><li>The conversion for the whole file, 135,841 triples, takes about 20 seconds with rdflib.</li></ul>'''))

# ------------------------------------------------------------------ Foreign key becomes an edge
k_nodes = [
    node("ol", "OrderList\nPlant Code = PLANT16", 230, 80, 380, 90),
    node("pp", "PlantPorts\nPlant Code = PLANT16", 230, 290, 380, 90),
    node("pl", "plant PLANT16\none IRI", 760, 185, 300, 96),
    node("o", "173 orders", 1200, 80, 260, 70),
    node("po", "port PORT09", 1200, 290, 260, 70),
]
k_edges = [
    edge("a", "ol", "pl", "mint"), edge("b", "pp", "pl", "mint"),
    edge("c", "o", "pl", "fromPlant"), edge("d", "pl", "po", "servesPort"),
]
k_steps = [
    {"show": ["ol", "pp"]},
    {"show": ["pl", "a", "b"], "run": ["a", "b"], "set": {"pl": "active"}},
    {"show": ["o", "po", "c", "d"], "run": ["c", "d"]},
]
k_caps = [
    ("Two tables, one code", "<b>Step 1.</b> Two tables both mention PLANT16. In SQL, a JOIN on Plant Code connects them at query time."),
    ("One name", "<b>Step 2.</b> The conversion mints the same IRI from both. The foreign key has become a shared name."),
    ("Already joined", "<b>Step 3.</b> 173 orders now reach PORT09 through the plant, with no JOIN in any query."),
]
SLIDES.append(slide("A foreign key becomes an edge", "The data model", 3,
    head("Joining by naming", "Two tables that share a code share a node. The graph is already joined.") +
    flow("How PlantPorts and OrderList meet at one IRI", 1448, 370, k_nodes, k_edges, k_steps, k_caps),
    '''<p>Three minutes. 173 is real: the orders from PLANT16 in OrderList. The price: if two systems use the same code for different things, a shared IRI merges them wrongly. That is why the source system is part of our IRIs.</p>'''))

# ------------------------------------------------------------------ Blank node
SLIDES.append(slide("Blank nodes: things with no name", "The data model", 3,
    head("When there is no key", "A freight rate band has no ID in the source. It is only its carrier, lane and weight range.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    ''' + code("one real row of FreightRates, as a blank node (Turtle)",
               "[] a ul:RateBand ;\n   ul:bandCarrier carrier:V444_6 ;\n   ul:bandFrom port:PORT08 ; ul:bandTo port:PORT09 ;\n   ul:bandService \"DTD\" ;\n   ul:minWeight 250.0 ; ul:maxWeight 499.99 ;\n   ul:rate 0.7132 .") + '''
    <div class="lu-stack">
      ''' + defnote([("Blank node", "a node with no global name, for something that matters only through its links.")]) + '''
      ''' + callout("In our graph", "1,540 rate bands, all blank nodes, 12,320 triples.", "neutral") + '''
    </div>
  </div>''',
    '''<p>Three minutes. The cost of a blank node: nobody outside can point at it; to say "this band is wrong", it needs an IRI. <code>[]</code> is Turtle's way to write a blank node inline. Ask: should rate bands have IRIs? A good answer: yes, if anything outside will ever refer to one, for example a contract.</p>'''))

# ------------------------------------------------------------------ Named graphs
SLIDES.append(slide("Named graphs: remembering where a triple came from", "The data model", 3,
    head("Provenance", "The same triples, grouped by the table they came from. Each group is a <b>named graph</b>.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    ''' + table(["Named graph in brunel.trig", "Triples"], [
        [".../graph/brunel/OrderList", "119,844"],
        [".../graph/brunel/FreightRates", "12,320"],
        [".../graph/brunel/ProductsPerPlant", "3,576"],
        [".../graph/brunel/PlantPorts", "52"],
        [".../graph/brunel/schema", "49"],
      ], "Real counts, one SPARQL query over brunel.trig (Oxigraph, 38 ms). Total 135,841.", cls="lu-table lu-table--mono") + '''
    <div class="lu-stack">
      ''' + defnote([("Named graph", "a set of triples with its own IRI, used to track where they came from.")]) + '''
      ''' + callout("Why it matters by Session 5", "When two sources disagree, you must know which one said what. The graph name is that record.", "neutral") + '''
    </div>
  </div>''',
    '''<p>Three minutes. The query is <code>SELECT ?g (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g</code>. It returns in 38 ms.</p>'''))

# ------------------------------------------------------------------ Three serializations
SLIDES.append(slide("One graph, three formats", "The data model", 3,
    head("Serializations", "The same triples can be written three ways. Pick by who reads them.") + '''
  <div class="lu-grid" style="margin-top:var(--lu-s2)">
    <div class="lu-col-4">''' + code("Turtle · for people", "order:1447296446.7 a ul:Order ;\n  ul:fromPlant plant:PLANT16 ;\n  ul:weight 14.3 ;\n  ul:serviceLevel \"CRF\" .") + '''<p class="lu-caption">Authoring and reading.</p></div>
    <div class="lu-col-4">''' + code("N-Triples · for bulk", "<.../order/brunel/1447296446.7>\n  <...scm#weight>\n  \"14.3\"^^<...XMLSchema#decimal> .") + '''<p class="lu-caption">One triple per line: split, stream, load.</p></div>
    <div class="lu-col-4">''' + code("JSON-LD · for web APIs", "{ \"@id\": \".../order/brunel/1447296446.7\",\n  \"@type\": \"ul:Order\",\n  \"ul:serviceLevel\": \"CRF\" }") + '''<p class="lu-caption">JSON that is also RDF.</p></div>
  </div>
  ''' + defnote([
        ("Turtle", "a compact, readable text format for triples."),
        ("N-Triples", "one full triple per line, simple to process in bulk."),
        ("JSON-LD", "triples written as JSON, used by web APIs."),
    ]),
    '''<p>Three minutes. The full files are in <code>demos/session-02-rdf-sparql/sample/</code>: order.ttl, order.nt, order.jsonld, all written by rdflib from the same 13 triples. IRIs are shortened with ... here only.</p>'''))
