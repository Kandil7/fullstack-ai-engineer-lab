# 52: Memory & Performance — Glossary

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `__slots__` | Class Attribute | Declares fixed attributes; removes the per-instance `__dict__` |
| `cProfile` | Module | Profiles real runs; finds hot spots by cumulative time |
| cycle | Concept | Objects referencing each other; refcounting cannot free them |
| deep size | Concept | An object plus everything it references (`tracemalloc`) |
| float32 math | Formula | `rows × dim × bytes` — 1M × 768 × 4 = 3.07 GB |
| `gc` | Module | Collects reference cycles that refcounting misses |
| generator | Pattern | Yields one value at a time; O(1) memory |
| GIL | Concept | Global Interpreter Lock; one bytecode thread at a time |
| interning | Concept | CPython reuses short strings; `is` may match equal values |
| `is` vs `==` | Rule | Identity vs equality; `is` only for `None`/singletons |
| `"".join` | Pattern | O(n) string building; `+=` in a loop is O(n²) |
| `memoryview` | Class | Zero-copy slice over a buffer |
| O(n²) | Complexity | Quadruples work when n doubles |
| refcount | Concept | CPython frees objects when references hit zero |
| shallow size | Concept | `sys.getsizeof` — the object alone, not its references |
| small-int cache | Concept | CPython caches ints −5..256; larger ints are distinct objects |
| `timeit` | Module | Microbenchmarks with timing control |
| `tracemalloc` | Module | Tracks deep memory allocations; peak snapshots |
| ThreadPool vs ProcessPool | Pattern | Threads for I/O (GIL released), processes for CPU |
| 3.07 GB | Benchmark | The whiteboard number: 1M × 768 float32 embeddings |

## Detailed Definitions

### `__slots__`
**Definition**: A class attribute listing fixed attribute names. The
class then stores attributes in descriptors instead of a per-instance
`__dict__` — smaller instances, faster access, and **no new attributes**.

**Example**:
```python
import sys

class Record:
    __slots__ = ("id", "vec")
    def __init__(self, i, v):
        self.id, self.vec = i, v

r = Record(1, [0.1, 0.2])
print(sys.getsizeof(r))          # ~56 for 2 slots, no dict
r.extra = 1                      # AttributeError: 'Record' object has no attribute 'extra'
```

**Complexity**: saves ~264 bytes per record (the dict); access is
faster (no dict lookup).

**Related**: deep size, shallow size

### `cProfile`
**Definition**: The standard profiler: `cProfile.Profile()` around a
workload, then `pstats.Stats(...).sort_stats("cumulative")` — shows
where time actually goes, by function.

**Example**:
```python
import cProfile, pstats
p = cProfile.Profile()
p.enable()
# ... real workload ...
p.disable()
pstats.Stats(p).sort_stats("cumulative").print_stats(10)
```

**Complexity**: ~10–50% overhead; used for real runs, not microbenchmarks.

**Related**: `timeit`

### cycle
**Definition**: A group of objects referencing each other (`a.next = b;
b.next = a`). Refcounting never sees a zero count, so the cycle GC
(`gc.collect()`) is required to reclaim them.

**Example**:
```python
import gc

class Node:
    __slots__ = ("next",)
n1, n2 = Node(), Node()
n1.next, n2.next = n2, n1
del n1, n2
print(gc.collect())              # 2 objects collected
```

**Complexity**: cyclic garbage is reclaimed generational-ly — not
deterministic; break cycles or checkpoint `gc.collect()` for large caches.

**Related**: refcount, `gc`

### deep size
**Definition**: The real memory of a structure: the object plus every
object it references (recursively). `sys.getsizeof` never gives this;
`tracemalloc` does, by tracking allocations.

**Example**:
```python
import tracemalloc
tracemalloc.start()
big = [0] * 1_000_000
_, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(peak / 1e6, "MB")          # list header + 1M references
```

**Complexity**: O(1) to query peak; allocation tracking adds overhead.

**Related**: shallow size, `tracemalloc`

### float32 math
**Definition**: `rows × dim × (bits // 8)` = tensor RAM bytes.
1,000,000 × 768 × 4 = 3,072,000,000 bytes ≈ **3.07 GB**; float64
doubles it (6.14 GB), float16 halves it (1.54 GB).

**Example**:
```python
def embedding_ram_bytes(rows, dim, dtype_bits=32):
    return rows * dim * (dtype_bits // 8)
print(embedding_ram_bytes(1_000_000, 768, 32) / 1e9)   # 3.07
```

**Complexity**: O(1).

**Related**: 3.07 GB

### `gc`
**Definition**: The garbage collector module. Its only job is reference
cycles — refcounting handles everything else. `gc.collect()` runs a
full collection; `gc.disable()` is almost always wrong.

**Example**:
```python
import gc
print(gc.get_objects()[:1])      # (inspect); gc.collect() -> n collected
```

**Complexity**: full collections are O(live objects); avoid hot paths.

**Related**: cycle, refcount

### generator
**Definition**: A function with `yield`; calling it returns an iterator
that computes one value at a time. Memory is O(1) regardless of the
sequence length — the streaming pattern.

**Example**:
```python
def lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.strip()

total = sum(len(l) for l in lines("big.txt"))   # O(1) memory
```

**Complexity**: O(1) memory, O(n) total time.

**Related**: deep size

### GIL
**Definition**: The Global Interpreter Lock — at most one thread runs
Python bytecode at a time. CPU-bound threads serialize; I/O-bound
threads benefit (they release the lock while waiting). Process pools
give real CPU parallelism.

**Example**:
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
# CPU-bound scoring: ProcessPoolExecutor wins
# I/O waits (API, DB): ThreadPoolExecutor (or asyncio) wins
```

**Complexity**: threads for I/O ≈ n× on waits; threads for CPU ≈ 1×.

**Related**: ThreadPool vs ProcessPool

### interning
**Definition**: CPython may reuse one object for equal short strings
(folded constants, some identifiers) and for small ints (−5..256). So
`is` can return True for equal values — and False for larger ones.

**Example**:
```python
a, b = 200, 200
print(a is b)                       # True (cached)
big_a, big_b = 2**40, int(str(2**40))
print(big_a is big_b)               # False (distinct objects)
```

**Complexity**: O(1) lookup when interned.

**Related**: `is` vs `==`, small-int cache

### `is` vs `==`
**Definition**: `==` compares values; `is` compares object identity.
Use `is` only for `None` and singletons — interning makes identity
predictable only for those.

**Example**:
```python
if x is None:      # correct idiom
if flag is True:   # works, but == is clearer
if count is 1000:  # WRONG - may be False for large ints
```

**Complexity**: O(1) both; `is` skips `__eq__`.

**Related**: interning, small-int cache

### `"".join`
**Definition**: The O(n) way to build a string from parts — one
allocation, one pass. `+=` in a loop copies the whole growing string
each iteration: O(n²).

**Example**:
```python
parts = ["<|im_start|>system\n", prompt, "\n<|im_end|>"]
message = "".join(parts)            # O(n)

s = ""
for p in parts:
    s += p                          # O(n^2) as s grows
```

**Complexity**: O(n) vs O(n²); measured ~11× at n = 500k.

**Related**: O(n²)

### `memoryview`
**Definition**: A zero-copy window over a buffer. `memoryview(payload)[:9]`
slices without copying; `.tobytes()` copies only when you need a real
bytes object. Release with `del view`/`view.release()`.

**Example**:
```python
payload = b"HEADER:v2" + b"\x00" * 64 + b"weights..."
print(memoryview(payload)[:9].tobytes())    # b'HEADER:v2'
```

**Complexity**: slicing O(1); `getsizeof(view)` ~184 regardless of
buffer size.

**Related**: deep size

### O(n²)
**Definition**: Work quadruples when n doubles. Classic Python sources:
`+=` string building in a loop, `list.index`/`in` scans in a loop,
repeated `del lst[0]`. The fix is usually a different structure
(`"".join`, dict/set, deque).

**Example**:
```python
# quadratic:        for i in range(n): s += "x"
# linear:           "".join(["x"] * n)
```

**Complexity**: n² operations vs n.

**Related**: `"".join`

### refcount
**Definition**: CPython's primary memory management: each object counts
its references; at zero, it is freed immediately. Fast and deterministic
— except for cycles, which are the GC's job.

**Example**:
```python
import sys
x = [1, 2, 3]
print(sys.getrefcount(x) - 1)       # 1 (the local binding)
```

**Complexity**: O(1) per reference change.

**Related**: cycle, `gc`

### shallow size
**Definition**: `sys.getsizeof(obj)` — the object header alone. A list
reports only its own buffer; the referenced ints/strings/dicts are
separate objects not counted.

**Example**:
```python
import sys
print(sys.getsizeof([0, 1, 2, 3]))   # 88 - just the list
print(sys.getsizeof({}))             # 64 - empty dict
```

**Complexity**: O(1).

**Related**: deep size, `tracemalloc`

### small-int cache
**Definition**: CPython pre-allocates ints −5..256; every reference to
`200` is the same object. Larger ints are created fresh — `is` fails
for equal values beyond the cache.

**Example**:
```python
print(200 is 200)                    # True (cached)
print(2**40 is int(str(2**40)))      # False (fresh objects)
```

**Complexity**: O(1).

**Related**: interning, `is` vs `==`

### `timeit`
**Definition**: `timeit.timeit(stmt, setup=..., number=...)` times a
snippet precisely — the microbenchmark tool. Compare candidates on the
real shape and scale; report ratios, not absolute wall-clock numbers.

**Example**:
```python
import timeit
t = timeit.timeit("''.join(['x'] * 1000)", number=10_000)
print(t)
```

**Complexity**: ~µs overhead per timing loop.

**Related**: `cProfile`

### `tracemalloc`
**Definition**: Tracks Python allocations and reports peak/live memory
— the deep-size truth. `tracemalloc.start()` → run → 
`tracemalloc.get_traced_memory()` → `tracemalloc.stop()`.

**Example**:
```python
import tracemalloc
tracemalloc.start()
big = [0] * 1_000_000
cur, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"peak {peak / 1e6:.1f} MB")
```

**Complexity**: tracking overhead ~20–50%; use around targeted regions.

**Related**: deep size, shallow size

### ThreadPool vs ProcessPool
**Definition**: `ThreadPoolExecutor` runs tasks on threads — right for
I/O waits (GIL released while waiting). `ProcessPoolExecutor` runs tasks
in separate processes — right for CPU-bound work (real parallelism).

**Example**:
```python
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor() as pool:
    scores = list(pool.map(score_embedding, batches))  # CPU: processes
```

**Complexity**: threads ≈ serial for CPU; processes ≈ n× cores.

**Related**: GIL

### 3.07 GB
**Definition**: The whiteboard number: 1,000,000 rows × 768 dims × 4
bytes (float32) = 3,072,000,000 bytes ≈ 3.07 GB. float64 = 6.14 GB,
float16 = 1.54 GB, float8 = 0.77 GB.

**Example**:
```python
print(1_000_000 * 768 * 4 / 1e9)    # 3.07
```

**Complexity**: O(1).

**Related**: float32 math

## Key Concepts Summary

### Sizes
- `sys.getsizeof` = shallow (header only); `tracemalloc` = deep truth.
- Per-record taxes: float 24 B, int 28–36 B, dict entry ~72 B,
  per-instance `__dict__` ~264 B.
- `__slots__` removes the dict for fixed-shape records.

### Identity
- `==` for values, `is` for `None`/singletons.
- Small ints (−5..256) and interned strings may share objects; large
  ints never do.

### The Two Classic Speed Traps
- `+=` string building: O(n²); `"".join`: O(n).
- Threads for CPU: serialized by the GIL; processes for CPU, threads/
  async for I/O.

### The AI Budget
- `rows × dim × bytes`: 1M × 768 × 4 ≈ 3.07 GB — the number to know
  before launching any embedding job.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `__slots__` — ___
2. shallow size — ___
3. GIL — ___
4. interning — ___
5. `"".join` — ___
6. generator — ___
7. `memoryview` — ___
8. refcount — ___
9. cycle — ___
10. 3.07 GB — ___

A. Removes the per-instance `__dict__`
B. `sys.getsizeof` measures this
C. One bytecode thread at a time
D. Equal short strings may be one object
E. O(n) string building
F. O(1) memory streaming
G. Zero-copy slicing
H. Frees objects at zero references
I. Objects referencing each other
J. 1M × 768 float32 embeddings

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H, 9-I, 10-J
