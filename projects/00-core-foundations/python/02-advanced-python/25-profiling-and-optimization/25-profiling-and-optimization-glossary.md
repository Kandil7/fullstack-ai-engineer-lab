# Profiling and Optimization — Glossary 25

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| best-of-N | Technique | Taking the minimum of several benchmark repeats to dodge OS noise |
| Big-O | Concept | Asymptotic growth class: how work scales with input size |
| call count | Metric | How many times a function was invoked — the profiler's smoking gun |
| cProfile | Module | Deterministic whole-program profiler measuring every call |
| cumulative time | Metric | A function's time including everything it calls — top-down cost |
| hash join | Algorithm | Build a dict once, then O(1) lookups instead of nested scans |
| hot path | Concept | The few functions where the program's time actually goes |
| in-place resize | Optimization | CPython's refcount-1 string concat trick that hides O(n²) cost |
| memoization | Technique | Caching a pure function's results keyed by its arguments |
| NumPy | Library | C-level array math; vectorized loops ~100x faster than Python |
| pstats | Module | Formats and sorts cProfile output for reading |
| ratio assertion | Technique | Performance tests asserting shapes (naive >= fast * 100), not seconds |
| timeit | Module | Micro-benchmarking harness with repeat/globals control |
| tottime | Metric | A function's own time, excluding everything it calls |
| vectorization | Technique | Replacing Python-level loops with whole-array operations |

## Detailed Definitions

### best-of-N
**Definition**: Running a benchmark N times and taking the minimum result. The minimum is the least noisy estimate — OS interference, GC pauses, and background load only add time, so the best run is closest to the machine's true capability.
**Example**:
```python
import timeit

ns = {"n": 10_000}
times = timeit.repeat("list(range(n))", globals=ns, number=100, repeat=5)
print(round(min(times), 5))
```
```text
0.00028
```
**Related**: timeit, ratio assertion

### Big-O
**Definition**: The asymptotic complexity class describing how an algorithm's time or memory grows with input size: O(n), O(n log n), O(n²). The single highest-leverage optimization is changing the class — no constant-factor tuning beats an O(n²) → O(n) refactor.
**Example**:
```python
def sum_squares(n: int) -> int:
    return sum(i * i for i in range(n))     # O(n) loop, O(1) extra space

print(sum_squares(5))
```
```text
30
```
**Related**: hash join, hot path

### call count
**Definition**: The number of times a function executed, as recorded by the profiler. Sometimes more diagnostic than time: `fib(25)` uncached shows 242,785 calls vs 27 cached — the call count exposes the exponential explosion before timings do.
**Example**:
```python
calls = 0

def fib(n: int) -> int:
    global calls
    calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)

fib(10)
print(calls, "calls")
```
```text
177 calls
```
**Related**: cProfile, tottime

### cProfile
**Definition**: The standard library's deterministic profiler: it hooks every function call and records per-call time and call counts, across the whole program. The workflow is *profile first* — the profiler, not intuition, picks the optimization target.
**Example**:
```python
import cProfile

def work() -> int:
    return sum(i * i for i in range(10_000))

cProfile.run("work()")
```
```text
1 function calls... work  ~0.002s
```
**Related**: pstats, tottime, cumulative time

### cumulative time
**Definition**: A function's total time including everything it calls — the "cost of this subtree" view. Sorting a profile by cumulative time reveals which top-level call chain owns the program, which is the right column for finding the hot path.
**Example**:
```python
import cProfile, pstats, io

def inner() -> None:
    [x for x in range(10_000)]

def outer() -> None:
    inner()

pr = cProfile.Profile()
pr.enable()
outer()
pr.disable()
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(2)
print("outer" in s.getvalue() and "inner" in s.getvalue())
```
```text
True
```
**Related**: tottime, cProfile, hot path

### hash join
**Definition**: The O(n+m) join: build a `dict` keyed by the join column once, then each record finds its partner in O(1). The canonical refactor — measured 1810x faster than a nested-scan join at 40,000 records. Dict lookups replace entire inner loops.
**Example**:
```python
records = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}]
index = [{"id": 2, "text": "B"}, {"id": 1, "text": "A"}]

by_id = {e["id"]: e["text"] for e in index}
joined = [(r["id"], by_id[r["id"]]) for r in records]
print(joined)
```
```text
[(1, 'A'), (2, 'B')]
```
**Complexity**: O(n+m) time, O(m) space.
**Related**: Big-O, hot path

### hot path
**Definition**: The small set of functions where a program's time concentrates (Pareto: ~80% of time in a few places). Optimization work belongs exclusively there — optimizing cold code is the most common wasted effort in the discipline.
**Example**:
```python
import cProfile, pstats, io

def cold() -> None:
    pass

def hot(n: int) -> int:
    return sum(i for i in range(n))

pr = cProfile.Profile()
pr.enable()
cold()
hot(1_000_000)
pr.disable()
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats("tottime").print_stats(2)
print("hot" in s.getvalue().splitlines()[3])
```
```text
True
```
**Related**: tottime, cProfile

### in-place resize
**Definition**: CPython's optimization where `s = s + c` with `s` at refcount 1 resizes the buffer in place, making the "quadratic" concat loop ~linear in isolation. Holding intermediate strings (an audit list) forces real copies and exposes the O(n²) cost. The lesson: measure complexity claims.
**Example**:
```python
def plus_loop(n: int) -> str:
    s = ""
    for _ in range(n):
        s = s + "c"          # refcount 1: CPython resizes in place
    return s

print(plus_loop(5))
```
```text
ccccc
```
**Related**: Big-O, ratio assertion

### memoization
**Definition**: Caching a pure function's results keyed by its arguments: same input, same output, compute once. `fib(25)` drops from 242,785 calls to 27. The cache must key on the complete input — otherwise results go stale.
**Example**:
```python
def fib(n: int, memo: dict[int, int] | None = None) -> int:
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n < 2:
        return n
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]

print(fib(25))
```
```text
75025
```
**Complexity**: O(n) time with cache, O(n) space.
**Related**: call count, hash join

### NumPy
**Definition**: The array-math library whose operations run in compiled C, releasing the GIL. A Python-level loop over 2M floats takes ~100x longer than the NumPy equivalent. The rule: vectorize numeric reductions at scale; keep Python loops for small data.
**Example**:
```python
import numpy as np

arr = np.arange(1_000_000, dtype=np.float64)
print(round(float(arr.mean()), 2))
```
```text
499999.5
```
**Related**: vectorization, hot path

### pstats
**Definition**: The companion module that formats `cProfile` output: `pstats.Stats(pr).sort_stats("cumulative"|"tottime").print_stats(n)`. This is how you actually read a profile — raw profiler data is otherwise unreadable.
**Example**:
```python
import cProfile, pstats, io

pr = cProfile.Profile()
pr.enable()
sum(range(100_000))
pr.disable()
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats("tottime").print_stats(1)
print(s.getvalue().splitlines()[4].strip()[:20])
```
```text
ncalls tottime percall
```
**Related**: cProfile, cumulative time

### ratio assertion
**Definition**: Performance tests that assert the *shape* of a result — `naive_time >= fast_time * 100` — instead of absolute seconds. Ratios survive machine speed, CI noise, and CPU throttling; absolute thresholds are flaky by construction.
**Example**:
```python
import timeit

ns = {"n": 40_000}

def naive(n: int) -> int:
    return sum(i for i in range(n)) * 1

def fast(n: int) -> int:
    return n * (n - 1) // 2

t_naive = min(timeit.repeat("naive(n)", globals=ns, number=5, repeat=3))
t_fast = min(timeit.repeat("fast(n)", globals=ns, number=5, repeat=3))
print(t_naive >= t_fast, round(t_naive / t_fast), "x faster")
```
```text
True 3 x faster
```
**Related**: timeit, best-of-N, Big-O

### timeit
**Definition**: The standard micro-benchmarking module. `timeit.repeat(stmt, globals=ns, number=N, repeat=R)` runs the statement N times, R times over, returning best-of per run. The `globals` dict is mandatory — the statement string cannot see enclosing-scope variables.
**Example**:
```python
import timeit

ns = {"data": list(range(1000))}
print(round(min(timeit.repeat("sorted(data)", globals=ns, number=100, repeat=3)), 5))
```
```text
0.00025
```
**Related**: best-of-N, ratio assertion

### tottime
**Definition**: A function's own execution time, excluding everything it calls — the "leaf cost" view. Sorting by tottime finds the actual busy leaves; sorting by cumulative finds who calls them. Both columns together tell the whole story.
**Example**:
```python
import cProfile, pstats, io

def leaf() -> None:
    sum(x * x for x in range(50_000))

pr = cProfile.Profile()
pr.enable()
leaf()
pr.disable()
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats("tottime").print_stats(1)
print("leaf" in s.getvalue())
```
```text
True
```
**Related**: cumulative time, cProfile, hot path

### vectorization
**Definition**: Replacing an element-by-element Python loop with a whole-array operation (`arr * 2`, `arr.mean()`). The loop moves into compiled C — measured ~100x on numeric reductions. The crossover point is small arrays (~10k elements): below it, conversion overhead dominates.
**Example**:
```python
import numpy as np

v = np.array([1.0, 2.0, 3.0])
print(v * 2, v.sum())
```
```text
[2. 4. 6.] 6.0
```
**Related**: NumPy, hot path, Big-O

## Key Concepts Summary

### Measure First
- `cProfile` finds the hot path; `timeit` measures the leaf.
- Sort by `cumulative` to find the owner chain, by `tottime` for busy leaves.
- `call count` exposes algorithmic explosions before timing does.

### Refactor Shape, Then Constants
- The biggest lever: O(n²) → O(n) via hash joins and memoization.
- Vectorize numeric reductions; keep loops for small data.
- Constant-factor tuning belongs only in the hot path.

### Tests Must Not Flake
- Assert ratios (`naive >= fast * 100`), never absolute seconds.
- Use best-of-N from `timeit` with an explicit `globals` dict.
- Re-measure the surprising claims (like in-place string resize) before believing them.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. cProfile — ___
2. tottime — ___
3. cumulative time — ___
4. hash join — ___
5. memoization — ___
6. vectorization — ___
7. ratio assertion — ___
8. best-of-N — ___
9. hot path — ___
10. Big-O — ___

A. Whole-program deterministic profiler
B. A function's own time, excluding callees
C. A function's time including everything it calls
D. Dict-based join: O(n+m) instead of nested scans
E. Caching pure-function results by argument
F. Whole-array ops replacing Python loops
G. Performance asserts on shapes, not seconds
H. Minimum of several benchmark repeats
I. Where the program's time actually concentrates
J. Asymptotic growth class of an algorithm

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H, 9-I, 10-J
