# 01-core-python — 45: Testing with pytest — Proving Behavior

## Topic Overview

Tests are the difference between "it runs" and "it is right." `pytest` is the
standard testing framework in the Python ecosystem: plain `assert` (no
assertion macros), fixtures with explicit scopes, parameterized tests, and
powerful plugins for mocking, coverage, and async. It is what CI gates run.

For AI and backend engineers this is where you prove a chunking function's
boundaries, mock the LLM API so tests are free and deterministic, and lock in
golden outputs for prompt templates. The discipline — write the test that
fails, watch it fail, make it pass — is the same whether the unit is a parser
or a RAG pipeline.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Discover and run tests with `pytest`
2. Write assertions with plain `assert` and readable failure messages
3. Use `pytest.raises` to test expected exceptions
4. Parameterize tests with `@pytest.mark.parametrize`
5. Write fixtures with `tmp_path`, `monkeypatch`, and explicit scope
6. Mock dependencies with `unittest.mock` (`Mock`, `patch`, `side_effect`)
7. Follow the AAA (Arrange-Act-Assert) structure
8. Explain what *not* to test
9. Measure coverage and read the report

## Prerequisites

| Need | Where |
|------|-------|
| Functions | `21-functions.py` lecture |
| Exceptions | `47-exceptions-advanced` lecture |
| Logging | `44-logging` lecture |

## 1. Why Tests, Why pytest

A test converts an assumption into a check that runs in CI forever. pytest wins
on simplicity: tests are functions whose names start with `test_`, and
assertions are plain Python `assert` statements. There is no framework API to
memorize for the basic case.

```python
# test_utils.py
def test_parse_tags_splits_on_comma():
    assert parse_tags("rag, eval, agents") == ["rag", "eval", "agents"]
```

`assert` failure messages are enriched automatically: pytest shows the values
of both sides of a failed comparison.

## 2. Test Discovery and Running

```text
python -m pytest                 # discover test_*.py / *_test.py
python -m pytest -v              # verbose per-test output
python -m pytest -k "chunk"      # run tests matching "chunk"
python -m pytest tests/test_x.py::test_case -q   # single test
```

pytest collects functions named `test_*` (or classes `Test*`) in files matching
`test_*.py` / `*_test.py`, recursively from the current directory.

## 3. Assertions — Plain `assert` + Messages

```python
def test_normalization():
    assert normalize("  RAG  ") == "rag"
    assert normalize("") == ""
    assert len(normalize("x") * 100) == 100, "length must be preserved"
```

pytest rewrites assert statements to show the actual vs expected values. Add an
explicit message only when the default diff is not self-explanatory.

## 4. `pytest.raises` — Testing Failures

```python
import pytest

def test_invalid_input_raises():
    with pytest.raises(ValueError, match="must be positive"):
        parse_config("lr=-1")

    with pytest.raises((TypeError, ValueError)) as exc_info:
        parse_config("x")
    assert "config" in str(exc_info.value)
```

`match=` checks the exception message; `exc_info` gives access to the exception
object for further assertions. Testing the *error path* is as important as
testing the happy path.

## 5. Parameterization — One Test, Many Cases

```python
@pytest.mark.parametrize("text,expected", [
    ("a,b,c", ["a", "b", "c"]),
    ("", []),
    ("a", ["a"]),
    (" a , b ", ["a", "b"]),
])
def test_split_csv(text, expected):
    assert split_csv(text) == expected
```

Each tuple becomes a separate test case with its own pass/fail reporting —
boundary cases (empty, single, whitespace) are the ones that catch real bugs.

## 6. Fixtures — Setup with Scope

Fixtures are functions that provide test dependencies; `tmp_path` is a
built-in per-test temp directory, `monkeypatch` mutates environment safely.

```python
import pytest

@pytest.fixture
def chunker():
    return Chunker(max_chars=300, overlap=50)

@pytest.fixture(scope="session")        # expensive once per session
def dataset_path(tmp_path_factory):
    return tmp_path_factory.mktemp("data")

def test_chunk_boundaries(chunker):
    chunks = chunker.split("a" * 1000)
    assert all(len(c) <= 300 for c in chunks)
```

Scopes: `function` (default), `class`, `module`, `session`. Use wider scopes for
expensive setup; keep mutation-scoped fixtures at `function` to isolate tests.

## 7. `monkeypatch` and `unittest.mock` — Free, Deterministic Tests

The AI-engineer rule: never call a paid or flaky API in a unit test. Mock it.

```python
from unittest.mock import patch, Mock

def test_call_retries_on_429():
    fake = Mock(side_effect=[RateLimitError("429"), "ok"])
    with patch("myapp.llm.call", fake):
        assert call_with_retry("prompt") == "ok"
    assert fake.call_count == 2
```

- `Mock(side_effect=[...])` — different results per call
- `patch("module.attr", ...)` — replace at the usage site
- `Mock.return_value` — fixed return
- `assert_called_once_with(...)` — verify the call contract

## 8. AAA Structure and What Not to Test

```python
def test_scoring_order():
    # Arrange
    hits = [Hit("b", 0.3), Hit("a", 0.9)]
    # Act
    ranked = rank(hits)
    # Assert
    assert [h.doc for h in ranked] == ["a", "b"]
```

**What not to test:** the stdlib, third-party library internals, private
implementation details, `print()` output, or one-off REPL scripts. Test *your*
contracts — the behavior you own.

## 9. Coverage

```text
python -m pytest --cov=. --cov-report=term-missing
```

Coverage tells you which lines never ran. High coverage is not the goal; it is
a *signal* — 100% coverage of code with no assertions is still useless. Cover
the branches that encode your rules (boundaries, error paths, fallbacks).

## 10. Production Pattern — Golden-Input Tests

Lock in behavior with fixed inputs and expected outputs, so a future "small"
change to a prompt template or a chunker gets caught loudly:

```python
def test_golden_prompt():
    prompt = build_prompt(
        system="You are a concise assistant.",
        question="What is RAG?",
        context=["RAG = retrieval-augmented generation."],
    )
    expected = (
        "You are a concise assistant.\n\n"
        "Context:\n- RAG = retrieval-augmented generation.\n\n"
        "Question: What is RAG?\n"
    )
    assert prompt == expected
```

## Common Mistakes to Avoid

### Mistake 1: Assertions that always pass

```python
# WRONG — testing the implementation, not the contract
assert result is not None           # trivially true
# CORRECT
assert result == expected
```

### Mistake 2: Test-order dependence

```python
# WRONG — relies on a previous test's side effect
# CORRECT — each test sets up its own state (fixtures, fresh data)
```

### Mistake 3: Hitting real services in unit tests

```python
# WRONG — slow, flaky, costs money, breaks offline
resp = openai.ChatCompletion.create(...)
# CORRECT — patch the client; test your logic, not their API
```

### Mistake 4: Comparing floats exactly

```python
# WRONG
assert score == 0.9
# CORRECT
assert abs(score - 0.9) < 1e-6   # or pytest.approx(0.9)
```

### Mistake 5: Catching exceptions in the test instead of asserting them

```python
# WRONG — swallows the failure
try:
    parse("bad")
except ValueError:
    pass
# CORRECT
with pytest.raises(ValueError):
    parse("bad")
```

## Best Practices

1. Name tests after the behavior: `test_returns_empty_list_for_blank_input`
2. One behavior per test; a failing test names the broken rule
3. Use `pytest.approx` for floats
4. Prefer `parametrize` over copy-pasted test functions
5. Use `monkeypatch`/`patch` to remove I/O, clocks, and randomness
6. Keep fixtures narrow and scoped; share only what is truly shared
7. Test boundaries: empty, single, duplicate, maximum, invalid
8. Run the suite in CI; a red build blocks merges
9. Make tests deterministic: seed RNG, no wall-clock asserts, no network
10. Write the failing test first when fixing a bug (regression test)

## Complexity and Cost

| Aspect | Cost | Notes |
|--------|------|-------|
| Test run | O(total work) | fast tests keep the loop tight |
| Fixture scope | shared setup runs once | session-scope for expensive setup |
| Mocked I/O | ~free | the reason unit tests are instant |
| Real API in tests | $ + seconds + flake | never in unit tests |
| Coverage tool | ~2-3x runtime | use in CI, not the inner loop |

**At scale:** a suite that takes 20 minutes instead of 2 minutes stops being
run. Keep unit tests fast; push slow integration tests to nightly CI.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| mocking the LLM | free, deterministic tests of prompt/agent logic |
| `parametrize` | chunk-size boundaries, prompt variants, token limits |
| golden tests | locking prompt template output and RAG response shape |
| `pytest.raises` | asserting 400-vs-retry classification of API errors |
| fixtures + `tmp_path` | testing ingestion against fixture datasets |
| coverage | finding untested branches in retrieval scoring code |

**Scale note:** as the codebase grows, an untested prompt change can silently
degrade a production RAG system. The eval loop — tests for logic, golden sets
for prompts — is what keeps deployments safe.

## Practice Exercises

### Exercise 1: First Test (Easy)
Write `test_split_tags` for a `split_tags(text: str) -> list[str]` covering
normal, empty, and whitespace inputs. Run it with `pytest -v`.

### Exercise 2: Parameterized + Raises (Medium)
`parse_config_line(line: str) -> tuple[str, str]` — parameterize over valid
lines; assert `ValueError` for lines without `=`.

### Exercise 3: Mocked LLM (Hard)
Write `call_with_retry(fn)` and test it with a `Mock(side_effect=[...])` that
fails twice with `RetryableError` then succeeds; assert retry count and that a
`FatalError` is NOT retried.

## Summary

| Concept | Description |
|---------|-------------|
| `assert` | plain Python assertions, enriched failure diffs by pytest |
| `pytest.raises` | assert an exception with optional message match |
| `parametrize` | many cases, one test body, per-case reporting |
| fixtures | setup with `function`/`session` scope; `tmp_path`, `monkeypatch` |
| `unittest.mock` | replace dependencies: `Mock`, `patch`, `side_effect` |
| AAA | Arrange-Act-Assert structure for readable tests |
| Coverage | signal for untested branches, not the goal itself |

Tests convert "it works on my machine" into "it is proven in CI."

## Quick Reference

| Task | Idiom |
|------|-------|
| Run suite | `python -m pytest` |
| Single test | `python -m pytest path::test_name -v` |
| Many cases | `@pytest.mark.parametrize("x,exp", [...])` |
| Expect error | `with pytest.raises(ValueError):` |
| Temp dir | `def test_x(tmp_path):` |
| Patch a call | `with patch("mod.fn", Mock(return_value=...)):` |
| Float compare | `assert x == pytest.approx(0.9)` |
| Coverage | `python -m pytest --cov=. --cov-report=term-missing` |

## Next Steps

Next: **[46-cli-and-config](46-cli-and-config-lecture.md)** — the training-script interface.
Continues in: **[02-advanced-python — 18 unit testing](../../02-advanced-python/lectures/18-unit-testing-lecture.md)** and
**[08-mlops — 12 CI/CD for ML](../../../08-mlops/lectures/12-ci-cd-for-ml-lecture.md)**.
Official docs: https://docs.pytest.org/
