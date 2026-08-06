# Quiz 51: Serialization & Persistence

**Instructions:** Choose the single best answer. Answers and explanations
are at the end.

## Questions

### Q1. Which types can JSON serialize natively?
**Difficulty:** Easy

- (A) dict, list, str, int, float, bool, None
- (B) dict, list, tuple, str, int, float, bool
- (C) Any picklable object
- (D) dict, list, str, int, float, datetime

### Q2. What is the output?
**Difficulty:** Easy

```python
import json
print(json.loads(json.dumps({"pair": (1, 2)}))["pair"])
```

- (A) `(1, 2)`
- (B) `[1, 2]`
- (C) `TypeError`
- (D) `"{1, 2}"`

### Q3. What is the output?
**Difficulty:** Easy

```python
import json
json.dumps({"tags": {"rag", "eval"}})
```

- (A) `'{"tags": ["rag", "eval"]}'`
- (B) `'{"tags": {"rag", "eval"}}'`
- (C) `TypeError: Object of type set is not JSON serializable`
- (D) `'{"tags": ["eval", "rag"]}'`

### Q4. Which pair of hooks extends JSON to custom types?
**Difficulty:** Easy

- (A) `encoder=` and `decoder=`
- (B) `default=` and `object_hook=`
- (C) `custom=` and `reviver=`
- (D) `transform=` and `parse=`

### Q5. Why must CSV files be opened with `newline=""` on Windows?
**Difficulty:** Medium

- (A) The csv module writes `\n` only; Windows text mode adds `\r`, producing `\r\n\r\n` rows
- (B) Without it the file is read-only
- (C) It enables UTF-8 encoding
- (D) It is only needed for `DictWriter`, not `DictReader`

### Q6. What is the output?
**Difficulty:** Medium

```python
import csv, io
buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=["id", "text"])
w.writeheader()
w.writerow({"id": 1, "text": "a,b"})
buf.seek(0)
rows = list(csv.DictReader(buf))
print(rows[0]["id"], type(rows[0]["id"]).__name__)
```

- (A) `1 int`
- (B) `1 str`
- (C) `"1" int`
- (D) `ValueError` — the comma must be escaped

### Q7. What is the output?
**Difficulty:** Medium

```python
import json
print(json.dumps({"x": "مرحبا"}, ensure_ascii=False))
```

- (A) `{"x": "\u0645\u0631\u062d\u0628\u0627"}`
- (B) `{"x": "مرحبا"}`
- (C) `TypeError`
- (D) `{"x": "?????"}`

### Q8. What is the output?
**Difficulty:** Medium

```python
import json
print(json.dumps({"s": float("nan")}))
```

- (A) `'{"s": NaN}'`
- (B) `'{"s": "nan"}'`
- (C) `ValueError`
- (D) `'{"s": null}'`

### Q9. Which statement about JSONL is TRUE?
**Difficulty:** Medium

- (A) A JSONL file must be loaded entirely into memory to read it
- (B) Each line is one complete JSON document; appends are crash-safe per line
- (C) JSONL files cannot contain Unicode
- (D) JSONL requires a schema declaration at the top

### Q10. Why is unpickling untrusted data dangerous?
**Difficulty:** Easy

- (A) It is slow and may hang the interpreter
- (B) A crafted pickle stream can execute arbitrary code on `loads`
- (C) Pickles expire after 30 days
- (D) It silently converts all data to strings

### Q11. What is the output?
**Difficulty:** Medium

```python
import pickle
print(pickle.DEFAULT_PROTOCOL, pickle.HIGHEST_PROTOCOL)
```

- (A) `0 5`
- (B) `1 4`
- (C) `4 5`
- (D) `5 5`

### Q12. Which format is the safe replacement for pickled model artifacts?
**Difficulty:** Medium

- (A) `shelve`
- (B) `safetensors` / numpy `.npy`
- (C) `base64` of the pickle
- (D) A second pickle with a checksum

### Q13. What is the output?
**Difficulty:** Medium

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (x INTEGER)")
with conn:
    conn.execute("INSERT INTO t VALUES (1)")
print(conn.execute("SELECT COUNT(*) FROM t").fetchone()[0])
conn.close()
```

- (A) `0`
- (B) `1`
- (C) `OperationalError: no such table: t`
- (D) `None`

### Q14. Which sqlite3 query is injection-safe?
**Difficulty:** Easy

- (A) `conn.execute(f"SELECT * FROM runs WHERE name = '{name}'")`
- (B) `conn.execute("SELECT * FROM runs WHERE name = ?", (name,))`
- (C) `conn.execute("SELECT * FROM runs WHERE name = %s", name)`
- (D) `conn.execute(f"SELECT * FROM runs WHERE name = {name}")`

### Q15. What does `with conn:` do for a sqlite3 connection?
**Difficulty:** Hard

- (A) Commits on success, rolls back on exception, and closes the connection
- (B) Commits on success, rolls back on exception — but does NOT close it
- (C) Opens a new transaction on every line of the block
- (D) Closes the connection but never commits

### Q16. What is the output?
**Difficulty:** Hard

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (x INTEGER)")
with conn:
    conn.execute("INSERT INTO t VALUES (1)")
    conn.execute("INSERT INTO t VALUES (2)")
    raise ValueError
print(conn.execute("SELECT COUNT(*) FROM t").fetchone()[0])
conn.close()
```

- (A) `2`
- (B) `0`
- (C) `1`
- (D) `ValueError` propagates; the `print` never runs

### Q17. Which statement about `executemany` is TRUE?
**Difficulty:** Hard

- (A) It is slower than a loop of `execute` calls
- (B) It executes one statement per row with a single Python-level call
- (C) It cannot be used with parameterized queries
- (D) It automatically commits the transaction

### Q18. What is the output?
**Difficulty:** Medium

```python
import shelve
with shelve.open("cache.shlv") as db:
    db["k"] = {"vec": [0.1, 0.2]}
with shelve.open("cache.shlv") as db:
    print(db["k"])
```

*(Both opens happen in the same process; the shelf file is fresh.)*

- (A) `{'vec': [0.1, 0.2]}`
- (B) `KeyError`
- (C) `None`
- (D) `TypeError` — shelves cannot store dicts

### Q19. What is the output?
**Difficulty:** Hard

```python
import struct, base64
print(struct.pack(">f", 3.5).hex(), base64.b64encode(b"hi").decode())
```

- (A) `40600000 aGk=`
- (B) `3f800000 aGk=`
- (C) `40600000 aGVsbG8=`
- (D) `3f800000 aGVsbG8=`

### Q20. A JSONL line is `{"user": "x\"}, {\"hacked\": true}"}`. What does `json.loads` of that line produce?
**Difficulty:** Hard

- (A) Two records: `{"user": "x"}, {"hacked": true}`
- (B) One record `{"user": 'x"}, {"hacked": true}'}` with a parse error on the trailing brace
- (C) One record whose `user` value is the whole string `x"}, {"hacked": true}`
- (D) `KeyError` — `hacked` is missing a value

---

## Answer Key

### Q1 — (A)
JSON natively supports exactly: dict, list, str, int, float, bool, None.
- (B) tuples become lists — there is no tuple type in JSON.
- (C) picklability is pickle's domain, not JSON's.
- (D) datetime is not natively serializable.

### Q2 — (B)
JSON has no tuple type, so `(1, 2)` round-trips as `[1, 2]`.
- (A) would require a tuple type that JSON lacks.
- (C) no error — the loss is silent, which is why it bites later.
- (D) it is a list, not a string.

### Q3 — (C)
Sets are not JSON-serializable; without a `default=` hook this raises
`TypeError`.
- (A/D) would require an explicit `default=` conversion.
- (B) invalid JSON — sets are not a JSON type.

### Q4 — (B)
`default=` customizes encoding; `object_hook=` customizes decoding. They
work in pairs with self-describing marker dicts.
- (A/C/D) are not real json module parameters.

### Q5 — (A)
The csv module already writes `\r\n` as its line terminator; Windows
text mode then translates each `\n` to `\r\n`, doubling the carriage
return and producing blank rows on read.
- (B/C) false — no such effect.
- (D) the rule applies to reading too.

### Q6 — (B)
CSV has no type system — every value arrives as a string, including
`"1"`.
- (A) would require explicit conversion on read.
- (C) is contradictory.
- (D) DictWriter quotes the comma correctly; no error.

### Q7 — (B)
`ensure_ascii=False` writes literal UTF-8 text instead of `\uXXXX`
escapes.
- (A) is the *default* (`ensure_ascii=True`) behavior.
- (C) Arabic is a valid string value.
- (D) nothing is dropped — that would be data loss.

### Q8 — (A)
By default `json.dumps` emits the non-standard `NaN` token — valid in
Python, invalid JSON for other parsers.
- (B) nan is not a string.
- (C) only with `allow_nan=False`.
- (D) it is not None.

### Q9 — (B)
Each line is a complete JSON document, so a crash corrupts at most the
last line, and appends never rewrite earlier data.
- (A) JSONL is streamable in O(1) memory — its defining advantage.
- (C) JSONL is UTF-8 text.
- (D) no schema declaration exists in JSONL.

### Q10 — (B)
pickle can encode `__reduce__` tricks; loading executes them — arbitrary
code execution on untrusted input.
- (A/C/D) are not the real (or any) risks.

### Q11 — (C)
On 3.13: `DEFAULT_PROTOCOL` is 4, `HIGHEST_PROTOCOL` is 5.
- (A/B/D) wrong versions for this runtime.

### Q12 — (B)
`safetensors` and numpy formats have no code-execution path on load —
safe for anything you did not author yourself.
- (A) shelve pickles its values — same RCE risk.
- (C) base64 of a pickle is still a pickle.
- (D) checksums verify integrity, not safety.

### Q13 — (B)
`with conn:` commits the transaction, so the row is persisted; the
connection remains open and queryable.
- (A) would mean the commit never happened.
- (C) the table was created before the `with` block.
- (D) `fetchone()[0]` returns an int.

### Q14 — (B)
`?` placeholders pass values as data — the only injection-safe form.
- (A/D) f-strings compile user input into SQL syntax.
- (C) `%s` is not sqlite3's placeholder (that's psycopg-style).

### Q15 — (B)
The context manager commits on success / rolls back on exception, but
closing is explicitly your job — a classic resource leak.
- (A) the close half is the common misconception.
- (C) one transaction per block, not per line.
- (D) it commits (or rolls back) — the close claim is wrong.

### Q16 — (D)
The exception inside the block triggers a rollback and propagates —
the `print` is never reached. (Had the print been reached, it would
have shown `0`.)
- (A/B/C) unreachable; the exception escapes the block.

### Q17 — (B)
`executemany` runs one statement many times through a single
Python-level call — orders of magnitude fewer calls than a loop.
- (A) it is faster, not slower.
- (C) it takes parameter tuples by design.
- (D) you still commit (or use `with conn:`).

### Q18 — (A)
shelve persists values (pickled) across opens within and across
processes — that is its purpose.
- (B) would mean nothing was persisted.
- (C) shelves don't return None for missing keys — they raise KeyError.
- (D) any picklable value works.

### Q19 — (A)
`struct.pack(">f", 3.5)` = `40600000` (big-endian float32); `b"hi"`
base64-encodes to `aGk=`.
- (B) `3f800000` is 1.0, not 3.5.
- (C) `aGVsbG8=` is the encoding of `hello`, not `hi`.
- (D) combines both wrong halves.

### Q20 — (C)
The `\"` sequences are escaped quotes *inside* the string value — the
line is one complete JSON object, and the value is the literal text
`x"}, {"hacked": true}`.
- (A) would require the quotes to *end* the string — but they are
  escaped, so no injection happened.
- (B) the line parses cleanly; there is no trailing-brace error.
- (D) `hacked` never becomes a key.
