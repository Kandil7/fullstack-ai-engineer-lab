# Functional Python — Glossary 29

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| associativity | Property | `(f∘g)∘h == f∘(g∘h)` — regrouping composition changes nothing |
| closure | Function | A function retaining its enclosing scope |
| composition | Function | `compose(g, f)(x)` computes `g(f(x))` |
| comprehension | Syntax | Inline loop producing a container: `[f(x) for x in it]` |
| currying | Function | Transforming `f(a, b)` into `f(a)(b)` |
| filter | Function | Keep items where a predicate is true (lazy) |
| frozen dataclass | Data | `@dataclass(frozen=True)`: immutable, hashable instance |
| functional core | Architecture | Pure logic isolated from I/O |
| groupby | itertools | Groups adjacent equal keys — requires sorted input |
| immutability | Data | An object that cannot change after creation |
| imperative shell | Architecture | Thin outer layer owning files, network, and user I/O |
| itertools | Module | Lazy functional toolkit: chain, islice, product, tee |
| lru_cache | Function | Memoization decorator; safe only for pure functions |
| map | Function | Apply a function to every item (lazy) |
| operator module | Module | Operators as first-class functions: add, itemgetter |
| partial | Function | Pre-binding leading arguments: `partial(f, a)` |
| pure function | Concept | Same args → same result; no side effects |
| reduce | Function | Fold a sequence to one value: `reduce(fn, it)` |
| referential transparency | Concept | Any expression may be replaced by its value |
| tail-call optimization | Concept | Reusing a stack frame for recursion — absent in CPython |

## Detailed Definitions

### associativity
**Definition**: Composition groups freely: `compose(f, compose(g, h))`
equals `compose(compose(f, g), h)` for every input. This is the
algebraic license to refactor pipelines.
**Example**:
```python
def compose(g, f):
    return lambda x: g(f(x))

def double(x): return x * 2
def inc(x): return x + 1
def neg(x): return -x

left = compose(compose(double, inc), neg)   # ((-x) + 1) * 2
right = compose(double, compose(inc, neg))  # -(x) -> inc -> double
print(left(3), right(3))
```
```text
-4 -4
```
**Related**: composition, pure function

### closure
**Definition**: A function that retains access to variables of the scope
where it was defined, even after that scope returns. The mechanism
behind decorators, partials, and factories.
**Example**:
```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor   # factor captured
    return multiply

triple = make_multiplier(3)
print(triple(5))
```
```text
15
```
**Related**: partial, composition

### composition
**Definition**: Building one function from two: `compose(g, f)(x) ==
g(f(x))`. The glue of functional pipelines.
**Example**:
```python
def compose(g, f):
    def composed(x):
        return g(f(x))
    return composed

pipeline = compose(str, lambda x: x + 1)
print(pipeline(4))
```
```text
5
```
**Related**: associativity, closure

### comprehension
**Definition**: Inline container construction: `[f(x) for x in it if
pred(x)]` for lists, `{}` for dicts, `()` for generators. Eager (O(n)
memory) except the generator form.
**Example**:
```python
squares = [x * x for x in range(5) if x % 2 == 0]
print(squares)
```
```text
[0, 4, 16]
```
**Related**: map, filter

### currying
**Definition**: Converting a multi-argument function into nested
single-argument functions: `f(a, b)` becomes `f(a)(b)`. Python prefers
`functools.partial`, which is currying with the first argument bound.
**Example**:
```python
def add(a, b):
    return a + b

add5 = lambda b: add(5, b)   # curried form, manually
print(add5(3))
```
```text
8
```
**Related**: partial, closure

### filter
**Definition**: A lazy higher-order function keeping items where the
predicate is true: `filter(pred, it)`.
**Example**:
```python
even = list(filter(lambda x: x % 2 == 0, range(10)))
print(even)
```
```text
[0, 2, 4, 6, 8]
```
**Related**: map, comprehension

### frozen dataclass
**Definition**: A `@dataclass(frozen=True)` class whose instances raise
`FrozenInstanceError` on any attribute write; generated `__hash__` makes
them usable as dict keys.
**Example**:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Chunk:
    doc_id: int
    text: str

c = Chunk(1, "hello")
try:
    c.text = "bye"
except AttributeError as exc:
    print(type(exc).__name__)
```
```text
FrozenInstanceError
```
**Related**: immutability, hashability

### functional core
**Definition**: The pure, deterministic part of a system — transforms,
scoring, ranking — containing no I/O, so it is testable, cacheable, and
replayable.
**Example**:
```python
def core(samples):
    return sorted(samples, key=len)   # pure: no I/O

print(core(["bb", "a"]))
```
```text
['a', 'bb']
```
**Related**: imperative shell, pure function

### groupby
**Definition**: `itertools.groupby` emits `(key, iterator)` for runs of
adjacent equal keys. Input MUST be sorted by the key, or the same key
splits into multiple groups.
**Example**:
```python
import itertools

data = [("a", 1), ("b", 2), ("a", 3)]   # NOT sorted by key
print([k for k, _ in itertools.groupby(data, key=lambda p: p[0])])
```
```text
['a', 'b', 'a']
```
**Related**: itertools, sort

### immutability
**Definition**: The property of an object that its state cannot change
after construction. In Python it is a convention (`tuple`, `str`) or a
guarantee (`frozen=True`).
**Example**:
```python
t = (1, 2, 3)
try:
    t[0] = 9
except TypeError as exc:
    print(type(exc).__name__)
```
```text
TypeError
```
**Related**: frozen dataclass, hashability

### imperative shell
**Definition**: The thin outer layer that owns files, sockets, user
input, and logging — deliberately impure, delegating logic to the pure
core.
**Example**:
```python
def shell(path):
    with open(path, encoding="utf-8") as fh:   # I/O lives here
        return core(fh.read().splitlines())     # logic is pure

def core(lines):
    return [line.strip() for line in lines]     # pure

print(core(["  x  "]))
```
```text
['x']
```
**Related**: functional core, pure function

### itertools
**Definition**: The standard-library module of lazy functional tools:
`chain`, `islice`, `takewhile`, `starmap`, `product`, `tee`, `groupby`.
Laziness means O(1) memory per stream.
**Example**:
```python
import itertools

print(list(itertools.islice(itertools.count(10), 3)))
print(list(itertools.chain([1, 2], [3])))
```
```text
[10, 11, 12]
[1, 2, 3]
```
**Related**: map, groupby

### lru_cache
**Definition**: `functools.lru_cache` memoizes call results keyed by
arguments. It is correct only for pure functions — impure ones return
stale data.
**Example**:
```python
import functools

calls = {"n": 0}

@functools.lru_cache(maxsize=None)
def square(x):
    calls["n"] += 1
    return x * x

square(4); square(4)
print(calls["n"])
```
```text
1
```
**Related**: pure function, referential transparency

### map
**Definition**: A lazy higher-order function applying a function to
every item: `map(f, it)`.
**Example**:
```python
print(list(map(str.upper, ["a", "b"])))
```
```text
['A', 'B']
```
**Related**: filter, comprehension, operator module

### operator module
**Definition**: Operators exposed as first-class functions — `add`,
`itemgetter`, `attrgetter`, `methodcaller` — removing lambdas from hot
paths and sorts.
**Example**:
```python
import operator

rows = [("b", 2), ("a", 1)]
print(sorted(rows, key=operator.itemgetter(1)))
```
```text
[('a', 1), ('b', 2)]
```
**Related**: map, reduce

### partial
**Definition**: `functools.partial(f, a)` returns a function with `a`
pre-bound as the first argument — configuration through binding.
**Example**:
```python
import functools

def scale(x, factor):
    return x * factor

halve = functools.partial(scale, factor=0.5)
print(halve(10))
```
```text
5.0
```
**Related**: currying, closure

### pure function
**Definition**: A function with no side effects and deterministic
output: same arguments always produce the same result.
**Example**:
```python
def add_one(x):
    return x + 1     # pure

print(add_one(1) == add_one(1))
```
```text
True
```
**Related**: referential transparency, lru_cache

### reduce
**Definition**: `functools.reduce(fn, it)` folds a sequence into one
value by applying `fn` left to right. Prefer `sum`, `min`, `max` where
they exist.
**Example**:
```python
import functools
import operator

print(functools.reduce(operator.add, [1, 2, 3, 4]))
```
```text
10
```
**Related**: operator module, map

### referential transparency
**Definition**: The property that any expression can be replaced by its
value without changing program behavior — the license for caching and
reordering.
**Example**:
```python
def f(x):
    return x * 2

print(2 + f(3))          # replace f(3) with 6
print(2 + 6)             # identical program
```
```text
8
8
```
**Related**: pure function, lru_cache

### tail-call optimization
**Definition**: A compiler trick reusing one stack frame for a recursive
call in tail position. CPython does not implement it — recursion depth
is bounded (~1000) and deep recursion raises `RecursionError`.
**Example**:
```python
def rec(n):
    return rec(n - 1) if n else 0

try:
    rec(10_000)
except RecursionError as exc:
    print(type(exc).__name__)
```
```text
RecursionError
```
**Related**: pure function, immutability

## Key Concepts Summary

### The Purity Contract
- Pure: same args → same result, no side effects
- Referential transparency: `f(x)` is interchangeable with its value
- Only pure functions may be memoized (`lru_cache`), reordered, or replayed
- Frozen dataclasses make immutability structural, not conventional

### The Functional Vocabulary
- `map`/`filter`/`reduce` + comprehensions: loops without `for`
- `operator` module: operators as data
- `partial`/currying: configuration through binding
- `compose`: pipelines as algebra (associative)
- `itertools`: lazy streams, sorted `groupby`

### The Architecture
- Functional core: pure, deterministic, cacheable
- Imperative shell: thin, owns I/O
- Iterate, never recurse deep: no tail-call optimization in CPython

## Practice Terms

Match each term to its definition (answers at the bottom).

1. pure function — ___
2. referential transparency — ___
3. frozen dataclass — ___
4. compose — ___
5. partial — ___
6. groupby — ___
7. lru_cache — ___
8. functional core — ___

A. Pre-binds leading arguments to make a new function
B. Groups adjacent equal keys; needs sorted input
C. Same arguments, same result, no side effects
D. `g(f(x))`; associative chain building
E. An expression is interchangeable with its value
F. Memoization decorator, safe only for pure functions
G. Immutable, hashable `@dataclass(frozen=True)` instances
H. Pure logic isolated from I/O

**Answers:** 1-C, 2-E, 3-G, 4-D, 5-A, 6-B, 7-F, 8-H
