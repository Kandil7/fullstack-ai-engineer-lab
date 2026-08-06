# Challenge 26: Design Patterns Advanced

Register tools declaratively, build an undoable editor, and prove
constructor injection with a signature check.

## 🥉 Bronze — Registry Dispatch (~15 min)

**Task:** Implement `Tool` with an `__init_subclass__` registry plus
two tools, and a dispatcher:

1. `Tool` — `registry: dict[str, type["Tool"]]`; every subclass
   registers itself under its lowercase class name via
   `__init_subclass__`; `run(args)` raises `NotImplementedError`.
2. `Calculator(Tool)` — `run({"a": 2, "b": 3})` → `"5"`.
3. `Search(Tool)` — `run({"q": "rag"})` → `"results-for:rag"`.
4. `registry_dispatch(name, args) -> str` — instantiate the tool by
   name and run it; raise `ValueError` for unknown names.

**Signature:**
```python
def registry_dispatch(name: str, args: dict) -> str:
```

| Input | Expected |
|---|---|
| `("calculator", {"a": 2, "b": 3})` | `"5"` |
| `("search", {"q": "rag"})` | `"results-for:rag"` |
| `("unknown", {})` | `ValueError` |

**Constraints:** no manual `registry["calculator"] = Calculator` line —
registration must come from `__init_subclass__` (a source inspection
checks `solution.py` does not assign to the registry by hand).

---

## 🥈 Silver — Undoable Editor (~35 min)

**Task:** Implement `Editor` with an undo/redo history:

- `insert(offset, text)` — insert text at offset; `delete(offset,
  count)` — delete `count` chars; `undo()` — reverse the last
  operation; `redo()` — re-apply it; `text()` — the current buffer
  (as a string).

**Signature:**
```python
class Editor:
    def insert(self, offset: int, text: str) -> None
    def delete(self, offset: int, count: int) -> None
    def undo(self) -> None
    def redo(self) -> None
    def text(self) -> str
```

| Sequence | Expected `text()` |
|---|---|
| `insert(0, "hello")` | `"hello"` |
| `+ delete(0, 2)` | `"llo"` |
| `+ undo()` | `"hello"` |
| `+ undo()` | `""` |
| `+ redo()` | `"hello"` |
| `+ insert(5, "!")` then `undo()` | `"hello"` |

**Constraints:** `delete` must capture the removed text **at
construction** — undo restores the exact deleted substring, not a
placeholder. A command without captured state cannot pass the delete
undo tests. New operations after undo must discard the redo history.

---

## 🥇 Gold — Constructor Injection (~75 min)

**Task:** Build the DI seam:

1. `LLMClient` — a `Protocol` with `complete(prompt: str,
   temperature: float = 0.0) -> str`.
2. `RealLLMClient` — returns `f"REAL:{prompt[:5]}:{temperature}"`.
3. `FakeLLMClient` — returns `f"FAKE:{prompt[:5]}:{temperature}"`.
4. `Summarizer` — takes `llm` **through its constructor** and calls it
   from `summarize(text)`.

**Signatures:**
```python
class Summarizer:
    def __init__(self, llm: LLMClient) -> None
    def summarize(self, text: str) -> str
```

| Call | Expected |
|---|---|
| `Summarizer(FakeLLMClient()).summarize("x")` | starts with `"FAKE:"` |
| `Summarizer(RealLLMClient()).summarize("x")` | starts with `"REAL:"` |
| `inspect.signature(Summarizer.__init__)` | has an `llm` parameter |

**Constraints:** the signature check is the point — a `Summarizer`
that constructs its client *inside* (`self._llm = FakeLLMClient()` in
`__init__`) has no `llm` parameter and fails. Both clients must satisfy
the `LLMClient` protocol exactly.

---

## Running

```bash
pytest challenges/26-design-patterns-advanced/test_challenge.py -v
```

Tests default to **starter.py** (must fail). To verify the reference
implementation:

```bash
# PowerShell
$env:CHALLENGE_MODULE = "solution"
pytest challenges/26-design-patterns-advanced/test_challenge.py -v
```

## Test File Structure

```
challenges/26-design-patterns-advanced/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
