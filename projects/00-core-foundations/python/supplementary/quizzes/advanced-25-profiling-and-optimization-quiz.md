# Profiling and Optimization Quiz

## Topic Overview
This quiz covers measurement-first discipline: `timeit` best-of-N,
`cProfile` and the tottime/cumulative split, complexity refactors
(hash joins, memoization), vectorization, and ratio-based performance
assertions.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer

---

## Questions

### Question 1
**What does the `cumulative` column in `pstats` show?**

A) A function's own time, excluding callees
B) A function's time including everything it calls
C) The number of times the function was called
D) The function's memory usage

**Difficulty:** Easy

---

### Question 2
**Which of these is the highest-leverage optimization?**

A) Micro-tuning a hot loop
B) Changing an O(n²) algorithm to O(n)
C) Inlining a helper function
D) Caching a frequently used local variable

**Difficulty:** Easy

---

### Question 3
**What is the output of this code?**
```python
import timeit

ns = {"n": 10_000}
print(round(min(timeit.repeat("list(range(n))", globals=ns, number=100, repeat=3)), 5))
```

A) A small positive float — the best-of-3 run
B) `0.0` — timeit prints nothing
C) `NameError` — `n` is not defined
D) `100` — the number of repetitions

**Difficulty:** Easy

---

### Question 4
**Why does `timeit.repeat("my_func()")` fail without `globals=...`?**

A) `timeit` runs in a sandbox without imports
B) The statement string cannot see enclosing-scope variables
C) `timeit` requires a module name
D) It only fails on Windows

**Difficulty:** Easy

---

### Question 5
**What does `tottime` exclude?**

A) The function's own statements
B) Time spent in functions the profiled function calls
C) I/O waits
D) The profiler's own overhead

**Difficulty:** Easy

---

### Question 6
**Why are performance tests written as ratio assertions (`naive >= fast * 100`) rather than absolute seconds?**

A) Ratios are easier to type
B) Absolute timings vary by machine; the shape does not
C) Absolute assertions always pass
D) Ratios make the code faster

**Difficulty:** Easy

---

### Question 7
**What is the output of this code?**
```python
def dedup(items):
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out

print(dedup(["a", "b", "a", "c"]))
```

A) `['a', 'b', 'a', 'c']`
B) `['a', 'b', 'c']`
C) `{'a', 'b', 'c'}`
D) `['b', 'c']`

**Difficulty:** Medium

---

### Question 8
**A nested-scan join is O(n²). The dict-based replacement is:**

A) O(n log n) — sorting the dict
B) O(n) — one build, O(1) lookups
C) O(n²) — the dict still scans
D) O(1) — free

**Difficulty:** Medium

---

### Question 9
**What is the call-count signature of exponential recursion (e.g. naive fib(25))?**

A) ~25 calls — one per level
B) ~242,000 calls — the exponential explosion
C) ~50 calls — two per level
D) 1 call — the root only

**Difficulty:** Medium

---

### Question 10
**What is the output of this code?**
```python
memo = {}

def fib(n):
    if n in memo:
        return memo[n]
    if n < 2:
        return n
    memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]

print(fib(10), len(memo))
```

A) `55 9`
B) `55 11`
C) `55 10`
D) `55 2`

**Difficulty:** Medium

---

### Question 11
**Which workload is the strongest candidate for vectorization with NumPy?**

A) Parsing 100 JSON files
B) Normalizing a 2M-element embedding array
C) Reading a CSV with 10 rows
D) Building a string from 5 parts

**Difficulty:** Medium

---

### Question 12
**What is the output of this code?**
```python
import numpy as np

v = np.array([1.0, 2.0, 3.0])
print(v * 2, v.sum())
```

A) `[2. 4. 6.] 6.0`
B) `[1. 2. 3.] 6.0`
C) `[2. 4. 6.] 12.0`
D) `2.0 6.0`

**Difficulty:** Medium

---

### Question 13
**`s = s + "c"` in a loop can appear linear on CPython because:**

A) Strings are mutable there
B) Refcount-1 concat resizes the buffer in place
C) The loop is compiled by a JIT
D) `str.__add__` always returns the same object

**Difficulty:** Medium

---

### Question 14
**Why does holding intermediate strings in a list expose the quadratic cost of `s = s + c`?**

A) The list duplicates memory, slowing the CPU
B) Extra references force real copies — the in-place optimization stops applying
C) The list triggers garbage collection constantly
D) It changes the algorithm to O(n³)

**Difficulty:** Medium

---

### Question 15
**Which is the correct first step of the optimization workflow?**

A) Rewrite the algorithm from scratch
B) Run `cProfile` and read the cumulative/tottime columns
C) Add `time.time()` prints everywhere
D) Rewrite the hot function in C

**Difficulty:** Medium

---

### Question 16
**What is the output of this code?**
```python
records = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}]
index = [{"id": 2, "text": "B"}, {"id": 1, "text": "A"}]

by_id = {e["id"]: e["text"] for e in index}
print([(r["id"], by_id[r["id"]]) for r in records])
```

A) `[(1, 'A'), (2, 'B')]`
B) `[(2, 'B'), (1, 'A')]`
C) `[(1, 'B'), (2, 'A')]`
D) `[(1, 'a'), (2, 'b')]`

**Difficulty:** Medium

---

### Question 17
**A 2M-element numeric reduction runs ~100x slower in a pure-Python loop than NumPy. Why?**

A) NumPy compiles the whole program
B) The C-level loop avoids per-element interpreter overhead
C) Python's loops are O(n²)
D) NumPy runs on the GPU by default

**Difficulty:** Hard

---

### Question 18
**At what array size does vectorization typically stop paying off?**

A) Below ~10k elements — conversion overhead dominates
B) Below 1 billion — never
C) Above 1M — Python is faster
D) Exactly 100k — the crossover is fixed

**Difficulty:** Hard

---

### Question 19
**What is the output of this code?**
```python
def naive(n):
    total = 0
    for i in range(n):
        total += i
    return total

def fast(n):
    return n * (n - 1) // 2

print(naive(10_000) == fast(10_000), fast(5))
```

A) `True 10`
B) `True 10.0`
C) `True 9`
D) `False 10`

**Difficulty:** Hard

---

### Question 20
**Which statement about profiling overhead is TRUE?**

A) `cProfile` records every call; overhead is real but acceptable for analysis
B) Profiling changes nothing — it is free
C) Profiling must never be used in CI
D) `timeit` measures whole-program hot paths

**Difficulty:** Hard

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! Measurement is your reflex.
- 14-17: Good! Review the complexity questions.
- 10-13: Fair. Re-read the hash join and memoization sections.
- Below 10: Revisit the lecture and the exercise before continuing.

---

## Answer Key

1. **B) A function's time including everything it calls** — the
   top-down cost view. A is `tottime`, C is the call-count column, D
   is memory.

2. **B) Changing an O(n²) algorithm to O(n)** — the complexity class
   dominates every constant factor. A, C, D tune constants.

3. **A) A small positive float — the best-of-3 run** — `min` of
   repeats is the measured estimate. B is false (timeit returns a
   number), C would happen without `globals`, D is the repetitions,
   not the time.

4. **B) The statement string cannot see enclosing-scope variables** —
   the namespace trap. A is false (imports work inside), C and D are
   false.

5. **B) Time spent in functions the profiled function calls** —
   tottime is leaf cost. A is what tottime includes, C and D are
   false.

6. **B) Absolute timings vary by machine; the shape does not** —
   ratios are the flake-free contract. A, C, D are false.

7. **B) `['a', 'b', 'c']`** — first-occurrence dedup with a set. A
   keeps duplicates, C is the set (unordered), D drops the first
   items.

8. **B) O(n) — one build, O(1) lookups** — the hash join. A adds a
   sort that is not needed, C is the naive behavior, D is fantasy.

9. **B) ~242,000 calls — the exponential explosion** — the profiler's
   smoking gun for fib(25). A and C are linear thinking, D is false.

10. **B) `55 11`** — memo keys 0..10 are stored, 11 entries. A
    miscounts, C and D undercount the cache.

11. **B) Normalizing a 2M-element embedding array** — numeric
    reduction at scale. A and C are I/O/parsing, D is tiny.

12. **A) `[2. 4. 6.] 6.0`** — element-wise multiply, then the sum.
    B shows the input, C doubles the sum, D drops array notation.

13. **B) Refcount-1 concat resizes the buffer in place** — the
    CPython optimization. A is false (strings are immutable), C and
    D are false.

14. **B) Extra references force real copies — the in-place
    optimization stops applying** — held refs raise the refcount. A
    is a side effect, not the cause, C and D are false.

15. **B) Run `cProfile` and read the cumulative/tottime columns** —
    measure first, optimize where the profiler points. A is
    premature, C is guesswork with prints, D skips measurement.

16. **A) `[(1, 'A'), (2, 'B')]`** — records keep their order; the
    dict resolves each id. B is index order, C mixes pairs, D reads
    the record's own value.

17. **B) The C-level loop avoids per-element interpreter overhead** —
    the whole reason vectorization wins. A and D are false, C is
    false.

18. **A) Below ~10k elements — conversion overhead dominates** — the
    crossover reality. B and C are wrong, D invents a fixed point.

19. **A) `True 10`** — the closed form matches the loop; `5*4//2 =
    10`. B shows a float, C miscounts, D claims inequality wrongly.

20. **A) `cProfile` records every call; overhead is real but
    acceptable for analysis** — profiling is instrumentation, not
    magic. B is false, C is false (CI profiling is standard), D
    confuses `timeit` with `cProfile`.
