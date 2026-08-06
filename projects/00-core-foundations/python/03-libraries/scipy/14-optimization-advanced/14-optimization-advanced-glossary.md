# Optimization Advanced — Glossary 14

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `BFGS` | Solver | Quasi-Newton gradient method; the smooth-default |
| Bounds | Concept | Hard box constraints `(lo, hi)` per variable |
| Cauchy loss | Loss | Aggressive robust loss: strongest outlier downweighting |
| Constraint | Concept | Equality/inequality rule on the solution (`eq`/`ineq`) |
| `curve_fit` | Function | Fit model parameters to data with `p0` and bounds |
| `differential_evolution` | Solver | Population-based global optimizer over a box |
| `f_scale` | Parameter | Residual scale below which robust losses are quadratic |
| Feasible set | Concept | The region of parameter space satisfying constraints |
| `least_squares` | Function | Robust nonlinear least-squares engine |
| `L-BFGS-B` | Solver | Bounded BFGS: smooth + box constraints, larger dims |
| Local optimum | Concept | Best point in a neighborhood — not necessarily global |
| `loss` | Parameter | Robust-loss selector: linear / soft_l1 / huber / cauchy |
| `message` | Field | Human-readable convergence verdict on the result |
| `Nelder-Mead` | Solver | Derivative-free simplex; for noisy/non-smooth objectives |
| `nfev` | Field | Number of objective evaluations — the real cost |
| `OptimizeResult` | Type | The result object: x, fun, success, nfev, nit, message |
| `p0` | Parameter | Initial parameter guess in `curve_fit` — the prior |
| `pcov` | Field | Covariance of fitted parameters — uncertainty report |
| `SLSQP` | Solver | Sequential quadratic programming; constrained local min |
| `success` | Field | Boolean convergence flag — check before trusting x |

## Detailed Definitions

### `BFGS`
**Definition**: Broyden-Fletcher-Goldfarb-Shanno — a quasi-Newton
method using approximate gradient information. The default choice
for smooth objectives without constraints.

**Example**:
```python
import numpy as np
from scipy import optimize

def rosen(z):
    x, y = z
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

r = optimize.minimize(rosen, np.array([-1.2, 1.0]), method="BFGS")
print(r.fun, r.nfev)        # ~1e-11, ~114
```

**Complexity**: O(d²) per iteration memory (Hessian approx).
**Related**: `L-BFGS-B`, `Nelder-Mead`

---

### Bounds
**Definition**: Hard per-variable limits `[(lo, hi), ...]` passed
to `L-BFGS-B`, `SLSQP`, `least_squares`, and
`differential_evolution`. The solver never evaluates outside.

**Example**:
```python
import numpy as np
from scipy import optimize

r = optimize.minimize(lambda x: (x[0] - 5.0) ** 2, np.array([0.0]),
                      method="L-BFGS-B", bounds=[(0.0, 2.0)])
print(r.x[0], r.fun)        # 2.0, 9.0 -- clamped to the bound
```

**Complexity**: free — a feasibility check per evaluation.
**Related**: Constraint, Feasible set

---

### Cauchy loss
**Definition**: `loss="cauchy"` in `least_squares`: the most
aggressive robust loss — residuals far beyond `f_scale` lose
almost all weight. Best when outliers are extreme; most
nonconvex of the robust family.

**Example**:
```python
from scipy import optimize

r = optimize.least_squares(residual, x0, loss="cauchy")
```

**Complexity**: same as linear — cost function shape only.
**Related**: `loss`, `f_scale`, `least_squares`

---

### Constraint
**Definition**: A rule the solution must satisfy:
`{"type": "eq", "fun": ...}` (fun == 0) or `{"type": "ineq",
"fun": ...}` (fun >= 0). SLSQP is the general constrained solver.

**Example**:
```python
import numpy as np
from scipy import optimize

cons = {"type": "eq", "fun": lambda z: np.sum(z) - 1.0}
r = optimize.minimize(lambda z: np.sum(z ** 2), np.zeros(3),
                      method="SLSQP", constraints=cons)
print(r.x.sum())            # ~1.0
```

**Complexity**: extra gradient evaluations per constraint.
**Related**: Bounds, Feasible set, `SLSQP`

---

### `curve_fit`
**Definition**: `optimize.curve_fit(f, x, y, p0, bounds)` fits the
parameterized model `f(x, A, B, ...)` to data. Wraps
least-squares machinery with the parameter API.

**Example**:
```python
import numpy as np
from scipy import optimize

def decay(x, A, B, C):
    return A * np.exp(-B * x) + C

popt, pcov = optimize.curve_fit(decay, t, y, p0=[1.0, 1.0, 0.0],
                                bounds=([0, 0, 0], [10, 3, 2]))
```

**Complexity**: ~10¹–10² evaluations.
**Related**: `p0`, `pcov`, `least_squares`

---

### `differential_evolution`
**Definition**: Global optimizer over a box: evolves a population
of candidate solutions; no gradients; finds the best basin.
Always pass `seed` for reproducibility.

**Example**:
```python
import numpy as np
from scipy import optimize

f = lambda x: x[0] ** 2 + 10.0 * np.sin(x[0])
r = optimize.differential_evolution(f, bounds=[(-10.0, 10.0)], seed=42)
print(r.x[0], r.fun)        # -1.3064, -7.9458 -- global min
```

**Complexity**: 10³–10⁵ evaluations by design.
**Related**: Local optimum

---

### `f_scale`
**Definition**: The residual scale in `least_squares`: residuals
smaller than `f_scale` are treated nearly quadratically; larger
ones get downweighted by the robust loss. Default 1.0.

**Example**:
```python
from scipy import optimize

r = optimize.least_squares(residual, x0, loss="soft_l1", f_scale=0.5)
```

**Complexity**: —.
**Related**: `loss`, Cauchy loss

---

### Feasible set
**Definition**: The region of parameter space where all bounds
and constraints hold. Solvers move inside it; the optimum is the
best point *in* it.

**Example**:
```python
# sum(z) == 1 with z >= 0: the simplex -- the feasible set of weights
```

**Complexity**: —.
**Related**: Bounds, Constraint

---

### `least_squares`
**Definition**: `optimize.least_squares(fun, x0, loss=...)`
minimizes `sum(rho(fun(x)²))` — the robust nonlinear fitting
engine. Supports bounds, `f_scale`, and analytic `jac`.

**Example**:
```python
import numpy as np
from scipy import optimize

x = np.linspace(0, 10, 25)
y = 2.0 * x + 1.0
r = optimize.least_squares(lambda p: p[0] * x + p[1] - y,
                           x0=[0.0, 0.0], loss="cauchy")
print(r.x[0])               # ~2.0
```

**Complexity**: ~10¹–10² evaluations.
**Related**: `loss`, `f_scale`

---

### `L-BFGS-B`
**Definition**: Limited-memory BFGS with box bounds — the
large-smooth-problem default. Bounds only; no general
constraints.

**Example**:
```python
from scipy import optimize

r = optimize.minimize(f, x0, method="L-BFGS-B", bounds=[(0.0, 1.0)])
```

**Complexity**: O(d) memory per iteration.
**Related**: `BFGS`, Bounds

---

### Local optimum
**Definition**: A point better than all nearby points but not
necessarily the best in the box. Gradient methods converge to
local optima near their start — the reason global search exists.

**Example**:
```python
# x^2 + 10*sin(x) has local minima; BFGS from x0=5 finds one, not the global
```

**Complexity**: —.
**Related**: `differential_evolution`

---

### `loss`
**Definition**: The robust-loss selector in `least_squares`:
`linear` (quadratic), `soft_l1`, `huber`, `cauchy` (most
aggressive). Choose by how extreme the outliers are.

**Example**:
```python
r = optimize.least_squares(residual, x0, loss="soft_l1")
```

**Complexity**: —.
**Related**: Cauchy loss, `f_scale`

---

### `message`
**Definition**: The human-readable convergence verdict on an
`OptimizeResult`, e.g. "CONVERGENCE: REL_REDUCTION_OF_F <= FTOL".
Read it when `success` is False.

**Example**:
```python
print(r.message)            # why the solver stopped
```

**Complexity**: —.
**Related**: `success`, `OptimizeResult`

---

### `Nelder-Mead`
**Definition**: Derivative-free simplex method: only function
values needed. The choice for noisy or non-smooth objectives;
slower and less accurate than BFGS on smooth ones.

**Example**:
```python
from scipy import optimize

r = optimize.minimize(f, x0, method="Nelder-Mead",
                      options={"xatol": 1e-6, "fatol": 1e-6})
```

**Complexity**: ~10²–10³ evaluations.
**Related**: `BFGS`

---

### `nfev`
**Definition**: Number of objective evaluations used — the true
cost of the solve, comparable across methods. Report it with any
solution.

**Example**:
```python
print(r.nfev)               # the evaluation budget spent
```

**Complexity**: —.
**Related**: `OptimizeResult`

---

### `OptimizeResult`
**Definition**: The object every `scipy.optimize` function
returns: `x`, `fun`, `success`, `nfev`, `nit`, `message`, plus
solver-specific fields.

**Example**:
```python
print(r.x, r.fun, r.success, r.nfev)
```

**Complexity**: —.
**Related**: `success`, `message`, `nfev`

---

### `p0`
**Definition**: The initial parameter guess in `curve_fit` — your
prior. A good `p0` turns a wild search into polishing; a bad one
can strand the fit in a local minimum.

**Example**:
```python
popt, pcov = optimize.curve_fit(decay, t, y, p0=[1.0, 1.0, 0.0])
```

**Complexity**: —.
**Related**: `curve_fit`, `pcov`

---

### `pcov`
**Definition**: The covariance matrix of the fitted parameters
from `curve_fit`. Its diagonal gives parameter uncertainty:
`A = popt[0] ± sqrt(pcov[0, 0])`.

**Example**:
```python
popt, pcov = optimize.curve_fit(decay, t, y)
print(np.sqrt(np.diag(pcov)))       # per-parameter std errors
```

**Complexity**: O(p³) after the fit.
**Related**: `curve_fit`, `p0`

---

### `SLSQP`
**Definition**: Sequential quadratic programming — the general
constrained local solver: bounds, equality (`eq`), and inequality
(`ineq`) constraints.

**Example**:
```python
from scipy import optimize

cons = [{"type": "eq", "fun": lambda z: np.sum(z) - 1.0}]
r = optimize.minimize(f, x0, method="SLSQP", bounds=[(0.0, 1.0)] * 3,
                      constraints=cons)
```

**Complexity**: extra constraint-gradient work per iteration.
**Related**: Constraint, Bounds

---

### `success`
**Definition**: The Boolean convergence flag on the result.
`False` means the solver gave up (max iterations, line-search
failure, infeasible). Never trust `x` when it is False.

**Example**:
```python
if r.success:
    best = r.x
else:
    print(r.message)
```

**Complexity**: —.
**Related**: `OptimizeResult`, `message`

## Key Concepts Summary

### The solver menu
- Smooth → BFGS; smooth + bounds → L-BFGS-B; noisy → Nelder-Mead;
  constraints → SLSQP; global → differential_evolution.

### Encoding reality
- Bounds: hard boxes per variable.
- Constraints: `eq`/`ineq` dicts, verified after solving.

### Robustness
- `least_squares` losses: linear → soft_l1/huber → cauchy.
- Cauchy survives extreme outliers; soft_l1 is gentler but can
  stall in bad basins.

### Trusting results
- Check `success`, `message`, `nfev`; verify constraints
  numerically; report `pcov` uncertainty with fits.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `SLSQP` — ___
2. `nfev` — ___
3. Cauchy loss — ___
4. `p0` — ___
5. Bounds — ___
6. `differential_evolution` — ___

**Answers:**
1. e, 2. b, 3. f, 4. c, 5. a, 6. d

a. Hard per-variable boxes the solver never leaves
b. Number of objective evaluations — the real cost
c. The prior guess for `curve_fit` parameters
d. Population-based global optimizer over a box
e. Constrained local solver for eq/ineq constraints
f. Most aggressive robust loss — extreme outlier downweighting

---

**Related docs:** [scipy.optimize](https://docs.scipy.org/doc/scipy/reference/optimize.html) ·
[Back to lecture](14-optimization-advanced-lecture.md)
