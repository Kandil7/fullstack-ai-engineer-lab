# SELECT Basics — Glossary 04

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| * wildcard | Projection | Selects all columns; fine for debug, costly in prod |
| Aliasing | Projection | Renaming a column with AS; the row dict key |
| Column order | Semantics | Headers follow the SELECT list, not table order |
| Comma-join | FROM clause | Multiple tables joined by a WHERE equality |
| Cross product | FROM clause | Every row of table A paired with every row of table B |
| DISTINCT | Projection | Removes duplicate result rows |
| Expressions | Projection | Computed values in the select list, e.g. price * 1.1 |
| fetchall | Driver | Returns all rows as a list of tuples |
| fetchone | Driver | Returns the next row as a tuple, or None |
| FROM clause | Query anatomy | Names the table(s) being read |
| Headers | Result | Column names from the select list aliases |
| LIMIT | Query anatomy | Maximum number of rows returned |
| Offset | Query anatomy | Rows skipped before the result (LIMIT ? OFFSET ?) |
| ORDER BY | Query anatomy | Sorts the result; ASC default, DESC explicit |
| Query plan | Engine | The engine's execution strategy for a query |
| Row factory | Driver | row_factory=sqlite3.Row enables access by name |
| SELECT | Query anatomy | The statement: projection over FROM rows |
| SQLite error | Errors | Exception for syntax/planning problems |
| WHERE clause | Query anatomy | Filters rows before projection |
| Cursor | Driver | The object that executes SQL and yields rows |

## Detailed Definitions

### * wildcard
**Definition**: Selects every column. Convenient for exploration;
against wide tables it ships unnecessary bytes and defeats covering
indexes.
**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
conn.execute("INSERT INTO t (name, age) VALUES (?, ?)", ("alice", 30))
print(conn.execute("SELECT * FROM t").fetchall())
```
```text
[(1, 'alice', 30)]
```
**Related**: Aliasing, Column order

### Aliasing
**Definition**: Renames a result column with `AS` — `SELECT price * 1.1
AS taxed` — and becomes the header (and the dict key under a row
factory).
**Example**:
```python
conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, price REAL)")
conn.execute("INSERT INTO items (price) VALUES (?)", (100,))
print(conn.execute("SELECT price * 1.1 AS taxed FROM items").fetchall())
```
```text
[(110.0,)]
```
**Related**: Expressions, Headers

### Column order
**Definition**: Result headers follow the SELECT list order — never the
table's column order. Positional consumers depend on it.
**Related**: * wildcard, Headers

### Comma-join
**Definition**: `FROM a, b WHERE a.x = b.x` — an implicit join: the
cross product filtered by the WHERE equality. Works, but explicit
JOINs are clearer (topic 07).
**Related**: Cross product, FROM clause

### Cross product
**Definition**: Pairing every row of A with every row of B — n*m rows.
The raw material for joins; without a join condition you get every
combination.
**Related**: Comma-join, FROM clause

### DISTINCT
**Definition**: Removes duplicate rows from the result (turns the bag
into a set). Costs a sort/hash.
**Example**:
```python
conn.execute("CREATE TABLE tags (tag TEXT)")
conn.executemany("INSERT INTO tags (tag) VALUES (?)", [("a",), ("a",), ("b",)])
print(conn.execute("SELECT DISTINCT tag FROM tags").fetchall())
```
```text
[('a',), ('b',)]
```
**Related**: ORDER BY, LIMIT

### Expressions
**Definition**: Computed values in the select list: arithmetic, string
functions, CASE, etc. Columns can be transformed without changing the
table.
**Related**: Aliasing, * wildcard

### fetchall / fetchone
**Definition**: Driver API: `fetchall()` returns the remaining rows as a
list of tuples; `fetchone()` returns one tuple or None when exhausted.
**Example**:
```python
cur = conn.execute("SELECT tag FROM tags")
print(cur.fetchone())
print(cur.fetchall())
```
```text
('a',)
[('a',), ('b',)]
```
**Related**: Cursor, Row factory

### FROM clause
**Definition**: Names the table(s) whose rows the query processes.
Everything else in the query filters, groups, or projects these rows.
**Related**: SELECT, WHERE clause

### Headers
**Definition**: The column names of the result, taken from the select
list (with AS aliases applied).
**Related**: Aliasing, Column order

### LIMIT / Offset
**Definition**: `LIMIT n` caps the row count; `LIMIT n OFFSET m` skips m
rows first. OFFSET pagination re-reads skipped rows (topic 14).
**Example**:
```python
conn.executemany("INSERT INTO tags (tag) VALUES (?)", [("c",), ("d",)])
print(conn.execute("SELECT tag FROM tags LIMIT 2 OFFSET 1").fetchall())
```
```text
[('a',), ('b',)]
```
**Related**: ORDER BY, DISTINCT

### ORDER BY
**Definition**: Sorts the result by one or more columns; ASC is default,
DESC explicit. Adds a sort (or uses an index if aligned).
**Example**:
```python
print(conn.execute("SELECT tag FROM tags ORDER BY tag DESC LIMIT 2").fetchall())
```
```text
[('d',), ('c',)]
```
**Related**: LIMIT, DISTINCT

### Query plan
**Definition**: The engine's chosen execution strategy (scan vs index
search, sort vs temp B-tree), inspectable with EXPLAIN QUERY PLAN.
**Related**: Cursor, Query anatomy

### Row factory
**Definition**: `conn.row_factory = sqlite3.Row` makes rows addressable
by name — `row["name"]` — instead of position.
**Example**:
```python
conn.row_factory = sqlite3.Row
r = conn.execute("SELECT id, name, age FROM t").fetchone()
print(r["name"])
```
```text
alice
```
**Related**: fetchall, Cursor

### SELECT
**Definition**: The read statement: projects (chooses columns) from the
rows delivered by FROM, filtered by WHERE, ordered and limited last.
**Related**: FROM clause, WHERE clause, ORDER BY

### SQLite error / Cursor
**Definition**: `sqlite3.Error` is raised for syntax or planning
failures. A Cursor executes SQL and returns rows/rowcount.
**Related**: fetchall, Query plan

### WHERE clause
**Definition**: Filters rows before projection/grouping — the row-level
gate of the query.
**Related**: SELECT, FROM clause

## Key Concepts Summary

### Query anatomy
- FROM: source rows -> WHERE: filter -> SELECT: project -> ORDER BY:
  sort -> LIMIT: cap.
- ORDER BY/LIMIT run after projection.

### Projection
- The select list chooses columns and computes expressions.
- AS aliases set result headers.
- SELECT * is a debug tool, not a prod habit.

### Result semantics
- Rows are tuples by default; sqlite3.Row enables name access.
- Column order follows the select list.
- DISTINCT deduplicates; ORDER BY sorts; LIMIT truncates.

### Drivers
- Cursor executes and returns; fetchone/fetchall consume rows.
- rowcount tells how many rows changed.

## Practice Terms

Match each term to its definition.

1. DISTINCT — ___
2. Cursor — ___
3. LIMIT — ___
4. ORDER BY — ___
5. Row factory — ___
6. Cross product — ___
7. Headers — ___
8. Expressions — ___

A. Caps the number of result rows
B. Removes duplicate result rows
C. Sorts the result rows
D. Every row of A paired with every row of B
E. Name-based row access (sqlite3.Row)
F. The object executing SQL and yielding rows
G. Computed values in the select list
H. Column names from the select list with aliases

**Answers:** 1-B, 2-F, 3-A, 4-C, 5-E, 6-D, 7-H, 8-G
