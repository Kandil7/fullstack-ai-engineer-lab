"""
Polars — 04: pandas Comparison
================================
Topics: side-by-side idioms (filter / groupby-agg / join / new columns);
measured micro-benchmarks; the migration guide; when pandas is still right.

Why this matters for AI/backend engineering:
    Most legacy feature pipelines are pandas. Most new large-scale ones
    are Polars. This file is the translation table: the same operations,
    side by side, with honest measurements (printed, not asserted —
    wall-clock is not reproducible). You must be able to read either
    codebase and port the other, and you must know when NOT to port:
    pandas still wins for timezone-heavy time series, apply-heavy
    research code, and any team already invested in the pandas ecosystem.

Run:      python 04-pandas-comparison.py
Verify:   python 04-pandas-comparison.py --verify
Reference: https://docs.pola.rs/user-guide/migration/pandas/
"""

from __future__ import annotations

import sys
import time

try:
    import polars as pl
except ImportError:  # pragma: no cover - optional dependency
    print("[skip] polars not installed - install with: pip install polars")
    sys.exit(0)

import numpy as np
import pandas as pd

# Deterministic synthetic clickstream: 200k rows.
rng = np.random.default_rng(42)
N = 200_000
users = np.random.default_rng(1).integers(0, 5000, N)
_records = {
    "user": [f"u{u:05d}" for u in users],
    "campaign": rng.choice(["a", "b", "c", "d"], N),
    "converted": rng.integers(0, 2, N).astype(bool),
    "revenue": rng.uniform(0.0, 50.0, N),
}

pdf = pd.DataFrame(_records)
pdframe = pdf  # pandas DataFrame
plf = pl.DataFrame(_records)  # polars DataFrame


# ============================================================
# 1. Filter: the same predicate, two grammars
# ============================================================
# pandas: boolean mask in square brackets. polars: filter() with an Expr.
# Both are vectorized; the polars one is also reusable in lazy mode.

def pandas_filter(df: pd.DataFrame, campaign: str, min_rev: float) -> pd.DataFrame:
    """pandas: boolean-mask row selection."""
    return df[(df["campaign"] == campaign) & (df["revenue"] >= min_rev)]


def polars_filter(df: pl.DataFrame, campaign: str, min_rev: float) -> pl.DataFrame:
    """polars: filter() with a compound Expr predicate."""
    return df.filter(
        (pl.col("campaign") == campaign) & (pl.col("revenue") >= min_rev)
    )


# Example 1: identical rows, same order (polars preserves input order here)
p_out = pandas_filter(pdframe, "a", 10.0)
pl_out = polars_filter(plf, "a", 10.0)
print(f"pandas rows: {len(p_out)}, polars rows: {pl_out.height}")

# Output:
# pandas rows: 39859, polars rows: 39859


# ============================================================
# 2. groupby + agg: split-apply-combine
# ============================================================
# pandas: df.groupby().agg({...}) with a dict. polars: group_by().agg()
# with expressions. Note: pandas computes the same aggregates; polars
# expressions read top-to-bottom like a spec.

def pandas_groupby(df: pd.DataFrame) -> pd.DataFrame:
    """pandas: per-campaign conversion and revenue stats."""
    return (
        df.groupby("campaign")
        .agg(conversions=("converted", "sum"),
             revenue=("revenue", "mean"),
             events=("user", "count"))
        .reset_index()
    )


def polars_groupby(df: pl.DataFrame) -> pl.DataFrame:
    """polars: per-campaign conversion and revenue stats."""
    return (
        df.group_by("campaign")
        .agg(pl.col("converted").sum().alias("conversions"),
             pl.col("revenue").mean().alias("revenue"),
             pl.len().alias("events"))
        .sort("campaign")
    )


# Example 2: equivalent aggregations
g_p = pandas_groupby(pdframe).sort_values("campaign")
g_l = polars_groupby(plf)
print(g_p[["campaign", "conversions"]].to_dict("list"))
print(g_l.select("campaign", "conversions").rows())

# Output:
# {'campaign': ['a', 'b', 'c', 'd'], 'conversions': [24739, 24780, 25233, 24974]}
# [('a', 24739), ('b', 24780), ('c', 25233), ('d', 24974)]


# ============================================================
# 3. Join: SQL-style merge, column for column
# ============================================================
# pandas: df.merge(other, on=...). polars: df.join(other, on=...). Both
# default to inner joins; both accept how=/how=.

campaign_meta_p = pd.DataFrame(
    {"campaign": ["a", "b", "c", "d"], "budget": [1000, 800, 1200, 600]}
)
campaign_meta_l = pl.DataFrame(campaign_meta_p)

def pandas_join(df: pd.DataFrame) -> pd.DataFrame:
    """pandas: merge on campaign id."""
    return df.merge(campaign_meta_p, on="campaign", how="left")


def polars_join(df: pl.DataFrame) -> pl.DataFrame:
    """polars: join on campaign id."""
    return df.join(campaign_meta_l, on="campaign", how="left")


# Example 3: both widen the frame with the budget column
j_p = pandas_join(pdframe)
j_l = polars_join(plf)
print(j_p.shape, j_l.shape)

# Output:
# (200000, 5) (200000, 5)


# ============================================================
# 4. New columns: assignment vs with_columns
# ============================================================
# pandas: df["new"] = expr (writes into the frame). polars:
# with_columns() returns a new frame — nothing mutates the input.

def pandas_new_col(df: pd.DataFrame) -> pd.DataFrame:
    """pandas: column assignment in place (returns the same frame)."""
    df = df.copy()
    df["revenue_per_user"] = df["revenue"] / df.groupby("user")["revenue"].transform("sum")
    return df


def polars_new_col(df: pl.DataFrame) -> pl.DataFrame:
    """polars: with_columns returns a NEW frame with the derived column."""
    return df.with_columns(
        (pl.col("revenue") / pl.col("revenue").sum().over("user"))
        .alias("revenue_per_user")
    )


# Example 4: derived column, same values
n_p = pandas_new_col(pdframe)
n_l = polars_new_col(plf)
print(f"pandas new col: {n_p['revenue_per_user'].iloc[0]:.6f}")
print(f"polars new col: {n_l['revenue_per_user'][0]:.6f}")

# Output:
# pandas new col: 0.084604
# polars new col: 0.084604


# ============================================================
# 5. Measured comparison (printed, never asserted)
# ============================================================
# Timing depends on machine and version, so we PRINT it for the student
# but never gate on it. Run the same workload several times; the polars
# advantage grows with data size and with lazy pipelines that avoid
# materialization.

def measure(label: str, fn, repeat: int = 3) -> None:
    """Run fn repeatedly, print best wall-clock time in ms."""
    best = float("inf")
    for _ in range(repeat):
        start = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - start)
    print(f"  {label}: {best * 1000:.2f} ms")


# Example 5: same analytics workload on 200k rows
print("filter:")
measure("pandas", lambda: pandas_filter(pdframe, "a", 10.0))
measure("polars", lambda: polars_filter(plf, "a", 10.0))
print("groupby-agg:")
measure("pandas", lambda: pandas_groupby(pdframe))
measure("polars", lambda: polars_groupby(plf))

# Output (machine-dependent, printed only):
# filter:
#   pandas: 13.xx ms
#   polars: 6.xx ms
# groupby-agg:
#   pandas: 26.xx ms
#   polars: 9.xx ms


# ============================================================
# 6. When pandas is still right
# ============================================================
# Migration is not a one-way street. pandas keeps the better ecosystem
# for: tz-aware time series (resample rules, business calendars),
# apply() with arbitrary Python callables per row, .rolling with
# irregular windows, and teams whose tooling (notebooks, SQLAlchemy,
# statsmodels) already speaks pandas. Port when: the data is large,
# the pipeline is a fixed set of vectorized steps, and Parquet/Arrow
# interop matters more than pandas convenience.

def pandas_why_still_right() -> str:
    """One-line summary of when NOT to migrate."""
    return (
        "pandas wins for tz-aware time series, apply-heavy research code, "
        "and ecosystems that already speak pandas."
    )


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: translating .apply(row-wise) to polars the same way
#   plf.with_columns(pl.col("x").apply(my_py_fn))  # slow per-element path
# CORRECT: rewrite as an expression, or use pl.map_batches for batch ops
#
# MISTAKE: expecting a pandas-style index
#   plf.loc[5]                        # AttributeError
# CORRECT: plf.row(5), or filter on a real id column
#
# MISTAKE: timing in production code and asserting on it
#   assert polars_time < pandas_time   # flaky on shared CI machines
# CORRECT: print measurements; gate on correctness and memory only


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    p_out = pandas_filter(pdframe, "a", 10.0)
    pl_out = polars_filter(plf, "a", 10.0)
    assert len(p_out) == pl_out.height, "filter must select identical row counts"
    assert pl_out.height > 10_000, "filter must keep a large subset"

    g_p = pandas_groupby(pdframe).sort_values("campaign")
    g_l = polars_groupby(plf)
    assert g_l.height == 4, "one row per campaign"
    assert g_l["conversions"].sum() == int(g_p["conversions"].sum()), \
        "total conversions must agree between engines"
    assert g_p["conversions"].tolist() == [c for _, c in g_l.select("campaign", "conversions").rows()], \
        "per-campaign conversion counts must match exactly"

    j_p = pandas_join(pdframe)
    j_l = polars_join(plf)
    assert j_p.shape == j_l.shape == (N, 5), \
        "left joins must widen both frames identically"
    assert "budget" in j_l.columns, "join must bring the budget column in"

    n_p = pandas_new_col(pdframe)
    n_l = polars_new_col(plf)
    assert abs(n_p["revenue_per_user"].iloc[0] - n_l["revenue_per_user"][0]) < 1e-9, \
        "derived column must match to float precision"
    assert "revenue_per_user" in n_l.columns, \
        "with_columns must add the derived column"
    assert n_l.columns == plf.columns + ["revenue_per_user"], \
        "polars must keep original columns and append the new one"

    # pandas input must be untouched by the polars pipeline (no mutation)
    assert list(pdframe.columns) == ["user", "campaign", "converted", "revenue"], \
        "polars pipeline must not mutate the pandas frame"

    # Cross-check the groupby numbers exactly (deterministic seed data)
    assert g_l.select("conversions").to_series().to_list() == \
        [24739, 24780, 25233, 24974], \
        "seeded data must reproduce the exact conversion counts"

    assert "pandas wins" in pandas_why_still_right(), \
        "the guidance must state when pandas remains the right choice"

    print("[OK] 04-pandas-comparison: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Same idioms, two grammars: filter / group_by.agg / join / new cols")
        print("2. Measurements are printed, never asserted (wall-clock is flaky)")
        print("3. Port for scale and Parquet; keep pandas for tz/apply ecosystems")
        _verify()   # always runs, so plain execution is also a test
