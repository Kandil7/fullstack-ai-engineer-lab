# Lecture 16: Scatter Plots in Pandas

## Learning Objectives

By the end of this lecture, you will be able to:
- Create scatter plots with Pandas and matplotlib
- Customize markers, colors, sizes, and transparency
- Add trend lines (regression lines)
- Create bubble charts with size-encoded third variables
- Use subplots for multi-variable comparison
- Interpret correlation patterns from scatter plots
- Export publication-quality figures

---

## 1. What is a Scatter Plot?

A scatter plot displays individual data points on a 2D coordinate system. Each point represents one observation, positioned by its x and y values. Scatter plots are the primary tool for visualizing **relationships between two continuous variables**.

---

## 2. Basic Scatter Plot

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample data
np.random.seed(42)
df = pd.DataFrame({
    'study_hours': np.random.uniform(1, 10, 50),
    'exam_score': np.random.uniform(40, 100, 50),
    'attendance': np.random.uniform(50, 100, 50)
})
# Add some correlation
df['exam_score'] = df['study_hours'] * 6 + np.random.normal(0, 8, 50) + 30
df['exam_score'] = df['exam_score'].clip(0, 100)

# Basic scatter plot
df.plot.scatter(x='study_hours', y='exam_score')
plt.title('Study Hours vs Exam Score')
plt.xlabel('Study Hours')
plt.ylabel('Exam Score')
plt.tight_layout()
plt.show()
```

---

## 3. Customizing Scatter Plots

### 3.1 Colors and Markers

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(
    df['study_hours'],
    df['exam_score'],
    c='steelblue',           # Color
    marker='o',              # Marker style
    s=50,                    # Size
    alpha=0.7,               # Transparency
    edgecolors='white',      # Border color
    linewidth=0.5            # Border width
)

ax.set_title('Study Hours vs Exam Score', fontsize=14)
ax.set_xlabel('Study Hours')
ax.set_ylabel('Exam Score')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### 3.2 Color Mapping by Value

```python
fig, ax = plt.subplots(figsize=(10, 6))

scatter = ax.scatter(
    df['study_hours'],
    df['exam_score'],
    c=df['attendance'],      # Color by attendance
    cmap='RdYlGn',          # Red-Yellow-Green colormap
    s=80,
    alpha=0.8,
    edgecolors='gray'
)

plt.colorbar(scatter, label='Attendance (%)')
ax.set_title('Study Hours vs Exam Score (colored by Attendance)')
ax.set_xlabel('Study Hours')
ax.set_ylabel('Exam Score')
plt.tight_layout()
plt.show()
```

### 3.3 Marker Styles by Category

```python
# Add categories
df['performance'] = pd.cut(
    df['exam_score'],
    bins=[0, 60, 80, 100],
    labels=['Below Average', 'Average', 'Above Average']
)

fig, ax = plt.subplots(figsize=(10, 6))

markers = {'Below Average': 'o', 'Average': '^', 'Above Average': 's'}
colors = {'Below Average': '#e74c3c', 'Average': '#f39c12', 'Above Average': '#2ecc71'}

for category in markers:
    mask = df['performance'] == category
    ax.scatter(
        df.loc[mask, 'study_hours'],
        df.loc[mask, 'exam_score'],
        c=colors[category],
        marker=markers[category],
        s=80,
        alpha=0.7,
        label=category
    )

ax.legend(title='Performance')
ax.set_title('Study Hours vs Exam Score by Performance')
ax.set_xlabel('Study Hours')
ax.set_ylabel('Exam Score')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 4. Bubble Charts

```python
fig, ax = plt.subplots(figsize=(12, 8))

# Size encoded by a third variable
sizes = df['attendance'] * 3  # Scale up for visibility

ax.scatter(
    df['study_hours'],
    df['exam_score'],
    s=sizes,
    c=df['attendance'],
    cmap='coolwarm',
    alpha=0.6,
    edgecolors='black',
    linewidth=0.5
)

ax.set_title('Study Hours vs Exam Score\n(Bubble size = Attendance)')
ax.set_xlabel('Study Hours')
ax.set_ylabel('Exam Score')
plt.colorbar(label='Attendance (%)')
plt.tight_layout()
plt.show()
```

---

## 5. Trend Lines

### 5.1 Simple Linear Trend

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(df['study_hours'], df['exam_score'], alpha=0.6, color='steelblue')

# Add trend line using numpy polyfit
z = np.polyfit(df['study_hours'], df['exam_score'], 1)
p = np.poly1d(z)
x_line = np.linspace(df['study_hours'].min(), df['study_hours'].max(), 100)
ax.plot(x_line, p(x_line), color='red', linewidth=2, linestyle='--', label=f'Trend: y={z[0]:.1f}x+{z[1]:.1f}')

ax.legend()
ax.set_title('Study Hours vs Exam Score with Trend Line')
ax.set_xlabel('Study Hours')
ax.set_ylabel('Exam Score')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### 5.2 Using Seaborn for Regression

```python
import seaborn as sns

# Linear regression with confidence interval
sns.regplot(
    data=df,
    x='study_hours',
    y='exam_score',
    scatter_kws={'alpha': 0.5, 'color': 'steelblue'},
    line_kws={'color': 'red', 'linewidth': 2}
)
plt.title('Study Hours vs Exam Score (with 95% CI)')
plt.tight_layout()
plt.show()
```

---

## 6. Subplots for Multi-Variable Comparison

```python
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Study hours vs exam score
axes[0].scatter(df['study_hours'], df['exam_score'], alpha=0.6, color='steelblue')
axes[0].set_title('Study Hours vs Exam Score')
axes[0].set_xlabel('Study Hours')
axes[0].set_ylabel('Exam Score')
axes[0].grid(True, alpha=0.3)

# Plot 2: Attendance vs exam score
axes[1].scatter(df['attendance'], df['exam_score'], alpha=0.6, color='coral')
axes[1].set_title('Attendance vs Exam Score')
axes[1].set_xlabel('Attendance (%)')
axes[1].set_ylabel('Exam Score')
axes[1].grid(True, alpha=0.3)

plt.suptitle('Factors Affecting Exam Performance', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()
```

---

## 7. Interpreting Scatter Plot Patterns

| Pattern | Correlation | Interpretation |
|---------|------------|----------------|
| Points trend upward | Positive | As x increases, y increases |
| Points trend downward | Negative | As x increases, y decreases |
| Points scattered randomly | None | No linear relationship |
| Tight cluster around line | Strong | High correlation |
| Loose spread | Weak | Low correlation |
| Curved pattern | Non-linear | May need transformation |
| Separate clusters | Segmented | Multiple subgroups exist |

---

## 8. Common Mistakes

1. **Overplotting** — Too many points overlap. Use `alpha`, smaller markers, or `plt.hexbin()`.
2. **Ignoring outliers** — A single extreme point can mislead. Identify and address them.
3. **Not labeling axes** — Always label x, y, and add a title.
4. **Assuming correlation = causation** — Scatter plots show association, not causation.
5. **Forgetting transparency** — Without `alpha`, dense areas look solid.

---

## 9. Best Practices

1. **Start with `alpha=0.6`** — Adjust transparency based on data density.
2. **Use colormaps meaningfully** — Color should encode a variable, not just decoration.
3. **Add trend lines** — They help the eye see the relationship.
4. **Label everything** — Title, axes, legend, units.
5. **Export at 300 DPI** for print, 150 DPI for web.

---

## 10. Exercises

### Exercise 1: Basic Scatter
Create a scatter plot of `seaborn.load_dataset('tips')` showing total_bill vs tip, colored by time of day.

### Exercise 2: Bubble Chart
Using the Iris dataset, create a bubble chart where x=sepal_length, y=petal_length, size=petal_width, color=species.

### Exercise 3: Trend Analysis
Generate 100 random data points with x and y having r=0.7 correlation. Plot with trend line and R² annotation.

---

## 11. Summary

| Feature | Method |
|---------|--------|
| Basic scatter | `df.plot.scatter()` or `ax.scatter()` |
| Color mapping | `c=` parameter with colormap |
| Size encoding | `s=` parameter |
| Transparency | `alpha=` parameter |
| Trend line | `np.polyfit()` or `sns.regplot()` |
| Subplots | `fig, axes = plt.subplots()` |

**Key takeaway**: Scatter plots reveal relationships between variables. Customize colors, sizes, and transparency to extract maximum insight from your data.

---

*Next: [17 – Histogram](17-histogram-lecture.md)*
