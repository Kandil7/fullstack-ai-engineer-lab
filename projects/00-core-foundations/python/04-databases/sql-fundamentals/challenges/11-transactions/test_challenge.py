"""
Challenge 11: transactions — Hidden Tests
==========================================
"""

import sqlite3
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

starter_spec = importlib.util.spec_from_file_location(
    "starter", Path(__file__).parent / "starter.py")
starter_module = importlib.util.module_from_spec(starter_spec)
starter_spec.loader.exec_module(starter_module)

solution_spec = importlib.util.spec_from_file_location(
    "solution", Path(__file__).parent / "solution.py")
solution_module = importlib.util.module_from_spec(solution_spec)
solution_spec.loader.exec_module(solution_module)

import pytest


def accounts_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance REAL NOT NULL "
        "CHECK (balance >= 0))")
    conn.executemany("INSERT INTO accounts (id, balance) VALUES (?, ?)",
                     [(1, 100.0), (2, 50.0)])
    conn.commit()  # close the implicit transaction so `with conn:` starts fresh
    return conn


class TestAtomicTransfer:
    def test_successful_transfer(self):
        conn = accounts_conn()
        result = solution_module.atomic_transfer(conn, 1, 2, 30.0)
        assert result == {"from": 70.0, "to": 80.0}

    def test_overdraft_rolls_back(self):
        conn = accounts_conn()
        result = solution_module.atomic_transfer(conn, 2, 1, 200.0)
        assert result["rolled_back"] is True
        assert result["total"] == pytest.approx(150.0)

    def test_no_partial_writes(self):
        conn = accounts_conn()
        solution_module.atomic_transfer(conn, 2, 1, 200.0)
        assert conn.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()[0] == 100.0
        assert conn.execute("SELECT balance FROM accounts WHERE id = 2").fetchone()[0] == 50.0

    def test_creates_table(self):
        conn = accounts_conn()
        result = solution_module.atomic_transfer(conn, 1, 2, 1.0)
        assert isinstance(result, dict)
        assert result == {"from": 99.0, "to": 51.0}


class TestRollbackOnError:
    def test_all_applied(self):
        conn = accounts_conn()
        result = solution_module.rollback_on_error(conn, [(1, -40.0), (2, -20.0)])
        assert result["applied"] == 2
        assert result["final_balances"] == {1: 60.0, 2: 30.0}

    def test_failure_rolls_back_all(self):
        conn = accounts_conn()
        result = solution_module.rollback_on_error(conn, [(1, -40.0), (2, -60.0)])
        assert result["rolled_back"] is True
        assert result["final_balances"] == {1: 100.0, 2: 50.0}

    def test_failure_leaves_db_clean(self):
        conn = accounts_conn()
        solution_module.rollback_on_error(conn, [(1, -40.0), (2, -60.0)])
        assert conn.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()[0] == 100.0


class TestSavepointPartial:
    def test_partial_success(self):
        conn = accounts_conn()
        result = solution_module.savepoint_partial(
            conn, [(1, -40.0), (2, -60.0), (1, -10.0)])
        assert result["applied"] == 2
        assert result["failed"] == 1
        assert result["final_balances"] == {1: 50.0, 2: 50.0}

    def test_all_success(self):
        conn = accounts_conn()
        result = solution_module.savepoint_partial(conn, [(1, -10.0), (2, -10.0)])
        assert result["applied"] == 2
        assert result["failed"] == 0
        assert result["final_balances"] == {1: 90.0, 2: 40.0}

    def test_all_fail(self):
        conn = accounts_conn()
        result = solution_module.savepoint_partial(conn, [(1, -500.0), (2, -500.0)])
        assert result["applied"] == 0
        assert result["failed"] == 2
        assert result["final_balances"] == {1: 100.0, 2: 50.0}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
