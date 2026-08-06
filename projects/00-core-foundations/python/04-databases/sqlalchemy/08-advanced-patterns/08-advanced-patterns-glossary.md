# Advanced Patterns — Glossary 08

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| @validates | Mapping | Per-attribute hook: convert/coerce a value before it is stored |
| before_insert | Event | Runs after flush started; rows not yet written; mapper attr access safe |
| before_update | Event | Runs before UPDATE; enables version bumps |
| CompositeType | Type | A TypeDecorator made of two Python values (two DB columns) |
| computed property | Mapping | A Python `@property` derived from column values — not SQL |
| hybrid_property | Mapping | An attribute with Python logic on the object AND SQL on the column |
| json stored as TEXT | Type | JSON encoded to TEXT — searchable with LIKE, no SQLite JSON support |
| row_number() | SQL | Window function numbering rows within a partition |
| type_decorator | Type | Custom column type; serialize/receive methods do conversions |
| version bump | Pattern | Increment a version column on every UPDATE via event |
| window function | SQL | Aggregate-like computation over a row partition, per row |
| X-NotImplemented | Practice | Marker for a pattern NOT chosen (e.g., subquery dedup) |
| decorator chain | Mapping | Expression-level @property | expression decorated hybrid |
| metadata rollback | Event | Explicit 2.0 rollback after failed flush in listeners |
| OLD/NEW pattern | Type | Receiving side compares old vs new value |

## Detailed Definitions

### @validates
**Definition**: Per-attribute decorator run before flush: validate or coerce
the assigned value — the cheap way to normalize (e.g., strip whitespace).
**Example**:
```python
from sqlalchemy.orm import validates

@validates("name")
def validate_name(self, key, value):
    return value.strip()
```
**Related**: hybrid_property, @property

### before_insert
**Definition**: INSERT-triggered listener; runs after flush has started, so
you may set mapper attributes but not load. Rows are not written yet.
**Example**:
```python
@event.listens_for(Prompt, "before_insert")
def _bump(mapper, connection, target):
    target.id = f"prm-{uuid4().hex[:10]}"
```
**Related**: before_update, version bump

### before_update
**Definition**: UPDATE-triggered listener; the hook that bumps a version
column on every change — the materialized optimistic-lock token.
**Example**:
```python
@event.listens_for(Prompt, "before_update")
def _bump(mapper, connection, target):
    target.version += 1
```
**Related**: before_insert, version bump

### CompositeType
**Definition**: A TypeDecorator with two Python values; `bind_processor` maps
it to TWO columns, `result_processor` reassembles it.
**Example**:
```python
class PointType(TypeDecorator):
    impl = LargeBinary
    def bind_processor(self, dialect): ...
    def result_processor(self, dialect, coltype): ...
```
**Related**: type_decorator

### computed property
**Definition**: A plain Python `@property` computed from columns — lives only
in Python; there is NO matching SQL expression.
**Example**:
```python
@property
def file_name(self) -> str:
    return f"{self.stem}{self.extension}"
```
**Related**: hybrid_property

### hybrid_property
**Definition**: The dual-mode attribute: a Python function on instances, a
SQL expression on the class. Write Python for display; use the SQL side in
filters. Expression-level decorators chain from left to right.
**Example**:
```python
@hybrid_property
def is_leader(self) -> bool:
    return self.score >= 0.90

@is_leader.expression
def is_leader(cls):
    return cls.score >= 0.90
```
**Related**: computed property, decorator chain

### json stored as TEXT
**Definition**: JSON dict encoded to TEXT because SQLite lacks a JSON column
type: searchable with LIKE, lossless via json.dumps/loads in a TypeDecorator.
**Example**:
```python
class JsonType(TypeDecorator):
    impl = Text
    cache_ok = True
```
**Related**: type_decorator

### row_number()
**Definition**: The window function numbering rows within a partition —
`row_number() OVER (PARTITION BY model ORDER BY score DESC)` gives each
model's ranking; rank == 1 means best per model.
**Example**:
```python
rank = func.row_number().over(
    partition_by=Experiment.model, order_by=Experiment.score.desc())
```
**Related**: window function

### type_decorator
**Definition**: Custom column type: `bind_processor` (Python -> DB),
`result_processor` (DB -> Python), `impl` (the underlying column type),
`cache_ok=True` for 2.0 statement caching.
**Example**:
```python
from sqlalchemy.types import TypeDecorator, LargeBinary

class VectorType(TypeDecorator):
    impl = LargeBinary
    cache_ok = True
    def bind_processor(self, dialect):
        return lambda v: np.asarray(v, dtype=np.float32).tobytes()
    def result_processor(self, dialect, coltype):
        return lambda b: np.frombuffer(b, dtype=np.float32)
```
**Related**: json stored as TEXT, CompositeType

### version bump
**Definition**: The optimistic-lock token: a version column incremented in
`before_update`, then compared on UPDATE — staleness becomes visible.
**Example**:
```python
stmt = update(Experiment).where(Experiment.id == e.id, Experiment.version == v)
```
**Related**: before_update, before_insert

### window function
**Definition**: Computes over a window of rows (`PARTITION BY` +
`ORDER BY`) but returns one value per row — the basis of per-group ranking.
**Related**: row_number()

### X-NotImplemented
**Definition**: The explicit marker in docs/solution for a pattern considered
and rejected (e.g., a dedup subquery) — the difference between an abandoned
design and a decided one.
**Related**: design-alternatives

### decorator chain
**Definition**: Expression-level decorators compose left to right:
`@a.expression` over `@b.expression` over the property — the outer-most
decorator's code runs first when applying SQL.
**Related**: hybrid_property

### metadata rollback
**Definition**: Calling `Session.rollback()` from inside an ORM event listener
(2.0 explicit control); automatic begin no longer suffices for listeners.
**Related**: before_update, version bump

### OLD/NEW pattern
**Definition**: A TypeDecorator receiving side comparing the incoming value
against the previous one — computing a delta (e.g., a diff) instead of
re-storing the whole value.
**Related**: type_decorator

## Key Concepts Summary

### Two Kinds of Python Logic
- object-level: @property, @validates — no SQL
- hybrid_property: Python on instances, SQL on the class

### Custom Types
- TypeDecorator: bind/result processors around an impl
- JSON-as-TEXT for SQLite; float32 bytes for embeddings
- `cache_ok=True` is mandatory for 2.0 caching

### Events
- before_insert/update: mutate target attributes, rollback explicitly
- window functions: per-group ranking without GROUP BY loss

## Practice Terms

Match each term to its definition (answers at the bottom).

1. hybrid_property — ___
2. row_number() — ___
3. TypeDecorator — ___
4. before_update — ___
5. @validates — ___
6. version bump — ___

A) Custom column type with bind/result processors
B) Attribute with Python logic on instances AND SQL on the class
C) Window function for per-partition ranking
D) Per-attribute hook that coerces values before storage
E) Increment a version column via event
F) Runs before UPDATE — the version-bump hook

**Answers:** 1-B, 2-C, 3-A, 4-F, 5-D, 6-E
