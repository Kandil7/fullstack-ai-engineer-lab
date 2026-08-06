# Advanced Python - 23: Typing Advanced

## Topic Overview

You already know `list[int]`, `Optional`, and function annotations. This lecture is the typing toolkit that production AI code actually ships with: **structural typing via `Protocol`** (so your `Retriever` interface accepts Qdrant, Chroma, and FAISS without inheritance), **generic functions and classes** that preserve type information through composition, **`TypeVar` and its bounds** for safe intersections, **`ParamSpec`** so decorators can forward a function's signature honestly, and **`Literal` / `TypeGuard` / `runtime_checkable`** for contracts the runtime can check. The exercise wraps this all in the canonical case from the phase doc: a typed `Retriever` protocol with Qdrant, Chroma, and FAISS implementations — one interface, three vector stores.

Two honest caveats come with the territory: `inspect.signature` shows *stringified* annotations (so runtime checks on parameters, not on annotation objects), and `runtime_checkable` protocols are **shallow** — they check only presence of members, not their signatures. Both are demonstrated in the exercise as teaching points rather than hidden bugs.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write `Protocol` classes and explain structural vs nominal typing
2. Make a class generic over a type parameter with `Generic[T]`
3. Use `TypeVar` with bounds to type intersections
4. Write `ParamSpec`-aware decorators that keep signatures
5. Use `Literal` and `TypeGuard` for narrow, checkable contracts
6. Explain what `runtime_checkable` can and cannot verify
7. Read `typing.get_type_hints` output in your own code

---

## Prerequisites

| Need | Where |
|---|---|
| Basic annotations: `list[int]`, `Optional` | `05-typing-fundamentals-lecture.md` |
| Classes and inheritance | Phase 1 OOP modules |
| Decorators with `functools.wraps` | `01-decorators-lecture.md` |
| Function overloading intuition | Phase 1 function modules |

---

## 1. Protocol: Contracts Without Inheritance

Nominal typing says "you are a `Retriever` because you inherit from it." **Structural typing** says "you are a `Retriever` because you have the same shape." `Protocol` declares the shape.

```python
from typing import Protocol

class Retriever(Protocol):
    def retrieve(self, query: str, k: int = 5) -> list[str]:
        ...

class QdrantRetriever:
    def retrieve(self, query: str, k: int = 5) -> list[str]:
        return [f"qdrant:{query[:10]}-{i}" for i in range(k)]

class ChromaRetriever:
    def retrieve(self, query: str, k: int = 5) -> list[str]:
        return [f"chroma:{query[:10]}-{i}" for i in range(k)]

def search(retriever: Retriever, query: str, k: int) -> list[str]:
    return retriever.retrieve(query, k)
```

```
qdrant-retrieves        -> ['qdrant:why-is-the-', 'qdrant:why-is-the-', ...]
chroma-retrieves        -> ['chroma:why-is-the-', 'chroma:why-is-the-', ...]
```

`search` never checks the class name — it checks the method. Swap Qdrant for Chroma and nothing in `search` changes. This is why the phase doc models the vector-store abstraction as a protocol: each store keeps its own driver, and the application depends on the shape, not the vendor.

---

## 2. Generic Classes: Preserving the Type

`Generic[T]` lets one class serve many element types *and* tell the type checker which one you used. Without generics, `vector_store.upsert(...)` would accept and return `Any`.

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Result(Generic[T]):
    def __init__(self, ok: bool, value: T | None, error: str | None = None) -> None:
        self.ok = ok
        self.value = value
        self.error = error

    @classmethod
    def success(cls, value: T) -> "Result[T]":
        return cls(True, value)

    @classmethod
    def failure(cls, error: str) -> "Result[T]":
        return cls(False, None, error)

def demo_generic() -> tuple[Result[int], Result[int]]:
    ok = Result.success(42)
    bad = Result.failure("embedding failed")
    return ok, bad
```

```
ok  -> Result(ok=True, value=42, error=None)
bad -> Result(ok=False, value=None, error='embedding failed')
```

`Result[T]` is the pattern behind typed error handling in pipelines: the value type travels with the wrapper, and callers get `int` out of `Result.success(42)` instead of `object | None`.

---

## 3. TypeVar Bounds: Type Intersections

A **bound** narrows what a type variable may be. `TypeVar("U", bound=float)` accepts `int` and `float` — but not `str` — and the result keeps the caller's actual type.

```python
Num = TypeVar("Num", bound=float)

def scale(v: Num, factor: float) -> Num:
    return v * factor          # type checker sees Num -> Num

def demo_bounds() -> tuple[int, float, str]:
    i: int = scale(10, 1.5)     # int in -> int out
    f: float = scale(2.5, 2.0)  # float in -> float out
    return i, f, "int 10 * 1.5 -> 15 | float 2.5 * 2.0 -> 5.0"
```

```
int 10 * 1.5 -> 15 | float 2.5 * 2.0 -> 5.0
```

The alternative — annotating `v: float` — would force callers to cast `int` to `float`. The bound keeps `scale(10, 1.5)` an `int`, which matters for code that then indexes or slices the result.

---

## 4. ParamSpec: Decorators That Tell the Truth

Without `ParamSpec`, a decorated function's signature collapses into `(*args: Any, **kwargs: Any)`: autocomplete dies and the type checker stops checking arguments. `ParamSpec` forwards the *original* signature.

```python
from typing import Callable, ParamSpec
import functools

P = ParamSpec("P")

def retry(times: int = 3) -> Callable[[Callable[P, str]], Callable[P, str]]:
    def decorator(func: Callable[P, str]) -> Callable[P, str]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ValueError:
                    if attempt == times:
                        raise
            return "unreachable"
        return wrapper
    return decorator

@retry(times=3)
def call_llm(prompt: str, temperature: float = 0.0) -> str:
    return f"FAKE:{prompt[:4]}:{temperature}"
```

```
FAKE:summ:0.0
```

Calling `call_llm("summarize")` type-checks its arguments exactly as if the decorator were not there — the wrapper's `P.args`/`P.kwargs` are the bridge. The exercise demonstrates the honest signature via `inspect.signature(wrapper)`, which shows `(prompt: str, temperature: float = 0.0)` — the decorated truth.

---

## 5. Literal and TypeGuard: Narrow Contracts

`Literal["dev", "prod"]` restricts a value, not a type. `TypeGuard` is a user-defined check that narrows a value's type for the caller — it says "if this returns True, the value is a `DocChunk`" even though the function only inspects a field.

```python
from typing import Literal, TypeGuard

Env = Literal["dev", "prod", "test"]

class DocChunk:
    def __init__(self, chunk_id: int, text: str) -> None:
        self.chunk_id = chunk_id
        self.text = text

class BadChunk:
    def __init__(self, chunk_id: int, text: str) -> None:
        self.chunk_id = chunk_id
        self.text = text

def is_doc_chunk(obj: object) -> TypeGuard[DocChunk]:
    return hasattr(obj, "chunk_id") and hasattr(obj, "text")

def demo_narrowing() -> tuple[str, str]:
    env: Env = "prod"
    good: object = DocChunk(1, "text")
    bad: object = BadChunk(1, "text")
    return (env + "-valid", "chunk" if is_doc_chunk(good) else "not", "chunk" if is_doc_chunk(bad) else "not")
```

```
prod-valid | good is a chunk | bad is a chunk too (shallow check)
```

The honest caveat: `is_doc_chunk(BadChunk(1, "text"))` returns **True** because the check is structural — both classes have the attributes. A real type guard would check for a distinguishing marker (e.g. `isinstance(obj, DocChunk)` or a `kind` field). That is the teaching point, not a flaw in the code.

---

## 6. runtime_checkable: What It Can Verify

`@runtime_checkable` lets `isinstance` work on a protocol — but only *shallowly*: it checks that members exist, never their signatures. A class whose `retrieve` takes completely different parameters still passes `isinstance`.

```python
from typing import runtime_checkable

class WrongSignatureRetriever:
    def retrieve(self, top_k: int) -> list[str]:   # different signature entirely
        return ["x"]

def demo_checkable() -> tuple[bool, str]:
    wrong = WrongSignatureRetriever()
    return isinstance(wrong, Retriever), "passes isinstance but has the WRONG shape"
```

```
True | passes isinstance but has the WRONG shape
```

The protocol is `@runtime_checkable` in the exercise precisely so this class *is* recognized by `isinstance` — demonstrating the shallow behavior. The lesson: `isinstance` against a protocol is a cheap sanity gate, not a signature verifier. If the contract must be enforced, validate the signature explicitly (as the exercise's `_verify()` does by inspecting parameter names) — and even then, annotations are strings at runtime.

---

## 7. Annotations Are Strings at Runtime

Python does not evaluate annotations at function definition time (unless you opt in). `inspect.signature` shows the *stringified* forms — which is why the exercise's asserts check parameter *names*, not annotation objects.

```python
import inspect

def demo_hints() -> tuple[list[str], list[str]]:
    sig = inspect.signature(search)
    params = list(sig.parameters.keys())
    ret = sig.return_annotation
    return params, [str(ret)]
```

```
('query', 'k') | 'list[str]' is shown as the string 'list[str]'
```

`typing.get_type_hints` resolves the strings *when they can be evaluated* (they can be, since `list` and `str` are builtins — so the exercise prints the resolved hints). The design lesson: use `get_type_hints` for introspection; use parameter *names* for robust runtime contract checks; never rely on `is` comparison of annotation objects in hot code.

---

## Common Mistakes to Avoid

### Mistake 1: `runtime_checkable` as a signature guard
```
# WRONG -- passes isinstance despite a broken signature
@runtime_checkable
class Retriever(Protocol):
    def retrieve(self, query: str, k: int = 5) -> list[str]: ...
class Wrong:
    def retrieve(self, top_k: int) -> list[str]: ...
isinstance(Wrong(), Retriever)   # True -- shallow check!
# CORRECT -- also validate the signature (parameter names) explicitly
```

### Mistake 2: Bare `TypeVar` when you need a bound
```
# WRONG -- accepts str silently
def double(v: T) -> T: ...
# CORRECT -- int/float only, result keeps caller's type
Num = TypeVar("Num", bound=float)
def scale(v: Num, factor: float) -> Num: ...
```

### Mistake 3: Decorator that erases the signature
```
# WRONG -- *args/**kwargs hides the real contract
def retry(f):
    def wrapper(*args, **kwargs): ...
# CORRECT -- ParamSpec forwards P.args/P.kwargs and functools.wraps keeps metadata
```

### Mistake 4: TypeGuard on a shallow check
```
# WRONG -- structural check claims a guarantee it cannot keep
def is_doc_chunk(obj: object) -> TypeGuard[DocChunk]:
    return hasattr(obj, "chunk_id") and hasattr(obj, "text")
# CORRECT -- check for a distinguishing marker, not shared attribute names
```

### Mistake 5: Comparing annotation objects at runtime
```
# WRONG -- annotations are strings until get_type_hints resolves them
assert inspect.signature(f).return_annotation is list[str]   # unreliable
# CORRECT
hints = typing.get_type_hints(f)  # resolved, but still compare carefully
```

---

## Best Practices

1. **Model interfaces with `Protocol`** — vendor classes stay independent.
2. **Make wrappers generic** — `Result[T]` preserves the value type.
3. **Bind `TypeVar`s** to what the operation can actually accept.
4. **Use `ParamSpec` in every decorator** that wraps a callable.
5. **`Literal` for enum-ish strings**, not `str`.
6. **`TypeGuard` only for checks that genuinely narrow** — add a marker if needed.
7. **Treat `runtime_checkable` as a shallow gate**; verify signatures separately.
8. **Introspect with `get_type_hints`**, assert on parameter names.
9. **Keep vendor imports out of the protocol file** — the interface owns no drivers.
10. **Run mypy on the protocol boundary** — this is exactly what static checking catches.

---

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Protocol dispatch | O(1) attribute lookup | O(1) | inheritance — same, but couples classes |
| Generic instantiation | O(1) — erased at runtime | O(1) | untyped `Any` — loses checks entirely |
| `runtime_checkable` isinstance | O(n) members | O(1) | `hasattr` — same cost, less formal |
| `get_type_hints` | imports/evaluates strings | annotation cache | `inspect.signature` — names only |
| ParamSpec wrapper call | O(1) overhead | O(1) | plain wrapper — loses signature |
| TypeGuard call | O(1) | O(1) | isinstance — same, but nominal |

Typing constructs are **zero-runtime-cost** — generics, protocols, and TypeVars are erased. The only real costs are introspection calls you should keep out of hot paths.

---

## AI Engineering Relevance

**Where this shows up:** the phase doc's canonical case is a typed `Retriever` protocol with Qdrant, Chroma, and FAISS implementations. In production you also see: `Literal`-typed model names in an LLM client, `Result[T]` for pipeline stages that can fail, `ParamSpec`-aware `retry`/`rate_limit` decorators wrapping provider calls, and `TypeGuard`-style parsing of model outputs. LLM function calling schemas map almost 1:1 to typed signatures — the same `Literal` and parameter annotations you write here become the JSON schema the model must match.

| Concept here | Used for |
|---|---|
| `Protocol` | one `Retriever` interface over Qdrant/Chroma/FAISS |
| `Generic[T]` / `Result[T]` | typed success/failure through pipeline stages |
| `TypeVar` bounds | numeric ops that keep `int` as `int` |
| `ParamSpec` | retry/rate-limit decorators that don't lie about signatures |
| `Literal` | model names, envs, modes as closed value sets |
| `TypeGuard` | validating parsed LLM output before use |
| `get_type_hints` | schema generation from function signatures |

**Scale note:** at interface boundaries, structural typing removes the "swap the vector store" refactor — the protocol is the seam. The same seam makes testing honest: a `FakeLLMClient` that satisfies the `LLMClient` protocol is indistinguishable from the real one to every consumer (which `26-design-patterns-advanced.py` then exploits with dependency injection).

---

## Practice Exercises

### Exercise 1: Protocol Swap (Difficulty: Easy)
Write `QdrantRetriever` and `ChromaRetriever` against a `Retriever` protocol; call a shared `search()` with both. Add a third store that *fails* the protocol and explain why.

### Exercise 2: Generic Result (Difficulty: Medium)
Build `Result[T]` with `success`/`failure` classmethods. Use it in a pipeline `parse -> embed -> store` where each stage returns `Result[NextType]`. Assert the failure path short-circuits.

### Exercise 3: ParamSpec Retry (Difficulty: Medium)
Write a `@retry(times=2)` decorator with `ParamSpec`; decorate `call_llm(prompt: str, temperature: float = 0.0)`. Assert `inspect.signature` shows the original parameters, and that a ValueError on attempt 1 succeeds on attempt 2.

### Exercise 4: Bounded Numerics (Difficulty: Medium)
Implement `scale(v: Num, factor: float) -> Num` with a bound. Assert `scale(10, 1.5)` is an `int` (type-level) by annotating the variable and assigning.

### Exercise 5: Shallow Check Honesty (Difficulty: Hard)
Create `WrongSignatureRetriever` whose `retrieve(top_k: int)` differs from the protocol. Assert `isinstance` passes (shallow) and that an explicit parameter-name check catches the mismatch. Document both results.

### Exercise 6: Schema From Signature (Difficulty: Hard)
Write a function that takes a callable and builds a JSON-schema-like dict from its parameters using `inspect.signature` + `typing.get_type_hints`. Verify it correctly describes `call_llm`.

---

## Summary

| Concept | Description |
|---|---|
| `Protocol` | structural contract; shape, not inheritance |
| `Generic[T]` | class-level type parameter, erased at runtime |
| `TypeVar(bound=...)` | constrained type intersection, keeps caller's type |
| `ParamSpec` | forwards a decorated function's true signature |
| `Literal[...]` | closed set of allowed values |
| `TypeGuard` | user-defined narrowing that callers trust |
| `runtime_checkable` | shallow isinstance; members only, never signatures |
| `get_type_hints` | resolves stringified annotations at runtime |

The theme: typing pays for itself at the **boundaries** — where vendors swap, where decorators wrap, where parsing meets code. Inside those seams, the runtime never sees a single type object; but the type checker sees everything, which is exactly the point.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Interface without inheritance | `class Retriever(Protocol): def retrieve(...): ...` |
| Typed wrapper | `class Result(Generic[T]): ...` |
| Numeric-only type var | `Num = TypeVar("Num", bound=float)` |
| Signature-preserving decorator | `P = ParamSpec("P")`; `wrapper(*args: P.args, **kwargs: P.kwargs)` |
| Closed value set | `Env = Literal["dev", "prod", "test"]` |
| User narrowing | `def is_x(o: object) -> TypeGuard[X]: ...` |
| Runtime isinstance on protocol | `@runtime_checkable` — remember: shallow |
| Resolve annotations | `typing.get_type_hints(func)` |

---

## Next Steps

Next: **[24-memory-and-gc-lecture.md](24-memory-and-gc-lecture.md)** — the memory side of scale: refcounts, cycles, weak references, `__slots__`, and `tracemalloc` hunting.
Continues in: **[30-advanced-typing](../../../02-advanced-python/30-advanced-typing.py)** (Phase 2 topic 30) — `TypeIs`, `Self`, `Unpack`/`TypeVarTuple`, and `NewType` in depth.
Official docs: [typing](https://docs.python.org/3/library/typing.html), [Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol), [ParamSpec](https://docs.python.org/3/library/typing.html#typing.ParamSpec), [TypeGuard](https://docs.python.org/3/library/typing.html#typing.TypeGuard).
