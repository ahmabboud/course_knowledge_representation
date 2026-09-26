"""Session 1, Part 6 (your project begins), the lab, and the wrap. About 80 minutes, 60 of them lab."""
from kit import slide, divider, head, defbox, callout, table, flow, node, edge

SLIDES = []

# ================================================================== Part 6
SLIDES.append(divider("Part 6 · The team project", "Team project",
    "Part 6 of 6 · The team project · about 15 minutes",
    "Your team project: the system you build, with whom, and how it is graded.",
    "Teams of 2 or 3. Your own topic and database. The same pipeline you see in the lectures. Team and topic locked before Session 2."))

p_nodes = [
    node("inv", "Constraint\ninventory\nSession 1", 105, 150, 190, 120),
    node("ont", "Ontology\nSession 3", 310, 150, 180, 120),
    node("shp", "Shapes\nSession 4", 510, 150, 180, 120),
    node("map", "Mapping and\nmatching\nSession 5", 715, 150, 190, 120),
    node("ml", "Graph\nmodels\nSession 6", 920, 150, 180, 120),
    node("qa", "Questions\nin English\nSession 7", 1120, 150, 180, 120),
    node("fin", "Deployed\nsystem, report,\ndefense · S8", 1335, 150, 210, 120),
]
p_edges = [edge(f"e{i}", a, b) for i, (a, b) in enumerate(
    [("inv", "ont"), ("ont", "shp"), ("shp", "map"), ("map", "ml"), ("ml", "qa"), ("qa", "fin")])]
p_steps = [
    {"show": ["inv"], "set": {"inv": "active"}},
    {"show": ["ont", "shp", "e0", "e1"], "run": ["e0", "e1"], "set": {"inv": "idle", "shp": "active"}},
    {"show": ["map", "ml", "e2", "e3"], "run": ["e2", "e3"], "set": {"shp": "idle", "ml": "active"}},
    {"show": ["qa", "fin", "e4", "e5"], "run": ["e4", "e5"], "set": {"ml": "idle", "fin": "active"}},
]
p_caps = [
    ("Start today", "<b>Step 1.</b> Your team's first piece: a constraint inventory on <b>your own</b> data, the same method as today's lab."),
    ("Milestone 1 · a checkpoint", "<b>Step 2.</b> End of Session 4: your ontology and shapes. <b>Milestone 1</b>, feedback, not graded."),
    ("Milestone 2 · a checkpoint", "<b>Step 3.</b> End of Session 6: your integrated graph and your prediction models. <b>Milestone 2</b>, a checkpoint, not graded."),
    ("Final · 85 percent", "<b>Step 4.</b> Before Session 8: system and report, 55 percent. Session 8: your defense, 30."),
]
SLIDES.append(slide("The team project: what you build", "Team project", 4,
    head("One system, one layer per session", "Every team builds the same pipeline. What differs is the domain and the data.") +
    flow("The team project, session by session, with its milestones", 1448, 300, p_nodes, p_edges, p_steps, p_caps) +
    callout("Graded once, at the end", "After each lab, repeat it on your own data. The milestones are feedback; the final system is graded once.", "neutral"),
    '''<p>Four minutes. The message: every lab is a rehearsal on the shared case, and the real work is repeating it on your own topic.</p>
    <ul><li>The remaining 15 percent is attendance and running the lab in class, Sessions 1 to 7.</li></ul>'''))

# ------------------------------------------------------------------ Topic menu
SLIDES.append(slide("The topic menu", "Team project", 3,
    head("Choose a topic area, then a database", "Five areas, each checked for open data and a real vocabulary to reuse.") +
    table(["Topic area", "Example open databases", "Vocabulary to reuse"], [
        ["Transit and mobility", "GTFS feeds from one transit agency", "Linked GTFS"],
        ["Bibliographic", "OpenAlex, CrossRef", "SemOpenAlex, BIBFRAME"],
        ["Cultural heritage, music", "MusicBrainz, Europeana", "Music Ontology, EDM"],
        ["Public procurement", "OCDS releases from one government", "OCDS ontology"],
        ["Food products", "Open Food Facts, USDA FoodData Central", "FoodOn"],
      ], "Full menu and licences: PROJECT-REDESIGN.md.") + '''
  ''' + callout("Or bring your own", "Any open database with a real vocabulary to reuse and unwritten rules to find. <b>You check and report every licence.</b>", "concept"),
    '''<p>Three minutes. Do not let them choose in the room; they need to look at the data first. The two tests are what matter: a vocabulary to reuse, and hidden rules to find.</p>'''))

# ------------------------------------------------------------------ Teams and deadline
t_nodes = [
    node("today", "Today\nSession 1", 170, 110, 240, 96),
    node("form", "Form a team of 2 or 3\nand pick a topic", 620, 110, 400, 96),
    node("dl", "Before Session 2\nstarts: locked in", 1100, 110, 320, 96),
    node("late", "No team by then:\nthe instructor places you", 1100, 290, 400, 96),
]
t_edges = [edge("a", "today", "form"), edge("b", "form", "dl"), edge("c", "dl", "late", kind="conflict")]
t_steps = [
    {"show": ["today"], "set": {"today": "active"}},
    {"show": ["form", "a"], "run": ["a"], "set": {"today": "idle", "form": "active"}},
    {"show": ["dl", "b"], "run": ["b"], "set": {"form": "idle", "dl": "active"}},
    {"show": ["late", "c"], "run": ["c"]},
]
t_caps = [
    ("Today", "<b>Step 1.</b> Today you meet the method on the shared case."),
    ("Form a team", "<b>Step 2.</b> Teams of <b>2 or 3</b>, formed by you, any mix. Agree on a topic area and a database."),
    ("The deadline", "<b>Step 3.</b> Team and topic are locked in <b>before Session 2 starts</b>."),
    ("Nobody is left out", "<b>Step 4.</b> Anyone without a team by then is placed by the instructor into a team with space."),
]
SLIDES.append(slide("Teams and the deadline", "Team project", 3,
    head("The rules", "Teams of 2 or 3, your choice, locked in before Session 2.") +
    flow("Team formation timeline", 1448, 350, t_nodes, t_edges, t_steps, t_caps) +
    '<p class="lu-sub">Graded as a team. In the Session 8 defense, <b>any teammate can be asked about any part</b>.</p>',
    '''<p>Three minutes. Say the deadline twice. Ask them to post team and topic where you collect them (your usual channel).</p>'''))

# ------------------------------------------------------------------ Grading
SLIDES.append(slide("How the project is graded", "Team project", 3,
    head("Read this now, not in week 6", "The project is graded once, at the end; the defense is yours alone.") + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    ''' + table(["Course grade", "Percent", "When"], [
        ["Attendance and lab run", "15", "Sessions 1 to 7"],
        ["Team project: system and report", "55", "48 hours before Session 8"],
        ["Individual defense", "30", "Session 8"],
      ]) + '''
    ''' + table(["Team project, one mark per layer", "Points"], [
        ["Ontology", "10"],
        ["Shapes and validation", "10"],
        ["Mapping and integration", "9"],
        ["Learning over the graph", "9"],
        ["Access layer", "9"],
        ["Report and open problem", "8"],
      ], build="1") + '''
  </div>''',
    '''<p>Three minutes. Each layer gets one mark: works (full points), partly (half), missing (none), judged from a clean checkout of the team's repository. The milestones at the end of Sessions 4 and 6 are feedback, not grades. The defense is individual: 2 or 3 questions each in Session 8, one overall mark from 0 to 3.</p>'''))

# ================================================================== Lab
SLIDES.append(divider("Lab · Profile the data, find the rules", "Lab",
    "Hands-on lab · about 60 minutes",
    "Lab: measure DataCo and Brunel, and write down the rules nobody wrote.",
    "Setup check, profiling, clustering in OpenRefine, then your constraint inventory. Each student on their own machine.",
    notes="<p>Ten seconds, then the brief. The lab clock starts on the next slide.</p>"))

SLIDES.append(slide("Lab brief", "Lab", 2,
    head("Hands-on lab · 60 minutes", "Measure two real datasets and write down the rules nobody wrote.", "h1", 34) + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <ol class="lu-list lu-list--num">
      <li><code>python smoke_test.py</code>: checks Python 3.12, JDK 21, Docker, Protégé.</li>
      <li><code>python data/fetch_data.py</code>, from the demos folder.</li>
      <li><code>python profiling.py</code>, or cell by cell in Jupyter.</li>
      <li>Cluster DataCo's <b>Order City</b> in OpenRefine. Check every cluster before you touch it.</li>
      <li>Write at least <b>five</b> rules in <code>constraint_inventory_template.csv</code>: rule, evidence, source.</li>
    </ol>
    <div class="lu-stack">
      ''' + callout("Deliverable, end of session", "Smoke test passing, both profiling reports, and your inventory with evidence for every rule. Committed to your repository.", "concept") + '''
      ''' + callout("What scores", "Rules the schema does not already state, each with a count, and exceptions written down rather than dropped.") + '''
    </div>
  </div>''',
    '''<p>Three minutes to brief, then stop talking and walk the room.</p>
    <ul>
      <li>Most common blocker: the DataCo profile takes several minutes and students think it hung. Say so before they start.</li>
      <li>Second: twenty trivial rules ("Order Id is unique"). Redirect early. A rule the schema already enforces is not a finding.</li>
      <li>Folder: <code>demos/session-01-environment-and-constraints/</code>. Its README has the same steps.</li>
    </ul>'''))

SLIDES.append(slide("Inside the lab: the method, in order", "Lab", 2, '''  <div class="lu-eyebrow">Inside the lab · about 20 minutes in</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-sort" data-qid="s1-sort" data-label="Order the method for finding a hidden rule">
      <p class="lu-h3" style="margin-bottom:var(--lu-s3)">Put the method in the order you actually work in.</p>
      <ul class="lu-sort__list">
        <li class="lu-sort__item" data-rank="4"><span>Write the rule in one sentence, with the count beside it</span></li>
        <li class="lu-sort__item" data-rank="1"><span>Read the column names and write what you think each means</span></li>
        <li class="lu-sort__item" data-rank="5"><span>Hunt for a row that breaks it; decide: row or rule?</span></li>
        <li class="lu-sort__item" data-rank="2"><span>Profile: distinct values, nulls, ranges, distributions</span></li>
        <li class="lu-sort__item" data-rank="3"><span>Find a link the data always obeys that no schema states</span></li>
      </ul>
    </div>
    ''' + callout("Two real examples from today", "Plant and port: 0 exceptions in 9,215 orders, the rule holds. Rate bands: 1,370 of 8,361 in a gap, the rate table is incomplete.", "concept") + '''
  </div>''',
    '''<p>Two minutes, run as a pause once everyone has a profiling report open. Let them argue whether profiling comes before reading the names. It comes after: a guess first, then the numbers.</p>''', kind="tint"))

SLIDES.append(slide("Lab time", "Lab", 60,
    head("Lab · 60 minutes", "Each student works on their own machine. Checkpoints keep you on time.") + '''
  <div class="lu-grid" style="margin-top:var(--lu-s3)">
    <div class="lu-card lu-col-4"><span class="lu-card__label">By minute 15</span><p class="lu-sub">Smoke test passes. Data fetched. Brunel profiles written.</p></div>
    <div class="lu-card lu-col-4"><span class="lu-card__label">By minute 35</span><p class="lu-sub">DataCo profile read. Order City clustered and every cluster checked.</p></div>
    <div class="lu-card lu-col-4"><span class="lu-card__label">By minute 60</span><p class="lu-sub">Five rules or more, each with evidence and source. Committed.</p></div>
  </div>
  ''' + callout("Stuck?", "Start from a slide of Part 5: every measure there is one query in pandas. Your job is to find rules those slides did not show.", "neutral"),
    '''<p>Sixty minutes. Circulate. At minute 35, check that nobody has merged an OpenRefine cluster. At minute 50, warn that commits are due.</p>''', kind="tint"))

# ================================================================== Wrap
SLIDES.append(slide("Failure gallery", "Wrap", 4,
    head("Discussion · which stage broke?", "Three failures. Name the stage of the architecture that broke.") + '''
  <div class="lu-grid" style="margin-top:var(--lu-s3)">
    <div class="lu-card lu-col-4"><span class="lu-card__label">Case A</span><p class="lu-sub">A recall went to 400,000 customers because the one plant at fault could not be traced.</p>
      <div class="lu-reveal"><button class="lu-reveal__btn" type="button">Which stage</button><div class="lu-reveal__panel" hidden><p>Integration. The parts list lived in one system and was never linked to shipments.</p></div></div></div>
    <div class="lu-card lu-col-4"><span class="lu-card__label">Case B</span><p class="lu-sub">A dashboard said 12 percent of shipments were late. Operations said 30. Both computed correctly.</p>
      <div class="lu-reveal"><button class="lu-reveal__btn" type="button">Which stage</button><div class="lu-reveal__panel" hidden><p>The ontology, by its absence. Two meanings of "late", like our 98,977 and 103,400.</p></div></div></div>
    <div class="lu-card lu-col-4"><span class="lu-card__label">Case C</span><p class="lu-sub">An assistant answered fluently about a supplier removed eight months before.</p>
      <div class="lu-reveal"><button class="lu-reveal__btn" type="button">Which stage</button><div class="lu-reveal__panel" hidden><p>The question layer. It could not say "stale" or "I do not know". Session 7 grades that.</p></div></div></div>
  </div>
  <p class="lu-sub"><b>Then, as a room:</b> compare inventories and count the rules only one person found. That number is the argument for writing meaning down.</p>''',
    '''<p>Four minutes. The cases are teaching composites, not named companies. Take each as a show of hands before the reveal.</p>'''))

GLOSS = [
    ("Grain", "What one row of a table stands for."),
    ("Schema", "The declared shape of data, not its meaning."),
    ("Semantic layer", "What the data means, readable by a program."),
    ("Ontology", "A precise description of things and how they relate."),
    ("Knowledge graph", "Things joined by named links, with meaning."),
    ("Data profiling", "Measuring a dataset's real shape."),
    ("Cardinality", "How many different values a column holds."),
    ("Null", "An empty cell."),
    ("Open world", "Missing means unknown, not false."),
    ("Distribution", "How often each value appears."),
    ("Referential integrity", "Every reference points at something that exists."),
    ("Clustering", "Grouping look alike values for a person to judge."),
    ("Constraint inventory", "Rules found in the data, with evidence."),
]
half = (len(GLOSS) + 1) // 2
SLIDES.append(slide("Glossary for this session", "Wrap", 1,
    head("Glossary", "The words this session introduced.") +
    '<div class="lu-split" style="margin-top:var(--lu-s2)">' +
    "".join('<dl class="lu-defs">' + "".join(f"<dt>{t}</dt><dd>{d}</dd>" for t, d in part) + "</dl>"
            for part in (GLOSS[:half], GLOSS[half:])) + '</div>',
    '''<p>One minute, or skip in class: it is for revision. Every term here is also clickable on the slides, and in GLOSSARY.md.</p>'''))

SLIDES.append(slide("Wrap and next session", "Wrap", 2, '''  <div class="lu-eyebrow">Wrap</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">One sentence to leave with.</h2>
      <p class="lu-statement">Integration does not fail because data is dirty. It fails because two correct descriptions of the world met and nobody wrote down how they differed.</p>
      ''' + callout("Before Session 2", "Form your team and choose your topic. Read Hogan et al., Chapters 1 and 2 (free at kgbook.org), and Sequeda and Lassila, Chapter 1.") + '''
    </div>
    <div class="lu-stack">
      <div class="lu-card">
        <span class="lu-card__label">Next session</span>
        <h3 class="lu-h3">Session 2 · RDF, SPARQL and the graph as a data model</h3>
        <p class="lu-sub">Turn today's rows into a graph, give every thing a global name, and ask questions that follow links.</p>
      </div>
      <div class="lu-row"><span class="lu-tag lu-tag--red">Due tonight</span><span class="lu-caption" style="flex:1">Profiling reports and constraint inventory, committed.</span></div>
    </div>
  </div>''', '''<p>Two minutes. End on the statement, not the admin.</p>''', kind="tint"))

SLIDES.append(slide("Self-check", "Wrap", 1, '''  <div class="lu-eyebrow">Self-check</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">How you did on this session's questions</h2>
      <div data-score></div>
    </div>
    <div class="lu-stack">
      ''' + callout("Studying alone?", "Press <kbd>S</kbd> for study mode: every definition shows inline, every reveal opens, every diagram shows its last step. Press <kbd>S</kbd> again to go back.", "concept") + '''
      <p class="lu-caption"><kbd>O</kbd> contents · <kbd>/</kbd> search · <kbd>?</kbd> all shortcuts. Answers are stored in this browser only.</p>
    </div>
  </div>''', '''<p>Close here so students know where the self study tools are.</p>'''))
