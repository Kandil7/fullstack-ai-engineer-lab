"""Challenge 29 starter — fill in the bodies (never return working code)."""
from __future__ import annotations

from typing import Callable


def square_evens(numbers: list[int]) -> list[int]:
    """Return squares of even inputs via map+filter; never mutate input."""
    raise NotImplementedError


def compose(g: Callable, f: Callable) -> Callable:
    """Return a function computing g(f(x))."""
    raise NotImplementedError


def memoize(fn: Callable) -> Callable:
    """Return a pure wrapper that caches results by argument tuple."""
    raise NotImplementedError


def pipeline(data: list[int]) -> list[int]:
    """Apply normalize -> double -> square as pure maps."""
    raise NotImplementedError


def steps_fingerprint(steps: list[Callable]) -> tuple:
    """Return a stable, hashable identity for a list of callables."""
    raise NotImplementedError


def cacheable_pipeline(steps: list[Callable], data: list[int]) -> list[int]:
    """Apply steps in order; cache the result by fingerprint of steps+data."""
    raise NotImplementedError
