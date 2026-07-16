# Matplotlib Lecture 09: Scatter Plots

## 🎯 Topic Overview

Scatter plots reveal relationships between two variables — correlations, clusters, and outliers. Matplotlib's `scatter()` offers extensive customization through color, size, and transparency.

## 📚 Learning Objectives

1. Create scatter plots with `scatter()`
2. Encode 3-5 dimensions using color, size, shape, and alpha
3. Add colorbars and customize colormaps
4. Distinguish between `plot()` markers and `scatter()` features

---

## 1. Basic Scatter Plot

```python
import matplotlib.pyplot as plt
import numpy as np

n = 100
rng = np.random.default_rng(42)
x = rng.normal(0, 1, n)
y = x * 0.5 + rng.normal(0, 0.5, n)

plt.figure(figsize=(8, 6))
plt.scatter(x, y, alpha=0.7, s=50)
plt.xlabel('X Variable')
plt.ylabel('Y Variable')
plt.title('Basic Scatter Plot')
plt.grid(True, alpha=0.3)
plt.show()
```

---

## 2. Multi-Dimensional Scatter

```python
# Encode 5 dimensions:
# 1. X position → sepal length
# 2. Y position → sepal width
# 3. Color → species (categorical)
# 4. Size → petal length (continuous)
# 5. Transparency → density

colors = ['red', 'green', 'blue']
sizes = np.random.uniform(20, 200, n)

for i, species in enumerate(['Setosa', 'Versicolor', 'Virginica']):
    mask = y_true == i  # Using Iris-like data
    plt.scatter(x[mask], y[mask],
                c=colors[i],
                s=sizes[mask],
                alpha=0.7,
                label=species,
                edgecolors='black',
                linewidth=0.5)

plt.colorbar(label='Petal Length (cm)')
plt.legend()
plt.show()
```

---

## 3. Colorbars and Colormaps

```python
x = rng.uniform(0, 10, 200)
y = rng.uniform(0, 10, 200)
z = x * y  # Color value

plt.figure(figsize=(10, 7))
scatter = plt.scatter(x, y, c=z, s=50, cmap='viridis',
                      alpha=0.7, edgecolors='black', linewidth=0.5)

plt.colorbar(scatter, label='Product (X × Y)', shrink=0.8)

# Built-in colormaps: 'viridis', 'plasma', 'inferno', 'magma',
# 'coolwarm', 'RdBu', 'jet', 'hsv', 'twilight'
```

---

## Practice Exercises

1. Create a scatter plot with color and size encoding additional variables
2. Generate random data and add a correlation line
3. Create a bubble chart with 4 dimensions of data
