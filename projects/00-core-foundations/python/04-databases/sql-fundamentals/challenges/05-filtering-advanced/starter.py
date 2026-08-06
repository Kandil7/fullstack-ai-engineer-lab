"""
Challenge 05: filtering-advanced — Starter Code
================================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def filter_range(conn: sqlite3.Connection, lo: float, hi: float) -> list[str]:
    """Names with metric in [lo, hi], sorted."""
    raise NotImplementedError


def pattern_match(conn: sqlite3.Connection, pattern: str) -> dict:
    """Return {"names": [...], "single_underscore": n} using SQL LIKE."""
    raise NotImplementedError


def null_aware_report(conn: sqlite3.Connection) -> dict:
    """CASE-bucket NULL vs ok; EXISTS for runs; return the report dict."""
    raise NotImplementedError
