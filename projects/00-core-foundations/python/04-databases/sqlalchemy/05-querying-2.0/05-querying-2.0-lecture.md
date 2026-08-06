# Databases (SQLAlchemy) — 05: Querying with select() (2.0 Style)

## Topic Overview

Reading data is where services live: "show me the best experiment for model
X", "which eval runs failed last week", "paginate the model registry". The
2.0 `select()` API is how those reads are shaped — typed, composable,
dialect-safe, and free of string SQL. The two result APIs matter: `scalars()`
unwraps ORM objects, `execute()` returns `Row` objects for projections and
aggregates. Joining with `.join()`/`.outerjoin()`, aliasing a table to itself,
and paginating with keyset cursors instead of OFFSET are the everyday skills.

For AI/backend engineers this is the read path of every registry, feature
store, and eval dashboard. The difference between `execute()` and `scalars()`,
or between OFFSET and keyset pagination, is the difference between a five-line
endpoint and a database-wide scan.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build a `select()` statement and read ORM objects with `session.scalars()`
2. Compose filters with `where()`, `in_`, `like`, `and_`, `or_`
3. Choose `execute()` over `scalars()` for projections and aggregates
4. Aggregate with `func.count`, `func.max`, `func.avg` and `group_by`
5. Join tables with `.join()` (FK inference) and `.outerjoin()`
6. Self-join with `aliased()` for parent/child and duplicate detection
7. Paginate with `limit().offset()` and know when it stops scaling
8. Implement keyset (seek) pagination on an indexed cursor
9. Use `tuple_` row-value comparisons for multi-column cursors
10. Debug the scalars/execute confusion and the join-multiplies-rows trap

---

## Prerequisites

| Need | Where |
|---|---|
| Models and relationships | `02-declarative-models-lecture.md`, `04-relationships-lecture.md` |
| Session basics | `03-session-lifecycle-lecture.md` |
| Core `select`/`text` | `01-core-vs-orm-lecture.md` |

---

## 1. select() and scalars(): the 2.0 Read Path

`select(Experiment)` builds a SELECT; `session.scalars(stmt)` returns the ORM
objects directly. This is the bread-and-butter read: one statement, typed
objects, zero string SQL.

```python
from sqlalchemy import ForeignKey, String, and_, func, or_, select, tuple_
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, aliased, mapped_column

class Base(DeclarativeBase):
    pass

class Experiment(Base):
    __tablename__ = "experiments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    model: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(12), default="running")

class EvalMetric(Base):
    __tablename__ = "eval_metrics"
    id: Mapped[int] = mapped_column(primary_key=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"), nullable=False)
    metric: Mapped[str] = mapped_column(String(30), nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)

with Session(bind=engine) as session:
    stmt = select(Experiment).order_by(Experiment.name)
    for exp in session.scalars(stmt).all():
        print(f"{exp.name}: {exp.model} [{exp.status}]")
# Output:
# bert-finetune-1: bert [done]
# bert-finetune-2: bert [running]
# gpt-finetune-1: gpt2 [done]
```

## 2. Filters: where(), in_, like, and_/or_

`.where()` composes with AND automatically; alternatives compose with
`or_()`; negation with `~`. Everything compiles to bound parameters — never
f-strings.

```python
with Session(bind=engine) as session:
    stmt = select(Experiment).where(Experiment.status.in_(["done", "archived"]))
    print(f"done/archived: {len(session.scalars(stmt).all())}")
# Output:
# done/archived: 2

with Session(bind=engine) as session:
    stmt = select(Experiment).where(
        and_(Experiment.model == "bert", Experiment.name.like("bert-%"))
    )
    print([e.name for e in session.scalars(stmt).all()])
# Output:
# ['bert-finetune-1', 'bert-finetune-2']

with Session(bind=engine) as session:
    stmt = select(Experiment).where(
        or_(Experiment.status == "running", Experiment.model == "gpt2")
    )
    print([e.name for e in session.scalars(stmt).all()])
# Output:
# ['bert-finetune-2', 'gpt-finetune-1']
```

## 3. execute() vs scalars(): Row vs Object

`session.execute(stmt)` returns `Row` objects — indexable by position and by
column name. Reach for it when the query has no ORM entity: projections and
aggregates. `scalars()` unwraps single-column results into values or objects.

```python
with Session(bind=engine) as session:
    stmt = select(Experiment.name, Experiment.status).order_by(Experiment.name)
    rows = session.execute(stmt).all()
    first = rows[0]
    print(f"row type: {type(first).__name__}; name via key: {first.name}")
# Output:
# row type: Row; name via key: bert-finetune-1
```

## 4. Aggregates: join, filter, group, order

The join multiplies rows — one output row per matched metric — so
`count(Experiment.id)` after a join counts *metric* rows. Narrow to one metric
before aggregating to keep the numbers meaningful.

```python
with Session(bind=engine) as session:
    stmt = (
        select(Experiment.model, func.count(Experiment.id), func.avg(EvalMetric.value))
        .join(EvalMetric, EvalMetric.experiment_id == Experiment.id)
        .where(EvalMetric.metric == "f1")
        .group_by(Experiment.model)
        .order_by(Experiment.model)
    )
    for model, f1_rows, avg_f1 in session.execute(stmt):
        print(f"{model}: {f1_rows} f1 rows, avg f1 = {avg_f1:.3f}")
# Output:
# bert: 2 f1 rows, avg f1 = 0.850
# gpt2: 1 f1 rows, avg f1 = 0.930
```

## 5. Joins: join() and outerjoin()

`.join(Target)` infers the ON clause from the foreign key. `.outerjoin()`
keeps left rows that have no match — every experiment, metric or not.

```python
with Session(bind=engine) as session:
    stmt = select(Experiment).join(EvalMetric).distinct().order_by(Experiment.name)
    print([e.name for e in session.scalars(stmt).all()])
# Output:
# ['bert-finetune-1', 'bert-finetune-2', 'gpt-finetune-1']

with Session(bind=engine) as session:
    stmt = (
        select(Experiment.name, func.count(EvalMetric.id))
        .outerjoin(EvalMetric)
        .group_by(Experiment.id)
        .order_by(Experiment.name)
    )
    for name, metric_count in session.execute(stmt):
        print(f"{name}: {metric_count} metrics")
# Output:
# bert-finetune-1: 2 metrics
# bert-finetune-2: 1 metrics
# gpt-finetune-1: 2 metrics
```

## 6. aliased(): Joining a Table to Itself

Self-joins need two distinct references to the same class — `aliased()` creates
the second. This is how template trees and duplicate detection queries are
built (SQLite renders it as `prompt_templates AS pt_1`).

```python
class PromptTemplate(Base):
    __tablename__ = "prompt_templates"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("prompt_templates.id"))

with Session(bind=engine) as session:
    parent = aliased(PromptTemplate)
    stmt = (
        select(PromptTemplate.name, parent.name)
        .join(parent, PromptTemplate.parent_id == parent.id)
        .order_by(PromptTemplate.name)
    )
    for child_name, parent_name in session.execute(stmt):
        print(f"{child_name} inherits from {parent_name}")
# Output:
# de-rag inherits from base-rag
# en-rag inherits from base-rag
```

## 7. Pagination: OFFSET vs Keyset

`.limit(n).offset(m)` is the simple pager. It degrades at scale: `OFFSET
100000` means the database reads and discards 100,000 rows. **Keyset
pagination** filters on the last-seen row instead — each page costs
O(page_size), and pages stay stable when new rows arrive.

```python
def keyset_page(session: Session, after_id: int | None, size: int) -> list[Experiment]:
    stmt = select(Experiment).order_by(Experiment.id).limit(size)
    if after_id is not None:
        stmt = stmt.where(Experiment.id > after_id)
    return list(session.scalars(stmt).all())
```

The cursor is the last `(id)` seen; the next query is `WHERE id > :last_id
ORDER BY id LIMIT :size`. For multi-column cursors, `tuple_` row-value
comparison extends the same idea:

```python
cursor = (last_id, last_name)
stmt = select(Experiment).where(
    tuple_(Experiment.id, Experiment.name) > cursor
).order_by(Experiment.id, Experiment.name)
```

## 8. Production Pattern: Registry Listing + Leaderboard

The shipping shape for a registry endpoint: keyset-paginated listing (seek,
not offset) plus a join-then-filter leaderboard.

```python
def metric_leaders(session: Session, metric: str, min_value: float, limit: int
                   ) -> list[tuple[str, float]]:
    stmt = (
        select(Experiment.name, EvalMetric.value)
        .join(EvalMetric, EvalMetric.experiment_id == Experiment.id)
        .where(and_(EvalMetric.metric == metric, EvalMetric.value >= min_value))
        .order_by(EvalMetric.value.desc())
        .limit(limit)
    )
    return [(name, value) for name, value in session.execute(stmt)]
```

Both functions are deterministic, pageable, and run entirely in the database.

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting .scalars() and getting Rows
```
# WRONG — rows, not Experiment objects; exp.Experiment awkwardness
rows = session.execute(select(Experiment)).all()
# CORRECT
exps = session.scalars(select(Experiment)).all()
```

### Mistake 2: OFFSET pagination on a big registry
```
# WRONG — page 10000 reads and discards 200k rows
page = select(...).limit(20).offset(200_000)
# CORRECT — keyset cursor: WHERE id > :last ORDER BY id LIMIT 20
```

### Mistake 3: f-string values into .where()
```
# WRONG — injection risk and quoting bugs
stmt = select(Exp).where(Exp.name == f"{user}")
# CORRECT — bound parameters are automatic
stmt = select(Exp).where(Exp.name == user)
```

### Mistake 4: Aggregating after a join without narrowing
```
# WRONG — count(Experiment.id) counts METRIC rows after the join
select(Experiment.model, func.count(Experiment.id)).join(EvalMetric)
# CORRECT — filter to one metric first (or count distinct ids)
.where(EvalMetric.metric == "f1")
```

### Mistake 5: Forgetting .distinct() on join-driven object lists
```
# WRONG — each experiment repeats once per metric
select(Experiment).join(EvalMetric)
# CORRECT — dedupe the object list (or select names only)
select(Experiment).join(EvalMetric).distinct()
```

---

## Best Practices

1. Prefer `scalars()` for ORM objects; use `execute()` only for projections/aggregates
2. Compose filters declaratively; bound parameters are automatic
3. Narrow joins to the metric/filter you aggregate on, before grouping
4. Use `outerjoin` when left-side rows must survive
5. Self-join with `aliased()` and an explicit ON clause
6. Paginate with keyset; reserve OFFSET for tiny tables
7. Order explicitly; never rely on default row order
8. Return `Row`/tuples from query helpers — keep ORM objects internal
9. Add `.distinct()` deliberately — it costs a sort
10. Test query shapes against real data (challenge 05 does exactly this)

---

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| WHERE with index | O(log n) seek | O(1) | index on the filtered column |
| join (inner) | O(n log n) merge / O(n) hash | O(n) | index on the FK |
| OFFSET page m | O(m) discarded rows | O(1) | keyset: O(page_size) |
| keyset page | O(page_size) | O(1) | — |
| GROUP BY aggregate | O(n log n) | O(groups) | pre-aggregated tables |

**Cost note:** the pagination choice is the big one — OFFSET is O(total rows)
per page; keyset is O(page size). At 1M rows and page 50,000, that is the
difference between 1M reads and 20.

---

## AI Engineering Relevance

**Where this shows up:** the model registry listing (keyset pagination), the
eval leaderboard (join + filter + order + limit), "which runs failed this
week" (filter + date range), and the feature-store read path.

| Concept here | Used for |
|---|---|
| scalars/execute split | object CRUD vs dashboard aggregates |
| join + filter + group | per-model best F1, failure rates, latency p95 |
| aliased self-join | template inheritance trees, duplicate detection |
| keyset pagination | registry pages that stay fast and stable |

**Scale note:** at 1M experiments the difference between OFFSET and keyset is
a paging endpoint that dies vs one that stays flat. At 200 QPS of dashboard
queries, pre-aggregated summary tables beat live GROUP BY.

---

## Practice Exercises

### Exercise 1: Filtering Compositions (Difficulty: Easy)
Write a query returning names of experiments that are running OR named
`like "bert-%"`, ordered by name. Check the output against the seed data.

### Exercise 2: Aggregate Per Metric (Difficulty: Medium)
For each metric name, return (metric, avg(value)) across all experiments,
ordered by metric. Verify the join does not distort the average.

### Exercise 3: Outer Join Count (Difficulty: Medium)
Return every experiment with its metric count, including experiments with
zero metrics. Add one metric-less experiment and confirm it appears with 0.

### Exercise 4: Self-Join Tree (Difficulty: Medium)
Using `aliased(PromptTemplate)`, list every child with its parent name.
Add a grandchild and confirm it is excluded (it has no child row of its own).

### Exercise 5: Keyset vs Offset (Difficulty: Hard)
Seed 10,000 experiments. Compare `keyset_page` timing for page 1 vs page 500
against the OFFSET equivalent. Record both and explain the difference in SQL
terms. (No wall-clock assertions — just measure and reason.)

---

## Summary

| Concept | Description |
|---|---|
| `scalars()` | unwraps ORM objects from a select |
| `execute()` | Rows for projections and aggregates |
| filters | `where`, `in_`, `like`, `and_`, `or_` — always bound params |
| joins | `.join()` infers ON; `.outerjoin()` keeps left rows |
| `aliased()` | second reference to a class for self-joins |
| keyset pagination | cursor-based; O(page_size), stable pages |

The 2.0 select API is the read path of every registry and dashboard. With the
query shapes from this lecture, the eager-loading decisions of topic 06 —
which often replace join work — become clear.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Objects | `session.scalars(select(M).where(...)).all()` |
| Projection | `session.execute(select(M.a, M.b)).all()` |
| Aggregate | `select(func.max(M.x)).group_by(M.y)` |
| Inner join | `.join(Other)` (FK inferred) |
| Outer join | `.outerjoin(Other, Other.fk == M.id)` |
| Self-join | `p = aliased(M); .join(p, M.parent_id == p.id)` |
| Page (offset) | `.limit(20).offset(40)` — small tables only |
| Page (keyset) | `.where(M.id > last_id).order_by(M.id).limit(20)` |

---

## Next Steps

Next: **[06 — Eager Loading and the N+1 Problem](06-eager-loading-and-n-plus-one-lecture.md)** —
measure query counts and load relationships in 1-2 queries.

Continues in: **[Phase 05 — Databases](../../05-web-frameworks/fastapi/19-orm.py)** —
select() queries behind FastAPI endpoints.

Official docs:
- 2.0 select guide: https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
- ORM querying: https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html
- SQL expressions: https://docs.sqlalchemy.org/en/20/core/expression_api.html
