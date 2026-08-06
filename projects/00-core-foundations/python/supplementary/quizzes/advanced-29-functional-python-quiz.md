# Functional Python Quiz

## Topic Overview
This quiz covers functional Python: pure functions and referential
transparency, frozen dataclasses, map/filter/reduce, the operator
module, partial application and currying, composition, itertools,
recursion limits, and the functional-core/imperative-shell architecture.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer

---

## Questions

### Question 1
**Which of these functions is pure?**

A) `def f(x): print(x); return x`
B) `def f(x): return x + random.random()`
C) `def f(x): return x * 2`
D) `def f(x): cache[x] = x; return x`

**Difficulty:** Easy

---

### Question 2
**What is referential transparency?**

A) The ability to see a function's source code
B) The property that any expression can be replaced by its value without changing the program
C) Returning a reference to the caller's object
D) Making all variables global

**Difficulty:** Easy

---

### Question 3
**What is the output of this code?**
```python
import functools

calls = {"n": 0}

@functools.lru_cache(maxsize=None)
def square(x):
    calls["n"] += 1
    return x * x

square(4)
square(4)
print(calls["n"])
```

A) 2
B) 1
C) 0
D) 4

**Difficulty:** Easy

---

### Question 4
**What is the output of this code?**
```python
nums = [1, 2, 3, 4, 5, 6]
result = list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, nums)))
print(result)
```

A) `[2, 4, 6, 8, 10, 12]`
B) `[4, 8, 12]`
C) `[2, 4, 6]`
D) `[1, 2, 3, 4, 5, 6]`

**Difficulty:** Easy

---

### Question 5
**Why must `itertools.groupby` receive sorted input?**

A) It sorts internally, which is slow
B) It only groups *adjacent* equal keys, so unsorted data splits one key into many groups
C) It requires the key function to be pure
D) It can only handle strings

**Difficulty:** Medium

---

### Question 6
**What is the output of this code?**
```python
import itertools

pairs = [("en", 1), ("fr", 3), ("en", 2)]
print(len(list(itertools.groupby(pairs, key=lambda p: p[0]))))
```

A) 1
B) 2
C) 3
D) 4

**Difficulty:** Medium

---

### Question 7
**What is the output of this code?**
```python
def compose(g, f):
    def composed(x):
        return g(f(x))
    return composed

def double(x): return x * 2
def increment(x): return x + 1

print(compose(double, increment)(3))
```

A) 7
B) 8
C) 9
D) 10

**Difficulty:** Medium

---

### Question 8
**What does `functools.partial(fetch, 50)` produce?**

A) A new function that ignores the first argument
B) A new function with 50 pre-bound as the first argument
C) A list of 50 fetched items
D) A closure over the number 50 that raises on call

**Difficulty:** Easy

---

### Question 9
**What is the output of this code?**
```python
import operator

rows = [("b", 2), ("a", 3), ("c", 1)]
print(sorted(rows, key=operator.itemgetter(1)))
```

A) `[('a', 3), ('b', 2), ('c', 1)]`
B) `[('c', 1), ('b', 2), ('a', 3)]`
C) `[('b', 2), ('a', 3), ('c', 1)]`
D) `[('c', 1), ('a', 3), ('b', 2)]`

**Difficulty:** Medium

---

### Question 10
**What happens when you assign to an attribute of a frozen dataclass?**

A) It silently succeeds
B) `FrozenInstanceError` (a subclass of `AttributeError`) is raised
C) The whole object is copied and the copy is mutated
D) The attribute is ignored at runtime but kept by the type checker

**Difficulty:** Medium

---

### Question 11
**What is the output of this code?**
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Chunk:
    doc_id: int
    text: str

c = Chunk(1, "hello")
d = Chunk(1, "hello")
print(c == d, hash(c) == hash(d))
```

A) `False False`
B) `True False`
C) `True True`
D) `False True`

**Difficulty:** Medium

---

### Question 12
**Why does `factorial_rec(10_000)` fail while an iterative version succeeds?**

A) 10000 exceeds the recursion limit (~1000); CPython has no tail-call optimization
B) Factorial overflows the integer type
C) The recursive version is O(n^2)
D) `10_000` is not a valid argument

**Difficulty:** Medium

---

### Question 13
**What is the output of this code?**
```python
import functools

def scale(x, factor):
    return x * factor

halve = functools.partial(scale, factor=0.5)
print(halve(10))
```

A) `0.5`
B) `5.0`
C) `10`
D) `10.5`

**Difficulty:** Easy

---

### Question 14
**Which architecture is the "functional core, imperative shell"?**

A) All logic and I/O in one function for simplicity
B) Pure transforms inside; files/network/logging at the edges
C) A class hierarchy where every method has a side effect
D) A global state dict shared by every function

**Difficulty:** Medium

---

### Question 15
**What is the output of this code?**
```python
import functools
import operator

print(functools.reduce(operator.add, [1, 2, 3, 4]))
```

A) `[1, 2, 3, 4]`
B) `24`
C) `10`
D) `4`

**Difficulty:** Easy

---

### Question 16
**Which is the best rewrite of `sorted(rows, key=lambda r: r[1])`?**

A) `sorted(rows, key=operator.itemgetter(1))`
B) `sorted(rows, key=operator.attrgetter(1))`
C) `sorted(rows, key=rows[1])`
D) `sorted(rows, key=1)`

**Difficulty:** Medium

---

### Question 17
**What is the output of this code?**
```python
def add(a, b):
    return a + b

curried = lambda b: add(5, b)
print(curried(3))
```

A) `5`
B) `3`
C) `8`
D) `15`

**Difficulty:** Medium

---

### Question 18
**Why is memoizing an impure function dangerous?**

A) The cache grows without bound
B) The cache returns stale results for inputs whose world state changed
C) lru_cache crashes on impure functions
D) It makes the function slower

**Difficulty:** Medium

---

### Question 19
**What is the output of this code?**
```python
def transform(s):
    return s.strip().lower()

print(transform(transform("  Hi  ")))
```

A) `"  hi  "`
B) `"hi"`
C) `"HI"`
D) `"Hi"`

**Difficulty:** Hard

---

### Question 20
**A preprocessing pipeline mutates its input list in place. Which failure
class does this create that a pure pipeline never has?**

A) It is 2x slower than the pure version
B) A stage's output depends on which other stages ran before it (ordering bugs that are silent)
C) The input list becomes immutable
D) The linter rejects the file

**Difficulty:** Hard

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! You think in pure functions.
- 14-17: Good! Review purity and composition details.
- 10-13: Fair. Re-read the key concepts sections.
- Below 10: Revisit the lecture and exercise before continuing.

---

## Answer Key

1. **C) `def f(x): return x * 2`** — no side effects, no hidden state,
   deterministic. A prints (side effect), B uses randomness
   (non-deterministic), D writes a cache (side effect).

2. **B) The property that any expression can be replaced by its value**
   — this is what licenses caching and reordering. A describes reading
   source, C is about object references, D is the opposite of the
   discipline.

3. **B) 1** — the second `square(4)` is a cache hit; the function body
   runs once. A (2) assumes no caching, C (0) assumes the call never
   runs, D (4) counts arguments, not calls.

4. **B) `[4, 8, 12]`** — filter keeps evens [2,4,6], map doubles them.
   A doubles everything without filtering, C keeps odds doubled wrongly,
   D is the untouched input.

5. **B) It only groups *adjacent* equal keys** — `groupby` never looks
   back; it emits a new group whenever the key changes. A is false (it
   does not sort), C and D are irrelevant constraints.

6. **C) 3** — `en`, `fr`, `en` are three runs because the second `en`
   is not adjacent to the first. A (1) assumes sorting happened, B (2)
   merges the two `en` groups, D (4) overcounts.

7. **B) 8** — `compose(double, increment)(3)` = `double(increment(3))`
   = `double(4)` = 8. A (7) computes `increment(double(3))`, C (9)
   computes `double(3)+increment(3)`, D (10) doubles after adding 2.

8. **B) A new function with 50 pre-bound as the first argument** —
   `page_50(offset=0, limit=200)` calls `fetch(50, 0, 200)`. A describes
   a different wrapper, C confuses a function with its result, D is
   nonsensical.

9. **B) `[('c', 1), ('b', 2), ('a', 3)]`** — `itemgetter(1)` sorts by
   the second element ascending. A sorts by the first element, C is the
   input order, D is not sorted by either field.

10. **B) `FrozenInstanceError` (a subclass of `AttributeError`)** —
    frozen dataclasses raise on write. A is wrong (it raises), C is a
    copy-on-write pattern that frozen does not implement, D is false
    (the error is raised at runtime).

11. **C) `True True`** — frozen dataclasses generate value-based `__eq__`
    and `__hash__` over the fields, so equal instances have equal
    hashes. A would be true for identity-hashed objects, B breaks the
    hash/eq contract (equal objects must hash equal), D is impossible
    for value-hashed objects.

12. **A) 10000 exceeds the recursion limit (~1000); no TCO** — each call
    pushes a frame; CPython never reuses it. B is false (Python ints
    are arbitrary precision), C is false (the recursion is O(n)
    depth/time), D is false (10_000 is a fine integer).

13. **B) `5.0`** — `halve(10)` = `scale(10, factor=0.5)` = `10 * 0.5`.
    A (0.5) prints the factor, C (10) ignores the factor, D (10.5) adds.

14. **B) Pure transforms inside; files/network/logging at the edges** —
    the core is testable and cacheable; the shell owns I/O. A merges
    them (unreadable), C is the opposite (impure everywhere), D is the
    global-state anti-pattern.

15. **C) `10`** — `operator.add` folds left: 1+2=3, +3=6, +4=10. A is
    the input, B is the product (24), D is the last element.

16. **A) `sorted(rows, key=operator.itemgetter(1))`** — itemgetter
    extracts by index. B extracts by attribute name (wrong for index
    access on tuples), C passes a list as key (unhashable, crashes),
    D is not a callable.

17. **C) `8`** — `curried(3)` = `add(5, 3)` = 8. A (5) prints only the
    bound argument, B (3) prints only the passed argument, D (15)
    multiplies instead of adding.

18. **B) The cache returns stale results for inputs whose world state
    changed** — the cache stores the *old* answer keyed by arguments
    that no longer imply it. A is a size concern, not the danger; C is
    false (it works, wrongly); D is false (it is faster, which is the
    trap).

19. **B) `"hi"`** — pure transforms compose: `strip().lower()` applied
    twice is idempotent, so `"  Hi  "` → `"hi"` → `"hi"`. A keeps the
    spaces (first call never stripped), C uppercases (wrong order), D
    keeps case (partial normalization).

20. **B) A stage's output depends on which other stages ran before it
    (silent ordering bugs)** — mutation creates hidden coupling between
    stages; pure pipelines are reorder-safe by construction. A is a
    micro-perf claim, C is false (mutation makes it *more* mutable),
    D is false (linters do not catch this).
