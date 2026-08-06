# SQL Fundamentals — 09: Window Functions

## Topic Overview

Window functions compute per-group values — rankings, running totals,
previous-row values — **without collapsing rows** the way GROUP BY does. Every
row survives; a computed column is added to it. That one property makes them
the tool for "rank models per dataset", "cumulative metrics over time", and
"lag features" in feature pipelines.

The syntax has three parts: the function (`ROW_NUMBER`, `RANK`, `SUM`, ...),
`OVER`, and the window definition — `PARTITION BY` (grouping), `ORDER BY`
(order inside the window), and optionally a **frame** (`ROWS BETWEEN ...`)
that limits which rows the function sees. This topic builds each part and the
mistakes around them: forgetting PARTITION BY (one global window), ROW_NUMBER
vs RANK with ties, and confusing window ORDER BY with output ORDER BY.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write `OVER (PARTITION BY ... ORDER BY ...)` windows.
2. Distinguish ROW_NUMBER, RANK, and DENSE_RANK on ties.
3. Use LAG/LEAD for previous/next row values.
4. Compute running totals and moving averages with frames.
5. Explain why window functions keep rows while GROUP BY collapses them.
6. Choose PARTITION BY to isolate per-group windows.
7. Diagnose a forgotten-frame moving average.
8. Convert a window query to GROUP BY when collapse is actually wanted.

## Prerequisites

| Need | Where |
|---|---|
| SELECT / ORDER BY | `04-select-basics-lecture.md` |
| Aggregation | `06-aggregation-lecture.md` |
| Subqueries/CTEs | `08-subqueries-ctes-lecture.md` |

---

## 1. ROW_NUMBER — ranking without ties

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE evals (id INTEGER PRIMARY KEY, model TEXT, dataset TEXT, score REAL)")
conn.executemany("INSERT INTO evals (model, dataset, score) VALUES (?, ?, ?)",
                 [("m1", "d1", 0.91), ("m1", "d2", 0.82),
                  ("m2", "d1", 0.88), ("m2", "d2", 0.90),
                  ("m3", "d1", 0.95), ("m3", "d2", 0.78)])
rows = conn.execute("""
    SELECT model, dataset, score,
           ROW_NUMBER() OVER (PARTITION BY dataset ORDER BY score DESC) AS rn
    FROM evals ORDER BY dataset, rn
""").fetchall()
for r in rows:
    print(r)
```

```
('m3', 'd1', 0.95, 1)
('m1', 'd1', 0.91, 2)
('m2', 'd1', 0.88, 3)
('m2', 'd2', 0.90, 1)
('m1', 'd2', 0.82, 2)
('m3', 'd2', 0.78, 3)
```

`PARTITION BY dataset` restarts the numbering per dataset; `ORDER BY score
DESC` decides the rank order. Every row survives with its per-partition rank.

## 2. RANK vs DENSE_RANK — ties

```python
rows = conn.execute("""
    SELECT score,
           RANK() OVER (ORDER BY score DESC) AS rk,
           DENSE_RANK() OVER (ORDER BY score DESC) AS drk
    FROM (SELECT DISTINCT score FROM evals) ORDER BY score DESC
""").fetchall()
print(rows)
```

```
[(0.95, 1, 1), (0.91, 2, 2), (0.9, 3, 3), (0.88, 4, 4), (0.82, 5, 5), (0.78, 6, 6)]
```

With ties (add a duplicate score): RANK leaves a gap after tied rows
(1, 1, 3), DENSE_RANK does not (1, 1, 2). Choose RANK for "1st, 1st, 3rd"
sports semantics; DENSE_RANK for contiguous standings.

## 3. LAG / LEAD — previous and next row

```python
rows = conn.execute("""
    SELECT model, score,
           LAG(score) OVER (ORDER BY id) AS prev_score,
           LEAD(score) OVER (ORDER BY id) AS next_score
    FROM evals ORDER BY id
""").fetchall()
print(rows)
```

```
[('m1', 0.91, None, 0.82), ('m1', 0.82, 0.91, 0.88), ('m2', 0.88, 0.82, 0.9), ...]
```

LAG gives the previous row's value, LEAD the next — the raw material of
deltas (`score - LAG(score)`) and lag features for time-series models.

## 4. Running totals — SUM with OVER

```python
rows = conn.execute("""
    SELECT id, score, SUM(score) OVER (ORDER BY id) AS running_total
    FROM evals ORDER BY id
""").fetchall()
print(rows)
```

```
[(1, 0.91, 0.91), (2, 0.82, 1.73), (3, 0.88, 2.61), ...]
```

Without a frame, `SUM OVER (ORDER BY ...)` accumulates from the start of the
partition to the current row — the running total.

## 5. Frames — the window inside the window

A frame bounds which rows the function sees relative to the current row.

```python
conn.execute("CREATE TABLE daily (day INTEGER PRIMARY KEY, metric REAL)")
conn.executemany("INSERT INTO daily (day, metric) VALUES (?, ?)",
                 [(1, 10.0), (2, 20.0), (3, 30.0), (4, 40.0), (5, 50.0)])
rows = conn.execute("""
    SELECT day, metric,
           AVG(metric) OVER (ORDER BY day ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS ma2
    FROM daily ORDER BY day
""").fetchall()
print(rows)
```

```
[(1, 10.0, 10.0), (2, 20.0, 15.0), (3, 30.0, 25.0), (4, 40.0, 35.0), (5, 50.0, 45.0)]
```

`ROWS BETWEEN 1 PRECEDING AND CURRENT ROW` = a 2-point moving average. The
frame is how analytics windows (7-day MA, cumulative quarters) are expressed.

## Common Mistakes to Avoid

### Mistake 1: Forgetting PARTITION BY

```sql
-- WRONG - one global window: rankings cross datasets
--   SELECT ..., ROW_NUMBER() OVER (ORDER BY score DESC) FROM evals
-- CORRECT - per-dataset windows
--   SELECT ..., ROW_NUMBER() OVER (PARTITION BY dataset ORDER BY score DESC)
```

### Mistake 2: ROW_NUMBER where ties should share a rank

```sql
-- WRONG - tied scores get arbitrary distinct numbers
--   SELECT ..., ROW_NUMBER() OVER (ORDER BY score DESC)
-- CORRECT - for tied scoring
--   SELECT ..., RANK() OVER (ORDER BY score DESC)
```

### Mistake 3: Confusing OVER's ORDER BY with the output ORDER BY

```sql
-- WRONG - thinking one ORDER BY does both
-- CORRECT - OVER's ORDER BY defines the window; a separate outer ORDER BY sorts output
```

### Mistake 4: Moving average without a frame

```sql
-- WRONG - AVG OVER (ORDER BY day) is a CUMULATIVE average, not a 2-day MA
-- CORRECT - ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
```

### Mistake 5: Expecting row collapse like GROUP BY

```sql
-- WRONG - "window functions shrink my result set"
-- CORRECT - windows keep every row and add a computed column; GROUP BY collapses
```

## Best Practices

1. Always state PARTITION BY when you mean per-group windows.
2. Choose RANK vs DENSE_RANK by tie semantics explicitly.
3. Give window expressions aliases (`AS rn`, `AS ma2`).
4. Use LAG/LEAD for deltas and lag features.
5. Specify frames for moving averages; know the default frame otherwise.
6. Keep OVER's ORDER BY separate from the output ORDER BY.
7. Test windows on small hand-computed data.
8. Combine with CTEs: compute the window in one step, filter after.
9. Use `DISTINCT` carefully when window values repeat.
10. Explain the query; window functions are index-sensitive.

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Window over n rows | O(n log n) (sort) | O(n) | index on the window ORDER BY |
| Partitioned window | O(n log n) per partition | O(partition) | index on partition+order keys |
| Frame operations | O(frame) per row | O(1) | bounded frames are cheap |
| LAG/LEAD | O(n) | O(1) | none — they are already cheap |

Windows require a sort unless the index already orders by the window keys —
topic 10 shows how to prove it with EXPLAIN.

## AI Engineering Relevance

**Where this shows up:** model ranking per benchmark, cumulative evaluation
curves, and time-series lag features in training data.

| Concept here | Used for |
|---|---|
| ROW_NUMBER / RANK | ranking models per dataset or task |
| Running totals | cumulative accuracy/coverage curves |
| LAG / LEAD | lag features for forecasting models |
| Frames | rolling evaluation windows |
| PARTITION BY | per-tenant or per-model isolation in metrics |

**Scale note:** at eval-corpus scale, a window sort per query is fine; at
feature-engineering scale you materialize the windowed features once into the
training table rather than recomputing per epoch.

## Practice Exercises

### Exercise 1: Per-group rank  (Difficulty: Easy)
Rank models per dataset with ROW_NUMBER. Assert the ranks restart per dataset.

### Exercise 2: Tie semantics  (Difficulty: Easy)
Add tied scores; assert RANK leaves a gap and DENSE_RANK does not.

### Exercise 3: Lag deltas  (Difficulty: Medium)
Compute `score - LAG(score)` per ordered rows; assert the delta values.

### Exercise 4: Running total  (Difficulty: Medium)
Compute a cumulative sum and assert it equals hand-computed values.

### Exercise 5: Moving average frame  (Difficulty: Hard)
Build a 3-day MA with an explicit frame; assert values including the warm-up
rows.

### Exercise 6: Window + CTE  (Difficulty: Hard)
Rank in a CTE, then filter to the top-2 per group in the outer query. Assert
the output.

## Summary

| Concept | Description |
|---|---|
| OVER | the window keyword |
| PARTITION BY | per-group window isolation |
| ROW_NUMBER/RANK/DENSE_RANK | rankings with chosen tie semantics |
| LAG/LEAD | previous/next row values |
| Frames | ROWS BETWEEN bounding the window |
| vs GROUP BY | windows keep rows; GROUP BY collapses |

Window functions are the professional answer to "per-group value without
losing rows". The three knobs — partition, order, frame — cover ranking,
running totals, and rolling statistics.

## Quick Reference

| Task | Idiom |
|---|---|
| Per-group rank | `ROW_NUMBER() OVER (PARTITION BY g ORDER BY v DESC)` |
| Tied ranking | `RANK()` / `DENSE_RANK()` |
| Previous row | `LAG(v) OVER (ORDER BY id)` |
| Running total | `SUM(v) OVER (ORDER BY id)` |
| Moving average | `AVG(v) OVER (ORDER BY d ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)` |
| Delta | `v - LAG(v) OVER (ORDER BY id)` |

## Next Steps

Next: **[10 — Indexes and Plans](10-indexes-and-plans-lecture.md)** — why the sort
behind windows is or isn't free.

Continues in: **[Phase 9 — RAG](../../09-ml-mlops/README.md)** — rankings are window
functions at retrieval scale.

Official docs: https://www.sqlite.org/windowfunctions.html
