"""
Challenge 51: Serialization & Persistence — Reference Solution
================================================================
"""

from __future__ import annotations

import csv
import io
import json
import sqlite3
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------- Bronze


def csv_roundtrip(rows: list[dict]) -> list[dict]:
    """Write rows (shared key set) via DictWriter to a StringIO, read
    back with DictReader, return the dicts (values as strings).

    Why this approach: DictWriter writes the header and quotes any
    field containing commas, newlines, or quotes; DictReader reverses
    it exactly. StringIO sidesteps the file newline="" rule so the test
    stays platform-independent.
    """
    buf = io.StringIO()
    if rows:
        writer = csv.DictWriter(buf, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    buf.seek(0)
    return list(csv.DictReader(buf))


# ---------------------------------------------------------------- Silver


def _default_encoder(obj):
    """Encode unsupported types as self-describing marker dicts."""
    if isinstance(obj, datetime):
        return {"$iso": obj.isoformat()}
    if isinstance(obj, set):
        return {"$set": sorted(obj)}
    raise TypeError(f"cannot serialize {type(obj)}")


def _object_decoder(d):
    """Decode the markers written by _default_encoder."""
    if "$iso" in d:
        return datetime.fromisoformat(d["$iso"])
    if "$set" in d:
        return set(d["$set"])
    return d


def write_jsonl(path: Path, records: list[dict]) -> int:
    """Append records as JSONL, one complete object per line.

    Why this approach: append mode makes writes crash-safe per line;
    ensure_ascii=False keeps Arabic/Chinese literal on disk;
    allow_nan=False turns non-finite floats into a loud ValueError
    instead of a line other parsers reject. json.dumps escapes \n and
    quotes inside string values, so injected-looking text stays inside
    its own line and never becomes new records.
    """
    written = 0
    with path.open("a", encoding="utf-8") as f:
        for rec in records:
            f.write(
                json.dumps(rec, default=_default_encoder, ensure_ascii=False, allow_nan=False)
                + "\n"
            )
            written += 1
    return written


def read_jsonl(path: Path) -> list[dict]:
    """Return the decoded records, skipping blank lines."""
    records = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line, object_hook=_object_decoder))
    return records


# ------------------------------------------------------------------ Gold


def create_schema(conn: sqlite3.Connection) -> None:
    """Create table runs (id INTEGER PRIMARY KEY, name TEXT NOT NULL,
    score REAL)."""
    conn.execute(
        "CREATE TABLE runs (id INTEGER PRIMARY KEY, name TEXT NOT NULL, score REAL)"
    )


def insert_runs(conn: sqlite3.Connection, rows: list[tuple[str, float]]) -> int:
    """Bulk-insert (name, score) rows inside ONE transaction using
    executemany; return the number of rows.

    Why this approach: executemany is a single Python-level call for the
    whole batch (per-row execute loops are 10^4x more calls), and
    `with conn:` commits on success / rolls back the whole batch on any
    error — no partial writes.
    """
    with conn:
        conn.executemany("INSERT INTO runs (name, score) VALUES (?, ?)", rows)
    return len(rows)


def top_runs(conn: sqlite3.Connection, threshold: float) -> list[tuple]:
    """Parameterized SELECT name, score WHERE score >= ? ORDER BY score
    DESC; return the fetched rows."""
    cur = conn.execute(
        "SELECT name, score FROM runs WHERE score >= ? ORDER BY score DESC",
        (threshold,),
    )
    return cur.fetchall()
