# Challenge 30: Vectorize the Given Loop

Every tier starts from a Python loop you are told to replace. The
test suite rejects loops and comprehensions for Silver and Gold
(AST operation counting), so the solutions must be single compiled
expressions.

## 🥉 Bronze — Sigmoid From a Loop (~15 min)

**Task:** Implement `sigmoid(X)` — the given loop multiplies,
exponentiates, and divides elementwise. Rewrite it as one
vectorized expression.

**Signature:**
```python
def sigmoid(X: np.ndarray) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `[[0.0]]` | `[[0.5]]` |
| `[0.0, 1.0]` | `[0.5, 0.73105858]` |
| `X` shape `(100, 8)`, seeded | shape `(100, 8)`, matches loop reference |

**Constraints:** n ≤ 10⁴. Any correct approach passes.

---

## 🥈 Silver — Score Cleanup (~35 min)

**Task:** Implement `clean_scores(scores, lo, hi)` that clamps scores
into `[lo, hi]` **and** zeroes out any score whose absolute value is
below `0.01`. One combined mask (or `where` chain) — no loops.

**Signature:**
```python
def clean_scores(scores: np.ndarray, lo: float, hi: float) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `[0.5, -0.005, 2.0, 0.0]`, lo=-1, hi=1 | `[0.5, 0.0, 1.0, 0.0]` |
| `scores` shape `(1_000_000,)`, seeded | same shape, matches reference |

**Constraints:** n ≤ 10⁶. **No Python loops or comprehensions.**

---

## 🥇 Gold — Stable Row Softmax (~75 min)

**Task:** Implement `softmax_rows(X)` — the numerically stable softmax
over each row: subtract the row max, exponentiate, divide by the row
sum. No loops. Use `keepdims=True` for the row max and the row sum.

**Signature:**
```python
def softmax_rows(X: np.ndarray) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `[[1.0, 2.0, 3.0]]` | `[0.09003057, 0.24472847, 0.66524096]` |
| `[[0.0, 0.0]]` | `[0.5, 0.5]` (all-equal row is uniform) |
| `X` shape `(20, 10)`, seeded | rows sum to 1, matches loop reference |

**Constraints:** n = 50 000 rows, d = 64, **peak memory < 100 MB**
(a loop-free but naive implementation that skips the max-subtraction
still passes values, but `tracemalloc` catches implementations that
materialize extra full-size temporaries per row). No Python loops or
comprehensions.

**Follow-up:** what breaks if the max-subtraction is removed?
(Answer: `exp(x)` overflows to `inf` at x > 709 for float64 — the
naive softmax returns `nan` rows; the stable version does not.)

---

## Running

```bash
pytest 03-libraries/numpy/challenges/30-vectorization/test_challenge.py -v
```

```text
collected ... items  (all tests pass against solution.py;
                      starter.py raises NotImplementedError by design)
```

## Test File Structure

```
challenges/30-vectorization/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Correctness + edge cases + op-count/memory guards
```
