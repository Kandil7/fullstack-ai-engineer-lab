"""
Challenge 12: normalization — Starter Code
===========================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def split_csv_column(conn: sqlite3.Connection) -> list[tuple]:
    """Migrate tags_csv into contact_tags; return sorted (contact_id, tag)."""
    raise NotImplementedError


def split_departments(conn: sqlite3.Connection) -> dict:
    """3NF split; return {"departments": n, "employees": n, "locations": [...]}."""
    raise NotImplementedError


def build_star_schema(conn: sqlite3.Connection) -> dict:
    """Dimensions + fact table; return the report dict."""
    raise NotImplementedError
