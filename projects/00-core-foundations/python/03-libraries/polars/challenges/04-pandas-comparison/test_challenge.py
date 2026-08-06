"""Challenge 04: Polars pandas Comparison — tests for all three tiers.

Run from the module root:
    python -m pytest 03-libraries/polars/challenges/04-pandas-comparison/test_challenge.py -v
"""

from __future__ import annotations

import importlib.util
import os

import numpy as np
import pandas as pd
import polars as pl
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution_04", os.path.join(HERE, "solution.py"))
starter = _load("starter_04", os.path.join(HERE, "starter.py"))


def _small() -> pd.DataFrame:
    return pd.DataFrame({
        "campaign": ["a", "b", "a", "c", "b"],
        "converted": [1, 0, 1, 1, 0],
        "revenue": [10.0, 5.0, 30.0, 12.0, 3.0],
    })


def _large(n: int = 200_000) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    return pd.DataFrame({
        "campaign": rng.choice(["a", "b", "c", "d"], n),
        "converted": rng.integers(0, 2, n),
        "revenue": rng.uniform(0.0, 50.0, n),
    })


def _assert_polars_pure():
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    assert ".apply(" not in source, "Polars side must be expression-only"


# ---------------------------------------------------------------- bronze

def test_bronze_matches_pandas_mask():
    pdf = _small()
    expected = pdf[(pdf["campaign"] == "a") & (pdf["revenue"] >= 10.0)]
    out = solution.polars_filter_equivalent(pdf, "a", 10.0)
    assert out.height == len(expected)
    assert out["campaign"].to_list() == expected["campaign"].tolist()
    assert out["revenue"].to_list() == expected["revenue"].tolist()


def test_bronze_preserves_row_order():
    pdf = _small()
    out = solution.polars_filter_equivalent(pdf, "b", 0.0)
    assert out["revenue"].to_list() == [5.0, 3.0]


def test_bronze_empty_result():
    pdf = _small()
    out = solution.polars_filter_equivalent(pdf, "z", 0.0)
    assert out.height == 0


def test_bronze_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.polars_filter_equivalent(_small(), "a", 10.0)


# ---------------------------------------------------------------- silver

def test_silver_matches_groupby_small():
    pdf = _small()
    expected = (pdf.groupby("campaign")
                .agg(conversions=("converted", "sum"),
                     revenue=("revenue", "mean"))
                .reset_index()
                .sort_values("campaign"))
    out = solution.polars_groupby_equivalent(pdf)
    assert out.columns == ["campaign", "conversions", "revenue"]
    assert out["conversions"].to_list() == expected["conversions"].tolist()
    assert np.allclose(out["revenue"].to_list(), expected["revenue"].tolist(), atol=1e-9)


def test_silver_matches_groupby_large():
    pdf = _large()
    expected = (pdf.groupby("campaign")
                .agg(conversions=("converted", "sum"))
                .reset_index()
                .sort_values("campaign"))
    out = solution.polars_groupby_equivalent(pdf)
    assert out["conversions"].to_list() == expected["conversions"].tolist()


def test_silver_expression_pure():
    _assert_polars_pure()


def test_silver_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.polars_groupby_equivalent(_small())


# ---------------------------------------------------------------- gold

def test_gold_verdict_true_large():
    report = solution.parity_suite(_large())
    assert report["verdict"] is True
    assert len(report["pandas_rows"]) == len(report["polars_rows"])
    for p_row, l_row in zip(report["pandas_rows"], report["polars_rows"]):
        assert p_row[0] == l_row[0], "campaign keys must match"
        assert abs(p_row[1] - l_row[1]) < 1e-9, "means must agree to 1e-9"


def test_gold_rows_shape():
    report = solution.parity_suite(_large())
    assert len(report["pandas_rows"]) == 4, "one row per campaign"
    assert len(report["pandas_rows"][0]) == 2, "campaign + mean_revenue"


def test_gold_join_used():
    """Budget must arrive via join — the README forbids manual assignment."""
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    assert ".join(" in source
    assert "budget" in source


def test_gold_expression_pure():
    _assert_polars_pure()


def test_gold_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.parity_suite(_small())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
