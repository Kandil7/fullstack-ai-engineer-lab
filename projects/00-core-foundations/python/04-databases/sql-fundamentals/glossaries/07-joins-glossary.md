# Joins — Glossary 07

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| AS | Alias | Renames tables in FROM for brevity and self-joins |
| CROSS JOIN | Join type | Every pair: A x B, no condition |
| Fan-out | Semantics | Join multiplies rows: 1 parent x 2 children = 2 rows |
| Filter vs condition | Semantics | WHERE drops rows post-join; ON keeps them pre-join |
| FULL OUTER JOIN | Join type | All rows from both sides; missing side NULL (SQLite 3.39+) |
| INNER JOIN | Join type | Only matching pairs |
| Join | Composition | Combining rows from two tables on a condition |
| LEFT JOIN | Join type | All left rows; unmatched right side NULL |
| Multi-join | Composition | Chaining several joins; left-to-right pairing |
| ON clause | Join syntax | The join condition: which rows pair |
| RIGHT JOIN | Join type | All right rows; unmatched left side NULL (SQLite 3.39+) |
| Self-join | Composition | Joining a table to itself; needs AS aliases |
| Unmatched row | Semantics | A side with no pair: NULLs fill the other side |
| USING | Join syntax | Equality on the named shared column(s) |

## Detailed Definitions

### INNER JOIN
**Definition**: Keeps only pairs satisfying the ON condition; rows
without a match vanish on both sides.
**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE a (id INTEGER PRIMARY KEY, v TEXT)")
conn.execute("CREATE TABLE b (aid INTEGER, w TEXT)")
conn.executemany("INSERT INTO a (v) VALUES (?)", [("a1",), ("a2",)])
conn.executemany("INSERT INTO b (aid, w) VALUES (?, ?)", [(1, "b1"), (1, "b2"), (3, "b3")])
print(conn.execute("SELECT a.v, b.w FROM a INNER JOIN b ON a.id = b.aid").fetchall())
```
```text
[('a1', 'b1'), ('a1', 'b2')]
```
**Related**: LEFT JOIN, ON clause

### LEFT JOIN
**Definition**: All left rows survive; missing right matches are padded
with NULLs. The workhorse of optional-relationship queries.
**Example**:
```python
print(conn.execute("SELECT a.v, b.w FROM a LEFT JOIN b ON a.id = b.aid").fetchall())
```
```text
[('a1', 'b1'), ('a1', 'b2'), ('a2', None)]
```
**Related**: INNER JOIN, Unmatched row

### RIGHT / FULL OUTER JOIN
**Definition**: RIGHT keeps all right rows (SQLite 3.39+); FULL keeps
everything from both sides, NULLs where a side has no match.
**Example**:
```python
print(conn.execute("SELECT a.v, b.w FROM a RIGHT JOIN b ON a.id = b.aid").fetchall())
```
```text
[('a1', 'b1'), ('a1', 'b2'), (None, 'b3')]
```
**Related**: LEFT JOIN, Unmatched row

### CROSS JOIN
**Definition**: Every row of A paired with every row of B — n*m rows.
Use deliberately (e.g., day x store grids), not accidentally.
**Related**: Multi-join, INNER JOIN

### AS
**Definition**: Table alias — `FROM a AS x` (AS optional) — required for
self-joins and used to shorten multi-join queries.
**Related**: Self-join, Qualified name

### Fan-out
**Definition**: The row multiplication caused by joining one-to-many
relationships: an aggregate over the joined result double-counts unless
you account for it. Aggregate on the child first, or deduplicate with
DISTINCT.
**Related**: Multi-join, LEFT JOIN

### Filter vs condition
**Definition**: ON is evaluated during pairing — a WHERE on the left
table still keeps left rows with no match; the same condition in ON
changes which pairs exist. Put left-side filters in WHERE, and
right-side filters in ON for LEFT JOINs.
**Related**: LEFT JOIN, ON clause

### Multi-join
**Definition**: Chaining joins: `FROM a JOIN b ON ... JOIN c ON ...`.
Each subsequent join pairs with the accumulated result. With LEFT
joins, a NULL from an earlier join fails later ON conditions.
**Related**: CROSS JOIN, Fan-out

### ON clause
**Definition**: The condition that decides which rows pair: equality of
keys, ranges, or arbitrary expressions.
**Related**: USING, INNER JOIN

### Self-join
**Definition**: A table joined to itself (manager->employee, reply
threads). Requires AS so each side has a name.
**Example**:
```python
conn.execute("CREATE TABLE emp (id INTEGER PRIMARY KEY, name TEXT, mgr INTEGER)")
conn.executemany("INSERT INTO emp (id, name, mgr) VALUES (?, ?, ?)",
                 [(1, "ana", None), (2, "bob", 1), (3, "cam", 1)])
print(conn.execute(
    "SELECT e.name, m.name FROM emp e LEFT JOIN emp m ON e.mgr = m.id ORDER BY e.id").fetchall())
```
```text
[('ana', None), ('bob', 'ana'), ('cam', 'ana')]
```
**Related**: AS, LEFT JOIN

### Unmatched row
**Definition**: A row whose other side has no pair; outer joins fill the
missing side with NULLs. Detect with `WHERE right.id IS NULL`.
**Related**: LEFT JOIN, RIGHT / FULL OUTER JOIN

### USING
**Definition**: Equality join on a shared column name:
`JOIN b USING (id)` — shorthand for `ON a.id = b.id`. Only for
identically named columns.
**Related**: ON clause, INNER JOIN

## Key Concepts Summary

### Join types
- INNER: pairs only.
- LEFT: all left, NULLs right.
- RIGHT: all right, NULLs left (SQLite 3.39+).
- FULL: everything, NULLs both sides (SQLite 3.39+).
- CROSS: every pair.

### Semantics traps
- Fan-out: one-to-many multiplies rows; re-aggregate carefully.
- ON vs WHERE: ON controls pairing, WHERE filters results.
- Multiple LEFT JOINs: earlier NULLs cascade into later conditions.

### Alias discipline
- Self-joins require AS; multi-joins benefit from short aliases.
- Qualify every column in multi-table queries.

## Practice Terms

Match each term to its definition.

1. LEFT JOIN — ___
2. CROSS JOIN — ___
3. Fan-out — ___
4. Self-join — ___
5. ON clause — ___
6. FULL OUTER JOIN — ___
7. USING — ___
8. INNER JOIN — ___

A. Only matching pairs survive
B. All left rows; missing right side NULL
C. Every row of A paired with every row of B
D. All rows both sides; NULLs where unmatched
E. Row multiplication from one-to-many pairing
F. The join condition deciding pairs
G. A table joined to itself
H. Equality join on shared column name

**Answers:** 1-B, 2-C, 3-E, 4-G, 5-F, 6-D, 7-H, 8-A
