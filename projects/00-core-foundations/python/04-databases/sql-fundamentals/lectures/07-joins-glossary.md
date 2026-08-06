# Joins — Glossary 07

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Alias | Join | Short name for a table in a query |
| Cardinality | Join | The number of output rows per key |
| CROSS JOIN | Join | Every row of A paired with every row of B |
| Full outer join | Join | Both sides kept; rows unmatched on either side appear |
| Hash join | Cost | Join via building a lookup of one side |
| INNER JOIN | Join | Rows matching on both sides only |
| Join predicate | Join | The ON condition connecting two tables |
| LEFT JOIN | Join | All left rows, right columns NULL-padded |
| Many-to-many | Cardinality | Both sides may have multiple matches per key |
| Multi-join | Join | Three or more tables chained with joins |
| Nested-loop join | Cost | Join via scanning one side per row of the other |
| NULL padding | Join | Unmatched right columns filled with NULL in LEFT |
| One-to-many | Cardinality | One left row matching many right rows |
| RIGHT JOIN | Join | All right rows; left columns NULL-padded |
| Row explosion | Failure | Output rows multiplied by a non-unique join key |
| Self join | Join | A table joined to itself via two aliases |
| ON condition | Join | The equality/condition defining matches |
| 1-to-1 | Cardinality | Each key matches at most once on both sides |

## Detailed Definitions

### Alias
**Definition**: A short name given to a table (`users u`) so columns read
`u.name` and self-joins can distinguish the two copies.
**Example**:
```sql
SELECT u.name, m.name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id
```
**Related**: Self join

### Cardinality
**Definition**: The number of output rows each join key produces — 1, many, or
zero — determined by the multiplicity of matches on the other side.
**Related**: Row explosion

### CROSS JOIN
**Definition**: A join with no predicate pairing every row of A with every row
of B — the Cartesian product.
**Example**:
```sql
SELECT * FROM users CROSS JOIN teams   -- 3 x 3 = 9 rows
```
**Complexity**: O(n x m).
**Related**: Join predicate

### Full outer join
**Definition**: A join keeping both sides; rows unmatched on either side appear
NULL-padded. Often emulated as LEFT UNION RIGHT.
**Related**: LEFT JOIN, RIGHT JOIN

### Hash join
**Definition**: A join strategy building a hash lookup of one side then
probing with the other — O(n + m) with O(min(n, m)) space.
**Related**: Nested-loop join

### INNER JOIN
**Definition**: Returns rows matching on both sides; unmatched rows on either
side are dropped.
**Example**:
```sql
SELECT * FROM users u INNER JOIN orders o ON o.user_id = u.id
```
**Related**: LEFT JOIN

### Join predicate
**Definition**: The ON condition that defines which rows match — omitted, it
becomes an accidental CROSS JOIN.
**Related**: ON condition

### LEFT JOIN
**Definition**: Keeps every row of the left table; unmatched right columns are
NULL-padded.
**Example**:
```sql
SELECT u.name, o.amount FROM users u LEFT JOIN orders o ON o.user_id = u.id
```
**Related**: INNER JOIN, NULL padding

### Many-to-many
**Definition**: A relationship where each key may match multiple rows on both
sides — the highest row-multiplication risk.
**Related**: Cardinality

### Multi-join
**Definition**: A query joining three or more tables; each join's output feeds
the next.
**Related**: Join predicate

### Nested-loop join
**Definition**: A join scanning one side for every row of the other —
O(n x m); the fallback when no index supports the predicate.
**Related**: Hash join

### NULL padding
**Definition**: The NULL values filling unmatched right-side columns in a
LEFT join — how "no match" is represented.
**Related**: LEFT JOIN

### One-to-many
**Definition**: A relationship where one left row matches many right rows —
each match appears as its own output row.
**Related**: Cardinality

### RIGHT JOIN
**Definition**: Keeps every row of the right table; left columns NULL-padded.
Emulated in sqlite by swapping the table order of a LEFT join.
**Related**: LEFT JOIN

### Row explosion
**Definition**: Output rows multiplied because the join key was non-unique —
aggregates then double-count, silently corrupting results.
**Related**: Cardinality

### Self join
**Definition**: Joining a table to itself using two aliases — the pattern for
hierarchies (manager/employee, parent/child).
**Related**: Alias

### ON condition
**Definition**: The clause defining join matches — `ON a.id = b.a_id` — the
predicate that separates a join from a product.
**Related**: Join predicate

### 1-to-1
**Definition**: A relationship where each key matches at most once on both
sides — the safest join; counts are preserved.
**Related**: Cardinality

## Key Concepts Summary

### Choose by survival
- INNER drops unmatched; LEFT keeps the left side; RIGHT keeps the right.
- FULL keeps both — emulate as LEFT UNION RIGHT where unsupported.
- The question is always: which rows must survive?

### Predict cardinality
- 1-to-1 preserves counts; 1-to-many multiplies by matches.
- Non-unique keys explode rows — check before aggregating.
- A forgotten ON is an accidental CROSS JOIN.

### Hierarchies
- Self joins with aliases resolve manager/employee, thread/reply.
- LEFT on the self join keeps the top-level rows.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Rows matching on both sides only — ___
2. All left rows, right NULL-padded — ___
3. Every row of A paired with every row of B — ___
4. A table joined to itself via aliases — ___
5. The ON condition connecting tables — ___
6. Output rows multiplied by a non-unique key — ___
7. Short name for a table in a query — ___
8. The number of output rows per key — ___

**Answers:** 1-INNER JOIN, 2-LEFT JOIN, 3-CROSS JOIN, 4-self join,
5-join predicate, 6-row explosion, 7-alias, 8-cardinality
