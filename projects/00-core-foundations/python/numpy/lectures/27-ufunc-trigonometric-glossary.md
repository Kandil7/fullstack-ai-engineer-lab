# Glossary: Trigonometric Ufuncs (Lecture 27)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| sin() | `np.sin(arr)` | Sine (radians) |
| cos() | `np.cos(arr)` | Cosine (radians) |
| tan() | `np.tan(arr)` | Tangent (radians) |
| arcsin() | `np.arcsin(arr)` | Inverse sine |
| arccos() | `np.arccos(arr)` | Inverse cosine |
| arctan() | `np.arctan(arr)` | Inverse tangent |
| arctan2() | `np.arctan2(y, x)` | Quadrant-aware arctan |
| radians() | `np.radians(arr)` | Degrees to radians |
| degrees() | `np.degrees(arr)` | Radians to degrees |
| sinh() | `np.sinh(arr)` | Hyperbolic sine |
| cosh() | `np.cosh(arr)` | Hyperbolic cosine |
| tanh() | `np.tanh(arr)` | Hyperbolic tangent |

---

## Detailed Definitions

### arccos()

**Definition:** Inverse cosine function. Returns the angle whose cosine is the given value. Output range: [0, π].

**Example:**
```python
import numpy as np

values = np.array([0, 0.5, 1])
angles = np.arccos(values)
print("arccos:", np.degrees(angles))
# Output: [90. 60.  0.]
```

**Related Terms:** arcsin(), arctan()

---

### arcsin()

**Definition:** Inverse sine function. Returns the angle whose sine is the given value. Input must be in [-1, 1]. Output range: [-π/2, π/2].

**Example:**
```python
import numpy as np

values = np.array([-1, -0.5, 0, 0.5, 1])
angles = np.arcsin(values)
print("arcsin:", np.degrees(angles).round(2))
# Output: [-90. -30.   0.  30.  90.]
```

**Related Terms:** arccos(), arctan()

---

### arctan()

**Definition:** Inverse tangent function. Returns the angle whose tangent is the given value. Output range: (-π/2, π/2).

**Example:**
```python
import numpy as np

values = np.array([-10, -1, 0, 1, 10])
angles = np.arctan(values)
print("arctan:", np.degrees(angles).round(2))
```

**Related Terms:** arctan2(), tan()

---

### arctan2()

**Definition:** Quadrant-aware inverse tangent. Takes y and x coordinates separately and returns the correct angle for all quadrants. Output range: (-π, π].

**Example:**
```python
import numpy as np

y = np.array([1, 1, -1, -1])
x = np.array([1, -1, -1, 1])
angles = np.arctan2(y, x)
print("arctan2:", np.degrees(angles))
# Output: [ 45. -45. -135.  135.]
```

**Related Terms:** arctan(), atan2

---

### cos()

**Definition:** Cosine function. Returns the cosine of an angle (in radians). Output range: [-1, 1].

**Example:**
```python
import numpy as np

angles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
print("cos:", np.cos(angles).round(4))
# Output: [1.     0.8661 0.7071 0.5    0.    ]
```

**Related Terms:** sin(), tan(), cosh()

---

### degrees()

**Definition:** Converts angles from radians to degrees.

**Example:**
```python
import numpy as np

radians = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
degrees = np.degrees(radians)
print("Degrees:", degrees.round(2))
# Output: [ 0.  30.  45.  60.  90.]
```

**Related Terms:** radians(), rad2deg()

---

### Hyperbolic Functions

**Definition:** Functions analogous to trigonometric functions but for hyperbolas. Include sinh, cosh, tanh and their inverses.

**Example:**
```python
import numpy as np

values = np.array([-2, -1, 0, 1, 2])
print("sinh:", np.sinh(values).round(4))
print("cosh:", np.cosh(values).round(4))
print("tanh:", np.tanh(values).round(4))
```

**Related Terms:** Trigonometric Functions, Exponential

---

### Phase

**Definition:** The offset of a periodic function from its standard position. Measured in radians or degrees.

**Example:**
```python
import numpy as np

t = np.linspace(0, 2*np.pi, 100)
phase = np.pi / 4  # 45 degrees
wave = np.sin(t + phase)

print(f"Phase: {np.degrees(phase):.0f}°")
print(f"Wave shifted by: {phase:.2f} radians")
```

**Related Terms:** Frequency, Amplitude

---

### radians()

**Definition:** Converts angles from degrees to radians.

**Example:**
```python
import numpy as np

degrees = np.array([0, 30, 45, 60, 90])
radians = np.radians(degrees)
print("Radians:", radians.round(4))
```

**Related Terms:** degrees(), deg2rad()

---

### sin()

**Definition:** Sine function. Returns the sine of an angle (in radians). Output range: [-1, 1].

**Example:**
```python
import numpy as np

angles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
print("sin:", np.sin(angles).round(4))
# Output: [0.     0.5    0.7071 0.866  1.    ]
```

**Related Terms:** cos(), tan(), sinh()

---

### tan()

**Definition:** Tangent function. Returns the tangent of an angle (in radians). Undefined at π/2 + nπ.

**Example:**
```python
import numpy as np

angles = np.array([0, np.pi/6, np.pi/4, np.pi/3])
print("tan:", np.tan(angles).round(4))
# Output: [0.     0.5774 1.     1.7321]
```

**Related Terms:** sin(), cos(), tanh()

---

### Trigonometric Identity

**Definition:** Mathematical equations involving trigonometric functions that are true for all values. Key identity: sin²(x) + cos²(x) = 1.

**Example:**
```python
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
identity = np.sin(x)**2 + np.cos(x)**2
print("sin² + cos²:", identity.round(10))  # All 1.0
```

**Related Terms:** sin(), cos(), Pythagorean Identity

---

### Unit Circle

**Definition:** A circle with radius 1 centered at the origin. Used to define trigonometric functions.

**Example:**
```python
import numpy as np

# Points on unit circle
theta = np.linspace(0, 2*np.pi, 8, endpoint=False)
x = np.cos(theta)
y = np.sin(theta)

# Verify radius = 1
radii = np.sqrt(x**2 + y**2)
print("Radii:", radii.round(10))  # All 1.0
```

**Related Terms:** sin(), cos(), Radian

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| arccos() | Inverse cosine | `np.arccos(0.5)` → 60° |
| arcsin() | Inverse sine | `np.arcsin(0.5)` → 30° |
| arctan() | Inverse tangent | `np.arctan(1)` → 45° |
| arctan2() | Quadrant-aware arctan | `np.arctan2(y, x)` |
| cos() | Cosine function | `np.cos(np.pi/3)` → 0.5 |
| degrees() | Convert to degrees | `np.degrees(np.pi)` → 180 |
| Hyperbolic | sinh, cosh, tanh | `np.sinh(1)` |
| Phase | Periodic offset | Wave shift |
| radians() | Convert to radians | `np.radians(90)` → π/2 |
| sin() | Sine function | `np.sin(np.pi/6)` → 0.5 |
| tan() | Tangent function | `np.tan(np.pi/4)` → 1.0 |
| Trig Identity | Mathematical rule | sin²+cos²=1 |
| Unit Circle | Radius 1 circle | cos²+sin²=1 |

---

**Back to Lecture:** [27 - Trigonometric Ufuncs](27-ufunc-trigonometric-lecture.md)
