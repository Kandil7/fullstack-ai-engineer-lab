# Challenge 09: Testing with a Database — Isolation Patterns

## 🥉 Bronze — Factory + Schema Reset (~15 min)

**Task:** Implement two helpers:

1. `make_experiment(name, **overrides)` — construct an `Experiment` with its
   column defaults applied (score `0.0`, config `{}`) plus any overrides.
2. `reset_schema(engine)` — drop **all** tables and recreate them, so a test
   run starts from a clean schema.

**Signatures:**
```python
def make_experiment(name: str, **overrides) -> Experiment:
def reset_schema(engine) -> None:
```

**Requirements:**
- `make_experiment("a")` → `score == 0.0` and `config == {}`
- `make_experiment("a", score=0.5)` → `score == 0.5`
- After `reset_schema(engine)` the table is empty and usable again

---

## 🥈 Silver — Transactional Rollback Fixture (~35 min)

**Task:** Implement `transactional_session(eng)` — the generator the pytest
fixture uses: a session bound to a **connection with an outer transaction**
(SAVEPOINT join mode). When the generator is closed, **every write the test
made is rolled back** — no cleanup code needed.

**Signature:**
```python
def transactional_session(eng):
    """Yield a session whose writes roll back when the generator ends."""
```

**Usage (in your tests):**
```python
gen = solution.transactional_session(engine)
session = next(gen)
try:
    ... assert ...
finally:
    gen.close()     # <- everything the test wrote vanishes
```

**Requirements:**
- Rows written inside the session are **visible during the test**
- After `gen.close()` a fresh session sees **zero** of those rows
- The engine stays fully usable afterwards

---

## 🥇 Gold — Two Tests, One Engine (~75 min)

**Task:** Implement `run_isolated_tests(eng)` which simulates two sequential
tests against the SAME engine and returns `(seen_test1, seen_test2)`:

- **"test 1"** writes 2 experiments inside `transactional_session` and counts
  the rows it can see → the first number
- After test 1's session closes, **"test 2"** (a plain committed session)
  counts the rows → the second number

**Signature:**
```python
def run_isolated_tests(eng) -> tuple[int, int]:
```

**Requirements:**
- Return `(2, 0)` on a fresh engine — test 2 must NOT see test 1's rows
- This is the guarantee that makes DB tests parallelizable and repeatable

**Follow-up:** why does this beat `DROP/CREATE` between tests?
(Answer: no schema churn, no lost identity-map state, and the outer
transaction rolls back *everything* — including cascades you forgot about.)

---

## Running

```bash
pytest challenges/09-testing-with-db/test_challenge.py -v
```

## Test File Structure

```
challenges/09-testing-with-db/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
