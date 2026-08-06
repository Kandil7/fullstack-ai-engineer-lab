"""
Challenge 29: Functional Python — Hidden Tests
===============================================
Correctness + purity (no input mutation) + cache-hit operation guards.
"""
from __future__ import annotations

import importlib.util
import sys
import tracemalloc
from pathlib import Path

import pytest

HERE = Path(__file__).parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution")
starter = _load("starter")


# --- Bronze: square_evens ---------------------------------------------------

def test_bronze_basic():
    assert solution.square_evens([1, 2, 3, 4]) == [4, 16]


def test_bronze_empty():
    assert solution.square_evens([]) == []


def test_bronze_duplicates_preserved():
    assert solution.square_evens([2, 2]) == [4, 4]


def test_bronze_no_evens():
    assert solution.square_evens([1, 3, 5]) == []


def test_bronze_input_not_mutated():
    data = [1, 2, 3, 4]
    solution.square_evens(data)
    assert data == [1, 2, 3, 4], "pure transform must not mutate input"


# --- Silver: compose / memoize / pipeline -----------------------------------

def test_silver_compose_order():
    double = lambda x: x * 2  # noqa: E731
    square = lambda x: x * x  # noqa: E731
    assert solution.compose(square, double)(3) == 36
    assert solution.compose(double, square)(3) == 18


def test_silver_pipeline_expected():
    assert solution.pipeline([1, -2, 3]) == [4, 0, 36]


def test_silver_pipeline_pure():
    data = [1, -2, 3]
    assert solution.pipeline(data) == solution.pipeline(data)
    assert data == [1, -2, 3], "pipeline must not mutate its input"


def test_silver_memoize_returns_same_value():
    memoized = solution.memoize(lambda x: x * 10)
    assert memoized(4) == 40
    assert memoized(4) == 40


def test_silver_memoize_computes_once():
    calls = {"n": 0}

    def count(x: int) -> int:
        calls["n"] += 1
        return x + 1

    memoized = solution.memoize(count)
    assert memoized(1) == 2
    assert memoized(1) == 2
    assert memoized(2) == 3
    assert calls["n"] == 2, "same argument must not re-invoke the function"


# --- Gold: steps_fingerprint / cacheable_pipeline ---------------------------

def _double(x: int) -> int:
    return x * 2


def _square(x: int) -> int:
    return x * x


def test_gold_fingerprint_order_sensitive():
    assert solution.steps_fingerprint([_double, _square]) != \
        solution.steps_fingerprint([_square, _double])


def test_gold_fingerprint_stable():
    assert solution.steps_fingerprint([_double, _square]) == \
        solution.steps_fingerprint([_double, _square])


def test_gold_correctness():
    assert solution.cacheable_pipeline([_double, _square], [1, 2]) == [4, 16]
    assert solution.cacheable_pipeline([_square, _double], [1, 2]) == [2, 8]


def test_gold_second_call_runs_zero_steps():
    calls = {"n": 0}

    def counting(step: str) -> Callable:
        def fn(x: int) -> int:
            calls["n"] += 1
            return x * 2
        return fn

    from typing import Callable  # noqa: F401 - re-export for annotation
    steps = [counting("a"), counting("b")]
    first = solution.cacheable_pipeline(steps, [1, 2, 3])
    assert first == [4, 8, 12]
    calls_before = calls["n"]
    second = solution.cacheable_pipeline(steps, [1, 2, 3])
    assert second == first
    assert calls["n"] == calls_before, \
        "repeat call with equal data must not re-run any step"


def test_gold_pure():
    data = [1, -3, 5]
    out1 = solution.cacheable_pipeline([_double], data)
    out2 = solution.cacheable_pipeline([_double], data)
    assert out1 == out2
    assert data == [1, -3, 5], "cacheable_pipeline must not mutate input"


def test_gold_memory_guard():
    big = list(range(50_000))
    tracemalloc.start()
    solution.cacheable_pipeline([_double, _square], big)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak < 8_000_000, f"peak {peak} bytes exceeds 8 MB budget"


# --- Starter must be unimplemented -----------------------------------------

def test_starter_not_implemented():
    with pytest.raises(NotImplementedError):
        starter.square_evens([1, 2])
    with pytest.raises(NotImplementedError):
        starter.compose(lambda x: x, lambda x: x)
    with pytest.raises(NotImplementedError):
        starter.memoize(lambda x: x)
    with pytest.raises(NotImplementedError):
        starter.pipeline([1])
    with pytest.raises(NotImplementedError):
        starter.steps_fingerprint([_double])
    with pytest.raises(NotImplementedError):
        starter.cacheable_pipeline([_double], [1])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
