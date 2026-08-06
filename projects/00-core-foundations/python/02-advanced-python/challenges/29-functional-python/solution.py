"""Challenge 29 solution — reference implementation with reasoning comments.

The whole challenge is one idea: pure functions compose and cache.
pipeline() is built from pure map transforms; cacheable_pipeline()
keys on (data-fingerprint, steps-fingerprint) so identical work is
done exactly once.
"""
from __future__ import annotations

from typing import Callable


# --- Bronze -----------------------------------------------------------------

def square_evens(numbers: list[int]) -> list[int]:
    """Return squares of even inputs via map+filter; never mutate input.

    map/filter over a list is lazy and O(1) extra memory; list() forces
    the result. No element of `numbers` is ever written to.
    """
    return list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, numbers)))


# --- Silver -----------------------------------------------------------------

def compose(g: Callable, f: Callable) -> Callable:
    """Return a function computing g(f(x)). O(1) per call wrapper."""
    def composed(x):
        return g(f(x))
    return composed


def memoize(fn: Callable) -> Callable:
    """Return a pure wrapper that caches results by argument tuple.

    Why key by argument tuple: that is the function's full observable
    input for a pure fn, so the cache cannot go stale. The wrapper is
    pure — same args, same result, only faster on repeats.
    """
    cache: dict[tuple, object] = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = fn(*args)
        cache[args] = result
        return result

    return wrapper


def _normalize(x: int) -> int:
    """Pure: negatives to zero."""
    return x if x >= 0 else 0


def _double(x: int) -> int:
    """Pure: double the value."""
    return x * 2


def _square(x: int) -> int:
    """Pure: square the value."""
    return x * x


def pipeline(data: list[int]) -> list[int]:
    """Apply normalize -> double -> square as pure maps.

    Each map produces a fresh list; the input `data` is never touched.
    O(n) time per stage, O(n) memory total.
    """
    return list(map(_square, map(_double, map(_normalize, data))))


# --- Gold -------------------------------------------------------------------

# Cache is module-level ON PURPOSE: "a repeat call" means a repeat call to
# cacheable_pipeline with equal (steps, data), not a repeat inside one
# invocation. Module-level state is the imperative-shell exception the
# functional pattern tolerates — it is the cache, not the computation.
_CACHE: dict[tuple, list[int]] = {}


def steps_fingerprint(steps: list[Callable]) -> tuple:
    """Return a stable, hashable identity for a list of callables.

    __qualname__ is stable within a process and across module reloads,
    unlike id(), which varies per run. Order matters: reversing the
    step list changes the fingerprint.
    """
    return tuple(getattr(fn, "__qualname__", repr(fn)) for fn in steps)


def cacheable_pipeline(steps: list[Callable], data: list[int]) -> list[int]:
    """Apply steps in order; cache the result by fingerprint of steps+data.

    The key is (steps_fingerprint, tuple(data)): both inputs fully
    identified, so a repeat call with equal data and equal steps skips
    every step. Pure with respect to its inputs: reads only, writes
    only the cache dict.
    """
    key = (steps_fingerprint(steps), tuple(data))
    if key in _CACHE:
        return _CACHE[key]
    result: list[int] = list(data)
    for step in steps:
        result = list(map(step, result))
    _CACHE[key] = result
    return result
