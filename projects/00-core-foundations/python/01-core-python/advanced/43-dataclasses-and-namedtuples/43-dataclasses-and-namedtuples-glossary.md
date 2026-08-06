# Dataclasses & NamedTuples — Glossary 43

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| `@dataclass` | Decorator | Generates `__init__`, `__repr__`, `__eq__` from annotations |
| `__post_init__` | Method | Runs after `__init__`; the place for validation/derivation |
| `default_factory` | Field option | Callable producing a fresh mutable default per instance |
| `field()` | Function | Configures per-field dataclass behavior |
| `frozen=True` | Option | Makes instances immutable and (usually) hashable |
| `FrozenInstanceError` | Exception | Raised when assigning to a frozen dataclass field |
| `order=True` | Option | Generates `<`, `<=`, `>`, `>=` via field-tuple comparison |
| `slots=True` | Option | Removes per-instance `__dict__`; smaller, faster (3.10+) |
| `kw_only=True` | Option | Requires keyword arguments for fields |
| `NamedTuple` | Class | Immutable tuple subclass with named fields |
| `TypedDict` | Type | Type-checker contract for dicts of fixed shape |
| `NotRequired` | Type | Marks a `TypedDict` key as optional |
| `asdict()` | Function | Converts a dataclass to a nested dict |
| `astuple()` | Function | Converts a dataclass to a tuple |
| `replace()` | Function | Returns a copy with selected fields changed |
| `is_dataclass()` | Function | True if the argument is a dataclass |
| `dataclasses.dataclass` | Module | Standard-library module defining the decorator |

## Detailed Definitions

### `@dataclass`
**Definition**: A class decorator that reads the class annotations and generates
`__init__`, `__repr__`, and `__eq__` (plus more with options) automatically.
**Example**:
```python
from dataclasses import dataclass

@dataclass
class Token:
    text: str
    freq: int = 1

print(Token("the"))       # Token(text='the', freq=1)
```
**Complexity**: construction O(k), k = number of fields.
**Related**: `field()`, `__post_init__`, `slots=True`

### `__post_init__`
**Definition**: A hook called at the end of the generated `__init__`; used for
validation and for fields derived from others.
**Example**:
```python
@dataclass
class Run:
    lr: float
    steps: int

    def __post_init__(self) -> None:
        if self.lr <= 0:
            raise ValueError("lr must be positive")
```
**Complexity**: O(1) unless it iterates fields.
**Related**: `frozen=True`, `field()`

### `default_factory`
**Definition**: The `field()` argument that supplies a callable run on every
construction, giving each instance its own mutable default.
**Example**:
```python
from dataclasses import dataclass, field

@dataclass
class Batch:
    items: list = field(default_factory=list)

a, b = Batch(), Batch()
a.items.append("x")
print(b.items)   # [] — no shared state
```
**Complexity**: O(1) per construction (list/dict factories).
**Related**: `field()`, mutable-default trap

### `field()`
**Definition**: The function that customizes a single field: defaults, metadata,
`repr` inclusion, comparison exclusion, `kw_only`, and `init` toggles.
**Example**:
```python
@dataclass
class Metric:
    name: str
    value: float = field(default=0.0, metadata={"unit": "ms"})
```
**Related**: `default_factory`, `kw_only=True`

### `frozen=True`
**Definition**: Dataclass option making instances immutable; assignment raises
`FrozenInstanceError`, and instances become hashable when all fields are.
**Example**:
```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float

try:
    Point(1, 2).x = 5
except Exception as e:
    print(type(e).__name__)   # FrozenInstanceError
```
**Related**: `FrozenInstanceError`, hashable records

### `FrozenInstanceError`
**Definition**: `AttributeError` subclass raised when a frozen dataclass field
is assigned.
**Related**: `frozen=True`

### `order=True`
**Definition**: Option generating the rich comparison methods by comparing the
fields as a tuple, left to right.
**Example**:
```python
@dataclass(order=True)
class Hit:
    score: float
    doc: str

print(sorted([Hit(0.3, "a"), Hit(0.9, "b")]))  # lowest score first
```
**Complexity**: O(k) worst case per comparison.
**Related**: `__lt__`, `total_ordering`

### `slots=True`
**Definition**: Option (3.10+) that replaces the per-instance `__dict__` with
fixed descriptors: smaller instances, faster access, no new attributes.
**Example**:
```python
import sys

@dataclass(slots=True)
class V:
    x: float

print(sys.getsizeof(V(0.0)))   # 48 — no dict attached
```
**Complexity**: O(1) attribute access, faster than dict lookup.
**Related**: `__slots__`, memory efficiency

### `kw_only=True`
**Definition**: Option requiring every field to be passed by keyword, removing
the positional-order foot-gun for configs with many fields.
**Example**:
```python
@dataclass(kw_only=True)
class Cfg:
    lr: float
    batch: int

Cfg(lr=1e-3, batch=32)   # OK
Cfg(1e-3, 32)            # TypeError
```
**Related**: `field(init=False)`

### `NamedTuple`
**Definition**: A subclass of `tuple` with named fields: immutable, hashable,
unpackable, with zero overhead beyond the tuple.
**Example**:
```python
from typing import NamedTuple

class Pair(NamedTuple):
    query: str
    score: float

p = Pair("rag", 0.9)
q, s = p              # unpacking
print(p.query, p[0])  # attribute and index access
```
**Complexity**: O(k) to build, same as tuple.
**Related**: `dataclass`, tuple

### `TypedDict`
**Definition**: A type-only construct describing the shape of a dict; no runtime
generation, checked by mypy/Pyright.
**Example**:
```python
from typing import TypedDict

class Response(TypedDict):
    id: str
    ok: bool

r: Response = {"id": "1", "ok": True}
```
**Related**: `NotRequired`, JSON records

### `NotRequired`
**Definition**: Marks a `TypedDict` key as optional.
**Example**:
```python
from typing import TypedDict, NotRequired

class Usage(TypedDict):
    tokens: int
    cache_hit: NotRequired[bool]
```
**Related**: `TypedDict`

### `asdict()`
**Definition**: Recursively converts a dataclass instance to nested dicts —
useful for JSON serialization.
**Example**:
```python
from dataclasses import asdict

@dataclass
class Node:
    name: str
    children: list

print(asdict(Node("root", [Node("leaf", [])])))
# {'name': 'root', 'children': [{'name': 'leaf', 'children': []}]}
```
**Related**: `astuple()`, JSON serialization

### `astuple()`
**Definition**: Converts a dataclass instance (and nested dataclasses) to a tuple.
**Related**: `asdict()`

### `replace()`
**Definition**: Returns a new instance with selected fields replaced — the
immutable-friendly way to "modify" frozen records.
**Example**:
```python
from dataclasses import replace

@dataclass(frozen=True)
class Cfg:
    lr: float
    seed: int = 0

new_cfg = replace(Cfg(1e-3), lr=1e-4)   # Cfg(lr=0.0001, seed=0)
```
**Related**: `frozen=True`

### `is_dataclass()`
**Definition**: Returns True if the argument is a dataclass instance or class.
**Related**: `@dataclass`

## Key Concepts Summary

### Choosing the right record type
- **Plain dict** — unstructured, ad-hoc JSON; loses type safety
- **NamedTuple** — tiny immutable records; tuple semantics; cheapest
- **dataclass** — mutable or frozen records with validation, defaults, ordering
- **TypedDict** — typing for dicts that must stay dicts (API payloads)

### Memory and immutability
- `slots=True` removes the per-instance `__dict__` — the big win at scale
- `frozen=True` gives immutability AND hashability for cache keys and sets
- Mutable defaults must go through `default_factory`, never `= []`

### Validation discipline
- `__post_init__` is the single choke point for construction-time checks
- Fail fast at the boundary, not in the middle of a pipeline

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `default_factory` — ___
2. `frozen=True` — ___
3. `__post_init__` — ___
4. `NamedTuple` — ___
5. `TypedDict` — ___
6. `slots=True` — ___
7. `kw_only=True` — ___
8. `replace()` — ___

A. Runs after `__init__` for validation and derived fields
B. Requires keyword arguments for every field
C. Per-instance fresh mutable default
D. Immutable tuple subclass with named fields
E. Returns a new instance with some fields changed
F. Removes the per-instance `__dict__` (3.10+)
G. Immutability + hashability from the compiler
H. Type-checker shape contract for plain dicts

**Answers:** 1-C, 2-G, 3-A, 4-D, 5-H, 6-F, 7-B, 8-E
