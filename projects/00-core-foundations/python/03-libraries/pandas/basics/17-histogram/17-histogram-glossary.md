# Glossary 17: Histograms

## Quick Reference

| Method / Function | Purpose | Returns |
|-------------------|---------|---------|
| `df.plot.hist()` | Pandas histogram | Axes |
| `ax.hist()` | Matplotlib histogram | Axes |
| `sns.histplot()` | Seaborn histogram with KDE | Axes |
| `density=True` | Normalize to density scale | — |
| `bins` | Number of bins | int or array |
| `range` | Bin range (min, max) | tuple |
| `cumulative=True` | Cumulative histogram | — |
| `stacked=True` | Stack multiple histograms | — |
| `edgecolor` | Border color for bars | color string |
| `alpha` | Bar transparency | float (0–1) |
| `plt.hist2d()` | 2D histogram | Axes |

---

## Alphabetical Definitions

### B

**Bin (Class Interval)**
A range of values into which data points are grouped. The number and width of bins affect the histogram's appearance.
```python
ax.hist(data, bins=30)           # 30 equal-width bins
ax.hist(data, bins=[0,10,20,30]) # Custom bin edges
```

**Bin Width**
The range covered by each bin. `bin_width = (max - min) / num_bins`.
```python
# Fixed bin width
bin_width = 5
bins = np.arange(0, 100 + bin_width, bin_width)
ax.hist(data, bins=bins)
```

### C

**Cumulative Histogram**
Shows running totals — each bar includes all values below it. Useful for percentiles.
```python
ax.hist(data, bins=30, cumulative=True, histtype='step')
```

### D

**Density Histogram**
Normalizes the histogram so the total area equals 1. Allows comparison of distributions with different sample sizes.
```python
ax.hist(data, bins=30, density=True)
```

### E

**edgecolor**
Sets the border color of histogram bars. White edges improve readability when bars are close.
```python
ax.hist(data, edgecolor='white', linewidth=0.5)
```

### F

**Frequency**
The count of observations in each bin. Default y-axis for histograms.
```python
ax.hist(data, bins=20)  # Y-axis = frequency
```

**Freedman-Diaconis Rule**
Automatic bin width selection: `2 * IQR * n^(-1/3)`. More robust than Sturges for skewed data.

### H

**hist2d()**
Creates a 2D histogram for visualizing the joint distribution of two continuous variables.
```python
plt.hist2d(x, y, bins=30, cmap='Blues')
plt.colorbar(label='Count')
```

**Histogram vs Bar Chart**
Histograms show distributions of continuous data (no gaps between bars). Bar charts compare discrete categories (gaps between bars).

### K

**KDE (Kernel Density Estimate)**
A smooth curve that estimates the probability density function. Overlay on histograms for a cleaner shape visualization.
```python
sns.histplot(data, kde=True)
```

### N

**Normal Distribution**
Bell-shaped, symmetric distribution. Mean = median = mode. About 68% of data within 1 std dev.
```python
data = np.random.normal(0, 1, 1000)
ax.hist(data, bins=30, density=True)
```

### S

**Skewness**
Asymmetry of a distribution. Right-skewed (positive) has a longer right tail. Left-skewed (negative) has a longer left tail.
```python
from scipy.stats import skew
print(f"Skewness: {skew(data):.2f}")
```

**Stacked Histogram**
Overlays multiple histograms on top of each other. Shows both individual and total contributions.
```python
ax.hist([data1, data2], stacked=True, label=['Group A', 'Group B'])
```

**Sturges' Rule**
Automatic bin count: `bins = 1 + 3.322 * log10(n)`. Good for normally distributed data.

---

## Code Examples

### Example 1: Histogram with Annotations

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = np.random.normal(70, 15, 500)

fig, ax = plt.subplots(figsize=(10, 6))

counts, bins, patches = ax.hist(data, bins=30, color='steelblue',
                                  edgecolor='white', alpha=0.8, density=True)

# Add mean and median lines
ax.axvline(data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {data.mean():.1f}')
ax.axvline(np.median(data), color='green', linestyle='-', linewidth=2, label=f'Median: {np.median(data):.1f}')

# Add KDE
from scipy.stats import gaussian_kde
kde = gaussian_kde(data)
x_kde = np.linspace(data.min(), data.max(), 200)
ax.plot(x_kde, kde(x_kde), color='purple', linewidth=2, label='KDE')

ax.set_title('Score Distribution', fontsize=14)
ax.set_xlabel('Score', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
```

### Example 2: Multi-Group Histogram

```python
import seaborn as sns

df = sns.load_dataset('titanic')

fig, ax = plt.subplots(figsize=(10, 6))

for pclass, color, label in [(1, '#e74c3c', '1st Class'),
                               (2, '#3498db', '2nd Class'),
                               (3, '#2ecc71', '3rd Class')]:
    data = df[df['pclass'] == pclass]['age'].dropna()
    ax.hist(data, bins=20, alpha=0.5, color=color, label=label, density=True)

ax.set_title('Age Distribution by Passenger Class')
ax.set_xlabel('Age')
ax.set_ylabel('Density')
ax.legend(title='Class')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
```

### Example 3: Custom Binning

```python
# Custom bins with specific edges
bins = [0, 18, 25, 35, 45, 55, 65, 75, 100]
labels = ['<18', '18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+']

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df['age'].dropna(), bins=bins, color='steelblue', edgecolor='white', alpha=0.8)
ax.set_xticks(bins)
ax.set_xticklabels(labels, rotation=45)
ax.set_title('Age Distribution (Custom Bins)')
ax.set_xlabel('Age Group')
ax.set_ylabel('Count')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Related Terms

| Term | Related To | Connection |
|------|-----------|------------|
| `bins` | `hist()` | Number or edges of bins |
| `density` | `KDE` | Normalized vs. smooth estimate |
| `skewness` | Distribution shape | Right/left tail direction |
| `KDE` | `sns.histplot(kde=True)` | Smooth density overlay |
| `cumulative` | Percentile calculation | Running total histogram |
| `hexbin()` | 2D histogram | For scatter plot density |

---

*See also: [Lecture 17](17-histogram-lecture.md) | [Lecture 15 – Statistics](15-statistics-lecture.md)*
