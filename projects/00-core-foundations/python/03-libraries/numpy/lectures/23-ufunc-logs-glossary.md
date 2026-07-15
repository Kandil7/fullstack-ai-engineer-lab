# Glossary: Logarithmic and Exponential Ufuncs (Lecture 23)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| log() | `np.log(arr)` | Natural logarithm (base e) |
| log2() | `np.log2(arr)` | Base-2 logarithm |
| log10() | `np.log10(arr)` | Base-10 logarithm |
| log1p() | `np.log1p(arr)` | log(1+x) for small x |
| exp() | `np.exp(arr)` | e^x |
| exp2() | `np.exp2(arr)` | 2^x |
| expm1() | `np.expm1(arr)` | exp(x)-1 for small x |
| power() | `np.power(x, n)` | x^n |
| square() | `np.square(arr)` | x^2 |
| sqrt() | `np.sqrt(arr)` | √x |
| cbrt() | `np.cbrt(arr)` | ∛x |
| Entropy | `-sum(p*log2(p))` | Information content |
| Decibels | `10*log10(ratio)` | Signal strength |

---

## Detailed Definitions

### Base

**Definition:** The number that is raised to a power in exponential expressions. Different logarithmic functions use different bases.

**Example:**
```python
import numpy as np

# Different bases
print("log base e:", np.log(np.e))      # 1.0
print("log base 2:", np.log2(2))        # 1.0
print("log base 10:", np.log10(10))     # 1.0
```

**Related Terms:** Natural Logarithm, Common Logarithm

---

### Common Logarithm

**Definition:** Logarithm with base 10. Calculated using `np.log10()`. Used in decibels, pH scale, and scientific notation.

**Example:**
```python
import numpy as np

print("log10(100):", np.log10(100))     # 2.0
print("log10(1000):", np.log10(1000))   # 3.0

# Decibels
power_ratio = 100
db = 10 * np.log10(power_ratio)
print(f"{power_ratio}x power = {db} dB")
```

**Related Terms:** Natural Logarithm, Binary Logarithm

---

### Compound Growth

**Definition:** Growth that occurs when gains are added to the principal, creating exponential growth. Calculated using e^(rate × time).

**Example:**
```python
import numpy as np

principal = 1000
rate = 0.05
years = np.array([1, 5, 10, 20])

# Continuous compounding
future_value = principal * np.exp(rate * years)
print("Continuous compounding:")
for t, fv in zip(years, future_value):
    print(f"  {t} years: ${fv:.2f}")
```

**Related Terms:** exp(), Continuous Compounding

---

### Continuous Compounding

**Definition:** The mathematical limit of compound interest as the compounding frequency approaches infinity. Formula: A = Pe^(rt).

**Example:**
```python
import numpy as np

P = 10000  # Principal
r = 0.05   # Annual rate
t = 10     # Years

A = P * np.exp(r * t)
print(f"${P} at {r:.0%} for {t} years = ${A:.2f}")
```

**Related Terms:** exp(), Compound Growth

---

### Entropy

**Definition:** A measure of information content or uncertainty in a probability distribution. Calculated as -sum(p * log2(p)).

**Example:**
```python
import numpy as np

def shannon_entropy(probs):
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))

# Uniform distribution (maximum entropy)
uniform = np.array([0.25, 0.25, 0.25, 0.25])
print(f"Uniform entropy: {shannon_entropy(uniform):.4f} bits")  # 2.0

# Skewed distribution
skewed = np.array([0.9, 0.05, 0.03, 0.02])
print(f"Skewed entropy: {shannon_entropy(skewed):.4f} bits")    # ~1.0
```

**Related Terms:** log2(), Information Theory

---

### Exponential Function

**Definition:** The function e^x, where e is Euler's number (≈2.71828). Inverse of the natural logarithm.

**Example:**
```python
import numpy as np

arr = np.array([0, 1, 2, 3, 4])
print("exp(x):", np.exp(arr))
# Output: [ 1.     2.718  7.389 20.086 54.598]
```

**Related Terms:** log(), exp2(), expm1()

---

### expm1()

**Definition:** Calculates exp(x) - 1 with better numerical precision for small x values.

**Example:**
```python
import numpy as np

x = 1e-10
print("exp(x) - 1:", np.exp(x) - 1)  # May be 0.0
print("expm1(x):", np.expm1(x))      # More accurate
```

**Related Terms:** exp(), log1p()

---

### Information Theory

**Definition:** A mathematical framework for quantifying information, uncertainty, and communication. Key concept: Shannon entropy.

**Example:**
```python
import numpy as np

# Shannon entropy in bits
probs = np.array([0.5, 0.5])  # Fair coin
entropy = -np.sum(probs * np.log2(probs))
print(f"Fair coin entropy: {entropy} bits")  # 1.0
```

**Related Terms:** Entropy, log2()

---

### log1p()

**Definition:** Calculates log(1 + x) with better numerical precision for small x values.

**Example:**
```python
import numpy as np

x = 1e-10
print("log(1 + x):", np.log(1 + x))  # May be 0.0
print("log1p(x):", np.log1p(x))      # More accurate
```

**Related Terms:** log(), expm1()

---

### Natural Logarithm

**Definition:** Logarithm with base e (Euler's number ≈2.71828). Most common in mathematics and calculus.

**Example:**
```python
import numpy as np

print("ln(e):", np.log(np.e))    # 1.0
print("ln(1):", np.log(1))       # 0.0
print("ln(10):", np.log(10))     # 2.303
```

**Related Terms:** log2(), log10(), exp()

---

### Numerical Stability

**Definition:** The property of an algorithm to produce accurate results despite floating-point arithmetic limitations. Important for values near zero.

**Example:**
```python
import numpy as np

x = 1e-15

# Unstable
result1 = np.log(1 + x)  # Loses precision

# Stable
result2 = np.log1p(x)    # Preserves precision
```

**Related Terms:** log1p(), expm1()

---

### Power Function

**Definition:** Raises each element to a specified power. `np.power(x, n)` computes x^n.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print("x^2:", np.power(arr, 2))
print("x^3:", np.power(arr, 3))
print("x^0.5:", np.power(arr, 0.5))
```

**Related Terms:** sqrt(), square()

---

### Square Root

**Definition:** Calculates the square root of each element. Equivalent to raising to power 0.5.

**Example:**
```python
import numpy as np

arr = np.array([1, 4, 9, 16, 25])
print("sqrt:", np.sqrt(arr))
# Output: [1. 2. 3. 4. 5.]
```

**Related Terms:** cbrt(), power()

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| Base | Number raised to power | e, 2, 10 |
| Common Logarithm | log base 10 | `np.log10(100)` → 2.0 |
| Compound Growth | Exponential growth | `P * e^(rt)` |
| Continuous Compounding | Limit of compound interest | `np.exp(r*t)` |
| Entropy | Information content | `-sum(p*log2(p))` |
| Exponential Function | e^x calculation | `np.exp(arr)` |
| expm1() | exp(x)-1 accurately | `np.expm1(x)` |
| Information Theory | Quantifying information | Shannon entropy |
| log1p() | log(1+x) accurately | `np.log1p(x)` |
| Natural Logarithm | log base e | `np.log(arr)` |
| Numerical Stability | Accuracy preservation | Use log1p for small x |
| Power Function | x^n calculation | `np.power(arr, 2)` |
| Square Root | √x calculation | `np.sqrt(arr)` |

---

**Back to Lecture:** [23 - Logarithmic Ufuncs](23-ufunc-logs-lecture.md)
