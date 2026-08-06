"""
Challenge 03: Polars Lazy Evaluation — Starter Code
=====================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

import polars as pl


def lazy_count(path: str) -> int:
    """Count rows of a CSV via a lazy scan; never read_csv."""
    raise NotImplementedError


def predicate_pushed(path: str, column: str, value: str) -> bool:
    """True iff the optimized plan pushes the filter into the scan."""
    raise NotImplementedError


def project_and_filter(path: str, keep: list[str], column: str, value: str) -> tuple[pl.DataFrame, int]:
    """Return (result, columns_read) with columns_read from the plan."""
    raise NotImplementedError
