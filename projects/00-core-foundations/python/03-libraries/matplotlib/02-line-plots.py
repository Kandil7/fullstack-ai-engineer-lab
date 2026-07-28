"""
Matplotlib Line Plots: Styles, markers, multiple lines
========================================================
"""

import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# 1. LINE STYLES
# =============================================================================

print("=" * 60)
print("1. LINE STYLES")
print("=" * 60)

x = np.linspace(0, 10, 50)

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
styles = [
    ('Solid', '-'),
    ('Dashed', '--'),
    ('Dash-dot', '-.'),
    ('Dotted', ':'),
    ('None', ''),
    ('Steps', 'steps')
]

for (name, style), ax in zip(styles, axes.flat):
    ax.plot(x, np.sin(x), linestyle=style, linewidth=2, color='blue')
    ax.set_title(f'{name} ({style})')
    ax.grid(True, alpha=0.3)

plt.suptitle('Line Styles', fontsize=16)
plt.tight_layout()
plt.savefig('output/line_styles.png', dpi=150)
plt.close()

print("Line styles plot saved")
print()

# =============================================================================
# 2. MARKERS
# =============================================================================

print("=" * 60)
print("2. MARKERS")
print("=" * 60)

fig, axes = plt.subplots(3, 4, figsize=(16, 10))
markers = ['o', 's', '^', 'v', 'D', 'p', '*', 'h', 'H', '+', 'x', '|']

for marker, ax in zip(markers, axes.flat):
    ax.plot(x, np.sin(x), marker=marker, markersize=8, 
            linestyle='-', color='green', markerfacecolor='red')
    ax.set_title(f"marker='{marker}'")
    ax.grid(True, alpha=0.3)

plt.suptitle('Marker Styles', fontsize=16)
plt.tight_layout()
plt.savefig('output/markers.png', dpi=150)
plt.close()

print("Markers plot saved")
print()

# =============================================================================
# 3. COLOR SPECIFICATION
# =============================================================================

print("=" * 60)
print("3. COLOR SPECIFICATION")
print("=" * 60)

fig, axes = plt.subplots(2, 3, figsize=(15, 8))

# Named colors
axes[0, 0].plot(x, np.sin(x), color='red')
axes[0, 0].set_title("Named: 'red'")

# Hex colors
axes[0, 1].plot(x, np.sin(x), color='#FF5733')
axes[0, 1].set_title("Hex: '#FF5733'")

# RGB tuple (0-1)
axes[0, 2].plot(x, np.sin(x), color=(0.2, 0.6, 0.8))
axes[0, 2].set_title("RGB tuple: (0.2, 0.6, 0.8)")

# RGBA tuple
axes[1, 0].plot(x, np.sin(x), color=(1, 0, 0, 0.5))
axes[1, 0].set_title("RGBA: (1, 0, 0, 0.5)")

# Grayscale string
axes[1, 1].plot(x, np.sin(x), color='0.5')
axes[1, 1].set_title("Grayscale: '0.5'")

# Color map
cmap = plt.cm.viridis
colors = cmap(np.linspace(0, 1, len(x)))
axes[1, 2].scatter(x, np.sin(x), c=colors, cmap='viridis')
axes[1, 2].set_title("Colormap: viridis")

plt.suptitle('Color Specification Methods', fontsize=16)
plt.tight_layout()
plt.savefig('output/colors.png', dpi=150)
plt.close()

print("Colors plot saved")
print()

# =============================================================================
# 4. LINE WIDTH & ALPHA
# =============================================================================

print("=" * 60)
print("4. LINE WIDTH & TRANSPARENCY")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Line widths
widths = [0.5, 1, 2, 3, 4, 5]
for w in widths:
    axes[0, 0].plot(x, np.sin(x) + w * 0.5, linewidth=w, label=f'lw={w}')
axes[0, 0].set_title('Line Widths')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Alpha (transparency)
alphas = [0.1, 0.3, 0.5, 0.7, 1.0]
for a in alphas:
    axes[0, 1].plot(x, np.sin(x) + a * 1.5, linewidth=3, alpha=a, label=f'α={a}')
axes[0, 1].set_title('Alpha Values')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Combined
for i in range(10):
    axes[1, 0].plot(x, np.sin(x) + i * 0.3, 
                    linewidth=0.5 + i * 0.3, 
                    alpha=0.1 + i * 0.09,
                    color=plt.cm.plasma(i/10))
axes[1, 0].set_title('Width + Alpha Gradient')
axes[1, 0].grid(True, alpha=0.3)

# Dashed with varying dash patterns
dash_patterns = [
    (5, 5),   # 5 on, 5 off
    (10, 5),  # 10 on, 5 off
    (5, 10),  # 5 on, 10 off
    (3, 5, 1, 5),  # complex pattern
]
for i, pattern in enumerate(dash_patterns):
    axes[1, 1].plot(x, np.sin(x) + i * 0.5, 
                    linestyle=(0, pattern), linewidth=2,
                    label=f'{pattern}')
axes[1, 1].set_title('Custom Dash Patterns')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('Line Width, Alpha, and Dash Patterns', fontsize=16)
plt.tight_layout()
plt.savefig('output/line_width_alpha.png', dpi=150)
plt.close()

print("Line width/alpha plot saved")
print()

# =============================================================================
# 5. MULTIPLE LINES WITH LEGEND
# =============================================================================

print("=" * 60)
print("5. MULTIPLE LINES WITH LEGEND")
print("=" * 60)

fig, ax = plt.subplots(figsize=(10, 6))

# Multiple trig functions
functions = [
    (np.sin, 'sin(x)', 'blue', '-'),
    (np.cos, 'cos(x)', 'red', '--'),
    (lambda x: np.tan(x), 'tan(x)', 'green', ':'),
    (lambda x: np.sin(x) * np.cos(x), 'sin(x)cos(x)', 'orange', '-.'),
]

for func, label, color, style in functions:
    y = func(x)
    # Mask extreme values for tan
    if 'tan' in label:
        y = np.ma.masked_where(np.abs(y) > 5, y)
    ax.plot(x, y, label=label, color=color, linestyle=style, linewidth=2)

ax.set_title('Multiple Trigonometric Functions', fontsize=14)
ax.set_xlabel('x (radians)')
ax.set_ylabel('y')
ax.set_ylim(-3, 3)
ax.legend(loc='upper right', framealpha=0.9, fontsize=11)
ax.grid(True, alpha=0.3)

# Custom legend
from matplotlib.lines import Line2D
custom_lines = [
    Line2D([0], [0], color='blue', lw=2, label='sin'),
    Line2D([0], [0], color='red', lw=2, linestyle='--', label='cos'),
]
ax.legend(handles=custom_lines, loc='lower right')

plt.tight_layout()
plt.savefig('output/multiple_lines.png', dpi=150)
plt.close()

print("Multiple lines plot saved")
print()

# =============================================================================
# 6. FILL BETWEEN
# =============================================================================

print("=" * 60)
print("6. FILL BETWEEN")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Basic fill
axes[0, 0].plot(x, np.sin(x), 'b-')
axes[0, 0].fill_between(x, np.sin(x), alpha=0.3, color='blue')
axes[0, 0].set_title('Basic fill_between')
axes[0, 0].grid(True, alpha=0.3)

# Fill between two curves
y1 = np.sin(x)
y2 = np.cos(x)
axes[0, 1].plot(x, y1, 'b-', label='sin')
axes[0, 1].plot(x, y2, 'r-', label='cos')
axes[0, 1].fill_between(x, y1, y2, where=(y1 > y2), alpha=0.3, color='blue', label='sin > cos')
axes[0, 1].fill_between(x, y1, y2, where=(y1 <= y2), alpha=0.3, color='red', label='cos > sin')
axes[0, 1].set_title('Fill Between Two Curves')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Confidence band
y_mean = np.sin(x)
y_std = 0.2 + 0.1 * np.sin(2 * x)
axes[1, 0].plot(x, y_mean, 'b-', linewidth=2)
axes[1, 0].fill_between(x, y_mean - y_std, y_mean + y_std, alpha=0.2, color='blue', label='±1σ')
axes[1, 0].set_title('Confidence Band')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Stacked fill
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * np.cos(x)
axes[1, 1].fill_between(x, 0, y1, alpha=0.5, color='red', label='sin')
axes[1, 1].fill_between(x, y1, y1 + y2, alpha=0.5, color='blue', label='cos')
axes[1, 1].fill_between(x, y1 + y2, y1 + y2 + y3, alpha=0.5, color='green', label='sin*cos')
axes[1, 1].set_title('Stacked Fill')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('Fill Between Examples', fontsize=16)
plt.tight_layout()
plt.savefig('output/fill_between.png', dpi=150)
plt.close()

print("Fill between plots saved")
print()

# =============================================================================
# 7. ERROR BARS
# =============================================================================

print("=" * 60)
print("7. ERROR BARS")
print("=" * 60)

# Sample data with errors
x_err = np.arange(1, 11)
y_err = 2 * x_err + np.random.randn(10)
y_err_std = 0.5 + 0.2 * x_err

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Basic error bars
axes[0, 0].errorbar(x_err, y_err, yerr=y_err_std, fmt='o-', capsize=5, 
                     label='Data ± Error', color='blue')
axes[0, 0].set_title('Basic Error Bars')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Asymmetric errors
y_err_low = 0.3 + 0.1 * x_err
y_err_high = 0.7 + 0.2 * x_err
axes[0, 1].errorbar(x_err, y_err, yerr=[y_err_low, y_err_high], fmt='s-', 
                     capsize=5, label='Asymmetric', color='red')
axes[0, 1].set_title('Asymmetric Error Bars')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# X and Y errors
x_err_vals = 0.2 * np.ones_like(x_err)
axes[1, 0].errorbar(x_err, y_err, xerr=x_err_vals, yerr=y_err_std, 
                     fmt='o', capsize=5, color='green')
axes[1, 0].set_title('X and Y Error Bars')
axes[1, 0].grid(True, alpha=0.3)

# Multiple series with errors
x_multi = np.arange(1, 6)
series = [
    (x_multi, [10, 12, 13, 15, 14], [0.5, 0.6, 0.4, 0.7, 0.5]),
    (x_multi, [8, 10, 11, 12, 11], [0.4, 0.5, 0.6, 0.4, 0.5]),
    (x_multi, [12, 14, 15, 16, 15], [0.6, 0.5, 0.7, 0.5, 0.6]),
]
colors = ['blue', 'red', 'green']
for (x_vals, y_vals, err_vals), color in zip(series, colors):
    axes[1, 1].errorbar(x_vals, y_vals, yerr=err_vals, fmt='o-', 
                         capsize=5, label=f'Series {color}', color=color)
axes[1, 1].set_title('Multiple Series with Errors')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('Error Bar Examples', fontsize=16)
plt.tight_layout()
plt.savefig('output/error_bars.png', dpi=150)
plt.close()

print("Error bars plot saved")
print()

# =============================================================================
# SUMMARY
# =============================================================================

print("=" * 60)
print("LINE PLOTS COMPLETE")
print("=" * 60)
print("""
Key Concepts:
1. Line styles: '-', '--', '-.', ':', 'steps'
2. Markers: 'o', 's', '^', 'D', '*', '+', 'x', etc.
3. Colors: named, hex, RGB, RGBA, grayscale, colormaps
4. Line width and alpha for emphasis
5. Multiple lines with legends
6. fill_between for areas, confidence bands, stacked areas
7. errorbar for measurement uncertainties

Next: Scatter plots, bar charts, histograms
""")