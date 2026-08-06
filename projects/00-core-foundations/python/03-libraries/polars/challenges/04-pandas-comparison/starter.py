"""
Challenge 04: Polars pandas Comparison — Starter Code
=======================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

import pandas as pd
import polars as pl


def polars_filter_equivalent(pdf: pd.DataFrame, campaign: str, min_rev: float) -> pl.DataFrame:
    """Translate a pandas boolean-mask filter to Polars, same rows/order."""
    raise NotImplementedError


def polars_groupby_equivalent(pdf: pd.DataFrame) -> pl.DataFrame:
    """Reproduce a pandas groupby().agg() exactly with Polars expressions."""
    raise NotImplementedError


def parity_suite(pdf: pd.DataFrame) -> dict[str, object]:
    """3-step pipeline in both engines; return verdict + final rows."""
    raise NotImplementedError
