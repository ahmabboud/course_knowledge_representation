repo: ahmabboud/course_knowledge_representation
branch: main
upstream template: ahmabboud/LebUniv_Course_Template @ `2322f1a`

## Last sync

date: 2026-09-07
commits: `537820e` (initial), `68599d9` (defect fixes)
status: `537820e` is pushed and live. **`68599d9` is committed locally and not
yet pushed.** Run `git push origin main`.
direction: this repository is DOWNSTREAM of the template. The stylesheet,
runtime and authoring contract were authored in `LebUniv_Course_Template`.

### `68599d9` fixes three defects that belong upstream

Diagnosed against the live site. All three are in `assets/` and affect every
deck built on this system, including the `kr-session-03` reference lecture,
which shows the same symptoms.

| # | File | Defect | Effect |
|---|---|---|---|
| 1 | `lu.css` | `.lu-mcq__why` set `display:block` with no `[hidden]` companion rule, so the UA `[hidden]` rule lost | Every unrevealed rationale still occupied space. MCQ and poll slides rendered 4 to 5 times taller than the slide: 1,440px and 1,398px of overflow here, 859px and 1,234px in session 3 |
| 2 | `lu.css` | A `.lu-board` inside `.lu-walk__view` is `width:100%` plus `aspect-ratio`, so it derived a height taller than the space available | The diagram overlapped the walkthrough caption bar by 90px here and 78px in session 3. Height now leads, width follows, with a print override |
| 3 | `lu-deck.js` | On reload the poll set `data-verdict="correct"` on whatever the student had answered, ignoring `data-answer` | A student restoring a wrong answer saw it confirmed as right. Now marks `data-picked` and leaves correctness to the reveal |

**These three fixes should be ported to `LebUniv_Course_Template`.** Until they
are, every new course seeded from the template inherits all three.

Also in `68599d9`: 46 content trims across 14 slides of session 1, and the
`&mdash;` entities removed from the walkthrough captions. Asset query strings
bumped to `v=1.0.3` in all four HTML files and in `SHELL` in `sw.js`.

### Verified how

Components were exercised directly on the live page: MCQ, fill-in-the-blank,
drag-to-order, poll, reveals, term popovers, the compare wipe, code copy and
run, progressive builds and the self-check all function correctly. The two
`lu.css` fixes were injected into the live page and re-measured before being
written to the file. **The content trims have not yet been measured against a
live render** and should be re-checked after this commit deploys.

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
