"""Session 8: the defense day (instructor, 2026-09-26: defense only, no build). A short deck for the room.

Sources: module-08-defense/DEFENSE-DAY.md (run of show), syllabus-source.json
(sessions[7], the rubric, the policies), the Session 7 checklist, and
the kr-team-template repository, https://github.com/ahmabboud/kr-team-template (the pipeline's five steps; on its example: 1,185 triples,
0 Violation, 189 VoID triples).
"""
from common import slide, divider, defbox, callout, code
from kit import flow, node, edge, head, table, bar
from svgkit import svg, text, rect, FULL, INK2, INK3, RED, RED_BG, BLUE, BLUE_BG, BLUE_TXT, PAPER2, LINE, GREEN, GREEN_BG

SLIDES = []

SLIDES.append('''<section class="slide slide--night" data-chrome="none" data-label="Title" data-section="Opening" data-minutes="2">
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
      <h1 class="lu-display" style="max-width:24ch">The Defense</h1>
      <p class="lu-lead" style="max-width:50ch">No lecture and no build today. Each team shows its system running, and each student answers for it, including the parts they did not build.</p>
    </div>
    <div class="lu-row" style="justify-content:space-between;font-size:var(--lu-t-caption);color:var(--lu-on-night-2)">
      <span>About 180 minutes · team defenses, course close</span>
      <span>Press <kbd>&rarr;</kbd> to begin · <kbd>?</kbd> for shortcuts</span>
    </div>
  </div>
  <template data-notes>
    <p>Before the day: every team handed in 48 hours ago, and Part 1 of each scoring sheet (<code>module-08-defense/scoring-sheet.html</code>) is filled in, with 3 or 4 questions per team. <code>DEFENSE-DAY.md</code> is the run of show. Leave the Defenses slide up during the slots.</p>
  </template>
</section>
''')

# ---------------------------------------------------------------- the day, drawn
parts = [("Opening", 10, PAPER2, INK2), ("Team defenses, one team at a time", 160, BLUE_BG, BLUE_TXT), ("Close", 10, GREEN_BG, "var(--lu-green-900)")]
g, x, W = "", 2.0, FULL - 4
for name, m, fill, col in parts:
    w = W * m / 180
    g += rect(x, 30, w, 90, fill, LINE, rx=6)
    if m > 20:
        g += text(x + w / 2, 66, name, color=col, weight=600)
        g += text(x + w / 2, 96, f"{m} min", "s-label", color=INK3)
    else:
        g += text(x + w / 2, 142, f"{name} · {m}", "s-label", color=INK3)
    x += w
pic = svg(FULL, 160, g, "The day: 10 minutes opening, 160 minutes of team defenses, 10 minutes course close.")
SLIDES.append(slide("The day", "Opening", 3,
    head("Today is the defense, nothing else", "Your system and report were handed in 48 hours ago, and already scored") + '''
  ''' + pic + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    ''' + callout("One team at a time", "About 15 minutes each, in the order on the board. Teams not on may leave and come back for their slot.") + '''
    ''' + callout("Nothing to build", "The stack you handed in is what you show. Start it before your slot, so it is running when you are called.", "neutral") + '''
  </div>''', '''<p>Three minutes. 160 minutes for 8 to 12 teams: 13 to 20 minutes a slot. Up to one extra hour is available if the count needs it, rather than cutting a team short (<code>DEFENSE-DAY.md</code>).</p>'''))

nodes = [node("d1", "demo: it answers\nyour question", 170, 60, 290, 70, kind="builtin"),
         node("d2", "demo: it refuses\none it cannot answer", 540, 60, 310, 70, kind="builtin"),
         node("q", "2 or 3 questions\nper student", 920, 60, 280, 70, kind="builtin"),
         node("m", "one mark\nper student, 0 to 3", 1270, 60, 290, 70, kind="builtin")]
edges = [edge("a1", "d1", "d2", ""), edge("a2", "d2", "q", ""), edge("a3", "q", "m", "")]
steps = [{"show": ["d1"], "set": {"d1": "active"}},
         {"show": ["d2", "a1"], "run": ["a1"], "set": {"d1": "idle", "d2": "active"}},
         {"show": ["q", "a2"], "run": ["a2"], "set": {"d2": "idle", "q": "active"}},
         {"show": ["m", "a3"], "run": ["a3"], "set": {"q": "idle", "m": "inferred"}}]
caps = [("Demo, 3 minutes", "<b>Step 1.</b> Your running stack answers one question the instructor chooses."),
        ("The refusal", "<b>Step 2.</b> Then a question your graph cannot answer: it must refuse, with a reason. This confirms the offline score; it is not marked again."),
        ("Questions", "<b>Step 3.</b> Each of you answers 2 or 3 questions about a part of the system you did not build."),
        ("The mark", "<b>Step 4.</b> One overall mark per student, from all the answers together, not question by question.")]
walk = flow("One team's slot", 1448, 130, nodes, edges, steps, caps, flags={"inferred": "yours"},
            legend={"builtin": "A step", "inferred": "Your own mark"})
SLIDES.append(slide("One team's slot", "Opening", 3, '''  <div class="lu-eyebrow">Walkthrough · about 15 minutes</div>
  <h2 class="lu-h2">Show it running, then answer for it, each of you</h2>
  ''' + walk, '''<p>Three minutes. The questions come from the offline scoring: the weakest layer, a decision that looks borrowed, a number that could not be traced.</p>'''))

rows = [("0", "cannot explain the team's system, even the parts asked about"),
        ("1", "says what the parts do, not why"),
        ("2", "explains why the team decided as it did"),
        ("3", "defends the decisions against an alternative, or a failure in your own system")]
SLIDES.append(slide("How you are marked", "Opening", 2,
    head("Attendance and lab run 15 · team project 55 · your defense 30", "The defense is the one mark that is yours alone") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    ''' + table(["Mark", "You"], rows) + '''
    ''' + callout("Not a quiz of every topic", "Two or three questions sample how well you understand the whole system, including what a teammate or a language model wrote. Defense points: mark &times; 10.", "neutral") + '''
  </div>''', '''<p>Two minutes. The syllabus policy still applies: an ontology the team cannot defend loses its ontology points in the project mark.</p>'''))

SLIDES.append(slide("Defenses", "Team defenses", 160, '''  <div class="lu-eyebrow">Team defenses · leave this slide up</div>
  <h2 class="lu-h1" style="max-width:30ch">When your team is called: stack running, one question, one refusal, then your questions.</h2>
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:var(--lu-s5)">
    <div class="lu-card"><span class="lu-card__label">Why does it exist?</span><p class="lu-sub">A class, a property: which competency question needs it?</p></div>
    <div class="lu-card"><span class="lu-card__label">Why there?</span><p class="lu-sub">This rule: a SHACL shape or an OWL axiom, and why?</p></div>
    <div class="lu-card"><span class="lu-card__label">How do you know?</span><p class="lu-sub">Does your split leak? What does the system do when it does not know?</p></div>
  </div>''', '''<p>160 minutes. Score each student right after the slot, on the scoring sheet (Part 2). Record the questions asked.</p>''', kind="tint"))

# ---------------------------------------------------------------- course close
n = [node("src", "Sources\nSession 1", 130, 200, 200, 84, kind="builtin"),
     node("prof", "Profiling\nSession 1", 420, 70, 220, 84, kind="builtin"),
     node("map", "Mapping\nSession 5", 420, 330, 220, 84, kind="builtin"),
     node("ont", "Ontology\nSession 3", 720, 70, 220, 84, kind="builtin"),
     node("shp", "Shapes\nSession 4", 720, 200, 220, 84, kind="builtin"),
     node("kg", "Knowledge graph\nSessions 2 and 5", 1050, 200, 250, 84, kind="builtin"),
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
