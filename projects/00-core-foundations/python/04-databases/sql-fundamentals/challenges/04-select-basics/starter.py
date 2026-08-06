"""
Challenge 04: select-basics — Starter Code
===========================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def top_n(conn: sqlite3.Connection, n: int) -> list[tuple]:
    """Return top-n (name, metric) by metric DESC, name ASC."""
    raise NotImplementedError


def metric_report(conn: sqlite3.Connection) -> dict:
    """Return {"report": [(name, score)...], "distinct_names": n}.

    score = metric * 100, sorted by score DESC.
    """
    raise NotImplementedError


def paginate(conn: sqlite3.Connection, page_size: int, page: int) -> dict:
    """Return {"rows": [...], "total": n, "has_next": bool}."""
    raise NotImplementedError
