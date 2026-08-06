# Databases (SQLAlchemy) — 01: Core vs ORM

## Topic Overview

SQLAlchemy is two APIs in one package. The **Core** layer is a SQL-first
foundation: schema objects (`Table`, `MetaData`), a SQL expression language,
and a `Connection` that compiles expressions into dialect-specific SQL. The
**ORM** layer sits on top of Core and maps Python classes to tables, adding the
`Session` unit of work, identity map, and relationship machinery. Because the
ORM is *built on* Core, everything the ORM emits is Core under the hood — one
mental model, two levels of abstraction.

For AI/backend engineers this split matters daily. Bulk loads of training
metadata, ETL jobs, ad-hoc analytics, and migrations are Core work: "rows in,
rows out" with no object ceremony. Service CRUD over object graphs — a model
registry, an experiment store — is ORM work. Choosing the wrong layer is how a
10-line bulk load becomes a 100-line object-mapping exercise, or how a simple
CRUD endpoint gets buried in string-built SQL.

This lecture covers the Core layer: engines and dialects, metadata and tables,
parameterized `text()` SQL, transactions, and the exact decision rule for when
Core beats the ORM (and when it does not).

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the two-layer architecture of SQLAlchemy and how the ORM builds on Core
2. Create an `Engine` and understand the role of dialects in SQL compilation
3. Define a table with `Table`/`MetaData` and create it with `create_all`
4. Execute parameterized `text()` statements with bound parameters
5. Perform Core inserts, including executemany-style bulk loads
6. Read rows as `Row` objects and access columns by name or position
7. Manage transactions explicitly with `conn.commit()` / `conn.rollback()`
8. Decide between Core and ORM for a given task using a concrete rule
9. Recognize the SQL-injection hazard of f-string values and avoid it
10. Run the self-verifying exercise and interpret its `_verify()` output

---

## Prerequisites

| Need | Where |
|---|---|
| Python type hints | `02-advanced-python/lectures/05-type-hints-lecture.md` |
| SQL basics (SELECT/INSERT/WHERE) | General SQL knowledge; any tutorial |
| Context managers (`with`) | `02-advanced-python/lectures/03-context-managers-lecture.md` |

---

## 1. Two Layers: Core and ORM

Every SQLAlchemy statement starts as a Python expression and ends as dialect
SQL. The **Engine** owns the database connection (via a pool) and the
**dialect** — the compiler that knows how SQLite, PostgreSQL, or MySQL spell
things. You write one expression; SQLAlchemy writes the dialect.

```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite://")   # in-memory; dialect = SQLite

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1 AS one"))
    print(result.scalar_one())
# Output:
# 1
```

The same `text("SELECT ...")` works against Postgres with a different URL —
only the dialect changes. Core is the layer that knows about `Table` objects
and `Connection`s; the ORM is the layer that knows about `Session` and mapped
classes.

## 2. Metadata and Tables

`MetaData` is a catalog of schema objects. `Table` describes a table without
any Python class: columns, types, constraints. `meta.create_all(engine)`
emits the `CREATE TABLE` statements.

```python
from sqlalchemy import Column, Integer, MetaData, String, Table

meta = MetaData()
widgets = Table(
    "widgets",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("qty", Integer, nullable=False, default=0),
)
meta.create_all(engine)
```

Column objects are addressable through the table: `widgets.c.name` is the
`name` column expression. This is the key that unlocks the expression language:
`select(widgets.c.name, widgets.c.qty)`.

## 3. Core Insert and Select

Core `insert()` accepts either a single dict or a **list of dicts** — the list
form compiles to a single multi-row INSERT (executemany). Core connections do
**not** auto-commit: a `with engine.connect()` block ends with a rollback
unless you commit explicitly.

```python
with engine.connect() as conn:
    conn.execute(
        widgets.insert(),
        [{"name": "bolt", "qty": 12}, {"name": "nut", "qty": 300}],
    )
    conn.commit()                     # explicit — never implicit

with engine.connect() as conn:
    rows = conn.execute(select(widgets.c.name, widgets.c.qty)).all()
    for row in rows:
        print(f"row: {row.name} x{row.qty}")
# Output:
# row: bolt x12
# row: nut x300
```

Rows are `Row` objects: indexable by position (`row[0]`) and by column name
(`row.name`). No classes involved — plain data out.

## 4. text(): Raw SQL Done Safely

`text()` wraps a raw SQL string — the escape hatch for window functions, CTEs,
and dialect features the expression language does not spell. The rule that
never bends: **values go through `:name` bound parameters, never f-strings**.

```python
with engine.connect() as conn:
    rows = conn.execute(
        text("SELECT name, qty FROM widgets WHERE qty > :qty ORDER BY qty"),
        {"qty": 50},
    ).all()
    for row in rows:
        print(f"big stock: {row[0]} = {row[1]}")
# Output:
# big stock: nut = 300
```

The `{"qty": 50}` dict is the parameter binding. F-string interpolation would
inline the value into the SQL text — that is how injection happens, and why
every parameterized path in this module uses `:name`.

## 5. Transactions: You Own the Commit

Core keeps transactions explicit. A `Connection` begins a transaction
immediately; `commit()` makes it permanent, `rollback()` discards it, and
leaving the `with` block without either rolls back. This is the same
transaction boundary the ORM Session later wraps — learning it here makes
Session behavior (topic 03) obvious.

```python
with engine.connect() as conn:
    conn.execute(widgets.insert(), {"name": "temp", "qty": 1})
    # no commit -> INSERT is rolled back when the block exits

with engine.connect() as conn:
    count = conn.execute(select(widgets.c.qty)).rowcount  # 0 rows visible
```

## 6. When Core Beats the ORM

The decision rule that keeps services honest:

- **Core** when the job is "rows in, rows out": bulk loads, ad-hoc analytics,
  migrations, ETL. No object graphs, no cascades, no identity — just
  statements and results.
- **ORM** when you have object graphs, relationships, and units of work:
  CRUD over a registry, nested writes, cascade deletes.

```python
BULK_N = 10_000
with engine.connect() as conn:
    conn.execute(
        widgets.insert(),
        [{"name": f"part-{i}", "qty": i} for i in range(BULK_N)],
    )
    conn.commit()
```

One statement, 10,000 rows. The ORM would track 10,000 objects through its
unit of work for no benefit. This is the canonical Core win.

## 7. Production Pattern: Table-Bounded Bulk Loader

The shipping shape for large loads: chunk the parameter list so a 1M-row load
never materializes a giant statement, and commit per chunk so a crash loses at
most one chunk.

```python
def safe_upsert_metrics(conn, rows: list[dict], batch_size: int = 500) -> int:
    total = 0
    for start in range(0, len(rows), batch_size):
        batch = rows[start : start + batch_size]
        conn.execute(widgets.insert(), batch)
        conn.commit()
        total += len(batch)
    return total
```

The bound is real: SQLite's default limit is ~999 bound parameters per
statement. Batching is what makes loaders scale past it.

---

## Common Mistakes to Avoid

### Mistake 1: f-string values into SQL
```
# WRONG — value inlined into SQL text; injection and quoting bugs
conn.execute(text(f"SELECT * FROM widgets WHERE name = '{user}'"))
# CORRECT — bound parameter; SQLite/Postgres handle quoting
conn.execute(text("SELECT * FROM widgets WHERE name = :name"), {"name": user})
```

### Mistake 2: Forgetting the explicit commit
```
# WRONG — "the rows vanished!"
with engine.connect() as conn:
    conn.execute(widgets.insert(), {"name": "x", "qty": 1})
# CORRECT
with engine.connect() as conn:
    conn.execute(widgets.insert(), {"name": "x", "qty": 1})
    conn.commit()
```

### Mistake 3: Reaching for the ORM for bulk loads
```
# WRONG — 10k ORM objects through the unit of work
session.add_all([Widget(name=f"p-{i}", qty=i) for i in range(10_000)])
# CORRECT — Core executemany, one statement
conn.execute(widgets.insert(), [{"name": f"p-{i}", "qty": i} for i in range(10_000)])
```

### Mistake 4: Assuming `sqlite://` shares one database across connections
```
# WRONG — each pooled connection gets a FRESH empty in-memory DB
engine = create_engine("sqlite://")
# CORRECT — pin one connection with StaticPool (used throughout this module)
from sqlalchemy.pool import StaticPool
engine = create_engine("sqlite://", poolclass=StaticPool)
```

### Mistake 5: Using `row.name` where the column does not exist in the SELECT
```
# WRONG — AttributeError: Row has no attribute 'qty'
row = conn.execute(select(widgets.c.name)).one()
print(row.qty)
# CORRECT — only selected columns exist on the Row
print(row.name)
```

---

## Best Practices

1. Always bind values with `:name` parameters — never f-strings
2. Commit explicitly at the end of a write block; never rely on implicit behavior
3. Use `Table`/`MetaData` for Core work; define columns once and reuse `table.c`
4. Bulk-load with executemany-style lists, chunked for very large inputs
5. Leave the `with engine.connect()` block on exceptions — rollback is automatic
6. Prefer the expression language; use `text()` only for dialect-specific SQL
7. Keep the Core/ORM decision explicit: rows-in/rows-out → Core
8. Inspect compiled SQL with `str(stmt.compile(dialect=engine.dialect))` when unsure
9. Name constraints and indexes so schema errors are self-describing
10. Treat Core as the foundation: when ORM behavior confuses you, look at the
    Core statements it emits

---

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Single-row Core insert | O(1) DB op | O(1) | — |
| Executemany bulk insert | O(rows) DB work, 1 round trip | O(batch) | chunk to bound params |
| `conn.execute(...).all()` | O(rows) | O(rows) memory | iterate the cursor instead |
| f-string SQL build per query | O(1) | O(1) | bound params (no rebuild cost) |

**Cost note:** the dominant cost in DB work is **round trips**, not Python
lines. One multi-row INSERT beats 10,000 single-row INSERTs by ~10,000
round trips — the entire reason bulk loading is a Core pattern.

---

## AI Engineering Relevance

**Where this shows up:** model registries, prompt stores, and eval-result
pipelines all do two things: bulk-load telemetry (Core) and serve CRUD over
object graphs (ORM). A training loop writing 1M metric rows per run *must* use
Core-style batch inserts or the logging itself becomes the bottleneck.

| Concept here | Used for |
|---|---|
| Executemany bulk insert | writing eval metrics, telemetry, dataset rows |
| `text()` + bound params | dialect-specific analytics, CTEs, window queries |
| Explicit transactions | ETL jobs that must be all-or-nothing |
| Engine/dialect abstraction | same code against SQLite (dev) and Postgres (prod) |

**Scale note:** at 1M rows per ingest, the parameter-limit per statement stops
being trivia — chunking (Production Pattern) becomes mandatory. At 200
concurrent requests, connection pooling (Engine default) matters more than
any single query.

---

## Practice Exercises

### Exercise 1: Parameterized Count (Difficulty: Easy)
Write a Core query using `text()` that returns the number of rows in `widgets`
whose `qty` is exactly `:qty`. Expected: `2` for qty 12. No solution here —
implement it in the challenge.

### Exercise 2: Metadata Introspection (Difficulty: Easy)
Create a `Table` with three columns (id, name, value), create it, and print
`engine.dialect.name` and the table's column names via `widgets.c.keys()`.

### Exercise 3: Batch Write + Readback (Difficulty: Medium)
Insert 100 rows `[{"name": f"p-{i}", "qty": i}]` in one executemany, then
SELECT names where `qty >= 90`, ordered by qty. Expected: `p-90` through `p-99`.

### Exercise 4: Chunked Loader (Difficulty: Medium)
Reimplement `safe_upsert_metrics` for 10,000 rows with `batch_size=1000`.
Verify the total matches and the table count is correct.

### Exercise 5: Core vs ORM Decision (Difficulty: Hard)
For each scenario, pick Core or ORM and justify: (a) nightly ETL of 5M rows;
(b) a FastAPI endpoint returning one experiment with its nested metrics;
(c) a migration backfilling a new nullable column. Write your answers with
one-line justifications.

---

## Summary

| Concept | Description |
|---|---|
| Core | SQL-first layer: `Table`, `MetaData`, `Connection`, expression language |
| ORM | Object-mapping layer built on Core: classes, Session, relationships |
| Engine | Owns pool + dialect; the single entry point |
| `text()` | Raw SQL with `:name` bound parameters |
| Transactions | Explicit in Core: `commit()` persists, exit-without-commit rolls back |
| Bulk loads | Executemany lists — the canonical Core win |

Core is the foundation every ORM statement compiles down to. Master the
transaction discipline and the parameter-binding rule here, and the Session
(which wraps the exact same boundaries) will feel like familiar ground.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Create an engine | `engine = create_engine("sqlite://", poolclass=StaticPool)` |
| Define a table | `Table("t", meta, Column(...), ...)` |
| Create schema | `meta.create_all(engine)` |
| Bulk insert | `conn.execute(t.insert(), [dicts...])` + `conn.commit()` |
| Raw SQL | `conn.execute(text("... :param"), {"param": v})` |
| Select columns | `conn.execute(select(t.c.a, t.c.b))` |
| Row access | `row.a` or `row[0]` |

---

## Next Steps

Next: **[02 — Declarative Models](02-declarative-models-lecture.md)** — turn
these tables into typed Python classes with `Mapped[...]` and constraints.

Continues in: **[Phase 05 — Databases](../../05-web-frameworks/fastapi/19-orm.py)** —
the ORM layer in a FastAPI service.

Official docs:
- Core tutorial: https://docs.sqlalchemy.org/en/20/core/tutorial.html
- Engine/dialect reference: https://docs.sqlalchemy.org/en/20/core/engines.html
- `text()`: https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text
