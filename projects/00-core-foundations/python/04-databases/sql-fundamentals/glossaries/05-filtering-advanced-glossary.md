# Advanced Filtering — Glossary 05

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| AND | Logic | All conditions must hold |
| BETWEEN | Range | Inclusive range check: a >= x AND a <= y |
| CASE | Logic | Row-level if/then/else producing a value |
| Column ambiguity | Errors | Same column name in two tables; must qualify |
| EXISTS | Subquery | True when the subquery returns any row |
| IN | Membership | Value matches any element of a list or subquery |
| IS NULL | Semantics | The only correct way to test for NULL |
| LIKE | Text | Pattern match with % (any run) and _ (one char) |
| NOT | Logic | Negates a condition |
| NULL-aware | Semantics | Behavior of operators under three-valued logic |
| OR | Logic | At least one condition must hold |
| Pattern | Text | The LIKE template: e.g. 'pre%', '%post' |
| Precedence | Logic | AND binds tighter than OR; parentheses override |
| Qualified name | FROM clause | table.column — disambiguates joins |
| Subquery | Composition | A SELECT nested inside another query |
| Three-valued logic | Semantics | TRUE/FALSE/UNKNOWN; NULL comparisons are UNKNOWN |
| Type affinity | Semantics | SQLite coerces values; '123' can match 123 |
| UNKNOWN | Logic | The result of comparing with NULL |
| WHERE | Query | Row filter applied before projection/grouping |
| % wildcard | Text | Any sequence of characters in a LIKE pattern |

## Detailed Definitions

### AND / OR / NOT
**Definition**: Boolean combinators. AND requires all sides TRUE; OR
requires at least one; NOT flips. AND binds tighter than OR — when in
doubt, parenthesize.
**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v INTEGER)")
conn.executemany("INSERT INTO t (v) VALUES (?)", [(1,), (5,), (9,), (15,)])
print(conn.execute("SELECT id FROM t WHERE v >= 5 AND v <= 10").fetchall())
print(conn.execute("SELECT id FROM t WHERE v < 5 OR v > 10").fetchall())
```
```text
[(2,), (3,)]
[(1,), (4,)]
```
**Related**: Precedence, BETWEEN

### BETWEEN
**Definition**: Inclusive range: `v BETWEEN 5 AND 10` equals `v >= 5 AND
v <= 10`. NULLs never satisfy it.
**Related**: AND, Three-valued logic

### CASE
**Definition**: Row-level branching in a select list: `CASE WHEN cond
THEN val ELSE other END`. NULLs fall through to ELSE.
**Example**:
```python
print(conn.execute(
    "SELECT id, CASE WHEN v < 10 THEN 'low' ELSE 'high' END AS bucket FROM t ORDER BY id").fetchall())
```
```text
[(1, 'low'), (2, 'low'), (3, 'low'), (4, 'high')]
```
**Related**: Expressions, OR

### Column ambiguity
**Definition**: When a join brings two columns with the same name, the
unqualified name is ambiguous — qualify with `t.column`.
**Related**: Qualified name, JOIN (topic 07)

### EXISTS
**Definition**: `WHERE EXISTS (SELECT ...)` — TRUE when the subquery
produces at least one row. The efficient test for "has children".
**Example**:
```python
conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, cust TEXT)")
conn.execute("CREATE TABLE payments (order_id INTEGER, amt REAL)")
conn.execute("INSERT INTO orders (cust) VALUES (?)", ("alice",))
conn.execute("INSERT INTO payments (order_id, amt) VALUES (?, ?)", (1, 9.99))
print(conn.execute(
    "SELECT cust FROM orders o WHERE EXISTS (SELECT 1 FROM payments p WHERE p.order_id = o.id)").fetchall())
```
```text
[('alice',)]
```
**Related**: IN, Subquery

### IN
**Definition**: Membership test: `v IN (1, 2, 3)` or against a subquery.
A row fails when the value is NULL — NULL IN (...) is UNKNOWN.
**Example**:
```python
print(conn.execute("SELECT id FROM t WHERE v IN (5, 9)").fetchall())
```
```text
[(2,), (3,)]
```
**Related**: EXISTS, Subquery

### IS NULL
**Definition**: The only correct NULL test — `v IS NULL`, never
`v = NULL` (which is always UNKNOWN).
**Example**:
```python
conn.execute("CREATE TABLE u (id INTEGER PRIMARY KEY, note TEXT)")
conn.execute("INSERT INTO u (note) VALUES (NULL)")
print(conn.execute("SELECT COUNT(*) FROM u WHERE note = NULL").fetchone()[0])
print(conn.execute("SELECT COUNT(*) FROM u WHERE note IS NULL").fetchone()[0])
```
```text
0
1
```
**Related**: Three-valued logic, UNKNOWN

### LIKE
**Definition**: Text pattern matching: % matches any run of characters,
_ matches exactly one. Case-insensitive for ASCII by default.
**Example**:
```python
print(conn.execute("SELECT id FROM t WHERE CAST(v AS TEXT) LIKE '1%'").fetchall())
```
```text
[(1,), (4,)]
```
**Related**: Pattern, % wildcard

### NULL-aware
**Definition**: Behavior of operators under three-valued logic — every
comparison with NULL yields UNKNOWN, so filters silently drop those
rows unless IS NULL is used explicitly.
**Related**: IS NULL, Three-valued logic

### Precedence
**Definition**: SQL's operator binding: AND before OR. `a OR b AND c`
means `a OR (b AND c)` — parenthesize to control it.
**Related**: AND, OR

### Qualified name
**Definition**: `table.column` — resolves ambiguity in joins and makes
intent explicit.
**Related**: Column ambiguity

### Subquery
**Definition**: A nested SELECT used as a value, a set (IN/EXISTS), or a
derived table (topic 08). Inner queries run per outer row when
correlated.
**Related**: IN, EXISTS

### Three-valued logic
**Definition**: SQL's logic with TRUE/FALSE/UNKNOWN. AND/OR/NOT follow
Kleene tables; WHERE keeps only rows whose condition is TRUE — UNKNOWN
rows are dropped.
**Related**: IS NULL, UNKNOWN

### Type affinity
**Definition**: SQLite compares '123' and 123 as equal (numeric
affinity). In practice: prefer explicit casting for predictable
filters.
**Related**: BETWEEN, LIKE

### UNKNOWN
**Definition**: The truth value of any comparison involving NULL. WHERE
drops UNKNOWN rows; CHECK constraints accept them.
**Related**: IS NULL, Three-valued logic

### WHERE
**Definition**: The row filter of a query — applied to FROM rows before
projection, grouping, and ordering.
**Related**: Subquery, LIKE

### % wildcard
**Definition**: In a LIKE pattern, % matches any sequence of characters
(including none); _ matches exactly one.
**Related**: LIKE, Pattern

## Key Concepts Summary

### Boolean logic
- AND binds tighter than OR; parenthesize.
- NOT flips TRUE/FALSE but leaves UNKNOWN as UNKNOWN.
- BETWEEN is inclusive; prefer explicit ranges for dates.

### NULL handling
- =, <>, BETWEEN, IN all return UNKNOWN on NULL.
- Test with IS NULL / IS NOT NULL only.
- WHERE drops UNKNOWN rows; CASE routes them to ELSE.

### Text and sets
- LIKE with % and _ for patterns; leading wildcards defeat indexes.
- IN for membership; EXISTS for "has children" checks.
- Prefer EXISTS over IN (subquery) when the list may be large.

### Composition
- Subqueries provide values, sets, and existence tests.
- Qualify column names in any multi-table query.

## Practice Terms

Match each term to its definition.

1. BETWEEN — ___
2. EXISTS — ___
3. IS NULL — ___
4. Precedence — ___
5. UNKNOWN — ___
6. LIKE — ___
7. IN — ___
8. Qualified name — ___

A. True when a subquery returns any row
B. The only correct NULL test
C. Inclusive range check
D. The truth value of comparing with NULL
E. AND binds tighter than OR
F. Pattern matching with % and _
G. Membership test against a list or subquery
H. table.column — disambiguates columns

**Answers:** 1-C, 2-A, 3-B, 4-E, 5-D, 6-F, 7-G, 8-H
