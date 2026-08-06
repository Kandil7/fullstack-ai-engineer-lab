"""
Challenge 03: insert-update-delete — Hidden Tests
==================================================
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


def fresh_conn() -> sqlite3.Connection:
    return sqlite3.connect(":memory:")


class TestInsertModels:
    def test_batch_insert(self):
        conn = fresh_conn()
        count = solution_module.insert_models(
            conn, [("bert", 1, 0.9), ("gpt", 2, 0.8), ("llm", 3, 0.7)])
        assert count == 3
        total = conn.execute("SELECT COUNT(*) FROM models").fetchone()[0]
        assert total == 3

    def test_empty_list(self):
        conn = fresh_conn()
        count = solution_module.insert_models(conn, [])
        assert count == 0

    def test_duplicate_name_rejected(self):
        conn = fresh_conn()
        solution_module.insert_models(conn, [("bert", 1, 0.9)])
        with pytest.raises(sqlite3.IntegrityError):
            solution_module.insert_models(conn, [("bert", 2, 0.95)])

    def test_reuses_existing_table(self):
        conn = fresh_conn()
        conn.execute(
            "CREATE TABLE models (id INTEGER PRIMARY KEY, name TEXT UNIQUE, "
            "epoch INT, metric REAL)")
        conn.execute("INSERT INTO models (name, epoch, metric) VALUES (?, ?, ?)",
                     ("old", 0, 0.0))
        count = solution_module.insert_models(conn, [("new", 1, 0.5)])
        assert count == 1


class TestSyncModels:
    def test_inserts_and_updates(self):
        conn = fresh_conn()
        solution_module.insert_models(conn, [("bert", 1, 0.9)])
        result = solution_module.sync_models(conn, [("bert", 2, 0.95), ("gpt", 1, 0.8)])
        assert result == [("bert", 2), ("gpt", 1)]

    def test_idempotent(self):
        conn = fresh_conn()
        rows = [("bert", 2, 0.95), ("gpt", 1, 0.8)]
        first = solution_module.sync_models(conn, rows)
        second = solution_module.sync_models(conn, rows)
        assert first == second
        total = conn.execute("SELECT COUNT(*) FROM models").fetchone()[0]
        assert total == 2

    def test_empty_sync(self):
        conn = fresh_conn()
        result = solution_module.sync_models(conn, [])
        assert result == []

    def test_sorted_by_name(self):
        conn = fresh_conn()
        result = solution_module.sync_models(
            conn, [("zebra", 1, 0.1), ("alpha", 2, 0.2)])
        assert result == [("alpha", 2), ("zebra", 1)]


class TestApplyChangeset:
    def test_ids_in_operation_order(self):
        conn = fresh_conn()
        ids = solution_module.apply_changeset(conn, [
            ("insert", "a", 1),
            ("insert", "b", 1),
            ("update", "a", 2),
            ("delete", "b"),
        ])
        assert ids == [1, 2, 1, 2]

    def test_delete_missing_is_skipped(self):
        conn = fresh_conn()
        ids = solution_module.apply_changeset(conn, [("delete", "ghost")])
        assert ids == []

    def test_update_missing_is_skipped(self):
        conn = fresh_conn()
        ids = solution_module.apply_changeset(conn, [("update", "ghost", 5)])
        assert ids == []

    def test_final_state_correct(self):
        conn = fresh_conn()
        solution_module.apply_changeset(conn, [
            ("insert", "a", 1),
            ("insert", "b", 2),
            ("delete", "a"),
        ])
        rows = conn.execute("SELECT name, epoch FROM models").fetchall()
        assert rows == [("b", 2)]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
