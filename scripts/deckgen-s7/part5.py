"""Session 7, Part 5 (deployment and governance) and the open problems.

References checked on 2026-09-25 (research brief in REPLAN-STATE.md): each
open problem cites one or two real, primary sources.
"""
from common import slide, divider, defbox, callout
from kit import flow, node, edge, head, table

SLIDES = []

SLIDES.append(divider("Part 5 · Deployment and governance", "Deployment",
    "Part 5 of 5 · about 12 minutes",
    "It works on your laptop. What does it take to run it for a company?",
    "One command to start it, signals that tell you when it breaks, and rules on who may ask what."))

nodes = [
    node("db", "operational database", 160, 45, 280, 56, kind="builtin"),
    node("mk", "mapping job\n(Morph-KGC)", 520, 45, 280, 70, kind="builtin"),
    node("sh", "SHACL gate\n(pyshacl)", 880, 45, 260, 70, kind="builtin"),
    node("fu", "SPARQL endpoint\n(Fuseki)", 880, 185, 280, 70, kind="builtin"),
    node("al", "access layer\n(serve.py)", 520, 185, 280, 70, kind="builtin"),
    node("u", "a manager's question", 160, 185, 280, 56, kind="literal"),
    node("llm", "model API (outside the stack)", 520, 315, 380, 56, kind="literal"),
]
edges = [edge("a", "db", "mk", "rows"), edge("b", "mk", "sh", "triples"), edge("c", "sh", "fu", "if valid"),
         edge("d", "u", "al", ""), edge("e", "al", "fu", "query"),
         edge("f", "al", "llm", "prompt")]
pic = flow("The Session 8 stack", 1448, 350, nodes, edges, [{"show": [n["id"] for n in nodes] + [e["id"] for e in edges]}],
           legend={"builtin": "A container in the stack", "literal": "Outside it"})
SLIDES.append(slide("The stack, one command", "Deployment", 4,
    head("Everything from Sessions 2 to 7, as containers in one Compose file", "docker compose up starts it all; only the model is outside") + '''
  ''' + pic + '''
  <div class="lu-split">
    ''' + defbox([("Container topology", "Which parts run in which containers, and which one talks to which.")]) + '''
    ''' + callout("For Session 8", "<code>deploy/compose-access-layer.yml</code> adds the access layer to your stack: it reads your endpoint's address and your key from <code>.env</code>, and listens on 127.0.0.1 only.", "neutral") + '''
  </div>''', '''<p>Four minutes. Every box is a tool the course already used: the database (Session 5), Morph-KGC (Session 5), pyshacl (Session 4), Fuseki (Session 2), the access layer (today). The model API is the one part a team does not run; say what that means for privacy on the next slide.</p>'''))

rows = [("The data drifts", "class counts move: compare today's void.ttl with last week's", "7"),
        ("A mapping breaks", "a renamed column: fewer triples, a jump in SHACL results", "4, 5"),
        ("The model changes", "the provider updates it: rerun evaluate.py, record model and date", "7"),
        ("A query is too slow", "set a timeout; Session 2's <code>NOT EXISTS</code> version of Q6 took 172 s", "2")]
SLIDES.append(slide("Knowing when it breaks", "Deployment", 3,
    head("Four things that break silently, and the signal for each", "Every signal is something you already built") + '''
  ''' + table(["What breaks", "How you notice", "Session"], rows) + '''
  ''' + defbox([("Data drift", "The data changing over time until what was true of it no longer is.")]),
    '''<p>Three minutes. The test set is a monitor too: run it every week, and a drop in F1 says something changed, in the data, the mapping or the model. References: Dimou and others, ISWC 2015, on assessing mapping quality.</p>'''))

SLIDES.append(slide("Who may ask what", "Deployment", 3,
    head("One query can cross departments. The layer must not.", "Access control on a graph, and what the model is allowed to see") + '''
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:var(--lu-s3)">
    <div class="lu-card"><span class="lu-card__label">Ask as the user</span><p class="lu-sub">The layer queries with the asker's rights, never an administrator's. Fuseki can limit each user to named datasets and graphs.</p></div>
    <div class="lu-card"><span class="lu-card__label">Send the schema, not the data</span><p class="lu-sub">The model gets VoID and examples. The rows stay in your stack. A free tier's inputs may be used to improve the provider's products.</p></div>
    <div class="lu-card"><span class="lu-card__label">Keep keys out of code</span><p class="lu-sub">The key lives in <code>.env</code>, which is never committed. A key in a script or a slide is a leaked key.</p></div>
  </div>
  ''' + defbox([("Access control", "Rules on who may read or change which data.")]),
    '''<p>Three minutes. Fuseki's data access control works per dataset and, for read-only datasets, per named graph (Apache Jena documentation). Kirrane, Mileo and Decker (Semantic Web journal, 2017) survey access control for RDF. The free tier note is Google's own terms for the Gemini API.</p>'''))

# ---------------------------------------------------------------- open problems
SLIDES.append(divider("Open problems", "Open problems",
    "Six questions the field has not settled · about 22 minutes",
    "This course checked every answer after the fact. What would it take not to have to?",
    "Six open questions. Each team picks one for its report."))

PROBLEMS = [
    ("Ontology learning from text", "Can a model write the ontology Session 3 wrote by hand, from documents?",
     "Models now suggest classes and relations well enough to help, but not well enough to trust: someone must still decide what the words mean.",
     "Asim and others, <i>Database</i>, 2018 (a survey) · Babaei Giglou, D'Souza and Auer, &ldquo;LLMs4OL&rdquo;, ISWC 2023"),
    ("Constraints by construction", "Can a learned model obey a rule because of how it is built, not because we check its output?",
     "Sessions 4 and 7 check afterwards: SHACL, the query check. Building the rule into training is possible for simple logic, hard for real shapes.",
     "Xu and others, &ldquo;A semantic loss function&rdquo;, ICML 2018 · Giunchiglia and Lukasiewicz, JAIR, 2021"),
    ("Do models reason over ontologies?", "When a model scores well on a benchmark, did it reason, or remember?",
     "A model may have seen the benchmark in training. Today's score, like ours, shows answers, not how they were reached.",
     "He and others, &ldquo;Language model analysis for ontology subsumption inference&rdquo;, Findings of ACL 2023 · Sainz and others, Findings of EMNLP 2023"),
    ("Time and space", "How do you ask when something was true, or how near two things are?",
     "This course left them out: Brunel has one order date. Facts that change over time, and places, need more than plain triples.",
     "Gutierrez, Hurtado and Vaisman, IEEE TKDE, 2007 · OGC GeoSPARQL 1.1, 2024"),
    ("Reproducible results", "Do reported gains in knowledge graph completion survive a fair comparison?",
     "Several did not: tuned old models matched new ones. Session 6's baseline was this lesson on our own data.",
     "Kadlec, Bajgar and Kleindienst, 2017 · Ruffinelli, Broscheit and Gemulla, ICLR 2020 · Sun and others, ACL 2020"),
    ("Standards in motion", "What do you build on when the standard is still changing?",
     "SHACL 1.2 Core is a W3C Working Draft (18 September 2026). The RML Working Group is not yet chartered; its charter was being refined from June 2026.",
     "W3C, SHACL 1.2 Core, Working Draft · W3C strategy issue 443, the RML Working Group charter"),
]
for i, (title, q, why, refs) in enumerate(PROBLEMS, 1):
    SLIDES.append(slide(f"Open problem {i}: {title}", "Open problems", 3, f'''  <div class="lu-eyebrow">Open problem {i} of 6</div>
  <h2 class="lu-h2">{title}</h2>
  <p class="lu-statement" style="font-size:var(--lu-t-h3);max-width:44ch">{q}</p>
  <div class="lu-split" style="margin-top:var(--lu-s4)">
    ''' + callout("Why it is open", why) + '''
    ''' + callout("Read", refs, "neutral") + '''
  </div>''', '''<p>Three minutes. Ask one team: how would this problem show up in your own project? The references are the reading list's starting points for this problem.</p>'''))

SLIDES.append(slide("Choose your team's problem", "Open problems", 3, '''  <div class="lu-eyebrow">For the report</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">Each team leaves with one of the six</h2>
      <ol class="lu-list lu-list--num">
        <li>Ontology learning from text</li><li>Constraints by construction</li><li>Do models reason over ontologies?</li>
        <li>Time and space</li><li>Reproducible results</li><li>Standards in motion</li>
      </ol>
    </div>
    <div class="lu-card">
      <span class="lu-card__label">What the report says about it</span>
      <p class="lu-sub">Where the problem appears in your own system, what you did about it, and what you could not do. One page, with at least one of the references.</p>
    </div>
  </div>''', '''<p>Three minutes. Write each team's choice on the board. The syllabus asks every team to leave this segment with its problem chosen.</p>''', kind="tint"))
