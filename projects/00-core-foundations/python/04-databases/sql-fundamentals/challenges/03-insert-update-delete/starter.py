"""
Challenge 03: insert-update-delete — Starter Code
==================================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def insert_models(conn: sqlite3.Connection, rows: list[tuple]) -> int:
    """Insert (name, epoch, metric) rows with executemany; return rowcount.

    Creates the models table if missing.
    """
    raise NotImplementedError


def sync_models(conn: sqlite3.Connection, rows: list[tuple]) -> list[tuple]:
    """Upsert rows by name; return final (name, epoch) sorted by name."""
    raise NotImplementedError


def apply_changeset(conn: sqlite3.Connection, ops: list[tuple]) -> list[int]:
    """Apply ("insert"|"update"|"delete", ...) ops with RETURNING id.

    Return affected ids in operation order.
    """
    raise NotImplementedError
