# Lecture 19: Bar Charts in Pandas

## Learning Objectives

By the end of this lecture, you will be able to:
- Create vertical and horizontal bar charts
- Build grouped and stacked bar charts
- Add value labels to bars
- Customize colors, spacing, and formatting
- Create waterfall charts
- Choose the right bar chart type for your data

---

## 1. What is a Bar Chart?

A bar chart uses rectangular bars to represent categorical data. The length/height of each bar is proportional to the value it represents. Bar charts are the most versatile and widely-used chart type for comparing categories.

---

## 2. Basic Bar Chart

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame({
    'product': ['Laptop', 'Phone', 'Tablet', 'Watch', 'Headphones'],
    'revenue': [45000, 38000, 22000, 15000, 12000]
})

# Vertical bar chart (Pandas)
df.plot.bar(x='product', y='revenue', figsize=(10, 6), legend=False)
plt.title('Revenue by Product')
plt.xlabel('Product')
plt.ylabel('Revenue ($)')
plt.tight_layout()
plt.show()
```

### 2.1 Matplotlib Version

```python
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df['product'], df['revenue'], color='steelblue', edgecolor='white')
ax.set_title('Revenue by Product')
ax.set_xlabel('Product')
ax.set_ylabel('Revenue ($)')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 3. Horizontal Bar Chart

```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(df['product'], df['revenue'], color='steelblue', edgecolor='white')
ax.set_title('Revenue by Product')
ax.set_xlabel('Revenue ($)')
ax.set_ylabel('Product')
ax.invert_yaxis()  # Largest on top
plt.tight_layout()
plt.show()
```

---

## 4. Grouped Bar Chart

```python
# Multi-category data
df_grouped = pd.DataFrame({
    'product': ['Laptop', 'Phone', 'Tablet', 'Watch'],
    'Q1': [12000, 15000, 8000, 5000],
    'Q2': [15000, 12000, 7000, 4500],
    'Q3': [18000, 11000, 7000, 5500]
})

# Pandas grouped bar
df_grouped.plot.bar(x='product', figsize=(10, 6))
plt.title('Revenue by Product and Quarter')
plt.xlabel('Product')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=0)
plt.legend(title='Quarter')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
```

### 4.1 Manual Grouped Bars

```python
fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(df_grouped['product']))
width = 0.25

bars1 = ax.bar(x - width, df_grouped['Q1'], width, label='Q1', color='#3498db')
bars2 = ax.bar(x, df_grouped['Q2'], width, label='Q2', color='#e74c3c')
bars3 = ax.bar(x + width, df_grouped['Q3'], width, label='Q3', color='#2ecc71')

ax.set_xticks(x)
ax.set_xticklabels(df_grouped['product'])
ax.set_title('Revenue by Product and Quarter')
ax.set_ylabel('Revenue ($)')
ax.legend(title='Quarter')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 5. Stacked Bar Chart

```python
df_grouped.plot.bar(x='product', stacked=True, figsize=(10, 6),
                     color=['#3498db', '#e74c3c', '#2ecc71'])
plt.title('Revenue by Product (Stacked)')
plt.xlabel('Product')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=0)
plt.legend(title='Quarter')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 6. Adding Value Labels

```python
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df['product'], df['revenue'], color='steelblue', edgecolor='white')

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2.,  # x position
        height + 500,                          # y position (above bar)
        f'${height:,.0f}',                     # label text
        ha='center',                           # horizontal alignment
        va='bottom',                           # vertical alignment
        fontsize=10,
        fontweight='bold'
    )

ax.set_title('Revenue by Product')
ax.set_ylabel('Revenue ($)')
ax.set_ylim(0, max(df['revenue']) * 1.15)  # Extra space for labels
plt.tight_layout()
plt.show()
```

---

## 7. Colored by Value

```python
fig, ax = plt.subplots(figsize=(10, 6))

# Color bars based on value
colors = ['#e74c3c' if v < 20000 else '#2ecc71' for v in df['revenue']]
bars = ax.bar(df['product'], df['revenue'], color=colors, edgecolor='white')

ax.set_title('Revenue by Product (Red < $20K, Green >= $20K)')
ax.set_ylabel('Revenue ($)')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 8. Percentage Bar Chart

```python
# Convert to percentages
df_pct = df_grouped.set_index('product')
df_pct = df_pct.div(df_pct.sum(axis=1), axis=0) * 100

df_pct.plot.bar(stacked=True, figsize=(10, 6), color=['#3498db', '#e74c3c', '#2ecc71'])
plt.title('Revenue Distribution by Quarter (%)')
plt.xlabel('Product')
plt.ylabel('Percentage (%)')
plt.xticks(rotation=0)
plt.legend(title='Quarter', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
```

---

## 9. Common Mistakes

1. **Starting y-axis at non-zero** — Misleading bar heights. Always start at 0 for bar charts.
2. **Too many categories** — Use horizontal bars for 10+ categories.
3. **Inconsistent colors** — Same category should always be the same color.
4. **Missing labels** — Every bar needs a value label or axis reference.
5. **3D effects** — Distort perception. Always use flat 2D.

---

## 10. Best Practices

1. **Horizontal for many categories** — Easier to read long labels.
2. **Sort bars** — By value (ascending or descending) for easier comparison.
3. **Limit to 5-7 colors** — Group small categories into "Other".
4. **Add value labels** — For precision when exact numbers matter.
5. **Use consistent spacing** — Bar width should be larger than gap width.

---

## 11. Exercises

### Exercise 1: Sales Comparison
Create a horizontal bar chart of the top 10 products by sales, sorted from highest to lowest, with value labels.

### Exercise 2: Grouped Chart
Using the Titanic dataset, create a grouped bar chart showing survival rate by class and sex.

### Exercise 3: Stacked Percentage
Create a 100% stacked bar chart showing the composition of movie genres across 5 theaters.

---

## 12. Summary

| Chart Type | When to Use | Pandas Method |
|-----------|-------------|---------------|
| Vertical bar | Few categories, short labels | `df.plot.bar()` |
| Horizontal bar | Many categories, long labels | `df.plot.barh()` |
| Grouped bar | Compare across two categories | `df.plot.bar()` with multiple columns |
| Stacked bar | Show composition | `df.plot.bar(stacked=True)` |
| 100% stacked | Show proportions | Normalize then stack |

**Key takeaway**: Bar charts are the most versatile visualization for categorical data. Choose vertical, horizontal, grouped, or stacked based on your comparison goal.

---

*Next: [20 – Merge](20-merge-lecture.md)*
