"""Session 3, Part 5: OWL profiles and the two reasoners.

The ELK against HermiT result is recorded in
demos/session-03-ontology/reference-outputs/explain_v0_ELK.md and
explain_v0_HermiT.md (ROBOT 1.9.10), and again with local_reasoner.py
(reference-outputs/my-axioms-check.txt).
"""
from common import slide, divider, defbox, callout, figure
from kit import flow, node, edge, defnote, table

SLIDES = []
IMG = "../assets/img/"

SLIDES.append(divider("Part 5 · Profiles and reasoners", "Profiles",
    "Part 5 of 5 · about 14 minutes",
    "One decision decides whether your reasoner finishes at all. Which one?",
    "How much of OWL you use. Less OWL, faster answers, and some questions you can no longer ask."))

# ---------------------------------------------------------------- Profiles
SLIDES.append(slide("Speed against expressiveness", "Profiles", 5, '''  <div class="lu-eyebrow">OWL profiles</div>
  <h2 class="lu-h2">Pick the part of OWL your workload can afford</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + table(["Profile", "Built for", "Gives up", "Reasoner"], [
        ["<b>EL</b>", "Very large class trees", "only, counting, not", "ELK, fast"],
        ["<b>QL</b>", "Queries over a relational database", "several constructs, to rewrite into SQL", "Ontop, Session 5"],
        ["<b>RL</b>", "Rule engines", "reasoning about unnamed things", "rule engines"],
        ["<b>DL</b>", "Everything OWL can say", "nothing, but can be slow", "HermiT, complete"],
    ], "Each of our classes records the profile it was written for, in a <code>ul:profile</code> note.") + '''
    <div class="lu-stack">
      ''' + defnote([
          ("OWL profile", "a restricted part of OWL chosen so reasoning stays fast."),
          ("Decidable", "a program is guaranteed to finish with the right answer. OWL DL is; full first order logic is not."),
          ("ELK · HermiT", "a very fast EL reasoner that ignores the rest; a complete, slower DL reasoner."),
      ]) + '''
    </div>
  </div>''', '''<p>Five minutes. The engineering point: the profile is a decision you make and record, not something you discover when the reasoner never returns. QL matters again in Session 5, where Ontop rewrites SPARQL into SQL.</p>
<ul><li>Description logic, the family OWL is built on, is first order logic cut down so the reasoner is guaranteed to finish. That is the whole bargain in one sentence.</li></ul>'''))

# ---------------------------------------------------------------- ELK 1, HermiT 2
n = [
    node("ssc", "Sole-sourced component", 260, 60, 320, 60, kind="ours", flag="right"),
    node("mc", "material component\nindependent continuant", 260, 210, 330, 76, kind="reused"),
    node("sup", "depends on supplier\nexactly 1 supplier", 800, 60, 330, 76, kind="reused"),
    node("sdc", "specifically dependent\ncontinuant", 800, 210, 320, 76, kind="upper"),
]
e = [edge("a", "ssc", "mc", "is a"), edge("b", "ssc", "sup", "exactly 1 (ELK skips this)"),
     edge("c", "sup", "sdc", "domain, through BFO"), edge("d", "mc", "sdc", "disjoint", both=True, kind="conflict")]
steps = [{"show": ["ssc", "mc", "a"], "run": ["a"], "set": {"ssc": "active"}},
         {"show": ["sup", "sdc", "b", "c"], "run": ["b", "c"], "set": {"sdc": "inferred"}},
         {"show": ["d"], "run": ["d"], "set": {"ssc": "impossible", "mc": "impossible", "sdc": "impossible"}}]
caps = [("A physical part", "<b>Step 1.</b> v0 says a sole-sourced component is a material component: a physical thing."),
        ("The counting rule", "<b>Step 2.</b> It also says it <b>depends on supplier exactly 1</b> supplier, and that property's domain makes it a dependent thing."),
        ("Only HermiT sees it", "<b>Step 3.</b> Physical and dependent are disjoint, so the class is impossible. ELK ignores <b>exactly 1</b>, so ELK never gets here. HermiT does.")]
pic = flow("Why HermiT finds a second red class", 1060, 280, n, e, steps, caps)
SLIDES.append(slide("ELK finds 1, HermiT finds 2", "Profiles", 4, '''  <div class="lu-eyebrow">A real result from the lab file</div>
  <h2 class="lu-h2">Same file, two reasoners: ELK finds one impossible class, HermiT finds two</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + pic + '''
    <div class="lu-stack">
      ''' + table(["Reasoner", "Impossible classes in v0"], [
          ["ELK", "Order for a sole-sourced good"],
          ["HermiT", "Order for a sole-sourced good<br>Sole-sourced component"],
      ]) + '''
      ''' + callout("So what", "A fast reasoner that says &ldquo;no errors&rdquo; only means no errors <b>it can see</b>. Run the complete one before you ship.") + '''
    </div>
  </div>''', '''<p>Four minutes. Real runs: ROBOT 1.9.10 with each reasoner on <code>scro-extension-v0.ttl</code> (<code>reference-outputs/explain_v0_ELK.md</code>, <code>explain_v0_HermiT.md</code>), and the same two classes again from <code>python local_reasoner.py workspace/scro-extension-v0.ttl</code> (HermiT, 13 seconds).</p>
<ul><li>This is the same trap as Part 4, a second time: <i>depends on supplier</i> is also a kind of BFO's <i>specifically depends on</i>. The fix is the same, our own <code>ul:suppliedBy</code>.</li></ul>'''))

# ---------------------------------------------------------------- Drill
SLIDES.append(slide("Drill: profiles and reasoning", "Profiles", 3, '''  <div class="lu-eyebrow">Drill · complete the statements</div>
  <div class="lu-blanks" data-qid="s3-blanks2" data-label="Profile and reasoning vocabulary">
    <p class="lu-h3" style="margin-bottom:var(--lu-s4)">Fill in the blanks</p>
    <ol class="lu-list lu-list--num">
      <li>Axioms about classes and properties live in the <input class="lu-blank" style="width:110px" data-answer="TBox|T-Box" data-label="Schema-level box" placeholder="?box">, facts about individuals in the <input class="lu-blank" style="width:110px" data-answer="ABox|A-Box" data-label="Instance-level box" placeholder="?box">.</li>
      <li>To query data that stays in PostgreSQL, choose the profile <input class="lu-blank" style="width:110px" data-answer="QL|OWL 2 QL|owl2 ql" data-label="Profile for query rewriting" placeholder="profile">.</li>
      <li>The reasoner that ignores &ldquo;exactly 1&rdquo; is <input class="lu-blank" style="width:140px" data-answer="ELK" data-label="Fast EL reasoner" placeholder="name">.</li>
      <li>The job that computes the full class tree is <input class="lu-blank lu-blank--wide" data-answer="classification" data-label="Reasoning task" placeholder="task">.</li>
    </ol>
  </div>''', '''<p>Three minutes. Ninety seconds to type, then check as a room.</p>''', kind="tint"))
