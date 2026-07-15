# Glossary: Introduction to Random Numbers in NumPy (Lecture 16)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| random() | `np.random.random(n)` | Random float in [0, 1) |
| rand() | `np.random.rand(n)` | Random float in [0, 1) (legacy) |
| randint() | `np.random.randint(low, high, n)` | Random integer in [low, high) |
| randn() | `np.random.randn(n)` | Standard normal distribution |
| normal() | `np.random.normal(μ, σ, n)` | Custom normal distribution |
| uniform() | `np.random.uniform(low, high, n)` | Uniform distribution |
| seed() | `np.random.seed(s)` | Set seed for reproducibility |
| RandomState() | `np.random.RandomState(s)` | Independent random stream |
| default_rng() | `np.random.default_rng(s)` | Modern Generator API |
| choice() | `np.random.choice(arr, n)` | Random selection from array |

---

## Detailed Definitions

### choice()

**Definition:** Randomly selects elements from a 1D array. Can sample with or without replacement, and supports weighted probabilities.

**Example:**
```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Single random choice
single = np.random.choice(arr)
print("Single:", single)

# Multiple choices with replacement
with_replace = np.random.choice(arr, size=10, replace=True)
print("With replacement:", with_replace)

# Without replacement (unique selections)
without_replace = np.random.choice(arr, size=3, replace=False)
print("Without replacement:", without_replace)

# Weighted selection
weights = [0.1, 0.1, 0.1, 0.1, 0.6]
weighted = np.random.choice(arr, size=10, p=weights)
print("Weighted:", weighted)
```

**Related Terms:** randint(), RandomState, seed()

---

### default_rng()

**Definition:** Creates a new instance of NumPy's modern random number Generator. Recommended approach for new code. Returns a Generator object with methods for generating random numbers.

**Example:**
```python
import numpy as np

# Create Generator with seed
rng = np.random.default_rng(42)

# Generate random numbers
arr = rng.random(10)
print("Random:", arr)

# Random integers
ints = rng.integers(0, 100, size=10)
print("Integers:", ints)

# Normal distribution
normal = rng.normal(0, 1, size=10)
print("Normal:", normal)
```

**Related Terms:** RandomState, seed()

---

### Normal Distribution

**Definition:** A probability distribution that is symmetric about the mean, showing that data near the mean are more frequent in occurrence than data far from the mean. Also called Gaussian distribution or bell curve.

**Example:**
```python
import numpy as np

# Standard normal (mean=0, std=1)
standard = np.random.randn(10000)
print(f"Standard normal:")
print(f"  Mean: {standard.mean():.4f}")  # ~0
print(f"  Std: {standard.std():.4f}")    # ~1

# Custom normal
custom = np.random.normal(100, 15, size=10000)
print(f"\nCustom normal (μ=100, σ=15):")
print(f"  Mean: {custom.mean():.4f}")  # ~100
print(f"  Std: {custom.std():.4f}")    # ~15
```

**Related Terms:** randn(), normal(), Standard Deviation, Mean

---

### rand()

**Definition:** Legacy function that returns random floats in [0, 1). Accepts shape arguments. Part of the older random API.

**Example:**
```python
import numpy as np

# Single random float
r = np.random.rand()
print("Single:", r)

# Array of random floats
arr = np.random.rand(5)
print("Array:", arr)

# 2D array
arr2d = np.random.rand(3, 3)
print("2D:\n", arr2d)
```

**Related Terms:** random(), uniform(), RandomState

---

### randint()

**Definition:** Returns random integers from a discrete uniform distribution in the range [low, high). High value is exclusive.

**Example:**
```python
import numpy as np

# Single integer
r = np.random.randint(0, 10)
print("Single:", r)

# Array of integers
arr = np.random.randint(0, 100, size=10)
print("Array:", arr)

# 2D array
arr2d = np.random.randint(1, 10, size=(3, 4))
print("2D:\n", arr2d)

# With dtype
arr8 = np.random.randint(0, 10, size=5, dtype=np.int8)
print("int8:", arr8)
```

**Related Terms:** choice(), uniform()

---

### randn()

**Definition:** Legacy function that returns samples from the standard normal distribution (mean=0, std=1). Part of the older random API.

**Example:**
```python
import numpy as np

# Single sample
r = np.random.randn()
print("Single:", r)

# Array of samples
arr = np.random.randn(5)
print("Array:", arr)

# 2D array
arr2d = np.random.randn(3, 3)
print("2D:\n", arr2d)

# Transform to custom normal
custom = np.random.randn(1000) * 10 + 50
print(f"Custom (μ=50, σ=10): mean={custom.mean():.1f}")
```

**Related Terms:** normal(), Normal Distribution

---

### random()

**Definition:** Returns random floats in the half-open interval [0.0, 1.0). Part of both legacy and modern APIs.

**Example:**
```python
import numpy as np

# Legacy API
r = np.random.random()
print("Legacy:", r)

arr = np.random.random(5)
print("Legacy array:", arr)

# Modern API
rng = np.random.default_rng(42)
r = rng.random()
print("Modern:", r)

arr = rng.random(5)
print("Modern array:", arr)
```

**Related Terms:** rand(), uniform(), default_rng()

---

### RandomState

**Definition:** Container for the Mersenne Twister pseudo-random number generator. Creates independent random streams that don't affect the global state.

**Example:**
```python
import numpy as np

# Create independent RandomState objects
rng1 = np.random.RandomState(42)
rng2 = np.random.RandomState(42)

# Each produces the same sequence (with same seed)
print("rng1:", rng1.random(3))
print("rng2:", rng2.random(3))  # Same as rng1!

# Different seed = different sequence
rng3 = np.random.RandomState(123)
print("rng3:", rng3.random(3))  # Different!
```

**Related Terms:** seed(), default_rng(), Generator

---

### Reproducibility

**Definition:** The ability to generate the same sequence of random numbers given the same seed. Essential for debugging, testing, and scientific research.

**Example:**
```python
import numpy as np

# Without seed - not reproducible
print("Without seed:")
print("  Run 1:", np.random.random(3))
print("  Run 2:", np.random.random(3))  # Different!

# With seed - reproducible
np.random.seed(42)
print("\nWith seed 42:")
print("  Run 1:", np.random.random(3))

np.random.seed(42)
print("  Run 2:", np.random.random(3))  # Same!
```

**Related Terms:** seed(), RandomState, default_rng()

---

### Seed

**Definition:** An initial value used to initialize a pseudo-random number generator. Same seed produces the same sequence of random numbers.

**Example:**
```python
import numpy as np

# Set seed
np.random.seed(42)
arr1 = np.random.random(5)
print("Seed 42:", arr1)

# Reset seed - same sequence
np.random.seed(42)
arr2 = np.random.random(5)
print("Seed 42 again:", arr2)
print("Equal:", np.array_equal(arr1, arr2))

# Modern API
rng = np.random.default_rng(42)
arr3 = rng.random(5)
print("Generator:", arr3)
```

**Related Terms:** Reproducibility, RandomState, default_rng()

---

### Uniform Distribution

**Definition:** A probability distribution where all values in a range are equally likely to occur.

**Example:**
```python
import numpy as np

# Uniform between 0 and 1
uniform = np.random.uniform(0, 1, size=1000)
print(f"Uniform [0,1]:")
print(f"  Mean: {uniform.mean():.4f}")  # ~0.5
print(f"  Std: {uniform.std():.4f}")    # ~0.29

# Uniform between custom range
custom = np.random.uniform(10, 20, size=1000)
print(f"\nUniform [10,20]:")
print(f"  Mean: {custom.mean():.4f}")  # ~15
print(f"  Std: {custom.std():.4f}")    # ~2.89
```

**Related Terms:** random(), rand(), Normal Distribution

---

### Weighted Selection

**Definition:** Random selection where different elements have different probabilities of being chosen.

**Example:**
```python
import numpy as np

categories = np.array(["A", "B", "C", "D"])
weights = np.array([0.1, 0.2, 0.3, 0.4])

# Weighted selection
np.random.seed(42)
selected = np.random.choice(categories, size=100, p=weights)

# Count occurrences
unique, counts = np.unique(selected, return_counts=True)
print("Distribution:")
for cat, count in zip(unique, counts):
    print(f"  {cat}: {count} ({count}%)")
```

**Related Terms:** choice(), probabilities

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| choice() | Random selection from array | `np.random.choice(arr, 5)` |
| default_rng() | Modern Generator API | `rng = np.random.default_rng(42)` |
| Normal Distribution | Bell-shaped probability curve | `np.random.normal(0, 1, 1000)` |
| rand() | Legacy random float generator | `np.random.rand(5)` |
| randint() | Random integer generator | `np.random.randint(0, 10, 5)` |
| randn() | Standard normal generator | `np.random.randn(5)` |
| random() | Random float in [0, 1) | `np.random.random(5)` |
| RandomState | Independent random stream | `np.random.RandomState(42)` |
| Reproducibility | Same seed = same sequence | `np.random.seed(42)` |
| Seed | Initial value for RNG | `np.random.seed(42)` |
| Uniform Distribution | Equal probability across range | `np.random.uniform(0, 1, 1000)` |
| Weighted Selection | Probabilities for each element | `np.random.choice(arr, p=weights)` |

---

**Back to Lecture:** [16 - Random Introduction](16-random-intro-lecture.md)
