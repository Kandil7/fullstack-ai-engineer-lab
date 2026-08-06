# Query Optimization — Glossary 14

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Batching | Technique | One query with an IN-list instead of N round trips |
| Covering index | Index | An index containing every projected column |
| EXPLAIN | Tool | Showing the optimizer's chosen strategy |
| Full scan | Cost | Reading every row because no index applies |
| Index range scan | Cost | Reading only rows inside a bounded key range |
| Keyset pagination | Technique | Continuing from the last seen key, no offset |
| N+1 | Anti-pattern | One query per row after a list query |
| Offset pagination | Technique | Skipping N rows with LIMIT/OFFSET |
| Plan | Concept | The optimizer's execution strategy |
| Projection | Technique | Selecting only the columns a feature needs |
| Sargable | Concept | Search ARGument ABLE: index-usable predicate |
| SELECT * | Anti-pattern | Fetching every column regardless of need |

## Detailed Definitions

### Batching
**Definition**: Replacing N per-row queries with one query taking an `IN`
list, then grouping results in application code.
**Example**:
```python
marks = ",".join("?" for _ in ids)
execute(f"SELECT ... WHERE id IN ({marks})", ids)
```
**Related**: N+1

### Covering index
**Definition**: An index that itself contains every column the query needs,
so the engine never touches the table — the fastest read shape.
**Related**: Projection

### EXPLAIN
**Definition**: The command showing the optimizer's plan — `EXPLAIN QUERY
PLAN` in sqlite, `EXPLAIN ANALYZE` in Postgres (adds counts and timings).
**Related**: Plan

### Full scan
**Definition**: The strategy of reading every row — required when no index
applies to the predicate (e.g. a function wraps the column).
**Related**: Sargable

### Index range scan
**Definition**: Reading only the rows inside a bounded key interval — the
strategy behind sargable `BETWEEN`/`>=`/`<` predicates.
**Related**: Sargable

### Keyset pagination
**Definition**: Pagination via `WHERE id > last_seen ORDER BY id LIMIT n` —
an indexed range scan costing O(page_size), never O(offset).
**Related**: Offset pagination

### N+1
**Definition**: The anti-pattern of one query per row after fetching a
list — 100 rows become 101 round trips.
**Related**: Batching

### Offset pagination
**Definition**: Pagination via `LIMIT n OFFSET m` — correct but re-scans and
discards m rows on every page; degrades on deep pages.
**Related**: Keyset pagination

### Plan
**Definition**: The optimizer's chosen execution strategy — the evidence to
read before and after any optimization.
**Related**: EXPLAIN

### Projection
**Definition**: Selecting only the columns a feature actually uses — enables
covering-index reads and shrinks payloads.
**Related**: SELECT *

### Sargable
**Definition**: Search ARGument ABLE — a predicate keeping the indexed
column bare on one side so the index can be used.
**Example**:
```sql
-- sargable        -- NOT sargable
v >= 10 AND v < 20 -- CAST(v AS TEXT) LIKE '1%'
```
**Related**: Index range scan

### SELECT *
**Definition**: The anti-pattern of fetching every column — defeats
covering-index reads and wastes bandwidth.
**Related**: Projection

## Key Concepts Summary

### The four shapes of a fast query
- Sargable predicate → index range scan.
- Projected columns → covering-index reads.
- Keyset continuation → constant-cost deep pages.
- IN-list batching → one round trip instead of N.

### The verification loop
1. EXPLAIN the plan (scan or index search?).
2. Rewrite the shape (predicate, projection, pagination, batching).
3. EXPLAIN again and time it.
4. Keep the version with the better plan and measured latency.

### The N+1 smell
- A query inside a `for` loop.
- An ORM that fires one SELECT per related object.
- Instrument round trips; if they scale with row count, it is N+1.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Search ARGument ABLE predicate — ___
2. One query per row — ___
3. Continuing from the last seen key — ___
4. Reading every row because no index applies — ___
5. Selecting only needed columns — ___
6. The optimizer's execution strategy — ___
7. One IN-list instead of N queries — ___
8. `LIMIT n OFFSET m` — ___

**Answers:** 1-sargable, 2-N+1, 3-keyset pagination, 4-full scan,
5-projection, 6-plan, 7-batching, 8-offset pagination
