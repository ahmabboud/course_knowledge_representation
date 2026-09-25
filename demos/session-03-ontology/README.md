# Session 3 lab: find the bug, fix it, write your own

**Why this lab exists:** to make the lecture concrete (classes and
restrictions, domain and range, SubClassOf against EquivalentTo, reuse of a
published ontology, BFO, ELK against HermiT) and to prepare the ontology
your team project will extend. Nothing is handed in or graded. The lab
works when you can explain why the reasoner turned a class red, and why the
fixed file does not.

**Read this first:** [What this lab is doing](OVERVIEW.md). It explains the
ontology problem, the Brunel examples, the reasoner results, the role of every
file, the essential terms, and the difference between source facts, course
modelling choices, and teaching data. Do not start Part A until the overall
story is clear.

Every number in `lectures/kr-session-03.html` comes from the files in
`reference-outputs/`, produced by these scripts on 2026-09-24.

## Before you start

- Shared setup from `demos/README.md` done in Session 1: Python 3.12,
  `demos/.venv` (keep it active), **Protégé Desktop** and **JDK 21**, both
  checked by Session 1's smoke test. New to Protégé? Watch the
  [Protégé fundamentals videos](https://www.youtube.com/watch?v=CduRWyyL3q8&list=PLNohRKRAHaszTV3puqFM9yXDXnEqjS6Fd)
  (the Protégé videos in that playlist) before the session.
- Run every command from this folder, `demos/session-03-ontology/`.
- **Always open files from `workspace/`**, never from this folder: only
  there does `catalog-v001.xml` send every import to a local file, so
  Protégé works offline.
- No Protégé, or it will not start? Do not debug it in the room.
  `python local_reasoner.py <file>` runs HermiT from the terminal and lists
  the same impossible classes (about 15 seconds). You lose the Protégé
  explanation window; read `reference-outputs/explain_v0_ELK.md` and
  `explain_v0_HermiT.md` instead, which hold the same explanations.

## Part A · build and observe (about 30 minutes)

1. `python fetch_ontologies.py` (about a minute, needs the network once).
   Downloads IOF Core and Supply Chain (SCRO) at release `Release_202603`
   with their catalog and cached BFO imports, the GS1 Web Vocabulary, and
   copies this lab's four files into `workspace/`. **Expect:** it ends by
   confirming that the SupplyChain, Core and BFO imports resolve to local
   files. A failed GS1 download only warns; GS1 is not needed today.
2. In Protégé: **File, Open**, `workspace/scro-extension-v0.ttl`. Menu
   **Reasoner, ELK**, then **Reasoner, Start reasoner**. **Expect:** one
   class in red, `Order for a sole-sourced good`, listed under
   `owl:Nothing` in the inferred class hierarchy. **Look at:** switch the
   hierarchy dropdown from Asserted to Inferred to see what the reasoner
   added.
3. Click the **?** next to the red class. **Expect:** an explanation of six
   lines, the chain on the slide "The reuse trap". **Notice:** only the
   first line is ours. We used SCRO's `depends on product` for its name,
   and its domain, through BFO, makes our product a specifically dependent
   continuant, which BFO says a material thing can never be.
4. **Reasoner, HermiT**, then **Reasoner, Start reasoner** (HermiT
   takes about 15 seconds on a cold start; it is not frozen). **Expect:** a
   second red class, `Sole-sourced component`. Click its **?**. **Notice:**
   the same trap through `depends on supplier` inside an `exactly 1`
   restriction, which is outside the EL profile, so ELK never looked at it.
5. Open `workspace/scro-extension-reference.ttl` (the fixed file, a
   different ontology IRI, so both can stay open). Run HermiT. **Expect:**
   no red class. **Look at:** `Order for a sole-sourced good` and
   `Sole-sourced component` now use our own properties, `ul:hasComponent`
   and `ul:suppliedBy`. That is the whole fix.
6. Open `workspace/sample-shipments.ttl` (three shipments of real Brunel
   orders, two real carriers) and run ELK. Open the **Individuals by
   class** tab, or ask **DL Query** for `At-risk shipment`. **Expect:** the
   shipments of orders `1447291369.7` and `1447311670.7`, both handled by
   carrier V444_1; not the shipment of `1447385217.7` (carrier V444_0).
   **Notice:** the last shipment has no type at all. The domain of
   `handled by` makes it a Shipment, then the EquivalentTo definition makes
   it at risk. V444_1 is typed Sanctioned carrier for this session only, a
   teaching flag, not a fact in the Brunel data.

Same results from the terminal (the fallback, HermiT through owlready2):

```sh
python local_reasoner.py workspace/scro-extension-v0.ttl         # impossible: Order for a sole-sourced good, Sole-sourced component
python local_reasoner.py workspace/scro-extension-reference.ttl  # impossible: none
```

## Part B · write your own axioms (about 15 minutes)

Open `my_axioms.ttl`. It asks for three axioms, each practising one idea
from the lecture: Y1 disjointness (no plant is a port), Y2 a defined class
with EquivalentTo and an intersection (late and at risk), Y3 `some` and
`only` together (every carrier sanctioned, and at least one). Write each
under its marker, in a text editor or in Protégé (save as Turtle), then:

```sh
python check_my_axioms.py
```

The checker runs HermiT (about 20 seconds) and says, per question, right or
not yet, with a hint. It tests what your axiom means, not how it is
spelled, so any correct axiom passes. **Expect** when all three are right:
`3 of 3`. Stuck after trying? `solutions/my_axioms_solutions.ttl`. The
common wrong answers and the checker's hints are in
`reference-outputs/my-axioms-check.txt`.

## Part C · think (about 10 minutes)

Answer for yourself, then in the closing discussion:

1. `ul:CancelledShipment` answers no competency question
   (`competency_questions.md`). Keep it or delete it, and what question
   would earn it a place?
2. Why did ELK miss the second red class, and when is that acceptable?
3. Name the three main kinds of thing in **your team project's own data**.
   Which are continuants, which occurrents, and which published class would
   each subclass?

## Optional

- **ROBOT, the same checks in a script.** From `workspace/`:
  `python ../robot_report.py --input scro-extension-v0.ttl` stops at the
  impossible classes and writes `explain.md`;
  `python ../robot_report.py` reasons over the fixed file and writes the
  quality report, `report.tsv`. Needs ROBOT and the JDK
  (robot.obolibrary.org/#installing); the script says what is missing.
- `python realize_sample.py` (ROBOT again) classifies the sample shipments
  twice, as shipped and with At-risk shipment turned into SubClassOf: the
  table on the slide "SubClassOf and EquivalentTo".
- Instructor demos used in the lecture:
  `python closed_world_demo.py` (a database refuses a row that OWL
  accepts and types) and
  `python local_reasoner.py workspace/domain-mistake.ttl` (one careless
  fact makes the whole ontology inconsistent).
- The licensing exercise (lecture, 10 minutes as a room): SCORVoc,
  [`vocol/scor`](https://github.com/vocol/scor), declares `scor.ttl` under
  ODC PDDL while the same repository's README says "All rights reserved".
  Check it is still so before teaching. `workspace/LICENCES.md` records the
  licences of what this lab reuses: IOF is MIT, GS1 is Apache 2.0 with a
  patent caveat.

## You understood this lab if you can say

- why a property borrowed for its name can make your own class impossible;
- why ELK found one red class and HermiT two;
- why the untyped shipment still became an at-risk shipment (domain, then
  EquivalentTo), and why a database would have refused it instead;
- what `some` and `only` each say, and why Y3 needs both.

## Take it to your team project

- `scro-extension-reference.ttl` is the model for your project ontology:
  import a published ontology, add your classes under its classes, and tag
  each class with the competency question it answers (`ul:answersCQ`).
- Before you reuse any property, open its definition and read its domain
  and range. Then run a reasoner before anyone else sees the file.
- Your Part C answer 3 is the first draft of where your classes attach.
- Record the licence of every ontology and dataset you reuse; your final
  report lists them.
