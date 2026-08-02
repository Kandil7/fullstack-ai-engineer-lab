# Python Clean Code Checklist

> PEP8 + Pythonic idioms + patterns that matter in AI/ML code. Source: planning conversation
> 2026-07-31, decomposed 2026-08-02. Working examples live in
> [`projects/00-core-foundations/python/02-advanced-python/`](../../projects/00-core-foundations/python/02-advanced-python/).

**PEP8** is the formatting standard — naming, spacing, line length. Mechanical, and a tool can
enforce it. **Pythonic** means writing in the language's own idiom rather than transliterating
from another language. A formatter cannot enforce that; review can.

---

## 1. PEP8 essentials

### Naming

```python
user_name = "Ahmed"        # snake_case — variables, functions
def calculate_score(): ...  # snake_case
class ModelTrainer: ...     # PascalCase — classes
MAX_EPOCHS = 100            # UPPER_CASE — constants
_internal = 1               # single underscore — private by convention
__mangled = 2               # double underscore — name mangling
```

Avoid: `camelCase` variables, `snake_case` class names.

### Formatting

- Line length: 79 per PEP8; 88 (Black default) or 100 in most modern projects. Pick one and
  enforce it in CI.
- Spaces around operators: `x = 1 + 2`, not `x = 1+2`.
- Two blank lines before module-level function and class definitions.
- Imports grouped and ordered: standard library → third-party → local, blank line between.

### Enforce automatically

```bash
ruff check .        # lint
ruff format .       # or: black .
mypy src/           # type checking
```

Run these in CI so style stops being a review topic. This repo:
`.github/workflows/ci.yml`, configured in `pyproject.toml`.

---

## 2. Pythonic idioms

| Instead of | Write |
| --- | --- |
| `for i in range(len(data)):` | `for i, item in enumerate(data):` |
| parallel indexing into two lists | `for name, score in zip(names, scores):` |
| a loop that appends to a list | a comprehension |
| `x = point[0]; y = point[1]` | `x, y, z = point` |
| `if x == None:` | `if x is None:` |
| `if len(items) > 0:` | `if items:` |
| `if k in d: v = d[k] else: v = default` | `v = d.get(k, default)` |
| `"a: " + str(b)` | `f"a: {b:.2f}"` |
| manual `open`/`close` | `with open(...) as f:` |

```python
# comprehensions
squares = [i ** 2 for i in range(10)]
labels = {i: f"class_{i}" for i in range(5)}

# partial unpacking
first, *rest = [1, 2, 3, 4, 5]

# multiple resources in one with
with open("in.txt") as fin, open("out.txt", "w") as fout:
    fout.write(fin.read().upper())
```

---

## 3. The mutable default argument trap

```python
# WRONG — the list is created once, at definition time, and shared across every call
def add_item(item, items=[]):
    items.append(item)
    return items

# RIGHT
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

The classic Python bug. It shows up in interviews and in real code — most often in config
dicts and accumulator lists.

---

## 4. Context managers

Use one wherever setup and teardown must happen together, guaranteed, including on exception.

### Class form

```python
class DatabaseConnection:
    def __enter__(self):
        self.conn = connect()
        return self.conn              # bound by `as`

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()             # always runs
        return False                  # False/None → exception propagates
                                      # True       → exception is swallowed
```

### Generator form

```python
from contextlib import contextmanager

@contextmanager
def database_connection():
    conn = connect()
    try:
        yield conn                    # everything before = __enter__
    finally:
        conn.close()                  # everything after  = __exit__
```

### AI/ML uses

```python
# timing
@contextmanager
def timer(name):
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"{name}: {time.perf_counter() - start:.2f}s")

# gradient suppression
with torch.no_grad():
    predictions = model(X_test)

# temporary state, restored even on error
@contextmanager
def eval_mode(model):
    model.eval()
    try:
        yield model
    finally:
        model.train()
```

⚠️ Returning `True` from `__exit__` **swallows the exception**. Almost always a bug; use it
only where suppression is the deliberate, documented purpose.

Full treatment: `02-advanced-python/03-context-managers.py` and its lecture.

---

## 5. Type hints

Non-negotiable in production code, and the basis of Pydantic validation.

```python
def train_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    epochs: int = 10,
) -> Model:
    ...

def chunk(text: str, size: int, overlap: int = 0) -> list[str]:
    ...
```

Modern syntax: `list[str]` not `List[str]`; `str | None` not `Optional[str]` (3.10+).
Enforce with mypy in CI.

---

## 6. Applied — before and after

```python
# before
def process(D):
    R = []
    for i in range(len(D)):
        if D[i] != None:
            if D[i] > 0:
                R.append(D[i] * 2)
    return R

# after
def double_positive_values(data: list[float]) -> list[float]:
    """Return positive values from `data`, doubled. None entries are skipped."""
    return [value * 2 for value in data if value is not None and value > 0]
```

Changed: meaningful names, type hints, docstring, comprehension over nested loop, `is not
None` over `!= None`.

---

## 7. General principles

- **One function, one responsibility.**
- **Clear names beat comments.** A comment explaining *what* code does usually means the code
  should be renamed.
- **DRY**, but not at the cost of coupling unrelated things.
- **Short functions.** Longer than a screen is usually two functions.
- **Type hints on anything crossing a module boundary.**
- **Docstrings on public functions**, stating what and why — not restating the signature.

---

## Review checklist

Before committing:

- [ ] `ruff check` and formatter clean
- [ ] `mypy` clean on changed files
- [ ] No mutable default arguments
- [ ] Resources acquired via `with`
- [ ] Type hints on public functions
- [ ] Names describe intent; no single letters outside comprehensions and math
- [ ] No commented-out code
- [ ] No secrets, keys, or absolute local paths
- [ ] New behaviour has a test

---

## Related

- [`../../projects/00-core-foundations/python/02-advanced-python/`](../../projects/00-core-foundations/python/02-advanced-python/)
  — 20 topics with lectures
- [`../../.ai/prompts/roles/code-reviewer.md`](../../.ai/prompts/roles/code-reviewer.md)
- [`../../.ai/prompts/critics/code-quality-validator.md`](../../.ai/prompts/critics/code-quality-validator.md)

*Extracted 2026-08-02 from `docs/plan/archive/Python-essentials-for-AI-engineers.md`*
