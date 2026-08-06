"""
Challenge 11: transactions — Reference Solution
================================================
"""

import sqlite3


def _ensure_accounts(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS accounts ("
        "id INTEGER PRIMARY KEY, balance REAL NOT NULL CHECK (balance >= 0))")


def _balances(conn: sqlite3.Connection) -> dict:
    return {r[0]: r[1] for r in conn.execute("SELECT id, balance FROM accounts")}


def atomic_transfer(conn: sqlite3.Connection, from_id: int, to_id: int, amount: float) -> dict:
    """One transaction; CHECK violation rolls everything back."""
    _ensure_accounts(conn)
    try:
        with conn:
            conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?",
                         (amount, from_id))
            conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?",
                         (amount, to_id))
        b = _balances(conn)
        return {"from": b[from_id], "to": b[to_id]}
    except sqlite3.IntegrityError:
        return {"rolled_back": True,
                "total": sum(_balances(conn).values())}


def rollback_on_error(conn: sqlite3.Connection, ops: list[tuple]) -> dict:
    """All-or-nothing batch."""
    _ensure_accounts(conn)
    try:
        with conn:
            for account_id, delta in ops:
                conn.execute(
                    "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                    (delta, account_id))
        return {"applied": len(ops), "final_balances": _balances(conn)}
    except sqlite3.IntegrityError:
        return {"rolled_back": True, "final_balances": _balances(conn)}


def savepoint_partial(conn: sqlite3.Connection, ops: list[tuple]) -> dict:
    """Savepoint per op; a failing op rolls back alone."""
    _ensure_accounts(conn)
    applied = 0
    failed = 0
    with conn:
        for i, (account_id, delta) in enumerate(ops):
            conn.execute("SAVEPOINT s")
            try:
                conn.execute(
                    "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                    (delta, account_id))
                conn.execute("RELEASE s")
                applied += 1
            except sqlite3.IntegrityError:
                conn.execute("ROLLBACK TO s")
                conn.execute("RELEASE s")
                failed += 1
    return {"applied": applied, "failed": failed,
            "final_balances": _balances(conn)}
