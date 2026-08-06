"""Challenge 33: Linear Algebra — correctness, edge cases, memory.

Run from the module root:
    python -m pytest 03-libraries/numpy/challenges/33-linear-algebra/test_challenge.py -v
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
solution = _load("solution_33", os.path.join(HERE, "solution.py"))
starter = _load("starter_33", os.path.join(HERE, "starter.py"))


# ---------------------------------------------------------------- helpers

def _assert_no_python_loops(mod):
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
    tracemalloc.start()
    result = fn(*args)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak


def _manual_cosine(X):
    """Reference cosine matrix computed pairwise (tests may loop)."""
    n = X.shape[0]
    out = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            out[i, j] = float(np.dot(X[i], X[j]) /
                              (np.linalg.norm(X[i]) * np.linalg.norm(X[j])))
    return out


# ---------------------------------------------------------------- bronze

def test_bronze_orthogonal_rows():
    X = np.array([[1.0, 0.0], [0.0, 1.0]])
    S = solution.cosine_matrix(X)
    assert np.allclose(S, [[1.0, 0.0], [0.0, 1.0]], atol=1e-12)


def test_bronze_collinear_rows():
    X = np.array([[2.0, 0.0], [4.0, 0.0]])
    S = solution.cosine_matrix(X)
    assert np.allclose(S, [[1.0, 1.0], [1.0, 1.0]], atol=1e-12)


def test_bronze_matches_manual_cosine():
    rng = np.random.default_rng(42)
    X = rng.normal(size=(6, 4))
    assert np.allclose(solution.cosine_matrix(X), _manual_cosine(X), atol=1e-12)


def test_bronze_large_seeded_properties():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(50, 32))
    S = solution.cosine_matrix(X)
    assert np.allclose(np.diag(S), 1.0, atol=1e-12)
    assert np.allclose(S, S.T, atol=1e-12)
    assert S.min() >= -1.0 - 1e-12 and S.max() <= 1.0 + 1e-12


def test_bronze_memory_linear():
    # Output is O(n^2) = 32 MB for (2000, 64); the contract is
    # "no extra full-size copies": peak < input + 3 x output.
    rng = np.random.default_rng(1)
    X = rng.normal(size=(2000, 64))          # ~1 MB
    S = solution.cosine_matrix(X)
    _, peak = _call_peak(solution.cosine_matrix, X)
    assert peak < X.nbytes + 3 * S.nbytes


def test_bronze_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- silver

def test_silver_clean_cubic_exact():
    t = np.linspace(-2.0, 2.0, 50)
    truth = np.array([1.0, 2.0, -3.0, 0.5])
    y = np.polynomial.polynomial.polyval(t, truth)
    coef = solution.fit_polynomial(t, y, 3)
    assert np.allclose(coef, truth, atol=1e-6)


def test_silver_noisy_line():
    rng = np.random.default_rng(7)
    t = np.linspace(0.0, 1.0, 40)
    y = 3.0 + 2.0 * t + rng.normal(scale=0.05, size=t.size)
    coef = solution.fit_polynomial(t, y, 1)
    assert abs(coef[0] - 3.0) < 0.2
    assert abs(coef[1] - 2.0) < 0.2


def test_silver_overfit_degree_returns_long_vector():
    rng = np.random.default_rng(7)
    t = np.linspace(0.0, 1.0, 40)
    y = 3.0 + 2.0 * t + rng.normal(scale=0.05, size=t.size)
    coef = solution.fit_polynomial(t, y, 5)
    assert coef.shape == (6,)
    resid_high = np.linalg.norm(
        np.polynomial.polynomial.polyval(t, coef) - y)
    resid_low = np.linalg.norm(
        np.polynomial.polynomial.polyval(
            t, solution.fit_polynomial(t, y, 1)) - y)
    assert resid_high <= resid_low + 1e-12


def test_silver_exact_interpolation():
    t = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([1.0, -2.0, 5.0, 10.0])
    coef = solution.fit_polynomial(t, y, 3)
    assert np.allclose(np.polynomial.polynomial.polyval(t, coef), y, atol=1e-6)


def test_silver_memory_ok():
    t = np.linspace(0.0, 1.0, 20000)
    y = 1.0 + t + t ** 2
    _, peak = _call_peak(solution.fit_polynomial, t, y, 5)
    assert peak < 20 * t.nbytes


def test_silver_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- gold

def _gold_matrix(seed=42, shape=(64, 64)):
    return np.random.default_rng(seed).normal(size=shape)


def test_gold_huge_budget_is_full_rank():
    A = _gold_matrix()
    approx, k = solution.compress_svd(A, max_bytes=10**12)
    assert k == 64
    assert np.allclose(approx, A, atol=1e-12)


def test_gold_exact_rank_budget():
    A = _gold_matrix()
    target_k = 5
    max_bytes = 8 * (64 + 64 + 1) * target_k
    approx, k = solution.compress_svd(A, max_bytes=max_bytes)
    assert k == target_k
    s = np.linalg.svd(A, compute_uv=False)
    err = np.linalg.norm(A - approx)
    assert np.allclose(err, np.sqrt(np.sum(s[k:] ** 2)), rtol=1e-6)


def test_gold_smallest_budget_rank_one():
    A = _gold_matrix(seed=3, shape=(32, 48))
    approx, k = solution.compress_svd(A, max_bytes=8 * (32 + 48 + 1))
    assert k == 1
    U, s, Vh = np.linalg.svd(A)
    assert np.allclose(approx, (U[:, :1] * s[:1]) @ Vh[:1, :], atol=1e-12)


def test_gold_rejects_impossible_budget():
    A = _gold_matrix(shape=(16, 16))
    with pytest.raises(ValueError):
        solution.compress_svd(A, max_bytes=8 * (16 + 16 + 1) - 1)


def test_gold_error_stays_within_full_spectrum():
    A = _gold_matrix(seed=11)
    approx, k = solution.compress_svd(A, max_bytes=8 * (64 + 64 + 1) * 20)
    assert k <= 20
    assert np.linalg.norm(A - approx) <= np.linalg.norm(A)


def test_gold_memory_bounded():
    A = _gold_matrix(seed=42)                 # 32 KB float64
    _, peak = _call_peak(solution.compress_svd, A, 8 * (64 + 64 + 1) * 10)
    assert peak < 6 * A.nbytes, f"peak {peak} for {A.nbytes} input"


def test_gold_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- starter

def test_starter_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        starter.cosine_matrix(np.eye(3))
    with pytest.raises(NotImplementedError):
        starter.fit_polynomial(np.arange(5.0), np.arange(5.0), 1)
    with pytest.raises(NotImplementedError):
        starter.compress_svd(np.eye(4), 1000)
