# Glossary 24: Advanced Plotting

## Quick Reference

| Method / Function | Purpose | Returns |
|-------------------|---------|---------|
| `plt.subplots()` | Create figure with subplots | Figure, Axes |
| `fig.add_subplot()` | Add subplot to figure | Axes |
| `gridspec.GridSpec()` | Complex subplot layouts | GridSpec |
| `plt.style.use()` | Apply theme | None |
| `plt.rcParams` | Customize defaults | dict |
| `plt.savefig()` | Export figure | None |
| `ax.annotate()` | Add text annotations | Text |
| `ax.fill_between()` | Shaded regions | PolyCollection |
| `ax.legend()` | Add legend | Legend |
| `ax.set_title()` | Set plot title | Text |
| `ax.set_xlabel()` | Set x-axis label | Text |
| `ax.yaxis.set_major_formatter()` | Format tick labels | Formatter |
| `mdates.DateFormatter()` | Format date ticks | Formatter |
| `mticker.FuncFormatter()` | Custom tick format | Formatter |

---

## Alphabetical Definitions

### A

**annotate()**
Adds text annotations with optional arrows. Essential for highlighting key data points.
```python
ax.annotate('Peak', xy=(x_peak, y_peak), xytext=(10, 10),
            textcoords='offset points', arrowprops=dict(arrowstyle='->'))
```

### B

**bbox_inches='tight'**
Parameter in `savefig()` that trims whitespace around the figure. Always use for clean exports.
```python
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
```

### C

**Colorblind-Friendly Palettes**
Color schemes that remain distinguishable for people with color vision deficiency. Use `seaborn.color_palette('colorblind')` or viridis.
```python
palette = sns.color_palette('colorblind', 6)
```

### D

**DateFormatter**
Matplotlib formatter that converts datetime objects to readable strings.
```python
import matplotlib.dates as mdates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
```

**DPI (Dots Per Inch)**
Resolution setting for raster exports. 300 DPI for print, 150 DPI for web, 72 DPI for screens.
```python
plt.savefig('plot.png', dpi=300)
```

### F

**fill_between()**
Creates a shaded region between two lines. Useful for confidence bands, ranges, or profit/loss zones.
```python
ax.fill_between(x, y1, y2, alpha=0.3, color='blue')
```

**FuncFormatter**
Custom function for formatting tick labels. More flexible than string formatting.
```python
import matplotlib.ticker as mticker
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
```

### G

**GridSpec**
Defines complex subplot layouts with varying sizes. Allows spanning rows/columns.
```python
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
ax = fig.add_subplot(gs[0, :2])  # Span 2 columns
```

### L

**legend()**
Adds a legend to the plot. Customize location, font, frame, and title.
```python
ax.legend(loc='upper left', framealpha=0.9, title='Metrics')
```

### M

**matplotlibrc**
Configuration file for default plot settings. Located at `~/.config/matplotlib/matplotlibrc`.

### P

**plt.style.use()**
Applies a built-in or custom style theme. Options: `'seaborn-v0_8'`, `'ggplot'`, `'dark_background'`, etc.
```python
plt.style.use('seaborn-v0_8-whitegrid')
```

**plt.rcParams**
Dictionary of default plot parameters. Can be updated for custom styling.
```python
plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 14,
    'figure.facecolor': 'white'
})
```

### R

**rcParams**
Runtime configuration parameters controlling fonts, colors, sizes, and behavior of all matplotlib plots.

### S

**savefig()**
Exports the current figure to a file. Supports PNG, PDF, SVG, EPS, and more.
```python
plt.savefig('figure.png', dpi=300, bbox_inches='tight', transparent=False)
```

**subplots()**
Creates a figure with a grid of subplots. Returns Figure and Axes objects.
```python
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes[0, 0].plot(x, y)  # Access specific subplot
```

---

## Code Examples

### Example 1: Publication-Quality Figure

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# Custom style
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'figure.facecolor': 'white',
    'axes.facecolor': '#f8f9fa',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--'
})

# Data
np.random.seed(42)
months = pd.date_range('2024-01-01', periods=12, freq='M')
revenue = np.cumsum(np.random.randn(12) * 10000) + 100000

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(months, revenue, color='#3498db', linewidth=2.5, marker='o', markersize=6)
ax.fill_between(months, revenue, alpha=0.15, color='#3498db')

# Format
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
ax.set_title('Annual Revenue Performance', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Month')
ax.set_ylabel('Revenue ($)')
ax.set_xlim(months[0], months[-1])

# Annotate peak
peak_idx = np.argmax(revenue)
ax.annotate(
    f'Peak: ${revenue[peak_idx]:,.0f}',
    xy=(months[peak_idx], revenue[peak_idx]),
    xytext=(20, 20), textcoords='offset points',
    arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1.5),
    fontsize=10, color='#e74c3c', fontweight='bold'
)

plt.tight_layout()
plt.savefig('revenue_chart.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Example 2: Multi-Panel Dashboard

```python
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

# Panel 1: Main trend (spans 2 columns)
ax1 = fig.add_subplot(gs[0, :2])
ax1.plot(months, revenue, color='blue', linewidth=2)
ax1.set_title('Revenue Trend')
ax1.fill_between(months, revenue, alpha=0.2)

# Panel 2: Stats box
ax2 = fig.add_subplot(gs[0, 2])
ax2.axis('off')
stats = f"""Revenue Summary
──────────────
Mean:    ${np.mean(revenue):>10,.0f}
Median:  ${np.median(revenue):>10,.0f}
Std Dev: ${np.std(revenue):>10,.0f}
Total:   ${np.sum(revenue):>10,.0f}"""
ax2.text(0.1, 0.5, stats, transform=ax2.transAxes,
         fontsize=11, fontfamily='monospace', verticalalignment='center')

# Panel 3: Monthly bars
ax3 = fig.add_subplot(gs[1, :])
colors = ['#2ecc71' if r > np.mean(revenue) else '#e74c3c' for r in revenue]
ax3.bar(months, revenue, color=colors, width=20)
ax3.set_title('Monthly Revenue (Green = Above Average)')
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))

# Panel 4: Pie
ax4 = fig.add_subplot(gs[2, 0])
quarters = pd.Series(revenue).groupby(np.arange(12)//3).sum()
ax4.pie(quarters, labels=[f'Q{i+1}' for i in range(4)],
        autopct='%1.1f%%', colors=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
ax4.set_title('Quarterly Split')

# Panel 5: Moving average
ax5 = fig.add_subplot(gs[2, 1:])
ma3 = pd.Series(revenue).rolling(3).mean()
ax5.plot(months, revenue, color='gray', alpha=0.5, label='Actual')
ax5.plot(months, ma3, color='red', linewidth=2, label='3-Month MA')
ax5.legend()
ax5.set_title('Moving Average')

plt.suptitle('Financial Dashboard', fontsize=18, fontweight='bold', y=1.01)
plt.savefig('dashboard.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## Related Terms

| Term | Related To | Connection |
|------|-----------|------------|
| `subplots()` | `GridSpec` | Simple vs complex layouts |
| `savefig()` | `dpi` | Export quality control |
| `rcParams` | `plt.style.use()` | Custom styling |
| `annotate()` | Arrow props | Highlighting data points |
| `fill_between()` | Confidence bands | Shaded regions |
| `FuncFormatter()` | `ticker` | Custom axis labels |
| `tight_layout()` | `bbox_inches` | Prevents label clipping |

---

*See also: [Lecture 24](24-plotting-lecture.md) | [Lecture 16 – Scatter Plot](16-scatter-plot-lecture.md)*
