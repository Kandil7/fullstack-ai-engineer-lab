# Matplotlib Lecture 14: Area Plots

## 🎯 Topic Overview

Area plots (filled line plots) emphasize magnitude over time by filling the area between the line and baseline. They're ideal for showing volume, cumulative totals, and stacked compositions.

## 📚 Learning Objectives

1. Create basic area plots with `fill_between`
2. Build stacked area plots for composition
3. Use `stackplot` for time-series composition

---

## 1. Basic Area Plot

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 13)  # Months
y = [15, 18, 22, 25, 28, 30, 32, 31, 28, 24, 19, 16]

plt.figure(figsize=(10, 6))
plt.fill_between(x, y, color='steelblue', alpha=0.4)
plt.plot(x, y, 'b-', linewidth=2, marker='o', markersize=8)
plt.title('Monthly Temperature')
plt.xlabel('Month')
plt.ylabel('Temperature (°C)')
plt.grid(True, alpha=0.3)

# Add labels for months
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(x, months)
plt.show()
```

---

## 2. Stacked Area Plot

```python
x = np.arange(1, 13)
categories = {
    'Product A': [10, 12, 15, 18, 20, 22, 25, 24, 22, 20, 18, 15],
    'Product B': [5, 6, 8, 10, 12, 14, 15, 14, 12, 10, 8, 6],
    'Product C': [3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4],
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Manual stacked area
y_stack = np.zeros_like(x)
for label, values in categories.items():
    ax1.fill_between(x, y_stack, y_stack + values, alpha=0.7, label=label)
    y_stack += values

ax1.set_title('Manual Stacked Area')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Using stackplot
labels = list(categories.keys())
values = list(categories.values())
ax2.stackplot(x, *values, labels=labels, alpha=0.7)
ax2.set_title('stackplot()')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Practice Exercises

1. Create an area plot showing cumulative sales over 12 months
2. Use stackplot to show quarterly revenue breakdown by product line
3. Create a filled confidence interval band around a mean trend line
