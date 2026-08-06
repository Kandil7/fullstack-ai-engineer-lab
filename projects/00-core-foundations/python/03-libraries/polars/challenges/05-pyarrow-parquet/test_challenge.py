"""Challenge 05: PyArrow & Parquet — tests for all three tiers.

Run from the module root:
    python -m pytest 03-libraries/polars/challenges/05-pyarrow-parquet/test_challenge.py -v
"""

from __future__ import annotations

import importlib.util
import os

import numpy as np
import polars as pl
import pyarrow.parquet as pq
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution_05", os.path.join(HERE, "solution.py"))
starter = _load("starter_05", os.path.join(HERE, "starter.py"))


def _frame(n: int = 50_000) -> pl.DataFrame:
    rng = np.random.default_rng(42)
    return pl.DataFrame({
        "id": range(n),
        "score": rng.uniform(0.0, 1.0, n),
        "label": ["neg" if i % 3 else "pos" for i in range(n)],
    })


# ---------------------------------------------------------------- bronze

def test_bronze_writes_somewhere(tmp_path):
    df = _frame()
    size = solution.write_zstd_parquet(df, str(tmp_path / "out.parquet"))
    assert size > 0
    assert os.path.exists(tmp_path / "out.parquet")


def test_bronze_actually_zstd(tmp_path):
    df = _frame()
    path = str(tmp_path / "out.parquet")
    solution.write_zstd_parquet(df, path)
    with pq.ParquetFile(path) as pf:
        compression = pf.metadata.row_group(0).column(0).compression
    assert compression.lower() == "zstd"


def test_bronze_roundtrips_rows(tmp_path):
    df = _frame()
    path = str(tmp_path / "out.parquet")
    solution.write_zstd_parquet(df, path)
    assert pl.read_parquet(path).height == df.height


def test_bronze_starter_raises(tmp_path):
    with pytest.raises(NotImplementedError):
        starter.write_zstd_parquet(_frame(), str(tmp_path / "x.parquet"))


# ---------------------------------------------------------------- silver

def test_silver_parquet_smaller(tmp_path):
    df = _frame()
    report = solution.compression_compare(
        df, str(tmp_path / "out.csv"), str(tmp_path / "out.parquet")
    )
    assert report["csv_bytes"] > 0
    assert report["parquet_bytes"] > 0
    assert report["parquet_bytes"] < report["csv_bytes"], \
        "zstd parquet must beat csv on a repetitive string column"


def test_silver_sizes_repeatable(tmp_path):
    df = _frame()
    r1 = solution.compression_compare(df, str(tmp_path / "a.csv"), str(tmp_path / "a.parquet"))
    r2 = solution.compression_compare(df, str(tmp_path / "b.csv"), str(tmp_path / "b.parquet"))
    assert r1 == r2


def test_silver_starter_raises(tmp_path):
    with pytest.raises(NotImplementedError):
        starter.compression_compare(_frame(), str(tmp_path / "x.csv"), str(tmp_path / "x.parquet"))


# ---------------------------------------------------------------- gold

def test_gold_roundtrip_match(tmp_path):
    df = _frame(100_000)
    report = solution.roundtrip_zero_copy(df, str(tmp_path / "rt.parquet"))
    assert report["match"] is True


def test_gold_zero_copy_flag(tmp_path):
    df = _frame(100_000)
    report = solution.roundtrip_zero_copy(df, str(tmp_path / "rt.parquet"))
    assert report["zero_copy"] is True, "numeric column must be zero-copy readable"


def test_gold_uses_allow_copy_kwarg():
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    assert "allow_copy=False" in source, \
        "must use the modern allow_copy=False (zero_copy_only is deprecated)"


def test_gold_starter_raises(tmp_path):
    with pytest.raises(NotImplementedError):
        starter.roundtrip_zero_copy(_frame(), str(tmp_path / "x.parquet"))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
