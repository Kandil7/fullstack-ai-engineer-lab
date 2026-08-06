# Databases (SQLAlchemy) — 08: Advanced Patterns

## Topic Overview

Beyond CRUD, real services need three advanced SQLAlchemy features. **Hybrid
properties** express one business rule in two contexts — Python instance
access and SQL WHERE clauses — so filtering and logic never drift.
**Custom types** (`TypeDecorator`) hide binary encoding behind a Python type:
embedding vectors stored as raw float32 bytes load back as `list[float]` with
no conversion code at the call site. **Optimistic locking** guards concurrent
writes: a `version` column, bumped by a `before_update` event, lets a stale
client write fail loudly instead of silently overwriting.

For AI/backend engineers these are the patterns that make metadata stores
production-grade: a model registry promoting only leaders, an embedding store
that round-trips vectors byte-exactly, and experiment updates that refuse
stale versions. This lecture covers all three, plus bulk operations and
`INSERT ... RETURNING`.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define a `hybrid_property` with matching Python and SQL expressions
2. Use the hybrid in both instance access and `where()` clauses
3. Write a `TypeDecorator` with `bind_processor`/`result_processor`
4. Store and load a vector embedding as raw bytes, byte-exact
5. Bump a `version` column with a `before_update` event
6. Implement optimistic updates that refuse stale versions
7. Use `insert().returning()` to get generated values in one round trip
8. Rank rows with `row_number() OVER (PARTITION BY ...)` in one query
9. Choose bulk operations (`bulk_insert_mappings`) for hot write paths
10. Recognize when SQL-side logic beats Python-side logic

---

## Prerequisites

| Need | Where |
|---|---|
| Session lifecycle | `03-session-lifecycle-lecture.md` |
| select() and aggregates | `05-querying-2.0-lecture.md` |
| events background | `06-eager-loading-and-n-plus-one-lecture.md` (event listener) |

---

## 1. Hybrid Properties: One Rule, Two Contexts

A hybrid property defines the SAME rule twice: the instance method runs in
Python; the `@is_leader.expression` body compiles into SQL. If they drift,
filtering and business logic disagree — so keep both bodies in lockstep.

```python
from sqlalchemy.ext.hybrid import hybrid_property

class Experiment(Base):
    __tablename__ = "experiments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    model: Mapped[str] = mapped_column(String(40), nullable=False)
    score: Mapped[float] = mapped_column(default=0.0)
    version: Mapped[int] = mapped_column(default=1)

    @hybrid_property
    def is_leader(self) -> bool:
        return self.score >= 0.90

    @is_leader.expression
    def is_leader(cls) -> bool:
        return cls.score >= 0.90
```

Instance access uses the Python method; queries use the SQL expression:

```python
with new_session() as session:
    exp = Experiment(name="bert-run-1", model="bert", score=0.92)
    session.add(exp); session.commit()
    print(f"instance is_leader: {exp.is_leader}")
# Output:
# instance is_leader: True

with new_session() as session:
    leaders = session.scalars(select(Experiment).where(Experiment.is_leader)).all()
    print(f"sql is_leader count: {len(leaders)}")
# Output:
# sql is_leader count: 1
```

## 2. Custom Types: Embeddings as Bytes

ML payloads (embedding vectors) are not scalars. A `TypeDecorator` wraps the
storage type (`LargeBinary`) and defines the Python <-> DB conversion:
`list[float] <-> float32 bytes`. The ORM then stores and loads vectors
transparently.

```python
import array
from sqlalchemy.types import LargeBinary, TypeDecorator

class VectorType(TypeDecorator):
    """Stores an embedding (list[float]) as raw float32 bytes."""

    impl = LargeBinary
    cache_ok = True

    def __init__(self, dim: int = 8) -> None:
        self.dim = dim
        super().__init__()

    def bind_processor(self, dialect):
        def to_bytes(value: list[float] | None) -> bytes | None:
            if value is None:
                return None
            return array.array("f", value).tobytes()
        return to_bytes

    def result_processor(self, dialect, coltype):
        def to_list(raw: bytes | None) -> list[float] | None:
            if raw is None:
                return None
            return list(array.array("f", raw))
        return to_list

class Embedding(Base):
    __tablename__ = "embeddings"
    id: Mapped[int] = mapped_column(primary_key=True)
    chunk_id: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    vector: Mapped[list[float] | None] = mapped_column(VectorType(dim=8))
```

Chosen over JSON text: fixed 4*N bytes per row, directly consumable by
vector-search code, no parsing. The round trip is byte-exact for values that
float32 represents exactly (0.25, 0.5, 1.0) and approximate for the rest.

## 3. Events: Optimistic Versioning

`before_update` fires inside the flush, in the same transaction. The pattern
here is optimistic locking: every UPDATE bumps the `version` column, so a
stale client write can be detected by comparing versions.

```python
from sqlalchemy import event

@event.listens_for(Experiment, "before_update")
def _bump_version(mapper, connection, target) -> None:
    target.version += 1
```

The guard then reads the row, checks the version, and refuses stale writes:

```python
def update_if_version(session, experiment_id: int, expected_version: int,
                      new_score: float) -> bool:
    exp = session.get(Experiment, experiment_id)
    if exp is None or exp.version != expected_version:
        return False
    exp.score = new_score
    session.commit()   # before_update bumps version in the same tx
    return True
```

A stale client (version 1 after someone else updated to 2) gets `False` — no
silent overwrite.

## 4. INSERT ... RETURNING and Bulk Operations

`insert().returning()` fetches generated values (ids, defaults) in the same
round trip. Bulk mappings bypass the unit of work for speed — at the cost of
bypassing the identity map and events.

```python
from sqlalchemy import insert

with Session(bind=engine) as session:
    stmt = insert(Experiment).values(name="bulk-run", model="bert", score=0.5)
    stmt = stmt.returning(Experiment.id)
    new_id = session.execute(stmt).scalar_one()
    session.commit()
    print(f"returned id: {new_id}")
# Output:
# returned id: 5
```

Use `bulk_insert_mappings`/`bulk_update_mappings` for hot write paths where
identity map bookkeeping is pure overhead — and remember they do not update
already-loaded objects.

## 5. Window Functions: Rank Inside the Database

`row_number() OVER (PARTITION BY model ORDER BY score DESC)` ranks rows within
each model family in SQL — one query, scales with the DB, instead of sorting
in Python.

```python
from sqlalchemy import func

def top_per_model(session: Session, k: int = 1) -> list[tuple[str, str, float]]:
    rank = (
        func.row_number()
        .over(partition_by=Experiment.model, order_by=Experiment.score.desc())
        .label("rk")
    )
    ranked = select(Experiment.name, Experiment.model, Experiment.score, rank).subquery()
    stmt = (
        select(ranked.c.name, ranked.c.model, ranked.c.score)
        .where(ranked.c.rk <= k)
        .order_by(ranked.c.model, ranked.c.rk)
    )
    return [(n, m, s) for n, m, s in session.execute(stmt)]
```

The subquery holds the ranking; the outer SELECT filters `rk <= k`. This is
the "top run per model family" query that registry dashboards use daily.

## 6. Production Pattern: Ranked Leaderboard + Version Guard

The shipping shape: a query function returning the top run per model family,
plus a version-guarded update that refuses stale writes. Both are deterministic
and testable — and both are exactly what Challenge 08 verifies.

---

## Common Mistakes to Avoid

### Mistake 1: Hybrid with different Python/SQL logic
```
# WRONG — Python says >=, SQL says >; filtering and logic disagree
def is_leader(self): return self.score > 0.9
@is_leader.expression
def is_leader(cls): return cls.score >= 0.9
# CORRECT — one threshold constant used by both bodies
```

### Mistake 2: Assuming bulk operations touch the identity map
```
# WRONG — exp stays stale after bulk_update_mappings
exp = session.get(Experiment, 1); session.bulk_update_mappings([...])
# CORRECT — bulk ops bypass the session; expire/refresh to re-read
```

### Mistake 3: Version checks only in application code
```
# WRONG — check-then-write has a race window between read and UPDATE
# CORRECT — WHERE id=? AND version=? in the UPDATE (the event bumps version
#   so a stale client's write fails loudly)
```

### Mistake 4: JSON for embeddings
```
# WRONG — text blobs, parsing cost, no binary compatibility
vector: Mapped[list[float]] = mapped_column(JSON)
# CORRECT — fixed 4*N bytes, indexable, direct binary consumption
vector: Mapped[list[float] | None] = mapped_column(VectorType(dim=8))
```

### Mistake 5: Sorting in Python instead of SQL for rankings
```
# WRONG — O(n log n) in Python, works only in-process
top = sorted(experiments, key=lambda e: e.score, reverse=True)[:k]
# CORRECT — row_number() in SQL; ranks at the database
```

---

## Best Practices

1. Keep hybrid Python/SQL bodies byte-identical (share a constant)
2. Choose binary column types for vectors; JSON only for ragged metadata
3. Use `before_update` events for cross-cutting version/audit logic
4. Guard every mutating endpoint with a version check where staleness matters
5. Prefer `insert().returning()` over a follow-up SELECT for generated ids
6. Reach for bulk mappings only on measured hot paths; know what you give up
7. Rank with window functions in SQL — never materialize to sort in Python
8. Name events and constraints so behavior is discoverable
9. Test round trips with exact and approximate float expectations
10. Keep advanced patterns behind small, documented functions

---

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| hybrid expression in WHERE | O(log n) with index | O(1) | — (SQL-side is the point) |
| TypeDecorator bind/result | O(dim) per row | O(dim) | — |
| version-bumped update | O(1) | O(1) | DB triggers, less portable |
| window function rank | O(n log n) | O(partitions) | Python sort, worse at scale |
| insert().returning() | 1 round trip | O(1) | 2 round trips without it |

**Cost note:** each avoided round trip matters at scale — `returning()`
halves the cost of insert-then-read-id. Window functions keep ranking in the
database where the data lives.

---

## AI Engineering Relevance

**Where this shows up:** the model registry (promote leaders), the embedding
store (vector round trips), the experiment tracker (concurrent run updates),
and every dashboard's "top run per model" panel.

| Concept here | Used for |
|---|---|
| hybrid is_leader | filtering leaders in SQL and Python identically |
| VectorType | storing chunk embeddings as binary |
| version bump + guard | concurrent experiment updates without lost writes |
| row_number() | top-1-per-model leaderboards |

**Scale note:** at 1M embeddings, binary vectors keep rows at 4*N bytes and
search libraries can mmap them. At 200 concurrent experiment updates, the
version guard is what stops last-writer-wins from silently discarding work.

---

## Practice Exercises

### Exercise 1: Hybrid in a WHERE (Difficulty: Easy)
Query all leader experiments using `Experiment.is_leader` in the WHERE.
Cross-check each returned row's Python `is_leader`.

### Exercise 2: Vector Round Trip (Difficulty: Easy)
Store `[0.25, 0.5, 0.75, 1.0]` and load it back. Assert exact equality.
Then store `[0.1, 0.2, 0.3]` and check it with `pytest.approx`.

### Exercise 3: Version Bump (Difficulty: Medium)
Update an experiment twice through `update_if_version`. After each success,
read the version and confirm it advanced by exactly 1.

### Exercise 4: Stale Write Refused (Difficulty: Medium)
Update once, then attempt an update with the OLD version. Confirm `False` and
that the score is unchanged.

### Exercise 5: Top-K Per Model (Difficulty: Hard)
Seed 4 experiments across 2 models. Implement `top_per_model(session, 2)` with
`row_number()`. Verify ordering per model and the `k` filter. (Challenge 08
tests this.)

---

## Summary

| Concept | Description |
|---|---|
| hybrid_property | one rule, Python and SQL contexts, no drift |
| TypeDecorator | custom column type; vectors as bytes |
| before_update event | automatic version bumping |
| optimistic locking | refuse stale writes with version guards |
| insert().returning() | generated ids in one round trip |
| row_number() OVER | SQL-side ranking per partition |

These patterns are the production polish: promotion logic that cannot drift,
vectors that store compactly, and writes that refuse to clobber each other.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Hybrid rule | `@hybrid_property` + `@is_leader.expression` |
| Custom type | `class VectorType(TypeDecorator)` with `bind_processor`/`result_processor` |
| Version bump | `@event.listens_for(M, "before_update")` |
| Stale guard | check `version == expected`, then mutate + commit |
| Get generated id | `insert(M).returning(M.id)` |
| Rank per group | `func.row_number().over(partition_by=..., order_by=...)` |

---

## Next Steps

Next: **[09 — Testing with a Database](09-testing-with-db-lecture.md)** —
make DB-backed tests isolated, repeatable, and fast.

Continues in: **[Phase 05 — Databases](../../05-web-frameworks/fastapi/19-orm.py)** —
advanced patterns inside a FastAPI service.

Official docs:
- Hybrids: https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html
- TypeDecorator: https://docs.sqlalchemy.org/en/20/core/custom_types.html
- Events: https://docs.sqlalchemy.org/en/20/orm/events.html
