"""
Challenge 29: Broadcasting Without Explicit Loops — Hidden Tests
=================================================================
Correctness with np.allclose, edge cases (empty/single/duplicates),
and deterministic performance guards: AST operation counting (no
Python loops or comprehensions in Silver/Gold solutions) and
tracemalloc peak-memory verification for Gold. Never wall-clock.
"""

from __future__ import annotations

import ast
import importlib.util
import inspect
import textwrap
import tracemalloc
from pathlib import Path

import numpy as np
import pytest

_DIR = Path(__file__).parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, _DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


starter = _load("starter")
solution = _load("solution")


def assert_no_python_loops(func) -> None:
    """Reject for/while loops and comprehensions in the function body.

    This is the deterministic operation-count guard: a vectorized
    solution contains no iteration constructs, so its AST cannot
    contain For/While nodes or comprehension expressions.
    """
    src = textwrap.dedent(inspect.getsource(func))
    tree = ast.parse(src)
    for node in ast.walk(tree):
        assert not isinstance(
            node, (ast.For, ast.While, ast.ListComp, ast.SetComp,
                   ast.DictComp, ast.GeneratorExp)
        ), f"{func.__name__} must be vectorized: no Python loops"


class TestStarterRaises:
    """Starter bodies must never contain working implementations."""

    def test_starter_add_bias(self):
        with pytest.raises(NotImplementedError):
            starter.add_bias(np.ones((2, 3)), np.ones(3))

    def test_starter_row_zscore(self):
        with pytest.raises(NotImplementedError):
            starter.row_zscore(np.ones((2, 3)))

    def test_starter_pairwise(self):
        with pytest.raises(NotImplementedError):
            starter.pairwise_distances(np.ones((2, 3)), np.ones((4, 3)))


class TestAddBias:
    def test_known_values(self):
        batch = np.array([[1.0, 2.0], [3.0, 4.0]])
        bias = np.array([10.0, 20.0])
        out = solution.add_bias(batch, bias)
        assert np.allclose(out, [[11.0, 22.0], [13.0, 24.0]])

    def test_shape_preserved(self):
        rng = np.random.default_rng(42)
        batch = rng.normal(size=(7, 3))
        bias = rng.normal(size=3)
        out = solution.add_bias(batch, bias)
        assert out.shape == (7, 3)
        assert np.allclose(out, batch + bias)

    def test_single_row(self):
        out = solution.add_bias(np.array([[1.0, 2.0]]), np.array([5.0, -1.0]))
        assert out.shape == (1, 2)
        assert np.allclose(out, [[6.0, 1.0]])

    def test_wrong_bias_length_raises(self):
        with pytest.raises(ValueError):
            solution.add_bias(np.ones((2, 3)), np.ones(4))

    def test_zero_bias_is_identity(self):
        batch = np.random.default_rng(1).normal(size=(4, 5))
        out = solution.add_bias(batch, np.zeros(5))
        assert np.array_equal(out, batch)


class TestRowZscore:
    def test_known_values(self):
        X = np.array([[1.0, 2.0, 3.0]])
        out = solution.row_zscore(X)
        # Population std (ddof=0): std([1,2,3]) = sqrt(2/3).
        assert np.allclose(out, [[-1.22474487, 0.0, 1.22474487]])

    def test_zero_std_row_becomes_zero(self):
        X = np.array([[1.0, 2.0, 3.0], [4.0, 4.0, 4.0]])
        out = solution.row_zscore(X)
        assert np.allclose(out[0], [-1.22474487, 0.0, 1.22474487])
        assert np.array_equal(out[1], [0.0, 0.0, 0.0]), \
            "zero-std rows must be zeroed, not nan"

    def test_random_rows_match_manual(self):
        rng = np.random.default_rng(7)
        X = rng.normal(size=(100, 8))
        out = solution.row_zscore(X)
        # Manual reference (Python loops allowed in the test).
        ref = np.empty_like(X)
        for i in range(X.shape[0]):
            ref[i] = (X[i] - X[i].mean()) / X[i].std()
        assert np.allclose(out, ref, atol=1e-12)

    def test_each_row_has_mean_zero_std_one(self):
        rng = np.random.default_rng(3)
        X = rng.normal(size=(100_000, 8))
        out = solution.row_zscore(X)
        assert out.shape == (100_000, 8)
        assert np.allclose(out.mean(axis=1), 0.0, atol=1e-12)
        assert np.allclose(out.std(axis=1), 1.0, atol=1e-12)

    def test_single_row_input(self):
        out = solution.row_zscore(np.array([[2.0, 2.0]]))
        assert out.shape == (1, 2)
        assert np.array_equal(out, [[0.0, 0.0]])

    def test_no_python_loops(self):
        assert_no_python_loops(solution.row_zscore)


class TestPairwiseDistances:
    def test_pythagoras(self):
        a = np.array([[0.0, 0.0]])
        b = np.array([[3.0, 4.0]])
        out = solution.pairwise_distances(a, b)
        assert np.allclose(out, [[5.0]])

    def test_matches_reference_formula(self):
        rng = np.random.default_rng(42)
        a = rng.normal(size=(20, 8))
        b = rng.normal(size=(30, 8))
        out = solution.pairwise_distances(a, b)
        assert out.shape == (20, 30)
        # Reference: explicit distance sum (small sizes only).
        ref = np.empty((20, 30))
        for i in range(20):
            for j in range(30):
                ref[i, j] = np.sqrt(np.sum((a[i] - b[j]) ** 2))
        assert np.allclose(out, ref, atol=1e-10)

    def test_zero_distance_for_identical(self):
        rng = np.random.default_rng(5)
        a = rng.normal(size=(10, 4))
        out = solution.pairwise_distances(a, a)
        # Squared-distance cancellation leaves ~1e-15 in sq; sqrt
        # amplifies it to ~1e-8 -- "approximately zero" is the claim.
        assert np.allclose(np.diag(out), 0.0, atol=1e-6)

    def test_symmetry(self):
        rng = np.random.default_rng(6)
        a = rng.normal(size=(25, 6))
        out = solution.pairwise_distances(a, a)
        assert np.allclose(out, out.T, atol=1e-12)

    def test_non_negative(self):
        rng = np.random.default_rng(8)
        a = rng.normal(size=(15, 5))
        b = rng.normal(size=(12, 5))
        out = solution.pairwise_distances(a, b)
        assert np.all(out >= 0.0)

    def test_empty_input(self):
        out = solution.pairwise_distances(np.zeros((0, 3)), np.ones((4, 3)))
        assert out.shape == (0, 4)

    def test_memory_bounded_at_scale(self):
        """n=m=2000, d=64: naive (n,m,d) route needs ~2 GB; the
        identity-based solution must stay far below 200 MB peak."""
        rng = np.random.default_rng(9)
        a = rng.normal(size=(2000, 64))
        b = rng.normal(size=(2000, 64))
        tracemalloc.start()
        try:
            out = solution.pairwise_distances(a, b)
            _current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        assert out.shape == (2000, 2000)
        assert peak < 200 * 1024 * 1024, \
            f"peak memory {peak / 1e6:.0f} MB exceeds 200 MB limit"

    def test_no_python_loops(self):
        assert_no_python_loops(solution.pairwise_distances)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
