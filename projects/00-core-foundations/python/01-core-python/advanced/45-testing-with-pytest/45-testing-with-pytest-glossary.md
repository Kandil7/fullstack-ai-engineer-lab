# Testing with pytest — Glossary 45

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| pytest | Tool | The standard Python testing framework built on plain `assert` |
| test discovery | Concept | Collects `test_*` functions in `test_*.py` / `*_test.py` files |
| `assert` | Keyword | Plain Python assertion; pytest enriches the failure diff |
| `pytest.raises` | Context | Asserts a specific exception is raised |
| `@pytest.mark.parametrize` | Decorator | Runs one test body over many (input, expected) cases |
| fixture | Concept | Function providing setup/teardown to tests |
| `tmp_path` | Fixture | Built-in per-test temporary directory |
| `monkeypatch` | Fixture | Safely patches attributes/env for the duration of a test |
| `Mock` | Class | `unittest.mock` object with configurable return/side effects |
| `patch` | Context | Replaces an attribute (e.g. an API client) at runtime |
| `side_effect` | Attribute | Callable/sequence/list producing per-call results or raises |
| `return_value` | Attribute | The value a Mock returns when called |
| `assert_called_once_with` | Method | Verifies the exact call contract |
| AAA | Structure | Arrange-Act-Assert: the canonical test layout |
| `pytest.approx` | Function | Float comparison with tolerance |
| `-k` flag | Option | Runs only tests whose names match an expression |
| coverage | Tool | Reports which lines/branches executed during the run |
| golden test | Pattern | Locks behavior to a fixed expected output |

## Detailed Definitions

### pytest
**Definition**: The de facto standard testing framework for Python; plain
`assert`, fixtures, parameterization, and a rich plugin ecosystem.
**Example**:
```bash
python -m pytest -v
```
**Related**: `assert`, fixtures, `parametrize`

### test discovery
**Definition**: pytest's default collection: functions named `test_*` (or
`Test*` classes) inside files matching `test_*.py` or `*_test.py`.
**Example**:
```python
# test_chunker.py
def test_chunk_size_limit(): ...
```
**Related**: `-k` flag

### `assert`
**Definition**: Python's built-in assertion; pytest rewrites it to display the
actual and expected values on failure.
**Example**:
```python
def test_split():
    assert split("a,b") == ["a", "b"]
```
**Related**: `pytest.raises`, failure messages

### `pytest.raises`
**Definition**: A context manager asserting that a block raises the named
exception, optionally matching the message.
**Example**:
```python
with pytest.raises(ValueError, match="positive"):
    parse("lr=-1")
```
**Related**: error-path testing

### `@pytest.mark.parametrize`
**Definition**: Feeds a list of argument tuples into one test body, generating
one test case per tuple.
**Example**:
```python
@pytest.mark.parametrize("text,exp", [("", []), ("a", ["a"])])
def test_split(text, exp):
    assert split(text) == exp
```
**Related**: boundary cases

### fixture
**Definition**: A `@pytest.fixture` function providing setup (and teardown);
injected by parameter name, scoped per function/module/session.
**Example**:
```python
@pytest.fixture
def chunker():
    return Chunker(max_chars=300)
```
**Related**: `tmp_path`, `monkeypatch`

### `tmp_path`
**Definition**: Built-in fixture giving each test its own `pathlib.Path`
temporary directory, removed afterwards — no manual cleanup.
**Example**:
```python
def test_writes_jsonl(tmp_path):
    path = tmp_path / "data.jsonl"
    write_records(path, [{"a": 1}])
    assert path.exists()
```
**Related**: fixture, determinism

### `monkeypatch`
**Definition**: Built-in fixture to temporarily set attributes, dict items, and
env vars, restored automatically after the test.
**Example**:
```python
def test_uses_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test")
    assert get_key() == "test"
```
**Related**: `patch`, environment

### `Mock`
**Definition**: `unittest.mock.Mock` — a stand-in object whose behavior you
program via `return_value`, `side_effect`, and call assertions.
**Example**:
```python
fake = Mock(return_value={"ok": True})
```
**Related**: `patch`, `side_effect`

### `patch`
**Definition**: `unittest.mock.patch` replaces an attribute at the usage site
for the duration of a test — the standard way to fake an LLM client.
**Example**:
```python
with patch("myapp.llm.call", fake):
    result = my_code()
```
**Related**: `Mock`, mocking I/O

### `side_effect`
**Definition**: Mock attribute making calls return different values in sequence,
or raise; also usable as a function of the arguments.
**Example**:
```python
mock = Mock(side_effect=[TimeoutError("429"), "ok"])
```
**Related**: `Mock`, retry tests

### `return_value`
**Definition**: Mock attribute holding the value returned on every call.
**Related**: `Mock`, `side_effect`

### `assert_called_once_with`
**Definition**: Asserts the mock was called exactly once with exactly these
arguments — the call-contract check.
**Example**:
```python
fake.assert_called_once_with("prompt", temperature=0.0)
```
**Related**: `Mock`

### AAA
**Definition**: Arrange-Act-Assert — set up state, perform the operation, verify
the outcome. The canonical readable test structure.
**Related**: test readability

### `pytest.approx`
**Definition**: Tolerance-aware float comparison; use instead of `==` on floats.
**Example**:
```python
assert score == pytest.approx(0.9, abs=1e-6)
```
**Related**: float equality

### `-k` flag
**Definition**: Runs only tests matching an expression on their names.
**Example**:
```bash
python -m pytest -k "chunk or retrieval"
```
**Related**: test discovery

### coverage
**Definition**: Tooling (pytest-cov) reporting executed lines/branches; a signal
for untested paths, not the goal itself.
**Example**:
```bash
python -m pytest --cov=. --cov-report=term-missing
```
**Related**: CI, regression safety

### golden test
**Definition**: A test pinning exact expected output for fixed input — used to
freeze prompt templates and serialization formats.
**Example**:
```python
assert build_prompt(...) == (
    "You are a concise assistant.\n\nContext:\n- ..."
)
```
**Related**: prompt engineering, regression

## Key Concepts Summary

### What to test
- Your contracts: parsing, scoring, chunking, retries, validation
- Boundaries: empty, single, duplicate, max, invalid
- Error paths via `pytest.raises`

### What to mock
- Network (LLM APIs), clocks, randomness, file systems
- Mocks keep tests free, fast, and deterministic

### Structure
- AAA layout; one behavior per test
- `parametrize` instead of copy-paste
- Fixtures with the narrowest sufficient scope

### Discipline
- Deterministic: seed RNG, no wall-clock asserts, no network
- Coverage as signal; golden tests for prompt/template regressions

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `parametrize` — ___
2. `pytest.raises` — ___
3. `tmp_path` — ___
4. `side_effect` — ___
5. `monkeypatch` — ___
6. `patch` — ___
7. `pytest.approx` — ___
8. AAA — ___

A. Per-test temp directory, auto-cleaned
B. Replaces an attribute at the usage site for the test duration
C. One body, many (input, expected) cases
D. Asserts a block raises the named exception
E. Per-call results/raises on a Mock
F. Temporarily mutates env/attributes, restored after
G. Tolerance-aware float comparison
H. Arrange-Act-Assert test layout

**Answers:** 1-C, 2-D, 3-A, 4-E, 5-F, 6-B, 7-G, 8-H
