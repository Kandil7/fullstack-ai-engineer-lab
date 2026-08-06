# Core vs ORM — Glossary 01

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| bind parameter | SQL | A `:name` placeholder in SQL text, filled with a value at execution |
| bulk insert | Core | One multi-row INSERT from a list of dicts (executemany) |
| Column | Core | A single column definition inside a `Table` |
| Connection | Core | A live database session from the pool; owns the transaction |
| Core | Layer | SQLAlchemy's SQL-first layer: schema objects, expressions, connections |
| create_all | DDL | Emits CREATE TABLE for every table in a `MetaData` |
| dialect | Engine | The compiler that translates expressions into a DB's SQL |
| Engine | Core | The pool + dialect entry point; owns connections |
| executemany | Core | DBAPI batching mode; drives multi-row inserts |
| MetaData | Core | Catalog of schema objects (tables) for one database |
| ORM | Layer | Object-relational mapping: classes <-> tables, Session on top |
| Row | Core | A result row; indexable by position and column name |
| select() | Core | The expression-language SELECT statement |
| Table | Core | A table definition independent of any Python class |
| text() | Core | Raw SQL string wrapper with bound-parameter support |
| transaction | Core | A unit of work; commit persists, rollback discards |
| URL | Engine | Connection string; determines the dialect (`sqlite://`, `postgresql://`) |

## Detailed Definitions

### bind parameter
**Definition**: A `:name` placeholder in raw SQL that receives a value from a
separate parameters dict at execution time. The database treats it as data,
never as SQL text — the injection-proof way to pass values.
**Example**:
```python
from sqlalchemy import create_engine, text
engine = create_engine("sqlite://")
with engine.connect() as conn:
    row = conn.execute(
        text("SELECT :a + :b AS total"), {"a": 2, "b": 3}
    ).one()
    print(row.total)
# Output:
# 5
```
**Complexity**: O(1) per bind.
**Related**: text(), transaction

### bulk insert
**Definition**: Inserting many rows in one statement by passing a list of
dicts to `table.insert()`. Saves N-1 round trips versus one INSERT per row.
**Example**:
```python
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
engine = create_engine("sqlite://")
meta = MetaData()
t = Table("t", meta, Column("id", Integer, primary_key=True), Column("name", String(50)))
meta.create_all(engine)
with engine.connect() as conn:
    conn.execute(t.insert(), [{"name": "a"}, {"name": "b"}, {"name": "c"}])
    conn.commit()
    print(conn.execute(t.select()).rowcount)
# Output:
# 3
```
**Complexity**: O(rows) DB work, 1 round trip.
**Related**: executemany, Connection, transaction

### Column
**Definition**: One column inside a `Table`: name, type, and constraints
(nullable, default, primary key). The Core unit that the ORM maps to a class
attribute.
**Example**:
```python
col = Column("qty", Integer, nullable=False, default=0)
print(col.name, col.type)
# Output:
# qty INTEGER
```
**Complexity**: O(1) definition.
**Related**: Table, MetaData

### Connection
**Definition**: A checked-out database session from the engine's pool. It owns
the current transaction: `commit()` persists, exiting the block rolls back.
**Example**:
```python
with engine.connect() as conn:
    conn.execute(t.insert(), {"name": "x"})
    # no commit -> rolled back on block exit
```
**Related**: Engine, transaction

### Core
**Definition**: The lower of SQLAlchemy's two layers: `MetaData`/`Table`
schema objects, the SQL expression language, and `Connection`. Everything the
ORM emits is Core under the hood.
**Example**:
```python
from sqlalchemy import select
stmt = select(t.c.name).where(t.c.name == "a")   # Core expression
```
**Complexity**: compilation O(1) per statement.
**Related**: ORM, Engine, Table

### create_all
**Definition**: `meta.create_all(engine)` emits CREATE TABLE for every table
in the metadata that does not yet exist. Idempotent; the usual dev bootstrap.
**Example**:
```python
meta.create_all(engine)   # creates table 't'
```
**Related**: MetaData, Table

### dialect
**Definition**: The component that compiles expressions into a database's SQL
and translates types. Chosen automatically from the URL (`sqlite`,
`postgresql`, `mysql`).
**Example**:
```python
print(engine.dialect.name)
# Output:
# sqlite
```
**Related**: Engine, URL

### Engine
**Definition**: The application's single entry point to a database: a
connection pool plus a dialect. Created once per database per process.
**Example**:
```python
engine = create_engine("sqlite://")
```
**Related**: Connection, dialect, URL

### executemany
**Definition**: DBAPI batching mode used when `conn.execute(insert, list_of_dicts)`
runs: the same statement executes against every parameter set in one call.
**Related**: bulk insert, Connection

### MetaData
**Definition**: A catalog of `Table` objects sharing a namespace. One metadata
per application/database; `create_all` and (later) `Base.metadata` build on it.
**Example**:
```python
meta = MetaData()
```
**Related**: Table, create_all

### ORM
**Definition**: The object-relational layer built on Core: mapped classes,
relationships, and the Session unit of work. The subject of topics 02-10.
**Example**:
```python
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
```
**Related**: Core, Session

### Row
**Definition**: A result row from `conn.execute(...)`: indexable by position
(`row[0]`) and by column name (`row.name`). The Core data shape.
**Example**:
```python
row = conn.execute(select(t.c.name, t.c.qty)).one()
print(row[0], row.name)
# Output:
# x x
```
**Related**: select(), Connection

### select()
**Definition**: The expression-language SELECT: `select(t.c.name)` compiles
to dialect SQL with bound parameters. The Core statement the ORM also uses.
**Example**:
```python
print(select(t.c.name).where(t.c.name == "a"))
# Output (compiled):
# SELECT t.name FROM t WHERE t.name = :name_1
```
**Related**: Row, text()

### Table
**Definition**: A table definition independent of any Python class: columns,
types, constraints. `table.c` exposes column expressions.
**Related**: Column, MetaData, create_all

### text()
**Definition**: Wraps a raw SQL string for execution. Supports `:name` bound
parameters — the escape hatch for dialect-specific SQL, never for string
interpolation of values.
**Example**:
```python
conn.execute(text("SELECT 1"))
```
**Related**: bind parameter, select()

### transaction
**Definition**: A unit of work on a Connection. `commit()` persists it;
`rollback()` (or block exit without commit) discards it. The boundary the
ORM Session later wraps.
**Example**:
```python
with engine.connect() as conn:
    conn.execute(t.insert(), {"name": "y"})
    conn.commit()          # persisted
```
**Related**: Connection, bulk insert

### URL
**Definition**: The connection string passed to `create_engine`. The scheme
selects the dialect: `sqlite://`, `postgresql+psycopg://`, `mysql+pymysql://`.
**Related**: Engine, dialect

## Key Concepts Summary

### The Two Layers
- Core is SQL-first: tables, statements, connections, explicit transactions
- ORM is built on Core: classes, sessions, relationships
- Choose Core for rows-in/rows-out; ORM for object graphs

### Statement Execution
- `text()` for raw SQL with bound parameters
- Expression language for composable, dialect-safe statements
- `Row` for results: position and name access

### Transactions
- Core connections never auto-commit
- `commit()` persists; block exit without commit rolls back
- Bulk loads belong in Core: one statement, thousands of rows

## Practice Terms

Match each term to its definition (answers at the bottom).

1. bind parameter — ___
2. executemany — ___
3. dialect — ___
4. Row — ___
5. transaction — ___
6. text() — ___

A) DBAPI batching mode driving multi-row inserts
B) A `:name` placeholder filled with a value at execution
C) Raw SQL wrapper supporting bound parameters
D) A unit of work; commit persists, rollback discards
E) The compiler that produces a database's SQL
F) A result row accessible by position and name

**Answers:** 1-B, 2-A, 3-E, 4-F, 5-D, 6-C
