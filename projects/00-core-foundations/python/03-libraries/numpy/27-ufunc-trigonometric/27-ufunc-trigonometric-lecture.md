# Lecture 27: Trigonometric Ufuncs in NumPy

## Topic Overview

Trigonometric functions are essential for mathematics, physics, engineering, and signal processing. NumPy provides comprehensive support for sine, cosine, tangent, their inverses, and hyperbolic variants. This lecture covers working with angles in radians and degrees, inverse trigonometric functions, hyperbolic functions, and practical applications like wave generation and coordinate transformations.

Understanding trigonometric functions is crucial for any work involving periodic phenomena, rotations, or spatial calculations.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `np.sin()`, `np.cos()`, `np.tan()` for basic trigonometric operations
2. Convert between degrees and radians using `np.radians()` and `np.degrees()`
3. Use inverse trigonometric functions: `np.arcsin()`, `np.arccos()`, `np.arctan()`
4. Use `np.arctan2()` for quadrant-aware arctangent
5. Apply hyperbolic functions: `np.sinh()`, `np.cosh()`, `np.tanh()`
6. Generate sine and cosine waves
7. Calculate distances using trigonometry
8. Work with unit circle coordinates
9. Understand the relationship between trig and hyperbolic functions
10. Apply trigonometric functions to practical scenarios

---

## Key Concepts

### 1. Basic Trig Functions

```python
import numpy as np

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
```

**Key points:**
- All trig functions work with radians by default
- Results are floating-point numbers
- Can operate on single values or arrays

### 2. Degree/Radian Conversion

```python
import numpy as np

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
```

### 3. Inverse Trigonometric Functions

```python
import numpy as np

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
```

### 4. Hyperbolic Functions

```python
import numpy as np

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
```

### 5. Practical Applications

```python
import numpy as np

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
```

---

## Code Examples with Explanations

### Example 1: Unit Circle Coordinates

```python
import numpy as np

# Generate points around the unit circle
n_points = 12
angles = np.linspace(0, 2 * np.pi, n_points, endpoint=False)

x_coords = np.cos(angles)
y_coords = np.sin(angles)

print("Unit Circle Points:")
print("Angle | X | Y")
print("-" * 30)
for angle, x, y in zip(np.degrees(angles), x_coords, y_coords):
    print(f"{angle:5.0f}° | {x:6.3f} | {y:6.3f}")
```

### Example 2: Wave Generation

```python
import numpy as np

# Generate different waves
t = np.linspace(0, 2 * np.pi, 200)

# Sine wave
sine_wave = np.sin(t)

# Cosine wave
cosine_wave = np.cos(t)

# Combined wave (superposition)
combined = 0.5 * np.sin(t) + 0.3 * np.cos(2 * t)

print("Wave amplitudes:")
print(f"  Sine max: {sine_wave.max():.2f}")
print(f"  Cosine max: {cosine_wave.max():.2f}")
print(f"  Combined max: {combined.max():.2f}")
```

### Example 3: Coordinate Transformation

```python
import numpy as np

# Rotate points by angle theta
def rotate_points(x, y, theta_deg):
    theta_rad = np.radians(theta_deg)
    cos_t = np.cos(theta_rad)
    sin_t = np.sin(theta_rad)
    
    x_new = x * cos_t - y * sin_t
    y_new = x * sin_t + y * cos_t
    
    return x_new, y_new

# Original points
x = np.array([1, 0, -1, 0])
y = np.array([0, 1, 0, -1])

# Rotate 90 degrees
x_rot, y_rot = rotate_points(x, y, 90)

print("Original → Rotated 90°")
for xi, yi, xr, yr in zip(x, y, x_rot, y_rot):
    print(f"  ({xi}, {yi}) → ({xr:.1f}, {yr:.1f})")
```

### Example 4: Distance Calculation

```python
import numpy as np

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points on Earth using haversine formula."""
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # Earth radius in km
    r = 6371
    return r * c

# Calculate distances
cities = {
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Tokyo": (35.6762, 139.6503),
    "Sydney": (-33.8688, 151.2093)
}

print("Distance between cities (km):")
for city1, (lat1, lon1) in cities.items():
    for city2, (lat2, lon2) in cities.items():
        if city1 < city2:
            dist = haversine_distance(lat1, lon1, lat2, lon2)
            print(f"  {city1} → {city2}: {dist:.0f}")
```

### Example 5: Phase and Frequency Analysis

```python
import numpy as np

# Generate signal with multiple frequencies
t = np.linspace(0, 1, 1000)
f1, f2 = 5, 20  # Hz
signal = np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t)

# Calculate instantaneous phase using arctan2
analytic_signal = signal + 1j * np.gradient(signal)  # Hilbert transform approximation
inst_phase = np.unwrap(np.angle(analytic_signal))

print(f"Signal frequencies: {f1} Hz, {f2} Hz")
print(f"Signal length: {len(signal)} samples")
print(f"Phase range: {inst_phase.min():.2f} to {inst_phase.max():.2f} radians")
```

---

## Common Mistakes to Avoid

### Mistake 1: Using Degrees Instead of Radians

```python
import numpy as np

# WRONG - Treating degrees as radians
# result = np.sin(90)  # Not 1.0!

# CORRECT - Convert degrees to radians first
result = np.sin(np.radians(90))
print("sin(90°):", result)  # 1.0
```

### Mistake 2: Domain Errors with Inverse Functions

```python
import numpy as np

# WRONG - arcsin/arccos require input in [-1, 1]
# result = np.arcsin(2)  # nan!

# CORRECT - Ensure valid input range
values = np.array([-1, -0.5, 0, 0.5, 1])
print("arcsin:", np.arcsin(values))
```

### Mistake 3: Confusing arctan and arctan2

```python
import numpy as np

# arctan only considers ratio, not quadrant
print("arctan(1/-1):", np.arctan(1/-1))  # -0.785 (4th quadrant)

# arctan2 considers both x and y for correct quadrant
print("arctan2(1, -1):", np.arctan2(1, -1))  # 2.356 (2nd quadrant)
```

---

## Best Practices

### 1. Always Convert Degrees to Radians

```python
import numpy as np

def sin_degrees(angle_deg):
    """Calculate sine of angle in degrees."""
    return np.sin(np.radians(angle_deg))
```

### 2. Use arctan2 for Full Angle Range

```python
import numpy as np

# For atan2(y, x), y comes first!
angle = np.arctan2(y_coord, x_coord)
```

### 3. Verify with Known Values

```python
import numpy as np

# Test with known trig values
assert np.isclose(np.sin(np.pi/6), 0.5)
assert np.isclose(np.cos(np.pi/3), 0.5)
assert np.isclose(np.tan(np.pi/4), 1.0)
```

---

## Practice Exercises

### Exercise 1: Basic Trigonometry

```python
import numpy as np

# TODO: Calculate sin, cos, tan for 45 degrees
angle_deg = 45
angle_rad = np.radians(angle_deg)

sin_val = np.sin(angle_rad)
cos_val = np.cos(angle_rad)
tan_val = np.tan(angle_rad)

print(f"sin({angle_deg}°) = {sin_val:.4f}")
print(f"cos({angle_deg}°) = {cos_val:.4f}")
print(f"tan({angle_deg}°) = {tan_val:.4f}")
```

### Exercise 2: Unit Circle

```python
import numpy as np

# TODO: Generate 8 points on unit circle
angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
x = np.cos(angles)
y = np.sin(angles)

for angle, xi, yi in zip(np.degrees(angles), x, y):
    print(f"{angle:.0f}°: ({xi:.3f}, {yi:.3f})")
```

### Exercise 3: Wave Generation

```python
import numpy as np

# TODO: Generate sine wave
t = np.linspace(0, 2*np.pi, 100)
amplitude = 2
frequency = 3

wave = amplitude * np.sin(2 * np.pi * frequency * t)
print(f"Wave max: {wave.max():.2f}")
print(f"Wave min: {wave.min():.2f}")
```

---

## Summary

| Function | Description |
|----------|-------------|
| **np.sin()** | Sine function (radians) |
| **np.cos()** | Cosine function (radians) |
| **np.tan()** | Tangent function (radians) |
| **np.arcsin()** | Inverse sine |
| **np.arccos()** | Inverse cosine |
| **np.arctan()** | Inverse tangent |
| **np.arctan2()** | Quadrant-aware arctangent |
| **np.radians()** | Degrees to radians |
| **np.degrees()** | Radians to degrees |
| **np.sinh()** | Hyperbolic sine |
| **np.cosh()** | Hyperbolic cosine |
| **np.tanh()** | Hyperbolic tangent |

---

**Next Lecture:** [28 - Set Operations](28-ufunc-set-operations-lecture.md)
