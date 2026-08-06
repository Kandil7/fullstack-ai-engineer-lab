# DML: INSERT / UPDATE / DELETE — Glossary 03

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| DELETE | DML | Removes rows matching a WHERE clause |
| executemany | Driver | Run one statement with many parameter sets |
| idempotent | Semantics | Safe to re-run; produces the same end state |
| INSERT | DML | Adds one or more rows |
| INSERT ... DEFAULT | DML | Inserts using every column's default |
| INSERT ... SELECT | DML | Fills a table from a query |
| lastrowid | Driver | The id of the last inserted row on the connection |
| Named parameters | Driver | `:name` placeholders bound by name, not position |
| ON CONFLICT DO NOTHING | DML | Skip a row that violates UNIQUE/PRIMARY KEY |
| ON CONFLICT DO UPDATE | DML | Upsert: update the existing row instead of failing |
| RETURNING | DML | Returns inserted/deleted rows directly from the DML |
| rowcount | Driver | Number of rows affected by the last statement |
| Transactions | DML | A unit of work: all statements commit or none do |
| UPDATE | DML | Modifies matching rows' columns |
| UPSERT | DML | INSERT that falls back to UPDATE on conflict |
| WHERE clause | DML | Filters which rows a DML statement affects |
| ? placeholders | Driver | Positional parameter binding; never string interpolation |
| CRUD | Model | Create, Read, Update, Delete — the four data operations |
| Prepared statement | Driver | SQL compiled once, executed many times |
| Sanitized | Security | Values made safe via parameters, never concatenation |

## Detailed Definitions

### DELETE
**Definition**: Removes rows matching a WHERE clause. Omit the WHERE to
delete the whole table — almost never what you want.
**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT)")
conn.executemany("INSERT INTO t (v) VALUES (?)", [("a",), ("b",), ("c",)])
cur = conn.execute("DELETE FROM t WHERE v = ?", ("b",))
print(cur.rowcount, conn.execute("SELECT COUNT(*) FROM t").fetchone()[0])
```
```text
1 2
```
**Related**: UPDATE, INSERT, WHERE clause

### executemany
**Definition**: Executes one statement repeatedly over a sequence of
parameter tuples — one compile, many executions. The standard way to
insert batches.
**Example**: see DELETE.
**Related**: Prepared statement, UPSERT

### idempotent
**Definition**: An operation that leaves the same end state no matter how
many times it runs — e.g., `UPDATE ... SET v = 'x' WHERE id = ?` is
idempotent; `INSERT` without dedup is not. Matters for retries.
**Related**: ON CONFLICT DO NOTHING, Transactions

### INSERT
**Definition**: Adds rows to a table: `INSERT INTO t (cols) VALUES (?)`.
Values must satisfy every constraint or the engine raises
IntegrityError.
**Related**: DELETE, UPDATE, RETURNING

### INSERT ... DEFAULT
**Definition**: `INSERT INTO t DEFAULT VALUES` inserts one row using all
column defaults.
**Related**: INSERT, UPSERT

### INSERT ... SELECT
**Definition**: Fills a table from a query result — the bulk-load form of
INSERT.
**Example**:
```python
conn.execute("CREATE TABLE t2 (id INTEGER PRIMARY KEY, v TEXT)")
conn.execute("INSERT INTO t2 (v) SELECT v FROM t WHERE v >= ?", ("b",))
print(conn.execute("SELECT COUNT(*) FROM t2").fetchone()[0])
```
```text
2
```
**Related**: INSERT, executemany

### lastrowid
**Definition**: `cursor.lastrowid` — the id of the most recent inserted
row. The reliable way to get back the generated key.
**Related**: RETURNING, rowcount

### Named parameters
**Definition**: `:name` placeholders bound by keyword instead of
position: `execute("INSERT INTO t (v) VALUES (:v)", {"v": "x"})`.
Improves readability for many-column statements.
**Related**: ? placeholders, Prepared statement

### ON CONFLICT DO NOTHING
**Definition**: Insert that silently skips rows violating a UNIQUE or
PRIMARY KEY constraint instead of raising. Making an insert idempotent.
**Example**:
```python
conn.execute("CREATE TABLE uniq (id INTEGER PRIMARY KEY, v TEXT)")
conn.execute("INSERT INTO uniq (id, v) VALUES (?, ?) ON CONFLICT DO NOTHING", (1, "x"))
conn.execute("INSERT INTO uniq (id, v) VALUES (?, ?) ON CONFLICT DO NOTHING", (1, "y"))
print(conn.execute("SELECT COUNT(*) FROM uniq").fetchone()[0])
```
```text
1
```
**Related**: UPSERT, ON CONFLICT DO UPDATE

### ON CONFLICT DO UPDATE
**Definition**: The upsert fallback: when a row conflicts, update it
instead. `... ON CONFLICT(id) DO UPDATE SET v = excluded.v` — the
`excluded` table holds the values that were about to be inserted.
**Related**: UPSERT, ON CONFLICT DO NOTHING

### RETURNING
**Definition**: SQLite 3.35+ lets DML return rows: `INSERT ... RETURNING
id, v` — the row is visible in a single round trip, no second SELECT.
**Example**:
```python
row = conn.execute("INSERT INTO t (v) VALUES (?) RETURNING id, v", ("d",)).fetchone()
print(row)
```
```text
(4, 'd')
```
**Related**: lastrowid, INSERT

### rowcount
**Definition**: `cursor.rowcount` — how many rows the last statement
affected. Critical for asserting "exactly one row changed".
**Related**: DELETE, UPDATE

### Transactions
**Definition**: A unit of work with ACID guarantees; SQLite wraps each
statement in a transaction automatically unless isolation_level=None
(autocommit). All statements commit, or none do.
**Related**: ON CONFLICT DO NOTHING, idempotent

### UPDATE
**Definition**: Changes columns on all rows matching the WHERE clause.
`SET` a column to a bare expression (never string-built SQL).
**Related**: DELETE, INSERT, WHERE clause

### UPSERT
**Definition**: The combination INSERT ... ON CONFLICT DO UPDATE: try the
insert, upgrade to an update on conflict. The standard way to
synchronize external data.
**Related**: ON CONFLICT DO UPDATE, ON CONFLICT DO NOTHING

### WHERE clause
**Definition**: The filter deciding which rows a DML statement touches.
A missing WHERE on UPDATE/DELETE affects the entire table.
**Related**: UPDATE, DELETE

### ? placeholders
**Definition**: SQLite's positional parameters. Values are bound safely
by the driver — never interpolated into the SQL string. The #1
anti-injection rule.
**Related**: Named parameters, Sanitized

### CRUD
**Definition**: Create (INSERT), Read (SELECT), Update (UPDATE), Delete
(DELETE) — the four operations every data layer exposes.
**Related**: INSERT, UPDATE, DELETE

### Prepared statement
**Definition**: SQL compiled once by the engine, then executed many
times with different parameters — reused by the driver and faster than
re-parsing.
**Related**: executemany, ? placeholders

### Sanitized
**Definition**: Values made safe by parameter binding — the engine
treats them as data, never as SQL syntax.
**Related**: ? placeholders, Named parameters

## Key Concepts Summary

### The four operations (CRUD)
- INSERT adds rows; UPDATE changes columns of matching rows.
- DELETE removes matching rows; SELECT (later) reads them.
- Always scope UPDATE/DELETE with WHERE.

### Safe value passing
- Use ? or :name placeholders; never f-string SQL.
- Parameters are data to the engine; concatenation is syntax.

### Batching and returning
- executemany for bulk inserts; INSERT ... SELECT for bulk fills.
- RETURNING hands back rows; lastrowid the generated key; rowcount
  the affected count.

### Idempotency patterns
- ON CONFLICT DO NOTHING: skip duplicates.
- ON CONFLICT DO UPDATE: upsert external data.
- Retries only make sense when re-runs are safe.

## Practice Terms

Match each term to its definition.

1. UPSERT — ___
2. executemany — ___
3. RETURNING — ___
4. rowcount — ___
5. lastrowid — ___
6. Named parameters — ___
7. Idempotent — ___
8. Prepared statement — ___

A. Rows affected by the last statement
B. Same end state no matter how many re-runs
C. INSERT with ON CONFLICT DO UPDATE fallback
D. One statement compiled once, executed many times
E. SQL that hands back rows from an INSERT/DELETE
F. The id of the last inserted row
G. :name placeholders bound by keyword
H. Batch execution over many parameter tuples

**Answers:** 1-C, 2-H, 3-E, 4-A, 5-F, 6-G, 7-B, 8-D
