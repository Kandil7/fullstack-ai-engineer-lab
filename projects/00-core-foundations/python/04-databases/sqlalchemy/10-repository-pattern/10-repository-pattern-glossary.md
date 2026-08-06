# Repository Pattern — Glossary 10

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| @runtime_checkable | Protocol | Makes isinstance() work with structural typing |
| boundary | Architecture | The seam between application logic and persistence |
| concrete dependency | Anti-pattern | Code tied to a specific engine/class — untestable at unit level |
| domain logic | Architecture | Pure rules about entities: when to promote, what is best |
| facade | Architecture | A single object exposing only the needed operations |
| flush-not-commit | Practice | WRITE operations persist rows but leave transactions open |
| InMemoryRepository | Test double | Repository backed by dicts — unit tests without a DB |
| isolation of concerns | Architecture | One layer per job: model / repository / service |
| optimistic conflict | Pattern | A change rejected when the version changed (staleness) |
| Protocol | Typing | Structural interface: any object with these methods satisfies it |
| repository | Architecture | The persistence abstraction between service and DB |
| runtime checking | Typing | isinstance(obj, Repo) works for structurally-matched objects |
| service | Architecture | The layer holding domain logic, using the repository |
| SqlRepository | Production | Repository over SQLAlchemy: flush, never commit |
| structural typing | Typing | Duck typing checkable by the type checker |
| transaction boundary | Architecture | Where commits happen — at the service, never inside the repo |
| unit-of-work | Architecture | One session/transaction per logical operation |

## Detailed Definitions

### @runtime_checkable
**Definition**: Protocol decorator enabling `isinstance(obj, Protocol)` at
runtime, not just static typing.
**Example**:
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class ExperimentRepository(Protocol):
    def add(self, experiment): ...
```
**Related**: Protocol, runtime checking

### boundary
**Definition**: The seam between application logic and persistence — the
repository interface. Swapping SQLite for Postgres means changing one class,
not the services.
**Related**: repository, service

### concrete dependency
**Definition**: An anti-pattern: a service importing the SQLAlchemy session
class directly. No unit test can run without a real DB.
**Related**: Protocol, InMemoryRepository

### domain logic
**Definition**: Pure rules about the entities — when an experiment is
promotable, which model is best. Lives in the service, not the repo.
**Example**:
```python
def should_promote(e) -> bool:
    return e.score >= 0.90 and e.status == "done"
```
**Related**: service, repository

### facade
**Definition**: A repository exposing only the operations the app needs
(add, get_by_id, top_per_model) — nothing else; no session leaks out.
**Related**: repository, boundary

### flush-not-commit
**Definition**: Repository WRITE methods call `session.flush()` to assign
IDs, but never `commit()` — commits belong to the transaction boundary.
**Example**:
```python
def add(self, experiment):
    self._session.add(experiment)
    self._session.flush()
    return experiment.id
```
**Related**: transaction boundary, unit-of-work

### InMemoryRepository
**Definition**: A repository over plain dicts implementing the same
Protocol — unit tests run in microseconds, no engine, no teardown.
**Example**:
```python
class InMemoryExperimentRepository:
    def __init__(self):
        self._store: dict[int, Experiment] = {}
```
**Related**: Protocol, concrete dependency

### isolation of concerns
**Definition**: One job per layer: models are data, repositories are
persistence, services are rules. Each layer testable on its own.
**Related**: boundary, service

### optimistic conflict
**Definition**: A rejected write when a row's version moved between read and
write — the repository raises instead of silently overwriting.
**Example**:
```python
result = session.execute(
    update(Experiment).where(
        Experiment.id == exp.id,
        Experiment.version == exp.version))
if result.rowcount == 0:
    raise OptimisticLockError(...)
```
**Related**: version bump (topic 08), unit-of-work

### Protocol
**Definition**: A structural interface: any object whose methods match
satisfies it — static duck typing. `@runtime_checkable` adds isinstance.
**Related**: @runtime_checkable, structural typing

### repository
**Definition**: The persistence abstraction between service and DB: the
service knows the interface, never the engine. The pattern's namesake.
**Related**: boundary, facade

### runtime checking
**Definition**: With `@runtime_checkable`, isinstance() works for objects
that match the Protocol structurally — in-memory and SQL repos are both
"the repository".
**Related**: Protocol, InMemoryRepository

### service
**Definition**: The layer holding domain logic: it accepts a repository,
executes rules, and calls repo methods. The only layer that may commit.
**Example**:
```python
def register_batch(self, items):
    try:
        self.repo.add_batch(items)
        self.repo.commit()
    except ValueError:
        self.repo.rollback()
        raise
```
**Related**: domain logic, repository

### SqlRepository
**Definition**: The production repository: SQLAlchemy session inside, flush
for writes, clean query construction — still never commits.
**Related**: flush-not-commit, repository

### structural typing
**Definition**: Compatibility by shape, not by inheritance — the type
checker accepts any object with the right methods; runtime checks require
`@runtime_checkable`.
**Related**: Protocol, runtime checking

### transaction boundary
**Definition**: The rule that commits happen at the service level (or the
request handler), never inside repository methods — repos join whatever
transaction is active.
**Related**: flush-not-commit, unit-of-work

### unit-of-work
**Definition**: One session and one transaction per logical operation — a
batch registers all-or-nothing because the repo participates in the
service's unit of work.
**Related**: transaction boundary, SqlRepository

## Key Concepts Summary

### The Layering
- model: data; repository: persistence; service: rules
- Protocol defines the seam; runtime_checkable makes it checkable
- commits belong to the transaction boundary, not the repo

### The Payoff
- InMemoryRepository: unit tests without a DB
- SqlRepository swapped freely; optimistic conflicts raise loudly
- services testable by injecting either implementation

## Practice Terms

Match each term to its definition (answers at the bottom).

1. repository — ___
2. Protocol — ___
3. flush-not-commit — ___
4. InMemoryRepository — ___
5. transaction boundary — ___
6. @runtime_checkable — ___

A) Persistence abstraction between service and DB
B) Structural interface checked by shape
C) Writes persist rows; commits happen elsewhere
D) Dict-backed repo for unit tests
E) Makes isinstance() work with Protocols
F) Commits happen at the service, never in the repo

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-F, 6-E
