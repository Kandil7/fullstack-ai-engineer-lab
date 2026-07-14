"""
01 - Introduction to SciPy
==========================
SciPy is a Python library built on top of NumPy that provides additional
functionality for scientific and technical computing. It includes modules
for optimization, integration, interpolation, linear algebra, statistics,
and more.

This module covers:
- What SciPy is and its ecosystem
- Key submodules overview
- Differences from NumPy
"""

import numpy as np

# ============================================================
# Example 1: SciPy vs NumPy — What SciPy Adds
# ============================================================
print("=" * 60)
print("Example 1: SciPy vs NumPy — Key Differences")
print("=" * 60)

from scipy import constants

# NumPy has basic math; SciPy adds scientific constants
print(f"Pi (from scipy.constants):      {constants.pi}")
print(f"Speed of light (m/s):           {constants.speed_of_light}")
print(f"Planck constant:                {constants.Planck}")
print(f"Elementary charge (C):          {constants.elementary_charge}")
print(f"Boltzmann constant (J/K):       {constants.Boltzmann}")

# Unit conversions built-in
print(f"\n1 inch in meters:               {constants.inch} m")
print(f"1 mile in meters:               {constants.mile} m")
print(f"0 degrees Celsius in Kelvin:    {constants.zero_Celsius} K")

# ============================================================
# Example 2: SciPy Submodule Tour
# ============================================================
print("\n" + "=" * 60)
print("Example 2: SciPy Submodule Tour")
print("=" * 60)

import scipy
print(f"SciPy version: {scipy.__version__}")

submodules = [
    "constants",  # Physical/mathematical constants
    "optimize",   # Optimization algorithms
    "integrate",  # Integration and ODE solvers
    "interpolate", # Interpolation tools
    "linalg",     # Linear algebra (beyond NumPy)
    "stats",      # Statistical distributions and tests
    "fft",        # Fourier transforms
    "signal",     # Signal processing
    "ndimage",    # N-dimensional image processing
    "spatial",    # Spatial data structures
    "io",         # File I/O for various formats
    "misc",       # Miscellaneous utilities
]

for mod in submodules:
    try:
        __import__(f"scipy.{mod}")
        print(f"  scipy.{mod:<14s} — loaded successfully")
    except Exception as e:
        print(f"  scipy.{mod:<14s} — error: {e}")

# ============================================================
# Example 3: Special Functions (scipy.special)
# ============================================================
print("\n" + "=" * 60)
print("Example 3: Special Mathematical Functions")
print("=" * 60)

from scipy import special

# Bessel functions
x = np.linspace(0, 20, 200)
j0 = special.jv(0, x)   # Bessel function of first kind, order 0
j1 = special.jv(1, x)   # Bessel function of first kind, order 1
y0 = special.yv(0, x)   # Bessel function of second kind, order 0

print(f"Bessel J0(1.0) = {special.jv(0, 1.0):.6f}")
print(f"Bessel J1(1.0) = {special.jv(1, 1.0):.6f}")
print(f"Bessel Y0(1.0) = {special.yv(0, 1.0):.6f}")

# Error function and related
print(f"\nError function erf(1.0)  = {special.erf(1.0):.6f}")
print(f"Complementary erf erfc(1.0) = {special.erfc(1.0):.6f}")
print(f"Inverse erf erfinv(0.5)  = {special.erfinv(0.5):.6f}")

# Gamma function
print(f"\nGamma(5) = {special.gamma(5):.1f}  (= 4! = 24)")
print(f"Gamma(0.5) = {special.gamma(0.5):.6f}  (= sqrt(pi))")
print(f"Log-gamma ln|Gamma(10)| = {special.gammaln(10):.4f}")

# ============================================================
# Example 4: Using SciPy Constants for Unit Conversion
# ============================================================
print("\n" + "=" * 60)
print("Example 4: Physical Constants & Unit Conversion")
print("=" * 60)

from scipy.constants import convert_temperature, electron_volt, eV

# Temperature conversions
temps_celsius = [0, 25, 100, 373.15]
temps_kelvin = convert_temperature(temps_celsius, "C", "K")
temps_fahr = convert_temperature(temps_celsius, "C", "F")

print("Temperature Conversion:")
print(f"  {'Celsius':>10s} {'Kelvin':>10s} {'Fahrenheit':>12s}")
print(f"  {'-'*10} {'-'*10} {'-'*12}")
for c, k, f in zip(temps_celsius, temps_kelvin, temps_fahr):
    print(f"  {c:10.2f} {k:10.2f} {f:12.2f}")

# Energy conversion
energy_joules = 1.0
energy_ev = convert_temperature(energy_joules, "J", "eV") if False else energy_joules / eV
print(f"\n1 Joule = {energy_ev:.4e} eV")
print(f"1 eV    = {eV:.4e} Joules")
print(f"Visible light (~2.5 eV) = {2.5 * eV:.4e} Joules")

# ============================================================
# Example 5: SciPy Integration with NumPy Arrays
# ============================================================
print("\n" + "=" * 60)
print("Example 5: SciPy + NumPy — Seamless Integration")
print("=" * 60)

from scipy import ndimage

# Create a 2D array and apply SciPy filters
np.random.seed(42)
data = np.random.rand(10, 10)
print(f"Original data shape: {data.shape}")
print(f"Original mean: {data.mean():.4f}")

# Gaussian filter (smoothing)
smoothed = ndimage.gaussian_filter(data, sigma=1.0)
print(f"After Gaussian filter (sigma=1): mean={smoothed.mean():.4f}")
print(f"  Std dev changed: {data.std():.4f} -> {smoothed.std():.4f}")

# Edge detection with Sobel filter
from scipy.ndimage import sobel
sobel_x = sobel(data, axis=0)
sobel_y = sobel(data, axis=1)
edge_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
print(f"Edge magnitude range: [{edge_magnitude.min():.4f}, {edge_magnitude.max():.4f}]")

print("\n[OK] SciPy provides powerful scientific tools that extend NumPy!")
print("     Next: 02-getting-started.py to install and start using SciPy.")
