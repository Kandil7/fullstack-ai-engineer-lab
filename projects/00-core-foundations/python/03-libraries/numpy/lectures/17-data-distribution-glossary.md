# Glossary: Data Distributions in NumPy (Lecture 17)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| Uniform | `np.random.uniform(low, high, n)` | Equal probability in range |
| Normal | `np.random.normal(μ, σ, n)` | Bell-shaped distribution |
| Binomial | `np.random.binomial(n, p, n)` | Success count in trials |
| Poisson | `np.random.poisson(λ, n)` | Event count in interval |
| Exponential | `np.random.exponential(β, n)` | Time between events |
| Mean | `np.average(arr)` | Average value |
| Standard Deviation | `np.std(arr)` | Spread of data |
| Variance | `np.var(arr)` | Squared spread |
| Percentile | `np.percentile(arr, q)` | Value at q-th percentile |
| Empirical Rule | 68-95-99.7 | Normal distribution percentages |

---

## Detailed Definitions

### Beta Distribution

**Definition:** A continuous distribution on [0, 1], often used to model probabilities or proportions. Parameterized by two shape parameters α and β.

**Example:**
```python
import numpy as np

# Beta distribution with α=2, β=5
beta_data = np.random.beta(2, 5, size=1000)
print(f"Beta(2,5):")
print(f"  Mean: {beta_data.mean():.4f}")  # ~0.286
print(f"  Std: {beta_data.std():.4f}")    # ~0.152
```

**Related Terms:** Uniform, Probability, Proportion

---

### Binomial Distribution

**Definition:** Discrete distribution representing the number of successes in a fixed number of independent Bernoulli trials. Each trial has the same probability of success.

**Example:**
```python
import numpy as np

# 10 coin flips, 50% probability, 1000 experiments
n_trials = 10
prob_success = 0.5
experiments = 1000

binomial = np.random.binomial(n_trials, prob_success, size=experiments)
print(f"Binomial(n={n_trials}, p={prob_success}):")
print(f"  Mean: {binomial.mean():.2f}")  # ~5.0
print(f"  Std: {binomial.std():.2f}")    # ~1.58

# Distribution of results
unique, counts = np.unique(binomial, return_counts=True)
for val, count in zip(unique, counts):
    print(f"    {val} successes: {count} times")
```

**Related Terms:** Bernoulli Trial, Probability, Success Rate

---

### Chi-Square Distribution

**Definition:** A continuous distribution often used in hypothesis testing and confidence interval estimation. Sum of squared standard normal variables.

**Example:**
```python
import numpy as np

# Chi-square with 5 degrees of freedom
chi2 = np.random.chisquare(5, size=10000)
print(f"Chi-square(df=5):")
print(f"  Mean: {chi2.mean():.2f}")  # ~5.0
print(f"  Std: {chi2.std():.2f}")    # ~3.16
```

**Related Terms:** Normal Distribution, Hypothesis Testing

---

### Continuous Distribution

**Definition:** A probability distribution where the random variable can take any value within a range. Examples include normal, uniform, and exponential distributions.

**Example:**
```python
import numpy as np

# Continuous distributions
normal = np.random.normal(0, 1, 1000)
uniform = np.random.uniform(0, 1, 1000)
exponential = np.random.exponential(1, 1000)

print("Continuous distributions can take any value in range")
print(f"Normal: {normal.min():.4f} to {normal.max():.4f}")
print(f"Uniform: {uniform.min():.4f} to {uniform.max():.4f}")
```

**Related Terms:** Discrete Distribution, Probability Density Function

---

### Discrete Distribution

**Definition:** A probability distribution where the random variable can only take specific, distinct values. Examples include binomial, Poisson, and uniform (discrete).

**Example:**
```python
import numpy as np

# Discrete distributions
binomial = np.random.binomial(10, 0.5, 1000)
poisson = np.random.poisson(5, 1000)
discrete_uniform = np.random.randint(1, 7, 1000)

print("Discrete distributions take specific values")
print(f"Binomial unique values: {np.unique(binomial)}")
print(f"Poisson unique values: {np.unique(poisson)[:10]}...")
```

**Related Terms:** Continuous Distribution, Probability Mass Function

---

### Exponential Distribution

**Definition:** A continuous distribution that describes the time between events in a Poisson process. Memoryless property: the probability of an event doesn't depend on how much time has passed.

**Example:**
```python
import numpy as np

# Mean wait time = 5 minutes
scale = 5
wait_times = np.random.exponential(scale, size=1000)
print(f"Exponential(scale={scale}):")
print(f"  Mean: {wait_times.mean():.2f}")  # ~5.0
print(f"  Std: {wait_times.std():.2f}")    # ~5.0
print(f"  P(wait < 5): {np.mean(wait_times < 5):.2%}")  # ~63.2%
```

**Related Terms:** Poisson Distribution, Wait Time, Rate Parameter

---

### Gamma Distribution

**Definition:** A continuous distribution that generalizes the exponential distribution. Often used for waiting times for multiple events.

**Example:**
```python
import numpy as np

# Gamma with shape=2, scale=2
gamma = np.random.gamma(2, 2, size=10000)
print(f"Gamma(shape=2, scale=2):")
print(f"  Mean: {gamma.mean():.2f}")  # ~4.0
print(f"  Std: {gamma.std():.2f}")    # ~2.83
```

**Related Terms:** Exponential Distribution, Shape Parameter

---

### Kurtosis

**Definition:** A measure of the "tailedness" of a probability distribution. Higher kurtosis means more of the variance comes from infrequent, extreme values.

**Example:**
```python
import numpy as np
from scipy import stats

normal = np.random.normal(0, 1, 10000)
leptokurtic = np.random.laplace(0, 1, 10000)  # Heavy tails

print(f"Normal kurtosis: {stats.kurtosis(normal):.2f}")  # ~0
print(f"Laplace kurtosis: {stats.kurtosis(leptokurtic):.2f}")  # ~3
```

**Related Terms:** Skewness, Normal Distribution, Variance

---

### Log-Normal Distribution

**Definition:** A continuous distribution where the logarithm of the random variable is normally distributed. Often used for financial data and natural phenomena.

**Example:**
```python
import numpy as np

# Log-normal with μ=0, σ=1
lognormal = np.random.lognormal(0, 1, size=10000)
print(f"LogNormal(μ=0, σ=1):")
print(f"  Mean: {lognormal.mean():.2f}")  # ~1.65
print(f"  Std: {lognormal.std():.2f}")    # ~2.16
```

**Related Terms:** Normal Distribution, Exponential Distribution

---

### Mean

**Definition:** The average of all values in a dataset. For a probability distribution, it's the expected value.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Different ways to calculate mean
print(f"np.mean(): {np.mean(arr)}")      # 3.0
print(f"np.average(): {np.average(arr)}")  # 3.0
print(f"arr.mean(): {arr.mean()}")        # 3.0

# Weighted mean
weights = np.array([1, 2, 3, 4, 5])
print(f"Weighted mean: {np.average(arr, weights=weights)}")  # 3.67
```

**Related Terms:** Median, Mode, Standard Deviation

---

### Median

**Definition:** The middle value when data is sorted. For even-sized datasets, it's the average of the two middle values.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

print(f"Median: {np.median(arr)}")  # 5.5

# Median is robust to outliers
arr_with_outlier = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 100])
print(f"Median with outlier: {np.median(arr_with_outlier)}")  # 5.5
print(f"Mean with outlier: {np.mean(arr_with_outlier)}")       # 14.5
```

**Related Terms:** Mean, Mode, Percentile

---

### Normal Distribution

**Definition:** A continuous probability distribution that is symmetric about the mean, forming a bell-shaped curve. Also called Gaussian distribution. Defined by mean (μ) and standard deviation (σ).

**Example:**
```python
import numpy as np

# Standard normal (μ=0, σ=1)
standard = np.random.standard_normal(10000)
print(f"Standard Normal:")
print(f"  Mean: {standard.mean():.4f}")  # ~0
print(f"  Std: {standard.std():.4f}")    # ~1

# Custom normal
custom = np.random.normal(100, 15, 10000)
print(f"\nCustom Normal (μ=100, σ=15):")
print(f"  Mean: {custom.mean():.4f}")  # ~100
print(f"  Std: {custom.std():.4f}")    # ~15
```

**Related Terms:** Standard Normal, Empirical Rule, Z-Score

---

### Poisson Distribution

**Definition:** A discrete distribution expressing the probability of a given number of events occurring in a fixed interval of time or space, given a constant average rate.

**Example:**
```python
import numpy as np

# Average 4 events per interval
lam = 4
events = np.random.poisson(lam, size=1000)
print(f"Poisson(λ={lam}):")
print(f"  Mean: {events.mean():.2f}")  # ~4.0
print(f"  Std: {events.std():.2f}")    # ~2.0
print(f"  P(0 events): {np.mean(events == 0):.4f}")
print(f"  P(>6 events): {np.mean(events > 6):.4f}")
```

**Related Terms:** Exponential Distribution, Rate Parameter, Lambda

---

### Probability Density Function (PDF)

**Definition:** A function that describes the likelihood of a continuous random variable taking on a particular value. The area under the curve equals 1.

**Example:**
```python
import numpy as np

# Generate data from normal distribution
data = np.random.normal(0, 1, 10000)

# Approximate PDF using histogram
hist, bin_edges = np.histogram(data, bins=50, density=True)
print(f"PDF approximation: {hist[:5]}")
print(f"Total area: {np.sum(hist * np.diff(bin_edges)):.4f}")  # ~1.0
```

**Related Terms:** Probability Mass Function, Cumulative Distribution Function

---

### Quantile

**Definition:** Values that divide a probability distribution into continuous intervals with equal probabilities. Includes percentiles, quartiles, etc.

**Example:**
```python
import numpy as np

data = np.random.normal(100, 15, 10000)

# Different quantiles
print(f"25th percentile (Q1): {np.percentile(data, 25):.1f}")
print(f"50th percentile (Q2): {np.percentile(data, 50):.1f}")  # Median
print(f"75th percentile (Q3): {np.percentile(data, 75):.1f}")

# Specific quantiles
quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]
for q in quantiles:
    print(f"{q*100:.0f}th: {np.quantile(data, q):.1f}")
```

**Related Terms:** Percentile, Quartile, Median

---

### Skewness

**Definition:** A measure of the asymmetry of a probability distribution. Positive skew means right tail is longer; negative skew means left tail is longer.

**Example:**
```python
import numpy as np
from scipy import stats

normal = np.random.normal(0, 1, 10000)
right_skewed = np.random.exponential(1, 10000)

print(f"Normal skewness: {stats.skew(normal):.2f}")      # ~0
print(f"Exponential skewness: {stats.skew(right_skewed):.2f}")  # ~2
```

**Related Terms:** Kurtosis, Mean, Median

---

### Standard Deviation

**Definition:** A measure of the amount of variation or dispersion of a set of values. Square root of variance.

**Example:**
```python
import numpy as np

arr = np.array([2, 4, 4, 4, 5, 5, 7, 9])

print(f"Std: {np.std(arr):.4f}")  # 2.0

# Population vs sample std
data = np.random.normal(0, 1, 100)
print(f"Population std: {np.std(data):.4f}")
print(f"Sample std: {np.std(data, ddof=1):.4f}")
```

**Related Terms:** Variance, Mean, Normal Distribution

---

### Variance

**Definition:** The average of the squared differences from the mean. Measures how spread out the data is.

**Example:**
```python
import numpy as np

arr = np.array([2, 4, 4, 4, 5, 5, 7, 9])

print(f"Variance: {np.var(arr):.4f}")  # 4.0
print(f"Std: {np.sqrt(np.var(arr)):.4f}")  # 2.0

# Population vs sample variance
data = np.random.normal(0, 1, 100)
print(f"Population variance: {np.var(data):.4f}")
print(f"Sample variance: {np.var(data, ddof=1):.4f}")
```

**Related Terms:** Standard Deviation, Mean, Dispersion

---

### Z-Score

**Definition:** The number of standard deviations a data point is from the mean. Formula: z = (x - μ) / σ

**Example:**
```python
import numpy as np

data = np.random.normal(100, 15, 1000)

# Calculate z-scores
z_scores = (data - data.mean()) / data.std()

print(f"Data point 115 z-score: {(115 - 100) / 15:.2f}")  # 1.0
print(f"Data point 70 z-score: {(70 - 100) / 15:.2f}")   # -2.0

# Count by z-score ranges
within_1 = np.mean(np.abs(z_scores) < 1) * 100
within_2 = np.mean(np.abs(z_scores) < 2) * 100
within_3 = np.mean(np.abs(z_scores) < 3) * 100
print(f"Within 1 std: {within_1:.1f}%")
print(f"Within 2 std: {within_2:.1f}%")
print(f"Within 3 std: {within_3:.1f}%")
```

**Related Terms:** Standard Deviation, Normal Distribution, Empirical Rule

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| Beta Distribution | Continuous on [0,1] | `np.random.beta(2, 5, 1000)` |
| Binomial | Success count in trials | `np.random.binomial(10, 0.5, 1000)` |
| Chi-Square | Sum of squared normals | `np.random.chisquare(5, 1000)` |
| Continuous | Any value in range | Normal, Uniform, Exponential |
| Discrete | Specific values only | Binomial, Poisson |
| Exponential | Time between events | `np.random.exponential(5, 1000)` |
| Gamma | Generalized exponential | `np.random.gamma(2, 2, 1000)` |
| Kurtosis | Tailedness measure | `scipy.stats.kurtosis(data)` |
| Log-Normal | Log is normal | `np.random.lognormal(0, 1, 1000)` |
| Mean | Average value | `np.mean(data)` |
| Median | Middle value | `np.median(data)` |
| Normal | Bell-shaped curve | `np.random.normal(0, 1, 1000)` |
| Poisson | Event count | `np.random.poisson(5, 1000)` |
| PDF | Probability density | Area under curve = 1 |
| Quantile | Value at probability | `np.quantile(data, 0.5)` |
| Skewness | Asymmetry measure | `scipy.stats.skew(data)` |
| Std Dev | Spread measure | `np.std(data)` |
| Variance | Squared spread | `np.var(data)` |
| Z-Score | Std devs from mean | `(x - μ) / σ` |

---

**Back to Lecture:** [17 - Data Distribution](17-data-distribution-lecture.md)
