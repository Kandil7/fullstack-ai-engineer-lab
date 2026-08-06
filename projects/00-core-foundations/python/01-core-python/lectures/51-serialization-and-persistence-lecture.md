# 01-core-python — 51: Serialization & Persistence — Data That Survives

## Topic Overview

Serialization turns live Python objects into bytes or text that survives
a restart, a network hop, or a dataset file. Persistence keeps that data
usable on disk: JSONL for datasets, CSV for tables, sqlite3 for queryable
metadata, pickle for Python-native objects — and a clear line between
safe formats (JSON, CSV) and dangerous ones (pickle on untrusted input).

For AI engineers this is day-one production work: fine-tuning datasets
are JSONL files, vector-store metadata lives in sqlite3, and pickled
model artifacts (`.pkl`) are a known supply-chain attack vector.

## Learning Objectives

After this topic you can:

- Explain exactly what JSON supports and what it loses (tuple→list,
  no sets, no datetime) and extend it with `default=` / `object_hook`.
- Write and read CSV safely with `DictReader`/`DictWriter`, correct
  quoting, and `newline=""`.
- Read and append JSONL streams without loading whole files.
- Explain why `pickle.loads` on untrusted data is arbitrary code
  execution, and when pickle *is* the right tool.
- Query sqlite3 with `?` placeholders only, and explain why f-string SQL
  is an injection vulnerability.
- Choose among json / csv / jsonl / pickle / sqlite3 / shelve / binary
  formats for a given job, with cost and safety tradeoffs.

## Prerequisites

- Files and paths: `pathlib.Path.open(...)` (topic 42).
- Containers: dict/list/set/tuple semantics (earlier topics).
- Exceptions: `TypeError`, `ValueError`, and try/finally cleanup
  (topics 47, 03-context-managers).
- Slight exposure to databases is helpful but not required — sqlite3 is
  taught from zero here.

---

## 1. JSON — Portable But Limited

JSON is the lingua franca of APIs and datasets, but it only understands
six types: `dict`, `list`, `str`, `int`, `float`, `bool`, `None`.
Everything else fails or silently degrades.

```python
import json

payload = {"pair": (1, 2), "name": "qwen"}
encoded = json.dumps(payload)
decoded = json.loads(encoded)
print(f"Tuple became: {type(decoded['pair']).__name__}")

# Output:
# Tuple became: list
```

Two failure modes to memorize:

```python
json.dumps({"tags": {"rag", "eval"}})          # TypeError: Object of type set is not JSON serializable
json.dumps({"created": datetime(2026, 8, 6)})  # TypeError: Object of type datetime is not JSON serializable
```

**Extending JSON** — encode with `default=`, decode with `object_hook`:

```python
from datetime import datetime

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
rt = json.loads(json.dumps(blob, default=default_encoder), object_hook=object_decoder)
print(rt)

# Output:
# {'created': datetime.datetime(2026, 8, 6, 9, 0), 'tags': {'rag', 'eval'}}
```

The `$iso` / `$set` prefix convention makes the extension self-describing —
a decoder can recognize its own markers and ignore foreign ones.

**Pitfall — non-standard tokens.** `json.dumps` emits `NaN`/`Infinity` for
non-finite floats by default. That is NOT valid JSON — other parsers
reject it. If your JSONL may be consumed outside Python, use
`allow_nan=False` so a `float("nan")` fails loudly instead of silently
writing an unreadable file.

---

## 2. CSV — DictReader/DictWriter + Quoting

CSV is *not* "split by comma". Fields containing commas, quotes, or
newlines must be quoted, and the Windows `newline=""` rule is mandatory
when writing to real files.

```python
import csv
import io

buf = io.StringIO()
fieldnames = ["id", "text"]
writer = csv.DictWriter(buf, fieldnames=fieldnames)
writer.writeheader()
writer.writerow({"id": 1, "text": "contains, a comma"})
writer.writerow({"id": 2, "text": "has a\nnewline"})
buf.seek(0)

rows = list(csv.DictReader(buf))
print(rows)

# Output:
# [{'id': '1', 'text': 'contains, a comma'}, {'id': '2', 'text': 'has a\nnewline'}]
```

Two rules that save hours:

1. **`newline=""` when opening the file**: `Path("f.csv").open("w", newline="")`.
   Without it on Windows, every row gains an extra `\r` — the file becomes
   `\r\n\r\n`-separated and the reader sees blank lines.
2. **DictWriter `extrasaction="ignore"`**: when a row dict has keys beyond
   `fieldnames`, the writer raises `ValueError` by default. Add
   `extrasaction="ignore"` if extra keys are acceptable, or keep rows
   strictly in schema.

All CSV values arrive as strings (`'1'` not `1`); convert on read with an
explicit schema step.

---

## 3. JSONL — The Dataset Format

JSONL is one JSON object per line. It is append-friendly, shard-friendly,
and stream-friendly — exactly why it is the standard on-disk format for
SFT/DPO fine-tuning datasets.

```python
import tempfile
from pathlib import Path

lines = [
    {"instruction": "Explain RAG", "output": "Retrieval-augmented generation"},
    {"instruction": "Explain LoRA", "output": "Low-rank adaptation"},
]

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "train.jsonl"
    with path.open("w", encoding="utf-8") as f:
        for item in lines:
            f.write(json.dumps(item) + "\n")

    # Stream: count lines without loading the file
    count = sum(1 for _ in path.open(encoding="utf-8"))
    print(f"JSONL lines: {count}")

# Output:
# JSONL lines: 2
```

Reading a large JSONL file as a stream costs O(1) memory — the generator
over the file yields one line at a time:

```python
def stream_jsonl(path: Path):
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:                      # skip blank/trailing lines
                yield json.loads(line)
```

A JSONL constraint worth knowing: each line must be a *complete* JSON
document. A `NaN` token from section 1 breaks other parsers line-by-line.

---

## 4. pickle — Powerful and DANGEROUS

pickle round-trips *arbitrary* Python objects — classes, lambdas, even
live function closures. That power is exactly the danger: a crafted
pickle stream can execute arbitrary code on `loads`.

```python
import pickle

class ModelCard:
    def __init__(self, name: str, params_m: int) -> None:
        self.name = name
        self.params_m = params_m

    def __repr__(self) -> str:
        return f"ModelCard({self.name}, {self.params_m}M)"

card = ModelCard("qwen2.5-7b", 7600)
data = pickle.dumps(card)
restored = pickle.loads(data)
print(restored)

# Output:
# ModelCard(qwen2.5-7b, 7600M)
```

**The security rule, stated once and clearly: NEVER unpickle data you did
not create yourself.** A model downloaded from a hub, a file from a user
upload, a cache from an untrusted service — all are arbitrary code
execution on `pickle.load`. This is the `.pkl` supply-chain attack class:
malicious artifacts execute during "loading the model".

**Protocols.** `pickle.dumps(obj, protocol=...)`; 3.13 defaults to
protocol 4 (`pickle.DEFAULT_PROTOCOL`), highest is 5 (out-of-band data,
better for large numpy buffers). Protocol 2 is the oldest you should
ever produce. Higher protocol = smaller/faster; lower = more readable by
old runtimes. Version pinning: pickled objects may break when classes
move modules — a real model-artifact maintenance problem.

**pickle vs json — the tradeoff table:**

| Criterion | json | pickle |
|---|---|---|
| Types | 6 portable types only | Any Python object |
| Safety | Safe on untrusted input | RCE on untrusted input |
| Human-readable | Yes | No (binary-ish) |
| Language-portable | Yes | Python only |
| Version tolerance | Easy to add fields | Class layout changes break loads |
| Typical use | APIs, datasets, configs | Your own cached artifacts |

**Cheaper alternative**: for models, prefer a safe binary format
(`safetensors`, numpy `.npy`/`.npz`, or ONNX) — same machine-native speed,
zero RCE risk.

---

## 5. sqlite3 — Parameterized Queries Only

sqlite3 is a real, serverless, file-backed relational database built into
the stdlib. It is the right home for local vector-store metadata,
experiment logs, and eval results.

```python
import sqlite3
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    db = Path(tmp) / "experiments.db"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE runs (id INTEGER PRIMARY KEY, name TEXT, score REAL)")
    conn.executemany(
        "INSERT INTO runs (name, score) VALUES (?, ?)",
        [("baseline", 0.71), ("augmented", 0.85)],
    )
    conn.commit()

    cur = conn.execute("SELECT name, score FROM runs WHERE score > ?", (0.8,))
    print(cur.fetchall())

    # A malicious string is DATA, not code
    evil = "'); DROP TABLE runs; --"
    cur = conn.execute("SELECT name FROM runs WHERE name = ?", (evil,))
    assert cur.fetchall() == []
    conn.close()

# Output:
# [('augmented', 0.85)]
```

**The one rule that matters: never build SQL with f-strings or `%`.**
`f"... WHERE name = '{name}'"` turns user input into SQL syntax —
injection. `?` placeholders make the value a value, always. The
parameterized `evil` above returns zero rows and the table survives;
the f-string version would have dropped the table.

**Transactions.** By default sqlite3 opens in `legacy` transaction mode:
writes are deferred until `commit()` and rollback-able. The connection
as a context manager (`with conn:`) commits on success / rolls back on
error — but it does **NOT close the connection**. `conn.close()` is still
your job:

```python
conn = sqlite3.connect(":memory:")
with conn:                      # commits the transaction
    conn.execute("INSERT INTO t VALUES (?)", (1,))
conn.execute("SELECT COUNT(*) FROM t")   # still works - connection is OPEN
conn.close()
```

**Cheaper alternative**: for pure append-only logs, JSONL often beats
sqlite3 (no schema, no transactions, trivially shardable). Use sqlite3
when you need queries, indexes, or joins.

---

## 6. shelve — Simple Persistent Mapping

shelve is a dict-like wrapper over a dbm file: assign, close, reopen.

```python
import shelve

with shelve.open("cache.shlv") as db:    # the with-block also closes the shelf
    db["embeddings_2026-08"] = {"count": 1_000_000, "dim": 768}
    db["meta"] = {"version": "v2"}
print("shelf closed and flushed on exit")
```

What you must know before using it:

- Values are **pickled** — the security rule from section 4 applies to
  shelves you read from anyone else.
- Keys must be strings; values must be pickleable.
- The same file must not be opened from multiple processes concurrently
  (dbm locking is not a coordination tool).
- **Cheaper alternative**: for small config-like data, JSON file beats
  shelve (portable, diffable, human-readable). For real concurrent or
  queryable data, sqlite3 beats shelve. shelve fits small single-process
  caches between "JSON file" and "database".

---

## 7. Binary vs Text — struct and base64

Text mode (`encoding="utf-8"`) is for JSON/CSV/JSONL. Binary mode
(`"rb"`/`"wb"`) is for raw bytes: images, model weights, pickles,
compressed archives.

```python
import base64
import struct

# struct: fixed-layout binary packing (big-endian float32)
raw = struct.pack(">f", 3.5)
print(raw.hex())

# base64: binary -> ASCII for JSON payloads
print(base64.b64encode(b"hello").decode())

# Output:
# 40600000
# aGVsbG8=
```

When a JSON API must carry binary data (image thumbnails, small blobs),
base64 is the standard encoding — with a ~33% size cost. For large
numeric payloads, `struct`/`array`/numpy give compact fixed-size
records; for float32 embeddings the numpy `.npy` format is the right
tool (topic 52 covers the size math).

---

## 8. Production Pattern — Versioned JSONL Writer

The pattern that keeps datasets append-safe and crash-safe:

```python
def append_jsonl(path: Path, records: list[dict]) -> int:
    """Append records as JSONL; return the number written.

    Each line is a complete JSON document, so a crash mid-write
    corrupts at most the last line — never the whole file.
    """
    written = 0
    with path.open("a", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            written += 1
    return written
```

Why this is production-shaped:

- **Append mode** — restarting a data collection job never clobbers
  earlier shards; count lines to resume.
- **Per-line atomicity** — each line parses independently; a truncated
  final line is detectable and skippable.
- **`ensure_ascii=False`** — keeps Arabic/Chinese text human-readable
  on disk instead of `\uXXXX` escapes.
- **Versioning** — record schema changes by adding a `"version": 2`
  field and migrating on read, not by rewriting history.

---

## Common Mistakes to Avoid

### Mistake 1: Unpickling untrusted data
```python
# WRONG - RCE: a crafted pickle runs code during loads
model = pickle.load(open(downloaded_from_hub, "rb"))

# CORRECT - safe formats for untrusted input
state = json.loads(text_from_user)              # JSON: safe
weights = safetensors.torch.load_file(hub_file) # safetensors: safe
```

### Mistake 2: Building SQL with f-strings
```python
# WRONG - injection: name becomes SQL syntax
rows = conn.execute(f"SELECT * FROM runs WHERE name = '{name}'")

# CORRECT - name is data, always
rows = conn.execute("SELECT * FROM runs WHERE name = ?", (name,))
```

### Mistake 3: Writing CSV files without newline=""
```python
# WRONG - Windows writes \r\n\r\n between rows; readers see blank lines
with open("out.csv", "w") as f:
    csv.writer(f).writerows(rows)

# CORRECT
with open("out.csv", "w", newline="") as f:
    csv.writer(f).writerows(rows)
```

### Mistake 4: json.dumps on a set / datetime directly
```python
# WRONG - TypeError: Object of type set is not JSON serializable
payload = json.dumps({"tags": {"a", "b"}})

# CORRECT - normalize before encoding
payload = json.dumps({"tags": sorted({"a", "b"})})
```

### Mistake 5: Assuming `with conn:` closes the sqlite3 connection
```python
# WRONG - connection stays open; file handles leak in long processes
with sqlite3.connect(db) as conn:
    conn.execute("INSERT ...")

# CORRECT - explicit close (or use a try/finally / resource wrapper)
conn = sqlite3.connect(db)
try:
    with conn:
        conn.execute("INSERT ...")
finally:
    conn.close()
```

### Mistake 6: Writing `NaN` into JSONL with other parsers in the path
```python
# WRONG - json emits NaN, not valid JSON; other tools reject the line
f.write(json.dumps({"score": float("nan")}) + "\n")

# CORRECT - fail loudly on non-finite floats
f.write(json.dumps({"score": value}, allow_nan=False) + "\n")
```

## Best Practices

- **JSON for APIs and datasets; pickle only for your own trusted
  artifacts; sqlite3 for queryable metadata; JSONL for append logs.**
- Read JSONL with `default=...` and `object_hook=...` pairs that are
  symmetric — every encoder marker must have a decoder.
- Open every CSV file with `newline=""`, both read and write.
- Parameterize every sqlite3 query; there is no "safe" exception.
- When a class moves modules, old pickles break — plan versioned
  migrations or prefer JSON for long-lived data.
- Keep records self-describing: add a `"version"` field from day one.

## Complexity and Cost

| Format | Write cost | Read cost | Memory on read | Notes |
|---|---|---|---|---|
| JSON | O(n) text | O(n) parse | Whole document | Fine below ~100 MB |
| JSONL | O(n) append | O(n) stream | O(1) streaming | The dataset format |
| CSV | O(n) | O(n) | O(1) streaming | All values are str |
| pickle | O(n) native | O(n) native | Whole object | Fast, unsafe, Python-only |
| sqlite3 | O(log n) per row | Indexed | Bounded by query | Add indexes for WHERE |
| shelve | O(1) per key | O(1) per key | One value | Values pickled; single process |

Big-O is the same everywhere; the differences are constants, safety, and
tooling. The engineering decision is which axis matters for the data:
streamability (JSONL), queryability (sqlite3), native speed (pickle,
with the safety cost).

## AI Engineering Relevance

- **Fine-tuning datasets are JSONL** — `{instruction, input, output}` per
  line, sharded and streamed. Reading them wrong (loading 5 GB into
  memory) is a training-pipeline failure before training starts.
- **sqlite3 backs local vector-store metadata** — chunk→source mappings,
  eval scores, ingestion state. Parameterized queries keep user-derived
  text from becoming SQL.
- **Pickled `.pkl` model artifacts are a supply-chain risk** — the
  "download + `pickle.load`" habit is how malicious model files execute
  code on AI workstations and CI runners. Use safe formats for anything
  not authored by you.
- **CSV is still the exchange format** for business/ops teams — being
  fluent with quoting and `newline=""` is a daily backend skill.
- **Versioned JSONL** is how you evolve dataset schemas without breaking
  previously collected shards — the same "migrate on read" strategy used
  for evaluation-history stores.

## Practice Exercises

### Exercise 1: Tuple Round-Trip (Difficulty: Easy)
Serialize `{"pair": (1, 2)}` with `json.dumps`, then load it back.
Confirm the type changed to `list`. Why can JSON not preserve the tuple?

### Exercise 2: CSV With Quoting (Difficulty: Easy)
Write `[{"id": 1, "text": "a,b\nc"}]` to a `StringIO` with
`DictWriter`, read it back with `DictReader`, and assert `text` equals
`"a,b\nc"` exactly.

### Exercise 3: Custom JSON Round-Trip (Difficulty: Medium)
Extend JSON to round-trip `datetime` and `set` using the `default=` /
`object_hook` marker pattern from section 1. Round-trip a dict containing
both types and assert equality with the original.

### Exercise 4: Injection-Resistant Query (Difficulty: Medium)
Create a `runs` table, insert one row, then run a parameterized query
with the payload `"x'); DROP TABLE runs; --"`. Assert zero rows match
and the table still exists afterwards. Then write the f-string version
of the same query and observe the difference in behavior.

### Exercise 5: Streaming JSONL Reader (Difficulty: Hard)
Write `stream_jsonl(path)` that yields parsed records one at a time
(O(1) memory), skipping blank lines. Verify on a 1,000-record file that
`sum(1 for _ in stream_jsonl(p)) == 1000` and that it handles a
trailing newline. Then extend it to skip one malformed line without
aborting the whole stream.

## Summary

- JSON is portable but limited: tuples→lists, no sets/datetime;
  extend with symmetric `default=` / `object_hook` markers.
- CSV needs `DictReader`/`DictWriter` and `newline=""`; values are
  strings until you convert them.
- JSONL is the fine-tuning dataset format — stream it, never load it.
- pickle round-trips anything, which is why unpickling untrusted data
  is RCE. Trusted artifacts only, and prefer safe formats for models.
- sqlite3: `?` placeholders, never f-string SQL; `with conn:` commits
  but does not close.
- Pick the format by what you need: streamability, queryability,
  portability, or native speed — and always by safety.

## Quick Reference

```python
import csv, json, pickle, sqlite3, shelve
from pathlib import Path

# JSON with extensions
json.dumps(obj, default=default_encoder)          # encode
json.loads(text, object_hook=object_decoder)      # decode
json.dumps(obj, allow_nan=False)                  # strict JSON

# CSV
with Path("f.csv").open("w", newline="") as f:
    csv.DictWriter(f, fieldnames=cols).writeheader()
rows = list(csv.DictReader(Path("f.csv").open(newline="")))

# JSONL append (crash-safe per line)
with path.open("a", encoding="utf-8") as f:
    f.write(json.dumps(rec, ensure_ascii=False) + "\n")

# pickle - TRUSTED DATA ONLY
data = pickle.dumps(obj)          # DEFAULT_PROTOCOL (4 on 3.13)
obj = pickle.loads(data)          # never with untrusted input

# sqlite3 - parameterized only
conn = sqlite3.connect(db)
conn.execute("INSERT INTO t (name) VALUES (?)", (name,))
conn.commit()                      # with conn: commits too, but no close
conn.close()

# shelve - small single-process caches
with shelve.open("c.shlv") as db:
    db["key"] = value             # values are pickled
```

## Next Steps

- Apply the injection rule to any database you meet (Postgres, MySQL,
  Redis) — `?` becomes `%s` / `$1`, the principle is identical.
- Read a real fine-tuning dataset file (`*.jsonl` from Hugging Face
  datasets) with `stream_jsonl` and inspect its schema — this is the
  file format you will write as a data engineer.
- Topic 52 continues the size math: why a 1M×768 float32 embedding
  matrix is ~3 GB and how numpy/`memoryview` change the storage story.
