"""
Challenge 13: sql-injection — Hidden Tests
===========================================
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


def users_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, role TEXT)")
    conn.execute("INSERT INTO users (username, role) VALUES ('admin', 'owner')")
    return conn


def models_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE models (id INTEGER PRIMARY KEY, name TEXT, metric REAL)")
    conn.executemany(
        "INSERT INTO models (name, metric) VALUES (?, ?)",
        [("bert", 0.9), ("gpt", 0.8), ("bert_v2", 0.95)])
    return conn


class TestSafeLogin:
    def test_found_user(self):
        conn = users_conn()
        assert solution_module.safe_login(conn, "admin") == (1, "admin", "owner")

    def test_missing_user(self):
        conn = users_conn()
        assert solution_module.safe_login(conn, "nobody") is None

    def test_injection_returns_none(self):
        conn = users_conn()
        result = solution_module.safe_login(conn, "admin' OR '1'='1")
        assert result is None

    def test_union_injection_returns_none(self):
        conn = users_conn()
        result = solution_module.safe_login(conn, "' UNION SELECT 1, 'x', 'y' --")
        assert result is None

    def test_creates_table(self):
        conn = sqlite3.connect(":memory:")
        assert solution_module.safe_login(conn, "x") is None


class TestSafeSort:
    def test_sort_by_metric_desc(self):
        conn = models_conn()
        result = solution_module.safe_sort(conn, "metric", False)
        assert [r[0] for r in result] == ["bert_v2", "bert", "gpt"]

    def test_sort_by_name_asc(self):
        conn = models_conn()
        result = solution_module.safe_sort(conn, "name", True)
        assert [r[0] for r in result] == ["bert", "bert_v2", "gpt"]

    def test_unknown_column_raises(self):
        conn = models_conn()
        with pytest.raises(ValueError):
            solution_module.safe_sort(conn, "metric; DROP TABLE models; --", False)

    def test_creates_table(self):
        conn = sqlite3.connect(":memory:")
        assert solution_module.safe_sort(conn, "name", True) == []


class TestSecureSearch:
    def test_pattern_search(self):
        conn = models_conn()
        result = solution_module.secure_search(conn, "bert", 10)
        assert [r[0] for r in result["rows"]] == ["bert", "bert_v2"]

    def test_limit_validated(self):
        conn = models_conn()
        result = solution_module.secure_search(conn, "", 999)
        assert len(result["rows"]) == 3  # clamped to 10

    def test_limit_string_coerced(self):
        conn = models_conn()
        result = solution_module.secure_search(conn, "bert", "1")
        assert len(result["rows"]) == 1

    def test_probe_blocked(self):
        conn = models_conn()
        result = solution_module.secure_search(
            conn, "bert'; DELETE FROM models; --", 5)
        assert result["probe_ok"] is True
        assert conn.execute("SELECT COUNT(*) FROM models").fetchone()[0] == 3

    def test_probe_rows_safe(self):
        conn = models_conn()
        result = solution_module.secure_search(
            conn, "x'; DROP TABLE models; --", 5)
        assert result["rows"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
