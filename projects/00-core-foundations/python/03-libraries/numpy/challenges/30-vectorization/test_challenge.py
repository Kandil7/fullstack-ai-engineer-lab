"""
Challenge 30: Vectorize the Given Loop — Hidden Tests
=======================================================
Correctness with np.allclose, edge cases (empty, single, uniform,
extreme values), and deterministic performance guards: AST operation
counting (no Python loops/comprehensions) and tracemalloc peak memory
for Gold. Never wall-clock.
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
    """Reject for/while loops and comprehensions in the function body."""
    src = textwrap.dedent(inspect.getsource(func))
    tree = ast.parse(src)
    for node in ast.walk(tree):
        assert not isinstance(
            node, (ast.For, ast.While, ast.ListComp, ast.SetComp,
                   ast.DictComp, ast.GeneratorExp)
        ), f"{func.__name__} must be vectorized: no Python loops"


class TestStarterRaises:
    def test_starter_sigmoid(self):
        with pytest.raises(NotImplementedError):
            starter.sigmoid(np.array([0.0]))

    def test_starter_clean_scores(self):
        with pytest.raises(NotImplementedError):
            starter.clean_scores(np.array([0.5]), -1.0, 1.0)

    def test_starter_softmax_rows(self):
        with pytest.raises(NotImplementedError):
            starter.softmax_rows(np.ones((2, 3)))


class TestSigmoid:
    def test_known_values(self):
        out = solution.sigmoid(np.array([0.0, 1.0, -1.0]))
        assert np.allclose(out, [0.5, 0.73105858, 0.26894142])

    def test_matches_loop_reference(self):
        rng = np.random.default_rng(42)
        X = rng.normal(size=(100, 8))
        out = solution.sigmoid(X)
        ref = np.empty_like(X)
        for i in range(X.size):
            ref.flat[i] = 1.0 / (1.0 + np.exp(-X.flat[i]))
        assert np.allclose(out, ref, atol=1e-12)

    def test_output_bounds(self):
        # At |x| > ~37, 1 + exp(-x) rounds to 1.0 in float64, so the
        # strict < 1 bound only holds on a moderate range.
        X = np.linspace(-30, 30, 10_000)
        out = solution.sigmoid(X)
        assert np.all((out > 0) & (out < 1))

    def test_empty(self):
        out = solution.sigmoid(np.zeros((0, 3)))
        assert out.shape == (0, 3)

    def test_shape_preserved(self):
        out = solution.sigmoid(np.ones((4, 5, 6)))
        assert out.shape == (4, 5, 6)


class TestCleanScores:
    def test_known_values(self):
        scores = np.array([0.5, -0.005, 2.0, 0.0])
        out = solution.clean_scores(scores, -1.0, 1.0)
        assert np.allclose(out, [0.5, 0.0, 1.0, 0.0])

    def test_matches_reference(self):
        rng = np.random.default_rng(7)
        scores = rng.normal(scale=0.5, size=100_000)
        out = solution.clean_scores(scores, -1.0, 1.0)
        ref = np.empty_like(scores)
        for i in range(scores.size):
            v = max(min(scores[i], 1.0), -1.0)
            ref[i] = 0.0 if abs(scores[i]) < 0.01 else v
        assert np.allclose(out, ref)

    def test_zero_out_small(self):
        out = solution.clean_scores(np.array([0.009, 0.011]), -1.0, 1.0)
        assert out[0] == 0.0 and np.isclose(out[1], 0.011)

    def test_empty(self):
        out = solution.clean_scores(np.zeros(0), -1.0, 1.0)
        assert out.shape == (0,)

    def test_no_python_loops(self):
        assert_no_python_loops(solution.clean_scores)


class TestSoftmaxRows:
    def test_known_values(self):
        out = solution.softmax_rows(np.array([[1.0, 2.0, 3.0]]))
        assert np.allclose(out, [[0.09003057, 0.24472847, 0.66524096]],
                           atol=1e-8)

    def test_rows_sum_to_one(self):
        rng = np.random.default_rng(3)
        X = rng.normal(size=(20, 10))
        out = solution.softmax_rows(X)
        assert np.allclose(out.sum(axis=1), 1.0, atol=1e-10)

    def test_all_equal_row_is_uniform(self):
        out = solution.softmax_rows(np.array([[5.0, 5.0, 5.0]]))
        assert np.allclose(out, [[1.0 / 3] * 3])

    def test_stability_against_overflow(self):
        """exp(1000) overflows to inf without max-subtraction;
        the stable version must return finite uniform rows."""
        X = np.array([[1000.0, 1000.0, 1000.0]])
        out = solution.softmax_rows(X)
        assert np.all(np.isfinite(out))
        assert np.allclose(out.sum(axis=1), 1.0)

    def test_matches_loop_reference(self):
        rng = np.random.default_rng(9)
        X = rng.normal(size=(20, 8))
        out = solution.softmax_rows(X)
        ref = np.empty_like(X)
        for i in range(X.shape[0]):
            e = np.exp(X[i] - X[i].max())
            ref[i] = e / e.sum()
        assert np.allclose(out, ref, atol=1e-12)

    def test_empty_and_single(self):
        assert solution.softmax_rows(np.zeros((0, 4))).shape == (0, 4)
        single = solution.softmax_rows(np.array([[7.0, 7.0]]))
        assert np.allclose(single, [[0.5, 0.5]])

    def test_memory_bounded_at_scale(self):
        """n=50000, d=64 float32: X alone is ~12.8 MB. Peak must stay
        under 100 MB -- implementations that allocate a full-size
        temporary per stage pass; anything loop-emulating blows past."""
        rng = np.random.default_rng(11)
        X = rng.normal(size=(50_000, 64)).astype(np.float32)
        tracemalloc.start()
        try:
            out = solution.softmax_rows(X)
            _current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        assert out.shape == (50_000, 64)
        assert peak < 100 * 1024 * 1024, \
            f"peak memory {peak / 1e6:.0f} MB exceeds 100 MB limit"

    def test_no_python_loops(self):
        assert_no_python_loops(solution.softmax_rows)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
