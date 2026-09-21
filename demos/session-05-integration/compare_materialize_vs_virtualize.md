# Materialize versus virtualize, filled in live

Both paths answer the same question (`query.sparql`) over the same
Postgres data. Fill in the blanks below during the lab, from what you
actually see, not from the general tradeoffs slide. Rows already
filled are carried over from real runs done while building this lab;
replace them with your own room's numbers where you can.

## Freshness

| | Morph-KGC (materialize) | Ontop (virtualize) |
|---|---|---|
| When does a Postgres UPDATE show up in query results? | Never, until you re-run `python3 -m morph_kgc config_materialize.ini` | Immediately, the next query rewrites to fresh SQL |
| Try it: update `po88`'s `delivery_date` in Postgres, re-run both queries without re-materializing | _fill in_ | _fill in_ |

## Storage and setup cost

| | Morph-KGC | Ontop |
|---|---|---|
| Extra copy of the data on disk? | Yes, `materialized.ttl`, grows with the source | No, mapping plus ontology only |
| What you needed to run a query | A materialize step, then any SPARQL engine over the `.ttl` | A live JDBC connection to Postgres, every query |

## Query latency

| | Morph-KGC | Ontop |
|---|---|---|
| `query.sparql` against the small seed | _fill in, this data set is too small for the numbers to mean much_ | _fill in_ |
| What would change at DataCo's real ~180k-row scale | Materialize is a one-time cost, then fast in-memory queries | Every query pays a SQL round trip, but never a stale one |

## Which queries each handles badly

- Morph-KGC: a query that needs data Postgres does not have yet
  (something upstream hasn't written), or a query pattern that needs a
  join Morph-KGC cannot push down efficiently at materialize time on a
  very large source.
- Ontop: a query whose SPARQL shape rewrites into an expensive SQL
  join or a full scan Postgres itself would be slow at, since Ontop
  cannot outrun the database underneath it, only translate to it.

## What Ontop actually generates

Captured from a real `ONTOP_LOG_LEVEL=debug` run against
`query.sparql`, see the SQL Ontop rewrote it to below (paste the room's
own capture here if it differs, the exact SQL depends on the Postgres
version and Ontop's own optimizer, worth comparing).

```sql
-- paste ontop_run.log's generated SQL here
```

## The room's decision (10-minute clinic)

Each team states, in one or two sentences, which architecture its own
capstone topic will use, and why:

- _Team 1:_
- _Team 2:_
- _Team 3:_
