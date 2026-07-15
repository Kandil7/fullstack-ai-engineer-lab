# Lecture 24: Advanced Plotting in Pandas

## Learning Objectives

By the end of this lecture, you will be able to:
- Create publication-quality figures with matplotlib
- Build complex multi-panel layouts
- Customize every aspect of a plot (colors, fonts, axes, legends)
- Export figures in multiple formats
- Use Pandas plotting API effectively
- Apply professional styling and themes
- Create time series plots with proper formatting

---

## 1. Pandas Plotting API

Pandas integrates with matplotlib for quick plotting.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample data
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=12, freq='M')
df = pd.DataFrame({
    'date': dates,
    'revenue': np.random.randint(50000, 150000, 12),
    'expenses': np.random.randint(30000, 100000, 12),
    'profit': np.random.randint(10000, 50000, 12)
})

# Quick line plot
df.plot(x='date', y=['revenue', 'expenses', 'profit'], figsize=(12, 6))
plt.title('Financial Overview')
plt.tight_layout()
plt.show()
```

---

## 2. Subplots and Layouts

### 2.1 Basic Subplots

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Top-left: Line plot
axes[0, 0].plot(df['date'], df['revenue'], color='blue', linewidth=2)
axes[0, 0].set_title('Revenue Trend')
axes[0, 0].set_ylabel('Revenue ($)')

# Top-right: Bar chart
axes[0, 1].bar(df['date'].dt.month, df['revenue'], color='steelblue')
axes[0, 1].set_title('Monthly Revenue')

# Bottom-left: Scatter
axes[1, 0].scatter(df['revenue'], df['expenses'], color='coral', s=50)
axes[1, 0].set_title('Revenue vs Expenses')
axes[1, 0].set_xlabel('Revenue')
axes[1, 0].set_ylabel('Expenses')

# Bottom-right: Pie chart
monthly_profit = df.groupby(df['date'].dt.quarter)['profit'].sum()
axes[1, 1].pie(monthly_profit.values, labels=[f'Q{i}' for i in monthly_profit.index],
               autopct='%1.1f%%', colors=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
axes[1, 1].set_title('Profit by Quarter')

plt.suptitle('Financial Dashboard', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()
```

### 2.2 GridSpec for Complex Layouts

```python
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(16, 10))
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.3)

# Large plot spanning 2 columns
ax1 = fig.add_subplot(gs[0, :2])
ax1.plot(df['date'], df['revenue'], color='blue', linewidth=2)
ax1.set_title('Revenue Trend')
ax1.fill_between(df['date'], df['revenue'], alpha=0.3)

# Right column - stats
ax2 = fig.add_subplot(gs[0, 2])
ax2.axis('off')
stats_text = f"""
Revenue Stats
─────────────
Mean:  ${df['revenue'].mean():,.0f}
Max:   ${df['revenue'].max():,.0f}
Min:   ${df['revenue'].min():,.0f}
Total: ${df['revenue'].sum():,.0f}
"""
ax2.text(0.1, 0.5, stats_text, transform=ax2.transAxes,
         fontsize=12, verticalalignment='center', fontfamily='monospace')

# Bottom row
ax3 = fig.add_subplot(gs[1, :])
ax3.bar(df['date'], df['revenue'], color='steelblue', alpha=0.7, label='Revenue')
ax3.bar(df['date'], df['expenses'], color='coral', alpha=0.7, label='Expenses')
ax3.legend()
ax3.set_title('Revenue vs Expenses')

plt.suptitle('Financial Dashboard', fontsize=16, fontweight='bold')
plt.show()
```

---

## 3. Professional Styling

### 3.1 Custom Style

```python
# Create a custom style
plt.style.use('seaborn-v0_8-whitegrid')

# Or create your own
custom_style = {
    'figure.facecolor': 'white',
    'axes.facecolor': '#f8f9fa',
    'axes.edgecolor': '#dee2e6',
    'axes.labelcolor': '#333333',
    'text.color': '#333333',
    'xtick.color': '#666666',
    'ytick.color': '#666666',
    'grid.color': '#e9ecef',
    'grid.linestyle': '--',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12
}

plt.rcParams.update(custom_style)
```

### 3.2 Custom Colors

```python
# Color palette
COLORS = {
    'primary': '#3498db',
    'secondary': '#e74c3c',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'muted': '#95a5a6'
}

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['date'], df['revenue'], color=COLORS['primary'], linewidth=2, label='Revenue')
ax.plot(df['date'], df['expenses'], color=COLORS['secondary'], linewidth=2, label='Expenses')
ax.fill_between(df['date'], df['revenue'], df['expenses'],
                where=df['revenue'] > df['expenses'],
                color=COLORS['success'], alpha=0.3, label='Profit Zone')
ax.fill_between(df['date'], df['revenue'], df['expenses'],
                where=df['revenue'] <= df['expenses'],
                color=COLORS['secondary'], alpha=0.3, label='Loss Zone')
ax.legend()
plt.tight_layout()
plt.show()
```

---

## 4. Axis Formatting

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df['date'], df['revenue'], color='blue', linewidth=2)

# Custom tick formatting
import matplotlib.ticker as mticker
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))

# Rotate date labels
plt.xticks(rotation=45)

# Add grid
ax.grid(True, alpha=0.3, linestyle='--')

# Set limits
ax.set_xlim(df['date'].min(), df['date'].max())
ax.set_ylim(0, df['revenue'].max() * 1.1)

# Add annotations
max_revenue = df.loc[df['revenue'].idxmax()]
ax.annotate(
    f'Peak: ${max_revenue["revenue"]:,.0f}',
    xy=(max_revenue['date'], max_revenue['revenue']),
    xytext=(10, 10),
    textcoords='offset points',
    arrowprops=dict(arrowstyle='->', color='red'),
    fontsize=10,
    color='red'
)

plt.tight_layout()
plt.show()
```

---

## 5. Legend Customization

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df['date'], df['revenue'], linewidth=2, label='Revenue')
ax.plot(df['date'], df['expenses'], linewidth=2, label='Expenses')
ax.plot(df['date'], df['profit'], linewidth=2, label='Profit', linestyle='--')

# Custom legend
ax.legend(
    loc='upper left',
    frameon=True,
    framealpha=0.9,
    edgecolor='gray',
    fontsize=11,
    title='Metrics',
    title_fontsize=12
)

plt.tight_layout()
plt.show()
```

---

## 6. Exporting Figures

```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['date'], df['revenue'])
ax.set_title('Revenue Trend')
plt.tight_layout()

# PNG (raster)
plt.savefig('plot.png', dpi=300, bbox_inches='tight')

# PDF (vector)
plt.savefig('plot.pdf', bbox_inches='tight')

# SVG (vector, web)
plt.savefig('plot.svg', bbox_inches='tight')

# Transparent background
plt.savefig('plot_transparent.png', transparent=True, dpi=300)
```

---

## 7. Time Series Plotting

```python
fig, ax = plt.subplots(figsize=(12, 6))

# Main line
ax.plot(df['date'], df['revenue'], color='blue', linewidth=2, label='Revenue')

# Moving average
df['revenue_ma3'] = df['revenue'].rolling(3).mean()
ax.plot(df['date'], df['revenue_ma3'], color='red', linewidth=2,
        linestyle='--', label='3-Month MA')

# Confidence band
std = df['revenue'].rolling(3).std()
ax.fill_between(df['date'],
                df['revenue_ma3'] - 2*std,
                df['revenue_ma3'] + 2*std,
                alpha=0.2, color='red', label='±2σ Band')

# Format x-axis as months
import matplotlib.dates as mdates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator())

plt.xticks(rotation=45)
ax.set_title('Revenue Trend with Moving Average')
ax.set_xlabel('Date')
ax.set_ylabel('Revenue ($)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 8. Common Mistakes

1. **Too much clutter** — Remove unnecessary elements (borders, ticks, gridlines).
2. **Inconsistent styling** — Use the same colors and fonts throughout a report.
3. **Not saving at high DPI** — Use 300 DPI for print, 150 for web.
4. **Ignoring accessibility** — Use colorblind-friendly palettes.
5. **Forgetting titles and labels** — Every plot needs context.

---

## 9. Best Practices

1. **Start with `plt.style.use()`** — Apply a consistent theme first.
2. **Use `fig, ax` interface** — More control than the pandas `.plot()` API.
3. **Limit to 5-6 colors** — Group similar categories.
4. **Export as vector (PDF/SVG)** for print, raster (PNG) for web.
5. **Add source attribution** — "Data: XYZ, 2024"

---

## 10. Exercises

### Exercise 1: Dashboard
Create a 2x2 dashboard with: line chart, bar chart, pie chart, and statistics text box.

### Exercise 2: Time Series
Plot monthly revenue with moving average, confidence band, and annotated peak value.

### Exercise 3: Export
Create a publication-quality figure and export it as both PNG (300 DPI) and PDF.

---

## 11. Summary

| Feature | Method |
|---------|--------|
| Subplots | `plt.subplots(rows, cols)` |
| GridSpec | `gridspec.GridSpec()` for complex layouts |
| Styling | `plt.style.use()` or `plt.rcParams` |
| Axis formatting | `ax.yaxis.set_major_formatter()` |
| Annotations | `ax.annotate()` |
| Export | `plt.savefig()` with dpi parameter |
| Time series | `mdates.DateFormatter()` for date axes |

**Key takeaway**: Professional plotting is about clarity and consistency. Master the `fig, ax` interface, apply consistent styling, and always export at appropriate resolution.

---

*This concludes the Pandas lecture series! Review earlier topics as needed.*
