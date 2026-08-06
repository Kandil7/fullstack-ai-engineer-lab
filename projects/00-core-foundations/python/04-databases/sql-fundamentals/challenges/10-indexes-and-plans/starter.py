"""
Challenge 10: indexes-and-plans — Starter Code
===============================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def plan_for(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> list[str]:
    """Return EXPLAIN QUERY PLAN detail strings for a query."""
    raise NotImplementedError


def sargable_vs_not(conn: sqlite3.Connection) -> dict:
    """Indexed events table; return {"sargable": [...], "wrapped": [...]}."""
    raise NotImplementedError


def covering_vs_table(conn: sqlite3.Connection) -> dict:
    """Return {"covering": [...], "star": [...]} plans."""
    raise NotImplementedError


def index_strategy(conn: sqlite3.Connection) -> dict:
    """Composite + partial indexes; return plan dict for three queries."""
    raise NotImplementedError
