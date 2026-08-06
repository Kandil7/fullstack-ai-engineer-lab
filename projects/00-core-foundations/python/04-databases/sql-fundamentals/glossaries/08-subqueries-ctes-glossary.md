# Subqueries & CTEs — Glossary 08

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| CTE | Composition | WITH clause naming a subquery for reuse |
| Correlated subquery | Subqueries | Inner query referencing the outer row |
| Derived table | Subqueries | A subquery in FROM; needs an alias |
| Materialization | CTE | SQLite materializes the CTE once at first use |
| NOT EXISTS | Subqueries | True when the subquery returns no rows |
| Recursive CTE | CTE | WITH RECURSIVE: a base row plus recursive expansion |
| Scalar subquery | Subqueries | Returns one value; usable in the select list |
| Seed (base case) | CTE | The initial row(s) of a recursive CTE |
| Union step | CTE | Recursive term: UNION ALL with the previous rows |
| Subquery | Composition | A SELECT nested inside another statement |
| Table-valued | CTE | A CTE acting as a table in FROM |
| Termination | CTE | Recursion must converge; missing guard = infinite loop |
| WITH RECURSIVE | CTE | Declares a recursive CTE |
| Anti-join | Semantics | Find rows without a match: NOT EXISTS / NOT IN |
| Chained CTEs | CTE | WITH a AS (...), b AS (... FROM a ...) — sequential steps |
| Depth | CTE | Number of expansion steps until termination |
| LEFT JOIN + IS NULL | Semantics | The join-based alternative to NOT EXISTS |

## Detailed Definitions

### CTE
**Definition**: `WITH name AS (SELECT ...) SELECT ... FROM name` — names
a subquery for readability and reuse within one statement. SQLite
materializes the CTE once at first reference.
**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE sales (region TEXT, amt REAL)")
conn.executemany("INSERT INTO sales (region, amt) VALUES (?, ?)",
                 [("east", 10), ("east", 5), ("west", 30)])
print(conn.execute(
    "WITH totals AS (SELECT region, SUM(amt) AS total FROM sales GROUP BY region) "
    "SELECT * FROM totals WHERE total > 10").fetchall())
```
```text
[('west', 30.0)]
```
**Related**: Derived table, Chained CTEs

### Correlated subquery
**Definition**: An inner query that references the outer row (e.g.,
`p.order_id = o.id`). Re-evaluated per outer row — correct, but watch
the N+1-style cost.
**Example**:
```python
conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, cust TEXT)")
conn.execute("CREATE TABLE payments (order_id INTEGER, amt REAL)")
conn.executemany("INSERT INTO orders (cust) VALUES (?)", [("alice",), ("bob",)])
conn.execute("INSERT INTO payments (order_id, amt) VALUES (?, ?)", (1, 9.99))
print(conn.execute(
    "SELECT cust FROM orders o WHERE EXISTS "
    "(SELECT 1 FROM payments p WHERE p.order_id = o.id)").fetchall())
```
```text
[('alice',)]
```
**Related**: EXISTS, NOT EXISTS

### Derived table
**Definition**: A subquery in the FROM clause — must have an alias:
`FROM (SELECT ...) AS d`. The building block of layered queries.
**Related**: CTE, Subquery

### Materialization
**Definition**: SQLite computes the CTE's result once into an internal
table, then references it — repeated references don't re-run the query.
**Related**: CTE, Chained CTEs

### NOT EXISTS
**Definition**: TRUE when the subquery returns zero rows — the natural
"rows without children" test (anti-join).
**Example**:
```python
print(conn.execute(
    "SELECT cust FROM orders o WHERE NOT EXISTS "
    "(SELECT 1 FROM payments p WHERE p.order_id = o.id)").fetchall())
```
```text
[('bob',)]
```
**Related**: Correlated subquery, Anti-join

### Recursive CTE
**Definition**: `WITH RECURSIVE name(n) AS (seed UNION ALL recursive)` —
starts from the seed and expands until no new rows appear. Tree
traversal, date spines, graph walks.
**Example**:
```python
print(conn.execute(
    "WITH RECURSIVE cnt(x) AS (SELECT 1 UNION ALL SELECT x + 1 FROM cnt WHERE x < 5) "
    "SELECT x FROM cnt").fetchall())
```
```text
[(1,), (2,), (3,), (4,), (5,)]
```
**Related**: Seed (base case), Termination

### Scalar subquery
**Definition**: A subquery returning exactly one value; usable in the
select list: `SELECT (SELECT MAX(amt) FROM sales) AS max_amt`.
**Related**: Subquery, Correlated subquery

### Seed (base case)
**Definition**: The first SELECT of a recursive CTE — the rows that
start the recursion (e.g., depth 1, root nodes).
**Related**: Recursive CTE, Union step

### Subquery
**Definition**: A SELECT nested inside another statement — as a value
(scalar), a set (IN/EXISTS), or a table (FROM).
**Related**: Derived table, CTE

### Termination
**Definition**: Recursive CTEs must converge. Missing or wrong
termination (WHERE on the recursion) means unbounded growth or an
infinite loop. Test with small data first.
**Related**: Recursive CTE, Seed (base case)

### Anti-join
**Definition**: Finding rows with no match: NOT EXISTS, NOT IN, or
LEFT JOIN + IS NULL. Watch NULLs: NOT IN with a NULL in the list
matches nothing.
**Related**: NOT EXISTS, LEFT JOIN + IS NULL

### Chained CTEs
**Definition**: Multiple WITH clauses building stepwise:
`WITH a AS (...), b AS (SELECT ... FROM a)` — pipeline each stage.
**Related**: CTE, Materialization

### Union step
**Definition**: The recursive term: `SELECT ... FROM name WHERE ...`
combined with UNION ALL to the seed.
**Related**: Recursive CTE, Termination

### LEFT JOIN + IS NULL
**Definition**: `FROM a LEFT JOIN b ON ... WHERE b.id IS NULL` — the
join-based anti-join, equivalent to NOT EXISTS.
**Related**: Anti-join, NOT EXISTS

## Key Concepts Summary

### Kinds of subqueries
- Scalar: one value in the select list.
- Set: IN / NOT IN membership.
- Existence: EXISTS / NOT EXISTS.
- Derived table: a subquery in FROM (must alias).

### CTEs
- WITH names a subquery; materialized once.
- Chained CTEs build pipelines; recursive CTEs walk trees/spines.
- Recursion: seed + UNION ALL + terminating condition.

### Anti-join semantics
- NOT EXISTS is the clearest "has no children".
- LEFT JOIN + IS NULL is the join form.
- NOT IN is dangerous with NULLs in the list.

## Practice Terms

Match each term to its definition.

1. Recursive CTE — ___
2. Correlated subquery — ___
3. Derived table — ___
4. Materialization — ___
5. Seed — ___
6. NOT EXISTS — ___
7. Scalar subquery — ___
8. Anti-join — ___

A. Subquery in FROM; must be aliased
B. Inner query referencing the outer row
C. CTE computed once, then reused
D. Returns one value for the select list
E. Base rows starting the recursion
F. True when the subquery returns nothing
G. Seed + UNION ALL until termination
H. Finding rows without a match

**Answers:** 1-G, 2-B, 3-A, 4-C, 5-E, 6-F, 7-D, 8-H
