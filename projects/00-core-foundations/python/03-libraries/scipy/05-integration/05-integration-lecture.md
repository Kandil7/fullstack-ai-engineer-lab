# SciPy Lecture 05: Numerical Integration

## 🎯 Topic Overview

Numerical integration (quadrature) calculates definite integrals when analytical solutions are impossible. SciPy provides robust integration routines for 1D, 2D, and n-dimensional integrals, plus ordinary differential equation (ODE) solvers.

## 📚 Learning Objectives

1. Perform 1D integration with `quad()`
2. Compute 2D and n-D integrals with `dblquad()` and `nquad()`
3. Solve ODEs with `solve_ivp()`

---

## 1. One-Dimensional Integration

```python
import numpy as np
from scipy import integrate

# Define function
def f(x):
    return np.exp(-x**2)

# Gaussian integral: ∫exp(-x²)dx from -∞ to ∞ = √π
result, error = integrate.quad(f, -np.inf, np.inf)
print(f"∫exp(-x²)dx = {result:.6f} (expected: {np.sqrt(np.pi):.6f})")
print(f"Error estimate: {error:.2e}")

# With parameters
def g(x, a, b):
    return np.sin(a * x) * np.exp(-b * x)

result, error = integrate.quad(g, 0, np.inf, args=(2, 0.5))
print(f"∫sin(2x)exp(-0.5x)dx from 0 to ∞ = {result:.6f}")

# Discrete integration (trapezoidal)
x = np.linspace(0, 10, 100)
y = np.sin(x)
area = integrate.trapz(y, x)
print(f"∫sin(x)dx from 0 to 10 ≈ {area:.4f}")

# Simpson's rule
area = integrate.simps(y, x)
print(f"Simpson's rule: ∫sin(x)dx from 0 to 10 ≈ {area:.4f}")
```

---

## 2. Multi-Dimensional Integration

```python
# Double integral: ∫∫(x² + y²)dxdy over [0,1] × [0,1]
def f_2d(y, x):
    return x**2 + y**2

result, error = integrate.dblquad(f_2d, 0, 1, lambda x: 0, lambda x: 1)
print(f"∬(x²+y²)dxdy = {result:.6f}")

# n-dimensional integration
def f_nd(*args):
    return sum(arg**2 for arg in args)

result, error = integrate.nquad(f_nd, [(0, 1), (0, 1), (0, 1)])
print(f"∭(x²+y²+z²)dxdydz = {result:.6f}")
```

---

## 3. Ordinary Differential Equations

```python
# Solve: dy/dt = -2y, y(0) = 1  → solution: y(t) = exp(-2t)
def ode_func(t, y):
    return -2 * y

sol = integrate.solve_ivp(ode_func, [0, 5], [1], method='RK45', 
                          t_eval=np.linspace(0, 5, 100))
print(f"y(1) = {sol.y[0, -1]:.4f} (expected: {np.exp(-2*5):.4f})")

# Simple harmonic oscillator: d²x/dt² = -x
def harmonic(t, state):
    x, v = state
    return [v, -x]

sol = integrate.solve_ivp(harmonic, [0, 10], [1, 0], 
                          t_eval=np.linspace(0, 10, 100))
print(f"x(10) = {sol.y[0, -1]:.4f} (expected: {np.cos(10):.4f})")
```

---

## Summary

| Function | Purpose | Use Case |
|----------|---------|----------|
| `quad()` | 1D integration | ∫f(x)dx |
| `dblquad()` | 2D integration | ∬f(x,y)dxdy |
| `nquad()` | N-D integration | Multiple dimensions |
| `trapz()` | Discrete trapezoidal | Sampled data |
| `simps()` | Discrete Simpson's | Sampled data |
| `solve_ivp()` | ODE solver | Initial value problems |
