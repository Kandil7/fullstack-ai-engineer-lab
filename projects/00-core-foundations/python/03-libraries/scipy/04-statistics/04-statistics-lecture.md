# SciPy Lecture 04: Statistics

## 🎯 Topic Overview

SciPy's `stats` module provides probability distributions, statistical tests, and descriptive statistics — forming the foundation of data analysis.

## 📚 Learning Objectives

1. Use probability distributions (normal, t, chi-square, etc.)
2. Perform statistical tests (t-test, ANOVA, chi-square, KS)
3. Calculate descriptive statistics

---

## 1. Probability Distributions

```python
import numpy as np
from scipy import stats

# Normal distribution
norm_dist = stats.norm(loc=0, scale=1)  # Standard normal
print(f"P(Z < 1.96) = {norm_dist.cdf(1.96):.4f}")
print(f"P(Z > 1.96) = {norm_dist.sf(1.96):.4f}")
print(f"99% CI at z = {norm_dist.ppf(0.995):.4f}")
print(f"PDF at 0 = {norm_dist.pdf(0):.4f}")

# Sample from distribution
samples = norm_dist.rvs(size=1000, random_state=42)

# Other distributions
stats.t(df=10)              # t-distribution
stats.chi2(df=5)            # Chi-squared
stats.f(dfn=3, dfd=20)      # F-distribution
stats.expon(scale=1)        # Exponential
stats.binom(n=10, p=0.5)    # Binomial
stats.poisson(mu=3)         # Poisson
```

---

## 2. Statistical Tests

```python
# One-sample t-test
sample = stats.norm.rvs(loc=0.5, scale=1, size=50)
t_stat, p_value = stats.ttest_1samp(sample, popmean=0.0)
print(f"One-sample t-test: t={t_stat:.3f}, p={p_value:.4f}")

# Two-sample t-test
group1 = stats.norm.rvs(loc=0, scale=1, size=50)
group2 = stats.norm.rvs(loc=0.5, scale=1, size=50)
t_stat, p_value = stats.ttest_ind(group1, group2)
print(f"Independent t-test: t={t_stat:.3f}, p={p_value:.4f}")

# Paired t-test
before = stats.norm.rvs(loc=100, scale=10, size=20)
after = before + stats.norm.rvs(loc=-5, scale=5, size=20)
t_stat, p_value = stats.ttest_rel(before, after)
print(f"Paired t-test: t={t_stat:.3f}, p={p_value:.4f}")

# ANOVA
from scipy import stats as ss
f_stat, p_value = ss.f_oneway(group1, group2, 
                               stats.norm.rvs(loc=1, scale=1, size=50))
print(f"ANOVA: F={f_stat:.3f}, p={p_value:.4f}")

# Chi-squared test
observed = np.array([[30, 10], [5, 55]])
chi2, p, dof, expected = stats.chi2_contingency(observed)
print(f"Chi-squared: χ²={chi2:.3f}, p={p_value:.4f}")
```

---

## 3. Descriptive Statistics

```python
data = np.random.normal(0, 1, 1000)

# Summary statistics
desc = stats.describe(data)
print(f"n: {desc.nobs}")
print(f"Mean: {desc.mean:.3f}")
print(f"Variance: {desc.variance:.3f}")
print(f"Skewness: {desc.skewness:.3f}")
print(f"Kurtosis: {desc.kurtosis:.3f}")

# Percentiles
print(f"Median: {np.median(data):.3f}")
print(f"Q1, Q3: {np.percentile(data, [25, 75])}")

# Mode
mode_result = stats.mode(data)
print(f"Mode: {mode_result.mode}")

# Correlation
x = np.random.normal(0, 1, 100)
y = x * 0.7 + np.random.normal(0, 0.5, 100)
r, p = stats.pearsonr(x, y)
print(f"Pearson r = {r:.3f}, p = {p:.4f}")
rho, p = stats.spearmanr(x, y)
print(f"Spearman ρ = {rho:.3f}, p = {p:.4f}")
```

---

## Summary

| Function | Purpose |
|----------|---------|
| `stats.norm()` | Normal distribution |
| `stats.ttest_ind()` | Independent t-test |
| `stats.ttest_rel()` | Paired t-test |
| `stats.f_oneway()` | One-way ANOVA |
| `stats.chi2_contingency()` | Chi-squared test |
| `stats.describe()` | Descriptive statistics |
| `stats.pearsonr()` | Pearson correlation |
| `stats.spearmanr()` | Spearman rank correlation |
