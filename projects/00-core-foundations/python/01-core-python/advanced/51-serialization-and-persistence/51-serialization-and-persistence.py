"""
01-core-python — 51: Serialization & Persistence — Data That Survives
=====================================================================
Topics: JSON limits (sets/tuples/datetime; default=/object_hook), CSV
        (DictReader/DictWriter, quoting, newline=''), pickle protocols and
        SECURITY (never unpickle untrusted data), JSONL for datasets, sqlite3
        with parameterized queries (never string interpolation), shelve

Why this matters for AI/backend engineering:
    JSONL is the standard fine-tuning dataset format. sqlite3 backs local
    vector-store metadata. Pickled .pkl model artifacts are a supply-chain
    risk — a malicious pickle executes code on load. Getting these right is
    day-one production work for any AI engineer.

Run:      python 51-serialization-and-persistence.py
Verify:   python 51-serialization-and-persistence.py --verify
Reference: https://docs.python.org/3/library/json.html
"""

from __future__ import annotations

import csv
import io
import json
import pickle
import sqlite3
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# ============================================================
# 1. JSON — Portable But Limited
# ============================================================
# JSON supports dict/list/str/int/float/bool/None ONLY. Tuples become lists,
# sets fail, datetime fails. Provide default= and object_hook to extend it.

# Example 1: the tuple -> list loss
payload = {"pair": (1, 2), "name": "qwen"}
encoded = json.dumps(payload)
print(f"Tuple became: {type(json.loads(encoded)['pair']).__name__}")

# Example 2: custom serialization for datetime and sets
def default_encoder(obj):
    if isinstance(obj, datetime):
        return {"$iso": obj.isoformat()}
    if isinstance(obj, set):
        return {"$set": sorted(obj)}
    raise TypeError(f"cannot serialize {type(obj)}")


def object_decoder(d):
    if "$iso" in d:
        return datetime.fromisoformat(d["$iso"])
    if "$set" in d:
        return set(d["$set"])
    return d


blob = {"created": datetime(2026, 8, 6, 9, 0), "tags": {"rag", "eval"}}
round_trip = json.loads(json.dumps(blob, default=default_encoder), object_hook=object_decoder)
print(f"Round-trip: {round_trip}")

# Output:
# Tuple became: list
# Round-trip: {'created': datetime.datetime(2026, 8, 6, 9, 0), 'tags': {'rag', 'eval'}}

# ============================================================
# 2. CSV — DictReader/DictWriter + Quoting
# ============================================================
# CSV is not "split by comma". Quotes, embedded newlines, and the Windows
# newline='' rule all bite. DictReader/DictWriter map rows to dicts by header.

# Example 3: writing with embedded commas/newlines, then reading back
buf = io.StringIO()
fieldnames = ["id", "text"]
writer = csv.DictWriter(buf, fieldnames=fieldnames)
writer.writeheader()
writer.writerow({"id": 1, "text": "contains, a comma"})
writer.writerow({"id": 2, "text": "has a\nnewline"})
buf.seek(0)

rows = list(csv.DictReader(buf))
print(f"CSV rows: {rows}")

# Output:
# CSV rows: [{'id': '1', 'text': 'contains, a comma'}, {'id': '2', 'text': 'has a\nnewline'}]

# ============================================================
# 3. JSONL — The Dataset Format
# ============================================================
# One JSON object per line. Append-friendly, shard-friendly, stream-friendly.
# This is what SFT/DPO datasets look like on disk.

# Example 4: writing and streaming a JSONL dataset
lines = [
    {"instruction": "Explain RAG", "output": "Retrieval-augmented generation"},
    {"instruction": "Explain LoRA", "output": "Low-rank adaptation"},
]

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "train.jsonl"
    with path.open("w", encoding="utf-8") as f:
        for item in lines:
            f.write(json.dumps(item) + "\n")

    # Stream without loading the whole file
    count = sum(1 for _ in path.open(encoding="utf-8"))
    print(f"JSONL lines: {count}")

# Output:
# JSONL lines: 2

# ============================================================
# 4. pickle — Powerful and DANGEROUS
# ============================================================
# pickle round-trips arbitrary Python objects (classes, lambdas) — which is
# exactly why unpickling untrusted data is arbitrary code execution. Use
# pickle ONLY for your own trusted artifacts, never for anything user-supplied.

# Example 5: round-trip a custom object
class ModelCard:
    def __init__(self, name: str, params_m: int) -> None:
        self.name = name
        self.params_m = params_m

    def __repr__(self) -> str:
        return f"ModelCard({self.name}, {self.params_m}M)"


card = ModelCard("qwen2.5-7b", 7600)
data = pickle.dumps(card)
restored = pickle.loads(data)
print(f"\npickle round-trip: {restored}")

# Output:
# pickle round-trip: ModelCard(qwen2.5-7b, 7600M)

# ============================================================
# 5. sqlite3 — Parameterized Queries Only
# ============================================================
# NEVER build SQL with f-strings or %: that is SQL injection. Use ? placeholders.
# sqlite3 is a real, serverless, file-backed relational DB — fine for local
# vector-store metadata and experiment logs.

# Example 6: schema, insert, query with parameters
with tempfile.TemporaryDirectory() as tmp:
    db = Path(tmp) / "experiments.db"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE runs (id INTEGER PRIMARY KEY, name TEXT, score REAL)")
    conn.executemany(
        "INSERT INTO runs (name, score) VALUES (?, ?)",
        [("baseline", 0.71), ("augmented", 0.85)],
    )
    conn.commit()

    # Parameterized read
    cur = conn.execute("SELECT name, score FROM runs WHERE score > ?", (0.8,))
    print(f"High-score runs: {cur.fetchall()}")

    # A malicious string is DATA, not code
    evil = "'); DROP TABLE runs; --"
    cur = conn.execute("SELECT name FROM runs WHERE name = ?", (evil,))
    assert cur.fetchall() == []
    conn.close()

# Output:
# High-score runs: [('augmented', 0.85)]

# ============================================================
# 6. Production Pattern — Versioned JSONL Writer
# ============================================================
def append_jsonl(path: Path, records: list[dict]) -> int:
    """Append records as JSONL; return number written. Crash-safe per line."""
    written = 0
    with path.open("a", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            written += 1
    return written


with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp) / "data.jsonl"
    append_jsonl(p, [{"a": 1}])
    append_jsonl(p, [{"a": 2}])
    print(f"\nAppended lines: {sum(1 for _ in p.open(encoding='utf-8'))}")

# Output:
# Appended lines: 2

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: unpickling untrusted data (model hub files, user uploads)
#   bad = model = pickle.load(open(url_downloaded_file, "rb"))   # RCE!
# CORRECT:
#   good = use a safe format (JSON/safetensors) or trusted-only pickle

# MISTAKE: SQL built by string interpolation
#   bad = cur.execute(f"SELECT * FROM runs WHERE name = '{name}'")  # injection
# CORRECT:
#   good = cur.execute("SELECT * FROM runs WHERE name = ?", (name,))

# MISTAKE: writing CSV without newline=''
#   bad = open(f, "w")   # Windows writes \\r\\n\\r\\n
# CORRECT:
#   good = open(f, "w", newline="")

# MISTAKE: json.dumps on a set/datetime directly
#   bad = json.dumps({"tags": {"a"}})   # TypeError
# CORRECT:
#   good = json.dumps({"tags": sorted({"a"})})

# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    # JSON tuple -> list
    assert json.loads(json.dumps({"p": (1, 2)}))["p"] == [1, 2], \
        "JSON has no tuples; they become lists"

    # Custom encoder/decoder round-trip
    blob2 = {"t": datetime(2026, 1, 1, 12, 0), "s": {1, 2}}
    rt = json.loads(json.dumps(blob2, default=default_encoder), object_hook=object_decoder)
    assert rt["t"] == datetime(2026, 1, 1, 12, 0), "datetime must round-trip"
    assert rt["s"] == {1, 2}, "set must round-trip"

    # CSV with embedded comma + newline
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["id", "text"])
    w.writeheader()
    w.writerow({"id": 1, "text": "a,b\nc"})
    buf.seek(0)
    rows = list(csv.DictReader(buf))
    assert rows[0]["text"] == "a,b\nc", "quoted fields must survive"

    # pickle round-trip a custom class
    obj = ModelCard("m", 1)
    assert pickle.loads(pickle.dumps(obj)).name == "m"

    # sqlite3: parameterized query + injection resistance
    with tempfile.TemporaryDirectory() as tmp:
        conn = sqlite3.connect(Path(tmp) / "t.db")
        conn.execute("CREATE TABLE t (name TEXT)")
        conn.execute("INSERT INTO t VALUES (?)", ("safe",))
        conn.commit()
        evil = "x'); DROP TABLE t; --"
        cur = conn.execute("SELECT name FROM t WHERE name = ?", (evil,))
        assert cur.fetchall() == [], "injection string must be inert data"
        # table still exists
        assert conn.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 1
        conn.close()

    # JSONL append is cumulative
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "d.jsonl"
        append_jsonl(p, [{"i": 0}])
        append_jsonl(p, [{"i": 1}, {"i": 2}])
        assert sum(1 for _ in p.open(encoding="utf-8")) == 3, \
            "append must not overwrite"

    print("[OK] 51-serialization-and-persistence: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. JSON: portable but limited; extend with default=/object_hook")
        print("2. CSV: use DictReader/DictWriter and newline=''")
        print("3. JSONL: the fine-tuning dataset format; stream it")
        print("4. pickle: trusted artifacts only — RCE risk")
        print("5. sqlite3: parameterized queries, never interpolation")
        _verify()
