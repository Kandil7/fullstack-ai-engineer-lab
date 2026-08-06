"""
Challenge 40: Memory Optimization — Tests
==========================================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest challenges/40-memory-optimization/test_challenge.py -q

Memory guards use post-measurement assertions and tracemalloc — never
wall-clock time.
"""

from __future__ import annotations

import importlib.util
import os
import tracemalloc
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(
    TARGET, Path(__file__).parent / f"{TARGET}.py"
)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import io

import numpy as np
import pandas as pd
import pytest  # noqa: E402


def _waste_frame(n: int) -> pd.DataFrame:
    """A deliberately memory-wasteful frame (100k rows by default)."""
    rng = np.random.RandomState(42)
    return pd.DataFrame({
        "user_id": rng.randint(0, 1_000_000, n),
        "score": rng.uniform(0, 1, n),
        "tier": rng.choice(["free", "pro", "enterprise"], n),
        "is_active": rng.choice([True, False], n),
    })


class TestMeasureDeep:
    """Bronze: honest memory measurement."""

    def test_numeric_total(self) -> None:
        frame = pd.DataFrame({"a": [1, 2, 3]})
        assert mod.measure_deep(frame) == int(frame.memory_usage(deep=True).sum())

    def test_strings_cost_more_than_pointers(self) -> None:
        frame = pd.DataFrame({"s": ["x", "y", "z"]})
        assert mod.measure_deep(frame) > 3 * 8, \
            "object payloads must be counted (deep=True)"

    def test_empty_frame(self) -> None:
        frame = pd.DataFrame({"a": pd.Series(dtype="float64")})
        assert mod.measure_deep(frame) >= 0

    def test_matches_reference(self) -> None:
        frame = pd.DataFrame({
            "a": np.arange(10),
            "s": ["str-%d" % i for i in range(10)],
        })
        assert mod.measure_deep(frame) == int(frame.memory_usage(deep=True).sum())


class TestOptimizeDtypes:
    """Silver: right-sized dtypes with preserved values."""

    def _frame(self) -> pd.DataFrame:
        return _waste_frame(100_000)

    def test_input_not_mutated(self) -> None:
        frame = self._frame()
        original = frame.copy()
        mod.optimize_dtypes(frame)
        pd.testing.assert_frame_equal(frame, original)

    def test_dtypes_right_sized(self) -> None:
        fixed = mod.optimize_dtypes(self._frame())
        assert fixed["user_id"].dtype == np.dtype("int32"), \
            "user_id range fits int32"
        assert fixed["score"].dtype == np.dtype("float32"), \
            "score must downcast to float32"
        assert str(fixed["tier"].dtype) == "category", \
            "low-cardinality strings must become category"

    def test_memory_reduced_below_35_percent(self) -> None:
        frame = self._frame()
        before = int(frame.memory_usage(deep=True).sum())
        fixed = mod.optimize_dtypes(frame)
        after = int(fixed.memory_usage(deep=True).sum())
        assert after < 0.35 * before, (
            f"optimized {after} bytes must be under 35% of original {before}"
        )

    def test_integers_preserved_exactly(self) -> None:
        frame = self._frame()
        fixed = mod.optimize_dtypes(frame)
        assert bool((frame["user_id"] == fixed["user_id"]).all()), \
            "integer values must survive downcasting exactly"

    def test_floats_within_tolerance(self) -> None:
        frame = self._frame()
        fixed = mod.optimize_dtypes(frame)
        assert np.allclose(frame["score"].values, fixed["score"].values,
                           atol=1e-6), \
            "float32 downcast must stay within 1e-6"

    def test_small_frame_not_broken(self) -> None:
        frame = pd.DataFrame({
            "a": np.arange(5),
            "b": np.random.RandomState(1).uniform(0, 1, 5),
        })
        fixed = mod.optimize_dtypes(frame)
        assert len(fixed) == 5
        assert bool((frame["a"] == fixed["a"]).all())


class TestStreamedMean:
    """Gold: chunked mean under a tracemalloc ceiling."""

    def _csv_text(self, n: int) -> str:
        rng = np.random.RandomState(7)
        return pd.DataFrame({"x": np.arange(n),
                             "y": rng.uniform(0, 1, n)}).to_csv(index=False)

    def test_three_rows(self) -> None:
        text = pd.DataFrame({"y": [1.0, 2.0, 3.0]}).to_csv(index=False)
        assert mod.streamed_mean(text, "y", 1) == 2.0

    def test_equals_full_frame(self) -> None:
        text = self._csv_text(1000)
        expected = float(pd.read_csv(io.StringIO(text))["y"].mean())
        assert mod.streamed_mean(text, "y", 250) == pytest.approx(expected)

    def test_all_chunksizes_agree(self) -> None:
        text = self._csv_text(1000)
        expected = float(pd.read_csv(io.StringIO(text))["y"].mean())
        for cs in (1, 7, 100, 1000):
            assert mod.streamed_mean(text, "y", cs) == pytest.approx(expected), \
                f"chunksize {cs} must agree"

    def test_empty_column_returns_nan(self) -> None:
        text = pd.DataFrame({"y": pd.Series(dtype="float64")}).to_csv(index=False)
        result = mod.streamed_mean(text, "y", 10)
        assert np.isnan(result)

    def test_memory_ceiling_guard(self) -> None:
        """tracemalloc guard over a 10^6-row CSV (~27 MB text).
        Measured on this stack: chunked read peaks ~109 MB, a full
        pd.read_csv materialization peaks ~141 MB. The 130 MB ceiling
        admits the chunked reader and rejects the full read."""
        n = 10**6
        text = self._csv_text(n)
        expected = float(pd.read_csv(io.StringIO(text), usecols=["y"])["y"].mean())

        tracemalloc.start()
        try:
            result = mod.streamed_mean(text, "y", 10_000)
        finally:
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

        assert result == pytest.approx(expected)
        assert peak < 130 * 1024 * 1024, (
            f"peak {peak / 1e6:.1f} MB exceeds the 130 MB ceiling; "
            "the file must be read in chunks, never materialized"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
