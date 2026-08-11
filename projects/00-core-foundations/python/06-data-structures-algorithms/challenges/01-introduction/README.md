# Challenge 01: Introduction — Complexity by Measurement

Nobody hands you a Big-O label in production. You get a latency graph and a bill.
The skill that actually pays is the inverse: given operation counts at a few input
sizes, *name the growth curve*, then decide whether one shard can hold the corpus.
Every later challenge in this module leans on that instinct.

## 🥉 Bronze — Classify the Growth Curve (~15 min)

**Task:** Implement `classify_growth(samples)`. Each sample is `(n, ops)` — the
number of operations your profiler counted at input size `n`. Return the label of
the growth curve that fits best, one of exactly:

```
"O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)"
```

**The fitting rule (use exactly this — the tests assume it):** for each candidate
basis `f(n)` in the order `1, log2(n), n, n*log2(n), n**2`, do a least-squares fit
through the origin, `c = sum(ops*f) / sum(f*f)` (use `c = 0.0` when `sum(f*f) == 0`),
then compute the residual `sum((ops - c*f)**2)`. Return the label with the smallest
residual; on a tie, prefer the **earlier / simpler** candidate.

**Signature:**
```python
def classify_growth(samples: list[tuple[int, int]]) -> str:
```

| Input | Expected |
|---|---|
| `[(100, 7), (200, 7), (400, 7)]` | `"O(1)"` |
| `[(128, 7), (256, 8), (512, 9)]` | `"O(log n)"` |
| `[(100, 100), (200, 200), (400, 400)]` | `"O(n)"` |
| `[(128, 896), (256, 2048), (512, 4608)]` | `"O(n log n)"` |
| `[(100, 10_000), (200, 40_000)]` | `"O(n^2)"` |
| `[(100, 0), (200, 0)]` | `"O(1)"` (all-zero ties resolve to the simplest) |

**Constraints:** raise `ValueError` on fewer than 2 samples, on any `n < 1`, and on
any `ops < 0`. Samples may arrive in any `n` order. Any correct implementation of
the stated rule passes.

---

## 🥈 Silver — Prove Your Dedup Pass Is Linear (~35 min)

**Task:** A corpus loader wants to know how much deduplication will save, so it
counts *colliding pairs*: the number of index pairs `i < j` with
`ids[i] == ids[j]`. Implement `duplicate_pair_count(ids)`.

The answer is a one-liner over a frequency table — `sum(c * (c - 1) // 2)` — and
that shape is O(n). The obvious nested loop is also *correct*, and it is the reason
somebody's ingest job takes four hours.

**Signature:**
```python
def duplicate_pair_count(ids: Sequence[int]) -> int:
```

| Input | Expected |
|---|---|
| `[1, 2, 1]` | `1` |
| `[5, 5, 5]` | `3` (pairs 0-1, 0-2, 1-2) |
| `[1, 2, 3]` | `0` |
| `[7]` | `0` |
| `[]` | `0` |
| `[4, 4, 9, 9]` | `2` |

**Constraints:** `n <= 4000` in the guard. The tests wrap every id in an `int`
subclass that counts **every comparison and every hash** it takes part in, then:

1. assert the total stays under `4 * n` — a hash table costs about one hash per
   element; the nested loop costs `n*(n-1)/2` comparisons, which at `n = 4000` is
   **~8.0M against a 16k budget (500x over)**, and a `sorted()`-then-group pass is
   O(n log n) and also over;
2. run the measurement at `n = 500, 1000, 2000, 4000` and feed the counts into the
   Bronze fitting rule — the classification must come back `"O(n)"`. The nested
   loop classifies as `"O(n^2)"`. The guard fails with that label in the message,
   so the test tells you your own complexity.

---

## 🥇 Gold — Capacity Planning Under an Op Budget (~75 min)

**Task:** You have a cost model: `predict(n)` returns the number of operations your
retrieval pass needs for a corpus of `n` chunks. It is non-decreasing and
`predict(0) == 0`. Your P95 latency budget converts to `op_budget` operations.
Implement `max_supported_n(predict, op_budget)`: the largest `n` in
`[0, 10**18]` whose predicted cost still fits the budget.

`predict` is expensive — in the real system it is a benchmark run, not arithmetic —
so the number of times you call it *is* the cost of the answer.

**Signature:**
```python
def max_supported_n(
    predict: Callable[[int], int],
    op_budget: int,
) -> int:
```

| Input | Expected |
|---|---|
| `predict = lambda n: n`, budget `1000` | `1000` |
| `predict = lambda n: n * n`, budget `1000` | `31` (`31^2 = 961`, `32^2 = 1024`) |
| `predict = lambda n: 5 * n`, budget `4` | `0` (not even `n = 1` fits) |
| `predict = lambda n: 0`, budget `0` | `10**18` (the clamp) |
| `predict = lambda n: n`, budget `0` | `0` |

**Constraints:** search space is `10**18`, so an answer needs about
`60 + 60 = 120` probes: **exponential (galloping) search** to bracket the answer,
then binary search inside the bracket. The test wraps `predict` in a spy that
**raises after 200 calls**, so a linear scan (`for n in range(...)`) does not run
slowly — it fails immediately with `predict call budget exceeded`. `op_budget < 0`
raises `ValueError`.

**Follow-up:** the plan says one shard holds `n_max` chunks. What breaks first when
the corpus is 10^9? (Answer: the cost model itself. `predict` was fitted on
in-memory sizes; past RAM the curve gains a new term — page faults / network round
trips — so the measured exponent shifts and `n_max` is overstated. You re-measure
*above* the working-set cliff, or you plan shards from the memory bound and treat
ops as a secondary constraint.)

---

## Running

```bash
# Should FAIL until you implement starter.py
pytest 06-data-structures-algorithms/challenges/01-introduction/test_challenge.py -v

# Validate the reference solution
CHALLENGE_USE_SOLUTION=1 pytest 06-data-structures-algorithms/challenges/01-introduction/test_challenge.py -q
```

## Test File Structure

```
challenges/01-introduction/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
├── test_challenge.py  # Tests (default: run against starter.py)
└── quiz.md            # 8 recall questions
```
