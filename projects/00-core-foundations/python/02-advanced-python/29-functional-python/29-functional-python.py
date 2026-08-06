"""
Advanced Python — 29: Functional Python
=========================================
Topics: pure functions, referential transparency, frozen dataclasses,
map/filter/reduce vs comprehensions, operator module, partial currying,
composition, itertools toolkit, recursion limits, functional-core/
imperative-shell

Why this matters for AI/backend engineering:
    A preprocessing pipeline is a chain of transforms. If each transform is
    pure (same input -> same output, no hidden state), the pipeline is
    testable, cacheable, and reorder-safe: you can memoize embeddings,
    replay any stage, and parallelize without shared-state bugs. This file
    builds the vocabulary and the machinery for that style.

Run:      python 29-functional-python.py
Verify:   python 29-functional-python.py --verify
Reference: https://docs.python.org/3/library/functools.html
"""

from __future__ import annotations

import functools
import itertools
import operator
import sys
from dataclasses import dataclass
from typing import Callable, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


# ============================================================
# 1. Pure Functions and Referential Transparency
# ============================================================
# A pure function: same arguments -> same result, no observable side
# effects. Referential transparency means any call can be replaced by
# its result without changing the program. That property is what makes
# caching and reordering safe.

# Example 1: pure vs impure
def pure_square(x: int) -> int:
    """Return x squared. No state, no I/O."""
    return x * x


_counter = {"calls": 0}

def impure_square(x: int) -> int:
    """Return x squared but count calls — a hidden side effect."""
    _counter["calls"] += 1
    return x * x


print(f"pure: {pure_square(4)}; impure: {impure_square(4)}; "
      f"hidden state: {_counter['calls']}")

# Output:
# pure: 16; impure: 16; hidden state: 1


# ============================================================
# 2. Frozen Dataclasses (Immutability)
# ============================================================
# Immutable data is the structural guarantee behind pure functions:
# a frozen object cannot be changed after construction, so it is safe
# to share across threads and safe to use as a dict key.

@dataclass(frozen=True)
class Chunk:
    """An immutable retrieved text chunk with its source id."""
    doc_id: int
    text: str
    score: float


# Example 2: frozen dataclasses are hashable and refuse mutation
c = Chunk(doc_id=1, text="attention is all you need", score=0.9)
cache: dict[Chunk, str] = {c: "cached"}
print(f"frozen instance: {c}")
print(f"usable as dict key? {Chunk(doc_id=1, text='x', score=0.1) in {c}}")
try:
    c.score = 0.1  # type: ignore[misc]  # frozen -> FrozenInstanceError
except AttributeError as exc:
    print(f"mutation refused: {type(exc).__name__}")

# Output:
# frozen instance: Chunk(doc_id=1, text='attention is all you need', score=0.9)
# usable as dict key? False
# mutation refused: FrozenInstanceError


# ============================================================
# 3. map/filter/reduce vs Comprehensions
# ============================================================
# map and filter are lazy and compact; comprehensions read better for
# anything but the simplest one-liner. Both are pure when the mapped
# function is pure. Complexity: O(n) time, O(1) memory (lazy) vs O(n)
# memory for the list comprehension.

# Example 3: the same transform, three notations
nums = [1, 2, 3, 4, 5, 6]

mapped = list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, nums)))
comprehended = [x * 2 for x in nums if x % 2 == 0]
print(f"map/filter:   {mapped}")
print(f"comprehension: {comprehended}")
print(f"equal? {mapped == comprehended}")

# Output:
# map/filter:   [4, 8, 12]
# comprehension: [4, 8, 12]
# equal? True


# ============================================================
# 4. The operator Module
# ============================================================
# operator.* turns operators into first-class functions, so you can
# pass them to map/sort/reduce without lambdas.

# Example 4: operator functions where lambdas would add noise
rows = [("b", 2), ("a", 3), ("c", 1)]
rows_sorted = sorted(rows, key=operator.itemgetter(1))
print(f"sorted by second field: {rows_sorted}")

total = functools.reduce(operator.add, [1, 2, 3, 4])
print(f"reduce with operator.add: {total}")

# Output:
# sorted by second field: [('c', 1), ('b', 2), ('a', 3)]
# reduce with operator.add: 10


# ============================================================
# 5. Partial Application and Currying
# ============================================================
# partial fixes leading arguments, producing a new pure function.
# Currying turns f(a, b) into f(a)(b); both are "function factories".

# Example 5: partial as a config-free retriever factory
def fetch_with(page_size: int, offset: int, limit: int) -> int:
    """Simulated page request: return how many rows would be fetched."""
    return min(limit - offset, page_size)


page_50 = functools.partial(fetch_with, 50)
print(f"partial applied: {page_50(offset=0, limit=200)}")

# Output:
# partial applied: 50


# ============================================================
# 6. Composition
# ============================================================
# compose chains pure functions right-to-left: compose(g, f)(x) == g(f(x)).
# Associativity: compose(f, compose(g, h)) == compose(compose(f, g), h).
# This is the algebra that makes pipelines reorderable.

def compose(g: Callable[[B], C], f: Callable[[A], B]) -> Callable[[A], C]:
    """Return g after f: (compose(g, f))(x) == g(f(x)). O(1) wrapper."""
    def composed(x: A) -> C:
        return g(f(x))
    return composed


def double(x: int) -> int:
    """Pure: x * 2."""
    return x * 2


def increment(x: int) -> int:
    """Pure: x + 1."""
    return x + 1


# Example 6: composed pipeline applied
pipeline = compose(double, increment)   # (x + 1) * 2
print(f"compose(double, increment)(3) = {pipeline(3)}")

# Output:
# compose(double, increment)(3) = 8


# ============================================================
# 7. itertools as the Functional Toolkit
# ============================================================
# itertools is the standard library's functional battery: lazy, O(1)
# memory, infinite streams supported. groupby REQUIRES pre-sorted input
# (the classic trap).

# Example 7: lazy chains and grouping
pairs = [("en", 1), ("en", 2), ("fr", 3)]
for key, group in itertools.groupby(pairs, key=operator.itemgetter(0)):
    print(f"group {key}: {[item for _, item in group]}")

# Output:
# group en: [1, 2]
# group fr: [3]


# ============================================================
# 8. Recursion and Python's Limit
# ============================================================
# Python has no tail-call optimization: every call consumes stack.
# Recursion limit is ~1000 by default. Deep recursion raises
# RecursionError — iterate instead. Complexity: O(n) time but O(n)
# stack space, which is why deep recursion is a memory bug.

def factorial_iter(n: int) -> int:
    """Iterative factorial: O(n) time, O(1) space. Safe for any n."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# Example 8: recursion dies at depth; iteration does not
def factorial_rec(n: int) -> int:
    """Recursive factorial: O(n) stack — dies around depth 1000."""
    return 1 if n <= 1 else n * factorial_rec(n - 1)


print(f"iterative factorial(5) = {factorial_iter(5)}")
print(f"recursive factorial(5) = {factorial_rec(5)}")
try:
    factorial_rec(10_000)
except RecursionError as exc:
    print(f"recursion at 10000: {type(exc).__name__}")

# Output:
# iterative factorial(5) = 120
# recursive factorial(5) = 120
# recursion at 10000: RecursionError


# ============================================================
# 9. Production Pattern: Functional Core, Imperative Shell
# ============================================================
# Keep the pipeline pure (functional core); push I/O and state to the
# edges (imperative shell). The core is memoizable and testable; the
# shell handles files, network, and user interaction.

@dataclass(frozen=True)
class TextSample:
    """Immutable unit of corpus data."""
    text: str
    label: str


def normalize(sample: TextSample) -> TextSample:
    """Pure: lower-case text, strip whitespace. Returns a NEW instance."""
    return TextSample(text=sample.text.strip().lower(), label=sample.label)


def tokenize(text: str) -> tuple[str, ...]:
    """Pure: split on whitespace into a hashable tuple."""
    return tuple(text.split())


def process_corpus(samples: list[TextSample]) -> dict[str, tuple[str, ...]]:
    """Functional core: pure pipeline, no I/O. O(n) time, O(n) space."""
    return {s.label: tokenize(normalize(s).text) for s in samples}


# Example 9: the core is pure; the shell would read files/print results
raw = [TextSample(text="  Hello World ", label="greeting")]
print(f"core output: {process_corpus(raw)}")

# Output:
# core output: {'greeting': ('hello', 'world')}


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: mutating inputs inside a "pure" transform
#   def scale(samples, factor):      # BAD - caller's list changes
#       for s in samples: s.score *= factor
# CORRECT: build new objects (frozen dataclasses force this)
#   def scale(sample, factor): return Chunk(sample.doc_id, sample.text,
#                                           sample.score * factor)
#
# MISTAKE: relying on recursion for deep structures
#   factorial_rec(10_000)  # RecursionError; Python has no TCO
# CORRECT: iterate, or reduce the problem size
#
# MISTAKE: groupby on unsorted data
#   itertools.groupby(items, key)  # silently splits repeated keys
# CORRECT: sort by the key first, then group


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # --- composition associativity ---
    add3 = compose(compose(increment, increment), increment)
    via_left = compose(increment, compose(increment, increment))
    assert add3(0) == 3 and via_left(0) == 3, \
        "compose must be associative: f.(g.h) == (f.g).h"

    # --- pure functions are memoizable ---
    calls = {"n": 0}

    @functools.lru_cache(maxsize=None)
    def memo_pure(x: int) -> int:
        """Pure function instrumented with a call counter."""
        calls["n"] += 1
        return pure_square(x)

    assert memo_pure(7) == 49 and memo_pure(7) == 49, \
        "pure function must return the same value on repeated calls"
    assert calls["n"] == 1, \
        "a pure function memoized must be computed only once"

    # --- pure transforms are reorder-safe ---
    def lowercase(s: str) -> str:
        """Pure: lowercase a string."""
        return s.lower()

    def strip_ws(s: str) -> str:
        """Pure: strip surrounding whitespace."""
        return s.strip()

    start = "  Hello  "
    assert strip_ws(lowercase(start)) == lowercase(strip_ws(start)) == "hello", \
        "commuting pure transforms must give the same result"

    # --- immutable structures are hashable ---
    key = Chunk(doc_id=1, text="alpha", score=0.5)
    table: dict[Chunk, str] = {key: "v"}
    assert table[Chunk(doc_id=1, text="alpha", score=0.5)] == "v", \
        "a frozen dataclass must be usable as a dict key"

    # --- frozen dataclasses refuse mutation ---
    try:
        key.score = 9.9  # type: ignore[misc]
        raise AssertionError("frozen dataclass must refuse attribute writes")
    except AttributeError:
        pass

    # --- map/filter equals comprehension ---
    evens_doubled = list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0,
                                                     [1, 2, 3, 4, 5, 6])))
    assert evens_doubled == [4, 8, 12], \
        "map/filter must equal the comprehension form"

    # --- operator module as first-class functions ---
    assert functools.reduce(operator.add, [1, 2, 3, 4]) == 10, \
        "operator.add must reduce a list to its sum"
    assert sorted([("b", 2), ("a", 3)], key=operator.itemgetter(1)) == \
        [("b", 2), ("a", 3)], "itemgetter must sort by the given field"

    # --- partial application ---
    page_50 = functools.partial(fetch_with, 50)
    assert page_50(offset=0, limit=200) == 50, \
        "partial must pre-bind the leading argument"

    # --- recursion limit is real ---
    try:
        factorial_rec(10_000)
        raise AssertionError("deep recursion must raise RecursionError")
    except RecursionError:
        pass
    assert factorial_iter(20) == 2_432_902_008_176_640_000, \
        "iterative factorial must handle deep inputs"

    # --- functional core / imperative shell ---
    assert process_corpus([TextSample(text="  Hi There ", label="x")]) == \
        {"x": ("hi", "there")}, \
        "the pure core must normalize and tokenize deterministically"

    print("[OK] 29-functional-python: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Pure functions make pipelines testable, memoizable, reorder-safe")
        print("2. Frozen dataclasses enforce immutability at the type level")
        print("3. compose is associative; that algebra enables safe refactoring")
        print("4. Keep the core pure; push I/O to the imperative shell")
        _verify()
