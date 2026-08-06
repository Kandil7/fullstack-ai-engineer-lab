"""
Challenge 11: transactions — Starter Code
==========================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def atomic_transfer(conn: sqlite3.Connection, from_id: int, to_id: int, amount: float) -> dict:
    """Transfer inside one transaction; roll back on any failure."""
    raise NotImplementedError


def rollback_on_error(conn: sqlite3.Connection, ops: list[tuple]) -> dict:
    """Apply (account_id, delta) ops; all-or-nothing on IntegrityError."""
    raise NotImplementedError


def savepoint_partial(conn: sqlite3.Connection, ops: list[tuple]) -> dict:
    """Per-op savepoints; failed ops roll back alone and the rest persist."""
    raise NotImplementedError
