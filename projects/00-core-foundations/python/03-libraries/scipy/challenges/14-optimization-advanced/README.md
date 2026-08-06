# Challenge 14: Optimization Advanced — Bound, Robust, Allocate

Three tiers of optimizer discipline: Bronze keeps the answer in a
box, Silver keeps the fit honest with outliers, Gold allocates
under constraints.

## 🥉 Bronze — Bounded Minimization (~15 min)

**Task:** Implement `minimize_box(func, x0, lo, hi)` that
minimizes `func` over the box `[lo, hi]` using L-BFGS-B and
returns the solution `x` (a float).

**Signature:**
```python
def minimize_box(func, x0: float, lo: float, hi: float) -> float:
```

| Input | Expected |
|---|---|
| `(x-5)**2`, x0=0, lo=0, hi=2 | `2.0` (clamped at the bound) |
| `(x-0.3)**2`, x0=0, lo=0, hi=2 | `0.3` (interior optimum) |
| `x**2`, x0=1, lo=-1, hi=1 | `0.0` |
| `(x+3)**2`, x0=0, lo=0, hi=2 | `0.0` (clamped at lo) |

**Constraints:** none on the objective. **No Python loops or
comprehensions.** The returned value must lie inside `[lo, hi]`
to machine precision.

---

## 🥈 Silver — Robust Line Fitting (~35 min)

**Task:** Implement `fit_robust_line(x, y, loss)` returning
`(slope, intercept)` from `scipy.optimize.least_squares` with the
given `loss` in `{"linear", "soft_l1", "huber", "cauchy"}`.
Unknown losses raise `ValueError`.

**Signature:**
```python
def fit_robust_line(x: np.ndarray, y: np.ndarray, loss: str) -> tuple[float, float]:
```

| Input | Expected |
|---|---|
| clean line, `"linear"` | slope ≈ truth (atol 0.1) |
| 7 high-x outliers, `"cauchy"` | slope within 0.3 of truth |
| same outliers, `"linear"` | slope off by > 0.5 (the fragility demo) |
| same outliers, `"huber"` | valid tuple, but **stalls in a bad basin** — slope off by > 1.0 (lecture's lesson: only cauchy recovers here) |
| `loss="fake"` | raises `ValueError` |

**Constraints:** n ≤ 10⁴. **No Python loops or comprehensions.**
The residual function must be a one-line array expression.

---

## 🥇 Gold — Max-Sharpe Allocation (~75 min)

**Task:** Implement `allocate_weights(mu, cov, risk_free)` that
maximizes the Sharpe ratio `(mu·w − rf) / sqrt(wᵀ cov w)` over
weights with `sum(w) = 1` and `w_i ∈ [0, 1]` (long-only, fully
invested) using SLSQP. Return the weight vector.

**Signature:**
```python
def allocate_weights(mu: np.ndarray, cov: np.ndarray,
                     risk_free: float) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `mu=[0.10, 0.05]`, equal diag cov, rf=0.02 | `w ≈ [0.727, 0.273]` — the tangency portfolio |
| `mu=[0.05, 0.10]`, same | `w ≈ [0.273, 0.727]` |
| `mu=[0.08, 0.08]`, equal cov, rf=0.02 | `w ≈ [0.5, 0.5]` (any split is optimal; SLSQP lands on the start) |
| seeded 3-asset case | sum ≈ 1, all in [0, 1], Sharpe > single-asset Sharpe |

**Constraints:** n ≤ 10 assets. **No Python loops or
comprehensions.** Equality constraint residual must be < 1e-6;
weights must satisfy the box to 1e-6.

**Follow-up:** why is the `[0.10, 0.05]` case not all-in on the
high-return asset? (Answer: with equal uncorrelated variances, the
max-Sharpe portfolio is the **tangency portfolio**
`w ∝ Σ⁻¹(μ − rf)` — here `[0.08, 0.03] / 0.11 = [0.727, 0.273]`.
Mixing the assets cuts volatility while keeping return, so the
Sharpe ratio *rises*. And in the equal-return case any split has
the same Sharpe — assert tolerance, not exact values, for ties.)

---

## Running

```bash
pytest 03-libraries/scipy/challenges/14-optimization-advanced/test_challenge.py -v
```

```text
collected ... items  (all tests pass against solution.py;
                      starter.py raises NotImplementedError by design)
```

## Test File Structure

```
challenges/14-optimization-advanced/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Correctness + edge cases + deterministic data
```
