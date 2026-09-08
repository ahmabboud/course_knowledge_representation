# Knowledge Representation, Lebanese University, MSc

Interactive HTML lectures for the Knowledge Representation course. 24 contact hours, 8 sessions of 3 hours. Static pages, no build step, deployed to GitHub Pages as-is.

**Students:** open the site and pick a session. Nothing to install. Your answers and your place in a lecture are stored in your own browser and never transmitted.

## The course in one paragraph

One enterprise problem, a supply chain, carried from raw operational data through to a deployed system that can be queried in natural language. Profile the source data and recover the constraints nobody wrote down, model the domain as an OWL ontology on top of published industrial ontologies, express the constraints as SHACL shapes, map the operational relational data into the graph, train a graph neural network on the result, and put a schema-aware language model query layer on top. Every lab from Session 3 onward extends your own graded system.

## Sessions

| # | Module | Title | Status |
|---|---|---|---|
| 1 | 1 | Enterprise Knowledge Representation and the Supply Chain Problem | Built |
| 2 | 1 | RDF, SPARQL, and the Graph as a Data Model | To build |
| 3 | 2 | Ontology Engineering: Description Logic, OWL, and Reuse | Built |
| 4 | 2 | Constraints, Quality, and Provenance: SHACL | To build · Milestone 1 |
| 5 | 3 | Integrating Operational Data | To build |
| 6 | 4 | Learning Over the Graph: Embeddings and Graph Neural Networks | To build · Milestone 2 |
| 7 | 5 | The Agentic Query Layer, Deployment, and Open Problems | To build |
| 8 | 5 | Supervised Build, Deployment, and Defense | To build |

## Repository

- **`index.html`**, the course index students land on.
- **`lectures/kr-session-NN.html`**, one self-contained lecture per file.
- **`design-system.html`**, the design system and a live gallery of all twelve interactive components. Start here before authoring.
- **`lectures/_template.html`**, copy this to start a new session.
- **`AGENTS.md`**, the authoring contract. Read it before writing a lecture, whether you are a person or an agent.
- **`PROMPT.md`**, the paste-ready brief for handing a new session to an agent.

Built from the [`LebUniv_Course_Template`](https://github.com/ahmabboud/LebUniv_Course_Template) design system. Fixes to the stylesheet or runtime belong upstream in the template, not here.

## What a lecture gives you

Presenter view on a second screen with speaker notes, elapsed time and pacing against the plan · deep-linkable slides (`#/12`) · contents panel and full-text search · a study mode that expands every popover, held-back answer and build step · one-page-per-slide printing with the instructor notes attached · offline support once installed · answers and position saved on the student's own device.

## Run it locally

Open any HTML file directly in a browser. Everything works from `file://` except the offline service worker, which needs `http`:

```
python3 -m http.server 8000
```

## Deploy

Enable GitHub Pages with **GitHub Actions** as the source, then push to `main`. `.github/workflows/pages.yml` uploads the repository unchanged. There is no build step.

## Before teaching from it

- Replace the `LU` placeholder in the lockup with the official crest at `assets/lu-crest.svg`. The mark here is a typographic stand-in, not the university's emblem.
- Replace every `.lu-figure__ph` placeholder with a real capture. Each one states the path and what must be visible in the shot.
- Session 1 slide 16 asserts the maintenance status of eight libraries as of September 2026. Re-check it before teaching. A stale slide about staleness is embarrassing.

## Accessibility

Built to WCAG 2.2 AA, with the contract and one stated exception documented in `design-system.html` §10.

## Licence

Course content belongs to its authors. The template, stylesheet and runtime are yours to reuse and adapt.
