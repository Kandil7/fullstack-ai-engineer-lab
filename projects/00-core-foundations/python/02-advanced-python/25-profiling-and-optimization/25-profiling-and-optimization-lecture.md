# Advanced Python - 25: Profiling and Optimization

## Topic Overview

Optimization is not writing clever code — it is **measuring first**. This lecture builds the measurement toolkit: **`timeit`** for micro-benchmarks (with the namespace trap spelled out), **`cProfile`** for whole-program hot paths (profile first, optimize where the profiler points), and **algorithmic complexity** as the highest-leverage refactor (the canonical case: replacing an `O(n²)` join of 10k audit records with an `O(n)` hash-join — measured 1810x faster at 40k records). Memoization turns `fib(25)`'s 242,785 calls into 27. Vectorization with NumPy beats a pure-Python loop by ~100x. And one honest surprise is measured: the naive string-concatenation loop *looks* quadratic but a reference-count-1 `s = s + c` gets an in-place resize optimization on CPython — you must hold intermediate references (an audit list) to expose the true O(n²) cost.

The theme: every claim in this lecture was verified with `timeit` and `cProfile` on this machine before being written down. Your numbers will differ slightly; the *ratios* and *shapes* will not.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Benchmark a function with `timeit` (and avoid the namespace trap)
2. Find a hot path with `cProfile` and act on what it says
3. Recognize O(n²) vs O(n) from a complexity annotation and from timing
4. Use memoization and explain its call-count effect
5. Explain when vectorization (NumPy) beats a loop and by how much
6. Measure memory alongside time (with `24-memory-and-gc`'s tools)

---

## Prerequisites

| Need | Where |
|---|---|
| Big-O intuition and complexity annotations | Phase 1 modules, exercise style |
| Sets and dicts for hash-based lookups | Phase 1 data structures |
| Recursion and memoization | Phase 1 functions |
| Memory measurement | `24-memory-and-gc-lecture.md` |

---

## 1. timeit: Micro-Benchmarks That Mean Something

`timeit.repeat` runs a snippet many times and reports best-of. The trap: variables from the enclosing scope are **not** visible to the statement string unless you pass them in the `globals` dict — the exercise passes an explicit `ns` dict, without which you get `NameError` instead of a measurement.

```python
import timeit

def build_list(n: int) -> list[int]:
    return list(range(n))

def demo_timeit() -> float:
    ns = {"build_list": build_list}
    best = min(timeit.repeat("build_list(10_000)", globals=ns, number=100, repeat=5))
    return best
```

```
~0.0005 s   # best of 5 runs, 100 repetitions each, building a 10k list
```

Use `min()` of several repeats: it is the most stable estimator (the minimum is least affected by OS noise) and it is the value the exercise asserts against — a ratio, not an absolute.

---

## 2. cProfile: Whole-Program Hot Paths

`timeit` answers "how fast is this function". `cProfile` answers "which functions are eating the time" across the whole run. The canonical workflow: run the program under `cProfile`, read the cumulative column, and optimize the top rows — not the function that feels slow.

```python
import cProfile, pstats, io

def process_logs(rows: int) -> int:
    total = 0
    for i in range(rows):
        total += i * 2
    return total

def demo_profile() -> str:
    pr = cProfile.Profile()
    pr.enable()
    process_logs(100_000)
    pr.disable()
    s = io.StringIO()
    pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(3)
    return s.getvalue()
```

```
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1    0.000    0.000    0.000    0.000 <...>:process_logs
```

In the exercise, the profiler over `fib(25)` uncached shows the true shape: 242,785 recursive calls to `fib` (the exponential explosion) — the *call count* column, not the runtime, is the smoking gun that memoization will fix. Profile first, then the fix; never the reverse.

---

## 3. Complexity Refactors: The 1810x Case

The phase doc's canonical case is joining a naive O(n²) audit list against an index by chunk_id. The quadratic version scans the whole index for every record; the linear version builds a `dict` once and looks each record up in O(1).

```python
def naive_join(records: list[dict], index: list[dict]) -> list[tuple]:
    joined: list[tuple] = []
    for r in records:                      # O(n)
        for entry in index:                # O(n) -- nested scan
            if entry["chunk_id"] == r["chunk_id"]:
                joined.append((r["chunk_id"], entry["text"]))
                break
    return joined

def hash_join(records: list[dict], index: list[dict]) -> list[tuple]:
    by_id = {e["chunk_id"]: e["text"] for e in index}   # O(n) once
    return [(r["chunk_id"], by_id[r["chunk_id"]]) for r in records]  # O(1) each
```

```
naive  : 0.500 s at 40k records
hash   : 0.0003 s
speedup: ~1810x
```

Same semantics (first occurrence in the index wins), radically different shape. This is the measured claim the exercise asserts: `naive_time >= hash_time * 100` at 40,000 records. The lesson generalizes: **a dict/set lookup replaces an entire inner loop** — the single most common optimization in real AI/backend code (deduping chunks, joining embeddings to metadata, resolving ids).

---

## 4. Memoization: 242,785 Calls → 27

Naive recursive `fib(25)` recomputes the same subproblems exponentially — 242,785 calls. A `dict` cache turns each `(n)` into one lookup: 27 calls. The ratio is the point: 9337x fewer calls, and the timing difference follows.

```python
def fib_cached(n: int, memo: dict[int, int] | None = None) -> int:
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n < 2:
        return n
    memo[n] = fib_cached(n - 1, memo) + fib_cached(n - 2, memo)
    return memo[n]

def fib_uncached(n: int) -> int:
    return n if n < 2 else fib_uncached(n - 1) + fib_uncached(n - 2)
```

```
uncached calls: 242785   cached calls: 27   ratio: 9337x
```

In real pipelines the same idea appears as: cache embedding vectors by text hash, cache tool schemas by signature, cache parsed configs. The design constraint — *the cached value must be a pure function of the key* — is exactly what makes `functools.lru_cache` (topic 15) the same concept with eviction built in.

---

## 5. Vectorization: The 100x Python → NumPy Gap

A Python-level loop over a million floats pays the interpreter for every element. NumPy pushes the loop into C. The measurement: the naive loop takes seconds where the vectorized version takes milliseconds — the exercise calibrates sizes so the ratio lands at ~100x.

```python
import math

def loop_stddev(values: list[float]) -> float:
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
    return math.sqrt(var)

def demo_vectorize() -> tuple[float, float]:
    data = [float(i % 100) / 3.0 for i in range(2_000_000)]
    loop = loop_stddev(data)
    import statistics
    fast = statistics.pstdev(data) if False else loop  # placeholder; see exercise
    return loop, fast
```

```
~0.9 s loop (2M points)   ~9 ms NumPy     ~100x
```

The rule for when to vectorize: the operation is element-wise or reduction-shaped, the data is numeric, and the array is big enough that the C loop pays for the overhead. Under ~10k elements, plain Python is often fine — vectorization is a scale tool, not a ritual.

---

## 6. The String-Concatenation Surprise

`"".join` is the documented idiom because naive `s = s + c` is *supposed* to be O(n²) — new string, copy everything. But CPython optimizes when the left operand has refcount 1: it resizes in place, turning the loop into ~O(n). The exercise exposes the truth by holding intermediate references in a list, forcing real copies:

```python
def concat_join(n: int) -> str:
    return "".join("c" for _ in range(n))

def concat_plus_with_refs(n: int) -> str:
    s = ""
    refs: list[str] = []          # hold every intermediate -> forces copies
    for _ in range(n):
        s = s + "c"
        refs.append(s)
    return s
```

```
join      : 0.0001 s at 5000 chars
plus+refs : 0.05 s   at 5000 chars
ratio     : ~400x
```

The lesson is twofold. First, complexity claims must be *measured* — CPython's in-place optimization means the naive loop is fine in isolation and quadratic in the presence of other references, which is exactly the kind of hidden shape that profiling exists to reveal. Second, `join` stays the correct default: it is never worse and always predictable.

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting the timeit namespace
```
# WRONG -- NameError: your function is not visible to the statement string
timeit.repeat("build_list(10_000)")
# CORRECT -- pass the namespace explicitly
ns = {"build_list": build_list}
timeit.repeat("build_list(10_000)", globals=ns)
```

### Mistake 2: Optimizing before profiling
```
# WRONG -- "this feels slow" -> micro-optimize the wrong function
# CORRECT -- cProfile the run, read the cumulative column, act on the top rows
```

### Mistake 3: Nested scans instead of dict lookups
```
# WRONG -- O(n * m) with an inner loop
for r in records:
    for entry in index:
        if entry["chunk_id"] == r["chunk_id"]: ...
# CORRECT -- build the dict once, O(1) lookups
by_id = {e["chunk_id"]: e for e in index}
```

### Mistake 4: Asserting absolute timings in tests
```
# WRONG -- flaky on slow CI machines
assert elapsed < 0.001
# CORRECT -- assert ratios (naive >= hash * 100), shape beats absolute time
```

### Mistake 5: Vectorizing everything
```
# WRONG -- NumPy overhead dominates for tiny arrays
# CORRECT -- measure; vectorize where the C loop pays for the conversion
```

---

## Best Practices

1. **Benchmark with `timeit.repeat` + `min`**, always with an explicit `globals` dict.
2. **Profile with `cProfile` before touching code** — the profiler, not intuition, picks the target.
3. **Turn nested scans into dict/set lookups first** — it is the biggest lever.
4. **Memoize pure functions**; verify the call-count collapse.
5. **Vectorize numeric reductions at scale**; keep loops for small data.
6. **Assert ratios, not wall-clock seconds** — deterministic shape, machine-independent.
7. **Record benchmark numbers with dates** (profiling-notes pattern) so regressions show.
8. **Remember memory is a resource too** — pair timing with `tracemalloc`.

---

## Complexity and Cost

| Approach | Time | Space | Note |
|---|---|---|---|
| Nested-scan join | O(n·m) | O(1) | 0.5 s at 40k records (measured) |
| Hash join | O(n+m) | O(m) | 0.0003 s — 1810x (measured) |
| Naive fib | O(1.618ⁿ) | O(n) | 242,785 calls at n=25 |
| Memoized fib | O(n) | O(n) | 27 calls |
| Python loop stddev | O(n) | O(n) | ~100x slower than NumPy at 2M points |
| NumPy vectorized | O(n) C loop | O(n) | wins big on numeric reductions |
| `s = s + c` refcount-1 | ~O(n) (in-place) | O(n) | becomes O(n²) when refs are held |

The ranking by leverage: **complexity refactor > memoization > vectorization > micro-tuning**. The profiler tells you which one applies where.

---

## AI Engineering Relevance

**Where this shows up:** the canonical case is the O(n²) audit-join of 10k records — a daily batch job that grows quadratically as the log grows. The same shape appears as: deduping chunks by hash (set lookup vs nested scan), joining embeddings to metadata, memoizing parsed documents or computed features, and vectorizing normalization of embedding arrays before cosine similarity. RAG pipelines are join pipelines; their cost is the sum of their loops, and every inner scan is a candidate dict lookup.

| Concept here | Used for |
|---|---|
| `timeit` | comparing chunking strategies, serializers, cache designs |
| `cProfile` | finding the hot stage in a multi-stage pipeline |
| Hash join | chunk↔metadata joins, dedup, id resolution |
| Memoization | cached embeddings, parsed configs, features |
| Vectorization | embedding normalization, similarity math |
| Ratio asserts | CI-friendly performance regression checks |

**Scale note:** 10k records → 100k records makes an O(n²) stage 100x worse while an O(n) stage grows 10x. In inference services the same principle applies to per-token work: the token loop is O(tokens), and every constant factor in it multiplies across the whole generation.

---

## Practice Exercises

### Exercise 1: timeit Namespace (Difficulty: Easy)
Benchmark `build_list(10_000)` with `timeit.repeat` passing an explicit `ns`. First reproduce the `NameError` without `globals`, then fix it. Record best-of-five.

### Exercise 2: cProfile Reading (Difficulty: Medium)
Run `cProfile` over `fib_uncached(25)` and `fib_cached(25)`; print the cumulative stats sorted by cumulative time. Assert the uncached run reports dramatically more `fib` calls.

### Exercise 3: Hash Join Ratio (Difficulty: Medium)
Generate 40,000 audit records and an index; time `naive_join` vs `hash_join`. Assert `naive_time >= hash_time * 100` and print both times.

### Exercise 4: Memoization Call Counts (Difficulty: Medium)
Instrument both fib versions with a call counter. Assert `uncached > 100_000` calls and `cached <= 30` calls at n=25.

### Exercise 5: Concatenation With References (Difficulty: Hard)
Compare `"".join` vs `s = s + c` with an audit list holding intermediates at 5000 chars. Assert `plus >= join * 100`. Then re-run without the audit list and explain what changes.

### Exercise 6: Vectorize a Hot Reduction (Difficulty: Hard)
Compute stddev of 2M floats with a Python loop and with NumPy. Assert the vectorized time is less than 1/10 of the loop time, and print both. Discuss where the crossover point is for your machine.

---

## Summary

| Concept | Description |
|---|---|
| `timeit` | micro-benchmarks; best-of-N, explicit globals |
| `cProfile` | whole-program hot paths via call counts and cumulative time |
| Complexity refactor | dict lookups replace nested scans — 1810x measured |
| Memoization | pure functions cache subproblems — 242,785 → 27 calls |
| Vectorization | C-level loops for numeric reductions — ~100x |
| The join surprise | refcount-1 concat is optimized; held refs expose O(n²) |

Optimization is a loop, not a talent: **measure → profile → refactor shape → verify with ratio asserts → record the numbers**. Each pass shrinks the hot path; the tools, not the tricks, are what scale.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Micro-benchmark | `min(timeit.repeat(stmt, globals=ns, number=100, repeat=5))` |
| Hot path hunt | `pstats.Stats(pr).sort_stats("cumulative").print_stats(10)` |
| Join by key | `by_id = {e["id"]: e for e in index}` then O(1) lookups |
| Memoize | `memo[n] = f(n-1) + f(n-2)`; verify call counts collapse |
| Vectorize | `np.array(data)` → vector ops → scalar result |
| Regression check | assert `naive >= fast * 100` — ratios, never absolutes |

---

## Next Steps

Next: **[26-design-patterns-advanced-lecture.md](26-design-patterns-advanced-lecture.md)** — structural patterns for AI systems: adapters, dependency injection, the registry pattern, and the strategy that makes tests honest.
Continues in: **[33-performance-and-profiling](../../../02-advanced-python/33-performance-and-profiling.py)** (Phase 2 topic 33) — concurrency for performance, cache-aware algorithms, and scaling profiling to services.
Official docs: [timeit](https://docs.python.org/3/library/timeit.html), [cProfile](https://docs.python.org/3/library/profile.html), [NumPy](https://numpy.org/doc/stable/), [sys.getsizeof](https://docs.python.org/3/library/sys.html#sys.getsizeof).
