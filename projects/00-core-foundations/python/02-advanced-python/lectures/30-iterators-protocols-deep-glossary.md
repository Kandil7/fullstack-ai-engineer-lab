# Iterators and Protocols Deep — Glossary 30

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `__call__` | Dunder | Makes an instance callable: `obj(args)` |
| `__contains__` | Dunder | Customizes `item in obj` |
| `__enter__`/`__exit__` | Dunder | The context-manager protocol behind `with` |
| `__getattr__` | Dunder | Runs only for MISSING attributes (fallback) |
| `__getattribute__` | Dunder | Runs for EVERY attribute access (intercept all) |
| `__getitem__` | Dunder | Indexing `obj[i]`; also drives fallback iteration |
| `__hash__` | Dunder | Dict/set placement; must follow the eq contract |
| `__iter__`/`__next__` | Dunder | The iterator protocol: `for` loop machinery |
| `__len__` | Dunder | `len(obj)`; required by the Sequence ABC |
| `__reversed__` | Dunder | Customizes `reversed(obj)` |
| `collections.abc` | Module | Abstract bases: Sequence, Mapping, Set, Iterable |
| context manager | Concept | Object implementing `__enter__`/`__exit__` |
| data descriptor | Concept | `__get__`/`__set__`-implementing attribute |
| hash/eq contract | Concept | `a == b` implies `hash(a) == hash(b)`; hash never changes |
| iterable | Concept | `iter(x)` succeeds; `for` works |
| iterator | Concept | Has `__next__`; raises `StopIteration` when done |
| Mapping ABC | Interface | `__getitem__`+`__len__`+`__iter__` unlock get/keys/items |
| Sequence ABC | Interface | `__len__`+`__getitem__` unlock in/slicing/reversed |
| StopIteration | Exception | Signals exhaustion of an iterator |
| total_ordering | Decorator | Derives `<=`, `>`, `>=` from `__eq__` + `__lt__` |

## Detailed Definitions

### `__call__`
**Definition**: Makes instances callable — `obj(args)` invokes
`obj.__call__(args)`. The mechanism behind class-based decorators and
callable configuration objects.
**Example**:
```python
class Adder:
    def __init__(self, n):
        self.n = n

    def __call__(self, x):
        return x + self.n

add5 = Adder(5)
print(add5(3))
```
```text
8
```
**Related**: `__getattr__`, context manager

### `__contains__`
**Definition**: Customizes `item in obj`. Without it, `in` falls back
to iteration (O(n)); with it you control semantics and speed.
**Example**:
```python
class TagSet:
    def __init__(self, tags):
        self.tags = {t.lower() for t in tags}

    def __contains__(self, item):
        return isinstance(item, str) and item.lower() in self.tags

print("PY" in TagSet(["py", "ml"]))
```
```text
True
```
**Related**: `__getitem__`, Mapping ABC

### `__enter__`/`__exit__`
**Definition**: The `with` protocol. `__enter__` returns the bound
handle; `__exit__(exc_type, exc, tb)` runs on block exit, even on
exceptions. Returning `True` suppresses the exception.
**Example**:
```python
class Session:
    def __init__(self):
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.closed = True
        return False

with Session() as s:
    pass
print(s.closed)
```
```text
True
```
**Related**: `__call__`, data descriptor

### `__getattr__`
**Definition**: Invoked only when normal attribute lookup fails. The
right tool for lazy defaults and compatibility shims.
**Example**:
```python
class Config:
    def __init__(self, known):
        self.known = known

    def __getattr__(self, name):
        return self.known.get(name, 0)

cfg = Config({"batch": 8})
print(cfg.batch, cfg.lr)
```
```text
8 0
```
**Related**: `__getattribute__`, `__call__`

### `__getattribute__`
**Definition**: Invoked on EVERY attribute access — even for attributes
that exist. Must delegate via `object.__getattribute__` or recurse.
**Example**:
```python
class Locked:
    def __init__(self, value):
        self.value = value

    def __getattribute__(self, name):
        if name == "secret":
            raise AttributeError("denied")
        return object.__getattribute__(self, name)

l = Locked(1)
print(l.value)
try:
    print(l.secret)
except AttributeError as exc:
    print(type(exc).__name__)
```
```text
1
AttributeError
```
**Related**: `__getattr__`, data descriptor

### `__getitem__`
**Definition**: Indexing `obj[i]`; also the legacy iteration protocol —
Python calls `obj[0]`, `obj[1]`, ... until `IndexError`.
**Example**:
```python
class Letters:
    def __init__(self, s):
        self.s = s

    def __getitem__(self, i):
        return self.s[i]

print(list(Letters("ab")))
```
```text
['a', 'b']
```
**Related**: Sequence ABC, `__len__`, `__contains__`

### `__hash__`
**Definition**: Dict/set placement hash. Must be stable for the object's
lifetime and consistent with `__eq__`: equal objects, equal hashes.
**Example**:
```python
class Key:
    def __init__(self, v):
        self.v = v

    def __hash__(self):
        return hash(self.v)

    def __eq__(self, other):
        return isinstance(other, Key) and self.v == other.v

print(Key("a") in {Key("a")})
```
```text
True
```
**Related**: hash/eq contract, `__getitem__`

### `__iter__`/`__next__`
**Definition**: The iterator protocol: `iter(x)` → `__iter__`;
`next(it)` → `__next__`; exhaustion signaled by `StopIteration`.
**Example**:
```python
class Odds:
    def __init__(self, n):
        self.n = n
        self.i = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.i += 2
        if self.i > self.n:
            raise StopIteration
        return self.i

print(list(Odds(7)))
```
```text
[1, 3, 5, 7]
```
**Related**: StopIteration, `__getitem__`

### `__len__`
**Definition**: `len(obj)` support; semantically "number of items".
Required by `Sequence` and `Mapping` ABCs.
**Example**:
```python
class Box:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

print(len(Box([1, 2, 3])))
```
```text
3
```
**Related**: Sequence ABC, `__getitem__`

### `__reversed__`
**Definition**: Customizes `reversed(obj)`. Without it, `reversed`
works only on sequences (via `__len__` + `__getitem__`).
**Example**:
```python
class Down:
    def __init__(self, n):
        self.n = n

    def __reversed__(self):
        return iter(range(self.n, 0, -1))

print(list(reversed(Down(3))))
```
```text
[3, 2, 1]
```
**Related**: `__getitem__`, Sequence ABC

### `collections.abc`
**Definition**: Abstract base classes defining Python's container
interfaces — `Sequence`, `Mapping`, `Set`, `Iterable`, `Iterator`,
`ContextManager`. Subclassing one registers your class and grants
mixin methods.
**Example**:
```python
from collections.abc import Sequence

class Pair(Sequence):
    def __init__(self, a, b):
        self._items = (a, b)

    def __len__(self):
        return 2

    def __getitem__(self, i):
        return self._items[i]

print(isinstance(Pair(1, 2), Sequence), 0 in Pair(1, 2))
```
```text
True False
```
**Related**: Sequence ABC, Mapping ABC

### context manager
**Definition**: An object with `__enter__`/`__exit__`, usable in `with`
statements to guarantee cleanup (files, locks, sessions).
**Example**:
```python
with open("nonexistent_never_created.txt", "w") as fh:
    fh.write("x")
# file closed even if write raised
print("cleanup guaranteed")
```
```text
cleanup guaranteed
```
**Related**: `__enter__`/`__exit__`

### data descriptor
**Definition**: An attribute object implementing `__get__` and `__set__`
that intercepts attribute access — the machinery behind `property`.
**Example**:
```python
class Positive:
    def __get__(self, obj, owner):
        return obj.__dict__["_v"]

    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("negative")
        obj.__dict__["_v"] = value

class Temp:
    celsius = Positive()

t = Temp()
t.celsius = 25
print(t.celsius)
```
```text
25
```
**Related**: `__getattribute__`, `__getattr__`

### hash/eq contract
**Definition**: The invariant `a == b` ⇒ `hash(a) == hash(b)`, plus a
hash that never changes during the object's lifetime in a dict/set.
Violations corrupt lookups silently.
**Example**:
```python
class Good:
    def __init__(self, v):
        self.v = v

    def __hash__(self):
        return hash(self.v)

    def __eq__(self, other):
        return isinstance(other, Good) and self.v == other.v

print(Good(1) in {Good(1)})
```
```text
True
```
**Related**: `__hash__`, `__getitem__`

### iterable
**Definition**: An object for which `iter(x)` succeeds — it has
`__iter__` (or the `__getitem__` fallback). Everything a `for` loop
accepts.
**Example**:
```python
print(iter([1, 2]))
```
```text
<list_iterator object at 0x...>
```
**Related**: iterator, `__iter__`/`__next__`

### iterator
**Definition**: An object with `__next__` that raises `StopIteration`
when exhausted. Every iterator is iterable (its `__iter__` returns
itself).
**Example**:
```python
it = iter([1, 2])
print(next(it), next(it))
try:
    next(it)
except StopIteration:
    print("exhausted")
```
```text
1 2
exhausted
```
**Related**: iterable, StopIteration

### Mapping ABC
**Definition**: Interface for read-only dict-likes: implement
`__getitem__` + `__len__` + `__iter__`, inherit `get`/`keys`/`values`/
`items`/`__contains__`/`__eq__`.
**Example**:
```python
from collections.abc import Mapping

class One(Mapping):
    def __init__(self):
        self._d = {"k": 1}

    def __getitem__(self, k):
        return self._d[k]

    def __len__(self):
        return 1

    def __iter__(self):
        return iter(self._d)

print(One().get("k"))
```
```text
1
```
**Related**: Mapping ABC, `__getitem__`

### Sequence ABC
**Definition**: Interface for read-only list-likes: implement
`__len__` + `__getitem__`, inherit `__contains__`/`__iter__`/
`__reversed__`/`index`/`count`.
**Example**:
```python
from collections.abc import Sequence

class Two(Sequence):
    def __init__(self, a, b):
        self._items = (a, b)

    def __len__(self):
        return 2

    def __getitem__(self, i):
        return self._items[i]

print(Two(1, 2)[1:2], 1 in Two(1, 2))
```
```text
(2,) True
```
**Related**: Sequence ABC, `__len__`

### StopIteration
**Definition**: The built-in exception signaling iterator exhaustion;
raised by `__next__` and caught by `for`/`next()` machinery.
**Example**:
```python
class Empty:
    def __next__(self):
        raise StopIteration

try:
    next(Empty())
except StopIteration:
    print("stopped")
```
```text
stopped
```
**Related**: `__iter__`/`__next__`, iterator

### total_ordering
**Definition**: A class decorator deriving `__le__`, `__gt__`, `__ge__`
from `__eq__` plus one comparison (usually `__lt__`).
**Example**:
```python
import functools

@functools.total_ordering
class Rank:
    def __init__(self, n):
        self.n = n

    def __eq__(self, other):
        return self.n == other.n

    def __lt__(self, other):
        return self.n < other.n

r = Rank(2)
print(r <= Rank(3), r >= Rank(2))
```
```text
True True
```
**Related**: `__getitem__`, hash/eq contract

## Key Concepts Summary

### The Dispatch Model
- Built-in syntax calls dunders by name: `len`→`__len__`, `in`→`__contains__`, `[]`→`__getitem__`
- Protocols compose: Sequence/Mapping ABCs derive the full interface from 2-3 dunders
- `collections.abc` registers your class for `isinstance` checks

### The Contracts
- Iterator: `__iter__` + `__next__` + `StopIteration`
- Context manager: `__enter__`/`__exit__`; return False to propagate
- Hash/eq: equal objects hash equally; hashes never change while stored
- Ordering: `__eq__` + `__lt__` + `total_ordering` fills the rest

### The Attribute Hooks
- `__getattr__`: fallback for missing attributes
- `__getattribute__`: total interception — delegate to `object` or recurse
- `__call__`: instances as functions

## Practice Terms

Match each term to its definition (answers at the bottom).

1. StopIteration — ___
2. hash/eq contract — ___
3. Sequence ABC — ___
4. `__getattr__` — ___
5. total_ordering — ___
6. `__enter__`/`__exit__` — ___
7. Mapping ABC — ___
8. `__getattribute__` — ___

A. The `with` protocol; `__exit__` guarantees cleanup
B. `__len__` + `__getitem__` unlock in/slicing/reversed
C. Signals iterator exhaustion
D. Runs for missing attributes only
E. Runs for every attribute access
F. `a == b` implies `hash(a) == hash(b)`; hash never changes
G. `__getitem__` + `__len__` + `__iter__` unlock get/keys/items
H. Derives `<=`, `>`, `>=` from `__eq__` + `__lt__`

**Answers:** 1-C, 2-F, 3-B, 4-D, 5-H, 6-A, 7-G, 8-E
