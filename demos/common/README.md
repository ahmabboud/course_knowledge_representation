# Shared code

Imported by more than one session's folder, never copy-pasted between
them.

- `iri.py`: the course's IRI scheme (`AGENTS.md` 2d), taught in Session 2
  and tested in its closing discussion. Every session from 3 onward, and
  the Session 5 mappings, import it rather than re-deciding it. Do not
  edit it for a team project.
- `data_paths.py`: where DataCo and Brunel live once `data/fetch_data.py`
  has run, imported instead of hardcoding a path in every notebook.

Add to this folder only when a second session needs the same code a
first session already wrote. Until then, code stays in its own session
folder.
