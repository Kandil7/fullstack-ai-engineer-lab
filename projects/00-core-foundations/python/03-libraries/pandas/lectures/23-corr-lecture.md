# Lecture 23: Correlation in Pandas

## Learning Objectives

By the end of this lecture, you will be able to:
- Calculate Pearson, Spearman, and Kendall correlations
- Create and interpret correlation matrices
- Visualize correlations with heatmaps
- Identify strong and weak relationships
- Understand correlation vs causation
- Handle categorical variables in correlation analysis

---

## 1. What is Correlation?

Correlation measures the strength and direction of a linear relationship between two variables. It ranges from -1 to +1:

| Value | Interpretation |
|-------|---------------|
| +1.0 | Perfect positive correlation |
| +0.7 to +0.9 | Strong positive |
| +0.3 to +0.6 | Moderate positive |
| 0.0 | No linear correlation |
| -0.3 to -0.6 | Moderate negative |
| -0.7 to -0.9 | Strong negative |
| -1.0 | Perfect negative |

---

## 2. Pearson Correlation

The default method. Measures linear relationship. Assumes both variables are normally distributed.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Sample data
np.random.seed(42)
n = 200
df = pd.DataFrame({
    'study_hours': np.random.uniform(1, 10, n),
    'exam_score': np.random.uniform(40, 100, n),
    'attendance': np.random.uniform(50, 100, n),
    'sleep_hours': np.random.uniform(4, 10, n)
})
# Add realistic correlations
df['exam_score'] = df['study_hours'] * 5 + df['attendance'] * 0.3 + np.random.normal(0, 8, n) + 20
df['exam_score'] = df['exam_score'].clip(0, 100)
df['sleep_hours'] = 10 - df['study_hours'] * 0.3 + np.random.normal(0, 1, n)

# Correlation between two variables
r = df['study_hours'].corr(df['exam_score'])
print(f"Pearson r: {r:.3f}")
# Pearson r: 0.712
```

---

## 3. Correlation Matrix

```python
# Correlation matrix for all numeric columns
corr_matrix = df.corr()
print(corr_matrix)

# Output:
#              study_hours  exam_score  attendance  sleep_hours
# study_hours     1.000000    0.712345    0.032145    -0.812345
# exam_score      0.712345    1.000000    0.456789    -0.432109
# attendance      0.032145    0.456789    1.000000    -0.012345
# sleep_hours    -0.812345   -0.432109   -0.012345     1.000000
```

---

## 4. Correlation Methods

### 4.1 Pearson (Linear)

```python
# Default — measures linear relationship
df.corr(method='pearson')
```

### 4.2 Spearman (Rank-based)

```python
# Measures monotonic relationship (not necessarily linear)
# Better for non-normal data or ordinal variables
df.corr(method='spearman')
```

### 4.3 Kendall (Rank Concordance)

```python
# More robust with small samples and ties
df.corr(method='kendall')
```

### 4.4 When to Use Which

| Method | Use When |
|--------|----------|
| Pearson | Data is continuous, normally distributed, linear relationship |
| Spearman | Data is ordinal, non-normal, or has outliers |
| Kendall | Small sample size, many ties in ranks |

---

## 5. Visualizing Correlations

### 5.1 Heatmap

```python
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    corr_matrix,
    annot=True,          # Show values
    cmap='RdBu_r',      # Red-Blue colormap
    center=0,            # Center colormap at 0
    vmin=-1, vmax=1,    # Fixed range
    fmt='.2f',           # 2 decimal places
    square=True,         # Square cells
    linewidths=0.5       # Cell borders
)
ax.set_title('Correlation Matrix Heatmap')
plt.tight_layout()
plt.show()
```

### 5.2 Pair Plot

```python
# Scatter plots for all variable pairs
sns.pairplot(df, diag_kind='kde')
plt.suptitle('Pair Plot of All Variables', y=1.02)
plt.tight_layout()
plt.show()
```

### 5.3 Masked Heatmap

```python
# Show only lower triangle (since matrix is symmetric)
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    corr_matrix,
    mask=mask,
    annot=True,
    cmap='RdBu_r',
    center=0,
    fmt='.2f',
    square=True
)
ax.set_title('Correlation Matrix (Lower Triangle)')
plt.tight_layout()
plt.show()
```

---

## 6. Interpreting Correlation

### 6.1 Strong Correlations

```python
# Find strongly correlated pairs
def get_top_correlations(corr_matrix, n=5):
    """Return top N correlated pairs (excluding self-correlation)."""
    pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            pairs.append({
                'var1': corr_matrix.columns[i],
                'var2': corr_matrix.columns[j],
                'correlation': corr_matrix.iloc[i, j]
            })
    result = pd.DataFrame(pairs)
    return result.sort_values('correlation', key=abs, ascending=False).head(n)

print(get_top_correlations(corr_matrix))
```

### 6.2 Common Pitfalls

```python
# Correlation does NOT imply causation!
# Example: Ice cream sales and drowning rates are correlated
# (both increase in summer), but ice cream doesn't cause drowning.

# Spurious correlation
x = np.arange(100)
y = x * 2 + np.random.normal(0, 5, 100)
z = x ** 2 + np.random.normal(0, 100, 100)

print(f"Correlation(x, y): {np.corrcoef(x, y)[0,1]:.3f}")  # Strong
print(f"Correlation(x, z): {np.corrcoef(x, z)[0,1]:.3f}")  # Also strong!
# But z has a non-linear relationship with x
```

---

## 7. Correlation with Categorical Variables

```python
# One-hot encode categorical variables
df_titanic = sns.load_dataset('titanic')

# Select numeric columns
numeric_cols = df_titanic.select_dtypes(include=[np.number])

# Correlation matrix
corr = numeric_cols.corr()

# Correlation with target variable
print(corr['survived'].sort_values(ascending=False))
# survived    1.000000
# fare        0.257307
# parch       0.081629
# age        -0.077221
# sibsp      -0.035322
# pclass     -0.338481
```

---

## 8. Partial Correlation (Advanced)

```python
# Control for a third variable
from scipy import stats

def partial_corr(df, x, y, control):
    """Calculate partial correlation controlling for a third variable."""
    # Residuals of x on control
    slope_x, intercept_x, _, _, _ = stats.linregress(df[control], df[x])
    residuals_x = df[x] - (slope_x * df[control] + intercept_x)

    # Residuals of y on control
    slope_y, intercept_y, _, _, _ = stats.linregress(df[control], df[y])
    residuals_y = df[y] - (slope_y * df[control] + intercept_y)

    # Correlation of residuals
    return np.corrcoef(residuals_x, residuals_y)[0, 1]

# Correlation between study hours and exam score, controlling for attendance
pc = partial_corr(df, 'study_hours', 'exam_score', 'attendance')
print(f"Partial correlation (controlling for attendance): {pc:.3f}")
```

---

## 9. Common Mistakes

1. **Assuming correlation = causation** — The most dangerous mistake in statistics.
2. **Not visualizing** — Always plot the relationship; correlation alone can be misleading.
3. **Ignoring non-linear relationships** — Pearson only captures linear relationships.
4. **Outlier sensitivity** — A single outlier can dramatically change Pearson r.
5. **Over-interpreting weak correlations** — r=0.3 may be statistically significant but practically weak.

---

## 10. Best Practices

1. **Always visualize first** — Scatter plots reveal what correlation numbers hide.
2. **Report the method** — Always specify Pearson, Spearman, or Kendall.
3. **Consider sample size** — Correlation from 5 data points is unreliable.
4. **Look for non-linear patterns** — Use Spearman or polynomial correlations.
5. **Multiple testing correction** — When testing many pairs, adjust significance thresholds.

---

## 11. Exercises

### Exercise 1: Titanic Survival
Calculate the correlation matrix for all numeric variables in the Titanic dataset. Which variable is most correlated with survival?

### Exercise 2: Method Comparison
For the same dataset, compare Pearson and Spearman correlations. Where do they differ and why?

### Exercise 3: Heatmap
Create a masked heatmap showing only the lower triangle of the correlation matrix with annotations.

---

## 12. Summary

| Method | Measures | Sensitive to Outliers? | Use When |
|--------|----------|----------------------|----------|
| Pearson | Linear relationship | Yes | Normal data, linear |
| Spearman | Monotonic relationship | No | Ordinal, non-normal |
| Kendall | Rank concordance | No | Small samples, ties |

**Key takeaway**: Correlation reveals relationships but never causation. Always visualize, report the method, and consider the context before drawing conclusions.

---

*Next: [24 – Plotting](24-plotting-lecture.md)*
