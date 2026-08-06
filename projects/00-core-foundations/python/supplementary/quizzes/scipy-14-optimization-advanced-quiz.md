# SciPy 14 — Optimization Advanced Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · 8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1.** Which solver works with **only function values** — no
gradients, no Hessians?

- A) `BFGS`
- B) `Nelder-Mead`
- C) `L-BFGS-B`
- D) `SLSQP`

**E2.** You need box constraints per variable but **no general
equality/inequality constraints**. The right `minimize` method is:

- A) `Nelder-Mead`
- B) `BFGS`
- C) `L-BFGS-B`
- D) `differential_evolution`

**E3 (code-output).** What prints?
```python
from scipy import optimize

r = optimize.minimize(lambda x: (x[0] - 5.0) ** 2, np.array([0.0]),
                      method="L-BFGS-B", bounds=[(0.0, 2.0)])
print(r.x[0], r.fun)
```

- A) `5.0 0.0`
- B) `0.0 25.0`
- C) `2.0 9.0`
- D) `2.5 6.25`

**E4.** A constraint `{"type": "eq", "fun": lambda z: z.sum() - 1.0}`
requires the solver to satisfy:

- A) `z.sum() - 1.0 >= 0`
- B) `z.sum() == 1.0` (within numerical tolerance)
- C) `z.sum() <= 1.0`
- D) nothing — it only nudges the start point

**E5.** In `least_squares`, `f_scale` sets:

- A) the number of function evaluations allowed
- B) the residual scale below which the robust loss behaves
  quadratically and above which it downweights
- C) the step size of the finite-difference Jacobian
- D) the maximum number of parameters to fit

**E6 (code-output).** What prints?
```python
from scipy import optimize

r = optimize.differential_evolution(
    lambda x: x[0] ** 2 + 10.0 * np.sin(x[0]),
    bounds=[(-10.0, 10.0)], seed=42)
print(round(float(r.fun), 2), round(float(r.x[0]), 2))
```

- A) `-7.95 -1.31`
- B) `7.95 -1.31`
- C) `-7.95 1.31`
- D) `0.0 0.0`

---

## Medium

**M1 (code-output).** What prints?
```python
from scipy import optimize

def f(z):
    return (z[0] - 1.0) ** 2 + (z[1] - 2.0) ** 2

r = optimize.minimize(f, np.zeros(2), method="BFGS")
print(np.round(r.x, 1).tolist())
```

- A) `[0.0, 0.0]`
- B) `[1.0, 2.0]`
- C) `[1.0, 1.0]`
- D) `[2.0, 1.0]`

**M2 (code-output).** A line with seven +40 outliers is fit with
`least_squares` from `x0=[0, 0]`. What prints?
```python
import numpy as np
from scipy import optimize

x = np.linspace(0.0, 10.0, 25)
y = 2.0 * x + 1.0
y[-7:] += 40.0

def residual(p):
    return p[0] * x + p[1] - y

for loss in ("linear", "cauchy"):
    r = optimize.least_squares(residual, np.zeros(2), loss=loss)
    print(round(float(r.x[0]), 1), end=" ")
```

- A) `6.7 6.7`
- B) `6.7 2.0`
- C) `2.0 6.7`
- D) `2.0 2.0`

**M3.** After a constrained solve you check the equality residual
and get `1e-8`. What does that mean?

- A) the solve failed — restart with a new method
- B) acceptable: SLSQP satisfies constraints to floating-point
  tolerance, so verify `abs(residual) < 1e-6` rather than `== 0`
- C) the constraint was ignored by the solver
- D) the result is unusable; only `== 0.0` is valid

**M4 (code-output).** What prints?
```python
import numpy as np

mu = np.array([0.10, 0.05])
rf = 0.02
excess = mu - rf
print(np.round(excess / excess.sum(), 3))
```

- A) `[0.5   0.5  ]`
- B) `[0.667 0.333]`
- C) `[0.727 0.273]`
- D) `[1.    0.   ]`

**M5.** You have a multimodal objective. `BFGS` from a single start
gets stuck in a local minimum. The right tool is:

- A) `BFGS` with a smaller `tol`
- B) `differential_evolution` — a population-based global search
  over the box, at the cost of 10³–10⁵ evaluations
- C) `L-BFGS-B` with wide bounds
- D) `least_squares` with `loss="huber"`

**M6 (code-output).** What prints?
```python
import numpy as np
from scipy import optimize

r = optimize.minimize(
    lambda z: z[0] ** 2 + z[1] ** 2, np.array([0.2, 0.2]),
    method="SLSQP",
    constraints={"type": "ineq",
                 "fun": lambda z: z.sum() - 1.0})
print(np.round(r.x, 2))
```

- A) `[0.2 0.2]`
- B) `[0.5 0.5]`
- C) `[1.  1. ]`
- D) `[0.  1. ]`

**M7.** On an `OptimizeResult`, `nfev` and `nit` differ how?

- A) `nfev` counts objective evaluations (the true cost); `nit`
  counts iterations of the solver
- B) they are synonyms
- C) `nfev` counts failed steps; `nit` counts successful ones
- D) `nit` is only defined for `differential_evolution`

**M8 (code-output).** What prints?
```python
from scipy import optimize

r = optimize.least_squares(lambda p: p[0] - 1.0,
                           x0=np.array([0.0]), loss="linear")
print(r.x[0] < 1.1, r.cost < 1e-12)
```

- A) `True False`
- B) `False True`
- C) `True True`
- D) `False False`

**M9.** On smooth Rosenbrock, BFGS converges with ~114 evaluations
while Nelder-Mead needs ~189. Why is Nelder-Mead still useful?

- A) it is always faster for large problems
- B) it needs no derivatives, so it keeps working on noisy or
  non-smooth objectives where gradient steps are unreliable
- C) it guarantees the global minimum
- D) it handles constraints without extra parameters

---

## Hard

**H1.** With `mu=[0.10, 0.05]`, equal uncorrelated variances, and
`rf=0.02`, max-Sharpe allocation is `w ≈ [0.727, 0.273]` — not all
in the higher-return asset. Why?

- A) SLSQP cannot reach the boundary from equal starts
- B) mixing cuts volatility faster than it cuts return, so Sharpe
  rises; the optimum is the tangency portfolio `w ∝ Σ⁻¹(μ − rf)`
- C) the higher-return asset violates the bounds
- D) the Sharpe ratio is maximized at `w = rf` for every asset

**H2.** On +40-outlier data, `loss="soft_l1"` from a start *near
the truth* stalls at slope 7.2, while `loss="linear"` gives 6.7.
The best fix is:

- A) raise `f_scale` so more points are treated quadratically
- B) switch to `loss="cauchy"` — its aggressive downweighting
  escapes the nonconvex basin and recovers the true slope
- C) run `BFGS` on the same residual sum instead
- D) increase `max_nfev` tenfold and keep soft_l1

**H3.** Given slopes on the same outlier data — linear 6.661,
soft_l1 7.193, huber 7.197, cauchy 2.024 (truth 2.0) — which
ordering is by `|slope − truth|` descending?

- A) huber > soft_l1 > linear > cauchy
- B) linear > huber > soft_l1 > cauchy
- C) cauchy > linear > soft_l1 > huber
- D) soft_l1 > huber > linear > cauchy

**H4 (code-output).** What prints?
```python
from scipy import optimize

f = lambda x: x[0] ** 2
r1 = optimize.differential_evolution(f, [(-2.0, 2.0)], seed=0)
r2 = optimize.differential_evolution(f, [(-2.0, 2.0)], seed=0)
print(r1.x[0] == r2.x[0], r1.fun <= r2.fun)
```

- A) `True True`
- B) `True False`
- C) `False True`
- D) `False False`

**H5.** `curve_fit` supports bounds but **no constraints**, and you
must fit a model whose parameters sum to 1. The cleanest approach:

- A) pass `constraints={"type": "eq", ...}` to `curve_fit`
- B) fit freely, then divide the parameters by their sum
- C) reparameterize with a softmax (or solve the sum-of-squares
  with `minimize(..., method="SLSQP")` plus an `eq` constraint)
- D) tighten the bounds until the sum is 1 by construction

---

## Answer Key

**E1. B — Nelder-Mead.**
The simplex method evaluates the objective only; it has no
gradient machinery. `BFGS` and `L-BFGS-B` are quasi-Newton
(gradient-based); `SLSQP` uses gradients plus constraint
Jacobians.
*Distractors:* A/C/D all require differentiability; D also assumes
smoothness.

**E2. C — L-BFGS-B.**
The "B" stands for *bounded*: box constraints, no general
constraints. `Nelder-Mead`/`BFGS` take no bounds; SLSQP is for
constraints beyond boxes (it is slower on pure-box problems).
*Distractors:* A/B ignore the bounds requirement; D does not
support constraints and is far too expensive for a smooth box
problem.

**E3. C — `2.0 9.0`.**
L-BFGS-B clamps to the box: the unconstrained optimum `x=5` is
outside `[0, 2]`, so the solution is the boundary point `x=2.0`,
`fun=(2−5)²=9.0`.
*Distractors:* A is the unconstrained answer; B is the objective
at the start; D is the midpoint of the box, which has no reason
to be optimal.

**E4. B — `z.sum() == 1.0` within tolerance.**
`eq` means equality: `fun(x) == 0`. Because solvers work in
floating point, you verify with a tolerance (`abs(fun(x)) < 1e-6`),
never `== 0.0`.
*Distractors:* A is `ineq`; C is an inequality; D misunderstands
constraints — they are enforced, not used as hints.

**E5. B — the residual scale below which the robust loss is
quadratic.**
Residuals ≪ `f_scale` keep full weight; residuals ≫ `f_scale` are
downweighted by the chosen loss. It does not limit evaluations
(A), steps (C), or parameter count (D).

**E6. A — `-7.95 -1.31`.**
With `seed=42` the population is reproducible; the global minimum
of `x² + 10 sin(x)` on `[−10, 10]` is at `x ≈ −1.3064` with
`fun ≈ −7.9458` → rounded `-7.95 -1.31`.
*Distractors:* B flips the sign of `fun`; C flips the sign of `x`;
D confuses the local `x=0` stationary point with the global min.

**M1. B — `[1.0, 2.0]`.**
A convex quadratic: BFGS (a quasi-Newton method) converges in a
few iterations to machine precision. `round(..., 1)` gives the
exact optimum.
*Distractors:* A is the start; C/D swap or halve the coordinates.

**M2. B — `6.7 2.0`.**
Verified exercise data: `linear` slopes to 6.661 (`6.7`), pulled
by the +40 outliers; `cauchy` downweights them and recovers
2.024 (`2.0`). This is the whole point of robust loss.
*Distractors:* A misses the robust recovery; C/D invert which
loss is which.

**M3. B — acceptable within floating-point tolerance.**
Constrained solvers converge to feasibility within machine
precision. `1e-8` is normal; check `abs(residual) < 1e-6`, never
demand exact equality. A/C/D treat a numerically-satisfied
constraint as a failure.

**M4. C — `[0.727 0.273]`.**
The tangency portfolio: `w ∝ Σ⁻¹(μ − rf)`, and with diagonal
equal covariance `w ∝ excess = [0.08, 0.03]`, normalized by
`0.11` → `[0.727, 0.273]`.
*Distractors:* A is the naive 50/50; B is `excess` unnormalized
to the *sum of all returns*; D is the wrong all-in idea that H1
refutes.

**M5. B — differential_evolution.**
It explores the whole box with a population, so it escapes local
minima — at a cost of 10³–10⁵ evaluations. Shrinking the
tolerance (A) or widening bounds (C) does not change which basin
BFGS converges to; the robust loss (D) fixes outliers, not
multimodality.

**M6. B — `[0.5 0.5]`.**
`ineq` means `z0+z1−1 ≥ 0`, i.e. `z0+z1 ≥ 1`: the unconstrained
minimum `[0,0]` is infeasible, so the optimum sits on the active
boundary `z0+z1=1`. By symmetry the minimum of the norm there is
`[0.5, 0.5]`.
*Distractors:* A ignores the constraint; C violates it (sum 2 is
feasible but not minimal); D is a valid point but not the minimum
of the norm.

**M7. A — `nfev` counts evaluations, `nit` counts iterations.**
One iteration may evaluate the objective several times (line
search, finite differences), so `nfev` is the true cost — and the
fair metric when comparing methods.
*Distractors:* B/C invent semantics; D is false — every
`OptimizeResult` exposes both.

**M8. C — `True True`.**
`least_squares` finds `p=1.0` (within tolerance, so `< 1.1` is
True) and the final cost — half the squared residual sum — is
machine-zero, `< 1e-12`.

**M9. B — Nelder-Mead needs no derivatives.**
Gradient steps are unreliable on noisy/non-smooth objectives, so
the derivative-free simplex remains the robust fallback — even
though it uses more evaluations on smooth problems.
*Distractors:* A is contradicted by the numbers; C is false
(simplex is local); D is false — it has no constraint support.

**H1. B — the tangency portfolio.**
With equal uncorrelated variances, mixing two assets cuts
volatility (vol is concave in weights) while return blends
linearly, so Sharpe *increases* until `w ∝ Σ⁻¹(μ − rf)`. The
all-in portfolio (D) maximizes return, not return-per-risk.
*Distractors:* A is solver mechanics, not math; C is false —
bounds are `[0, 1]`.

**H2. B — switch to cauchy.**
Robust losses create nonconvex basins; soft_l1's gentler
downweighting stalls at 7.2 even from a good start. Cauchy's
aggressive downweighting (verified: 2.024) escapes it. Raising
`f_scale` (A) makes the loss *more* linear — worse; BFGS (C) and
more evaluations (D) do not change the loss landscape.

**H3. A — huber > soft_l1 > linear > cauchy.**
`|slope − 2|`: huber 5.197, soft_l1 5.193, linear 4.661, cauchy
0.024. The near-tie between huber/soft_l1 is the bad-basin
signature; cauchy uniquely recovers.
*Distractors:* B/C/D misorder the three failing losses or place
cauchy anywhere but last.

**H4. A — `True True`.**
`differential_evolution` with a fixed `seed` is fully
reproducible: identical runs give identical `x`; and a run can
never be worse than... well, `fun` is the global minimum found,
so `r1.fun <= r2.fun` is trivially `True` for identical runs.
Without a seed, results are not reproducible — a production bug
waiting to happen.

**H5. C — reparameterize or use SLSQP on the residual sum.**
`curve_fit` has no constraints argument (A). Post-normalizing
(B) changes the model's predictions. Bounds cannot express a
sum constraint (D). The two clean options: softmax
reparameterization `p = softmax(q)`, or minimize
`0.5 * sum(residual²)` with `method="SLSQP"` plus the `eq`
constraint — the exact pattern from the portfolio exercise.
