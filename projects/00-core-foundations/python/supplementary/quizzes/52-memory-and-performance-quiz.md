# Quiz 52: Memory & Performance

**Instructions:** Choose the single best answer. Answers and explanations
are at the end.

## Questions

### Q1. What does `sys.getsizeof(x)` measure?
**Difficulty:** Easy

- (A) The object plus everything it references
- (B) Only the object itself — a shallow size
- (C) The peak memory of the process
- (D) The number of bytes on disk

### Q2. What is the output?
**Difficulty:** Easy

```python
import sys
print(sys.getsizeof({}))
```

- (A) `0`
- (B) `64`
- (C) `sys.getsizeof` raises for empty containers
- (D) It depends on the process memory

### Q3. What does `__slots__` remove from each instance?
**Difficulty:** Easy

- (A) The ability to be garbage-collected
- (B) The per-instance `__dict__`
- (C) The class's `__init__`
- (D) The `__weakref__` only

### Q4. What is the output?
**Difficulty:** Medium

```python
a, b = 200, 200
print(a is b)
big_a = 2**40
big_b = int(str(2**40))
print(big_a is big_b)
```

- (A) `True` then `True`
- (B) `True` then `False`
- (C) `False` then `False`
- (D) `True` then `TypeError`

### Q5. Which is the correct identity idiom?
**Difficulty:** Easy

- (A) `if x is 1000:`
- (B) `if x is None:`
- (C) `if x == None:`
- (D) `if x is 0.0:`

### Q6. What is the complexity of building a string with `s += c` in a loop?
**Difficulty:** Medium

- (A) O(n)
- (B) O(n²)
- (C) O(log n)
- (D) O(1) amortized

### Q7. What is the output?
**Difficulty:** Medium

```python
s1 = "model_checkpoint"
s2 = "model_" + "checkpoint"
print(s1 == s2, s1 is s2)
```

- (A) `True True`
- (B) `True False`
- (C) `False False`
- (D) `False True`

### Q8. Which code streams a file with O(1) memory?
**Difficulty:** Medium

- (A) `lines = open(f).read().splitlines()`
- (B) `lines = list(open(f))`
- (C) `total = sum(len(l) for l in open(f))`
- (D) `data = open(f).read()`

### Q9. What is the output?
**Difficulty:** Medium

```python
import tracemalloc
tracemalloc.start()
big = [0] * 1_000_000
_, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(peak > sys.getsizeof(big))
```

*(Assume `sys` is imported.)*

- (A) `True`
- (B) `False`
- (C) `TypeError`
- (D) `peak` equals `sys.getsizeof(big)` exactly

### Q10. What is `memoryview(payload)[:9].tobytes()`?
**Difficulty:** Medium

- (A) A copy of the first 9 bytes
- (B) A zero-copy view of 9 bytes
- (C) The whole payload
- (D) An error — memoryview cannot slice bytes

### Q11. Why don't threads speed up CPU-bound Python?
**Difficulty:** Medium

- (A) Threads have higher startup cost than processes
- (B) The GIL allows only one thread to run Python bytecode at a time
- (C) The OS schedules all threads on one core
- (D) Python threads do not exist on Windows

### Q12. What is the output?
**Difficulty:** Hard

```python
import gc

class Node:
    __slots__ = ("next",)

n1, n2 = Node(), Node()
n1.next, n2.next = n2, n1
del n1, n2
print(gc.collect())
```

- (A) `0`
- (B) `2`
- (C) `NodeError`
- (D) `-1`

### Q13. Which tool finds hot spots in a real run?
**Difficulty:** Medium

- (A) `timeit`
- (B) `cProfile`
- (C) `sys.getsizeof`
- (D) `time.sleep`

### Q14. What is the output?
**Difficulty:** Easy

```python
def embedding_ram_bytes(rows, dim, dtype_bits=32):
    return rows * dim * (dtype_bits // 8)

print(embedding_ram_bytes(1_000_000, 768, 32) / 1e9)
```

- (A) `1.54`
- (B) `3.07`
- (C) `6.14`
- (D) `768.0`

### Q15. A 32 GB server holds an 8 GB model and a 4 GB index. What is the largest batch of 768-dim float32 embeddings?
**Difficulty:** Hard

- (A) 32 GB / 3072 bytes ≈ 11,145,833
- (B) (32 − 8 − 4) GB / 3072 bytes ≈ 6,510,416
- (C) (32 − 8) GB / 768 ≈ 32,552,083
- (D) 20 GB / 768 bytes ≈ 27,322,916

### Q16. What is the output?
**Difficulty:** Hard

```python
import timeit

def concat(n):
    s = ""
    for _ in range(n):
        s += "x"
    return s

def join_build(n):
    return "".join(["x"] * n)

print(concat(100) == join_build(100))
print(timeit.timeit(lambda: concat(500_000), number=5) >
      timeit.timeit(lambda: join_build(500_000), number=5))
```

- (A) `True` then `True`
- (B) `True` then `False`
- (C) `False` then `True`
- (D) `False` then `False`

### Q17. Which statement about `gc` is TRUE?
**Difficulty:** Hard

- (A) The GC is what normally frees objects; refcounting is a backup
- (B) The GC exists to collect reference cycles that refcounting cannot
- (C) `gc.disable()` speeds up all programs
- (D) The GC never runs unless you call `gc.collect()`

### Q18. What is the output?
**Difficulty:** Medium

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

def spin(n):
    return sum(range(n))

def time_pool(cls):
    t0 = time.perf_counter()
    with cls(max_workers=4) as pool:
        list(pool.map(spin, [300_000] * 4))
    return time.perf_counter() - t0

a = time_pool(ThreadPoolExecutor)
b = time_pool(ProcessPoolExecutor)
print(a > b)
```

*(Single-core machine; both calls succeed.)*

- (A) `True` — threads serialize on the GIL
- (B) `False` — threads are faster for CPU work
- (C) `True` always, even on 4 cores
- (D) `False` — ProcessPool cannot run on Windows

### Q19. What is the per-record memory win of `__slots__`?
**Difficulty:** Medium

- (A) 0 bytes — instances are the same size
- (B) ~264 bytes per record (the removed `__dict__`)
- (C) Exactly 8 bytes
- (D) The win only exists on 64-bit systems

### Q20. Which is the correct memory ceiling statement for a 1M×768 float32 matrix in numpy?
**Difficulty:** Hard

- (A) 3.07 GB contiguous — the `rows × dim × bytes` formula
- (B) 3.07 GB plus 24 MB of Python float objects
- (C) 6.14 GB because numpy doubles memory
- (D) ~64 MB — the same as a Python list of ints

---

## Answer Key

### Q1 — (B)
`sys.getsizeof` returns the object's own size — its header and internal
slots — not the referenced objects. That is the shallow size.
- (A) describes the deep size, which needs `tracemalloc`.
- (C/D) are different measurements entirely.

### Q2 — (B)
An empty dict is 64 bytes on CPython 3.13.
- (A) empty containers still have an allocation cost.
- (C) `getsizeof` works on any object.
- (D) object sizes are fixed per type, not per process.

### Q3 — (B)
`__slots__` replaces the per-instance `__dict__` with fixed
descriptors — smaller, faster, and new attributes are rejected.
- (A) slots objects are still GC-tracked when they hold references.
- (C) `__init__` still works.
- (D) `__weakref__` is also dropped (unless declared) — but the dict is
  the memory story.

### Q4 — (B)
200 is in the cached range −5..256, so `200 is 200` is True; `2**40`
parsed at runtime is a fresh object, so identity is False.
- (A) large ints are never shared.
- (C) the small-int cache makes the first True.
- (D) no error occurs.

### Q5 — (B)
`is None` is the canonical idiom — `None` is a singleton.
- (A) `1000` is outside the small-int cache; identity is unreliable.
- (C) `== None` works but is non-idiomatic.
- (D) floats are never interned.

### Q6 — (B)
`str` is immutable; every `+=` copies the whole growing string —
O(1) + O(2) + ... + O(n) = O(n²).
- (A) would be true of `"".join`.
- (C/D) wrong complexity classes.

### Q7 — (A)
The two literals fold to the same constant, so they are both equal
and identical.
- (B) is the interning "gotcha" answer — but constant folding makes
  them one object here.
- (C/D) wrong — equality holds.

### Q8 — (C)
The generator expression sums one line at a time — O(1) memory.
- (A) `.read().splitlines()` materializes everything.
- (B) `list(open(f))` materializes all lines.
- (D) `.read()` loads the whole file.

### Q9 — (A)
`tracemalloc` reports the deep size — the list header *plus* the
million references it holds — which exceeds the shallow
`sys.getsizeof(big)`.
- (B) would mean shallow == deep.
- (C) no error.
- (D) exact equality is never the case for containers.

### Q10 — (B)
`memoryview` slicing is zero-copy; `.tobytes()` then copies only the
sliced bytes out.
- (A) the slice itself does not copy.
- (C) only 9 bytes are involved.
- (D) memoryview slicing bytes is fully supported.

### Q11 — (B)
The GIL lets one thread execute Python bytecode at a time; CPU-bound
threads take turns.
- (A) process startup is slower, not threads' problem.
- (C) the OS schedules across cores — the GIL is the limit.
- (D) threads exist everywhere; the GIL is the constraint.

### Q12 — (B)
The two nodes form a reference cycle; refcounting cannot free them,
so the cycle collector reclaims exactly 2 objects.
- (A) would mean nothing was collected.
- (C) no such error.
- (D) `gc.collect()` returns a count.

### Q13 — (B)
`cProfile` profiles real runs and reports per-function cumulative time.
- (A) `timeit` measures microbenchmarks, not hot spots.
- (C) `getsizeof` measures one object.
- (D) sleeps don't measure anything.

### Q14 — (B)
1,000,000 × 768 × 4 = 3,072,000,000 bytes ≈ 3.07 GB.
- (A) 1.54 is the float16 value.
- (C) 6.14 is the float64 value.
- (D) wrong formula entirely.

### Q15 — (B)
Available RAM = 32 − 8 − 4 = 20 GB; per-row cost = 768 × 4 = 3072 B;
20e9 // 3072 ≈ 6,510,416.
- (A) ignores the model and index overhead.
- (C) divides bytes by dim, forgetting the 4 bytes per element.
- (D) same unit error.

### Q16 — (A)
Both functions produce `"x" * 100`, so equality is True; `+=` is
O(n²) and measurably slower than `join` at n = 500k, so the ratio
comparison is also True.
- (B) contradicts the measured O(n²) vs O(n) gap.
- (C/D) the strings are identical.

### Q17 — (B)
Refcounting is the primary reclamation mechanism; `gc` exists only
for reference cycles.
- (A) the roles are reversed.
- (C) `gc.disable()` risks leaking cyclic garbage.
- (D) the GC runs automatically on thresholds.

### Q18 — (A)
On a single core, threads serialize on the GIL; processes run in
parallel, so processes finish faster.
- (B) threads are never faster for CPU-bound work under the GIL.
- (C) on 4 cores the gap may shrink, but single-core is what the
  scenario states.
- (D) ProcessPoolExecutor works on Windows (spawn).

### Q19 — (B)
The per-instance `__dict__` costs ~264–300 bytes; `__slots__` removes
it — the win is real and per record.
- (A) is false; the dict is the difference.
- (C) 8 bytes is the size of a pointer, not the dict.
- (D) the win exists on every platform.

### Q20 — (A)
numpy stores the matrix contiguously: rows × dim × bytes = 3.07 GB —
no per-element Python object overhead.
- (B) is the *Python-list* cost model, not numpy's.
- (C) numpy does not double memory.
- (D) 64 MB is nowhere near the real figure.
