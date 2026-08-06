# Challenge 32: Dtype Decisions — Range, Sanity, Budget

Precision is a budget you allocate. Bronze checks integer ranges
before downcasting; Silver sanitizes `nan`/`inf` at the boundary;
Gold measures float16 error and *decides* — the exact serving
trade-off from the lecture.

## 🥉 Bronze — Smallest Safe Integer Dtype (~15 min)

**Task:** Implement `int_downcast(values)` returning the values cast
to the smallest integer dtype that holds them without wraparound:
int8, int16, int32, or int64.

**Signature:**
```python
def int_downcast(values: np.ndarray) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `[0, 1, -1, 127]` | dtype `int8` |
| `[0, 1, -1, 128]` | dtype `int16` |
| `[300, -300]` | dtype `int16` |
| `[100_000]` | dtype `int32` |
| `[3_000_000_000]` | dtype `int64` |

**Constraints:** n ≤ 10⁵. Any correct approach passes — but no
Python loops in any tier.

---

## 🥈 Silver — Sanitize Non-Finite Values (~35 min)

**Task:** Implement `sanitize(X, fill)` that replaces every `nan`
and `inf` with `fill` and returns `(cleaned, n_bad)` — the number of
replaced values.

**Signature:**
```python
def sanitize(X: np.ndarray, fill: float) -> tuple[np.ndarray, int]:
```

| Input | Expected |
|---|---|
| `[1.0, nan, inf, 2.0]`, fill=0.0 | `([1.0, 0.0, 0.0, 2.0], 2)` |
| seeded `(1000, 8)` with 37 non-finite, fill=-1.0 | cleaned, `n_bad == 37` |
| all-finite array, fill=5.0 | same values, `n_bad == 0` |

**Constraints:** n ≤ 10⁶. **No Python loops or comprehensions.**
`np.isfinite` + masking is the whole solution.

---

## 🥇 Gold — Precision-Budget Serving Cast (~75 min)

**Task:** Implement `serving_cast(weights, budget)` that returns
float16 **only when the worst-case relative error stays under
`budget`**; otherwise returns the weights unchanged (float32/f64 as
given). This is the measured decision from the lecture's float16
section.

**Signature:**
```python
def serving_cast(weights: np.ndarray, budget: float) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `rng.normal(size=(1024, 1024))`, budget=0.01 | float16 array (error ≈ 0.0005 ≪ 0.01) |
| same weights, budget=1e-4 | same object (error ≈ 0.0005 > 1e-4) |
| all-zeros weights, budget=1e-4 | float16 array (error ≈ 0) |
| weights already float16, any budget | same object (no re-cast) |

**Constraints:** n = 10⁶ elements. **Memory contract
(tracemalloc-enforced):** the keep path must return the *same
object* — `result is weights` — and peak allocation in *either*
path must stay under **3× input bytes** (one measurement pass + one
final cast; anything copying twice trips the guard). No Python
loops or comprehensions.

**Follow-up:** why does `budget=1e-4` reject normal-distributed
weights but accept all-zeros? (Answer: the zero weights are exactly
representable in float16 — error is 0; normal weights round at
~2⁻¹¹ ≈ 5e-4 relative, exceeding a 1e-4 budget.)

---

## Running

```bash
pytest 03-libraries/numpy/challenges/32-dtypes-and-precision/test_challenge.py -v
```

```text
collected ... items  (all tests pass against solution.py;
                      starter.py raises NotImplementedError by design)
```

## Test File Structure

```
challenges/32-dtypes-and-precision/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Correctness + edge cases + memory guards
```
