# SciPy Lecture 01: Introduction to SciPy

## 🎯 Topic Overview

SciPy (Scientific Python) is a powerful library built on NumPy that provides advanced algorithms for scientific computing. It includes modules for optimization, integration, interpolation, linear algebra, signal processing, statistics, and more.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Understand SciPy's role in the scientific Python ecosystem
2. Install and import SciPy correctly
3. Navigate SciPy's module structure
4. Know which module to use for common scientific tasks

---

## 1. What is SciPy?

SciPy extends NumPy with higher-level scientific algorithms. While NumPy provides the array data structure and basic operations, SciPy provides algorithms that operate on those arrays.

### SciPy Module Structure

| Module | Description | Key Functions |
|--------|-------------|--------------|
| `scipy.optimize` | Optimization and root finding | `minimize()`, `curve_fit()`, `root()` |
| `scipy.integrate` | Numerical integration | `quad()`, `solve_ivp()`, `trapz()` |
| `scipy.interpolate` | Interpolation | `interp1d()`, `griddata()`, `splrep()` |
| `scipy.stats` | Statistical functions | `norm()`, `ttest_ind()`, `describe()` |
| `scipy.linalg` | Linear algebra | `solve()`, `eig()`, `svd()` |
| `scipy.fft` | Fourier transforms | `fft()`, `ifft()`, `fftfreq()` |
| `scipy.signal` | Signal processing | `convolve()`, `spectrogram()`, `butter()` |
| `scipy.sparse` | Sparse matrices | `csr_matrix()`, `linalg.spsolve()` |
| `scipy.spatial` | Spatial algorithms | `KDTree()`, `Delaunay()`, `Voronoi()` |
| `scipy.ndimage` | Image processing | `gaussian_filter()`, `zoom()`, `label()` |

---

## 2. Installation

```bash
pip install scipy
# or
conda install scipy

# Verify
import scipy
print(scipy.__version__)  # e.g., 1.14.0
print(scipy.__all__)      # List all submodules
```

---

## 3. Quick Tour — Common Tasks

```python
import numpy as np
from scipy import optimize, integrate, stats, linalg

# 1. Find minimum of a function
result = optimize.minimize(lambda x: x**2 + 10*np.sin(x), x0=0)
print(f"Minimum at x={result.x[0]:.3f}")

# 2. Integrate a function
area, error = integrate.quad(lambda x: np.exp(-x**2), -np.inf, np.inf)
print(f"∫exp(-x²)dx from -∞ to ∞ = {area:.4f}")

# 3. Statistical test
np.random.seed(42)
sample1 = np.random.normal(0, 1, 100)
sample2 = np.random.normal(0.5, 1, 100)
t_stat, p_value = stats.ttest_ind(sample1, sample2)
print(f"t-test: t={t_stat:.3f}, p={p_value:.4f}")

# 4. Solve linear system
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])
x = linalg.solve(A, b)
print(f"Solution: x={x}")
```

---

## Summary

SciPy turns NumPy arrays into a complete scientific computing environment. The key is knowing which module to use for your problem:
- **Optimize**: Find minima, fit curves, solve equations
- **Integrate**: Calculate areas under curves, solve ODEs
- **Stats**: Statistical tests, distributions, descriptive stats
- **Interpolate**: Fill in missing data, smooth curves
- **Linalg**: Matrix operations beyond NumPy's basics
- **FFT**: Frequency analysis of signals
- **Signal**: Filter and analyze time-series data
- **Sparse**: Work with large sparse matrices efficiently
