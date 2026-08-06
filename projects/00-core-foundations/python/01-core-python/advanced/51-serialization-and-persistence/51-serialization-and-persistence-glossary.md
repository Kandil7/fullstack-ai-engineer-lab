# 51: Serialization & Persistence — Glossary

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `allow_nan` | Parameter | `json.dumps(..., allow_nan=False)` rejects NaN/Infinity — strict JSON |
| `base64` | Module | Encodes binary as ASCII (~33% bigger) for JSON payloads |
| `commit` | Method | Persists a pending sqlite3 transaction |
| CSV | Format | Delimited table; quoting handles commas/newlines; values are strings |
| `default=` | Parameter | `json.dumps` hook: custom encode for unsupported types |
| `DictReader` | Class | Reads CSV rows as dicts keyed by the header row |
| `DictWriter` | Class | Writes dict rows under a declared `fieldnames` schema |
| `ensure_ascii` | Parameter | `json.dumps(..., ensure_ascii=False)` keeps non-Latin text readable |
| `executemany` | Method | sqlite3 bulk insert from a list of parameter tuples |
| injection | Security | User input compiled as SQL; prevented by `?` placeholders |
| `object_hook` | Parameter | `json.loads` hook: custom decode for marked dicts |
| JSON | Format | Portable, 6 types only; tuples→lists; no sets/datetime |
| JSONL | Format | One JSON object per line; streamable, appendable, shardable |
| `newline=""` | Rule | Required when opening CSV files — prevents `\r\r` on Windows |
| parameterized query | Pattern | sqlite3 `?` placeholders — values stay data, never syntax |
| pickle | Module | Native Python serialization; RCE risk on untrusted input |
| protocol | Attribute | pickle format version (`DEFAULT_PROTOCOL` 4; highest 5 on 3.13) |
| safetensors | Alternative | Safe binary model format — no code execution on load |
| shelve | Module | Dict-like persistence over dbm; values are pickled |
| `struct` | Module | Packs/unpacks fixed-layout binary records (e.g. `">f"`) |
| transaction | Concept | A batch of DB writes; commits as a unit or rolls back |
| tuple→list loss | Gotcha | JSON has no tuples; `(1, 2)` round-trips as `[1, 2]` |

## Detailed Definitions

### `allow_nan`
**Definition**: `json.dumps(..., allow_nan=False)` makes non-finite floats
(`float("nan")`, `inf`) raise `ValueError` instead of emitting the
non-standard `NaN`/`Infinity` tokens that other parsers reject.

**Example**:
```python
import json
json.dumps({"s": float("nan")})              # '{"s": NaN}' - not valid JSON
json.dumps({"s": float("nan")}, allow_nan=False)  # ValueError
```

**Complexity**: O(1) per value.

**Related**: JSON, JSONL

### `base64`
**Definition**: The standard way to carry binary data inside JSON/XML:
`base64.b64encode(b"...").decode()` yields pure ASCII, ~33% larger than
the raw bytes.

**Example**:
```python
import base64
print(base64.b64encode(b"hello").decode())   # aGVsbG8=
```

**Complexity**: O(n).

**Related**: `struct`, JSON

### `commit`
**Definition**: `conn.commit()` persists all writes since the last
commit. Until commit, a sqlite3 write is pending and rollback-able. The
`with conn:` context manager commits on success, rolls back on error —
but does not close the connection.

**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
with conn:                                   # commits
    conn.execute("CREATE TABLE t (x INTEGER)")
conn.close()
```

**Complexity**: O(1) (fsync cost depends on the journal mode).

**Related**: transaction, sqlite3

### CSV
**Definition**: Comma-separated values with quoting rules: fields
containing commas, quotes, or newlines are wrapped in quotes. Values
always arrive as strings; convert numbers explicitly. Windows files need
`newline=""` to avoid doubled `\r`.

**Example**:
```python
import csv, io
buf = io.StringIO()
csv.DictWriter(buf, fieldnames=["id", "text"]).writerow({"id": 1, "text": "a,b"})
print(buf.getvalue())                        # 'id,text\r\n1,"a,b"\r\n'
```

**Complexity**: O(n) streaming.

**Related**: `DictReader`, `DictWriter`, `newline=""`

### `default=`
**Definition**: `json.dumps(obj, default=fn)` — `fn(obj)` is called for
any type JSON cannot encode; it must return a JSON-able value or raise
`TypeError`. Used with the marker convention (`{"$iso": ...}`) that
`object_hook` recognizes.

**Example**:
```python
from datetime import datetime
import json
def enc(o):
    if isinstance(o, datetime):
        return {"$iso": o.isoformat()}
    raise TypeError(o)
print(json.dumps({"t": datetime(2026, 8, 6)}, default=enc))
# '{"t": {"$iso": "2026-08-06T00:00:00"}}'
```

**Complexity**: O(1) per unsupported object.

**Related**: `object_hook`, JSON

### `DictReader`
**Definition**: Reads CSV rows as `dict`s keyed by the first (header)
row. Missing cells become `None` (restval); extra columns become
`None`-valued keys unless `fieldnames` is given.

**Example**:
```python
import csv, io
rows = list(csv.DictReader(io.StringIO("id,name\n1,ada")))
print(rows)                                  # [{'id': '1', 'name': 'ada'}]
```

**Complexity**: O(n) streaming.

**Related**: `DictWriter`, CSV

### `DictWriter`
**Definition**: Writes dict rows under a declared `fieldnames` list;
writes the header with `writeheader()`. Rows with keys outside
`fieldnames` raise `ValueError` unless `extrasaction="ignore"`.

**Example**:
```python
import csv, io
buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=["id", "text"])
w.writeheader()
w.writerow({"id": 1, "text": "hello"})
```

**Complexity**: O(n) streaming.

**Related**: `DictReader`, CSV

### `ensure_ascii`
**Definition**: `json.dumps(..., ensure_ascii=False)` writes Arabic,
Chinese, emoji, etc. as literal UTF-8 text instead of `\uXXXX` escapes —
essential for human-readable JSONL datasets.

**Example**:
```python
import json
print(json.dumps({"x": "مرحبا"}))                       # '{"x": "\\u0645..."}'
print(json.dumps({"x": "مرحبا"}, ensure_ascii=False))   # '{"x": "مرحبا"}'
```

**Complexity**: O(1) per character.

**Related**: JSONL, JSON

### `executemany`
**Definition**: `conn.executemany(sql, rows)` runs one parameterized
statement for each tuple in `rows` — the efficient bulk-insert path.

**Example**:
```python
conn.executemany(
    "INSERT INTO runs (name, score) VALUES (?, ?)",
    [("baseline", 0.71), ("augmented", 0.85)],
)
```

**Complexity**: O(n) inserts, one Python-level call.

**Related**: parameterized query, sqlite3

### injection
**Definition**: Occurs when user input is interpolated into SQL text —
`f"... WHERE name = '{name}'"` — turning a value into syntax (`'); DROP
TABLE ...`). Parameterized queries (`?`) make the value data, always.

**Example**:
```python
evil = "'); DROP TABLE runs; --"
# WRONG:     conn.execute(f"SELECT * FROM runs WHERE name = '{evil}'")
# CORRECT:   conn.execute("SELECT * FROM runs WHERE name = ?", (evil,))  # 0 rows
```

**Complexity**: — (it is a security property, not a runtime cost).

**Related**: parameterized query, sqlite3

### `object_hook`
**Definition**: `json.loads(text, object_hook=fn)` — `fn(dict)` is called
for every decoded dict; return a replacement value. Pairs with `default=`
markers.

**Example**:
```python
def dec(d):
    if "$iso" in d:
        return datetime.fromisoformat(d["$iso"])
    return d
```

**Complexity**: O(1) per dict.

**Related**: `default=`, JSON

### JSON
**Definition**: The portable data format: `dict/list/str/int/float/bool/
None` only. Tuples become lists, sets and datetime raise on encode,
non-finite floats emit invalid `NaN` tokens unless `allow_nan=False`.

**Example**:
```python
import json
print(json.loads(json.dumps({"pair": (1, 2)}))["pair"])  # [1, 2] - list!
```

**Complexity**: O(n) serialize/parse.

**Related**: JSONL, `default=`, `object_hook`

### JSONL
**Definition**: One complete JSON document per line. Append-friendly
(crash corrupts at most the last line), shard-friendly, and streamable
in O(1) memory — the standard fine-tuning dataset format.

**Example**:
```python
with path.open("a", encoding="utf-8") as f:
    f.write(json.dumps({"instruction": "Explain RAG"}) + "\n")
count = sum(1 for _ in path.open(encoding="utf-8"))
```

**Complexity**: O(n) write/read, O(1) memory when streamed.

**Related**: JSON, `ensure_ascii`

### `newline=""`
**Definition**: The mandatory argument when opening CSV files
(`open(f, "w", newline="")`). On Windows the default translates `\n` to
`\r\n`, and the csv module already writes `\r\n` — the combination
produces `\r\n\r\n` rows that readers see as blank lines.

**Example**:
```python
# WRONG: with open("out.csv", "w") as f:    -> doubled \r on Windows
# CORRECT:
with open("out.csv", "w", newline="") as f:
    csv.writer(f).writerows(rows)
```

**Complexity**: — (correctness rule, no cost).

**Related**: CSV, `DictWriter`

### parameterized query
**Definition**: SQL with `?` placeholders, values passed separately:
`conn.execute("SELECT * FROM t WHERE name = ?", (name,))`. The only
injection-proof way to put data into SQL.

**Example**:
```python
cur = conn.execute("SELECT score FROM runs WHERE score > ?", (0.8,))
```

**Complexity**: same as the equivalent literal query.

**Related**: injection, `executemany`, sqlite3

### pickle
**Definition**: Python's native serializer — round-trips arbitrary
objects including classes. `pickle.dumps(obj)` / `pickle.loads(data)`.
Because loading can execute code (`__reduce__` tricks), unpickling
untrusted data is arbitrary code execution.

**Example**:
```python
import pickle
data = pickle.dumps({"a": [1, 2]})
print(pickle.loads(data))                      # {'a': [1, 2]}
```

**Complexity**: O(n) native speed.

**Related**: protocol, safetensors

### protocol
**Definition**: pickle's format version, set per dump:
`pickle.dumps(obj, protocol=5)`. On 3.13 `DEFAULT_PROTOCOL` is 4 and
`HIGHEST_PROTOCOL` is 5. Higher = smaller/faster; lower = readable by
older runtimes. Objects survive moves between versions poorly.

**Example**:
```python
import pickle
print(pickle.DEFAULT_PROTOCOL, pickle.HIGHEST_PROTOCOL)   # 4 5
```

**Complexity**: — (compat knob).

**Related**: pickle

### safetensors
**Definition**: A safe binary format for model weights: metadata is a
JSON header, tensors are raw bytes — no code execution path on load.
The recommended replacement for pickled `.pkl` model artifacts.

**Example**:
```python
# from safetensors import safe_open
# tensors = safe_open("model.safetensors", framework="pt")
```

**Complexity**: O(n) memory-mapped reads.

**Related**: pickle

### shelve
**Definition**: `shelve.open(path)` returns a dict-like mapping persisted
over dbm. Keys are strings, values are pickled — so the pickle security
rule applies. One process at a time; no concurrency guarantees.

**Example**:
```python
import shelve
with shelve.open("cache.shlv") as db:
    db["meta"] = {"version": "v2"}
```

**Complexity**: O(1) per key access.

**Related**: pickle, sqlite3

### `struct`
**Definition**: Packs/unpacks fixed-layout binary records —
`struct.pack(">f", 3.5)` = 4 big-endian bytes (`40600000`). The
low-level tool for compact wire formats and file headers.

**Example**:
```python
import struct
print(struct.pack(">f", 3.5).hex())          # 40600000
```

**Complexity**: O(n) per record.

**Related**: `base64`

### transaction
**Definition**: A group of sqlite3 writes that commit as a unit or roll
back together. `conn.commit()` persists; `with conn:` commits on success
and rolls back on exception — but never closes the connection.

**Example**:
```python
conn = sqlite3.connect(db)
try:
    with conn:
        conn.execute("INSERT INTO t VALUES (?)", (1,))
        conn.execute("INSERT INTO t VALUES (?)", (2,))
finally:
    conn.close()
```

**Complexity**: journal-dependent; batch many writes per transaction.

**Related**: `commit`, sqlite3

### tuple→list loss
**Definition**: JSON has no tuple type, so `(1, 2)` round-trips as
`[1, 2]`. Code that later relies on tuple unpacking against JSON-loaded
data fails with `TypeError` — plan for lists.

**Example**:
```python
import json
pair = json.loads('{"pair": [1, 2]}')["pair"]
print(type(pair).__name__)                   # list
```

**Complexity**: — (type semantics).

**Related**: JSON

## Key Concepts Summary

### The Safety Line
- **JSON / CSV / JSONL**: safe to read from anyone.
- **pickle / shelve / `pkl` model files**: only from sources you trust —
  loading is code execution.
- **safetensors / numpy / ONNX**: safe binary model formats.

### The Format Decision
- **JSON**: APIs, configs, small documents.
- **JSONL**: datasets, append logs, streams (O(1) memory).
- **CSV**: tables for business/ops exchange (values are strings).
- **sqlite3**: queryable metadata, indexes, joins.
- **pickle**: your own cached native objects; version-pin classes.
- **shelve**: small single-process caches between JSON and a database.

### SQL Rule
- `?` placeholders only; f-string SQL is injection, no exceptions.
- `with conn:` commits/rolls back but does not close — close explicitly.

### Symmetry Rule
- Every `default=` encoder marker needs its `object_hook` decoder;
- otherwise round-trips are lossy or fail.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `default=` — ___
2. injection — ___
3. pickle — ___
4. JSONL — ___
5. `newline=""` — ___
6. `object_hook` — ___
7. tuple→list loss — ___
8. transaction — ___
9. protocol — ___
10. `ensure_ascii` — ___

A. Encoder hook for unsupported types
B. User input compiled as SQL
C. Native serializer with RCE risk
D. One JSON object per line
E. Required for CSV files on Windows
F. Decoder hook for marked dicts
G. `(1, 2)` round-trips as `[1, 2]`
H. Writes commit as a unit or roll back
I. pickle format version
J. Keep Arabic/Chinese readable instead of `\uXXXX`

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H, 9-I, 10-J
