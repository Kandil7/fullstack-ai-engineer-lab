# SciPy Lecture 06: Interpolation

## 🎯 Topic Overview

Interpolation fills in missing data or creates smooth curves from discrete points. SciPy provides 1D, N-D, spline, and radial basis function interpolation.

## 📚 Learning Objectives

1. Perform 1D interpolation with `interp1d()`
2. Use spline interpolation with `splrep()`/`splev()`
3. Handle N-D interpolation with `griddata()`

---

## 1. 1D Interpolation

```python
import numpy as np
from scipy import interpolate

# Sparse data points
x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([0, 2, 1, 4, 3, 5])

# Create interpolation functions
f_linear = interpolate.interp1d(x, y, kind='linear')
f_cubic = interpolate.interp1d(x, y, kind='cubic')
f_quadratic = interpolate.interp1d(x, y, kind='quadratic')

# Query at new points
x_new = np.linspace(0, 5, 50)
y_linear = f_linear(x_new)
y_cubic = f_cubic(x_new)

print(f"Linear: y(2.5) = {f_linear(2.5):.3f}")
print(f"Cubic: y(2.5) = {f_cubic(2.5):.3f}")
```

### Interpolation Kinds

| Kind | Method | Smoothness |
|------|--------|-----------|
| `'linear'` | Linear segments | C⁰ |
| `'quadratic'` | Quadratic spline | C¹ |
| `'cubic'` | Cubic spline | C² |
| `'nearest'` | Nearest neighbor | C⁻¹ (discontinuous) |
| `'slinear'` | Linear on spline grid | C⁰ |

---

## 2. Spline Interpolation

```python
# Create spline (B-spline representation)
tck = interpolate.splrep(x, y, s=0)  # s=0: exact interpolation

# Evaluate spline
x_new = np.linspace(0, 5, 100)
y_spline = interpolate.splev(x_new, tck)

# Derivative
y_deriv = interpolate.splev(x_new, tck, der=1)
y_integral = interpolate.splint(0, 5, tck)

print(f"∫y dx from 0 to 5 = {y_integral:.3f}")

# Smoothing spline (with noise reduction)
tck_smooth = interpolate.splrep(x, y + np.random.normal(0, 0.1, len(x)), s=len(x))
```

---

## 3. Multi-Dimensional Interpolation

```python
# 2D scattered data interpolation
points = np.random.rand(50, 2) * 10
values = np.sin(points[:, 0]) * np.cos(points[:, 1])

# Grid for evaluation
grid_x, grid_y = np.meshgrid(np.linspace(0, 10, 50), 
                              np.linspace(0, 10, 50))

# Cubic interpolation
grid_z = interpolate.griddata(points, values, (grid_x, grid_y), 
                               method='cubic')
print(f"Interpolated grid shape: {grid_z.shape}")

# Radial basis function (RBF) interpolation
rbf = interpolate.RBFInterpolator(points, values, kernel='thin_plate_spline')
grid_z_rbf = rbf(np.column_stack([grid_x.ravel(), grid_y.ravel()]))
grid_z_rbf = grid_z_rbf.reshape(grid_z.shape)
```

---

## Summary

| Function | Purpose | Use Case |
|----------|---------|----------|
| `interp1d()` | 1D interpolation | Given x, y points |
| `splrep()`/`splev()` | B-spline | Smooth curve fitting |
| `splint()` | Spline integral | Area under spline |
| `griddata()` | N-D interpolation | Scattered data |
| `RBFInterpolator()` | RBF interpolation | Smooth N-D |
