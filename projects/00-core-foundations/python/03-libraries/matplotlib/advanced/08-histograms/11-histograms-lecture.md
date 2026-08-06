# Matplotlib Lecture 11: Histograms

## 🎯 Topic Overview

Histograms show the distribution of continuous data by binning values into intervals. They reveal shape, spread, central tendency, outliers, and modality.

## 📚 Learning Objectives

1. Create histograms with custom bins
2. Use cumulative and normalized histograms
3. Compare distributions with multiple histograms
4. Customize histograms with edge colors, transparency, and stacked bars

---

## 1. Basic Histogram

```python
import matplotlib.pyplot as plt
import numpy as np

data = np.random.randn(1000)

plt.figure(figsize=(10, 6))
plt.hist(data, bins=30, color='steelblue', edgecolor='white', alpha=0.7)
plt.title('Distribution of Random Data')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3)
plt.show()
```

---

## 2. Histogram Variants

```python
# Normalized (density) histogram
plt.hist(data, bins=30, density=True, alpha=0.7,
         label='Density')

# Cumulative histogram
plt.hist(data, bins=30, cumulative=True, alpha=0.7,
         label='Cumulative')

# Multiple datasets comparison
data1 = np.random.normal(0, 1, 1000)
data2 = np.random.normal(2, 1.5, 1000)
plt.hist(data1, bins=30, alpha=0.5, label='Dataset 1')
plt.hist(data2, bins=30, alpha=0.5, label='Dataset 2')
plt.legend()

# With density curve (KDE-like)
counts, bins, _ = plt.hist(data, bins=30, density=True, alpha=0.5)
from scipy.stats import gaussian_kde
kde = gaussian_kde(data)
x_range = np.linspace(data.min(), data.max(), 200)
plt.plot(x_range, kde(x_range), 'r-', linewidth=2, label='KDE')
plt.legend()
```

---

## 3. 2D Histogram

```python
x = np.random.randn(5000)
y = x * 0.5 + np.random.randn(5000) * 0.5

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.hist2d(x, y, bins=30, cmap='viridis')
plt.colorbar(label='Count')
plt.xlabel('X')
plt.ylabel('Y')

plt.subplot(1, 2, 2)
plt.hexbin(x, y, gridsize=30, cmap='plasma')
plt.colorbar(label='Count')
plt.xlabel('X')
plt.ylabel('Y')

plt.tight_layout()
plt.show()
```

---

## Practice Exercises

1. Create a histogram of 1000 normally distributed values with 50 bins
2. Overlay two distributions with different colors and transparency
3. Create a 2D histogram showing correlation between two variables
