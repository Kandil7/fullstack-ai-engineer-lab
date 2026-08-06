"""
Challenge 02: ddl-schema — Starter Code
========================================
Fill in the function bodies. Do not modify signatures.
"""

import sqlite3


def create_products_table(conn: sqlite3.Connection) -> None:
    """Create products: id PK, sku NOT NULL UNIQUE, price CHECK >= 0, stock DEFAULT 0."""
    raise NotImplementedError


def add_status_and_backfill(conn: sqlite3.Connection) -> dict:
    """Add nullable status column; backfill in batches of 1000.

    price > 50 -> 'premium', else 'standard'.
    Returns {"rows": n, "premium": n}.
    """
    raise NotImplementedError


def create_audit_schema(conn: sqlite3.Connection) -> dict:
    """Build orders/order_items with CASCADE + generated total column.

    Insert a 2-item order, delete the order, and return
    {"items": 0, "generated": 14.5}.
    """
    raise NotImplementedError
