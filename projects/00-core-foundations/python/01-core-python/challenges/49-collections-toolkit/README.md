# Challenge 49: Collections Toolkit

Top-k is *the* retrieval operation: candidates in, best k out. Do it with
the right structure — a heap, not a sort.

## 🥉 Bronze — Token Top-K (~15 min)

**Task:** Implement `top_k_tokens(tokens, k)`, which returns the `k` most
frequent tokens as `(token, count)` pairs, ordered by count descending and
**alphabetically among ties**. Use `Counter` and a deterministic tie-break
sort (`(-count, token)`).

**Signature:**
```python
def top_k_tokens(tokens: list[str], k: int) -> list[tuple[str, int]]:
```

| Input | Expected |
|---|---|
| `["a", "b", "a", "c", "a", "b"], 2` | `[("a", 3), ("b", 2)]` |
| `["x", "y"], 1` | `[("x", 1)]` |
| `["b", "a", "b", "a"], 2` | `[("a", 2), ("b", 2)]` (alphabetical tie-break) |
| `[], 3` | `[]` |

**Constraints:** `n <= 10^3`, `k <= 10^2`. Any correct approach passes.

---

## 🥈 Silver — Top-K Scores (~35 min)

**Task:** Implement `top_k_scores(scores, k)`, which returns the `k`
largest values from an iterable of floats, descending. The right structure
is a **heap** (`heapq.nlargest`): O(n log k). A sort-based solution
(`sorted(scores, reverse=True)[:k]`) is O(n log n) and must fail the
comparison budget.

**Signature:**
```python
def top_k_scores(scores: Iterable[float], k: int) -> list[float]:
```

| Input | Expected |
|---|---|
| `[0.1, 0.9, 0.4, 0.8], 2` | `[0.9, 0.8]` |
| `[5.0], 1` | `[5.0]` |
| `[1.0, 2.0], 5` | `[2.0, 1.0]` (k > n returns all) |
| `[], 3` | `[]` |
| `[3.0, 3.0, 1.0], 2` | `[3.0, 3.0]` |

**Constraints:** `n <= 10^6`, `k = 10`. The tests wrap every score in a
comparison-counting object and assert the total comparisons stay under
`10 * n` — `sorted` needs ~`n log2 n` (≈ 17x over budget at n = 10^5);
`nlargest` stays near `n`. Counting comparisons, never wall-clock.

---

## 🥇 Gold — Streaming Top-K (~75 min)

**Task:** Implement `top_k_stream(stream, k)`, which returns the `k`
highest-scoring `(doc_id, score)` pairs, descending by score, from a
**stream** — an iterable you may only pass over once. Same O(n log k)
heap approach as Silver, but now the memory bound matters: you may not
materialize the stream; a heap of size `k` is the only permitted state.

**Signature:**
```python
def top_k_stream(
    stream: Iterable[tuple[str, float]],
    k: int,
) -> list[tuple[str, float]]:
```

| Input | Expected |
|---|---|
| `[("a", 0.1), ("b", 0.9), ("c", 0.5)], 2` | `[("b", 0.9), ("c", 0.5)]` |
| `[("a", 0.7), ("b", 0.7)], 2` | both, in any tie order (scores equal) |
| `[], 5` | `[]` |
| `[("a", 1.0)], 0` | `[]` |

**Constraints:** stream of `10^7` items, memory <= 50 MB, single pass. The
tests run the memory guard with `tracemalloc` over `10^6` items (materializing
that stream is ~140 MB — far over the ceiling) and verify the result is
exactly the top-k.

**Follow-up:** what breaks first at 10^9 items? (Answer: the single-pass
constraint — you cannot re-read the stream, so any two-pass or
materializing approach is impossible; the heap of size k is the only
structure that fits.)

---

## Running

```bash
pytest challenges/49-collections-toolkit/test_challenge.py -v
```

## Test File Structure

```
challenges/49-collections-toolkit/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
