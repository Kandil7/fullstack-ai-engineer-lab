# Challenge 05: filtering-advanced — Logic, NULLs & Patterns

## 🥉 Bronze — Range + Precedence (~20 min)

**Task:** Implement `filter_range(conn, lo, hi)` returning model names
with `metric` in `[lo, hi]`, using an explicit `BETWEEN`-free form:
`metric >= lo AND metric <= hi`, sorted by name.

**Signature:**
```python
def filter_range(conn: sqlite3.Connection, lo: float, hi: float) -> list[str]:
```

**Requirements:**
- Correct AND/OR precedence: the range must be parenthesized when
  combined with anything else
- Return sorted names

**Constraints:** n ≤ 10⁴.

| Setup | Input | Expected |
|-------|-------|----------|
| bert 0.9, gpt 0.8, llm 0.7 | `(0.75, 0.85)` | `['gpt']` |

---

## 🥈 Silver — Pattern Matching (~35 min)

**Task:** Implement `pattern_match(conn, pattern)` that returns model
names matching a LIKE `pattern`, using only SQL LIKE (no Python
`fnmatch`/`re`). Additionally return the count of names that contain an
underscore (`_`) — escaped as a literal with `ESCAPE '\'` so the `_`
wildcard doesn't match every single character.

**Signature:**
```python
def pattern_match(conn: sqlite3.Connection, pattern: str) -> dict:
```

**Requirements:**
- `%` and `_` semantics must be SQL's, not Python's
- Literal underscore counts use `LIKE '%\_%' ESCAPE '\'`
- Return `{"names": [...], "single_underscore": n}`

**Constraints:** n ≤ 10⁴.

| Setup | Input | Expected |
|-------|-------|----------|
| bert_v2, bert_v3, gpt | `'bert%'` | `names == ['bert_v2','bert_v3']` |
| Same table | — | `single_underscore == 2` |

---

## 🥇 Gold — NULL-Aware Filter (~50 min)

**Task:** Implement `null_aware_report(conn)` that buckets rows by
`metric IS NULL` / not, via CASE, and returns only non-NULL rows
matching an optional `EXISTS` condition: names whose id appears in a
`runs` table (create `runs(id, model_id)` if missing).

**Signature:**
```python
def null_aware_report(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- Use `CASE WHEN metric IS NULL THEN 'missing' ELSE 'ok' END`
- Use `EXISTS (SELECT 1 FROM runs r WHERE r.model_id = m.id)` — never
  a Python membership check
- Return `{"buckets": {"ok": n, "missing": n}, "with_runs": [names]}`

**Constraints:** n ≤ 10⁴.

| Setup | Expected |
|-------|----------|
| 3 ok rows (2 with runs), 1 NULL row | `buckets == {'ok': 3, 'missing': 1}`, `with_runs` has 2 names |

**Follow-up:** Why does `metric = NULL` never match? (Answer: any
comparison with NULL is UNKNOWN, so WHERE drops the row — IS NULL is the
only correct test.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/05-filtering-advanced/test_challenge.py -v
```

## Test File Structure

```
challenges/05-filtering-advanced/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
