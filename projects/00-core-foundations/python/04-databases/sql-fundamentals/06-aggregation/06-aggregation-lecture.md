# SQL Fundamentals — 06: Aggregation

## Topic Overview

Aggregation collapses many rows into one number: total, average, count,
min, max. With `GROUP BY` it does this *per group* — the "for each
model", "per label", "per day" pattern that powers evaluation code,
drift monitoring, and analytics dashboards. This lecture covers the five
core aggregate functions, GROUP BY, HAVING vs WHERE, and the
`COUNT(*)` vs `COUNT(col)` distinction that hides silent metric bugs.

The central idea is **stages**: WHERE filters *rows* before grouping;
HAVING filters *groups* after aggregation. Mixing them up either errors
(aggregates are not allowed in WHERE) or silently computes the wrong
statistic. And NULLs interact with aggregates asymmetrically — `AVG`
and `SUM` ignore them, `COUNT(col)` ignores them, `COUNT(*)` does not —
which is exactly where evaluation numbers quietly change.

For AI engineers, aggregation is the language of model reporting:
per-model accuracy, per-label recall, per-bucket latency, cumulative
coverage. Every metric you put on a dashboard is a GROUP BY query with a
NULL policy.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Apply COUNT, SUM, AVG, MIN, MAX over a whole table
2. Explain the COUNT(*) vs COUNT(col) difference with NULLs present
3. Group rows with GROUP BY and compute per-group statistics
4. Filter rows with WHERE and groups with HAVING at the right stage
5. Explain why aggregates are not allowed in WHERE
6. Handle NULLs inside aggregates with COALESCE deliberately
7. Write a per-model accuracy report query
8. Avoid bare-column GROUP BY traps (portable SQL)

## Prerequisites

| Need | Where |
|---|---|
| NULL semantics | `01-relational-model-lecture.md`, `05-filtering-advanced-lecture.md` |
| SELECT basics | `04-select-basics-lecture.md` |

---

## 1. Whole-table aggregates

Aggregates collapse rows into one number. `AVG`/`SUM`/`MIN`/`MAX`
ignore NULLs — they run over the non-NULL subset. `COUNT(*)` counts
rows; `COUNT(col)` counts non-NULL values of that column.

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE predictions (id INTEGER PRIMARY KEY, model TEXT, correct INTEGER, latency_ms REAL, confidence REAL)")
conn.executemany(
    "INSERT INTO predictions (model, correct, latency_ms, confidence) VALUES (?, ?, ?, ?)",
    [
        ("v1", 1, 12.0, 0.91),
        ("v1", 0, 15.0, 0.62),
        ("v1", 1, 11.0, 0.97),
        ("v2", 1, 30.0, 0.80),
        ("v2", 1, 28.0, 0.85),
        ("v2", 0, 33.0, 0.55),
        ("v2", 0, 29.0, None),
    ],
)
row = conn.execute(
    "SELECT COUNT(*), COUNT(correct), SUM(correct), AVG(latency_ms), MIN(latency_ms), MAX(latency_ms) FROM predictions"
).fetchone()
print(row)
row = conn.execute("SELECT COUNT(*), COUNT(confidence) FROM predictions").fetchone()
print(row)
```

```
(7, 7, 4, 22.571428571428573, 11.0, 33.0)
(7, 6)
```

`COUNT(confidence) = 6` — the abstained row's NULL was dropped.

## 2. GROUP BY — per-group aggregates

GROUP BY splits rows into groups; each aggregate runs per group. This is
the "for each model" query of evaluation code.

```python
rows = conn.execute("""
    SELECT model,
           COUNT(*) AS n,
           SUM(correct) AS correct,
           ROUND(100.0 * SUM(correct) / COUNT(*), 1) AS acc_pct,
           ROUND(AVG(latency_ms), 1) AS avg_lat
    FROM predictions
    GROUP BY model
    ORDER BY model
""").fetchall()
for r in rows:
    print(r)
```

```
('v1', 3, 2, 66.7, 12.7)
('v2', 4, 2, 50.0, 30.0)
```

## 3. HAVING vs WHERE — which stage filters what

WHERE filters **rows** before grouping; HAVING filters **groups** after
aggregation. You cannot put per-group conditions in WHERE — the group
does not exist yet.

```python
rows = conn.execute("""
    SELECT model, COUNT(*) AS n
    FROM predictions
    WHERE latency_ms < ?      -- filters rows FIRST
    GROUP BY model
    HAVING COUNT(*) >= ?      -- filters groups AFTER
    ORDER BY model
""", (32.0, 2)).fetchall()
print(rows)
```

```
[('v1', 3), ('v2', 3)]
```

## 4. GROUP BY pitfalls — bare columns and NULL groups

Any selected column must be a group key or inside an aggregate. sqlite
*allows* bare columns (returning an arbitrary row's value); Postgres
raises an error. Write portable SQL: keys + aggregates only.

```python
row = conn.execute(
    "SELECT model, latency_ms FROM predictions GROUP BY model ORDER BY model"
).fetchall()
print(row)   # latency_ms is ARBITRARY here
```

```
[('v1', 12.0), ('v2', 30.0)]
```

Also note: `GROUP BY` treats NULLs as one group — rows with NULL
confidence all land together, which is usually what you want for an
"abstained" bucket.

## Common Mistakes to Avoid

### Mistake 1: COUNT(col) when you meant COUNT(*)

```sql
-- WRONG - one NULL and your "how many predictions" number shrinks
--   SELECT COUNT(confidence) FROM predictions
-- CORRECT - COUNT(*) for rows; COUNT(col) deliberately for non-null
--   SELECT COUNT(*) FROM predictions
```

### Mistake 2: Aggregate in WHERE

```sql
-- WRONG - SQL error: aggregates are not allowed in WHERE
--   SELECT model FROM predictions WHERE SUM(correct) > 1 GROUP BY model
-- CORRECT
--   SELECT model FROM predictions GROUP BY model HAVING SUM(correct) > 1
```

### Mistake 3: AVG over a NULL-heavy column without deciding

```sql
-- WRONG - AVG ignores NULLs; the average is over the non-abstained subset
--   SELECT AVG(confidence) FROM predictions
-- CORRECT - decide what NULL means:
--   SELECT AVG(COALESCE(confidence, 0)) FROM predictions   -- NULL as 0
--   SELECT AVG(confidence) FROM predictions WHERE confidence IS NOT NULL
```

### Mistake 4: Bare columns in GROUP BY

```sql
-- WRONG - arbitrary value per group; works in sqlite, errors in Postgres
--   SELECT model, latency_ms FROM predictions GROUP BY model
-- CORRECT - keys and aggregates only
--   SELECT model, AVG(latency_ms) FROM predictions GROUP BY model
```

### Mistake 5: HAVING without understanding the stage

```sql
-- WRONG - HAVING runs after grouping; it cannot see row-level detail
--   SELECT model FROM predictions GROUP BY model HAVING latency_ms < 20
-- CORRECT - row filter in WHERE, group filter in HAVING
--   SELECT model FROM predictions WHERE latency_ms < 20 GROUP BY model
```

## Best Practices

1. `COUNT(*)` for rows; `COUNT(col)` only when you mean non-NULL values.
2. Put row filters in WHERE, group filters in HAVING — always.
3. Decide the NULL policy of every aggregate (COALESCE or filter).
4. Select only group keys and aggregates — portable SQL.
5. Name computed metrics with aliases (`acc_pct`, `avg_lat`).
6. Cast ratios to REAL/float before dividing to avoid integer division.
7. Verify group counts add up: `SUM(n)` should equal the row count.
8. Use HAVING for threshold filters on aggregates (topic 10 uses the same idea for index costs).
9. Test aggregation queries with at least one NULL-bearing group.
10. Round at the presentation layer or in the query — but be explicit.

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Whole-table aggregate | O(n) | O(1) | pre-aggregated rollup tables |
| GROUP BY (hash) | O(n) | O(g) groups | indexed scan can stream sorted groups |
| DISTINCT inside COUNT | O(n log n) | O(n) | approximate counts (HyperLogLog) at scale |
| HAVING filter | O(g) | O(1) | — (post-aggregation, cheap) |
| AVG over NULLs | O(n) | O(1) | COALESCE policy decided up front |

## AI Engineering Relevance

**Where this shows up:** evaluation reports, drift monitoring, cohort
statistics, training-data profiling.

| Concept here | Used for |
|---|---|
| GROUP BY model | per-model accuracy/latency dashboards |
| COUNT(*) vs COUNT(col) | abstained-prediction accounting |
| HAVING | "models with fewer than 100 evals" filters |
| AVG + COALESCE | mean confidence including abstentions |
| GROUP BY + CASE | bucketed metrics (latency quantiles, score bands) |

**Scale note:** at 100M prediction rows, a GROUP BY model query is a
single O(n) pass — but a `COUNT(col)` vs `COUNT(*)` mistake changes
every downstream percentage by the abstention rate, and nobody gets an
error message. Aggregates amplify both good and bad decisions.

## Practice Exercises

### Exercise 1: The COUNT distinction  (Difficulty: Easy)

Build a table with 10 rows where one column has 2 NULLs. Assert
`COUNT(*)` and `COUNT(col)` differ by exactly the NULL count.

### Exercise 2: Per-group report  (Difficulty: Easy)

Write a query returning per-model `n`, `correct`, and `acc_pct` for a
predictions table. Assert the values for one hand-computed group.

### Exercise 3: WHERE vs HAVING  (Difficulty: Medium)

Write the same "models with >= 2 fast rows" report two ways: WHERE on
latency + HAVING on count, and HAVING on both. Show the results differ
and explain the stage.

### Exercise 4: COALESCE policy  (Difficulty: Medium)

Compute `AVG(confidence)` and `AVG(COALESCE(confidence, 0))` on data
with abstentions. Assert both values and explain which policy each
represents.

### Exercise 5: Group buckets  (Difficulty: Hard)

Use `CASE` inside the SELECT to bucket latency into
`<20`, `20-50`, `>50`, then GROUP BY the bucket expression (with an
alias). Assert bucket counts.

### Exercise 6: Bare-column trap  (Difficulty: Hard)

Run a bare-column GROUP BY in sqlite and confirm it returns *some*
value. Re-express the query portably with an aggregate. Explain what a
Postgres engine would do.

## Summary

| Concept | Description |
|---|---|
| COUNT/SUM/AVG/MIN/MAX | collapse many rows into one number |
| COUNT(*) vs COUNT(col) | rows vs non-NULL values — differ with NULLs |
| GROUP BY | per-group aggregation |
| HAVING vs WHERE | group filters after, row filters before |
| COALESCE | explicit NULL policy inside aggregates |
| bare columns | sqlite allows, Postgres rejects — avoid |

Aggregation is the engine of every model metric. The three rules that
keep metrics honest: count rows with COUNT(*), filter rows in WHERE and
groups in HAVING, and decide explicitly what NULLs mean inside every
aggregate. Get these right and every dashboard number is trustworthy.

## Quick Reference

| Task | Idiom |
|---|---|
| Row count | `SELECT COUNT(*) FROM t` |
| Per-group | `SELECT g, COUNT(*), AVG(v) FROM t GROUP BY g` |
| Group filter | `... GROUP BY g HAVING COUNT(*) >= ?` |
| NULL-aware mean | `AVG(COALESCE(v, 0))` |
| Buckets | `GROUP BY CASE WHEN v < 20 THEN 'fast' ELSE 'slow' END` |
| Accuracy pct | `ROUND(100.0 * SUM(correct) / COUNT(*), 1)` |

## Next Steps

Next: **[07 — Joins](07-joins-lecture.md)** — combining rows across
tables: INNER/LEFT/RIGHT/FULL/CROSS, self-joins, and row-explosion
control.

Continues in: **[Phase 9 — ML](../../../09-ml-mlops/README.md)** —
evaluation dashboards are aggregation at production scale.

Official docs: https://www.sqlite.org/lang_aggfunc.html
