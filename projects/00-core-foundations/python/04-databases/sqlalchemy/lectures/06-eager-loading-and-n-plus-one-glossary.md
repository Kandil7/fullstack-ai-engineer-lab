# Eager Loading and the N+1 Problem — Glossary 06

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| before_cursor_execute | Event | Fires before every SQL statement; used to count queries |
| eager loading | Loading | Loading related rows in the same statement batch |
| identity map | Session | One row -> one object; loaded children are cached |
| InvalidRequestError | Error | Raised by lazy="raise" on accidental lazy access |
| joinedload | Loading | Loads children in ONE query via LEFT OUTER JOIN |
| lazy loading | Loading | Default: children fetched on first attribute access |
| lazy="raise" | Loading | Relationship config that turns lazy access into an exception |
| N+1 problem | Performance | 1 query for parents + N queries for children |
| QueryCounter | Tooling | Event listener that counts statements on an engine |
| row duplication | Performance | Parent rows repeated once per child in a JOIN result |
| selectinload | Loading | Loads children in ONE extra IN(...) query: 2 total |
| subqueryload | Loading | Loads children via a derived-table JOIN: 2 queries |
| unique() | Loading | Dedupes parent rows after a collection JOIN |
| options() | Loading | Attaches loader strategies to a statement |
| round trip | Performance | One statement sent to the DB and answered |
| loader strategy | Loading | How a relationship is populated: lazy/selectin/joined/subquery |

## Detailed Definitions

### before_cursor_execute
**Definition**: A SQLAlchemy engine event that fires just before every cursor
execute — the hook that makes query counting honest.
**Example**:
```python
from sqlalchemy import event

def count(conn, cursor, statement, parameters, context, executemany):
    queries.append(statement)

event.listen(engine, "before_cursor_execute", count)
```
**Complexity**: O(1) per statement.
**Related**: QueryCounter, round trip

### eager loading
**Definition**: Loading related rows together with the parent — one or two
statements instead of 1 + N. The N+1 fix.
**Related**: selectinload, joinedload, subqueryload

### identity map
**Definition**: The session's cache: once children are loaded, later access
costs nothing. It can also *mask* N+1 if you reuse one session — reset the
query counter right before the code under test.
**Related**: selectinload, QueryCounter

### InvalidRequestError
**Definition**: The exception `lazy="raise"` raises when an unloaded
relationship is touched — the loud failure that replaces silent N+1.
**Example**:
```python
from sqlalchemy.exc import InvalidRequestError
try:
    _ = project.experiments   # lazy="raise" configured
except InvalidRequestError:
    print("lazy access rejected")
# Output:
# lazy access rejected
```
**Related**: lazy="raise", lazy loading

### joinedload
**Definition**: Loads children in ONE query with a LEFT OUTER JOIN. Requires
`.unique()` for collections; the JOIN fans out parent rows.
**Example**:
```python
from sqlalchemy.orm import joinedload
projects = session.scalars(
    select(Project).options(joinedload(Project.experiments))
).unique().all()
```
**Complexity**: 1 query; O(parents x children) rows transferred.
**Related**: row duplication, unique()

### lazy loading
**Definition**: The default strategy: children are fetched with a query on
first attribute access. One extra query per child — the seed of N+1.
**Related**: N+1 problem, loader strategy

### lazy="raise"
**Definition**: Relationship configuration making lazy access raise
`InvalidRequestError` — the model-level guard that turns accidental N+1 into
a test failure anywhere in the codebase.
**Example**:
```python
experiments: Mapped[list["Experiment"]] = relationship(
    back_populates="project", lazy="raise"
)
```
**Related**: InvalidRequestError, loader strategy

### N+1 problem
**Definition**: 1 + N queries: one for the parents, then one per parent for
children. Turns a 5 ms listing into a 500 ms one.
**Example**:
```python
for project in projects:            # 1 parent query
    _ = len(project.experiments)    # N child queries
```
**Complexity**: O(N) round trips.
**Related**: round trip, eager loading

### QueryCounter
**Definition**: A listener class wrapping `before_cursor_execute` to count
statements — the measurement tool that makes N+1 visible and regression tests
possible.
**Example**:
```python
counter = QueryCounter(engine)
counter.reset()
solution.load_projects(session)
assert counter.count() == 2
```
**Related**: before_cursor_execute, round trip

### row duplication
**Definition**: With a collection JOIN, each parent row repeats once per
child (4 parents x 3 runs = 12 rows). `unique()` restores one row per parent.
**Related**: joinedload, unique()

### selectinload
**Definition**: Loads children in one extra `WHERE parent_id IN (...)` query:
1 + 1 = 2 total. The default recommendation: no duplication, pagination-safe.
**Example**:
```python
from sqlalchemy.orm import selectinload
stmt = select(Project).options(selectinload(Project.experiments))
```
**Complexity**: 2 round trips.
**Related**: eager loading, loader strategy

### subqueryload
**Definition**: Wraps the parent query in a subquery and joins children
against that — 2 queries, JOIN against a small derived set. Niche.
**Related**: selectinload, joinedload

### unique()
**Definition**: Dedupes parent rows after a collection JOIN — mandatory with
`joinedload` of a collection; 2.0 `scalars()` does not apply it automatically.
**Example**:
```python
projects = session.scalars(stmt).unique().all()
```
**Related**: joinedload, row duplication

### options()
**Definition**: Attaches loader strategies to a statement:
`.options(selectinload(Project.experiments))`.
**Related**: selectinload, joinedload, subqueryload

### round trip
**Definition**: One statement sent to the database and answered. Round trips
dominate latency — N+1 is an O(N) round-trip disease.
**Related**: N+1 problem, QueryCounter

### loader strategy
**Definition**: How a relationship is populated: lazy, selectin, joined,
subquery, raise. Set per-query with `options()` or per-relationship with
`lazy=`.
**Related**: lazy loading, selectinload, lazy="raise"

## Key Concepts Summary

### The Problem
- lazy traversal = 1 + N queries
- round trips dominate latency; N is the multiplier
- measured with before_cursor_execute listeners

### The Fixes
- selectinload: 2 queries, the default
- joinedload: 1 query, needs unique()
- subqueryload: 2 queries, niche

### The Guards
- lazy="raise" turns accidental lazy access into InvalidRequestError
- query-count assertions make regression impossible silently

## Practice Terms

Match each term to its definition (answers at the bottom).

1. N+1 problem — ___
2. selectinload — ___
3. joinedload — ___
4. unique() — ___
5. lazy="raise" — ___
6. QueryCounter — ___

A) 1 parent query + N child queries
B) Loads children in one IN(...) query (2 total)
C) Loads children in one JOIN query (1 total)
D) Dedupes parent rows after a collection JOIN
E) Turns accidental lazy access into an exception
F) Counts statements via before_cursor_execute

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F
