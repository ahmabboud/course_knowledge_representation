"""Session 7, Part 4: measuring it, the TEXT2SPARQL way.

The three settings' numbers are read from
demos/session-07-access-layer/reference-outputs/evaluate.txt, the
instructor's recorded run; until it exists the slide says so. Leaderboard:
TEXT2SPARQL 2026 overall results (text2sparql.aksw.org, published
2026-05-13).
"""
import re
from pathlib import Path

from common import slide, divider, defbox, callout, code
from kit import head, table, bar

SLIDES = []
S, C, E = '<span class="tok-str">', '<span class="tok-com">', '</span>'
EVAL = Path(__file__).resolve().parents[2] / "demos" / "session-07-access-layer" / "reference-outputs" / "evaluate.txt"


def rules_id():
    """The same fingerprint of the prompt rules as access_layer.RULES_ID."""
    import hashlib
    src = (EVAL.parents[1] / "access_layer.py").read_text()
    rules = re.search(r'RULES = """(.*?)"""', src, re.S).group(1)
    return hashlib.sha256(rules.encode()).hexdigest()[:8]


def recorded():
    """{setting: (f1, refused_right, refused_wrong, repaired)} and the header line, or None.
    A recording made with other prompt rules than today's is ignored: its numbers are stale."""
    if not EVAL.exists():
        return None, None
    txt = EVAL.read_text()
    if f"rules {rules_id()}" not in txt.splitlines()[0]:
        return None, None
    out = {}
    for m in re.finditer(r"^(\w+)\s+mean F1 ([\d.]+) on \d+ answerable questions; refused (\d+) of \d+ it should; "
                         r"refused (\d+) it should not; (\d+) answered after a repair", txt, re.M):
        out[m.group(1)] = (float(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)))
    return out, txt.splitlines()[0]


SLIDES.append(divider("Part 4 · Measuring", "Measuring",
    "Part 4 of 5 · about 16 minutes",
    "Is the repair loop worth it? The examples? Believe a number, not a demo.",
    "Score every answer against the right one, on questions the model has never seen."))

gq = (f'''GET /?question=How many late orders are there?
     &amp;dataset=https://ul.edu.lb/kr/brunel/

{{"dataset": "https://ul.edu.lb/kr/brunel/",
 "question": "How many late orders are there?",
 "query": "SELECT (COUNT(?o) AS ?n) WHERE ..."}}''')
SLIDES.append(slide("The TEXT2SPARQL contract", "Measuring", 3, '''  <div class="lu-eyebrow">serve.py · what a benchmark calls</div>
  <h2 class="lu-h2">One web address in, one query out: any system, any harness</h2>
  <div class="lu-split lu-split--wide-left">
    ''' + code("the request and the reply", gq) + '''
    <div class="lu-stack">
      ''' + defbox([("TEXT2SPARQL", "A yearly benchmark for text to SPARQL systems, with a fixed contract and scorer.")]) + '''
      ''' + callout("Why a contract", "The harness runs the returned query itself and scores the rows. So the system is judged on answers, not on how it got them.", "neutral") + '''
    </div>
  </div>''', '''<p>Three minutes. The contract is TEXT2SPARQL's (2025 and 2026 editions): <code>GET /?question=...&amp;dataset=...</code> returning dataset, question and query. The official client, <code>text2sparql-client</code>, can call <code>serve.py</code>; the lab's own <code>evaluate.py</code> scores the same way without it.</p>'''))

rows = [("Right answer (the gold query)", "V444_0 · V444_1 · V44_3"),
        ("An answer to score (made up)", "V444_0 · V44_3 · V444_5"),
        ("In both", "V444_0 · V44_3: 2 values")]
SLIDES.append(slide("Scoring one answer", "Measuring", 4,
    head("Test question 3: &ldquo;Which carriers carry orders?&rdquo;", "Every value returned goes into one set; compare it with the right set") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <div class="lu-stack">
      ''' + table(["", "The set of values"], rows) + '''
      <p class="lu-statement" style="font-size:var(--lu-t-h3)">precision 2/3 · recall 2/3 · F1 0.67</p>
    </div>
    <div class="lu-stack">
      ''' + defbox([("Execution accuracy", "Judging a query by the answer it returns, not by its text.")]) + '''
      ''' + callout("Why not compare query text?", "The same answer has many correct queries. Only the answer can be compared fairly.", "neutral") + '''
    </div>
  </div>''', '''<p>Four minutes. The right set is real (the three carriers with orders); the answer to score is made up for the example (V444_5 has rate bands but no orders). This is exactly <code>score_utils.py</code>: set precision, recall and F1, as TEXT2SPARQL computes them.</p>'''))

SLIDES.append(slide("Check: one number", "Measuring", 3, '''  <div class="lu-eyebrow">Check question</div>
  <div class="lu-mcq" data-qid="s7-q2" data-answer="b" data-label="F1 of a count that is slightly wrong"
       data-fb-correct=" A count is a set of one value: it is right or it is not."
       data-fb-wrong=" Write both answers as sets and count what they share.">
    <p class="lu-mcq__q">Test question 1's right answer is the single value 9,215. Suppose a model's query returns 9,023. What F1 does it score?</p>
    <div class="lu-mcq__opts">
      <button class="lu-mcq__opt" type="button" data-key="a">0.98, it is close<span class="lu-mcq__why" hidden>Sets do not measure closeness: 9,023 is not 9,215.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="b">0<span class="lu-mcq__why" hidden>Right: {9023} and {9215} share nothing.</span></button>
      <button class="lu-mcq__opt" type="button" data-key="c">0.5, half right<span class="lu-mcq__why" hidden>There is nothing half right in a set of one value.</span></button>
    </div>
  </div>''', '''<p>Three minutes. This is the subclass mistake again: the check passes it, the score does not.</p>''', kind="tint"))

rec, header = recorded()
if rec:
    rows = [(f"<b>{s}</b>" if s == "repair" else s, d, f"{rec[s][0]:.3f}", f"{rec[s][1]} of 3", str(rec[s][2]), str(rec[s][3]))
            for s, d in (("schema", "the schema only"), ("examples", "plus 3 examples"), ("repair", "plus check and repair")) if s in rec]
    note = header.split("(recorded ", 1)[-1].rstrip(")")
    cap = f"Recorded run: {note}. Your live run may differ."
    notes = f'''<p>Four minutes. <code>reference-outputs/evaluate.txt</code>, {note}. Ask: is the gain from one setting to the next bigger than the difference between two students' runs? Compare two laptops in the room.</p><ul><li>In this run the examples did all the work (questions 7 and 10 went from 0 to 1) and the repair loop added nothing: no query failed the check. That is a real result: the loop is insurance against a failure this model did not make here, and a room of live runs may show it.</li></ul>'''
else:
    rows = [(s, d, "recorded run pending", "", "", "") for s, d in (("schema", "the schema only"), ("examples", "plus 3 examples"), ("repair", "plus check and repair"))]
    cap = "The instructor's recorded run (record_llm.py) fills this table."
    notes = '''<p>Four minutes. <b>Not recorded yet:</b> run <code>python record_llm.py</code> on the Mac, then rebuild this deck; the table reads <code>reference-outputs/evaluate.txt</code>.</p>'''
SLIDES.append(slide("Three settings, one test set", "Measuring", 4,
    head("15 questions: 12 answerable, 3 to refuse; mean F1 on the 12", cap) + '''
  ''' + table(["Setting", "What the model gets", "Mean F1", "Refused rightly", "Refused wrongly", "Repaired"], rows) + '''
  ''' + callout("Read it as Session 6 taught", "One run, 15 questions: a difference of one question is 0.08 of F1. State what changed, by how much, and whether it survives a second run.", "neutral"),
    notes))

lb = [("SPARQL-LLM", 0.790), ("INFAI-ETI-AND-FRIENDS-A", 0.593), ("ADFR", 0.418)]
bars = "".join(f'<div class="lu-stack" style="gap:var(--lu-s2)"><span class="lu-card__label">{n}</span>' + bar(v, 1, f"{v:.3f}", "red" if i == 0 else "ink") + '</div>'
               for i, (n, v) in enumerate(lb))
SLIDES.append(slide("The TEXT2SPARQL 2026 leaderboard", "Measuring", 3,
    head("TEXT2SPARQL 2026, overall F1, the top three", "The winner is the system this lab imitates in small") + '''
  <div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <div class="lu-stack" style="gap:var(--lu-s4)">''' + bars + '''</div>
    <div class="lu-stack">
      ''' + callout("Not our number's rival", "Their questions are over DBpedia and a corporate graph, and there are many more of them. Ours are 15 over Brunel. The metric is the same; the test is not.") + '''
      ''' + callout("What wins", "SPARQL-LLM: VoID, retrieved examples, validation and repair. The same four parts as the lab, done at scale.", "neutral") + '''
    </div>
  </div>''', '''<p>Three minutes. Results published 2026-05-13 at text2sparql.aksw.org (datasets DB26 and CK26). In 2025 the organisers reported a plain Qwen2.5 7B model at 0.129 on DBpedia: grounding is most of the difference.</p>'''))
