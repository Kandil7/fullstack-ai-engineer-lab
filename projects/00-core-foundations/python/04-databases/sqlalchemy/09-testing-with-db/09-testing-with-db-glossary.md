# Testing with a Database — Glossary 09

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| create_savepoint | Fixture | `join_transaction_mode` joining the session to an outer tx via SAVEPOINTs |
| Factory | Pattern | Helper building rows with column defaults set explicitly |
| IntegrityError | Failure | Constraint violation; must rollback before reusing the session |
| Isolation | Goal | Test A's writes invisible to test B — order-independent tests |
| Per-test engine | Fixture | A fresh in-memory engine + schema per test |
| Reset schema | Fixture | `drop_all` + `create_all` between suites for a clean slate |
| Rollback fixture | Fixture | Outer transaction rolled back on teardown; writes vanish |
| SAVEPOINT | Mechanism | A marked point letting the session join an outer transaction |
| sqlite divergence | Risk | Behaviors where sqlite differs from Postgres (length, JSON, operators) |
| StaticPool | Pool | Pins one connection so in-memory sqlite survives across sessions |
| Testcontainers | Tool | Real Postgres in CI for dialect-faithful tests |
| Transactional rollback | Concept | Writes real inside the test, invisible after — zero cleanup code |

## Detailed Definitions

### create_savepoint
**Definition**: The `join_transaction_mode` value making a session bind to a
connection's outer transaction through SAVEPOINTs — the core of the rollback
fixture.
**Related**: Rollback fixture

### Factory
**Definition**: A helper like `make_experiment(name, **overrides)` that sets
column defaults explicitly at construction — because defaults apply at
*flush*, not instantiation, so tests read intent without ORM timing.
**Related**: Rollback fixture

### IntegrityError
**Definition**: A constraint violation surfaced on flush/commit; after it, the
session's transaction is poisoned and must be rolled back (or closed) before
any further work.
**Related**: Isolation

### Isolation
**Definition**: The property that one test's writes never leak into another —
what makes DB tests repeatable, parallelizable, and order-independent.
**Related**: Rollback fixture

### Per-test engine
**Definition**: Creating a brand-new in-memory engine (with schema) for each
test — the simplest hard guarantee against shared state.
**Example**:
```python
eng = create_engine("sqlite://", poolclass=StaticPool)
Base.metadata.create_all(eng)
```
**Related**: StaticPool

### Reset schema
**Definition**: `Base.metadata.drop_all(eng)` + `create_all(eng)` between
suites — a clean slate without restarting the engine.
**Related**: Per-test engine

### Rollback fixture
**Definition**: The workhorse: the session joins an outer transaction held on
a connection; teardown rolls the outer transaction back, so every write the
test made vanishes — no cleanup code.
**Related**: create_savepoint

### SAVEPOINT
**Definition**: A marked transaction point; the session creates savepoints
inside the outer transaction so its own commits are real during the test yet
discardable when the outer rollback fires.
**Related**: Rollback fixture

### sqlite divergence
**Definition**: Behaviors where sqlite is only a *model* of Postgres — `VARCHAR(n)`
length not enforced, JSON returned as text, missing operators like `@>`.
Know them so CI stays honest.
**Related**: Testcontainers

### StaticPool
**Definition**: The pool class that pins one connection, so the shared
in-memory database survives across sessions/engines in tests.
**Related**: Per-test engine

### Testcontainers
**Definition**: Running real database images (e.g. `PostgresContainer`) in
tests — true dialect fidelity for the suites where sqlite divergence matters.
**Related**: sqlite divergence

### Transactional rollback
**Definition**: The concept underlying the fixture — writes are genuinely
visible during the test and entirely gone after; the database appears
untouched between tests.
**Related**: Rollback fixture

## Key Concepts Summary

### The isolation ladder
- Per-test engine + schema: zero shared state.
- Rollback fixture: writes real in-test, gone after.
- `reset_schema`: clean slate between suites.
- Testcontainers: real Postgres in CI for dialect-critical suites.

### The sqlite honesty list
- String length is not enforced.
- JSON columns come back as str.
- Postgres operators (`@>`, `ILIKE` nuances) may not exist.
- Guard dialect-specific assertions or run them only on Postgres.

### The determinism rule
- Assert counts and states — never wall-clock timing.
- Assert query counts (like the N+1 exercise) — deterministic and meaningful.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Writes real during the test, gone after — ___
2. The session joins an outer tx via savepoints — ___
3. A fresh in-memory engine per test — ___
4. Defaults set explicitly in a helper — ___
5. drop_all + create_all between suites — ___
6. sqlite ignores this constraint — ___
7. Real Postgres in CI tests — ___
8. Poisoned after a constraint violation — ___

**Answers:** 1-transactional rollback, 2-create_savepoint, 3-per-test engine,
4-factory, 5-reset schema, 6-string length, 7-testcontainers, 8-session
