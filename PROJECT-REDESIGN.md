# Project redesign: team topics replace the single shared case

Decided 2026-09-17. This is the locked source of truth for the new
capstone project. Read this before touching the syllabus or any lecture
module, several of those still describe the old single-case,
individual-work design and need to be brought in line with what is
written here, not the other way around.

## Why this exists

The original design (one supply chain case, one ontology, individual
work, defended one student at a time) has two problems at cohort scale:

1. **Defense math does not work.** Session 8 has a 150-minute supervised
   build and defense block. At 24 individual students that is about 6
   minutes each, for both deployment supervision and a defense meant to
   cover an 11-line rubric. Not a real defense.
2. **A single shared case is the easiest shape to hand a coding agent.**
   Everyone building the same ontology on the same data means the
   pipeline itself, not the student's understanding of it, is what is
   actually being produced and graded.

Team size fixes the first problem directly (see `DSCAI`'s own
`PROJECT-REDESIGN.md`, decided the same day, for the reference case).
Team topic choice weakens the second, though it is a partial fix, not a
complete one: unlike DSCAI's paper-extension model, KR does not add a
novelty requirement. This course teaches applied engineering competence,
not research contribution, so no idea-pitch or extension gate was added.
What KR relies on instead is that 8 to 12 teams, each on a different
open database, cannot share or look up a common answer key the way 24
students on one fixed case eventually could.

## What changes

### Teams of 2 to 3

Individual work is dropped. Teams of 2 to 3, formed by the students
themselves, working together for the rest of the course from directly
after Session 1.

**Formation:** self-formed, free choice, no instructor assignment.
**Deadline:** locked in before Session 2 starts, giving a few days after
Session 1 to find teammates and agree on a topic. A student left without
a team by the deadline is placed by the instructor into a team with
space, so no one is left out.

### The shared case stays, as the teaching vehicle, for the whole course

Session 1 through Session 8 lectures and labs continue to be taught and
demonstrated on the course's own supply chain case (DataCo and Brunel),
exactly as today. This is deliberate: a common worked example is what
makes concept teaching efficient, and the instructor only has to support
one dataset live in the room.

**Topic choice happens directly after Session 1.** From that point, each
team is encouraged to progress their own chosen project, on their own
chosen database, in parallel with the taught labs, mirroring each
session's technique on their own data as they go. This is not a graded
weekly checkpoint. **Evaluation happens at the end**, on the team's own
accumulated project, not on their in-class exercises against the shared
case.

Practical effect: the shared case is now purely a teaching device. The
graded artifact is always the team's own system, on the team's own
topic, from Session 1 onward.

### No compute or connectivity cap, for now

Considered and explicitly deferred. Not adopted at this time. Revisit if
a specific team's topic or a specific defense-day constraint makes it
necessary.

### No novelty or idea-pitch gate

Considered (DSCAI's model) and explicitly rejected. This is a Master's
applied engineering course, not a research course. Teams are not required
to invent something unpublished; they are required to understand and
correctly build the full pipeline on their own chosen data.

### Topic areas, databases first, dataset choice left open to the team

Topic areas were not chosen first and databases fitted to them after.
Each area below started from real, accessible open databases, checked
for three things the supply chain case already provides: a real
published vocabulary or ontology worth reusing, enough undocumented
structure in the data to make constraint discovery genuinely hard, and a
scope a team can reasonably work with in this course. Supply chain is
not offered as a team topic, it is already the course's own taught case.

**Within a topic area, which specific database to use is the team's own
choice.** The examples below are verified starting points, not a
mandatory pairing. A team may pick a different open database inside the
same topic area, or bring their own, as long as it is openly licensed
and a real vocabulary exists to reuse against it.

| Topic area | Example open databases | Ontology to reuse | Why it holds up |
|---|---|---|---|
| Transit and mobility | GTFS static feeds (published by most public transit agencies, pick any city or operator); OpenMobilityData / Mobility Database aggregates many feeds in one place | [Linked GTFS](https://github.com/OpenTransport/linked-gtfs); a Transmodel-aligned OWL-DL bus transport ontology, peer reviewed in the [Semantic Web Journal](https://www.semantic-web-journal.net/content/applying-lot-methodology-public-bus-transport-ontology-aligned-transmodel-challenges-and-0); listed in [Linked Open Vocabularies](https://lov.linkeddata.es/dataset/lov/vocabs/gtfs) | Real constraints to recover: schedule consistency, stop sequence validity, transfer timing |
| Bibliographic and academic | OpenAlex open dataset; CrossRef open metadata (DOI-based works, a different source with a different quirks profile) | [SemOpenAlex](https://link.springer.com/chapter/10.1007/978-3-031-47243-5_6) (ISWC 2023, OpenAlex mapped to RDF); BIBFRAME as a fallback library-standard vocabulary | Real entity resolution problem: same author, different name spellings across sources |
| Cultural heritage and music | MusicBrainz open data dumps; Europeana's open cultural-heritage metadata | [Music Ontology](https://motools.sourceforge.net/doc/musicontology.html) for MusicBrainz, with [LinkedBrainz](https://wiki.musicbrainz.org/LinkedBrainz) already doing the RDF mapping; Europeana Data Model (EDM) for Europeana | Real duplicate-record problem: the same work or release catalogued differently across sources |
| Public procurement | Open Contracting Data Standard (OCDS) releases, World Bank backed, published by many national and local governments, team picks a jurisdiction | Peer-reviewed [OCDS ontology](https://github.com/TBFY/ocds-ontology) | Real constraints: contract value must match line-item totals, tender-to-award timing rules |
| Food products | Open Food Facts; USDA FoodData Central (public domain, a different data profile: lab-measured composition rather than crowd-sourced labels) | [FoodOn](https://vest.agrisemantics.org/content/open-food-facts-food-ontology), reused directly by Open Food Facts itself, and general enough to fit either source; GS1 Web Vocabulary as a complementary industry standard | Real constraints: nutrition values must be internally consistent, allergen declarations, unit conventions |

A team may also propose a topic area and database outside this table
entirely, subject to the same two checks: a real ontology to reuse
exists, and the data has genuine undocumented structure to recover.
Licence check still needed per dataset instance actually used, before it
goes in front of students, same as the course's own existing rule that
every third-party ontology or dataset must be listed in the report with
its licence.

### Licence check on the topic-menu databases

Checked 2026-09-17, against each database's own published terms.

| Topic area | Database | Licence | Note |
|---|---|---|---|
| Transit and mobility | GTFS feeds (via Mobility Database) | No single licence, set per agency | The catalog itself is CC0, but that does not cover the feeds. **Team must check the specific agency's own licence before use**; many US agencies publish CC0 or public domain, some do not. Reject a feed with no stated licence. |
| Bibliographic and academic | OpenAlex | CC0 (public domain) | Clean. The MAG-format snapshot only is ODC-BY, avoid that format. |
| Bibliographic and academic | CrossRef | Metadata treated as facts, not copyrightable; abstracts may be copyrighted | Clean for the bibliographic fields a team would actually use. |
| Cultural heritage and music | MusicBrainz | CC0 (public domain) | Clean. |
| Cultural heritage and music | Europeana | Varies per item (Europeana Rights Statements) | Not clean by default. **Team must filter to items with an open rights statement**, do not assume the whole aggregate is open. |
| Public procurement | OCDS releases | Standard/schema is CC BY 4.0; actual released data licence set by the publishing government | Team picks a jurisdiction whose publisher states an open licence (most World Bank-backed publishers do); check that specific publisher's terms, not just the OCDS standard. |
| Food products | Open Food Facts | ODbL (database) + DbCL (contents) + CC BY-SA (images) | Requires attribution and share-alike on derivative use, both satisfiable in a course report. |
| Food products | USDA FoodData Central | CC0 (public domain) | Clean. Attribution requested, not required. |

Net effect: three of the five topic areas (bibliographic, music via MusicBrainz,
food via either source) are unconditionally clean. Transit, cultural heritage
via Europeana, and public procurement carry a real but manageable condition:
the team confirms the licence on the specific feed, item set, or jurisdiction
they actually use, not the aggregator as a whole. Add this as an explicit
report requirement (see "Team work" policy: every third-party dataset and
ontology is listed in the report with its licence).

### Rubric, rebalanced

> **Superseded 2026-09-26 (instructor).** The grade is now attendance and lab
> run 15, team project 55 (scored once, offline, one mark per layer: ontology
> 10, shapes 10, mapping 9, learning 9, access layer 9, report 8), individual
> defense 30; the milestones are ungraded checkpoints. See
> `module-08-defense/DEFENSE-DAY.md` and `syllabus-source.json`. The table
> below is kept as history.

The 100-point capstone rubric (scores the "final deployed system and
technical report" line, and the two milestones, per the existing
Assessment table) is rebalanced away from anything tied to one fixed
case, toward the core build and the course's own central concepts.

| Line | Old | New | Why |
|---|---|---|---|
| Problem framing and scope | 7 | 7 | Unchanged, already topic-agnostic |
| Data understanding and constraint discovery | 10 | 12 | Raised. With each team on its own database, this is the least copyable, most diagnostic line |
| Ontology quality | 16 | 18 | Raised. Reworded topic-agnostic: reuses a real published vocabulary appropriate to the chosen domain, not IOF SCRO by name |
| Constraint validation with SHACL | 13 | 15 | Raised, a core course concept named directly |
| Operational data integration | 13 | 12 | Slightly lowered to fund the above |
| Prediction and evaluation honesty | 13 | 13 | Unchanged |
| Access layer | 9 | 9 | Unchanged |
| Deployment and reproducibility | 6 | 9 | Raised. When every team's setup differs by topic, "clone it fresh and run it" is the fairness anchor across the cohort |
| Literature and open problem | 5 | 5 | Unchanged, field awareness, not novelty |
| Method transfer to a second domain | 8 | dropped | Its old purpose, proving the method is not case-specific, is now handled by the cohort itself running 5 different topics |

Total: 100.

Defense stays its own separate 10 percent line in the top-level
Assessment table, outside this rubric, unchanged in weight. Team defense
mechanics (any teammate can be asked about any part, timing at 6 to 7 or
8 to 12 teams instead of 24 individuals) still need writing up, see
"Still to build" below.

## What stays the same

- The five modules and eight sessions, same order, same taught content,
  same production depth. Only the project's shape changes, not the
  lectures.
- The reused-ontology, competency-question, SHACL-shape, RML-mapping,
  GNN, and text-to-SPARQL pipeline stays the spine of every team's build,
  regardless of topic.
- Milestone 1 (end of Session 4) and Milestone 2 (end of Session 6) stay
  in place, now scored against each team's own chosen topic instead of
  the shared case.

## Still to build

1. ~~Update `syllabus-source.json`'s capstone, assessment, and
   policies sections~~ Done.
2. ~~Mirror the same changes into `Knowledge Representation -
   Syllabus.docx`~~ Done.
3. ~~Write the actual Session 8 defense-day run of show~~ Done:
   `module-08-defense/DEFENSE-DAY.md`.
4. ~~Decide and document team formation mechanics~~ Done: self-formed,
   locked in before Session 2, instructor places any leftover students.
5. ~~Licence-check each of the five topic-menu databases~~ Done, see
   "Licence check on the topic-menu databases" above. Three of five are
   unconditionally clean; transit, Europeana, and procurement need a
   per-feed/per-publisher check by the team, now written into the
   report requirement.
6. ~~Update `README.md`'s course description and any lecture slide~~
   Done: `README.md` and `index.html` reworded to team plus own-topic
   language; lecture decks checked, no individual-work language found.

This document is the thing every one of those six items gets checked
against, not chat history. If a future decision changes something above,
edit this file in the same change, so it never drifts out of date with
what actually shipped.
