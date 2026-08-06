"""
Challenge 02: Polars Expressions — Starter Code
=================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

import polars as pl


def filter_and_project(df: pl.DataFrame, min_score: float, min_spend: float) -> pl.DataFrame:
    """Keep rows with score >= min_score AND spend >= min_spend.

    Output exactly two columns: user, score.
    """
    raise NotImplementedError


def derive_features(df: pl.DataFrame) -> pl.DataFrame:
    """Add band, score_rank (descending), and spend_norm in one call."""
    raise NotImplementedError


def group_ranked_features(df: pl.DataFrame) -> pl.DataFrame:
    """Window features over user, then per-user aggregates, sorted by user."""
    raise NotImplementedError
