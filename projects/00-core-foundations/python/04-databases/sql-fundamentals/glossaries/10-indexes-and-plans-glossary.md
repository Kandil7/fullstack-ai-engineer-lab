# Indexes & Query Plans — Glossary 10

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| B-tree | Structure | Balanced tree: O(log n) lookups and range scans |
| Covering index | Index | Contains every requested column; plan says COVERING |
| Composite index | Index | Multiple columns in one B-tree (equality -> range -> sort) |
| CREATE INDEX | DDL | Builds a B-tree on column(s) |
| EXPLAIN QUERY PLAN | Plans | Shows the engine's strategy (SCAN / SEARCH / sort) |
| Full scan | Plans | Reading every row: the no-index fallback |
| Index lookup | Plans | SEARCH using an index: O(log n) |
| Leading edge | Index | The first column of a composite index; must be constrained |
| Partial index | Index | WHERE-limited index; smaller, faster |
| Planner | Plans | Chooses the strategy from statistics and costs |
| Range predicate | Plans | >, >=, <, <= — can use an index |
| SCAN | Plans | Plan keyword: full table (or index) read |
| SEARCH | Plans | Plan keyword: index-driven lookup |
| Sargability | Index | Predicate shape that lets the index work (bare column) |
| Unused index | Index | Created but never SEARCHed; writes pay, reads gain nothing |
| USE TEMP B-TREE | Plans | A sort is needed; an ordered index avoids it |
| Write amplification | Cost | Every index makes INSERT/UPDATE/DELETE slower |
| Left-prefix | Index | Composite index usable when leading columns are constrained |
| Selectivity | Index | How many rows a predicate keeps; high selectivity -> index wins |
| Statistics | Planner | Table-size metadata the planner uses to estimate costs |

## Detailed Definitions

### B-tree
**Definition**: The balanced tree structure backing SQLite indexes —
lookups, range scans, and ordered iteration in O(log n).
**Related**: CREATE INDEX, Index lookup

### CREATE INDEX
**Definition**: Builds a B-tree on one or more columns. Duplicates of
the data; the engine keeps it updated on every write.
**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, model TEXT, latency REAL)")
conn.execute("CREATE INDEX idx_model ON events(model)")
print(conn.execute("EXPLAIN QUERY PLAN SELECT * FROM events WHERE model = ?", ("m1",)).fetchall())
```
```text
[(3, 0, 203, 'SEARCH events USING INDEX idx_model (model=?)')]
```
**Related**: B-tree, Write amplification

### Composite index
**Definition**: An index on multiple columns. Best order: equality
columns first, then range, then sort column.
**Related**: Leading edge, Left-prefix

### Covering index
**Definition**: An index holding every column the query needs; the plan
says USING COVERING INDEX — reads never touch the table.
**Example**:
```python
conn.execute("CREATE TABLE wide (id INTEGER PRIMARY KEY, a TEXT, b TEXT, payload TEXT)")
conn.execute("CREATE INDEX idx_wide_ab ON wide(a, b)")
conn.execute("INSERT INTO wide (a, b, payload) VALUES ('x', 'y', 'zzz')")
print(conn.execute("EXPLAIN QUERY PLAN SELECT a, b FROM wide WHERE a = ?", ("x",)).fetchall())
print(conn.execute("EXPLAIN QUERY PLAN SELECT * FROM wide WHERE a = ?", ("x",)).fetchall())
```
```text
[(2, 0, 56, 'SEARCH wide USING COVERING INDEX idx_wide_ab (a=?)')]
[(3, 0, 63, 'SEARCH wide USING INDEX idx_wide_ab (a=?)')]
```
**Related**: CREATE INDEX, Full scan

### EXPLAIN QUERY PLAN
**Definition**: The tool that reveals the strategy: SCAN (full read),
SEARCH (index lookup), USE TEMP B-TREE (sort). The first step of any
optimization.
**Related**: SCAN, SEARCH

### Full scan
**Definition**: Reading every row of the table — O(n). Fine for small
tables; the failure mode for big ones without indexes.
**Related**: SCAN, Index lookup

### Index lookup
**Definition**: SEARCH — descending the B-tree in O(log n), often with
a range after the equality.
**Related**: B-tree, Range predicate

### Leading edge
**Definition**: The first column of a composite index; predicates on it
activate the index. Constraining only later columns cannot use it.
**Related**: Composite index, Left-prefix

### Partial index
**Definition**: `CREATE INDEX ... WHERE status = 'active'` — indexes
only matching rows: smaller, cheaper writes, and the planner uses it
for that predicate.
**Related**: CREATE INDEX, Selectivity

### Planner
**Definition**: The component choosing between scan, index search, and
sort using statistics and cost estimates.
**Related**: Statistics, EXPLAIN QUERY PLAN

### Range predicate
**Definition**: >, >=, <, <= (and BETWEEN) — indexes support ranges; the
planner can stop early. LIKE with a trailing wildcard also works.
**Related**: Index lookup, Sargability

### SCAN / SEARCH
**Definition**: Plan keywords: SCAN reads the whole table/index;
SEARCH uses an index to jump to rows. The core vocabulary of plan
reading.
**Related**: EXPLAIN QUERY PLAN, Full scan

### Sargability
**Definition**: A predicate shape that allows index use: the column
bare, the value wrapped. `DATE(ts) = ?` is not sargable; `ts >= ? AND
ts < ?` is.
**Related**: Range predicate, Leading edge

### Unused index
**Definition**: An index the planner never SEARCHes — writes pay, reads
gain nothing. Audit with index-usage queries; drop unused ones.
**Related**: Write amplification, Statistics

### USE TEMP B-TREE
**Definition**: Plan text meaning a sort is required; an index ordered
the same way avoids the temp sort.
**Related**: EXPLAIN QUERY PLAN, Composite index

### Write amplification
**Definition**: Every index is another structure to maintain: inserts,
updates, deletes all slow down with more indexes. Index what queries
need, not what's imaginable.
**Related**: CREATE INDEX, Unused index

### Left-prefix
**Definition**: A composite index serves any query constraining its
leading columns: index (a, b, c) helps `a=?`, `a=? AND b=?`, and
`a=? AND b=? AND c=?`.
**Related**: Composite index, Leading edge

### Selectivity
**Definition**: The fraction of rows a predicate keeps. High
selectivity (few rows) makes an index win; low selectivity (many
rows) may be faster as a scan.
**Related**: Planner, Statistics

### Statistics
**Definition**: The metadata (row counts, etc.) the planner uses to
estimate costs; stale statistics produce bad plans.
**Related**: Planner, Selectivity

## Key Concepts Summary

### Index mechanics
- B-tree on column(s): O(log n) lookups, ordered ranges.
- Composite order: equality -> range -> sort; left-prefix rules.
- Covering indexes serve queries without touching the table.

### Plan vocabulary
- SCAN: full read; SEARCH: index lookup; USE TEMP B-TREE: sort.
- Verify every index with EXPLAIN QUERY PLAN before and after.

### Costs
- Writes pay for every index (write amplification).
- Unused indexes are pure tax — audit and drop.
- High selectivity favors indexes; low selectivity favors scans.

### Predicate shapes
- Sargable: bare column, wrapped value.
- Leading wildcard LIKE and function-wrapped columns kill index use.

## Practice Terms

Match each term to its definition.

1. SCAN — ___
2. SEARCH — ___
3. Covering index — ___
4. Left-prefix — ___
5. Partial index — ___
6. Sargability — ___
7. USE TEMP B-TREE — ___
8. Write amplification — ___

A. Full read of the table
B. Index-driven lookup
C. Holds every requested column
D. Leading columns of a composite index unlock it
E. WHERE-limited index, smaller and faster
F. Bare column, wrapped value — index usable
G. A sort is needed
H. Every index slows writes

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H
