"""Session 8: the defense day. A short deck for the room, not a lecture.

Sources: module-08-defense/DEFENSE-DAY.md (run of show), syllabus-source.json
(sessions[7], the rubric, the policies), the Session 7 checklist, and
kr-team-template/ (the pipeline's five steps; on its example: 1,185 triples,
0 Violation, 189 VoID triples).
"""
from common import slide, divider, defbox, callout, code
from kit import flow, node, edge, head, table, bar
from svgkit import svg, text, rect, FULL, INK2, INK3, RED, RED_BG, BLUE, BLUE_BG, BLUE_TXT, PAPER2, LINE, GREEN, GREEN_BG

SLIDES = []

SLIDES.append('''<section class="slide slide--night" data-chrome="none" data-label="Title" data-section="Standup" data-minutes="2">
  <div class="slide__body" style="justify-content:space-between">
    <div class="lu-row" style="justify-content:space-between;align-items:flex-start">
      <div class="lu-lockup">
        <span class="lu-lockup__mark">LU</span>
        <span class="lu-lockup__text">
          <span class="lu-lockup__name">Lebanese University</span>
          <span class="lu-lockup__unit">Faculty of Sciences · MSc Computer Science</span>
        </span>
      </div>
      <div class="lu-tag lu-tag--red" style="background:transparent;color:#FF9AA7;border-color:#96122B">Module 5 · Defense</div>
    </div>
    <div class="lu-stack">
      <div class="lu-eyebrow">Knowledge Representation · Session 8 of 8</div>
      <h1 class="lu-display" style="max-width:24ch">Build, Deploy, Defend</h1>
      <p class="lu-lead" style="max-width:50ch">No lecture today. Every team brings its whole system up from a clean checkout with one command, and every teammate answers for every part of it.</p>
    </div>
    <div class="lu-row" style="justify-content:space-between;font-size:var(--lu-t-caption);color:var(--lu-on-night-2)">
      <span>About 180 minutes · standup, build and defense, course close</span>
      <span>Press <kbd>&rarr;</kbd> to begin · <kbd>?</kbd> for shortcuts</span>
    </div>
  </div>
  <template data-notes>
    <p>Before the block: every team's repository is pushed; the scoring sheets (<code>module-08-defense/scoring-sheet.html</code>, one printed page per team) are on the desk; <code>DEFENSE-DAY.md</code> is the run of show. This deck is for the room: leave slide 8 (build time) up during the block.</p>
  </template>
</section>
''')

# ---------------------------------------------------------------- the day, drawn
parts = [("Standup", 20, PAPER2, INK2), ("Build and defense, in parallel", 150, BLUE_BG, BLUE_TXT), ("Close", 10, GREEN_BG, "var(--lu-green-900)")]
g, x, W = "", 2.0, FULL - 4
for name, m, fill, col in parts:
    w = W * m / 180
    g += rect(x, 30, w, 90, fill, LINE, rx=6)
    g += text(x + w / 2, 66, name, color=col, weight=600)
    g += text(x + w / 2, 96, f"{m} min", "s-label", color=INK3)
    x += w
pic = svg(FULL, 140, g, "The day: 20 minutes standup, 150 minutes build and defense in parallel, 10 minutes course close.")
SLIDES.append(slide("The day", "Standup", 3,
    head("One room, every team building at once", "The instructor moves from team to team; nobody waits for a turn") + '''
  ''' + pic + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    ''' + callout("While you build", "The instructor visits each team for 10 to 12 minutes: that is your defense. Between visits, ask for help like any lab.") + '''
    ''' + callout("Also today", "Finish the technical report in the same block: it documents what is deployed, so write it from what comes up, not from the plan.", "neutral") + '''
  </div>''', '''<p>Three minutes. At 4 to 12 teams, the defense visits take 40 to 144 minutes of the 150; up to one extra hour is available if the team count needs it (<code>DEFENSE-DAY.md</code>).</p>'''))

SLIDES.append(slide("Standup: one minute per team", "Standup", 15, '''  <div class="lu-eyebrow">Standup · 20 minutes</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">Each team, in under a minute</h2>
      <ol class="lu-list lu-list--num">
        <li>What is deployed and comes up.</li>
        <li>What is not.</li>
        <li>Your single largest blocker.</li>
      </ol>
    </div>
    <div class="lu-card">
      <span class="lu-card__label">Then, out loud</span>
      <p class="lu-sub">The blockers are put in the order the instructor will reach them, so each team knows whether to work around its blocker or wait.</p>
    </div>
  </div>''', '''<p>Fifteen minutes for the round, then the triage. Write the blocker order on the board next to the visit order.</p>''', kind="tint"))

# ---------------------------------------------------------------- the clean checkout
nodes = [node("c", "git clone", 130, 50, 200, 56, kind="builtin"),
         node("e", "cp .env.example .env\n(your key)", 430, 50, 300, 70, kind="builtin"),
         node("u", "docker compose up --build", 830, 50, 380, 56, kind="builtin"),
         node("p", "pipeline: map, gate,\nVoID, load", 830, 170, 330, 70, kind="builtin"),
         node("a", "access layer answers\non 127.0.0.1:8000", 1250, 170, 330, 70, kind="builtin"),
         node("x", "stops: a Violation,\na missing file, a path", 430, 170, 360, 70, kind="builtin")]
edges = [edge("a1", "c", "e", ""), edge("a2", "e", "u", ""), edge("a3", "u", "p", ""),
         edge("a4", "p", "a", "passes"), edge("a5", "p", "x", "fails")]
steps = [{"show": ["c", "e", "a1"], "run": ["a1"], "set": {"c": "active"}},
         {"show": ["u", "a2"], "run": ["a2"], "set": {"c": "idle", "u": "active"}},
         {"show": ["p", "a3"], "run": ["a3"], "set": {"u": "idle", "p": "active"}},
         {"show": ["x", "a5"], "run": ["a5"], "set": {"x": "impossible"}},
         {"show": ["a", "a4"], "run": ["a4"], "set": {"p": "idle", "a": "inferred"}}]
caps = [("Fresh", "<b>Step 1.</b> A new folder, as the instructor will: clone, then only the <code>.env</code> file, which is never committed."),
        ("One command", "<b>Step 2.</b> Nothing typed by hand after this. No manual step survives a clean checkout."),
        ("The pipeline", "<b>Step 3.</b> Map the source, run the SHACL gate, describe with VoID, load the endpoint."),
        ("Where it breaks", "<b>Step 4.</b> This is where most of the day goes: a package not declared, a path that exists only on one laptop, data that fails the gate."),
        ("Up", "<b>Step 5.</b> The access layer answers. Try it from the browser, then try the unanswerable question.")]
walk = flow("A clean checkout", 1448, 230, nodes, edges, steps, caps,
            flags={"impossible": "stops", "inferred": "up"},
            legend={"builtin": "A step", "impossible": "It stops", "inferred": "It is up"})
SLIDES.append(slide("The clean checkout", "Build and defense", 5, '''  <div class="lu-eyebrow">Walkthrough · the test your stack must pass</div>
  <h2 class="lu-h2">Clone it into an empty folder and run one command, as the instructor will</h2>
  ''' + walk, '''<p>Five minutes. The template's pipeline prints its five steps; on its own example: 1,185 triples, 0 Violation, 189 VoID triples, then the endpoint is loaded. A team that has never tried a clean checkout will find its first undeclared dependency today, not later.</p>'''))

rows = [("One command starts the whole stack from a clean checkout", "2 to 7"),
        ("Every service listens on 127.0.0.1 only; keys only in <code>.env</code>", "2, 7"),
        ("The SHACL gate runs before data reaches the endpoint, and in CI", "4"),
        ("The test set's score is recorded, with the model and the date", "7"),
        ("A real unanswerable question is refused, with a reason", "7")]
SLIDES.append(slide("The Session 8 checklist", "Build and defense", 5,
    head("The checklist agreed in Session 7", "The defense tries each item on your machine, from a clean checkout") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    ''' + table(["Item", "Session"], rows) + '''
    ''' + callout("Check it yourself first", "Run the five items now, in this order, before the instructor reaches your team. The template's README lists them too.", "neutral") + '''
  </div>''', '''<p>Five minutes. These are the five items the room agreed at the end of Session 7; if the room changed any of them then, edit this slide's generator to match.</p>'''))

SLIDES.append(slide("How the defense works", "Build and defense", 5,
    head("10 to 12 minutes per team, at your table", "Any teammate can be asked about any part: the data, the ontology, the shapes, the mapping, the model, the access layer") + '''
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:var(--lu-s3)">
    <div class="lu-card"><span class="lu-card__label">One question per rubric line</span><p class="lu-sub">Enough to cover the system in a visit; the artifact itself is graded separately, by cloning and running it.</p></div>
    <div class="lu-card"><span class="lu-card__label">Spread across the team</span><p class="lu-sub">Each teammate answers about a part they did not build. Who answered what is recorded.</p></div>
    <div class="lu-card"><span class="lu-card__label">Decisions, not just code</span><p class="lu-sub">Explain why, including a choice a language model suggested. An ontology the team cannot defend scores zero on that line.</p></div>
  </div>''', '''<p>Five minutes. The scoring sheet has a row per question: the question, the rubric line, who answered, and a mark from 0 to 2. The defense is its own 10 percent of the grade, outside the 100-point rubric.</p>'''))

rows = [("Why does this class exist? Which competency question needs it?", "Ontology"),
        ("This constraint: why a SHACL shape and not an OWL axiom, or the reverse?", "SHACL"),
        ("Materialized or virtualized in your deployed system, and why?", "Integration"),
        ("Does your split leak? What did the baseline score?", "Prediction"),
        ("What does the system do when it does not know?", "Access layer"),
        ("This step fails on a clean checkout: what happens?", "Deployment")]
SLIDES.append(slide("Questions to expect", "Build and defense", 5,
    head("The kind of question each line gets", "Short to ask, impossible to answer without having done the work") + '''
  ''' + table(["Question", "Rubric line"], rows),
    '''<p>Five minutes. Drawn from <code>DEFENSE-DAY.md</code> and the syllabus. Add one on full-scale validation for any part a smoke test stood in for.</p>'''))

pts = [("Ontology quality", 18), ("Constraint validation with SHACL", 15), ("Prediction and evaluation honesty", 13),
       ("Data understanding and constraint discovery", 12), ("Operational data integration", 12),
       ("Access layer", 9), ("Deployment and reproducibility", 9), ("Problem framing and scope", 7), ("Literature and open problem", 5)]
bars = "".join(f'<div class="lu-stack" style="gap:2px"><span class="lu-caption">{n}</span>' + bar(v, 18, f"{v}", "red" if v >= 15 else "ink") + '</div>' for n, v in pts)
SLIDES.append(slide("The rubric", "Build and defense", 5,
    head("100 points for the system and the report", "Plus the defense: a separate 10 percent of the grade") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s2)">
    <div class="lu-stack" style="gap:var(--lu-s2)">''' + bars + '''</div>
    <div class="lu-stack">
      ''' + callout("Full marks for losing", "A graph model that loses to the baseline, reported as such with an explanation, scores full marks on prediction.") + '''
      ''' + callout("Graded by running it", "The system is graded by cloning it fresh and running it. What does not come up cannot score.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. The rubric is the syllabus's (<code>syllabus-source.json</code>, capstone rubric, 100 points); the assessment table gives it 35 percent of the grade, the defense 10.</p>'''))

rows = [("Length", "At most 16 pages, the open problem included"),
        ("What it documents", "What was deployed, not what was planned"),
        ("Numbers", "Only numbers a file in your repository holds"),
        ("Open problem", "At most 2 pages: a question, your own position, at least 3 primary sources"),
        ("Licences", "Every ontology, vocabulary and dataset, with its licence")]
SLIDES.append(slide("The technical report", "Build and defense", 5,
    head("Finish it today, from what comes up", "report/REPORT.md in the template has one section per rubric line") + '''
  ''' + table(["", "The rule"], rows),
    '''<p>Five minutes. The report is read, not presented: the defense refers to it.</p>'''))

SLIDES.append(slide("Build time", "Build and defense", 120, '''  <div class="lu-eyebrow">Build and defense · leave this slide up</div>
  <h2 class="lu-h1" style="max-width:30ch">Clean checkout first. Then the checklist. Then the report.</h2>
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:var(--lu-s5)">
    <div class="lu-card"><span class="lu-card__label">1 · Comes up</span><p class="lu-sub">An empty folder, clone, <code>.env</code>, <code>docker compose up --build</code>.</p></div>
    <div class="lu-card"><span class="lu-card__label">2 · The five items</span><p class="lu-sub">Gate, ports, keys, recorded score, a real refusal.</p></div>
    <div class="lu-card"><span class="lu-card__label">3 · Written down</span><p class="lu-sub">The report says what came up, with the numbers your files hold.</p></div>
  </div>''', '''<p>The block: 150 minutes in all, of which the slides before this one take about 30. Visit teams in the triage order; score each right after its visit.</p>''', kind="tint"))

# ---------------------------------------------------------------- course close
n = [node("src", "Sources\nSession 1", 130, 200, 200, 84, kind="builtin"),
     node("prof", "Profiling\nSession 1", 420, 70, 220, 84, kind="builtin"),
     node("map", "Mapping\nSession 5", 420, 330, 220, 84, kind="builtin"),
     node("ont", "Ontology\nSession 3", 720, 70, 220, 84, kind="builtin"),
     node("shp", "Shapes\nSession 4", 720, 200, 220, 84, kind="builtin"),
     node("kg", "Knowledge graph\nSessions 2 and 5", 1030, 200, 250, 84, kind="builtin"),
     node("learn", "Learning\nSession 6", 1325, 90, 200, 84, kind="builtin"),
     node("ask", "Questions\nSession 7", 1325, 310, 200, 84, kind="builtin")]
e = [edge("e1", "src", "prof"), edge("e2", "src", "map"), edge("e3", "prof", "ont", "rules"), edge("e4", "prof", "shp"),
     edge("e5", "ont", "kg", "meaning", route="elbow", sides=["right", "top"]), edge("e6", "shp", "kg", "checks"),
     edge("e7", "map", "kg", "tables in", route="elbow", sides=["right", "bottom"]), edge("e8", "kg", "learn"), edge("e9", "kg", "ask")]
allids = [x["id"] for x in n] + [x["id"] for x in e]
steps = [{"show": allids, "set": {x["id"]: "active" for x in n}}]
arch = flow("The reference architecture", 1448, 400, n, e, steps, legend=False)
SLIDES.append(slide("The architecture, built", "Course close", 6, '''  <div class="lu-eyebrow">Course close · Session 1's picture, again</div>
  <h2 class="lu-h2">In Session 1 this was a promise. Today every box runs, on your own data.</h2>
  ''' + arch + '''
  ''' + callout("Look back at your own", "Which box was hardest for your data? Which would you build differently now?", "neutral"),
    '''<p>Six minutes. The same diagram as Session 1's "The architecture, stage by stage", every stage now lit. Ask two teams: which box cost you most, and why.</p>'''))

cards = [("SHACL 1.2", "A W3C Working Draft (September 2026). Watch what it adds to the shapes you wrote, as it moves toward a Recommendation."),
         ("The RML Working Group", "Mappings for CSV, JSON and XML becoming a W3C standard; its charter was being refined in 2026."),
         ("Time and space", "Facts that change over time, and places: what this course left out. GeoSPARQL covers the spatial side."),
         ("Neurosymbolic work", "Models that respect rules by construction, not by being checked afterwards as ours were.")]
grid = "".join(f'<div class="lu-card"><span class="lu-card__label">{a}</span><p class="lu-sub">{b}</p></div>' for a, b in cards)
SLIDES.append(slide("Where to go next", "Course close", 3,
    head("Further study", "Four directions the field is moving in, each touching a layer you built") + f'''
  <div class="lu-cards" style="grid-template-columns:repeat(2,minmax(0,1fr));margin-top:var(--lu-s3)">{grid}</div>''',
    '''<p>Three minutes. The four study paths the syllabus names for the course close. The Session 7 open problems slides have the references.</p>'''))

SLIDES.append(slide("Thank you", "Course close", 1, '''  <div class="lu-eyebrow">Knowledge Representation · end of the course</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">Meaning, written down, checked, and asked for.</h2>
      <p class="lu-statement">You built a system that says what its data means, refuses data that breaks its rules, learns honestly, and answers in plain words, or says it cannot.</p>
    </div>
    ''' + callout("After today", "Grades follow the Assessment section of the syllabus. Keep your repository: it is a portfolio piece.", "neutral") + '''
  </div>''', '''<p>One minute. End on the sentence.</p>''', kind="tint"))
