# Glossary: Correlation Analysis (Lecture 13)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Correlation Coefficient | Statistical measure of linear relationship strength | r = 0.85 |
| Pearson Correlation | Measures linear relationships between continuous variables | `np.corrcoef(x, y)` |
| Spearman Correlation | Rank-based correlation for monotonic relationships | `scipy.stats.spearmanr(x, y)` |
| Kendall Tau | Ordinal correlation for small samples | `scipy.stats.kendalltau(x, y)` |
| Correlation Matrix | Table showing pairwise correlations between all variables | `df.corr()` |
| Positive Correlation | Variables move in the same direction | r > 0 |
| Negative Correlation | Variables move in opposite directions | r < 0 |
| No Correlation | No linear relationship between variables | r ≈ 0 |
| Multicollinearity | High correlation between independent features | VIF > 5 |
| Confounding Variable | Hidden variable affecting both correlated variables | Temperature |
| Coefficient of Determination | Proportion of variance explained (r²) | r² = 0.72 |
| Covariance | Measure of joint variability | `np.cov(x, y)` |
| Autocorrelation | Correlation of a variable with itself over time | Time series analysis |
| Partial Correlation | Correlation controlling for other variables | `pingouin.partial_corr()` |
| Correlation Threshold | Cutoff value for feature selection | |r| > 0.3 |

---

## Detailed Term Definitions

### Correlation Coefficient

**Definition:** A numerical measure that quantifies the strength and direction of the linear relationship between two variables. Ranges from -1 to +1.

**Formula:**
```
r = Σ[(xi - x̄)(yi - ȳ)] / √[Σ(xi - x̄)² × Σ(yi - ȳ)²]
```

**Example:**
```python
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 6])

r = np.corrcoef(x, y)[0, 1]
print(f"Correlation coefficient: {r:.4f}")
# Output: 0.8571
```

**Related Terms:** Pearson Correlation, Spearman Correlation, Coefficient of Determination

---

### Pearson Correlation

**Definition:** The most common correlation measure, assessing linear relationships between two continuous variables. Assumes normal distribution and homoscedasticity.

**When to Use:**
- Both variables are continuous
- Linear relationship exists
- Variables are approximately normally distributed
- No significant outliers

**Example:**
```python
import numpy as np
from scipy.stats import pearsonr

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([2, 4, 5, 7, 8, 10, 11, 13, 14, 16])

# NumPy method
corr_numpy = np.corrcoef(x, y)[0, 1]

# SciPy method (with p-value)
corr_scipy, p_value = pearsonr(x, y)

print(f"NumPy correlation: {corr_numpy:.4f}")
print(f"SciPy correlation: {corr_scipy:.4f}")
print(f"P-value: {p_value:.6f}")
# Output: ~0.997, p < 0.001 (significant)
```

**Related Terms:** Correlation Coefficient, Linear Regression, P-value

---

### Spearman Correlation

**Definition:** A rank-based correlation measure that assesses monotonic relationships (not necessarily linear). More robust to outliers than Pearson.

**When to Use:**
- Variables are ordinal or non-normally distributed
- Relationship is monotonic but not linear
- Outliers are present

**Example:**
```python
import numpy as np
from scipy.stats import spearmanr

# Non-linear monotonic relationship
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([1, 4, 9, 16, 25, 36, 49, 64, 81, 100])  # y = x²

# Pearson would be high but not perfect
pearson_r, _ = pearsonr(x, y)

# Spearman captures the monotonic relationship perfectly
spearman_r, p_value = spearmanr(x, y)

print(f"Pearson: {pearson_r:.4f}")
print(f"Spearman: {spearman_r:.4f}")
# Output: Pearson: 0.9750, Spearman: 1.0000
```

**Related Terms:** Monotonic Relationship, Rank Correlation, Non-parametric

---

### Kendall Tau

**Definition:** A rank-based correlation measure that assesses ordinal association. More robust with small samples and ties than Spearman.

**When to Use:**
- Small sample sizes
- Data has many tied ranks
- Ordinal data

**Example:**
```python
import numpy as np
from scipy.stats import kendalltau

x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 6])

tau, p_value = kendalltau(x, y)
print(f"Kendall's tau: {tau:.4f}")
print(f"P-value: {p_value:.4f}")
```

**Related Terms:** Spearman Correlation, Rank Correlation, Ordinal Data

---

### Correlation Matrix

**Definition:** A square, symmetric matrix showing pairwise correlations between all variables in a dataset. Diagonal values are always 1.0.

**Example:**
```python
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    'A': np.random.randn(100),
    'B': np.random.randn(100),
    'C': np.random.randn(100)
})

# Calculate correlation matrix
corr_matrix = df.corr()
print("Correlation Matrix:")
print(corr_matrix)

# Access specific correlation
print(f"\nCorrelation between A and B: {corr_matrix.loc['A', 'B']:.4f}")
```

**Related Terms:** Pairwise Correlation, Diagonal Matrix, Symmetric Matrix

---

### Positive Correlation

**Definition:** A relationship where both variables tend to increase or decrease together. Correlation coefficient is between 0 and +1.

**Example:**
```python
import numpy as np

# Height and weight (positive correlation)
height = np.array([150, 160, 170, 180, 190])  # cm
weight = np.array([50, 60, 70, 80, 90])  # kg

r = np.corrcoef(height, weight)[0, 1]
print(f"Correlation: {r:.4f}")
# Output: 1.0000 (perfect positive)
```

**Related Terms:** Direct Relationship, Positive Association

---

### Negative Correlation

**Definition:** A relationship where one variable tends to increase as the other decreases. Correlation coefficient is between -1 and 0.

**Example:**
```python
import numpy as np

# Speed and travel time (negative correlation)
speed = np.array([30, 50, 70, 90, 110])  # km/h
travel_time = np.array([2.0, 1.2, 0.86, 0.67, 0.55])  # hours

r = np.corrcoef(speed, travel_time)[0, 1]
print(f"Correlation: {r:.4f}")
# Output: -1.0000 (perfect negative)
```

**Related Terms:** Inverse Relationship, Negative Association

---

### No Correlation

**Definition:** No linear relationship between variables. Correlation coefficient is approximately 0.

**Example:**
```python
import numpy as np

# Shoe size and IQ (no correlation)
shoe_size = np.array([7, 8, 9, 10, 11, 12])
iq = np.array([110, 95, 120, 105, 115, 100])

r = np.corrcoef(shoe_size, iq)[0, 1]
print(f"Correlation: {r:.4f}")
# Output: ~0.0 (no correlation)
```

**Related Terms:** Independence, Zero Association

---

### Multicollinearity

**Definition:** A situation where two or more independent variables in a regression model are highly correlated, making it difficult to isolate their individual effects.

**Example:**
```python
import numpy as np
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

np.random.seed(42)
n = 100

# Create multicollinear features
x1 = np.random.randn(n)
x2 = x1 * 0.9 + np.random.randn(n) * 0.1  # Highly correlated with x1
x3 = np.random.randn(n)  # Independent

df = pd.DataFrame({'x1': x1, 'x2': x2, 'x3': x3})

# Calculate VIF
def calculate_vif(df):
    vif_data = pd.DataFrame()
    vif_data["feature"] = df.columns
    vif_data["VIF"] = [variance_inflation_factor(df.values, i) 
                       for i in range(df.shape[1])]
    return vif_data

print(calculate_vif(df))
# x1 and x2 will have high VIF (>5-10)
```

**Related Terms:** Variance Inflation Factor (VIF), Feature Selection, Regularization

---

### Confounding Variable

**Definition:** A hidden or third variable that influences both the independent and dependent variables, creating a spurious correlation.

**Example:**
```python
# Ice cream sales and drowning incidents are correlated
# But the confounding variable is TEMPERATURE

# Summer -> More ice cream sales
# Summer -> More people swimming -> More drownings

# Ice cream doesn't cause drowning!
# Temperature is the confounder

print("Correlation does NOT imply causation!")
print("Always consider confounding variables.")
```

**Related Terms:** Spurious Correlation, Causal Inference, Bias

---

### Coefficient of Determination (R²)

**Definition:** The proportion of variance in the dependent variable that is predictable from the independent variable(s). R² = r² where r is the correlation coefficient.

**Example:**
```python
import numpy as np

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([2, 4, 5, 7, 8, 10, 11, 13, 14, 16])

r = np.corrcoef(x, y)[0, 1]
r_squared = r ** 2

print(f"Correlation (r): {r:.4f}")
print(f"R-squared: {r_squared:.4f}")
print(f"Variance explained: {r_squared * 100:.1f}%")
# Output: R² ≈ 0.994, explains ~99.4% of variance
```

**Related Terms:** Correlation Coefficient, Explained Variance, Goodness of Fit

---

### Covariance

**Definition:** A measure of how two variables change together. Unlike correlation, covariance is not normalized and depends on the scale of variables.

**Formula:**
```
Cov(X, Y) = Σ[(xi - x̄)(yi - ȳ)] / (n - 1)
```

**Example:**
```python
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])

# Covariance
cov_matrix = np.cov(x, y)
print(f"Covariance matrix:\n{cov_matrix}")
print(f"Covariance: {cov_matrix[0, 1]:.4f}")

# Correlation (normalized covariance)
corr = np.corrcoef(x, y)[0, 1]
print(f"Correlation: {corr:.4f}")
```

**Related Terms:** Correlation Coefficient, Variance, Standard Deviation

---

### Autocorrelation

**Definition:** Correlation of a time series with a lagged version of itself. Measures how current values relate to past values.

**Example:**
```python
import numpy as np
import pandas as pd

# Generate time series with autocorrelation
np.random.seed(42)
n = 100
x = np.zeros(n)
x[0] = np.random.randn()
for i in range(1, n):
    x[i] = 0.7 * x[i-1] + np.random.randn()  # AR(1) process

# Calculate autocorrelation
df = pd.DataFrame({'value': x})
autocorr = df['value'].autocorr(lag=1)
print(f"Autocorrelation (lag=1): {autocorr:.4f}")
# Output: ~0.7 (as expected)
```

**Related Terms:** Time Series, Lag, Stationarity, ARIMA

---

### Partial Correlation

**Definition:** The correlation between two variables after controlling for the effect of one or more other variables.

**Example:**
```python
import numpy as np
import pandas as pd

np.random.seed(42)
n = 100

# Create correlated variables
x1 = np.random.randn(n)
x2 = x1 * 0.5 + np.random.randn(n) * 0.5
x3 = x2 * 0.5 + np.random.randn(n) * 0.5

df = pd.DataFrame({'x1': x1, 'x2': x2, 'x3': x3})

# Regular correlation
print("Regular correlations:")
print(df.corr())

# Partial correlation (controlling for x2)
# Simple implementation using linear regression residuals
from sklearn.linear_model import LinearRegression

# Residuals of x1 and x3 after removing x2
reg1 = LinearRegression().fit(x2.reshape(-1, 1), x1)
residuals_x1 = x1 - reg1.predict(x2.reshape(-1, 1))

reg2 = LinearRegression().fit(x2.reshape(-1, 1), x3)
residuals_x3 = x3 - reg2.predict(x2.reshape(-1, 1))

partial_corr = np.corrcoef(residuals_x1, residuals_x3)[0, 1]
print(f"\nPartial correlation (x1, x3 | x2): {partial_corr:.4f}")
```

**Related Terms:** Confounding Variables, Control Variable, Causal Inference

---

### Correlation Threshold

**Definition:** A cutoff value used to identify features for selection or removal based on their correlation with the target or other features.

**Example:**
```python
import pandas as pd
import numpy as np

np.random.seed(42)
n = 100

# Create features with varying correlations to target
f1 = np.random.randn(n)
f2 = f1 * 0.8 + np.random.randn(n) * 0.2
f3 = np.random.randn(n)
f4 = np.random.randn(n) * 0.1  # Weak correlation with target

target = f1 * 2 + f3 + np.random.randn(n) * 0.5

df = pd.DataFrame({'f1': f1, 'f2': f2, 'f3': f3, 'f4': f4, 'target': target})

# Apply threshold
threshold = 0.3
corr_with_target = df.corr()['target'].drop('target').abs()
selected = corr_with_target[corr_with_target > threshold].index.tolist()

print(f"Features with |correlation| > {threshold}:")
print(selected)
```

**Related Terms:** Feature Selection, Correlation Matrix, Multicollinearity

---

### Spurious Correlation

**Definition:** A mathematical relationship in which two or more variables are associated but not causally related, often due to coincidence or the presence of a confounding variable.

**Example:**
```python
import numpy as np

# Classic example: Nicolas Cage movies and pool drownings
# (Both increased in certain years by coincidence)

years = np.arange(2000, 2010)
cage_movies = np.array([1, 2, 1, 3, 2, 1, 2, 1, 2, 1])
pool_drownings = np.array([100, 120, 110, 130, 125, 115, 125, 105, 120, 110])

r = np.corrcoef(cage_movies, pool_drownings)[0, 1]
print(f"Correlation: {r:.4f}")
print("This is a spurious correlation!")
print("Nicolas Cage movies do NOT cause pool drownings.")
```

**Related Terms:** Confounding Variable, Causal Inference, Coincidence

---

### Outlier Effect on Correlation

**Definition:** Extreme values that can significantly distort correlation coefficients, making relationships appear stronger or weaker than they actually are.

**Example:**
```python
import numpy as np

# Data without outlier
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([2, 4, 5, 4, 6, 8, 7, 9, 10, 12])

r_original = np.corrcoef(x, y)[0, 1]
print(f"Without outlier: {r_original:.4f}")

# Add outlier
x_outlier = np.append(x, [50])
y_outlier = np.append(y, [50])

r_outlier = np.corrcoef(x_outlier, y_outlier)[0, 1]
print(f"With outlier: {r_outlier:.4f}")
# The outlier can dramatically change the correlation
```

**Related Terms:** Robust Statistics, Spearman Correlation, Data Cleaning

---

## Formulas Summary

| Formula | Expression |
|---------|-----------|
| Pearson Correlation | r = Σ[(xi - x̄)(yi - ȳ)] / √[Σ(xi - x̄)² × Σ(yi - ȳ)²] |
| Covariance | Cov(X,Y) = Σ[(xi - x̄)(yi - ȳ)] / (n - 1) |
| Coefficient of Determination | R² = r² |
| Variance Inflation Factor | VIF = 1 / (1 - R²) |
| Spearman Correlation | Based on rank differences |
| Kendall Tau | Based on concordant/discordant pairs |

---

## Code Snippets Quick Reference

```python
# Pearson correlation
import numpy as np
r = np.corrcoef(x, y)[0, 1]

# With p-value
from scipy.stats import pearsonr
r, p = pearsonr(x, y)

# Spearman correlation
from scipy.stats import spearmanr
rho, p = spearmanr(x, y)

# Kendall correlation
from scipy.stats import kendalltau
tau, p = kendalltau(x, y)

# Correlation matrix
import pandas as pd
corr_matrix = df.corr()

# Covariance matrix
cov_matrix = np.cov(x, y)

# VIF calculation
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = variance_inflation_factor(X.values, i)
```

---

## Common Pitfalls

1. **Using Pearson for non-linear relationships** — Use Spearman instead
2. **Ignoring outliers** — Check data before computing correlation
3. **Assuming causation** — Correlation ≠ Causation
4. **Not checking multicollinearity** — Use VIF for regression
5. **Using correlation on categorical data** — Use Chi-square or Cramér's V

---

## Further Reading

- [Pandas Documentation - DataFrame.corr()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html)
- [SciPy Stats - Correlation Functions](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Wikipedia - Correlation and Dependence](https://en.wikipedia.org/wiki/Correlation_and_dependence)
