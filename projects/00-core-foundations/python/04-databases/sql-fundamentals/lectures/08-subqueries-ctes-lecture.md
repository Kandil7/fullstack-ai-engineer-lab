# SQL Fundamentals — 08: Subqueries and CTEs

## Topic Overview

Subqueries are queries inside queries — one value, a row, or a whole table
produced inline. They power the "users with more than N orders", "top model
per dataset", and "documents above average relevance" patterns that every
evaluation and retrieval system needs. CTEs (`WITH`) lift subqueries into
named, reusable steps, turning unreadable nesting into readable pipelines; a
recursive CTE walks trees and hierarchies that ordinary SQL cannot touch.

The performance story matters as much as the syntax: **correlated subqueries
execute once per row**, which without an index is O(n x m) — the classic
"why is my query slow" answer. The discipline is knowing when to nest and when
to JOIN/GROUP BY instead.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write scalar, table, and IN subqueries.
2. Explain how correlated subqueries execute (per row).
3. Replace correlated subqueries with joins where appropriate.
4. Structure multi-step queries with CTEs.
5. Write a recursive CTE for tree traversal.
6. Explain the NOT IN / NULL trap and use NOT EXISTS.
7. Name the readability win of CTEs over nesting.
8. Predict the cost of a subquery before running it.

## Prerequisites

| Need | Where |
|---|---|
| SELECT / WHERE | `04-select-basics-lecture.md` |
| Aggregation / GROUP BY | `06-aggregation-lecture.md` |
| Joins | `07-joins-lecture.md` |
| NULL semantics | `05-filtering-advanced-lecture.md` |

---

## 1. Scalar subqueries — one value inline

A subquery returning a single value can appear anywhere a value can — in
SELECT, WHERE, or HAVING.

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, amount REAL)")
conn.executemany("INSERT INTO orders (id, amount) VALUES (?, ?)", [(1, 100.0), (2, 50.0), (3, 75.0)])
print(conn.execute("SELECT (SELECT AVG(amount) FROM orders) AS avg_order").fetchone()[0])
```

```
75.0
```

## 2. Table subqueries in FROM — query a query

A subquery in FROM is a derived table — you can join against it. The pattern
that prevents row explosion: pre-aggregate inside the subquery, then join.

```python
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
conn.executemany("INSERT INTO users (id, name) VALUES (?, ?)", [(1, "ada"), (2, "bob"), (3, "cyn")])
conn.executemany("INSERT INTO orders (id, user_id, amount) VALUES (?, ?, ?)",
                 [(1, 1, 100.0), (2, 1, 50.0), (3, 2, 75.0)])
rows = conn.execute("""
    SELECT u.name, t.total
    FROM users u
    LEFT JOIN (SELECT user_id, SUM(amount) AS total FROM orders GROUP BY user_id) t
      ON t.user_id = u.id
    ORDER BY u.id
""").fetchall()
print(rows)
```

```
[('ada', 150.0), ('bob', 75.0), ('cyn', None)]
```

## 3. IN / NOT IN — membership tests

```python
rows = conn.execute("""
    SELECT name FROM users
    WHERE id IN (SELECT user_id FROM orders WHERE amount > 60)
    ORDER BY name
""").fetchall()
print(rows)
```

```
[('ada',)]
```

## 4. Correlated subqueries — the per-row trap

A correlated subquery references the outer row, so the engine runs it **once
for every outer row**.

```python
rows = conn.execute("""
    SELECT u.name, (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) AS n
    FROM users u ORDER BY u.id
""").fetchall()
print(rows)
```

```
[('ada', 2), ('bob', 1), ('cyn', 0)]
```

Correct but costly: 3 users x a scan of orders per user. Without an index on
orders.user_id this is O(n x m). The JOIN + GROUP BY version does the same work
in one pass:

```python
rows = conn.execute("""
    SELECT u.name, COUNT(o.id) AS n
    FROM users u LEFT JOIN orders o ON o.user_id = u.id
    GROUP BY u.id, u.name ORDER BY u.id
""").fetchall()
print(rows)
```

```
[('ada', 2), ('bob', 1), ('cyn', 0)]
```

## 5. CTEs — named query steps

`WITH name AS (subquery) SELECT ...` names a step and lets later steps reference
it — the readability win over nested subqueries, and the same step can be
referenced multiple times.

```python
rows = conn.execute("""
    WITH user_totals AS (
        SELECT user_id, SUM(amount) AS total FROM orders GROUP BY user_id
    )
    SELECT u.name, COALESCE(ut.total, 0) AS total
    FROM users u LEFT JOIN user_totals ut ON ut.user_id = u.id
    ORDER BY u.id
""").fetchall()
print(rows)
```

```
[('ada', 150.0), ('bob', 75.0), ('cyn', 0)]
```

## 6. Recursive CTEs — walking trees

A recursive CTE has an anchor (the roots) and a recursive part that references
itself — walking one level per iteration.

```python
conn.execute("CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER)")
conn.executemany("INSERT INTO employees (id, name, manager_id) VALUES (?, ?, ?)",
                 [(1, "ceo", None), (2, "eng", 1), (3, "intern", 2), (4, "junior", 2)])
rows = conn.execute("""
    WITH RECURSIVE team AS (
        SELECT id, name, manager_id, 0 AS depth
        FROM employees WHERE manager_id IS NULL
        UNION ALL
        SELECT e.id, e.name, e.manager_id, t.depth + 1
        FROM employees e JOIN team t ON e.manager_id = t.id
    )
    SELECT name, depth FROM team ORDER BY depth, name
""").fetchall()
print(rows)
```

```
[('ceo', 0), ('eng', 1), ('intern', 2), ('junior', 2)]
```

The `UNION ALL` with an anchor and a self-referencing SELECT is the whole
mechanism — without the anchor, infinite recursion.

## 7. NOT IN vs NOT EXISTS — the NULL trap

`NOT IN (SELECT ...)` with a NULL anywhere in the subquery result returns NO
rows — three-valued logic: `x NOT IN (NULL)` is never true.

```python
conn.execute("CREATE TABLE p (id INTEGER PRIMARY KEY, a_id INTEGER)")
conn.executemany("INSERT INTO p (id, a_id) VALUES (?, ?)", [(1, 1), (2, None)])
print(conn.execute("SELECT COUNT(*) FROM users WHERE id NOT IN (SELECT a_id FROM p)").fetchone()[0])
print(conn.execute("SELECT COUNT(*) FROM users WHERE NOT EXISTS (SELECT 1 FROM p WHERE p.a_id = users.id)").fetchone()[0])
```

```
0        # NOT IN: the NULL poisons the whole set
2        # NOT EXISTS: NULL row safely ignored
```

When the subquery can contain NULLs, prefer `NOT EXISTS`.

## Common Mistakes to Avoid

### Mistake 1: Correlated subqueries in hot paths

```sql
-- WRONG - runs per outer row: O(n x m) without an index
--   SELECT u.name, (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) FROM users u
-- CORRECT - one pass
--   SELECT u.name, COUNT(o.id) FROM users u LEFT JOIN orders o ON o.user_id = u.id GROUP BY u.id
```

### Mistake 2: NOT IN with NULLs

```sql
-- WRONG - returns nothing when the subquery has a NULL
--   ... WHERE id NOT IN (SELECT a_id FROM p)
-- CORRECT
--   ... WHERE NOT EXISTS (SELECT 1 FROM p WHERE p.a_id = a.id)
```

### Mistake 3: Recursive CTE without an anchor

```sql
-- WRONG - infinite recursion: no base case
--   WITH RECURSIVE t AS (SELECT ... UNION ALL SELECT ... FROM e JOIN t ...)
-- CORRECT - anchor first (the roots), then UNION ALL the recursive step
```

### Mistake 4: Deep nesting instead of CTEs

```sql
-- WRONG - SELECT (SELECT ... (SELECT ...)) becomes unreadable
-- CORRECT - WITH step1 AS (...), step2 AS (...) SELECT ...
```

### Mistake 5: Aggregating after a join instead of before

```sql
-- WRONG - SUM over exploded rows double-counts (see 07-joins)
-- CORRECT - pre-aggregate in a subquery/CTE, then join
```

## Best Practices

1. Use CTEs for any query with more than one logical step.
2. Prefer JOIN + GROUP BY over correlated subqueries in loops.
3. Use NOT EXISTS when the subquery can contain NULLs.
4. Name CTEs for what they compute — they are the query's documentation.
5. Anchor recursive CTEs; always bound the recursion depth.
6. Use table subqueries to pre-aggregate before joining (anti-explosion).
7. Test scalar subqueries return exactly one value (or use LIMIT 1).
8. Explain queries before and after rewriting to confirm the plan changes.
9. Prefer EXISTS over IN when only existence matters.
10. Keep recursive CTEs on indexed keys for sane performance.

## Complexity and Cost

| Pattern | Time | Space | Cheaper alternative |
|---|---|---|---|
| Scalar subquery | O(subquery) | O(1) | computed once |
| IN subquery | O(subquery + probe) | O(set) | EXISTS short-circuits |
| Correlated subquery | O(n x m) per row | O(1) | JOIN + GROUP BY: O(n + m) |
| CTE | O(sum of steps) | per step | same; readability win |
| Recursive CTE | O(nodes x edges) | O(depth) | indexed keys help |

The correlated subquery is the one to fear — its cost multiplies by the outer
row count.

## AI Engineering Relevance

**Where this shows up:** ranking queries, cohort filters ("users with > N
events"), evaluation aggregations, and tree-shaped structures in conversation
and document hierarchies.

| Concept here | Used for |
|---|---|
| Table subqueries | pre-aggregating eval metrics before joining |
| IN subqueries | filtering documents by a retrieved ID set |
| CTEs | multi-step feature pipelines with named stages |
| Recursive CTEs | walking document section or thread trees |
| NOT EXISTS | safe cohort filtering with NULLable keys |

**Scale note:** at 100M rows, a correlated subquery is a production incident
and a CTE pipeline is a batch job. The same query shape that was fine at 10k
rows becomes the thing you rewrite at 10M.

## Practice Exercises

### Exercise 1: Scalar subquery  (Difficulty: Easy)
Return the row(s) above the table average using a scalar subquery in WHERE.
Assert the result set.

### Exercise 2: Pre-aggregate then join  (Difficulty: Easy)
Produce per-user totals with a FROM subquery, then LEFT JOIN. Assert no row
explosion (each user appears once).

### Exercise 3: Correlated rewrite  (Difficulty: Medium)
Write the per-user order count both ways — correlated subquery and JOIN +
GROUP BY. Assert identical results and count the difference in rows scanned.

### Exercise 4: NOT IN vs NOT EXISTS  (Difficulty: Medium)
Build a table with NULL keys; assert NOT IN returns nothing and NOT EXISTS
returns the correct set.

### Exercise 5: CTE pipeline  (Difficulty: Hard)
Write a 3-step WITH: filter, aggregate, rank. Assert the final ranking.

### Exercise 6: Recursive tree  (Difficulty: Hard)
Build a 3-level hierarchy; write a recursive CTE with a depth column and
assert level ordering.

## Summary

| Concept | Description |
|---|---|
| Scalar subquery | one value inline |
| Table subquery | derived table in FROM — pre-aggregate before join |
| IN / NOT IN | membership |
| Correlated subquery | runs per row — O(n x m) trap |
| CTE | named, reusable query steps |
| Recursive CTE | anchor + UNION ALL self-reference walks trees |
| NOT EXISTS | the NULL-safe membership complement |

Subqueries and CTEs are how SQL composes. The professional discipline is
readability (CTEs over nesting), correctness (NOT EXISTS over NOT IN), and
cost (joins over correlated subqueries).

## Quick Reference

| Task | Idiom |
|---|---|
| One value | `(SELECT AVG(v) FROM t)` inline |
| Pre-aggregate | `FROM (SELECT g, SUM(v) s FROM t GROUP BY g) x` |
| Membership | `WHERE id IN (SELECT ...)` |
| Safe complement | `WHERE NOT EXISTS (SELECT 1 FROM p WHERE p.a_id = a.id)` |
| Named step | `WITH totals AS (SELECT ...) SELECT ... FROM totals` |
| Tree walk | `WITH RECURSIVE t AS (anchor UNION ALL SELECT ... JOIN t)` |

## Next Steps

Next: **[09 — Window Functions](09-window-functions-lecture.md)** — ranking, running
totals, and per-group rows without GROUP BY collapse.

Continues in: **[04-databases — SQLAlchemy](../../04-databases/sqlalchemy/lectures/05-querying-2.0-lecture.md)** — the same ideas in the ORM.

Official docs: https://www.sqlite.org/lang_with.html
