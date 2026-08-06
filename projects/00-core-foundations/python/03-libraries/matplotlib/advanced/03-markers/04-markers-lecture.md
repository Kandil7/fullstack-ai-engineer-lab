# Matplotlib Lecture 04: Markers

## 🎯 Topic Overview

Markers highlight individual data points on plots. They are essential for distinguishing datasets, emphasizing discrete measurements, and creating publication-quality visualizations.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Use all marker styles: shapes, letters, custom markers
2. Control marker size, color, edge properties, and transparency
3. Combine markers with line styles effectively
4. Create custom marker styles
5. Use markers strategically for clarity

---

## 1. Marker Styles

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(6)
shapes = ['.', ',', 'o', 'v', '^', '<', '>', 's', 'D', '*', 'P', 'X']

plt.figure(figsize=(12, 5))
for i, marker in enumerate(shapes):
    plt.plot(x, np.full_like(x, i), marker=marker, markersize=10,
             label=f"'{marker}'", linestyle='none')

plt.legend(ncol=6, fontsize=10)
plt.ylim(-1, len(shapes))
plt.title('Common Marker Styles')
plt.show()
```

| Marker | Description | Marker | Description |
|--------|-------------|--------|-------------|
| `'.'` | Point | `'o'` | Circle |
| `'*'` | Star | `'+'` | Plus |
| `'x'` | X | `'D'` | Diamond |
| `'s'` | Square | `'^'` | Triangle up |
| `'v'` | Triangle down | `'<'` | Triangle left |
| `'>'` | Triangle right | `'p'` | Pentagon |
| `'h'` | Hexagon | `'H'` | Rotated hexagon |
| `'d'` | Thin diamond | `'P'` | Plus (filled) |
| `'X'` | X (filled) | `'|'` | Vertical line |
| `'_'` | Horizontal line | `','` | Pixel |

---

## 2. Marker Properties

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 20)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(12, 6))

# Marker with all properties
plt.plot(x, y1,
         color='steelblue',
         marker='o',
         markersize=10,
         markerfacecolor='white',    # Inside color
         markeredgecolor='steelblue', # Edge color
         markeredgewidth=2,           # Edge width
         linewidth=2,
         alpha=0.9,
         label='sin(x)')

plt.plot(x, y2,
         color='crimson',
         marker='s',
         markersize=10,
         markerfacecolor='white',
         markeredgecolor='crimson',
         markeredgewidth=2,
         linewidth=2,
         alpha=0.9,
         label='cos(x)')

plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.show()
```

---

## 3. Marker + Line Combinations

```python
# Different marker+line strategies
plt.figure(figsize=(12, 8))

x = np.linspace(0, 10, 10)

# Strategy 1: Markers only (no lines) - sparse data
plt.subplot(2, 2, 1)
plt.plot(x, np.sin(x), 'o', markersize=8)
plt.title('Markers Only')

# Strategy 2: Lines only - smooth continuous data
plt.subplot(2, 2, 2)
x_dense = np.linspace(0, 10, 100)
plt.plot(x_dense, np.sin(x_dense), '-', linewidth=2)
plt.title('Line Only')

# Strategy 3: Lines + Markers - show data points on line
plt.subplot(2, 2, 3)
plt.plot(x, np.sin(x), '-o', linewidth=2, markersize=8)
plt.title('Line + Markers')

# Strategy 4: Marker spacing - every Nth data point
plt.subplot(2, 2, 4)
plt.plot(x_dense, np.sin(x_dense), '-', linewidth=2)
plt.plot(x, np.sin(x), 'o', markersize=10, color='red')
plt.title('Selective Markers')

plt.tight_layout()
plt.show()
```

---

## 4. Custom Markers with `markevery`

```python
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(12, 6))
plt.plot(x, y, '-o',
         markevery=10,          # Every 10th point
         markersize=8,
         linewidth=2,
         color='steelblue')

# markevery can be:
# - int: every N points
# - list: specific indices [0, 5, 15, 25]
# - slice: [::10] style
# - float: fraction of data (0.1 = every 10%)
plt.show()
```

---

## Practice Exercises

1. Create a plot with 5 different marker styles, each with custom colors and sizes
2. Use markevery to selectively display markers
3. Create a scatter-like plot using `plot()` with markers only
