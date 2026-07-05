"""
Random Intro
W3Schools: https://www.w3schools.com/python/numpy_random_intro.asp

Introduction to NumPy's random number generation.
"""

import numpy as np

# ============================================================
# Example 1: Random Floating Point Numbers
# Generate random floats between 0 and 1.
# ============================================================

# Single random float
r = np.random.random()
print("Single random:", r)  # e.g., 0.5488135039273248

# Array of random floats
arr = np.random.random(5)
print("\nRandom array (5):", arr)
# Output: [0.715 0.603 0.545 0.424 0.646]

# 2D random array
arr_2d = np.random.random((3, 3))
print("\nRandom 2D (3x3):\n", arr_2d)

# Random float in range [a, b)
r = np.random.uniform(1.5, 10.5)
print(f"\nRandom in [1.5, 10.5): {r:.2f}")

arr_uniform = np.random.uniform(0, 100, size=(2, 3))
print("Uniform array:\n", arr_uniform)
# Output:
# Single random: 0.5488135039273248
#
# Random array (5): [0.715 0.603 0.545 0.424 0.646]
#
# Random in [1.5, 10.5): 7.32

# ============================================================
# Example 2: Random Integers
# Generate random integers within a range.
# ============================================================

# Single random integer [low, high)
r = np.random.randint(0, 100)
print("\nRandom int [0,100):", r)

# Array of random integers
arr = np.random.randint(0, 50, size=10)
print("Random ints:", arr)

# 2D random integers
arr_2d = np.random.randint(1, 10, size=(3, 4))
print("\nRandom 2D ints (1-9):\n", arr_2d)

# With specific dtype
arr_int8 = np.random.randint(0, 10, size=5, dtype=np.int8)
print("int8 random:", arr_int8)
# Output:
# Random int [0,100): 42
# Random ints: [12 35  3 28 41  7 19 33  8 25]
#
# Random 2D ints (1-9):
#  [[3 7 2 8]
#   [1 5 9 4]
#   [6 3 2 7]]

# ============================================================
# Example 3: Random Normal Distribution
# Generate values from a normal (Gaussian) distribution.
# ============================================================

# Standard normal (mean=0, std=1)
r = np.random.randn()
print("\nStandard normal:", r)

arr_normal = np.random.randn(5)
print("Normal array:", arr_normal)

# Normal with custom mean and std
mean, std = 100, 15
arr_custom = np.random.normal(mean, std, size=1000)
print(f"\nNormal (mean={mean}, std={std}):")
print(f"  Sample mean: {arr_custom.mean():.2f}")
print(f"  Sample std: {arr_custom.std():.2f}")
print(f"  Min: {arr_custom.min():.2f}")
print(f"  Max: {arr_custom.max():.2f}")

# 2D normal distribution
arr_2d = np.random.randn(3, 3) * 10 + 50
print("\n2D normal (mean=50, std=10):\n", arr_2d.round(2))
# Output:
# Standard normal: -0.204...
#
# Normal (mean=100, std=15):
#   Sample mean: 99.85
#   Sample std: 14.92
#   Min: 58.32
#   Max: 145.67

# ============================================================
# Example 4: Random with Seed
# Reproducible random numbers using seed.
# ============================================================

# Without seed - different each time
print("\nWithout seed:")
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
# Output:
# With seed 42:
#   Run 1: [0.375 0.951 0.732]
#   Run 2: [0.375 0.951 0.732]
#
# RandomState(42):
#   rng1: [0.375 0.951 0.732]
#   rng2: [0.375 0.951 0.732]

# ============================================================
# Example 5: Practical Random Examples
# Common use cases for random numbers.
# ============================================================

# Simulate coin flips (0 or 1)
coin_flips = np.random.randint(0, 2, size=20)
print("\n20 coin flips:", coin_flips)
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
