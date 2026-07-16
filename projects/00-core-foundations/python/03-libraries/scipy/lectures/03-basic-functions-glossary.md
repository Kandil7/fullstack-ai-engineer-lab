# SciPy Lecture 03: Basic Functions — Glossary

| Term | Definition | Example |
|------|-----------|---------|
| Root Finding | Solving f(x) = 0 | `optimize.root_scalar(f, bracket=[a,b])` |
| Minimization | Finding function minimum | `optimize.minimize(f, x0)` |
| Curve Fitting | Fitting model to data | `optimize.curve_fit(model, x, y)` |
| Scalar Root | 1D root finder | `root_scalar()` |
| Multivariate Root | N-D root finder | `root()` |
| Nelder-Mead | Direct search optimization | `method='Nelder-Mead'` |
| BFGS | Quasi-Newton optimization | `method='BFGS'` |
| Least Squares | Minimize sum of squared residuals | `least_squares()` |
| Rosenbrock | Banana-shaped test function | `rosenbrock(x)` |
| `root_scalar()` | 1D root finding | `root_scalar(f, bracket=[a,b])` |
| `root()` | N-D root finding | `root(f, x0)` |
| `minimize()` | N-D optimization | `minimize(f, x0, method='BFGS')` |
| `curve_fit()` | Curve fitting | `curve_fit(model, xdata, ydata, p0)` |
