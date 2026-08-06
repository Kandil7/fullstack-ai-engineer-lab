# Challenge 51: Serialization & Persistence

Data survives restarts — but only if you pick the right format and the
safe path. Round-trip CSV with embedded punctuation, write JSONL that
resists line injection, and bulk-insert into sqlite3 the way production
code does.

## 🥉 Bronze — CSV Round-Trip (~15 min)

**Task:** Implement `csv_roundtrip(rows)`, which writes `rows` (dicts all
sharing one key set) with `csv.DictWriter` to a `StringIO` (header first),
then reads them back with `csv.DictReader` and returns the list of dicts
as strings. Fields containing commas, newlines, or double quotes must
round-trip **exactly**.

**Signature:**
```python
def csv_roundtrip(rows: list[dict]) -> list[dict]:
```

| Input | Expected |
|---|---|
| `[{"id": "1", "text": "plain"}]` | `[{"id": "1", "text": "plain"}]` |
| `[{"id": "1", "text": "contains, a comma"}]` | identical |
| `[{"id": "2", "text": "has a\nnewline"}]` | identical |
| `[{"id": "3", "text": 'says "hi"'}]` | identical |
| `[]` | `[]` |

**Constraints:** DictWriter must write the header (`writeheader`).
Numeric-looking values stay strings (`"1"`, not `1`).

---

## 🥈 Silver — Injection-Safe JSONL (~35 min)

**Task:** Implement `write_jsonl(path, records)` and `read_jsonl(path)`.
The writer must:

- write one complete JSON object per line (append mode), `ensure_ascii=False`,
  `allow_nan=False` (a non-finite float must raise `ValueError`),
- round-trip `datetime` and `set` via symmetric `default=` / `object_hook`
  markers,
- and treat every string as data: a value containing `\n` or
  `"}, {"hacked": true}` must stay **inside one line** and come back as
  one string — never as extra records or injected keys.

`read_jsonl` returns the list of decoded dicts, skipping blank lines.

**Signatures:**
```python
def write_jsonl(path: Path, records: list[dict]) -> int:  # count written
def read_jsonl(path: Path) -> list[dict]:
```

| Input | Expected |
|---|---|
| `[{"a": 1}, {"a": 2}]` written twice | file has 4 non-empty lines; `read_jsonl` returns all 4 |
| record with `"text": "x\nsecond line"` | file has exactly 1 non-empty line; value round-trips with the `\n` |
| record with `"text": 'x"}, {"hacked": true}'` | 1 line; `read_jsonl` returns 1 record; no `hacked` key anywhere |
| record with `{"t": datetime(2026, 8, 6, 9, 0)}` | round-trips to the identical datetime |
| record with `{"s": {"b", "a"}}` | round-trips to the identical set |
| record with `"text": "مرحبا"` | the raw file contains the literal `مرحبا` (not `\uXXXX`) |
| record with `float("nan")` | `ValueError` |
| empty file | `[]` |

**Constraints:** Unicode must be preserved; line counts must be exact.

---

## 🥇 Gold — Transactional Bulk Insert (~75 min)

**Task:** Implement three sqlite3 functions for an experiment-run store:

- `create_schema(conn)` — `CREATE TABLE runs (id INTEGER PRIMARY KEY, name TEXT NOT NULL, score REAL)`.
- `insert_runs(conn, rows)` — bulk-insert `(name, score)` tuples inside a
  single transaction (`with conn:`); returns the row count. **Must use
  `executemany`, not a loop of `execute` calls.**
- `top_runs(conn, threshold)` — parameterized `SELECT name, score ...
  WHERE score >= ? ORDER BY score DESC`; returns the fetched rows.

The tests enforce:

- **Injection resistance** — a name like `"x'); DROP TABLE runs; --"`
  is inert data: zero matching rows, and the `runs` table still exists.
- **One Python-level call** — bulk-inserting 20,000 rows must make at
  most 1 `execute`/`executemany` call (the tests count calls).
- **Atomic rollback** — a batch containing a row that violates
  `NOT NULL` raises `IntegrityError` and leaves the table empty (no
  partial writes).

**Signatures:**
```python
def create_schema(conn: sqlite3.Connection) -> None:
def insert_runs(conn: sqlite3.Connection, rows: list[tuple[str, float]]) -> int:
def top_runs(conn: sqlite3.Connection, threshold: float) -> list[tuple]:
```

| Input | Expected |
|---|---|
| `insert_runs(conn, [("baseline", 0.71), ("augmented", 0.85)])` | returns 2; `top_runs(conn, 0.8)` → `[("augmented", 0.85)]` |
| `insert_runs(conn, [("a", 0.1), (None, 0.2)])` | `IntegrityError`; `SELECT COUNT(*)` → 0 |
| name `"x'); DROP TABLE runs; --"` inserted | table `runs` still present; query for it returns no rows |
| 20,000-row bulk insert | ≤ 1 counted DB call |

---

## Running

```bash
pytest challenges/51-serialization-and-persistence/test_challenge.py -v
```

## Test File Structure

```
challenges/51-serialization-and-persistence/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
