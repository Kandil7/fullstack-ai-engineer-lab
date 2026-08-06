# Challenge 45: Testing with pytest

A meta-challenge: build a *tiny test framework* — the pieces pytest gives you.

## 🥉 Bronze — Safe Test Runner (~15 min)

**Task:** Implement `run_test(fn) -> tuple[bool, str]` that calls a zero-arg
test function and returns `(True, "")` if it passes or `(False, error_message)`
if it raises.

| Input | Expected |
|-------|----------|
| `lambda: None` | `(True, "")` |
| `lambda: 1/0` | `(False, ...)` with a message |

**Constraints:** n ≤ 10^3. Never let the exception escape.

---

## 🥈 Silver — Mini `pytest.raises` (~35 min)

**Task:** Implement `assert_raises(fn, exc_type) -> None` that calls `fn` and
raises `AssertionError` if it does **not** raise `exc_type`; otherwise returns
silently.

**Signature:**
```python
def assert_raises(fn, exc_type: type) -> None: ...
```

| Input | Expected |
|-------|----------|
| `assert_raises(lambda: 1/0, ZeroDivisionError)` | passes |
| `assert_raises(lambda: 1, ValueError)` | raises `AssertionError` |

**Constraints:** n ≤ 10^3. Must also pass when `fn` raises a *subclass* of
`exc_type`.

---

## 🥇 Gold — Mini Test Suite (~75 min)

**Task:** Implement `run_suite(module) -> dict[str, bool]` that discovers all
callables named `test_*` in a module, runs each, and returns
`{name: passed}`. Then `summarize(results) -> str` returns a one-line report:
`"N passed, M failed"`.

**Signature:**
```python
def run_suite(module) -> dict[str, bool]: ...
def summarize(results: dict[str, bool]) -> str: ...
```

**Constraints:** 10^3 tests, single pass; failures must not stop discovery of
later tests. A test that raises must be reported as failed, not crash the run.

**Follow-up:** what would you add to make this usable? (Answer: fixtures,
parametrization, assertion diffing, exit codes — the pytest feature list.)

---

## Running

```bash
pytest challenges/45-testing-with-pytest/test_challenge.py -v
```
