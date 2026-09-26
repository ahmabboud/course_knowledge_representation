"""Session 7, Part 2: grounding the model in the graph's own description.

Numbers: reference-outputs/make-void.txt and show-prompt.txt (2026-09-25);
the prompt's parts measured with access_layer.build_prompt on the same day
(rules 1,021 characters, schema 1,317, examples 796, question 50, headings 55).
"""
from common import slide, divider, defbox, callout, code
from kit import head, table
from svgkit import svg, text, rect, FULL, INK2, INK3, BLUE, BLUE_BG, BLUE_TXT, PAPER2, GREEN, GREEN_BG, AMBER, LINE

SLIDES = []
S, C, E = '<span class="tok-str">', '<span class="tok-com">', '</span>'

SLIDES.append(divider("Part 2 · Grounding", "Grounding",
    "Part 2 of 5 · about 20 minutes",
    "What does the model need to know about the graph, and how little is enough?",
    "Its classes and properties, and a few worked examples. Not the whole ontology."))

vd = (f'''&lt;.../brunel/void&gt;
    void:classPartition ul:Plant-partition .
ul:Plant-partition void:class ul:Plant ;
    void:entities 19 ;
    void:propertyPartition ul:Plant-makes .
ul:Plant-makes void:property ul:makes ;
    void:triples 2035 ;
    void:classPartition [ void:class ul:Product ] .''')
SLIDES.append(slide("VoID: the graph describes itself", "Grounding", 5, '''  <div class="lu-eyebrow">What make_void.py writes</div>
  <h2 class="lu-h2">For each class: how many things. For each property: from which class, to which.</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code("void.ttl · the Plant partition, shortened", vd) + '''
    <div class="lu-stack">
      ''' + defbox([("VoID", "Vocabulary of Interlinked Datasets: a small RDF description of a graph's classes, properties and counts.")]) + '''
      ''' + callout("Small on purpose", "<b>189 triples</b> describe all 135,841. One SPARQL CONSTRUCT writes them, in 0.3 seconds, in the layout of SIB's void-generator.") + '''
    </div>
  </div>''', '''<p>Five minutes. Real run: <code>reference-outputs/make-void.txt</code>. The 2,035 makes links are those whose plant is typed <code>ul:Plant</code>: CND9 makes one product and is typed nothing in Session 2's graph.</p>
<ul><li>SIB's void-generator (Java 17) writes the same layout from any live endpoint, and sparql-llm reads it; the lab's README has the command.</li><li>Why not the ontology? It says what could be true (Session 3's classes and axioms); VoID says what is actually there, with counts. The model needs the second.</li></ul>'''))

sc = '''ul:Order (9,023 things)
ul:Product (1,540 things)
ul:RateBand (1,540 things)
ul:LateOrder (192 things)
ul:Customer (46 things)
...
ul:Order ul:carriedBy ul:Carrier
ul:Order ul:lateDays xsd:integer
ul:Plant ul:makes ul:Product
ul:Plant ul:servesPort ul:Port'''
SLIDES.append(slide("The schema, as the model reads it", "Grounding", 3, '''  <div class="lu-eyebrow">schema_text(): VoID turned into plain lines</div>
  <h2 class="lu-h2">One line per class, one line per property: 41 lines for the whole graph</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code("the schema part of the prompt, shortened", sc) + '''
    <div class="lu-stack">
      ''' + callout("Why plain lines", "A model reads text. &ldquo;ul:Order ul:carriedBy ul:Carrier&rdquo; says which way the link goes and what is at the other end: all a query writer needs.") + '''
      ''' + callout("The counts help too", "ul:LateOrder (192 things) sitting next to ul:Order (9,023) is a hint that orders come in two kinds.", "neutral") + '''
    </div>
  </div>''', '''<p>Three minutes. The whole schema is 1,317 characters (<code>show_prompt.py</code> prints it). The rules at the top of the prompt also state the subclass explicitly, because a count alone is a weak hint.</p>'''))

ex3 = (f'''ex:3 a sh:SPARQLExecutable ;
  rdfs:comment
    {S}"Which products does plant PLANT08 make?"{E} ;
  sh:select {S}"""
SELECT ?product WHERE {{
  &lt;.../plant/brunel/PLANT08&gt; ul:makes ?product .
}}"""{E} .''')
SLIDES.append(slide("Examples, in the SHACL vocabulary", "Grounding", 4, '''  <div class="lu-eyebrow">examples.ttl · six worked examples</div>
  <h2 class="lu-h2">A question and its query, stored as RDF, so tools can find and share them</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code("examples.ttl · ex:3, shortened", ex3) + '''
    <div class="lu-stack">
      ''' + defbox([("Few-shot examples", "Worked question and query pairs placed in the prompt for the model to imitate.")]) + '''
      ''' + callout("Why the SHACL vocabulary", "<code>sh:SPARQLExecutable</code> is how SIB's endpoints publish their examples, and what sparql-llm loads. Your examples become reusable data.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. The model copies patterns: the IRI form of a code, the property name, the shape of a count. Part B's Y1 is a copy of this example with one property changed.</p>'''))

rows = [("<b>1</b>", "Which orders did carrier V44_3 carry, with their service level?", "<b>4</b>: carrier, carry, orders, v44_3"),
        ("<b>2</b>", "How many orders and how many late orders does each carrier have?", "<b>2</b>: carrier, orders"),
        ("<b>4</b>", "How many orders are there in total, late ones included?", "<b>1</b>: orders"),
        ("6", "How many orders did customer V555_15 place with service level DTP?", "1: orders (a tie, later in the file)"),
        ("3, 5", "Which products does plant PLANT08 make? · Which ports does ...", "0")]
SLIDES.append(slide("Picking the closest examples", "Grounding", 3,
    head("For &ldquo;How many orders did carrier V44_3 carry?&rdquo;: the words it shares with each example", "The three with most shared words go into the prompt: 1, 2 and 4") + '''
  ''' + table(["Example", "Its question", "Shared words"], rows) + '''
  ''' + callout("A simple rule, on purpose", "Common words (how, many, did) are ignored first. sparql-llm does the same job with embeddings of the questions; word overlap needs no download and always picks the same three.", "neutral"),
    '''<p>Three minutes. Real output of <code>show_prompt.py</code>: <code>examples picked: 1, 2, 4</code>. Example 1 is almost the question itself, which is why test questions and examples must never be the same (next slide).</p>'''))

# ---------------------------------------------------------------- prompt anatomy, drawn
parts = [("rules", 1021, PAPER2, INK2), ("schema", 1372, BLUE_BG, BLUE_TXT), ("3 examples", 796, GREEN_BG, "var(--lu-green-900)"), ("question", 50, "var(--lu-amber-050)", AMBER)]
total = sum(p[1] for p in parts)
g, x = "", 0.0
W = FULL - 4
for name, n, fill, col in parts:
    w = W * n / total
    g += rect(2 + x, 40, max(w, 6), 70, fill, LINE, rx=4)
    lx = 2 + x + w / 2
    if name == "question":
        g += text(FULL - 4, 142, f"question · {n}", "s-label", anchor="end", color=col)
    else:
        g += text(lx, 75, name, color=col, weight=600)
        g += text(lx, 142, f"{n:,} characters", "s-label", color=INK3)
    x += w
g += text(2, 18, "3,239 characters in all, about a page", "s-label", anchor="start", color=INK2)
pic = svg(FULL, 160, g, "The prompt: rules 1,021 characters, schema 1,372, three examples 796, the question 50.")
SLIDES.append(slide("What the model is sent", "Grounding", 3,
    head("The whole prompt for one question", "Nothing hidden: python show_prompt.py prints every character") + '''
  ''' + pic + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    ''' + defbox([("Prompt", "Everything the model is given in one call: rules, schema, examples, question.")]) + '''
    ''' + callout("Grounding", "Giving the model the facts it must use, here the schema and examples, instead of relying on what it remembers.", "neutral") + '''
  </div>''', '''<p>Three minutes. Measured with <code>build_prompt</code>: rules 1,021, schema 1,317 plus 55 of headings, examples 796, question 50; 3,239 in all (<code>reference-outputs/show-prompt.txt</code>). The Session 3 ontology would be many times this, and would still not say what is actually in the data.</p>'''))

SLIDES.append(slide("Check: examples and tests", "Grounding", 2, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-mcq" data-qid="s7-q1" data-answer="b" data-label="Why no test question may also be an example"
       data-fb-correct=" The same leak as Session 6: the test would measure memory, not skill."
       data-fb-wrong=" Think of Session 6: what does a test measure if the answer was in training?">
    <p class="lu-mcq__q">Why may no question of the test set also be one of the examples in the prompt?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">It would make the prompt too long<span class="lu-mcq__why" hidden>One example adds a few hundred characters; length is not the issue.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">The model would copy the answer, so the score would measure memory<span class="lu-mcq__why" hidden>Right: a leak, as in Session 6.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">SHACL does not allow the same question twice<span class="lu-mcq__why" hidden>SHACL has no such rule; this is about honest testing.</span></button>
    </div>
  </div>''', '''<p>Two minutes. The Part B checker refuses a test question that is already an example, for exactly this reason.</p>''', kind="tint"))
