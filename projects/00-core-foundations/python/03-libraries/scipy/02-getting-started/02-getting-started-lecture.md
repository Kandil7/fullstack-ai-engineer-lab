# SciPy Lecture 02: Getting Started with SciPy

## 🎯 Topic Overview

This lecture covers the fundamental workflow of using SciPy modules, understanding submodule imports, and the relationship between SciPy and NumPy.

## 📚 Learning Objectives

1. Import and use SciPy submodules correctly
2. Understand NumPy as the foundation
3. Use common SciPy constants and special functions

---

## 1. Importing SciPy Modules

```python
from scipy import optimize, integrate, stats, linalg, fft
from scipy.signal import find_peaks, convolve
from scipy.ndimage import gaussian_filter
from scipy.interpolate import interp1d

# Avoid: from scipy import *  (doesn't import submodules)
# Best practice: import exactly what you need
```

---

## 2. Constants and Special Functions

```python
from scipy import constants

# Physical constants
print(f"Speed of light: {constants.c} m/s")
print(f"Planck constant: {constants.h} J·s")
print(f"Gravitational constant: {constants.G} m³/kg/s²")
print(f"Avogadro number: {constants.N_A} mol⁻¹")
print(f"Boltzmann constant: {constants.k} J/K")
print(f"Electron mass: {constants.m_e} kg")

# Unit conversions
print(f"1 eV = {constants.eV} Joules")
print(f"1 atm = {constants.atm} Pascal")
print(f"1 parsec = {constants.parsec} meters")
```

---

## 3. Special Functions

```python
from scipy import special

# Bessel functions
print(f"J₀(1) = {special.jv(0, 1):.4f}")  # Bessel function of first kind
print(f"Y₀(1) = {special.yv(0, 1):.4f}")  # Bessel function of second kind

# Gamma function
print(f"Γ(5) = {special.gamma(5):.1f}")     # 4! = 24
print(f"Γ(0.5) = {special.gamma(0.5):.4f}")  # √π

# Error function
print(f"erf(1) = {special.erf(1):.4f}")
print(f"erfc(1) = {special.erfc(1):.4f}")

# Combinatorial
print(f"C(10, 3) = {special.comb(10, 3):.0f}")
print(f"P(10, 3) = {special.perm(10, 3):.0f}")
```

---

## Quick Reference

| Import Pattern | Description |
|---------------|-------------|
| `from scipy import optimize` | Full submodule |
| `from scipy.optimize import minimize` | Single function |
| `from scipy import constants` | Physical constants |
| `from scipy import special` | Special math functions |

> **Always import exactly what you need** — SciPy is large; don't import it entirely.
