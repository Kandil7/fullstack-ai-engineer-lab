# Lecture 16: Introduction to Random Numbers in NumPy

## Topic Overview

NumPy's random module provides a powerful suite of functions for generating random numbers, which are essential for simulations, statistical sampling, machine learning initialization, and testing. This lecture covers the fundamentals of random number generation in NumPy, including different distributions, seeding for reproducibility, and the modern Generator API.

Random numbers are fundamental to many areas of computing: Monte Carlo simulations, stochastic algorithms, data augmentation, and probabilistic models all rely on random number generation.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Generate random floating-point numbers using various methods
2. Generate random integers within specified ranges
3. Generate random numbers from normal (Gaussian) distributions
4. Use seeds for reproducible random number generation
5. Understand the difference between legacy and modern random APIs
6. Apply random number generation to practical use cases
7. Use `np.random.choice()` for random selection with and without replacement
8. Create weighted random selections
9. Generate random arrays of any shape
10. Apply random numbers to simulations and testing scenarios

---

## Key Concepts

### 1. Random Floating-Point Numbers

NumPy provides several ways to generate random floating-point numbers between 0 and 1.

```python
import numpy as np

# Single random float between 0 and 1
r = np.random.random()
print("Single random:", r)
# Output: e.g., 0.5488135039273248

# Array of random floats
arr = np.random.random(5)
print("Random array (5):", arr)
# Output: [0.715 0.603 0.545 0.424 0.646]

# 2D random array
arr_2d = np.random.random((3, 3))
print("Random 2D (3x3):\n", arr_2d)
```

**Key points:**
- `np.random.random()` or `np.random.rand()` returns float in [0.0, 1.0)
- Pass shape as argument for arrays
- Uniform distribution across the range

### 2. Random Integers

Generate random integers within a specified range.

```python
import numpy as np

# Single random integer [low, high)
r = np.random.randint(0, 100)
print("Random int [0,100):", r)

# Array of random integers
arr = np.random.randint(0, 50, size=10)
print("Random ints:", arr)

# 2D random integers
arr_2d = np.random.randint(1, 10, size=(3, 4))
print("Random 2D ints (1-9):\n", arr_2d)

# With specific dtype
arr_int8 = np.random.randint(0, 10, size=5, dtype=np.int8)
print("int8 random:", arr_int8)
```

**Key points:**
- `np.random.randint(low, high, size)` generates integers in [low, high)
- High value is exclusive (like Python's range)
- Can specify dtype for memory efficiency

### 3. Normal (Gaussian) Distribution

Generate numbers following a bell-shaped curve centered at the mean.

```python
import numpy as np

# Standard normal (mean=0, std=1)
r = np.random.randn()
print("Standard normal:", r)

arr_normal = np.random.randn(5)
print("Normal array:", arr_normal)

# Normal with custom mean and std
mean, std = 100, 15
arr_custom = np.random.normal(mean, std, size=1000)
print(f"Normal (mean={mean}, std={std}):")
print(f"  Sample mean: {arr_custom.mean():.2f}")
print(f"  Sample std: {arr_custom.std():.2f}")
print(f"  Min: {arr_custom.min():.2f}")
print(f"  Max: {arr_custom.max():.2f}")

# 2D normal distribution
arr_2d = np.random.randn(3, 3) * 10 + 50
print("2D normal (mean=50, std=10):\n", arr_2d.round(2))
```

**Key points:**
- `np.random.randn()` generates from standard normal (μ=0, σ=1)
- `np.random.normal(mean, std)` allows custom parameters
- About 68% of values within 1 std of mean
- About 95% within 2 std, 99.7% within 3 std

### 4. Random Seeds for Reproducibility

Seeds ensure the same random numbers are generated each time, essential for debugging and reproducible research.

```python
import numpy as np

# Without seed - different each time
print("Without seed:")
print("  Run 1:", np.random.rand(3))
print("  Run 2:", np.random.rand(3))

# With seed - same every time
np.random.seed(42)
print("\nWith seed 42:")
print("  Run 1:", np.random.rand(3))

np.random.seed(42)
print("  Run 2:", np.random.rand(3))  # Same as Run 1!

# RandomState for independent streams
rng1 = np.random.RandomState(42)
rng2 = np.random.RandomState(42)
print("\nRandomState(42):")
print("  rng1:", rng1.rand(3))
print("  rng2:", rng2.rand(3))  # Same as rng1!

# Modern Generator API (recommended)
rng = np.random.default_rng(42)
print("\nDefault Generator:")
print("  rng.random(3):", rng.random(3))
print("  rng.integers(0, 100, 5):", rng.integers(0, 100, 5))
print("  rng.normal(0, 1, 3):", rng.normal(0, 1, 3))
```

**Key points:**
- Set seed before generating random numbers
- Same seed → same sequence (reproducibility)
- `np.random.seed()` affects global state
- `RandomState` creates independent streams
- `default_rng()` is the modern, recommended approach

### 5. Uniform Distribution

Numbers are equally likely across a range.

```python
import numpy as np

# Uniform between 0 and 1
uniform = np.random.uniform(0, 1, size=1000)
print("Uniform distribution:")
print(f"  Mean: {uniform.mean():.4f}")    # ~0.5
print(f"  Std: {uniform.std():.4f}")      # ~0.29
print(f"  Min: {uniform.min():.4f}")      # ~0.00
print(f"  Max: {uniform.max():.4f}")      # ~1.00

# Uniform between custom range
uniform_custom = np.random.uniform(10, 20, size=1000)
print(f"\nUniform [10, 20):")
print(f"  Mean: {uniform_custom.mean():.4f}")  # ~15.0
print(f"  Std: {uniform_custom.std():.4f}")    # ~2.89
```

### 6. Practical Random Examples

```python
import numpy as np

# Simulate coin flips (0 or 1)
coin_flips = np.random.randint(0, 2, size=20)
print("20 coin flips:", coin_flips)
print("Heads:", np.sum(coin_flips == 1))
print("Tails:", np.sum(coin_flips == 0))

# Simulate dice rolls (1-6)
dice_rolls = np.random.randint(1, 7, size=30)
print("\n30 dice rolls:", dice_rolls)
print("Average:", dice_rolls.mean())

# Random selection from a list
choices = np.array(["red", "green", "blue", "yellow"])
selected = np.random.choice(choices, size=10)
print("\nRandom colors:", selected)

# Random without replacement (unique selections)
selected_unique = np.random.choice(choices, size=3, replace=False)
print("Unique colors:", selected_unique)

# Weighted random selection
weights = [0.1, 0.2, 0.3, 0.4]  # Blue most likely
selected_weighted = np.random.choice(choices, size=10, p=weights)
print("Weighted colors:", selected_weighted)
```

---

## Code Examples with Explanations

### Example 1: Basic Random Number Generation

```python
import numpy as np

# Generate different types of random numbers
print("=== Random Floats ===")
print("random():", np.random.random())        # [0, 1)
print("rand():", np.random.rand())            # [0, 1)
print("randf():", np.random.randf())          # [0, 1) - alias

print("\n=== Random Integers ===")
print("randint(0, 10):", np.random.randint(0, 10))     # [0, 10)
print("randint(1, 100):", np.random.randint(1, 100))   # [1, 100)

print("\n=== Random Normal ===")
print("randn():", np.random.randn())           # Standard normal
print("normal(0, 1):", np.random.normal(0, 1))  # Custom normal
```

### Example 2: Random Arrays of Different Shapes

```python
import numpy as np

# 1D arrays
arr1d = np.random.random(5)
print("1D (5):", arr1d.round(3))

# 2D arrays
arr2d = np.random.random((3, 4))
print("\n2D (3x4):\n", arr2d.round(3))

# 3D arrays
arr3d = np.random.random((2, 3, 4))
print("\n3D (2x3x4):")
print("Shape:", arr3d.shape)

# Integer arrays
int_arr = np.random.randint(0, 100, size=(4, 4))
print("\nInteger 4x4:\n", int_arr)
```

### Example 3: Seeding for Reproducibility

```python
import numpy as np

# Demonstrate seed effect
np.random.seed(123)
print("With seed 123:")
print("  First:", np.random.random(3))
print("  Second:", np.random.random(3))

# Reset seed - get same numbers
np.random.seed(123)
print("\nReset seed 123:")
print("  First:", np.random.random(3))  # Same as above!

# Different seed - different numbers
np.random.seed(456)
print("\nWith seed 456:")
print("  First:", np.random.random(3))  # Different!

# Modern approach with Generator
rng1 = np.random.default_rng(123)
rng2 = np.random.default_rng(123)
print("\nModern Generator (seed 123):")
print("  rng1:", rng1.random(3))
print("  rng2:", rng2.random(3))  # Same!
```

### Example 4: Weighted Random Selection

```python
import numpy as np

# Categories with different probabilities
categories = np.array(["cat_a", "cat_b", "cat_c", "cat_d"])
probabilities = np.array([0.1, 0.2, 0.3, 0.4])

# Generate 1000 samples
np.random.seed(42)
samples = np.random.choice(categories, size=1000, p=probabilities)

# Count occurrences
unique, counts = np.unique(samples, return_counts=True)
print("Category distribution:")
for cat, count in zip(unique, counts):
    print(f"  {cat}: {count} ({count/1000:.1%})")

# Output (approximate):
# Category distribution:
#   cat_a: 98 (9.8%)
#   cat_b: 203 (20.3%)
#   cat_c: 301 (30.1%)
#   cat_d: 398 (39.8%)
```

### Example 5: Simulating Random Processes

```python
import numpy as np

# Simulate random walk
np.random.seed(42)
steps = np.random.choice([-1, 1], size=100)
position = np.cumsum(steps)
print(f"Random walk final position: {position[-1]}")
print(f"Max position: {position.max()}, Min: {position.min()}")

# Simulate dice rolls and statistics
np.random.seed(42)
rolls = np.random.randint(1, 7, size=10000)
print(f"\nDice statistics (10000 rolls):")
print(f"  Mean: {rolls.mean():.2f} (expected: 3.50)")
print(f"  Std: {rolls.std():.2f} (expected: ~1.71)")

# Distribution of each face
unique, counts = np.unique(rolls, return_counts=True)
print(f"  Face distribution:")
for face, count in zip(unique, counts):
    print(f"    {face}: {count} ({count/10000:.1%})")
```

---

## Common Mistakes to Avoid

### Mistake 1: Not Setting Seed for Reproducibility

```python
# WRONG - Results vary each run
result = np.random.random(5)
print(result)  # Different every time!

# CORRECT - Set seed for reproducibility
np.random.seed(42)
result = np.random.random(5)
print(result)  # Same every time!
```

### Mistake 2: Using Global State in Functions

```python
# WRONG - Modifies global state
def get_random():
    return np.random.random(5)

# CORRECT - Use local RandomState or Generator
def get_random(seed=None):
    rng = np.random.default_rng(seed)
    return rng.random(5)
```

### Mistake 3: Confusing randn() with normal()

```python
# WRONG - Assuming randn() can take mean/std
# arr = np.random.randn(1000, mean=50, std=10)  # TypeError!

# CORRECT - Use normal() for custom parameters
arr = np.random.normal(50, 10, size=1000)

# Or transform randn()
arr = np.random.randn(1000) * 10 + 50  # Same result
```

### Mistake 4: Forgetting high is Exclusive

```python
# WRONG - Want integers 1-10 inclusive
arr = np.random.randint(1, 10)  # Only 1-9!

# CORRECT - Use high+1 for inclusive range
arr = np.random.randint(1, 11)  # 1-10 inclusive
```

### Mistake 5: Not Normalizing Probabilities

```python
# WRONG - Probabilities don't sum to 1
# probs = [0.3, 0.4, 0.5]  # Sums to 1.2
# arr = np.random.choice(3, p=probs)  # ValueError!

# CORRECT - Normalize probabilities
probs = np.array([0.3, 0.4, 0.5])
probs = probs / probs.sum()  # Now sums to 1
arr = np.random.choice(3, size=1000, p=probs)
```

---

## Best Practices

### 1. Use the Modern Generator API

```python
import numpy as np

# Recommended: default_rng()
rng = np.random.default_rng(42)
arr = rng.random(100)

# Legacy (still works, but less recommended)
arr = np.random.random(100)
```

### 2. Set Seeds for Debugging and Testing

```python
import numpy as np

# Always set seed in tests
def test_random_function():
    np.random.seed(42)
    result = my_random_function()
    expected = np.array([...])
    np.testing.assert_array_almost_equal(result, expected)
```

### 3. Document Random Seeds in Research

```python
import numpy as np

# Document seed for reproducibility
SEED = 12345
np.random.seed(SEED)

# Generate data
X = np.random.randn(1000, 10)
y = np.random.randint(0, 2, size=1000)
```

### 4. Use Appropriate Distribution

```python
import numpy as np

# Uniform: equal probability across range
uniform = np.random.uniform(0, 1, size=1000)

# Normal: clustered around mean
normal = np.random.normal(0, 1, size=1000)

# Binomial: count of successes in trials
binomial = np.random.binomial(10, 0.5, size=1000)

# Poisson: count of events
poisson = np.random.poisson(5, size=1000)
```

### 5. Validate Random Output

```python
import numpy as np

np.random.seed(42)
arr = np.random.random(10000)

# Check basic properties
assert arr.min() >= 0, "Values should be >= 0"
assert arr.max() < 1, "Values should be < 1"
assert abs(arr.mean() - 0.5) < 0.05, "Mean should be ~0.5"
assert abs(arr.std() - 0.289) < 0.05, "Std should be ~0.289"
```

---

## Practice Exercises

### Exercise 1: Basic Random Generation

```python
import numpy as np

# TODO: Generate 10 random floats between 0 and 1
arr = np.random.random(10)
print("Random floats:", arr)

# TODO: Generate 5 random integers between 1 and 100
ints = np.random.randint(1, 101, size=5)
print("Random integers:", ints)

# TODO: Generate a 3x3 array of random floats
matrix = np.random.random((3, 3))
print("Random matrix:\n", matrix)
```

### Exercise 2: Normal Distribution

```python
import numpy as np

# TODO: Generate 1000 values from standard normal distribution
standard = np.random.randn(1000)
print(f"Standard normal - Mean: {standard.mean():.3f}, Std: {standard.std():.3f}")

# TODO: Generate 1000 values with mean=50, std=10
custom = np.random.normal(50, 10, size=1000)
print(f"Custom normal - Mean: {custom.mean():.3f}, Std: {custom.std():.3f}")

# TODO: How many values are within 1 std of mean?
within_1std = np.sum((custom > 40) & (custom < 60))
print(f"Within 1 std: {within_1std} ({within_1std/10:.1f}%)")
```

### Exercise 3: Reproducible Random

```python
import numpy as np

# TODO: Generate array with seed 42
np.random.seed(42)
arr1 = np.random.random(5)
print("First:", arr1)

# TODO: Reset seed and generate again
np.random.seed(42)
arr2 = np.random.random(5)
print("Second:", arr2)

# TODO: Verify they're equal
print("Equal:", np.array_equal(arr1, arr2))

# TODO: Use modern Generator API
rng = np.random.default_rng(42)
arr3 = rng.random(5)
print("Generator:", arr3)
```

### Exercise 4: Random Selection

```python
import numpy as np

# TODO: Create array of colors
colors = np.array(["red", "green", "blue", "yellow", "purple"])

# TODO: Select 5 colors randomly (with replacement)
selected = np.random.choice(colors, size=5, replace=True)
print("With replacement:", selected)

# TODO: Select 3 colors without replacement
unique_selected = np.random.choice(colors, size=3, replace=False)
print("Without replacement:", unique_selected)

# TODO: Weighted selection (blue 50%, others 10% each)
weights = [0.1, 0.1, 0.5, 0.1, 0.1]
weighted = np.random.choice(colors, size=20, p=weights)
print("Weighted:", weighted)
```

### Exercise 5: Simulation

```python
import numpy as np

# TODO: Simulate 100 coin flips
np.random.seed(42)
flips = np.random.randint(0, 2, size=100)
print(f"Heads: {np.sum(flips)}, Tails: {100 - np.sum(flips)}")

# TODO: Simulate rolling two dice 1000 times
die1 = np.random.randint(1, 7, size=1000)
die2 = np.random.randint(1, 7, size=1000)
total = die1 + die2
print(f"Average sum: {total.mean():.2f} (expected: 7.00)")

# TODO: Simulate 10000 normal measurements (mean=170, std=10)
heights = np.random.normal(170, 10, size=10000)
print(f"Height stats: mean={heights.mean():.1f}, std={heights.std():.1f}")
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **np.random.random()** | Random float in [0, 1) |
| **np.random.rand()** | Random float in [0, 1) (legacy) |
| **np.random.randint()** | Random integer in [low, high) |
| **np.random.randn()** | Standard normal (μ=0, σ=1) |
| **np.random.normal()** | Custom normal distribution |
| **np.random.uniform()** | Uniform distribution in [low, high) |
| **np.random.seed()** | Set seed for reproducibility |
| **np.random.RandomState()** | Independent random stream |
| **np.random.default_rng()** | Modern Generator API (recommended) |
| **np.random.choice()** | Random selection from array |

---

## Quick Reference

```python
import numpy as np

# Random floats
arr = np.random.random(10)           # [0, 1)
arr = np.random.uniform(0, 100, 10)  # [0, 100)

# Random integers
arr = np.random.randint(0, 10, 10)   # [0, 10)

# Normal distribution
arr = np.random.randn(10)            # Standard normal
arr = np.random.normal(50, 10, 10)   # Custom normal

# Seed for reproducibility
np.random.seed(42)

# Modern API (recommended)
rng = np.random.default_rng(42)
arr = rng.random(10)
arr = rng.integers(0, 100, 10)
arr = rng.normal(0, 1, 10)
```

---

**Next Lecture:** [17 - Data Distribution](17-data-distribution-lecture.md)
