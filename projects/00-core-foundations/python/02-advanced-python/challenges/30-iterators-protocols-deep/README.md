# Challenge 30: Iterators and Protocols Deep

Build a dict-equivalent container the way the standard library would:
a few dunders plus a `collections.abc` base, and the ABC supplies the
rest of the interface for free.

## 🥉 Bronze — Dict-Like Core (~15 min)

**Task:** Implement `KeyValueStore` with `__getitem__`, `__setitem__`,
`__len__`, and `__contains__` backed by a private dict. Keys are stored
as given (exact-match semantics, like a dict).

**Signature:**
```python
class KeyValueStore:
    def __init__(self, data: dict | None = None): ...
    def __getitem__(self, key: str) -> int: ...
    def __setitem__(self, key: str, value: int) -> None: ...
    def __len__(self) -> int: ...
    def __contains__(self, key: object) -> bool: ...
```

| Input | Expected |
|-------|----------|
| `s = KeyValueStore({"a": 1}); s["a"]` | `1` |
| `s["b"] = 2; len(s)` | `2` |
| `"a" in s` | `True` |
| `s["missing"]` | `KeyError` |

**Constraints:** n ≤ 10^3. Missing keys must raise `KeyError`, not return
`None`.

---

## 🥈 Silver — Full Mapping Semantics via the ABC (~35 min)

**Task:** Extend the store to subclass `collections.abc.Mapping` AND
implement `__iter__`. With `__getitem__` + `__len__` + `__iter__` in
place, the ABC supplies `get`, `keys`, `values`, `items`, `__eq__` for
free. The result must behave like a real read-only dict.

**Signature:**
```python
class KeyValueStore(Mapping):  # full Mapping mixin
    ...
    def __iter__(self): ...
```

| Input | Expected |
|-------|----------|
| `s.get("nope", 99)` | `99` |
| `sorted(s.keys())` | `['a', 'b']` |
| `dict(s.items())` | `{'a': 1, 'b': 2}` |
| `s == {"a": 1, "b": 2}` | `True` |
| `isinstance(s, Mapping)` | `True` |

**Constraints:** n ≤ 10^4. The ABC must do the work: the solution may
implement ONLY `__getitem__`, `__len__`, `__iter__` (plus storage) —
implementing `get`/`keys` by hand is the wrong approach (the test
checks the ABC supplies them via `Mapping` in the MRO).

---

## 🥇 Gold — Hashable, Immutable Snapshot Dict (~75 min)

**Task:** Add `snapshot(self) -> SnapshotDict` returning an immutable,
**hashable** copy that (a) hashes consistently with value equality
(`s1 == s2` implies `hash(s1) == hash(s2)`), (b) is safe to use as a
dict key, and (c) never changes when the source store mutates.

`SnapshotDict` must implement `__hash__`, `__eq__`, `__getitem__`,
`__len__`, `__iter__` and be a `Mapping`. Its hash must be precomputed
once at construction — O(n) once, O(1) per access afterwards.

**Signature:**
```python
class SnapshotDict(Mapping):
    def __init__(self, data: dict[str, int]): ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...

class KeyValueStore(Mapping):
    ...
    def snapshot(self) -> SnapshotDict: ...
```

| Input | Expected |
|-------|----------|
| `s.snapshot()["a"]` | `1` |
| `s["a"] = 999` after snapshot | snapshot still `1` |
| `hash(s.snapshot()) == hash(s.snapshot())` | `True` |
| `s.snapshot() == {"a": 1, "b": 2}` | `True` |

**Constraints:** n ≤ 10^5 keys. Hash must be computed in **one pass**
over the items (operation-count guard: an item-counting iterator proves
each key visited exactly once at construction). Memory: a 50k-key
snapshot stays under 8 MB (`tracemalloc`). Follow-up: what breaks if
`__hash__` changed after insertion into a dict? (Answer: the exact
corruption demoed in `30-iterators-protocols-deep.py` — lookups miss,
entries leak.)

---

## Running

```bash
pytest challenges/30-iterators-protocols-deep/test_challenge.py -v
```
