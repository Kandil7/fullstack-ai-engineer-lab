# Matplotlib Lecture 13: Box Plots

## 🎯 Topic Overview

Box plots (box-and-whisker plots) summarize distributions through five statistics: minimum, first quartile (Q1), median (Q2), third quartile (Q3), and maximum. They excel at comparing multiple distributions side-by-side.

## 📚 Learning Objectives

1. Create single and grouped box plots
2. Interpret the five-number summary and outliers
3. Customize box plot appearance
4. Add swarm plots and violins as complementary views

---

## 1. Basic Box Plot

```python
import matplotlib.pyplot as plt
import numpy as np

# Generate 3 datasets
data = [np.random.normal(0, std, 100) for std in [1, 2, 3]]

plt.figure(figsize=(10, 6))
plt.boxplot(data, labels=['Group A', 'Group B', 'Group C'],
            patch_artist=True)
plt.title('Distribution Comparison')
plt.ylabel('Value')
plt.grid(True, axis='y', alpha=0.3)
plt.show()
```

### Anatomy of a Box Plot

```
    Upper Whisker (max within 1.5×IQR)
    ─────────────────
           │
    ┌──── Box ────┐
    │   Q3 (75%)   │
    │   Median     │
    │   Q1 (25%)   │
    └──────────────┘
           │
    ─────────────────
    Lower Whisker (min within 1.5×IQR)
    
    ○  Outliers (beyond 1.5×IQR)
```

---

## 2. Customized Box Plot

```python
plt.boxplot(data,
    patch_artist=True,           # Fill boxes with color
    showmeans=True,              # Show mean marker
    meanline=True,               # Show mean as line
    notch=True,                  # Notched box (shows CI of median)
    vert=True,                   # Vertical (False for horizontal)
    widths=0.6,                  # Box width
    showfliers=True,             # Show outliers
    boxprops={'facecolor': 'steelblue', 'alpha': 0.7},
    medianprops={'color': 'red', 'linewidth': 2},
    whiskerprops={'color': 'black', 'linewidth': 1.5},
    capprops={'color': 'black', 'linewidth': 1.5},
    flierprops={'marker': 'o', 'markerfacecolor': 'red', 'markersize': 6}
)
```

---

## 3. Box Plot + Swarm Overlay

```python
# Box plot with individual points
bp = plt.boxplot(data, patch_artist=True)
for i, dataset in enumerate(data, 1):
    # Add jittered points
    jitter = np.random.normal(i, 0.04, len(dataset))
    plt.scatter(jitter, dataset, alpha=0.4, s=15, color='black')
```

---

## Practice Exercises

1. Create box plots comparing 4 distributions with different sample sizes
2. Customize box colors, median lines, and outlier markers
3. Overlay a violin plot with a box plot for richer comparison
