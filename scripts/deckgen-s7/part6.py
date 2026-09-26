"""Session 7: the lab (AGENTS.md 2e: individual, not collected or graded;
every Part B task a twin of something shown in full), the discussion with
the Session 8 checklist, and the wrap."""
from common import slide, divider, callout, code
from kit import head, table

SLIDES = []
S, C, E = '<span class="tok-str">', '<span class="tok-com">', '</span>'

SLIDES.append(divider("Lab · Ask, check, measure", "Lab", "Lab · about 50 minutes · on your own machine",
    "How good is the layer on questions it has never seen, and what does each part add?",
    "Then make it better in three small ways, and measure again."))

SLIDES.append(slide("Lab brief", "Lab", 3,
    head("Hands-on lab · about 50 minutes", "The access layer over Session 2's Brunel graph, with your own Gemini key.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <ol class="lu-list lu-list--num">
      <li><b>Build and observe.</b> VoID (189 triples), the prompt (no call), one question (854), the check, the test set in three settings, the TEXT2SPARQL contract.</li>
      <li><b>Three improvements.</b> An example, a class check, a test question, each a twin of one in the lab; <code>check_my_access.py</code> says right or not yet.</li>
      <li><b>Think.</b> Three questions, one about your own team's graph.</li>
    </ol>
    <div class="lu-stack">
      ''' + callout("Nothing to hand in", "The lab is for understanding. Start with <code>OVERVIEW.md</code> in <code>demos/session-07-access-layer/</code>.", "concept") + '''
      ''' + callout("Key not working?", "Put <code>LLM_MODE=replay</code> in front of a command: it replays the instructor's recorded answers for the lab's own questions.", "neutral") + '''
    </div>
  </div>''', '''<p>Three minutes, then walk the room. Most common blocker: no <code>demos/.env</code>, or the key pasted with quotes or a space. The error message says which. Second: error 429 on the free tier; <code>LLM_DELAY=4</code>.</p>'''))

tw = (f'''def unknown_properties(query, classes, props):
    known = {{p.split("#")[1] for p in props}}
    used = {{t for t in ul_terms(query)
            if t[0].islower()}}
    listed = ", ".join(sorted("ul:" + k
                              for k in known))
    return [f"ul:{{t}} is not a property of "
            f"this graph. The properties are: {{listed}}"
            for t in sorted(used - known)]''')
rows = [("Y1 <code>my_examples.ttl</code>", "<code>ex:3</code>: PLANT08 and <code>ul:servesPort</code>"),
        ("Y2 <code>my_access.py</code>", "this function, for classes"),
        ("Y3 <code>my_questions.yaml</code>", "question 5: PLANT08, id 101")]
SLIDES.append(slide("Part B: each task has a twin", "Lab", 2,
    head("Lab Part B · three improvements", "Copy the twin, change one thing") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s2)">
    ''' + code("access_layer.py · the twin of Y2, wrapped to fit", tw) + '''
    <div class="lu-stack">
      ''' + table(["Write", "Copy, then change"], rows) + '''
      ''' + callout("Then measure", "<code>python evaluate.py --setting repair --add-class-check --questions my_questions.yaml</code>", "neutral") + '''
    </div>
  </div>''', '''<p>Two minutes. For Y2, three things change: classes instead of props, <code>isupper</code> instead of <code>islower</code>, "class" in the message. Most common wrong answer: keeping <code>islower</code>; the checker says it reports <code>ul:shippedBy</code>, a property.</p>'''))

SLIDES.append(slide("Lab time", "Lab", 44,
    head("Lab · 44 minutes", "Each student on their own machine. Checkpoints keep you on time.") + '''
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:var(--lu-s4)">
    <div class="lu-card"><span class="lu-card__label">By minute 26 · Part A</span><p class="lu-sub">189 triples; examples 1, 2, 4; 854; one problem found; three F1 lines; the JSON contract in a browser.</p></div>
    <div class="lu-card"><span class="lu-card__label">By minute 38 · Part B</span><p class="lu-sub"><code>python check_my_access.py</code> says 3 of 3, then one more evaluate run.</p></div>
    <div class="lu-card"><span class="lu-card__label">By minute 44 · Part C</span><p class="lu-sub">Your three settings' F1 on the board, and your answer about your own graph.</p></div>
  </div>
  ''' + callout("For your team project", "Session 8 runs this layer in front of your graph: your void.ttl, your examples, your test set, and the Compose service in <code>deploy/</code>.", "concept"),
    '''<p>Forty four minutes. <code>evaluate.py</code> makes about 50 calls; start it early and read <code>access_layer.py</code> while it runs. Collect each student's three F1 numbers on the board for the discussion.</p>'''))

rows = [("One command starts the whole stack from a clean checkout", "Sessions 2 to 7"),
        ("Every service listens on 127.0.0.1 only; keys only in .env", "2, 7"),
        ("The SHACL gate runs before data reaches the endpoint", "4"),
        ("The test set's score is recorded, with the model and the date", "7"),
        ("A real unanswerable question is refused, with a reason", "7")]
SLIDES.append(slide("Discussion and the Session 8 checklist", "Wrap", 7, '''  <div class="lu-eyebrow">Discussion · the room's scores, then the checklist</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">Our F1 on the board, against 0.790</h2>
      <ol class="lu-list lu-list--num">
        <li>How far apart are two students' runs of the same setting?</li>
        <li>Which part added most: examples, or repair?</li>
        <li>What would it take to score 0.790 on your own graph, and would it mean the same?</li>
      </ol>
    </div>
    ''' + table(["The Session 8 checklist", "From"], rows) + '''
  </div>''', '''<p>Seven minutes. The syllabus: read the room's scores against the TEXT2SPARQL 2026 leaderboard, then agree the deployment checklist each team is held to in Session 8. Adjust the list with the room and write the agreed version into the course page; Session 8's defense tries each item on a clean checkout.</p>'''))

GLOSS = [
    ("Text to SPARQL", "A question in words becomes a query."),
    ("Large language model", "A model that writes text and code."),
    ("VoID", "The graph's classes, properties, counts."),
    ("Prompt · grounding", "What the model is sent · facts it must use."),
    ("Few-shot examples", "Worked pairs to imitate."),
    ("Hallucination", "Fluent, and not true."),
    ("Validation · repair loop", "Check the query · send problems back."),
    ("Refusal", "The graph cannot answer, and why."),
    ("Execution accuracy", "Judge the answer, not the text."),
    ("TEXT2SPARQL", "The benchmark, its contract and scorer."),
    ("Container topology", "Which part runs where."),
    ("Data drift · access control", "Data changing · who may read what."),
]
half = (len(GLOSS) + 1) // 2
SLIDES.append(slide("Glossary for this session", "Wrap", 1,
    head("Glossary", "The main words this session introduced. Every one is clickable on the slides.") +
    '<div class="lu-split" style="margin-top:var(--lu-s2)">' +
    "".join('<dl class="lu-defs">' + "".join(f"<dt>{t}</dt><dd>{d}</dd>" for t, d in part) + "</dl>"
            for part in (GLOSS[:half], GLOSS[half:])) + '</div>',
    '''<p>One minute, or skip in class: it is for revision. The full list is in <code>GLOSSARY.md</code>.</p>'''))

SLIDES.append(slide("Wrap and next session", "Wrap", 2, '''  <div class="lu-eyebrow">Wrap</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">One sentence to leave with.</h2>
      <p class="lu-statement">Trust the layer around the model, not the model: ground it, check it, let it refuse, and measure it.</p>
      ''' + callout("Reading", "Kejriwal, Knoblock and Szekely (2021), chapters 12 and 13, structured querying and question answering. Hogan and others (2021), chapter 9, publication.") + '''
    </div>
    <div class="lu-stack">
      <div class="lu-card">
        <span class="lu-card__label">Next session</span>
        <h3 class="lu-h3">Session 8 · The defense</h3>
        <p class="lu-sub">No lecture, no build: your team hands in the stack 48 hours before, with this layer in front, and every teammate answers for every part.</p>
      </div>
      <div class="lu-row"><span class="lu-tag lu-tag--green">For your team</span><span class="lu-caption" style="flex:1">Put the access layer in your stack, and write up your open problem.</span></div>
    </div>
  </div>''', '''<p>Two minutes. End on the sentence. Remind teams: a stack that has never come up from a clean checkout will not come up on defense day either.</p>''', kind="tint"))

SLIDES.append(slide("Self-check", "Wrap", 1, '''  <div class="lu-eyebrow">Self-check</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">How you did on this session's questions</h2>
      <div data-score></div>
    </div>
    <div class="lu-stack">
      ''' + callout("Studying alone?", "Press <kbd>S</kbd> for study mode: every definition shows inline, every reveal opens, every diagram shows its last step.", "concept") + '''
      <p class="lu-caption"><kbd>O</kbd> contents · <kbd>/</kbd> search · <kbd>?</kbd> all shortcuts. Answers are stored in this browser only.</p>
    </div>
  </div>''', '''<p>Close here so students know where the self study tools are.</p>'''))
