# SQL Fundamentals — 05: Advanced Filtering

## Topic Overview

Filtering looks like the easiest part of SQL, and it is where the most
silent bugs live. This lecture covers the predicate zoo — `IN`,
`BETWEEN`, `LIKE`, `IS NULL` — boolean logic with `AND`/`OR`/`NOT`, and
the three-valued logic traps that follow from NULL being UNKNOWN.

The headline trap: **`NOT IN` with a NULL in the list matches
nothing**. `x NOT IN (1, NULL)` is `x <> 1 AND x <> NULL`, which is
`TRUE AND UNKNOWN`, which is UNKNOWN — the row is dropped. No error, no
warning, an empty result set that everyone reads as "there is no data".
This exact bug has shipped empty dashboards and empty training sets more
times than any other SQL mistake.

For AI engineers, filtering is the data-quality layer: "predictions
without abstained confidence", "sessions in the beta cohort", "samples
whose label matches a pattern". Getting NULL semantics right is what
keeps evaluation numbers honest.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Filter with IN and BETWEEN, knowing their exact semantics
2. Match patterns with LIKE (`%` and `_`) and explain index impact
3. Test NULLs with IS NULL / IS NOT NULL, never with `=`
4. Combine predicates with AND/OR/NOT, respecting precedence
5. Explain three-valued logic and predict UNKNOWN propagation
6. Avoid the `NOT IN (..., NULL)` empty-result trap
7. Use NOT EXISTS as the NULL-safe alternative
8. Write NULL-safe filters for feature and evaluation queries

## Prerequisites

| Need | Where |
|---|---|
| NULL semantics (NULL is UNKNOWN) | `01-relational-model-lecture.md` |
| WHERE basics | `04-select-basics-lecture.md` |

---

## 1. IN and BETWEEN

`IN` is a set-membership test; `BETWEEN` is inclusive on both ends. The
planner turns both into range/OR lookups. `BETWEEN` is *not* `[a, b)` —
people regularly write `BETWEEN 0 AND 100` expecting 100 excluded.

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL, stock INTEGER)")
conn.executemany(
    "INSERT INTO items (name, category, price, stock) VALUES (?, ?, ?, ?)",
    [
        ("widget", "tools", 9.99, 12),
        ("gadget", "tools", 15.50, 0),
        ("bolt", "hardware", 0.25, 500),
        ("sensor", "electronics", 45.00, None),
        ("cable", "electronics", 3.25, 80),
    ],
)
print([r[0] for r in conn.execute(
    "SELECT name FROM items WHERE category IN (?, ?) ORDER BY id", ("tools", "optics")).fetchall()])
print([r[0] for r in conn.execute(
    "SELECT name FROM items WHERE price BETWEEN ? AND ? ORDER BY id", (1.0, 50.0)).fetchall()])
```

```
['widget', 'gadget']
['widget', 'gadget', 'sensor', 'cable']
```

## 2. LIKE — pattern matching

`%` matches any run of characters, `_` matches exactly one. A **leading
wildcard** (`LIKE '%x'`) cannot use a B-tree index — the engine must
scan (topics 10, 14). Prefer anchored patterns (`'x%'`) where possible.

```python
print([r[0] for r in conn.execute("SELECT name FROM items WHERE name LIKE ? ORDER BY id", ("%et",)).fetchall()])
print([r[0] for r in conn.execute("SELECT name FROM items WHERE name LIKE ? ORDER BY id", ("w_dg_t",)).fetchall()])
```

```
['widget', 'gadget']
['widget']
```

## 3. IS NULL — the only correct NULL test

`= NULL`, `!= NULL`, `IN (NULL)` all yield UNKNOWN and therefore exclude
the row. `IS NULL` / `IS NOT NULL` are the only correct tests. In
feature data, `stock IS NULL` ("no inventory data") is different from
`stock = 0` ("genuinely zero") — collapsing them corrupts statistics.

```python
print([r[0] for r in conn.execute("SELECT name FROM items WHERE stock IS NULL ORDER BY id").fetchall()])
print([r[0] for r in conn.execute("SELECT name FROM items WHERE stock = ? ORDER BY id", (0,)).fetchall()])
```

```
['sensor']
['gadget']
```

## 4. Boolean logic — AND, OR, NOT

`AND` binds tighter than `OR`. `NOT` flips truth — but `NOT UNKNOWN` is
still UNKNOWN. Parenthesize OR groups; the classic bug is
`WHERE a = 1 OR a = 2 AND b = 3` meaning `a = 1 OR (a = 2 AND b = 3)`.

```python
print([r[0] for r in conn.execute(
    "SELECT name FROM items WHERE (category = ? OR category = ?) AND price > ? ORDER BY id",
    ("tools", "electronics", 3.0)).fetchall()])
```

```
['widget', 'gadget', 'sensor', 'cable']
```

## 5. Three-valued logic traps

For a row with `x = 2`, the test `x NOT IN (1, NULL)` is
`(2 <> 1) AND (2 <> NULL)` = `TRUE AND UNKNOWN` = UNKNOWN — the row is
dropped. The whole query returns nothing, silently. NULL also propagates
through arithmetic: `5 + NULL` is NULL.

```python
trap = conn.execute(
    "SELECT name FROM items WHERE category NOT IN (?, ?) AND category IS NOT NULL ORDER BY id",
    ("tools", "electronics")).fetchall()
print([r[0] for r in trap])
print(conn.execute("SELECT 5 + NULL").fetchone()[0])
```

```
['bolt']
None
```

The fix has two shapes: exclude NULLs from the *subject* column
(`AND category IS NOT NULL`), or rewrite with `NOT EXISTS`, which
short-circuits per row and is immune to the trap.

## Common Mistakes to Avoid

### Mistake 1: `= NULL`

```sql
-- WRONG - matches nothing, no error, silent
--   WHERE stock = NULL
-- CORRECT
--   WHERE stock IS NULL
```

### Mistake 2: NOT IN with a NULL in the list

```sql
-- WRONG - the whole query silently returns nothing
--   WHERE category NOT IN ('tools', NULL)
-- CORRECT - exclude NULLs from the subject, or use NOT EXISTS
--   WHERE category NOT IN ('tools', 'electronics') AND category IS NOT NULL
```

### Mistake 3: BETWEEN when you mean half-open

```sql
-- WRONG - BETWEEN is inclusive; 100 is included
--   WHERE x BETWEEN 0 AND 100
-- CORRECT - write the range explicitly when you mean [0, 100)
--   WHERE x >= 0 AND x < 100
```

### Mistake 4: Forgetting precedence

```sql
-- WRONG - means a = 1 OR (a = 2 AND b = 3)
--   WHERE a = 1 OR a = 2 AND b = 3
-- CORRECT
--   WHERE (a = 1 OR a = 2) AND b = 3
```

### Mistake 5: LIKE with a leading wildcard on a hot path

```sql
-- WRONG - cannot use an index; full scan every time
--   WHERE name LIKE '%et'
-- CORRECT - anchored pattern when the semantics allow it
--   WHERE name LIKE 'et%'
```

## Best Practices

1. Use `IS NULL` / `IS NOT NULL` exclusively for NULL tests.
2. Exclude NULLs from the subject before any `NOT IN`.
3. Prefer `NOT EXISTS` over `NOT IN (subquery)` — NULL-safe by design.
4. Parenthesize every OR group; never rely on precedence memory.
5. Write half-open ranges explicitly (`>= a AND < b`).
6. Keep patterns anchored (`prefix%`) to preserve index use.
7. Treat "unknown" and "zero" as different values — do not merge them.
8. When a filter returns nothing, suspect NULLs before suspecting data.
9. Test filters against rows that contain NULLs in every predicate column.
10. Document the NULL policy of each column in the schema (topic 02).

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| IN with k values | O(log n) per value (indexed) | O(k) | join instead of a giant IN list |
| BETWEEN (indexed) | O(log n) | O(1) | — |
| LIKE 'prefix%' (indexed) | O(log n) | O(1) | — |
| LIKE '%suffix' | O(n) scan | O(1) | FTS (topic 07 postgres) or inverted index |
| NOT IN with NULLs | O(n) — and wrong | O(1) | NOT EXISTS — correct and short-circuits |

## AI Engineering Relevance

**Where this shows up:** evaluation filters, feature-store predicates,
cohort queries.

| Concept here | Used for |
|---|---|
| IS NULL | excluding abstained predictions from accuracy |
| NOT IN trap | the empty-dashboard bug in model reporting |
| BETWEEN | latency/score buckets for drift monitoring |
| LIKE | pattern filters on model/label names |
| Boolean logic | compound cohort membership rules |

**Scale note:** at 10M rows a leading-wildcard LIKE is a full scan
(minutes); the same query anchored is milliseconds. And the `NOT IN
(NULL)` trap produces an empty evaluation set — which every downstream
metric reads as "score zero" without a single error message.

## Practice Exercises

### Exercise 1: IN vs BETWEEN  (Difficulty: Easy)

Given an items table, return rows whose category is in a list, then rows
whose price is in an inclusive range. Assert exact row sets.

### Exercise 2: LIKE wildcards  (Difficulty: Easy)

Write queries matching `%et`, `w_dg_t`, and `bolt` with LIKE. Assert
each returns the expected names. Confirm `_` matches exactly one char.

### Exercise 3: IS NULL vs = 0  (Difficulty: Medium)

Build a table where stock can be NULL, 0, or positive. Show that
`stock IS NULL`, `stock = 0`, and `stock IS NOT NULL` partition the rows
into three different sets.

### Exercise 4: The NOT IN trap  (Difficulty: Medium)

Construct a query using `NOT IN` with a NULL in the literal list. Assert
it returns zero rows. Then fix it with an explicit `IS NOT NULL` guard
and assert the correct rows return.

### Exercise 5: NOT EXISTS alternative  (Difficulty: Hard)

Write the NULL-safe version of `WHERE x NOT IN (SELECT v FROM t2)` using
`NOT EXISTS`. Prove both return identical results on data where the
subquery yields NULLs.

### Exercise 6: Compound cohort filter  (Difficulty: Hard)

Design a WHERE clause selecting "sessions from the beta cohort OR the
trial cohort, with latency under 200ms, that did NOT abstain". Build it
with explicit parentheses and NULL guards; assert the result matches a
manual set enumeration.

## Summary

| Concept | Description |
|---|---|
| IN / BETWEEN | set membership; inclusive range |
| LIKE | `%` any run, `_` one char; leading wildcards scan |
| IS NULL | the only NULL test |
| AND/OR/NOT | precedence: AND binds tighter; NOT UNKNOWN = UNKNOWN |
| NOT IN trap | a NULL in the list makes the whole test UNKNOWN |
| NOT EXISTS | NULL-safe membership negation |

Filtering is where NULL semantics earn their keep: one wrong test and a
query silently returns nothing, or worse, returns the *wrong subset*.
The rules are small and final: test NULLs with IS NULL, exclude NULLs
before NOT IN, parenthesize booleans, and remember that UNKNOWN
propagates through everything.

## Quick Reference

| Task | Idiom |
|---|---|
| NULL test | `WHERE col IS NULL` |
| Range | `WHERE price BETWEEN a AND b` (inclusive) |
| Membership | `WHERE cat IN ('a', 'b')` |
| Pattern | `WHERE name LIKE 'prefix%'` |
| Safe exclusion | `WHERE x NOT IN (...) AND x IS NOT NULL` or `NOT EXISTS` |
| Boolean group | `WHERE (a OR b) AND c` |

## Next Steps

Next: **[06 — Aggregation](06-aggregation-lecture.md)** — turning filtered
rows into per-group statistics: COUNT, SUM, AVG, GROUP BY, HAVING.

Continues in: **[Phase 4 — Postgres](../../postgres/07-full-text-search-lecture.md)** —
when LIKE is not enough, real full-text search takes over.

Official docs: https://www.sqlite.org/lang_expr.html
