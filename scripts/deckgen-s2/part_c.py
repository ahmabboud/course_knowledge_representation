"""Session 2, Part 4 (asking questions: SPARQL). About 34 minutes."""
import html
from kit import slide, divider, head, defbox, defnote, callout, table, bar, flow, node, edge
from part_a import code

SLIDES = []

SLIDES.append(divider("Part 4 · Asking questions: SPARQL", "SPARQL",
    "Part 4 of 5 · about 34 minutes",
    "How do you ask a graph a question?",
    "Draw the shape of the answer, with holes in it. Every result on these slides is a real run on our 135,841 triples."))

# ------------------------------------------------------------------ Pattern with holes
p_nodes = [
    node("v", "?order", 200, 60, 240, 76),
    node("c", "carrier V44_3", 760, 60, 300, 76),
    node("r", "854 orders match", 1260, 60, 300, 76),
]
p_edges = [edge("p", "v", "c", "ul:carriedBy"), edge("m", "c", "r", "matches")]
p_steps = [
    {"show": ["v", "c", "p"], "set": {"v": "active"}},
    {"show": ["r", "m"], "run": ["m"], "set": {"v": "idle", "r": "active"}},
]
p_caps = [
    ("A triple with a hole", "<b>Step 1.</b> Write a triple, and put a <b>variable</b> where you do not know the answer: <code>?order</code>."),
    ("Every match", "<b>Step 2.</b> The engine finds every order that fits. Real answer: <b>854</b> orders carried by V44_3."),
]
SLIDES.append(slide("A pattern is a triple with holes", "SPARQL", 4,
    head("The core idea", "A <b>SPARQL</b> query is a picture of the answer, with holes for what you want to know.") +
    flow("One triple pattern and its matches", 1448, 130, p_nodes, p_edges, p_steps, p_caps) + '''
  <div class="lu-split" style="margin-top:var(--lu-s2)">
    ''' + code("Q1 in queries.sparql (the count version)", "PREFIX ul: <https://ul.edu.lb/kr/scm#>\nSELECT (COUNT(*) AS ?n) WHERE {\n  ?order ul:carriedBy carrier:V44_3 .\n}") + '''
    ''' + defnote([
        ("SPARQL", "the query language for RDF graphs."),
        ("Triple pattern", "a triple with some parts replaced by variables."),
        ("Variable", "a placeholder, written ?name, filled by every match."),
    ]) + '''
  </div>''',
    '''<p>Four minutes. The prefix <code>carrier:</code> is shortened on the slide; the file writes the full IRI. Real result on Fuseki: 854, the same number Session 1 found with pandas.</p>'''))

# ------------------------------------------------------------------ Two patterns share a variable
j_nodes = [
    node("c", "?carrier", 230, 70, 240, 70),
    node("o", "?order", 720, 70, 240, 76),
    node("l", "?late", 1210, 70, 240, 70, kind="literal"),
]
j_edges = [edge("a", "o", "c", "ul:carriedBy"), edge("b", "o", "l", "ul:lateDays")]
j_steps = [
    {"show": ["o", "c", "a"], "run": ["a"]},
    {"show": ["l", "b"], "run": ["b"], "set": {"o": "active"}},
]
j_caps = [
    ("First pattern", "<b>Step 1.</b> Pattern one: an order and its carrier."),
    ("Shared variable", "<b>Step 2.</b> Pattern two uses the same <code>?order</code>. The shared variable is the join: both must be true of the same order."),
]
SLIDES.append(slide("Two patterns, one shared variable", "SPARQL", 3,
    head("Joins without JOIN", "Two patterns that share a variable must match the same thing. That is the whole join mechanism.") +
    flow("A two pattern query drawn as a graph", 1448, 150, j_nodes, j_edges, j_steps, j_caps) +
    code("the WHERE part of Q2", "?order ul:carriedBy ?carrier ;\n       ul:lateDays  ?late .      # ; repeats the subject ?order"),
    '''<p>Three minutes. Point at the semicolon: it means "same subject". Students read it as a statement end; it is not.</p>'''))

# ------------------------------------------------------------------ OPTIONAL and FILTER
SLIDES.append(slide("OPTIONAL and FILTER", "SPARQL", 3,
    head("Missing parts and conditions", "OPTIONAL keeps a row even when part of the pattern has no match. FILTER removes rows.") + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    ''' + code("Q3 · does every carrier have a freight rate?", "SELECT ?carrier (COUNT(?band) AS ?bands) WHERE {\n  ?carrier a ul:Carrier .\n  OPTIONAL { ?band ul:bandCarrier ?carrier }\n} GROUP BY ?carrier ORDER BY ?bands") + '''
    <div class="lu-stack">
      ''' + table(["?carrier", "?bands"], [["V44_3", "<b>0</b>"], ["V444_0", "39"], ["V444_1", "292"]], "Real result, Fuseki, 12.5 ms.", cls="lu-table lu-table--mono") + '''
      ''' + callout("Without OPTIONAL", "V44_3 would vanish from the result, and the finding with it. OPTIONAL is how a missing link stays visible.", build="1") + '''
    </div>
  </div>''',
    '''<p>Three minutes. This is Session 1's referential integrity finding, now one query. Remember open world: 0 bands in our graph means "none stated", not "none exist".</p>'''))

# ------------------------------------------------------------------ Aggregation
SLIDES.append(slide("Aggregation: counting and grouping", "SPARQL", 3,
    head("Numbers from the graph", "<code>GROUP BY</code> and <code>COUNT</code> turn matches into a table of totals.") + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    ''' + code("Q2 · orders and late orders per carrier", "SELECT ?carrier (COUNT(?order) AS ?orders)\n       (SUM(IF(?late > 0, 1, 0)) AS ?lateOrders)\nWHERE { ?order ul:carriedBy ?carrier ;\n              ul:lateDays ?late . }\nGROUP BY ?carrier ORDER BY DESC(?orders)") + '''
    <div class="lu-stack">
      ''' + table(["Carrier", "Orders", "Late"], [
          ["V444_0", bar(6264, 6264, "6,264"), "183"],
          ["V444_1", bar(2097, 6264, "2,097"), "9"],
          ["V44_3", bar(854, 6264, "854"), "0"]], "Real result, Fuseki, 47 ms.") + '''
      ''' + defnote([("Aggregation", "combining many matches into one number (a count, a sum, an average), grouped by something.")]) + '''
    </div>
  </div>''',
    '''<p>Three minutes. 183 plus 9 is 192, the late orders from the RDFS slide. Numbers that agree across slides are how students start to trust the graph.</p>'''))

# ------------------------------------------------------------------ Four forms
SLIDES.append(slide("The four query forms", "SPARQL", 3,
    head("Four kinds of answer", "The same pattern language, four shapes of result.") +
    table(["Form", "Returns", "Our real example"], [
        ["<b>SELECT</b>", "A table", "Q2: three carriers with their order counts"],
        ["<b>ASK</b>", "true or false", "Q4: is any order leaving through a port its plant does not serve? <b>false</b>"],
        ["<b>CONSTRUCT</b>", "A new graph", "Q7: carrier serves plant, <b>12</b> new triples built from 9,215 orders"],
        ["<b>DESCRIBE</b>", "Everything about a thing", "Order 1447296446.7: <b>13</b> triples"],
      ], "All four run on Fuseki against the lab graph.") +
    callout("Federation, in one line", "A query can also reach another endpoint with <code>SERVICE &lt;url&gt; { ... }</code>. We do not run it in the lab; know that it exists.", "neutral"),
    '''<p>Three minutes. CONSTRUCT is the one to stress: a query whose answer is more graph. It is how Session 5 builds graphs from other graphs.</p>'''))

# ------------------------------------------------------------------ Property paths
pp_nodes = [
    node("o", "?order", 150, 45, 220, 64),
    node("pl", "plant", 540, 45, 220, 64),
    node("po", "?port", 930, 45, 220, 64),
    node("x", "?anyOrder", 150, 180, 240, 64),
    node("lo", "ul:LateOrder", 540, 180, 250, 64),
    node("or", "ul:Order", 930, 180, 220, 64),
    node("res", "9,023 without\nthe path;\n9,215 with it", 1300, 180, 250, 110),
]
pp_edges = [
    edge("a", "o", "pl", "fromPlant"), edge("b", "pl", "po", "servesPort"),
    edge("c", "x", "lo", "a"), edge("d", "lo", "or", "subClassOf*"), edge("e", "or", "res"),
]
pp_steps = [
    {"show": ["o", "pl", "po", "a", "b"], "run": ["a", "b"], "set": {"po": "active"}},
    {"show": ["x", "lo", "or", "c", "d"], "run": ["c", "d"], "set": {"po": "idle", "or": "active"}},
    {"show": ["res", "e"], "run": ["e"], "set": {"or": "idle", "res": "active"}},
]
pp_caps = [
    ("Two hops, one step", "<b>Step 1.</b> <code>ul:fromPlant/ul:servesPort</code>: follow two links in a row. Q4 uses it to test the plant and port rule: <b>false</b>, no order breaks it."),
    ("Any number of hops", "<b>Step 2.</b> <code>a/rdfs:subClassOf*</code>: a type, then zero or more subclass links, however deep the hierarchy goes."),
    ("Real counts", "<b>Step 3.</b> Q5: 9,023 orders by type alone, <b>9,215</b> with the path. The 192 late orders are found only through the hierarchy."),
]
SLIDES.append(slide("Property paths: follow links of any length", "SPARQL", 4,
    head("One character, many hops", "A <b>property path</b> follows links in sequence, or any number of times.") +
    flow("Two real property paths from queries.sparql", 1448, 240, pp_nodes, pp_edges, pp_steps, pp_caps) +
    defnote([("Property path", "a shortcut to follow a relationship in sequence (/), one or more times (+), or zero or more times (*).")]),
    '''<p>Four minutes. Session 1's sanction question, "which products contain a part from this plant, at any depth", is a <code>+</code> path. Brunel has no parts list, so the hierarchy example here is classes; Session 3 gives us part hierarchies.</p>'''))

# ------------------------------------------------------------------ SQL comparison
SLIDES.append(slide("The same question in SQL", "SPARQL", 3,
    head("Where SPARQL is better, and where it is not", "Any depth is one character in SPARQL. In SQL it is a recursive query.") + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    ''' + code("SPARQL · Q5", "SELECT (COUNT(?o) AS ?n) WHERE {\n  ?o a/rdfs:subClassOf* ul:Order .\n}") + '''
    ''' + code("SQL · the same idea, for comparison", "WITH RECURSIVE sub(cls) AS (\n  SELECT 'Order'\n  UNION\n  SELECT c.child FROM class_parent c\n  JOIN sub ON c.parent = sub.cls )\nSELECT COUNT(*) FROM orders o\nJOIN sub ON o.type = sub.cls;") + '''
  </div>
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    ''' + callout("SPARQL wins", "Paths of unknown length, data from many sources with one set of names, and a schema you can query like data.", "concept") + '''
    ''' + callout("SQL wins", "Fixed, well known tables, heavy arithmetic, and decades of tuning. For a monthly sales total, use SQL.", build="1") + '''
  </div>''',
    '''<p>Three minutes. The SQL is an illustration of the shape (a recursive common table expression), not run in the lab. Be fair to SQL: this course does not claim graphs are always better.</p>'''))

# ------------------------------------------------------------------ Where time goes
SLIDES.append(slide("Where a query spends its time", "SPARQL", 3,
    head("Measure, do not guess", "The same question, written two ways, on the same data and engine.") + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    ''' + table(["Q6 · orders in a rate band gap", "Time (Oxigraph)", "Answer"], [
        ["<code>FILTER NOT EXISTS</code>, per order", bar(172482, 172482, "172 s", "red"), "1,370"],
        ["One join, then <code>GROUP BY</code>", bar(2312, 172482, "2.3 s"), "1,370"],
      ], "Real runs, reference-outputs/.") + '''
    ''' + table(["Question", "Fuseki", "Oxigraph"], [
        ["Q2 aggregation", "47 ms", "20 ms"],
        ["Q4 ASK with path", "84 ms", "23 ms"], ["Q5 subclass path", "32 ms", "14 ms"],
        ["Q6 band gap", "2,931 ms", "2,313 ms"]], "Fuseki timings include the web request.", cls="lu-table lu-table--mono") + '''
  </div>
  ''' + '<p class="lu-sub" data-build="1"><b>Why:</b> <code>NOT EXISTS</code> reran the band search for each of 8,361 orders. The rewrite joins once, then counts. Same answer, 75 times faster.</p>',
    '''<p>Three minutes. Students see these timings themselves in the lab. Oxigraph runs inside Python, so it has no network cost; Fuseki answers over HTTP.</p>'''))

# ------------------------------------------------------------------ Sandbox
SANDBOX_TTL = open(__file__.replace("part_c.py", "sandbox.ttl")).read()
SANDBOX_Q = """PREFIX ul: <https://ul.edu.lb/kr/scm#>

# Which orders were late, and by how many days?
SELECT ?order ?carrier ?days
WHERE {
  ?order ul:carriedBy ?carrier ; ul:lateDays ?days .
  FILTER (?days > 0)
}"""
SLIDES.append(slide("Query nine real orders, live", "SPARQL", 5, '''  <div class="lu-eyebrow">Sandbox · runs in your browser, offline</div>
  <h2 class="lu-h2" style="margin-bottom:var(--lu-s2)">Nine real Brunel orders. Edit the query and run it.</h2>
  <div class="lu-query" data-lang="sparql">
    <template data-data>''' + html.escape(SANDBOX_TTL) + '''</template>
    <template data-query>''' + html.escape(SANDBOX_Q) + '''</template>
  </div>
  <p class="lu-sub" style="margin-top:var(--lu-s3)">Real orders, weights rounded to 2 decimals. <b>Try next:</b> count orders per carrier with <code>GROUP BY</code>, or find orders leaving through a port their plant does not serve (<code>OPTIONAL</code> plus <code>!bound</code>). <kbd>Ctrl</kbd>+<kbd>Enter</kbd> runs.</p>''',
    '''<p>Five minutes. The in-browser engine is small on purpose: no property paths, no UNION. For those, use Fuseki in the lab.</p>
    <ul><li>Expected: the two late orders 1447288338.7 and 1447298099.7, 6 days each, carrier V444_0. Per carrier: V444_0 4, V44_3 3, V444_1 2. The plant and port query returns no rows: the rule holds.</li></ul>'''))
