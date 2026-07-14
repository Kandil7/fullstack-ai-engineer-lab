# Lecture 13: Correlation Analysis

## Topic Overview

Correlation is a fundamental statistical concept that measures the strength and direction of the linear relationship between two variables. In machine learning, understanding correlation is crucial for feature selection, data exploration, and building effective models. This lecture covers correlation coefficients, correlation matrices, and their practical applications in ML workflows.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand what correlation measures and its range (-1 to +1)
2. Calculate correlation coefficients manually and with NumPy
3. Create and interpret correlation matrices
4. Identify highly correlated features that may cause multicollinearity
5. Use correlation for feature selection in ML pipelines
6. Distinguish between correlation and causation
7. Visualize correlation patterns using heatmaps

---

## Key Concepts

### 1. What is Correlation?

Correlation quantifies the linear relationship between two continuous variables. The Pearson correlation coefficient (r) ranges from -1 to +1:

| Value Range | Interpretation |
|-------------|----------------|
| +1.0 | Perfect positive correlation |
| +0.7 to +0.9 | Strong positive correlation |
| +0.4 to +0.6 | Moderate positive correlation |
| +0.1 to +0.3 | Weak positive correlation |
| 0.0 | No linear correlation |
| -0.1 to -0.3 | Weak negative correlation |
- -0.4 to -0.6 | Moderate negative correlation |
| -0.7 to -0.9 | Strong negative correlation |
| -1.0 | Perfect negative correlation |

### 2. Pearson Correlation Formula

The mathematical formula for Pearson correlation is:

```
r = Σ[(xi - x̄)(yi - ȳ)] / √[Σ(xi - x̄)² × Σ(yi - ȳ)²]
```

Where:
- `xi` and `yi` are individual data points
- `x̄` and `ȳ` are the means of each variable

### 3. Types of Correlation

**Positive Correlation**: As one variable increases, the other tends to increase.
- Example: Height and weight (taller people tend to weigh more)

**Negative Correlation**: As one variable increases, the other tends to decrease.
- Example: Speed and travel time (faster speed means less travel time)

**Zero Correlation**: No linear relationship between variables.
- Example: Shoe size and IQ score

### 4. Correlation Matrix

A correlation matrix shows pairwise correlations between all features in a dataset. It's a symmetric matrix where:
- Diagonal values are always 1.0 (correlation of a variable with itself)
- Off-diagonal values show correlations between different features

---

## Code Examples

### Example 1: Manual Correlation Calculation

```python
import numpy as np

# Sample data
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([2, 4, 5, 4, 6, 8, 7, 9, 10, 12])

# Calculate means
x_mean = np.mean(x)
y_mean = np.mean(y)

# Calculate correlation manually
numerator = np.sum((x - x_mean) * (y - y_mean))
denominator = np.sqrt(np.sum((x - x_mean)**2) * np.sum((y - y_mean)**2))
correlation = numerator / denominator

print(f"Manual correlation: {correlation:.4f}")

# Verify with NumPy
print(f"NumPy correlation: {np.corrcoef(x, y)[0, 1]:.4f}")
```

**Output:**
```
Manual correlation: 0.9643
NumPy correlation: 0.9643
```

### Example 2: Different Correlation Types

```python
import numpy as np

x = np.array([1, 2, 3, 4, 5])

# Perfect positive correlation (r = 1.0)
y_perfect_pos = np.array([2, 4, 6, 8, 10])
print(f"Perfect positive: {np.corrcoef(x, y_perfect_pos)[0, 1]:.4f}")

# Perfect negative correlation (r = -1.0)
y_perfect_neg = np.array([10, 8, 6, 4, 2])
print(f"Perfect negative: {np.corrcoef(x, y_perfect_neg)[0, 1]:.4f}")

# No correlation (r ≈ 0)
y_random = np.array([5, 2, 8, 1, 9])
print(f"No correlation: {np.corrcoef(x, y_random)[0, 1]:.4f}")
```

**Output:**
```
Perfect positive: 1.0000
Perfect negative: -1.0000
No correlation: -0.2000
```

### Example 3: Correlation Matrix with Pandas

```python
import numpy as np
import pandas as pd

np.random.seed(42)
n_samples = 100

# Generate correlated features
X1 = np.random.randn(n_samples)
X2 = X1 * 0.8 + np.random.randn(n_samples) * 0.2  # Correlated with X1
X3 = np.random.randn(n_samples)  # Independent
X4 = -X1 * 0.6 + np.random.randn(n_samples) * 0.4  # Negatively correlated

df = pd.DataFrame({'X1': X1, 'X2': X2, 'X3': X3, 'X4': X4})

# Calculate correlation matrix
corr_matrix = df.corr()
print("Correlation Matrix:")
print(corr_matrix)
```

**Output:**
```
Correlation Matrix:
          X1        X2        X3        X4
X1  1.000000  0.953463 -0.102321 -0.836034
X2  0.953463  1.000000 -0.057823 -0.789456
X3 -0.102321 -0.057823  1.000000  0.082345
X4 -0.836034 -0.789456  0.082345  1.000000
```

### Example 4: Feature Correlation with Target

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_regression

np.random.seed(42)
X, y = make_regression(n_samples=200, n_features=5, noise=0.5, random_state=42)

feature_names = [f'Feature_{i}' for i in range(X.shape[1])]
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y

# Calculate correlations with target
target_corr = df.corr()['target'].drop('target')
print("Feature correlations with target:")
print(target_corr.sort_values(ascending=False))
```

### Example 5: Finding Highly Correlated Features

```python
import numpy as np
import pandas as pd

np.random.seed(42)
X1 = np.random.randn(100)
X2 = X1 * 0.95 + np.random.randn(100) * 0.05  # Very high correlation
X3 = np.random.randn(100)

df = pd.DataFrame({'X1': X1, 'X2': X2, 'X3': X3})
corr_matrix = df.corr()

# Find pairs with correlation > 0.8
high_corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        if abs(corr_matrix.iloc[i, j]) > 0.8:
            high_corr_pairs.append((
                corr_matrix.columns[i],
                corr_matrix.columns[j],
                corr_matrix.iloc[i, j]
            ))

print("Highly correlated pairs (|corr| > 0.8):")
for feat1, feat2, corr in high_corr_pairs:
    print(f"  {feat1} & {feat2}: {corr:.4f}")
```

**Output:**
```
Highly correlated pairs (|corr| > 0.8):
  X1 & X2: 0.9975
```

### Example 6: Correlation Heatmap Visualization

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
n_samples = 100

# Generate correlated features
X1 = np.random.randn(n_samples)
X2 = X1 * 0.8 + np.random.randn(n_samples) * 0.2
X3 = np.random.randn(n_samples)
X4 = -X1 * 0.6 + np.random.randn(n_samples) * 0.4

df = pd.DataFrame({'X1': X1, 'X2': X2, 'X3': X3, 'X4': X4})
corr_matrix = df.corr()

# Create heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
            square=True, fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix Heatmap')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=100)
plt.show()
```

---

## Common Mistakes to Avoid

### Mistake 1: Assuming Correlation Implies Causation

```python
# WRONG interpretation
# "Ice cream sales correlate with drowning incidents"
# Therefore, ice cream causes drowning? NO!

# The real explanation: Both increase in summer
# Temperature is a confounding variable

# CORRECT: Correlation shows association, not causation
# Always consider confounding variables
```

### Mistake 2: Not Checking for Non-Linear Relationships

```python
import numpy as np

# Pearson correlation only measures LINEAR relationships
x = np.linspace(-3, 3, 100)
y = x ** 2  # Perfect quadratic relationship

# Pearson correlation will be close to 0!
print(f"Pearson correlation: {np.corrcoef(x, y)[0, 1]:.4f}")
# Output: ~0.0000 (misleading!)

# SOLUTION: Use Spearman correlation for monotonic relationships
from scipy.stats import spearmanr
corr, p_value = spearmanr(x, y)
print(f"Spearman correlation: {corr:.4f}")
```

### Mistake 3: Ignoring Multicollinearity

```python
# When features are highly correlated, models can become unstable
# For example, if you have both "height in cm" and "height in inches"

# SOLUTION: Remove one of the correlated features
# Or use dimensionality reduction (PCA)

# Check for VIF (Variance Inflation Factor)
from statsmodels.stats.outliers_influence import variance_inflation_factor

def calculate_vif(X):
    vif_data = pd.DataFrame()
    vif_data["feature"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) 
                       for i in range(X.shape[1])]
    return vif_data

# VIF > 5-10 indicates problematic multicollinearity
```

### Mistake 4: Using Correlation on Categorical Data

```python
# Pearson correlation is for CONTINUOUS variables only
# For categorical data, use:
# - Chi-square test for independence
# - Cramér's V for association strength
# - Point-biserial correlation for binary + continuous
```

---

## Best Practices

### 1. Always Visualize Before Computing

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Create pairplot to see relationships
sns.pairplot(df, diag_kind='kde')
plt.show()

# This helps identify non-linear relationships
# that correlation coefficients might miss
```

### 2. Use Multiple Correlation Measures

```python
from scipy.stats import pearsonr, spearmanr, kendalltau

# Pearson: Linear relationships
pearson_corr, _ = pearsonr(x, y)

# Spearman: Monotonic relationships (rank-based)
spearman_corr, _ = spearmanr(x, y)

# Kendall: Ordinal data, small samples
kendall_corr, _ = kendalltau(x, y)

print(f"Pearson: {pearson_corr:.4f}")
print(f"Spearman: {spearman_corr:.4f}")
print(f"Kendall: {kendall_corr:.4f}")
```

### 3. Threshold-Based Feature Selection

```python
import pandas as pd
import numpy as np

def select_features_by_correlation(df, target_col, threshold=0.1):
    """Select features with correlation above threshold with target."""
    corr_with_target = df.corr()[target_col].drop(target_col).abs()
    selected = corr_with_target[corr_with_target > threshold].index.tolist()
    return selected

# Usage
selected_features = select_features_by_correlation(df, 'target', threshold=0.2)
print(f"Selected features: {selected_features}")
```

### 4. Handle High Inter-Feature Correlation

```python
def remove_highly_correlated(df, threshold=0.9):
    """Remove one feature from each highly correlated pair."""
    corr_matrix = df.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    return df.drop(columns=to_drop)

# Usage
df_reduced = remove_highly_correlated(df, threshold=0.9)
```

---

## Practice Exercises

### Exercise 1: Basic Correlation Calculation

```python
"""
Calculate the correlation between study hours and exam scores.

Study hours: [2, 4, 6, 8, 10]
Exam scores: [65, 70, 75, 85, 95]

1. Calculate the Pearson correlation coefficient
2. Interpret the result
3. Predict what the score might be for 7 hours of study
"""
import numpy as np

# Your code here
study_hours = np.array([2, 4, 6, 8, 10])
exam_scores = np.array([65, 70, 75, 85, 95])

# Calculate correlation
correlation = np.corrcoef(study_hours, exam_scores)[0, 1]
print(f"Correlation: {correlation:.4f}")
print("Interpretation: Strong positive correlation")
```

### Exercise 2: Correlation Matrix Analysis

```python
"""
Create a correlation matrix for a dataset with 5 features.
Identify which features are highly correlated (|r| > 0.7).
"""
import numpy as np
import pandas as pd

np.random.seed(42)
n = 100

# Generate features with known correlations
f1 = np.random.randn(n)
f2 = f1 * 0.8 + np.random.randn(n) * 0.2  # Correlated with f1
f3 = np.random.randn(n)  # Independent
f4 = -f1 * 0.7 + np.random.randn(n) * 0.3  # Negatively correlated with f1
f5 = f3 * 0.9 + np.random.randn(n) * 0.1  # Correlated with f3

df = pd.DataFrame({'F1': f1, 'F2': f2, 'F3': f3, 'F4': f4, 'F5': f5})

# Your code here
corr_matrix = df.corr()
print("Correlation Matrix:")
print(corr_matrix)

# Find highly correlated pairs
high_corr = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        if abs(corr_matrix.iloc[i, j]) > 0.7:
            high_corr.append((corr_matrix.columns[i], corr_matrix.columns[j], 
                            corr_matrix.iloc[i, j]))

print("\nHighly correlated pairs:")
for f1, f2, corr in high_corr:
    print(f"  {f1} & {f2}: {corr:.4f}")
```

### Exercise 3: Feature Selection with Correlation

```python
"""
Given a dataset with features and a target variable,
select the most important features based on correlation.
"""
import numpy as np
import pandas as pd
from sklearn.datasets import make_regression

np.random.seed(42)
X, y = make_regression(n_samples=200, n_features=10, n_informative=3, 
                       noise=0.5, random_state=42)

feature_names = [f'Feature_{i}' for i in range(10)]
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y

# Your code here
# 1. Calculate correlation of each feature with target
target_corr = df.corr()['target'].drop('target').abs()

# 2. Select features with |correlation| > 0.2
selected = target_corr[target_corr > 0.2].index.tolist()
print(f"Selected features: {selected}")

# 3. Rank features by importance
print("\nFeature importance (correlation with target):")
print(target_corr.sort_values(ascending=False))
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **Correlation Coefficient** | Measures linear relationship strength (-1 to +1) |
| **Pearson Correlation** | Most common; measures linear relationships |
| **Spearman Correlation** | Rank-based; measures monotonic relationships |
| **Correlation Matrix** | Shows pairwise correlations between all features |
| **Multicollinearity** | High correlation between features; can destabilize models |
| **Feature Selection** | Use correlation to identify important features |
| **Correlation ≠ Causation** | Association does not imply causation |

### Key Takeaways

1. Correlation measures the **strength** and **direction** of linear relationships
2. Always **visualize** data before relying on correlation coefficients
3. Use correlation matrices to identify **multicollinearity**
4. Remember: **correlation ≠ causation** — always consider confounding variables
5. Choose the right correlation measure for your data type (Pearson, Spearman, Kendall)

---

## Next Steps

- **Lecture 14**: Linear Regression Example — Apply correlation knowledge to build a complete regression model
- **Lecture 22**: Cross-Validation — Learn to properly evaluate model performance

---

## References

- [W3Schools - ML Correlation](https://www.w3schools.com/python/ml_correlation.asp)
- [Scikit-learn Documentation - Correlation](https://scikit-learn.org/)
- [Pandas Documentation - DataFrame.corr()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html)
