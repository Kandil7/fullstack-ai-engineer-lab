"""
Challenge 09: window-functions — Starter Code
==============================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def rank_rows(conn: sqlite3.Connection) -> list[tuple]:
    """(model, metric, rn, rank, dense) per partition by metric DESC."""
    raise NotImplementedError


def lag_delta(conn: sqlite3.Connection) -> list[tuple]:
    """(model, run_ts, metric, delta) with LAG over the model partition."""
    raise NotImplementedError


def frames_report(conn: sqlite3.Connection) -> list[tuple]:
    """Running total + 3-row moving average per model."""
    raise NotImplementedError
