# Knowledge Representation, Lebanese University, MSc

Interactive HTML lectures for the Knowledge Representation course. 24 contact hours, 8 sessions of 3 hours. Static pages, no build step, deployed to GitHub Pages as-is.

**Students:** open the site and pick a session. Nothing to install. Your answers and your place in a lecture are stored in your own browser and never transmitted.

## The course in one paragraph

One enterprise problem, a supply chain, carried from raw operational data through to a deployed system that can be queried in natural language. Profile the source data and recover the constraints nobody wrote down, model the domain as an OWL ontology on top of published industrial ontologies, express the constraints as SHACL shapes, map the operational relational data into the graph, train a graph neural network on the result, and put a schema-aware language model query layer on top. Every lab from Session 3 onward demonstrates the technique on the course's own supply chain case. Teams of 2 to 3, on their own chosen topic and open database, apply the same technique to their own project from directly after Session 1, and are evaluated on that project at the end.

## Sessions

| # | Module | Title | Status |
|---|---|---|---|
| 1 | 1 | Enterprise Knowledge Representation and the Supply Chain Problem | Done |
| 2 | 1 | RDF, SPARQL, and the Graph as a Data Model | Done |
| 3 | 2 | Ontology Engineering: OWL and Reuse | Done |
| 4 | 2 | Constraints, Quality, and Provenance: SHACL | Done · Milestone 1 (checkpoint) |
| 5 | 3 | Integrating Operational Data | Done |
| 6 | 4 | Learning Over the Graph: Embeddings and Graph Neural Networks | Done · Milestone 2 (checkpoint) |
| 7 | 5 | The Agentic Query Layer, Deployment, and Open Problems | Done |
| 8 | 5 | The Defense | Done |


## Repository

- **`index.html`**, the course index students land on.
- **`lectures/kr-session-NN.html`**, one self-contained lecture per file.
- **`demos/`**, lab material for the sessions, real code against real data (Docker services, a local Neo4j, notebooks and scripts), separate from the small in-slide sandboxes. See `demos/README.md` for setup, and each `demos/session-NN-.../README.md` for that session's own lab.

## What a lecture gives you

Presenter view on a second screen with speaker notes, elapsed time and pacing against the plan · deep-linkable slides (`#/12`) · contents panel and full-text search · a study mode that expands every popover, held-back answer and build step · one-page-per-slide printing with the instructor notes attached · offline support once installed · answers and position saved on the student's own device.

## Run it locally

Clone the repository, then start a small web server in its folder (the one that holds `index.html`).

macOS or Linux:

```
python3 -m http.server 8000
```

Windows PowerShell:

```
python -m http.server 8000
```

Open <http://localhost:8000/> in a browser. Press `Ctrl+C` in the terminal to stop it.

You can also open any HTML file directly in a browser. Everything works from `file://` except the offline support (the service worker), which needs `http`. If port 8000 is busy, use another number, for example `8080`, and open that port instead.

## Deploy

Enable GitHub Pages with **GitHub Actions** as the source, then push to `main`. `.github/workflows/pages.yml` uploads the repository unchanged. There is no build step.

## Accessibility

Built to WCAG 2.2 AA.

## Licence

Course content belongs to its authors. The template, stylesheet and runtime are yours to reuse and adapt.
