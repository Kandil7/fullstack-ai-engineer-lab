"""
Challenge 08: subqueries-ctes — Starter Code
=============================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def scalar_report(conn: sqlite3.Connection) -> dict:
    """Return {"rows": [(name, spend)...], "avg_spend": float}."""
    raise NotImplementedError


def anti_join(conn: sqlite3.Connection) -> dict:
    """Return {"not_exists": [...], "left_join": [...], "identical": bool}."""
    raise NotImplementedError


def recursive_spine(conn: sqlite3.Connection, start: str, end: str) -> list[tuple]:
    """Zero-filled daily event counts via WITH RECURSIVE."""
    raise NotImplementedError
