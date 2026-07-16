# Glossary 16: Scatter Plots

## Quick Reference

| Method / Function | Purpose | Returns |
|-------------------|---------|---------|
| `df.plot.scatter()` | Pandas scatter plot | Axes object |
| `ax.scatter()` | Matplotlib scatter plot | PathCollection |
| `plt.colorbar()` | Add color scale legend | Colorbar |
| `sns.regplot()` | Scatter + regression line | Axes |
| `sns.lmplot()` | Scatter + regression (figure level) | FacetGrid |
| `np.polyfit()` | Fit polynomial to data | Coefficients |
| `np.poly1d()` | Create polynomial function | Callable |
| `plt.hexbin()` | 2D histogram for dense data | PolyCollection |

---

## Alphabetical Definitions

### A

**alpha**
Transparency parameter (0.0 = invisible, 1.0 = opaque). Essential for overplotting.
```python
ax.scatter(x, y, alpha=0.5)
```

**annotate()**
Adds text annotations to the plot. Useful for labeling points or adding statistics.
```python
ax.annotate(f'R² = {r2:.2f}', xy=(0.05, 0.95), xycoords='axes fraction')
```

### B

**Bubble Chart**
A scatter plot where point size encodes a third variable. Created with the `s` parameter.
```python
ax.scatter(x, y, s=df['size_var'] * 100)
```

### C

**cmap (Colormap)**
A color scheme mapping values to colors. Common colormaps: `viridis`, `coolwarm`, `RdYlGn`, `plasma`.
```python
ax.scatter(x, y, c=values, cmap='viridis')
plt.colorbar(label='Value')
```

### D

**Density Scatter**
For very large datasets, use `plt.hexbin()` or `sns.kdeplot()` to show point density instead of individual points.
```python
plt.hexbin(x, y, gridsize=20, cmap='YlOrRd')
plt.colorbar(label='Count')
```

### H

**hexbin()**
Creates a 2D histogram using hexagonal bins. Better than scatter for dense datasets with thousands of points.
```python
plt.hexbin(df['x'], df['y'], gridsize=30, cmap='Blues', mincnt=1)
```

### L

**lmplot()**
Seaborn function that creates a scatter plot with regression line. Figure-level function (creates its own figure).
```python
sns.lmplot(data=df, x='study_hours', y='exam_score', hue='group')
```

### M

**Marker Styles**
Different point shapes: `'o'` circle, `'^'` triangle, `'s'` square, `'D'` diamond, `'P'` plus, `'*'` star.
```python
ax.scatter(x, y, marker='^', s=100)
```

### O

**Overplotting**
When many data points overlap, making patterns invisible. Fix with: `alpha`, smaller markers, `hexbin()`, or `sns.kdeplot()`.
```python
# Fix overplotting
ax.scatter(x, y, s=10, alpha=0.1)
# Or use hexbin
plt.hexbin(x, y, gridsize=20, cmap='Blues')
```

### R

**regplot()**
Seaborn function that adds a regression line to a scatter plot. Shows 95% confidence interval by default.
```python
sns.regplot(data=df, x='x', y='y', scatter_kws={'alpha': 0.5})
```

### S

**scatter_kws / line_kws**
Dictionary parameters passed to scatter points or regression line in seaborn functions.
```python
sns.regplot(
    x='x', y='y', data=df,
    scatter_kws={'color': 'blue', 'alpha': 0.5},
    line_kws={'color': 'red', 'linewidth': 2}
)
```

**Subplot**
A separate axes within the same figure. Created with `plt.subplots()` for side-by-side comparison.
```python
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].scatter(x1, y1)
axes[1].scatter(x2, y2)
```

---

## Code Examples

### Example 1: Publication-Quality Scatter

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

fig, ax = plt.subplots(figsize=(8, 6))

# Simulated data
np.random.seed(42)
x = np.random.randn(200) * 10 + 50
y = x * 0.8 + np.random.randn(200) * 5

ax.scatter(x, y, c='steelblue', s=40, alpha=0.6, edgecolors='white', linewidth=0.5)

# Trend line
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
x_line = np.linspace(x.min(), x.max(), 100)
ax.plot(x_line, p(x_line), 'r--', linewidth=2, label=f'y = {z[0]:.2f}x + {z[1]:.2f}')

# R-squared
from scipy import stats
r, p_val = stats.pearsonr(x, y)
ax.annotate(f'R² = {r**2:.3f}', xy=(0.05, 0.95), xycoords='axes fraction',
            fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax.set_xlabel('Variable X', fontsize=12)
ax.set_ylabel('Variable Y', fontsize=12)
ax.set_title('Scatter Plot with Regression Line', fontsize=14)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('scatter_plot.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Example 2: Multi-Group Scatter

```python
import seaborn as sns

df = sns.load_dataset('iris')

fig, ax = plt.subplots(figsize=(10, 7))

colors = {'setosa': '#e74c3c', 'versicolor': '#3498db', 'virginica': '#2ecc71'}
markers = {'setosa': 'o', 'versicolor': '^', 'virginica': 's'}

for species in colors:
    mask = df['species'] == species
    ax.scatter(
        df.loc[mask, 'sepal_length'],
        df.loc[mask, 'petal_length'],
        c=colors[species],
        marker=markers[species],
        s=60,
        alpha=0.7,
        label=species,
        edgecolors='gray',
        linewidth=0.5
    )

ax.set_xlabel('Sepal Length (cm)', fontsize=12)
ax.set_ylabel('Petal Length (cm)', fontsize=12)
ax.set_title('Iris Dataset: Sepal vs Petal Length', fontsize=14)
ax.legend(title='Species', fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### Example 3: Dense Data with Hexbin

```python
np.random.seed(42)
n = 5000
x = np.random.randn(n)
y = x * 0.5 + np.random.randn(n) * 0.8

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: overplotting problem
axes[0].scatter(x, y, s=5, alpha=0.3, color='gray')
axes[0].set_title('Scatter (Overplotting)')
axes[0].set_xlabel('X')
axes[0].set_ylabel('Y')

# Right: hexbin solution
hb = axes[1].hexbin(x, y, gridsize=30, cmap='YlOrRd', mincnt=1)
axes[1].set_title('Hexbin (Density)')
axes[1].set_xlabel('X')
axes[1].set_ylabel('Y')
plt.colorbar(hb, ax=axes[1], label='Count')

plt.suptitle('Handling Dense Data', fontsize=14)
plt.tight_layout()
plt.show()
```

---

## Related Terms

| Term | Related To | Connection |
|------|-----------|------------|
| `alpha` | `scatter()` | Controls transparency for overplotting |
| `cmap` | `colorbar()` | Maps values to colors |
| `marker` | `scatter()` | Different point shapes per group |
| `s` | `scatter()` | Point size (bubble chart) |
| `regplot()` | `polyfit()` | Both add trend lines |
| `hexbin()` | `scatter()` | Dense-data alternative |
| `subplots()` | `scatter()` | Side-by-side comparison |

---

*See also: [Lecture 16](16-scatter-plot-lecture.md) | [Lecture 23 – Correlation](23-corr-lecture.md)*
