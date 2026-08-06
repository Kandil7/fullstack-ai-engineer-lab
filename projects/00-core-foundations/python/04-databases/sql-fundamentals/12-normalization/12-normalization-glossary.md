# Normalization — Glossary 12

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| 1NF | Normal form | Atomic columns, no repeating groups, a key |
| 2NF | Normal form | 1NF + no partial dependency on part of a composite key |
| 3NF | Normal form | 2NF + no transitive dependency on non-key columns |
| BCNF | Normal form | Every determinant is a candidate key |
| Anomaly | Failure | Update/insert/delete inconsistency from bad design |
| Candidate key | Key | A minimal set of columns uniquely identifying a row |
| Composite key | Key | A key made of two or more columns |
| Denormalization | Design | Deliberately reintroducing redundancy for read speed |
| Determinant | Key | The left-hand side of a functional dependency |
| Functional dependency | Concept | Column B depends on column A: A uniquely determines B |
| Insert anomaly | Anomaly | Cannot store a fact until a related fact exists |
| Partial dependency | Violation | A column depends on part, not all, of a composite key |
| Primary key | Key | The chosen candidate key identifying each row |
| Surrogate key | Key | An artificial key (e.g. auto-increment id) |
| Transitive dependency | Violation | A non-key column depends on another non-key column |
| Update anomaly | Anomaly | A fact stored in many rows must change everywhere |
| Delete anomaly | Anomaly | Deleting one row removes facts about something else |

## Detailed Definitions

### 1NF
**Definition**: First Normal Form — every column holds atomic (indivisible)
values, there are no repeating groups or arrays, and rows have a key.
**Example**:
```sql
-- Violates 1NF: tags is a comma-separated list
CREATE TABLE post (id INT, tags TEXT);
-- 1NF: one tag per row (junction table)
CREATE TABLE post_tag (post_id INT, tag TEXT);
```
**Related**: Anomaly

### 2NF
**Definition**: Second Normal Form — 1NF plus no partial dependency: every
non-key column depends on the *entire* composite key.
**Example**:
```sql
-- Violates 2NF in (order_id, product_id): product_name depends only on product_id
-- Fix: split product into its own table
```
**Related**: Partial dependency

### 3NF
**Definition**: Third Normal Form — 2NF plus no transitive dependency: no
non-key column depends on another non-key column.
**Example**:
```sql
-- Violates 3NF: department_name depends on department_id, a non-key
-- Fix: departments get their own table, referenced by FK
```
**Related**: Transitive dependency

### Anomaly
**Definition**: An inconsistency a bad schema invites — update, insert, or
delete anomalies.
**Related**: Update anomaly

### BCNF
**Definition**: Boyce-Codd Normal Form — every determinant is a candidate
key. Stronger than 3NF for schemas with overlapping candidate keys.
**Related**: 3NF

### Candidate key
**Definition**: A minimal set of columns that uniquely identifies a row; the
primary key is one candidate chosen by the designer.
**Related**: Primary key

### Composite key
**Definition**: A key composed of two or more columns; the target of the
2NF partial-dependency rule.
**Related**: Partial dependency

### Denormalization
**Definition**: Deliberately reintroducing redundancy (e.g. cached counts,
pre-joined columns) to speed reads — the controlled exception to normal
forms.
**Related**: 3NF

### Determinant
**Definition**: The left-hand side of a functional dependency — the column
(set) that determines another.
**Related**: Functional dependency

### Functional dependency
**Definition**: Column set A functionally determines B (A -> B) when every
value of A maps to exactly one value of B.
**Example**:
```text
employee_id -> employee_name    (an id names exactly one person)
```
**Related**: Determinant

### Insert anomaly
**Definition**: Cannot represent a fact until a different fact exists — e.g.
a new department cannot be stored without a dummy employee.
**Related**: Anomaly

### Partial dependency
**Definition**: In a composite key, a non-key column depending on only part
of the key — the 2NF violation.
**Related**: 2NF

### Primary key
**Definition**: The candidate key chosen to identify rows and serve as the
reference target for foreign keys.
**Related**: Candidate key

### Surrogate key
**Definition**: An artificial, meaningless key (auto-increment `id`, UUID)
added so natural data never has to serve as identity.
**Related**: Primary key

### Transitive dependency
**Definition**: A non-key column depending on another non-key column (A -> B,
B -> C) — the 3NF violation.
**Related**: 3NF

### Update anomaly
**Definition**: A fact stored redundantly must be updated in every copy or
the copies drift apart.
**Related**: Anomaly

### Delete anomaly
**Definition**: Deleting a row also deletes unrelated facts that were only
stored alongside it.
**Related**: Anomaly

## Key Concepts Summary

### The normal forms as a ladder
- 1NF: atomic values, no repeating groups.
- 2NF: no partial dependencies (composite keys).
- 3NF: no transitive dependencies.
- BCNF: every determinant a candidate key.

### The anomaly test
- Update anomaly: is a fact stored in more than one row?
- Insert anomaly: can a fact exist only after another exists?
- Delete anomaly: does deleting a row destroy unrelated facts?

### The engineering tradeoff
- Normalize to write-correctness; denormalize deliberately for read
  performance (caches, precomputed aggregates) and document why.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. No partial dependencies — ___
2. A column depending on part of a composite key — ___
3. No transitive dependencies — ___
4. A fact stored in many rows must change everywhere — ___
5. Cannot store a fact until another exists — ___
6. Deliberate redundancy for read speed — ___
7. The chosen unique identifier of a row — ___
8. Column B depends on column A — ___

**Answers:** 1-2NF, 2-partial dependency, 3-3NF, 4-update anomaly,
5-insert anomaly, 6-denormalization, 7-primary key, 8-functional dependency
