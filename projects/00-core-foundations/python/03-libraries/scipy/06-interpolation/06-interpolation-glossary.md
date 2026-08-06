# SciPy Lecture 06: Interpolation — Glossary

| Term | Definition | Example |
|------|-----------|---------|
| Interpolation | Estimating between known points | `interp1d(x, y, kind='cubic')` |
| Spline | Piecewise polynomial curve | `splrep(x, y, s=0)` |
| B-Spline | Basis spline representation | `(t, c, k)` tuple |
| `interp1d()` | 1D interpolation function | `f = interp1d(x, y)` |
| `splrep()` | B-spline representation | `splrep(x, y)` |
| `splev()` | Evaluate B-spline | `splev(x_new, tck)` |
| `splint()` | Integrate B-spline | `splint(a, b, tck)` |
| `griddata()` | N-D scattered interpolation | `griddata(points, values, xi)` |
| `RBFInterpolator` | Radial basis function | `RBFInterpolator(points, values)` |
| Extrapolation | Estimating beyond known range | `fill_value='extrapolate'` |

### Interpolation Kinds

| kind | Smoothness | Use When |
|------|-----------|----------|
| `linear` | C⁰ | Quick, simple |
| `quadratic` | C¹ | Smooth enough |
| `cubic` | C² | Requires smoothness |
| `nearest` | C⁻¹ | Categorical data |
