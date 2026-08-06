# Glossary 23: Correlation

## Quick Reference

| Method / Function | Purpose | Returns |
|-------------------|---------|---------|
| `df.corr()` | Correlation matrix | DataFrame |
| `df['a'].corr(df['b'])` | Pairwise correlation | float |
| `method='pearson'` | Linear correlation (default) | — |
| `method='spearman'` | Rank-based correlation | — |
| `method='kendall'` | Rank concordance | — |
| `sns.heatmap()` | Visualize correlation matrix | Axes |
| `sns.pairplot()` | Scatter matrix for all pairs | PairGrid |
| `np.corrcoef()` | NumPy correlation | ndarray |

---

## Alphabetical Definitions

### C

**Coefficient of Determination (R²)**
Square of the correlation coefficient. Represents the proportion of variance in one variable explained by the other.
```python
r = df['x'].corr(df['y'])
r_squared = r ** 2  # e.g., 0.51 means 51% of variance explained
```

**Correlation**
A statistical measure of the linear relationship between two variables, ranging from -1 to +1.

### K

**Kendall's Tau**
Rank-based correlation measuring the concordance of pairs. More robust than Spearman for small samples with many tied ranks.
```python
df.corr(method='kendall')
```

### M

**Monotonic Relationship**
A relationship where one variable consistently increases (or decreases) as the other increases, but not necessarily at a constant rate. Spearman captures this.
```python
# Monotonic but not linear
x = np.arange(100)
y = x ** 3  # Monotonic increasing
print(f"Pearson: {np.corrcoef(x, y)[0,1]:.3f}")  # High but not 1
print(f"Spearman: {pd.Series(x).corr(pd.Series(y), method='spearman'):.3f}")  # 1.0
```

### N

**np.corrcoef()**
NumPy function that returns the correlation matrix as an ndarray. Use `[0,1]` to extract pairwise correlation.
```python
r = np.corrcoef(x, y)[0, 1]
```

### P

**Partial Correlation**
Correlation between two variables after removing the effect of a third variable. Shows the direct relationship.
```python
# Correlation between X and Y, controlling for Z
residuals_x = X - predict(X, Z)
residuals_y = Y - predict(Y, Z)
partial_r = np.corrcoef(residuals_x, residuals_y)[0, 1]
```

**Pearson Correlation (r)**
Measures the linear relationship between two continuous variables. Assumes normality and homoscedasticity.
```python
r = df['study_hours'].corr(df['exam_score'])
```

### S

**Spearman's Rho**
Rank-based correlation. Converts values to ranks and computes Pearson on ranks. Robust to outliers and non-linearity.
```python
rho = df['x'].corr(df['y'], method='spearman')
```

**Spurious Correlation**
A mathematical relationship that exists by coincidence, not causation. Two variables may be correlated due to a hidden third variable or pure chance.

---

## Code Examples

### Example 1: Correlation Analysis

```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = sns.load_dataset('iris')

# Correlation matrix
corr = df.select_dtypes(include=[np.number]).corr()
print("Correlation Matrix:")
print(corr.round(3))

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Full heatmap
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f',
            square=True, ax=axes[0])
axes[0].set_title('Full Correlation Matrix')

# Masked heatmap
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', center=0,
            fmt='.2f', square=True, ax=axes[1])
axes[1].set_title('Lower Triangle Only')

plt.tight_layout()
plt.show()
```

### Example 2: Correlation Methods Comparison

```python
import scipy.stats as stats

# Compare methods
methods = ['pearson', 'spearman', 'kendall']
results = []

for col1 in df.select_dtypes(include=[np.number]).columns:
    for col2 in df.select_dtypes(include=[np.number]).columns:
        if col1 != col2:
            for method in methods:
                r = df[col1].corr(df[col2], method=method)
                results.append({
                    'var1': col1, 'var2': col2,
                    'method': method, 'correlation': r
                })

results_df = pd.DataFrame(results)
print(results_df.pivot_table(
    index=['var1', 'var2'],
    columns='method',
    values='correlation'
).round(3))
```

### Example 3: Correlation Filter

```python
def filter_high_correlations(corr_matrix, threshold=0.7):
    """Return pairs with correlation above threshold."""
    pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) > threshold:
                pairs.append({
                    'var1': corr_matrix.columns[i],
                    'var2': corr_matrix.columns[j],
                    'correlation': corr_matrix.iloc[i, j]
                })
    return pd.DataFrame(pairs).sort_values('correlation', key=abs, ascending=False)

print("Highly correlated pairs (|r| > 0.7):")
print(filter_high_correlations(corr))
```

---

## Related Terms

| Term | Related To | Connection |
|------|-----------|------------|
| `r` (Pearson) | `R²` | Coefficient and determination |
| `Spearman` | `Kendall` | Both rank-based methods |
| `heatmap` | `corr()` | Visual representation |
| `pairplot` | `scatter` | All variable pairs |
| `causation` | `correlation` | Correlation ≠ causation |
| `outlier` | `Pearson` | Sensitive to extreme values |

---

*See also: [Lecture 23](23-corr-lecture.md) | [Lecture 16 – Scatter Plot](16-scatter-plot-lecture.md)*
