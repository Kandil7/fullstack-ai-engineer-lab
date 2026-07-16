# SciPy Lecture 07: Optimization — Glossary

| Term | Definition | Example |
|------|-----------|---------|
| Optimization | Minimizing/maximizing a function | `minimize(fun, x0)` |
| Constraint | Restriction on variables | `bounds=[(0, None)]` |
| Global Optimum | Best solution over all space | `differential_evolution()` |
| Local Optimum | Best in a neighborhood | `minimize()` may find local |
| Gradient | Derivative (slope) information | Used by BFGS method |
| `minimize_scalar()` | 1D optimization | `minimize_scalar(f)` |
| `least_squares()` | Nonlinear least squares | `least_squares(residuals, x0)` |
| `differential_evolution()` | Global optimizer | Stochastically samples space |

### Method Selection

| Method | Requires | When to Use |
|--------|----------|-------------|
| Nelder-Mead | None | Simple, derivative-free |
| BFGS | Gradient | Smooth, unconstrained |
| L-BFGS-B | Gradient | Large problems with bounds |
| SLSQP | Jacobian | General constrained |
| differential_evolution | Bounds | Global optimization |
