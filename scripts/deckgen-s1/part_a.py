"""Session 1, opening and Part 2 (meet the supply chain and the data). About 36 minutes."""
from kit import slide, divider, head, defbox, callout, table, flow, node, edge

SLIDES = []

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
      <div class="lu-eyebrow">Knowledge Representation · Session 1 of 8</div>
      <h1 class="lu-display" style="max-width:24ch">Enterprise Knowledge Representation and the Supply Chain Problem</h1>
      <p class="lu-lead" style="max-width:46ch">One question no company can answer quickly. Two real datasets that show why. And the project your team will build to answer it.</p>
    </div>
    <div class="lu-row" style="justify-content:space-between;font-size:var(--lu-t-caption);color:var(--lu-on-night-2)">
      <span>About 180 minutes · about 120 of lecture, about 60 of lab</span>
      <span>Press <kbd>&rarr;</kbd> to begin · <kbd>?</kbd> for shortcuts</span>
    </div>
  </div>
  <template data-notes>
    <p>Rebuilt on 2026-09-24 to the course standard (AGENTS.md 2c): every concept slide leads with a picture, every term is defined where it first appears, every number comes from a real run (<code>demos/session-01-environment-and-constraints/reference-outputs/s1-facts.txt</code>).</p>
    <ul>
      <li>Do not open with housekeeping. Say your name and the course name, then go to slide 2.</li>
      <li>Setup was due before today. Ask who has Python 3.12, JDK 21, Docker and Protégé installed. Note who does not; the lab smoke test will catch them.</li>
      <li>Minutes on each slide are realistic. A dry run of the old deck ran 40 minutes against a plan of 112, so this version adds depth, not padding.</li>
    </ul>
  </template>
</section>
''')

# ------------------------------------------------------------------ The question
SLIDES.append(slide("The question nobody can answer", "Opening", 5,
    head("Start here · an illustration, not our data", "A regulator calls at nine in the morning.") + '''
  <p class="lu-lead" style="max-width:70ch">A supplier's plant was sanctioned overnight. Which products you shipped last quarter contain a part from it?</p>
  ''' + table(["System", "Stands for, and what it holds", "Supplier is called"], [
        ["<b>ERP</b>", "Enterprise Resource Planning: orders, suppliers, money", "vendor_id"],
        ["<b>WMS</b>", "Warehouse Management System: goods in and out", "supplier_code"],
        ["<b>PLM</b>", "Product Lifecycle Management: designs and parts", "mfr_ref"],
        ["<b>TMS</b>", "Transportation Management System: shipments", "party_no"],
        ["<b>CRM</b>", "Customer Relationship Management: customers", "no supplier at all"],
      ], build="1") + '''
  <p class="lu-sub" data-build="2"><b>The honest answer:</b> three weeks, four analysts, a spreadsheet nobody can rebuild.</p>''', '''<p>Five minutes. This is the slide the whole course hangs off.</p>
    <ul>
      <li>Ask: who has worked somewhere with more than five systems holding customer or supplier data? Hands go up. Use it.</li>
      <li>Build the table and let them read the five names in silence. Then the last line.</li>
      <li>The table is an illustration, and the caption says so. From Part 2 on, every example is real data.</li>
    </ul>'''))

# ------------------------------------------------------------------ The promise
SLIDES.append(slide("What you will have built by Session 8", "Opening", 2,
    head("The promise", "In eight sessions you answer that question in one sentence of English.") + '''
  <div class="lu-split" style="margin-top:var(--lu-s4)">
    <div class="lu-stack">
      <div class="lu-code lu-code--sm" data-name="what Session 7 looks like from the outside">
<pre><code><span class="tok-com"># You type this:</span>
Which finished goods used a part from plant P-114
last quarter, and who did we ship them to?

<span class="tok-com"># Your system writes this, checks it, and repairs it</span>
<span class="tok-com"># if it does not fit your own model:</span>
<span class="tok-kw">SELECT</span> ?product ?customer <span class="tok-kw">WHERE</span> {
  ?good ul:hasComponent+ ?part .
  ?part ul:producedAt    ul:plant-P114 .
  ?ship ul:carries ?good ; ul:consignedTo ?customer .
}</code></pre>
      </div>
      <p class="lu-caption">Not expected to read this yet. Expected to want to.</p>
    </div>
    <div class="lu-stack" data-build="1">
      ''' + callout("What is underneath it", "A model of what the data means, rules that refuse bad data, a mapping from live tables, a model that predicts the next late shipment, and a stack that starts with one command.", "concept") + '''
      ''' + callout("And it is your team's own", "The lectures use one supply chain case. Your team builds the same pipeline on its own topic and its own data. Part 6 today, the team project, explains how.", "neutral") + '''
    </div>
  </div>''', '''<p>Two minutes. Do not explain the query. If someone asks about the plus sign after <code>hasComponent</code>: "any depth of sub assembly, the question SQL is worst at." Move on.</p>'''))

# ------------------------------------------------------------------ Today
SLIDES.append(slide("Today: objective and time plan", "Opening", 2,
    '''  <div class="lu-eyebrow">Objective</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <p class="lu-statement">By the end of today you have met two real supply chain datasets, measured them, and written down rules they obey that no schema states.</p>
      ''' + callout("Deliverable, end of session", "A working environment, a profiling report for both datasets, and a constraint inventory: at least five rules, each with its evidence in the data. Sessions 3, 4 and 5 start from it.", "concept") + '''
    </div>
    ''' + table(["Part", "Minutes"], [
        ["1 · Opening", "10"], ["2 · The supply chain and the data", "25"], ["3 · Meaning is not in the schema", "20"],
        ["4 · The architecture", "15"], ["5 · Profiling and hidden rules", "30"], ["6 · The team project", "15"],
        ["Lab, then wrap", "65 + 5"]], "About 185 minutes in all.") + '''
  </div>''', '''<p>Two minutes. Read the deliverable aloud. The word that matters is <b>evidence</b>: a rule without a count behind it is an opinion.</p>''', kind="tint"))

# ================================================================== Part 2
SLIDES.append(divider("Part 2 · Meet the supply chain and the data", "The supply chain and the data",
    "Part 2 of 6 · about 25 minutes",
    "Before any theory: what does a supply chain look like, and what is in our two datasets?",
    "Every example for the rest of the course comes from these rows."))

# ------------------------------------------------------------------ Supply chain picture
sc_nodes = [
    node("order", "Order", 360, 55, 200, 70),
    node("supplier", "Supplier", 110, 190, 190, 70),
    node("plant", "Plant", 360, 190, 190, 70),
    node("oport", "Origin port", 610, 190, 190, 70),
    node("ship", "Shipment", 860, 190, 190, 70),
    node("dport", "Destination\nport", 1110, 190, 190, 76),
    node("customer", "Customer", 1340, 190, 170, 70),
    node("carrier", "Carrier", 860, 325, 190, 70),
]
sc_edges = [
    edge("e_co", "customer", "order", "places", route="elbow", sides=["top", "right"]),
    edge("e_op", "order", "plant", "made at"),
    edge("e_sp", "supplier", "plant"),
    edge("e_po", "plant", "oport"),
    edge("e_os", "oport", "ship"),
    edge("e_cs", "carrier", "ship", "handles"),
    edge("e_sd", "ship", "dport"),
    edge("e_dc", "dport", "customer"),
]
sc_steps = [
    {"show": ["customer", "order", "e_co"], "run": ["e_co"], "set": {"order": "active"}},
    {"show": ["plant", "e_op"], "run": ["e_op"], "set": {"order": "idle", "plant": "active"}},
    {"show": ["supplier", "e_sp"], "run": ["e_sp"], "set": {"plant": "idle", "supplier": "active"}},
    {"show": ["oport", "e_po"], "run": ["e_po"], "set": {"supplier": "idle", "oport": "active"}},
    {"show": ["ship", "carrier", "e_os", "e_cs"], "run": ["e_os", "e_cs"], "set": {"oport": "idle", "ship": "active"}},
    {"show": ["dport", "e_sd", "e_dc"], "run": ["e_sd", "e_dc"], "set": {"ship": "idle", "customer": "active"}},
]
sc_caps = [
    ("A customer places an order", "<b>Step 1.</b> A <b>customer</b> places an <b>order</b>: a request to buy a quantity of a product, with a date and a destination."),
    ("A plant makes it", "<b>Step 2.</b> The order is made at a <b>plant</b>, a factory."),
    ("A supplier feeds the plant", "<b>Step 3.</b> A <b>supplier</b> sells the plant the parts it needs."),
    ("It leaves through a port", "<b>Step 4.</b> The goods leave through a <b>port</b>, a place where goods enter or leave a country by sea or air."),
    ("A carrier moves it", "<b>Step 5.</b> The <b>shipment</b> is the physical movement of the goods. A <b>carrier</b>, a transport company, handles it."),
    ("It reaches the customer", "<b>Step 6.</b> The goods arrive. Every arrow here is a hand over between two companies, and between two computer systems."),
]
SLIDES.append(slide("The supply chain in one picture", "The supply chain and the data", 4,
    head("The domain", "A <b>supply chain</b> is the path goods take from raw material to the customer.") +
    flow("A supply chain, step by step", 1448, 370, sc_nodes, sc_edges, sc_steps, sc_caps),
    '''<p>Four minutes. Step through slowly; each step names one word the rest of the course uses.</p>
    <ul>
      <li>Keyboard: with the diagram focused, left and right arrows move the steps.</li>
      <li>End on step 6: "every arrow is a hand over". That is where meaning gets lost, and Part 3 shows it happening in our data.</li>
    </ul>'''))

# ------------------------------------------------------------------ DataCo at a glance
SLIDES.append(slide("DataCo: what is in it", "The supply chain and the data", 4,
    head("Dataset 1 · DataCo", "<b>DataCo</b>: three years of orders from a sports and electronics retailer, in one wide table.") + '''
  <p class="lu-sub"><b>180,519</b> rows · <b>53</b> columns · <b>65,752</b> orders · <b>20,652</b> customers · <b>118</b> products · 1 Jan 2015 to 31 Jan 2018</p>
  ''' + table(["Order Id", "Order Country", "Shipping Mode", "Days real", "Days scheduled", "Delivery Status"], [
        ["77202", "Indonesia", "Standard Class", "3", "4", "Advance shipping"],
        ["75939", "India", "Standard Class", "5", "4", "Late delivery"],
        ["75938", "India", "Standard Class", "4", "4", "Shipping on time"],
      ], "The first three real rows, 6 of 53 columns. Source: DataCo Global, Mendeley Data, DOI 10.17632/8gx2fvg2k6.5, CC BY 4.0.", cls="lu-table lu-table--mono", build="1"),
    '''<p>Four minutes. Read one row aloud as a sentence: "order 75939, placed on 13 January 2018, shipped Standard Class to Bikaner in India, took 5 days against 4 scheduled, marked late."</p>
    <ul><li>Point at the two day columns and the status column. Part 3 comes back to exactly these three.</li></ul>'''))

# ------------------------------------------------------------------ Grain
g_nodes = [
    node("o2", "Order 2\n1 Jan 2015\nDos Quebradas", 140, 180, 260, 110),
    node("l2", "Line 2 · Pelican kayak · qty 1", 555, 60, 480, 70),
    node("l3", "Line 3 · Nike golf polo · qty 5", 555, 180, 480, 70),
    node("l4", "Line 4 · Nike football cleat · qty 1", 555, 300, 480, 70),
]
g_edges = [edge("a", "o2", "l2"), edge("b", "o2", "l3"), edge("c", "o2", "l4")]
g_steps = [
    {"show": ["o2"], "set": {"o2": "active"}},
    {"show": ["l2", "l3", "l4", "a", "b", "c"], "run": ["a", "b", "c"], "set": {"o2": "idle", "l2": "active", "l3": "active", "l4": "active"}},
]
g_caps = [
    ("One order", "<b>Step 1.</b> One real order: order 2, placed on 1 January 2015 for Dos Quebradas."),
    ("Three rows", "<b>Step 2.</b> It fills <b>three rows</b> of the file, one per product. Counting rows counts order lines, not orders."),
]
SLIDES.append(slide("One row is an order line, not an order", "The supply chain and the data", 3,
    head("The first profiling question", "What does one row stand for? In DataCo, one product inside an order.") +
    '<div class="lu-split lu-split--wide-left" style="align-items:center">' +
    flow("One order, three rows", 800, 360, g_nodes, g_edges, g_steps, g_caps) +
    '<div class="lu-stack">' + defbox([
        ("Order line", "One product inside an order, with its quantity. DataCo stores one order line per row."),
        ("Grain", "What one row of a table stands for. Always the first thing to find out."),
    ]) + callout("Real counts", "65,752 orders fill 180,519 rows. 19,850 orders have one line; the rest have 2 to 5.", "neutral") + '</div></div>',
    '''<p>Three minutes. This is the first real finding of the day, and it has a cost: anyone who counts rows and calls them orders is wrong by a factor of 2.7.</p>
    <ul><li>Ask before step 2: "how many rows does order 2 take?" Most will say one.</li></ul>'''))

# ------------------------------------------------------------------ Brunel seven tables
b_nodes = [
    node("ol", "OrderList\n9,215 rows", 724, 190, 260, 90),
    node("pp", "PlantPorts\n22 rows", 215, 60, 270, 80),
    node("ppl", "ProductsPerPlant\n2,036 rows", 215, 190, 270, 80),
    node("vmi", "VmiCustomers\n14 rows", 215, 320, 270, 80),
    node("fr", "FreightRates\n1,540 rows", 1233, 60, 270, 80),
    node("wcap", "WhCapacities\n19 rows", 1233, 190, 270, 80),
    node("wcost", "WhCosts\n19 rows", 1233, 320, 270, 80),
]
b_edges = [
    edge("a", "ol", "pp", "Plant Code", sides=["left", "right"], route="elbow"),
    edge("b", "ol", "ppl", "Plant Code", sides=["left", "right"]),
    edge("c", "ol", "vmi", "Customer", sides=["left", "right"], route="elbow"),
    edge("d", "ol", "fr", "Carrier", sides=["right", "left"], route="elbow"),
    edge("e", "ol", "wcap", "Plant ID", sides=["right", "left"]),
    edge("f", "ol", "wcost", "WH", sides=["right", "left"], route="elbow"),
]
b_steps = [
    {"show": ["ol"], "set": {"ol": "active"}},
    {"show": ["pp", "ppl", "a", "b"], "run": ["a", "b"], "set": {"ol": "idle"}},
    {"show": ["fr", "d"], "run": ["d"]},
    {"show": ["wcap", "wcost", "e", "f"], "run": ["e", "f"], "set": {"wcap": "active", "wcost": "active"}},
    {"show": ["vmi", "c"], "run": ["c"], "set": {"wcap": "idle", "wcost": "idle"}},
]
b_caps = [
    ("The orders", "<b>Step 1.</b> <b>OrderList</b>: 9,215 orders, each with a plant, two ports, a carrier, a customer, a product and a weight."),
    ("What each plant can do", "<b>Step 2.</b> Which ports each plant ships through, and which products each plant makes. They link by <b>Plant Code</b>."),
    ("What shipping costs", "<b>Step 3.</b> <b>FreightRates</b>: a price per carrier, per port pair, per weight band."),
    ("Same plant, three names", "<b>Step 4.</b> Warehouse capacity and cost. The same plant is called <b>Plant Code</b>, <b>Plant ID</b> and <b>WH</b> in three tables of one file."),
    ("Special customers", "<b>Step 5.</b> <b>VmiCustomers</b>: 14 pairs of plant and customer that get special treatment. Nothing in the file says what VMI means."),
]
SLIDES.append(slide("Brunel: seven tables, drawn", "The supply chain and the data", 4,
    head("Dataset 2 · Brunel", "<b>Brunel</b>: one day of a real logistics problem, in seven linked tables.") +
    flow("Brunel's seven tables and the columns that link them", 1448, 380, b_nodes, b_edges, b_steps, b_caps) +
    '<p class="lu-caption">Source: Kalganova and Dzalbs, Brunel University London, on Figshare, licence CC BY 4.0. Exported from one workbook to seven CSV files by demos/data/fetch_data.py.</p>',
    '''<p>Four minutes. Stop on step 4. Three names for one plant, in one file, made by one team. That is the whole course in one step.</p>
    <ul><li>Someone will ask what VMI means. Answer: vendor managed inventory, a standard term, but the file never says so. A human knows; the data does not.</li></ul>'''))

# ------------------------------------------------------------------ Brunel one row each
SLIDES.append(slide("Brunel: one real row from each table", "The supply chain and the data", 3,
    head("Dataset 2 · the rows", "Seven tables, one real row each. Read them like sentences.") +
    table(["Table", "Its first real row"], [
        ["OrderList", "order <b>1447296446.7</b> · 2013-05-26 · PLANT16 · PORT09 · V44_3 · CRF · 808 units · weight 14.3"],
        ["FreightRates", "V444_6 · PORT08 to PORT09 · 250 to 499.99 · DTD · rate 0.7132 · 'AIR   '"],
        ["PlantPorts", "PLANT01 ships through PORT01"],
        ["ProductsPerPlant", "PLANT15 makes product 1698815"],
        ["WhCapacities", "PLANT15 · daily capacity 11"],
        ["WhCosts", "PLANT15 · cost per unit 1.4151"],
        ["VmiCustomers", "PLANT02 · customer V5555555555555_16"],
      ], "Real first rows, from reference-outputs/s1-facts.txt.", cls="lu-table lu-table--mono") + '''
  <p class="lu-sub" data-build="1"><b>Look again:</b> an order number with a decimal point, a mode with three trailing spaces, codes that mean nothing outside this file.</p>''',
    '''<p>Three minutes. Let them spot the oddities before you build the callout. Somebody usually sees the decimal in the order number first.</p>'''))

# ------------------------------------------------------------------ Why they do not join
SLIDES.append(slide("Why the two datasets do not join", "The supply chain and the data", 3,
    head("Two correct datasets", "Both describe orders, plants and shipping. Not one name is shared.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    ''' + table(["", "DataCo", "Brunel"], [
        ["Time", "1 Jan 2015 to 31 Jan 2018", "One day: 26 May 2013"],
        ["One row is", "An order line", "An order"],
        ["An order is called", "Order Id 75939", "Order ID 1447296446.7"],
        ["A place is", "A city and a country, in Spanish: Estados Unidos", "A code: PORT09"],
        ["Shipping is", "A class: Standard Class", "A carrier code: V444_0"],
      ], "Real values from both datasets.") + '''
    <div class="lu-stack">
      ''' + defbox([("JOIN", "SQL's way to combine rows from two tables that share a key.")]) + '''
      ''' + callout("This is normal", "Both correct, no shared key. This course writes down what names mean, so a machine can connect them.", build="1") + '''
    </div>
  </div>''',
    '''<p>Three minutes. The point is not that the data is bad. Each dataset is fine. They simply never agreed on names, which is the everyday state of enterprise data.</p>'''))

# ------------------------------------------------------------------ Check: grain
SLIDES.append(slide("Check: what one row means", "The supply chain and the data", 2, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-stack">
    <div class="lu-mcq" data-qid="s1-q-grain" data-answer="c" data-label="How many orders are in 180,519 DataCo rows?"
         data-fb-correct=" Rows are order lines; orders are counted by distinct Order Id."
         data-fb-wrong=" Count what one row stands for before you count rows.">
      <p class="lu-mcq__q">A manager reads "180,519 rows" in DataCo and reports "180,519 orders last quarter". What is the real number of orders in the file?</p>
      <div class="lu-mcq__opts" style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr))">
        <button class="lu-mcq__opt" type="button" data-key="a">180,519, one per row<span class="lu-mcq__why" hidden>One row is one order line, one product inside an order.</span></button>
        <button class="lu-mcq__opt" type="button" data-key="b">20,652, one per customer<span class="lu-mcq__why" hidden>That is the number of customers. Most customers ordered more than once.</span></button>
        <button class="lu-mcq__opt" type="button" data-key="c">65,752, the distinct order numbers<span class="lu-mcq__why" hidden>Correct. Count distinct Order Id values, not rows.</span></button>
        <button class="lu-mcq__opt" type="button" data-key="d">It cannot be known from the file<span class="lu-mcq__why" hidden>It can: the Order Id column tells you which rows belong together.</span></button>
      </div>
      <div class="lu-mcq__fb" hidden></div>
    </div>
    ''' + callout("The habit this trains", "<b>Find the grain before you count anything.</b> It is the first line of every profiling report you will write.", "concept") + '''
  </div>''', '''<p>Forty seconds, show of hands, then reveal. Distractor <b>a</b> is the one that ships to management every day.</p>''', kind="tint"))
