repo: ahmabboud/course_knowledge_representation
branch: main
upstream template: ahmabboud/LebUniv_Course_Template @ `2322f1a`

## Last sync

date: 2026-09-07
commit: `0a6ca86` (`Knowledge Representation course site: design system, Session 1 and Session 3`)
status: committed locally, **not yet pushed**. The remote is configured and the
repository exists and is empty. Run `git push -u origin main` from a terminal
with your GitHub credentials.
direction: this repository is DOWNSTREAM of the template. The stylesheet,
runtime and authoring contract were authored in `LebUniv_Course_Template` and
copied here unchanged. Fixes to `assets/` belong upstream, then flow back.

### In this commit

- Full template copy: `assets/lu.css`, `assets/lu-deck.js`, `assets/sparql-lite.js`,
  `design-system.html`, `lectures/_template.html`, `AGENTS.md`, `PROMPT.md`,
  the Pages workflow, the PWA manifest and the service worker.
- `lectures/kr-session-01.html` authored here. 22 slides, 180 minutes.
- `lectures/kr-session-03.html` carried over from the template, where it was
  written as the worked example. It is a real session of this course.
- `index.html` narrowed to Knowledge Representation, sessions ordered 1 to 8,
  Session 1 and Session 3 linked, the other six marked not yet built.
- `manifest.webmanifest` and `README.md` retitled for the course.
- `uploads/` and `github.md` from the template were not copied.

## Screen map

| Repo path | Built from |
|---|---|
| `index.html` | template, narrowed to this course |
| `lectures/kr-session-01.html` | `Knowledge Representation - Syllabus.docx`, Session 1 |
| `lectures/kr-session-03.html` | template worked example, same syllabus, Session 3 |
| `lectures/_template.html`, `design-system.html`, `assets/*` | template, unchanged |
| `AGENTS.md`, `PROMPT.md` | template, unchanged |

## Sessions still to build

2, 4, 5, 6, 7, 8. Source of truth is
`../Knowledge Representation - Syllabus.docx` and its `syllabus-source.json`.
Use the brief in `PROMPT.md` and build against `AGENTS.md`.

## Notes

- Asset links carry `?v=1.0.2`. Bump in every HTML file and in `SHELL` in `sw.js`
  when anything in `assets/` changes.
- Enable Pages with **GitHub Actions** as the source before the first push, or
  the workflow will run and fail on the deploy step.
- `.nojekyll` must stay. Without it Jekyll hides `lectures/_template.html`.
- Session 1 slide 16 asserts the maintenance status of eight libraries as of
  September 2026. Re-check every row before teaching it.
- `<html class="lu-deck-page">` on both lectures is inherited from the template
  and is not defined in `lu.css`. Harmless, but it is dead markup upstream.
