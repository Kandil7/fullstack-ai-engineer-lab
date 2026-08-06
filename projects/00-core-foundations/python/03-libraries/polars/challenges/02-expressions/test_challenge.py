"""Challenge 02: Polars Expressions — tests for all three tiers.

Run from the module root:
    python -m pytest 03-libraries/polars/challenges/02-expressions/test_challenge.py -v
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


solution = _load("solution_02", os.path.join(HERE, "solution.py"))
starter = _load("starter_02", os.path.join(HERE, "starter.py"))


def _small_frame() -> pl.DataFrame:
    return pl.DataFrame(
        {"user": ["a", "b", "c", "a"],
         "score": [0.9, 0.4, 0.7, 0.2],
         "spend": [10, 20, 30, 40]}
    )


def _assert_expression_pure():
    """Forbid .apply()/iter_rows: the whole point of expressions."""
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    assert ".apply(" not in source
    assert "iter_rows" not in source
    assert "iter_slices" not in source


# ---------------------------------------------------------------- bronze

def test_bronze_basic_filter():
    out = solution.filter_and_project(_small_frame(), 0.5, 15.0)
    assert out.rows() == [("c", 0.7)]


def test_bronze_projects_two_columns():
    out = solution.filter_and_project(_small_frame(), 0.0, 0.0)
    assert out.columns == ["user", "score"]
    assert out.height == 4


def test_bronze_edge_no_match():
    out = solution.filter_and_project(_small_frame(), 1.0, 100.0)
    assert out.height == 0


def test_bronze_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.filter_and_project(_small_frame(), 0.5, 15.0)


# ---------------------------------------------------------------- silver

def test_silver_band_values():
    out = solution.derive_features(_small_frame())
    assert out["band"].to_list() == ["high", "low", "high", "low"]


def test_silver_rank_descending():
    out = solution.derive_features(_small_frame())
    assert out["score_rank"].to_list() == [1.0, 3.0, 2.0, 4.0]


def test_silver_norm_and_preservation():
    out = solution.derive_features(_small_frame())
    assert out["spend_norm"].to_list() == [0.1, 0.2, 0.3, 0.4]
    assert out.columns == ["user", "score", "spend", "band", "score_rank", "spend_norm"]


def test_silver_expression_pure():
    _assert_expression_pure()


def test_silver_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.derive_features(_small_frame())


# ---------------------------------------------------------------- gold

def test_gold_window_features_small():
    out = solution.group_ranked_features(_small_frame())
    row_a = out.filter(pl.col("user") == "a").row(0)
    row_b = out.filter(pl.col("user") == "b").row(0)
    assert row_a == ("a", 2, 0.8, 50), "a: 2 events, max share 40/50=0.8"
    assert row_b == ("b", 1, 1.0, 20)


def test_gold_shares_sum_to_one():
    df = pl.DataFrame({"user": ["a"] * 3, "spend": [10, 30, 60]})
    out = solution.group_ranked_features(df)
    assert out.filter(pl.col("user") == "a").row(0) == ("a", 3, 0.6, 100)


def test_gold_sorted_by_user():
    out = solution.group_ranked_features(_small_frame())
    assert out["user"].to_list() == ["a", "b", "c"]


def test_gold_large_scale():
    rng = __import__("numpy").random.default_rng(42)
    n = 200_000
    df = pl.DataFrame({
        "user": [f"u{rng.integers(0, 10_000)}" for _ in range(n)],
        "spend": rng.uniform(0.0, 100.0, n),
    })
    out = solution.group_ranked_features(df)
    assert out.height == 10_000, "one row per user"
    assert abs(out["spend_total"].sum() - df["spend"].sum()) < 1e-6, \
        "spend_total must partition the total spend"


def test_gold_expression_pure():
    _assert_expression_pure()


def test_gold_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.group_ranked_features(_small_frame())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
