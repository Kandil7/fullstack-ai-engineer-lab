# Databases (SQLAlchemy) — 09: Testing with a Database

## Topic Overview

Database tests fail for two reasons: tests step on each other's rows, and the
database state from test A leaks into test B. The industry-standard fix is the
**transactional rollback fixture**: each test runs inside a transaction that is
rolled back at the end, so every write vanishes without cleanup code. The
fixture binds the session to a connection holding an *outer* transaction and
joins it via SAVEPOINTs — the same pattern pytest plugins and FastAPI test
clients use.

For AI/backend engineers this is how metadata-store code gets tested safely:
registry CRUD, eval insert paths, repository logic — all against a real
database (sqlite in CI, Postgres in staging) with zero cross-test pollution.
This lecture covers the rollback fixture, per-test schema creation, factories
that apply column defaults explicitly, the sqlite-vs-Postgres divergence traps,
and the testcontainers note for true-production fidelity.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Create a fresh in-memory engine per test with `StaticPool`
2. Build the transactional rollback fixture with SAVEPOINT join mode
3. Prove writes are visible *during* a test and vanish *after* it
4. Write factory helpers that apply column defaults explicitly
5. Reset schema between suites with `drop_all`/`create_all`
6. Recognize sqlite divergences (length, JSON, operators) and code around them
7. Structure tests so two "tests" on one engine see isolated state
8. Predict which failure modes cross-test isolation prevents
9. Know when testcontainers are worth the cost
10. Keep DB tests deterministic, fast, and parallelizable

---

## Prerequisites

| Need | Where |
|---|---|
| Session lifecycle | `03-session-lifecycle-lecture.md` |
| pytest fixtures | `02-advanced-python/lectures/18-unit-testing-lecture.md` |
| Mapped models | `02-declarative-models-lecture.md` |

---

## 1. The Workhorse Pattern: Transactional Rollback Fixture

The session is bound to a connection that holds an outer transaction; the
session joins it via SAVEPOINTs. When the test ends we roll the outer
transaction back — every INSERT the test made vanishes without any cleanup
code.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

def make_engine() -> object:
    """Create a brand-new in-memory engine with the schema applied."""
    eng = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(eng)
    return eng

def transactional_session(eng):
    """Yield a session whose writes roll back when the generator ends."""
    connection = eng.connect()
    outer = connection.begin()   # outer transaction: never committed
    session = Session(
        bind=connection, join_transaction_mode="create_savepoint"
    )
    try:
        yield session
    finally:
        session.close()
        outer.rollback()         # discard every write the test made
        connection.close()
```

Usage inside pytest:

```python
def test_something(eng):
    gen = transactional_session(eng)
    session = next(gen)
    try:
        ... assert ...
    finally:
        gen.close()   # <- rolls back everything
```

## 2. Isolation, Demonstrated

Two "tests" run against the SAME engine. The first writes rows inside a
rollback fixture; the second sees NONE of them. This is the guarantee that
makes DB tests parallelizable and repeatable.

```python
def simulate_rollback_isolation(eng) -> tuple[int, int]:
    # "test 1": insert two rows, expect them visible DURING the test
    gen = transactional_session(eng)
    session = next(gen)
    session.add_all([make_experiment("t1-a"), make_experiment("t1-b")])
    seen_test1 = len(session.scalars(select(Experiment.id)).all())
    gen.close()   # rollback

    # "test 2": a plain committed session must see NONE of test 1's rows
    with Session(bind=eng) as fresh:
        seen_test2 = len(fresh.scalars(select(Experiment.id)).all())
    return seen_test1, seen_test2
```

The result is `(2, 0)`: the write was real inside the test, invisible after.

## 3. Factories: Defaults Made Explicit

Column defaults apply at **flush**, not construction — so a factory that sets
them explicitly makes tests read intent, not ORM timing.

```python
def make_experiment(name: str, **overrides) -> Experiment:
    experiment = Experiment(name=name, score=0.0, config={})
    for key, value in overrides.items():
        setattr(experiment, key, value)
    return experiment
```

`make_experiment("a", score=0.5)` is unambiguous: score 0.5, config `{}` —
no flush required to know what was written.

## 4. Schema Resets

Between suites (or when a test genuinely needs committed state), reset the
schema: `drop_all` then `create_all` gives a clean slate without restarting
the engine.

```python
def reset_schema(engine) -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
```

## 5. SQLite Divergence Traps

sqlite is a *model* of the target database, not a replica. Three traps that
bite:

```python
# 1. String length is NOT enforced on sqlite
#    (Postgres enforces VARCHAR(10); sqlite accepts 20 chars silently)

# 2. JSON columns come back as str on sqlite, not dict
#    -> use a JSON type / parse explicitly when the dialect differs

# 3. Postgres operators like @> (contains) do not exist on sqlite
#    -> write dialect-agnostic filters or skip dialect-specific tests
```

When the divergence matters (a CHECK that sqlite ignores, an operator that
does not exist), either guard the test with a dialect check or run it only in
CI against the real database.

## 6. Production Pattern: Testcontainers for Real Fidelity

For true-production fidelity, run tests against a containerized Postgres via
testcontainers: same dialect, same constraints, same operators.

```python
# from testcontainers.postgres import PostgresContainer
# with PostgresContainer("postgres:16") as pg:
#     engine = create_engine(pg.get_connection_url())
#     # same fixtures, same tests — now against real Postgres
```

The rollback fixture is dialect-agnostic: the same pattern works on Postgres
unchanged. Start with sqlite for speed in local dev; promote to containers in
CI for the suites that exercise dialect-specific behavior.

---

## Common Mistakes to Avoid

### Mistake 1: One shared engine + committed state across tests
```
# WRONG — test A's rows leak into test B; order-dependent failures
@pytest.fixture()
def session():
    with Session(bind=shared_engine) as s:
        yield s          # commits persist forever
# CORRECT — per-test engine + rollback fixture (or reset_schema)
```

### Mistake 2: Forgetting that defaults apply at flush
```
# WRONG — asserts 0.0 before any flush; config is None, not {}
exp = Experiment(name="x")
assert exp.score == 0.0 and exp.config == {}   # False!
# CORRECT — set defaults in the factory explicitly
```

### Mistake 3: Testing sqlite-only behavior as if it were Postgres
```
# WRONG — "the CHECK rejected it" on sqlite is not guaranteed
# CORRECT — know sqlite ignores VARCHAR(n); verify constraints in CI on Postgres
```

### Mistake 4: Catching IntegrityError and reusing the same session
```
# WRONG — poisoned transaction poisons the next assertion
try:
    session.commit()
except IntegrityError:
    pass
# CORRECT — rollback (or close) before continuing the test
```

### Mistake 5: Asserting wall-clock timing in tests
```
# WRONG — flaky on CI machines
assert elapsed < 0.1
# CORRECT — assert query COUNTS (deterministic), never wall-clock
```

---

## Best Practices

1. Fresh engine + schema per test; StaticPool for in-memory sqlite
2. Rollback fixture as the default; commit only in tests that must persist
3. Factories set defaults explicitly; tests read intent
4. `reset_schema` between suites, not between tests
5. Know the sqlite divergence list; guard dialect-specific asserts
6. Test with the same ORM code paths the service uses (no raw-SQL shortcuts)
7. Assert counts and states, never timing
8. Promote to testcontainers for dialect-critical suites in CI
9. Keep fixtures thin: engine + session; everything else in helpers
10. Make every test runnable in any order — isolation is the contract

---

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| per-test engine + create_all | ~ms | O(schema) | reuse engine; reset schema |
| rollback fixture teardown | ~ms | O(1) | — |
| full schema reset | O(tables) DDL | O(1) | only between suites |
| testcontainers Postgres | seconds to start | ~1GB | sqlite for most suites |

**Cost note:** the rollback fixture is nearly free and buys parallelizability.
Containers cost seconds per suite — pay it only where dialect fidelity
matters (constraints, operators, indexes).

---

## AI Engineering Relevance

**Where this shows up:** testing the experiment registry CRUD, eval-metric
insert paths, model-version uniqueness, and repository/service layers of an
ML platform.

| Concept here | Used for |
|---|---|
| rollback fixture | isolated tests for every DB-touching service |
| factories | readable test fixtures for registry rows |
| schema reset | clean suites for migration backfills |
| sqlite divergence awareness | honest CI: unit-fast, integration-faithful |

**Scale note:** at 10,000 tests, per-test engines still run in seconds on
sqlite; containers would take minutes. The tiered strategy — sqlite locally,
containers in CI — keeps both fast and honest.

---

## Practice Exercises

### Exercise 1: Isolation Proof (Difficulty: Easy)
Run `simulate_rollback_isolation` on a fresh engine and assert `(2, 0)`.
Explain why test 2 sees nothing.

### Exercise 2: Factory Defaults (Difficulty: Easy)
Assert `make_experiment("a")` yields score 0.0 and config `{}` *before any
flush*, and that overrides win.

### Exercise 3: Reset Between Suites (Difficulty: Medium)
Write two rows, `reset_schema`, then assert the table is empty and usable.

### Exercise 4: Divergence Audit (Difficulty: Medium)
Write a test that inserts a 20-character name into a `String(10)` column and
confirm sqlite accepts it. Add a comment explaining where Postgres would
reject it.

### Exercise 5: Fixture-Less Rollback (Difficulty: Hard)
Reimplement `transactional_session` as a pytest fixture using `yield`, then
write three tests that each insert rows and assert their own visibility —
proving order-independence. (Challenge 09 tests this shape.)

---

## Summary

| Concept | Description |
|---|---|
| rollback fixture | outer tx + SAVEPOINTs; writes vanish on close |
| per-test engine | StaticPool in-memory; no cross-test state |
| factories | explicit defaults; tests read intent |
| reset_schema | drop_all/create_all between suites |
| sqlite divergences | length, JSON, operators differ from Postgres |
| testcontainers | real Postgres in CI for dialect-critical suites |

DB tests are only as good as their isolation. The rollback fixture makes
every test self-cleaning, and knowing the sqlite gaps keeps CI honest.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Fresh engine | `create_engine("sqlite://", poolclass=StaticPool)` |
| Rollback fixture | `Session(bind=conn, join_transaction_mode="create_savepoint")` + outer.rollback() |
| Factory | `make_experiment(name, **overrides)` with explicit defaults |
| Schema reset | `Base.metadata.drop_all(eng); create_all(eng)` |
| Commit-worthy tests | plain `Session(bind=eng)` + commit |
| Real Postgres | testcontainers PostgresContainer |

---

## Next Steps

Next: **[10 — Repository Pattern](10-repository-pattern-lecture.md)** — wrap
sessions behind a contract so storage is swappable and testable.

Continues in: **[Phase 05 — Databases](../../05-web-frameworks/fastapi/19-orm.py)** —
tested repositories inside a FastAPI service.

Official docs:
- Session transactions: https://docs.sqlalchemy.org/en/20/orm/session_transaction.html
- Testcontainers Python: https://testcontainers-python.readthedocs.io/
- SQLite dialect notes: https://docs.sqlalchemy.org/en/20/dialects/sqlite.html
