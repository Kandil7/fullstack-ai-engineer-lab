# Lecture 18: Pie Charts in Pandas

## Learning Objectives

By the end of this lecture, you will be able to:
- Create pie charts for proportional data
- Customize colors, labels, and formatting
- Create donut charts
- Add percentage labels
- Know when to use (and avoid) pie charts
- Compare pie charts with bar charts

---

## 1. What is a Pie Chart?

A pie chart shows how a whole is divided into parts. Each "slice" represents a category's proportion of the total. Pie charts are best for showing **parts of a whole** with **few categories (5–7 max)**.

---

## 2. Basic Pie Chart

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    'category': ['Electronics', 'Clothing', 'Food', 'Books', 'Other'],
    'sales': [45000, 32000, 28000, 15000, 8000]
})

# Basic pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(df['sales'], labels=df['category'], autopct='%1.1f%%')
ax.set_title('Sales by Category')
plt.tight_layout()
plt.show()
```

---

## 3. Customizing Pie Charts

### 3.1 Colors and Styling

```python
fig, ax = plt.subplots(figsize=(8, 8))

colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
explode = (0.05, 0, 0, 0, 0.1)  # Explode first and last slices

ax.pie(
    df['sales'],
    labels=df['category'],
    autopct='%1.1f%%',
    colors=colors,
    explode=explode,
    startangle=90,           # Rotate starting angle
    shadow=True,             # Add shadow
    textprops={'fontsize': 12}
)

ax.set_title('Sales by Category', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

### 3.2 Custom Percentage Format

```python
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return f'{pct:.1f}%\n(${val:,})'
    return my_autopct

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    df['sales'],
    labels=df['category'],
    autopct=make_autopct(df['sales']),
    colors=colors,
    startangle=90
)
ax.set_title('Sales by Category (with Values)')
plt.tight_layout()
plt.show()
```

### 3.3 Legend Placement

```python
fig, ax = plt.subplots(figsize=(10, 8))

wedges, texts, autotexts = ax.pie(
    df['sales'],
    autopct='%1.1f%%',
    colors=colors,
    startangle=90,
    pctdistance=0.85         # Distance of percentage labels from center
)

# Add legend
ax.legend(
    wedges,
    df['category'],
    title='Categories',
    loc='center left',
    bbox_to_anchor=(1, 0, 0.5, 1)
)

ax.set_title('Sales Distribution')
plt.tight_layout()
plt.show()
```

---

## 4. Donut Chart

```python
fig, ax = plt.subplots(figsize=(8, 8))

wedges, texts, autotexts = ax.pie(
    df['sales'],
    labels=df['category'],
    autopct='%1.1f%%',
    colors=colors,
    startangle=90,
    pctdistance=0.85,
    wedgeprops=dict(width=0.4)  # Creates donut hole
)

# Add center text
ax.text(0, 0, f'Total\n${df["sales"].sum():,}', ha='center', va='center', fontsize=14, fontweight='bold')

ax.set_title('Sales by Category (Donut Chart)')
plt.tight_layout()
plt.show()
```

---

## 5. Small Multiples

```python
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 2023 data
df_2023 = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'sales': [30, 25, 25, 20]
})

# 2024 data
df_2024 = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'sales': [20, 35, 25, 20]
})

axes[0].pie(df_2023['sales'], labels=df_2023['category'], autopct='%1.0f%%', colors=colors)
axes[0].set_title('2023')

axes[1].pie(df_2024['sales'], labels=df_2024['category'], autopct='%1.0f%%', colors=colors)
axes[1].set_title('2024')

plt.suptitle('Sales Distribution Comparison', fontsize=14)
plt.tight_layout()
plt.show()
```

---

## 6. When to Use (and Avoid) Pie Charts

### Use When:
- Showing parts of a single whole
- Few categories (2–5 ideal, max 7)
- Emphasizing one or two dominant slices
- Presenting to non-technical audiences

### Avoid When:
- More than 7 categories — use a bar chart instead
- Comparing across multiple groups — use grouped bar charts
- Precise comparison is needed — humans are bad at comparing angles
- Categories have similar values — bars are easier to compare

---

## 7. Common Mistakes

1. **Too many slices** — 10+ categories make the chart unreadable.
2. **3D effects** — Distort proportions. Always use flat 2D.
3. **Not starting at 0** — The total should represent 100%.
4. **Inconsistent ordering** — Sort slices by size (largest first, clockwise).
5. **Missing labels** — Every slice needs a label and percentage.

---

## 8. Best Practices

1. **Limit to 5–7 categories** — Group small values into "Other".
2. **Sort by size** — Largest slice at top (12 o'clock), going clockwise.
3. **Use consistent colors** — Same category = same color across charts.
4. **Add percentages** — `autopct='%1.1f%%'` makes values readable.
5. **Consider a bar chart** — When precision matters, bars are better.

---

## 9. Exercises

### Exercise 1: Market Share
Create a pie chart showing market share of 5 companies with the largest company exploded and a donut style.

### Exercise 2: Time Comparison
Create side-by-side pie charts comparing expense breakdowns for 2023 vs 2024.

### Exercise 3: Replace with Bar
Take a pie chart with 8 categories and convert it to a horizontal bar chart. Which is more readable?

---

## 10. Summary

| Feature | Method |
|---------|--------|
| Basic pie | `ax.pie()` |
| Percentage labels | `autopct='%1.1f%%'` |
| Donut chart | `wedgeprops=dict(width=0.4)` |
| Explode slice | `explode=(0.1, 0, ...)` |
| Legend | `ax.legend(wedges, labels)` |
| Custom format | `autopct=make_autopct(values)` |

**Key takeaway**: Pie charts are simple and intuitive for showing proportions, but they have strict limits. For more than 7 categories or when precision matters, switch to bar charts.

---

*Next: [19 – Bar Chart](19-bar-chart-lecture.md)*
