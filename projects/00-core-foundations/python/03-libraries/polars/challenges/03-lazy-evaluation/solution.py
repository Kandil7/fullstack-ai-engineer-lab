"""
Challenge 03: Polars Lazy Evaluation — Reference Solution
===========================================================
"""

from __future__ import annotations

import polars as pl


def lazy_count(path: str) -> int:
    """Count rows of a CSV via a lazy scan; never read_csv.

    Why this approach: pl.len() over a lazy scan answers the count from
    the plan; the streaming engine keeps memory bounded. The [0, 0]
    index extracts the int from the single-cell frame.
    """
    return pl.scan_csv(path).select(pl.len()).collect(engine="streaming")[0, 0]


def predicate_pushed(path: str, column: str, value: str) -> bool:
    """True iff the optimized plan pushes the filter into the scan.

    Why this approach: the optimized plan shows a pushed predicate as a
    SELECTION line at the scan node. Explaining is metadata-only — no
    data is read, which is exactly what the check is for.
    """
    plan = (
        pl.scan_parquet(path)
        .filter(pl.col(column) == value)
        .explain(optimized=True)
    )
    return "SELECTION" in plan


def _projected_columns(plan: str) -> int:
    """Parse 'PROJECT n/m COLUMNS' from an optimized plan text."""
    for line in plan.splitlines():
        line = line.strip()
        if line.startswith("PROJECT") and "COLUMNS" in line:
            return int(line.split()[1].split("/")[0])
    return -1


def project_and_filter(path: str, keep: list[str], column: str, value: str) -> tuple[pl.DataFrame, int]:
    """Return (result, columns_read) with columns_read from the plan.

    Why this approach: building the whole pipeline on the lazy frame lets
    the optimizer push both the predicate and the projection into the
    parquet scan; the plan text then proves how many columns were read.
    """
    lf = (
        pl.scan_parquet(path)
        .filter(pl.col(column) == value)
        .select(keep)
    )
    plan = lf.explain(optimized=True)
    result = lf.collect(engine="streaming")
    return result, _projected_columns(plan)
