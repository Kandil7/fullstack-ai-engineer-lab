# Matplotlib Lecture 05: Line Customization

## 🎯 Topic Overview

Line styles communicate the nature of data — solid for primary data, dashed for predictions, dotted for confidence intervals. Mastering line customization is essential for clear visual communication.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Apply all line styles: solid, dashed, dotted, dash-dot
2. Customize line width, color, and transparency
3. Use dashed patterns for clear communication
4. Create stair-step and vertical/horizontal lines
5. Apply error bars and fill between lines

---

## 1. Line Styles

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

plt.figure(figsize=(12, 8))

# Four main line styles
plt.subplot(2, 2, 1)
plt.plot(x, np.sin(x), '-', linewidth=2, label='Solid (-)')
plt.plot(x, np.sin(x) + 1, '--', linewidth=2, label='Dashed (--)')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(x, np.sin(x), '-.', linewidth=2, label='Dash-Dot (-.)')
plt.plot(x, np.sin(x) + 1, ':', linewidth=2, label='Dotted (:)')
plt.legend()

# Line widths
plt.subplot(2, 2, 3)
for w in [0.5, 1, 2, 3, 5]:
    plt.plot(x, np.sin(x) + w/5, linewidth=w, label=f'width={w}')
plt.legend()

# Custom dash patterns
plt.subplot(2, 2, 4)
plt.plot(x, np.sin(x), linestyle=(0, (5, 5)), linewidth=2, label='(5,5)')
plt.plot(x, np.sin(x) + 1, linestyle=(0, (10, 5)), linewidth=2, label='(10,5)')
plt.plot(x, np.sin(x) + 2, linestyle=(0, (3, 5, 10, 5)), linewidth=2, label='(3,5,10,5)')
plt.legend()

plt.tight_layout()
```

### Custom Dash Patterns

```python
# (offset, (on_length, off_length, on_length, off_length, ...))
linestyle=(0, (5, 5))        # 5pt on, 5pt off
linestyle=(0, (10, 5))       # 10pt on, 5pt off
linestyle=(0, (3, 5, 10, 5)) # 3on, 5off, 10on, 5off
linestyle='dashed'           # Equivalent to (0, (6, 3))
linestyle='dotted'           # Equivalent to (0, (3, 3))
```

---

## 2. Color Maps for Multiple Lines

```python
from matplotlib import cm

x = np.linspace(0, 10, 100)
plt.figure(figsize=(10, 6))

# Viridis colormap for 10 lines
colors = cm.viridis(np.linspace(0, 1, 10))
for i, color in enumerate(colors):
    y = np.sin(x - i/2)
    plt.plot(x, y, color=color, linewidth=2, label=f'Phase {i/2:.1f}')

plt.legend(ncol=2, fontsize=8)
plt.title('Using Colormaps for Multiple Lines')
plt.colorbar(plt.cm.ScalarMappable(cmap='viridis'), label='Phase')
plt.show()
```

---

## 3. Vertical and Horizontal Lines

```python
plt.figure(figsize=(10, 6))
x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x), linewidth=2, color='steelblue')

# Helper lines
plt.axhline(y=0, color='gray', linestyle=':', alpha=0.7)        # Horizontal
plt.axvline(x=np.pi, color='red', linestyle='--', alpha=0.5)    # Vertical
plt.axhline(y=0.5, xmin=0.25, xmax=0.75, color='green')         # Partial horizontal
plt.axvline(x=2*np.pi, ymin=0.2, ymax=0.8, color='orange')      # Partial vertical

# Span fill
plt.axhspan(ymin=-0.5, ymax=0.5, alpha=0.1, color='gray')       # Horizontal span
plt.axvspan(xmin=2, xmax=4, alpha=0.1, color='green')           # Vertical span

plt.title('Helper Lines and Spans')
plt.show()
```

---

## 4. Fill Between

```python
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2, label='sin(x)')

# Fill between curve and axis
plt.fill_between(x, y, 0, where=(y > 0), color='green', alpha=0.3, label='Positive')
plt.fill_between(x, y, 0, where=(y < 0), color='red', alpha=0.3, label='Negative')

# Fill between two curves
plt.fill_between(x, y, y + 0.5, alpha=0.2, color='purple', label='±0.5 band')

plt.legend()
plt.title('Fill Between Applications')
plt.show()
```

---

## Practice Exercises

1. Plot 5 lines with different dash patterns and a shared legend
2. Use `fill_between` to show a confidence interval around a mean line
3. Add vertical/horizontal lines and spans to highlight key regions
