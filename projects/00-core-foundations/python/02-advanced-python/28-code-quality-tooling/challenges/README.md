# Challenge 28: Code Quality Tooling

Build a mini linter on the `ast` module — the same machinery ruff uses,
with zero dependencies, so it runs in any CI.

## 🥉 Bronze — Mutable Default Finder (~15 min)

**Task:** Implement `find_mutable_defaults(source: str) -> list[tuple[int, str]]`
that parses Python source and returns `(line, function_name)` for every
function whose default argument is a mutable object (list/dict/set literals,
or calls to `list()`/`dict()`/`set()`). Never execute the source — parse only.

**Signature:**
```python
def find_mutable_defaults(source: str) -> list[tuple[int, str]]: ...
```

| Input | Expected |
|-------|----------|
| `"def f(a=[]):\n    pass\n"` | `[(1, "f")]` |
| `"def f(a=None, b={}):\n    pass\n"` | `[(1, "f")]` (only `b` is bad, one hit) |
| `"def f(a=5, b='x'):\n    pass\n"` | `[]` |
| `""` | `[]` |

**Constraints:** n ≤ 10^4 AST nodes. Single `ast.parse`, single walk.
Immutables (`None`, `int`, `str`, `tuple`) must never be flagged.

---

## 🥈 Silver — Multi-Rule Analyzer (~35 min)

**Task:** Implement `analyze(source: str, max_complexity: int = 10)`
returning `{"B006": [...], "E722": [...], "C901": [...]}` where:
- `B006` — mutable defaults, as in Bronze
- `E722` — bare `except:` line numbers
- `C901` — `(lineno, "name: complexity N > M")` for top-level functions
  whose cyclomatic complexity (1 + decisions: `if`/`for`/`while`/`except`/
  `and`/`or`/ternary) exceeds `max_complexity`

**Signature:**
```python
def analyze(source: str, max_complexity: int = 10) -> dict[str, list[tuple[int, str]]]: ...
```

| Input | Expected |
|-------|----------|
| `"def f(x):\n    if x:\n        return 1\n    return 0\n"` | `C901 == []` with default cap (complexity 2 ≤ 10) |
| `"def f(x):\n    if x:\n        return 1\n    return 0\n"` | `C901` flags it with `max_complexity=1` |
| `"try:\n    x()\nexcept:\n    pass\n"` | `E722 == [(3, "bare except")]` |

**Constraints:** n ≤ 10^5 nodes. **The source must be parsed exactly once**
across all three rules — a solution that re-parses per rule is wrong
(measured: `ast.parse` is called once, or the test fails).

---

## 🥇 Gold — Full Linter with noqa + Config (~75 min)

**Task:** Implement `lint_source(source: str, config: dict | None = None)`
returning `{"RULE": [(line, message), ...]}` for all rules above plus:

- `E501` — lines longer than `config["max_line_length"]` (default 88)
- `E999` — syntax errors, as `[(line, "syntax error")]` — must not crash
- **noqa discipline:** a violation on a line whose source carries
  `# noqa` (with or without a rule code) is suppressed
- **select/ignore:** `config = {"select": ["B006", "E722"], "ignore": ["E722"]}`
  runs only the selected rules minus the ignored ones

Empty dict on fully clean source. The linter must visit every AST node
exactly once — expose the visit count as `lint_source.last_visit_count`.

**Signature:**
```python
def lint_source(source: str, config: dict[str, list[str]] | None = None) -> dict[str, list[tuple[int, str]]]: ...
```

| Input | Expected |
|-------|----------|
| `"def f(x=[]):  # noqa: B006\n    return x\n"` | `{}` |
| `"def f(x=[]):\n    return x\n"` | `{"B006": [(1, "f")]}` (message contains `f`) |
| `"def broken(:\n"` | `{"E999": [(1, "syntax error")]}` |

**Constraints:** source up to 10^4 lines; `last_visit_count` must equal the
total node count from a reference `ast.walk` (single pass, O(n)); peak
memory for a 2,000-function generated source must stay within 2x of a bare
`ast.parse` on the same source (measured with `tracemalloc`).

**Follow-up:** what breaks first at 10^6 lines? (Answer: `ast.parse` is
C-speed and fine; the per-node Python-level visit becomes the bottleneck —
that's why ruff is Rust, not Python.)

---

## Running

```bash
pytest challenges/28-code-quality-tooling/test_challenge.py -v
```
