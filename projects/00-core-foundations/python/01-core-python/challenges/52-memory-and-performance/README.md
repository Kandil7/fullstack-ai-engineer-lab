# Challenge 52: Memory & Performance

Think in bytes. Compute the embedding budget before the job, stream a
multi-GB corpus under a memory ceiling, and derive statistics in a
single pass.

## 🥉 Bronze — Embedding RAM Math (~15 min)

**Task:** Implement `embedding_ram_bytes(rows, dim, dtype_bits)`, the
whiteboard calculation: `rows × dim × (dtype_bits // 8)` bytes.

**Signature:**
```python
def embedding_ram_bytes(rows: int, dim: int, dtype_bits: int = 32) -> int:
```

| Input | Expected |
|---|---|
| `(1_000_000, 768, 32)` | `3_072_000_000` (≈3.07 GB) |
| `(1_000_000, 768, 16)` | `1_536_000_000` (half) |
| `(1_000_000, 768, 64)` | `6_144_000_000` (double) |
| `(0, 768, 32)` | `0` |

---

## 🥈 Silver — Single-Pass Streaming Statistics (~35 min)

**Task:** Implement `streaming_stats(path)`, which reads a file of
numbers (one per line, blank lines skipped) and returns
`(mean, variance)` — **population** variance — in a **single pass with
O(1) memory** (Welford's algorithm: running mean + running sum of
squared deviations; never collect the values).

**Signature:**
```python
def streaming_stats(path: Path) -> tuple[float, float]:
```

| Input (file) | Expected |
|---|---|
| `2\n4\n4\n4\n5\n5\n7\n9` | `(5.0, 4.0)` |
| `1\n2\n3` | `(2.0, 0.6666666666666666)` |
| `10` | `(10.0, 0.0)` |
| `\n\n` (blanks only) | `(0.0, 0.0)` |
| empty file | `(0.0, 0.0)` |

**Constraints:** single pass, O(1) memory. The tests run `tracemalloc`
over a 1,000,000-line file: the streaming peak must stay under
**2 MiB** (a materialized list of 1M floats is ~32 MB). Use
`pytest.approx`-style tolerance for the variance of big files.

---

## 🥇 Gold — Process a Multi-GB Corpus Under a 50 MiB Ceiling (~75 min)

**Task:** Implement two functions.

1. `corpus_stats(path)` — one pass over a corpus file (one token per
   line): return a dict with `lines` (count), `total_chars` (sum of
   token lengths, excluding the trailing newline), `longest` (length of
   the longest token), and `histogram` (token length → count). The
   histogram is bounded by the max token length — O(max_len) memory,
   never O(n).
2. `embedding_budget(ram_bytes, model_bytes, index_bytes, dim,
   dtype_bits)` — the largest batch of `dim`-dim embeddings that fits
   in the remaining RAM (0 if the model + index already exceed RAM):
   `available = ram - model - index`; `available // (dim * bytes)`.

**Signatures:**
```python
def corpus_stats(path: Path) -> dict:
def embedding_budget(ram_bytes: int, model_bytes: int, index_bytes: int,
                     dim: int, dtype_bits: int = 32) -> int:
```

| Input | Expected |
|---|---|
| file `abc\na\nabc\nxy` | `{"lines": 4, "total_chars": 9, "longest": 3, "histogram": {3: 2, 1: 1, 2: 1}}` |
| `(32e9, 8e9, 4e9, 768, 32)` | `6_510_416` |
| `(32e9, 8e9, 4e9, 768, 16)` | `13_020_833` |
| `(8e9, 8e9, 4e9, 768, 32)` | `0` (no room) |

**Constraints:** `corpus_stats` must stream: the tests generate a
1,000,000-line corpus and assert a `tracemalloc` peak **under 50 MiB**
(materializing the tokens as a list is ~65 MB and fails the ceiling)
plus exact histogram/total correctness against the token-length
formula (4 + number of digits).

---

## Running

```bash
pytest challenges/52-memory-and-performance/test_challenge.py -v
```

## Test File Structure

```
challenges/52-memory-and-performance/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
