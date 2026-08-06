# Databases (SQLAlchemy) — 10: Repository Pattern

## Topic Overview

The repository pattern separates **what** storage means from **how** it is
implemented. Business code talks to a `Protocol` — `add`, `get`, `list_all`,
`count`, `delete` — and the storage backend (a dict, a SQLAlchemy session, a
REST API, a mock) implements that contract. Domain rules stay pure functions
over plain data; repositories stay dumb persistence objects; a service layer
owns transactions. This is the architecture that makes an ML platform's
metadata store testable without a database and swappable without a rewrite.

For AI/backend engineers the pattern answers three daily questions: how do I
unit-test business logic without a DB (use the in-memory repository), how do I
keep the service layer decoupled from SQLAlchemy (depend on the Protocol), and
how do I make batch writes atomic (the Unit of Work owns commit/rollback)?
This lecture covers pure domain rules, the repository Protocol with
`runtime_checkable`, SQL and in-memory implementations, and the all-or-nothing
batch service.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Separate domain rules (pure functions) from persistence (repositories)
2. Define a storage contract with `Protocol` + `@runtime_checkable`
3. Implement an in-memory repository for unit tests
4. Implement a SQLAlchemy repository that flushes but never commits
5. Explain the Unit of Work: the caller owns the transaction
6. Build an all-or-nothing batch registration service
7. Verify structural typing with `isinstance(repo, Repository)`
8. Swap repositories without touching domain code
9. Predict duplicate-name behavior in both implementations
10. Test service logic against the in-memory backend in milliseconds

---

## Prerequisites

| Need | Where |
|---|---|
| Session lifecycle | `03-session-lifecycle-lecture.md` |
| select() queries | `05-querying-2.0-lecture.md` |
| Testing patterns | `09-testing-with-db-lecture.md` |

---

## 1. Domain Rules, Kept OUT of the ORM

Business rules are pure functions over plain data: no session, no SQL —
trivially unit-testable and reusable by any caller.

```python
PROMOTE_THRESHOLD = 0.9

def should_promote(score: float) -> bool:
    """Pure domain rule: is this run good enough to promote?"""
    return score >= PROMOTE_THRESHOLD

def best_model_name(experiments: list[Experiment]) -> str | None:
    """Pure domain query: name of the highest-scoring run, or None."""
    if not experiments:
        return None
    return max(experiments, key=lambda e: e.score).model
```

No import of `Session`, no database URL, no setup — `should_promote(0.9)` is
`True` and that is the whole test.

## 2. The Repository Interface

The contract every storage backend must honor. Domain code depends on THIS,
never on `Session` or `Experiment` details. `@runtime_checkable` lets
`isinstance()` work on structural typing.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class ExperimentRepository(Protocol):
    """Storage contract: how experiments are stored is an implementation detail."""

    def add(self, experiment: Experiment) -> int: ...
    def get(self, name: str) -> Experiment | None: ...
    def list_all(self) -> list[Experiment]: ...
    def count(self) -> int: ...
    def delete(self, name: str) -> bool: ...
```

Any class with these methods — dict-backed or SQL-backed — satisfies the
contract. Services can `isinstance(repo, ExperimentRepository)` to guard
dependency injection.

## 3. SQLAlchemy Implementation (Unit of Work Injected)

The repository takes a `Session` — it does **not** create or commit one. The
caller (a service, a request handler) owns the transaction: this is the Unit
of Work pattern. Repos stay composable: several repositories can share one
session/transaction.

```python
from sqlalchemy import select

class SqlExperimentRepository:
    """Repository backed by SQLAlchemy. Session = injected Unit of Work."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, experiment: Experiment) -> int:
        self.session.add(experiment)
        self.session.flush()   # assign the PK; commit stays with the caller
        return experiment.id

    def get(self, name: str) -> Experiment | None:
        return self.session.scalars(
            select(Experiment).where(Experiment.name == name)
        ).first()

    def list_all(self) -> list[Experiment]:
        return list(self.session.scalars(select(Experiment).order_by(Experiment.id)))

    def count(self) -> int:
        return len(self.session.scalars(select(Experiment.id)).all())

    def delete(self, name: str) -> bool:
        experiment = self.get(name)
        if experiment is None:
            return False
        self.session.delete(experiment)
        self.session.flush()
        return True
```

`add` flushes so the PK is assigned; nothing persists until the service
commits. That is the discipline that makes `register_batch_with_transaction`
possible below.

## 4. The In-Memory Implementation

For unit tests: a dict-backed repo with the same contract and the same
duplicate-name semantics. The service cannot tell the difference.

```python
class InMemoryExperimentRepository:
    """Repository backed by a plain dict (for unit tests)."""

    def __init__(self) -> None:
        self._store: dict[str, Experiment] = {}
        self._next_id = 1

    def add(self, experiment: Experiment) -> int:
        if experiment.name in self._store:
            raise ValueError(f"duplicate experiment name: {experiment.name}")
        experiment.id = self._next_id
        self._next_id += 1
        self._store[experiment.name] = experiment
        return experiment.id

    def get(self, name: str) -> Experiment | None:
        return self._store.get(name)

    def list_all(self) -> list[Experiment]:
        return list(self._store.values())

    def count(self) -> int:
        return len(self._store)

    def delete(self, name: str) -> bool:
        return self._store.pop(name, None) is not None
```

Duplicate name raises `ValueError` — the same outcome the SQL repo produces
via `IntegrityError` (which the service normalizes).

## 5. The Service Layer: Unit of Work in Action

The service owns the transaction. Batch registration is **all-or-nothing**:
add every experiment, flush, commit once; on any duplicate, roll back and
raise — no partial rows survive.

```python
def register_batch_with_transaction(
    session: Session, experiments: list[Experiment]
) -> list[int]:
    """All-or-nothing batch registration; raise ValueError on duplicates."""
    try:
        session.add_all(experiments)
        session.flush()   # duplicates surface here as IntegrityError
    except Exception:
        session.rollback()
        raise ValueError("duplicate experiment name in batch") from None
    session.commit()
    return [exp.id for exp in experiments]
```

The rollback is what guarantees atomicity: a batch of 10 with 1 duplicate
leaves the table exactly as it was.

## 6. Production Pattern: Swap Storage, Keep Logic

The payoff: services written against the Protocol run unmodified against both
repositories. Tests use the in-memory backend (milliseconds, no engine);
production uses the SQL backend; a future rewrite (Redis, REST) implements the
same five methods.

```python
repo: ExperimentRepository = (
    InMemoryExperimentRepository()        # in unit tests
    # SqlExperimentRepository(session)    # in production
)
repo.add(Experiment(name="run-1", model="bert", score=0.95))
assert repo.get("run-1") is not None
```

---

## Common Mistakes to Avoid

### Mistake 1: Business logic inside the repository
```
# WRONG — repo decides what is promotable; logic is untestable without a DB
def add(self, exp): 
    if exp.score >= 0.9: ...  # domain rule leaked into storage
# CORRECT — repos store; should_promote() lives in domain functions
```

### Mistake 2: The repository commits
```
# WRONG — repo.add() calls session.commit(); batch atomicity impossible
def add(self, exp):
    self.session.add(exp); self.session.commit()
# CORRECT — flush only; the service owns commit/rollback
```

### Mistake 3: Services depending on Session directly
```
# WRONG — SQLAlchemy leaks into every service; mocks get painful
def register(service, session, rows): ...
# CORRECT — depend on ExperimentRepository; swap implementations freely
```

### Mistake 4: Reusing a session after IntegrityError
```
# WRONG — the failed transaction poisons later writes
try:
    session.commit()
except IntegrityError:
    pass
# CORRECT — rollback before any further work on that session
```

### Mistake 5: Duplicate handling only in one implementation
```
# WRONG — in-memory raises, SQL raises a different exception; service breaks
# CORRECT — normalize both to ValueError at the service boundary
```

---

## Best Practices

1. Domain rules are pure functions; repositories are pure persistence
2. Define the storage contract as a `Protocol` with `@runtime_checkable`
3. Repos take a Session; they never create or commit one
4. Flush inside `add` to assign PKs; commit stays with the caller
5. Normalize storage errors (IntegrityError/ValueError) at the service boundary
6. Roll back on any exception before reusing a session
7. Keep batch writes all-or-nothing; document the guarantee
8. Test services against the in-memory repo; smoke-test the SQL repo
9. Name duplicate detection explicitly — `ValueError` with the offending name
10. Make `isinstance(repo, Repository)` assertions part of DI checks

---

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| in-memory `get` | O(1) dict | O(n) | — |
| SQL `get` | O(log n) indexed | O(1) | unique index on name |
| batch register | O(n) flushes, 1 commit | O(n) | — |
| Protocol check | O(1) | O(1) | — |

**Cost note:** the pattern costs almost nothing at runtime — one indirection
through five methods — and pays for itself in test speed (no engine in unit
tests) and in swap-ability when storage requirements change.

---

## AI Engineering Relevance

**Where this shows up:** the experiment registry service, the model version
store, eval result persistence — every place where business rules (promote,
best-of, dedupe) meet a storage backend that must be testable.

| Concept here | Used for |
|---|---|
| pure domain rules | promotion thresholds, best-model selection |
| Protocol contract | swapping sqlite/dev for Postgres/prod storage |
| Unit of Work | one transaction for batch eval-result registration |
| in-memory repo | unit tests that run in milliseconds |

**Scale note:** at 1M rows the repository hides the pagination/keyset work
behind `list_all`; at 200 concurrent registrations the Unit of Work's
all-or-nothing commit is what keeps the registry consistent.

---

## Practice Exercises

### Exercise 1: Pure Rules (Difficulty: Easy)
Write `should_promote` and `best_model_name`; test with lists of experiments
including an empty list.

### Exercise 2: In-Memory Repo (Difficulty: Easy)
Implement add/get/list_all/count/delete; verify duplicate names raise
`ValueError` and `delete` returns True/False correctly.

### Exercise 3: SQL Repo Flush-Not-Commit (Difficulty: Medium)
Add through `SqlExperimentRepository`, assert the PK is assigned after `add`,
and prove a fresh session cannot see the row until the caller commits.

### Exercise 4: Protocol Check (Difficulty: Medium)
Assert `isinstance(InMemoryExperimentRepository(), ExperimentRepository)` and
the same for the SQL repo — structural typing in action.

### Exercise 5: All-or-Nothing Batch (Difficulty: Hard)
Implement `register_batch_with_transaction`; prove a batch with a duplicate
rolls back completely (table count unchanged) and raises `ValueError`.
(Challenge 10 tests this.)

---

## Summary

| Concept | Description |
|---|---|
| domain rules | pure functions; no session, no SQL |
| Protocol | storage contract; `@runtime_checkable` structural typing |
| SQL repo | flush-only; caller owns the transaction |
| in-memory repo | same contract, milliseconds, no DB |
| Unit of Work | service layer decides commit vs rollback |
| batch registration | all-or-nothing; rollback on any duplicate |

The repository pattern is the architectural capstone of the module: domain
logic clean, storage swappable, transactions explicit, tests fast.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Contract | `@runtime_checkable class Repo(Protocol)` with add/get/list_all/count/delete |
| SQL add | `session.add(exp); session.flush(); return exp.id` |
| In-memory add | dict + `ValueError` on duplicate name |
| All-or-nothing batch | `add_all` + flush + commit; rollback + raise on failure |
| Type check | `isinstance(repo, ExperimentRepository)` |
| Swap backends | inject a different implementation; domain code untouched |

---

## Next Steps

Next: **[Phase 05 — Databases](../../05-web-frameworks/fastapi/19-orm.py)** —
wire the repository + session-per-request into a FastAPI service.

Continues in: **[FastAPI ORM exercise](../../05-web-frameworks/fastapi/19-orm.py)** —
the full stack: models, sessions, repositories behind REST endpoints.

Official docs:
- Typing Protocol: https://docs.python.org/3/library/typing.html#typing.Protocol
- Unit of Work (Martin Fowler): https://martinfowler.com/eaaCatalog/unitOfWork.html
- Repository (Martin Fowler): https://martinfowler.com/eaaCatalog/repository.html
