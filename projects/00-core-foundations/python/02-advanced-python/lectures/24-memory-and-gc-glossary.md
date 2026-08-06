# Memory Management and GC — Glossary 24

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `__del__` | Dunder | Finalizer hook; runs at refcount zero — unreliable, avoid for cleanup |
| `__dict__` | Attribute | Per-instance namespace dict; the main cost `__slots__` removes |
| `__slots__` | Class attribute | Declares fixed attributes, removing the per-instance dict |
| cycle | Concept | Two+ objects referencing each other; refcounts cannot free them |
| garbage collector | Component | Cyclic GC: finds and collects unreachable reference cycles |
| gc.collect() | API | Runs the cyclic collector immediately over all generations |
| generation | Concept | GC tiering: young (gen 0) objects collected far more often |
| memory leak | Bug | Memory kept alive by lingering references after it is no longer needed |
| reference count | Mechanism | Per-object counter; freed eagerly when it reaches zero |
| RSS | Metric | Resident Set Size: the process's actual RAM footprint |
| temporary value trap | Pattern | Weak caches drop temporaries instantly — the value dies at line end |
| tracemalloc | Module | Traces allocation sites; the leak-hunting tool |
| WeakKeyDictionary | Data structure | Weak keys, strong values; self-evicts when keys die |
| weak reference | Mechanism | Observes an object without keeping it alive |
| WeakValueDictionary | Data structure | Weak values, strong keys; self-evicts when values die |

## Detailed Definitions

### `__del__`
**Definition**: The finalizer called when an object's refcount hits zero. Timing is nondeterministic (cycles, exceptions, shutdown), so it must not be relied on for critical cleanup — explicit `close()` via a context manager is the production pattern. It is, however, a great *measurement* tool for exercises.
**Example**:
```python
class Watch:
    alive = 0
    def __init__(self) -> None:
        type(self).alive += 1
    def __del__(self) -> None:
        type(self).alive -= 1

a = Watch()
b = a
del a
print(Watch.alive, end=" ")   # still referenced by b
del b
print(Watch.alive)
```
```text
1 0
```
**Related**: reference count, memory leak

### `__dict__`
**Definition**: The per-instance namespace holding an instance's attributes — flexible (any attribute, any time) but expensive: ~264 bytes per instance on CPython. `sys.getsizeof(instance)` (48 bytes on 3.13) hides it, so honest sizing must add it.
**Example**:
```python
class Plain:
    def __init__(self, x: int) -> None:
        self.x = x

p = Plain(1)
print(p.__dict__, p.x)
```
```text
{'x': 1} 1
```
**Related**: `__slots__`, RSS

### `__slots__`
**Definition**: A class-level declaration of fixed attributes, replacing the per-instance `__dict__` with descriptors. Saves ~264 bytes per instance and blocks new attributes. At 10,000 rows, measured: 468 KB vs 1328 KB — nearly 3x.
**Example**:
```python
class Slotted:
    __slots__ = ("x",)

    def __init__(self, x: int) -> None:
        self.x = x

s = Slotted(1)
print(hasattr(s, "__dict__"), s.x)
```
```text
False 1
```
**Complexity**: O(1) attribute access, no dict lookup.
**Related**: `__dict__`, RSS, memory leak

### cycle
**Definition**: A graph of objects referencing each other (`a.peer = b; b.peer = a`). Every member's refcount stays ≥1, so eager frees never happen; only the cyclic garbage collector can reclaim the graph.
**Example**:
```python
import gc

class Node:
    pass

a, b = Node(), Node()
a.peer, b.peer = b, a
del a, b
print(gc.collect(), "objects collected")
```
```text
2 objects collected
```
**Related**: garbage collector, gc.collect(), reference count

### garbage collector
**Definition**: CPython's second memory manager, layered over refcounting: it finds unreachable cycles among tracked containers. It runs automatically on allocation thresholds; `gc.collect()` forces a full pass — expensive, so not for hot paths.
**Example**:
```python
import gc

print(len(gc.get_objects()) > 0, gc.isenabled())
```
```text
True True
```
**Related**: cycle, generation, gc.collect()

### gc.collect()
**Definition**: Forces the cyclic collector to sweep all generations immediately and returns the number of unreachable objects freed. The exercise's assertion tool: build a cycle, `del` the roots, collect, and check the count dropped by exactly the cycle size.
**Example**:
```python
import gc

class A:
    pass

x, y = A(), A()
x.other, y.other = y, x
del x, y
print(gc.collect())
```
```text
2
```
**Related**: cycle, generation, garbage collector

### generation
**Definition**: The collector's tiering: new tracked objects live in generation 0, promoted to 1, then 2 as they survive sweeps. Gen 0 is collected often (cheap), gen 2 rarely (expensive) — most objects die young, so most collection work is cheap.
**Example**:
```python
import gc

print(gc.get_count())          # (objects in gen0, gen1, gen2)
gc.collect()
print(gc.get_count())
```
```text
(5, 0, 0)
(0, 0, 0)
```
**Related**: garbage collector, gc.collect()

### memory leak
**Definition**: Memory retained long after it should be dead — typically a lingering reference (a cache, a closure, a global) or an unbroken cycle. Symptom: RSS grows monotonically across batches. Tool: `tracemalloc` names the allocation site.
**Example**:
```python
kept: list[bytes] = []

def batch(n: int) -> None:
    kept.append(b"x" * 1024 * 100)   # leaked: lives in the global

batch(1)
print(len(kept), "chunks retained")
```
```text
1 chunks retained
```
**Related**: RSS, tracemalloc, weak reference

### reference count
**Definition**: Every CPython object carries a counter of live references. Assignment increments it; rebinding and `del` decrement it. At zero the object is freed **eagerly** — deterministic and immediate, which is why plain `del` works when you can see all references.
**Example**:
```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x) - 1, end=" ")   # -1 for the call frame
y = x
print(sys.getrefcount(x) - 1)
```
```text
1 2
```
**Related**: cycle, `__del__`, memory leak

### RSS
**Definition**: Resident Set Size — the actual RAM pages a process holds, as reported by the OS (Task Manager / `resource`). The metric that matters in production ("memory grew overnight"). Profiling memory means watching RSS, not `sys.getsizeof` of individual objects.
**Example**:
```python
import tracemalloc

tracemalloc.start()
data = [i for i in range(100_000)]
current, peak = tracemalloc.get_traced_memory()
print(round(current / 1024), "KB current", round(peak / 1024), "KB peak")
```
```text
~3572 KB current ~3572 KB peak
```
**Related**: memory leak, tracemalloc, `__slots__`

### temporary value trap
**Definition**: The weak-cache failure mode: `cache[key] = Entry(...)` with a temporary value — the value's last strong reference dies at the end of the statement, so the entry is evicted immediately and `len(cache)` is 0. Weak caches require an external strong owner.
**Example**:
```python
import weakref

class Entry:
    pass

cache: weakref.WeakValueDictionary[int, Entry] = weakref.WeakValueDictionary()
cache[1] = Entry()          # temporary: dies instantly
print(len(cache))

e = Entry()                 # strong owner
cache[2] = e
print(len(cache))
del e
print(len(cache))
```
```text
0
1
0
```
**Related**: weak reference, WeakValueDictionary

### tracemalloc
**Definition**: The standard-library allocation tracer: `tracemalloc.start()`, then `get_traced_memory()` returns `(current, peak)` and `get_traced_memory()`/top-statistics name the file and line of every allocation. The leak hunter's first tool — replace guessing with data.
**Example**:
```python
import tracemalloc

tracemalloc.start()
big = [b"y" * 1024 for _ in range(5_000)]     # ~5 MB
current, _ = tracemalloc.get_traced_memory()
print(round(current / 1024), "KB traced")
```
```text
~5124 KB traced
```
**Related**: memory leak, RSS

### WeakKeyDictionary
**Definition**: `weakref.WeakKeyDictionary` — keys held weakly, values strongly. The entry disappears when the *key* dies. Correct for caches keyed by objects whose lifetime you do not control (e.g., per-session state keyed by session objects).
**Example**:
```python
import weakref

class Key:
    pass

k = Key()
d: weakref.WeakKeyDictionary[Key, str] = weakref.WeakKeyDictionary()
d[k] = "state"
print(len(d))
del k
print(len(d))
```
```text
1
0
```
**Related**: WeakValueDictionary, weak reference

### weak reference
**Definition**: A reference that observes an object without incrementing its refcount. `weakref.ref(obj)` / the weak dicts let you build caches and observers that never keep their subjects alive — the subject's death evicts the entry automatically.
**Example**:
```python
import weakref

class Entry:
    pass

e = Entry()
ref = weakref.ref(e)
print(ref() is e)
del e
print(ref() is None)          # the reference is now dead
```
```text
True
True
```
**Related**: WeakValueDictionary, WeakKeyDictionary, temporary value trap

### WeakValueDictionary
**Definition**: `weakref.WeakValueDictionary` — values held weakly, keys strongly. When a value's last strong reference dies, the entry vanishes. The canonical case: a chat-history cache whose entries live only while the sessions using them live.
**Example**:
```python
import weakref

class Entry:
    def __init__(self, text: str) -> None:
        self.text = text

cache: weakref.WeakValueDictionary[int, Entry] = weakref.WeakValueDictionary()
e = Entry("history")
cache[7] = e
print(len(cache), cache[7].text)
del e
print(len(cache))
```
```text
1 history
0
```
**Related**: WeakKeyDictionary, weak reference, temporary value trap

## Key Concepts Summary

### Two Managers, Two Jobs
- Refcounting frees eagerly and deterministically — when it can see the references.
- The cyclic GC handles what refcounts cannot: reference cycles.
- `gc.collect()` forces a sweep; generations make automatic runs cheap.

### Sizing Is Not What It Seems
- `sys.getsizeof(instance)` is 48 bytes for both plain and slotted classes on 3.13.
- The real cost is the per-instance `__dict__` (~264 bytes) — include it.
- `__slots__` trades flexibility for ~3x less memory at scale.

### Weak References Need Owners
- Weak caches self-evict when the real owner dies — they do not own anything.
- Temporaries evict instantly: keep a strong reference.
- Choose by which side must die: `WeakValueDictionary` (values) or `WeakKeyDictionary` (keys).

## Practice Terms

Match each term to its definition (answers at the bottom).

1. reference count — ___
2. cycle — ___
3. `__slots__` — ___
4. tracemalloc — ___
5. WeakValueDictionary — ___
6. temporary value trap — ___
7. generation — ___
8. RSS — ___
9. `__del__` — ___
10. memory leak — ___

A. Counter that frees the object eagerly at zero
B. Mutual references refcounts cannot reclaim
C. Fixed attributes replacing the per-instance dict
D. Traces allocation sites for leak hunting
E. Weak values that self-evict when the value dies
F. Instant eviction of cache entries holding temporaries
G. GC tiering: young objects collected most often
H. The process's actual RAM footprint
I. Finalizer hook with nondeterministic timing
J. Memory retained by lingering references after use

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H, 9-I, 10-J
