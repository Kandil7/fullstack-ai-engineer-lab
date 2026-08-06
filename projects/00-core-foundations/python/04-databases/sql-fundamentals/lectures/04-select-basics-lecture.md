# SQL Fundamentals — 04: SELECT Basics

## Topic Overview

SELECT is where SQL earns its keep: every model-serving endpoint, every
evaluation query, every analytics dashboard starts as a SELECT. This
lecture covers the core clauses — projection, WHERE, ORDER BY,
LIMIT/OFFSET, DISTINCT, aliases — and the *discipline* around them.

Two ideas carry the lecture. First, **projection is a contract**: naming
the columns you need keeps queries fast, small, and resilient to schema
changes; `SELECT *` is a convenience that ships a whole row when one
float was needed. Second, **order is never free**: without ORDER BY,
row order is undefined; with it, you pay a sort — and LIMIT without
ORDER BY is not "top-k", it is "any k rows".

For AI engineers, SELECT basics are the daily vocabulary of feature
extraction and evaluation: "the top-3 highest-confidence predictions per
label", "the second page of model runs", "the distinct set of users in
the beta cohort".

## Learning Objectives

By the end of this lecture, you will be able to:

1. Project exactly the columns a query needs, with aliases for computed ones
2. Filter rows with WHERE and explain the evaluation order
3. Order results deterministically with ORDER BY, knowing NULL placement
4. Page results with LIMIT/OFFSET and describe its scaling cost
5. Deduplicate with DISTINCT and say what it actually deduplicates
6. Name computed expressions with aliases for downstream consumers
7. Explain why `SELECT *` is a performance and maintenance hazard
8. Write a deterministic "top-k by score" query

## Prerequisites

| Need | Where |
|---|---|
| Tables and rows | `01-relational-model-lecture.md` |
| DML (inserting test data) | `03-insert-update-delete-lecture.md` |

---

## 1. Projection — choose columns, not SELECT *

Projection picks **columns**; WHERE picks **rows**. Selecting only what
you consume is the cheapest performance win in SQL — and the most
ignored. Projection also enables covering indexes (topics 10 and 14).

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE samples (id INTEGER PRIMARY KEY, label TEXT, score REAL)")
conn.executemany(
    "INSERT INTO samples (label, score) VALUES (?, ?)",
    [("cat", 0.95), ("dog", 0.88), ("cat", 0.62), ("bird", 0.40)],
)
result = conn.execute("SELECT label, score FROM samples").fetchall()
print(result)
```

```
[('cat', 0.95), ('dog', 0.88), ('cat', 0.62), ('bird', 0.4)]
```

## 2. WHERE — row filtering

WHERE filters before ORDER BY and LIMIT run. The evaluation order —
filter, then sort, then limit — is why `LIMIT 10` on a big unfiltered
table still scans everything: the filter has already happened by the
time the limit could help.

```python
high = conn.execute("SELECT label FROM samples WHERE score > ?", (0.9,)).fetchall()
print([r[0] for r in high])
```

```
['cat', 'dog']
```

## 3. ORDER BY — and NULL ordering

ORDER BY gives rows a defined order (ASC by default). NULL placement is
dialect-dependent: sqlite sorts NULLs first in ASC; Postgres sorts them
last. Never rely on NULL position — use `NULLS FIRST/LAST` (sqlite 3.30+,
Postgres both support it) when it matters.

```python
top3 = conn.execute(
    "SELECT label, score FROM samples ORDER BY score DESC LIMIT ?", (3,)
).fetchall()
print(top3)
```

```
[('cat', 0.95), ('dog', 0.88), ('cat', 0.62)]
```

## 4. LIMIT / OFFSET — pagination

`LIMIT n OFFSET m` returns n rows after skipping m. It works, but each
page re-reads the m skipped rows — O(offset) work per page, O(n^2) over
all pages. Topic 14 shows keyset pagination, the fix.

```python
page = conn.execute(
    "SELECT label, score FROM samples ORDER BY id LIMIT ? OFFSET ?", (2, 2)
).fetchall()
print(page)
```

```
[('cat', 0.62), ('bird', 0.4)]
```

## 5. DISTINCT — set semantics

DISTINCT collapses duplicates across the **projected row**, not per
column. It is a sort/hash — not free — so ask for it only when you need
the set.

```python
labels = conn.execute("SELECT DISTINCT label FROM samples ORDER BY label").fetchall()
print([r[0] for r in labels])
```

```
['bird', 'cat', 'dog']
```

## 6. Aliases — readability and computed columns

Aliases rename a column or expression. Computed features get names that
downstream code — or the next join — can reference.

```python
rows = conn.execute(
    "SELECT label, ROUND(score * 100, 1) AS confidence_pct FROM samples WHERE id = ?",
    (1,),
).fetchall()
print(rows)
```

```
[('cat', 95.0)]
```

## Common Mistakes to Avoid

### Mistake 1: SELECT * when two columns are enough

```sql
-- WRONG - more I/O, more bytes, defeats covering indexes
--   SELECT * FROM samples
-- CORRECT
--   SELECT label, score FROM samples
```

### Mistake 2: Relying on default order

```sql
-- WRONG - row order is not stable without ORDER BY
--   SELECT label FROM samples
-- CORRECT - order exists only when you ask for it
--   SELECT label FROM samples ORDER BY id
```

### Mistake 3: LIMIT without ORDER BY

```sql
-- WRONG - "any 3 rows", not "top 3"
--   SELECT label, score FROM samples LIMIT 3
-- CORRECT
--   SELECT label, score FROM samples ORDER BY score DESC LIMIT 3
```

### Mistake 4: Confusing DISTINCT scope

```sql
-- WRONG - dedupes on (label, score), not on label
--   SELECT DISTINCT label, score FROM samples
-- CORRECT - dedupe on exactly what you need
--   SELECT DISTINCT label FROM samples
```

### Mistake 5: OFFSET as the default pagination

```sql
-- WRONG - O(offset) re-read work per page at scale
--   ... ORDER BY id LIMIT 10 OFFSET 10000
-- CORRECT - keyset: WHERE id > last_id ORDER BY id LIMIT 10  (topic 14)
```

## Best Practices

1. Project explicitly; let `SELECT *` be a deliberate choice, never the default.
2. Always pair LIMIT with ORDER BY when order matters (it almost always does).
3. Alias every computed expression; consumers will reference it by name.
4. Parameterize every value in WHERE — always (topic 13).
5. Use DISTINCT deliberately; it costs a sort or hash.
6. When paging, prefer keyset over OFFSET for anything past a few pages.
7. Name columns in the SELECT that downstream code will map — avoid
   positional tuple indexing.
8. Keep WHERE predicates sargable (bare columns) for indexability (topic 14).
9. Test ORDER BY with NULLs in the column; know your dialect's placement.
10. Verify page boundaries with explicit LIMIT/OFFSET numbers in tests.

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Projection (fewer columns) | O(n) read | less I/O | the single cheapest win |
| WHERE on indexed column | O(log n) | O(1) | needs index (topic 10) |
| ORDER BY | O(n log n) | O(n) | index-satisfied ordering (topic 10) |
| LIMIT/OFFSET page m | O(m) skipped | O(1) | keyset pagination — O(log n) |
| DISTINCT | O(n log n) sort / O(n) hash | O(n) | skip when duplicates are fine |

## AI Engineering Relevance

**Where this shows up:** feature queries, evaluation reports,
model-serving read paths.

| Concept here | Used for |
|---|---|
| Projection | serving only the features the model needs |
| ORDER BY + LIMIT | top-k predictions, best checkpoint per metric |
| OFFSET | dashboard paging over runs |
| DISTINCT | unique users/entities in a cohort |
| Aliases | naming computed features for downstream code |

**Scale note:** at 1M rows, `SELECT *` on a wide row can move 10x the
bytes of a projected query; at 100M rows an unindexed ORDER BY spills to
disk. The projection habit costs nothing at small scale and saves
everything at large scale.

## Practice Exercises

### Exercise 1: Minimal projection  (Difficulty: Easy)

From a `samples` table, return only `label` for rows with `score > 0.5`.
Assert each returned row has exactly one element.

### Exercise 2: Deterministic top-k  (Difficulty: Easy)

Return the 3 highest-scoring labels with a tie-breaker (id) in the
ORDER BY. Run twice and assert identical results.

### Exercise 3: Pagination equivalence  (Difficulty: Medium)

Write two queries returning page 3 of size 2: one with OFFSET, one with
keyset (`WHERE id > last_id`). Assert they return the same rows.

### Exercise 4: DISTINCT scope  (Difficulty: Medium)

Create rows with duplicate labels but different scores. Show that
`SELECT DISTINCT label` and `SELECT DISTINCT label, score` return
different numbers of rows. Explain why.

### Exercise 5: Aliased computed column  (Difficulty: Medium)

Return `ROUND(score * 100, 1) AS confidence_pct` for each sample.
Assert the alias resolves and the values are rounded as expected.

### Exercise 6: NULL ordering  (Difficulty: Hard)

Insert a row with a NULL score. Query `ORDER BY score ASC` and
`ORDER BY score ASC NULLS LAST`. Document the difference and write a
query that is portable across sqlite and Postgres.

## Summary

| Concept | Description |
|---|---|
| Projection | naming the columns you consume |
| WHERE | row filtering before sort/limit |
| ORDER BY | the only source of row order |
| LIMIT/OFFSET | simple pagination, O(offset) per page |
| DISTINCT | set semantics over the projected row |
| Alias | naming a column or computed expression |

SELECT basics are small but their discipline compounds: explicit
projection, deterministic ordering, deliberate DISTINCT, and named
computed columns are what make feature and evaluation queries fast,
stable, and maintainable. Every later topic — joins, windows, indexes,
optimization — assumes you write SELECTs this cleanly.

## Quick Reference

| Task | Idiom |
|---|---|
| Project | `SELECT col1, col2 FROM t` |
| Filter | `WHERE score > ?` |
| Top-k | `ORDER BY score DESC LIMIT ?` |
| Page | `LIMIT ? OFFSET ?` |
| Dedupe | `SELECT DISTINCT col FROM t` |
| Rename | `SELECT ROUND(x, 2) AS label_pct FROM t` |

## Next Steps

Next: **[05 — Advanced Filtering](05-filtering-advanced-lecture.md)** —
IN, BETWEEN, LIKE, IS NULL, and the three-valued-logic traps hidden in
compound filters.

Continues in: **[Phase 9 — GenAI](../../../09-ml-mlops/README.md)** —
feature-serving queries follow the same projection discipline.

Official docs: https://www.sqlite.org/lang_select.html
