# Glossary 18: Pie Charts

## Quick Reference

| Method / Function | Purpose | Returns |
|-------------------|---------|---------|
| `ax.pie()` | Create pie chart | Wedges, texts, autotexts |
| `autopct` | Format percentage labels | string or callable |
| `explode` | Offset slices from center | tuple of floats |
| `startangle` | Rotate starting angle | int (degrees) |
| `wedgeprops` | Customize wedge appearance | dict |
| `pctdistance` | Distance of labels from center | float (0–1) |
| `labeldistance` | Distance of category labels | float (0–1) |
| `shadow` | Add shadow effect | bool |
| `colors` | Custom slice colors | list of colors |

---

## Alphabetical Definitions

### A

**autopct**
A format string or function that controls percentage labels on slices. `'%1.1f%%'` shows one decimal place.
```python
ax.pie(sizes, autopct='%1.1f%%')
# With callable for custom format
ax.pie(sizes, autopct=lambda p: f'{p:.1f}%')
```

### C

**colors**
A list of color values assigned to each slice. Can be hex codes, named colors, or colormap values.
```python
colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
ax.pie(sizes, colors=colors)
```

### D

**Donut Chart**
A pie chart with a hole in the center, created by setting `wedgeprops={'width': 0.4}`. Often used with center text showing totals.
```python
ax.pie(sizes, wedgeprops=dict(width=0.4))
ax.text(0, 0, 'Total', ha='center', va='center', fontsize=16)
```

### E

**explode**
A tuple that offsets slices from the center. `0.1` means 10% offset. Use to emphasize specific slices.
```python
explode = (0.1, 0, 0, 0)  # Only first slice is offset
ax.pie(sizes, explode=explode)
```

### L

**labeldistance**
Distance of category labels from the center. Default is 1.1. Values > 1 push labels outward.
```python
ax.pie(sizes, labels=labels, labeldistance=1.2)
```

### P

**pctdistance**
Distance of percentage labels from the center. Default is 0.6. Values > 1 place labels outside the pie.
```python
ax.pie(sizes, autopct='%1.1f%%', pctdistance=0.85)
```

**Proportion**
The fraction of each category relative to the total. Pie slices represent proportions that sum to 1 (100%).
```python
proportions = sizes / sizes.sum()
```

### S

**startangle**
Rotates the starting position of the first slice. 90 degrees places the first slice at the top (12 o'clock).
```python
ax.pie(sizes, startangle=90)  # Start from top
```

**shadow**
Adds a shadow effect behind the pie chart. Default is False. Set to True for a 3D-like appearance (generally not recommended).
```python
ax.pie(sizes, shadow=True)
```

### W

**wedges**
The slice objects returned by `ax.pie()`. Can be passed to `ax.legend()` for custom legends.
```python
wedges, texts, autotexts = ax.pie(sizes, autopct='%1.1f%%')
ax.legend(wedges, labels, title='Categories')
```

**wedgeprops**
Dictionary of properties for each wedge (slice). Used to create donut charts or customize appearance.
```python
ax.pie(sizes, wedgeprops=dict(width=0.3, edgecolor='white', linewidth=2))
```

---

## Code Examples

### Example 1: Custom Pie Chart

```python
import matplotlib.pyplot as plt
import numpy as np

labels = ['Python', 'JavaScript', 'Java', 'C++', 'Other']
sizes = [35, 25, 20, 12, 8]
colors = ['#3776ab', '#f7df1e', '#f89820', '#00599c', '#cccccc']
explode = (0.05, 0, 0, 0, 0)

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    sizes,
    explode=explode,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    shadow=False,
    textprops={'fontsize': 12}
)

# Make percentage text bold
for autotext in autotexts:
    autotext.set_fontweight('bold')

ax.set_title('Programming Language Popularity', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.show()
```

### Example 2: Donut with Center

```python
fig, ax = plt.subplots(figsize=(8, 8))

sizes = [40, 30, 20, 10]
labels = ['Product A', 'Product B', 'Product C', 'Product D']
colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']

wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,
    autopct='%1.0f%%',
    colors=colors,
    startangle=90,
    pctdistance=0.78,
    wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
)

# Center text
total = sum(sizes)
ax.text(0, 0.05, f'${total}K', ha='center', va='center', fontsize=20, fontweight='bold')
ax.text(0, -0.1, 'Total Revenue', ha='center', va='center', fontsize=11, color='gray')

ax.set_title('Revenue by Product Line', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

### Example 3: Waffle Chart Alternative

```python
# When pie charts fail, use a waffle-style visualization
fig, ax = plt.subplots(figsize=(10, 6))

categories = ['Electronics', 'Clothing', 'Food', 'Books']
values = [35, 25, 25, 15]
colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']

# Create horizontal stacked bar (waffle-like)
bottom = 0
for val, color, cat in zip(values, colors, categories):
    ax.barh(0, val, left=bottom, color=color, height=0.5, label=f'{cat} ({val}%)')
    if val > 5:
        ax.text(bottom + val/2, 0, f'{cat}\n{val}%', ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')
    bottom += val

ax.set_xlim(0, 100)
ax.set_ylim(-0.5, 0.5)
ax.set_yticks([])
ax.set_xlabel('Percentage')
ax.set_title('Market Share (Waffle Style)')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4)

plt.tight_layout()
plt.show()
```

---

## Related Terms

| Term | Related To | Connection |
|------|-----------|------------|
| `autopct` | `ax.pie()` | Percentage label formatting |
| `explode` | `ax.pie()` | Slice emphasis |
| `wedgeprops` | Donut chart | Creates center hole |
| `startangle` | `ax.pie()` | Rotation control |
| `bar chart` | Pie chart | More precise comparison alternative |
| `donut` | `wedgeprops` | Pie chart variant |
| `waffle chart` | Pie chart | Better alternative for many categories |

---

*See also: [Lecture 18](18-pie-chart-lecture.md) | [Lecture 19 – Bar Chart](19-bar-chart-lecture.md)*
