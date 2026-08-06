"""
Challenge 14: query-optimization — Starter Code
================================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def sargable_plan(conn: sqlite3.Connection) -> dict:
    """Return {"sargable": [...], "wrapped": [...]} plan strings."""
    raise NotImplementedError


def keyset_page(conn: sqlite3.Connection, after_id: int, limit: int) -> dict:
    """Keyset page; return {"rows": [...], "plan": [...]}."""
    raise NotImplementedError


def batch_fetch(conn: sqlite3.Connection, parent_ids: list[int], batch_size: int) -> dict:
    """Chunked IN queries; return {"rows": [...], "queries": n}."""
    raise NotImplementedError
