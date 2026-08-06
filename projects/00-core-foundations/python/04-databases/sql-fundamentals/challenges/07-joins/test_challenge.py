"""
Challenge 07: joins — Hidden Tests
==================================
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


def post_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT)")
    conn.executemany("INSERT INTO users (name) VALUES (?)", [("ana",), ("bob",)])
    conn.executemany(
        "INSERT INTO posts (user_id, title) VALUES (?, ?)",
        [(1, "alpha"), (1, "beta")])
    return conn


class TestInnerJoinPairs:
    def test_only_writers(self):
        conn = post_conn()
        result = solution_module.inner_join_pairs(conn)
        assert result == [("ana", "alpha"), ("ana", "beta")]

    def test_sorted(self):
        conn = post_conn()
        conn.execute("INSERT INTO posts (user_id, title) VALUES (1, 'zero')")
        result = solution_module.inner_join_pairs(conn)
        assert result == [("ana", "alpha"), ("ana", "beta"), ("ana", "zero")]

    def test_empty_posts(self):
        conn = post_conn()
        conn.execute("DELETE FROM posts")
        assert solution_module.inner_join_pairs(conn) == []

    def test_creates_tables(self):
        conn = sqlite3.connect(":memory:")
        assert solution_module.inner_join_pairs(conn) == []


class TestLeftJoinWithNulls:
    def test_counts_and_inactive(self):
        conn = post_conn()
        result = solution_module.left_join_with_nulls(conn)
        assert result["counts"] == [("ana", 2), ("bob", 0)]
        assert result["inactive_names"] == ["bob"]

    def test_all_active(self):
        conn = post_conn()
        conn.execute("INSERT INTO posts (user_id, title) VALUES (2, 'b1')")
        result = solution_module.left_join_with_nulls(conn)
        assert result["inactive_names"] == []

    def test_no_users(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT)")
        result = solution_module.left_join_with_nulls(conn)
        assert result["counts"] == []
        assert result["inactive_names"] == []


class TestSelfJoinReport:
    def _emp(self):
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, mgr_id INTEGER)")
        conn.executemany(
            "INSERT INTO employees (id, name, mgr_id) VALUES (?, ?, ?)",
            [(1, "ana", None), (2, "bob", 1), (3, "cam", 1), (4, "dave", 2)])
        return conn

    def test_report_rows(self):
        conn = self._emp()
        result = solution_module.self_join_report(conn)
        assert ("ana", "ROOT", 0) in result["rows"]
        assert ("bob", "ana", 1) in result["rows"]
        assert ("cam", "ana", 1) in result["rows"]
        assert ("dave", "bob", 2) in result["rows"]

    def test_distinct_teams(self):
        conn = self._emp()
        result = solution_module.self_join_report(conn)
        assert result["distinct_teams"] == [("ana", 2), ("bob", 1)]

    def test_single_root(self):
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, mgr_id INTEGER)")
        conn.execute("INSERT INTO employees (id, name, mgr_id) VALUES (1, 'solo', NULL)")
        result = solution_module.self_join_report(conn)
        assert result["rows"] == [("solo", "ROOT", 0)]
        assert result["distinct_teams"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
