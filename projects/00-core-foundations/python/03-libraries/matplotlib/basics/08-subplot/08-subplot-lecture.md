# Matplotlib Lecture 08: Subplots and Multi-Plot Layouts

## 🎯 Topic Overview

Complex data stories often require multiple coordinated plots. Matplotlib provides several mechanisms for creating subplots, from simple grids to complex nested layouts.

## 📚 Learning Objectives

1. Create subplot grids with `subplots()`
2. Use GridSpec for unequal subplot layouts
3. Share axes between subplots
4. Handle nested layouts and insets

---

## 1. Basic Subplot Grids

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)

# 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# axes is a 2D array: axes[row, col]
axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title('sin(x)')

axes[0, 1].plot(x, np.cos(x))
axes[0, 1].set_title('cos(x)')

axes[1, 0].plot(x, np.tan(x))
axes[1, 0].set_ylim(-5, 5)
axes[1, 0].set_title('tan(x)')

axes[1, 1].plot(x, np.sin(x) * np.cos(x))
axes[1, 1].set_title('sin(x) * cos(x)')

for ax in axes.flat:
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 2. Shared Axes

```python
fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

x = np.linspace(0, 10, 100)
axes[0].plot(x, np.sin(x))
axes[0].set_title('sin(x)')
axes[0].set_ylabel('Amplitude')

axes[1].plot(x, np.cos(x))
axes[1].set_title('cos(x)')
axes[1].set_ylabel('Amplitude')

axes[2].plot(x, np.sin(x) * np.cos(x))
axes[2].set_title('sin(x) * cos(x)')
axes[2].set_xlabel('Time (s)')
axes[2].set_ylabel('Amplitude')

plt.tight_layout()
plt.show()
```

---

## 3. GridSpec: Unequal Subplots

```python
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(12, 8))
gs = GridSpec(3, 3, figure=fig, height_ratios=[1, 1, 0.5],
              width_ratios=[1, 1, 1.5])

ax1 = fig.add_subplot(gs[0, :])     # Top row, full width
ax2 = fig.add_subplot(gs[1, 0])      # Middle-left
ax3 = fig.add_subplot(gs[1, 1:])     # Middle-right (spans 2 cols)
ax4 = fig.add_subplot(gs[2, :2])     # Bottom-left (spans 2 cols)
ax5 = fig.add_subplot(gs[2, 2])      # Bottom-right

x = np.linspace(0, 10, 100)
ax1.plot(x, np.sin(x + 0.0), label='0')
ax1.plot(x, np.sin(x + 0.5), label='0.5')
ax1.plot(x, np.sin(x + 1.0), label='1.0')
ax1.legend()

ax2.scatter(np.random.randn(50), np.random.randn(50), alpha=0.6)
ax3.plot(x, np.cos(x), 'r--')
ax4.bar([1,2,3,4], [3, 1, 4, 2])
ax5.pie([30, 25, 25, 20], autopct='%1.0f%%')

fig.suptitle('Complex GridSpec Layout', fontsize=16)
plt.show()
```

---

## 4. Inset Plots

```python
fig, ax = plt.subplots(figsize=(10, 6))

# Main plot
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), linewidth=2)
ax.set_title('Main Plot with Inset')

# Inset axes
left, bottom, width, height = [0.2, 0.6, 0.2, 0.2]
inset = fig.add_axes([left, bottom, width, height])
x_zoom = np.linspace(4, 6, 50)
inset.plot(x_zoom, np.sin(x_zoom), 'r-', linewidth=2)
inset.set_title('Zoomed Region')
inset.set_xlim(4, 6)
inset.grid(True)

plt.show()
```

---

## Practice Exercises

1. Create a 2×2 grid with one plot spanning the entire bottom row
2. Create 3 vertically stacked plots sharing the x-axis
3. Add an inset zoom panel to a main plot