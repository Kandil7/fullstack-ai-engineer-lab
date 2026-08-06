# Challenge 23: Typing Advanced

Introspect signatures honestly, build a runtime contract check that
beats the shallow `isinstance` trap, and ship a typed retrieval seam
with a generic `Result`.

## 🥉 Bronze — Schema From Signature (~15 min)

**Task:** Implement `build_schema(func)` — introspect a function and
return its contract as a dict: `name`, `params` (list of `(name,
default)` tuples in order, `None` when the parameter has no default),
and `return` (the *stringified* return annotation, or `"None"` if
unannotated).

**Signature:**
```python
def build_schema(func) -> dict:
```

For `def sample(a: int, b: str = "x") -> bool`:

| Field | Expected |
|---|---|
| `name` | `"sample"` |
| `params` | `[("a", None), ("b", "x")]` |
| `return` | `"bool"` |

**Constraints:** use `inspect.signature`. Annotations are strings at
runtime — `str(sig.return_annotation)` is the honest value.

---

## 🥈 Silver — Signature Check That Actually Checks (~35 min)

**Task:** Implement `signature_matches(func, expected)` — return `True`
only if the function's parameter *names* match `expected` exactly, in
order.

**Signature:**
```python
def signature_matches(func, expected: list[str]) -> bool:
```

| Input | Expected |
|---|---|
| `(sample, ["a", "b"])` | `True` |
| `(sample, ["b", "a"])` | `False` (order matters) |
| `(sample, ["a"])` | `False` (missing param) |
| `(sample, ["a", "b", "c"])` | `False` (extra param) |

**Constraints:** parameter *names* are the robust runtime signal —
annotations are stringified and unreliable to compare. This is the
check `runtime_checkable` cannot do (it only sees member *existence*).

---

## 🥇 Gold — The Seam That Rejects Wrong Shapes (~75 min)

**Task:** Build the typed retrieval seam. In your module:

1. `Retriever` — a `@runtime_checkable` `Protocol` with
   `def retrieve(self, query: str, k: int = 5) -> list[str]: ...`
2. `QdrantRetriever` / `ChromaRetriever` — two classes satisfying the
   protocol exactly; `retrieve` returns
   `[f"qdrant:{query[:8]}-{i}" ...]` / `"chroma:..."`.
3. `WrongSignatureRetriever` — `def retrieve(self, top_k: int)` —
   deliberately wrong, to prove the trap.
4. `Result(Generic[T])` — `success(value)` / `failure(error)` with
   `.ok`, `.value`, `.error`.
5. `verify_retriever(obj) -> bool` — returns `True` **only if**
   `isinstance(obj, Retriever)` *and* the signature check passes.

**Signatures:**
```python
def verify_retriever(obj) -> bool
def safe_search(retriever, query: str, k: int = 5) -> Result[list[str]]
```

| Call | Expected |
|---|---|
| `verify_retriever(QdrantRetriever())` | `True` |
| `verify_retriever(ChromaRetriever())` | `True` |
| `verify_retriever(WrongSignatureRetriever())` | `False` — *but* `isinstance(..., Retriever)` is `True` |
| `safe_search(QdrantRetriever(), "hello")` | `Result(ok=True, value=['qdrant:hello-0', ...], error=None)` |

**Constraints:** the isinstance-only check (the naive solution) returns
`True` for the wrong-shape class — the explicit signature check is what
catches it. `safe_search` must fail gracefully: a non-retriever
argument yields `Result.failure` instead of raising.

---

## Running

```bash
pytest challenges/23-typing-advanced/test_challenge.py -v
```

Tests default to **starter.py** (must fail). To verify the reference
implementation:

```bash
# PowerShell
$env:CHALLENGE_MODULE = "solution"
pytest challenges/23-typing-advanced/test_challenge.py -v
```

## Test File Structure

```
challenges/23-typing-advanced/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
