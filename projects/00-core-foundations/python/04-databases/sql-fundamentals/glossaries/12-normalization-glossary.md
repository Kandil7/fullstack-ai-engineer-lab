# Normalization — Glossary 12

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| 1NF | Normal forms | Atomic values: one value per cell, no repeating groups |
| 2NF | Normal forms | 1NF + no partial dependencies on part of a key |
| 3NF | Normal forms | 2NF + no transitive dependencies (non-key -> non-key) |
| Anomaly | Semantics | A bug the schema invites: insert, update, delete |
| Atomic value | 1NF | A cell holds one indivisible value |
| Boyce-Codd (BCNF) | Normal forms | Stronger 3NF: every determinant is a key |
| Data dictionary | Model | The documented schema: tables, columns, constraints |
| Denormalization | Strategy | Deliberately reintroducing redundancy for reads |
| Dimension table | Star schema | The descriptive sides of a star: users, dates, products |
| Fact table | Star schema | The measured center: rows of events, amounts |
| Functional dependency | Theory | A -> B: each A value determines one B value |
| Natural key | Keys | A real-world identifier: email, SSN, code |
| Partial dependency | Theory | A non-key column depends on part of a composite key |
| Repeating group | 1NF | Multiple values in one cell (e.g., CSV in a column) |
| Snowflake schema | Star schema | Fully normalized dimensions |
| Star schema | Modeling | Denormalized dimensions around a fact table |
| Surrogate key | Keys | An engine-generated id with no external meaning |
| Transitive dependency | Theory | A -> B -> C: non-key C depends on non-key B |
| Update anomaly | Semantics | One fact stored in many rows; edits must touch them all |
| FKs as wiring | Keys | Foreign keys connect the normalized pieces |

## Detailed Definitions

### 1NF
**Definition**: Every cell holds one atomic value; no repeating groups.
CSV-in-a-column violates 1NF.
**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
# 1NF violation: comma list of skills in one cell
conn.execute("CREATE TABLE bad (id INTEGER PRIMARY KEY, skills TEXT)")
# 1NF fix: one row per skill
conn.execute("CREATE TABLE good (id INTEGER PRIMARY KEY, person_id INTEGER, skill TEXT)")
print("bad stores 'py,sql'; good stores one skill per row")
```
```text
bad stores 'py,sql'; good stores one skill per row
```
**Related**: Atomic value, Repeating group

### 2NF
**Definition**: 1NF + every non-key column depends on the WHOLE key —
no partial dependencies on part of a composite key.
**Related**: Partial dependency, 3NF

### 3NF
**Definition**: 2NF + no transitive dependencies — a non-key column
must not depend on another non-key column (a -> b -> c).
**Related**: Transitive dependency, BCNF

### Anomaly
**Definition**: A schema-induced bug: update anomalies (same fact in
many rows), insert anomalies (can't add a fact without a dependent),
delete anomalies (deleting a row destroys facts).
**Related**: Update anomaly, Normalization

### Atomic value
**Definition**: A cell holding one indivisible value — the 1NF
requirement; lists, JSON blobs, and CSV strings break it.
**Related**: 1NF, Repeating group

### BCNF
**Definition**: A stronger 3NF: every determinant must be a candidate
key. Rarely needed beyond 3NF for ordinary applications.
**Related**: 3NF, Normalization

### Data dictionary
**Definition**: The documented schema — table names, column names,
types, constraints, and meanings; the contract between schema and
application.
**Related**: FKs as wiring, Surrogate key

### Denormalization
**Definition**: Intentionally re-adding redundancy (or star schemas)
to serve read-heavy workloads; the data pipeline's counter-move after
normalizing writes.
**Related**: Star schema, Anomaly

### Dimension table
**Definition**: The descriptive sides of a star: users, dates,
products — denormalized for fast joins and labels.
**Related**: Fact table, Star schema

### Fact table
**Definition**: The measured center of a star: one row per event with
FKs to dimensions and numeric measures.
**Related**: Dimension table, Star schema

### Functional dependency
**Definition**: A -> B means each A value determines exactly one B
value; the theoretical basis of every normal form.
**Related**: Partial dependency, Transitive dependency

### Natural key
**Definition**: A real-world identifier (email, product code) used as
a key. Meaningful, but mutable and often wide.
**Example**:
```python
conn.execute("CREATE TABLE emp (id INTEGER PRIMARY KEY, email TEXT UNIQUE, dept TEXT)")
conn.execute("INSERT INTO emp (email, dept) VALUES (?, ?)", ("a@x.com", "eng"))
try:
    conn.execute("UPDATE emp SET email = ? WHERE id = ?", ("new@x.com", 1))
    print("email is updatable: natural keys drift")
except sqlite3.IntegrityError:
    print("blocked")
```
```text
email is updatable: natural keys drift
```
**Related**: Surrogate key, FKs as wiring

### Partial dependency
**Definition**: A non-key column determined by only part of a composite
key — the 2NF violation.
**Related**: 2NF, Functional dependency

### Repeating group
**Definition**: Multiple values packed into one cell (CSV, JSON list)
— the classic 1NF violation.
**Related**: 1NF, Atomic value

### Snowflake schema
**Definition**: Star dimensions split into fully normalized tables —
more joins, less redundancy.
**Related**: Star schema, 3NF

### Star schema
**Definition**: One fact table surrounded by denormalized dimension
tables — the standard analytical shape; join-friendly, readable.
**Related**: Fact table, Dimension table

### Surrogate key
**Definition**: An engine-generated integer id with no external
meaning — stable, small, and immutable; the recommended primary key.
**Related**: Natural key, FKs as wiring

### Transitive dependency
**Definition**: a -> b and b -> c (non-key) — the 3NF violation; fix by
splitting the dependent columns into their own table.
**Related**: 3NF, Functional dependency

### Update anomaly
**Definition**: One fact stored in many rows; a single edit must
propagate to all of them or data diverges. Normalization removes it.
**Related**: Anomaly, 3NF

### FKs as wiring
**Definition**: Foreign keys connect normalized tables back together;
JOINs rebuild the original view of the data.
**Related**: Surrogate key, Denormalization

## Key Concepts Summary

### The ladder
- 1NF: atomic cells, no repeating groups.
- 2NF: no partial dependencies on part of a key.
- 3NF: no transitive dependencies.
- BCNF: every determinant is a key (rarely needed beyond 3NF).

### Why normalize
- Kills update/insert/delete anomalies.
- One fact lives in one place.
- Data dictionary + FKs make the wiring explicit.

### When to denormalize
- Analytics: star schemas with denormalized dimensions.
- OLAP reads win; OLTP writes stay normalized.
- Redundancy is a deliberate trade, not an accident.

## Practice Terms

Match each term to its definition.

1. 1NF — ___
2. 2NF — ___
3. 3NF — ___
4. Star schema — ___
5. Surrogate key — ___
6. Transitive dependency — ___
7. Repeating group — ___
8. Update anomaly — ___

A. Atomic values only
B. No partial dependencies
C. No transitive dependencies
D. Fact table + denormalized dimensions
E. Engine-generated id, no external meaning
F. Non-key depends on non-key
G. Many values packed in one cell
H. One fact in many rows; edits diverge

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H
