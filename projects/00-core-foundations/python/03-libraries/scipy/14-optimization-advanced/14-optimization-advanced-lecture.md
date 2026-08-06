# SciPy 14 — Optimization Advanced: methods, constraints, robustness

## Topic Overview

SciPy 07 introduced `minimize`, `curve_fit`, and root finding. This
lecture is the production layer: how to *choose* a solver, how to
make the solver respect reality (bounds, constraints), how to fit
when your data has outliers, how to search when the landscape is
multimodal, and how to read the result object so you never trust a
number without its diagnostics. Every concept maps to an
engineering decision: hyperparameter tuning, portfolio-style
allocation, calibration, and robust fitting pipelines.

## Learning Objectives

By the end of this lecture you will be able to:

1. Choose between Nelder-Mead, BFGS, L-BFGS-B, and SLSQP based on
   the problem's smoothness, size, and constraints.
2. Encode hard bounds and equality/inequality constraints.
3. Fit with `least_squares` robust losses and explain why
   "linear" loss is fragile.
4. Use `curve_fit` with priors and bounds for calibration.
5. Run global optimization (`differential_evolution`) on
   multimodal problems, seeded and reproducible.
6. Interpret the `OptimizeResult` diagnostics (success, nfev,
   nit, message) before trusting a solution.

## Prerequisites

- SciPy 07 (optimization basics: scalar min, `minimize`,
  `curve_fit`, `linprog`).
- NumPy 33 (linear algebra: matmul, norms — the portfolio example
  is a quadratic form).
- NumPy 30 (vectorization: objective functions should be
  array-friendly).

---

## Key Concepts

### 1. The solver menu — four methods cover 95% of problems

| Method | Needs | Best for | Weakness |
|---|---|---|---|
| `Nelder-Mead` | only function values | rough, noisy, non-smooth objectives | slow in high dims; no guarantees |
| `BFGS` | smooth objective (finite-diff gradient) | small/medium smooth problems | dense Hessian; no bounds natively |
| `L-BFGS-B` | smooth objective + bounds | large smooth problems with boxes | bounds only (no general constraints) |
| `SLSQP` | smooth objective + constraints | constrained problems (eq/ineq) | more evaluations; local method |

On Rosenbrock, BFGS converges in ~100 function evaluations;
Nelder-Mead needs ~200 and lands at 1e-14 instead of 1e-16. The
gradient information is not decoration — it is a 2-3× speedup on
the same problem.

```python
from scipy import optimize
import numpy as np

def rosenbrock(z):
    x, y = z
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

res = optimize.minimize(rosenbrock, np.array([-1.2, 1.0]), method="BFGS")
print(res.fun, res.nfev)     # ~1e-11, ~114
```

**Rule of thumb:** smooth → BFGS (or L-BFGS-B with bounds); noisy
or non-smooth → Nelder-Mead; constrained → SLSQP; global →
`differential_evolution` (Section 5).

---

### 2. Bounds — hard limits on the search box

Pass `bounds=[(lo, hi), ...]` to `L-BFGS-B`, `SLSQP`, and others.
Bounds are *hard*: the solver never evaluates outside them.

```python
res = optimize.minimize(lambda x: (x[0] - 5.0) ** 2, np.array([0.0]),
                        method="L-BFGS-B", bounds=[(0.0, 2.0)])
print(res.x[0], res.fun)     # 2.0, 9.0 -- optimum clamped to the bound
```

Use `(None, hi)` or `(lo, None)` for one-sided boxes. Bounds are
the cheapest way to encode domain knowledge: weights ≥ 0, rates in
(0, 3), prices in [0, 1].

---

### 3. Constraints — SLSQP and the geometry of feasible sets

`constraints` accepts a dict or list of dicts:

```python
cons = {"type": "eq", "fun": lambda z: np.sum(z) - 3.0}   # sum(z) == 3
res = optimize.minimize(lambda z: np.sum((z - 1.0) ** 2),
                        np.zeros(3), method="SLSQP", constraints=cons)
```

- `"eq"`: `fun(x) == 0` (equality).
- `"ineq"`: `fun(x) >= 0` (inequality).

**Verify the constraint after solving** — `res.x.sum()` should
equal the target to ~1e-6. SLSQP is a local method: with a
nonconvex feasible set it may stop at a local optimum, so try
several starting points or combine with a global pass (Section 5).

**AI relevance:** the portfolio example in the exercise —
maximize (return − risk-free)/risk over weights with `sum(w) = 1`
and `w_i ∈ [0, 1]` — is exactly the shape of allocation problems
(and of mixture-weight tuning in ensembles).

---

### 4. `least_squares` — the robust fitting engine

`scipy.optimize.least_squares(fun, x0, loss=...)` minimizes
`sum(rho(fun(x)^2))`. With `loss="linear"` it is plain least
squares — and one outlier at high x can drag the slope from 2.0
to 6.7.

| loss | behavior |
|---|---|
| `"linear"` | quadratic — every outlier counts fully |
| `"soft_l1"` / `"huber"` | gentle downweighting of large residuals |
| `"cauchy"` | aggressive downweighting — most outlier-proof |

In the exercise data, 7 extreme outliers at high x: linear fit
slope 6.66, cauchy fit slope 2.02 (truth 2.0). Cauchy's
aggressiveness is a double-edged sword: it also makes the problem
more nonconvex — the same data with `soft_l1` stalls in a bad
basin at 7.19. **Practical playbook:** try `soft_l1` first for
mild protection; escalate to `cauchy` when outliers are extreme;
always compare against the linear fit and look at residuals.

`least_squares` also supports `bounds`, `f_scale` (the residual
scale below which losses behave quadratically), and analytic
`jac` for speed.

---

### 5. Global optimization — when the landscape lies

Gradient methods answer "which minimum is near my start?".
`differential_evolution(func, bounds, seed=...)` answers "what is
the best minimum in this box?" by evolving a population of
candidates — no gradients, robust to multimodal landscapes.

```python
def multimodal(x):
    return x[0] ** 2 + 10.0 * np.sin(x[0])

res = optimize.differential_evolution(multimodal, bounds=[(-10.0, 10.0)],
                                      seed=42)
print(res.x[0], res.fun)     # -1.3064, -7.9458 -- the global minimum
```

`f(x) = x² + 10·sin(x)` has several local minima; from x0 = 5,
BFGS would happily report the local one. `differential_evolution`
found the global min at −7.95, deterministically, because of the
seed.

**Cost:** population × generations of evaluations — typically
10³–10⁵ objective calls. Use it for low-dimensional tuning
(sparse-feature selection, kernel parameters), not for
million-parameter problems.

---

### 6. Convergence diagnostics — read the result object

Every `OptimizeResult` carries the verdict:

| field | meaning |
|---|---|
| `success` | did the solver claim convergence? |
| `message` | human-readable reason (e.g., "CONVERGENCE: REL_REDUCTION_OF_F <= FTOL") |
| `nfev` | number of objective evaluations — the real cost |
| `nit` | iterations |
| `fun` / `x` | best value / best point |

**Never trust `x` without `success`.** A "solution" from a
converged-but-wrong basin is the classic silent failure: the
solver is happy, the answer is garbage. When `success=False`,
inspect `message` (max iterations? line search failed?) and
relax/repair accordingly.

---

### 7. `curve_fit` with priors and bounds — calibration done right

`curve_fit(f, x, y, p0, bounds)` wraps `least_squares` (or
Levenberg-Marquardt) with the parameter-vector API:

```python
def decay(x, A, B, C):
    return A * np.exp(-B * x) + C

popt, pcov = optimize.curve_fit(decay, t, y, p0=[1.0, 1.0, 0.0],
                                bounds=([0.0, 1e-3, 0.0], [10.0, 3.0, 2.0]))
```

- `p0` is the prior — a good guess turns a wild search into
  polishing; a bad one can still land in a local minimum.
- `bounds` keep parameters physically meaningful (A ≥ 0, B > 0).
- `pcov` is the covariance of the estimates — its diagonal is the
  parameter uncertainty, which is how you report "A = 3.02 ± 0.05".

---

### 8. The evaluation budget — objective functions are the currency

Every optimizer works in units of objective evaluations:

- BFGS: ~100 evals on smooth 2-D problems.
- Nelder-Mead: ~200 evals on the same problem, lower accuracy.
- `differential_evolution`: 10³–10⁵ evals by design.

If your objective costs 100 ms (a model retrain, a database
query), a global search is hours; Nelder-Mead is minutes. **Match
the optimizer to the evaluation budget**, not to elegance.

---

## Common Mistakes to Avoid

1. **Using Nelder-Mead on smooth problems** — BFGS is faster and
   more accurate when gradients exist.
2. **Ignoring bounds** — unbounded fits produce negative weights,
   negative rates, and absurd parameters; encode domain knowledge.
3. **Trusting `x` without `success`** — a converged solver can
   still be in the wrong basin; check `success`, `message`, and
   the constraint residuals.
4. **Plain `loss="linear"` on dirty data** — one outlier column
   can double your slope; switch to `soft_l1`/`cauchy` and
   compare.
5. **Local methods on multimodal landscapes** — run
   `differential_evolution` (seeded) or multiple starts.
6. **Forgetting `seed` in global search** — without it every run
   is unreproducible and CI breaks.
7. **Not checking constraints after SLSQP** — `sum(x) == 1` is
   only true to solver tolerance; assert it.
8. **`curve_fit` without `p0` or bounds** — defaults are
   `p0=[1]*n`, which is fine only when your truth is near 1.

---

## Best Practices

- **Start from multiple points** for any local method; keep the
  best `fun`.
- **Seal every global search with a seed.**
- **Report `nfev` and `success` alongside solutions** — they are
  the provenance of the number.
- **Use robust losses by default on real data**; treat `linear`
  as the clean-data special case.
- **Verify constraints numerically** after solving, always.
- **Prefer analytic `jac` when you have it** — it converts a
  slow, noisy fit into a tight one.
- **Budget evaluations**: `differential_evolution` on a 100-ms
  objective is 10⁴ seconds — think first.

---

## Complexity and Cost

| Method | Evaluations (typical) | Needs | Use when |
|---|---|---|---|
| Nelder-Mead | ~10²–10³ | function only | noisy/non-smooth, low dim |
| BFGS | ~10² | smooth + gradient | smooth, small/medium |
| L-BFGS-B | ~10² | smooth + gradient | smooth + bounds, larger dims |
| SLSQP | ~10²–10³ | smooth + constraints | constrained local |
| `least_squares` | ~10¹–10² | residual vector | fitting, robust losses |
| `differential_evolution` | 10³–10⁵ | function + box | global search, low dim |
| `curve_fit` | ~10¹–10² | model + p0 | calibration with priors |

---

## AI Engineering Relevance

- **Hyperparameter tuning** at small scale: `differential_
  evolution` on validation loss (seeded) before reaching for
  Optuna; the budget math transfers.
- **Model calibration**: `curve_fit` temperature scaling,
  Platt scaling, or reward-model calibration with bounds and
  `pcov`-reported uncertainty.
- **Ensemble/mixture weights**: SLSQP with `sum(w)=1`, `w≥0` —
  the exact portfolio pattern of Example 8.
- **Robust metric fitting**: latency/throughput models with
  outliers → `least_squares(loss="cauchy")`.
- **Serving-time optimization**: L-BFGS-B on memory/accuracy
  trade-off curves with hard bounds on budget.
- **Evaluation honesty**: `success` + `nfev` + constraint checks
  are the reproducibility contract for any fitted parameter.

---

## Practice Exercises

1. Run BFGS and Nelder-Mead on Rosenbrock from the same start;
   compare `fun`, `nfev`, and `success`. Confirm the gradient
   method wins on both axes.
2. Minimize `(x−5)²` under bounds `(0, 2)` with L-BFGS-B and
   verify the optimum is exactly the bound; then add an equality
   constraint `x == 1.5` with SLSQP and verify it holds to 1e-6.
3. Build the outlier dataset (25 points, 7 high-x outliers);
   fit with linear, soft_l1, and cauchy losses; compare slopes
   and residuals. Which loss do you trust, and why?
4. Fit `A·exp(−B·x) + C` with `curve_fit` from a deliberately bad
   `p0`; show that bounds save the fit where no bounds fail.
5. On `x² + 10·sin(x)` over [−10, 10]: run BFGS from x0=5 (local
   minimum), then `differential_evolution(seed=42)` (global).
   Print both `fun` values and explain the difference.

---

## Summary

- Solver menu: BFGS (smooth), L-BFGS-B (smooth + bounds),
  Nelder-Mead (noisy), SLSQP (constraints),
  `differential_evolution` (global).
- Bounds are hard boxes; equality/inequality constraints are
  SLSQP's job — verify them after solving.
- `least_squares` robust losses (soft_l1 → cauchy) save fits from
  outliers; compare against linear and read residuals.
- `curve_fit(p0=..., bounds=...)` is calibration with priors and
  `pcov` uncertainty.
- Never trust a solution without `success`, `message`, and
  `nfev`.

## Quick Reference

```python
from scipy import optimize
import numpy as np

# local, smooth
r = optimize.minimize(f, x0, method="BFGS")

# bounded
r = optimize.minimize(f, x0, method="L-BFGS-B",
                      bounds=[(0.0, 1.0), (None, 3.0)])

# constrained
cons = [{"type": "eq", "fun": lambda z: np.sum(z) - 1.0},
        {"type": "ineq", "fun": lambda z: z[0] - 0.1}]
r = optimize.minimize(f, x0, method="SLSQP", constraints=cons)

# robust least squares
r = optimize.least_squares(residual, x0, loss="cauchy")

# global, reproducible
r = optimize.differential_evolution(f, bounds=[(-10.0, 10.0)], seed=42)

# calibration with priors
popt, pcov = optimize.curve_fit(model, x, y, p0=[1.0, 1.0],
                                bounds=([0, 0], [10, 5]))

# always check
print(r.success, r.nfev, r.message)
```

## Next Steps

- SciPy 15 (sparse matrices): optimization over sparse systems
  (`spsolve`) — the same fitting ideas at 10⁶+ rows.
- SciPy 13 (statistical tests): use `curve_fit`+`pcov` to report
  parameter uncertainty alongside significance.
- Revisit SciPy 07 to connect the basics with this advanced
  layer.
