# Subqueries and CTEs — Glossary 08

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Anchor | Recursive CTE | The base SELECT that seeds the recursion |
| Correlated subquery | Subquery | A subquery referencing the outer row; runs per row |
| CTE | Structure | A named query step (`WITH name AS (...)`) |
| Derived table | Subquery | A subquery used as a table in FROM |
| EXISTS | Membership | Tests whether at least one matching row exists |
| IN subquery | Membership | Tests set membership against a subquery result |
| NOT EXISTS | Membership | The NULL-safe complement of NOT IN |
| NOT IN | Membership | Membership complement — breaks on NULLs |
| Recursive CTE | Structure | anchor + UNION ALL self-reference walking trees |
| Scalar subquery | Subquery | A subquery returning exactly one value |
| Table subquery | Subquery | A subquery returning many rows used as a table |
| Three-valued logic | Semantics | SQL's TRUE/FALSE/NULL truth system |
| UNION ALL | Recursive CTE | The operator joining anchor and recursive steps |
| WITH | Structure | The keyword introducing CTEs |
| WITH RECURSIVE | Structure | The keyword for recursive CTEs |
| Pre-aggregation | Pattern | Aggregating inside a subquery before joining |

## Detailed Definitions

### Anchor
**Definition**: The first SELECT of a recursive CTE — the roots that seed the
recursion; without it, infinite recursion.
**Example**:
```sql
SELECT id, 0 AS depth FROM employees WHERE manager_id IS NULL
```
**Related**: Recursive CTE

### Correlated subquery
**Definition**: A subquery that references the outer query's row, executed
once per outer row — O(n x m) without an index.
**Example**:
```sql
SELECT u.name, (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) FROM users u
```
**Related**: Derived table

### CTE
**Definition**: A Common Table Expression — a named subquery introduced with
WITH, reusable and readable across later steps.
**Example**:
```sql
WITH totals AS (SELECT user_id, SUM(amount) s FROM orders GROUP BY user_id)
SELECT * FROM totals
```
**Related**: WITH

### Derived table
**Definition**: A subquery placed in FROM, producing a table you can join
against.
**Example**:
```sql
FROM (SELECT g, SUM(v) s FROM t GROUP BY g) x
```
**Related**: Table subquery

### EXISTS
**Definition**: A predicate testing whether at least one row satisfies a
correlated condition; short-circuits on the first match.
**Example**:
```sql
WHERE EXISTS (SELECT 1 FROM p WHERE p.a_id = a.id)
```
**Related**: NOT EXISTS

### IN subquery
**Definition**: Tests whether a value is a member of a subquery's result set.
**Related**: NOT IN

### NOT EXISTS
**Definition**: The complement of EXISTS — returns true when no matching row
exists; NULL-safe because it does not compare values.
**Related**: EXISTS

### NOT IN
**Definition**: The complement of IN — but if the subquery result contains a
NULL, the whole predicate returns nothing (three-valued logic).
**Related**: IN subquery, Three-valued logic

### Recursive CTE
**Definition**: A CTE with an anchor and a self-referencing recursive SELECT
joined by UNION ALL — walks trees and hierarchies.
**Example**:
```sql
WITH RECURSIVE t AS (
  SELECT id, 0 AS d FROM e WHERE mgr IS NULL
  UNION ALL
  SELECT e.id, t.d + 1 FROM e JOIN t ON e.mgr = t.id
)
SELECT * FROM t
```
**Related**: Anchor, UNION ALL

### Scalar subquery
**Definition**: A subquery returning exactly one value, usable anywhere a
value can appear.
**Related**: Subquery

### Table subquery
**Definition**: A subquery returning a result set used as a table in FROM.
**Related**: Derived table

### Three-valued logic
**Definition**: SQL's truth system with TRUE, FALSE, and NULL — where
`x NOT IN (NULL)` and `NULL = NULL` are neither true nor false.
**Related**: NOT IN

### UNION ALL
**Definition**: The operator combining the anchor and recursive SELECTs of a
recursive CTE without deduplication.
**Related**: Recursive CTE

### WITH
**Definition**: The keyword introducing CTEs before the main SELECT.
**Related**: CTE

### WITH RECURSIVE
**Definition**: The keyword form enabling self-referencing CTEs.
**Related**: Recursive CTE

### Pre-aggregation
**Definition**: Aggregating inside a subquery/CTE before joining, preventing
row-explosion double-counts (topic 07).
**Related**: Derived table

## Key Concepts Summary

### The nesting menu
- Scalar: one value inline.
- Table/derived: many rows in FROM.
- IN/EXISTS: membership.

### The cost trap
- Correlated subqueries run per outer row — O(n x m).
- Rewrite as JOIN + GROUP BY for one pass.
- Pre-aggregate before joining to avoid explosion.

### The NULL trap
- NOT IN breaks when the set contains NULL.
- NOT EXISTS is the safe complement.
- Recursive CTEs need an anchor + UNION ALL.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. A subquery referencing the outer row — ___
2. The anchor + UNION ALL tree walker — ___
3. The NULL-safe complement of NOT IN — ___
4. A named query step — ___
5. The base SELECT seeding recursion — ___
6. A subquery used as a table in FROM — ___
7. Breaks on NULLs in the set — ___
8. A subquery returning exactly one value — ___

**Answers:** 1-correlated subquery, 2-recursive CTE, 3-NOT EXISTS, 4-CTE,
5-anchor, 6-derived table, 7-NOT IN, 8-scalar subquery
