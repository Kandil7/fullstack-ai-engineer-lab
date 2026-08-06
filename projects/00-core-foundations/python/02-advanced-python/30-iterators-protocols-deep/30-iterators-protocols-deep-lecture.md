# Advanced Python — 30: Iterators and Protocols Deep

## Topic Overview

Python's "dunder" methods — `__len__`, `__getitem__`, `__iter__`,
`__hash__`, and friends — are the language's protocol layer. When you
write `len(x)`, `x[i]`, `item in x`, `with x:`, or `for i in x:`, Python
does not inspect the class; it *calls a method by name*. That is the
whole architecture: built-in syntax is dispatched to methods you can
implement, which is why `len()` works on lists, strings, numpy arrays,
and your custom `Dataset` alike.

This lecture goes deep on the protocols that matter for AI and backend
engineering: the iterator protocol (`__iter__`/`__next__`), the sequence
protocol (`__getitem__` and its `IndexError` fallback), the container
protocols (`__contains__`, `__reversed__`, `__len__`), the context
manager protocol (`__enter__`/`__exit__`), the callable protocol
(`__call__`), the ordering protocol (`__lt__` + `total_ordering`), the
hash/equality contract (`__hash__`/`__eq__`) — and the two attribute
access hooks (`__getattr__` vs `__getattribute__`). The `collections.abc`
hierarchy is the map: implement the minimal core, inherit the full
interface.

The most important idea is the **hash/eq contract**: if `a == b`, then
`hash(a) == hash(b)`, and a hash must never change while the object is
inside a dict or set. Breaking it does not crash — it *silently
corrupts* lookups. That silent corruption is exactly the bug class that
costs ML engineers days of debugging.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Implement `__iter__`/`__next__` and explain `StopIteration`
2. Explain and use the `__getitem__` fallback iteration protocol
3. Build a custom `Sequence` and get `len`/`in`/slicing/`reversed` free
4. Implement `__contains__`, `__reversed__`, `__call__`, `__enter__`/`__exit__`
5. State and obey the `__hash__`/`__eq__` contract, and demonstrate the corruption it prevents
6. Use `@functools.total_ordering` to derive comparison operators
7. Choose between `__getattr__` and `__getattribute__` correctly
8. Subclass `collections.abc.Mapping` and `Sequence` to inherit full interfaces
9. Recognize the PyTorch `Dataset` protocol (`__len__` + `__getitem__`)

## Prerequisites

| Need | Where |
|---|---|
| Iterators and generators | `02-generators-lecture.md` |
| Dataclasses (frozen, eq) | `06-dataclasses-lecture.md` |
| `functools.total_ordering` | `09-functools-lecture.md` |
| `collections.abc` overview | `11-collections-lecture.md` |
| Class basics and `super()` | `01-core-python` OOP modules |

---

## 1. The Iterator Protocol: __iter__ and __next__

An object is **iterable** if `iter(x)` returns an iterator. An object is
an **iterator** if it has `__next__` that raises `StopIteration` when
exhausted. Every `for` loop is desugared into exactly this dance.

```python
class Countdown:
    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

print(list(Countdown(3)))
```

Output:

```text
[3, 2, 1, 0]
```

The desugaring of `for x in obj:` is:

```python
it = iter(obj)            # obj.__iter__()
while True:
    try:
        x = next(it)      # it.__next__()
    except StopIteration:
        break
```

One object can be both iterable and iterator (as above) — but then a
single `for` loop consumes it. If you want *reusable* iteration, return
a fresh iterator from `__iter__` each time (that is what lists do).

---

## 2. The __getitem__ Fallback

Before `__iter__` existed, any object with `__getitem__` was iterable:
Python calls `obj[0]`, `obj[1]`, ... until `IndexError`. The fallback is
still alive and is the cheapest way to make a container iterable.

```python
class SliceByIndex:
    def __init__(self, items):
        self.items = items

    def __getitem__(self, index: int) -> int:
        return self.items[index]

print(list(SliceByIndex([10, 20, 30])))
```

Output:

```text
[10, 20, 30]
```

The subtle point: `__getitem__` raising `IndexError` is what *ends*
iteration. If your container silently returns garbage for out-of-range
indexes, iteration never terminates — an infinite loop with no
traceback.

---

## 3. Custom Sequence via collections.abc

The `Sequence` ABC has one job: from `__len__` + `__getitem__`, supply
`__contains__`, `__iter__`, `__reversed__`, `index`, and `count`. This
is the exact pattern behind PyTorch `Dataset`: implement
`__len__` and `__getitem__`, get the full data-loading contract.

```python
from collections.abc import Sequence

class EmbeddingDataset(Sequence):
    def __init__(self, ids, vectors):
        self._ids = ids
        self._vectors = vectors

    def __len__(self) -> int:
        return len(self._ids)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return list(zip(self._ids[index], self._vectors[index]))
        return (self._ids[index], self._vectors[index])

ds = EmbeddingDataset([0, 1, 2], [(1.0,), (2.0,), (3.0,)])
print(len(ds), ds[1], (2, (3.0,)) in ds, ds[1:3], list(reversed(ds)))
```

Output:

```text
3 (1, (2.0,)) True [(1, (2.0,)), (2, (3.0,))] [(2, (3.0,)), (1, (2.0,)), (0, (1.0,))]
```

Slice support: `ds[1:3]` passes a `slice` object to `__getitem__` — your
implementation must handle it explicitly, as above. The ABC's
`__iter__` is `iter(self[i] for i in range(len(self)))` — correct, if
not fast; override it for performance when needed.

---

## 4. __contains__, __reversed__, __call__

`in` dispatches to `__contains__`; `reversed(x)` dispatches to
`__reversed__` (falling back to `__getitem__` + `__len__`); and
`__call__` makes instances callable — the mechanism behind class-based
decorators.

```python
class Membership:
    def __init__(self, values):
        self.values = [v.lower() for v in values]

    def __contains__(self, item: object) -> bool:
        return isinstance(item, str) and item.lower() in self.values

    def __call__(self, prefix: str) -> list[str]:
        return [v for v in self.values if v.startswith(prefix.lower())]

m = Membership(["Alpha", "Beta"])
print("ALPHA" in m)
print(m("b"))
```

Output:

```text
True
['beta']
```

`__call__` is how `@decorator` classes work: `Timer(fn)` stores the
function, and every `timer(...)` call routes through `__call__`. It is
also the cleanest way to build a *callable configuration object*.

---

## 5. __enter__ / __exit__: The Context Manager Protocol

`with x as y:` calls `x.__enter__()`, runs the block, then guarantees
`x.__exit__(exc_type, exc, tb)` — even on exceptions. `__exit__`
returning `True` swallows the exception; returning `False` (the sane
default) propagates it.

```python
class ManagedVector:
    def __init__(self, name):
        self.name = name
        self.open = False

    def __enter__(self):
        self.open = True
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.open = False
        return False   # never swallow errors

with ManagedVector("emb") as store:
    print("inside:", store.open)
print("after:", store.open)
```

Output:

```text
inside: True
after: False
```

The guarantee that matters: `__exit__` runs even if the block raises, so
sessions, files, and locks are always released. This is the protocol
behind `torch.no_grad()`, DB sessions, and every `with` you have used.

---

## 6. The __hash__ / __eq__ Contract

The contract has two clauses:

1. **If `a == b`, then `hash(a) == hash(b)`** — equal objects must hash equally.
2. **A hash must never change while the object is in a dict/set** — hash on immutable state only.

Breaking clause 2: a mutable `__hash__` lets an object change its hash
*between* insertion and lookup. The dict does not crash — it silently
cannot find the entry, and a duplicate sneaks in. Both are corruption.

```python
class MutableKey:
    """DELIBERATELY BROKEN: hash follows a mutable field."""
    def __init__(self, value):
        self.value = value

    def __hash__(self):
        return hash(self.value)      # changes when value changes!

    def __eq__(self, other):
        return isinstance(other, MutableKey) and self.value == other.value

key = MutableKey("a")
table = {key: 1}
key.value = "b"
fresh = MutableKey("b")
print(fresh == key)                  # equal...
print(fresh in table)                # ...yet not found!
print(len(table))                    # entry still there, orphaned
```

Output:

```text
True
False
1
```

The entry is still in the table — hashed under `hash("a")` — but any
lookup with a correct, equal key probes `hash("b")` and misses. The
dict is corrupted: one orphaned entry and one lost value. (The same
object can even still be found via CPython's identity fast-path, which
makes the bug *harder* to see, not better.)

The fix: hash on immutable fields only, or use `@dataclass(frozen=True)`
which generates a correct `__hash__` from the fields and refuses
mutation.

---

## 7. Ordering: __lt__ + total_ordering

Python only needs `__eq__` plus one rich comparison; the
`@functools.total_ordering` decorator derives `<=`, `>`, `>=` from them.
Sorting itself only requires `__lt__`.

```python
import functools

@functools.total_ordering
class Score:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Score) and self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

a, b = Score(1.0), Score(2.0)
print(a < b, a <= b, b > a, a >= a)
```

Output:

```text
True True True True
```

One trap: defining `__eq__` alone sets `__hash__` to `None` (the class
becomes unhashable) unless you define `__hash__` explicitly. If you add
`__eq__` for sorting, add a hash too — or your objects stop working as
dict keys and set members.

---

## 8. __getattr__ vs __getattribute__

`__getattr__` runs **only when normal lookup fails** — perfect for
defaults. `__getattribute__` runs **on every attribute access** —
dangerous and rarely needed.

```python
class LazyConfig:
    def __init__(self, known):
        self.known = known

    def __getattr__(self, name: str) -> int:
        return self.known.get(name, 0)   # default for missing keys

cfg = LazyConfig({"batch": 32})
print(cfg.batch, cfg.lr)
```

Output:

```text
32 0
```

Rules of thumb: use `__getattr__` for fallbacks; use `property` for
computed attributes; override `__getattribute__` only when you must
intercept *every* access — and then always delegate via
`object.__getattribute__(self, name)`, or you recurse forever.

---

## 9. Mapping via collections.abc

`Mapping` needs `__getitem__`, `__len__`, `__iter__`; the ABC then
supplies `get`, `keys`, `values`, `items`, `__contains__`, `__eq__`.
The same bargain as `Sequence`: three dunders, full interface.

```python
from collections.abc import Mapping

class CaseInsensitiveMap(Mapping):
    def __init__(self, data):
        self._data = {k.lower(): v for k, v in data.items()}

    def __getitem__(self, key):
        return self._data[key.lower()]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

cm = CaseInsensitiveMap({"Rate": 10})
print(cm.get("rate"), dict(cm.items()))
```

Output:

```text
10 {'rate': 10}
```

The ABC also gives you `isinstance(x, Mapping)` checks, which make your
containers interchangeable with dicts in generic code — a retriever
returning a custom mapping works anywhere a dict was expected.

---

## 10. Production Pattern: A Dataset That Just Works

The pattern to ship: `__len__` + `__getitem__` (the PyTorch `Dataset`
protocol) plus `Sequence` registration for free slicing/membership, and
frozen data objects so items are safe to share.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class RetrievedChunk:
    doc_id: int
    text: str
    score: float

class ChunkDataset(Sequence):
    def __init__(self, chunks):
        self._chunks = list(chunks)

    def __len__(self):
        return len(self._chunks)

    def __getitem__(self, index):
        return self._chunks[index]
```

Every DataLoader, every `len(ds)` in a training loop, every
`ds[i]` batch index, every `chunk in ds` sanity check — all dispatch to
the two methods you wrote. That is the protocol layer earning its keep.

---

## Common Mistakes to Avoid

### Mistake 1: Mutable hash (the corruption bug)
```python
# WRONG — hash changes while the object sits in a dict
def __hash__(self):
    return hash(self.value)   # value mutates later

# CORRECT — frozen dataclass, or hash on immutable fields
@dataclass(frozen=True)
class Key:
    value: str
```

### Mistake 2: __eq__ without __hash__
```python
# WRONG — defining __eq__ sets __hash__ to None; keys/sets break
class Key:
    def __eq__(self, other): ...

# CORRECT — define both
def __hash__(self): return hash(self.value)
```

### Mistake 3: Infinite recursion in __getattribute__
```python
# WRONG — self.value re-enters __getattribute__
def __getattribute__(self, name):
    return self.value

# CORRECT — always delegate to the base
def __getattribute__(self, name):
    return object.__getattribute__(self, name)
```

### Mistake 4: __getitem__ that never raises IndexError
```python
# WRONG — iteration never terminates
def __getitem__(self, i):
    return self.items[i % len(self.items)]

# CORRECT — raise IndexError past the end
def __getitem__(self, i):
    return self.items[i]
```

### Mistake 5: Ignoring slices in __getitem__
```python
# WRONG — ds[1:3] crashes because slice is not an int
def __getitem__(self, i): return self._ids[i]

# CORRECT — handle slice explicitly
def __getitem__(self, i):
    if isinstance(i, slice):
        return self._ids[i]
    return self._ids[i]
```

### Mistake 6: __enter__ returning a different object
```python
# WRONG — `with x as y:` binds the RETURN value
def __enter__(self):
    return self.open_state   # y is now a bool

# CORRECT — return self (or a purpose-built handle)
def __enter__(self):
    return self
```

## Best Practices

1. **Register with `collections.abc`** — Sequence/Mapping/Set give you the interface for free
2. **Hash on immutable state only** — frozen dataclasses make this automatic
3. **Define `__hash__` whenever you define `__eq__`** — unless you want unhashable
4. **Return `False` from `__exit__`** — swallow exceptions only when you mean it
5. **Handle slices in `__getitem__`** — they arrive as `slice` objects
6. **Raise `IndexError` to end fallback iteration** — never wrap around
7. **`__getattr__` for defaults; `property` for computed; `__getattribute__` almost never**
8. **Keep `__hash__` O(1)** — if hashing is expensive, precompute at construction
9. **Document which protocols your class implements** — a docstring listing dunders beats discovery
10. **Test the contracts, not the dunders** — `len()`, `in`, `reversed()`, dict-key behavior

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| `__next__` | O(1) | O(1) | — |
| `__getitem__` fallback iteration | O(1)/item | O(1) | — |
| ABC `Sequence.__iter__` | O(n) | O(1) | override with a generator |
| `in` without `__contains__` (Sequence) | O(n) | O(1) | `__contains__` with a set — O(1) |
| `__hash__` on frozen dataclass | O(fields) | O(1) | precompute at construction |
| `reversed()` fallback | O(n) | O(1) | `__reversed__` if order differs |
| `total_ordering` derived ops | O(1) | O(1) | — |
| `__getattribute__` | O(1) | O(1) | skip it; use `__getattr__` |

The cost traps: ABC `__iter__` is a Python loop (fine at 10^4, slow at
10^8); `in` on a Sequence is a linear scan (use `__contains__` with a
set for hot membership); `__hash__` runs on every dict insert — keep it
cheap or precompute.

## AI Engineering Relevance

**Where this shows up:** the PyTorch `Dataset` protocol is the reference
case — `__len__` + `__getitem__` is all a `DataLoader` needs. Custom
containers for batched inference, immutable `RetrievedChunk` objects
shared across rerankers, and case-insensitive/config mappings are the
daily bread.

| Concept here | Used for |
|---|---|
| `__len__` + `__getitem__` | PyTorch `Dataset` protocol for training loops |
| `Sequence` ABC | chunk lists with `in`/slicing/reversed for debugging |
| frozen dataclass keys | embedding caches keyed by immutable `TextChunk` |
| `__hash__`/`__eq__` contract | dict-keyed caches that must not corrupt |
| `__enter__`/`__exit__` | model-inference sessions, `torch.no_grad()` |
| `Mapping` ABC | config objects, prompt-template registries |
| `__call__` | callable rerankers and scorers as configuration objects |

**Scale note:** at 10^6 cached embeddings, one mutable-hash bug silently
loses 30% of cache hits — no crash, no warning, just slower runs and
duplicate compute. The contract is not academic; it is a cost model.
And a `Dataset` whose `__getitem__` does I/O per index will make a
DataLoader crawl — the protocol puts the performance pressure exactly
where you can see it.

## Practice Exercises

### Exercise 1: Reusable iterator (Difficulty: Easy)
Implement `Squares(n)` whose `__iter__` returns a *fresh* iterator each
time, so `list(Squares(3))` twice gives `[0, 1, 4]` twice.

### Exercise 2: Fallback iteration (Difficulty: Easy)
Implement `Lines` with only `__getitem__` that yields the first `n`
lines of a string split — verify `list()` works without `__iter__`.

### Exercise 3: total_ordering Score (Difficulty: Medium)
Implement `Score` with `__eq__` and `__lt__` plus `total_ordering`; sort
a list of scores and verify all four comparisons.

### Exercise 4: Contract-correct key (Difficulty: Medium)
Implement `CacheKey` whose hash is computed once from immutable fields;
prove equal keys are found in a dict even after the source data object
mutates.

### Exercise 5: Dataset + Sequence (Difficulty: Hard)
Implement `ChunkDataset(Sequence)` for a list of frozen `RetrievedChunk`
objects; verify `len`, `in`, slicing, `reversed`, and DataLoader-style
indexing all work, and that items are immutable.

## Summary

| Concept | Description |
|---|---|
| Iterator protocol | `__iter__` + `__next__` + `StopIteration` |
| `__getitem__` fallback | iteration via indexing until `IndexError` |
| `Sequence` ABC | `__len__` + `__getitem__` unlock the full interface |
| `__contains__`/`__reversed__`/`__call__` | `in`, `reversed()`, callable instances |
| `__enter__`/`__exit__` | `with` lifecycle; return False to propagate errors |
| hash/eq contract | `a == b` ⇒ `hash(a) == hash(b)`; hash never changes |
| `total_ordering` | one rich comparison derives the rest |
| `__getattr__` vs `__getattribute__` | fallback vs total interception |
| `Mapping` ABC | three dunders unlock `get`/`keys`/`values`/`items` |

The protocol layer is what makes Python containers compose: write the
two or three methods your domain needs, and every built-in behaves
correctly with your objects. The hash/eq contract is the one place
where correctness is *silent* — respect it, or your caches and dicts
will lie to you.

## Quick Reference

| Task | Idiom |
|---|---|
| Iterable container | `__iter__` returning a fresh iterator |
| Iterator | `__next__` raising `StopIteration` at the end |
| Full list-like API | `class X(Sequence)` + `__len__` + `__getitem__` |
| Custom membership | `def __contains__(self, item): ...` |
| Callable instance | `def __call__(self, *args): ...` |
| Context manager | `__enter__` / `__exit__(self, exc_type, exc, tb)` |
| Orderable class | `@total_ordering` + `__eq__` + `__lt__` |
| Safe dict key | frozen dataclass (or hash on immutable fields) |
| Attribute defaults | `__getattr__`; never `__getattribute__` for this |
| Full dict-like API | `class X(Mapping)` + `__getitem__` + `__len__` + `__iter__` |

## Next Steps

Next: **[31 — Concurrency Patterns](31-concurrency-patterns-lecture.md)** —
producer-consumer, worker pools, rate limiting, and circuit breakers;
the protocols from this topic (`__enter__`/`__exit__`) show up as lock
and session management in every pattern.

Continues in: **[Phase 3 — numpy/pandas containers](../../03-libraries/README.md)** —
vectorized containers implement the same protocols at C speed.

Official docs:
- [Data model — dunder methods](https://docs.python.org/3/reference/datamodel.html)
- [collections.abc — abstract base classes](https://docs.python.org/3/library/collections.abc.html)
- [functools.total_ordering](https://docs.python.org/3/library/functools.html#functools.total_ordering)
- [PyTorch Dataset & DataLoader](https://pytorch.org/docs/stable/data.html)
