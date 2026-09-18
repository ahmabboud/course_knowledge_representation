# Session 3 lab: ontology construction in Protege

Builds the syllabus deliverable: a domain ontology v1 on IOF SCRO,
eight annotated competency questions, a clean reasoner run, a recorded
OWL profile, and a ROBOT quality report, per
`course_knowledge_representation/lectures/kr-session-03.html`'s lab
brief slide.

Protege itself is a GUI application, so this lab is smaller than
Sessions 1 and 2's: what's scriptable is built and verified below;
running the reasoners and reading the inferred hierarchy live is
yours to do in the room, per the lecture.

## Run, in order

1. `python fetch_ontologies.py` — downloads the real ontologies this
   lab builds on into `workspace/` (gitignored, regenerate, do not
   commit): IOF Core and Supply Chain (SCRO) at release `Release_202603`
   from the real IOF repository, with the repo's own `catalog-v001.xml`
   and cached BFO/OMG-Commons imports, so Protege resolves everything
   **offline**; and the GS1 Web Vocabulary, for the reuse step. Ends
   by checking that the SupplyChain → Core → BFO import chain actually
   resolves to a local file, not just that the download succeeded.
2. In Protege: **Open File**, browse to
   `workspace/scro-extension-starter.ttl`, then immediately **Save As**
   `scro-extension.ttl` in the same folder, so you are editing your own
   copy, not the reference file. This is the "provided workspace with
   IOF SCRO already loaded" the lecture's lab brief opens with: SCRO is
   already imported, two worked-example classes are already there
   (`ul:LateShipment`, `ul:CancelledShipment`), and `ul:answersCQ` /
   `ul:profile` are already declared as annotation properties.
3. Fill in `competency_questions_template.md` as you draft your eight
   competency questions, four are given, four are yours. Each becomes a
   `ul:answersCQ` annotation on the class that answers it.
4. Extend `scro-extension.ttl` with the classes and properties your
   Session 1 constraint inventory demands, reusing SCRO or GS1 Web
   Vocabulary terms where they fit, per the lecture's reuse-first
   ordering.
5. In Protege: run **ELK**, then **HermiT** (both bundled reasoner
   plugins, checked by Session 1's smoke test). Read the inferred class
   hierarchy for unsatisfiable classes, unintended equivalences, and
   subsumptions you did not mean. Fix the model, not the reasoner
   output, and re-run until the hierarchy matches your intent.
6. `python robot_report.py --input scro-extension.ttl` — runs the two
   commands the lecture's lab brief shows verbatim
   (`robot reason ... --reasoner ELK`, then `robot report ... --profile QC`),
   writing `reasoned.ttl` and `report.tsv` next to your file. Needs
   ROBOT itself (a JDK plus `robot`, see robot.obolibrary.org/#installing);
   the script checks for it and tells you what's missing rather than
   failing silently.
7. The ten-minute licensing exercise, done live in the room (see
   below), is not pre-solved here on purpose.

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
there verbatim from the vocabulary file itself, not paraphrased.

## Real tools, matching the lecture

- **Protege** (GUI, checked by Session 1's smoke test), the **ELK** and
  **HermiT** reasoner plugins (bundled with Protege).
- **IOF SCRO** (Industrial Ontology Foundry Supply Chain Reference
  Ontology, MIT licensed), the starting ontology, real, downloaded by
  `fetch_ontologies.py`, not a stub.
- **GS1 Web Vocabulary**, for term reuse.
- **ROBOT** (robot.obolibrary.org), for the quality report and OWL
  profile check.

## What "done" looks like

A domain ontology v1 built on IOF SCRO (`scro-extension.ttl`), eight
annotated competency questions, a clean reasoner run, a recorded OWL
profile, and a ROBOT quality report (`reasoned.ttl`, `report.tsv`).
Committed to your repository, per the lecture's own deliverable slide,
not sitting on your laptop.
