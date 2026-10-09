# Read first: what this lab is doing

Do not begin by opening Protégé or running a reasoner. First understand the
question this lab asks:

> How can an ontology reuse published meanings safely, and how can a reasoner
> expose a definition that is impossible or classify facts we did not label by
> hand?

This is individual practice, not graded work. You are not being asked to
memorise Protégé menus. You are following an ontology from a deliberately
broken first version, through a reasoner's explanation, to a repaired version
that classifies real course examples.

## The short story

In Session 2, the Brunel tables became an RDF graph. In this session, we add
an **ontology**: a shared, explicit account of what the graph's classes and
relationships mean. It lets a reasoner check whether our definitions can
possibly have members and infer classes that follow from the definitions.

We want to describe supply-chain ideas such as a sole-sourced component and
an at-risk shipment. Instead of creating every term from scratch, we reuse
the published **Supply Chain Reference Ontology (SCRO)** from the Industrial
Ontologies Foundry (IOF). SCRO is built in three layers, from the bottom up:

- **BFO** (Basic Formal Ontology) says what kinds of thing exist at all, such
  as physical objects and processes.
- **IOF Core** adds general industry terms on top of BFO.
- **SCRO** adds supply-chain terms, such as Shipment and Carrier, on top of
  IOF Core.

(The SCRO file's own label reads just "Supply Chain Ontology". It is the same
ontology.)

Each layer **imports** the one below it, which means it loads that ontology
and builds on its terms. Our course file imports only SCRO, and the rest
arrive through the chain:

```text
  +------------------------------------------------------+
  | OUR EXTENSION (course)                               |
  | SoleSourcedComponent, AtRiskShipment, hasComponent   |
  +------------------------------------------------------+
        | imports, and adds only what our questions need
        v
  +------------------------------------------------------+
  | SCRO  (supply chain)                                 |
  | Shipment, Carrier, dependsOnProduct                  |
  +------------------------------------------------------+
        | imports; its terms are specialisations of IOF Core terms
        v
  +------------------------------------------------------+
  | IOF Core  (general industry)                         |
  | Material product, Organization, Supplier             |
  +------------------------------------------------------+
        | imports; its terms are specialisations of BFO terms
        v
  +------------------------------------------------------+
  | BFO  (what kinds of thing exist at all)              |
  | independent thing, dependent thing,                  |
  | "specifically depends on"                            |
  +------------------------------------------------------+
```

Read upward, each box specialises the one below: a SCRO Shipment is a kind of
IOF Core thing, which is a kind of BFO thing. Read downward, each box inherits
the formal meaning of the one below. That inheritance is exactly what caused
the lab's mistake: our property borrowed SCRO's name, and so it also
inherited the BFO rule underneath.

The danger is that a property can have a familiar name but a different formal
meaning. The starting file reuses two SCRO properties because their names
sound right. Their definitions, inherited from BFO, make our physical product
and component impossible. A reasoner finds the conflict. The fixed ontology
uses two carefully defined course properties instead.

The lab follows this path. Read it top to bottom:

```text
1. START WITH TWO INGREDIENTS

   Reused (written by others)        Ours (written by the course)
   SCRO, IOF Core and BFO:           Our own supply-chain classes,
   ready-made classes and            such as Shipment and
   properties, each with a           AtRiskShipment, plus how we
   precise formal meaning            link them to the reused terms
                 \                   /
                  \                 /
                   v               v
2. OUR FIRST VERSION: scro-extension-v0.ttl
   It reuses two SCRO properties because their names sound right.
   Their formal meaning is not what we intended. This is a
   deliberate mistake.
                         |
                         |  run a reasoner (ELK, then HermiT):
                         |  a program that checks the definitions
                         v
3. THE REASONER REPORTS THE PROBLEM
   Some of our classes can never have a member (impossible
   classes), and it explains which axioms cause this.
                         |
                         |  replace the two reused properties with
                         |  two course properties that say what we mean
                         v
4. THE FIXED VERSION: scro-extension-reference.ttl
   No impossible classes.
                         |
                         |  add sample-shipments.ttl, run ELK again
                         v
5. THE REASONER CLASSIFIES FACTS FOR US
   Shipments handled by a sanctioned carrier are inferred to be
   AtRiskShipment, without anyone labelling them by hand.
```

## The business questions the ontology must earn

An ontology is useful only when it supports questions someone needs to ask.
This lab's reference ontology is organised around competency questions, for
example:

- Which shipments arrived after their committed date, by carrier?
- Which plants are authorised to serve a port, and which actually did so?
- If a supplier fails, which finished goods lose their only source of a
  component?
- Which freight-rate band applies to a shipment on a route?
- Which shipments are at risk because their carrier is sanctioned?

These questions explain why classes such as `LateShipment`,
`SoleSourcedComponent`, `FreightRateBand`, and `AtRiskShipment` exist. A
class is not added merely because its name sounds useful. See
[`competency_questions.md`](competency_questions.md) for the full list and
the class that answers each question.

## The examples you are using

The sample contains three shipments linked to real Brunel order identifiers
and the two anonymised carrier codes used in Sessions 1 and 2:

| Shipment of order | Carrier | What the reasoner should infer |
|---|---|---|
| `1447385217.7` | `V444_0` | Shipment, but not At-risk shipment. |
| `1447291369.7` | `V444_1` | At-risk shipment. |
| `1447311670.7` | `V444_1` | At-risk shipment, even though the file does not explicitly type it as a shipment. |

The third row demonstrates two inferences. The `handledBy` property has
`Shipment` as its domain, so using that property makes the subject a
shipment. Then the definition of `AtRiskShipment` makes a shipment handled by
a sanctioned carrier an at-risk shipment.

### Important: what is real and what is a teaching choice

- **Source facts:** the Brunel order identifiers and the carrier codes are
  real values from the course's Brunel data.
- **Course examples:** the three shipment statements are small teaching data
  built around those real identifiers; Brunel does not supply this shipment
  ontology file.
- **Teaching flag:** `V444_1` is marked as a `SanctionedCarrier` only so the
  definition has an example to classify. Brunel does not say that carrier is
  sanctioned, and its anonymised code is not a company name.
- **Deliberate mistakes:** the errors in `scro-extension-v0.ttl` are course
  examples. They are not claims that the published SCRO ontology is broken.
  SCRO's formal property meanings are real; our first reuse of them is wrong.

## The two ideas you will see

### 1. A reasoner catches a bad reuse decision

The v0 file uses SCRO's `dependsOnProduct` and `dependsOnSupplier` properties
to mean “has a physical component” and “is supplied by.” Their names are
tempting, but they are subproperties of BFO's “specifically depends on.” BFO
gives that relationship a domain for a dependent thing, whereas a material
product or component is a physical, independent thing. BFO declares those
two kinds disjoint.

So the reasoner concludes that no possible thing can be an `Order for a
sole-sourced good` or a `Sole-sourced component`. Protégé shows such a class
in red under `owl:Nothing`. This is an **unsatisfiable class**: a broken
definition, not a red record in the Brunel data.

The reference file fixes the meaning by using course properties with the
intended domains and ranges:

```text
Material product   --hasComponent--> Material component
Material component --suppliedBy----> Supplier
```

The lesson is simple: never reuse a property based only on its label. Read
its definition, domain, range, and superproperties first.

### 2. A defined class lets the reasoner add a useful type

The reference ontology defines an At-risk shipment as exactly:

```text
a Shipment that is handled by at least one Sanctioned carrier
```

“Exactly” matters. In OWL, `EquivalentTo` is a two-way definition. If the
facts meet the condition, the reasoner can add `AtRiskShipment`. A one-way
`SubClassOf` statement only says that existing at-risk shipments are
shipments; it does not let the reasoner recognise new ones.

## What each lab step proves

| Step | You run or open | What it does | What you should understand afterward |
|---|---|---|---|
| 1 | `fetch_ontologies.py` | Downloads the pinned IOF release once and builds `workspace/` with local imports. | Reuse must be reproducible; the catalog lets Protégé and the scripts find the same ontology files offline. |
| 2 | `scro-extension-v0.ttl` with ELK | Opens the deliberately broken starting ontology and checks it with the fast EL reasoner. | A reasoner checks whether a class definition can have a member, not merely whether Turtle syntax is valid. |
| 3 | the explanation for the red class | Shows the chain of axioms that makes the first class impossible. | The conflict comes from the meaning inherited through reused properties, not from their English names. |
| 4 | v0 with HermiT | Runs a more expressive OWL DL reasoner. | HermiT finds a second impossible class because it understands the `exactly 1` restriction that lies outside ELK's EL profile. |
| 5 | `scro-extension-reference.ttl` with HermiT | Opens the corrected ontology. | The two course properties say what we actually mean, and no course class is impossible. |
| 6 | `sample-shipments.ttl` with ELK | Classifies the three teaching shipments. | A domain assertion and an `EquivalentTo` definition can add types that were never written explicitly. |
| B | `my_axioms.ttl` and `check_my_axioms.py` | You write three small axioms; HermiT checks their meaning. | OWL axioms express constraints and definitions, not just labels. |
| C | `competency_questions.md` | You assess whether a class earns its place by answering a question. | The ontology should be driven by questions your project needs to answer. |

## Why there are two reasoners

| Reasoner | Use in this lab | Important limit |
|---|---|---|
| **ELK** | Fast checking and classification for the EL fragment of OWL. | It deliberately ignores constructs outside EL, including the qualified `exactly 1` restriction that causes the second v0 problem. |
| **HermiT** | More expressive OWL DL checking, used by the terminal fallback and the axiom checker. | It is slower, about 15 to 20 seconds in this lab. |

Different results are not a software failure. They show the trade-off between
speed and the OWL language features a reasoner supports.

## The files and their roles

| File | Role | What you do with it |
|---|---|---|
| `fetch_ontologies.py` | Fetches the pinned IOF/SCRO release, creates the offline catalog, and copies the course files into `workspace/`. | Run first; rerun rather than trying to repair missing imports by hand. |
| `workspace/` | The safe working folder where the catalog resolves imports locally. | Open ontology files from here in Protégé. |
| `workspace/supplychain/SupplyChain.rdf` | SCRO itself, the reused supply-chain axioms (about 4,200 lines of RDF/XML). | Do not edit. Read it in Protégé (select a class and look at its description panel), not as raw XML. |
| `workspace/core/Core.rdf` | IOF Core, the layer under SCRO. | Do not edit. Look here when a SCRO term is defined in terms of a Core term. |
| `workspace/cache/bfo/2020/bfo.rdf` | BFO, the bottom layer. The meaning behind the lab's mistake ("specifically depends on", and the disjointness of dependent and independent things) is defined here. | Do not edit. In Protégé, follow a property up through its superproperties to find it. |
| `scro-extension-v0.ttl` | The deliberate starting mistake. | Open it first; do not save over it. |
| `scro-extension-reference.ttl` | The corrected reference ontology. | Open it after you have examined v0's explanations. |
| `sample-shipments.ttl` | Three teaching individuals built on real Brunel identifiers. | Open it after the reference ontology to see classification. |
| `local_reasoner.py` | Terminal fallback that merges local imports and runs HermiT. | Use if Protégé is unavailable. |
| `my_axioms.ttl` | Three small axiom exercises. | This is your Part B work area. |
| `check_my_axioms.py` | Uses HermiT to check the meaning of your Part B axioms. | Run it after each attempt. |
| `competency_questions.md` | The questions each reference class is intended to answer. | Use it to understand why the ontology has each class. |
| `reference-outputs/` | Recorded explanations and results from real course runs. | Use it to verify a result, not as a file to edit. |

## Terms you need before starting

| Term | Plain definition |
|---|---|
| **ontology** | A formal, shared description of classes, relationships, and their meanings. |
| **axiom** | A statement the ontology treats as true, such as a class definition or a property domain. |
| **class** | A category of things, such as Shipment or Carrier. |
| **individual** | One particular thing, such as the shipment of order `1447291369.7`. |
| **property** | A named relationship between things, such as `handledBy`. |
| **domain** | A rule saying what kind of thing can appear as the subject of a property; using the property lets the reasoner infer that type. |
| **restriction** | A class condition involving a property, such as “handled by some sanctioned carrier.” |
| **reasoner** | Software that checks the logical consequences of ontology axioms and data. |
| **unsatisfiable class** | A class whose definition is contradictory, so it can have no members. Protégé shows it under `owl:Nothing`. |
| **inference** | A fact the reasoner adds because it follows from the axioms and stated facts. |
| **`SubClassOf`** | A one-way rule: every member of one class is also a member of another. |
| **`EquivalentTo`** | A two-way definition: meeting the stated conditions is enough for the reasoner to classify a thing in the class. |
| **EL / DL** | OWL language profiles: EL supports a fast, limited kind of reasoning; DL supports more expressions at a higher cost. |

## How to judge a claim in this lab

Keep these separate:

1. **Published ontology meaning:** SCRO, IOF Core, and BFO define their own
   classes and properties. The pinned release and its licence are recorded in
   `workspace/LICENCES.md` after step 1.
2. **Course modelling decision:** the course chooses which published terms to
   reuse, which new `ul:` terms to add, and how to define them. Those choices
   must be justified by a competency question and the imported meanings.
3. **Teaching data:** the sample uses real Brunel identifiers but includes a
   fictional sanction flag and constructed shipment facts to make an
   inference visible.
4. **Reasoner result:** “this class is impossible” or “this shipment is at
   risk” follows from the stated axioms and data. Reproduce it with the
   reasoner, then compare it with `reference-outputs/`.

Now return to the [lab README](README.md), then begin Part A.
