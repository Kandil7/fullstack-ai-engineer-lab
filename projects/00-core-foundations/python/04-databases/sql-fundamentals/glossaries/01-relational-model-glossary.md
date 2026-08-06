# Relational Model — Glossary 01

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| 1:1 relation | Relations | One row on each side; rare, usually a split table |
| 1:N relation | Relations | One parent row, many child rows |
| Attribute | Model | A named, typed column of a table |
| Bag | Set theory | A multiset: SELECT returns one unless DISTINCT |
| Column | Model | A named, typed attribute shared by all rows |
| Composite key | Keys | A key built from two or more columns |
| Domain | Model | The set of legal values for an attribute |
| Foreign key | Keys | A column referencing another table's primary key |
| IntegrityError | Engine | The exception when a constraint is violated |
| Junction table | Relations | A table expressing an N:M relation |
| N:M relation | Relations | Many-to-many; always through a junction table |
| NULL | Semantics | Unknown/missing; never equal to anything |
| Primary key | Keys | Uniquely identifies a row; enforced unique |
| Relation | Model | The formal name for a table |
| Row | Model | One record; a tuple of attribute values |
| Set | Set theory | A collection of distinct elements |
| Set-oriented | Language | SQL describes whole sets, not row-by-row steps |
| Table | Model | A named collection of rows with fixed columns |
| Tuple | Model | A row as an ordered list of values |
| Three-valued logic | Semantics | TRUE / FALSE / UNKNOWN — NULL comparisons yield UNKNOWN |
| UNIQUE constraint | Keys | No duplicate values; multiple NULLs still allowed |
| Uniqueness | Keys | Engine-enforced property of a key |

## Detailed Definitions

### Attribute
**Definition**: A named, typed column of a table; the smallest unit of
data the model describes. Every row has exactly one value per attribute.
**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
# attributes: id (INTEGER), name (TEXT), age (INTEGER)
print(conn.execute("PRAGMA table_info(t)").fetchall()[1][1])
```
```text
name
```
**Related**: Column, Domain, Table

### Bag
**Definition**: A multiset — a collection where duplicates survive.
A plain SELECT returns a bag; only DISTINCT converts it to a set.
**Example**:
```python
conn.execute("INSERT INTO t (name, age) VALUES (?, ?)", ("a", 1))
conn.execute("INSERT INTO t (name, age) VALUES (?, ?)", ("a", 1))
print(len(conn.execute("SELECT name FROM t").fetchall()))
print(len(conn.execute("SELECT DISTINCT name FROM t").fetchall()))
```
```text
2
1
```
**Complexity**: DISTINCT costs a sort (O(n log n)) or hash (O(n)).
**Related**: Set, Set-oriented

### Column
**Definition**: A named, typed attribute; the vertical dimension of a
table. All rows share the same columns.
**Example**: see Attribute.
**Related**: Attribute, Row

### Composite key
**Definition**: A key made of two or more columns, e.g.
`PRIMARY KEY (post_id, tag_id)`. The combination is unique even when
each column alone is not.
**Example**:
```python
conn.execute("CREATE TABLE pt (post_id INTEGER, tag_id INTEGER, PRIMARY KEY (post_id, tag_id))")
conn.execute("INSERT INTO pt (post_id, tag_id) VALUES (?, ?)", (1, 1))
try:
    conn.execute("INSERT INTO pt (post_id, tag_id) VALUES (?, ?)", (1, 1))
except sqlite3.IntegrityError:
    print("duplicate (post_id, tag_id) rejected")
```
```text
duplicate (post_id, tag_id) rejected
```
**Related**: Primary key, Uniqueness

### Foreign key
**Definition**: A column referencing another table's primary key,
expressing a relation and enforcing referential integrity. sqlite keeps
FK checks off unless `PRAGMA foreign_keys = ON`.
**Example**:
```python
conn.execute("CREATE TABLE parent (id INTEGER PRIMARY KEY)")
conn.execute("CREATE TABLE child (pid INTEGER REFERENCES parent(id))")
conn.execute("PRAGMA foreign_keys = ON")
try:
    conn.execute("INSERT INTO child (pid) VALUES (?)", (99,))
except sqlite3.IntegrityError as exc:
    print(exc)
```
```text
FOREIGN KEY constraint failed
```
**Related**: 1:N relation, Junction table, Primary key

### IntegrityError
**Definition**: The exception sqlite3 raises when a constraint (PK,
UNIQUE, CHECK, NOT NULL, FK) is violated.
**Related**: Primary key, Uniqueness

### Junction table
**Definition**: A table whose only job is to link two tables in an N:M
relation, holding a composite key of both foreign keys.
**Related**: Composite key, N:M relation, Foreign key

### NULL
**Definition**: The marker for unknown/missing. Never equal to
anything — not even to itself — so it is tested only with IS NULL.
**Example**:
```python
print(conn.execute("SELECT NULL = NULL").fetchone()[0])
print(conn.execute("SELECT NULL IS NULL").fetchone()[0])
```
```text
None
1
```
**Related**: Three-valued logic

### Primary key
**Definition**: The column(s) that uniquely identify each row. UNIQUE +
NOT NULL semantics, plus an automatic index.
**Related**: Uniqueness, Composite key, Foreign key

### Relation
**Definition**: The formal relational-model name for a table: a set of
tuples over a fixed set of attributes.
**Related**: Table, Tuple

### Row
**Definition**: One record — a tuple of attribute values. A member of
the table's set (or bag).
**Related**: Column, Tuple, Table

### Set
**Definition**: A collection of distinct elements. SQL queries produce
bags; DISTINCT produces sets.
**Related**: Bag, Set-oriented

### Set-oriented
**Definition**: The property of SQL that you describe which rows you
want, and the engine decides how to find them — the opposite of
imperative, row-by-row programming.
**Related**: Set, Bag

### Table
**Definition**: A named collection of rows with a fixed set of typed
columns; the unit of storage in the relational model.
**Related**: Relation, Row, Column

### Three-valued logic
**Definition**: SQL's logic with three outcomes — TRUE, FALSE, UNKNOWN —
where any comparison with NULL yields UNKNOWN. `NULL OR TRUE` is TRUE;
`NULL AND FALSE` is FALSE; everything else with NULL is UNKNOWN.
**Related**: NULL

### Tuple
**Definition**: A row as an ordered list of values — what `fetchall()`
returns: `(1, 'alice', 30)`.
**Related**: Row, Relation

### UNIQUE constraint
**Definition**: No two rows may hold the same value — except NULL,
because NULLs are never equal to each other.
**Example**:
```python
conn.execute("CREATE TABLE u (token TEXT UNIQUE)")
conn.execute("INSERT INTO u (token) VALUES (NULL)")
conn.execute("INSERT INTO u (token) VALUES (NULL)")  # allowed
print(len(conn.execute("SELECT * FROM u WHERE token IS NULL").fetchall()))
```
```text
2
```
**Related**: Primary key, Uniqueness

### Uniqueness
**Definition**: The engine-enforced property that a key's values never
repeat, making rows addressable and deduplicatable.
**Related**: Primary key, UNIQUE constraint

## Key Concepts Summary

### Table anatomy
- A table is a set of rows over fixed, typed columns.
- Order is never guaranteed without ORDER BY.
- Each row is a tuple of attribute values.

### Keys
- PRIMARY KEY = UNIQUE + NOT NULL + automatic index.
- FOREIGN KEY references a primary key and enforces integrity.
- Composite keys express uniqueness across several columns.
- N:M relations always pass through a junction table.

### NULL semantics
- NULL means unknown, not zero and not empty string.
- Any comparison with NULL is UNKNOWN; `= NULL` never matches.
- Only IS NULL / IS NOT NULL test for NULL.
- UNKNOWN propagates through arithmetic and boolean logic.

### Set thinking
- SELECT returns a bag; DISTINCT produces a set.
- SQL describes whole sets: "which rows satisfy P?" not "for each row...".

## Practice Terms

Match each term to its definition.

1. Table — ___
2. NULL — ___
3. Primary key — ___
4. Foreign key — ___
5. Junction table — ___
6. Bag — ___
7. Three-valued logic — ___
8. Composite key — ___

A. A multiset: duplicates survive SELECT until DISTINCT
B. The marker for unknown; never equal to anything
C. A named collection of rows with fixed typed columns
D. A table linking two tables in an N:M relation
E. A key built from multiple columns
F. Uniquely identifies a row; enforced by the engine
G. A column referencing another table's primary key
H. TRUE/FALSE/UNKNOWN — NULL comparisons yield UNKNOWN

**Answers:** 1-C, 2-B, 3-F, 4-G, 5-D, 6-A, 7-H, 8-E
