"""
Data Distribution
W3Schools: https://www.w3schools.com/python/numpy_random_distribution.asp

Generating random data from various probability distributions.
"""

import numpy as np

# ============================================================
# Example 1: Uniform Distribution
# Equal probability across a range.
# ============================================================

# Uniform distribution between 0 and 1
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

# Discrete uniform (integers)
discrete = np.random.randint(1, 7, size=1000)
print(f"\nDiscrete uniform (dice):")
print(f"  Mean: {discrete.mean():.4f}")    # ~3.5
print(f"  Std: {discrete.std():.4f}")      # ~1.71
# Output:
# Uniform distribution:
#   Mean: 0.4987
#   Std: 0.2892
#   Min: 0.0023
#   Max: 0.9987
#
# Uniform [10, 20):
#   Mean: 14.9872
#   Std: 2.8891

# ============================================================
# Example 2: Normal (Gaussian) Distribution
# Bell-shaped curve centered at mean.
# ============================================================

# Standard normal (mean=0, std=1)
normal = np.random.randn(10000)
print("\nStandard normal:")
print(f"  Mean: {normal.mean():.4f}")    # ~0.0
print(f"  Std: {normal.std():.4f}")      # ~1.0

# Custom normal distribution
mean, std = 170, 10  # Height in cm
heights = np.random.normal(mean, std, size=10000)
print(f"\nHeight distribution (mean={mean}, std={std}):")
print(f"  Mean: {heights.mean():.4f}")    # ~170.0
print(f"  Std: {heights.std():.4f}")      # ~10.0
print(f"  Min: {heights.min():.4f}")      # ~135.0
print(f"  Max: {heights.max():.4f}")      # ~205.0

# Percentage within 1 std
within_1std = np.sum((heights > mean - std) & (heights < mean + std)) / len(heights)
print(f"  Within 1 std: {within_1std:.2%}")  # ~68%
# Output:
# Standard normal:
#   Mean: 0.0012
#   Std: 1.0015
#
# Height distribution (mean=170, std=10):
#   Mean: 170.0234
#   Std: 9.9876
#   Within 1 std: 68.24%

# ============================================================
# Example 3: Binomial Distribution
# Number of successes in n independent trials.
# ============================================================

# Flip coin 10 times, repeat 1000 experiments
n_trials = 10
n_experiments = 1000
prob_heads = 0.5

binomial = np.random.binomial(n_trials, prob_heads, size=n_experiments)
print("\nBinomial (10 flips, p=0.5):")
print(f"  Mean heads: {binomial.mean():.2f}")  # ~5.0
print(f"  Std: {binomial.std():.2f}")          # ~1.58

# Count distribution
unique, counts = np.unique(binomial, return_counts=True)
print("  Distribution:")
for u, c in zip(unique, counts):
    print(f"    {u} heads: {c} times ({c/n_experiments:.1%})")

# Quality control: 5% defect rate, sample of 100
defects = np.random.binomial(100, 0.05, size=1000)
print(f"\nDefects (n=100, p=0.05):")
print(f"  Mean defects: {defects.mean():.2f}")  # ~5.0
print(f"  Max defects: {defects.max()}")

# ============================================================
# Example 4: Poisson Distribution
# Number of events in a fixed interval.
# ============================================================

# Average 4 customers per hour
lambda_val = 4
customers = np.random.poisson(lambda_val, size=1000)
print(f"\nPoisson (lambda={lambda_val}):")
print(f"  Mean: {customers.mean():.2f}")    # ~4.0
print(f"  Std: {customers.std():.2f}")      # ~2.0

# Probability of exactly 0 customers
p_zero = np.sum(customers == 0) / len(customers)
print(f"  P(0 customers): {p_zero:.4f}")

# Probability of more than 6 customers
p_more6 = np.sum(customers > 6) / len(customers)
print(f"  P(>6 customers): {p_more6:.4f}")

# Website hits: average 100 per minute
hits = np.random.poisson(100, size=60)
print(f"\nWebsite hits per minute (avg=100):")
print(f"  Mean: {hits.mean():.2f}")
print(f"  Min: {hits.min()}")
print(f"  Max: {hits.max()}")
# Output:
# Poisson (lambda=4):
#   Mean: 4.0123
#   Std: 2.0234

# ============================================================
# Example 5: Exponential Distribution
# Time between events in a Poisson process.
# ============================================================

# Mean wait time = 5 minutes
scale = 5
wait_times = np.random.exponential(scale, size=1000)
print(f"\nExponential (mean={scale} min):")
print(f"  Mean wait: {wait_times.mean():.2f} min")   # ~5.0
print(f"  Std: {wait_times.std():.2f} min")           # ~5.0

# P(wait < 5 min)
p_short = np.sum(wait_times < scale) / len(wait_times)
print(f"  P(wait < 5 min): {p_short:.2%}")  # ~63.2%

# P(wait < 1 min)
p_very_short = np.sum(wait_times < 1) / len(wait_times)
print(f"  P(wait < 1 min): {p_very_short:.2%}")

# Custom exponential
arr = np.random.exponential(1.0 / 0.5, size=1000)  # rate=0.5
print(f"\nExponential (rate=0.5):")
print(f"  Mean: {arr.mean():.2f}")  # ~2.0
print(f"  Std: {arr.std():.2f}")    # ~2.0
