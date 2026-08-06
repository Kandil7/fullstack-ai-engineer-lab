# 01-core-python — 52: Memory & Performance — Thinking in Bytes

## Topic Overview

Python hides memory and speed behind a friendly face — until a 5 GB
dataset or a slow loop reveals the truth. This topic makes you think in
bytes: shallow vs deep sizes, `__slots__`, interning surprises, the
O(n²) string trap, streaming generators, zero-copy views, the GIL, and
the embedding-memory calculation every AI engineer must be able to do
on a whiteboard: 1M × 768 float32 ≈ 3 GB.

## Learning Objectives

After this topic you can:

- Explain why `sys.getsizeof` is shallow and use `tracemalloc` for the
  real number.
- Measure the `__slots__` win and know what it costs (no new attrs).
- Distinguish `is` (identity) from `==` (equality) and predict the
  small-int / interned-string surprises.
- Prove that `"".join` beats `+=` string building and explain why
  (O(n) vs O(n²)).
- Choose generators over lists for streaming, and `memoryview` for
  zero-copy slicing.
- Explain the GIL: threads for I/O, processes for CPU, async for waits.
- Estimate RAM for any tensor: `rows × dim × bytes_per_element`.

## Prerequisites

- Object model basics: instances, attributes, `__dict__` (topics 41, 43).
- Iterators and generators (topics 02-generators, 48).
- `timeit` exposure is helpful; it is introduced from scratch here.

---

## 1. Measuring Object Size — Shallow vs Deep

`sys.getsizeof(x)` returns the size of the object itself — **not** the
objects it references. A list of a million ints "is" just the list
header; the ints are separate objects the header points to.

```python
import sys

print(sys.getsizeof([0, 1, 2, 3]))                    # 88  (list header only)
print(sys.getsizeof({}))                              # 64  (empty dict)
print(sys.getsizeof({"a": 1, "b": 2, "c": 3, "d": 4}))  # 184
print(sys.getsizeof(2**62), sys.getsizeof(1.5))       # 36 24

# Output:
# 88
# 64
# 184
# 36 24
```

The shallow truth is a trap: a 10-million-element list of ints reports
~80 MB of header but the ints themselves cost 28+ bytes each — the real
footprint is 3–4× larger. For the **deep** number, use `tracemalloc`:

```python
import tracemalloc

tracemalloc.start()
big = [0] * 1_000_000
_cur, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"deep memory: {peak / 1e6:.1f} MB")   # list header + 1M int refs
```

Memory accounting rules of thumb: a `float` is 24 bytes, an `int` is 28
(small) to 36 (large), each `str` adds ~50 bytes plus the text, and a
dict entry is ~72 bytes. Every "small" Python object has a fixed tax.

---

## 2. `__slots__` — Drop the Per-Instance Dict

Every normal instance carries a `__dict__` (a dict of attributes). That
dict is ~290–300 bytes per record — enormous for million-row workloads.
`__slots__` replaces it with fixed descriptors: smaller instances, faster
attribute access, and no new attributes.

```python
import sys

class ManyDict:
    def __init__(self) -> None:
        self.a = 1; self.b = 2; self.c = 3; self.d = 4; self.e = 5

class ManySlots:
    __slots__ = ("a", "b", "c", "d", "e")
    def __init__(self) -> None:
        self.a = 1; self.b = 2; self.c = 3; self.d = 4; self.e = 5

md = ManyDict()
ms = ManySlots()
print(sys.getsizeof(md) + sys.getsizeof(md.__dict__))  # 336  (instance + dict)
print(sys.getsizeof(ms))                               # 72   (slots only)

# Output:
# 336
# 72
```

The win is ~264 bytes per record — for a million records, ~264 MB.
(Note: on 3.13 the bare instance may measure the same either way; the
dict is where the memory lives, and that is what `__slots__` removes.)

**The cost**: `__slots__` blocks new attributes —

```python
ms.z = 1  # AttributeError: 'ManySlots' object has no attribute 'z'
```

— and interacts with inheritance: a subclass must redeclare `__slots__`
or it gets a `__dict__` again. Use slots for hot, fixed-shape records
(rows, chunks, tokens), never for flexible DTOs.

---

## 3. Small-Int Caching & String Interning — `is` vs `==`

CPython caches ints from -5 to 256 and interns many short strings —
meaning `is` can say "same object" for values that merely compare equal,
and then say "different object" for larger ones. Never use `is` for
value comparison.

```python
a, b = 200, 200
print(a is b)                        # True  (cached small int)

big_a = 2**40
big_b = int(str(2**40))              # parsed at runtime -> fresh object
print(big_a == big_b)                # True  (equal values)
print(big_a is big_b)                # False (distinct objects)

s1 = "model_checkpoint"
s2 = "model_" + "checkpoint"         # folded constant -> same object
print(s1 is s2)                      # True  (interned)

# Output:
# True
# True
# False
# True
```

Rules of thumb: `is` is for `None`, singletons, and identity checks;
`==` is for values. The interning behavior is an implementation detail —
rely on it never, and enjoy it when it happens.

---

## 4. String Building — `join`, Not `+=`

`str` is immutable: `s += x` allocates a brand-new string and copies
everything each iteration. Building a string in a loop is O(n²); a single
`"".join` is O(n). The fix is one line.

```python
import timeit

def concat_loop(n: int) -> str:
    s = ""
    for _ in range(n):
        s += "x"
    return s

def join_parts(n: int) -> str:
    return "".join(["x"] * n)

for n in (50_000, 500_000):
    t_loop = timeit.timeit(lambda: concat_loop(n), number=5)
    t_join = timeit.timeit(lambda: join_parts(n), number=5)
    print(f"n={n}: +=  {t_loop:.3f}s   join {t_join:.4f}s   {t_loop / t_join:.0f}x")

# Output (indicative):
# n=50000: +=  0.020s   join 0.0019s   11x
# n=500000: +=  0.204s   join 0.0178s   11x
```

The ratio is ~constant per magnitude because both are re-measured at
larger n — but the *asymptotics* differ: double n and `+=` quadruples
its work, join doubles. At prompt-assembly scale (10⁵–10⁶ tokens) the
quadratic cost is a real latency tax. Prefer:

```python
parts = ["<|im_start|>system\n", system_prompt, "\n<|im_end|>"]
message = "".join(parts)
```

`+=` is fine for a handful of appends; the rule is: never build strings
in a loop whose length you can't bound.

---

## 5. Generators vs Lists at Scale

A generator holds one value at a time; a list holds all of them. The
difference is O(1) vs O(n) memory — the difference between processing a
10 GB corpus and crashing.

```python
import tracemalloc

def stream_lines(n: int) -> int:
    """Sum lengths of n synthetic lines — O(1) memory."""
    return sum(len(f"line {i}") for i in range(n))

tracemalloc.start()
total = stream_lines(1_000_000)
_cur, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(total, f"peak: {peak / 1024:.0f} KiB")

# Output:
# 9000000 peak: 4 KiB
```

The list equivalent (`[len(f"line {i}") for i in range(n)]`) would hold
a million ints — ~36 MB. Generators defer computation; that is also why
`json.loads` of a whole dataset file is different from a JSONL stream
(topic 51): the stream is O(1).

---

## 6. `memoryview` — Zero-Copy Slicing

Slicing `bytes` copies. `memoryview` slices without copying — reading a
header from a model artifact without loading the payload twice.

```python
payload = b"HEADER:v2" + b"\x00" * 64 + b"weights..."
view = memoryview(payload)

header = view[:9].tobytes()        # copy only the 9 bytes you need
print(header)

# Output:
# b'HEADER:v2'
```

`sys.getsizeof(memoryview(b"x" * 100_000_000))` is ~184 bytes regardless
of the buffer size — the view is a pointer plus metadata, not a copy.
Use memoryview for: slicing big binary artifacts (model files, images),
feeding buffers to numpy, and avoiding double-copies in hot parse loops.
The rules: a memoryview must be released (`view.release()` or del) to
free the underlying buffer, and you must call `.tobytes()` when you need
a real bytes object.

---

## 7. The GIL — Threads for I/O, Processes for CPU

CPython's Global Interpreter Lock lets exactly one thread run Python
bytecode at a time. Consequence: **CPU-bound work does not parallelize
across threads** — they take turns. **I/O-bound work does benefit**:
while a thread waits on a socket/disk (releasing the GIL), other threads
run.

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

def spin(n: int) -> int:
    total = 0
    for i in range(n):
        total += i
    return total

def time_pool(pool_cls, n_workers: int, n: int) -> float:
    t0 = time.perf_counter()
    with pool_cls(max_workers=n_workers) as pool:
        list(pool.map(spin, [n] * n_workers))
    return time.perf_counter() - t0

print(f"threads: {time_pool(ThreadPoolExecutor, 4, 300_000):.3f}s")
print(f"processes: {time_pool(ProcessPoolExecutor, 4, 300_000):.3f}s")

# Output (indicative, single core):
# threads:    0.095s   (GIL serializes)
# processes:  0.030s   (real parallelism)
```

The AI consequences are concrete:

- **Inference servers use processes or async, not threads**, for CPU/GPU
  work — the GIL would serialize them.
- Threads are right for I/O: waiting on the model API, the database, the
  filesystem. `asyncio` is the modern answer for many concurrent waits.
- Since 3.13 the GIL can be *disabled* (free-threaded builds) — but the
  default CPython everyone runs still has it. Design for it.

---

## 8. Refcounting, Cycles, and `gc`

CPython frees objects by **reference counting**: when the count hits
zero, memory is reclaimed immediately. The garbage collector (`gc`)
exists for one reason — **reference cycles** (a points to b, b to a),
which refcounting alone cannot detect.

```python
import gc, sys

x = [1, 2, 3]
print(sys.getrefcount(x) - 1)        # 1  (the local binding)

class Node:
    __slots__ = ("next",)

n1, n2 = Node(), Node()
n1.next = n2                          # cycle: n1 -> n2 -> n1
n2.next = n1
del n1, n2                            # refcounts never reach zero
print(gc.collect())                   # 2  objects collected by the cycle GC

# Output:
# 1
# 2
```

Practical rules: cycles get cleaned eventually (generational GC), but
"eventually" is not deterministic — for large cyclic caches, call
`gc.collect()` at safe checkpoints or break cycles manually (`next = None`).
Dataclasses with back-references are a common cycle source; `__slots__`
does not prevent cycles, it only shrinks them.

---

## 9. `timeit` and `cProfile` — Measure First

Never guess which code is slow. `timeit` measures microbenchmarks;
`cProfile` finds hot spots in real runs.

```python
import timeit

setup = "nums = list(range(1000))"
t_map = timeit.timeit("list(map(lambda x: x * 2, nums))", setup=setup, number=10_000)
t_comp = timeit.timeit("[x * 2 for x in nums]", setup=setup, number=10_000)
print(f"map: {t_map:.3f}s   comp: {t_comp:.3f}s")
```

```python
import cProfile, pstats

profiler = cProfile.Profile()
profiler.enable()
# ... real workload ...
profiler.disable()
pstats.Stats(profiler).sort_stats("cumulative").print_stats(10)
```

Rules: benchmark the *real* shape (n, data types) at realistic scale;
run each candidate several times and compare medians; profile before
optimizing — the 80/20 rule means the hot function is usually not the
one you guessed. `tracemalloc` (sections 1, 5) is the memory-side twin:
measure before and after a change, and keep the number.

---

## 10. Production Pattern — Embedding Memory Estimate

The calculation every AI engineer must be able to do on a whiteboard:

```python
def embedding_ram_bytes(rows: int, dim: int, dtype_bits: int = 32) -> int:
    """Total bytes for a rows x dim matrix, dtype-aware."""
    return rows * dim * (dtype_bits // 8)

rows, dim = 1_000_000, 768
for bits in (64, 32, 16, 8):
    gb = embedding_ram_bytes(rows, dim, bits) / 1e9
    print(f"float{bits}: {gb:.2f} GB for {rows:,} x {dim}")

# Output:
# float64: 6.14 GB for 1,000,000 x 768
# float32: 3.07 GB for 1,000,000 x 768
# float16: 1.54 GB for 1,000,000 x 768
# float8:  0.77 GB for 1,000,000 x 768
```

Notes that make the number honest:

- **float32 over float64 halves your bill** — 3.07 GB vs 6.14 GB. This
  is why embeddings and weights are float32 by default.
- The Python-side cost is separate: 1M Python floats as a list is
  ~24 MB of floats + ~8 MB of pointers + list overhead; numpy stores
  the raw matrix in 3.07 GB *contiguously*.
- Batch size vs OOM: `batch × dim × bytes` must fit alongside the model
  and the index; compute it *before* launching the job, not after the
  OOM killer.

---

## Common Mistakes to Avoid

### Mistake 1: Trusting `sys.getsizeof` as the deep size
```python
# WRONG - shallow: header only, ints are separate objects
size = sys.getsizeof(huge_list_of_ints)

# CORRECT - tracemalloc for the real footprint
tracemalloc.start()
_ = build_huge_structure()
_, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
```

### Mistake 2: `is` for value comparison
```python
# WRONG - False for large ints; correct by accident for small ones
if cache_hits is 1000:

# CORRECT - == for values, is only for None/singletons
if cache_hits == 1000:
```

### Mistake 3: String building with `+=` in a hot loop
```python
# WRONG - O(n^2): each append copies the whole growing string
msg = ""
for part in parts:
    msg += part

# CORRECT - O(n): one pass
msg = "".join(parts)
```

### Mistake 4: Threads for CPU-bound work
```python
# WRONG - GIL serializes CPU-bound scoring
with ThreadPoolExecutor() as pool:
    pool.map(score_cpu_heavy, docs)

# CORRECT - processes for CPU; threads/async for I/O waits
with ProcessPoolExecutor() as pool:
    pool.map(score_cpu_heavy, docs)
```

### Mistake 5: Materializing a stream you can iterate
```python
# WRONG - O(n) memory; OOM on big files
lines = [parse(line) for line in open_big_file()]

# CORRECT - O(1) memory
total = sum(parse(line) for line in open_big_file())
```

### Mistake 6: Optimizing without measuring
```python
# WRONG - rewrite the "obviously slow" part blindly
# CORRECT - profile first: cProfile, then timeit the candidates
#           (the hot function is usually not the one you guessed)
```

## Best Practices

- Size things for real: `tracemalloc` for deep memory, `timeit` for
  microbenchmarks, `cProfile` for hot spots.
- Use `__slots__` for fixed-shape hot records; keep `__dict__` for
  flexible DTOs.
- `==` for values, `is` for `None`/identity; never rely on interning.
- Build strings with `"".join`; stream with generators; slice big
  binaries with `memoryview`.
- Threads for I/O, processes for CPU, async for waits.
- Do the embedding math before the job: `rows × dim × bytes`.

## Complexity and Cost

| Operation | Cost | Why |
|---|---|---|
| `sys.getsizeof` | O(1) | Header only — shallow by design |
| `__slots__` per record | ~264 B saved | No per-instance `__dict__` |
| `s += x` in a loop | O(n²) | Every append copies the string |
| `"".join(parts)` | O(n) | Single allocation, one pass |
| Generator `next()` | O(1) memory | One value at a time |
| `bytes[i:j]` | O(j−i) copy | New object |
| `memoryview[i:j]` | O(1) | Pointer arithmetic, no copy |
| ThreadPool for CPU | ~1× speedup | GIL serializes bytecode |
| ProcessPool for CPU | ~n× speedup | Real parallelism |
| 1M × 768 float32 | 3.07 GB | rows × dim × 4 bytes |

## AI Engineering Relevance

- **The 3 GB whiteboard question**: 1M × 768 float32 ≈ 3.07 GB; float16
  halves it, float64 doubles it. This single calculation drives index
  sizing, batch sizing, and cloud bills.
- **Batch size vs OOM**: `batch × dim × bytes_per_element` must fit
  alongside model weights and the index — compute it before launching.
- **The GIL shapes inference servers**: processes or async, not threads;
  thread pools are for I/O (API calls, DB waits, file loads).
- **Streaming datasets**: generators + JSONL (topic 51) process
  multi-GB fine-tuning corpora in O(1) memory.
- **Zero-copy artifacts**: `memoryview` reads model headers and image
  buffers without double allocations.

## Practice Exercises

### Exercise 1: Measure the Dict Tax (Difficulty: Easy)
Build `ManyDict` and `ManySlots` with 5 attributes (section 2). Print
`getsizeof(instance) + getsizeof(__dict__)` vs `getsizeof(slots_instance)`.
For 1,000,000 records, compute the total MB saved.

### Exercise 2: is vs == Quiz (Difficulty: Easy)
Predict the outputs of section 3's snippet, then run it. Explain why
`big_a is big_b` is False while `a is b` is True.

### Exercise 3: join vs += Measurement (Difficulty: Medium)
Reproduce section 4's benchmark at n = 50_000 and n = 500_000. Report
both ratios. Then confirm `concat_loop(100) == join_parts(100)` (same
string, different cost).

### Exercise 4: Streaming vs Materializing (Difficulty: Medium)
Using `tracemalloc`, compare `stream_lines(1_000_000)` (generator) with
a list-comprehension version. Report both peaks — expect ~4 KiB vs
~36 MB.

### Exercise 5: Embedding Budget (Difficulty: Hard)
A server has 32 GB of RAM. The model occupies 8 GB and the index 4 GB.
Compute the largest batch of 768-dim float32 embeddings you can hold in
the remaining memory, and again for float16. Verify with
`embedding_ram_bytes`.

## Summary

- `sys.getsizeof` is shallow; `tracemalloc` is the truth.
- `__slots__` removes the ~264-byte per-instance dict — huge for
  million-row workloads, at the cost of dynamic attributes.
- `is` ≠ `==`; small ints and interned strings make identity surprising.
- `"".join` is O(n); `+=` in a loop is O(n²).
- Generators stream with O(1) memory; `memoryview` slices zero-copy.
- GIL: threads for I/O, processes for CPU.
- Embedding memory: `rows × dim × bytes` — 1M × 768 × 4 ≈ 3.07 GB.

## Quick Reference

```python
import sys, timeit, tracemalloc

sys.getsizeof(obj)                 # shallow size
# tracemalloc.start() ... get_traced_memory() ... stop()   # deep size

class Record:                      # fixed-shape hot records
    __slots__ = ("id", "vec")

x == y                             # values
x is y                             # identity (None, singletons only)

"".join(parts)                     # O(n) - never s += part in a loop
sum(len(line) for line in f)       # O(1) memory streaming
memoryview(payload)[:9].tobytes()  # zero-copy slice

# ThreadPoolExecutor -> I/O; ProcessPoolExecutor -> CPU; asyncio -> waits
rows * dim * (bits // 8)           # tensor bytes: 1M*768*4 = 3.07 GB
```

## Next Steps

- Apply the size math to real artifacts: `tracemalloc` the JSONL reader
  from topic 51 on a large dataset file, then the sqlite3 bulk insert.
- Meet numpy: the same 1M × 768 matrix in numpy is one contiguous
  buffer — the natural successor to this topic for AI workloads.
- Revisit 49's top-k challenge with the memory lens: why the heap
  version survives 10⁷ items and the sort version does not.
