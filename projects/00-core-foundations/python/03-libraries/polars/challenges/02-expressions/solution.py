"""
Challenge 02: Polars Expressions — Reference Solution
=======================================================
"""

from __future__ import annotations

import polars as pl


def filter_and_project(df: pl.DataFrame, min_score: float, min_spend: float) -> pl.DataFrame:
    """Keep rows with score >= min_score AND spend >= min_spend.

    Why this approach: & joins parenthesized comparisons into one
    predicate; Python's `and` would raise on Expr truthiness. select
    projects exactly the two output columns.
    """
    return df.filter(
        (pl.col("score") >= min_score) & (pl.col("spend") >= min_spend)
    ).select("user", "score")


def derive_features(df: pl.DataFrame) -> pl.DataFrame:
    """Add band, score_rank (descending), and spend_norm in one call.

    Why this approach: one with_columns call keeps all original columns
    and runs all three derived features in a single kernel pass. rank
    needs descending=True because the default ranks ascending.
    """
    return df.with_columns(
        pl.when(pl.col("score") >= 0.5)
        .then(pl.lit("high"))
        .otherwise(pl.lit("low"))
        .alias("band"),
        pl.col("score").rank(descending=True).alias("score_rank"),
        (pl.col("spend") / 100).alias("spend_norm"),
    )


def group_ranked_features(df: pl.DataFrame) -> pl.DataFrame:
    """Window features over user, then per-user aggregates, sorted by user.

    Why this approach: .over("user") computes the aggregate per group and
    aligns it back to the original rows in one pass — no join, no
    re-keying. The final group_by reduces one row per user.
    """
    return (
        df.with_columns(
            pl.col("spend").rank().over("user").alias("spend_rank_in_user"),
            (pl.col("spend") / pl.col("spend").sum().over("user"))
            .alias("share_of_user"),
        )
        .group_by("user")
        .agg(
            pl.len().alias("n_events"),
            pl.col("share_of_user").max().alias("max_share"),
            pl.col("spend").sum().alias("spend_total"),
        )
        .sort("user")
    )
