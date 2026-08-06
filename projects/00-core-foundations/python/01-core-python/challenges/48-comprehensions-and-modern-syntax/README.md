# Challenge 48: Comprehensions & Modern Syntax

Turn batch transforms into readable expressions, parse once instead of
twice, and stream a deduplicated corpus without materializing it.

## 🥉 Bronze — Token Filter (~15 min)

**Task:** Implement `tokenize_and_filter(texts, min_len)`, which returns a
list of uppercased tokens whose length is at least `min_len`. Write it as a
**single list comprehension** (transform + filter).

**Signature:**
```python
def tokenize_and_filter(texts: list[str], min_len: int) -> list[str]:
```

| Input | Expected |
|---|---|
| `["the", "cat", "on", "mat"], 3` | `["THE", "CAT", "MAT"]` |
| `["a", "ab", "abc"], 2` | `["AB", "ABC"]` |
| `["a", "b"], 5` | `[]` |
| `[], 1` | `[]` |

**Constraints:** `n <= 10^3`. Any correct approach passes.

---

## 🥈 Silver — Parse Once, Use Once (~35 min)

**Task:** Implement `parse_floats(values, parser)`, which calls `parser` on
every value and keeps the parsed floats for values that did not parse to
`None`, preserving order. The requirement: **each value is parsed exactly
once** — use the walrus `:=` (or a loop variable) so the parse result is
computed once and tested once, never twice.

**Signature:**
```python
def parse_floats(
    values: list[str],
    parser: Callable[[str], float | None],
) -> list[float]:
```

| Input | Expected |
|---|---|
| `["3.14", "abc", "2.5"], float_or_none` | `[3.14, 2.5]` |
| `["1", "2", "3"], float_or_none` | `[1.0, 2.0, 3.0]` |
| `["x", "y"], float_or_none` | `[]` |
| `[], float_or_none` | `[]` |

**Constraints:** `n <= 10^6`, `parser` is O(1). The tests **count calls to
`parser`** and fail if it is invoked more than `len(values)` times — a
double-parse solution (`parser(v)` in the condition and again in the body)
runs `2n` calls and fails the guard.

---

## 🥇 Gold — Lazy Dedup Stream (~75 min)

**Task:** Implement `dedupe_stream(rows)`, a **generator** that yields
rows in first-seen order, dropping duplicates. It must consume its input
**lazily**: producing the first output requires only a bounded prefix of
the input, not the whole stream. The dedup set is the only state you may
retain.

**Signature:**
```python
def dedupe_stream(rows: Iterable[str]) -> Iterator[str]:
```

| Input | Expected |
|---|---|
| `["a", "b", "a", "c", "b"]` | `["a", "b", "c"]` |
| `["x", "x", "x"]` | `["x"]` |
| `[]` | `[]` |
| `["a"]` | `["a"]` |

**Constraints:** stream of `10^7` rows, **single pass** — each input row is
fetched exactly once, and no row is fetched before it is needed. The tests
wrap the input in a counting iterator: fetching the first output must
consume at most 2 input rows, and full consumption must fetch every row
exactly once.

**Follow-up:** what breaks first at 10^9 rows? (Answer: the dedup set —
holding 10^9 unique strings exceeds any memory budget. You would switch to
probabilistic membership — a Bloom filter — accepting a small false-duplicate
rate.)

---

## Running

```bash
pytest challenges/48-comprehensions-and-modern-syntax/test_challenge.py -v
```

## Test File Structure

```
challenges/48-comprehensions-and-modern-syntax/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
