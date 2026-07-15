"""
Ufunc Trigonometric
W3Schools: https://www.w3schools.com/python/numpy_ufunc_trigonometric.asp

Trigonometric functions for array operations.
"""

import numpy as np

# ============================================================
# Example 1: Basic Trig Functions
# sin(), cos(), tan() work with radians.
# ============================================================

# Single values
print("sin(0):", np.sin(0))          # 0.0
print("cos(0):", np.cos(0))          # 1.0
print("tan(0):", np.tan(0))          # 0.0

# pi/2 (90 degrees)
print("\nsin(pi/2):", np.sin(np.pi/2))  # 1.0
print("cos(pi/2):", np.cos(np.pi/2))   # 6.12e-17 ≈ 0

# Arrays of angles (in radians)
angles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
print("\nAngles:", np.round(angles, 4))
print("sin:", np.sin(angles).round(4))
print("cos:", np.cos(angles).round(4))
print("tan:", np.tan(angles).round(4))
# Output:
# sin(0): 0.0
# cos(0): 1.0
# sin(pi/2): 1.0

# ============================================================
# Example 2: Degree/Radian Conversion
# Convert between degrees and radians.
# ============================================================

# Degrees to radians
degrees = np.array([0, 30, 45, 60, 90, 180, 270, 360])
radians = np.radians(degrees)
print("Degrees:", degrees)
print("Radians:", np.round(radians, 4))

# Radians to degrees
radians_back = np.degrees(radians)
print("Back to degrees:", radians_back)

# Trig functions with degrees
print("\nsin(30):", np.sin(np.radians(30)))    # 0.5
print("cos(60):", np.cos(np.radians(60)))      # 0.5
print("tan(45):", np.tan(np.radians(45)))      # 1.0

# Convert then calculate
angles_deg = np.array([0, 45, 90, 135, 180])
angles_rad = np.deg2rad(angles_deg)
print("\nDeg2rad:", np.round(angles_rad, 4))
print("Rad2deg:", np.rad2deg(angles_rad))
# Output:
# Degrees: [  0  30  45  60  90 180 270 360]
# Radians: [0.    0.524 0.785 1.047 1.571 3.142 4.712 6.283]

# ============================================================
# Example 3: Inverse Trigonometric Functions
# arcsin(), arccos(), arctan().
# ============================================================

# Values must be in [-1, 1] for arcsin and arccos
values = np.array([-1, -0.5, 0, 0.5, 1])

# Inverse sine
print("\narcsin:", np.arcsin(values).round(4))
print("arcsin degrees:", np.degrees(np.arcsin(values)).round(2))

# Inverse cosine
print("\narccos:", np.arccos(values).round(4))
print("arccos degrees:", np.degrees(np.arccos(values)).round(2))

# Inverse tangent (works for all real numbers)
x_values = np.array([-10, -1, 0, 1, 10])
print("\narctan:", np.arctan(x_values).round(4))
print("arctan degrees:", np.degrees(np.arctan(x_values)).round(2))

# arctan2 - quadrant-aware arctangent
y = np.array([1, 1, -1, -1])
x = np.array([1, -1, -1, 1])
print("\narctan2(y, x):", np.arctan2(y, x).round(4))
print("arctan2 degrees:", np.degrees(np.arctan2(y, x)).round(2))
# Output:
# arcsin: [-1.571 -0.524  0.     0.524  1.571]
# arctan: [-1.472 -0.785  0.     0.785  1.472]

# ============================================================
# Example 4: Hyperbolic Functions
# sinh(), cosh(), tanh() and their inverses.
# ============================================================

values = np.array([-2, -1, 0, 1, 2])

print("\nHyperbolic functions:")
print("sinh:", np.sinh(values).round(4))
print("cosh:", np.cosh(values).round(4))
print("tanh:", np.tanh(values).round(4))

print("\nInverse hyperbolic:")
print("arcsinh:", np.arcsinh(values).round(4))
print("arccosh:", np.arccosh(np.abs(values) + 1).round(4))  # Need |x| >= 1
print("arctanh:", np.arctanh(values / 2).round(4))  # Need |x| < 1

# Hyperbolic identities
x = 1.5
print(f"\nHyperbolic identity (x={x}):")
print(f"  cosh^2 - sinh^2 = {np.cosh(x)**2 - np.sinh(x)**2:.6f}")  # 1.0
# Output:
# Hyperbolic functions:
# sinh: [-3.6269 -1.1752  0.     1.1752  3.6269]
# cosh: [3.7622 1.5431 1.     1.5431 3.7622]
# tanh: [-0.964 -0.762  0.     0.762  0.964]

# ============================================================
# Example 5: Practical Applications
# Real-world trigonometric calculations.
# ============================================================

# Unit circle points
theta = np.linspace(0, 2 * np.pi, 8)
x = np.cos(theta)
y = np.sin(theta)
print("\nUnit circle points:")
for t, xi, yi in zip(np.degrees(theta), x.round(4), y.round(4)):
    print(f"  {t:.0f}°: ({xi}, {yi})")

# Wave generation
t = np.linspace(0, 2 * np.pi, 100)
frequency = 3  # Hz
amplitude = 5
phase = np.pi / 4
wave = amplitude * np.sin(2 * np.pi * frequency * t + phase)
print(f"\nWave: A*sin(2πft + φ)")
print(f"  A={frequency}, f={amplitude}, φ={np.degrees(phase):.0f}°")
print(f"  Max: {wave.max():.2f}, Min: {wave.min():.2f}")

# Distance between points (using trigonometry)
lat1, lon1 = np.radians(40.7128), np.radians(-74.0060)  # NYC
lat2, lon2 = np.radians(51.5074), np.radians(-0.1278)   # London

dlat = lat2 - lat1
dlon = lon2 - lon1
a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
c = 2 * np.arcsin(np.sqrt(a))
r = 6371  # Earth radius in km
distance = r * c
print(f"\nDistance NYC to London: {distance:.0f} km")
