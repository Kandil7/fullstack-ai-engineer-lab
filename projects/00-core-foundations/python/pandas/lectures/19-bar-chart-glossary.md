# Glossary 19: Bar Charts

## Quick Reference

| Method / Function | Purpose | Returns |
|-------------------|---------|---------|
| `df.plot.bar()` | Vertical bar chart | Axes |
| `df.plot.barh()` | Horizontal bar chart | Axes |
| `ax.bar()` | Matplotlib vertical bars | BarContainer |
| `ax.barh()` | Matplotlib horizontal bars | BarContainer |
| `stacked=True` | Stack bars on top of each other | — |
| `width` | Bar width (0–1) | float |
| `color` | Bar colors | str, list, or dict |
| `edgecolor` | Bar border color | color |
| `align` | Bar alignment ('center' or 'edge') | str |
| `tick_label` | Custom tick labels | list |

---

## Alphabetical Definitions

### A

**align**
Controls bar position relative to tick mark. `'center'` centers the bar on the tick. `'edge'` aligns the left edge.
```python
ax.bar(x, heights, align='center')  # Default
ax.bar(x, heights, align='edge')    # Left-aligned
```

### B

**Bar Chart vs Pie Chart**
Bar charts compare values across categories using length (easier to compare). Pie charts show parts of a whole using angles (harder to compare precisely). Use bars when precision matters.

**barh()**
Horizontal bar chart. Preferred when category labels are long or there are many categories.
```python
ax.barh(categories, values)
ax.invert_yaxis()  # Largest at top
```

### C

**Color Coding**
Assigning colors to bars based on category or value. Use consistent colors across charts for the same categories.
```python
colors = ['green' if v > threshold else 'red' for v in values]
ax.bar(categories, values, color=colors)
```

### G

**Grouped Bar Chart**
Side-by-side bars for comparing values across two categorical variables. Each group contains bars for the second category.
```python
x = np.arange(n_categories)
width = 0.35
ax.bar(x - width/2, group1, width, label='Group 1')
ax.bar(x + width/2, group2, width, label='Group 2')
```

### H

**Horizontal Bar Chart**
Bars extend left to right. Better for long labels and many categories.
```python
ax.barh(categories, values, color='steelblue')
```

### P

**Percentage Bar Chart**
Stacked bar chart normalized to 100%. Shows relative composition rather than absolute values.
```python
df_pct = df.div(df.sum(axis=1), axis=0) * 100
df_pct.plot.bar(stacked=True)
```

### S

**Stacked Bar Chart**
Bars stacked on top of each other. Shows total and composition simultaneously.
```python
df.plot.bar(stacked=True, color=['#3498db', '#e74c3c', '#2ecc71'])
```

**Sorted Bars**
Arranging bars by value (ascending or descending) makes comparison easier than alphabetical order.
```python
df_sorted = df.sort_values('revenue', ascending=True)
ax.barh(df_sorted['product'], df_sorted['revenue'])
```

### V

**Value Labels**
Text annotations on or above bars showing exact values. Added with `ax.text()`.
```python
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:,.0f}',
            ha='center', va='bottom', fontsize=10)
```

### W

**width**
Controls the width of bars (0 to 1). Default is 0.8. Narrower bars add whitespace between groups.
```python
ax.bar(x, heights, width=0.6)
```

---

## Code Examples

### Example 1: Sorted Horizontal Bar

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({
    'language': ['Python', 'JavaScript', 'Java', 'C++', 'Go', 'Rust', 'TypeScript'],
    'users_millions': [15.8, 12.1, 10.5, 7.2, 4.8, 3.5, 8.9]
}).sort_values('users_millions')

fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.viridis(df['users_millions'] / df['users_millions'].max())

bars = ax.barh(df['language'], df['users_millions'], color=colors, edgecolor='white', height=0.6)

# Add value labels
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.2, bar.get_y() + bar.get_height()/2,
            f'{width:.1f}M', va='center', fontsize=10, fontweight='bold')

ax.set_title('Programming Language Users (Millions)', fontsize=14, fontweight='bold')
ax.set_xlabel('Users (Millions)')
ax.set_xlim(0, max(df['users_millions']) * 1.15)
ax.grid(axis='x', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()
```

### Example 2: Grouped Bar with Error Bars

```python
import numpy as np

categories = ['Method A', 'Method B', 'Method C', 'Method D']
accuracy = [0.85, 0.92, 0.78, 0.88]
std_dev = [0.03, 0.02, 0.05, 0.04]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(categories, accuracy, yerr=std_dev, capsize=5,
              color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'],
              edgecolor='white', error_kw={'linewidth': 1.5})

# Value labels
for bar, acc in zip(bars, accuracy):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f'{acc:.1%}', ha='center', va='bottom', fontweight='bold')

ax.set_ylabel('Accuracy')
ax.set_title('Model Comparison (with Std Dev)')
ax.set_ylim(0, 1.0)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
```

### Example 3: Waterfall Chart

```python
# Approximate waterfall chart
categories = ['Revenue', 'COGS', 'Gross', 'Expenses', 'Taxes', 'Net Income']
values = [100, -40, 60, -25, -10, 25]

fig, ax = plt.subplots(figsize=(10, 6))

cumulative = 0
bottoms = []
for i, v in enumerate(values):
    if i == 0 or i == len(values) - 1:
        bottoms.append(0)
    elif v >= 0:
        bottoms.append(cumulative)
    else:
        bottoms.append(cumulative + v)
    if i not in [0, len(values) - 1]:
        cumulative += v
    elif i == 0:
        cumulative = v

colors = ['#3498db' if v >= 0 else '#e74c3c' for v in values]
bars = ax.bar(categories, [abs(v) for v in values], bottom=bottoms, color=colors, edgecolor='white')

# Value labels
for bar, val, bot in zip(bars, values, bottoms):
    y_pos = bot + abs(val) + 1 if val >= 0 else bot - 2
    ax.text(bar.get_x() + bar.get_width()/2, y_pos,
            f'${val:+d}K', ha='center', va='bottom', fontweight='bold')

ax.set_title('Income Statement Waterfall')
ax.set_ylabel('Amount ($K)')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Related Terms

| Term | Related To | Connection |
|------|-----------|------------|
| `bar()` | `barh()` | Vertical vs horizontal |
| `stacked` | Composition | Shows parts of whole |
| `grouped` | Comparison | Side-by-side bars |
| `value labels` | `ax.text()` | Exact value annotation |
| `color` | Consistency | Same category = same color |
| `width` | Spacing | Controls bar thickness |

---

*See also: [Lecture 19](19-bar-chart-lecture.md) | [Lecture 18 – Pie Chart](18-pie-chart-lecture.md)*
