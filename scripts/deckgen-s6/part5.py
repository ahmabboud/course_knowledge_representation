"""Session 6: the lab (AGENTS.md 2e: individual, not collected or graded;
2026-09-25 rule: every Part B task is the twin of a function already shown),
the discussion, the project clinic, Milestone 2, and the wrap."""
from common import slide, divider, callout, code
from kit import head, table

SLIDES = []
C, E = '<span class="tok-com">', '</span>'

SLIDES.append(divider("Lab · Train, compare, split", "Lab", "Lab · about 55 minutes · on your own machine",
    "Does the graph model still win when the test is fair?",
    "Then write three small functions, each a copy of one you can read."))

SLIDES.append(slide("Lab brief", "Lab", 3,
    head("Hands-on lab · about 55 minutes", "The Brunel graph as PyTorch Geometric reads it, three models, two splits.") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <ol class="lu-list lu-list--num">
      <li><b>Build and observe.</b> Convert the graph, run the baseline (the leak, the random split, the split by customer), GraphSAGE on both splits, TransE against the count.</li>
      <li><b>Three functions.</b> <code>my_learning.py</code>, each a twin of one in <code>learning_utils.py</code>; <code>check_my_learning.py</code> says right or not yet.</li>
      <li><b>Think.</b> Three questions, one about your own team's data.</li>
    </ol>
    <div class="lu-stack">
      ''' + callout("Nothing to hand in", "The lab is for understanding. Start with <code>OVERVIEW.md</code> in <code>demos/session-06-learning/</code>: the data, the facts that decide everything, and every file's role.", "concept") + '''
      ''' + callout("CPU only", "No GPU needed: the slowest step, TransE over three seeds, takes under a minute.", "neutral") + '''
    </div>
  </div>''', '''<p>Three minutes, then walk the room. Most common blocker: PyTorch missing, because the install lines of <code>demos/README.md</code> were not run again after Session 5. On Linux, the CPU build first (the command is in that README).</p>
<ul><li>Second: <code>data/brunel-graph.pt</code> missing because step 1 was skipped. Every later script needs it.</li></ul>'''))

pb = (f'''def split_by_customer(customer, test_share=0.3,
                      seed=0):
    rng = np.random.RandomState(seed)
    groups = np.unique(customer)
    rng.shuffle(groups)
    test_groups = groups[:int(round(
        test_share * len(groups)))]
    test = np.flatnonzero(
        np.isin(customer, test_groups))
    train = np.flatnonzero(
        ~np.isin(customer, test_groups))
    return train, test''')
rows = [("Y1 · <code>split_by_plant</code>", "<code>split_by_customer</code>", "group by plant"),
        ("Y2 · <code>recall_at_k</code>", "<code>precision_at_k</code>", "divide by all late orders, not by k"),
        ("Y3 · <code>hits_at_k</code>", "<code>mrr</code>", "average &ldquo;rank at most k&rdquo;, not 1 / rank")]
SLIDES.append(slide("Part B: each task has a twin", "Lab", 2,
    head("Lab Part B · three functions", "Copy the twin, change one thing") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s2)">
    ''' + code("learning_utils.py · the twin of Y1, in full", pb) + '''
    <div class="lu-stack">
      ''' + table(["Write", "Copy", "Change"], rows) + '''
      ''' + callout("Then run", "<code>python check_my_learning.py</code>. Expect <code>3 of 3 right</code>; each hint names what to change.", "neutral") + '''
    </div>
  </div>''', '''<p>Two minutes. The split by customer on this slide is the function behind the honest numbers of Part 4; Y1 is the same idea for plants. Most common wrong answer: Y3 with <code>&lt; k</code>; the checker says rank 10 is a hit at k = 10.</p>'''))

SLIDES.append(slide("Lab time", "Lab", 48,
    head("Lab · 48 minutes", "Each student on their own machine. Checkpoints keep you on time.") + '''
  <div class="lu-cards" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:var(--lu-s4)">
    <div class="lu-card"><span class="lu-card__label">By minute 28 · Part A</span><p class="lu-sub">Graph built; baseline 1.000, 0.788, then near 0.02; GraphSAGE about 0.86 random; TransE below the count.</p></div>
    <div class="lu-card"><span class="lu-card__label">By minute 40 · Part B</span><p class="lu-sub"><code>python check_my_learning.py</code> says 3 of 3. Each hint names the change.</p></div>
    <div class="lu-card"><span class="lu-card__label">By minute 48 · Part C</span><p class="lu-sub">Answers to the three questions, one of them about your own team's data.</p></div>
  </div>
  ''' + callout("For your team project", "Milestone 2 asks for this evaluation on your own graph: a baseline, a split that does not leak, several seeds, and the limits written down.", "concept"),
    '''<p>Forty eight minutes. Numbers may differ in the last digit on another computer; the pattern must not (leak near 1.0, random high, by customer near 0.02, count ahead of TransE). If a student's pattern differs, check first that <code>build_graph.py</code> read Session 5's graph.</p>'''))

SLIDES.append(slide("Discussion: whose graph model lost?", "Wrap", 7, '''  <div class="lu-eyebrow">Discussion · as a room, from Part C</div>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <h2 class="lu-h2">Both graph models lost today. Is that a failure?</h2>
      <ol class="lu-list lu-list--num">
        <li>TransE lost to a count. What would the graph need for its shape to beat popularity?</li>
        <li>GraphSAGE won only where it could remember customers. How would you write that in a report without hiding it?</li>
        <li>Your own data: which field is the date, and which group (customer, supplier, site) must not be on both sides?</li>
      </ol>
    </div>
    ''' + callout("Why losing is reportable", "It says, with evidence, that the simple model is enough for this task on this data. That saves a company from running, and trusting, a model that only looks better.") + '''
  </div>''', '''<p>Seven minutes. The syllabus question verbatim: whose graph model lost to the tabular baseline, and why that is a legitimate and reportable result rather than a failure. Push for the specific wording of question 2: "on customers seen in training, PR-AUC 0.86; on new customers, no better than guessing".</p>'''))

rows = [("Node classification", "a heterogeneous GNN on your own graph, for your own label"),
        ("Link prediction", "an embedding such as TransE, filtered MRR and Hits@k"),
        ("A baseline", "a table model on the same rows, next to every result, and guessing"),
        ("A split that does not leak", "by time if your data has dates; by group otherwise, and say why"),
        ("The limits", "several seeds, the spread, and what the numbers do not show")]
SLIDES.append(slide("Milestone 2 and the project clinic", "Wrap", 5,
    head("Milestone 2 · due at the end of this session · 20% · on your team's own topic", "Today's lab is the pattern. The clinic checks one thing: does your split leak?", width=72) + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    ''' + table(["Part", "What it must show"], rows) + '''
    <div class="lu-card">
      <span class="lu-card__label">Project clinic · each team, 1 minute</span>
      <p class="lu-sub">Say your label, your split, and the one thing that could leak across it. The room names one more.</p>
      <p class="lu-caption">Removed features go in the report too, with the reason: the label hides in more places than one.</p>
    </div>
  </div>''', '''<p>Five minutes here; the full clinic runs in the discussion time if the lab finished early. The syllabus deliverable: a trained heterogeneous node classification model and a link prediction model over the integrated graph, a leakage-free temporal split, a tabular baseline, and a written evaluation of the limits. Scored against the project rubric criteria that apply now.</p>'''))

GLOSS = [
    ("Node classification", "A label for each node."),
    ("Link prediction", "A missing edge, found."),
    ("Baseline", "The simple rival to beat, or not."),
    ("Embedding · TransE", "A position per thing · h + r near t."),
    ("DistMult · ComplEx · RotatE", "Other ways to score a triple."),
    ("Negative sampling", "Made-up false triples for training."),
    ("Filtered ranking", "Other right answers removed first."),
    ("MRR · Hits@k", "Mean 1 / rank · share in the top k."),
    ("Message passing", "Nodes update from their neighbours."),
    ("GraphSAGE · to_hetero", "Own plus neighbours' mean · one copy per link kind."),
    ("Oversmoothing", "Too many layers, all nodes alike."),
    ("Inductive · transductive", "Scores new things · only seen ones."),
    ("Leakage", "The answer reaches the model."),
    ("PR-AUC", "Ranking of the rare class; guessing scores its share."),
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
      <p class="lu-statement">A model's score is only as honest as its split: compare with the simple rival, on things the model has never seen.</p>
      ''' + callout("Reading", "Kejriwal, Knoblock and Szekely (2021), chapter 10, Representation Learning for Knowledge Graphs. For the theory: Hamilton, <i>Graph Representation Learning</i>, free online.") + '''
    </div>
    <div class="lu-stack">
      <div class="lu-card">
        <span class="lu-card__label">Next session</span>
        <h3 class="lu-h3">Session 7 · The agentic query layer</h3>
        <p class="lu-sub">A stakeholder asks the graph a question in plain words; a language model writes the SPARQL, and a validation loop repairs it.</p>
      </div>
      <div class="lu-row"><span class="lu-tag lu-tag--green">For your team</span><span class="lu-caption" style="flex:1">Submit Milestone 2. Take the Session 7 open problems reading list from your instructor.</span></div>
    </div>
  </div>''', '''<p>Two minutes. End on the sentence. The syllabus issues the Session 7 open problems reading list here; hand it out with this slide.</p>''', kind="tint"))

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
