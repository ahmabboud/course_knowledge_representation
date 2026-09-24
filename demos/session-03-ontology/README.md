# Session 3 lab: run and observe ontology construction in Protege

Run live in the room, per `demos/README.md`: this is the instructor's
own copy of the lab, projected and narrated step by step, students
follow along on their own screens with the same files. Nobody drafts a
competency question or extends the ontology in this lab. That authoring
skill is real and gets practiced on each team's own capstone topic
(see `PROJECT-REDESIGN.md`), starting right after Session 1, not here.
This lab exists to show, once, cleanly, and without anyone stuck
debugging their own file, what the whole pipeline looks like when it
works: reuse a published ontology, reason over an extension of it, and
read what a real quality report says.

Every file this lab opens is finished. If something looks broken, it
almost always is not, see "Nothing here is broken" below before
assuming otherwise.

## Working directory

Complete the shared environment setup from `demos/README.md` first. Run the
two Python commands below from `demos/session-03-ontology/`, with the shared
`demos/.venv` activated. Paths beginning with `workspace/` are relative to
this Session 3 folder on both macOS/Linux and Windows.

## Learn Protege first

New to Protege? Before this lab, watch the short video series on Protege
fundamentals the instructor recommends:
<https://www.youtube.com/watch?v=CduRWyyL3q8&list=PLNohRKRAHaszTV3puqFM9yXDXnEqjS6Fd>
(The AI & DS Channel; the playlist is titled "Big Data" on YouTube, the
Protege videos are the ones to watch). Then read the course's own
screen by screen guide, `lectures/guide-protege.html`, which uses this
lab's exact files.

## Run, in order

1. **`python fetch_ontologies.py`** — downloads the real ontologies
   this lab runs against into `workspace/` (gitignored, regenerate, do
   not commit): IOF Core and Supply Chain (SCRO) at release
   `Release_202603` from the real IOF repository, with the repo's own
   `catalog-v001.xml` and cached BFO/OMG-Commons imports, so Protege
   resolves everything **offline**; the GS1 Web Vocabulary, for the
   licensing exercise later; and a copy of the finished reference
   ontology, `scro-extension-reference.ttl`. Ends by checking that the
   SupplyChain to Core to BFO import chain actually resolves to a
   local file, not just that the download succeeded. If the GS1
   download fails (a flaky network, nothing more), the script warns
   and keeps going, that file is not needed until step 6.

2. **In Protege: Open File**, browse to
   `workspace/scro-extension-reference.ttl`. Open it directly, there is
   no Save As step, nothing in this file gets edited today. SCRO is
   already imported, and every class in the file already carries a
   `ul:answersCQ` or an explanatory comment for why it does not, see
   `competency_questions.md` for the full map from question to class.

3. **Run ELK, then HermiT** (both bundled reasoner plugins, checked by
   Session 1's smoke test). Read the inferred class hierarchy together.
   Point at what the reasoner added that nobody asserted directly, for
   example `ul:AtRiskShipment` and `ul:SanctionedCarrier` composing
   rather than duplicating each other, that composition is the payoff
   of modelling this way instead of writing a flat list of unrelated
   classes. This run should come back clean: no unsatisfiable classes,
   no unintended equivalences. If it does not, see "Nothing here is
   broken" below before treating it as a teaching moment about a real
   bug.

4. **`python robot_report.py`** — runs the two commands the lecture's
   lab brief shows (`robot reason ... --reasoner ELK`, then
   `robot report ... --fail-on none`) against
   `workspace/scro-extension-reference.ttl`, writing `reasoned.ttl` and
   `report.tsv` next to it. Needs ROBOT itself (a JDK plus `robot`, see
   robot.obolibrary.org/#installing); the script checks for it and
   tells you what is missing rather than failing silently. Read
   `report.tsv` together: this is what a clean report from a finished
   ontology actually looks like, the thing to compare a real, in-
   progress submission against once teams start running this same
   pipeline on their own project.

5. **Discuss `ul:CancelledShipment` live.** It has no
   `ul:answersCQ`, on purpose, see `competency_questions.md`. Ask the
   room: keep it or delete it, and what competency question, if any,
   would earn it a place. This is the one place in the walkthrough
   where the room reasons about the model rather than just watching it
   run.

6. **The ten-minute licensing exercise**, below, run as a live,
   whole-room pause.

## Nothing here is broken

Everything this lab opens, `scro-extension-reference.ttl`, the ELK and
HermiT run, and `report.tsv`, is meant to come back clean, or with only
the two documented exceptions above (`CancelledShipment`,
`CommittedDate`/`Plant`/`Port`). If Protege reports an unsatisfiable
class, HermiT never returns, or `report.tsv` shows an ERROR row nobody
here put there on purpose, that is a real problem with this lab's own
files, environment, or the IOF release having changed shape upstream,
not a lesson to teach through. Stop and fix it (or fall back to a
previous release tag) rather than narrating a bug as if it were part of
the design. The one known slow step: HermiT can take a while to return
on a cold JVM start, give it a minute before assuming it has hung.

## The licensing exercise, verified real and still live

The lecture has the room resolve a real licence conflict:
[`vocol/scor`](https://github.com/vocol/scor) (SCORVoc, the vocabulary
this course deliberately does not build on) declares its `scor.ttl` as
`dct:license` [ODC PDDL](http://www.opendatacommons.org/licenses/pddl/1.0/)
(public domain), while that **same repository's** `README.md` carries
"© APICS 2015 [...] All rights reserved." Confirmed live, both
statements, while building this lab. If IOF has fixed it by the time
you teach, say so on the day and let the room verify that rather than
swapping in a different example.

`workspace/LICENCES.md` (written by `fetch_ontologies.py`) records the
licences for what this lab actually reuses: IOF SCRO and Core are MIT;
GS1 Web Vocabulary is Apache 2.0 with a patent-claims caveat, quoted
there verbatim from the vocabulary file itself, not paraphrased. Worth
naming live that `scro-extension-reference.ttl` checked GS1 for terms
covering "port" and "freight rate band" and found neither, an honest,
unglamorous outcome of reuse-first search that is just as real as a
successful reuse.

## Real tools, matching the lecture

- **Protege** (GUI, checked by Session 1's smoke test), the **ELK** and
  **HermiT** reasoner plugins (bundled with Protege).
- **IOF SCRO** (Industrial Ontology Foundry Supply Chain Reference
  Ontology, MIT licensed), real, downloaded by `fetch_ontologies.py`,
  not a stub.
- **GS1 Web Vocabulary**, checked for reuse, see above.
- **ROBOT** (robot.obolibrary.org), for the quality report and OWL
  profile check.

## What this walkthrough shows

A domain ontology already built on IOF SCRO, answering eight
competency questions (`competency_questions.md`), a clean ELK and
HermiT run, a recorded OWL profile per class, and a real ROBOT quality
report, read together, not built today. Nothing to submit from this
session. Apply the same pipeline, fetch a real vocabulary, extend it
where it falls short, reason over it, run ROBOT, to your own team's
capstone topic as you build it.
