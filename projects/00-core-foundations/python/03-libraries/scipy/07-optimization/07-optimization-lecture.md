# SciPy Lecture 07: Optimization

## 🎯 Topic Overview

Optimization finds the best solution from available alternatives — minimizing or maximizing a function subject to constraints. SciPy's `optimize` module provides algorithms for unconstrained, constrained, and global optimization.

## 📚 Learning Objectives

1. Use `minimize()` with different methods
2. Apply constrained optimization
3. Solve least-squares problems
4. Perform global optimization

---

## 1. Unconstrained Optimization

```python
import numpy as np
from scipy import optimize

# 1D minimization
result = optimize.minimize_scalar(lambda x: x**2 + 10*np.sin(x))
print(f"Minimum at x = {result.x:.4f}, f(x) = {result.fun:.4f}")

# Multi-dimensional
def rosenbrock(x):
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

result = optimize.minimize(rosenbrock, [0, 0], method='Nelder-Mead')
print(f"Rosenbrock minimum: {result.x}")

# With gradient (BFGS)
result = optimize.minimize(rosenbrock, [0, 0], method='BFGS')
print(f"BFGS: {result.x}")
```

---

## 2. Constrained Optimization

```python
# Bounds
result = optimize.minimize(
    lambda x: (x[0] - 1)**2 + (x[1] - 2.5)**2,
    [2, 0],
    bounds=[(0, None), (0, None)]
)
print(f"With bounds: {result.x}")

# Constraints
def constraint(x):
    return x[0] + 2*x[1] - 2  # Must be >= 0

result = optimize.minimize(
    lambda x: (x[0] - 1)**2 + (x[1] - 2.5)**2,
    [2, 0],
    constraints={'type': 'ineq', 'fun': constraint}
)
print(f"With constraints: {result.x}")
```

---

## 3. Least-Squares and Global Optimization

```python
# Least-squares fitting
def model(x, a, b, c):
    return a * np.exp(-b * x) + c

x_data = np.linspace(0, 4, 50)
y_data = model(x_data, 2.5, 1.3, 0.5) + np.random.normal(0, 0.1, 50)

def residuals(params):
    return model(x_data, *params) - y_data

result = optimize.least_squares(residuals, [1, 1, 1])
print(f"Fitted: {result.x}")

# Global optimization
result = optimize.differential_evolution(
    rosenbrock, bounds=[(-5, 5), (-5, 5)]
)
print(f"Global minimum: {result.x}")
```

---

## Summary

| Method | When to Use |
|--------|-------------|
| `Nelder-Mead` | Derivative-free, robust but slow |
| `BFGS` | With gradient information |
| `L-BFGS-B` | With bounds constraints |
| `SLSQP` | With equality/inequality constraints |
| `least_squares` | Least-squares problems |
| `differential_evolution` | Global optimization |
