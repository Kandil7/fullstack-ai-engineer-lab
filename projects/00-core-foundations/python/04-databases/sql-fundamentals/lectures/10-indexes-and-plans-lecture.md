# SQL Fundamentals — 10: Indexes and Query Plans

## Topic Overview

An index is a sorted copy of selected columns that turns an O(n) scan into an
O(log n) lookup. It is the single most effective performance tool in SQL —
and the most misused. The professional skill is not "add an index"; it is
**proving with EXPLAIN that the plan changed from SCAN to SEARCH**, and
knowing when an index will never be used: low selectivity, wrong composite
column order, or a predicate that can't use the structure.

This topic covers B-tree mechanics at the level you need, `EXPLAIN QUERY
PLAN` as the evidence loop, composite index column order, the selectivity
threshold, and the write-cost tradeoff every index carries.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Read an EXPLAIN QUERY PLAN and distinguish SCAN from SEARCH.
2. Explain how a B-tree index serves equality lookups in O(log n).
3. Decide when an index is worth it (selectivity, query mix).
4. Design composite index column order by predicate coverage.
5. Explain why low-cardinality indexes go unused.
6. State the write-cost tradeoff of every index.
7. Use EXPLAIN before and after to prove the change.
8. Diagnose "index exists but query still scans".

## Prerequisites

| Need | Where |
|---|---|
| WHERE filtering | `05-filtering-advanced-lecture.md` |
| Joins | `07-joins-lecture.md` |
| Query optimization | `14-query-optimization-lecture.md` |

---

## 1. The scan — what a missing index costs

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE logs (id INTEGER PRIMARY KEY, level TEXT, user_id INTEGER)")
# (100k rows inserted)
print(conn.execute("EXPLAIN QUERY PLAN SELECT * FROM logs WHERE user_id = 42").fetchall())
```

```
[(4, 0, 0, 'SCAN logs')]
```

Without an index, the planner reads every row — 100k row reads to find the
matches. Fine at 1k rows, minutes at 1B.

## 2. The index — and the proof

```python
conn.execute("CREATE INDEX idx_logs_user ON logs(user_id)")
print(conn.execute("EXPLAIN QUERY PLAN SELECT * FROM logs WHERE user_id = 42").fetchall())
```

```
[(3, 0, 0, 'SEARCH logs USING INDEX idx_logs_user (user_id=?)')]
```

The plan changed from SCAN to SEARCH. The index holds (user_id -> rowids)
sorted; the lookup is a tree descent, O(log n). **This before/after pair is
the evidence that an index matters** — never add one without it.

## 3. B-tree mechanics in one paragraph

A B-tree keeps keys sorted in pages with branching factors in the hundreds. An
equality lookup descends ~log_f(n) levels — for a billion rows that is ~4
levels, not a billion comparisons. Range queries (`BETWEEN`, `>`) use the same
structure via sequential page scans. The sortedness is also what makes
`ORDER BY` and join keys free when the index covers them.

## 4. Selectivity — when an index is unused

An index pays when it narrows the set; a planner may ignore it when most rows
match.

```python
conn.execute("CREATE INDEX idx_logs_level ON logs(level)")
print(conn.execute("EXPLAIN QUERY PLAN SELECT * FROM logs WHERE level = 'info'").fetchall())
print(conn.execute("EXPLAIN QUERY PLAN SELECT * FROM logs WHERE level = 'error'").fetchall())
```

```
[(3, 0, 0, 'SEARCH logs USING INDEX idx_logs_level (level=?)')]
[(3, 0, 0, 'SEARCH logs USING INDEX idx_logs_level (level=?)')]
```

With 'info' matching 90% of rows, reading the index then fetching 90% of the
table is more work than scanning — good planners choose a scan. Indexing
low-cardinality columns (level with 3 values, booleans) is usually wasted
because the selectivity is too low to help.

## 5. Composite indexes — column order decides coverage

A composite index `(level, user_id)` is sorted by level first, then user_id
within each level. Consequences:

- `WHERE level = ?` alone — uses the index (leading column).
- `WHERE level = ? AND user_id = ?` — uses the index fully.
- `WHERE user_id = ?` alone — **cannot** use it; user_id is not leading.

```python
conn.execute("CREATE INDEX idx_logs_level_user ON logs(level, user_id)")
print(conn.execute("EXPLAIN QUERY PLAN SELECT * FROM logs WHERE user_id = 5 AND level = 'error'").fetchall())
print(conn.execute("EXPLAIN QUERY PLAN SELECT * FROM logs WHERE user_id = 5").fetchall())
```

```
[(3, 0, 0, 'SEARCH logs USING INDEX idx_logs_level_user (level=? AND user_id=?)')]
[(0, 0, 0, 'SCAN logs')]
```

The rule: **leading column = the one filters always include**; put the most
restrictive or most-common filter first. A composite index with the wrong
leading column is an index that silently does nothing for its most important
query.

## 6. The write cost — every index taxes INSERT

Every index must be maintained on every write: an insert that once wrote one
row now writes the row plus an entry in every index (and possibly splits a
B-tree page).

```python
# bench_inserts(False) ~ 0.03s ; bench_inserts(True) ~ 0.05s on 20k rows
```

```
insert 20k rows, no index: 0.031s
insert 20k rows, 1 index : 0.048s
```

On a hot write table (event logs, usage records), the write amplification is
real. The discipline: index what queries need, measure the write cost, and
drop indexes that don't serve a query.

## 7. Covering indexes — the free read

A covering index contains every column the query needs, so the engine never
returns to the table — the index alone answers it. `SELECT level, user_id
FROM logs WHERE user_id = 5` with `(user_id, level)` reads only the index. The
cost is a wider index; the win is eliminating table fetches.

## Common Mistakes to Avoid

### Mistake 1: Adding an index without EXPLAIN proof

```sql
-- WRONG - "I added an index" with no plan check; it may be unused
-- CORRECT - before/after EXPLAIN: SCAN -> SEARCH
```

### Mistake 2: Wrong leading column in a composite

```sql
-- WRONG - (user_id, level) when queries filter by level then user_id
-- CORRECT - (level, user_id): leading = the common filter
```

### Mistake 3: Indexing low-cardinality columns

```sql
-- WRONG - index on a boolean or a 3-value enum
-- CORRECT - only when the query mix needs it AND selectivity justifies it
```

### Mistake 4: Ignoring write amplification

```sql
-- WRONG - 5 indexes on an event-log table that absorbs 10k inserts/s
-- CORRECT - measure insert latency; keep the indexes that serve queries
```

### Mistake 5: Confusing the plan's existence with its quality

```sql
-- WRONG - "EXPLAIN says SEARCH, done"
-- CORRECT - read which index and whether the predicate used it fully
```

## Best Practices

1. Prove every index with a before/after EXPLAIN.
2. Put the most common filter first in composite indexes.
3. Index selective columns; skip low-cardinality ones.
4. Measure write cost on hot tables.
5. Use covering indexes for hot read queries.
6. Drop unused indexes — each costs writes and storage.
7. Keep index column types matching the query (no implicit casts).
8. Beware functions on indexed columns (`WHERE UPPER(name) = ...` disables the index).
9. Check EXPLAIN after schema changes, not just once.
10. Use `ANALYZE` so the planner has accurate statistics (topic 11).

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Full scan | O(n) | O(1) | index lookup |
| Index equality | O(log n) | O(k) index | covering index removes fetches |
| Index range | O(log n + matches) | O(1) | bounded ranges |
| Insert (k indexes) | O(k log n) | O(k) | fewer indexes on hot tables |
| Composite coverage | O(log n) | composite size | right column order |

The trade is always: read speed vs write cost. Every index is a bet that the
queries it serves run more often than the writes it taxes.

## AI Engineering Relevance

**Where this shows up:** retrieval metadata filters (tenant, date, type),
eval tables keyed by model+dataset, and feature-store lookups — all index
patterns.

| Concept here | Used for |
|---|---|
| Composite indexes | (tenant, date) filtering in retrieval |
| Selectivity | choosing which metadata to index |
| Covering indexes | embedding/hash lookups without table fetches |
| Write cost | ingestion tables that must stay fast to write |
| EXPLAIN proof | verifying plan changes before promoting a migration |

**Scale note:** at 100M rows, an unindexed filter is minutes; a covered index
lookup is microseconds. The EXPLAIN evidence loop is what keeps a schema
fast as it grows — indexes are decisions you revisit, not one-time fixes.

## Practice Exercises

### Exercise 1: Scan to search  (Difficulty: Easy)
Create a table, EXPLAIN a WHERE query (SCAN), add an index, EXPLAIN again
(SEARCH). Assert the plan string changed.

### Exercise 2: Selectivity  (Difficulty: Easy)
On skewed data, show EXPLAIN for a broad and a narrow predicate; assert the
narrow one prefers the index.

### Exercise 3: Composite order  (Difficulty: Medium)
Build (a, b); show a-alone uses it, b-alone does not. Assert via the plan text.

### Exercise 4: Covering index  (Difficulty: Medium)
Show EXPLAIN for a SELECT limited to indexed columns; assert no table fetch
in the plan.

### Exercise 5: Write cost  (Difficulty: Hard)
Benchmark inserts with 0, 1, and 3 indexes; report the ratios (print, never
assert wall-clock).

### Exercise 6: Index repair  (Difficulty: Hard)
Given a slow query and an unused composite index, fix the column order and
prove the plan changed.

## Summary

| Concept | Description |
|---|---|
| B-tree index | sorted copy enabling O(log n) lookup |
| SCAN vs SEARCH | the plan evidence of index usage |
| Selectivity | how much an index narrows the set |
| Composite order | leading column decides coverage |
| Covering index | index answers the query alone |
| Write cost | every index taxes inserts |

Indexes are the difference between a database and a data warehouse disaster.
The discipline: prove with EXPLAIN, order composites by the real query mix,
and pay for each index in writes — knowingly.

## Quick Reference

| Task | Idiom |
|---|---|
| Check the plan | `EXPLAIN QUERY PLAN <sql>` |
| Equality index | `CREATE INDEX i ON t(col)` |
| Composite | `CREATE INDEX i ON t(a, b)` — leading a |
| Covering | index includes every selected column |
| Selectivity check | `SELECT COUNT(DISTINCT col) / COUNT(*) FROM t` |
| Drop unused | `DROP INDEX i` after proving no SEARCH uses it |

## Next Steps

Next: **[11 — Transactions](11-transactions-lecture.md)** — ACID and isolation.

Continues in: **[04-databases — Postgres 04 Indexes](../../04-databases/postgres/lectures/04-indexes-postgres-lecture.md)** — GIN, GiST, and partial indexes beyond B-tree.

Official docs: https://www.sqlite.org/queryplanner.html
