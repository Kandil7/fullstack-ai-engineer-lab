# Window Functions — Glossary 09

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| DENSE_RANK | Ranking | Rank without gaps after ties |
| Frame | Window | The subset of rows the function sees relative to current |
| GROUP BY | Contrast | Collapses rows; the opposite of window semantics |
| LAG | Window | The previous row's value in window order |
| LEAD | Window | The next row's value in window order |
| Moving average | Frame | Rolling mean over a bounded frame |
| OVER | Window | The keyword introducing the window clause |
| PARTITION BY | Window | Per-group window isolation |
| RANK | Ranking | Rank with gaps after ties |
| ROW_NUMBER | Ranking | Unique sequential number, no ties |
| Running total | Window | Cumulative sum from partition start to current row |
| Window | Concept | The ordered, partitioned row set a function sees |
| Window function | Concept | Aggregate/ranking computed per row over a window |
| Window order | Window | The ORDER BY inside OVER defining sequence |
| ROWS BETWEEN | Frame | The frame-bounding syntax |
| Tie | Ranking | Equal sort values sharing a rank position |

## Detailed Definitions

### DENSE_RANK
**Definition**: Assigns ranks with no gaps after ties — tied rows share a
number and the next row gets the next consecutive number.
**Example**:
```sql
DENSE_RANK() OVER (ORDER BY score DESC)   -- 1, 1, 2
```
**Related**: RANK, Tie

### Frame
**Definition**: The subset of window rows a function computes over, relative to
the current row — `ROWS BETWEEN 1 PRECEDING AND CURRENT ROW`.
**Example**:
```sql
AVG(m) OVER (ORDER BY day ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)
```
**Related**: ROWS BETWEEN, Moving average

### GROUP BY
**Definition**: The clause that collapses rows into groups — the opposite
semantics of window functions, which keep every row and add a column.
**Related**: Window function

### LAG
**Definition**: A window function returning the value from the previous row in
window order; NULL at the start.
**Example**:
```sql
LAG(score) OVER (ORDER BY id)
```
**Related**: LEAD

### LEAD
**Definition**: A window function returning the value from the next row in
window order; NULL at the end.
**Related**: LAG

### Moving average
**Definition**: The average over a bounded frame, e.g. the last k rows — the
smoothing statistic behind trend analysis.
**Related**: Frame

### OVER
**Definition**: The SQL keyword that turns an aggregate into a window function
by attaching the window definition.
**Example**:
```sql
SUM(v) OVER (PARTITION BY g ORDER BY id)
```
**Related**: PARTITION BY

### PARTITION BY
**Definition**: The window clause dividing rows into independent groups; each
partition restarts the function.
**Related**: OVER

### RANK
**Definition**: Assigns ranks with gaps after ties — 1, 1, 3 for two tied
leaders.
**Example**:
```sql
RANK() OVER (ORDER BY score DESC)
```
**Related**: DENSE_RANK, Tie

### ROW_NUMBER
**Definition**: Assigns a unique sequential number within the window — ties
get arbitrary distinct numbers.
**Related**: RANK, Tie

### Running total
**Definition**: A cumulative sum from the partition start to the current row,
produced by `SUM(v) OVER (ORDER BY ...)` without a frame.
**Related**: Window function

### Window
**Definition**: The ordered, partitioned set of rows visible to a window
function at each current row.
**Related**: OVER

### Window function
**Definition**: A function computing a value per row over its window — ranking,
lagging, or aggregating — while keeping every row.
**Related**: Window

### Window order
**Definition**: The ORDER BY inside OVER that defines sequence within the
window — distinct from the outer query's ORDER BY.
**Related**: OVER

### ROWS BETWEEN
**Definition**: The frame syntax bounding the window — e.g.
`BETWEEN 1 PRECEDING AND CURRENT ROW`.
**Related**: Frame

### Tie
**Definition**: Equal sort values within a window; ROW_NUMBER breaks them
arbitrarily, RANK and DENSE_RANK share them.
**Related**: RANK

## Key Concepts Summary

### The three window parts
- Function: ROW_NUMBER / RANK / SUM / LAG / ...
- OVER: the window keyword.
- Definition: PARTITION BY (groups), ORDER BY (sequence), frame (bounds).

### The tie menu
- ROW_NUMBER: unique numbers, ties broken arbitrarily.
- RANK: shared ranks with gaps.
- DENSE_RANK: shared ranks, no gaps.

### Semantics
- Windows keep every row; GROUP BY collapses.
- Over ORDER BY defines the window; outer ORDER BY sorts output.
- Frames bound moving averages; no frame = cumulative.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Rank with gaps after ties — ___
2. Rank without gaps — ___
3. Unique sequential number — ___
4. The previous row's value — ___
5. Per-group window isolation — ___
6. The frame syntax bounding rows — ___
7. The keyword introducing windows — ___
8. Cumulative sum from partition start — ___

**Answers:** 1-RANK, 2-DENSE_RANK, 3-ROW_NUMBER, 4-LAG, 5-PARTITION BY,
6-ROWS BETWEEN, 7-OVER, 8-running total
