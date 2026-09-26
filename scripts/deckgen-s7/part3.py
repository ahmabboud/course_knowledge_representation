"""Session 7, Part 3: validate, repair, refuse.

Numbers: reference-outputs/check.txt (the real hint for broken.sparql);
Session 2's counts (9,023 and 9,215). The repair walk draws broken.sparql's
repair as an illustration and says so; the model's real repairs are in the
recorded evaluate.txt.
"""
from common import slide, divider, defbox, callout, code
from kit import flow, node, edge, head, table

SLIDES = []
S, C, E = '<span class="tok-str">', '<span class="tok-com">', '</span>'

SLIDES.append(divider("Part 3 · Validate, repair, refuse", "Check and repair",
    "Part 3 of 5 · about 22 minutes",
    "The model will be wrong sometimes. Can the system notice before the user does?",
    "Some mistakes, yes: check every query against the graph's description. Some, never."))

bq = (f'''SELECT (COUNT(?order) AS ?n) WHERE {{
  ?order ul:shippedBy
    &lt;.../carrier/brunel/V44_3&gt; .
}}''')
out = '''broken.sparql: 1 problem
  - ul:shippedBy is not a property of this
    graph. The properties are: ul:bandCarrier,
    ul:bandFrom, ..., ul:carriedBy, ...'''
SLIDES.append(slide("Check before running", "Check and repair", 4, '''  <div class="lu-eyebrow">check.py broken.sparql · a real run</div>
  <h2 class="lu-h2">Two tests: is it SPARQL, and does every term exist in void.ttl?</h2>
  <div class="lu-split">
    <div class="lu-stack">
      ''' + code("broken.sparql · a query a model could write", bq) + '''
      ''' + code("the check's answer, shortened", out) + '''
    </div>
    <div class="lu-stack">
      ''' + defbox([("Validation", "Checking a generated query against the endpoint's description before it runs.")]) + '''
      ''' + callout("An error that helps", "The message does not just say &ldquo;wrong&rdquo;: it lists the properties that do exist. That list is what the model gets back.") + '''
    </div>
  </div>''', '''<p>Four minutes. Real output: <code>reference-outputs/check.txt</code>. Run as written, this query does not fail: it returns a count of 0, a wrong answer with no error. That is why the check comes first.</p>'''))

nodes = [
    node("t1", "try 1: ul:shippedBy", 230, 50, 340, 56, kind="literal"),
    node("c1", "check: 1 problem", 700, 50, 300, 56, kind="builtin"),
    node("h", "hint: the real properties", 1160, 50, 380, 56, kind="literal"),
    node("t2", "try 2: ul:carriedBy", 1160, 170, 340, 56, kind="literal"),
    node("c2", "check: no problem", 700, 170, 300, 56, kind="builtin"),
    node("r", "run: n = 854", 230, 170, 280, 56, kind="literal"),
]
edges = [edge("a", "t1", "c1", ""), edge("b", "c1", "h", ""), edge("c", "h", "t2", "model again"),
         edge("d", "t2", "c2", ""), edge("e", "c2", "r", "")]
steps = [
    {"show": ["t1"], "set": {"t1": "active"}},
    {"show": ["c1", "a"], "run": ["a"], "set": {"t1": "idle", "c1": "impossible"}},
    {"show": ["h", "b"], "run": ["b"]},
    {"show": ["t2", "c"], "run": ["c"], "set": {"t2": "active"}},
    {"show": ["c2", "r", "d", "e"], "run": ["d", "e"], "set": {"t2": "idle", "c2": "active", "r": "inferred"}},
]
caps = [
    ("Try 1", "<b>Step 1.</b> The model's first query uses a property that sounds right."),
    ("Caught", "<b>Step 2.</b> The check finds it before anything runs."),
    ("Hint", "<b>Step 3.</b> The problem, with the list of real properties, is added to the prompt: &ldquo;your previous query had these problems&rdquo;."),
    ("Try 2", "<b>Step 4.</b> The model writes the query again, with the hint in front of it."),
    ("Answer", "<b>Step 5.</b> The new query passes the check and runs: 854 orders. At most two repairs; after that, the layer refuses."),
]
walk = flow("The repair loop", 1448, 210, nodes, edges, steps, caps,
            flags={"impossible": "problem", "inferred": "answer"},
            legend={"literal": "A query or a message", "builtin": "The check", "impossible": "Problem found", "inferred": "Answer"})
SLIDES.append(slide("The repair loop", "Check and repair", 5, '''  <div class="lu-eyebrow">Walkthrough · broken.sparql, repaired</div>
  <h2 class="lu-h2">A problem the model can read becomes a second, better try</h2>
  ''' + walk + '''
  ''' + defbox([("Repair loop", "Sending the check's problems back to the model and asking again, a fixed number of times.")]),
    '''<p>Five minutes. The walk draws the repair of <code>broken.sparql</code> as an illustration: the queries are real, the model's two tries are drawn. What the recorded model actually did, question by question, is in <code>reference-outputs/evaluate.txt</code> (the "tries" column).</p>
<ul><li>This loop is the design decision the syllabus calls the one that separates working systems from demonstrations: sparql-llm and SIB's endpoints do exactly this.</li></ul>'''))

rows = [("Not SPARQL at all", "yes", "the parser"),
        ("A property the graph lacks (ul:shippedBy)", "yes", "unknown_properties"),
        ("A class the graph lacks (ul:Shipment)", "after Part B", "unknown_classes, Y2"),
        ("<b>Only ul:Order: 9,023 instead of 9,215</b>", "<b>no</b>", "every term exists"),
        ("The right terms, the wrong question", "no", "only a test set can tell")]
SLIDES.append(slide("What the check cannot catch", "Check and repair", 3,
    head("A valid query can still be the wrong query", "The check knows the graph's words, not the manager's meaning") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    ''' + table(["Mistake", "Caught?", "By"], rows) + '''
    ''' + callout("So: measure", "The subclass mistake passes every check and returns a number that looks fine. Only comparing with the right answer, on a test set, shows it. That is Part 4.") + '''
  </div>''', '''<p>Three minutes. Test question 1 of the lab is exactly this case; look at it in the <code>schema</code> setting of the recorded run.</p>'''))

rows = [("Which customers are located in Beirut?", "no places at all"),
        ("What is the email address of customer V555_15?", "no contact details"),
        ("Which orders were cancelled?", "no order status")]
SLIDES.append(slide("The refusal path", "Check and repair", 4,
    head("Three test questions the graph cannot answer", "A query can be written for each. The right answer is to refuse.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    ''' + table(["Question", "What the graph lacks"], rows) + '''
    <div class="lu-stack">
      ''' + defbox([("Refusal", "Saying the graph cannot answer, and why, instead of guessing.")]) + '''
      ''' + callout("Two ways to refuse", "The rules say: reply <code>REFUSE: &lt;what is missing&gt;</code>. And if no valid query survives two repairs, the layer refuses for the model.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. The refusal must name what is missing, so the user learns what the graph holds. Refusing is harder than it sounds: a model trained to be helpful prefers to answer. The lab counts refusals separately from F1.</p>'''))

ev = (f'''question: How many orders did carrier V44_3 carry?
SELECT (COUNT(?o) AS ?n) WHERE {{
  ?o ul:carriedBy &lt;.../carrier/brunel/V44_3&gt; }}
answer: 1 row
  n=854''')
SLIDES.append(slide("The answer shows its evidence", "Check and repair", 3, '''  <div class="lu-eyebrow">Grounding and citation</div>
  <h2 class="lu-h2">Never a bare number: the query and the rows come with it</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code("what ask.py prints for test question 4, shortened", ev) + '''
    <div class="lu-stack">
      ''' + callout("Anyone can check it", "The query is the citation: an analyst can read it, run it on the endpoint, and see 854. A wrong query is visible, not hidden in a sentence.") + '''
      ''' + callout("For your stack", "serve.py returns the query itself (the TEXT2SPARQL contract): the evidence travels with every answer.", "neutral") + '''
    </div>
  </div>''', '''<p>Three minutes. The query and 854 are the gold ones for test question 4; the recorded model's own query is in <code>reference-outputs/ask-v44-3.txt</code>.</p>'''))

SLIDES.append(slide("Poll: refuse or guess?", "Check and repair", 3, '''  <div class="lu-eyebrow">Room poll · 45 seconds</div>
  <div class="lu-poll" data-qid="s7-poll" data-seconds="45" data-answer="b" data-label="What the layer should do when the graph cannot answer">
    <p class="lu-mcq__q">A manager asks which customers are in Beirut. The graph has no places. What should the layer do?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">Answer from what the model knows about Brunel<span class="lu-mcq__why" hidden>Then the answer does not come from the graph, and nobody can check it.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">Refuse, and say the graph has no locations<span class="lu-mcq__why" hidden>Yes: honest, checkable, and it tells the manager what data is missing.</span></button>
    </div>
  </div>''', '''<p>Forty five seconds, then discuss. Someone will say "but the manager wants an answer": the refusal is an answer, about the data. Session 8's defense asks every team what its system does when it does not know.</p>''', kind="tint", extra_attr=' style="--lu-s5:12px"'))
