# 01-core-python — 43: Dataclasses & NamedTuples — Structured Records

## Topic Overview

A `@dataclass` is a class that carries data. In one decorator it generates
`__init__`, `__repr__`, `__eq__`, and optionally `__hash__`, `__lt__`, and more —
the boilerplate every data-carrying class used to hand-write. `NamedTuple` is
the lighter, immutable, tuple-based sibling. `TypedDict` describes plain dicts
for type checkers.

For AI and backend engineers this is the difference between passing a dozen
loose variables around and passing one typed record. A `RetrievedChunk(text,
score, source)` dataclass makes retrieval code readable and type-checkable;
`frozen=True` records become hashable so they can live in sets and dicts; and
`slots=True` (Python 3.10+) cuts memory sharply when you hold millions of them
in RAM — exactly the embedding-index scenario.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Create a dataclass with `@dataclass` and explain what it generates
2. Use `field(default_factory=...)` for mutable defaults
3. Build hashable, immutable records with `frozen=True`
4. Enable ordering with `order=True`
5. Save memory with `slots=True` (3.10+)
6. Validate values in `__post_init__`
7. Compare `dataclass` vs `NamedTuple` vs `TypedDict` vs plain dict and choose correctly
8. Use dataclasses for config objects and ML records

## Prerequisites

| Need | Where |
|------|-------|
| Classes and OOP | `34-classes.py` lecture |
| Tuples and unpacking | `14-tuples.py` lecture |
| Type hints | `02-advanced-python/05-type-hints-lecture.md` |

## 1. The Problem Dataclasses Solve

A data record used to require hand-written boilerplate:

```python
class Config:
    def __init__(self, lr, batch, seed=0):
        self.lr = lr
        self.batch = batch
        self.seed = seed

    def __repr__(self):
        return f"Config(lr={self.lr}, batch={self.batch}, seed={self.seed})"

    def __eq__(self, other):
        return (self.lr, self.batch, self.seed) == (other.lr, other.batch, other.seed)
```

Every field appears three times. Add ordering, hashing, or serialization and the
class becomes mostly plumbing. `@dataclass` generates all of it from the
annotations:

```python
from dataclasses import dataclass

@dataclass
class Config:
    lr: float
    batch: int
    seed: int = 0

c1 = Config(1e-3, 32)
c2 = Config(1e-3, 32)
print(c1)            # Config(lr=0.001, batch=32, seed=0)
print(c1 == c2)      # True — __eq__ compares fields
```

## 2. Mutable Defaults — `field(default_factory=...)`

The Python default-argument trap (a mutable default shared by all instances)
exists in dataclasses too — but the compiler refuses the naive form:

```python
from dataclasses import dataclass, field

@dataclass
class Batch:
    items: list[str] = field(default_factory=list)   # fresh list per instance
    scores: dict[str, float] = field(default_factory=dict)
```

`default_factory` runs the callable on every construction, so no state leaks
between instances. Use it for `list`, `dict`, `set`, and any mutable value.

## 3. `frozen=True` — Immutable and Hashable

Freezing makes assignment raise `FrozenInstanceError` and — as long as every
field is hashable — gives you a hashable object that can live in sets and dict
keys:

```python
@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    score: float
    source: str

chunk = RetrievedChunk("RAG stands for...", 0.92, "docs/rag.md")
try:
    chunk.score = 0.99
except Exception as e:
    print(type(e).__name__)   # FrozenInstanceError

chunks = {chunk, RetrievedChunk("x", 0.1, "y")}   # works — hashable
```

This is the natural shape for cache keys and deduplication.

## 4. `order=True` — Sorting Records

With `order=True` the dataclass implements the full comparison family
(`<`, `<=`, `>`, `>=`) by treating the fields as a tuple:

```python
@dataclass(order=True)
class Hit:
    score: float
    doc_id: str

hits = [Hit(0.5, "b"), Hit(0.9, "a"), Hit(0.5, "c")]
print(sorted(hits))  # sorts by score, then doc_id
```

Note the field order matters: comparison walks fields left to right.

## 5. `__post_init__` — Validation and Derived Values

Runs after `__init__`. The place for cross-field validation and normalization:

```python
@dataclass
class TrainingRun:
    lr: float
    epochs: int

    def __post_init__(self) -> None:
        if not 0 < self.lr <= 1:
            raise ValueError(f"lr must be in (0, 1], got {self.lr}")
        if self.epochs < 1:
            raise ValueError("epochs must be >= 1")
```

Fail fast at construction, not deep inside a training loop.

## 6. `slots=True` — Memory Efficiency (3.10+)

Normal instances carry a `__dict__`; `slots=True` replaces it with fixed
descriptors — smaller instances, faster attribute access, and no new attributes.
For a million records the win is real:

```python
@dataclass(slots=True)
class Embedding:
    id: str
    vector: list[float]
```

```text
With __dict__: ~48 bytes + ~296-byte dict per instance
With slots:    the dict disappears
```

## 7. NamedTuple — The Lightweight Immutable Record

`NamedTuple` subclasses `tuple`, so it is immutable, hashable, unpackable, and
has zero overhead beyond the tuple itself. Perfect for small, frequent records:

```python
from typing import NamedTuple

class Token(NamedTuple):
    text: str
    id: int
    pos: int

t = Token("the", 1, 0)
text, tid, pos = t          # tuple unpacking works
print(t.text, t[0])         # both attribute and index access
```

**When to choose which:** NamedTuple when the record is small, immutable, and
you want tuple semantics (unpacking, ordering, hashing). Dataclass when you need
mutation, defaults beyond simple values, validation, or inheritance.

## 8. TypedDict — Describing JSON-Style Dicts

`TypedDict` does not generate anything at runtime — it is a type-checker
contract for dicts that carry a fixed shape, exactly like JSON records:

```python
from typing import TypedDict, NotRequired

class LLMResponse(TypedDict):
    id: str
    choices: list[dict]
    usage: NotRequired[dict]
```

Mypy/Pyright will flag a missing `choices` key or a wrong value type. This is
the idiomatic way to type API payloads without paying for a class.

## 9. Production Pattern — Config as a Frozen Dataclass

```python
@dataclass(frozen=True)
class ModelConfig:
    model_name: str
    lr: float
    batch_size: int = 32
    warmup_steps: int = 0

    def __post_init__(self) -> None:
        if self.batch_size < 1:
            raise ValueError("batch_size must be positive")

cfg = ModelConfig("qwen2.5-7b", lr=3e-4)
# Frozen + typed + validated at construction — safe to pass anywhere.
```

## Common Mistakes to Avoid

### Mistake 1: Mutable default without default_factory

```python
# WRONG — compiler error, and correct: fields with defaults must come last
@dataclass
class A:
    items: list = []          # ValueError: mutable default
# CORRECT
@dataclass
class A:
    items: list = field(default_factory=list)
```

### Mistake 2: Forgetting `kw_only` when field order is confusing

```python
# WRONG — positional args invite silent mis-ordering
Config(32, 1e-3)             # batch=32, lr=1e-3? or reversed?
# CORRECT
@dataclass(kw_only=True)
class Config:
    batch: int
    lr: float
Config(batch=32, lr=1e-3)
```

### Mistake 3: Using `==` on dataclasses with floats

```python
# WRONG — exact float equality is fragile
chunk1 == chunk2
# CORRECT — compare with math.isclose on numeric fields, or round them
```

### Mistake 4: Making a large mutable dataclass frozen *without* thinking

```python
# WRONG — frozen + mutable field (list) is still mutable inside
@dataclass(frozen=True)
class B:
    items: list          # hash() will raise TypeError
# CORRECT — use tuple, or keep it non-frozen
```

## Best Practices

1. Use dataclasses for every structured record with more than two fields
2. Always `frozen=True` when the record must not change (configs, cache keys)
3. Always `slots=True` when you will hold many instances (3.10+)
4. Validate in `__post_init__`, never silently
5. Prefer `kw_only=True` for configs with many optional fields
6. Choose NamedTuple for small immutable tuple-like records
7. Use TypedDict for dicts that mirror JSON/API shapes
8. Keep dataclasses free of business logic; separate behavior into functions

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| `@dataclass` construction | O(1) fields written | same as hand-written `__init__` |
| `slots=True` instance | smaller + faster attribute access | no per-instance `__dict__` |
| `frozen=True` hashing | O(k) where k = field count | hash of the field tuple |
| `order=True` comparisons | O(k) worst case | field-tuple comparison |
| NamedTuple | O(1) + tuple overhead | cheapest record type |
| `==` on records | O(k) | field-by-field |

**At scale:** a million `slots=True` dataclass records vs plain classes is the
difference between ~100 MB and ~400 MB of instance overhead.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| `RetrievedChunk(text, score, source)` | every retrieval result in a RAG pipeline |
| `frozen=True` records | dedup keys for cached embeddings/prompts |
| `ModelConfig` dataclass | hyperparameters passed to training and eval |
| `slots=True` | a million-row in-memory embedding index |
| `NamedTuple` | token records, (idx, score) pairs, KV cache entries |
| `TypedDict` | typed LLM API responses and JSONL dataset rows |

**Scale note:** when your index grows to 10M rows, the dataclass layout (slots,
dtype choice, float32 vs float64) moves from a nicety to the difference between
fitting in RAM and spilling to disk.

## Practice Exercises

### Exercise 1: Minimal Record (Easy)
Create a `@dataclass` `Point(x: float, y: float)` with a `__post_init__` that
rejects non-finite values.

### Exercise 2: Hashable Cache Key (Medium)
Make a frozen dataclass `CacheKey(model: str, prompt: str, temperature: float)`
and verify instances can be used as dict keys and that two equal keys hash
equally.

### Exercise 3: Memory-Conscious Records (Hard)
Build `@dataclass(slots=True)` `Embedding(id: str, vector: tuple[float, ...])`,
create 100k instances, and measure `sys.getsizeof` of an instance plus total
memory via `tracemalloc`. Compare with the non-slots version.

## Summary

| Concept | Description |
|---------|-------------|
| `@dataclass` | generates `__init__`/`__repr__`/`__eq__` from annotations |
| `field(default_factory=...)` | correct way to default mutable values |
| `frozen=True` | immutable, hashable records |
| `order=True` | field-tuple comparison for sorting |
| `slots=True` | memory-efficient instances (3.10+) |
| `NamedTuple` | immutable tuple subclass, zero overhead |
| `TypedDict` | type-checked dict shape, no runtime cost |

Dataclasses turn ad-hoc dicts and tuple soup into typed, validated, and often
hashable records — the backbone of clean production data flow.

## Quick Reference

| Task | Idiom |
|------|-------|
| Simple record | `@dataclass class ...` |
| Mutable default | `field(default_factory=list)` |
| Immutable record | `@dataclass(frozen=True)` |
| Sortable record | `@dataclass(order=True)` |
| Low-memory record | `@dataclass(slots=True)` |
| Tiny immutable record | `NamedTuple` |
| Type a JSON dict | `TypedDict` |
| Validate on create | `__post_init__` |

## Next Steps

Next: **[44-logging](44-logging-lecture.md)** — the observability baseline.
Continues in: **[02-advanced-python — 06 dataclasses](../../02-advanced-python/lectures/06-dataclasses-lecture.md)** and
**[02-advanced-python — 05 type hints](../../02-advanced-python/lectures/05-type-hints-lecture.md)**.
Official docs: https://docs.python.org/3/library/dataclasses.html
