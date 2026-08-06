"""
Challenge 13: sql-injection — Starter Code
===========================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def safe_login(conn: sqlite3.Connection, username: str) -> tuple | None:
    """Parameterized user lookup; malicious input returns None."""
    raise NotImplementedError


def safe_sort(conn: sqlite3.Connection, column_name: str, ascending: bool) -> list[tuple]:
    """Sort by whitelisted column; ValueError for unknown names."""
    raise NotImplementedError


def secure_search(conn: sqlite3.Connection, term: str, limit: int) -> dict:
    """Parameterized LIKE search; return {"rows": [...], "probe_ok": bool}."""
    raise NotImplementedError
