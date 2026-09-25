"""Session 6, Part 3: message passing and graph neural networks.

Numbers: reference-outputs/build-graph.txt and gnn.txt; the reach after one,
two and four layers is counted on Session 5's brunel-mapped.nt over the seven
kinds of link build_graph.py keeps, both directions (the notes say so).
Code is an excerpt of build_graph.py and gnn.py; lines stay under ~50
characters.
"""
from common import slide, divider, defbox, callout, code
from kit import flow, node, edge, head, table, bar

SLIDES = []
S, C, E = '<span class="tok-str">', '<span class="tok-com">', '</span>'

SLIDES.append(divider("Part 3 · Message passing", "Message passing",
    "Part 3 of 4 · about 30 minutes",
    "How does an order learn from the things it is linked to?",
    "Each thing sends its numbers along its links; each order combines what it receives."))

# ---------------------------------------------------------------- one round, on a real order
nb = [("c", "customer V555_15"), ("k", "carrier V444_0"), ("p", "PLANT08"), ("q", "PORT04"), ("d", "product 1681878")]
n = [node(i, lab, 150 + 287 * j, 30, 262, 50, kind="individual") for j, (i, lab) in enumerate(nb)]
n += [node("o", "order 1447135386.7", 724, 160, 330, 56, kind="individual"),
      node("x", "own numbers:\n3.1 kg, 1,045 units, DTP", 220, 160, 360, 70, kind="literal"),
      node("h", "new numbers\nfor the order (32)", 1230, 160, 300, 70, kind="literal")]
e = [edge("m" + i, i, "o", "") for i, _ in nb] + [edge("u", "o", "h", "combine"), edge("v", "x", "o", "")]
steps = [
    {"show": ["o", "x", "v"], "set": {"o": "active"}},
    {"show": [i for i, _ in nb]},
    {"show": ["m" + i for i, _ in nb], "run": ["m" + i for i, _ in nb]},
    {"show": ["h", "u"], "run": ["u"], "set": {"o": "idle", "h": "inferred"}},
]
caps = [
    ("Before", "<b>Step 1.</b> The order starts with its own three numbers."),
    ("Neighbours", "<b>Step 2.</b> Its five neighbours have numbers too. Here they only say which one each is: customer 23 of 46, say."),
    ("Messages", "<b>Step 3.</b> Each neighbour sends its numbers along its link. That is a <b>message</b>."),
    ("Update", "<b>Step 4.</b> The order averages the messages of each kind of link, weighs them and its own numbers with learned weights, and adds them up. One layer done."),
]
walk = flow("One round of message passing", 1448, 200, n, e, steps, caps,
            flags={"inferred": "learned"},
            legend={"individual": "Thing in the graph", "literal": "Numbers", "inferred": "Computed by the layer"})
SLIDES.append(slide("One round of message passing", "Message passing", 5, '''  <div class="lu-eyebrow">Walkthrough · the order from Part 1</div>
  <h2 class="lu-h2">A layer mixes each node's own numbers with its neighbours'</h2>
  ''' + walk + '''
  ''' + defbox([("Message passing", "Each node updates itself from what its neighbours send it, one round per layer."),
                ("GraphSAGE", "A layer where a node combines its own numbers with the average of its neighbours'.")]),
    '''<p>Five minutes. Every node does this at the same time, so the customer also updates, from its 110 orders. That is the point of the next slide.</p>
<ul><li>GraphSAGE: Hamilton, Ying and Leskovec, 2017. The weights are shared by every node of a kind, so the model learns a rule, not one answer per order.</li></ul>'''))

# ---------------------------------------------------------------- how far two layers reach
SLIDES.append(slide("Two layers reach almost everything", "Message passing", 4,
    head("How many other orders has one order heard from, after k layers?", "On Brunel, two layers already reach almost every order") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <div class="lu-stack" style="gap:var(--lu-s4)">
      <div class="lu-stack" style="gap:var(--lu-s2)"><span class="lu-card__label">1 layer · its 5 neighbours</span>''' + bar(0, 9214, "0 orders") + '''</div>
      <div class="lu-stack" style="gap:var(--lu-s2)"><span class="lu-card__label">2 layers · through a shared port or carrier</span>''' + bar(9074, 9214, "9,074") + '''</div>
      <div class="lu-stack" style="gap:var(--lu-s2)"><span class="lu-card__label">4 layers</span>''' + bar(9214, 9214, "all 9,214", "red") + '''</div>
    </div>
    <div class="lu-stack">
      ''' + defbox([("Oversmoothing", "After many layers every node has heard from the same crowd, so all their numbers look alike.")]) + '''
      ''' + callout("Why the lab stops at 2", "PORT04 alone serves 9,041 orders. More layers add no new neighbours, only more averaging.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. Counted on <code>brunel-mapped.nt</code> over the seven kinds of link <code>build_graph.py</code> keeps, in both directions: the median over 200 random orders is 9,074 at two layers and 9,214 at four; the order from Part 1 gives the same 9,074.</p>
<ul><li>Oversmoothing: Li, Han and Wu, 2018, among others. Real GNNs are usually 2 or 3 layers deep for this reason.</li></ul>'''))

# ---------------------------------------------------------------- HeteroData
rows = [("order", "9,215", "weight, quantity, service level: 5 numbers"),
        ("customer", "46", "which one it is: 46 numbers, one set to 1"),
        ("carrier · plant · port · product", "3 · 20 · 11 · 1,540", "which one it is")]
hd = (f'''data = HeteroData()
data[{S}"order"{E}].x = torch.tensor(x)  {C}# 9215 x 5{E}
data[{S}"order"{E}, {S}"orderedBy"{E}, {S}"customer"{E}
     ].edge_index = pairs.T   {C}# 2 x 9215{E}''')
SLIDES.append(slide("The graph as PyTorch Geometric sees it", "Message passing", 4, '''  <div class="lu-eyebrow">What build_graph.py writes</div>
  <h2 class="lu-h2">One table of numbers per kind of node, one list of pairs per kind of link</h2>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      ''' + table(["Node kind", "How many", "Numbers per node"], rows) + '''
      ''' + code("build_graph.py and gnn.py · shortened", hd) + '''
    </div>
    <div class="lu-stack">
      ''' + defbox([("HeteroData", "PyTorch Geometric's object for a graph with several kinds of node and link.")]) + '''
      ''' + callout("ToUndirected", "Every link points from the order outward. Messages flow along links, so without the reverse links an order would receive nothing at all.") + '''
    </div>
  </div>''', '''<p>Four minutes. Seven kinds of link, 9,215 of each order link, 2,036 makes, 22 servesPort (<code>reference-outputs/build-graph.txt</code>); ToUndirected adds the seven reverse kinds.</p>
<ul><li>The label is not in <code>x</code>. Part 4 shows where it was hiding and what happens if it stays.</li></ul>'''))

# ---------------------------------------------------------------- the ontology decides the kinds
rows = [("<code>ul:Order</code>, and its subclass <code>ul:LateOrder</code>", "one node kind: order"),
        ("<code>ul:Customer</code>, <code>ul:Carrier</code>, <code>ul:Plant</code>, ...", "one node kind each"),
        ("<code>ul:orderedBy</code> (domain Order, range Customer)", "one link kind: order to customer"),
        ("<code>ul:makes</code> (domain Plant, range Product)", "one link kind: plant to product")]
SLIDES.append(slide("The ontology decides the kinds", "Message passing", 3,
    head("Where Session 3 pays off", "Classes become node kinds, properties become link kinds") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    ''' + table(["In the ontology", "In HeteroData"], rows) + '''
    <div class="lu-stack">
      ''' + callout("A subclass is not a kind", "LateOrder &#8849; Order, so build_graph.py makes one kind, order. A separate kind for late orders would <b>be</b> the label.") + '''
      ''' + callout("Better ontology, better graph", "A property with a clear domain and range becomes one clean link kind. A vague one mixes different things in one list.", "neutral") + '''
    </div>
  </div>''', '''<p>Three minutes. The mapped data types late orders only as <code>ul:LateOrder</code>; <code>build_graph.py</code> takes both classes as orders, which is the subclass axiom of Session 3 applied by hand (Session 5 found the same gap with SHACL targets).</p>'''))

# ---------------------------------------------------------------- to_hetero and its gotcha
sg = (f'''class SAGE(torch.nn.Module):
    def __init__(self):
        self.conv1 = SAGEConv((-1, -1), 32)
        self.conv2 = SAGEConv((-1, -1), 32)
        self.score = Linear(32, 1)
    def forward(self, x, edge_index):
        h = self.conv1(x, edge_index).relu()
        h = self.conv2(h, edge_index).relu()
        return self.score(h)

model = to_hetero(SAGE(), data.metadata(), aggr={S}"sum"{E})''')
SLIDES.append(slide("to_hetero: one model, every kind of link", "Message passing", 4, '''  <div class="lu-eyebrow">What gnn.py trains</div>
  <h2 class="lu-h2">Write the model for one kind of link. to_hetero copies it for all fourteen.</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code("gnn.py · the model, shortened", sg) + '''
    <div class="lu-stack">
      ''' + defbox([("to_hetero", "PyTorch Geometric's tool that copies a model once per kind of link.")]) + '''
      ''' + callout("A real gotcha", "The argument must be called <code>edge_index</code>. We called it <code>ei</code> first: to_hetero failed with an error about edge_index that never said why.") + '''
      ''' + callout("(-1, -1)", "Sizes are read from the data on the first pass, since each kind of node has a different number of columns.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. 236,870 weights after conversion (<code>reference-outputs/gnn.txt</code>): each of the 14 kinds of link gets its own copy of each layer, and <code>aggr="sum"</code> adds up what an order receives from its different kinds.</p>
<ul><li>to_hetero rewrites the forward function by reading its argument names, which is why the name matters. Found in our own feasibility run on 2026-09-25.</li></ul>'''))

# ---------------------------------------------------------------- RGCN on the slide only
rows = [("How it is written", "a normal model, converted in one line", "wired by hand, relations as numbers"),
        ("Weights per kind of link", "a full copy of each layer", "one matrix, or a mix of a few shared ones"),
        ("In this course", "the lab", "this slide")]
SLIDES.append(slide("RGCN, the explicit version", "Message passing", 3,
    head("The same idea, written for relations from the start", "RGCN: one weight matrix per relation") + '''
  ''' + table(["", "<code>to_hetero(SAGE)</code>", "<code>RGCNConv</code>"], rows) + '''
  <div class="lu-split">
    ''' + defbox([("RGCN", "Relational graph convolutional network: a layer with one weight matrix per kind of link.")]) + '''
    ''' + callout("Weights multiply", "to_hetero gave 236,870 weights for 14 kinds of link: each new kind adds a full copy. RGCN can share a few basis matrices instead.", "neutral") + '''
  </div>''', '''<p>Three minutes. RGCN: Schlichtkrull and others, 2018, built for knowledge graphs. In PyTorch Geometric it is <code>RGCNConv(in, out, num_relations, num_bases=...)</code>. On Brunel's 14 kinds of link, either works; the lab keeps one model to stay simple.</p>'''))

# ---------------------------------------------------------------- inductive and transductive
SLIDES.append(slide("New things: inductive and transductive", "Message passing", 4,
    head("What happens when something appears that training never saw?", "Some models learn a position per thing, some learn a rule") + '''
  <div class="lu-split" style="margin-top:var(--lu-s3)">
    <div class="lu-card">
      <span class="lu-card__label">Transductive · TransE</span>
      <p class="lu-sub">One position per thing seen in training. A new product has none.</p>
      <p class="lu-sub">CND9 makes one product. When that link is hidden, CND9 has no position, and the lab ranks it last for every other product.</p>
    </div>
    <div class="lu-card">
      <span class="lu-card__label">Inductive · GraphSAGE</span>
      <p class="lu-sub">Learns weights, not positions: a new order gets numbers from its neighbours.</p>
      <p class="lu-sub">But a customer's numbers only say which one it is. A new customer is a column the model never trained.</p>
    </div>
  </div>
  ''' + defbox([("Transductive", "A model that can only score things it saw in training."),
                ("Inductive", "A model that can score new things, from their numbers and neighbours.")]),
    '''<p>Four minutes. CND9 appears only in the ProductsPerPlant table, with one product; <code>link_prediction.py</code> gives a plant it never saw the lowest possible score.</p>
<ul><li>The second card is Part 4 in one sentence: a split by customer asks the model about customers it never saw.</li></ul>'''))

SLIDES.append(slide("Check: a new customer", "Message passing", 2, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-mcq" data-qid="s6-q2" data-answer="c" data-label="Which model has learned about a new customer"
       data-fb-correct=" Inductive means it can compute numbers for a new node; it still learned nothing about this customer."
       data-fb-wrong=" Ask what the model saw about this customer during training.">
    <p class="lu-mcq__q">A customer that never ordered before places its first order. Which of today's models has learned anything about that customer?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">GraphSAGE, because it is inductive<span class="lu-mcq__why" hidden>It can compute numbers for the order, but the customer's column was never trained.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">TransE, because it embeds every thing<span class="lu-mcq__why" hidden>Only every thing it saw: a new customer has no position.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">None of them<span class="lu-mcq__why" hidden>Right: whatever they predict comes from the order's other links, not from the customer.</span></button>
    </div>
  </div>''', '''<p>Two minutes. Keep this answer on the board: it explains the result of the split by customer in Part 4.</p>''', kind="tint"))

SLIDES.append(slide("Drill: graph learning words", "Message passing", 3, '''  <div class="lu-eyebrow">Drill · type the missing word</div>
  <div class="lu-blanks" data-qid="s6-blanks1" data-label="Graph learning words">
    <p class="lu-h3" style="margin-bottom:var(--lu-s4)">Fill in the blanks</p>
    <ol class="lu-list lu-list--num">
      <li>For to_hetero, the model's second argument must be named <input class="lu-blank" data-answer="edge_index" data-label="Blank 1" placeholder="…">.</li>
      <li>The tool that copies a model once per kind of link is <input class="lu-blank" data-answer="to_hetero" data-label="Blank 2" placeholder="…">.</li>
      <li>After too many layers every node looks alike: <input class="lu-blank" data-answer="oversmoothing|over-smoothing" data-label="Blank 3" placeholder="…">.</li>
      <li>A model that can score a node it never saw in training is <input class="lu-blank" data-answer="inductive" data-label="Blank 4" placeholder="…">.</li>
    </ol>
  </div>''', '''<p>Three minutes. Blank 1 is the one students will meet on their own project: say it twice.</p>''', kind="tint"))
