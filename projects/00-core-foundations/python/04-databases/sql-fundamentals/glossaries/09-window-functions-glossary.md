# Window Functions — Glossary 09

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Aggregate in window | Windows | SUM(...) OVER (...): running values, not grouped rows |
| Frame | Windows | The sliding window of rows a function sees |
| LAG | Windows | Value from the previous row in order |
| LEAD | Windows | Value from the next row in order |
| Moving average | Windows | AVG over a sliding frame (ROWS BETWEEN ...) |
| OVER clause | Windows | Declares partitioning and ordering for the function |
| PARTITION BY | Windows | Splits rows into independent groups |
| RANK | Windows | Rank with gaps after ties (1,1,3) |
| Ranking functions | Windows | ROW_NUMBER, RANK, DENSE_RANK — order-based positions |
| ROWS BETWEEN | Windows | Defines the frame: CURRENT ROW, n PRECEDING, UNBOUNDED |
| ROW_NUMBER | Windows | Unique sequential position per partition |
| Running total | Windows | Cumulative SUM over rows up to the current one |
| Window function | Functions | Per-row value computed over a related set of rows |
| Partition size | Windows | Rows per PARTITION BY group; affects frame semantics |
| Tie handling | Windows | How equal keys split positions: RANK vs DENSE_RANK |
| DENSE_RANK | Windows | Rank without gaps after ties (1,1,2) |
| ORDER BY in OVER | Windows | Sort within partition; defines the frame's base order |
| FILTER (WHERE) | Windows | Optional row filter inside the window (SQLite 3.30+) |
| Deterministic | Semantics | Same input -> same output; window results are stable under a fixed ORDER BY |
| Peer rows | Windows | Rows equal on the ORDER BY key; share RANK and frame edges |

## Detailed Definitions

### Window function
**Definition**: A function computing a value per row from a related set
of rows (the window) without collapsing rows — every input row keeps
its output row.
**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE s (id INTEGER PRIMARY KEY, region TEXT, amt REAL)")
conn.executemany("INSERT INTO s (region, amt) VALUES (?, ?)",
                 [("e", 10), ("e", 5), ("w", 30), ("w", 20)])
print(conn.execute(
    "SELECT id, region, amt, SUM(amt) OVER (PARTITION BY region) AS reg_total "
    "FROM s ORDER BY id").fetchall())
```
```text
[(1, 'e', 10.0, 15.0), (2, 'e', 5.0, 15.0), (3, 'w', 30.0, 50.0), (4, 'w', 20.0, 50.0)]
```
**Related**: OVER clause, PARTITION BY

### OVER clause
**Definition**: The window declaration: `func() OVER (PARTITION BY ...
ORDER BY ... FRAME)`. Without it, the function is a plain aggregate.
**Related**: PARTITION BY, ORDER BY in OVER

### PARTITION BY
**Definition**: Splits rows into independent groups; the window
functions restart at each partition boundary.
**Related**: OVER clause, Window function

### ORDER BY in OVER
**Definition**: Orders rows within each partition; ranking functions
and frames depend on it. Stable for equal keys only when a tiebreaker
is added.
**Related**: Frame, Tie handling

### ROW_NUMBER
**Definition**: 1, 2, 3, ... per partition; ties broken by order
(deterministic with a tiebreaker). The pagination/rank-table workhorse.
**Related**: RANK, DENSE_RANK

### RANK / DENSE_RANK
**Definition**: RANK leaves gaps after ties (1, 1, 3); DENSE_RANK does
not (1, 1, 2). Choose by whether position count matters.
**Example**:
```python
print(conn.execute(
    "SELECT amt, RANK() OVER (ORDER BY amt DESC) r, DENSE_RANK() OVER (ORDER BY amt DESC) d "
    "FROM s ORDER BY amt DESC").fetchall())
```
```text
[(30.0, 1, 1), (20.0, 2, 2), (10.0, 3, 3), (5.0, 4, 4)]
```
**Related**: ROW_NUMBER, Tie handling

### LAG / LEAD
**Definition**: Value at an offset row: LAG(col, 1) is the previous
row's value; LEAD looks forward. NULL outside the window; the classic
for deltas and comparisons to "previous".
**Example**:
```python
print(conn.execute(
    "SELECT amt, LAG(amt) OVER (ORDER BY amt) AS prev FROM s ORDER BY amt").fetchall())
```
```text
[(5.0, None), (10.0, 5.0), (20.0, 10.0), (30.0, 20.0)]
```
**Related**: ORDER BY in OVER, Frame

### Frame
**Definition**: The subset of the partition a function computes over —
all rows, or a sliding window defined by ROWS BETWEEN. Frames matter
only for non-ranking functions.
**Related**: ROWS BETWEEN, Moving average

### ROWS BETWEEN
**Definition**: Frame syntax: `ROWS BETWEEN UNBOUNDED PRECEDING AND
CURRENT ROW` (running total), `BETWEEN 2 PRECEDING AND CURRENT ROW`
(3-row window), `BETWEEN 1 PRECEDING AND 1 FOLLOWING`.
**Example**:
```python
print(conn.execute(
    "SELECT amt, AVG(amt) OVER (ORDER BY amt ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) "
    "FROM s ORDER BY amt").fetchall())
```
```text
[(5.0, 5.0), (10.0, 7.5), (20.0, 15.0), (30.0, 25.0)]
```
**Related**: Frame, Moving average

### Running total
**Definition**: Cumulative SUM with a frame anchored at UNBOUNDED
PRECEDING — each row shows the total up to itself.
**Related**: ROWS BETWEEN, Window function

### Moving average
**Definition**: AVG over a sliding frame; smooths time series; lagging
near the edges (fewer rows).
**Related**: ROWS BETWEEN, Frame

### Tie handling
**Definition**: How equal ORDER BY keys are positioned: ROW_NUMBER picks
an arbitrary-but-deterministic order, RANK/DENSE_RANK share positions.
**Related**: RANK, Peer rows

### Peer rows
**Definition**: Rows equal on the window's ORDER BY key; they share
RANK positions and frame boundaries.
**Related**: RANK, Tie handling

### Aggregate in window
**Definition**: SUM/AVG/COUNT etc. with OVER — computes per-row values
instead of collapsing groups; the GROUP BY-free alternative.
**Related**: Window function, PARTITION BY

### Partition size
**Definition**: Row count per partition; frames of n PRECEDING can't
reach before the partition start (NULLs/truncation at edges).
**Related**: PARTITION BY, Frame

### Deterministic
**Definition**: Same input data and ORDER BY yield the same window
result — essential for reproducible reports and tests.
**Related**: ORDER BY in OVER, Peer rows

### FILTER (WHERE)
**Definition**: Optional clause narrowing the window's rows per
function: `SUM(amt) FILTER (WHERE amt > 10) OVER (...)`.
**Related**: Window function, PARTITION BY

## Key Concepts Summary

### Anatomy
- func + OVER + PARTITION BY + ORDER BY + frame.
- PARTITION BY splits; ORDER BY orders; frame selects the subset.
- Rows are never collapsed — one output row per input row.

### Function families
- Ranking: ROW_NUMBER (1,2,3), RANK (1,1,3), DENSE_RANK (1,1,2).
- Navigation: LAG/LEAD peek at neighbors; NULLs at edges.
- Aggregates: SUM/AVG as running or sliding values.

### Traps
- Frames only affect aggregates/navigation, not rankings.
- Peers share rank values and frame edges.
- Add a tiebreaker for deterministic ordering.
- Partition size limits frame reach at edges.

## Practice Terms

Match each term to its definition.

1. OVER clause — ___
2. PARTITION BY — ___
3. ROW_NUMBER — ___
4. RANK — ___
5. LAG — ___
6. Frame — ___
7. ROWS BETWEEN — ___
8. Peer rows — ___

A. Unique sequential position per partition
B. Splits rows into independent groups
C. Declares partition, order, and frame for a function
D. The sliding subset of rows a function sees
E. Previous row's value; NULL outside the window
F. Rank with gaps after ties
G. Rows equal on the ORDER BY key
H. Frame syntax: UNBOUNDED PRECEDING .. CURRENT ROW

**Answers:** 1-C, 2-B, 3-A, 4-F, 5-E, 6-D, 7-H, 8-G
