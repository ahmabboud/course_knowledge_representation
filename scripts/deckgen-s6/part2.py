"""Session 6, Part 2: knowledge graph embeddings, on "plant makes product".

Numbers: reference-outputs/link-prediction.txt; plant counts on Session 5's
brunel-mapped.nt (the 2,036 ul:makes triples). Code lines stay under ~50
characters in a wide column.
"""
from common import slide, divider, defbox, callout, code
from kit import flow, node, edge, head, table, bar
from svgkit import svg, text, dot, circle, arrow, line, rect, WL, INK2, INK3, GREEN, RED, LINE

SLIDES = []
S, C, E = '<span class="tok-str">', '<span class="tok-com">', '</span>'

SLIDES.append(divider("Part 2 · Embeddings", "Embeddings",
    "Part 2 of 4 · about 30 minutes",
    "How does a model learn which plant makes a product it has never been told about?",
    "Give every thing a position, so that true links become short steps."))

# ---------------------------------------------------------------- TransE, drawn
g = rect(2, 2, WL - 4, 336, "var(--lu-paper)", LINE)
g += text(24, 30, "32 numbers per thing in the lab; drawn here with 2", "s-label", anchor="start", color=INK3)
g += dot(150, 270, None, "green") + text(150, 302, "PLANT08  (h)", "s-label", color=GREEN)
g += arrow(158, 262, 452, 122, "+ makes  (r)", kind="strong", lx=250, ly=160, label_anchor="end")
g += circle(460, 115, 34, None, "muted", fill=False, dashed=True)
g += text(460, 60, "h + r", "s-mono", color=INK2)
g += dot(478, 128, None, "green") + text(496, 150, "1681878: made by PLANT08", "s-label", anchor="start", color=GREEN)
g += dot(700, 280, None, "red") + text(690, 312, "a product it does not make", "s-label", anchor="end", color=RED)
g += line(470, 140, 692, 272, RED, 2, dashed=True)
g += text(640, 205, "far: low score", "s-label", anchor="start", color=RED)
pic = svg(WL, 340, g, "TransE: the plant's position plus the step for makes lands near the products it makes, far from the others.")
SLIDES.append(slide("TransE: a relation is a step", "Embeddings", 5, '''  <div class="lu-eyebrow">The idea behind knowledge graph embeddings</div>
  <h2 class="lu-h2">Every thing gets a position. A relation is a step. A true link is a short trip.</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + pic + '''
    <div class="lu-stack">
      ''' + defbox([("Embedding", "A short list of numbers learned for each thing, so that related things end up close."),
                    ("TransE", "An embedding where head + relation should land near the tail.")]) + '''
      ''' + callout("The score", "score(h, r, t) = &minus; distance(h + r, t). Close: likely true. Far: likely false.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. The picture is a drawing of the idea, not the trained model (which uses 32 numbers per thing). The link itself is real: PLANT08 makes product 1681878, and so do PLANT07 and PLANT10.</p>
<ul><li>TransE: Bordes and others, 2013. Training moves the positions until true triples are short trips and made-up ones are long.</li></ul>'''))

# ---------------------------------------------------------------- four scoring functions
rows = [
    ("TransE, 2013", "h + r lands near t", "no", "yes", "yes", "yes"),
    ("DistMult, 2015", "h, r and t multiplied, number by number: every relation symmetric", "yes", "no", "no", "no"),
    ("ComplEx, 2016", "DistMult with complex numbers: a relation can go one way", "yes", "yes", "yes", "no"),
    ("RotatE, 2019", "r rotates h onto t, in complex numbers", "yes", "yes", "yes", "yes"),
]
SLIDES.append(slide("Four ways to score a triple", "Embeddings", 5,
    head("The same idea, four scoring functions", "They differ in which patterns of relations they can represent") + '''
  ''' + table(["Model", "How a triple is scored", "Symmetric", "Antisymmetric", "Inverse", "Composition"], rows) + '''
  ''' + callout("For Brunel", "Every relation links two different kinds (a plant makes a product; a product never makes a plant), so none is symmetric. TransE fits: it is the one the lab trains.", "neutral"),
    '''<p>Five minutes. The pattern table is the one in the RotatE paper (Sun and others, 2019). Symmetric: <i>married to</i>. Antisymmetric: <i>makes</i>. Inverse: <i>makes</i> and <i>made by</i>. Composition: an order <i>from</i> a plant that <i>serves</i> a port <i>ships from</i> that port.</p>
<ul><li>All four are one word apart in PyKEEN: <code>model="DistMult"</code>. The lab README's optional task tries it.</li></ul>'''))

# ---------------------------------------------------------------- negative sampling
n = [
    node("h0", "PLANT08", 200, 32, 200, 52, kind="individual"),
    node("h1", "PLANT03", 200, 102, 200, 52, kind="individual"),
    node("h2", "PLANT07", 200, 172, 200, 52, kind="individual"),
    node("t", "product 1681878", 1150, 102, 300, 52, kind="individual"),
]
e = [edge("a", "h0", "t", "makes"), edge("b", "h1", "t", ""), edge("c", "h2", "t", "")]
steps = [
    {"show": ["h0", "t", "a"], "run": ["a"], "set": {"h0": "active"}},
    {"show": ["h1", "b"], "run": ["b"], "set": {"h0": "idle", "h1": "impossible"}},
    {"show": ["h2", "c"], "run": ["c"], "set": {"h2": "inferred"}},
]
caps = [
    ("A true link", "<b>Step 1.</b> Training shows the model a link from the graph. Its score should go up."),
    ("A made-up link", "<b>Step 2.</b> Swap the plant for a random one: PLANT03. The graph does not say PLANT03 makes it, so its score should go down."),
    ("A made-up link that is true", "<b>Step 3.</b> Another random swap: PLANT07. But PLANT07 <b>does</b> make 1681878. A random negative can be true; evaluation must allow for it."),
]
walk = flow("Negative sampling", 1448, 205, n, e, steps, caps,
            flags={"impossible": "negative", "inferred": "also true"},
            legend={"individual": "Thing in the graph", "impossible": "Negative sample", "inferred": "Negative that is true"})
SLIDES.append(slide("Negative sampling", "Embeddings", 4, '''  <div class="lu-eyebrow">Walkthrough · how training learns what is false</div>
  <h2 class="lu-h2">The graph holds only true links. Training makes up false ones to compare.</h2>
  ''' + walk + '''
  ''' + defbox([("Negative sampling", "Making up false triples by swapping the head or the tail, so the model learns to score them lower.")]),
    '''<p>Four minutes. All three plants are real: PLANT07, PLANT08 and PLANT10 make 1681878 in <code>brunel-mapped.nt</code>; PLANT03 does not.</p>
<ul><li>The graph is open world (Session 3): a missing link is unknown, not false. Negative sampling pretends it is false, and is sometimes wrong. That is the price of learning from positives only.</li></ul>'''))

# ---------------------------------------------------------------- filtered ranking
rows = [
    ("1 to 5", "PLANT03, 01, 13, 04, 05", "781 to 127", "1 to 5"),
    ("6", "PLANT10", "121", "<i>removed: also right</i>"),
    ("7 to 10", "PLANT02, 16, 11, 12", "116 to 57", "6 to 9"),
    ("11", "PLANT07", "29", "<i>removed: also right</i>"),
    ("12", "PLANT06", "26", "10"),
    ("<b>13</b>", "<b>PLANT08, hidden</b>", "<b>20</b>", "<b>11</b>: 1/11 = 0.09"),
]
SLIDES.append(slide("Ranking, raw and filtered", "Embeddings", 5,
    head("Hide one link, then rank every plant by how many products it makes", "Hidden: PLANT08 makes 1681878. Two other right answers rank above it.", width=72) + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s2)">
    ''' + table(["Raw rank", "Plant", "Products", "Filtered rank"], rows) + '''
    <div class="lu-stack">
      ''' + defbox([("Filtered ranking", "Removing the other right answers before ranking the hidden one."),
                    ("MRR", "The average of 1 / rank of the right answer."),
                    ("Hits@k", "The share of right answers ranked k or better.")]) + '''
    </div>
  </div>''', '''<p>Five minutes. This is the popularity model's real ranking for one link, counted over the other 2,035 makes links of <code>brunel-mapped.nt</code> (PLANT08 makes 21 products, 20 once this one is hidden; PLANT17 also makes 20 and ranks after it).</p>
<ul><li>Filtered ranking: Bordes and others, 2013, the TransE paper. Every published link prediction score today is filtered.</li></ul>'''))

SLIDES.append(slide("Check: filtered rank", "Embeddings", 3, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-mcq" data-qid="s6-q1" data-answer="b" data-label="Filtered rank of a hidden link"
       data-fb-correct=" Filtering removes only the other right answers, so the hidden one moves up by exactly that many."
       data-fb-wrong=" Filtering removes the other right answers, and nothing else.">
    <p class="lu-mcq__q">A hidden link's right answer ranks 7th among all plants. Three of the plants ranked above it are also right answers. What is its filtered rank?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">7<span class="lu-mcq__why" hidden>That is the raw rank: the other right answers still count against it.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">4<span class="lu-mcq__why" hidden>Right: 7 minus the 3 right answers above it.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">1<span class="lu-mcq__why" hidden>Only the right answers are removed, not the wrong plants above it.</span></button>
    </div>
  </div>''', '''<p>Three minutes. Then ask: which rank does PyKEEN report by default? Filtered, like this.</p>''', kind="tint"))

# ---------------------------------------------------------------- the lab's code
pk = (f'''result = pipeline(
    training=train, validation=valid,
    testing=test, model={S}"TransE"{E},
    model_kwargs=dict(embedding_dim=32),
    training_kwargs=dict(num_epochs=150),
    random_seed=seed)
model = result.model
{C}# score every head for (?, makes, product){E}
scores = model.score_h(torch.tensor(
    [[makes_id, product_id]]))''')
SLIDES.append(slide("TransE in PyKEEN", "Embeddings", 4, '''  <div class="lu-eyebrow">What the lab runs</div>
  <h2 class="lu-h2">One call trains the model. Ranking is ours: among plants only.</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code("link_prediction.py · shortened", pk) + '''
    <div class="lu-stack">
      ''' + defbox([("PyKEEN", "The Python library for training knowledge graph embeddings, used in the lab.")]) + '''
      ''' + callout("A fair rival", "PyKEEN's own evaluation ranks the answer against every thing in the graph: customers, ports, products. Only a plant can make a product, so the lab ranks among the 19 plants, as popularity does.") + '''
    </div>
  </div>''', '''<p>Four minutes. The lab trains on five kinds of link: makes, plus four from the orders (a customer orders a product, a carrier ships it, it leaves from a port, a plant serves a port). The pair "this plant shipped this product" is left out on purpose: every one of them is also a makes link, so it would give the answer away.</p>'''))

# ---------------------------------------------------------------- TransE against popularity
runs = [("seed 0", 0.573, 0.631), ("seed 1", 0.469, 0.597), ("seed 2", 0.543, 0.634)]
bars = "".join(
    f'<div class="lu-stack" style="gap:var(--lu-s2)"><span class="lu-card__label">{s}</span>'
    + bar(a, 1, f"TransE {a:.3f}") + bar(b, 1, f"count {b:.3f}", "red") + '</div>'
    for s, a, b in runs)
SLIDES.append(slide("TransE against a count", "Embeddings", 5,
    head("A real run, three seeds, filtered MRR among plants", "The count wins every time") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <div class="lu-stack" style="gap:var(--lu-s4)">''' + bars + '''</div>
    <div class="lu-stack">
      ''' + callout("Why the count wins", "PLANT03 makes 781 of the 2,036 links, and 1,271 of the 1,540 products are made by one plant only. There is little shape to learn, and one big answer.") + '''
      ''' + callout("And some links cannot be scored", "In seed 0, 61 of the 203 hidden links name a product that appears in no other link. The model has no position for it, so the lab leaves them out.", "neutral") + '''
    </div>
  </div>''', '''<p>Five minutes. <code>reference-outputs/link-prediction.txt</code>: TransE MRR 0.573, 0.469, 0.543; popularity 0.631, 0.597, 0.634; 142, 142 and 126 links scored. Counts of plants and products from <code>brunel-mapped.nt</code>.</p>
<ul><li>Ask: is this a failure? No. It is a finding: on Brunel's product catalogue, the graph's shape tells you less than one count. On a graph with richer structure, the order can flip; the only way to know is this comparison.</li></ul>'''))
