# Challenge 15: Sets

A retriever returns the same chunk from three overlapping documents. Send all
three to the model and you pay for the same tokens three times and push real
context out of the window. Dedup is not tidying — it is a cost and quality
control, and the container you pick decides whether it is O(n) or O(n^2).

## 🥉 Bronze — Dedup Retrieved Chunks (~15 min)

**Task:** Implement `dedupe_chunks(chunk_ids)`, returning the ids with
duplicates removed and **first-seen order preserved**. Retrieval order is rank
order — most relevant first — so `list(set(ids))` is wrong here even though it
is O(n): it discards the ranking.

**Signature:**
```python
def dedupe_chunks(chunk_ids: list[str]) -> list[str]:
```

| Input | Expected |
|---|---|
| `["a", "b", "a", "c", "b"]` | `["a", "b", "c"]` |
| `["z", "y", "x", "z"]` | `["z", "y", "x"]` |
| `["d", "d", "d"]` | `["d"]` |
| `[]` | `[]` |

**Constraints:** `n <= 10^4`. Must not mutate the input. Any correct
order-preserving approach passes — but use a `seen` set, not
`if cid not in result`, which is O(n^2).

---

## 🥈 Silver — Stopword Filtering (~35 min)

**Task:** Implement `filter_stopwords(tokens, stopwords)`, returning the tokens
with every stopword removed, order preserved. The lesson is the **container**:
`tok not in stopwords` against a `set` hashes once per token; the identical line
against a `list` rescans the whole collection every time.

**Signature:**
```python
def filter_stopwords(tokens: list[str], stopwords: set[str]) -> list[str]:
```

| Input | Expected |
|---|---|
| `["the", "cat", "sat"], {"the"}` | `["cat", "sat"]` |
| `["ml", "ml", "the"], {"the"}` | `["ml", "ml"]` |
| `["The", "the"], {"the"}` | `["The"]` (case-sensitive) |
| `["a", "b"], set()` | `["a", "b"]` |
| `[], {"the"}` | `[]` |

**Constraints:** `n = 10^4` tokens, 500 stopwords. The tests wrap values in a
`str` subclass that counts equality comparisons and assert the total stays under
`2 * n`. Set membership registers ~0 counted comparisons; converting the
stopwords to a list and scanning registers **~3.7M against a 20k budget** —
185x over. Same source line, 500x the work.

---

## 🥇 Gold — Streaming Novelty Filter (~75 min)

**Task:** Implement `novel_chunks(retrieved, already_sent)`, a **generator**
yielding only ids not already sent in earlier conversation turns, each at most
once, in rank order. This is the multi-turn agent case: the stream can be huge,
you may pass over it once, and `already_sent` belongs to the caller.

**Signature:**
```python
def novel_chunks(
    retrieved: Iterable[str],
    already_sent: set[str],
) -> Iterator[str]:
```

| Input | Expected |
|---|---|
| `["a", "b", "c"], {"b"}` | yields `"a"`, `"c"` |
| `["a", "a", "b"], set()` | yields `"a"`, `"b"` |
| `["a", "b"], {"a", "b"}` | yields nothing |
| `[], {"a"}` | yields nothing |

**Constraints:** stream of `4 * 10^5` ids with only 500 distinct, memory
< 2 MB, single pass, **must not mutate `already_sent`**. The tests check three
things a shortcut breaks:

- `tracemalloc` peak — `list(retrieved)` or `set(retrieved)` costs **23 MB
  against a 2 MB ceiling**.
- **Laziness** — the generator body must not run before the first `next()`.
  A function that builds a list and returns `iter(...)` fails this.
- **Caller's set untouched** — `already_sent.add(...)` would silently shrink a
  later turn's context. Copy into a local `seen` instead.

Note that `set(retrieved) - already_sent` fails on all three counts *and*
destroys rank order.

**Follow-up:** the memory bound is proportional to the number of *distinct
novel* ids, not the stream length — so what breaks when nearly every id is
novel (10^8 distinct)? (Answer: `seen` itself becomes the ceiling. You would
trade exactness for a probabilistic membership structure — a Bloom filter —
accepting a false-positive rate that silently drops a few novel chunks.)

---

## Running

```bash
# Should FAIL until you implement starter.py
pytest 01-core-python/challenges/15-sets/test_challenge.py -v

# Validate the reference solution
CHALLENGE_USE_SOLUTION=1 pytest 01-core-python/challenges/15-sets/test_challenge.py -q
```

## Test File Structure

```
challenges/15-sets/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
