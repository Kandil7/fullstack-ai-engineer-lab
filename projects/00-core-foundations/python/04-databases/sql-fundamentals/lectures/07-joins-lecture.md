# SQL Fundamentals — 07: Joins

## Topic Overview

Joins combine rows across tables — the heart of relational data. Every
retrieval system, evaluation store, and analytics pipeline joins: documents to
embeddings, users to sessions, models to experiments. The join TYPE decides
which rows survive (INNER drops unmatched; LEFT keeps the left side and
NULL-pads), and join CARDINALITY decides whether your result set is correct
or silently exploded by a non-unique key.

The two failure modes this topic exists to prevent: **silent row drops** (using
INNER where LEFT was needed) and **row explosion** (joining on a non-unique
key, multiplying rows until every aggregate is wrong).

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write INNER, LEFT, and CROSS joins.
2. Explain what each join type does to unmatched rows.
3. Emulate RIGHT/FULL joins where unsupported.
4. Write self-joins for hierarchies.
5. Chain multiple joins in one query.
6. Predict join cardinality and avoid row explosion.
7. Diagnose silent row drops by checking NULLs.
8. Choose the join type by which rows must survive.

## Prerequisites

| Need | Where |
|---|---|
| SELECT basics | `04-select-basics-lecture.md` |
| WHERE/IS NULL | `05-filtering-advanced-lecture.md` |
| Keys and relations | `01-relational-model-lecture.md` |

---

## 1. INNER JOIN — matched rows only

INNER returns rows that match on BOTH sides. Rows without a match on either
side disappear.

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL)")
conn.executemany("INSERT INTO users (id, name) VALUES (?, ?)", [(1, "ada"), (2, "bob"), (3, "cyn")])
conn.executemany("INSERT INTO orders (id, user_id, amount) VALUES (?, ?, ?)",
                 [(1, 1, 100.0), (2, 1, 50.0), (3, 2, 75.0), (4, None, 25.0)])
rows = conn.execute("""
    SELECT u.name, o.amount
    FROM users u INNER JOIN orders o ON o.user_id = u.id
    ORDER BY o.amount
""").fetchall()
print(rows)
```

```
[('ada', 50.0), ('bob', 75.0), ('ada', 100.0)]
```

`cyn` (no orders) and order 4 (no user) are both gone. If you need them, this
is the wrong join.

## 2. LEFT JOIN — all left rows, NULL-padded

LEFT keeps every row of the left table and fills unmatched right columns with
NULL. It is the default "I must not lose rows" join.

```python
rows = conn.execute("""
    SELECT u.name, o.amount
    FROM users u LEFT JOIN orders o ON o.user_id = u.id
    ORDER BY u.id
""").fetchall()
print(rows)
```

```
[('ada', 100.0), ('ada', 50.0), ('bob', 75.0), ('cyn', None)]
```

`cyn` survives with a NULL amount — exactly the "users with no orders" report.

## 3. RIGHT / FULL joins — emulation

sqlite lacks RIGHT and FULL JOIN. RIGHT is a LEFT with the tables swapped;
FULL is both sides kept (LEFT UNION RIGHT), which most engines express
directly.

```python
rows = conn.execute("""
    SELECT u.name, o.amount
    FROM orders o LEFT JOIN users u ON o.user_id = u.id
    ORDER BY o.id
""").fetchall()
print(rows)
```

```
[('ada', 100.0), ('ada', 50.0), ('bob', 75.0), (None, 25.0)]
```

Order 4's user is NULL — every order shown even without a user.

## 4. Self join — a table joined to itself

Hierarchies (manager/employee, parent/child, reply/thread) are self-joins:
the same table appears twice with different aliases.

```python
conn.execute("CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER)")
conn.executemany("INSERT INTO employees (id, name, manager_id) VALUES (?, ?, ?)",
                 [(1, "ceo", None), (2, "eng1", 1), (3, "eng2", 1), (4, "intern", 2)])
rows = conn.execute("""
    SELECT e.name AS employee, m.name AS manager
    FROM employees e
    LEFT JOIN employees m ON e.manager_id = m.id
    ORDER BY e.id
""").fetchall()
print(rows)
```

```
[('ceo', None), ('eng1', 'ceo'), ('eng2', 'ceo'), ('intern', 'eng1')]
```

Aliases (`e`, `m`) make the two roles readable. LEFT keeps the top of the
hierarchy with a NULL manager.

## 5. Multi-joins — chaining

Three or more tables chain joins left to right. Each join's output feeds the
next; the WHERE and SELECT see the full joined row.

```python
conn.execute("CREATE TABLE teams (id INTEGER PRIMARY KEY, name TEXT, user_id INTEGER)")
conn.executemany("INSERT INTO teams (id, name, user_id) VALUES (?, ?, ?)",
                 [(1, "ml", 1), (2, "backend", 1), (3, "data", 2)])
rows = conn.execute("""
    SELECT u.name, t.name
    FROM users u
    LEFT JOIN orders o ON o.user_id = u.id
    LEFT JOIN teams t ON t.user_id = u.id
    ORDER BY u.id, t.name
""").fetchall()
print(rows)
```

```
[('ada', 'backend'), ('ada', 'ml'), ('bob', 'data'), ('cyn', None)]
```

## 6. Join cardinality — the row-explosion trap

The number of output rows per key = the number of matches on the other side.
Joining users to teams on `user_id` where ada is in 2 teams yields 2 ada rows.
That is correct for a 1-to-many; it is a BUG when you then SUM amounts.

```python
print(conn.execute("SELECT COUNT(*) FROM users u INNER JOIN teams t ON t.user_id = u.id").fetchone()[0])
print(conn.execute("SELECT COUNT(*) FROM users CROSS JOIN teams").fetchone()[0])
```

```
3
9
```

Always predict cardinality before joining: 1-to-1 keeps counts, 1-to-many
multiplies by matches, many-to-many multiplies both ways. If your aggregate
looks too big, suspect the join, not the data.

## 7. CROSS JOIN — the deliberate product

CROSS JOIN pairs every row of A with every row of B — no condition. Used for
generating combinations (all model x dataset cells) and rarely elsewhere;
a forgotten ON condition is an accidental CROSS JOIN.

```python
print(conn.execute("SELECT COUNT(*) FROM users CROSS JOIN teams").fetchone()[0])
```

```
9   # 3 users x 3 teams
```

## Common Mistakes to Avoid

### Mistake 1: INNER where LEFT was needed

```sql
-- WRONG - cyn silently vanishes; nobody sees the drop
--   SELECT u.name, o.amount FROM users u INNER JOIN orders o ON o.user_id = u.id
-- CORRECT - keep every user, NULL for no orders
--   SELECT u.name, o.amount FROM users u LEFT JOIN orders o ON o.user_id = u.id
```

### Mistake 2: Row explosion from a non-unique key

```sql
-- WRONG - one user in 2 teams: SUM(amount) double-counts every order
--   SELECT u.name, SUM(o.amount) FROM users u
--   JOIN teams t ON t.user_id = u.id JOIN orders o ON o.user_id = u.id
-- CORRECT - aggregate before joining to teams, or join unique keys
```

### Mistake 3: Forgetting the ON condition

```sql
-- WRONG - no ON = accidental CROSS JOIN = product cardinality
--   SELECT * FROM users JOIN orders
-- CORRECT - always a join predicate
--   SELECT * FROM users JOIN orders ON orders.user_id = users.id
```

### Mistake 4: Assuming RIGHT/FULL exist everywhere

```sql
-- WRONG - sqlite raises: RIGHT JOIN not supported
-- CORRECT - swap tables for RIGHT; LEFT UNION for FULL
--   SELECT ... FROM orders o LEFT JOIN users u ON o.user_id = u.id
```

### Mistake 5: Not checking for NULL padding

```sql
-- WRONG - a LEFT JOIN with matches everywhere: is it really LEFT?
-- CORRECT - verify with WHERE right_key IS NULL to see the unmatched rows
```

## Best Practices

1. Choose the join type by which rows must survive — LEFT for "don't drop".
2. Always write the ON predicate explicitly.
3. Predict cardinality before joining; verify counts after.
4. Aggregate before joining to many-sided tables.
5. Use aliases for readability, mandatory for self-joins.
6. Check `WHERE right_key IS NULL` to inspect LEFT-padding.
7. Prefer explicit joins over comma-joins.
8. Test joins on small hand-computed data before trusting aggregates.
9. Emulate RIGHT/FULL with swapped LEFT / UNION when needed.
10. Keep join keys indexed (topic 10) — joins scan without them.

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| INNER/LEFT (hash join) | O(n + m) | O(min(n, m)) | index join O(n log m) with a key index |
| Nested-loop join | O(n x m) | O(1) | hash join |
| CROSS JOIN | O(n x m) | O(n x m) | only for tiny sets |
| Self join | same as join | same | same |
| Multi-join | sum of stages | per stage | reduce joins via denormalized columns |

Joins are where database cost lives. Without an index on the join key, every
join is a scan — topic 10 shows the EXPLAIN evidence.

## AI Engineering Relevance

**Where this shows up:** evaluation tables (predictions x labels x models),
retrieval (documents x embeddings x chunks), and usage accounting.

| Concept here | Used for |
|---|---|
| LEFT JOIN | keeping every document even without an embedding row |
| Join cardinality | avoiding double-counted evaluation metrics |
| Self joins | thread/hierarchy structures in conversation logs |
| Multi-joins | predictions x model x dataset rollups |
| INNER vs LEFT | choosing whether unmatched rows matter to the report |

**Scale note:** at 100M-row scale, a join with a missing index is minutes; a
join on a non-unique key is a corrupted dashboard. Cardinality discipline is
what keeps evaluation numbers reproducible.

## Practice Exercises

### Exercise 1: INNER vs LEFT  (Difficulty: Easy)
Build users/orders with an orphan order and a user with no orders. Assert
INNER returns fewer rows than LEFT and explain which rows each drops.

### Exercise 2: Self join  (Difficulty: Easy)
Create a manager hierarchy; write the self-join report and assert every
employee's manager name (NULL for the top).

### Exercise 3: Cardinality prediction  (Difficulty: Medium)
Given a user in 3 teams and 2 orders, predict the row counts of (a) users
JOIN teams, (b) users JOIN orders, (c) both in one query. Assert the counts.

### Exercise 4: Emulated FULL  (Difficulty: Medium)
Implement FULL OUTER as LEFT UNION RIGHT on sqlite and assert both orphan
rows appear.

### Exercise 5: Multi-join report  (Difficulty: Hard)
Join users -> orders -> teams; assert the aggregate SUM equals the sum over
unique orders (expose the double-count bug, then fix by pre-aggregating).

### Exercise 6: Accidental CROSS  (Difficulty: Hard)
Show a forgotten-ON join producing product cardinality; fix it and assert
the corrected count.

## Summary

| Concept | Description |
|---|---|
| INNER JOIN | matched rows on both sides only |
| LEFT JOIN | all left rows, NULL-padded right |
| RIGHT/FULL | emulated by swapped LEFT / UNION |
| Self join | table joined to itself via aliases |
| Multi-join | chained joins, output feeds next |
| Cardinality | output rows per key — predict before joining |
| CROSS JOIN | deliberate product; accidental when ON is forgotten |

Joins are the language of connecting data. The discipline is choosing the type
by which rows must survive and predicting the cardinality before you write the
aggregate.

## Quick Reference

| Task | Idiom |
|---|---|
| Matched only | `FROM a INNER JOIN b ON b.a_id = a.id` |
| Keep all a | `FROM a LEFT JOIN b ON b.a_id = a.id` |
| All orders | `FROM orders o LEFT JOIN users u ON o.user_id = u.id` |
| Hierarchy | `FROM e LEFT JOIN e m ON e.manager_id = m.id` |
| Product | `FROM a CROSS JOIN b` |
| Check drops | `WHERE b.id IS NULL` after LEFT |

## Next Steps

Next: **[08 — Subqueries and CTEs](08-subqueries-ctes-lecture.md)** — nested queries
and WITH blocks.

Continues in: **[10 — Indexes and Plans](10-indexes-and-plans-lecture.md)** — the
index that makes joins fast.

Official docs: https://www.sqlite.org/lang_select.html
