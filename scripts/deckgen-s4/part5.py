"""Session 4, Part 5: reuse (GS1's EPCIS shapes, shacl-play) and the gate.

Numbers: EPCIS-SHACL counted in the browser on 2026-09-25 from
https://ref.gs1.org/standards/epcis/epcis-shacl.ttl (fetch_epcis.py prints
the same counts); the two GitHub Actions runs are in
reference-outputs/ci-runs.txt.
"""
from common import slide, divider, defbox, callout, code, placeholder
from kit import flow, node, edge, head

SLIDES = []

K = '<span class="tok-kw">'
S = '<span class="tok-str">'
C = '<span class="tok-com">'
N = '<span class="tok-num">'
E = '</span>'
REPO = "https://github.com/ahmabboud/course_knowledge_representation"
GREEN_RUN = REPO + "/actions/runs/36143273457"
RED_RUN = REPO + "/actions/runs/36143360459"

SLIDES.append(divider("Part 5 · Reuse and the gate", "Reuse and the gate",
    "Part 5 of 5 · about 17 minutes",
    "Who stops the next bad triple before it reaches the graph?",
    "Not a person. A check that runs on every change."))

# ---------------------------------------------------------------- EPCIS as a reference
nums = [("1,138", "lines"), ("30", "node shapes"), ("71", "property shapes"), ("0", "SPARQL rules"), ("0", "severities set")]
cards = "".join(f'<div class="lu-card"><div class="lu-display" style="color:var(--lu-ink)">{v}</div><p class="lu-sub">{t}</p></div>' for v, t in nums)
ex = (f'''epcis:EventTimeShape {K}a{E} sh:PropertyShape ;
    sh:path epcis:eventTime ;
    sh:datatype xsd:dateTimeStamp ;
    sh:minCount {N}1{E} ; sh:maxCount {N}1{E} ;
    sh:message {S}"In all EPCIS events, eventTime is mandatory,
      single valued and an xsd:dateTimeStamp"{E} .''')
SLIDES.append(slide("GS1's EPCIS shapes, an industrial example", "Reuse and the gate", 4,
    head("Reuse: read before you write", "GS1 publishes the shapes for EPCIS 2.0, its standard for supply chain events") + f'''
  <div class="lu-cards" style="grid-template-columns:repeat(5,minmax(0,1fr))">{cards}</div>
  <div class="lu-split lu-split--wide-left">
    ''' + code("epcis-shacl.ttl · one of its 71 property shapes", ex, small=False) + '''
    <div class="lu-stack">
      ''' + defbox([("EPCIS", "GS1's standard for recording supply chain events: what was seen, where, when and why.")]) + '''
      ''' + callout("Licence", "The repository's <code>LICENSE</code> file is GS1's intellectual property disclaimer, not an open source licence. Borrow the patterns freely; read GS1's intellectual property policy before shipping the file.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. Counted on 2026-09-25 from <code>https://ref.gs1.org/standards/epcis/epcis-shacl.ttl</code> (the same file as <code>Ontology/EPCIS-SHACL.ttl</code> in github.com/gs1/EPCIS); <code>python fetch_epcis.py</code> downloads it and prints the same counts.</p>
<ul><li>The two zeros are the lesson of Part 3 at industrial scale: a large, standard shapes file needs no SPARQL rule and uses only the default severity.</li>
<li>Licence literacy again, as in Session 3: this is not MIT or Apache; it is a patent and intellectual property statement. Name the difference.</li></ul>'''))

# ---------------------------------------------------------------- Three patterns worth borrowing
p1 = (f'''epcis:ObjectEventShape
    sh:property epcis:EventTimeShape ;
epcis:AggregationEventShape
    sh:property epcis:EventTimeShape ;''')
p2 = (f'''epcis:ChildEPCsForbiddenShape
    sh:path epcis:childEPCs ;
    sh:maxCount {N}0{E} .''')
p3 = (f'''sh:message {S}"childEPCs should not
  appear within ObjectEvent,
  TransactionEvent or
  TransformationEvent"{E}''')
cells = [
    ("1 · Write a rule once, reuse it by name", code("27 property shapes used by 2 to 5 node shapes", p1),
     "Our order and late order rules could share one carrier rule the same way."),
    ("2 · Say what must not be there", code("13 &ldquo;forbidden&rdquo; shapes", p2),
     "<code>sh:maxCount 0</code> forbids a property: EPCIS keeps fields out of the event types where they make no sense."),
    ("3 · A message a person can act on", code("77 shapes carry one", p3),
     "A report is read by whoever fixes the data. Write the fix into the message."),
]
grid = "".join(f'<div class="lu-card"><span class="lu-card__label">{t}</span>{c}<p class="lu-sub">{d}</p></div>' for t, c, d in cells)
SLIDES.append(slide("Three patterns worth borrowing", "Reuse and the gate", 4,
    head("What EPCIS does that our first draft did not", "Three habits from a real standard, each one line of Turtle") + f'''
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:var(--lu-s3)">{grid}</div>''',
    '''<p>Four minutes. All three counts from the real file (27 reused shapes, 13 forbidden shapes, 77 messages). The syllabus asks students to note three patterns worth borrowing: these are the three.</p>
<ul><li>Pattern 2 is new to most students: SHACL can forbid, not only require.</li></ul>'''))

# ---------------------------------------------------------------- The tool: shacl-play
SLIDES.append(slide("The tool: shacl-play", "Reuse and the gate", 3, '''  <div class="lu-eyebrow">One slide for the tool</div>
  <h2 class="lu-h2">shacl-play validates in the browser: paste the data, paste the shapes, read the report</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + placeholder("Screenshot: shacl-play's report for the broken CI sample",
        "On shacl-play.sparna.fr/play/validate: paste <code>ci/sample-orders-broken.ttl</code> as data and <code>brunel-shapes.ttl</code> as shapes, press Validate. Capture the report page showing 1 Violation on order 1447385217.7, save as <code>assets/img/s4-shacl-play-report.png</code>.",
        "shacl-play (v0.12.4 on 2026-09-25) runs TopQuadrant's SHACL engine, a second implementation next to pySHACL.") + '''
    <div class="lu-stack">
      ''' + callout("Use it for", "Trying one shape on a small file, and showing a report to someone who will not install Python.", "concept") + '''
      ''' + callout("Not for", "The full 6 megabyte graph, or a gate. The gate is a script in the repository.", "neutral") + '''
    </div>
  </div>''', '''<p>Three minutes. A web tool, so one slide (AGENTS.md 2c rule 5). Demo it live if the network holds: paste the broken sample and the shapes.</p>
<ul><li>It warns "Shapes did not match anything!" when a shape targets nothing: the targeting trap of Part 2, caught by the tool.</li>
<li>Two engines agreeing (pySHACL and TopQuadrant's) is itself a check on our shapes.</li></ul>'''))

# ---------------------------------------------------------------- The gate
n = [
    node("c", "a push changes one value:\nV444_0 typed V444_O", 200, 45, 360, 70, kind="builtin"),
    node("a", "GitHub Actions\nruns validate.py", 580, 45, 290, 70, kind="builtin"),
    node("r", "1 Violation: Class\non carried by", 930, 45, 300, 70, kind="builtin", flag="bottom"),
    node("m", "exit code 1:\nred run, no merge", 1290, 45, 290, 70, kind="builtin", flag="bottom"),
]
e = [edge("x", "c", "a", ""), edge("y", "a", "r", ""), edge("z", "r", "m", "")]
steps = [
    {"show": ["c"], "set": {"c": "active"}},
    {"show": ["a", "x"], "run": ["x"], "set": {"c": "idle", "a": "active"}},
    {"show": ["r", "y"], "run": ["y"], "set": {"a": "idle", "r": "impossible"}},
    {"show": ["m", "z"], "run": ["z"], "set": {"m": "impossible"}},
]
caps = [
    ("One typo", "<b>Step 1.</b> A commit changes one character: order 1447385217.7 is carried by V444_O (letter O), not V444_0 (zero). Nobody would see it in a spreadsheet."),
    ("The check runs", "<b>Step 2.</b> The push starts the workflow <code>shacl-gate.yml</code>: GitHub installs pySHACL and runs <code>validate.py</code> on the sample orders."),
    ("The report", "<b>Step 3.</b> V444_O is not a Carrier: one Violation, Class on <b>carried by</b>."),
    ("Blocked", "<b>Step 4.</b> The script exits with code 1, so GitHub marks the run red. A red pull request is not merged."),
]
walk = flow("A bad commit, stopped", 1448, 130, n, e, steps, caps, flags={"impossible": "blocked"},
            legend={"builtin": "Step of the gate", "impossible": "Blocked"})
SLIDES.append(slide("The gate blocking a bad commit", "Reuse and the gate", 5, '''  <div class="lu-eyebrow">A real run on GitHub</div>
  <h2 class="lu-h2">Every push runs the shapes. One wrong character turns the run red.</h2>
  ''' + walk + '''
  <div class="lu-split">
    ''' + defbox([("Validation gate", "A check every change must pass before it is accepted; here, validation with no Violation.")]) + '''
    ''' + callout("Open both runs", f'<a href="{RED_RUN}">Red: branch demo/broken-carrier-code</a> · <a href="{GREEN_RUN}">Green: main</a>. Same shapes, same six orders, one value different.', "neutral") + '''
  </div>''', '''<p>Five minutes. Open the red run live and click into the failed step: the report printed there is the same as <code>python validate.py --data ci/sample-orders-broken.ttl</code> on a laptop.</p>
<ul><li>Both runs are real (2026-09-25, <code>reference-outputs/ci-runs.txt</code>). The demo branch is kept on purpose and never merged.</li>
<li>Why a sample: the gate runs on six real orders (515 triples) in a second. The full graph is 6 megabytes and takes about two minutes; teams decide what their gate checks.</li></ul>'''))

# ---------------------------------------------------------------- What the gate runs
wf = (f'''{K}on{E}:
  push:
    paths: [ {S}"demos/session-04-shacl/**"{E} ]
{K}jobs{E}:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {{ python-version: {S}"3.12"{E} }}
      - run: pip install pyshacl==0.40.1 rdflib==7.6.0
      - working-directory: demos/session-04-shacl
        run: python validate.py --data ci/sample-orders.ttl''')
SLIDES.append(slide("What the gate runs", "Reuse and the gate", 3, '''  <div class="lu-eyebrow">The whole gate is one file</div>
  <h2 class="lu-h2">Four steps: get the code, get Python, install pySHACL, validate</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code(".github/workflows/shacl-gate.yml · shortened", wf, small=False) + '''
    <div class="lu-stack">
      ''' + defbox([
        ("CI", "Continuous integration: checks that run automatically on every change, and fail the build when a rule breaks."),
        ("GitHub Actions", "GitHub's service that runs such checks on every push; a failed check marks the commit red."),
      ]) + '''
      ''' + callout("For your team", "Copy this file into your repository and change two paths: your data and your shapes. Milestone 1 asks for a gate that blocks a bad commit.") + '''
    </div>
  </div>''', '''<p>Three minutes. The real file is <code>.github/workflows/shacl-gate.yml</code> in the course repository; it also runs on pull requests.</p>
<ul><li>Versions are pinned (pySHACL 0.40.1, rdflib 7.6.0) so the gate gives the same answer next month as today.</li></ul>'''))
