"""Session 5, Part 2: R2RML, on the real Brunel orders table.

Every code panel is an excerpt of demos/session-05-integration/brunel-mapping.ttl.
Code lines stay under ~56 characters (20 px code in a wide column).
"""
from common import slide, divider, defbox, callout, code
from kit import flow, node, edge, head, table

SLIDES = []
K, S, C, V, E = '<span class="tok-kw">', '<span class="tok-str">', '<span class="tok-com">', '<span class="tok-var">', '</span>'

SLIDES.append(divider("Part 2 · R2RML", "R2RML",
    "Part 2 of 5 · about 36 minutes",
    "How do you say, once, what every row of a table means?",
    "A subject from the key, then one rule per column."))

# ---------------------------------------------------------------- standards status
cards = [
    ("R2RML", "W3C Recommendation, 2012", "Relational databases to RDF. What we use today, and what Ontop and Morph-KGC both read."),
    ("RML-Core", "Final Community Group Report, 31 October 2025", "The same ideas for CSV, JSON and XML too, by the W3C Knowledge Graph Construction group."),
    ("RML-LV", "Final Community Group Report, 31 October 2025", "Logical views: prepare or combine rows before mapping them."),
]
grid = "".join(f'<div class="lu-card"><span class="lu-card__label">{a}</span><h3 class="lu-h3">{b}</h3><p class="lu-sub">{c}</p></div>' for a, b, c in cards)
SLIDES.append(slide("R2RML and RML, where the standards stand", "R2RML", 4,
    head("Standards status, checked 25 September 2026", "One Recommendation, and its successor on the way") + f'''
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:var(--lu-s3)">{grid}</div>
  ''' + defbox([("RML", "RDF Mapping Language: R2RML extended to CSV, JSON and XML sources.")]),
    '''<p>Four minutes. A Community Group Report is not a W3C Recommendation; a W3C Working Group to standardise RML was in its charter phase in September 2026. Build on R2RML for databases; know that RML is where the tools are going.</p>'''))

# ---------------------------------------------------------------- one row becomes triples
n = [
    node("row", "row of orders: order_id 1447296446.7,\ncarrier V44_3, weight 14.3, ...", 300, 50, 560, 70, kind="literal"),
    node("s", "order 1447296446.7", 300, 200, 320, 56, kind="individual"),
    node("c", "carrier V44_3", 960, 100, 260, 56, kind="individual"),
    node("w", "14.3 (xsd:decimal)", 960, 200, 280, 56, kind="literal"),
    node("id", '"1447296446.7"', 960, 300, 260, 56, kind="literal"),
]
e = [edge("a", "row", "s", "subject template"), edge("b", "s", "c", "carriedBy"),
     edge("c1", "s", "w", "weight"), edge("d", "s", "id", "orderId")]
steps = [
    {"show": ["row"], "set": {"row": "active"}},
    {"show": ["s", "a"], "run": ["a"], "set": {"row": "idle", "s": "active"}},
    {"show": ["id", "d"], "run": ["d"]},
    {"show": ["w", "c1"], "run": ["c1"]},
    {"show": ["c", "b"], "run": ["b"], "set": {"c": "active"}},
]
caps = [
    ("One row", "<b>Step 1.</b> One real row of the orders table, the order Session 1 met first."),
    ("The subject", "<b>Step 2.</b> A template builds the order's IRI from its key: <code>.../order/brunel/{order_id}</code>, the course naming rule."),
    ("A plain value", "<b>Step 3.</b> A column copied as text: the order id."),
    ("A typed value", "<b>Step 4.</b> A column with a datatype: the weight is an <code>xsd:decimal</code>."),
    ("A link", "<b>Step 5.</b> The carrier column holds another thing's key, so a second template builds the carrier's IRI: a link, not text."),
]
walk = flow("One row becomes triples", 1448, 330, n, e, steps, caps,
            legend={"literal": "Value", "individual": "Thing with an IRI"})
SLIDES.append(slide("One row becomes triples", "R2RML", 6, '''  <div class="lu-eyebrow">Walkthrough</div>
  <h2 class="lu-h2">A subject from the key, then one rule per column</h2>
  ''' + walk, '''<p>Six minutes. The row, the IRIs and the values are real (<code>demos/session-02-rdf-sparql/sample/order.ttl</code> holds the same order as Session 2 wrote it). Ask at step 4: why does the datatype matter? Session 4's shape checks <code>sh:datatype xsd:decimal</code>.</p>'''))

# ---------------------------------------------------------------- the triples map in R2RML
tm = (f'''&lt;#Orders&gt;
  rr:logicalTable [ rr:tableName {S}"orders"{E} ] ;
  rr:subjectMap [ rr:template
    {S}"https://ul.edu.lb/kr/id/order/brunel/{{order_id}}"{E} ] ;
  rr:predicateObjectMap [ rr:predicate ul:orderId ;
    rr:objectMap [ rr:column {S}"order_id"{E} ] ] ;
  rr:predicateObjectMap [ rr:predicate ul:weight ;
    rr:objectMap [ rr:column {S}"weight"{E} ;
                   rr:datatype xsd:decimal ] ] .''')
SLIDES.append(slide("The triples map, in R2RML", "R2RML", 5, '''  <div class="lu-eyebrow">The same rules, written down</div>
  <h2 class="lu-h2">A table, a subject, and one predicate-object map per column</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code("brunel-mapping.ttl · <#Orders>, shortened", tm) + '''
    <div class="lu-stack">
      ''' + defbox([("Triples map", "One table or query, and the triples each of its rows becomes."),
                    ("IRI template", "A pattern that builds an IRI from a column: <code>{order_id}</code> is replaced by the row's value.")]) + '''
      ''' + callout("Read it as English", "For each row of <i>orders</i>, make the order's IRI; give it the id as text and the weight as a decimal.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. Every triples map has these three parts: where rows come from (<code>rr:logicalTable</code>), the subject (<code>rr:subjectMap</code>), the properties (<code>rr:predicateObjectMap</code>).</p>'''))

# ---------------------------------------------------------------- a link needs no join
lk = (f'''rr:predicateObjectMap [ rr:predicate ul:carriedBy ;
  rr:objectMap [ rr:template
    {S}"https://ul.edu.lb/kr/id/carrier/brunel/{{carrier}}"{E}
  ] ] ;''')
SLIDES.append(slide("A link needs no join", "R2RML", 4, '''  <div class="lu-eyebrow">Foreign keys</div>
  <h2 class="lu-h2">The carrier's IRI is built from the key in the order's own row</h2>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      ''' + code("brunel-mapping.ttl · inside <#Orders>", lk) + '''
      ''' + callout("A column, or a template?", "<code>rr:column \"carrier\"</code> would give the text \"V44_3\". <code>rr:template</code> gives the carrier's IRI: a link to the same node the carriers map makes.") + '''
    </div>
    ''' + callout("Why no join", "Both maps use the same template, so they build the same IRI for V44_3. R2RML can also join tables (<code>rr:parentTriplesMap</code>); with a naming rule like ours, it rarely needs to.", "neutral") + '''
  </div>''', '''<p>Four minutes. This is the payoff of Session 2's naming rule (AGENTS.md 2d): the IRI is a function of the kind and the key, so every table that mentions V44_3 lands on the same node.</p>'''))

# ---------------------------------------------------------------- logical view, all carriers
lv = (f'''&lt;#Carriers&gt;
  rr:logicalTable [ rr:sqlQuery {S}"""
    SELECT carrier FROM orders
    UNION
    SELECT carrier FROM freight_rates"""{E} ] ;
  rr:subjectMap [ rr:template
    {S}"https://ul.edu.lb/kr/id/carrier/brunel/{{carrier}}"{E} ;
    rr:class ul:Carrier ] .''')
SLIDES.append(slide("A logical view types every carrier", "R2RML", 5, '''  <div class="lu-eyebrow">Session 4's triage, fixed</div>
  <h2 class="lu-h2">An SQL query as the source: every carrier from both tables, typed once</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code("brunel-mapping.ttl · <#Carriers>", lv) + '''
    <div class="lu-stack">
      ''' + defbox([("Logical view", "An SQL query used in place of a table, to prepare or combine rows first.")]) + '''
      ''' + callout("The fix", "Session 2 typed a carrier only when an order used it: 3 carriers. This view finds all <b>10</b>. Session 4's 1,209 untyped rate bands: gone.") + '''
    </div>
  </div>''', '''<p>Five minutes. Session 4 triaged 1,209 Warnings as "the conversion's fault, fix it in the mapping". Here is the fix: one query. The 7 carriers are V444_2 and V444_4 to V444_9.</p>'''))

# ---------------------------------------------------------------- class from a value
cv = (f'''&lt;#LateOrders&gt;
  rr:logicalTable [ rr:sqlQuery {S}"""
    SELECT order_id FROM orders
    WHERE ship_late_day_count &gt; 0"""{E} ] ;
  rr:subjectMap [ rr:template
    {S}"https://ul.edu.lb/kr/id/order/brunel/{{order_id}}"{E} ;
    rr:class ul:LateOrder ] .''')
SLIDES.append(slide("A class from a column value", "R2RML", 4, '''  <div class="lu-eyebrow">Two small maps, one per class</div>
  <h2 class="lu-h2">An order with late days is a late order: a filter chooses the class</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code("brunel-mapping.ttl · <#LateOrders>", cv) + '''
    <div class="lu-stack">
      ''' + callout("The twin", "<code>&lt;#OnTimeOrders&gt;</code> is the same map with <code>= 0</code> and <code>rr:class ul:Order</code>: 9,023 orders and 192 late orders, as in Session 2.") + '''
      ''' + callout("Same subject, several maps", "Three maps make the same order IRI: the properties, the date, the class. The triples simply add up.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. R2RML classes are constants, so a class that depends on data needs a filtered source. The same trick turns any status column into classes.</p>'''))

# ---------------------------------------------------------------- a table with no key
rows = [("rows in FreightRates", "1,540"), ("different rows", "1,537 (5 rows are exact copies of another)"),
        ("different on carrier, ports, service, minimum weight", "1,258")]
SLIDES.append(slide("A table with no key", "R2RML", 4, '''  <div class="lu-eyebrow">Rate bands</div>
  <h2 class="lu-h2">No column, and no combination of columns, names one rate band</h2>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      ''' + table(["FreightRates", "Count"], rows) + '''
      ''' + code("brunel-mapping.ttl · <#RateBands>", f'''rr:subjectMap [ rr:template {S}"rate-band-{{rate_id}}"{E} ;
  rr:termType rr:BlankNode ; rr:class ul:RateBand ] ;''') + '''
    </div>
    <div class="lu-stack">
      ''' + callout("The decision", "A band gets no permanent IRI. It is a <b>blank node</b>, one per row, told apart by the row number the loader adds. As in Session 2.") + '''
      ''' + callout("Why not invent a key?", "An IRI promises that the same name means the same thing tomorrow. A row number cannot keep that promise; a blank node makes none.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. Counts checked with pandas on <code>FreightRates.csv</code> on 2026-09-25. The mapped graph has 1,540 bands, each equal to one of Session 2's (<code>reference-outputs/materialize-and-compare.txt</code>).</p>'''))

SLIDES.append(slide("Drill: mapping words", "R2RML", 3, '''  <div class="lu-eyebrow">Drill · type the missing word</div>
  <div class="lu-blanks" data-qid="s5-blanks1" data-label="R2RML words">
    <p class="lu-h3" style="margin-bottom:var(--lu-s4)">Fill in the blanks</p>
    <ol class="lu-list lu-list--num">
      <li>To build the order's IRI from its key, the subject map uses an <code>rr:</code><input class="lu-blank" data-answer="template" data-label="Blank 1" placeholder="…">.</li>
      <li>To copy a column as a plain value, the object map uses <code>rr:</code><input class="lu-blank" data-answer="column" data-label="Blank 2" placeholder="…">.</li>
      <li>To make the weight a decimal, add <code>rr:</code><input class="lu-blank" data-answer="datatype" data-label="Blank 3" placeholder="…"> <code>xsd:decimal</code>.</li>
      <li>An SQL query used as a source is written with <code>rr:</code><input class="lu-blank" data-answer="sqlQuery|sqlquery" data-label="Blank 4" placeholder="…">.</li>
    </ol>
  </div>''', '''<p>Three minutes. These four words are exactly Part B's three tasks plus the view.</p>''', kind="tint"))
