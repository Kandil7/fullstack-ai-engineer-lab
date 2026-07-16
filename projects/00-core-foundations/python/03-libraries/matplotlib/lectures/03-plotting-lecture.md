# Matplotlib Lecture 03: Basic Plotting

## 🎯 Topic Overview

Line plots are the most fundamental visualization in Matplotlib. This lecture covers the `plot()` function in depth — color, style, markers, and customizations — along with essential plot elements like legends, grids, and limits.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Master the `plot()` function with format strings and keyword arguments
2. Create plots with multiple lines and custom styles
3. Control axes limits, ticks, and scales
4. Add legends, annotations, and text
5. Use logarithmic and polar axes

---

## 1. The `plot()` Function

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

# Simplest form - default blue line
plt.plot(x, y)
plt.show()
```

### Format Strings

```python
# fmt = '[color][marker][line]'
plt.plot(x, y, 'r--')     # Red dashed line
plt.plot(x, y, 'go')      # Green circle markers, no line
plt.plot(x, y, 'b^-')     # Blue triangle-up markers with line
plt.plot(x, y, 'ks:')     # Black square markers with dotted line
```

| Character | Color | Character | Marker | Character | Line Style |
|-----------|-------|-----------|--------|-----------|------------|
| `'b'` | Blue | `'.'` | Point | `'-'` | Solid |
| `'g'` | Green | `','` | Pixel | `'--'` | Dashed |
| `'r'` | Red | `'o'` | Circle | `'-.'` | Dash-dot |
| `'c'` | Cyan | `'^'` | Triangle up | `':'` | Dotted |
| `'m'` | Magenta | `'s'` | Square | `' '` | None |
| `'y'` | Yellow | `'*'` | Star | | |
| `'k'` | Black | `'D'` | Diamond | | |
| `'w'` | White | `'x'` | X | | |

### Keyword Arguments (More Flexible)

```python
plt.plot(x, y,
         color='darkorange',
         linestyle='--',
         linewidth=2,
         marker='o',
         markersize=6,
         markerfacecolor='red',
         markeredgecolor='black',
         markeredgewidth=1,
         alpha=0.8,
         label='sin(x)')
```

---

## 2. Multiple Lines

```python
x = np.linspace(0, 2*np.pi, 100)

plt.figure(figsize=(10, 6))
plt.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
plt.plot(x, np.cos(x), 'r--', linewidth=2, label='cos(x)')
plt.plot(x, np.sin(x + 1), 'g:', linewidth=2, label='sin(x+1)')
plt.plot(x, np.cos(x + 1), 'm-.', linewidth=2, label='cos(x+1)')

plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.title('Multiple Lines Comparison')
plt.xlabel('x (radians)')
plt.ylabel('y')
plt.tight_layout()
```

---

## 3. Controlling Axes Limits and Ticks

```python
x = np.linspace(-10, 10, 200)
y = x**3

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2)

# Custom limits
plt.xlim(-10, 10)
plt.ylim(-500, 500)

# Custom ticks
plt.xticks([-10, -5, 0, 5, 10])
plt.yticks([-500, -250, 0, 250, 500])

# Or automatic nice limits
plt.axis('tight')  # Fit tightly to data
plt.axis('equal')  # Equal aspect ratio
plt.axis('off')    # Hide axes entirely
```

### Logarithmic Scales

```python
x = np.logspace(-2, 2, 100)
y = x**2

plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.plot(x, y, 'b-')
plt.title('Linear-Linear')

plt.subplot(1, 3, 2)
plt.semilogx(x, y, 'r-')
plt.title('Log-X')

plt.subplot(1, 3, 3)
plt.loglog(x, y, 'g-')
plt.title('Log-Log')

plt.tight_layout()
```

---

## 4. Legends and Annotations

```python
x = np.linspace(0, 10, 100)

plt.figure(figsize=(10, 6))
plt.plot(x, np.sin(x), label='sin(x)', linewidth=2)
plt.plot(x, np.cos(x), label='cos(x)', linewidth=2)

# Legend positions
plt.legend(loc='upper right')  # 'best', 'center', 'lower left', etc.

# Annotations
plt.annotate('Max value',
             xy=(np.pi/2, 1),
             xytext=(np.pi/2 + 1, 0.8),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=12,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Text box
plt.text(0.5, -0.5, 'Note: Periodic behavior', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))
```

---

## Practice Exercises

1. Plot `y = e^{-x} * sin(x)` with customized color, line style, and legend
2. Create a plot with linear, semi-log, and log-log subplots
3. Customize ticks, limits, and add annotations to a plot
