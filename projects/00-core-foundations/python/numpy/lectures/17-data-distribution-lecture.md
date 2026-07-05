# Lecture 17: Data Distributions in NumPy

## Topic Overview

Understanding probability distributions is crucial for data science, statistics, and machine learning. NumPy provides functions to generate random data from various probability distributions, each with unique characteristics and applications. This lecture covers the most important distributions: uniform, normal (Gaussian), binomial, Poisson, and exponential.

Each distribution models different real-world phenomena — from coin flips (binomial) to customer arrivals (Poisson) to wait times (exponential).

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Generate data from uniform distributions (continuous and discrete)
2. Generate data from normal (Gaussian) distributions
3. Understand and apply binomial distribution for success/failure scenarios
4. Use Poisson distribution for event counting
5. Apply exponential distribution for time-between-events modeling
6. Calculate statistical properties of generated distributions
7. Verify distribution characteristics using statistics
8. Choose the appropriate distribution for different use cases
9. Understand the empirical rule (68-95-99.7) for normal distributions
10. Apply distributions to practical data analysis scenarios

---

## Key Concepts

### 1. Uniform Distribution

All values in a range are equally likely.

```python
import numpy as np

# Continuous uniform between 0 and 1
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
```

**Applications:** Random sampling, shuffling, simulations where all outcomes are equally likely.

### 2. Normal (Gaussian) Distribution

The bell-shaped curve, most common in nature and statistics.

```python
import numpy as np

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

# Percentage within 1 std (empirical rule)
within_1std = np.sum((heights > mean - std) & (heights < mean + std)) / len(heights)
print(f"  Within 1 std: {within_1std:.2%}")  # ~68%
```

**The Empirical Rule (68-95-99.7):**
- ~68% of data within 1 standard deviation
- ~95% within 2 standard deviations
- ~99.7% within 3 standard deviations

**Applications:** Heights, test scores, measurement errors, natural phenomena.

### 3. Binomial Distribution

Number of successes in a fixed number of independent trials.

```python
import numpy as np

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
```

**Parameters:**
- `n`: Number of trials
- `p`: Probability of success
- Mean = n × p
- Std = √(n × p × (1-p))

**Applications:** Quality control, A/B testing, medical trials.

### 4. Poisson Distribution

Number of events occurring in a fixed interval of time or space.

```python
import numpy as np

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
```

**Parameters:**
- `lambda` (λ): Average rate of events
- Mean = λ
- Std = √λ

**Applications:** Customer arrivals, website hits, defects per unit, phone calls per hour.

### 5. Exponential Distribution

Time between events in a Poisson process.

```python
import numpy as np

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
```

**Parameters:**
- `scale` (β): Mean time between events
- Rate (λ) = 1/scale
- Mean = scale
- Std = scale

**Applications:** Wait times, time between failures, radioactive decay, queuing theory.

---

## Code Examples with Explanations

### Example 1: Comparing Distributions

```python
import numpy as np

np.random.seed(42)

# Generate data from different distributions
n = 10000

uniform = np.random.uniform(0, 1, n)
normal = np.random.normal(0.5, 0.15, n)
binomial = np.random.binomial(10, 0.5, n) / 10  # Normalize to [0,1]
poisson = np.random.poisson(5, n) / 10  # Normalize
exponential = np.random.exponential(1, n)
exponential = exponential / exponential.max()  # Normalize to [0,1]

# Compare statistics
distributions = {
    'Uniform': uniform,
    'Normal': normal,
    'Binomial': binomial,
    'Poisson': poisson,
    'Exponential': exponential
}

print("Distribution Statistics:")
print(f"{'Name':<12} {'Mean':>8} {'Std':>8} {'Min':>8} {'Max':>8}")
print("-" * 50)
for name, data in distributions.items():
    print(f"{name:<12} {data.mean():>8.4f} {data.std():>8.4f} {data.min():>8.4f} {data.max():>8.4f}")
```

### Example 2: Normal Distribution Analysis

```python
import numpy as np

np.random.seed(42)

# Generate IQ scores (mean=100, std=15)
iq_scores = np.random.normal(100, 15, size=10000)

# Statistics
print("IQ Score Distribution:")
print(f"  Mean: {iq_scores.mean():.1f}")
print(f"  Median: {np.median(iq_scores):.1f}")
print(f"  Std: {iq_scores.std():.1f}")

# Percentiles
percentiles = [10, 25, 50, 75, 90]
print("\nPercentiles:")
for p in percentiles:
    print(f"  {p}th: {np.percentile(iq_scores, p):.1f}")

# Count by ranges
ranges = [
    ("Below 70 (Intellectual Disability)", iq_scores < 70),
    ("70-85 (Borderline)", (iq_scores >= 70) & (iq_scores < 85)),
    ("85-115 (Average)", (iq_scores >= 85) & (iq_scores < 115)),
    ("115-130 (Superior)", (iq_scores >= 115) & (iq_scores < 130)),
    ("Above 130 (Gifted)", iq_scores >= 130)
]

print("\nRange Distribution:")
for name, mask in ranges:
    count = np.sum(mask)
    print(f"  {name}: {count} ({count/100:.1f}%)")
```

### Example 3: Binomial Distribution Simulation

```python
import numpy as np

np.random.seed(42)

# Simulate A/B test
n_visitors = 1000
conversion_rate_a = 0.12  # 12% conversion
conversion_rate_b = 0.15  # 15% conversion

# Generate conversions
conversions_a = np.random.binomial(n_visitors, conversion_rate_a)
conversions_b = np.random.binomial(n_visitors, conversion_rate_b)

print("A/B Test Results:")
print(f"  Group A: {conversions_a}/{n_visitors} ({conversions_a/n_visitors:.1%})")
print(f"  Group B: {conversions_b}/{n_visitors} ({conversions_b/n_visitors:.1%})")
print(f"  Difference: {(conversions_b - conversions_a)/n_visitors:.1%}")

# Run multiple simulations
n_sims = 10000
results_a = np.random.binomial(n_visitors, conversion_rate_a, n_sims)
results_b = np.random.binomial(n_visitors, conversion_rate_b, n_sims)

print(f"\nSimulation ({n_sims} runs):")
print(f"  A mean: {results_a.mean():.1f} ({results_a.mean()/n_visitors:.1%})")
print(f"  B mean: {results_b.mean():.1f} ({results_b.mean()/n_visitors:.1%})")
print(f"  B > A probability: {np.mean(results_b > results_a):.1%}")
```

### Example 4: Poisson Process Simulation

```python
import numpy as np

np.random.seed(42)

# Simulate customer arrivals at a store
# Average 20 customers per hour
lambda_per_hour = 20

# Simulate 12 hours (1 business day)
hourly_customers = np.random.poisson(lambda_per_hour, size=12)

print("Hourly Customer Arrivals:")
print("-" * 40)
for hour, customers in enumerate(hourly_customers, 1):
    bar = '█' * customers
    print(f"  Hour {hour:2d}: {customers:3d} {bar}")

print(f"\nDaily Total: {hourly_customers.sum()}")
print(f"Average per hour: {hourly_customers.mean():.1f}")

# Predict busy hours
print(f"\nHours with >25 customers: {np.sum(hourly_customers > 25)}")
print(f"Hours with <15 customers: {np.sum(hourly_customers < 15)}")
```

### Example 5: Exponential Distribution for Wait Times

```python
import numpy as np

np.random.seed(42)

# Simulate server response times
# Average response time: 100ms
avg_response_time = 100  # milliseconds
response_times = np.random.exponential(avg_response_time, size=1000)

print("Server Response Times (ms):")
print(f"  Mean: {response_times.mean():.1f}")
print(f"  Median: {np.median(response_times):.1f}")
print(f"  Std: {response_times.std():.1f}")
print(f"  Min: {response_times.min():.1f}")
print(f"  Max: {response_times.max():.1f}")

# SLA analysis
print("\nSLA Analysis:")
percentiles = [50, 90, 95, 99]
for p in percentiles:
    print(f"  {p}th percentile: {np.percentile(response_times, p):.1f}ms")

# Availability calculation
threshold = 500  # 500ms SLA
available = np.mean(response_times < threshold) * 100
print(f"\nAvailability (response < {threshold}ms): {available:.1f}%")
```

---

## Common Mistakes to Avoid

### Mistake 1: Confusing Parameters

```python
# WRONG - Mixing up parameters
# binomial(n, p) where n=trials, p=probability
# poisson(lam) where lam=average rate
# exponential(scale) where scale=mean wait time

# CORRECT - Understanding each distribution's parameters
binomial = np.random.binomial(n=10, p=0.5)  # 10 trials, 50% success
poisson = np.random.poisson(lam=5)           # Average 5 events
exponential = np.random.exponential(scale=10) # Mean wait = 10
```

### Mistake 2: Using Wrong Distribution

```python
# WRONG - Using normal for count data
# counts = np.random.normal(5, 2, 1000)  # Can be negative!

# CORRECT - Use Poisson for count data
counts = np.random.poisson(5, 1000)  # Always non-negative integers
```

### Mistake 3: Not Checking Distribution Properties

```python
import numpy as np

# Always verify your generated data
data = np.random.normal(100, 15, 10000)

# Check if it matches expected properties
assert abs(data.mean() - 100) < 1, "Mean mismatch!"
assert abs(data.std() - 15) < 1, "Std mismatch!"
```

### Mistake 4: Forgetting Seed for Reproducibility

```python
# WRONG - Different results each time
data = np.random.normal(0, 1, 1000)

# CORRECT - Set seed for reproducibility
np.random.seed(42)
data = np.random.normal(0, 1, 1000)
```

---

## Best Practices

### 1. Understand Your Data Before Choosing Distribution

```python
import numpy as np

# Binary outcomes (success/failure) → Binomial
successes = np.random.binomial(n=100, p=0.3)

# Count data → Poisson
events = np.random.poisson(lam=5)

# Continuous measurements → Normal
measurements = np.random.normal(170, 10)

# Wait times → Exponential
wait = np.random.exponential(scale=10)

# Equal probability → Uniform
random_val = np.random.uniform(0, 1)
```

### 2. Validate Generated Data

```python
import numpy as np

np.random.seed(42)
data = np.random.normal(50, 10, 10000)

# Check basic statistics
print(f"Mean: {data.mean():.2f} (expected: 50)")
print(f"Std: {data.std():.2f} (expected: 10)")
print(f"Min: {data.min():.2f}")
print(f"Max: {data.max():.2f}")

# Check empirical rule
within_1std = np.mean(np.abs(data - 50) < 10) * 100
print(f"Within 1 std: {within_1std:.1f}% (expected: ~68%)")
```

### 3. Use Appropriate Sample Size

```python
import numpy as np

# Larger samples → more stable statistics
for n in [100, 1000, 10000, 100000]:
    data = np.random.normal(0, 1, n)
    print(f"n={n:>6}: mean={data.mean():.4f}, std={data.std():.4f}")
```

### 4. Document Distribution Parameters

```python
import numpy as np

# Clearly document what you're generating
# Normal distribution: heights of adult males
# Mean: 175 cm, Std: 8 cm
MEAN_HEIGHT = 175
STD_HEIGHT = 8
SAMPLE_SIZE = 1000

np.random.seed(42)
heights = np.random.normal(MEAN_HEIGHT, STD_HEIGHT, SAMPLE_SIZE)
```

---

## Practice Exercises

### Exercise 1: Uniform Distribution

```python
import numpy as np

# TODO: Generate 1000 uniform values between 50 and 100
data = np.random.uniform(50, 100, size=1000)
print(f"Mean: {data.mean():.2f} (expected: ~75)")
print(f"Std: {data.std():.2f} (expected: ~14.43)")

# TODO: Generate 1000 dice rolls (1-6)
rolls = np.random.randint(1, 7, size=1000)
print(f"Dice mean: {rolls.mean():.2f} (expected: 3.5)")
```

### Exercise 2: Normal Distribution

```python
import numpy as np

# TODO: Generate 10000 test scores (mean=75, std=12)
np.random.seed(42)
scores = np.random.normal(75, 12, size=10000)

# TODO: Calculate percentage of students passing (>=60)
pass_rate = np.mean(scores >= 60) * 100
print(f"Pass rate: {pass_rate:.1f}%")

# TODO: Find the 90th percentile
p90 = np.percentile(scores, 90)
print(f"90th percentile: {p90:.1f}")
```

### Exercise 3: Binomial Distribution

```python
import numpy as np

# TODO: Simulate 500 coin flips
np.random.seed(42)
flips = np.random.binomial(500, 0.5)
print(f"Heads in 500 flips: {flips} ({flips/500:.1%})")

# TODO: Simulate 1000 patients with 30% recovery rate
recovered = np.random.binomial(1000, 0.3)
print(f"Recovered: {recovered} ({recovered/1000:.1%})")
```

### Exercise 4: Poisson Distribution

```python
import numpy as np

# TODO: Simulate 24 hours of website traffic (avg 50 hits/hour)
np.random.seed(42)
hourly_hits = np.random.poisson(50, size=24)

print(f"Total daily hits: {hourly_hits.sum()}")
print(f"Peak hour hits: {hourly_hits.max()}")
print(f"Quiet hour hits: {hourly_hits.min()}")
```

### Exercise 5: Exponential Distribution

```python
import numpy as np

# TODO: Simulate 100 customer wait times (avg 5 minutes)
np.random.seed(42)
wait_times = np.random.exponential(5, size=100)

print(f"Average wait: {wait_times.mean():.1f} min")
print(f"Customers waited < 2 min: {np.mean(wait_times < 2):.1%}")
print(f"Customers waited > 10 min: {np.mean(wait_times > 10):.1%}")
```

---

## Summary

| Distribution | Function | Parameters | Applications |
|-------------|----------|------------|--------------|
| **Uniform** | `np.random.uniform()` | low, high | Random sampling, simulations |
| **Normal** | `np.random.normal()` | mean, std | Heights, scores, errors |
| **Binomial** | `np.random.binomial()` | n, p | Success/failure trials |
| **Poisson** | `np.random.poisson()` | lambda | Event counting |
| **Exponential** | `np.random.exponential()` | scale | Wait times, time between events |

---

## Quick Reference

```python
import numpy as np

# Uniform distribution
arr = np.random.uniform(low, high, size)
arr = np.random.randint(low, high, size)  # Discrete

# Normal distribution
arr = np.random.normal(mean, std, size)
arr = np.random.randn(size)  # Standard normal

# Binomial distribution
arr = np.random.binomial(n, p, size)

# Poisson distribution
arr = np.random.poisson(lam, size)

# Exponential distribution
arr = np.random.exponential(scale, size)

# Verify statistics
print(f"Mean: {arr.mean():.4f}")
print(f"Std: {arr.std():.4f}")
print(f"Min: {arr.min():.4f}")
print(f"Max: {arr.max():.4f}")
```

---

**Next Lecture:** [18 - Random Permutation](18-random-permutation-lecture.md)
