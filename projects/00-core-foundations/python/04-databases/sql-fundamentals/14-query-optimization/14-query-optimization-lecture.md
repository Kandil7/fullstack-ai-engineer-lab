# SQL Fundamentals — 14: Query Optimization

## Topic Overview

Slow queries are almost never a hardware problem. They are a shape problem:
the predicate wraps the indexed column so the index cannot be used, the
query drags `SELECT *` across the wire, pagination re-scans skipped rows, or
the code fires one query per row (N+1). Optimization is reading the plan,
keeping predicates sargable, projecting only what you need, continuing from
keys instead of offsets, and batching round trips. These five habits turn
5-second endpoints into 5-millisecond ones — the difference between a demo
and a product.

The mental model: the optimizer works off *shape*, not data. Give it shapes
it recognizes — bare indexed columns, bounded ranges, `IN` lists — and it
returns fast plans.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Read `EXPLAIN QUERY PLAN` and tell a scan from an index search.
2. Explain sargability and keep predicates index-friendly.
3. Project only the columns a feature needs.
4. Choose keyset pagination over offset for deep pages.
5. Recognize N+1 query storms and replace them with batching.
6. Verify optimizations with plans and measured timing, not vibes.

## Prerequisites

| Need | Where |
|---|---|
| Indexes and plans | `10-indexes-and-plans-lecture.md` |
| GROUP BY / aggregation | `06-aggregation-lecture.md` |

---

## 1. Read the plan

```python
conn.execute("EXPLAIN QUERY PLAN SELECT * FROM events WHERE user_id = 7").fetchall()
```

Plans say which strategy the optimizer chose. `SEARCH ... USING INDEX` means
the index did the work; `SCAN` means every row was read. sqlite's
`EXPLAIN QUERY PLAN` gives one readable line per step; Postgres `EXPLAIN
ANALYZE` adds row counts and timings. The habit: any query you care about
gets a plan check.

## 2. Sargability

**Sargable** = "Search ARGument ABLE" — the indexed column stands alone on
one side of the comparison:

```sql
-- Sargable: index range scan
WHERE user_id >= 10 AND user_id < 20
-- NOT sargable: function around the column forces a full scan
WHERE CAST(user_id AS TEXT) LIKE '1%'
```

`WHERE DATE(created_at) = 'today'` is the classic killer — wrap the *other*
side instead: `created_at >= '2026-08-06' AND created_at < '2026-08-07'`.

## 3. Project the columns you use

`SELECT *` fetches every column, preventing covering-index reads and bloating
network payloads. Name the columns the code actually touches. This is
free performance and better API hygiene.

## 4. Keyset vs offset pagination

Offset pagination discards the skipped rows *every page* — page 10,000 costs
10,000 rows of work. Keyset pagination remembers the last key and continues
from it:

```sql
-- OFFSET: O(page_number * page_size) work
SELECT id FROM events ORDER BY id LIMIT 50 OFFSET 10000;
-- Keyset: indexed range scan, O(page_size)
SELECT id FROM events WHERE id > 10049 ORDER BY id LIMIT 50;
```

Keyset needs a stable, ordered key (the primary key works) and a `WHERE id >
last_id` continuation — no offsets at all. Tradeoff: no arbitrary jump to
page N; you navigate forward only.

## 5. N+1 and batching

N+1 is one query for a list, then one query *per row*: 100 rows = 101 round
trips, each with network + parse + plan overhead. The fix is one query with
an `IN` list (or a JOIN) and re-grouping in Python:

```python
# BROKEN: N+1
for uid in user_ids:
    count += execute("SELECT COUNT(*) FROM events WHERE user_id = ?", (uid,))[0]
# FIXED: one round trip
execute("SELECT COUNT(*) FROM events WHERE user_id IN (?, ?, ...)", user_ids)
```

The N+1 pattern is how every slow ORM API starts — including RAG pipelines
that fetch a document then its chunks one query at a time.

## Common Mistakes to Avoid

### Mistake 1: Functions on the indexed column

```python
# WRONG - WHERE DATE(created_at) = 'today'   (full scan)
# CORRECT - WHERE created_at >= ? AND created_at < ?
```

### Mistake 2: Deep offsets

```python
# WRONG - LIMIT 50 OFFSET 100000            (re-scans 100k rows)
# CORRECT - WHERE id > last_id LIMIT 50
```

### Mistake 3: Per-row queries in a loop

```python
# WRONG - query inside the for loop          (N+1)
# CORRECT - one IN/JOIN query, group in Python
```

### Mistake 4: SELECT * + Python-side filtering

```python
# WRONG - fetch everything, filter in code
# CORRECT - project columns; push filters into WHERE
```

### Mistake 5: Optimizing without measuring

```python
# WRONG - assuming a rewrite helps
# CORRECT - EXPLAIN the plan and time it before/after
```

## Best Practices

1. Read the plan before and after every "optimization".
2. Keep predicates sargable: bare indexed columns on one side.
3. Project the columns a feature needs.
4. Use keyset pagination for deep or long-lived pages.
5. Batch lookups with IN lists; group results in Python.
6. Add the index the query's WHERE/JOIN/ORDER BY actually wants.
7. Measure latency percentiles, not just averages.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Full scan (non-sargable) | O(rows) per query | sargable predicate + index |
| OFFSET deep page | O(offset) work per page | keyset, O(page_size) |
| N+1 round trips | O(N) × network latency | one IN-list query |
| SELECT * | every column over the wire | projected columns |
| Missing index | scan even when sargable | matching index |

Every row here is a shape decision. Indexes turn O(n) scans into O(log n)
lookups; the plan tells you which shape you actually got.

## AI Engineering Relevance

**Where this shows up:** RAG chunk fetch (embedding lookup then chunk read),
evaluation result pagination, feature stores, and every read path behind an
LLM endpoint — a 50ms query becomes 500ms × 3 inside a chain and decides
your p95.

| Concept here | Used for |
|---|---|
| Sargable predicates | embedding-vector + metadata filter queries |
| Projection | returning only ids, not whole blobs |
| Keyset pagination | scrolling eval logs / audit trails |
| IN-list batching | bulk chunk fetch for a query's top-k |
| Plan reading | verifying pgvector / hybrid plans |

**Scale note:** LLM apps multiply every database cost by the number of
parallel chain calls. Optimizing one query's shape optimizes the whole
agent's latency.

## Practice Exercises

### Exercise 1: Read plans  (Difficulty: Easy)
Build a table + index; assert the plan uses the index for a sargable
predicate and scans for a non-sargable one.

### Exercise 2: Sargable rewrite  (Difficulty: Easy)
Rewrite a function-wrapped predicate as a range; assert the plan improves.

### Exercise 3: Projection  (Difficulty: Medium)
Prove `SELECT id, v` returns fewer columns than `SELECT *` on the same rows.

### Exercise 4: Keyset vs offset  (Difficulty: Medium)
Show keyset page 2 equals offset page 2; assert equality on real data.

### Exercise 5: Kill the N+1  (Difficulty: Medium)
Reproduce N+1 and IN-list batching on the same data; assert equal results
and fewer round trips (instrument with a counter).

### Exercise 6: End-to-end tuning  (Difficulty: Hard)
Create a 10k-row table, find a slow query via EXPLAIN, add the right index,
and assert both the plan change and a measured speedup.

## Summary

| Concept | Description |
|---|---|
| Plan reading | the evidence for every optimization |
| Sargable predicates | bare indexed columns; never wrap them |
| Projection | fetch only needed columns |
| Keyset pagination | continue from a key, not an offset |
| Batching | one IN-list instead of N+1 round trips |
| Measurement | plans and timings before/after |

Fast queries are shaped, not tuned. Index-friendly predicates, projected
columns, keyset navigation, and batched round trips are the four shapes that
keep databases fast at scale.

## Quick Reference

| Task | Idiom |
|---|---|
| See the plan | `EXPLAIN QUERY PLAN SELECT ...` |
| Day range, index-safe | `created_at >= ? AND created_at < ?` |
| Next page, deep | `WHERE id > ? ORDER BY id LIMIT 50` |
| Batch lookup | `WHERE id IN (?, ?, ...)` |
| Verify a fix | plan before/after + `time.perf_counter()` |

## Next Steps

This completes **SQL Fundamentals**. Continue to:
- **[SQLAlchemy 05 — Querying 2.0](../sqlalchemy/05-querying-2-0-lecture.md)** — the same
  habits through an ORM.
- **[04-databases — Postgres 07 Query Tuning](../../04-databases/postgres/lectures/07-query-tuning-lecture.md)** —
  `EXPLAIN ANALYZE` and planner internals in a real engine.

Official docs: https://www.sqlite.org/optoverview.html
