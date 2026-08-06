"""
Matplotlib Scatter Plots: scatter, bubble, color mapping
=========================================================
"""

import pathlib
import matplotlib.pyplot as plt
OUTPUT_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "outputs" / "matplotlib"
import pathlib
import numpy as np

# =============================================================================
# 1. BASIC SCATTER
# =============================================================================

print("=" * 60)
print("1. BASIC SCATTER PLOT")
print("=" * 60)

np.random.seed(42)
n = 200
x = np.random.randn(n)
y = 2 * x + np.random.randn(n) * 0.8

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(x, y, alpha=0.6, edgecolors='black', linewidth=0.5)
ax.set_title('Basic Scatter Plot')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("../../../outputs/matplotlib/scatter_basic.png", dpi=150)
plt.close()

print("Basic scatter saved")
print()

# =============================================================================
# 2. COLOR MAPPING
# =============================================================================

print("=" * 60)
print("2. COLOR MAPPING")
print("=" * 60)

# Third variable mapped to color
z = np.random.randn(n)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Continuous colormap
sc1 = axes[0, 0].scatter(x, y, c=z, cmap='viridis', alpha=0.7, s=50)
plt.colorbar(sc1, ax=axes[0, 0], label='Z Value')
axes[0, 0].set_title('Continuous: viridis')
axes[0, 0].grid(True, alpha=0.3)

# Different colormap
sc2 = axes[0, 1].scatter(x, y, c=z, cmap='RdYlBu', alpha=0.7, s=50)
plt.colorbar(sc2, ax=axes[0, 1], label='Z Value')
axes[0, 1].set_title('Diverging: RdYlBu')
axes[0, 1].grid(True, alpha=0.3)

# Categorical colors
categories = np.random.choice(['A', 'B', 'C', 'D'], n)
cat_colors = {'A': 'red', 'B': 'blue', 'C': 'green', 'D': 'orange'}
colors = [cat_colors[c] for c in categories]
axes[1, 0].scatter(x, y, c=colors, alpha=0.7, s=50)
# Legend for categories
for cat, color in cat_colors.items():
    axes[1, 0].scatter([], [], c=color, label=cat, alpha=0.7)
axes[1, 0].legend(title='Category')
axes[1, 0].set_title('Categorical Colors')
axes[1, 0].grid(True, alpha=0.3)

# Custom normalization
sc3 = axes[1, 1].scatter(x, y, c=z, cmap='plasma', alpha=0.7, s=50,
                          vmin=-2, vmax=2)  # Fixed range
plt.colorbar(sc3, ax=axes[1, 1], label='Z Value (clipped)')
axes[1, 1].set_title('Custom vmin/vmax')
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('Color Mapping Techniques', fontsize=16)
plt.tight_layout()
plt.savefig("../../../outputs/matplotlib/scatter_colormap.png", dpi=150)
plt.close()

print("Color mapping scatter saved")
print()

# =============================================================================
# 3. SIZE MAPPING (BUBBLE PLOTS)
# =============================================================================

print("=" * 60)
print("3. BUBBLE PLOTS (SIZE MAPPING)")
print("=" * 60)

# Fourth variable mapped to size
sizes = np.abs(np.random.randn(n)) * 500 + 20

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Basic bubble
axes[0, 0].scatter(x, y, s=sizes, alpha=0.5, c='blue')
axes[0, 0].set_title('Basic Bubble Plot')
axes[0, 0].grid(True, alpha=0.3)

# Color + Size
sc = axes[0, 1].scatter(x, y, s=sizes, c=z, cmap='viridis', alpha=0.6)
plt.colorbar(sc, ax=axes[0, 1], label='Z')
axes[0, 1].set_title('Color + Size Mapping')
axes[0, 1].grid(True, alpha=0.3)

# Log scale for sizes
sizes_log = np.exp(np.random.randn(n) * 0.5) * 100
axes[1, 0].scatter(x, y, s=sizes_log, alpha=0.5, c='red')
axes[1, 0].set_title('Log-scale Sizes')
axes[1, 0].grid(True, alpha=0.3)

# Custom size scaling
def scale_sizes(values, min_size=10, max_size=1000):
    vmin, vmax = values.min(), values.max()
    if vmax == vmin:
        return np.full_like(values, (min_size + max_size) / 2)
    return min_size + (values - vmin) / (vmax - vmin) * (max_size - min_size)

scaled_sizes = scale_sizes(np.abs(z), 20, 500)
axes[1, 1].scatter(x, y, s=scaled_sizes, c=z, cmap='coolwarm', alpha=0.6)
axes[1, 1].set_title('Custom Size Scaling')
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('Bubble Plot Variations', fontsize=16)
plt.tight_layout()
plt.savefig("../../../outputs/matplotlib/scatter_bubble.png", dpi=150)
plt.close()

print("Bubble plots saved")
print()

# =============================================================================
# 4. REGRESSION & TREND LINES
# =============================================================================

print("=" * 60)
print("4. REGRESSION LINES")
print("=" * 60)

from scipy import stats

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
line_x = np.array([x.min(), x.max()])
line_y = slope * line_x + intercept

axes[0, 0].scatter(x, y, alpha=0.5, s=30)
axes[0, 0].plot(line_x, line_y, 'r-', linewidth=2, 
                label=f'y={slope:.2f}x+{intercept:.2f}, R²={r_value**2:.3f}')
axes[0, 0].legend()
axes[0, 0].set_title('Linear Regression')
axes[0, 0].grid(True, alpha=0.3)

# Multiple groups with regression
groups = np.random.choice(['Group 1', 'Group 2', 'Group 3'], n)
colors = {'Group 1': 'red', 'Group 2': 'blue', 'Group 3': 'green'}

for group in ['Group 1', 'Group 2', 'Group 3']:
    mask = groups == group
    x_g, y_g = x[mask], y[mask]
    axes[0, 1].scatter(x_g, y_g, alpha=0.5, s=30, c=colors[group], label=group)
    if len(x_g) > 1:
        slope_g, intercept_g, _, _, _ = stats.linregress(x_g, y_g)
        line_x_g = np.array([x_g.min(), x_g.max()])
        line_y_g = slope_g * line_x_g + intercept_g
        axes[0, 1].plot(line_x_g, line_y_g, '-', color=colors[group], linewidth=2)
axes[0, 1].legend()
axes[0, 1].set_title('Grouped Regression')
axes[0, 1].grid(True, alpha=0.3)

# LOWESS smoothing
from scipy.interpolate import UnivariateSpline
spline = UnivariateSpline(x, y, s=len(x))
x_smooth = np.linspace(x.min(), x.max(), 200)
y_smooth = spline(x_smooth)

axes[1, 0].scatter(x, y, alpha=0.3, s=20)
axes[1, 0].plot(x_smooth, y_smooth, 'r-', linewidth=3, label='Spline')
axes[1, 0].legend()
axes[1, 0].set_title('Spline Smoothing')
axes[1, 0].grid(True, alpha=0.3)

# Quantile regression concept (using rolling)
sorted_idx = np.argsort(x)
x_sorted = x[sorted_idx]
y_sorted = y[sorted_idx]
window = 20
rolling_median = pd.Series(y_sorted).rolling(window, center=True).median()
rolling_q25 = pd.Series(y_sorted).rolling(window, center=True).quantile(0.25)
rolling_q75 = pd.Series(y_sorted).rolling(window, center=True).quantile(0.75)

axes[1, 1].scatter(x, y, alpha=0.3, s=20)
axes[1, 1].plot(x_sorted, rolling_median, 'r-', linewidth=2, label='Rolling Median')
axes[1, 1].fill_between(x_sorted, rolling_q25, rolling_q75, alpha=0.2, color='red', label='IQR')
axes[1, 1].legend()
axes[1, 1].set_title('Rolling Quantiles')
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('Regression and Trend Lines', fontsize=16)
plt.tight_layout()
plt.savefig("../../../outputs/matplotlib/scatter_regression.png", dpi=150)
plt.close()

print("Regression plots saved")
print()

# =============================================================================
# 5. HEXBIN AND 2D HISTOGRAM
# =============================================================================

print("=" * 60)
print("5. HEXBIN AND 2D DENSITY")
print("=" * 60)

# Large dataset for density
n_large = 50000
x_large = np.random.randn(n_large)
y_large = 2 * x_large + np.random.randn(n_large) * 0.8

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Hexbin
hb1 = axes[0, 0].hexbin(x_large, y_large, gridsize=30, cmap='Blues', mincnt=1)
plt.colorbar(hb1, ax=axes[0, 0], label='Count')
axes[0, 0].set_title('Hexbin (Count)')
axes[0, 0].grid(True, alpha=0.3)

# Hexbin with log scale
hb2 = axes[0, 1].hexbin(x_large, y_large, gridsize=30, cmap='Reds', 
                         bins='log', mincnt=1)
plt.colorbar(hb2, ax=axes[0, 1], label='Log Count')
axes[0, 1].set_title('Hexbin (Log Scale)')
axes[0, 1].grid(True, alpha=0.3)

# 2D Histogram
hb3 = axes[1, 0].hist2d(x_large, y_large, bins=40, cmap='Greens')
plt.colorbar(hb3[3], ax=axes[1, 0], label='Count')
axes[1, 0].set_title('2D Histogram (hist2d)')
axes[1, 0].grid(True, alpha=0.3)

# KDE contour
from scipy.stats import gaussian_kde
xy = np.vstack([x_large, y_large])
kde = gaussian_kde(xy)
xi, yi = np.mgrid[x_large.min():x_large.max():100j, y_large.min():y_large.max():100j]
zi = kde(np.vstack([xi.flatten(), yi.flatten()]))

axes[1, 1].contourf(xi, yi, zi.reshape(xi.shape), levels=20, cmap='Purples', alpha=0.7)
axes[1, 1].scatter(x_large[::100], y_large[::100], alpha=0.1, s=1, c='black')
axes[1, 1].set_title('KDE Contour')
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('Density Visualization for Large Datasets', fontsize=16)
plt.tight_layout()
plt.savefig("../../../outputs/matplotlib/scatter_density.png", dpi=150)
plt.close()

print("Density plots saved")
print()

# =============================================================================
# 6. ANNOTATIONS AND HIGHLIGHTING
# =============================================================================

print("=" * 60)
print("6. ANNOTATIONS AND HIGHLIGHTING")
print("=" * 60)

fig, ax = plt.subplots(figsize=(10, 8))

# Plot
sc = ax.scatter(x, y, c=z, cmap='viridis', alpha=0.6, s=50)

# Highlight specific points
# Top 5 by Z value
top5_idx = np.argsort(z)[-5:]
ax.scatter(x[top5_idx], y[top5_idx], s=200, facecolors='none', 
           edgecolors='red', linewidths=2, label='Top 5 Z')

# Annotate
for idx in top5_idx:
    ax.annotate(f'Z={z[idx]:.2f}', (x[idx], y[idx]), 
                xytext=(10, 10), textcoords='offset points',
                fontsize=9, color='red', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='red'))

# Quadrant lines
ax.axhline(y=y.mean(), color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=x.mean(), color='gray', linestyle='--', alpha=0.5)

# Quadrant labels
ax.text(0.95, 0.95, 'Q1', transform=ax.transAxes, fontsize=14, 
        ha='right', va='top', alpha=0.5)
ax.text(0.05, 0.95, 'Q2', transform=ax.transAxes, fontsize=14, 
        ha='left', va='top', alpha=0.5)
ax.text(0.05, 0.05, 'Q3', transform=ax.transAxes, fontsize=14, 
        ha='left', va='bottom', alpha=0.5)
ax.text(0.95, 0.05, 'Q4', transform=ax.transAxes, fontsize=14, 
        ha='right', va='bottom', alpha=0.5)

ax.set_title('Annotated Scatter with Highlights', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)
plt.colorbar(sc, ax=ax, label='Z Value')
plt.tight_layout()
plt.savefig("../../../outputs/matplotlib/scatter_annotated.png", dpi=150)
plt.close()

print("Annotated scatter saved")
print()

# =============================================================================
# SUMMARY
# =============================================================================

print("=" * 60)
print("SCATTER PLOTS COMPLETE")
print("=" * 60)
print("""
Key Concepts:
1. Basic scatter: plt.scatter(x, y)
2. Color mapping: c parameter with colormaps (viridis, RdYlBu, etc.)
3. Size mapping: s parameter for bubble plots
4. Regression lines: scipy.stats.linregress
5. Density: hexbin, hist2d, KDE contours for large datasets
6. Annotations: annotate, highlight outliers, quadrant lines

Next: Bar charts, histograms, box plots
""")