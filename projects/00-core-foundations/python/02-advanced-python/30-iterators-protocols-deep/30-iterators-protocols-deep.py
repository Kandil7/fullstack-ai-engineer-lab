"""
Advanced Python — 30: Iterators and Protocols Deep
====================================================
Topics: __iter__/__next__, __len__, __getitem__ fallback, __contains__,
__reversed__, __enter__/__exit__, __call__, __hash__/__eq__ contract,
__lt__ + total_ordering, __getattr__ vs __getattribute__,
collections.abc hierarchy, custom Sequence/Mapping

Why this matters for AI/backend engineering:
    A PyTorch Dataset is just __len__ + __getitem__. A custom container
    for batched inference is a Sequence. Getting the dunder contract
    wrong — especially __hash__/__eq__ — silently corrupts dicts and
    caches. This file makes those contracts concrete and testable.

Run:      python 30-iterators-protocols-deep.py
Verify:   python 30-iterators-protocols-deep.py --verify
Reference: https://docs.python.org/3/reference/datamodel.html
"""

from __future__ import annotations

import functools
import sys
from collections.abc import Mapping, Sequence
from typing import Any, Iterator


# ============================================================
# 1. __iter__ / __next__: The Iterator Protocol
# ============================================================
# An object is iterable if it returns an iterator from __iter__; the
# iterator advances with __next__ and signals exhaustion with
# StopIteration. Complexity: O(1) per next().

class Countdown:
    """Iterable AND iterator: counts down from start to 0."""
    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self) -> "Countdown":
        """Return self — we are our own iterator."""
        return self

    def __next__(self) -> int:
        """Return next value or raise StopIteration. O(1)."""
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


# Example 1: a custom iterator in a for loop
print(f"countdown: {list(Countdown(3))}")

# Output:
# countdown: [3, 2, 1, 0]


# ============================================================
# 2. __getitem__ Fallback (The Legacy Sequence Protocol)
# ============================================================
# Iteration works on ANY object with __getitem__ raising IndexError —
# no __iter__ needed. This is how the protocol grew before __iter__.

class SliceByIndex:
    """Iterable via __getitem__ alone: the fallback protocol."""
    def __init__(self, items: list[int]) -> None:
        self.items = items

    def __getitem__(self, index: int) -> int:
        """Return item or raise IndexError to end iteration. O(1)."""
        return self.items[index]


# Example 2: __getitem__-only objects are iterable
print(f"fallback iteration: {list(SliceByIndex([10, 20, 30]))}")

# Output:
# fallback iteration: [10, 20, 30]


# ============================================================
# 3. Custom Sequence via collections.abc
# ============================================================
# Register as a Sequence and the ABC gives you index(), count(),
# __contains__, __iter__, __reversed__ for free from just __len__ +
# __getitem__. This is the PyTorch Dataset pattern.

class EmbeddingDataset(Sequence):
    """A read-only Sequence of (id, vector) pairs — Dataset-like."""
    def __init__(self, ids: list[int], vectors: list[tuple[float, ...]]) -> None:
        self._ids = ids
        self._vectors = vectors

    def __len__(self) -> int:
        """Dataset size. O(1)."""
        return len(self._ids)

    def __getitem__(self, index: int | slice) -> Any:
        """Dataset[i] -> item; slice support comes via Sequence mixin."""
        if isinstance(index, slice):
            ids = self._ids[index]
            vecs = self._vectors[index]
            return list(zip(ids, vecs))
        return (self._ids[index], self._vectors[index])


# Example 3: len/in/slicing/reversed all work from two dunders
ds = EmbeddingDataset([0, 1, 2], [(1.0,), (2.0,), (3.0,)])
print(f"len: {len(ds)}")
print(f"index: {ds[1]}")
print(f"in: {(2, (3.0,)) in ds}")
print(f"slice: {ds[1:3]}")
print(f"reversed ids: {[i for i, _ in reversed(ds)]}")

# Output:
# len: 3
# index: (1, (2.0,))
# in: True
# slice: [(1, (2.0,)), (2, (3.0,))]
# reversed ids: [2, 1, 0]


# ============================================================
# 4. __contains__, __reversed__, __call__
# ============================================================
# __contains__ customizes `in`; __reversed__ customizes reversed();
# __call__ makes instances callable (used by decorators-as-classes).

class Membership:
    """Custom `in` semantics: case-insensitive string containment."""
    def __init__(self, values: list[str]) -> None:
        self.values = [v.lower() for v in values]

    def __contains__(self, item: object) -> bool:
        """Case-insensitive membership. O(n) — fine for small lists."""
        return isinstance(item, str) and item.lower() in self.values

    def __call__(self, prefix: str) -> list[str]:
        """Make the instance callable: filter by prefix. O(n)."""
        return [v for v in self.values if v.startswith(prefix.lower())]


# Example 4: `in` and calling an instance
m = Membership(["Alpha", "Beta"])
print(f"'ALPHA' in m: {'ALPHA' in m}")
print(f"m('b') -> {m('b')}")

# Output:
# 'ALPHA' in m: True
# m('b') -> ['beta']


# ============================================================
# 5. __enter__ / __exit__: Context Manager Protocol
# ============================================================
# The `with` protocol. __exit__ returning True suppresses the exception
# (usually you return False and let it propagate).

class ManagedVector:
    """Context manager mimicking a vector-store session."""
    def __init__(self, name: str) -> None:
        self.name = name
        self.open = False

    def __enter__(self) -> "ManagedVector":
        """Begin the session. Called by `with`. O(1)."""
        self.open = True
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        """Always close the session; never swallow errors. O(1)."""
        self.open = False
        return False


# Example 5: with-statement lifecycle
with ManagedVector("emb") as store:
    print(f"inside with: open={store.open}")
print(f"after with: open={store.open}")

# Output:
# inside with: open=True
# after with: open=False


# ============================================================
# 6. The __hash__ / __eq__ Contract
# ============================================================
# Contract: if a == b then hash(a) == hash(b). Equal objects must hash
# equally, and the hash of an object in a dict/set must NEVER change.
# Breaking it corrupts dict behavior: lookups miss, duplicates appear.

class MutableKey:
    """DELIBERATELY BROKEN: hash follows a mutable field."""
    def __init__(self, value: str) -> None:
        self.value = value

    def __hash__(self) -> int:
        return hash(self.value)          # changes when value changes!

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MutableKey) and self.value == other.value

    def __repr__(self) -> str:
        return f"MutableKey({self.value!r})"


# Example 6: the corruption, demonstrated
# NOTE: with CPython 3.10+, looking up the SAME mutated object can still
# hit an identity fast-path (bucket-layout dependent, not portable).
# The deterministic proof of corruption is a FRESH equal key: it must be
# findable by __eq__ and yet the dict cannot locate it.
key = MutableKey("a")
table: dict[MutableKey, int] = {key: 1}
print(f"lookup before mutation: {table.get(key)}")
key.value = "b"                          # mutate the hash-relevant field
fresh = MutableKey("b")                  # equal to the mutated key...
print(f"fresh equal key in table: {fresh in table}  (fresh == key: {fresh == key})")
print(f"len(table): {len(table)}")

# Output:
# lookup before mutation: 1
# fresh equal key in table: False  (fresh == key: True)
# len(table): 1


# ============================================================
# 7. __lt__ + total_ordering
# ============================================================
# Define __eq__ + one rich comparison and total_ordering fills the
# rest (__le__, __gt__, __ge__) from them.

@functools.total_ordering
class Score:
    """Orderable score with only __eq__ and __lt__ defined."""
    def __init__(self, value: float) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Score) and self.value == other.value

    def __lt__(self, other: "Score") -> bool:
        return self.value < other.value


# Example 7: one dunder, four operators
a = Score(1.0)
b = Score(2.0)
print(f"a < b: {a < b} | a <= b: {a <= b} | b > a: {b > a} | a >= a: {a >= a}")

# Output:
# a < b: True | a <= b: True | b > a: True | a >= a: True


# ============================================================
# 8. __getattr__ vs __getattribute__
# ============================================================
# __getattr__ runs ONLY for missing attributes; __getattribute__ runs
# for EVERY attribute access. Use __getattr__ for lazy defaults;
# override __getattribute__ only when you must intercept everything.

class LazyConfig:
    """__getattr__ computes defaults for missing keys."""
    def __init__(self, known: dict[str, int]) -> None:
        self.known = known

    def __getattr__(self, name: str) -> int:
        """Return 0 for any unknown attribute. O(1)."""
        return self.known.get(name, 0)


class CountingAccess:
    """__getattribute__ sees every access — use sparingly."""
    def __init__(self, value: int) -> None:
        self.value = value
        self.accesses = 0

    def __getattribute__(self, name: str) -> Any:
        """Intercept every read, then delegate to the base. O(1) per read."""
        if name == "value":
            # Without the base call we would recurse forever.
            base = object.__getattribute__
            base(self, "accesses")  # increment tracking is an exercise
        return object.__getattribute__(self, name)


# Example 8: fallback vs total interception
cfg = LazyConfig({"batch": 32})
print(f"known: {cfg.batch} | unknown: {cfg.lr}")

ca = CountingAccess(7)
print(f"value: {ca.value}")

# Output:
# known: 32 | unknown: 0
# value: 7


# ============================================================
# 9. Production Pattern: Mapping via collections.abc
# ============================================================
# Subclass Mapping, implement __getitem__ + __len__ + __iter__, and the
# ABC supplies get/keys/values/items/__contains__ for free.

class CaseInsensitiveMap(Mapping):
    """A read-only mapping with case-insensitive string keys."""
    def __init__(self, data: dict[str, int]) -> None:
        self._data = {k.lower(): v for k, v in data.items()}

    def __getitem__(self, key: str) -> int:
        """Lookup, case-insensitively. O(1) average."""
        return self._data[key.lower()]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)


# Example 9: Mapping ABC gives the full dictionary API
cm = CaseInsensitiveMap({"Rate": 10})
print(f"get: {cm.get('rate')} | items: {dict(cm.items())}")

# Output:
# get: 10 | items: {'rate': 10}


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: mutable hash — the dict corruption in Section 6
# CORRECT: hash on immutable fields, or frozen dataclass keys
#
# MISTAKE: __getattr__ for existing attributes
#   __getattr__ never fires for attributes that exist — surprising when
#   a real attribute shadows your fallback
# CORRECT: use __getattr__ only for genuine defaults; property for computed
#
# MISTAKE: __getattribute__ without calling object.__getattribute__
#   infinite recursion: self.value inside __getattribute__ re-enters it
# CORRECT: always delegate via object.__getattribute__(self, name)
#
# MISTAKE: __eq__ without __hash__ — the class becomes unhashable
#   defining __eq__ sets __hash__ to None; dict keys and sets break
# CORRECT: define both, or use dataclass(eq=True, frozen=True)


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # --- iterator protocol ---
    assert list(Countdown(3)) == [3, 2, 1, 0], \
        "__iter__/__next__ must drive for-loop iteration"
    assert next(iter(Countdown(0))) == 0, \
        "first next() must return the start value"

    # --- __getitem__ fallback ---
    assert list(SliceByIndex([10, 20, 30])) == [10, 20, 30], \
        "__getitem__ with IndexError must support iteration"

    # --- custom Sequence: len/in/slicing/reversed ---
    ds = EmbeddingDataset([0, 1, 2], [(1.0,), (2.0,), (3.0,)])
    assert len(ds) == 3, "__len__ must report the dataset size"
    assert ds[1] == (1, (2.0,)), "__getitem__ must return items by index"
    assert (2, (3.0,)) in ds, "Sequence ABC must supply __contains__"
    assert ds[1:3] == [(1, (2.0,)), (2, (3.0,))], \
        "Sequence ABC must supply slicing"
    assert [i for i, _ in reversed(ds)] == [2, 1, 0], \
        "Sequence ABC must supply __reversed__"
    assert isinstance(ds, Sequence), \
        "the class must register as collections.abc.Sequence"

    # --- __contains__ / __call__ ---
    m = Membership(["Alpha", "Beta"])
    assert "ALPHA" in m, "__contains__ must be case-insensitive"
    assert m("b") == ["beta"], "__call__ must make instances callable"

    # --- context manager ---
    with ManagedVector("emb") as store:
        assert store.open is True, "__enter__ must open the session"
    assert store.open is False, "__exit__ must close the session"

    # --- __hash__/__eq__ contract corruption, demonstrated ---
    key = MutableKey("a")
    table: dict[MutableKey, int] = {key: 1}
    assert table.get(key) == 1, "fresh key must be found"
    key.value = "b"
    fresh = MutableKey("b")
    assert fresh == key, "the fresh key must equal the mutated one"
    assert fresh not in table, \
        "an EQUAL key must not be found after mutation (contract violation)"
    assert len(table) == 1, \
        "the entry still exists — the dict is now corrupted, not empty"

    # --- hash/eq contract respected: equal objects hash equal ---
    class Good:
        """Contract-correct key: hash on an immutable field."""
        def __init__(self, value: str) -> None:
            self.value = value

        def __hash__(self) -> int:
            return hash(self.value)

        def __eq__(self, other: object) -> bool:
            return isinstance(other, Good) and self.value == other.value

    assert hash(Good("x")) == hash(Good("x")), \
        "equal objects must hash equally"
    assert Good("x") in {Good("x")}, "contract-correct keys must be found"

    # --- total_ordering ---
    a = Score(1.0)
    b = Score(2.0)
    assert a < b and a <= b and b > a and a >= a, \
        "total_ordering must derive <=, >, >= from __eq__ and __lt__"

    # --- __getattr__ vs __getattribute__ ---
    cfg = LazyConfig({"batch": 32})
    assert cfg.batch == 32 and cfg.lr == 0, \
        "__getattr__ must only fire for missing attributes"
    assert ca.value == 7, "__getattribute__ must delegate to the base"

    # --- Mapping ABC ---
    cm = CaseInsensitiveMap({"Rate": 10})
    assert isinstance(cm, Mapping), "class must register as a Mapping"
    assert cm["RATE"] == 10, "__getitem__ must be case-insensitive"
    assert dict(cm.items()) == {"rate": 10}, \
        "Mapping ABC must supply items()"
    assert "rate" in cm, "Mapping ABC must supply __contains__"

    print("[OK] 30-iterators-protocols-deep: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. __len__ + __getitem__ unlock the whole Sequence API")
        print("2. The __hash__/__eq__ contract protects dicts and caches")
        print("3. __getattr__ is for missing attributes only")
        print("4. collections.abc turns two dunders into a full interface")
        _verify()
