# SQL Fundamentals — 03: DML — INSERT / UPDATE / DELETE

## Topic Overview

DML (Data Manipulation Language) is the workhorse of every pipeline:
`INSERT` puts rows in, `UPDATE` changes them, `DELETE` takes them out.
On the surface it is the simplest SQL there is; in practice, ingestion
pipelines live or die on four DML skills: capturing what you just wrote
(`RETURNING`), writing idempotently (`ON CONFLICT` upsert), loading in
bulk (`executemany`), and deleting in bounded batches (portable
`DELETE ... LIMIT`).

The theme that ties this lecture together is **idempotency and
boundedness**. Training-data ingestion must be safe to re-run: the same
pipeline executed twice must produce exactly the same table. Writes and
deletes must be *bounded*: a million-row UPDATE or DELETE locks the
table, blows up the transaction log, and rolls back everything on one
bad row. DML is where "works on my laptop" pipelines become production
pipelines.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Insert single and multiple rows, capturing generated ids with RETURNING
2. Write idempotent upserts with `ON CONFLICT DO UPDATE` / `DO NOTHING`
3. Bulk-load with `executemany` and explain why row-by-row loops are wrong
4. Update with a parameterized WHERE and RETURNING to see what changed
5. Delete in bounded batches using the portable rowid-subquery pattern
6. Explain why `DELETE ... LIMIT` is MySQL-only and how to port it
7. Recognize the "UPDATE without WHERE" data-loss pattern
8. Build a re-runnable ingestion loop that is safe on a live table

## Prerequisites

| Need | Where |
|---|---|
| Tables, keys, constraints | `02-ddl-schema-lecture.md` |
| PRIMARY KEY/UNIQUE semantics | `01-relational-model-lecture.md` |

---

## 1. INSERT and RETURNING

`RETURNING` returns the row as written — including generated ids and
defaults — without a second SELECT. Ingestion pipelines use it to hand
the created key to a cache, a queue, or a downstream join.

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE features (id INTEGER PRIMARY KEY, entity TEXT NOT NULL UNIQUE, value REAL NOT NULL)")
row = conn.execute(
    "INSERT INTO features (entity, value) VALUES (?, ?) RETURNING id, entity",
    ("user_42", 0.87),
).fetchone()
print(row)
```

```
(1, 'user_42')
```

One round trip, no second SELECT, no race between the insert and the
read. (sqlite needs 3.35+; Postgres has had RETURNING forever.)

## 2. Upsert — ON CONFLICT

The ingestion workhorse: try to insert; if the unique key already
exists, update instead. Idempotent by construction — run the pipeline
twice and the table still has one row per entity.

```python
sql = """
    INSERT INTO features (entity, value) VALUES (?, ?)
    ON CONFLICT (entity) DO UPDATE SET value = excluded.value
"""
conn.execute(sql, ("user_42", 0.92))
conn.execute(sql, ("user_42", 0.92))   # re-run: idempotent
print(conn.execute("SELECT entity, value FROM features WHERE entity = ?", ("user_42",)).fetchall())
```

```
[('user_42', 0.92)]
```

One row, updated value. `excluded` refers to the row that *would have
been* inserted. The `DO NOTHING` variant is for dedup of raw logs: first
writer wins.

```python
conn.execute(
    "INSERT INTO features (entity, value) VALUES (?, ?) ON CONFLICT (entity) DO NOTHING",
    ("user_42", 0.1),
)
print(conn.execute("SELECT value FROM features WHERE entity = ?", ("user_42",)).fetchall())
```

```
[(0.92,)]
```

## 3. Bulk insert — executemany

One INSERT per row in a Python loop is a compile + round trip per row.
`executemany` sends the same statement with many parameter tuples; the
engine compiles once and reuses it.

```python
batch = [(f"entity_{i}", float(i) / 100.0) for i in range(500)]
conn.executemany(
    "INSERT INTO features (entity, value) VALUES (?, ?) ON CONFLICT (entity) DO NOTHING",
    batch,
)
print(conn.execute("SELECT COUNT(*) FROM features").fetchone()[0])
```

```
501
```

`ON CONFLICT DO NOTHING` makes the bulk load re-runnable: re-running the
same batch inserts zero new rows.

## 4. UPDATE — targeted, parameterized, visible

`UPDATE` without a WHERE touches **every row** — the data-loss classic
with no warning and no undo. Always parameterize the WHERE, and use
RETURNING to see what changed.

```python
updated = conn.execute(
    "UPDATE features SET value = value * 2 WHERE entity = ? RETURNING entity, value",
    ("user_42",),
).fetchall()
print(updated)
```

```
[('user_42', 1.84)]
```

## 5. DELETE with LIMIT — the portable pattern

MySQL supports `DELETE ... LIMIT n`; sqlite and Postgres do **not**.
The portable form deletes a bounded batch selected in a subquery. Bounded
batches keep transactions short, locks small, and let a delete loop make
progress on huge tables without grinding the server.

```python
conn.execute(
    "DELETE FROM features WHERE rowid IN (SELECT rowid FROM features WHERE value > ? ORDER BY rowid LIMIT ?)",
    (0.9, 1),
)
total_deleted = 0
while True:
    cur = conn.execute(
        "DELETE FROM features WHERE rowid IN (SELECT rowid FROM features WHERE value > ? ORDER BY rowid LIMIT ?)",
        (0.5, 10),
    )
    if cur.rowcount == 0:
        break
    total_deleted += cur.rowcount
print(f"purged {total_deleted} rows in batches of 10")
```

```
purged 449 rows in batches of 10
```

## Common Mistakes to Avoid

### Mistake 1: UPDATE without WHERE

```sql
-- WRONG - every row zeroed, no warning, no undo
--   UPDATE features SET value = 0
-- CORRECT - always bound the update
--   UPDATE features SET value = ? WHERE entity = ?
```

### Mistake 2: MySQL-only DELETE LIMIT

```sql
-- WRONG - syntax error on sqlite/Postgres
--   DELETE FROM t WHERE cond LIMIT 1
-- CORRECT - portable bounded delete
--   DELETE FROM t WHERE rowid IN (SELECT rowid FROM t WHERE cond ORDER BY rowid LIMIT 1)
```

### Mistake 3: Row-by-row INSERT loops for bulk loads

```python
# WRONG - one round trip per row
#   for item in items:
#       conn.execute("INSERT INTO t (v) VALUES (?)", (item,))
# CORRECT - compile once, execute many
#   conn.executemany("INSERT INTO t (v) VALUES (?)", [(i,) for i in items])
```

### Mistake 4: Upsert without a conflict target

```sql
-- WRONG - the engine needs to know what to conflict ON
--   INSERT ... ON CONFLICT DO UPDATE SET v = excluded.v
-- CORRECT
--   INSERT ... ON CONFLICT (entity) DO UPDATE SET v = excluded.v
```

### Mistake 5: Forgetting RETURNING exists

```python
# WRONG - SELECT after INSERT: racy, extra round trip
#   conn.execute("INSERT INTO t (v) VALUES (?)", (1,))
#   row = conn.execute("SELECT id FROM t WHERE v = ?", (1,)).fetchone()
# CORRECT
#   row = conn.execute("INSERT INTO t (v) VALUES (?) RETURNING id", (1,)).fetchone()
```

## Best Practices

1. Use RETURNING for every insert whose id you need.
2. Make every ingestion pipeline idempotent with ON CONFLICT.
3. Bulk-load with executemany; never loop single inserts.
4. Parameterize every WHERE — values are data, never SQL text.
5. Bound UPDATE/DELETE by a key (entity, id, rowid) whenever possible.
6. Delete in batches of a few thousand; commit per batch in production.
7. Prefer `DO NOTHING` for raw-log dedup, `DO UPDATE` for upserts.
8. Test the re-run: pipeline executed twice == table unchanged.
9. Use `rowcount` to verify deletes did what you expected.
10. Keep DML inside explicit transactions (topic 11) for atomicity.

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Single INSERT with RETURNING | O(log n) | O(1) | — (this is the floor) |
| executemany batch of k rows | O(k log n) | O(k) | never a per-row loop |
| Upsert (conflict check) | O(log n) | O(1) | requires UNIQUE/PK on the target |
| UPDATE without WHERE | O(n) | O(n) | add a bound — usually the bug |
| Bounded DELETE batch of k | O(k log n) | O(k) | unbounded DELETE locks longer |

## AI Engineering Relevance

**Where this shows up:** feature ingestion, log dedup, prediction
backfill, evaluation-result loading.

| Concept here | Used for |
|---|---|
| ON CONFLICT upsert | idempotent feature-store ingestion (re-run safe) |
| RETURNING | handing written ids to caches/message queues |
| executemany | bulk-loading training rows by the million |
| Bounded DELETE | purging stale predictions without long locks |
| parameterized DML | hostile model outputs stored as data, not SQL |

**Scale note:** at 1M rows per batch, executemany is ~100x faster than a
loop; an idempotent upsert saves a full table rebuild on every failed
pipeline retry; an unbounded UPDATE can hold the write lock for minutes
and block every other writer.

## Practice Exercises

### Exercise 1: RETURNING probe  (Difficulty: Easy)

Insert three rows with RETURNING id and confirm the ids are 1, 2, 3
without any SELECT.

### Exercise 2: Idempotent upsert  (Difficulty: Easy)

Upsert the same key 5 times with different values. Assert the table has
exactly one row and the final value is the last one written.

### Exercise 3: DO NOTHING dedup  (Difficulty: Medium)

Insert 10 rows with `ON CONFLICT DO NOTHING`, then the same 10 again.
Assert the count does not change on the second run.

### Exercise 4: Portable bounded delete  (Difficulty: Medium)

Fill a table with 1000 rows. Delete them 25 at a time using the
rowid-subquery pattern. Assert the loop terminates with zero rows left
and record the number of batches.

### Exercise 5: UPDATE with RETURNING  (Difficulty: Medium)

Double all values above a threshold, capture what changed with
RETURNING, and verify only the intended rows were touched.

### Exercise 6: Re-runnable ingestion  (Difficulty: Hard)

Write a function `ingest(rows)` that upserts a batch idempotently and
returns `(inserted_count, updated_count)` using RETURNING + rowcount.
Run it twice; assert the second run updates, never duplicates.

## Summary

| Concept | Description |
|---|---|
| INSERT ... RETURNING | write and read back in one round trip |
| ON CONFLICT DO UPDATE | upsert — idempotent by construction |
| ON CONFLICT DO NOTHING | dedup — first writer wins |
| executemany | bulk insert, compile once |
| parameterized UPDATE/DELETE | bounded, safe, auditable |
| portable DELETE LIMIT | bounded batches via rowid subquery |

DML is where data actually moves, and the rules are simple: write
idempotently, load in bulk, bound every change, parameterize everything.
A pipeline that follows these four rules can be re-run forever without
corrupting the table — which is the difference between an ingestion
pipeline and an incident ticket.

## Quick Reference

| Task | Idiom |
|---|---|
| Insert and get the id | `INSERT ... RETURNING id` |
| Upsert | `INSERT ... ON CONFLICT (k) DO UPDATE SET v = excluded.v` |
| Dedup insert | `INSERT ... ON CONFLICT (k) DO NOTHING` |
| Bulk load | `conn.executemany(stmt, batch)` |
| Bounded delete | `DELETE FROM t WHERE rowid IN (SELECT rowid FROM t WHERE cond ORDER BY rowid LIMIT ?)` |

## Next Steps

Next: **[04 — SELECT Basics](04-select-basics-lecture.md)** — reading the
data you just learned to write: projection, filtering, ordering, and
pagination.

Continues in: **[Phase 4 — Postgres](../../postgres/01-setup-and-psycopg-lecture.md)** —
the same DML against a real server with cursors and server-side batching.

Official docs: https://www.sqlite.org/lang_insert.html ,
https://www.sqlite.org/lang_update.html , https://www.sqlite.org/lang_delete.html
