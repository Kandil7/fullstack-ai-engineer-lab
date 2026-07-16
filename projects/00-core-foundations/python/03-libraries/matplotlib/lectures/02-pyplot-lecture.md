# Matplotlib Lecture 02: The Pyplot Interface

## 🎯 Topic Overview

Pyplot is Matplotlib's convenience module that provides a MATLAB-like functional interface for creating plots. It manages a "state machine" — tracking the current figure and axes so you can modify them with simple function calls. This lecture explores pyplot in depth, teaching you to create effective visualizations quickly.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Understand pyplot's state machine architecture
2. Create and customize figures using pyplot functions
3. Manage multiple figures and subplots
4. Use pyplot for quick exploratory data analysis
5. Transition between pyplot and OOP interfaces

---

## 1. The State Machine Model

Pyplot maintains a global state that tracks the "current" figure and axes:

```python
import matplotlib.pyplot as plt
import numpy as np

# pyplot creates a figure and axes automatically
plt.plot([1, 2, 3], [1, 4, 2])  # Uses "current" axes

# All subsequent calls affect the current axes
plt.title("Current Axes Modified")
plt.xlabel("X")
plt.ylabel("Y")

# You can explicitly manage which figure is current
plt.figure(1)  # Switch to/create Figure 1
plt.plot([1, 2, 3], [1, 2, 3], label='Line A')

plt.figure(2)  # Switch to/create Figure 2
plt.plot([1, 2, 3], [3, 2, 1], label='Line B')

plt.figure(1)  # Back to Figure 1
plt.legend()
```

### How the State Machine Works

```
plt.figure()      → Sets current figure
plt.subplot()     → Creates/selects current axes
plt.plot()        → Plots on current axes
plt.title()       → Sets title on current axes
plt.xlabel()      → Sets x-label on current axes
plt.show()        → Displays everything
```

---

## 2. Essential pyplot Functions

### Figure Management

```python
plt.figure(figsize=(8, 5))        # Create new figure
plt.figure(1)                      # Activate existing figure
plt.close()                        # Close current figure
plt.close('all')                   # Close all figures
plt.gcf()                          # Get current figure
plt.clf()                          # Clear current figure
```

### Plot Types

```python
plt.plot(x, y)                     # Line plot
plt.scatter(x, y)                  # Scatter plot
plt.bar(x, height)                 # Bar chart
plt.hist(data, bins=20)            # Histogram
plt.pie(sizes, labels=labels)      # Pie chart
plt.boxplot(data)                  # Box plot
plt.imshow(image)                  # Image display
plt.contour(X, Y, Z)               # Contour plot
```

### Customization

```python
plt.title("Title", fontsize=14)     # Title with font size
plt.xlabel("X Label")               # X-axis label
plt.ylabel("Y Label")               # Y-axis label
plt.xlim(0, 10)                     # X-axis limits
plt.ylim(-1, 1)                     # Y-axis limits
plt.grid(True, alpha=0.3)           # Grid lines
plt.legend(loc='best')              # Legend
plt.colorbar()                      # Color bar
plt.text(x, y, "text")              # Text annotation
plt.axhline(y=0, color='gray')      # Horizontal line
plt.axvline(x=0, color='gray')      # Vertical line
```

---

## 3. Creating Multiple Subplots with pyplot

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)

# 2 rows, 2 columns, select each subplot
plt.subplot(2, 2, 1)
plt.plot(x, np.sin(x))
plt.title('sin(x)')

plt.subplot(2, 2, 2)
plt.plot(x, np.cos(x))
plt.title('cos(x)')

plt.subplot(2, 2, 3)
plt.plot(x, np.tan(x))
plt.title('tan(x)')
plt.ylim(-5, 5)

plt.subplot(2, 2, 4)
plt.plot(x, np.sin(x)**2 + np.cos(x)**2)
plt.title('sin²(x) + cos²(x)')

plt.tight_layout()
plt.show()
```

---

## 4. Quick Data Exploration with pyplot

```python
import matplotlib.pyplot as plt
import numpy as np

# Generate sample data
data = np.random.randn(1000)

# Quick histogram
plt.figure(1)
plt.hist(data, bins=30, alpha=0.7, color='steelblue', edgecolor='white')
plt.title('Histogram')
plt.xlabel('Value')
plt.ylabel('Frequency')

# Quick box plot
plt.figure(2)
plt.boxplot(data, vert=True, patch_artist=True)
plt.title('Box Plot')
plt.ylabel('Value')

# Quick scatter
x = np.random.randn(200)
y = x * 0.5 + np.random.randn(200) * 0.5

plt.figure(3)
plt.scatter(x, y, alpha=0.6, s=30)
plt.title('Scatter Plot')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 5. Common Customizations

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(10, 6))

# Multiple lines with customization
plt.plot(x, y1, 'b-', linewidth=2, label='sin(x)')
plt.plot(x, y2, 'r--', linewidth=2, label='cos(x)')

# Fill between
plt.fill_between(x, y1, y2, alpha=0.1, color='purple')

# Annotations
plt.annotate('Intersection',
             xy=(np.pi/4, np.sin(np.pi/4)),
             xytext=(np.pi/2, 0.5),
             arrowprops=dict(arrowstyle='->', color='green'))

# Grid and styling
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper right')
plt.title('Trigonometric Functions with Annotations', fontsize=14)
plt.xlabel('x (radians)')
plt.ylabel('y')

plt.tight_layout()
plt.show()
```

---

## 6. Best Practices for pyplot

1. **Use for exploration** — pyplot is great for quick analysis in notebooks
2. **Switch to OOP** when building reusable or publication code
3. **Close figures** after saving to free memory: `plt.close()`
4. **Use `plt.subplots_adjust()`** for fine-grained spacing control
5. **Combine with `plt.style.context()`** for temporary style changes

---

## Practice Exercises

1. Create a pyplot figure with 4 subplots showing different trig functions
2. Use pyplot to explore a random dataset with histogram, boxplot, and scatter
3. Customize a line plot with annotations, grid, and fill_between

---

## 🔗 Next Lecture

→ [03-plotting-lecture.md](./03-plotting-lecture.md) — Basic Plotting
