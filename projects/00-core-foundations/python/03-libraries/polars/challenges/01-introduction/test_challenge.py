"""Challenge 01: Polars Introduction — tests for all three tiers.

Run from the module root:
    python -m pytest 03-libraries/polars/challenges/01-introduction/test_challenge.py -v
"""

from __future__ import annotations

import importlib.util
import os

import polars as pl
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Unique module names: several challenge dirs share solution.py/starter.py.
solution = _load("solution_01", os.path.join(HERE, "solution.py"))
starter = _load("starter_01", os.path.join(HERE, "starter.py"))


def _assert_no_python_row_loops(mod):
    """Forbid per-row Python dispatch: .apply() and iter_rows() calls."""
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    assert ".apply(" not in source, "solution.py must not use .apply()"
    assert "iter_rows" not in source, "solution.py must not iterate rows"
    assert "iter_slices" not in source, "solution.py must not iterate batches"


# ---------------------------------------------------------------- bronze

def test_bronze_forces_schema():
    df = solution.build_features_frame(
        {"sample_id": ["1", "2"], "score": [0.9, 0.4], "split": ["a", "b"]}
    )
    assert isinstance(df, pl.DataFrame)
    assert df.schema["sample_id"] == pl.Int64, "string '1' must become Int64"
    assert df.schema["score"] == pl.Float64
    assert df.schema["split"] == pl.String


def test_bronze_values_preserved():
    df = solution.build_features_frame(
        {"sample_id": ["10", "20"], "score": [0.5, 0.8], "split": ["t", "v"]}
    )
    assert df["sample_id"].to_list() == [10, 20]
    assert df.height == 2 and df.width == 3


def test_bronze_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.build_features_frame({"a": [1]})


# ---------------------------------------------------------------- silver

def test_silver_stats_exact():
    df = pl.DataFrame({"a": [1.0, 2.0, 3.0], "s": ["x", "y", "z"]})
    stats = solution.column_stats(df)
    assert stats == {"a": (2.0, 1.0, 3.0)}


def test_silver_skips_strings_and_bools():
    df = pl.DataFrame({"f": [1.5, 2.5], "s": ["x", "y"], "b": [True, False]})
    stats = solution.column_stats(df)
    assert set(stats) == {"f"}


def test_silver_empty_numeric():
    df = pl.DataFrame({"s": ["a", "b"]})
    assert solution.column_stats(df) == {}


def test_silver_no_python_loops():
    _assert_no_python_row_loops(solution)


def test_silver_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.column_stats(pl.DataFrame({"a": [1.0]}))


# ---------------------------------------------------------------- gold

def test_gold_int64_footprint():
    df = pl.DataFrame({"a": [0] * 1_000_000}).with_columns(
        pl.col("a").cast(pl.Int64)
    )
    assert solution.estimate_numeric_bytes(df) == 8_000_000


def test_gold_mixed_widths():
    n = 500_000
    df = pl.DataFrame({
        "f32": pl.Series([0.0] * n).cast(pl.Float32),
        "i16": pl.Series([0] * n).cast(pl.Int16),
    })
    assert solution.estimate_numeric_bytes(df) == 2_000_000 + 1_000_000


def test_gold_ignores_strings():
    df = pl.DataFrame({"a": [0] * 100, "s": ["x"] * 100})
    assert solution.estimate_numeric_bytes(df) == 800


def test_gold_scales_with_rows_not_columns():
    small = pl.DataFrame({"a": [0] * 10})
    large = pl.DataFrame({"a": [0] * 10_000_000})
    assert solution.estimate_numeric_bytes(large) == \
        solution.estimate_numeric_bytes(small) * 1_000_000


def test_gold_uint_and_float64():
    df = pl.DataFrame({
        "u32": pl.Series([1] * 100).cast(pl.UInt32),
        "f64": pl.Series([1.0] * 100).cast(pl.Float64),
    })
    assert solution.estimate_numeric_bytes(df) == 100 * (4 + 8)


def test_gold_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.estimate_numeric_bytes(pl.DataFrame({"a": [1]}))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
