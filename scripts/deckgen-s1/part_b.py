"""Session 1, Part 3 (meaning is not in the schema) and Part 4 (the architecture). About 34 minutes."""
from kit import slide, divider, head, defbox, defnote, callout, table, flow, node, edge

SLIDES = []

# ================================================================== Part 3
SLIDES.append(divider("Part 3 · Meaning is not in the schema", "Meaning and storage",
    "Part 3 of 6 · about 20 minutes",
    "The file stores every value correctly. So where did its meaning go?",
    "Meaning is written down nowhere a program can reach it. Our own data shows it leaving."))

# ------------------------------------------------------------------ Storing vs meaning
SLIDES.append(slide("Storing data against representing meaning", "Meaning and storage", 5,
    head("The distinction the course is built on", "A schema records the shape of data. It does not record what anything means.") + '''
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <div class="lu-code lu-code--sm" data-name="DataCo · real columns and what the file never says">
<pre><code>Late_delivery_risk  <span class="tok-kw">INTEGER</span>  <span class="tok-com">-- 1 means the line WAS late</span>
Customer Country    <span class="tok-kw">TEXT</span>     <span class="tok-com">-- 'EE. UU.' is Spanish for USA</span>
Order Zipcode       <span class="tok-kw">NUMBER</span>   <span class="tok-com">-- 155,679 of 180,519 missing</span>
Product Status      <span class="tok-kw">INTEGER</span>  <span class="tok-com">-- always 0, carries nothing</span></code></pre>
      </div>
      ''' + callout("Where meaning lives today", "In heads, in a stale wiki, in the WHERE clauses of old reports. <b>Nowhere a program can read.</b>") + '''
    </div>
    <div class="lu-stack" data-build="1">
      ''' + defnote([
        ("Schema", "the declared shape of data: tables, columns, types, keys. How it looks, not what it means."),
        ("Semantic layer", "a machine readable description of what the data means, above the systems that store it."),
      ]) + '''
    </div>
  </div>''',
    '''<p>Five minutes. Read the four comments at the bottom of the code aloud, slowly. Every one is a real fact about a real column.</p>
    <ul>
      <li><code>Late_delivery_risk</code> is the best one: its name says "risk", yet it equals 1 on exactly the 98,977 lines marked late. The name lies and the schema cannot tell you.</li>
      <li>Ask: who has met a status column with an undocumented code? Thirty seconds, always lands.</li>
    </ul>'''))

# ------------------------------------------------------------------ Where meaning leaks
SLIDES.append(slide("Where meaning leaks: two columns, one country", "Meaning and storage", 4,
    head("A real leak, inside one file", "Same country, two spellings. Same word \"customer\", two different places.") + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    <div class="lu-stack">
      ''' + table(["Customer Country · 2 values", "Lines"], [
        ["EE. UU.", "111,146"],
        ["Puerto Rico", "69,373"],
      ], cls="lu-table lu-table--mono") + '''
      ''' + table(["Order Country · 164 values", "Lines"], [
        ["Estados Unidos", "24,840"],
        ["Francia", "13,222"],
        ["México", "13,172"],
        ["161 more countries", "129,285"],
      ], cls="lu-table lu-table--mono", build="1") + '''
    </div>
    <div class="lu-stack">
      <ul class="lu-list">
        <li>Every customer lives in the United States or Puerto Rico. Their orders go to <b>164 countries</b>.</li>
        <li>The United States is <code>EE. UU.</code> in one column and <code>Estados Unidos</code> in the next. A JOIN on country finds no match.</li>
      </ul>
      ''' + callout("Say this one out loud", "Integration rarely fails because data is dirty. <b>It fails because two correct descriptions of the world meet, and nobody wrote down how they differ.</b>", build="2") + '''
    </div>
  </div>''',
    '''<p>Four minutes. Build the second table only after they have read the first and think "customer country" answers "where do we sell".</p>
    <ul>
      <li>Both columns are correct. One is the billing address of the customer, the other is the delivery destination. The file does not say which is which.</li>
      <li>Expected question: "would master data management not fix this?" Answer: it picks one spelling and throws the reason away. We want to record the difference, not erase it.</li>
    </ul>'''))

# ------------------------------------------------------------------ Two meanings of late
l_nodes = [
    node("data", "DataCo\n180,519 order lines", 150, 180, 260, 96),
    node("ra", "Rule A: Delivery Status\n= 'Late delivery'", 560, 70, 360, 90),
    node("rb", "Rule B: Days real\n> Days scheduled", 560, 290, 360, 90),
    node("na", "98,977 late\n54.8 percent", 950, 70, 250, 90),
    node("nb", "103,400 late\n57.3 percent", 950, 290, 250, 90),
    node("gap", "4,423 lines\ncanceled, yet\nlate by the clock", 1300, 180, 250, 120),
]
l_edges = [
    edge("a1", "data", "ra"), edge("b1", "data", "rb"),
    edge("a2", "ra", "na"), edge("b2", "rb", "nb"),
    edge("a3", "na", "gap", kind="conflict"), edge("b3", "nb", "gap", kind="conflict"),
]
l_steps = [
    {"show": ["data"], "set": {"data": "active"}},
    {"show": ["ra", "na", "a1", "a2"], "run": ["a1", "a2"], "set": {"data": "idle", "na": "active"}},
    {"show": ["rb", "nb", "b1", "b2"], "run": ["b1", "b2"], "set": {"na": "idle", "nb": "active"}},
    {"show": ["gap", "a3", "b3"], "run": ["a3", "b3"], "set": {"nb": "idle", "gap": "impossible"}},
]
l_caps = [
    ("The same rows", "<b>Step 1.</b> One file. The question: how many order lines were late?"),
    ("Answer A", "<b>Step 2.</b> Count the lines the status column calls late: <b>98,977</b>."),
    ("Answer B", "<b>Step 3.</b> Count the lines that took longer than planned: <b>103,400</b>."),
    ("Where they differ", "<b>Step 4.</b> The gap is <b>4,423</b> lines: shipments canceled, but past their date. Both answers are correct. The word <b>late</b> has two meanings."),
]
SLIDES.append(slide("The two meanings of late", "Meaning and storage", 5,
    head("Same data, same question, two answers", "How many DataCo order lines were late? It depends on what \"late\" means.") +
    flow("Two definitions of late on the same rows", 1448, 370, l_nodes, l_edges, l_steps, l_caps,
         flags={"impossible": "differ"}),
    '''<p>Five minutes. This is the most important slide of Part 3: a real disagreement, in real data, with no error anywhere.</p>
    <ul>
      <li>Before step 4 ask: which number is right? Let two people argue for A and B. Then show that the difference is exactly the canceled shipments.</li>
      <li>Case B in the failure gallery (the dashboard said 12 percent, operations said 30) is this slide at company scale.</li>
      <li>The fix is not better data. It is writing down which meaning each report uses. That is an ontology's job, Session 3.</li>
    </ul>'''))

# ------------------------------------------------------------------ Four words
SLIDES.append(slide("Four words, defined", "Meaning and storage", 3,
    head("The vocabulary of this course", "Four words you will use every session, from the bottom up.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <ul class="lu-layers">
      <li><span class="lu-layers__name">Knowledge graph · Session 2 onward</span><span class="lu-layers__note">Things joined by named links, plus the ontology that says what they mean.</span></li>
      <li><span class="lu-layers__name">Ontology · Session 3</span><span class="lu-layers__note">A precise, machine readable description of the things in a domain and how they relate.</span></li>
      <li><span class="lu-layers__name">Semantic layer · the goal</span><span class="lu-layers__note">What the data means, readable by a program, above the systems that store it.</span></li>
      <li><span class="lu-layers__name">Schema · what we have today</span><span class="lu-layers__note">Tables, columns, types, keys. The shape, not the meaning.</span></li>
    </ul>
    <div class="lu-stack">
      ''' + callout("Defined on this slide", "Each row is one definition. The glossary link on any later slide takes you back here.", "concept") + '''
      ''' + callout("A test you can apply", "If a new team member must ask a person what a column means, the meaning is in a head, not in a semantic layer.", "neutral", build="1") + '''
    </div>
  </div>''',
    '''<p>Three minutes. Read from the bottom up: what we have (schema), what we want (semantic layer), and the two tools that build it (ontology, knowledge graph).</p>'''))

# ------------------------------------------------------------------ Check: a working join
SLIDES.append(slide("Check: what a working join proves", "Meaning and storage", 2, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-stack">
    <div class="lu-mcq" data-qid="s1-q1" data-answer="b" data-label="What does a join that works on 80 percent of rows establish?"
         data-fb-correct=" A join shows values coincide. Shared meaning is a separate claim."
         data-fb-wrong=" Matching values is about strings. Shared meaning is a modelling claim.">
      <p class="lu-mcq__q">Two systems store suppliers as <code>vendor_id</code> and <code>supplier_code</code>. An engineer joins them and 80 percent of rows match. What has been established?</p>
      <div class="lu-mcq__opts" style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr))">
        <button class="lu-mcq__opt" type="button" data-key="a">The two columns mean the same thing<span class="lu-mcq__why" hidden>A company you pay and a plant that makes the part overlap heavily and stay different things.</span></button>
        <button class="lu-mcq__opt" type="button" data-key="b">Only that 80 percent of the values are equal<span class="lu-mcq__why" hidden>Correct. Meaning must be argued and written down separately.</span></button>
        <button class="lu-mcq__opt" type="button" data-key="c">That the second system is wrong<span class="lu-mcq__why" hidden>Neither is wrong. Both are correct on their own, which is what hides the mismatch.</span></button>
        <button class="lu-mcq__opt" type="button" data-key="d">That the other 20 percent are data errors<span class="lu-mcq__why" hidden>The costly answer: it sends you to clean data instead of to model meaning. Those rows may be correct.</span></button>
      </div>
      <div class="lu-mcq__fb" hidden></div>
    </div>
    ''' + callout("The habit this trains", "<b>Separate what the data shows from what you decided it means.</b> Remember the 4,423 canceled lines: correct rows, different meaning.", "concept") + '''
  </div>''', '''<p>Forty seconds, show of hands, then reveal. Spend the time on <b>d</b>: it is a good engineer's instinct, and it wastes a quarter.</p>''', kind="tint"))

# ================================================================== Part 4
SLIDES.append(divider("Part 4 · The architecture", "Reference architecture",
    "Part 4 of 6 · about 15 minutes",
    "Eight sessions, one pipeline. Where does each session fit?",
    "Each session adds one stage. By Session 8 the whole system starts with one command."))

a_nodes = [
    node("src", "Sources\nToday", 130, 200, 200, 84),
    node("prof", "Profiling\nToday", 420, 70, 220, 84),
    node("map", "Mapping\nSession 5", 420, 330, 220, 84),
    node("ont", "Ontology\nSession 3", 720, 70, 220, 84),
    node("shp", "Shapes\nSession 4", 720, 200, 220, 84),
    node("kg", "Knowledge graph\nSessions 2 and 5", 1030, 200, 250, 84),
    node("learn", "Learning\nSession 6", 1325, 90, 200, 84),
    node("ask", "Questions\nSession 7", 1325, 310, 200, 84),
]
a_edges = [
    edge("e1", "src", "prof"), edge("e2", "src", "map"),
    edge("e3", "prof", "ont", "rules"), edge("e4", "prof", "shp"),
    edge("e5", "ont", "kg", "meaning", route="elbow", sides=["right", "top"]),
    edge("e6", "shp", "kg", "checks"),
    edge("e7", "map", "kg", "tables in", route="elbow", sides=["right", "bottom"]),
    edge("e8", "kg", "learn"), edge("e9", "kg", "ask"),
]
a_steps = [
    {"show": ["src"], "set": {"src": "active"}},
    {"show": ["prof", "e1"], "run": ["e1"], "set": {"src": "idle", "prof": "active"}},
    {"show": ["ont", "shp", "e3", "e4"], "run": ["e3", "e4"], "set": {"prof": "idle", "ont": "active", "shp": "active"}},
    {"show": ["map", "kg", "e2", "e5", "e6", "e7"], "run": ["e2", "e7", "e5", "e6"], "set": {"ont": "idle", "shp": "idle", "kg": "active"}},
    {"show": ["learn", "e8"], "run": ["e8"], "set": {"kg": "idle", "learn": "active"}},
    {"show": ["ask", "e9"], "run": ["e9"], "set": {"learn": "idle", "ask": "active"}},
]
a_caps = [
    ("Where you start", "<b>Step 1.</b> Systems that are each correct and share no names. For us: DataCo and Brunel."),
    ("Profile, find the rules", "<b>Step 2, today.</b> Measure the data and write down the rules it obeys. Your constraint inventory feeds everything after."),
    ("Meaning and checks", "<b>Step 3, Sessions 3 and 4.</b> The rules become two things. The <b>ontology</b> says what things are. The <b>shapes</b> say what data must look like. One adds facts, the other refuses bad data."),
    ("Build the graph", "<b>Step 4, Sessions 2 and 5.</b> A mapping turns the tables into a <b>knowledge graph</b>, given meaning by the ontology and checked by the shapes."),
    ("Predict", "<b>Step 5, Session 6.</b> A model learns from the graph, for example which shipment will be late next."),
    ("Ask in English", "<b>Step 6, Session 7.</b> You ask a question in English; the system writes the query, checks it, and answers or says it does not know. Session 8 ships it all."),
]
SLIDES.append(slide("The architecture, stage by stage", "Reference architecture", 7,
    head("The spine of the course", "From disconnected systems to a question answered in English, in six moves.") +
    flow("The reference architecture, session by session", 1448, 400, a_nodes, a_edges, a_steps, a_caps),
    '''<p>Seven minutes, the spine of the course. One step per session so they can count weeks against the picture.</p>
    <ul>
      <li>Stop at step 3 and ask for the difference between the two boxes before reading the caption. "One is meaning, one is validation" is the answer to build on all term.</li>
      <li>Come back to this slide in later sessions; each recap starts from it.</li>
    </ul>'''))

# ------------------------------------------------------------------ Tools
SLIDES.append(slide("The tools, and which ones are alive", "Reference architecture", 3,
    head("Something a textbook cannot tell you", "One tool per stage. Half the tools in older tutorials are dead.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    ''' + table(["Stage", "Tool we use"], [
        ["Profiling · today", "ydata-profiling, OpenRefine"],
        ["Graph · Session 2", "Apache Jena Fuseki"],
        ["Ontology · Session 3", "Protégé"],
        ["Shapes · Session 4", "pySHACL"],
        ["Mapping · Session 5", "Morph-KGC, Ontop"],
        ["Learning · Session 6", "PyTorch Geometric"],
      ], "Protégé, pySHACL, Ontop, Morph-KGC and PyTorch Geometric all had releases in 2026.") + '''
    <div class="lu-stack">
      ''' + callout("A dead tool you will meet", "DGL: no commits in 2026, last package release May 2024. Tutorials still recommend it.") + '''
      ''' + callout("The habit", "Check the last release and whether it still installs. <b>A confident README is not evidence.</b>", "concept", build="1") + '''
    </div>
  </div>''',
    '''<p>Three minutes. One line per tool; each gets its own slide in the session that uses it.</p>
    <ul><li>If you teach this after September 2026, re-check every status before class. A stale slide about stale tools is embarrassing.</li></ul>'''))

# ------------------------------------------------------------------ Where it pays
SLIDES.append(slide("Where a semantic layer pays", "Reference architecture", 3,
    head("The business case", "Nobody funds an ontology. They fund a question with a deadline.") + '''
  <div class="lu-grid" style="margin-top:var(--lu-s3)">
    <div class="lu-card lu-col-3" data-build="1"><span class="lu-card__label">01 · Traceability</span><h3 class="lu-h3">Which products contain a part from this plant?</h3><p class="lu-sub">A recall makes this a legal deadline.</p></div>
    <div class="lu-card lu-col-3" data-build="2"><span class="lu-card__label">02 · Supplier risk</span><h3 class="lu-h3">If this supplier fails, what loses its only source?</h3><p class="lu-sub">Parts of parts, to any depth.</p></div>
    <div class="lu-card lu-col-3" data-build="3"><span class="lu-card__label">03 · Late delivery</span><h3 class="lu-h3">Which shipment is late next, and why?</h3><p class="lu-sub">Session 6. And which "late"?</p></div>
    <div class="lu-card lu-col-3" data-build="4"><span class="lu-card__label">04 · Wrong answers</span><h3 class="lu-h3">What does a confident wrong answer cost?</h3><p class="lu-sub">More than no answer. Session 7.</p></div>
  </div>''',
    '''<p>Three minutes. Build the cards one at a time. Card 03 links back to the two meanings of late: the business question cannot even be asked until the word is defined.</p>'''))
