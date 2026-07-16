# SciPy Lecture 03: Basic Functions

## 🎯 Topic Overview

SciPy extends NumPy with advanced mathematical functions for optimization, root finding, and curve fitting — essential tools for data analysis and scientific modeling.

## 📚 Learning Objectives

1. Use SciPy for root finding with `root()` and `root_scalar()`
2. Use `minimize()` for multivariate optimization
3. Perform curve fitting with `curve_fit()`

---

## 1. Root Finding

```python
import numpy as np
from scipy import optimize

# Single variable root finding
def f(x):
    return x**2 - 4  # Roots at x = ±2

# Using root_scalar
sol = optimize.root_scalar(f, bracket=[0, 5])  # Find positive root
print(f"Root: x = {sol.root:.4f}")

# Using root (multivariate)
def system(vars):
    x, y = vars
    return [x**2 + y**2 - 25, x - y - 1]

sol = optimize.root(system, [1, 4])
print(f"Solution: x={sol.x[0]:.3f}, y={sol.x[1]:.3f}")
```

---

## 2. Optimization

```python
# Function minimization
def rosenbrock(x):
    """Rosenbrock banana function."""
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

result = optimize.minimize(rosenbrock, [0, 0], method='Nelder-Mead')
print(f"Optimal at: x={result.x[0]:.4f}, y={result.x[1]:.4f}")
print(f"Function value: {result.fun:.6f}")

# Global optimization
result = optimize.shgo(rosenbrock, bounds=[(-2, 2), (-2, 2)])
print(f"Global optimum: x={result.x}")
```

---

## 3. Curve Fitting

```python
# Generate noisy data
x = np.linspace(0, 10, 50)
true_params = (2.5, 1.3, 0.5)
y = true_params[0] * np.exp(-true_params[1] * x) + true_params[2]
y_noisy = y + np.random.normal(0, 0.1, size=len(x))

# Define model
def model(x, a, b, c):
    return a * np.exp(-b * x) + c

# Fit
popt, pcov = optimize.curve_fit(model, x, y_noisy, p0=[1, 1, 1])
print(f"Estimated: a={popt[0]:.3f}, b={popt[1]:.3f}, c={popt[2]:.3f}")
print(f"True:      a={true_params[0]:.3f}, b={true_params[1]:.3f}, c={true_params[2]:.3f}")
```

---

## Summary

| Function | Task | Key Parameters |
|----------|------|---------------|
| `root_scalar()` | 1D root finding | `f`, `bracket`, `method` |
| `root()` | N-D root finding | `fun`, `x0`, `method` |
| `minimize()` | N-D optimization | `fun`, `x0`, `method` |
| `curve_fit()` | Curve fitting | `f`, `xdata`, `ydata`, `p0` |
