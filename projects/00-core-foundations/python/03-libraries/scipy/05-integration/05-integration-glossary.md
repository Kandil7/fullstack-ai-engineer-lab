# SciPy Lecture 05: Numerical Integration — Glossary

| Term | Definition | Example |
|------|-----------|---------|
| Quadrature | Numerical integration | `integrate.quad(f, a, b)` |
| Definite Integral | Area under curve | ∫f(x)dx |
| ODE | Ordinary Differential Equation | `dy/dt = f(t, y)` |
| `quad()` | 1D adaptive quadrature | `quad(func, a, b)` |
| `dblquad()` | 2D integration | `dblquad(f, x_low, x_high, y_low, y_high)` |
| `nquad()` | N-D integration | `nquad(f, ranges)` |
| `trapz()` | Trapezoidal rule | `trapz(y, x)` |
| `simps()` | Simpson's rule | `simps(y, x)` |
| `solve_ivp()` | ODE solver | `solve_ivp(f, t_span, y0)` |
| RK45 | Runge-Kutta 4(5) method | `method='RK45'` |

### Integration Methods

| Method | Accuracy | Use Case |
|--------|----------|----------|
| `quad()` | High | Analytic functions |
| `trapz()` | Low | Sampled data |
| `simps()` | Medium | Smoother sampled data |
| `solve_ivp()` | Variable | Initial value problems |
