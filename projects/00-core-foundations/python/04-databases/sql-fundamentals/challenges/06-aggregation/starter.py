"""
Challenge 06: aggregation — Starter Code
=========================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def group_totals(conn: sqlite3.Connection) -> list[tuple]:
    """Per-model (model, runs, total, avg) ordered by avg DESC."""
    raise NotImplementedError


def having_filter(conn: sqlite3.Connection, min_runs: int, min_avg: float) -> list[tuple]:
    """Models with >= min_runs runs and avg >= min_avg (HAVING only)."""
    raise NotImplementedError


def aggregate_report(conn: sqlite3.Connection) -> dict:
    """WHERE-before-GROUP report; return {"rows": [...], "global_avg": float}."""
    raise NotImplementedError
