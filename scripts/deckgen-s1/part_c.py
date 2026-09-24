"""Session 1, Part 5 (profiling and hidden rules). About 30 minutes."""
from kit import slide, divider, head, defbox, defnote, callout, table, figure, bar, flow, node, edge

SLIDES = []

SLIDES.append(divider("Part 5 · Profiling and hidden rules", "Profiling and hidden rules",
    "Part 5 of 6 · about 30 minutes",
    "The data obeys rules nobody wrote down. How do you find them?",
    "Guess, measure, then try to break your guess. Every example here comes from our two datasets."))

# ------------------------------------------------------------------ Why profile
c_nodes = [
    node("guess", "Guess what a\ncolumn means", 170, 110, 260, 90),
    node("meas", "Measure it\n(profile)", 540, 110, 240, 90),
    node("rule", "Write the rule,\nwith the count", 910, 110, 260, 90),
    node("attack", "Look for a row\nthat breaks it", 1280, 110, 260, 90),
]
c_edges = [
    edge("a", "guess", "meas"), edge("b", "meas", "rule"), edge("c", "rule", "attack"),
    edge("d", "attack", "guess", "repeat", route="elbow", sides=["bottom", "bottom"]),
]
c_steps = [
    {"show": ["guess"], "set": {"guess": "active"}},
    {"show": ["meas", "a"], "run": ["a"], "set": {"guess": "idle", "meas": "active"}},
    {"show": ["rule", "b"], "run": ["b"], "set": {"meas": "idle", "rule": "active"}},
    {"show": ["attack", "c", "d"], "run": ["c", "d"], "set": {"rule": "idle", "attack": "active"}},
]
c_caps = [
    ("Guess", "<b>Step 1.</b> Read the column names and write what you think each one means. A guess gives the numbers something to test."),
    ("Measure", "<b>Step 2.</b> <b>Profile</b> it: count values, empty cells, ranges, links between tables."),
    ("Write the rule", "<b>Step 3.</b> Write the rule in one sentence, with the count that supports it."),
    ("Try to break it", "<b>Step 4.</b> Hunt for a row that breaks the rule. Then decide: is the row wrong, or the rule? Repeat."),
]
SLIDES.append(slide("Why profile before modelling", "Profiling and hidden rules", 3,
    head("The method", "<b>Data profiling</b>: measuring a dataset to learn its real shape.") +
    flow("The profiling loop", 1448, 230, c_nodes, c_edges, c_steps, c_caps) +
    '<div class="lu-row" style="gap:var(--lu-s5)">' +
    defbox([("Data profiling", "Measuring a dataset to learn its real shape: counts, missing values, ranges, repeated values, links between tables.")]) +
    '</div>',
    '''<p>Three minutes. The loop is the lab. Everything in the next nine slides is one turn of it on real data.</p>
    <ul><li>Profiling without a guess produces statistics, not findings. Say it once, clearly.</li></ul>'''))

# ------------------------------------------------------------------ Cardinality
k_nodes = [node(f"p{i}", n, 170, 28 + 46 * i, 230, 38) for i, n in enumerate(
    ["PLANT03", "PLANT08", "PLANT09", "PLANT12", "PLANT13", "PLANT01", "PLANT16"])]
k_nodes += [node("port4", "PORT04", 620, 120, 200, 52), node("port1", "PORT01", 620, 258, 200, 38),
            node("port2", "PORT02", 620, 304, 200, 38), node("port9", "PORT09", 620, 350, 200, 38)]
k_edges = [edge(f"k{i}", f"p{i}", "port4") for i in range(5)]
k_edges += [edge("k5a", "p5", "port1"), edge("k5b", "p5", "port2"), edge("k6", "p6", "port9")]
k_steps = [{"show": [n["id"] for n in k_nodes] + [e["id"] for e in k_edges], "set": {"port4": "active", "p5": "active"}}]
SLIDES.append(slide("Distinct values and links", "Profiling and hidden rules", 3,
    head("Measure 1 · cardinality", "How many different values? How many links from each side?") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s2)">
    <div class="lu-stack">''' +
    flow("Real plant to port links from PlantPorts", 800, 372, k_nodes, k_edges, k_steps) +
    '''<p class="lu-caption">Real links, 7 of 19 plants shown. Rings: the many side and the two way side.</p></div>
    <div class="lu-stack">''' +
    defnote([
        ("Cardinality (of a column)", "how many different values it holds. Order Date: 1. Order ID: 9,215."),
        ("One to many", "one thing links to several on the other side. Seven plants share PORT04."),
    ]) +
    table(["PlantPorts", "Real count"], [
        ["Plants · ports", "19 · 11"],
        ["Possible pairs", "209"],
        ["Pairs that exist", "<b>22</b>"],
    ], cls="lu-table lu-table--mono", build="1") +
    '</div></div>',
    '''<p>Three minutes. Two kinds of cardinality: a column's number of distinct values, and a link's number of partners on each side.</p>
    <ul><li>22 of 209 is the headline: only one pair in ten exists. That smells like a rule. Slide "One real row of the inventory" writes it down.</li></ul>'''))

# ------------------------------------------------------------------ Nulls
SLIDES.append(slide("Empty cells, and what missing means", "Profiling and hidden rules", 3,
    head("Measure 2 · nulls", "An empty cell is a fact about the data. What it means is a decision.") + '''
  <div class="lu-split" style="margin-top:var(--lu-s2)">
    <div class="lu-stack">
      ''' + table(["DataCo column", "Empty cells out of 180,519"], [
        ["Product Description", bar(180519, 180519, "180,519", "red")],
        ["Order Zipcode", bar(155679, 180519, "155,679", "red")],
        ["Customer Lname", bar(8, 180519, "8")],
        ["Customer Zipcode", bar(3, 180519, "3")],
      ], "Every other column is full. Real counts.") + '''
    </div>
    <div class="lu-stack" data-build="1">
      <div class="lu-grid">
        <div class="lu-card lu-col-6"><span class="lu-card__label">Closed world · SQL</span><p class="lu-sub">No zip code stored, so the order <b>has no</b> zip code. Missing means <b>false</b>.</p></div>
        <div class="lu-card lu-col-6"><span class="lu-card__label">Open world · Session 3</span><p class="lu-sub">No zip code stored, so we <b>do not know</b> it. Missing means <b>unknown</b>.</p></div>
      </div>
      ''' + defnote([
        ("Null", "an empty cell."),
        ("Closed world", "missing means false, as in SQL."),
        ("Open world", "missing means unknown. Session 3."),
      ]) + '''
    </div>
  </div>''',
    '''<p>Three minutes. A whole column that is always empty is not a quality problem, it is a column nobody uses. Zip code missing for 86 percent is different: someone needs it and it is not there.</p>
    <ul><li>Open world is only previewed. The line to leave: missing is not false. Session 3 spends real time on it.</li></ul>'''))

# ------------------------------------------------------------------ Distributions
SLIDES.append(slide("Distributions: what the counts say", "Profiling and hidden rules", 3,
    head("Measure 3 · distribution", "How often each value appears. A strange shape is a question to ask.") + '''
  <div class="lu-split" style="margin-top:var(--lu-s2)">
    <div class="lu-stack">
      ''' + table(["DataCo · Shipping Mode", "Order lines"], [
        ["Standard Class", bar(107752, 180519, "107,752")],
        ["Second Class", bar(35216, 180519, "35,216")],
        ["First Class", bar(27814, 180519, "27,814")],
        ["Same Day", bar(9737, 180519, "9,737")],
      ], "A normal shape: most orders ship the cheap way.") + '''
      ''' + defnote([("Distribution", "how often each value, or range of values, appears in a column.")]) + '''
    </div>
    <div class="lu-stack" data-build="1">
      ''' + table(["Brunel · OrderList", "What the counts show"], [
        ["Order Date", "<b>1</b> distinct value: 2013-05-26"],
        ["Destination Port", "<b>1</b> distinct value: PORT09"],
        ["Ship Late Day count", bar(9023, 9215, "9,023 zeros", "red")],
        ["Ship ahead day count", bar(4426, 9215, "4,426 zeros")],
      ], "Real counts out of 9,215 orders.") + '''
    </div>
  </div>''',
    '''<p>Three minutes. The Brunel side is the finding: every order is on one day, to one port. Brunel is a snapshot, not a history, so it cannot teach "late over time". Know that before Session 6 asks you to predict.</p>'''))

# ------------------------------------------------------------------ Referential integrity
r_nodes = [
    node("c0", "V444_0 · 6,264 orders", 190, 35, 330, 56),
    node("c1", "V444_1 · 2,097 orders", 190, 112, 330, 56),
    node("c3", "V44_3 · 854 orders", 190, 190, 330, 56),
    node("fr", "FreightRates\ncarriers V444_0 to V444_9", 720, 73, 370, 80),
    node("miss", "No rate for V44_3", 720, 190, 370, 56),
    node("crf", "All 854 are CRF", 1235, 190, 300, 56),
]
r_edges = [
    edge("a", "c0", "fr"), edge("b", "c1", "fr"),
    edge("c", "c3", "miss", kind="conflict"),
    edge("d", "miss", "crf"),
]
r_steps = [
    {"show": ["c0", "c1", "fr", "a", "b"], "run": ["a", "b"], "set": {"fr": "active"}},
    {"show": ["c3", "miss", "c"], "run": ["c"], "set": {"fr": "idle", "miss": "impossible"}},
    {"show": ["crf", "d"], "run": ["d"], "set": {"crf": "active"}},
]
r_caps = [
    ("Carriers with rates", "<b>Step 1.</b> Two carriers in OrderList find their prices in FreightRates, joined on <b>Carrier</b>."),
    ("A carrier with none", "<b>Step 2.</b> <b>854</b> orders use carrier V44_3, which has <b>no row</b> in FreightRates. The reference points at nothing."),
    ("A hidden rule", "<b>Step 3.</b> All 854 have service level CRF, and no other order does. A rule no table states: CRF orders go with V44_3 and are not priced here."),
]
SLIDES.append(slide("Referential integrity: does every reference point somewhere?", "Profiling and hidden rules", 4,
    head("Measure 4 · links between tables", "Every order names a carrier. Does every carrier have a price?") +
    flow("Carriers in OrderList against FreightRates", 1448, 250, r_nodes, r_edges, r_steps, r_caps,
         flags={"impossible": "missing"}) +
    '<div class="lu-row" style="gap:var(--lu-s5)">' +
    defbox([("Referential integrity", "Every reference points at something that exists, for example every order's carrier has a row in the rate table.")]) +
    '</div>',
    '''<p>Four minutes. Step 3 is the payoff: a broken reference turned into a rule. The counts match exactly: 854 V44_3 orders, 854 CRF orders, the same 854.</p>
    <ul><li>Do not claim to know what CRF means. The file does not say. Writing "we do not know what CRF means" in the inventory is a correct, graded answer.</li></ul>'''))

# ------------------------------------------------------------------ Tool: ydata-profiling
SLIDES.append(slide("The tool: ydata-profiling", "Profiling and hidden rules", 2,
    head("One slide for the tool", "<b>ydata-profiling</b> measures every column and lists what looks odd.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s2)">
    ''' + figure("../assets/img/s1-ydata-alerts.png", "ydata-profiling report for Brunel OrderList, Alerts tab, listing constant Order Date and Destination Port and many zeros",
                 "Real report for Brunel OrderList, Alerts tab, made by profiling.py in the lab.") + '''
    <div class="lu-stack">
      <ol class="lu-list lu-list--num">
        <li><b>Constant</b>: Order Date and Destination Port.</li>
        <li><b>Zeros</b>: Ship Late Day count, 97.9 percent.</li>
        <li><b>Order ID</b> typed as a <b>real number</b>: an identifier with a decimal point.</li>
      </ol>
    </div>
  </div>''',
    '''<p>Two minutes. The concepts came first; this is only where to click. The Alerts tab is the fastest way in.</p>'''))

# ------------------------------------------------------------------ Clustering concept
f_nodes = [
    node("v1", "Los Angeles", 150, 45, 250, 64, kind="literal"),
    node("v2", "Los Ángeles", 150, 175, 250, 64, kind="literal"),
    node("key", "Same key:\nangeles los", 560, 110, 270, 90),
    node("cl", "One cluster:\nthe same city?", 940, 110, 270, 90),
    node("chk", "California · 1,845\nChile · 16", 1300, 110, 270, 90),
]
f_edges = [
    edge("a", "v1", "key"), edge("b", "v2", "key"),
    edge("c", "key", "cl"), edge("d", "cl", "chk"),
]
f_steps = [
    {"show": ["v1", "v2"]},
    {"show": ["key", "a", "b"], "run": ["a", "b"], "set": {"key": "active"}},
    {"show": ["cl", "c"], "run": ["c"], "set": {"key": "idle", "cl": "active"}},
    {"show": ["chk", "d"], "run": ["d"], "set": {"cl": "impossible"}},
]
f_caps = [
    ("Two values", "<b>Step 1.</b> Two real values from DataCo's <code>Order City</code>. They look like one city spelled twice."),
    ("A key for each", "<b>Step 2.</b> A <b>fingerprint</b> removes case, accents and punctuation, and sorts the words. Both become <code>angeles los</code>."),
    ("A cluster", "<b>Step 3.</b> Values with the same key form a <b>cluster</b>: a suggestion that they are one thing."),
    ("Check before you merge", "<b>Step 4.</b> Check the other columns. One is Los Angeles in California, the other is Los Ángeles in Chile. <b>Different cities.</b>"),
]
SLIDES.append(slide("Clustering: same text, same thing?", "Profiling and hidden rules", 3,
    head("Measure 5 · near duplicates", "Clustering suggests values that may be one thing. You decide.") +
    flow("How a fingerprint clusters two city names", 1448, 220, f_nodes, f_edges, f_steps, f_caps,
         flags={"impossible": "differ"}) +
    '<div class="lu-row" style="gap:var(--lu-s5)">' +
    defbox([("Clustering (of values)", "Grouping values that look alike, such as two spellings, so a person can decide whether they mean the same thing.")]) +
    '</div>',
    '''<p>Three minutes. Everyone expects step 4 to be a merge. It is not. This is the whole lesson of clustering: a cluster is a question, not an answer.</p>'''))

# ------------------------------------------------------------------ Tool: OpenRefine
SLIDES.append(slide("The tool: OpenRefine", "Profiling and hidden rules", 2,
    head("One slide for the tool", "<b>OpenRefine</b> clusters a column for you. You still decide.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s2)">
    ''' + figure("../assets/img/s1-openrefine-clusters.png", "OpenRefine Cluster and edit dialog on the Order City column, three clusters found",
                 "Real run, OpenRefine 3.8.7: Order City menu, Edit cells, Cluster and edit. 3 clusters among 3,597 city names.") + '''
    <div class="lu-stack">
      ''' + table(["Cluster", "Really"], [
        ["Los Angeles · Los Ángeles", "California · Chile"],
        ["Vitória · Vitoria", "Brazil · Spain"],
        ["Macon · Mâcon", "Georgia, US · France"],
      ], "Checked against Order Country.") + '''
      ''' + callout("Do not click Merge", "All three clusters are different cities. The Merge box stays empty.", build="1") + '''
    </div>
  </div>''',
    '''<p>Two minutes. Only the path to the dialog is new; the idea was the last slide. If a student merges, their DataCo loses a Chilean city and 16 orders move to California.</p>'''))

# ------------------------------------------------------------------ Inventory row
SLIDES.append(slide("One real row of the constraint inventory", "Profiling and hidden rules", 3,
    head("Writing it down", "A rule, its evidence, and where it lives. Two of three is not a finding.") +
    table(["Rule, one sentence", "Evidence in the data", "Source columns"], [
        ["A plant ships only through a port it is linked to.", "22 of 209 possible pairs exist. <b>All 9,215 orders</b> leave through a linked port: 0 exceptions.", "OrderList: Plant Code, Origin Port · PlantPorts"],
        ["An order with service level CRF uses carrier V44_3, which has no freight rate.", "854 CRF orders, 854 V44_3 orders, the same rows. V44_3 is absent from FreightRates.", "OrderList: Service Level, Carrier · FreightRates: Carrier"],
      ], "Both rules are real and hold on every row. The file states neither.", cls="lu-table") +
    defbox([
        ("Business rule", "A rule the business follows that the data should obey."),
        ("Constraint inventory", "Our table of business rules found in the data, each with evidence and source."),
      ]),
    '''<p>Three minutes. Read row 1 across: rule, evidence, source. Where it goes next: Session 3 turns rules into meaning, Session 4 into checks, Session 5 into mapping decisions. That is the standard for the lab. <code>constraint_inventory_template.csv</code> has the same three columns.</p>'''))

# ------------------------------------------------------------------ Rule or exception
x_nodes = [
    node("rule", "Rule: every order's weight\nfalls in a rate band\nfor its lane", 185, 180, 340, 120),
    node("ord", "An order on lane\nV444_1 · PORT04 · DTD\nweight 11.8", 590, 70, 320, 110),
    node("bands", "Bands for that lane:\n... 2.01 to 2.50\nthen 70.51 to 99.99 ...", 590, 300, 320, 110),
    node("gap", "No band fits.\n1,370 of 8,361 orders\nfall in such gaps", 980, 180, 310, 120),
    node("dec", "Decision: the rate\ntable has a gap.\nThe rows are fine.", 1315, 180, 260, 120),
]
x_edges = [
    edge("a", "rule", "ord"), edge("b", "rule", "bands"),
    edge("c", "ord", "gap", kind="conflict"), edge("d", "bands", "gap", kind="conflict"),
    edge("e", "gap", "dec"),
]
x_steps = [
    {"show": ["rule"], "set": {"rule": "active"}},
    {"show": ["ord", "bands", "a", "b"], "run": ["a", "b"], "set": {"rule": "idle"}},
    {"show": ["gap", "c", "d"], "run": ["c", "d"], "set": {"gap": "impossible"}},
    {"show": ["dec", "e"], "run": ["e"], "set": {"dec": "active"}},
]
x_caps = [
    ("A rule", "<b>Step 1.</b> A rule from the syllabus: a freight rate band must cover the shipped weight."),
    ("Attack it", "<b>Step 2.</b> Take a real order and the real bands for its lane."),
    ("It breaks", "<b>Step 3.</b> Weight 11.8 falls between 2.50 and 70.51. <b>1,370</b> orders fall in gaps like this; 1,364 of them on this one lane."),
    ("Row or rule?", "<b>Step 4.</b> The weights are plausible, so the rows are not wrong. The rate table is missing bands. Record the rule <b>and</b> its exceptions."),
]
SLIDES.append(slide("Rule or exception?", "Profiling and hidden rules", 3,
    head("The last step of the loop", "A rule that breaks is still a finding. Decide what broke.") +
    flow("Testing the rate band rule on real orders", 1448, 360, x_nodes, x_edges, x_steps, x_caps,
         flags={"impossible": "breaks"}),
    '''<p>Three minutes. The contrast with the plant and port rule is the lesson: one rule holds on 9,215 of 9,215 rows, this one fails on 1,370 of 8,361. Both go in the inventory, with their counts.</p>
    <ul><li>Session 4 decides what each becomes: no exceptions, an error; real exceptions, a warning or a new class.</li></ul>'''))
