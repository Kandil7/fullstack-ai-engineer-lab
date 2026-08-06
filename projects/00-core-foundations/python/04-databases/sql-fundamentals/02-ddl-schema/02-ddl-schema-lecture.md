# SQL Fundamentals — 02: DDL — Schema Definition

## Topic Overview

DDL (Data Definition Language) is the part of SQL that *defines* the
shape of your data: `CREATE`, `ALTER`, and `DROP`. It is the least
glamorous SQL and the most expensive to get wrong — because it is the
hardest to change later. A schema is a contract: it says what columns
exist, what types they have, and what rules every row must obey.

The deep idea of this lecture: **constraints are data-quality checks
running inside the database**. `NOT NULL`, `DEFAULT`, `CHECK`, `UNIQUE`,
and foreign keys catch bad rows at *write* time — in the engine, for
every writer, forever — instead of you discovering corrupt data at
*read* time, when training sets or dashboards are already wrong.

The second idea: **the schema itself is queryable data**. sqlite stores
table definitions in `sqlite_master`, and column details come from
`PRAGMA table_info`. Migrations, ORMs, and feature-store registries all
read this metadata instead of hardcoding column lists — and so can your
tooling.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write `CREATE TABLE` with the major sqlite types and affinities
2. Enforce `NOT NULL`, `DEFAULT`, `CHECK`, and `UNIQUE` correctly
3. Explain the UNIQUE-with-NULLs asymmetry and its dedup implications
4. Model relations with FOREIGN KEY and pick ON DELETE behavior
5. Evolve a schema with `ALTER TABLE` and backfill new columns
6. Read schema metadata from `sqlite_master` and `PRAGMA table_info`
7. Drop tables safely, knowing indexes go with them
8. Design a small feature-table schema that rejects bad rows at insert

## Prerequisites

| Need | Where |
|---|---|
| Tables, keys, NULL semantics | `01-relational-model-lecture.md` |
| `sqlite3` connect/execute | `04-databases/mysql/01-getting-started.py` |

---

## 1. CREATE TABLE — columns, types, constraints

sqlite has five storage classes — `INTEGER`, `REAL`, `TEXT`, `BLOB`,
`NULL` — and a *type affinity* system that coarsens declared types toward
them. Postgres has far more precise types; the DDL concepts transfer
exactly.

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")
conn.execute("""
    CREATE TABLE events (
        id        INTEGER PRIMARY KEY,
        name      TEXT NOT NULL,
        severity  INTEGER NOT NULL DEFAULT 0,
        score     REAL CHECK (score BETWEEN 0.0 AND 1.0),
        payload   TEXT
    )
""")
conn.execute("INSERT INTO events (name) VALUES (?)", ("anomaly",))
print(conn.execute("SELECT name, severity FROM events").fetchall())
```

```
[('anomaly', 0)]
```

`severity` was omitted, so `DEFAULT 0` filled it. The constraint trio
fires next:

```python
try:
    conn.execute("INSERT INTO events (name, score) VALUES (?, ?)", ("bad", 1.5))
except sqlite3.IntegrityError as exc:
    print(f"CHECK rejected 1.5: {exc}")
try:
    conn.execute("INSERT INTO events (name) VALUES (NULL)")
except sqlite3.IntegrityError as exc:
    print(f"NOT NULL rejected: {exc}")
```

```
CHECK rejected 1.5: CHECK constraint failed: score BETWEEN 0.0 AND 1.0
NOT NULL rejected: NOT NULL constraint failed: events.name
```

## 2. The schema is queryable data

Every table is registered in `sqlite_master`; column details come from
`PRAGMA table_info`. Tools read this metadata — never trust it, *derive*
it.

```python
print(conn.execute(
    "SELECT type, name FROM sqlite_master WHERE type = ? AND name = ?",
    ("table", "events"),
).fetchall())
for col in conn.execute("PRAGMA table_info(events)").fetchall():
    print(col)
```

```
[('table', 'events')]
(0, 'id', 'INTEGER', 0, None, 1)
(1, 'name', 'TEXT', 1, None, 0)
(2, 'severity', 'INTEGER', 1, '0', 0)
(3, 'score', 'REAL', 0, None, 0)
(4, 'payload', 'TEXT', 0, None, 0)
```

The tuple is `(cid, name, type, notnull, dflt_value, pk)`. A migration
tool or a schema-validator is exactly this loop plus some rules.

## 3. PRIMARY KEY vs UNIQUE — the NULL asymmetry

PRIMARY KEY means UNIQUE **and** NOT NULL. UNIQUE alone still allows
*one* NULL — because NULLs are never equal to each other, two NULLs do
not collide. This asymmetry is a classic dedup bug: you declare a column
UNIQUE to deduplicate on it, and NULL rows slip through as "duplicates".

```python
conn.execute("CREATE TABLE dedup (token TEXT UNIQUE)")
conn.execute("INSERT INTO dedup (token) VALUES (?)", ("emb-a",))
conn.execute("INSERT INTO dedup (token) VALUES (NULL)")
conn.execute("INSERT INTO dedup (token) VALUES (NULL)")   # allowed!
print(conn.execute("SELECT * FROM dedup").fetchall())
```

```
[('emb-a',), (None,), (None,)]
```

If "no token" must mean "no row", say `token TEXT NOT NULL UNIQUE`.

## 4. FOREIGN KEY with ON DELETE behavior

Foreign keys express relations *and* their lifecycle. `ON DELETE
CASCADE` removes children with the parent; `ON DELETE SET NULL` keeps
the child rows but nulls the reference. The default (`NO ACTION`)
*blocks* the delete — which is often the safest and most surprising.

```python
conn.execute("CREATE TABLE model_runs (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
conn.execute("""
    CREATE TABLE metrics (
        id INTEGER PRIMARY KEY,
        run_id INTEGER NOT NULL REFERENCES model_runs(id) ON DELETE CASCADE,
        metric TEXT NOT NULL,
        value REAL NOT NULL
    )
""")
conn.execute("INSERT INTO model_runs (name) VALUES (?)", ("run-A",))
conn.execute("INSERT INTO metrics (run_id, metric, value) VALUES (?, ?, ?)", (1, "f1", 0.91))
conn.execute("DELETE FROM model_runs WHERE name = ?", ("run-A",))
print(conn.execute("SELECT * FROM metrics").fetchall())
```

```
[]
```

The metrics vanished with the run. Choosing the wrong action leaks
orphaned rows into joins or blocks legitimate deletes.

## 5. ALTER and DROP — evolving a live schema

`ALTER TABLE ADD COLUMN` is metadata-only and cheap. Backfilling the new
column is a **separate step** — the "expand, backfill, contract"
migration pattern starts here. `DROP TABLE` removes the table *and its
indexes*, irreversibly without a backup.

```python
conn.execute("ALTER TABLE events ADD COLUMN created_at TEXT")
conn.execute("UPDATE events SET created_at = ? WHERE created_at IS NULL", ("2026-08-06",))
print(conn.execute("SELECT name, created_at FROM events").fetchall())
conn.execute("DROP TABLE dedup")
print(conn.execute(
    "SELECT name FROM sqlite_master WHERE type = ? AND name = ?", ("table", "dedup")
).fetchall())
```

```
[('anomaly', '2026-08-06')]
[]
```

## Common Mistakes to Avoid

### Mistake 1: UNIQUE when you need NOT NULL too

```sql
-- WRONG - NULLs slip through your dedup
--   token TEXT UNIQUE
-- CORRECT
--   token TEXT NOT NULL UNIQUE
```

### Mistake 2: FK with no ON DELETE clause

```sql
-- WRONG - deletes either block or accumulate orphans, silently
--   run_id INTEGER REFERENCES runs(id)
-- CORRECT - pick deliberately:
--   run_id INTEGER REFERENCES runs(id) ON DELETE CASCADE
--   run_id INTEGER REFERENCES runs(id) ON DELETE SET NULL
```

### Mistake 3: CHECK referencing other rows

```sql
-- WRONG - CHECK sees only the row being written
--   CHECK (score <= AVG(score))   -- not expressible
-- CORRECT - column-scoped conditions only
--   CHECK (score BETWEEN 0.0 AND 1.0)
```

### Mistake 4: Forgetting the sqlite FK pragma

```python
# WRONG - FK enforcement silently off on this connection
#   conn.execute("INSERT INTO child (pid) VALUES (999)")
# CORRECT - before any DML, every connection
#   conn.execute("PRAGMA foreign_keys = ON")
```

### Mistake 5: Backfilling inside the ALTER

```sql
-- WRONG - ALTER is metadata-only; do not assume data comes with it
--   ALTER TABLE t ADD COLUMN x INTEGER NOT NULL   -- fails on non-empty table
-- CORRECT - add nullable, backfill in batches, then tighten
--   ALTER TABLE t ADD COLUMN x INTEGER;
--   UPDATE t SET x = ... WHERE x IS NULL;
```

## Best Practices

1. Give every table a single-column INTEGER PRIMARY KEY.
2. Declare `NOT NULL` on every column that has no legitimate "missing" state.
3. Prefer `DEFAULT` over nullable columns when a sane default exists.
4. Put a `CHECK` on every numeric range you care about (scores, ratios).
5. Choose FK `ON DELETE` behavior explicitly for every relation.
6. Name constraints and indexes (`idx_events_ts`, not the auto names) when the tooling allows.
7. Keep the schema in code (migrations), never only in the live DB.
8. Backfill new columns in bounded batches, not one giant UPDATE.
9. Back up before `DROP TABLE` — it takes indexes with it.
10. Read `PRAGMA table_info`/`sqlite_master` instead of hardcoding columns.

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| CREATE TABLE / ALTER ADD COLUMN | O(1) metadata | O(1) | — |
| Backfill of a new column | O(n) writes | O(n) | batch it; `NOT NULL` after backfill |
| CHECK / NOT NULL enforcement | O(1) per write | O(1) | — (this is the point) |
| UNIQUE enforcement | O(log n) per write | O(n) | only when uniqueness is a requirement |
| DROP TABLE | O(n) pages freed | O(n) | keep backups; it is irreversible |

## AI Engineering Relevance

**Where this shows up:** feature-store schemas, evaluation-result
tables, ML-metadata registries.

| Concept here | Used for |
|---|---|
| NOT NULL | labels and entity ids that must always exist |
| CHECK | score/probability ranges, latency bounds on predictions |
| UNIQUE | dedup keys for ingestion (entity_id, (model, version)) |
| FK + CASCADE | deleting a model run removes its metrics automatically |
| Queryable metadata | registry tools that enumerate feature tables |

**Scale note:** at 1M rows/day ingested, constraints are your only
guarantee that bad rows never enter training data. A CHECK that rejects
probability 1.7 at write time is worth more than any read-time cleanup
job.

## Practice Exercises

### Exercise 1: Constraint zoo  (Difficulty: Easy)

Create a table with NOT NULL, DEFAULT, CHECK, and UNIQUE columns. Insert
valid rows; then trigger each constraint failure and print the error.

### Exercise 2: UNIQUE NULL asymmetry  (Difficulty: Easy)

Create `dedup(token TEXT UNIQUE)`. Insert two NULL rows and confirm both
are accepted. Then re-create with `NOT NULL UNIQUE` and confirm the
second NULL is rejected.

### Exercise 3: FK action matrix  (Difficulty: Medium)

Create parent/child pairs with `ON DELETE CASCADE`, `SET NULL`, and the
default. Delete the parent in each and record what happens to the child.

### Exercise 4: Schema reader  (Difficulty: Medium)

Write a function `table_columns(conn, name) -> list[str]` using
`PRAGMA table_info`. Verify it returns the right columns for a table you
created. Then use `sqlite_master` to list all tables.

### Exercise 5: Expand-backfill-contract  (Difficulty: Medium)

Add a nullable `created_at` column to a populated table, backfill it in
batches of 10 rows, then verify no NULLs remain.

### Exercise 6: Feature-table DDL  (Difficulty: Hard)

Design DDL for a feature table that stores per-entity, per-day numeric
features: entity_id NOT NULL, day NOT NULL, value REAL with CHECK,
UNIQUE(entity_id, day). Explain which constraint makes ingestion
idempotent.

## Summary

| Concept | Description |
|---|---|
| CREATE TABLE | defines columns, types, and constraints |
| NOT NULL / DEFAULT | refuse missing values / supply them |
| CHECK | row-level range and shape guards |
| UNIQUE | dedup key — but NULLs do not collide |
| FK + ON DELETE | relations with explicit lifecycle |
| ALTER / DROP | cheap metadata evolution; expensive mistakes |
| sqlite_master / PRAGMA | the schema as queryable data |

DDL is where data quality is won or lost. The same bad row that a CHECK
catches in one millisecond at write time would otherwise corrupt a
training set, an evaluation report, or a feature join — and take days to
trace. Schema as code, constraints as enforcement, metadata as data:
these three habits carry every database topic that follows.

## Quick Reference

| Task | Idiom |
|---|---|
| Create table | `CREATE TABLE t (id INTEGER PRIMARY KEY, ...)` |
| Range guard | `CHECK (score BETWEEN 0.0 AND 1.0)` |
| Fill omitted | `col INTEGER NOT NULL DEFAULT 0` |
| Dedup key | `col TEXT NOT NULL UNIQUE` |
| Relation + cleanup | `col INTEGER REFERENCES p(id) ON DELETE CASCADE` |
| Add column | `ALTER TABLE t ADD COLUMN c TEXT` |
| Inspect schema | `PRAGMA table_info(t)` / `sqlite_master` |

## Next Steps

Next: **[03 — DML: INSERT / UPDATE / DELETE](03-insert-update-delete-lecture.md)** —
now that the schema enforces quality, write rows into it correctly:
upserts, bulk loads, and safe bounded deletes.

Continues in: **[Phase 4 — Postgres](../../postgres/02-postgres-types-lecture.md)** —
JSONB, arrays, enums, and the richer type system DDL gains on a real server.

Official docs: https://www.sqlite.org/lang_createtable.html ,
https://www.sqlite.org/foreignkeys.html
