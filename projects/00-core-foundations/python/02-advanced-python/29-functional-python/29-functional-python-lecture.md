# Advanced Python — 29: Functional Python

## Topic Overview

Functional programming is a discipline, not a library: write functions
that compute, and keep the side effects at the edges. A **pure function**
returns the same value for the same arguments and does nothing else —
no file writes, no counter increments, no hidden caches. Python is not
Haskell; it will not enforce purity. But you can *choose* it, and the
choice pays off exactly where ML engineering hurts most: preprocessing
pipelines that must be reproducible, testable, and cacheable.

The tools are already in the standard library: `map`/`filter`/`reduce`,
the `operator` module, `functools.partial` and `functools.lru_cache`,
`itertools` for lazy composition, and `@dataclass(frozen=True)` for
immutable data. This lecture teaches the vocabulary (pure functions,
referential transparency, currying, composition), the traps (recursion
limits, `groupby` sorting, hidden state), and the architecture that
makes it all useful: a functional core wrapped in an imperative shell.

Where this fits: topic 28 gave you the tooling to *check* code; this
topic gives you the design that needs fewer checks. Topics 24 (memory)
and 29 are siblings — immutability is the cheapest memory-safety
guarantee you will ever get.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define purity and referential transparency and spot violations
2. Write frozen dataclasses and explain why immutability enables hashing and sharing
3. Choose between `map`/`filter`/`reduce` and comprehensions by readability
4. Use the `operator` module to replace trivial lambdas
5. Apply `functools.partial` for configuration and build curried functions
6. Compose functions and verify associativity
7. Use `itertools` lazily and avoid the `groupby` unsorted trap
8. Explain Python's recursion limit and why tail calls are absent
9. Structure code as functional core + imperative shell

## Prerequisites

| Need | Where |
|---|---|
| Functions as first-class objects | `01-decorators-lecture.md` |
| Dataclasses | `06-dataclasses-lecture.md` |
| `functools` (`partial`, `lru_cache`, `reduce`) | `09-functools-lecture.md` |
| `itertools` laziness and `groupby` | `10-itertools-lecture.md` |
| Tuples/hashability basics | `01-core-python` data structures |

---

## 1. Pure Functions and Referential Transparency

A function is **pure** when (a) the same arguments always produce the
same result, and (b) it has no observable side effects. **Referential
transparency** is the property that any expression `f(x)` can be
replaced by its value without changing the program.

```python
def pure_square(x: int) -> int:
    return x * x

calls = {"n": 0}

def impure_square(x: int) -> int:
    calls["n"] += 1          # side effect: hidden state
    return x * x

print(pure_square(3), pure_square(3))      # same, always
print(impure_square(3), calls["n"])        # result same, world changed
```

Output:

```text
9 9
9 1
```

Why purity matters in practice: a pure function can be **cached**
(`lru_cache`), **replayed** (rerun any pipeline stage), **parallelized**
(no shared state to corrupt), and **tested** (no fixtures for hidden
state). Impure code can do none of these safely.

---

## 2. Frozen Dataclasses: Immutability as a Guarantee

Immutability makes purity structural. A `@dataclass(frozen=True)` raises
`FrozenInstanceError` on any attribute write — the type system defends
the promise.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Chunk:
    doc_id: int
    text: str
    score: float

c = Chunk(doc_id=1, text="attention is all you need", score=0.9)
print(hash(c))                      # usable as dict key / set member
try:
    c.score = 0.5
except AttributeError as exc:
    print(type(exc).__name__)       # FrozenInstanceError (an AttributeError)
```

Output:

```text
<some int>
FrozenInstanceError
```

The payoff: frozen objects are hashable (fields are), shareable across
threads, and can never be observed mid-mutation. A `RetrievedChunk`
passed to a reranker cannot be changed by the reranker — the bug class
"function modified my input" disappears.

---

## 3. map/filter/reduce vs Comprehensions

`map(f, it)` applies a function lazily; `filter(pred, it)` keeps
matching items; `reduce(fn, it)` folds to a single value. Comprehensions
do the same job in a more readable shape. The rule: use `map`/`filter`
when the function already exists (no lambda), otherwise prefer the
comprehension.

```python
nums = [1, 2, 3, 4, 5, 6]
mapped = list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, nums)))
comprehended = [x * 2 for x in nums if x % 2 == 0]
print(mapped == comprehended)
```

Output:

```text
True
```

Both are O(n) time; `map`/`filter` are O(1) memory (lazy), the
comprehension is O(n) memory (eager). For a 10-million-row corpus the
difference is 80 MB — the lazy version streams.

---

## 4. The operator Module

`operator` turns operators into first-class functions: `operator.add`,
`operator.itemgetter(1)`, `operator.attrgetter("name")`,
`operator.methodcaller("upper")`. This removes lambdas from the
exact places where lambdas add noise.

```python
import functools
import operator

rows = [("b", 2), ("a", 3), ("c", 1)]
print(sorted(rows, key=operator.itemgetter(1)))
print(functools.reduce(operator.add, [1, 2, 3, 4]))
```

Output:

```text
[('c', 1), ('b', 2), ('a', 3)]
10
```

`itemgetter` is also faster than a lambda (C-implemented) — a
micro-benefit that compounds in hot sort paths.

---

## 5. Partial Application and Currying

`functools.partial` binds leading arguments, producing a new function.
Currying splits `f(a, b)` into `f(a)(b)`. Both are "configuration as
composition": you derive specialized functions from general ones without
touching the general one.

```python
import functools

def fetch(page_size: int, offset: int, limit: int) -> int:
    return min(limit - offset, page_size)

page_50 = functools.partial(fetch, 50)
print(page_50(offset=0, limit=200))
```

Output:

```text
50
```

In AI code this is how you build `embed = partial(embed_docs, batch=32)`
or `retriever = partial(search, k=5, filter={"lang": "en"})` — one
general function, many derived configurations, zero duplication.

---

## 6. Composition

Composition chains functions: `compose(g, f)(x) == g(f(x))`. It is
**associative** — `f∘(g∘h) == (f∘g)∘h` — which is the algebraic
guarantee that lets you refactor pipelines: regroup the parentheses
however you like, the result is identical.

```python
def compose(g, f):
    def composed(x):
        return g(f(x))
    return composed

def double(x: int) -> int:
    return x * 2

def increment(x: int) -> int:
    return x + 1

pipeline = compose(double, increment)
print(pipeline(3))   # (3 + 1) * 2
```

Output:

```text
8
```

Associativity is asserted in the exercise: `compose(f, compose(g, h))`
must equal `compose(compose(f, g), h)` for all inputs. That property is
why you can extract, reorder, and cache sub-chains of a real pipeline
without fear.

---

## 7. itertools: The Functional Toolkit

`itertools` is lazy composition: `chain`, `islice`, `takewhile`,
`starmap`, `product`, `tee`, `groupby`. The one trap: **`groupby` only
groups adjacent equal keys** — unsorted input silently produces multiple
groups for the same key.

```python
import itertools
import operator

pairs = [("en", 1), ("en", 2), ("fr", 3)]
for key, group in itertools.groupby(pairs, key=operator.itemgetter(0)):
    print(key, [item for _, item in group])

pairs_unsorted = [("en", 1), ("fr", 3), ("en", 2)]
print("unsorted groups:", len(list(itertools.groupby(pairs_unsorted))))
```

Output:

```text
en [1, 2]
fr [3]
unsorted groups: 3
```

The unsorted example produces three groups: `en`, `fr`, `en`. Every
groupby-based statistics bug I have seen in production traces to this.
Sort by the key first, always.

---

## 8. Recursion and Python's Limit

Python has no tail-call optimization: every call pushes a stack frame,
and the default limit is ~1000. Deep recursion raises `RecursionError`
deterministically — the stack is a memory structure, so recursion depth
is a memory cost: O(n) stack space.

```python
def factorial_rec(n: int) -> int:
    return 1 if n <= 1 else n * factorial_rec(n - 1)

try:
    factorial_rec(10_000)
except RecursionError as exc:
    print(type(exc).__name__)
```

Output:

```text
RecursionError
```

The iterative version is O(1) space and never fails. Functional
programming in Python therefore means *composition of shallow
functions*, not deep recursion. If you need recursion for a tree or a
graph, prefer an explicit stack (`collections.deque` / list) or
`functools` tricks — or reach for the data structure that fits (see
topic 30's protocols).

---

## 9. Production Pattern: Functional Core, Imperative Shell

The architecture that ships: a **pure core** (transforms, scoring,
ranking — no I/O) wrapped in an **imperative shell** (file reads,
network calls, user interaction, logging). The core is testable without
fixtures and cacheable wholesale; the shell is thin and deliberately
impure.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class TextSample:
    text: str
    label: str

def normalize(sample: TextSample) -> TextSample:
    return TextSample(text=sample.text.strip().lower(), label=sample.label)

def tokenize(text: str) -> tuple[str, ...]:
    return tuple(text.split())

def process_corpus(samples: list[TextSample]) -> dict[str, tuple[str, ...]]:
    """Functional core: pure, deterministic, cacheable."""
    return {s.label: tokenize(normalize(s).text) for s in samples}

raw = [TextSample(text="  Hello World ", label="greeting")]
print(process_corpus(raw))
```

Output:

```text
{'greeting': ('hello', 'world')}
```

The shell would read the files, call `process_corpus`, and write the
cache — but the core contains all the logic, and the core is what gets
unit-tested and memoized. Reproducible preprocessing is this pattern
plus a fixed seed (see topic 34).

---

## Common Mistakes to Avoid

### Mistake 1: Mutating inputs inside a "pure" transform
```python
# WRONG — caller's list changes under it
def scale(samples, factor):
    for s in samples:
        s.score *= factor

# CORRECT — new objects, inputs untouched (frozen forces this)
def scale(sample, factor):
    return Chunk(sample.doc_id, sample.text, sample.score * factor)
```

### Mistake 2: Relying on deep recursion
```python
# WRONG — RecursionError at ~1000 frames; no TCO in CPython
def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)

# CORRECT — iterate, or use functools.lru_cache only for SHALLOW depth
def fib_iter(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

### Mistake 3: groupby on unsorted input
```python
# WRONG — same key yields multiple groups
for k, g in itertools.groupby(items, key):
    ...

# CORRECT — sort by the key first, then group
items_sorted = sorted(items, key=key)
for k, g in itertools.groupby(items_sorted, key):
    ...
```

### Mistake 4: Lambdas where operator functions exist
```python
# WRONG — lambda noise on a hot sort path
sorted(rows, key=lambda r: r[1])

# CORRECT — C-implemented, faster, readable
sorted(rows, key=operator.itemgetter(1))
```

### Mistake 5: Mutable defaults as "cache"
```python
# WRONG — the default object is shared state across calls
def cache(store={}):
    ...

# CORRECT — explicit memoization with lru_cache (pure)
@functools.lru_cache(maxsize=128)
def compute(key):
    ...
```

### Mistake 6: Impure "pure" wrappers (hidden counters, prints)
```python
# WRONG — logging inside the core makes it untestable
def normalize(s): print("normalizing", s); return s.strip()

# CORRECT — pure core, log in the shell
def normalize(s): return s.strip()
```

## Best Practices

1. **Default to pure functions** — same inputs, same outputs, no side effects
2. **Frozen dataclasses for shared data** — `Chunk`, `Config`, `Sample`
3. **Comprehensions by default; map/filter when the function exists**
4. **`operator` over lambdas** for `itemgetter`/`attrgetter`/`add`
5. **`functools.partial` for configuration** — derive, don't duplicate
6. **Compose with `compose` and trust associativity**
7. **Sort before `groupby`** — every time, without exception
8. **Iterate, don't recurse** — Python has no tail-call optimization
9. **Isolate I/O in the shell** — the core must run anywhere, instantly
10. **Memoize the pure, never the impure** — `lru_cache` on I/O is a lie

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| `map`/`filter` (lazy) | O(n) | O(1) | comprehension (O(n) memory) |
| `reduce` | O(n) | O(1) | `sum`/`math.fsum` (C-speed) |
| `functools.partial` | O(1) | O(1) | — |
| `compose` wrapper | O(1)/call | O(depth) | flatten the chain |
| `lru_cache` hit | O(1) | O(maxsize) | `functools.cache` if unbounded OK |
| recursion depth n | O(n) | **O(n) stack** | iteration: O(1) |
| `groupby` (sorted) | O(n) | O(1) | — |
| frozen dataclass | O(fields) | O(fields) | slots=True for memory |

The cost model that matters: purity is free at runtime and saves
developer time — a cached pure transform costs one dict lookup instead
of a 200 ms embedding call, and a replayable pipeline costs nothing to
re-run. Recursion is the one place functional style genuinely costs
you: O(n) stack versus O(1) iteration.

## AI Engineering Relevance

**Where this shows up:** every preprocessing pipeline in the repo —
tokenization, chunking, normalization, embedding batching. The phase
doc's framing: *pure transforms make data pipelines testable and
cacheable; functional core keeps ML preprocessing reproducible.*

| Concept here | Used for |
|---|---|
| Pure transforms | chunk/normalize/embed stages that can be replayed and cached |
| Frozen dataclasses | `RetrievedChunk`/`TrainingSample` shared across stages |
| `functools.partial` | `embed = partial(embed_docs, batch=32)` configs |
| `lru_cache` on pure fns | embedding memoization — the cheapest cost cut available |
| `operator.itemgetter` | sorting candidates by score before top-k |
| Iteration over recursion | processing 10^7 tokens without stack death |
| Core/shell split | reproducible preprocessing: core + fixed seed |

**Scale note:** at 1M rows, an impure transform that mutates its input
corrupts every downstream stage and the bug is silent. At 100M rows, a
pure pipeline with memoized embedding calls is hours cheaper per run.
Functional style is not elegance — it is the difference between a
pipeline you can trust and one you must re-derive from scratch.

## Practice Exercises

### Exercise 1: Purity audit (Difficulty: Easy)
Classify each function as pure or impure and name the impurity:
`f(x): return x + 1`, `g(x): print(x); return x`, `h(x): return x + random()`,
`k(x): cache[x] = x; return x`.

### Exercise 2: operator over lambda (Difficulty: Easy)
Rewrite `sorted(records, key=lambda r: r["age"])` and
`reduce(lambda a, b: a + b, values)` using the `operator` module.

### Exercise 3: Partial config factory (Difficulty: Medium)
Write `make_embedder(provider, model)` returning a partial-ready function
`embed(batch) -> list[float]` without any I/O — the "configuration as
composition" pattern.

### Exercise 4: Associativity check (Difficulty: Medium)
Prove with three pure functions (`double`, `increment`, `negate`) that
`compose(compose(f, g), h)(5) == compose(f, compose(g, h))(5)`.

### Exercise 5: Cacheable stage (Difficulty: Hard)
Wrap a pure `normalize(sample) -> Chunk` in `functools.lru_cache`; then
build `process(list[Chunk]) -> dict` that reuses cached normalizations
and prove (with a call counter) that repeat runs compute zero
normalizations.

## Summary

| Concept | Description |
|---|---|
| Pure function | Same args, same result, no side effects |
| Referential transparency | `f(x)` can be replaced by its value anywhere |
| Frozen dataclass | Immutable, hashable, shareable data |
| map/filter/reduce | Lazy functional loops; comprehensions often read better |
| operator module | Operators as first-class functions |
| partial / currying | Configuration through function binding |
| Composition | `g(f(x))`; associative, so refactoring is safe |
| itertools | Lazy toolkit; `groupby` needs sorted input |
| Recursion limit | ~1000 frames; no TCO; iterate |
| Core/shell | Pure logic inside, I/O at the edges |

Functional Python is a discipline with a payoff: pipelines you can
cache, replay, and trust. You do not need to abandon OOP or write
point-free one-liners — you need the *core* pure and the *shell* thin.

## Quick Reference

| Task | Idiom |
|---|---|
| Immutable data | `@dataclass(frozen=True)` |
| Lazy transform | `map(f, items)` |
| Keep matches | `filter(pred, items)` |
| Fold to one value | `functools.reduce(operator.add, items)` |
| Sort by field | `sorted(rows, key=operator.itemgetter(1))` |
| Bind arguments | `functools.partial(fetch, 50)` |
| Chain functions | `compose(g, f)` → `g(f(x))` |
| Memoize pure fn | `@functools.lru_cache` |
| Group runs | `sorted(items, key=k)` then `groupby` |
| Deep iteration | `for` loop, explicit stack — never recursion |

## Next Steps

Next: **[30 — Iterators and Protocols Deep](30-iterators-protocols-deep-lecture.md)** —
the data-model dunder methods that make custom containers work with
`len()`, `in`, slicing, and hashing; frozen dataclasses from this topic
are the natural building blocks.

Continues in: **[Phase 7 — ML fundamentals](../../07-machine-learning/README.md)** —
reproducible preprocessing pipelines put the functional core to work.

Official docs:
- [functools — higher-order functions](https://docs.python.org/3/library/functools.html)
- [itertools — functions creating iterators](https://docs.python.org/3/library/itertools.html)
- [operator — standard operators as functions](https://docs.python.org/3/library/operator.html)
- [dataclasses](https://docs.python.org/3/library/dataclasses.html)
