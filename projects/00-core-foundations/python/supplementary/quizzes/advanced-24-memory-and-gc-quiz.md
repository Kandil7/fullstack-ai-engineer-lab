# Memory Management and GC Quiz

## Topic Overview
This quiz covers reference counting, cycles and the cyclic collector,
weak references and their traps, `__slots__` sizing (with the
`__dict__` gotcha on 3.13), and `tracemalloc`-based leak hunting.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer

---

## Questions

### Question 1
**When does CPython free an object with no cycles?**

A) When the garbage collector next runs
B) Immediately when its reference count reaches zero
C) When the process exits
D) When the object is older than one generation

**Difficulty:** Easy

---

### Question 2
**What can reference counting NOT reclaim?**

A) Large lists
B) Reference cycles
C) String internals
D) Cached integers

**Difficulty:** Easy

---

### Question 3
**What is the output of this code?**
```python
class Watch:
    alive = 0
    def __init__(self):
        type(self).alive += 1
    def __del__(self):
        type(self).alive -= 1

a = Watch()
b = a
del a
print(Watch.alive, end=" ")
del b
print(Watch.alive)
```

A) `1 0`
B) `0 0`
C) `2 0`
D) `1 1`

**Difficulty:** Easy

---

### Question 4
**Which is the primary use of `weakref.WeakValueDictionary`?**

A) A cache whose entries self-evict when their values die
B) A dict that stores only integers
C) A dict that survives garbage collection
D) A thread-safe dict

**Difficulty:** Easy

---

### Question 5
**What does `__slots__` replace in each instance?**

A) The `__class__` reference
B) The per-instance `__dict__` (and weakref slot)
C) The method table
D) The type's docstring

**Difficulty:** Easy

---

### Question 6
**Which tool names the file and line where memory was allocated?**

A) `sys.getsizeof`
B) `tracemalloc`
C) `gc.get_objects`
D) `memoryview`

**Difficulty:** Easy

---

### Question 7
**What is the output of this code?**
```python
import weakref

class Entry:
    pass

cache = weakref.WeakValueDictionary()
cache[1] = Entry()   # temporary
print(len(cache), end=" ")

e = Entry()
cache[2] = e
print(len(cache), end=" ")
del e
print(len(cache))
```

A) `0 1 0`
B) `1 1 0`
C) `0 0 0`
D) `1 2 1`

**Difficulty:** Medium

---

### Question 8
**Why does `sys.getsizeof(instance)` alone understate memory on Python 3.13?**

A) It returns 48 bytes for both plain and slotted classes
B) It measures the type, not the instance
C) It includes the garbage collector's overhead
D) It rounds to the nearest megabyte

**Difficulty:** Medium

---

### Question 9
**What is the output of this code?**
```python
import gc

class Node:
    pass

a, b = Node(), Node()
a.peer, b.peer = b, a
del a, b
print(gc.collect())
```

A) `0` — nothing is freed
B) `2` — the cycle is collected
C) `1` — one node survives
D) `NameError`

**Difficulty:** Medium

---

### Question 10
**A `WeakValueDictionary` entry holding a *temporary* value is evicted:**

A) When the collector runs — eventually
B) At the end of the statement that created the value
C) Never — weak dicts hold everything
D) When the dict exceeds 1000 entries

**Difficulty:** Medium

---

### Question 11
**What is the output of this code?**
```python
class Slotted:
    __slots__ = ("x",)
    def __init__(self, x):
        self.x = x

s = Slotted(1)
print(hasattr(s, "__dict__"), s.x)
```

A) `True 1`
B) `False 1`
C) `False 0`
D) `TypeError: no attribute x`

**Difficulty:** Medium

---

### Question 12
**Where does the memory saved by `__slots__` actually come from?**

A) Smaller type objects
B) The removed per-instance `__dict__` (~264 bytes each)
C) Shorter method names
D) Compressed attribute values

**Difficulty:** Medium

---

### Question 13
**What does `tracemalloc.get_traced_memory()` return?**

A) The current and peak traced bytes
B) The RSS of the process
C) The number of allocated objects
D) The size of the largest object

**Difficulty:** Medium

---

### Question 14
**Which pattern signals a memory leak in production?**

A) RSS grows monotonically across identical batches
B) RSS is constant across batches
C) RSS drops after `gc.collect()`
D) RSS matches the sum of `sys.getsizeof` values

**Difficulty:** Medium

---

### Question 15
**What is the output of this code?**
```python
import sys

class Plain:
    pass

p = Plain()
print(sys.getsizeof(p), hasattr(p, "__dict__"))
```

A) `48 True`
B) `48 False`
C) `312 False`
D) `312 True`

**Difficulty:** Hard

---

### Question 16
**Why should `gc.collect()` not be called on the hot path?**

A) It allocates a new heap
B) It walks all tracked objects — expensive, and usually unnecessary
C) It blocks the GIL forever
D) It is deprecated since 3.10

**Difficulty:** Hard

---

### Question 17
**Which design prevents a chat-history cache from growing unboundedly in an inference server?**

A) `WeakValueDictionary` keyed by sessions, or an LRU with a hard cap
B) A plain dict — it is fast enough
C) `WeakKeyDictionary` with string keys
D) A global list of histories

**Difficulty:** Hard

---

### Question 18
**What is the output of this code?**
```python
import tracemalloc

tracemalloc.start()
data = [b"x" * 1024 for _ in range(5_000)]
current, peak = tracemalloc.get_traced_memory()
print(round(current / 1024), round(peak / 1024))
```

A) `0 0` — lists are not traced
B) `~5124 ~5124` (KB)
C) `5 5`
D) `5124 0`

**Difficulty:** Hard

---

### Question 19
**A `WeakKeyDictionary` entry disappears when:**

A) The value is garbage-collected
B) The key is garbage-collected
C) The dict is resized
D) Either side is dereferenced once

**Difficulty:** Hard

---

### Question 20
**Which assertion makes a memory test honest rather than flaky?**

A) `assert elapsed < 0.001`
B) `assert peak_slotted < peak_plain` at 10,000 instances
C) `assert gc.collect() > 0` always
D) `assert sys.getsizeof(x) < 100` for every object

**Difficulty:** Hard

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! Memory is visible to you.
- 14-17: Good! Review the weak-reference questions.
- 10-13: Fair. Re-read the sizing and trapping sections.
- Below 10: Revisit the lecture and the exercise before continuing.

---

## Answer Key

1. **B) Immediately when its reference count reaches zero** —
   refcounting is eager and deterministic. A describes cycles, C is
   false, D confuses generations.

2. **B) Reference cycles** — the one gap refcounts cannot see. A, C,
   D are all reclaimable by refcounting.

3. **A) `1 0`** — `b` keeps the object alive after `del a`; the
   second `del` frees it. B misses the first print, C overcounts, D
   misses the final free.

4. **A) A cache whose entries self-evict when their values die** —
   the weak-value contract. B, C, D are false.

5. **B) The per-instance `__dict__` (and weakref slot)** — slots
   replace the namespace dict with descriptors. A and C are
   untouched, D is unrelated.

6. **B) `tracemalloc`** — it records allocation sites with file and
   line. A sizes one object, C lists objects, D is a buffer view.

7. **A) `0 1 0`** — the temporary is evicted instantly; the owned
   entry lives; deleting the owner evicts it. B and C miss the
   trap/owner steps, D never evicts.

8. **A) It returns 48 bytes for both plain and slotted classes** —
   the 3.13 measurement surprise; the `__dict__` must be added. B, C,
   D are false.

9. **B) `2` — the cycle is collected** — the cyclic collector frees
   exactly the two nodes. A ignores the cycle, C is false, D is
   false.

10. **B) At the end of the statement that created the value** — the
    temporary value trap. A is too late, C and D are false.

11. **B) `False 1`** — no `__dict__`; the slot works. A would mean
    slots are ignored, C loses the value, D is false.

12. **B) The removed per-instance `__dict__` (~264 bytes each)** —
    the dict is the cost; slots delete it. A, C, D are false.

13. **A) The current and peak traced bytes** — `(current, peak)`.
    B is OS-level, C is `gc.get_objects`, D is not a trace API.

14. **A) RSS grows monotonically across identical batches** — the
    leak signature. B is healthy, C is a one-time event, D is
    misleading (getsizeof understates).

15. **A) `48 True`** — on 3.13 a plain instance is 48 bytes and has
    a `__dict__`. B denies the dict, C and D are wrong sizes.

16. **B) It walks all tracked objects — expensive, and usually
    unnecessary** — the collector runs on its own schedule. A and C
    are false, D is false (it is current).

17. **A) `WeakValueDictionary` keyed by sessions, or an LRU with a
    hard cap** — the canonical case's two honest answers. B grows
    forever, C inverts key/value lifetimes, D is a leak by design.

18. **B) `~5124 ~5124` (KB)** — 5,000 × 1 KiB traced; peak equals
    current. A is false (lists and bytes are traced), C is the count,
    D reports a zero peak wrongly.

19. **B) The key is garbage-collected** — weak keys, strong values.
    A is the WeakValueDictionary behavior, C and D are false.

20. **B) `assert peak_slotted < peak_plain` at 10,000 instances** —
    a shape/ratio assertion that survives machine differences. A is
    wall-clock, C is not always true, D is an absolute bound.
