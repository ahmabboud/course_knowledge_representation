# Shared code

Imported by more than one session's folder, never copy-pasted between
them.

- `iri.py` — the IRI scheme the cohort agrees on at the end of Session
  2's discussion block. Landed here right after that session, every
  session from 3 onward imports it rather than re-deciding it.
- `data_paths.py` — where DataCo and Brunel live once `data/fetch_data.py`
  has run, imported instead of hardcoding a path in every notebook.

Add to this folder only when a second session needs the same code a
first session already wrote. Until then, code stays in its own session
folder.
