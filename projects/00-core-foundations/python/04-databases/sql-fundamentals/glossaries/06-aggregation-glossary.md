# Aggregation — Glossary 06

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Aggregate function | Functions | Summarizes many rows into one value |
| AVG | Functions | Mean of a group (NULLs skipped) |
| COUNT | Functions | Number of rows (or non-NULL values) |
| COUNT(DISTINCT) | Functions | Number of distinct non-NULL values |
| Group | GROUP BY | The set of rows sharing the same key |
| GROUP BY | Clauses | Collapses rows into groups by key column(s) |
| Grouped columns | Clauses | Columns that may appear in the select list unaggregated |
| HAVING | Clauses | Filters groups after aggregation |
| Literal | Functions | A constant in the select list; fine with GROUP BY |
| MAX / MIN | Functions | Extremes of a group |
| NULL skipping | Functions | Aggregates ignore NULL inputs |
| SELECT * with GROUP BY | Errors | Nonsense: non-grouped columns have no single value |
| SUM | Functions | Total of a group |
| WHERE vs HAVING | Clauses | WHERE filters rows before grouping; HAVING filters groups after |
| COUNT(*) | Functions | Counts rows including NULLs — the group's size |

## Detailed Definitions

### Aggregate function
**Definition**: A function that consumes many rows and emits one value:
COUNT, SUM, AVG, MIN, MAX, and extensions. Applied per group when
GROUP BY is present.
**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE sales (id INTEGER PRIMARY KEY, region TEXT, amt REAL)")
conn.executemany("INSERT INTO sales (region, amt) VALUES (?, ?)",
                 [("east", 10), ("west", 20), ("east", 5), ("west", 30)])
print(conn.execute("SELECT region, COUNT(*) AS n, SUM(amt) AS total FROM sales GROUP BY region").fetchall())
```
```text
[('east', 2, 15.0), ('west', 2, 50.0)]
```
**Related**: GROUP BY, COUNT

### AVG
**Definition**: Arithmetic mean of a group; NULL inputs are skipped.
If every value is NULL, the result is NULL.
**Related**: SUM, MAX / MIN

### COUNT
**Definition**: `COUNT(*)` counts rows (NULLs included); `COUNT(col)`
counts non-NULL values. `COUNT(DISTINCT col)` counts distinct
non-NULL values.
**Example**:
```python
conn.execute("CREATE TABLE u (id INTEGER PRIMARY KEY, tag TEXT)")
conn.executemany("INSERT INTO u (tag) VALUES (?)", [(None,), ("a",), ("a",)])
print(conn.execute("SELECT COUNT(*), COUNT(tag), COUNT(DISTINCT tag) FROM u").fetchone())
```
```text
(3, 2, 1)
```
**Related**: COUNT(DISTINCT), GROUP BY

### GROUP BY
**Definition**: Collapses rows sharing the same key into one group; the
select list may then use aggregates over each group. `GROUP BY 1`
groups by the first select column.
**Example**: see Aggregate function.
**Related**: HAVING, Grouped columns

### Grouped columns
**Definition**: Columns appearing in GROUP BY (or wrapped in aggregates)
are the only columns allowed in the select list without aggregation.
**Related**: GROUP BY, SELECT * with GROUP BY

### HAVING
**Definition**: Filters groups after aggregation — the WHERE for groups.
`HAVING COUNT(*) > 1` keeps only groups with at least two rows.
**Example**:
```python
print(conn.execute(
    "SELECT region, COUNT(*) n FROM sales GROUP BY region HAVING COUNT(*) >= 2").fetchall())
```
```text
[('east', 2), ('west', 2)]
```
**Related**: GROUP BY, WHERE vs HAVING

### MAX / MIN
**Definition**: Extreme values of a group; NULLs skipped.
**Related**: AVG, SUM

### NULL skipping
**Definition**: Aggregates ignore NULL inputs — SUM over (1, NULL, 2)
is 3, not NULL. COUNT(col) also skips NULLs; COUNT(*) does not.
**Related**: COUNT, AVG

### SELECT * with GROUP BY
**Definition**: An error: with groups, non-grouped columns have many
values per group — SQLite raises "misuse of aggregate" or produces
undefined values.
**Related**: Grouped columns, GROUP BY

### SUM
**Definition**: Total of a group; NULLs skipped; empty group -> NULL.
**Related**: AVG, COUNT

### WHERE vs HAVING
**Definition**: WHERE removes rows before grouping; HAVING removes
groups after. Use WHERE for pre-aggregation filters — it reduces work;
use HAVING only for group-level conditions.
**Related**: GROUP BY, HAVING

## Key Concepts Summary

### The pipeline
- WHERE filters rows -> GROUP BY forms groups -> aggregates compute ->
  HAVING filters groups -> ORDER BY sorts.
- Mixing WHERE-only and HAVING-only conditions is the classic
  aggregation bug.

### Aggregate semantics
- COUNT(*): rows, NULLs included; COUNT(col): non-NULL values.
- SUM/AVG/MAX/MIN skip NULLs; empty input -> NULL.
- COUNT(DISTINCT col) for unique values.

### Group rules
- Select list: grouped columns or aggregates only.
- HAVING operates on aggregate results.
- GROUP BY 1 is shorthand for the first select column.

## Practice Terms

Match each term to its definition.

1. HAVING — ___
2. COUNT(*) — ___
3. GROUP BY — ___
4. NULL skipping — ___
5. WHERE — ___
6. Aggregate function — ___
7. Grouped columns — ___
8. COUNT(DISTINCT) — ___

A. Filters groups after aggregation
B. Filters rows before grouping
C. Rows per group, NULLs included
D. Summarizes many rows into one value
E. Distinct non-NULL values per group
F. Collapses rows into groups by key
G. Aggregates ignore NULL inputs
H. Columns allowed unaggregated in the select list

**Answers:** 1-A, 2-C, 3-F, 4-G, 5-B, 6-D, 7-H, 8-E
