"""
Challenge 02: ddl-schema — Reference Solution
==============================================
"""

import sqlite3


def create_products_table(conn: sqlite3.Connection) -> None:
    """Products table with NOT NULL, UNIQUE, CHECK, DEFAULT constraints."""
    conn.execute(
        "CREATE TABLE products ("
        "id INTEGER PRIMARY KEY,"
        "sku TEXT NOT NULL UNIQUE,"
        "price REAL NOT NULL CHECK (price >= 0),"
        "stock INTEGER NOT NULL DEFAULT 0)"
    )


def add_status_and_backfill(conn: sqlite3.Connection) -> dict:
    """Add nullable status; backfill in batches of 1000."""
    conn.execute("ALTER TABLE products ADD COLUMN status TEXT")

    total = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    batch_size = 1000
    lo, hi = 1, batch_size
    while lo <= total:
        conn.execute(
            "UPDATE products SET status = CASE WHEN price > 50 THEN 'premium'"
            " ELSE 'standard' END WHERE id BETWEEN ? AND ?", (lo, hi))
        lo += batch_size
        hi += batch_size

    premium = conn.execute(
        "SELECT COUNT(*) FROM products WHERE status = 'premium'").fetchone()[0]
    return {"rows": total, "premium": premium}


def create_audit_schema(conn: sqlite3.Connection) -> dict:
    """Orders/order_items with CASCADE and a generated total column."""
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY)")
    conn.execute(
        "CREATE TABLE order_items ("
        "id INTEGER PRIMARY KEY,"
        "order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,"
        "qty INTEGER NOT NULL,"
        "unit_price REAL NOT NULL,"
        "total REAL GENERATED ALWAYS AS (qty * unit_price) STORED)"
    )
    conn.execute("INSERT INTO orders DEFAULT VALUES")
    conn.executemany(
        "INSERT INTO order_items (order_id, qty, unit_price) VALUES (?, ?, ?)",
        [(1, 1, 10.0), (1, 1, 4.5)])
    generated = conn.execute(
        "SELECT SUM(total) FROM order_items WHERE order_id = 1").fetchone()[0]
    conn.execute("DELETE FROM orders WHERE id = 1")
    items = conn.execute("SELECT COUNT(*) FROM order_items").fetchone()[0]
    return {"items": items, "generated": generated}
