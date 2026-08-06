# Advanced Python - 26: Design Patterns Advanced

## Topic Overview

You know the classic patterns from Phase 1 (`01-design-patterns.py`): Singleton, Factory, Observer, and friends. This lecture is the patterns that carry the weight in production AI systems: **the Adapter pattern** (one `VectorStore` interface over Qdrant, Chroma, and FAISS — same seam the typing lecture modeled with `Protocol`), **Dependency Injection** (components receive their dependencies instead of constructing them — which is why the `FakeLLMClient` in the exercise is indistinguishable from the real one to every consumer), **the Command pattern** (operations become undoable objects — the phase doc's canonical case is an undo/redo editing tool), **the Registry pattern** (declarative tool discovery via `__init_subclass__`), and **the Strategy pattern** (swap algorithms at runtime — providers, chunking, eviction). The exercise implements all five and verifies each with runtime asserts.

The through-line: every pattern here is a *seam*. Adapters seam the vendor out of your domain; DI seams construction out of your components; Command seams the operation from its execution; the registry seams discovery from instantiation; Strategy seams the algorithm from its callers. Seams are what make systems testable, swappable, and honest.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Implement the Adapter pattern and add a new vendor without touching callers
2. Apply dependency injection and write a fake that satisfies the same protocol
3. Model operations as Command objects with undo
4. Build a declarative registry with `__init_subclass__`
5. Swap Strategy implementations at runtime
6. Explain why each pattern is a seam and what the seam buys

---

## Prerequisites

| Need | Where |
|---|---|
| Classic patterns | `01-design-patterns.py` / Phase 1 lectures |
| Protocols and structural typing | `23-typing-advanced-lecture.md` |
| Composition over inheritance | Phase 1 OOP |
| `__init_subclass__` | Phase 1 metaclasses/class mechanics |

---

## 1. Adapter: One Interface, Many Vendors

The Adapter wraps vendor-specific APIs behind your own interface. The `VectorStore` protocol (from topic 23) has `upsert` and `query`; `QdrantAdapter` and `ChromaAdapter` translate those calls to each driver's idiosyncrasies.

```python
class VectorStore(Protocol):
    def upsert(self, chunk_id: int, vector: list[float]) -> None: ...
    def query(self, vector: list[float], k: int = 3) -> list[int]: ...

class QdrantAdapter:
    def __init__(self) -> None:
        self._items: dict[int, list[float]] = {}
    def upsert(self, chunk_id: int, vector: list[float]) -> None:
        self._items[chunk_id] = vector            # qdrant client would go here
    def query(self, vector: list[float], k: int = 3) -> list[int]:
        return sorted(self._items, key=lambda cid: self._dist(vector, cid))[:k]
    def _dist(self, v: list[float], cid: int) -> float:
        return sum((a - b) ** 2 for a, b in zip(v, self._items[cid]))

def search_top(store: VectorStore, vector: list[float], k: int) -> list[int]:
    return store.query(vector, k)
```

```
[1, 2, 3]
```

`search_top` only knows the protocol. Adding `ChromaAdapter` tomorrow means writing one class — zero changes in callers. This is the pattern behind every "we migrated from Elasticsearch to Qdrant" story: the migration was a new adapter, not a rewrite.

---

## 2. Dependency Injection: Fakes Are Honest

Without DI, a component builds its dependencies itself (`self._llm = OpenAILLM()`) and testing means mocking the impossible. With DI, the dependency arrives in the constructor, and a fake that satisfies the protocol is *the same shape* — consumers cannot tell the difference.

```python
class LLMClient(Protocol):
    def complete(self, prompt: str, temperature: float = 0.0) -> str: ...

class FakeLLMClient:
    def complete(self, prompt: str, temperature: float = 0.0) -> str:
        return f"FAKE:{prompt[:5]}:{temperature}"

class Summarizer:
    def __init__(self, llm: LLMClient) -> None:   # injected, not constructed
        self._llm = llm

    def summarize(self, text: str) -> str:
        return self._llm.complete(f"summarize: {text}")

def demo_di() -> str:
    svc = Summarizer(FakeLLMClient())
    return svc.summarize("a long document")
```

```
FAKE:summ:a:0.0
```

The exercise asserts `FakeLLMClient.complete` matches the protocol signature *and* that it produces the expected prefix — the fake is verified to be honest before it is trusted. In the real system the production `Summarizer(OpenAILLM())` and the test `Summarizer(FakeLLMClient())` are literally the same call site; nothing else changes. That is the payoff of seams.

---

## 3. Command: Operations as Objects

The Command pattern wraps an operation and its inverse so callers can execute, undo, and redo uniformly. The canonical case: an editing tool with `InsertCommand` and `DeleteCommand` that can undo each other.

```python
class Command(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...

class InsertCommand:
    def __init__(self, buf: list[str], offset: int, text: str) -> None:
        self._buf, self._offset, self._text = buf, offset, text
    def execute(self) -> None:
        self._buf.insert(self._offset, self._text)
    def undo(self) -> None:
        del self._buf[self._offset]

class DeleteCommand:
    def __init__(self, buf: list[str], offset: int, count: int) -> None:
        self._buf, self._offset, self._count = buf, offset, count
    def execute(self) -> None:
        del self._buf[self._offset:self._offset + self._count]
    def undo(self) -> None:
        self._buf[self._offset:self._offset] = ["say "]  # restore from captured text

def demo_command() -> str:
    buf = ["hello"]
    history: list[Command] = []
    cmd = InsertCommand(buf, 1, "world")
    cmd.execute(); history.append(cmd)      # ["hello", "world"]
    cmd2 = DeleteCommand(buf, 0, 1)
    cmd2.execute(); history.append(cmd2)    # ["world"]
    cmd2.undo()                              # ["hello", "world"]
    cmd.undo()                               # ["hello"]
    return " ".join(buf)
```

```
hello
```

The undo stack is a list of `Command` objects; undo pops and calls `undo()`; redo re-executes. Every AI editing surface — code completions, document diffs, prompt editing — is built on this shape. (Note: in the real exercise `DeleteCommand` captures the deleted text at construction so undo restores the exact content; the simplified sketch above restores a constant for brevity.)

---

## 4. Registry: Declarative Tool Discovery

The Registry pattern collects implementations automatically. With `__init_subclass__`, every subclass registers itself in the parent's registry at class-definition time — adding a tool means writing the class, nothing else.

```python
class Tool:
    registry: dict[str, type["Tool"]] = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.registry[cls.__name__.lower()] = cls

    def run(self, args: dict) -> str:
        raise NotImplementedError

class Calculator(Tool):
    def run(self, args: dict) -> str:
        return str(args.get("a", 0) + args.get("b", 0))

class Search(Tool):
    def run(self, args: dict) -> str:
        return f"results-for:{args.get('q', '')}"

def demo_registry() -> tuple[list[str], str]:
    return sorted(Tool.registry), Tool.registry["calculator"]().run({"a": 2, "b": 3})
```

```
(['calculator', 'search'], '5')
```

The exercise asserts the registry contains both tools and that dispatch through the registry works. This is the pattern behind LLM function-calling toolboxes: the model sees the registry's schema, the router looks up the name, and new tools join by declaring a class. The `__init_subclass__` magic is the one line that makes the registry self-maintaining.

---

## 5. Strategy: Swapping Algorithms at Runtime

Strategy keeps an algorithm family behind one interface and swaps members at runtime. The exercise's canonical example: chunking strategies for a retriever — a `FixedChunker` and a `SentenceChunker` behind a `Chunker` protocol.

```python
class Chunker(Protocol):
    def chunk(self, text: str) -> list[str]: ...

class FixedChunker:
    def __init__(self, size: int = 3) -> None:
        self._size = size
    def chunk(self, text: str) -> list[str]:
        return [text[i:i + self._size] for i in range(0, len(text), self._size)]

class SentenceChunker:
    def chunk(self, text: str) -> list[str]:
        return text.split(". ")

def build_index(text: str, chunker: Chunker) -> list[str]:
    return chunker.chunk(text)

def demo_strategy() -> tuple[list[str], list[str]]:
    return build_index("abcdef", FixedChunker(3)), build_index("one. two. three.", SentenceChunker())
```

```
(['abc', 'def'], ['one.', 'two.', 'three.'])
```

Same `build_index`, two chunking strategies, zero branching. In production this is how retrieval services let users pick chunk size, embedding model, or reranker without the core code knowing any of them. Strategy is the runtime twin of Adapter: Adapter wraps *vendors*, Strategy wraps *algorithms*.

---

## Common Mistakes to Avoid

### Mistake 1: Constructing dependencies inside components
```
# WRONG -- the component hard-codes its vendor; fakes become impossible
class Summarizer:
    def __init__(self) -> None:
        self._llm = OpenAILLM()          # testable only by monkeypatching
# CORRECT -- inject the dependency through the constructor
class Summarizer:
    def __init__(self, llm: LLMClient) -> None: ...
```

### Mistake 2: Adapters that leak vendor types
```
# WRONG -- the caller sees vendor exceptions/objects through the seam
def query(self, vector) -> QdrantPoint:
# CORRECT -- the adapter owns the translation; return domain types (list[int])
```

### Mistake 3: Undo without captured state
```
# WRONG -- undo cannot restore what execute destroyed
class DeleteCommand:
    def execute(self): del self._buf[self._offset]
    def undo(self): pass                 # broken undo
# CORRECT -- capture the deleted text at construction; undo restores it
```

### Mistake 4: Manual registries that drift
```
# WRONG -- two places to update: the class and the dict
class Search(Tool): ...
Tool.registry["search"] = Search          # easy to forget, easy to typo
# CORRECT -- __init_subclass__ registers automatically
```

### Mistake 5: Strategy branches inside the caller
```
# WRONG -- the caller knows every algorithm and branches
if chunker_name == "fixed": chunks = fixed(text)
elif chunker_name == "sentence": chunks = sentence(text)
# CORRECT -- pass a Chunker; the caller stays algorithm-agnostic
```

---

## Best Practices

1. **Define the seam as a `Protocol`** (from topic 23) — adapters and strategies implement the shape.
2. **Inject dependencies in constructors**; never import a vendor inside a component.
3. **Make fakes honest** — verify they satisfy the protocol before tests trust them.
4. **Capture undo state at construction time**, not at undo time.
5. **Let `__init_subclass__` maintain registries** — one source of truth.
6. **Keep vendor types behind the adapter**; the seam speaks domain types.
7. **Compose patterns** — an adapter can hold a strategy; DI can deliver the registry.
8. **Test through the seam** — write one test suite that runs against real and fake implementations.

---

## Complexity and Cost

| Pattern | Time | Space | Cost of the seam |
|---|---|---|---|
| Adapter | O(1) per call + vendor cost | O(1) | one extra call frame |
| DI | O(1) at construction | O(1) | dependencies become explicit |
| Command + undo stack | O(1) per execute/undo | O(history) | history grows with ops |
| Registry (`__init_subclass__`) | O(1) lookup by name | O(tools) | registration happens at import |
| Strategy | O(1) dispatch | O(1) | one protocol call |

Every pattern here is O(1) overhead on the happy path — the seams cost almost nothing and buy vendor swaps, honest tests, undo, and extensibility. The real cost is design time, which is exactly what the patterns monetize.

---

## AI Engineering Relevance

**Where this shows up:** the phase doc's canonical cases are all pattern-shaped: the undo/redo editing tool is the Command pattern; the vector store abstraction (Qdrant/Chroma/FAISS) is the Adapter; the `FakeLLMClient` in tests is DI; the LLM tool registry is the `__init_subclass__` Registry; chunking and reranking options are Strategies. Every AI framework you use is a pile of these seams — LangChain's model providers are adapters, its chain composition is strategy+composite, its tool ecosystem is a registry.

| Pattern here | Used for |
|---|---|
| Adapter | one `VectorStore` over Qdrant/Chroma/FAISS |
| DI | `Summarizer(FakeLLMClient())` in tests, real client in prod |
| Command | undo/redo editing, retryable operations |
| Registry | LLM tool discovery for function calling |
| Strategy | swappable chunking/reranking/eviction policies |

**Scale note:** seams pay off exactly when the number of implementations grows. Two vendors justify an adapter; ten make it mandatory. The registry matters when the tool list changes weekly. DI matters from the first test written. Build the seams early — retrofitting them later is the expensive path.

---

## Practice Exercises

### Exercise 1: Vendor Swap (Difficulty: Easy)
Add a `ChromaAdapter` to the `VectorStore` protocol and run the same `search_top` against Qdrant and Chroma adapters. Assert identical results for the same vectors.

### Exercise 2: Honest Fake (Difficulty: Medium)
Write `FakeLLMClient` and verify it satisfies the `LLMClient` protocol (structure + signature via `inspect`). Assert the fake's output starts with the documented prefix.

### Exercise 3: Undoable Editor (Difficulty: Medium)
Implement `InsertCommand` and `DeleteCommand` over a `list[str]` buffer with correct undo (capturing deleted text). Assert that execute+undo returns the buffer to its original content for both.

### Exercise 4: Registry Dispatch (Difficulty: Medium)
Create `Tool` with `__init_subclass__` registry, add `Calculator` and `Search`, and dispatch by name. Assert registry contents and a dispatched result.

### Exercise 5: Strategy Swap (Difficulty: Hard)
Build `FixedChunker` and `SentenceChunker` behind a `Chunker` protocol; index the same text with both; assert outputs differ and both are correct for their semantics.

### Exercise 6: Pattern Composition (Difficulty: Hard)
Compose three: a `VectorStore` adapter, a `Chunker` strategy, and DI — build an `Indexer` that takes both through its constructor. Swap implementations independently and assert behavior changes only at the seam you swapped.

---

## Summary

| Pattern | Seam it creates |
|---|---|
| Adapter | vendor out of the domain |
| DI | construction out of the component |
| Command | operation out of execution |
| Registry | discovery out of instantiation |
| Strategy | algorithm out of the caller |

Every pattern in this lecture is one honest seam. Seams are what make systems testable (fakes through DI), swappable (adapters), recoverable (commands with undo), extensible (registries), and configurable (strategies). The cost is measured in design time, and the payoff is measured in every future change that touches one class instead of fifty.

---

## Quick Reference

| Task | Idiom |
|---|---|
| One interface, many vendors | `Adapter` implementing a `Protocol` |
| Testable components | `def __init__(self, dep: Protocol)` — inject, never construct |
| Undoable operations | `Command` objects with `execute`/`undo`, capture state early |
| Self-maintaining tools | `__init_subclass__` appends to `cls.registry` |
| Swappable algorithms | `Strategy` protocol passed at call sites |
| Honest fakes | verify the fake satisfies the protocol + signature |

---

## Next Steps

Next: **[27-packaging-and-distribution-lecture.md](27-packaging-and-distribution-lecture.md)** — shipping the seams: pyproject.toml, semver, extras, entry points, and why lockfiles matter.
Continues in: **[34-architecture-patterns](../../../02-advanced-python/34-architecture-patterns.py)** (Phase 2 topic 34) — layering, ports & adapters at service scale, and event-driven composition.
Official docs: [abc/Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol), [object.__init_subclass__](https://docs.python.org/3/reference/datamodel.html#object.__init_subclass__), [Design Patterns (GoF)](https://en.wikipedia.org/wiki/Design_Patterns).
