# Declarative Models — Glossary 02

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| CheckConstraint | Constraint | Table-level rule the DB enforces on every write |
| DeclarativeBase | Mapping | The 2.0 base class every mapped model inherits |
| default | Column | Python-side value applied when the attribute is not set |
| ForeignKey | Constraint | Declares that a column references another table's column |
| Index | Performance | Accelerates lookups on the indexed columns |
| inspect() | Tooling | Reflects a created schema back from the database |
| IntegrityError | Error | Raised when the DB rejects a write (unique, NOT NULL, CHECK) |
| Mapped | Mapping | Annotation wrapper: `Mapped[str]` declares the column type |
| mapped_column() | Mapping | Configures a mapped attribute: length, defaults, constraints |
| NOT NULL | Constraint | The column must have a value; derived from `Mapped[T]` |
| Optional | Mapping | `Mapped[Optional[str]]` — NULL is allowed |
| primary_key | Mapping | The row identity; auto-increments on SQLite/Postgres |
| String(n) | Type | Variable-length text with an optional length limit |
| __tablename__ | Mapping | The actual table name for a mapped class |
| __table_args__ | Mapping | Table-level constraints and indexes as a tuple |
| UniqueConstraint | Constraint | Values must be unique (single or composite) |

## Detailed Definitions

### CheckConstraint
**Definition**: A table-level rule the database enforces on every insert and
update — e.g., a score must stay in [0, 1]. The DB is the last word; Python
validation is only a UX layer.
**Example**:
```python
from sqlalchemy import CheckConstraint

class Experiment(Base):
    __tablename__ = "experiments"
    score: Mapped[float] = mapped_column(default=0.0)
    __table_args__ = (
        CheckConstraint("score >= 0.0 AND score <= 1.0", name="ck_score_range"),
    )
```
**Related**: UniqueConstraint, IntegrityError

### DeclarativeBase
**Definition**: The 2.0 base class. One per application; every mapped class
inherits it, and `Base.metadata` collects all tables.
**Example**:
```python
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
```
**Related**: Mapped, __tablename__

### default
**Definition**: A Python-side column default applied when an instance is
constructed without that attribute. Applied at flush time — not at
construction, not by Core bulk inserts.
**Example**:
```python
class Experiment(Base):
    __tablename__ = "experiments"
    version: Mapped[int] = mapped_column(default=1)

exp = Experiment()          # version is None until flush
session.add(exp); session.flush()
print(exp.version)
# Output:
# 1
```
**Related**: mapped_column, Mapped

### ForeignKey
**Definition**: Declares that this column references another table's column —
the schema edge that relationships (topic 04) traverse. Written as a string
so it resolves lazily.
**Example**:
```python
from sqlalchemy import ForeignKey
class EvalMetric(Base):
    __tablename__ = "eval_metrics"
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"))
```
**Related**: UniqueConstraint, Index

### Index
**Definition**: A table-level structure that accelerates lookups on the
indexed columns — the difference between a scan and a seek for
`WHERE model = ...`.
**Example**:
```python
from sqlalchemy import Index
__table_args__ = (Index("ix_experiments_model", "model"),)
```
**Complexity**: O(log n) lookups; O(n) storage.
**Related**: CheckConstraint, __table_args__

### inspect()
**Definition**: Reflects a created schema back from the database — the way to
verify what the model actually declared (columns, nullability, types).
**Example**:
```python
from sqlalchemy import create_engine, inspect
engine = create_engine("sqlite://")
Base.metadata.create_all(engine)
cols = {c["name"] for c in inspect(engine).get_columns("experiments")}
print(sorted(cols))
# Output:
# ['id', 'model', 'name', 'notes', 'score']
```
**Related**: create_all (via metadata), Mapped

### IntegrityError
**Definition**: Raised when the database rejects a write: duplicate unique
value, NOT NULL violation, CHECK failure. The ORM will try to write anything —
the DB says no.
**Example**:
```python
from sqlalchemy.exc import IntegrityError
with Session(bind=engine) as session:
    session.add(Experiment(name="dupe")); session.commit()
    try:
        session.add(Experiment(name="dupe")); session.commit()
    except IntegrityError:
        print("rejected")
# Output:
# rejected
```
**Related**: UniqueConstraint, CheckConstraint

### Mapped
**Definition**: The annotation wrapper that declares a column: `Mapped[str]`
means NOT NULL text; `Mapped[Optional[str]]` means NULL-able. The 2.0 typed
style replaces 1.x `Column(...)` everywhere.
**Example**:
```python
name: Mapped[str] = mapped_column(String(80), unique=True)
```
**Related**: mapped_column, Optional

### mapped_column()
**Definition**: Configures a mapped attribute — length, defaults, per-column
constraints — on top of the type in the annotation.
**Example**:
```python
score: Mapped[float] = mapped_column(default=0.0)
```
**Related**: Mapped, default

### NOT NULL
**Definition**: The constraint that a column must have a value. In the 2.0
style it is implied by `Mapped[T]` (non-Optional) — the annotation is the truth.
**Related**: Mapped, Optional

### Optional
**Definition**: `Mapped[Optional[str]]` (or `Mapped[str | None]`) declares a
NULL-able column in both Python typing and the schema — they must never drift.
**Related**: Mapped, NOT NULL

### primary_key
**Definition**: The column (or composite) that identifies a row. An integer
PK auto-increments on SQLite and Postgres.
**Example**:
```python
id: Mapped[int] = mapped_column(primary_key=True)
```
**Related**: Mapped, mapped_column

### String(n)
**Definition**: Variable-length text with an optional length. SQLite ignores
the length; Postgres enforces it — a divergence to remember (topic 09).
**Related**: Mapped, mapped_column

### __tablename__
**Definition**: The actual table name for a mapped class. Without it the class
is not mapped to a table.
**Example**:
```python
class Experiment(Base):
    __tablename__ = "experiments"
```
**Related**: DeclarativeBase, __table_args__

### __table_args__
**Definition**: A tuple of table-level constraints and indexes applied to the
table — the home of `UniqueConstraint`, `CheckConstraint`, and `Index`.
**Example**:
```python
__table_args__ = (
    CheckConstraint("score >= 0.0", name="ck_score"),
    Index("ix_model", "model"),
)
```
**Related**: UniqueConstraint, CheckConstraint, Index

### UniqueConstraint
**Definition**: Values in the column (or composite columns) must be unique —
enforced by the DB, which raises `IntegrityError` on violation. The last line
of defense against duplicate rows.
**Example**:
```python
class ModelVersion(Base):
    __tablename__ = "model_versions"
    model_name: Mapped[str] = mapped_column(String(60))
    version: Mapped[int] = mapped_column(default=1)
    __table_args__ = (
        UniqueConstraint("model_name", "version", name="uq_model_version"),
    )
```
**Related**: IntegrityError, CheckConstraint

## Key Concepts Summary

### The 2.0 Typed Style
- `Mapped[T]` declares the type once; `mapped_column()` configures it
- `Mapped[Optional[T]]` is the NULL-able column
- The annotation is the single source of truth for Python and the DB

### Constraints Are Database Business
- unique / NOT NULL / CHECK are enforced by the DB, not by Python
- `__table_args__` hosts table-level constraints and indexes
- `IntegrityError` is the DB saying no

### Verification Workflow
- `Base.metadata.create_all(engine)` builds the schema
- `inspect(engine)` reflects it back for verification

## Practice Terms

Match each term to its definition (answers at the bottom).

1. DeclarativeBase — ___
2. IntegrityError — ___
3. Optional — ___
4. __table_args__ — ___
5. ForeignKey — ___
6. Index — ___

A) NULL-able column annotation
B) The 2.0 base every mapped model inherits
C) Home of table-level constraints and indexes
D) The DB rejecting a write
E) Accelerates lookups on columns
F) A column referencing another table's column

**Answers:** 1-B, 2-D, 3-A, 4-C, 5-F, 6-E
