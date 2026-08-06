"""Challenge 06: Larger Than Memory — tests for all three tiers.

Run from the module root:
    python -m pytest 03-libraries/polars/challenges/06-larger-than-memory/test_challenge.py -v
"""

from __future__ import annotations

import importlib.util
import os

import numpy as np
import polars as pl
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution_06", os.path.join(HERE, "solution.py"))
starter = _load("starter_06", os.path.join(HERE, "starter.py"))


@pytest.fixture()
def csv_path(tmp_path):
    rng = np.random.default_rng(42)
    n = 100_000
    df = pl.DataFrame({
        "id": range(n),
        "metric": rng.uniform(0.0, 1.0, n),
    })
    path = str(tmp_path / "events.csv")
    df.write_csv(path)
    return path, df


@pytest.fixture()
def shard_dir(tmp_path):
    """4 parquet shards of 50k rows each in a clean directory."""
    rng = np.random.default_rng(7)
    d = tmp_path / "shards"
    d.mkdir()
    n = 50_000
    for i in range(4):
        df = pl.DataFrame({
            "id": range(i * n, (i + 1) * n),
            "metric": rng.uniform(0.0, 1.0, n),
        })
        df.write_parquet(d / f"part-{i}.parquet")
    return str(d)


@pytest.fixture()
def right_dir(tmp_path):
    """50k rows with unique id -> category for the gold join."""
    d = tmp_path / "right"
    d.mkdir()
    df = pl.DataFrame({
        "id": range(200_000),
        "category": ["cat"] * 200_000,
    })
    df.write_parquet(d / "part-0.parquet")
    return str(d)


# ---------------------------------------------------------------- bronze

def test_bronze_count_matches(csv_path):
    path, df = csv_path
    report = solution.streaming_count(path)
    assert report["rows"] == df.height == 100_000


def test_bronze_streaming_flag(csv_path):
    path, _ = csv_path
    report = solution.streaming_count(path)
    assert report["streaming"] is True


def test_bronze_never_read_csv(csv_path):
    path, _ = csv_path
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    assert "read_csv(" not in source, "must stay lazy: no read_csv"


def test_bronze_starter_raises(csv_path):
    path, _ = csv_path
    with pytest.raises(NotImplementedError):
        starter.streaming_count(path)


# ---------------------------------------------------------------- silver

def test_silver_counts_all_shards(shard_dir):
    report = solution.chunked_stats(shard_dir, "metric")
    assert report["rows"] == 200_000


def test_silver_mean_approx(shard_dir):
    report = solution.chunked_stats(shard_dir, "metric")
    assert abs(report["mean"] - 0.5) < 0.05, "uniform(0,1) mean should be ~0.5"


def test_silver_single_scan(shard_dir):
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    fn_src = source.split("def sink_join")[0]
    assert fn_src.count("scan_parquet(") == 1, "must use one directory scan"


def test_silver_starter_raises(shard_dir):
    with pytest.raises(NotImplementedError):
        starter.chunked_stats(shard_dir, "metric")


# ---------------------------------------------------------------- gold

def test_gold_join_rows(tmp_path, shard_dir, right_dir):
    out = str(tmp_path / "joined.parquet")
    rows = solution.sink_join(shard_dir, right_dir, "id", "id", out)
    assert rows == 200_000


def test_gold_join_content(tmp_path, shard_dir, right_dir):
    out = str(tmp_path / "joined.parquet")
    solution.sink_join(shard_dir, right_dir, "id", "id", out)
    df = pl.scan_parquet(out).select(pl.col("metric").sum(), pl.col("category").first()).collect()
    assert df["category"][0] == "cat"
    assert df["metric"][0] > 0


def test_gold_lazy_end_to_end():
    """collect must not appear before sink_parquet inside sink_join."""
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    # limit the scan to the sink_join function body only
    fn = source[source.find("def sink_join"):]
    sink_idx = fn.find("sink_parquet")
    assert sink_idx != -1, "must use sink_parquet"
    collect_idx = fn.find("collect(")
    assert collect_idx == -1 or collect_idx > sink_idx, \
        "no collect() may run before the sink (that would materialize RAM)"


def test_gold_starter_raises(tmp_path, shard_dir, right_dir):
    with pytest.raises(NotImplementedError):
        starter.sink_join(shard_dir, right_dir, "id", "id", str(tmp_path / "x.parquet"))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
