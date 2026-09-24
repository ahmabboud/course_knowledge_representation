# Course replan, Sessions 1 to 3

**Status: proposed, pending approval (2026-09-22).** Nothing below is built yet.
When approved, the authoring rules in section 2 move into `AGENTS.md`, and
`PROGRESS.md` tracks the build. Do not mark any session done without the
instructor's explicit agreement.

---

## 1. Why: what the audit found

Every number below comes from reading the actual decks, labs and files on
2026-09-22, not from memory.

### Slide depth and visuals

| Session | Content slides (no title, dividers, wrap) | With a diagram or table | Code only | Text only |
|---|---|---|---|---|
| 1 | 15 | 4 | 4 | 7 |
| 2 | 17 | 2 | 5 | 10 |
| 3 | 14 | 5 | 3 | 6 |
| 4 (depth benchmark) | 32 | 5 | 11 | 16 |

Session 4 has the depth you asked for, but even it is mostly text. The new
standard (section 2) applies to 1 to 3 now and to 4 to 6 in a later pass.

### Session 3 lab is broken by its own README

The README says the reasoner run "should come back clean, no unsatisfiable
classes". It does not. Verified with ROBOT 1.9.10 on your machine today:

| Reasoner | Impossible (unsatisfiable) classes found |
|---|---|
| ELK | `Order for a sole-sourced good` |
| HermiT | `Order for a sole-sourced good` and `Sole-sourced component` |

**Why, in plain words.** Our file reused two SCRO properties,
`dependsOnProduct` and `dependsOnSupplier`, to mean "a product needs this
component" and "a component comes from this supplier". In SCRO they mean
something else: both are kinds of BFO's *specifically depends on*, which only
a **dependent** thing (a role, a quality) can have. But a product and a
component are **physical things** (BFO *independent continuants*), and BFO
says nothing can be both. So no product can ever satisfy our definition,
and the reasoner marks the class impossible. ELK misses the second class
because it ignores "exactly 1" rules, which HermiT reads.

This is exactly what the syllabus asks the lab to teach ("read the inferred
hierarchy as a diagnostic: unsatisfiable classes... fix the model"). It just
was never designed in, explained, or verified.

### The data does not exist

`demos/data/brunel/brunel.zip` is 0 bytes, and DataCo was skipped (Kaggle
needs credentials). Session 1 profiling and Session 2 conversion cannot run
today. No slide in any session shows what the datasets contain.

### Terms used before they are defined (main ones)

- **Session 1:** ERP, WMS, PLM, TMS, CRM (never expanded), ontology,
  knowledge graph, RDF, property graph, triple and IRI (a drill asks for them
  before Session 2 teaches them), OWL, reasoner, SPARQL, GNN, cardinality,
  profiling, constraint inventory.
- **Session 2:** prefix, Turtle, datatype, `rdf:type`, EAV, endpoint, TDB2,
  variable and triple pattern, recursive CTE. **Missing entirely, although
  the syllabus lists them:** blank nodes, named graphs, serializations
  (N-Triples, JSON-LD), RDFS, constraint versus entailment, aggregation,
  federation.
- **Session 3:** first order logic, decidable, predicate, subsumption,
  satisfiable, entailment, Manchester syntax (the `some`, `only`, `and`
  that Protégé shows everywhere), **SubClassOf versus EquivalentTo** (the
  reason nothing gets auto classified), owl:Thing and owl:Nothing, every
  BFO term Protégé displays (continuant, material entity, role...),
  property characteristics and punning (both in the syllabus, both missing).

### Tools are used without a guide

No slide or document shows Protégé, ROBOT, Fuseki, Neo4j, OpenRefine or
the profiling report. Session 3's two screenshot slots are still placeholders.

---

## 2. Course authoring standard (new rules)

1. **Visual first.** Every concept slide leads with a picture that carries
   the idea: a diagram on the course's own entities, an annotated real
   screenshot, or a real data table. Text explains the picture, never the
   reverse. A bullets only slide is allowed only for glossary and wrap.
2. **Define at first use, visibly.** The first time a term appears in the
   course it is **bolded** and defined on the slide in one plain sentence
   (a visible definition box, not only a hidden popover). Later uses get a
   `.lu-term` popover. No term is used before its defining slide.
3. **Why, then how, then example.** Each part opens with the problem the
   idea solves, then the mechanism, then a worked example on the teaching
   slice.
4. **One cast of characters.** The same small set of real entities
   (section 3) appears on every slide in every session.
5. **No tool before its guide.** A lab never uses a tool until a guide
   with real annotated screenshots has shown it.
6. **Every deck ends with a glossary slide** listing the terms it
   introduced, matching the course glossary.
7. **Depth target:** about 30 content slides per session.
8. **Real only** (existing rule, kept): every screenshot, number, error
   message and output comes from a real run.

---

## 3. Shared foundations, built once

- **Real data, fetched and checked in.** DataCo (Mendeley DOI
  10.17632/8gx2fvg2k6.5, CC BY 4.0) and Brunel (7 tables, CC BY 4.0).
  Figshare's 202 response means "archive being prepared, retry", so
  `fetch_data.py` gets a retry loop.
- **The cast (teaching slice).** About 10 orders, 3 plants, 3 ports,
  3 carriers, 4 suppliers, drawn from real rows, each shown as a card with
  a friendly label. Reconciles today's inconsistency (Session 2 uses
  carriers `dhl, mae, xpo`, Session 6 uses `dhl, aramex, fedex`).
- **Course glossary** (`GLOSSARY.md` plus a glossary page): term, plain
  definition, session that introduces it.
- **Tool guides**, standalone pages in the course design system, step by
  step with real screenshots: Protégé (S3), ROBOT (S3), Fuseki and Neo4j
  (S2), Jupyter, ydata-profiling and OpenRefine (S1).

---

## 4. Session 3, new outline (build first)

Target: about 28 lecture slides plus the lab guide.

**Part 1 · What an ontology is** (why: "late" means two things to two teams)
1. Two dashboards, 12% late against 30% late: one word, two meanings.
2. An ontology in one picture: boxes, dots, arrows on the cast.
   Defines **ontology, class, individual, property**.
3. The class tree: Shipment, Late shipment, Cancelled shipment.
   Defines **subclass, owl:Thing**.
4. Two kinds of arrow: to a thing, or to a value.
   Defines **object property, datatype property, annotation**.
5. Two layers: rules above, data below. Defines **axiom, TBox, ABox**.

**Part 2 · Writing rules a machine can use** (classes drawn as sets)
6. Classes as circles of members. Defines **set semantics**.
7. `some` against `only`, compare wipe, each shown three ways: English,
   Protégé's words, Turtle. Defines **restriction, existential, universal,
   Manchester syntax**.
8. `and`, `or`, `not`, and disjoint circles. Defines **intersection,
   union, complement, disjoint**.
9. Counting: `exactly 1`, `min 2`. Defines **cardinality**.
10. Domain and range infer, they do not reject (SQL error against OWL
    inference). Defines **domain, range, entailment**.
11. SubClassOf against EquivalentTo: a one way door against a two way door.
    Only a **defined class** can pull data in by itself.
    Defines **primitive class, defined class**.
12. Property characteristics: transitive part of, functional, inverse.
13. Check question plus drill.

**Part 3 · What a reasoner does**
14. 4,809 axioms (your real metric): nobody checks that by hand.
    Defines **reasoner, inference**; open world recap in one picture.
15. Three jobs, three before and after trees.
    Defines **consistency, classification, subsumption, realization**.
16. The red class: what owl:Nothing means (your real screenshot).
    Defines **satisfiable, unsatisfiable, owl:Nothing**.
17. Walkthrough: the domain and range bug in four steps (kept).
18. Reading an explanation: the real chain behind the red class, drawn.
    Defines **justification**.
19. Check question.

**Part 4 · Reuse, and BFO in plain words**
20. Why reuse, and the stack BFO, IOF Core, SCRO, ours.
    Defines **upper ontology, BFO, IOF, SCRO, alignment**.
21. Things against happenings: a truck against a delivery.
    Defines **continuant, occurrent, process**.
22. A truck, its colour, its role, its paperwork.
    Defines **material entity, quality, role, independent, specifically
    dependent, generically dependent continuant**.
23. The reuse trap: our real bug, told as a story.
24. Competency questions decide scope (sort exercise and poll, kept).
25. Alignment hazards: sameAs and equivalentClass (kept, drawn).

**Part 5 · Profiles and reasoners**
26. Speed against expressiveness, one curve, one table.
    Defines **OWL profile, EL, QL, RL, DL, ELK, HermiT, decidable**.
27. Real proof: ELK finds 1, HermiT finds 2. Why.
28. Drill.

**Lab (guided, with the Protégé guide open)**
1. Tour the Protégé window (annotated screenshot).
2. Open the file, read IRI and metrics.
3. Read a class: annotations, SubClassOf, what each panel means.
4. Start ELK, switch Asserted to Inferred, find the red class.
5. Click **?**, read the explanation, translate it into plain words.
6. Switch to HermiT, find the second red class.
7. **Fix the model:** replace the misused SCRO properties with our own,
   rerun, nothing red.
8. **See the payoff:** make `At-risk shipment` a defined class, load three
   sample shipments, rerun, watch one get classified automatically
   (realization), confirm in DL Query.
9. ROBOT from the terminal: reason, report, read ERROR against WARN.
10. Licensing exercise (kept).

**Lab file changes:** current file becomes `scro-extension-v0.ttl` (the
buggy starting point, documented); a fixed `scro-extension-reference.ttl`;
new `sample-shipments.ttl` for realization; README rewritten honestly.
Every step verified with real ELK and HermiT runs before it ships.

---

## 5. Session 1, new outline

**Part 1 · The question and the course** (3): the sanction call; the five
systems as a picture with each acronym expanded; the Session 8 promise.
**Part 2 · Meet the supply chain and the data** (7, new): the supply chain
in one picture (supplier, plant, port, carrier, customer, order,
shipment, each defined); DataCo: origin, size, 5 real rows, key columns;
Brunel: the 7 tables as a diagram with one real row each; why they do not
join; the cast; check question.
**Part 3 · Meaning is not in the schema** (5): storing against meaning,
drawn; the boundary leak; first plain definitions of **schema, semantic
layer, ontology, knowledge graph**; the two meanings of "late"; check.
**Part 4 · The architecture** (4): stage by stage walkthrough (each stage
defined when shown); what each tool is, one line each; tooling honesty; poll.
**Part 5 · Profiling and hidden rules** (7): why profile; **cardinality,
null, distribution, referential integrity**, each on real data; the real
ydata-profiling report; real OpenRefine clusters; the constraint inventory
with a filled real row; the plant and port worked example drawn; rule
against exception. Open world stays, as one simple picture ("missing is
not false"); RDF against property graph moves to Session 2.
**Lab guide** (3): the smoke test explained, running the notebook,
filling the inventory.

## 6. Session 2, new outline

**Part 1 · From a table row to triples** (9): why a graph; the triple;
**IRI, namespace, prefix**; **literal, datatype**; one real Brunel row
converted into triples, step by step; foreign key becomes an edge;
**blank node**; **named graph**; one graph in Turtle, N-Triples, JSON-LD.
**Part 2 · IRI design** (3, kept, drawn).
**Part 3 · RDFS, the first meaning** (4, new): `rdf:type`,
`rdfs:subClassOf`, domain and range; **entailment against constraint**; check.
**Part 4 · SPARQL** (9): a pattern is a triple with holes (drawn); one
pattern, two patterns and the shared variable; OPTIONAL and FILTER;
aggregation on real late orders per carrier; the four forms; property
paths drawn as hops; the SQL comparison; federation; live sandbox.
**Part 5 · RDF against property graph** (3, moved here from Session 1).
**Lab guide** (4): Docker and the Fuseki screen, convert, load, query in
the Fuseki UI, the Neo4j browser.

---

## 7. Build order and how each is checked

0. Foundations: rules into `AGENTS.md`, data fetched, cast, glossary.
1. **Session 3:** Protégé guide, then lab fixes, then deck.
2. **Session 1**, then **Session 2**.
3. Later pass: apply the visual first standard to Sessions 4 to 6.

Each session: real tool runs, real screenshots, Playwright audit, then your
review. `PROGRESS.md` changes only after you agree it is done.

## 8. Open decisions

Asked separately, with a recommendation for each: scope (all three or
only Session 3), session length, where the Protégé guide lives, and who
captures screenshots and fetches the data.
