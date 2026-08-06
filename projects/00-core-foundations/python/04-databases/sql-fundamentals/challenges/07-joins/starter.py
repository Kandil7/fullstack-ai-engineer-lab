"""
Challenge 07: joins — Starter Code
==================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def inner_join_pairs(conn: sqlite3.Connection) -> list[tuple]:
    """(user_name, post_title) for every post; users without posts absent."""
    raise NotImplementedError


def left_join_with_nulls(conn: sqlite3.Connection) -> dict:
    """Return {"counts": [(name, n)...], "inactive_names": [...]}."""
    raise NotImplementedError


def self_join_report(conn: sqlite3.Connection) -> dict:
    """Self-join employee report; return {"rows": [...], "distinct_teams": [...]}."""
    raise NotImplementedError
