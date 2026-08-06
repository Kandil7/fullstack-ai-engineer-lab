# DDL & Schema — Glossary 02

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| ALTER TABLE | DDL | Modifies an existing table (ADD/DROP COLUMN, RENAME) |
| AUTOINCREMENT | DDL | INTEGER PRIMARY KEY with a never-reuse counter |
| CHECK | Constraint | Row-level rule verified on every insert/update |
| CREATE INDEX | DDL | Builds a B-tree for fast lookups |
| CREATE TABLE | DDL | Defines a new table and its schema |
| CASCADE | FK option | Parent delete/update propagates to children |
| Constraints | Schema | Rules the engine enforces: PK, FK, UNIQUE, CHECK, NOT NULL |
| DEFAULT | Schema | The value inserted when a column is omitted |
| DROP TABLE | DDL | Deletes a table and its data permanently |
| FK action | FK option | ON DELETE / ON UPDATE behavior: CASCADE, SET NULL, RESTRICT |
| Generated column | Schema | A column computed from other columns (e.g., ts->date) |
| INTEGER PRIMARY KEY | DDL | Rowid alias: fast integer IDs |
| NOT NULL | Constraint | Column must never hold NULL |
| ON DELETE CASCADE | FK option | Deleting a parent deletes its children |
| PRAGMA foreign_keys | Engine | Switch that turns FK enforcement on/off (off by default in sqlite) |
| RESTRICT | FK option | Refuse the parent change if children exist |
| RETURNS clause | DDL | Not SQLite syntax; SQL Server-style output columns |
| ROWID | Engine | SQLite's hidden integer row identifier |
| Schema | Model | The complete structural definition of a database |
| SET NULL | FK option | Parent delete/update nulls the child's FK column |
| Strict table | DDL | STRICT mode: enforces declared types at write time |
| Type affinity | Engine | SQLite's permissive type handling; STRICT tables disable it |

## Detailed Definitions

### ALTER TABLE
**Definition**: DDL for evolving a table — add/drop columns, rename
columns (recent SQLite), rename tables. Dropping a column is supported
in SQLite 3.35+.
**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
conn.execute("ALTER TABLE t ADD COLUMN age INTEGER")
print(conn.execute("PRAGMA table_info(t)").fetchall())
```
```text
[(0, 'id', 'INTEGER', 0, None, 1), (1, 'name', 'TEXT', 0, None, 0), (2, 'age', 'INTEGER', 0, None, 0)]
```
**Related**: CREATE TABLE, Schema

### AUTOINCREMENT
**Definition**: Makes INTEGER PRIMARY KEY use a monotonically increasing
counter that is never reused, even after deletes. SQLite guarantees
`max(rowid)+1` anyway; AUTOINCREMENT only prevents reuse.
**Related**: INTEGER PRIMARY KEY, ROWID

### CHECK
**Definition**: A row-level constraint evaluated on every INSERT/UPDATE;
rejects the write when the expression is FALSE. NULL results pass.
**Example**:
```python
conn.execute("CREATE TABLE sensor (id INTEGER PRIMARY KEY, v REAL CHECK (v BETWEEN -100 AND 100))")
try:
    conn.execute("INSERT INTO sensor (v) VALUES (?)", (1000,))
except sqlite3.IntegrityError as exc:
    print(exc)
```
```text
CHECK constraint failed: v BETWEEN -100 AND 100
```
**Related**: NOT NULL, Constraints

### CREATE TABLE
**Definition**: DDL statement defining a table's columns, types,
constraints, and indexes — the primary schema-building tool.
**Related**: ALTER TABLE, Schema

### CASCADE
**Definition**: An FK action where deleting (or updating the key of) a
parent automatically deletes (or updates) the children.
**Related**: FK action, RESTRICT, SET NULL

### DEFAULT
**Definition**: The value a column receives when INSERT omits it; can be
a literal or an expression such as CURRENT_TIMESTAMP.
**Related**: Constraints, NOT NULL

### DROP TABLE
**Definition**: Permanently removes a table, its data, and its indexes.
There is no undo — always back up before dropping.
**Related**: CREATE TABLE

### FK action
**Definition**: The ON DELETE / ON UPDATE behavior of a foreign key:
CASCADE (propagate), SET NULL (null the child column), RESTRICT
(block the parent change), NO ACTION (defer), SET DEFAULT.
**Related**: CASCADE, RESTRICT, SET NULL

### Generated column
**Definition**: A column computed from other columns, stored or virtual;
keeps derived values consistent without application code.
**Example**:
```python
conn.execute("CREATE TABLE log (id INTEGER PRIMARY KEY, ts INTEGER, day TEXT GENERATED ALWAYS AS (date(ts, 'unixepoch')) STORED)")
conn.execute("INSERT INTO log (ts) VALUES (?)", (1750000000,))
print(conn.execute("SELECT day FROM log").fetchone()[0])
```
```text
2025-06-15
```
**Related**: Schema

### INTEGER PRIMARY KEY
**Definition**: An alias for the hidden ROWID column — integer IDs are
fast, auto-assigned, and unique. Only INTEGER PRIMARY KEY gets this
optimization.
**Related**: ROWID, AUTOINCREMENT

### NOT NULL
**Definition**: A constraint forbidding NULL in the column; every row
must provide a real value.
**Related**: CHECK, DEFAULT

### ON DELETE CASCADE
**Definition**: `FOREIGN KEY (pid) REFERENCES parent(id) ON DELETE CASCADE`
— deleting a parent row deletes all its children. Typical for child
records with no standalone meaning.
**Related**: CASCADE, FK action

### PRAGMA foreign_keys
**Definition**: The switch controlling FK enforcement in SQLite — OFF by
default. Must be set outside a transaction (`isolation_level=None`) to
take effect mid-session.
**Example**:
```python
conn2 = sqlite3.connect(":memory:", isolation_level=None)
conn2.execute("CREATE TABLE p (id INTEGER PRIMARY KEY)")
conn2.execute("CREATE TABLE c (pid INTEGER REFERENCES p(id))")
conn2.execute("PRAGMA foreign_keys = ON")
try:
    conn2.execute("INSERT INTO c (pid) VALUES (?)", (1,))
except sqlite3.IntegrityError:
    print("orphan rejected")
```
```text
orphan rejected
```
**Related**: Constraints, FK action

### RESTRICT
**Definition**: An FK action that blocks a parent delete/update while
matching children exist.
**Related**: FK action, CASCADE, SET NULL

### ROWID
**Definition**: SQLite's hidden 64-bit integer row identifier; the
backing of INTEGER PRIMARY KEY and the fastest lookup key.
**Related**: INTEGER PRIMARY KEY, AUTOINCREMENT

### Schema
**Definition**: The complete structural definition of a database: tables,
columns, types, constraints, and indexes. In SQLite, a "schema" can also
mean a named namespace (e.g., `main`).
**Related**: CREATE TABLE, ALTER TABLE

### SET NULL
**Definition**: An FK action that sets the child's FK column to NULL when
the parent is deleted — keeps the child row but unlinks it.
**Related**: FK action, CASCADE, RESTRICT

### STRICT table
**Definition**: `CREATE TABLE ... STRICT` enforces declared column types
at write time (rejects 'abc' into INTEGER), disabling SQLite's
permissive affinity behavior.
**Related**: Type affinity

### Type affinity
**Definition**: SQLite's rule that a value is coerced toward a column's
declared type but not hard-rejected. STRICT tables opt out.
**Related**: STRICT table

## Key Concepts Summary

### Building blocks
- CREATE TABLE defines columns, types, and constraints in one place.
- ALTER TABLE evolves it: ADD/DROP COLUMN, RENAME.
- DROP TABLE is permanent — no undo.

### Constraint families
- NOT NULL — column must have a value.
- UNIQUE — no duplicate values (NULLs exempt).
- CHECK — row-level rule; FALSE rejects the write.
- PRIMARY KEY — UNIQUE + NOT NULL + auto index (INTEGER = rowid alias).
- FOREIGN KEY — references another table; enforcement is opt-in via
  PRAGMA foreign_keys = ON.

### FK actions
- CASCADE — propagate the parent change to children.
- SET NULL — unlink children by nulling their FK.
- RESTRICT — block the parent change while children exist.

### SQLite specifics
- INTEGER PRIMARY KEY aliases the hidden ROWID.
- AUTOINCREMENT prevents id reuse, at a small cost.
- Type affinity is permissive; STRICT tables enforce types.
- Generated columns keep derived values consistent.

## Practice Terms

Match each term to its definition.

1. CHECK — ___
2. ROWID — ___
3. CASCADE — ___
4. STRICT table — ___
5. INTEGER PRIMARY KEY — ___
6. PRAGMA foreign_keys — ___
7. Generated column — ___
8. Type affinity — ___

A. Hidden integer row identifier backing integer keys
B. Row-level rule; FALSE rejects the write
C. Computed from other columns; kept consistent by the engine
D. Enforced type checking; no affinity coercion
E. Parent delete propagates to children
F. Alias for ROWID; fast auto-incrementing IDs
G. The switch enabling FK enforcement (off by default)
H. SQLite's permissive type coercion toward the declared type

**Answers:** 1-B, 2-A, 3-E, 4-D, 5-F, 6-G, 7-C, 8-H
