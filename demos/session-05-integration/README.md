# Session 5 lab: from a live database to the graph

**Read this first:** [What this lab is doing](OVERVIEW.md). It explains the
data, why each step exists, and the role of every file.

**Why this lab exists:** to make the lecture concrete (R2RML mappings,
materializing against virtualizing, entity resolution) on the same Brunel
data as Sessions 1 to 4, and to give you the mapping pattern your team
project will use for its own database. Nothing is handed in or graded.

Every number in `lectures/kr-session-05.html` comes from the files in
`reference-outputs/`, produced by these scripts on 2026-09-25 (SQLite path;
the PostgreSQL and Ontop runs are recorded separately, see their files).

## Before you start

- The shared course environment `demos/.venv`, active, **installed with both
  lines** of `demos/README.md` (the second adds Morph-KGC). Already set up
  earlier? Run both install lines again now.
- Session 2's graph exists (`demos/session-02-rdf-sparql/brunel.ttl`): the
  comparison in step 4 needs it. If not, run `python convert_to_rdf.py`
  there first.
- Docker Desktop running, and Java (the JDK 21 from Session 1) for Ontop.
- Run every command from this folder, `demos/session-05-integration/`.
- **No Docker?** Use `--sqlite` in steps 2 and 3 (a database file instead of
  PostgreSQL; the same tables and the same mapping), skip step 6 and read
  `reference-outputs/ontop-q2.txt` instead. You lose only virtualization.

## Part A · build and observe (about 30 minutes)

1. `docker compose up -d`. Starts PostgreSQL 16 on this computer
   (127.0.0.1:5432). **Expect:** `Container ... Started`.
2. `python load_database.py` (or `--sqlite`). **Expect:** orders 9,215 rows,
   plant_ports 22, products_per_plant 2,036, freight_rates 1,540.
3. `python materialize.py` (or `--sqlite`). Morph-KGC runs
   `brunel-mapping.ttl`. **Expect:** `135,799 triples` in a few seconds,
   written to `brunel-mapped.nt`. **Look at:** `brunel-mapping.ttl`, the
   `<#Orders>` map: a template for the subject, a column for a plain value,
   a column with a datatype, a template for a link.
4. `python compare_with_session2.py`. **Expect:** `only in Session 2's graph
   0`, `only in the mapped graph 7`, `rate bands in both 1,540`. The 7 are
   carriers V444_2 and V444_4 to V444_9, now typed `ul:Carrier`: the
   mapping's `<#Carriers>` view reads both tables. **Notice:** Session 2's
   graph has 49 more triples, its vocabulary; a mapping makes data only.
5. `python ../session-04-shacl/validate.py --data brunel-mapped.nt --data vocabulary.ttl`
   (about 2 minutes). **Expect:** focus nodes 9,215, then `2 Violation,
   1,370 Warning`, and no band carrier line: Session 4's 1,209 warnings are
   gone. **Notice:** run it once without `--data vocabulary.ttl`: focus
   nodes drop to 9,023, because nothing then says a late order is an order
   (`reference-outputs/validate-mapped-without-vocabulary.txt`).
6. `python ontop/setup_ontop.py` once (downloads about 90 MB), then
   `python ontop/run_ontop.py`. Ontop answers Session 2's Q2 from the
   database. **Expect:** V444_0 6,264 orders and 183 late, V444_1 2,097 and
   9, V44_3 854 and 0, then the SQL Ontop sent to PostgreSQL.
7. `python er/match_customers.py`. **Expect:** 2,392 possible pairs, 1,818
   after blocking; at threshold 4 precision 0.878 and recall 0.935, at
   threshold 8 precision 1.000 and recall 0.870. **Look at:** the wrong
   matches and the misses it lists, and why each happened.

## Part B · extend a mapping (about 15 minutes)

Open `my_mapping.ttl`. It maps orders (id, weight, carrier) and carriers.
Three rules are missing, and each is a copy of a rule already in the file
with one thing changed: Y1 a map for customers (copy `<#Carriers>`), Y2
`ul:ofProduct` (copy `ul:carriedBy`), Y3 `ul:unitQuantity` as an integer
(copy `ul:weight`). Then:

```sh
python check_my_mapping.py
```

It runs your mapping on the database (PostgreSQL if running, otherwise
`brunel.db`) and compares the triples each rule makes with the ones it
should make. **Expect** when all three are right: `3 of 3 right.` Stuck?
`solutions/my_mapping_solutions.ttl`. The common wrong answers and their
hints are in `reference-outputs/my-mapping-check.txt`.

## Part C · think (about 10 minutes)

1. Materialize or virtualize: which would you choose if the orders change
   every minute, and which if you must run SHACL on every change?
2. The matcher at threshold 4 matched a customer that is not in Brunel.
   What would that error cost a real company, compared with a miss?
3. For **your team project's own database**: which table becomes which
   class, which column is the key in your IRI template, and which table has
   no key at all?

## Optional

- `python ontop/run_ontop.py --query my-question.sparql` with any Session 2
  query that uses no `*` or `+` path (Ontop does not support those).
- `python er/match_customers.py --threshold 6` to see the trade-off move.
- Read `er/make_teaching_set.py` to see exactly how the teaching data was
  made.

## You understood this lab if you can say

- what a triples map, a template and a logical view each do;
- why the mapping needs no join to link an order to its carrier;
- why a rate band is a blank node;
- what materializing and virtualizing each give up;
- why precision and recall move in opposite directions with the threshold.

## Take it to your team project

- `brunel-mapping.ttl` is the model for your own mapping: one triples map
  per table, templates from your IRI rule (Session 2, part C).
- Validate what the mapping produces with your Session 4 shapes, together
  with your vocabulary.
- Decide and write down: materialize or virtualize, and why.
- If your project has two sources for the same things, record how you
  matched them and your precision and recall.
