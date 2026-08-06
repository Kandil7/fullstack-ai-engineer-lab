"""
Challenge 51: Serialization & Persistence — Tests

Runs against starter.py by default (functions raise NotImplementedError
and must FAIL). Set CHALLENGE_USE_SOLUTION=1 to validate solution.py
(expect ALL PASS).
"""

from __future__ import annotations

import importlib.util
import json
import os
import sqlite3
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

_DIR = Path(__file__).parent
_TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"

_spec = importlib.util.spec_from_file_location("mod51", _DIR / f"{_TARGET}.py")
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


def _call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except NotImplementedError:
        pytest.fail("Not implemented yet")


def _fresh_db():
    conn = sqlite3.connect(":memory:")
    _call(mod.create_schema, conn)
    return conn


# ---------------------------------------------------------------- Bronze


def test_csv_plain_roundtrip():
    rows = [{"id": "1", "text": "plain"}]
    assert _call(mod.csv_roundtrip, rows) == rows


def test_csv_embedded_comma():
    rows = [{"id": "1", "text": "contains, a comma"}]
    assert _call(mod.csv_roundtrip, rows) == rows


def test_csv_embedded_newline():
    rows = [{"id": "2", "text": "has a\nnewline"}]
    assert _call(mod.csv_roundtrip, rows) == rows


def test_csv_embedded_quote():
    rows = [{"id": "3", "text": 'says "hi"'}]
    assert _call(mod.csv_roundtrip, rows) == rows


def test_csv_values_stay_strings():
    got = _call(mod.csv_roundtrip, [{"id": "1", "n": "007"}])
    assert got == [{"id": "1", "n": "007"}]
    assert isinstance(got[0]["n"], str)


def test_csv_empty_rows():
    assert _call(mod.csv_roundtrip, []) == []


# ---------------------------------------------------------------- Silver


def test_jsonl_basic_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "d.jsonl"
        records = [{"a": 1, "b": [1, 2]}, {"a": 2, "b": []}]
        assert _call(mod.write_jsonl, p, records) == 2
        assert _call(mod.read_jsonl, p) == records


def test_jsonl_append_is_cumulative():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "d.jsonl"
        _call(mod.write_jsonl, p, [{"i": 0}])
        _call(mod.write_jsonl, p, [{"i": 1}, {"i": 2}])
        raw_lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln]
        assert len(raw_lines) == 3
        assert _call(mod.read_jsonl, p) == [{"i": 0}, {"i": 1}, {"i": 2}]


def test_jsonl_newline_in_value_stays_one_line():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "d.jsonl"
        text = "x\nsecond line"
        _call(mod.write_jsonl, p, [{"text": text}])
        raw_lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln]
        assert len(raw_lines) == 1, "embedded newline must be escaped, not split"
        assert _call(mod.read_jsonl, p) == [{"text": text}]


def test_jsonl_injection_string_is_inert():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "d.jsonl"
        evil = 'x"}, {"hacked": true}'
        _call(mod.write_jsonl, p, [{"user": evil}])
        raw_lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln]
        assert len(raw_lines) == 1, "injection payload must not create lines"
        # the raw line must parse as exactly ONE object with the payload
        # still inside the string value — it must not escape into keys
        assert json.loads(raw_lines[0]) == {"user": evil}
        got = _call(mod.read_jsonl, p)
        assert got == [{"user": evil}]
        assert "hacked" not in got[0]


def test_jsonl_datetime_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "d.jsonl"
        rec = {"t": datetime(2026, 8, 6, 9, 0)}
        _call(mod.write_jsonl, p, [rec])
        got = _call(mod.read_jsonl, p)
        assert got == [rec]
        assert isinstance(got[0]["t"], datetime)


def test_jsonl_set_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "d.jsonl"
        rec = {"s": {"b", "a"}}
        _call(mod.write_jsonl, p, [rec])
        got = _call(mod.read_jsonl, p)
        assert got == [rec]
        assert isinstance(got[0]["s"], set)


def test_jsonl_unicode_literal_on_disk():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "d.jsonl"
        _call(mod.write_jsonl, p, [{"text": "مرحبا"}])
        raw = p.read_text(encoding="utf-8")
        assert "مرحبا" in raw, "ensure_ascii=False must keep the literal text"


def test_jsonl_nan_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "d.jsonl"
        with pytest.raises(ValueError):
            _call(mod.write_jsonl, p, [{"s": float("nan")}])
        assert not p.exists() or p.read_text(encoding="utf-8") == "", (
            "a rejected record must not leave a partial line"
        )


def test_jsonl_empty_file():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "d.jsonl"
        p.write_text("\n\n", encoding="utf-8")
        assert _call(mod.read_jsonl, p) == []


# ------------------------------------------------------------------ Gold


def test_insert_and_top_runs_basic():
    conn = _fresh_db()
    assert _call(mod.insert_runs, conn, [("baseline", 0.71), ("augmented", 0.85)]) == 2
    assert _call(mod.top_runs, conn, 0.8) == [("augmented", 0.85)]
    conn.close()


def test_top_runs_ordering_and_boundary():
    conn = _fresh_db()
    _call(mod.insert_runs, conn, [("c", 0.5), ("a", 0.9), ("b", 0.7), ("d", 0.5)])
    assert _call(mod.top_runs, conn, 0.6) == [("a", 0.9), ("b", 0.7)]
    # boundary is inclusive (>=)
    assert _call(mod.top_runs, conn, 0.5) == [("a", 0.9), ("b", 0.7), ("c", 0.5), ("d", 0.5)]
    conn.close()


def test_injection_resistance():
    conn = _fresh_db()
    evil = "x'); DROP TABLE runs; --"
    assert _call(mod.insert_runs, conn, [("safe", 0.9), (evil, 0.5)]) == 2
    assert _call(mod.top_runs, conn, 0.6) == [("safe", 0.9)]
    tables = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='runs'"
    ).fetchone()[0]
    assert tables == 1, "injection payload must be inert data"
    conn.close()


def test_rollback_on_bad_row():
    conn = _fresh_db()
    with pytest.raises(sqlite3.IntegrityError):
        _call(mod.insert_runs, conn, [("ok", 0.1), (None, 0.2)])
    count = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
    assert count == 0, "a failed batch must leave no partial rows"
    conn.close()


def test_insert_uses_single_bulk_call():
    # sqlite3.Connection is immutable: the documented extension point is
    # subclassing via the factory= parameter, with execute() tracing.
    # executemany dispatches exactly ONE internal execute; a per-row
    # execute loop would count 20,000.
    class CountingConn(sqlite3.Connection):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._db_calls = 0

        def execute(self, sql, params=()):
            self._db_calls += 1
            return super().execute(sql, params)

    conn = sqlite3.connect(":memory:", factory=CountingConn)
    _call(mod.create_schema, conn)

    n = 20_000
    rows = [(f"run-{i}", i / n) for i in range(n)]
    got = _call(mod.insert_runs, conn, rows)
    assert got == n
    assert conn._db_calls == 1, (
        f"expected exactly 1 DB call, got {conn._db_calls}"
    )
    conn.close()


def test_insert_returns_count():
    conn = _fresh_db()
    assert _call(mod.insert_runs, conn, []) == 0
    assert _call(mod.insert_runs, conn, [("x", 0.1), ("y", 0.2), ("z", 0.3)]) == 3
    assert _call(mod.top_runs, conn, 0.0) == [("z", 0.3), ("y", 0.2), ("x", 0.1)]
    conn.close()
