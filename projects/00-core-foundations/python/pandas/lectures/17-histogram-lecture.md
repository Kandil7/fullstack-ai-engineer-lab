# Lecture 17: Histograms in Pandas

## Learning Objectives

By the end of this lecture, you will be able to:
- Create histograms to visualize data distributions
- Choose appropriate bin sizes and counts
- Overlay multiple distributions for comparison
- Add KDE (Kernel Density Estimate) curves
- Create stacked and grouped histograms
- Interpret distribution shapes (normal, skewed, bimodal)
- Customize axes, labels, and styling

---

## 1. What is a Histogram?

A histogram divides data into bins and counts how many observations fall into each bin. Unlike a bar chart (which compares categories), a histogram shows the **distribution of a single continuous variable**.

---

## 2. Basic Histogram

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample data
np.random.seed(42)
df = pd.DataFrame({
    'age': np.random.normal(35, 10, 1000).clip(18, 80),
    'income': np.random.lognormal(10.5, 0.8, 1000),
    'score': np.random.beta(5, 2, 1000) * 100
})

# Basic histogram using pandas
df['age'].plot.hist(bins=20, figsize=(10, 6))
plt.title('Distribution of Age')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
```

### 2.1 Matplotlib Version

```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df['age'], bins=25, color='steelblue', edgecolor='white', alpha=0.8)
ax.set_title('Distribution of Age')
ax.set_xlabel('Age')
ax.set_ylabel('Frequency')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 3. Choosing Bin Size

### 3.1 Different Bin Counts

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].hist(df['age'], bins=10, color='steelblue', edgecolor='white')
axes[0].set_title('10 bins (too coarse)')

axes[1].hist(df['age'], bins=50, color='steelblue', edgecolor='white')
axes[1].set_title('50 bins (too fine)')

axes[2].hist(df['age'], bins=30, color='steelblue', edgecolor='white')
axes[2].set_title('30 bins (just right)')

for ax in axes:
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    ax.grid(axis='y', alpha=0.3)

plt.suptitle('Effect of Bin Count on Histogram Shape', fontsize=14)
plt.tight_layout()
plt.show()
```

### 3.2 Automatic Binning Rules

```python
# Sturges' rule: bins = 1 + 3.322 * log10(n)
n = len(df)
sturges_bins = int(1 + 3.322 * np.log10(n))
print(f"Sturges' rule suggests {sturges_bins} bins")

# Freedman-Diaconis rule
from scipy import stats
q75, q25 = np.percentile(df['age'], [75, 25])
iqr = q75 - q25
bin_width = 2 * iqr / (n ** (1/3))
fd_bins = int((df['age'].max() - df['age'].min()) / bin_width)
print(f"Freedman-Diaconis suggests {fd_bins} bins")
```

---

## 4. Normalized Histograms (Density)

```python
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Frequency
axes[0].hist(df['age'], bins=25, color='steelblue', edgecolor='white')
axes[0].set_title('Frequency Histogram')
axes[0].set_ylabel('Count')

# Density (area sums to 1)
axes[1].hist(df['age'], bins=25, density=True, color='coral', edgecolor='white')
axes[1].set_title('Density Histogram')
axes[1].set_ylabel('Density')

for ax in axes:
    ax.set_xlabel('Age')
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 5. Histogram with KDE Overlay

```python
import seaborn as sns

# With KDE curve
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=df, x='age', bins=25, kde=True, color='steelblue', ax=ax)
ax.set_title('Age Distribution with KDE')
ax.set_xlabel('Age')
ax.set_ylabel('Count')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 6. Multiple Distributions

### 6.1 Overlapping Histograms

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(df['age'], bins=25, alpha=0.5, label='Age', color='steelblue')
ax.hist(df['score'], bins=25, alpha=0.5, label='Score', color='coral')

ax.set_title('Age vs Score Distributions')
ax.set_xlabel('Value')
ax.set_ylabel('Frequency')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
```

### 6.2 Stacked Histogram

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(
    [df['age'], df['score']],
    bins=25,
    label=['Age', 'Score'],
    color=['steelblue', 'coral'],
    stacked=True,
    alpha=0.7
)

ax.set_title('Stacked Histogram: Age vs Score')
ax.set_xlabel('Value')
ax.set_ylabel('Frequency')
ax.legend()
plt.tight_layout()
plt.show()
```

### 6.3 Faceted Histograms by Category

```python
df_titanic = sns.load_dataset('titanic')

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, pclass in enumerate([1, 2, 3]):
    mask = df_titanic['pclass'] == pclass
    axes[i].hist(df_titanic.loc[mask, 'age'].dropna(), bins=20,
                 color=['#e74c3c', '#3498db', '#2ecc71'][i],
                 edgecolor='white', alpha=0.8)
    axes[i].set_title(f'Class {pclass}')
    axes[i].set_xlabel('Age')
    axes[i].set_ylabel('Count')
    axes[i].grid(axis='y', alpha=0.3)

plt.suptitle('Age Distribution by Passenger Class', fontsize=14)
plt.tight_layout()
plt.show()
```

---

## 7. Interpreting Distribution Shapes

| Shape | Description | Example |
|-------|-------------|---------|
| Normal (bell) | Symmetric, centered | Heights, test scores |
| Right-skewed | Tail extends right | Income, house prices |
| Left-skewed | Tail extends left | Exam scores (easy test) |
| Bimodal | Two peaks | Two distinct groups |
| Uniform | Flat distribution | Random numbers |
| Heavy-tailed | More extreme values | Stock returns |

---

## 8. Common Mistakes

1. **Too few bins** — Masks the true shape. Use 20–50 bins for most datasets.
2. **Too many bins** — Creates noise. Each bin should have multiple observations.
3. **Using bar charts instead** — Bar charts compare categories; histograms show distributions.
4. **Not labeling axes** — Always include title, x-label, y-label.
5. **Ignoring outliers** — Extreme values can make the main distribution invisible.

---

## 9. Best Practices

1. **Start with 25-30 bins** — Adjust based on data size and shape.
2. **Use `density=True`** when comparing distributions of different sizes.
3. **Overlay KDE** for a smooth shape estimate.
4. **Use consistent bin edges** when comparing groups.
5. **Check for skewness** — It affects which statistics are appropriate.

---

## 10. Exercises

### Exercise 1: Income Distribution
Create a histogram of log-normal income data with 30 bins, KDE overlay, and a vertical line at the median.

### Exercise 2: Group Comparison
Using the Titanic dataset, create overlapping histograms of `fare` for each `pclass`.

### Exercise 3: Distribution Shape
Generate 1000 values from each of these distributions (normal, uniform, exponential) and create a 3-panel histogram figure.

---

## 11. Summary

| Feature | Method |
|---------|--------|
| Basic histogram | `df.plot.hist()` or `ax.hist()` |
| With KDE | `sns.histplot(kde=True)` |
| Density mode | `density=True` parameter |
| Multiple distributions | Overlapping `ax.hist()` calls |
| Stacked | `stacked=True` parameter |
| Faceted by category | Loop over groups |

**Key takeaway**: Histograms reveal the shape of your data distribution — normal, skewed, bimodal, or uniform. This shape determines which statistical methods are appropriate.

---

*Next: [18 – Pie Chart](18-pie-chart-lecture.md)*
