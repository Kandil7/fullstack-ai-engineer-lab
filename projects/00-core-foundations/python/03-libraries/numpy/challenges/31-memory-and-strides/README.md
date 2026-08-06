# Challenge 31: Memory Contracts — Views, Copies, Layout

Memory is the contract: these tiers test that you can produce
zero-copy views, repair layout without over-copying, and downcast
without unnecessary allocation. The test suite uses
`np.shares_memory`, `base` checks, and `tracemalloc` — never wall
clock.

## 🥉 Bronze — Column View (~15 min)

**Task:** Implement `column_view(X, j)` returning a **view** of
column `j` — no copy. Writing through the result must change `X`.

**Signature:**
```python
def column_view(X: np.ndarray, j: int) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `X = [[1,2],[3,4]]`, `j=1` | `[2, 4]` |
| `X` shape `(100, 8)`, any `j` | shape `(100,)`, `np.shares_memory(X, out)` is True |
| `out[0] = 99` after | `X[0, j] == 99` |

**Constraints:** n ≤ 10⁵. Any correct approach passes.

---

## 🥈 Silver — Layout Repair (~35 min)

**Task:** Implement `ensure_contiguous(x)` — return `x` itself when
it is already C-contiguous, otherwise return a **C-contiguous copy**
of the same values.

**Signature:**
```python
def ensure_contiguous(x: np.ndarray) -> np.ndarray:
```

| Input | Expected |
|---|---|
| C-contiguous `(50, 30)` | same object (`out is x`) |
| `x.T` of a C array | new object, `flags.c_contiguous` True, same values |
| F-order `np.asfortranarray(x)` | new object, C-contiguous |

**Constraints:** n ≤ 10⁶. **No Python loops or comprehensions.**
Copy only when the layout demands it — `tracemalloc` asserts the
contiguous path allocates ~nothing.

---

## 🥇 Gold — Downcast Without Waste (~75 min)

**Task:** Implement `downcast_when_safe(X)` that returns float32
data **with zero copying when the data is already float32** and a
single float32 cast otherwise. Goal: a serving pipeline that halves
embedding memory without paying for needless copies.

**Signature:**
```python
def downcast_when_safe(X: np.ndarray) -> np.ndarray:
```

| Input | Expected |
|---|---|
| float32 `(5000, 1000)` | `out is X` (identity, zero allocation) |
| float64 `(5000, 1000)` | new float32 array, `np.allclose(out, X, atol=1e-6)` |
| int64 `(5000, 1000)` | new float32 array, values preserved |

**Constraints:** n = 5·10⁶ elements. **Peak allocation: float32 path
< 1 KB (no copy); float64 path < 30 MB** (the 20 MB result plus
slack — a double-copy implementation is rejected by `tracemalloc`).
No Python loops or comprehensions.

**Follow-up:** what breaks first if you apply this to int64 weights
with values above 2²⁴? (Answer: float32 can represent all integers
up to 2²⁴ exactly; beyond that, `astype` silently rounds — a
precision contract, not just a memory one.)

---

## Running

```bash
pytest 03-libraries/numpy/challenges/31-memory-and-strides/test_challenge.py -v
```

```text
collected ... items  (all tests pass against solution.py;
                      starter.py raises NotImplementedError by design)
```

## Test File Structure

```
challenges/31-memory-and-strides/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Correctness + aliasing + memory guards
```
