"""Session 2, Part 2 (IRI design) and Part 3 (RDFS, the first meaning). About 20 minutes."""
from kit import slide, divider, head, defbox, defnote, callout, table, flow, node, edge
from part_a import code

SLIDES = []

SLIDES.append(divider("Part 2 · Naming things: IRI design", "IRI design",
    "Part 2 of 5 · about 8 minutes",
    "Your IRI scheme is a contract with every future data source. Which scheme survives?",
    "Three real ways to name a Brunel order. Two of them break."))

SLIDES.append(slide("IRI design: three schemes", "IRI design", 4,
    head("The decision you cannot quietly undo", "Three ways to name the first Brunel order. Watch what breaks, and when.") +
    table(["Scheme", "The IRI", "It breaks when"], [
        ["Row number", "<span class='lu-mono'>.../order/1</span>", "The file is sorted differently, or a row is deleted. Every name shifts."],
        ["Key only", "<span class='lu-mono'>.../order/1447296446.7</span>", "A second system also has an order 1447296446.7. Two different orders, one name."],
        ["<b>Kind, source, key</b>", "<span class='lu-mono'>.../order/<b>brunel</b>/1447296446.7</span>", "<b>Survives both.</b> A second source gets its own space."],
      ], "The third is what common/iri.py mints today.") +
    callout("The trap", "One IRI per real thing, not per row, and not one per string that looks alike. Two systems' orders get two IRIs; deciding they are the same is a Session 5 decision, with evidence.", "concept", build="1"),
    '''<p>Four minutes. The silent failure is the second one: it does not collide loudly, it merges two orders into one and nobody notices.</p>'''))

SLIDES.append(slide("IRI design: our rules", "IRI design", 3,
    head("Three rules", "Name things so the next source cannot lie to you by accident.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <ol class="lu-list lu-list--num">
      <li><b>Say which system minted it.</b> You will have two sources by Session 5.</li>
      <li><b>Never put anything that changes</b> into an IRI: names, status, country. Keys do not change; names do.</li>
      <li><b>Words and things live apart.</b> <code>ul:</code> (ends in #) for classes and properties. <code>.../kr/id/</code> (ends in /) for things, so each can have its own web page later.</li>
    </ol>
    ''' + code("common/iri.py, the scheme the lab uses", "VOCAB = \"https://ul.edu.lb/kr/scm#\"\nDATA  = \"https://ul.edu.lb/kr/id/\"\n\ndef order_iri(source, key):\n    return f\"{DATA}order/{source}/{key}\"") + '''
  </div>''',
    '''<p>Three minutes. The room agrees its own final convention in the closing discussion; this file is the default until then.</p>'''))

# ================================================================== Part 3
SLIDES.append(divider("Part 3 · RDFS, the first meaning", "RDFS",
    "Part 3 of 5 · about 12 minutes",
    "The graph has names. Can it say anything about what an order is?",
    "A small schema, written as triples too, and the first surprise: it concludes instead of checking."))

s_nodes = [
    node("lo", "ul:LateOrder", 230, 40, 260, 60),
    node("or", "ul:Order", 230, 175, 260, 60),
    node("pr", "ul:carriedBy", 760, 40, 280, 60),
    node("ca", "ul:Carrier", 1220, 40, 260, 60),
]
s_edges = [
    edge("a", "lo", "or", "rdfs:subClassOf"),
    edge("b", "pr", "or", "rdfs:domain", route="elbow", sides=["bottom", "right"]),
    edge("c", "pr", "ca", "rdfs:range"),
]
s_steps = [
    {"show": ["lo", "or", "a"], "run": ["a"], "set": {"lo": "active"}},
    {"show": ["pr", "b"], "run": ["b"], "set": {"lo": "idle", "pr": "active"}},
    {"show": ["ca", "c"], "run": ["c"]},
]
s_caps = [
    ("Subclass", "<b>Step 1.</b> <code>rdfs:subClassOf</code>: every late order is an order. 192 Brunel orders are typed only as LateOrder."),
    ("Domain", "<b>Step 2.</b> <code>rdfs:domain</code>: whatever has a carrier is an order."),
    ("Range", "<b>Step 3.</b> <code>rdfs:range</code>: whatever it points to is a carrier."),
]
SLIDES.append(slide("RDFS: classes, subclasses, domain and range", "RDFS", 4,
    head("The first schema", "<b>RDFS</b> adds a few words for describing the data, written as triples like the data itself.") +
    flow("Part of the real schema at the top of brunel.ttl", 1448, 215, s_nodes, s_edges, s_steps, s_caps) +
    defnote([
        ("rdf:type", "the predicate that says what class a thing belongs to (written <code>a</code>)."),
        ("RDFS", "RDF Schema: the first vocabulary for classes and properties: subclass, domain, range, label."),
    ]),
    '''<p>Four minutes. The schema is 49 triples in its own named graph. Nothing new to install: it is data, queried with the same SPARQL.</p>'''))

e_nodes = [
    node("bad", "careless triple:\ncarrier V444_0\nul:carriedBy carrier V444_1", 215, 80, 400, 110),
    node("dom", "rdfs:domain\nof ul:carriedBy\nis ul:Order", 640, 80, 290, 110),
    node("res", "carrier V444_0\nis now an Order", 1000, 80, 280, 90),
    node("cnt", "Orders:\n9,023 become\n9,216", 1330, 80, 210, 110),
]
e_edges = [edge("a", "bad", "dom"), edge("b", "dom", "res"), edge("c", "res", "cnt")]
e_steps = [
    {"show": ["bad"], "set": {"bad": "active"}},
    {"show": ["dom", "a"], "run": ["a"], "set": {"bad": "idle", "dom": "active"}},
    {"show": ["res", "b"], "run": ["b"], "set": {"dom": "idle", "res": "inferred"}},
    {"show": ["cnt", "c"], "run": ["c"], "set": {"cnt": "active"}},
]
e_caps = [
    ("A mistake", "<b>Step 1.</b> Someone writes that a carrier is carried by a carrier. In SQL this would fail a foreign key check."),
    ("The schema", "<b>Step 2.</b> The schema says: whatever has <code>ul:carriedBy</code> is an Order."),
    ("An entailment", "<b>Step 3.</b> So RDFS concludes the carrier <b>is an Order</b>. No error. A new fact, derived."),
    ("Real counts", "<b>Step 4.</b> Real run: orders go from 9,023 to 9,216. That is 9,215 real orders (192 late ones join through the subclass) plus one carrier, wrongly."),
]
SLIDES.append(slide("Entailment, not constraint", "RDFS", 5,
    head("The most important difference in the course", "RDFS never rejects data. It concludes new facts from it.") +
    flow("What RDFS does with a careless triple", 1448, 170, e_nodes, e_edges, e_steps, e_caps,
         flags={"inferred": "derived"}) +
    '<p class="lu-caption">Real run: rdfs_entailment_demo.py, rdflib with owlrl, 2.6 seconds.</p>' +
    defnote([
        ("Entailment", "a fact that follows from stated facts and rules, even though nobody wrote it down."),
        ("Constraint", "a rule data must obey; breaking it is reported as an error. That is Session 4."),
    ]),
    '''<p>Five minutes, and protect them. Everyone from SQL expects an error at step 3. The shock is the lesson: domain and range are not checks. Session 4 (SHACL) is where checks live.</p>'''))

SLIDES.append(slide("Check: domain is not a check", "RDFS", 2, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-stack">
    <div class="lu-mcq" data-qid="s2-q-domain" data-answer="c" data-label="What does RDFS do with a triple that breaks a domain?"
         data-fb-correct=" RDFS infers; it never rejects." data-fb-wrong=" RDFS has no errors for domain or range. It draws conclusions.">
      <p class="lu-mcq__q">The schema says the domain of <code>ul:carriedBy</code> is <code>ul:Order</code>. A port is given a carrier by mistake. What does an RDFS reasoner do?</p>
      <div class="lu-mcq__opts" style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr))">
        <button class="lu-mcq__opt" type="button" data-key="a">Rejects the triple<span class="lu-mcq__why" hidden>That is a constraint. RDFS has none.</span></button>
        <button class="lu-mcq__opt" type="button" data-key="b">Reports a warning<span class="lu-mcq__why" hidden>RDFS has no warnings either. SHACL, Session 4, has both.</span></button>
        <button class="lu-mcq__opt" type="button" data-key="c">Concludes the port is an Order<span class="lu-mcq__why" hidden>Correct. Like our carrier, 9,215 became 9,216.</span></button>
        <button class="lu-mcq__opt" type="button" data-key="d">Ignores the domain<span class="lu-mcq__why" hidden>It uses it: that is exactly how the wrong conclusion appears.</span></button>
      </div>
      <div class="lu-mcq__fb" hidden></div>
    </div>
    ''' + callout("The habit this trains", "<b>Inference adds facts; validation refuses data.</b> Never use one for the other's job.", "concept") + '''
  </div>''', '''<p>Forty seconds. If most pick a, good: that is the SQL instinct, and it is now visible.</p>''', kind="tint"))
