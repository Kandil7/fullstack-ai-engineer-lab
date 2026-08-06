"""
Challenge 31: Memory Contracts — Hidden Tests
===============================================
Correctness with np.allclose, aliasing proofs with np.shares_memory
and base, edge cases (empty, single column, non-contiguous, dtypes),
and deterministic memory guards with tracemalloc. Never wall-clock.
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
    def test_starter_column_view(self):
        with pytest.raises(NotImplementedError):
            starter.column_view(np.ones((3, 4)), 0)

    def test_starter_ensure_contiguous(self):
        with pytest.raises(NotImplementedError):
            starter.ensure_contiguous(np.ones((3, 4)))

    def test_starter_downcast(self):
        with pytest.raises(NotImplementedError):
            starter.downcast_when_safe(np.ones(3, dtype=np.float64))


class TestColumnView:
    def test_known_values(self):
        X = np.array([[1.0, 2.0], [3.0, 4.0]])
        out = solution.column_view(X, 1)
        assert np.array_equal(out, [2.0, 4.0])

    def test_is_a_view(self):
        X = np.random.default_rng(42).normal(size=(100, 8))
        out = solution.column_view(X, 3)
        assert np.shares_memory(X, out), "must be a view, not a copy"
        assert out.base is X, "view must share X's buffer"

    def test_write_propagates(self):
        X = np.zeros((10, 5))
        out = solution.column_view(X, 2)
        out[0] = 99.0
        assert X[0, 2] == 99.0, "write through view must reach X"

    def test_shape_and_dtype(self):
        X = np.arange(30, dtype=np.int32).reshape(6, 5)
        out = solution.column_view(X, 4)
        assert out.shape == (6,)
        assert out.dtype == np.int32

    def test_first_and_last_columns(self):
        X = np.arange(12).reshape(4, 3)
        assert np.array_equal(solution.column_view(X, 0), [0, 3, 6, 9])
        assert np.array_equal(solution.column_view(X, 2), [2, 5, 8, 11])

    def test_empty_rows(self):
        X = np.zeros((0, 4))
        out = solution.column_view(X, 1)
        assert out.shape == (0,)


class TestEnsureContiguous:
    def test_identity_for_c_input(self):
        x = np.random.default_rng(1).normal(size=(50, 30))
        out = solution.ensure_contiguous(x)
        assert out is x, "C input must be returned as-is (no copy)"

    def test_copies_transposed_view(self):
        x = np.random.default_rng(2).normal(size=(50, 30))
        t = x.T
        out = solution.ensure_contiguous(t)
        assert out is not t, "transposed view must be copied"
        assert out.flags.c_contiguous, "output must be C-contiguous"
        assert np.allclose(out, t)

    def test_copies_fortran_input(self):
        x = np.asfortranarray(np.random.default_rng(3).normal(size=(40, 20)))
        out = solution.ensure_contiguous(x)
        assert out.flags.c_contiguous
        assert np.allclose(out, x)

    def test_strided_view_also_repaired(self):
        x = np.random.default_rng(4).normal(size=(100, 10))
        stride_view = x[::2]
        out = solution.ensure_contiguous(stride_view)
        assert out.flags.c_contiguous
        assert np.allclose(out, stride_view)

    def test_no_allocation_on_fast_path(self):
        x = np.random.default_rng(5).normal(size=(5000, 1000))
        tracemalloc.start()
        try:
            out = solution.ensure_contiguous(x)
            _current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        assert out is x
        assert peak < 1024, \
            f"fast path must not allocate (peak {peak} bytes)"

    def test_no_python_loops(self):
        assert_no_python_loops(solution.ensure_contiguous)


class TestDowncastWhenSafe:
    def test_identity_for_float32(self):
        X = np.random.default_rng(6).normal(size=(5000, 1000)
                                            ).astype(np.float32)
        out = solution.downcast_when_safe(X)
        assert out is X, "float32 input must be returned as-is"
        assert out.dtype == np.float32

    def test_float32_path_allocates_nothing(self):
        X = np.random.default_rng(7).normal(size=(5000, 1000)
                                            ).astype(np.float32)
        tracemalloc.start()
        try:
            out = solution.downcast_when_safe(X)
            _current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        assert out is X
        assert peak < 1024, \
            f"float32 path must not allocate (peak {peak} bytes)"

    def test_float64_downcast(self):
        X = np.random.default_rng(8).normal(size=(5000, 1000))
        tracemalloc.start()
        try:
            out = solution.downcast_when_safe(X)
            _current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        assert out.dtype == np.float32
        assert np.allclose(out, X, atol=1e-6)
        # Result is 5000*1000*4 = 20 MB; a double-copy path exceeds
        # 30 MB because it allocates an extra full-size temporary.
        assert peak < 30 * 1024 * 1024, \
            f"downcast must be a single copy (peak {peak / 1e6:.0f} MB)"

    def test_int64_downcast(self):
        X = np.arange(1_000_000, dtype=np.int64).reshape(1000, 1000)
        out = solution.downcast_when_safe(X)
        assert out.dtype == np.float32
        assert np.allclose(out, X)   # integers < 2^24 are exact

    def test_small_inputs(self):
        assert solution.downcast_when_safe(
            np.zeros(0, dtype=np.float64)).dtype == np.float32
        single = solution.downcast_when_safe(
            np.array([3.5], dtype=np.float64))
        assert single.dtype == np.float32 and single[0] == 3.5

    def test_no_python_loops(self):
        assert_no_python_loops(solution.downcast_when_safe)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
