# Databases (SQLAlchemy) — 06: Eager Loading and the N+1 Problem (STAR)

## Topic Overview

The N+1 problem is the single most common performance defect in ORM-backed
services. It happens the moment you load a list of parents and then touch each
parent's children: the ORM fires one query for the parents and **N queries for
the children**. Listing 100 model versions lazily becomes 101 queries; in an ML
platform (registry listing, run explorer, eval matrix) the "one extra query per
row" pattern turns a 5 ms endpoint into a 500 ms one and the database into a
bottleneck.

This lecture does two things no tutorial usually does: it **measures** query
counts with a SQLAlchemy event listener, and it fixes N+1 with the three eager
loading strategies — `selectinload`, `joinedload`, `subqueryload` — and then
hardens the fix with `lazy="raise"` so accidental N+1 fails loudly in tests.
The exercise and challenge assert query counts in code, so the fix cannot
silently regress.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Recognize the N+1 pattern: 1 + N queries for N parents with lazy children
2. Measure SQL statement counts with `event.listen(engine, "before_cursor_execute", ...)`
3. Fix N+1 with `selectinload` (2 queries) and know why it is the default choice
4. Use `joinedload` (1 query) and apply `.unique()` for collection loads
5. Explain when `subqueryload` beats the alternatives
6. Configure `lazy="raise"` on relationships to turn N+1 into test failures
7. Set eager loading as a relationship *default*, not just per query
8. Predict query counts for a given options() combination
9. Choose the right strategy: SELECT IN vs JOIN vs SUBQUERY
10. Guard listings with query-count assertions in tests

---

## Prerequisites

| Need | Where |
|---|---|
| Relationships | `04-relationships-lecture.md` |
| select() queries | `05-querying-2.0-lecture.md` |
| Session identity map | `03-session-lifecycle-lecture.md` |

---

## 1. The N+1 Problem, Made Visible

Default loading is **lazy**: `.experiments` fires a query every time it is
touched on an unloaded instance. The measurement technique: SQLAlchemy fires
an event before every cursor execute; a listener counts statements — the honest
way to see what your ORM code really sends.

```python
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import (DeclarativeBase, Mapped, Session, joinedload,
                            mapped_column, relationship, selectinload, subqueryload)
from sqlalchemy.pool import StaticPool

class QueryCounter:
    def __init__(self, engine) -> None:
        self.queries: list[str] = []
        event.listen(engine, "before_cursor_execute", self._on_execute)

    def _on_execute(self, conn, cursor, statement, parameters, context, executemany):
        self.queries.append(statement)

    def count(self) -> int:
        return len(self.queries)

    def reset(self) -> None:
        self.queries = []

counter = QueryCounter(engine)

with new_session() as session:
    counter.reset()
    projects = session.scalars(select(Project).order_by(Project.id)).all()
    for project in projects:
        _ = len(project.experiments)   # ONE query per project
    print(f"lazy: {counter.count()} queries for 4 projects")
# Output:
# lazy: 5 queries for 4 projects
#   -> N+1: 5 = 1 (projects) + 4 (children)
```

For N parents, lazy traversal is 1 + N queries. That is the problem, measured.

## 2. selectinload: Children in ONE Extra Query

`selectinload` turns the per-child queries into a single
`WHERE project_id IN (...)` query: 1 + 1 = 2 total. It is the default
recommendation: no row duplication, works with pagination, simple.

```python
with new_session() as session:
    stmt = select(Project).options(selectinload(Project.experiments)).order_by(Project.id)
    projects = session.scalars(stmt).all()
    counter.reset()
    total_runs = sum(len(p.experiments) for p in projects)   # no SQL fired
    print(f"selectinload: {counter.count()} queries ({total_runs} runs loaded)")
# Output:
# selectinload: 0 queries (12 runs loaded)   [counted AFTER loading]
#   -> 1 (projects) + 1 (children IN ...)
```

When the counter is reset *after* the statement executes, traversal fires
zero extra queries — the whole graph is already in the identity map.

## 3. joinedload: ONE Query with a JOIN

`joinedload` emits a single SELECT with LEFT OUTER JOIN; children arrive in
the same result set. The cost: the parent row repeats once per child, so the
result must be de-duplicated with `.unique()` — SQLAlchemy 2.0 `scalars()`
does **not** apply it automatically for collection loads.

```python
with new_session() as session:
    stmt = select(Project).options(joinedload(Project.experiments)).order_by(Project.id)
    projects = session.scalars(stmt).unique().all()   # dedupe parent rows
    print(f"joinedload: {len(projects)} projects deduped")
# Output:
# joinedload: 4 projects deduped
```

Forget `.unique()` and the parent list contains one entry per child (4
projects x 3 runs = 12 rows). The JOIN can also be slow when the one side is
large, because every parent row is duplicated per child.

## 4. subqueryload: Children via a Derived Table

`subqueryload` wraps the parent query in a subquery and joins children against
*that* — 2 queries, but the JOIN is against a small derived set instead of the
full parent table. Rarely needed; `selectinload` is the modern default.

```python
with new_session() as session:
    stmt = select(Project).options(subqueryload(Project.experiments)).order_by(Project.id)
    projects = session.scalars(stmt).all()
    total_runs = sum(len(p.experiments) for p in projects)
    print(f"subqueryload: 2 queries ({total_runs} runs loaded)")
```

## 5. lazy= Strategies and lazy="raise"

The relationship default is `lazy="select"` (one query per access). Setting
`lazy="raise"` turns accidental lazy loading into an **exception** — the
standard trick to catch N+1 in tests. Joined and selectin can also be set as
relationship defaults, not just per-query options.

```python
class StrictProject(Base):
    __tablename__ = "strict_projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    experiments: Mapped[list["StrictExperiment"]] = relationship(
        back_populates="project", lazy="raise"
    )
```

Touching `.experiments` on an unloaded `StrictProject` raises
`InvalidRequestError` — the codebase fails loudly instead of degrading into
N+1.

## 6. Production Pattern: Batch-Loaded Listing

The shipping shape for a registry listing: one query with `selectinload`,
counted and asserted in tests.

```python
def fetch_projects_with_runs(session: Session) -> list[tuple[str, list[str]]]:
    stmt = select(Project).options(selectinload(Project.experiments)).order_by(Project.id)
    projects = session.scalars(stmt).all()
    return [(p.name, sorted(e.name for e in p.experiments)) for p in projects]
```

A test wraps this with the QueryCounter and asserts exactly 2 queries — the
guard that keeps the endpoint fast forever.

---

## Common Mistakes to Avoid

### Mistake 1: Touching lazy collections in a loop
```
# WRONG — 1 + N queries; the classic N+1
for project in projects:
    print(len(project.experiments))
# CORRECT — eager load once
projects = session.scalars(select(Project).options(selectinload(Project.experiments))).all()
```

### Mistake 2: joinedload without .unique()
```
# WRONG — every parent repeats once per child (row duplication)
projects = session.scalars(select(Project).options(joinedload(Project.experiments))).all()
# CORRECT — dedupe parent rows
projects = session.scalars(...).unique().all()
```

### Mistake 3: joinedload on a many-to-many (the row explosion)
```
# WRONG — parents x children x grandchildren rows
joinedload(Parent.children).joinedload(Child.grandchildren)
# CORRECT — one selectinload per level (2 queries, no explosion)
selectinload(Parent.children).selectinload(Child.grandchildren)
```

### Mistake 4: Relying on the identity map to hide N+1
```
# WRONG — "it worked in my test" (same session reused the objects)
# CORRECT — reset the counter right before the code under test, and use a
# fresh session so every load hits the database (exercise 06 does both)
```

### Mistake 5: Forgetting lazy="raise" in models you ship
```
# WRONG — N+1 stays silent until production traffic
experiments = relationship(back_populates="project")
# CORRECT — lazy="raise" on hot collections; explicit options() where eager
experiments = relationship(back_populates="project", lazy="raise")
```

---

## Best Practices

1. Default to `selectinload` — simple, no row duplication, pagination-safe
2. Use `joinedload` for many-to-one (no duplicate rows possible) and tiny collections
3. Always `.unique()` after `joinedload` of a collection
4. Set `lazy="raise"` on hot collections in models you ship
5. Assert query counts in tests for every listing endpoint
6. Prefer per-query options over changing relationship defaults globally
7. Measure with `before_cursor_execute` — never guess
8. Combine strategies: one `selectinload` per relationship level
9. Keep eager loads inside the session scope (detachment kills lazy fallback)
10. Document the expected count: `# 1 + 1 = 2 queries: parents + IN(...)`

---

## Complexity and Cost

| Strategy | Queries | Row duplication | Best for |
|---|---|---|---|
| lazy (default) | 1 + N | none | single object access, never in loops |
| `selectinload` | 2 | none | collections; the default choice |
| `joinedload` | 1 | parent x children | many-to-one; small collections |
| `subqueryload` | 2 | none | huge parent tables where JOIN fans out |
| `lazy="raise"` | 0 (throws) | none | enforcing eager-only access |

**Cost note:** N+1 is O(N) round trips — the same N that defeats a paginated
endpoint. Eager loading makes it O(1) round trips with O(N) row transfer. At
100 projects x 3 runs, that is 101 vs 2 queries; at 10,000 projects, 10,001
vs 2.

---

## AI Engineering Relevance

**Where this shows up:** the run explorer (project -> experiments), the eval
matrix (experiment -> metrics), the model registry (model -> versions), and
every list endpoint in an ML platform.

| Concept here | Used for |
|---|---|
| selectinload | registry listing pages with nested runs |
| joinedload | fetching one experiment with its project |
| lazy="raise" | making accidental N+1 a CI failure |
| query counting | performance regression tests |

**Scale note:** at 10,000 models, the difference between lazy (10,001 queries)
and selectin (2 queries) is the difference between an endpoint that times out
and one that returns in 20 ms. At 200 concurrent list requests, that is the
difference between a healthy DB and a connection-pool collapse.

---

## Practice Exercises

### Exercise 1: Count the Queries (Difficulty: Easy)
With the `QueryCounter`, load 4 projects and touch `.experiments` on each.
Record the count; verify it equals 1 + N.

### Exercise 2: Selectin vs Joined (Difficulty: Easy)
Run the same traversal with `selectinload` and `joinedload`. Record counts (2
vs 1) and result shapes (with and without `.unique()`).

### Exercise 3: Raise Guard (Difficulty: Medium)
Declare a `StrictProject` with `lazy="raise"`, load one, and confirm that
touching `.experiments` raises `InvalidRequestError`.

### Exercise 4: Nested Eager Loading (Difficulty: Medium)
Load projects with experiments and their metrics in exactly 3 queries using
chained `selectinload` options. Verify with the counter.

### Exercise 5: Regression Guard (Difficulty: Hard)
Write a test that asserts `fetch_projects_with_runs` fires exactly 2 queries,
then temporarily comment out the `.options(...)` line and confirm the test
fails. That failure is the guard working. (Challenge 06 tests this.)

---

## Summary

| Concept | Description |
|---|---|
| N+1 | 1 + N queries: parents + one query per child |
| QueryCounter | `before_cursor_execute` listener that counts statements |
| `selectinload` | 2 queries; the default fix |
| `joinedload` | 1 query; needs `.unique()` for collections |
| `subqueryload` | 2 queries via derived table; niche |
| `lazy="raise"` | turns accidental lazy access into an exception |

N+1 is the ORM tax on lazy traversal — and it is fully avoidable. Measure with
the counter, fix with eager loading, and guard with `lazy="raise"` plus
query-count assertions.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Measure queries | `event.listen(engine, "before_cursor_execute", listener)` |
| 2-query listing | `select(M).options(selectinload(M.children))` |
| 1-query fetch | `select(M).options(joinedload(M.child)).unique()` |
| Nested eager | `selectinload(A.bs).selectinload(B.cs)` |
| Enforce eager | `children = relationship(..., lazy="raise")` |

---

## Next Steps

Next: **[07 — Async SQLAlchemy](07-async-sqlalchemy-lecture.md)** — the same
patterns with `await` boundaries for async endpoints.

Continues in: **[Phase 05 — Databases](../../05-web-frameworks/fastapi/19-orm.py)** —
eager-loaded listings in a FastAPI service.

Official docs:
- Loading relationships: https://docs.sqlalchemy.org/en/20/orm/loading_relationships.html
- Relationship loaders API: https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html
- Events: https://docs.sqlalchemy.org/en/20/core/events.html
