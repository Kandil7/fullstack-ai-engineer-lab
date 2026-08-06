"""Challenge 32: Dtype Decisions — correctness, edge cases, memory.

Run from the module root:
    python -m pytest 03-libraries/numpy/challenges/32-dtypes-and-precision/test_challenge.py -v
"""

import ast
import importlib.util
import os
import tracemalloc

import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Unique module names per challenge dir: several test files share the
# filenames solution.py/starter.py, and sys.modules caching would make
# the first import win when pytest runs multiple challenge dirs at once.
solution = _load("solution_32", os.path.join(HERE, "solution.py"))
starter = _load("starter_32", os.path.join(HERE, "starter.py"))


# ---------------------------------------------------------------- helpers

def _assert_no_python_loops(mod):
    """Reject for/while loops and comprehensions in either module."""
    for name in ("starter", "solution"):
        tree = ast.parse(
            open(os.path.join(HERE, name + ".py"), encoding="utf-8").read()
        )
        banned = [
            n
            for n in ast.walk(tree)
            if isinstance(
                n, (ast.For, ast.While, ast.ListComp, ast.DictComp,
                    ast.SetComp, ast.GeneratorExp)
            )
        ]
        assert not banned, f"{name}.py contains Python loops/comprehensions"


def _call_peak(fn, *args):
    """Return (result, peak_bytes) measured with tracemalloc."""
    tracemalloc.start()
    result = fn(*args)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak


# ---------------------------------------------------------------- bronze

BRONZE_CASES = [
    (np.array([0, 1, -1, 127]), np.int8),
    (np.array([0, 1, -1, 128]), np.int16),
    (np.array([300, -300]), np.int16),
    (np.array([100_000]), np.int32),
    (np.array([3_000_000_000]), np.int64),
]


@pytest.mark.parametrize("values,dtype", BRONZE_CASES)
def test_bronze_smallest_safe_dtype(values, dtype):
    out = solution.int_downcast(values)
    assert out.dtype == dtype
    assert np.array_equal(out.astype(np.int64), values.astype(np.int64))


@pytest.mark.parametrize("low,high,dtype", [
    (-128, 128, np.int8),
    (-32768, 32768, np.int16),
    (-(2**31), 2**31, np.int32),
    (-(2**63), 2**63 - 1, np.int64),
])
def test_bronze_random_ranges(low, high, dtype):
    rng = np.random.default_rng(42)
    values = rng.integers(low, high, size=50, dtype=np.int64)
    out = solution.int_downcast(values)
    assert out.dtype == dtype


def test_bronze_rejects_non_integer():
    with pytest.raises(ValueError):
        solution.int_downcast(np.array([0.0, 1.0, 2.0]))


def test_bronze_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- silver

def test_silver_basic_mixed_non_finite():
    X = np.array([1.0, np.nan, np.inf, -np.inf, 2.0])
    cleaned, n_bad = solution.sanitize(X, fill=0.0)
    assert n_bad == 3
    assert np.array_equal(cleaned, [1.0, 0.0, 0.0, 0.0, 2.0])


def test_silver_seeded_corruption_count():
    rng = np.random.default_rng(7)
    X = rng.normal(size=(1000, 8))
    flat = X.ravel()
    bad = rng.choice(flat.size, size=37, replace=False)
    flat[bad[::3]] = np.nan
    flat[bad[1::3]] = np.inf
    flat[bad[2::3]] = -np.inf
    cleaned, n_bad = solution.sanitize(X, fill=-1.0)
    assert n_bad == 37
    assert np.all(np.isfinite(cleaned))


def test_silver_all_finite_returns_copy_with_zero_count():
    X = np.arange(12.0).reshape(3, 4)
    cleaned, n_bad = solution.sanitize(X, fill=5.0)
    assert n_bad == 0
    assert cleaned is not X
    assert np.array_equal(cleaned, X)


def test_silver_preserves_dtype():
    X = np.array([1.0, np.nan], dtype=np.float32)
    cleaned, _ = solution.sanitize(X, fill=0.0)
    assert cleaned.dtype == np.float32


def test_silver_memory_bounded():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(500, 2000))  # 8 MB float64
    X.ravel()[::97] = np.nan
    _, peak = _call_peak(solution.sanitize, X, 0.0)
    assert peak < 2.5 * X.nbytes, f"peak {peak} bytes for {X.nbytes} input"


def test_silver_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- gold

def _gold_weights(seed=42):
    """Normal weights shifted away from zero: avoids float16 subnormals,
    where relative error explodes (that explosion is correct behavior,
    but it would poison these tests' budgets)."""
    rng = np.random.default_rng(seed)
    return (rng.normal(size=(1024, 1024)) + 1.0).astype(np.float32)


def test_gold_normal_weights_cast_with_loose_budget():
    out = solution.serving_cast(_gold_weights(), budget=0.01)
    assert out.dtype == np.float16


def test_gold_normal_weights_kept_with_tight_budget():
    w = _gold_weights()
    out = solution.serving_cast(w, budget=1e-4)
    assert out is w  # no copy on the keep path
    assert out.dtype == np.float32


def test_gold_zeros_are_exact():
    w = np.zeros((1024, 1024), dtype=np.float32)
    out = solution.serving_cast(w, budget=1e-4)
    assert out.dtype == np.float16  # error is exactly 0


def test_gold_already_float16_returns_same_object():
    w = np.zeros(64, dtype=np.float16)
    assert solution.serving_cast(w, budget=0.0) is w


def test_gold_float64_input_casts():
    rng = np.random.default_rng(11)
    w = rng.normal(size=(512, 512))
    out = solution.serving_cast(w, budget=0.01)
    assert out.dtype == np.float16


def test_gold_cast_error_stays_within_budget():
    budget = 0.01
    out = solution.serving_cast(_gold_weights(), budget=budget)
    err = np.abs(out.astype(np.float32) - _gold_weights()) / (np.abs(_gold_weights()) + 1e-30)
    assert float(err.max()) < budget


@pytest.mark.parametrize("budget", [0.01, 1e-4])
def test_gold_memory_bounded(budget):
    w = _gold_weights()  # 4 MB
    _, peak = _call_peak(solution.serving_cast, w, budget)
    assert peak < 3 * w.nbytes, f"peak {peak} bytes for {w.nbytes} input"


def test_gold_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- starter

def test_starter_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        starter.int_downcast(np.array([1, 2, 3]))
    with pytest.raises(NotImplementedError):
        starter.sanitize(np.array([1.0, np.nan]), 0.0)
    with pytest.raises(NotImplementedError):
        starter.serving_cast(np.zeros(4, dtype=np.float32), 0.01)
