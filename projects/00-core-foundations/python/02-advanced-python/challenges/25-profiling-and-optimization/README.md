# Challenge 25: Profiling and Optimization

Replace nested scans with dicts, dedup without losing order, and prove
memoization by call count — all with guards the naive solutions fail.

## 🥉 Bronze — First-Occurrence Dedup (~15 min)

**Task:** Implement `dedup_chunks(items)`: return the items with
duplicates removed, keeping the **first occurrence** of each value in
its original position.

**Signature:**
```python
def dedup_chunks(items: list[str]) -> list[str]:
```

| Input | Expected |
|---|---|
| `["a", "b", "a", "c", "b"]` | `["a", "b", "c"]` |
| `["x"]` | `["x"]` |
| `[]` | `[]` |
| `["a", "a", "a"]` | `["a"]` |

**Constraints:** n ≤ 10^5 — must be O(n) via a `set` of seen values.
The naive `if x not in result` list scan is O(n²): at 100,000 items it
takes tens of seconds and the time guard fails it.

---

## 🥈 Silver — Hash Join (~35 min)

**Task:** Implement `hash_join(records, index)`: join audit records to
index entries on `chunk_id` (the classic O(n²) → O(n) case). Each
record is `{"chunk_id": int, "op": str}`; each index entry is
`{"chunk_id": int, "text": str}`. Return `(chunk_id, text)` tuples for
records whose id exists in the index; **skip** records with missing
ids.

**Signature:**
```python
def hash_join(records: list[dict], index: list[dict]) -> list[tuple]:
```

| Input | Expected |
|---|---|
| `records=[{"chunk_id": 1, "op": "add"}], index=[{"chunk_id": 1, "text": "A"}]` | `[(1, "A")]` |
| record with id missing from index | skipped |
| empty inputs | `[]` |

**Constraints:** n = 25,000 records and 25,000 index entries, with
matches deliberately at the *end* of the index (reverse-ordered ids) so
the nested-scan solution must scan ~half the index per record — O(n²)
and the time guard fails it. Build the `dict` once; each lookup is O(1).

---

## 🥇 Gold — Memoization by the Numbers (~75 min)

**Task:** Implement `fib_stats(n)`: compute `fib(n)` with memoization
while counting every call to the recursive function. Return
`(result, call_count)`.

**Signature:**
```python
def fib_stats(n: int) -> tuple[int, int]:
```

| Input | Expected |
|---|---|
| `(0)` | `(0, 1)` |
| `(1)` | `(1, 1)` |
| `(10)` | `(55, <= 20)` |
| `(25)` | `(75025, <= 60)` |

**Constraints:** the naive exponential version makes **242,785 calls**
at n=25 and fails the `calls <= 60` guard; the memoized version makes
~49 (counting every invocation, memo hits included). Cache results in
a dict keyed by `n` — the number of calls is the smoking gun the
profiler (lecture 25) uses to spot this class of bug.

---

## Running

```bash
pytest challenges/25-profiling-and-optimization/test_challenge.py -v
```

Tests default to **starter.py** (must fail). To verify the reference
implementation:

```bash
# PowerShell
$env:CHALLENGE_MODULE = "solution"
pytest challenges/25-profiling-and-optimization/test_challenge.py -v
```

## Test File Structure

```
challenges/25-profiling-and-optimization/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
