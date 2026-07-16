# Matplotlib Lecture 07: Grid and Layout

## 🎯 Topic Overview

Grid lines help readers estimate data values. Proper layout ensures plots are readable and professional.

## 📚 Learning Objectives

1. Customize grid lines (style, color, transparency, axis-specific)
2. Master `tight_layout()` and `constrained_layout`
3. Control axis spines and borders

---

## 1. Grid Customization

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x), linewidth=2)

# Basic grid
plt.grid(True)

# Customized grid
plt.grid(True,
         which='both',        # 'major', 'minor', or 'both'
         axis='both',         # 'x', 'y', or 'both'
         color='gray',
         linestyle='--',
         linewidth=0.5,
         alpha=0.7)

# Minor ticks and grid
from matplotlib.ticker import MultipleLocator
ax = plt.gca()
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
ax.yaxis.set_minor_locator(MultipleLocator(0.1))
ax.grid(True, which='minor', alpha=0.2)
ax.grid(True, which='major', alpha=0.5)

plt.show()
```

---

## 2. Axis Spines

```python
# Remove top and right spines
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Move spines
ax.spines['left'].set_position(('outward', 10))  # Move outward 10pts
ax.spines['bottom'].set_position(('data', 0))    # Move to y=0

# Customize spine color/width
ax.spines['left'].set_color('darkblue')
ax.spines['left'].set_linewidth(2)
```

---

## 3. Figure Layout

```python
# tight_layout - auto adjust spacing
plt.tight_layout()
plt.tight_layout(pad=2.0, w_pad=1.0, h_pad=1.0)

# constrained_layout - better for complex figures
fig, axs = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)

# subplots_adjust - manual control
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1,
                    wspace=0.3, hspace=0.3)
```

---

## Practice Exercises

1. Create a plot with major and minor grid lines in different styles
2. Hide top and right spines, move the remaining spines outward
3. Create a 3×3 grid of subplots with proper spacing using both layouts
