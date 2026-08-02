"""
Matplotlib Histograms and Density Plots
========================================
"""

import pathlib
import matplotlib.pyplot as plt
OUTPUT_DIR = pathlib.Path(__file__).parent.parent.parent / "outputs" / "matplotlib"
import pathlib
import numpy as np
import pandas as pd
from scipy import stats

# =============================================================================
# 1. BASIC HISTOGRAM
# =============================================================================

print("=" * 60)
print("1. BASIC HISTOGRAM")
print("=" * 60)

np.random.seed(42)

# Generate sample data
normal_data = np.random.randn(10000)
exponential_data = np.random.exponential(2, 10000)
bimodal_data = np.concatenate([
    np.random.normal(-2, 1, 5000),
    np.random.normal(2, 1, 5000)
])

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Normal distribution
axes[0, 0].hist(normal_data, bins=50, density=True, alpha=0.7, 
                color='steelblue', edgecolor='black', linewidth=0.5)
# Overlay theoretical normal
x = np.linspace(-4, 4, 100)
axes[0, 0].plot(x, stats.norm.pdf(x), 'r-', linewidth=2, label='N(0,1)')
axes[0, 0].set_title('Normal Distribution')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Exponential
axes[0, 1].hist(exponential_data, bins=50, density=True, alpha=0.7,
                color='coral', edgecolor='black', linewidth=0.5)
x = np.linspace(0, 10, 100)
axes[0, 1].plot(x, stats.expon.pdf(x, scale=2), 'r-', linewidth=2, label='Exp(2)')
axes[0, 1].set_title('Exponential Distribution')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Bimodal
axes[0, 2].hist(bimodal_data, bins=50, density=True, alpha=0.7,
                color='mediumseagreen', edgecolor='black', linewidth=0.5)
axes[0, 2].set_title('Bimodal Distribution')
axes[0, 2].grid(True, alpha=0.3)

# Cumulative histogram
axes[1, 0].hist(normal_data, bins=50, density=True, cumulative=True, 
                alpha=0.7, color='purple', edgecolor='black', linewidth=0.5)
axes[1, 0].plot(x, stats.norm.cdf(x), 'r-', linewidth=2, label='CDF')
axes[1, 0].set_title('Cumulative Histogram')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Step histogram
axes[1, 1].hist(normal_data, bins=50, density=True, histtype='step',
                linewidth=2, color='darkred', label='Step')
axes[1, 1].hist(normal_data, bins=50, density=True, histtype='stepfilled',
                alpha=0.3, color='red', label='Stepfilled')
axes[1, 1].set_title('Step vs Stepfilled')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# Log scale histogram
axes[1, 2].hist(exponential_data, bins=50, density=True, alpha=0.7,
                color='orange', edgecolor='black', linewidth=0.5)
axes[1, 2].set_yscale('log')
axes[1, 2].set_title('Log Scale Y-axis')
axes[1, 2].grid(True, alpha=0.3)

plt.suptitle('Histogram Variations', fontsize=16)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "hist_basic.png", dpi=150)
plt.close()

print("Basic histograms saved")
print()

# =============================================================================
# 2. HISTOGRAM CUSTOMIZATION
# =============================================================================

print("=" * 60)
print("2. HISTOGRAM CUSTOMIZATION")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Different bin strategies
data = np.random.randn(1000) + np.random.randn(1000) * 0.5  # Mixture

# Auto bins (Sturges)
axes[0, 0].hist(data, bins='auto', density=True, alpha=0.7, 
                color='skyblue', edgecolor='black')
axes[0, 0].set_title("bins='auto' (Sturges)")

# Square root rule
axes[0, 1].hist(data, bins=int(np.sqrt(len(data))), density=True, alpha=0.7,
                color='lightcoral', edgecolor='black')
axes[0, 1].set_title("bins=sqrt(n)")

# Freedman-Diaconis
from scipy.stats import iqr
bin_width = 2 * iqr(data) / (len(data) ** (1/3))
bins_fd = int((data.max() - data.min()) / bin_width)
axes[1, 0].hist(data, bins=bins_fd, density=True, alpha=0.7,
                color='lightgreen', edgecolor='black')
axes[1, 0].set_title(f"Freedman-Diaconis ({bins_fd} bins)")

# Custom bins
custom_bins = np.linspace(-4, 4, 21)
axes[1, 1].hist(data, bins=custom_bins, density=True, alpha=0.7,
                color='gold', edgecolor='black')
axes[1, 1].set_title("Custom bins (linspace)")

for ax in axes.flat:
    ax.grid(True, alpha=0.3)

plt.suptitle('Binning Strategies', fontsize=16)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "hist_bins.png", dpi=150)
plt.close()

print("Binning strategies saved")
print()

# =============================================================================
# 3. 2D HISTOGRAMS
# =============================================================================

print("=" * 60)
print("3. 2D HISTOGRAMS")
print("=" * 60)

# Correlated data
x = np.random.randn(10000)
y = 0.7 * x + np.random.randn(10000) * 0.7

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# hist2d
h = axes[0, 0].hist2d(x, y, bins=40, cmap='Blues', density=True)
plt.colorbar(h[3], ax=axes[0, 0], label='Density')
axes[0, 0].set_title('hist2d')
axes[0, 0].grid(True, alpha=0.3)

# hexbin
hb = axes[0, 1].hexbin(x, y, gridsize=30, cmap='Reds', mincnt=1)
plt.colorbar(hb, ax=axes[0, 1], label='Count')
axes[0, 1].set_title('hexbin')
axes[0, 1].grid(True, alpha=0.3)

# 2D histogram with marginal
# Main plot
h = axes[1, 0].hist2d(x, y, bins=30, cmap='Greens', density=True)
plt.colorbar(h[3], ax=axes[1, 0], label='Density')
# Marginal x
axes[1, 0].hist(x, bins=30, density=True, alpha=0.5, color='red', 
                orientation='vertical', bottom=axes[1, 0].get_ylim()[0])
# Marginal y
axes[1, 0].hist(y, bins=30, density=True, alpha=0.5, color='blue',
                orientation='horizontal', bottom=axes[1, 0].get_xlim()[0])
axes[1, 0].set_title('hist2d with Marginals')
axes[1, 0].grid(True, alpha=0.3)

# Joint plot style (using subplots manually)
from mpl_toolkits.axes_grid1 import make_axes_locatable

fig2 = plt.figure(figsize=(8, 8))
ax_main = fig2.add_subplot(111)
hb = ax_main.hexbin(x, y, gridsize=30, cmap='Blues', mincnt=1)
divider = make_axes_locatable(ax_main)
ax_histx = divider.append_axes("top", size=1.2, pad=0.1, sharex=ax_main)
ax_histy = divider.append_axes("right", size=1.2, pad=0.1, sharey=ax_main)

ax_histx.hist(x, bins=30, density=True, alpha=0.5, color='steelblue')
ax_histy.hist(y, bins=30, density=True, alpha=0.5, color='coral', 
              orientation='horizontal')
ax_histx.axis('off')
ax_histy.axis('off')

plt.colorbar(hb, ax=ax_main, label='Count')
ax_main.set_title('Joint Hexbin with Marginals')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "hist_2d.png", dpi=150)
plt.close()

print("2D histograms saved")
print()

# =============================================================================
# 4. KDE AND DENSITY
# =============================================================================

print("=" * 60)
print("4. KDE AND DENSITY ESTIMATION")
print("=" * 60)

from scipy.stats import gaussian_kde

data = np.random.randn(1000) * 2 + 1

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Histogram with KDE
axes[0, 0].hist(data, bins=30, density=True, alpha=0.5, 
                color='skyblue', edgecolor='black', label='Histogram')
# KDE
kde = gaussian_kde(data)
x_grid = np.linspace(data.min() - 1, data.max() + 1, 200)
axes[0, 0].plot(x_grid, kde(x_grid), 'r-', linewidth=2, label='KDE')
axes[0, 0].plot(x_grid, stats.norm.pdf(x_grid, data.mean(), data.std()), 
                'g--', linewidth=2, label='Normal Fit')
axes[0, 0].legend()
axes[0, 0].set_title('Histogram + KDE + Normal Fit')
axes[0, 0].grid(True, alpha=0.3)

# Multiple KDEs (different bandwidths)
for bw in [0.1, 0.3, 0.5, 1.0]:
    kde = gaussian_kde(data, bw_method=bw)
    axes[0, 1].plot(x_grid, kde(x_grid), label=f'bw={bw}')
axes[0, 1].hist(data, bins=30, density=True, alpha=0.2, color='gray')
axes[0, 1].legend()
axes[0, 1].set_title('KDE with Different Bandwidths')
axes[0, 1].grid(True, alpha=0.3)

# 2D KDE
x2 = np.random.randn(2000)
y2 = 0.5 * x2 + np.random.randn(2000) * 0.8
xy = np.vstack([x2, y2])
kde2d = gaussian_kde(xy)

xi, yi = np.mgrid[x2.min():x2.max():100j, y2.min():y2.max():100j]
zi = kde2d(np.vstack([xi.flatten(), yi.flatten()]))

axes[1, 0].contourf(xi, yi, zi.reshape(xi.shape), levels=20, cmap='Blues', alpha=0.7)
axes[1, 0].scatter(x2, y2, s=1, alpha=0.1, c='black')
axes[1, 0].set_title('2D KDE Contour')
axes[1, 0].grid(True, alpha=0.3)

# Violin plot (density-based)
data_list = [
    np.random.normal(0, 1, 200),
    np.random.normal(2, 1.5, 200),
    np.random.exponential(2, 200) - 2,
    np.random.gamma(2, 1, 200) - 2
]
parts = axes[1, 1].violinplot(data_list, showmeans=True, showmedians=True, 
                               showextrema=True)
for pc in parts['bodies']:
    pc.set_facecolor('lightblue')
    pc.set_alpha(0.7)
axes[1, 1].set_xticks([1, 2, 3, 4])
axes[1, 1].set_xticklabels(['Normal', 'Normal\n(wider)', 'Exponential', 'Gamma'])
axes[1, 1].set_title('Violin Plots (KDE-based)')
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('Kernel Density Estimation', fontsize=16)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "hist_kde.png", dpi=150)
plt.close()

print("KDE plots saved")
print()

# =============================================================================
# 5. COMPARISON PLOTS
# =============================================================================

print("=" * 60)
print("5. COMPARISON PLOTS")
print("=" * 60)

# Multiple distributions comparison
groups = {
    'Group A': np.random.normal(0, 1, 500),
    'Group B': np.random.normal(1, 1.5, 500),
    'Group C': np.random.exponential(2, 500) - 2,
    'Group D': np.random.gamma(2, 1, 500) - 2
}

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Overlaid histograms
colors = ['skyblue', 'lightcoral', 'lightgreen', 'gold']
for (name, data), color in zip(groups.items(), colors):
    axes[0, 0].hist(data, bins=30, density=True, alpha=0.4, 
                    color=color, label=name, edgecolor='black', linewidth=0.5)
axes[0, 0].legend()
axes[0, 0].set_title('Overlaid Histograms')
axes[0, 0].grid(True, alpha=0.3)

# Side-by-side histograms
bins = np.linspace(-4, 6, 25)
bin_centers = (bins[:-1] + bins[1:]) / 2
bar_width = (bins[1] - bins[0]) / len(groups)

for i, (name, data) in enumerate(groups.items()):
    counts, _ = np.histogram(data, bins=bins, density=True)
    offset = (i - len(groups)/2 + 0.5) * bar_width
    axes[0, 1].bar(bin_centers + offset, counts, width=bar_width * 0.9,
                   alpha=0.7, color=colors[i], label=name, edgecolor='black')
axes[0, 1].legend()
axes[0, 1].set_title('Side-by-Side Histograms')
axes[0, 1].grid(True, alpha=0.3)

# Stacked histograms
for i, (name, data) in enumerate(groups.items()):
    axes[1, 0].hist(data, bins=bins, density=True, alpha=0.5,
                    color=colors[i], label=name, stacked=True, 
                    edgecolor='black', linewidth=0.5)
axes[1, 0].legend()
axes[1, 0].set_title('Stacked Histograms')
axes[1, 0].grid(True, alpha=0.3)

# Ridge plot style (using histograms)
for i, (name, data) in enumerate(groups.items()):
    y_pos = len(groups) - i
    axes[1, 1].hist(data, bins=30, density=True, alpha=0.5,
                    color=colors[i], label=name, 
                    orientation='horizontal', 
                    cumulative=False,
                    bottom=y_pos * 0.1,
                    histtype='stepfilled')
axes[1, 1].set_title('Ridge-style Overlay')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('Distribution Comparison Techniques', fontsize=16)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "hist_comparison.png", dpi=150)
plt.close()

print("Comparison plots saved")
print()

# =============================================================================
# SUMMARY
# =============================================================================

print("=" * 60)
print("HISTOGRAMS COMPLETE")
print("=" * 60)
print("""
Key Concepts:
1. Basic: hist() with bins, density, cumulative
2. Bin selection: auto, sqrt(n), Freedman-Diaconis, custom
3. 2D: hist2d, hexbin, marginal distributions
3, joint plots
4. KDE: gaussian_kde for smooth density estimation
5. Comparison: overlaid, side-by-side, stacked, ridge

Next: Box plots, violin plots, statistical visualizations
""")