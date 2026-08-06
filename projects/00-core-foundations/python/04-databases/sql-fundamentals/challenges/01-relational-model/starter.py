"""
Challenge 01: relational-model — Starter Code
==============================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def create_relational_schema(conn: sqlite3.Connection) -> list[str]:
    """Build students/courses/enrollments with PKs and FKs.

    Returns the sorted list of table names.
    """
    raise NotImplementedError


def enforce_keys(conn: sqlite3.Connection) -> dict:
    """Insert sample rows; prove PK uniqueness and FK enforcement.

    Returns {"rows": n, "dup_rejected": bool, "orphan_rejected": bool}.
    """
    raise NotImplementedError


def purge_abandoned_courses(conn: sqlite3.Connection) -> list[str]:
    """Delete courses with no enrollments; return remaining titles sorted.

    Use NOT EXISTS or LEFT JOIN + IS NULL. Never NOT IN (NULL trap).
    """
    raise NotImplementedError
