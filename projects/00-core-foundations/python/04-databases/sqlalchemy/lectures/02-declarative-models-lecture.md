# Databases (SQLAlchemy) — 02: Declarative Models

## Topic Overview

The declarative mapping is where a table becomes a Python class. Instead of
writing `Table(...)` and then separately maintaining SQL, you declare a class
whose attributes *are* the columns: `class Experiment(Base)` with
`name: Mapped[str]` produces a real `experiments` table. SQLAlchemy 2.0
standardized this on `DeclarativeBase` plus the `Mapped[...]` / `mapped_column()`
typed style, which makes the schema readable directly from the type hints.

For AI/backend engineers, mapped classes are the schema contract of every
service: experiments, runs, datasets, eval results, model versions. The
2.0 style matters because it is checked in two places — Python sees the type,
the database sees the column — and because constraints (`unique`, `NOT NULL`,
`CHECK`, `INDEX`) are enforced by the database, not by hope. A unique
constraint is what stops the second training run with the same name from
silently overwriting the first.

This lecture covers `DeclarativeBase`, `Mapped[...]` and `mapped_column(...)`,
column defaults, nullable vs optional, table-level constraints through
`__table_args__`, and the inspect workflow that verifies what a model actually
declared.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Create a `DeclarativeBase` subclass and map a table as a class
2. Distinguish the 2.0 typed style (`Mapped[str]`) from the legacy `Column` style
3. Choose when to use plain `Mapped[str]` vs `mapped_column(...)`
4. Declare nullable columns with `Mapped[Optional[str]]`
5. Apply Python-side and DB-side defaults correctly
6. Add `UniqueConstraint`, `CheckConstraint`, and `Index` via `__table_args__`
7. Use `ForeignKey` to reference another table's column
8. Inspect the created schema with `inspect(engine)` to verify the mapping
9. Predict when `IntegrityError` will be raised and why the DB — not Python — raises it
10. Run the self-verifying exercise and confirm the schema contract

---

## Prerequisites

| Need | Where |
|---|---|
| Core tables and metadata | `01-core-vs-orm-lecture.md` |
| Type hints including `Optional` | `02-advanced-python/lectures/05-type-hints-lecture.md` |
| SQL constraints (UNIQUE, CHECK, FK) | General SQL knowledge |

---

## 1. DeclarativeBase — the 2.0 Starting Point

One `Base` per application; every model inherits from it. SQLAlchemy reads the
class body, turns annotated attributes into columns, and registers the class
with `Base.metadata`. The 1.x style used `declarative_base()` with raw
`Column(...)` everywhere; 2.0 prefers `Mapped[...]` + `mapped_column(...)` so
the type appears once in the annotation and once in the column definition.

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Application-wide declarative base (SQLAlchemy 2.0 style)."""
```

Every mapped class below inherits `Base`; its metadata knows all tables, which
is why one `Base.metadata.create_all(engine)` creates everything.

## 2. Mapped[...] and mapped_column(...)

The annotation is the column type: `name: Mapped[str]` means NOT NULL
unbounded text. Add `mapped_column(...)` when you need length, defaults, or
constraints — the annotation says *what*, the call says *how*.

```python
class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    model: Mapped[str] = mapped_column(String(60), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(String(200))   # NULL allowed
    score: Mapped[float] = mapped_column(default=0.0)
```

Key decisions encoded in four lines: `id` is the integer PK (auto-increment on
SQLite and Postgres), `name` must be globally unique, `model` cannot be NULL,
`notes` is optional (Python says `Optional`, the DB says nullable), and `score`
defaults to 0.0.

## 3. Nullable vs Optional

`Mapped[str]` implies NOT NULL. `Mapped[Optional[str]]` (or `Mapped[str | None]`)
implies NULL allowed. The annotation is the single source of truth for both
Python typing and the SQL column — the two must never drift.

```python
# The inspect workflow proves what was declared:
from sqlalchemy import create_engine, inspect

engine = create_engine("sqlite://")
Base.metadata.create_all(engine)

insp = inspect(engine)
cols = {c["name"]: c for c in insp.get_columns("experiments")}
print(f"columns: {sorted(cols)}")
# Output:
# columns: ['id', 'model', 'name', 'notes', 'score']
print(f"notes nullable: {cols['notes']['nullable']}")
# Output:
# notes nullable: True
```

## 4. Defaults: Python-side and DB-side

`default=0.0` is a Python-side default applied when you construct an instance
without the value. SQLAlchemy also renders a `DEFAULT` clause for the column
when possible. The distinction matters in one place: **bulk Core inserts
bypass ORM defaults** — the value must be in the dict. The ORM applies defaults
at flush time, not construction time, so `exp.score` is `None` until flush if
you read it too early.

```python
exp = Experiment(name="run-1", model="bert")   # score not set yet
session.add(exp)
session.flush()                                # defaults apply here
print(exp.score)                               # 0.0
```

## 5. Table-Level Constraints via __table_args__

Column-level constraints go inside `mapped_column(...)`; table-level ones
(uniqueness across several columns, CHECK ranges, indexes) go in
`__table_args__` as a tuple.

```python
class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    model: Mapped[str] = mapped_column(String(60), nullable=False)
    score: Mapped[float] = mapped_column(default=0.0)

    __table_args__ = (
        CheckConstraint("score >= 0.0 AND score <= 1.0", name="ck_score_range"),
        Index("ix_experiments_model", "model"),
    )
```

`CheckConstraint` makes the database refuse a score of 1.5 — not Python
validation, the schema itself. `Index("ix_experiments_model", "model")`
accelerates every `WHERE model = ...` query. Both are named so schema errors
and query plans are self-describing.

## 6. Foreign Keys: The Schema's Edges

A `ForeignKey` states that one column references another table's column — the
edge that relationships (topic 04) will traverse. The FK is declared as a
string `"experiments.id"` so it resolves lazily, even when the target table is
defined later in the file.

```python
class EvalMetric(Base):
    __tablename__ = "eval_metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    experiment_id: Mapped[int] = mapped_column(
        ForeignKey("experiments.id"), nullable=False
    )
    metric: Mapped[str] = mapped_column(String(30), nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)
```

## 7. The Database Enforces; Python Only Asks

The unique constraint is not cosmetic: the ORM will happily attempt to insert a
duplicate name; the *database* raises `IntegrityError`. This is the contract —
constraints live in the schema because they are the last line of defense,
below every bug in application logic.

```python
from sqlalchemy.exc import IntegrityError

with Session(bind=engine) as session:
    session.add(Experiment(name="dupe", model="bert"))
    session.commit()
    try:
        session.add(Experiment(name="dupe", model="gpt2"))
        session.commit()
    except IntegrityError:
        print("duplicate rejected by the schema")
# Output:
# duplicate rejected by the schema
```

---

## Common Mistakes to Avoid

### Mistake 1: Mixing legacy `Column` into a 2.0 class
```
# WRONG — 1.x style; breaks the typed Mapped contract
class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True)
# CORRECT — 2.0 typed style
class Model(Base):
    __tablename__ = "models"
    id: Mapped[int] = mapped_column(primary_key=True)
```

### Mistake 2: `Mapped[str]` for a column that must be NULL-able
```
# WRONG — NOT NULL in the DB, Optional in Python logic (drift!)
notes: Mapped[str] = mapped_column(String(200), nullable=True)
# CORRECT — the annotation is the truth
notes: Mapped[Optional[str]] = mapped_column(String(200))
```

### Mistake 3: Enforcing uniqueness only in application code
```
# WRONG — two concurrent requests both pass the Python check
if session.scalars(select(Exp).where(Exp.name == name)).first() is None:
    session.add(Exp(name=name))     # race: both requests pass
# CORRECT — unique=True in the schema; catch IntegrityError
```

### Mistake 4: Reading a defaulted attribute before flush
```
# WRONG — prints None; defaults apply at flush, not construction
exp = Experiment(name="x", model="bert")
print(exp.score)
# CORRECT — flush first (or construct with the value explicitly)
session.add(exp); session.flush(); print(exp.score)
```

### Mistake 5: Forgetting that Core bulk inserts bypass ORM defaults
```
# WRONG — the DB DEFAULT may differ or be absent; value is NULL
conn.execute(experiments.insert(), [{"name": "x", "model": "y"}])
# CORRECT — put the default in the dict explicitly
conn.execute(experiments.insert(), [{"name": "x", "model": "y", "score": 0.0}])
```

---

## Best Practices

1. One `Base` per application; never re-define it per module
2. Let the annotation carry the type: `Mapped[str]`, `Mapped[Optional[str]]`
3. Use `mapped_column()` for length, defaults, constraints; plain annotation otherwise
4. Name every constraint and index — `ck_`, `uq_`, `ix_` prefixes
5. Declare FKs as strings so definition order never matters
6. Keep constraints in the schema; treat validation as a UX layer
7. Inspect with `inspect(engine)` after `create_all` to confirm the contract
8. Set Python defaults explicitly in tests/factories to make intent visible
9. Put `__table_args__` tuples in a stable order (constraints, then indexes)
10. Remember: the ORM is not a validator — the database is the last word

---

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Class definition / mapper config | O(1) per class, once | O(columns) | — |
| `create_all` | O(tables) DDL | O(1) | once per deployment, not per request |
| IntegrityError on duplicate | O(1) DB op | O(1) | unique index lookup (fast fail) |
| Defaults at flush | O(1) per row | O(1) | explicit values skip default logic |

**Cost note:** constraints cost nothing per query — they are enforced on
write. A `CHECK` that stops a bad row costs one comparison; a missing
constraint that lets bad data through costs a debugging week. Schema is
free insurance.

---

## AI Engineering Relevance

**Where this shows up:** every table in an AI service is a mapped class — the
experiment registry, the model version table, the eval metric sink, the
dataset manifest. The schema is the contract between the training loop writing
metadata and the API serving it.

| Concept here | Used for |
|---|---|
| `unique=True` | one row per experiment name, one row per model version |
| `CheckConstraint` | scores in [0,1], latency >= 0, split ratios summing to 1 |
| `Index` | `WHERE model = ?` registry lookups |
| `Optional` | nullable fields like `deployed_at`, `notes` |

**Scale note:** at 1M rows, a missing index turns every registry listing into
a full scan; at 200 concurrent writes, a missing unique constraint turns every
race into corrupted data. The schema is load-bearing — design it first.

---

## Practice Exercises

### Exercise 1: Minimal Mapped Class (Difficulty: Easy)
Map `Dataset(id, name unique, rows: int, format: str)` with `Mapped[...]`.
Create the schema and inspect the columns.

### Exercise 2: Optional + Defaults (Difficulty: Easy)
Add `description: Optional[str]` and `version: Mapped[int] = mapped_column(default=1)`
to the `Dataset` class. Verify with `inspect` that description is nullable and
that a flush assigns `version == 1`.

### Exercise 3: Table-Level Constraints (Difficulty: Medium)
Add `CheckConstraint("rows >= 0")` and `Index` on `format`. Insert a row with
`rows=-5` and confirm the database raises `IntegrityError`.

### Exercise 4: Unique Contract (Difficulty: Medium)
Write a `get_or_create`-style function that relies on the unique constraint:
attempt the insert, catch `IntegrityError`, return the existing row. Prove it
behaves correctly on a duplicate.

### Exercise 5: Model Review (Difficulty: Hard)
Design the schema for a model registry: `ModelVersion(name, version, uri,
created_at, metrics JSON)`. Justify: which columns are unique, which are
optional, which constraints apply, and which index the registry listing needs.
(You will build this in Challenge 02.)

---

## Summary

| Concept | Description |
|---|---|
| `DeclarativeBase` | one base per app; classes become tables |
| `Mapped[...]` | annotation-driven column typing (2.0 style) |
| `mapped_column(...)` | length, defaults, per-column constraints |
| `Optional[...]` | NULL-able column; the annotation is the truth |
| `__table_args__` | table-level constraints and indexes |
| `ForeignKey` | schema edge; resolved lazily from strings |
| `IntegrityError` | the database enforcing what Python only asked |

Declarative models are the bridge between the Core tables of topic 01 and the
object graphs of topics 03-06. Get the constraints right here — the Session
will faithfully try to write whatever you give it.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Start a mapping | `class Base(DeclarativeBase): pass` |
| Map a table | `class T(Base): __tablename__ = "t"` |
| Integer PK | `id: Mapped[int] = mapped_column(primary_key=True)` |
| Unique text | `name: Mapped[str] = mapped_column(String(80), unique=True)` |
| Optional column | `notes: Mapped[Optional[str]] = mapped_column(String(200))` |
| Default | `score: Mapped[float] = mapped_column(default=0.0)` |
| Table constraints | `__table_args__ = (CheckConstraint(...), Index(...))` |
| Foreign key | `parent_id: Mapped[int] = mapped_column(ForeignKey("t.id"))` |
| Create schema | `Base.metadata.create_all(engine)` |
| Verify schema | `inspect(engine).get_columns("t")` |

---

## Next Steps

Next: **[03 — Session Lifecycle](03-session-lifecycle-lecture.md)** — what the
Session does with your mapped objects: unit of work, identity map, commit.

Continues in: **[Phase 05 — Databases](../../05-web-frameworks/fastapi/19-orm.py)** —
models powering a FastAPI CRUD service.

Official docs:
- Declarative mapping: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html
- `Mapped`/`mapped_column`: https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
- Constraints: https://docs.sqlalchemy.org/en/20/core/constraints.html
