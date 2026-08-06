# Indexes and Query Plans — Glossary 10

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| B-tree | Index | The sorted tree structure backing most indexes |
| Composite index | Index | An index over multiple columns, ordered |
| Covering index | Index | An index containing every needed column |
| EXPLAIN QUERY PLAN | Evidence | The command revealing the access plan |
| Full scan | Plan | Reading every row — O(n) |
| Index lookup | Plan | Reading via the tree — O(log n) |
| Leading column | Index | The first column of a composite index |
| Low cardinality | Index | Few distinct values — often not worth indexing |
| O(log n) | Cost | The index lookup complexity |
| Page | Index | The B-tree's fixed-size storage unit |
| Plan | Cost | The engine's chosen access path |
| Range scan | Plan | Sequential reads over a bounded key range |
| SCAN | Plan | The plan token for full scans |
| SEARCH | Plan | The plan token for index lookups |
| Selectivity | Index | How much a predicate narrows the row set |
| Write amplification | Cost | Extra work per write from maintaining indexes |
| Index maintenance | Cost | Updating every index on each write |
| ANALYZE | Tooling | Refreshing planner statistics |

## Detailed Definitions

### B-tree
**Definition**: A balanced, sorted tree of pages where keys are stored in
order; equality lookups descend ~log_f(n) levels.
**Related**: Page, Index lookup

### Composite index
**Definition**: An index over multiple columns, ordered left to right —
`(a, b)` serves predicates on `a` and on `a AND b`, not `b` alone.
**Example**:
```sql
CREATE INDEX idx ON logs(level, user_id)
```
**Related**: Leading column

### Covering index
**Definition**: An index containing every column a query needs, so the engine
answers from the index alone without table fetches.
**Related**: Index lookup

### EXPLAIN QUERY PLAN
**Definition**: The SQLite command printing the access plan — the evidence for
whether an index is used.
**Example**:
```sql
EXPLAIN QUERY PLAN SELECT * FROM logs WHERE user_id = 42
```
**Related**: SCAN, SEARCH

### Full scan
**Definition**: Reading every row of the table — O(n); the plan before a
useful index exists.
**Related**: SCAN

### Index lookup
**Definition**: Finding rows by descending the B-tree — O(log n); the plan
after a useful index exists.
**Related**: SEARCH, B-tree

### Leading column
**Definition**: The first column of a composite index; predicates can use the
index only when the leading column is constrained.
**Related**: Composite index

### Low cardinality
**Definition**: A column with few distinct values (boolean, 3-value enum) —
indexing it rarely narrows the set enough to pay.
**Related**: Selectivity

### O(log n)
**Definition**: The complexity of an index lookup — the number of tree levels
descents, near-constant even at billions of rows.
**Related**: Index lookup

### Page
**Definition**: The fixed-size block in which B-tree keys are stored; the
branching unit of the tree.
**Related**: B-tree

### Plan
**Definition**: The engine's chosen access path for a query — scan, index
search, sort — revealed by EXPLAIN.
**Related**: EXPLAIN QUERY PLAN

### Range scan
**Definition**: Sequential reads over a bounded key range using the index's
sorted order — the structure behind BETWEEN and `>`.
**Related**: Index lookup

### SCAN
**Definition**: The EXPLAIN token for a full table scan — O(n), the sign an
index is missing or unusable.
**Related**: Full scan

### SEARCH
**Definition**: The EXPLAIN token for an index lookup — O(log n), the sign the
index serves the predicate.
**Related**: Index lookup

### Selectivity
**Definition**: The fraction of rows a predicate matches; high selectivity
(1%) makes an index pay, low selectivity (90%) does not.
**Related**: Low cardinality

### Write amplification
**Definition**: The extra per-write work from maintaining indexes — each index
adds an O(log n) update per insert.
**Related**: Index maintenance

### Index maintenance
**Definition**: Updating every index on each INSERT/UPDATE/DELETE — the write
cost of indexes.
**Related**: Write amplification

### ANALYZE
**Definition**: The command refreshing planner statistics so the engine makes
good index decisions.
**Related**: Selectivity

## Key Concepts Summary

### The evidence loop
- EXPLAIN before (SCAN) and after (SEARCH) adding an index.
- Read which index and whether the predicate used it fully.

### Design rules
- Leading column = the most common filter.
- Index selective columns; skip low-cardinality ones.
- Covering indexes answer queries without table fetches.

### The trade
- Indexes speed reads and tax writes.
- Drop unused indexes; measure insert latency on hot tables.
- Revisit index design as query mix and data grow.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The plan token for index lookups — ___
2. The first column of a composite index — ___
3. An index containing every needed column — ___
4. Reading every row — ___
5. The command revealing the access plan — ___
6. How much a predicate narrows the set — ___
7. Extra per-write work from indexes — ___
8. An index over multiple ordered columns — ___

**Answers:** 1-SEARCH, 2-leading column, 3-covering index, 4-full scan,
5-EXPLAIN QUERY PLAN, 6-selectivity, 7-write amplification, 8-composite index
