"""
Matplotlib Introduction: Basic Plotting
========================================

This module covers the fundamentals of matplotlib plotting.
"""


import matplotlib.pyplot as plt
import numpy as np
import pathlib
OUTPUT_DIR = pathlib.Path(__file__).parent.parent.parent / "outputs" / "matplotlib"

# =============================================================================
# 1. BASIC PLOT
# =============================================================================

print("=" * 60)
print("1. BASIC LINE PLOT")
print("=" * 60)

x = np.linspace(0, 10, 100)
y = np.sin(x)

# Simple plot
plt.figure(figsize=(8, 4))
plt.plot(x, y)
plt.title('Sine Wave')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_basic_plot.png", dpi=150)
plt.close()

print("Basic plot saved to output/01_basic_plot.png")
print()

# =============================================================================
# 2. MULTIPLE LINES
# =============================================================================

print("=" * 60)
print("2. MULTIPLE LINES")
print("=" * 60)

plt.figure(figsize=(8, 4))
plt.plot(x, np.sin(x), label='sin(x)', color='blue')
plt.plot(x, np.cos(x), label='cos(x)', color='red', linestyle='--')
plt.plot(x, np.sin(x) * np.cos(x), label='sin(x)*cos(x)', color='green', linewidth=2)
plt.title('Multiple Trig Functions')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_multiple_lines.png", dpi=150)
plt.close()

print("Multiple lines plot saved")
print()

# =============================================================================
# 3. SCATTER PLOT
# =============================================================================

print("=" * 60)
print("3. SCATTER PLOT")
print("=" * 60)

np.random.seed(42)
n = 200
x_scatter = np.random.randn(n)
y_scatter = 2 * x_scatter + np.random.randn(n) * 0.5
colors = np.random.rand(n)
sizes = 100 * np.random.rand(n) + 20

plt.figure(figsize=(8, 6))
sc = plt.scatter(x_scatter, y_scatter, c=colors, s=sizes, alpha=0.6, cmap='viridis')
plt.colorbar(sc, label='Color Value')
plt.title('Scatter Plot with Color and Size')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_scatter.png", dpi=150)
plt.close()

print("Scatter plot saved")
print()

# =============================================================================
# 4. BAR CHART
# =============================================================================

print("=" * 60)
print("4. BAR CHART")
print("=" * 60)

categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]
colors_bar = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

plt.figure(figsize=(8, 5))
bars = plt.bar(categories, values, color=colors_bar, edgecolor='black', linewidth=1.2)
plt.bar_label(bars, fmt='%d', fontsize=12)
plt.title('Bar Chart with Labels')
plt.xlabel('Category')
plt.ylabel('Value')
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_bar.png", dpi=150)
plt.close()

print("Bar chart saved")
print()

# =============================================================================
# 5. HISTOGRAM
# =============================================================================

print("=" * 60)
print("5. HISTOGRAM")
print("=" * 60)

data = np.random.randn(10000)

plt.figure(figsize=(8, 5))
n, bins, patches = plt.hist(data, bins=50, density=True, alpha=0.7, 
                             color='steelblue', edgecolor='black')
# Overlay normal distribution
x_norm = np.linspace(-4, 4, 100)
plt.plot(x_norm, 1/np.sqrt(2*np.pi) * np.exp(-x_norm**2/2), 
         'r-', linewidth=2, label='Normal PDF')
plt.title('Histogram with Normal Overlay')
plt.xlabel('Value')
plt.ylabel('Density')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "05_histogram.png", dpi=150)
plt.close()

print("Histogram saved")
print()

# =============================================================================
# 6. SUBPLOTS
# =============================================================================

print("=" * 60)
print("6. SUBPLOTS")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Top left
axes[0, 0].plot(x, np.sin(x), 'b-')
axes[0, 0].set_title('sin(x)')
axes[0, 0].grid(True, alpha=0.3)

# Top right
axes[0, 1].plot(x, np.cos(x), 'r-')
axes[0, 1].set_title('cos(x)')
axes[0, 1].grid(True, alpha=0.3)

# Bottom left
axes[1, 0].scatter(x_scatter[:50], y_scatter[:50], alpha=0.6)
axes[1, 0].set_title('Scatter Sample')
axes[1, 0].grid(True, alpha=0.3)

# Bottom right
axes[1, 1].hist(data, bins=30, alpha=0.7, color='green')
axes[1, 1].set_title('Histogram')
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('2x2 Subplot Grid', fontsize=16)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "06_subplots.png", dpi=150)
plt.close()

print("Subplots saved")
print()

# =============================================================================
# 7. CUSTOMIZATION
# =============================================================================

print("=" * 60)
print("7. PLOT CUSTOMIZATION")
print("=" * 60)

plt.figure(figsize=(10, 6))

# Plot
plt.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
plt.plot(x, np.cos(x), 'r--', linewidth=2, label='cos(x)')

# Customize
plt.title('Customized Plot', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('X Axis', fontsize=12)
plt.ylabel('Y Axis', fontsize=12)
plt.xlim(0, 10)
plt.ylim(-1.5, 1.5)
plt.xticks(np.arange(0, 11, 1))
plt.yticks(np.arange(-1.5, 1.6, 0.5))

# Legend
plt.legend(loc='upper right', framealpha=0.9, fontsize=11)

# Grid
plt.grid(True, which='major', linestyle='-', alpha=0.5)
plt.grid(True, which='minor', linestyle=':', alpha=0.3)
plt.minorticks_on()

# Spines
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)

# Annotate
plt.annotate('Peak', xy=(np.pi/2, 1), xytext=(2, 1.3),
             arrowprops=dict(arrowstyle='->', color='red', lw=2),
             fontsize=12, color='red')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "07_customization.png", dpi=150)
plt.close()

print("Customized plot saved")
print()

# =============================================================================
# 8. SAVE FIGURES
# =============================================================================

print("=" * 60)
print("8. SAVING FIGURES")
print("=" * 60)

plt.figure(figsize=(6, 4))
plt.plot(x, np.sin(x))
plt.title('Save Demo')

# Save in different formats
plt.savefig(OUTPUT_DIR / "plot.png", dpi=300, bbox_inches='tight')
plt.savefig(OUTPUT_DIR / "plot.pdf", bbox_inches='tight')
plt.savefig(OUTPUT_DIR / "plot.svg", bbox_inches='tight')
plt.savefig(OUTPUT_DIR / "plot_transparent.png", dpi=150, transparent=True, bbox_inches='tight')
plt.close()

print("Saved: PNG (300 DPI), PDF, SVG, Transparent PNG")
print()

# =============================================================================
# 9. STYLE SHEETS
# =============================================================================

print("=" * 60)
print("9. STYLE SHEETS")
print("=" * 60)

# Available styles
print("Available styles:")
for style in sorted(plt.style.available):
    print(f"  {style}")

# Use a style
with plt.style.context('seaborn-v0_8-whitegrid'):
    plt.figure(figsize=(8, 4))
    plt.plot(x, np.sin(x))
    plt.title('With seaborn-v0_8-whitegrid style')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "09_style.png", dpi=150)
    plt.close()

print("\nStyle demo saved")
print()

# =============================================================================
# 10. OBJECT-ORIENTED INTERFACE
# =============================================================================

print("=" * 60)
print("10. OBJECT-ORIENTED INTERFACE")
print("=" * 60)

# Create figure and axes explicitly
fig, ax = plt.subplots(figsize=(8, 5))

# Plot on axes
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

# Configure axes
ax.set_title('Object-Oriented Plot')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend()
ax.grid(True, alpha=0.3)

# Save
fig.savefig(OUTPUT_DIR / '10_oop.png', dpi=150)
plt.close(fig)

print("OOP interface demo saved")
print()

# =============================================================================
# SUMMARY
# =============================================================================

print("=" * 60)
print("MATPLOTLIB BASICS COMPLETE")
print("=" * 60)
print("""
Key Concepts Covered:
1. Basic line plots with plt.plot()
2. Multiple lines with labels and legends
3. Scatter plots with color/size mapping
4. Bar charts with labels
5. Histograms with density overlay
6. Subplot grids (plt.subplots)
7. Customization (titles, labels, limits, grid, spines)
8. Saving in multiple formats (PNG, PDF, SVG)
9. Style sheets (seaborn, ggplot, etc.)
10. Object-oriented interface (fig, ax)

Next: Advanced plotting (3D, animations, etc.)
""")