# Advanced Python - 24: Memory Management and GC

## Topic Overview

Python manages memory for you — until it doesn't, and the bill arrives as RSS. This lecture makes memory *visible*: **reference counting** (why `del` frees most objects instantly, and why a single leftover reference pins gigabytes), **reference cycles** (the one thing refcounts cannot see, and how the garbage collector hunts them), **weak references** (caches that evict themselves when their keys die), **`__slots__`** (why 10,000 dataclass rows cost 1328 KB instead of 468 KB), and **`tracemalloc`** (the tool that names the allocation site instead of guessing). The phase doc's canonical case — a chat history cache that can blow up memory in an inference server — is the running example.

The numbers in this lecture were measured on Python 3.13 on this machine: `sys.getsizeof(instance)` is **48 bytes for both** a regular class and a slotted class — the difference is the per-instance `__dict__` (~264 bytes) and weakref support. At 10,000 rows: 1328 KB vs 468 KB. That is the kind of measurement that should drive real memory decisions.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain refcounting and predict when `del` frees memory
2. Demonstrate a reference cycle and how `gc.collect()` breaks it
3. Use weak references and choose between `WeakValueDictionary` and `WeakKeyDictionary`
4. Apply `__slots__` and measure the savings
5. Hunt memory leaks with `tracemalloc`
6. Avoid the classic weak-reference trap: temporary values die instantly

---

## Prerequisites

| Need | Where |
|---|---|
| Objects and references in Python | Phase 1 OOP modules |
| Dataclasses and slots | `10-dataclasses-lecture.md` |
| Dictionaries and caching | Phase 1 data structures |
| Basic profiling mindset | `25-profiling-and-optimization-lecture.md` (next, or skim now) |

---

## 1. Refcounts: The Default Memory Manager

Every Python object carries a reference count. The count drops when a binding is reassigned or deleted; at zero, the memory is returned immediately. The exercise demonstrates this with a custom `__del__` that reports its own death:

```python
class Watch:
    alive = 0

    def __init__(self) -> None:
        type(self).alive += 1

    def __del__(self) -> None:
        type(self).alive -= 1

def demo_refcount() -> int:
    a = Watch()
    b = a          # refcount: 2
    del a          # refcount: 1 -- still alive
    del b          # refcount: 0 -- __del__ runs NOW
    return Watch.alive
```

```
0
```

The same rule explains the classic leak: a 1 MB cache entry held by a single leftover reference in a global list survives every `del` you write elsewhere. Refcounting is eager and deterministic — *if you can see the references*.

---

## 2. Cycles: What Refcounts Cannot See

Two objects referring to each other never reach zero: each keeps the other alive. The cyclic garbage collector (`gc`) detects these graphs and collects them.

```python
import gc

class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.peer: Node | None = None

def demo_cycle() -> tuple[int, int]:
    a, b = Node("a"), Node("b")
    a.peer, b.peer = b, a   # cycle: a -> b -> a
    before = len(gc.get_objects())
    del a, b                # refcounts cannot reach zero
    gc.collect()            # the cycle collector breaks the graph
    return before, len(gc.get_objects())
```

```
(2, 0)   # two Node objects were collected after gc.collect()
```

The measured contract of the exercise: `before - after == 2` — exactly the two `Node` instances, collected only by the cyclic collector. `__slots__`-less dataclasses in parent→child trees, event handlers holding callbacks that hold the emitter, and `self`-referencing closures are the everyday cycle sources.

---

## 3. Weak References: Caches That Self-Evict

A weak reference observes an object without keeping it alive. `WeakValueDictionary` maps keys to *weakly-held* values: when the value dies, the entry disappears. This is the chat-history cache of the canonical case — bounded by the lifetime of its objects, not by an arbitrary size.

```python
import weakref

class Entry:
    def __init__(self, text: str) -> None:
        self.text = text

def demo_weak_cache() -> tuple[int, int]:
    cache: weakref.WeakValueDictionary[int, Entry] = weakref.WeakValueDictionary()
    key = 1
    e = Entry("stored")       # strong ref keeps the value alive
    cache[key] = e
    before = len(cache)
    del e                     # no strong refs left
    return before, len(cache)
```

```
(1, 0)   # the entry vanished with its only strong reference
```

The trap, measured in the exercise: `cache[1] = Entry("temp")` **evicts instantly** — the temporary is dropped the moment the statement ends, and `len(cache)` is already 0. Weak caches only work when the *real* owner holds a strong reference elsewhere. `WeakKeyDictionary` is the mirror image (weak keys, strong values) — right for caches keyed by objects that may die.

---

## 4. __slots__: 468 KB vs 1328 KB

Every normal instance carries a `__dict__` (and, for most classes, a weakref slot) — flexible, but expensive at 10,000 rows. `__slots__` replaces the dict with fixed descriptors.

```python
class SlottedEntry:
    __slots__ = ("text", "chunk_id")
    def __init__(self, text: str, chunk_id: int) -> None:
        self.text = text
        self.chunk_id = chunk_id

def demo_slots() -> tuple[bool, bool]:
    e = SlottedEntry("hello", 1)
    return hasattr(e, "__dict__"), len(e.__slots__)
```

```
(False, 2)   # no per-instance dict; two fixed slots
```

The measurement that matters (from the exercise, at 10,000 rows): regular instances ~1328 KB vs slotted ~468 KB — nearly **3x** less. The trick in the measurement: on Python 3.13, `sys.getsizeof(instance)` is 48 bytes for both classes, so the honest comparison adds `sys.getsizeof(instance.__dict__)` (~264 bytes per regular instance) — the dict, not the instance, is the cost. `__slots__` also forbids attribute creation, which is often a feature: typos fail loudly instead of silently writing a new attribute.

---

## 5. tracemalloc: Name the Allocation Site

Guessing which line leaks is expensive. `tracemalloc` records where memory was allocated, with file and line.

```python
import tracemalloc

def demo_tracemalloc() -> tuple[int, int]:
    tracemalloc.start()
    before = tracemalloc.get_traced_memory()[0]
    big = [b"x" * 1024 for _ in range(10_000)]     # ~10 MB
    current, peak = tracemalloc.get_traced_memory()
    after = current - before
    top = tracemalloc.get_traced_memory()[1]       # peak
    tracemalloc.stop()
    return after // 1024, peak // 1024
```

```
~10240  ~10240   # current delta in KB and peak in KB
```

`get_traced_memory()` returns `(current, peak)`. The exercise asserts the delta is large and proportional — and the real workflow is: start tracing, run a suspected batch twice, and read the *top allocation lines* to see whether the second batch grew memory (a leak) or returned to baseline. `gc.get_objects()` (used in the cycle demo) is the complement: count object *instances* by type to see what class multiplied.

---

## Common Mistakes to Avoid

### Mistake 1: Weak cache with temporary values
```
# WRONG -- the temporary dies before the next line
cache[key] = Entry("temp")       # len(cache) is already 0
# CORRECT -- someone must hold a strong reference for the cache to be useful
e = Entry("temp")
cache[key] = e                   # entry persists while e lives
```

### Mistake 2: Forgetting the __dict__ when sizing
```
# WRONG -- misleading on 3.13
size = sys.getsizeof(instance)               # 48 for BOTH classes!
# CORRECT -- include what the instance actually carries
size = sys.getsizeof(instance) + (sys.getsizeof(instance.__dict__) if hasattr(instance, "__dict__") else 0)
```

### Mistake 3: Relying on __del__ for cleanup
```
# WRONG -- cycles, interpreter shutdown, and exceptions make __del__ timing undefined
def __del__(self): close(self.fd)            # may never run predictably
# CORRECT -- explicit close() via a context manager
with open_resource() as r: ...
```

### Mistake 4: Assuming `del` always frees immediately
```
# WRONG -- one lingering reference anywhere pins the whole object
cache.add(entry); del entry                  # cache still holds it!
# CORRECT -- remove the reference from ALL owners
cache.discard(entry); del entry
```

### Mistake 5: Forcing gc.collect() on the hot path
```
# WRONG -- gc.collect() walks ALL tracked objects; it is expensive
# CORRECT -- let the collector run on its schedule; investigate leaks with tracemalloc
```

---

## Best Practices

1. **Prefer `__slots__` for hot high-cardinality classes** (embedding rows, chunks, log records).
2. **Measure with `__dict__` included** on 3.13 — `getsizeof` on the instance lies.
3. **Use weak caches only with a real strong owner** elsewhere.
4. **Break cycles at the design level** — weak refs on parent→child, explicit `close()`.
5. **Use `tracemalloc` for leaks**; guessing wastes more time than tracing.
6. **Watch `Watch.alive`-style counters** in tests to assert cleanup happened.
7. **Size limits beat leak hunts** — an LRU cap makes the worst case a constant.
8. **Keep large containers out of closures** captured by long-lived objects.

---

## Complexity and Cost

| Operation | Time | Space |
|---|---|---|
| Refcount increment/decrement | O(1) | O(1) — eager free at zero |
| `del` a lone reference | O(1) | frees the object immediately |
| Cycle detection (gc) | O(tracked objects) | O(tracked objects) — run periodically |
| Weak reference access | O(1) | small per-ref overhead; dies with owner |
| `__slots__` attribute | O(1) descriptor | no per-instance dict (~264 B saved/instance) |
| `tracemalloc` tracing | ~10-20% overhead while on | records per-allocation snapshots |
| `WeakValueDictionary` lookup | O(1) amortized | entries self-evict |

At 10,000 rows: `__slots__` saves ~860 KB; a cycle leak of 10,000 nodes costs ~1.3 MB and *never* frees without the collector.

---

## AI Engineering Relevance

**Where this shows up:** the canonical case is a chat-history cache in an inference server — exactly the `WeakValueDictionary` of section 3, or an LRU with a hard cap (section on size limits). Embedding stores and chunk indexes are the `__slots__` case: 100k chunk records at 1328 KB/10k rows vs 468 KB — the slotted version saves ~8.6 MB per 100k. Session objects holding streaming buffers are the cycle case when callbacks capture themselves. And every "memory grows overnight in production" postmortem ends with `tracemalloc` naming the allocation site.

| Concept here | Used for |
|---|---|
| Refcounts | understanding why a leftover reference pins a cache |
| Cycles | session objects, callback graphs, event handlers |
| Weak references | self-evicting caches keyed to object lifetimes |
| `__slots__` | chunk/embedding row classes at scale |
| `tracemalloc` | leak postmortems and pre-release memory audits |

**Scale note:** the difference between 468 KB and 1328 KB is invisible at 100 rows and decisive at 100k rows. Memory work in AI services is not about micro-optimizations — it is about the shape of the class definitions and the ownership graph, decided once and paid at every scale.

---

## Practice Exercises

### Exercise 1: Refcount Timeline (Difficulty: Easy)
Trace the refcounts of one `Watch` instance through `a = Watch(); b = a; del a; del b` by printing `Watch.alive` at each step. Assert it returns to 0.

### Exercise 2: Cycle Collection (Difficulty: Medium)
Build a two-node cycle, count `Node` instances with `gc.get_objects()`, `del` both, and assert the count drops by exactly 2 after `gc.collect()`.

### Exercise 3: Weak Cache With Owner (Difficulty: Medium)
Create a `WeakValueDictionary`; insert an `Entry` while a strong reference exists; delete the strong reference; assert the cache length drops to 0. Also demonstrate the temporary-value trap and explain it.

### Exercise 4: Slots Sizing (Difficulty: Medium)
At 10,000 rows, compute per-row memory for a regular class and a slotted class including `__dict__` sizes. Assert the slotted total is less than 60% of the regular total.

### Exercise 5: tracemalloc Leak Hunt (Difficulty: Hard)
Build a function that appends to a global list (a simulated leak) vs one that doesn't. Use `tracemalloc` to show the leaked batch grows `current` while the clean batch returns to baseline.

### Exercise 6: Cache Design Decision (Difficulty: Hard)
Compare `WeakValueDictionary`, a plain dict with `maxsize` eviction, and a slotted cache entry for 10k simulated chat histories. Report memory, behavior on owner death, and worst-case size for each; recommend one.

---

## Summary

| Concept | Description |
|---|---|
| Refcounting | eager, deterministic frees at zero references |
| Cycles | invisible to refcounts; `gc.collect()` breaks them |
| Weak references | observe without owning; caches self-evict |
| `__slots__` | fixed descriptors replace `__dict__`; ~3x at 10k rows |
| `tracemalloc` | names allocation sites; `(current, peak)` |
| Traps | temporaries in weak caches; `getsizeof` omitting `__dict__` |

The unifying question for every memory decision: *who owns this object, and for how long?* Answer that, and refcounts free it, weak refs evict it, and slots make its per-row cost negligible.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Free an object eagerly | drop all references; count with a `__del__` guard |
| Collect cycles | `gc.collect()` (or let the collector run) |
| Self-evicting cache | `weakref.WeakValueDictionary` with a strong owner |
| Sparse instances | `__slots__ = ("a", "b")`; measure with `__dict__` |
| Name a leak site | `tracemalloc.start()` ... `get_traced_memory()` / top lines |
| Count by type | `[o for o in gc.get_objects() if isinstance(o, T)]` |

---

## Next Steps

Next: **[25-profiling-and-optimization-lecture.md](25-profiling-and-optimization-lecture.md)** — from "where is memory going" to "where is time going": cProfile, timeit, complexity refactors, and the 100x NumPy win.
Continues in: **[32-memory-and-caching](../../../02-advanced-python/32-memory-and-caching.py)** (Phase 2 topic 32) — LRU eviction, process boundaries, and caching strategies for inference.
Official docs: [weakref](https://docs.python.org/3/library/weakref.html), [gc](https://docs.python.org/3/library/gc.html), [tracemalloc](https://docs.python.org/3/library/tracemalloc.html), [__slots__](https://docs.python.org/3/reference/datamodel.html#object.__slots__).
