# Query Optimization — Glossary 14

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Sargable predicate | Optimization | Bare column + wrapped value: index usable |
| Projection | Optimization | Selecting only the columns consumed |
| SELECT * | Anti-pattern | Ships every column; defeats covering indexes |
| Keyset pagination | Optimization | WHERE id > last_id ORDER BY id LIMIT n |
| OFFSET pagination | Anti-pattern | LIMIT n OFFSET m; re-reads m rows per page |
| N+1 problem | Anti-pattern | 1 + N queries for N parents' children |
| IN-batching | Optimization | One query for all children via IN list |
| executemany | Optimization | One statement, many parameter sets |
| Query counter | Verification | Counts executed queries to prove structure |
| EXPLAIN QUERY PLAN | Verification | Shows SCAN vs SEARCH vs sort |
| Covering index | Optimization | Index holding every requested column |
| Round trip | Cost | Each execute() crossing the driver boundary |
| Parameter limit | Constraint | Chunk IN lists when too long (e.g., 500-999) |
| Chunking | Optimization | Splitting batches to respect limits |
| Cursor | Pagination | The keyset position marker (last seen id) |
| Plan assertion | Verification | Locking optimization into tests via EXPLAIN |
| B-tree lookup | Cost | O(log n) index search |
| Full scan | Cost | O(n) reading every row |
| Sargability rule | Optimization | Never wrap the column in a function |
| Regression guard | Verification | Tests that fail when an optimization is lost |

## Detailed Definitions

### Sargable predicate
**Definition**: A WHERE shape the index can serve: the column bare, the
value wrapped. `ts >= ?` SEARCHes; `ts / 1000 >= ?` scans.
**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE e (id INTEGER PRIMARY KEY, ts INTEGER)")
conn.execute("CREATE INDEX idx_e_ts ON e(ts)")
conn.executemany("INSERT INTO e (ts) VALUES (?)", [(i,) for i in range(1, 5001)])
print(conn.execute("EXPLAIN QUERY PLAN SELECT * FROM e WHERE ts >= ?", (2500,)).fetchall())
print(conn.execute("EXPLAIN QUERY PLAN SELECT * FROM e WHERE ts / 1000 >= ?", (2,)).fetchall())
```
```text
[(3, 0, 203, 'SEARCH e USING INDEX idx_e_ts (ts>?)')]
[(2, 0, 216, 'SCAN e')]
```
**Related**: EXPLAIN QUERY PLAN, Sargability rule

### Projection / SELECT *
**Definition**: Projection lists only consumed columns — cheaper I/O,
covering-index friendly. SELECT * ships everything; a debug habit,
not a prod habit.
**Related**: Covering index, Full scan

### Keyset pagination
**Definition**: `WHERE id > last_id ORDER BY id LIMIT n` — jumps via the
primary key; O(log n) per page, stable under concurrent inserts.
**Example**:
```python
print(conn.execute(
    "EXPLAIN QUERY PLAN SELECT id FROM e WHERE id > ? ORDER BY id LIMIT ?", (100, 3)).fetchall())
print(conn.execute(
    "EXPLAIN QUERY PLAN SELECT id FROM e ORDER BY id LIMIT ? OFFSET ?", (3, 100)).fetchall())
```
```text
[(4, 0, 196, 'SEARCH e USING INTEGER PRIMARY KEY (rowid>?)')]
[(7, 0, 216, 'SCAN e')]
```
**Related**: OFFSET pagination, Cursor

### OFFSET pagination
**Definition**: `LIMIT n OFFSET m` — discards m rows per page: O(m) work
per page, O(n^2) total; also drifts when rows change between pages.
**Related**: Keyset pagination, Full scan

### N+1 problem
**Definition**: One query for the parents plus one per child — 1 + N
round trips. Fixed by fetching all children in one IN query.
**Related**: IN-batching, Query counter

### IN-batching
**Definition**: `WHERE parent_id IN (?, ?, ...)` with all parent ids —
children arrive in one round trip.
**Related**: N+1 problem, Chunking

### executemany
**Definition**: Runs one statement over many parameter tuples — one
compile, one round trip for the batch; the write-side twin of
IN-batching.
**Related**: IN-batching, Round trip

### Query counter
**Definition**: A wrapper counting execute() calls; assertions like
`count == 2` prove N+1 is gone. Counts beat vibes.
**Related**: N+1 problem, Regression guard

### EXPLAIN QUERY PLAN
**Definition**: The plan inspector: SCAN (full read), SEARCH (index
lookup), USE TEMP B-TREE (sort). Read it before and after every
change.
**Related**: Sargable predicate, Plan assertion

### Covering index
**Definition**: An index containing every projected column — the plan
says USING COVERING INDEX, and the table is never touched.
**Related**: Projection, B-tree lookup

### Round trip
**Definition**: One execute() across the driver boundary; each round
trip carries latency. Batching collapses many round trips into one.
**Related**: N+1 problem, executemany

### Parameter limit
**Definition**: The cap on placeholders per query (SQLite: 999,
modern; older: 32766). Beyond it, chunk the IN list.
**Related**: Chunking, IN-batching

### Chunking
**Definition**: Splitting an IN list or write batch into slices (e.g.,
500 ids) and looping — bounded round trips, respected limits.
**Related**: Parameter limit, IN-batching

### Cursor
**Definition**: The keyset marker — the last-seen id passed to the next
page request; stateless and cheap.
**Related**: Keyset pagination

### Plan assertion
**Definition**: A test asserting the plan contains SEARCH / COVERING /
no TEMP B-TREE — a regression guard that fails when an index is lost.
**Related**: EXPLAIN QUERY PLAN, Regression guard

### B-tree lookup / Full scan
**Definition**: O(log n) index search vs O(n) reading every row — the
two ends of the plan spectrum every optimization pushes toward.
**Related**: EXPLAIN QUERY PLAN, Sargable predicate

### Sargability rule
**Definition**: Never wrap the indexed column in a function or
arithmetic; wrap the value instead. The #1 index-killer is a wrapped
column.
**Related**: Sargable predicate, Full scan

### Regression guard
**Definition**: Tests encoding performance structure (query counts,
plan keywords) so future changes can't silently undo optimizations.
**Related**: Plan assertion, Query counter

## Key Concepts Summary

### The five moves
- Sargable predicates: bare column, wrapped value.
- Projection: select only what you consume.
- Keyset over OFFSET: O(log n) pages.
- IN-batching over N+1: one query for all children.
- executemany over loops: one compile for the batch.

### Verification culture
- EXPLAIN QUERY PLAN for strategy; query counters for structure.
- Plan assertions and count assertions lock optimizations into tests.
- Optimize with counts and plans, never vibes.

### Scale reality
- Every rule compounds: sargable filters turn minutes into
  milliseconds on billion-row tables; batching turns 10,001 queries
  into 2.
- Chunk when placeholders exceed the parameter limit.

## Practice Terms

Match each term to its definition.

1. Sargable predicate — ___
2. Keyset pagination — ___
3. OFFSET pagination — ___
4. N+1 problem — ___
5. IN-batching — ___
6. executemany — ___
7. Covering index — ___
8. Plan assertion — ___

A. Bare column, wrapped value
B. WHERE id > last_id ORDER BY id LIMIT n
C. Re-reads m rows per page
D. 1 + N queries for N parents
E. One query for all children
F. One statement, many parameter sets
G. Index holding every requested column
H. Test asserting SEARCH/COVERING in the plan

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H
