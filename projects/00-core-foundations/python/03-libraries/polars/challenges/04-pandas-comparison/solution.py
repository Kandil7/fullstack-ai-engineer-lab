"""
Challenge 04: Polars pandas Comparison — Reference Solution
=============================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import polars as pl


def polars_filter_equivalent(pdf: pd.DataFrame, campaign: str, min_rev: float) -> pl.DataFrame:
    """Translate a pandas boolean-mask filter to Polars, same rows/order.

    Why this approach: the Expr predicate composes with & exactly like the
    mask; Polars filters preserve input order, matching pandas row order.
    """
    plf = pl.from_pandas(pdf)
    return plf.filter(
        (pl.col("campaign") == campaign) & (pl.col("revenue") >= min_rev)
    )


def polars_groupby_equivalent(pdf: pd.DataFrame) -> pl.DataFrame:
    """Reproduce a pandas groupby().agg() exactly with Polars expressions.

    Why this approach: named expressions replace the pandas
    {column: function} dict; alias() pins the output names so the frames
    compare column-for-column. reset_index() has no Polars equivalent
    because group_by output is already flat.
    """
    plf = pl.from_pandas(pdf)
    return (
        plf.group_by("campaign")
        .agg(
            pl.col("converted").sum().alias("conversions"),
            pl.col("revenue").mean().alias("revenue"),
        )
        .sort("campaign")
    )


def parity_suite(pdf: pd.DataFrame) -> dict[str, object]:
    """3-step pipeline in both engines; return verdict + final rows.

    Why this approach: running both engines on the same seeded input and
    comparing final rows is the migration discipline: verify parity on a
    sample before porting at scale. The Polars side is lazy so it could
    stream the same steps at 10^8 rows.
    """
    meta_p = pd.DataFrame(
        {"campaign": ["a", "b", "c", "d"],
         "budget": [1000.0, 800.0, 1200.0, 600.0]}
    )

    # pandas reference pipeline
    step = pdf[pdf["revenue"] >= 5.0]
    step = step.merge(meta_p, on="campaign", how="left")
    p_final = (step.groupby("campaign")
               .agg(mean_revenue=("revenue", "mean"))
               .reset_index()
               .sort_values("campaign"))

    # polars pipeline: same steps, expression-only
    meta_l = pl.from_pandas(meta_p)
    l_final = (
        pl.from_pandas(pdf)
        .filter(pl.col("revenue") >= 5.0)
        .join(meta_l, on="campaign", how="left")
        .group_by("campaign")
        .agg(pl.col("revenue").mean().alias("mean_revenue"))
        .sort("campaign")
    )

    p_rows = [tuple(row) for row in p_final.itertuples(index=False)]
    l_rows = [tuple(row) for row in l_final.rows()]
    verdict = len(p_rows) == len(l_rows) and all(
        abs(a - b) < 1e-9 for a, b in zip(
            [r[1] for r in p_rows], [r[1] for r in l_rows]
        )
    )
    return {"verdict": bool(verdict), "pandas_rows": p_rows, "polars_rows": l_rows}


def _seeded_frame(n: int = 200_000) -> pd.DataFrame:
    """Deterministic clickstream frame shared by the gold tests."""
    rng = np.random.default_rng(42)
    return pd.DataFrame({
        "campaign": rng.choice(["a", "b", "c", "d"], n),
        "converted": rng.integers(0, 2, n),
        "revenue": rng.uniform(0.0, 50.0, n),
    })
