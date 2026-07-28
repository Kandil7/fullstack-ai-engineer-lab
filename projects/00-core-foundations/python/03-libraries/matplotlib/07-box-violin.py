"""
Matplotlib Box and Violin Plots
================================
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# =============================================================================
# 1. BASIC BOX PLOTS
# =============================================================================

print("=" * 60)
print("1. BASIC BOX PLOTS")
print("=" * 60)

np.random.seed(42)

# Generate data for multiple groups
groups = {
    'Group A': np.random.normal(0, 1, 100),
    'Group B': np.random.normal(2, 1.5, 100),
    'Group C': np.random.exponential(2, 100) - 2,
    'Group D': np.random.gamma(2, 1, 100) - 2,
    'Group E': np.random.normal(-1, 0.5, 100)
}

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Basic boxplot
data_list = list(groups.values())
labels = list(groups.keys())
bp = axes[0, 0].boxplot(data_list, labels=labels, patch_artist=True)
colors = ['skyblue', 'lightcoral', 'lightgreen', 'gold', 'lightblue']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
axes[0, 0].set_title('Basic Box Plot')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Horizontal boxplot
bp = axes[0, 1].boxplot(data_list, labels=labels, patch_artist=True, vert=False)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
axes[0, 1].set_title('Horizontal Box Plot')
axes[0, 1].grid(True, alpha=0.3, axis='x')

# Boxplot with custom outliers
bp = axes[1, 0].boxplot(data_list, labels=labels, patch_artist=True, 
                        showfliers=True, flierprops=dict(marker='o', 
                        color='red', alpha=0.5, markersize=6))
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
axes[1, 0].set_title('Custom Outlier Style')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Boxplot with notches (confidence interval for median)
bp = axes[1, 1].boxplot(data_list, labels=labels, patch_artist=True, 
                        notch=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
axes[1, 1].set_title('Notched Box Plot (Median CI)')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.suptitle('Box Plot Variations', fontsize=16)
plt.tight_layout()
plt.savefig('output/box_basic.png', dpi=150)
plt.close()

print("Basic box plots saved")
print()

# =============================================================================
# 2. BOX PLOT CUSTOMIZATION
# =============================================================================

print("=" * 60)
print("2. BOX PLOT CUSTOMIZATION")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Custom whiskers (percentiles)
bp = axes[0, 0].boxplot(data_list, labels=labels, patch_artist=True,
                        whis=(5, 95))  # 5th and 95th percentiles
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
axes[0, 0].set_title('Whiskers at 5th/95th Percentile')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Show means
bp = axes[0, 1].boxplot(data_list, labels=labels, patch_artist=True,
                        showmeans=True, meanline=True,
                        meanprops=dict(color='red', linewidth=2))
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
axes[0, 1].set_title('Show Means (Red Line)')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Custom colors for all elements
bp = axes[1, 0].boxplot(data_list, labels=labels, patch_artist=True,
                        boxprops=dict(facecolor='lightblue', color='darkblue', linewidth=2),
                        whiskerprops=dict(color='darkblue', linewidth=1.5),
                        capprops=dict(color='darkblue', linewidth=1.5),
                        medianprops=dict(color='red', linewidth=3),
                        flierprops=dict(marker='D', color='red', alpha=0.7))
axes[1, 0].set_title('Fully Customized Style')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Boxplot with individual points (strip plot overlay)
bp = axes[1, 1].boxplot(data_list, labels=labels, patch_artist=True, 
                        showfliers=False)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.5)
# Overlay individual points
for i, (label, data) in enumerate(groups.items()):
    x = np.random.normal(i + 1, 0.04, len(data))
    axes[1, 1].scatter(x, data, alpha=0.3, s=10, c=colors[i])
axes[1, 1].set_title('Box Plot + Strip Plot')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.suptitle('Box Plot Customizations', fontsize=16)
plt.tight_layout()
plt.savefig('output/box_custom.png', dpi=150)
plt.close()

print("Customized box plots saved")
print()

# =============================================================================
# 3. VIOLIN PLOTS
# =============================================================================

print("=" * 60)
print("3. VIOLIN PLOTS")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Basic violin plot
parts = axes[0, 0].violinplot(data_list, showmeans=True, showmedians=True, 
                               showextrema=True)
for pc, color in zip(parts['bodies'], colors):
    pc.set_facecolor(color)
    pc.set_alpha(0.7)
axes[0, 0].set_xticks(range(1, len(labels) + 1))
axes[0, 0].set_xticklabels(labels)
axes[0, 0].set_title('Basic Violin Plot')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Horizontal violin
parts = axes[0, 1].violinplot(data_list, showmeans=True, showmedians=True, 
                               showextrema=True, vert=False)
for pc, color in zip(parts['bodies'], colors):
    pc.set_facecolor(color)
    pc.set_alpha(0.7)
axes[0, 1].set_yticks(range(1, len(labels) + 1))
axes[0, 1].set_yticklabels(labels)
axes[0, 1].set_title('Horizontal Violin Plot')
axes[0, 1].grid(True, alpha=0.3, axis='x')

# Violin with custom bandwidth
parts = axes[1, 0].violinplot(data_list, showmeans=True, showmedians=True, 
                               showextrema=True, bw_method=0.2)
for pc, color in zip(parts['bodies'], colors):
    pc.set_facecolor(color)
    pc.set_alpha(0.7)
axes[1, 0].set_xticks(range(1, len(labels) + 1))
axes[1, 0].set_xticklabels(labels)
axes[1, 0].set_title('Narrow Bandwidth (bw=0.2)')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Violin + box + strip (combined)
parts = axes[1, 1].violinplot(data_list, showmeans=False, showmedians=False, 
                               showextrema=False)
for pc, color in zip(parts['bodies'], colors):
    pc.set_facecolor(color)
    pc.set_alpha(0.3)

# Add box plot inside
bp = axes[1, 1].boxplot(data_list, labels=labels, patch_artist=True, 
                        widths=0.2, showfliers=False)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor('white')
    patch.set_edgecolor(color)
    patch.set_linewidth(2)

# Add strip plot
for i, (label, data) in enumerate(groups.items()):
    x = np.random.normal(i + 1, 0.05, len(data))
    axes[1, 1].scatter(x, data, alpha=0.3, s=8, c=colors[i])

axes[1, 1].set_title('Violin + Box + Strip')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.suptitle('Violin Plot Variations', fontsize=16)
plt.tight_layout()
plt.savefig('output/violin_basic.png', dpi=150)
plt.close()

print("Violin plots saved")
print()

# =============================================================================
# 4. STATISTICAL ANNOTATIONS
# =============================================================================

print("=" * 60)
print("4. STATISTICAL ANNOTATIONS")
print("=" * 60)

from scipy import stats

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Boxplot with statistical annotations
bp = axes[0, 0].boxplot(data_list, labels=labels, patch_artist=True, 
                        showfliers=False)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Add sample size and stats
for i, (label, data) in enumerate(groups.items()):
    n = len(data)
    median = np.median(data)
    mean = np.mean(data)
    axes[0, 0].text(i + 1, median, f'n={n}\nμ={mean:.2f}\nM={median:.2f}', 
                    ha='center', va='bottom', fontsize=8,
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
axes[0, 0].set_title('Box Plot with Statistics')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Significance brackets
def add_significance(ax, x1, x2, y, text, height=0.05):
    """Add significance bracket between two boxes."""
    y_max = ax.get_ylim()[1]
    bracket_y = y_max * (1 + height)
    ax.plot([x1, x1, x2, x2], [bracket_y - 0.02, bracket_y, bracket_y, bracket_y - 0.02], 
            'k-', linewidth=1)
    ax.text((x1 + x2) / 2, bracket_y, text, ha='center', va='bottom', fontsize=10)

bp = axes[0, 1].boxplot(data_list, labels=labels, patch_artist=True, showfliers=False)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Add significance brackets (example comparisons)
add_significance(axes[0, 1], 1, 2, 0, '**')
add_significance(axes[0, 1], 2, 3, 0, '*')
add_significance(axes[0, 1], 4, 5, 0, 'ns')

axes[0, 1].set_ylim(bottom=axes[0, 1].get_ylim()[0], top=axes[0, 1].get_ylim()[1] * 1.15)
axes[0, 1].set_title('Significance Brackets')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Violin with quartile lines
parts = axes[1, 0].violinplot(data_list, showmedians=True, showextrema=True)
for pc, color in zip(parts['bodies'], colors):
    pc.set_facecolor(color)
    pc.set_alpha(0.5)

# Add quartile lines manually
for i, data in enumerate(data_list):
    q1, q3 = np.percentile(data, [25, 75])
    axes[1, 0].hlines([q1, q3], i + 0.8, i + 1.2, colors='black', 
                      linewidth=1.5, linestyles='dashed')
    axes[1, 0].hlines(np.median(data), i + 0.8, i + 1.2, colors='red', 
                      linewidth=2)
axes[1, 0].set_xticks(range(1, len(labels) + 1))
axes[1, 0].set_xticklabels(labels)
axes[1, 0].set_title('Violin with Quartile Lines')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Raincloud plot (violin + box + scatter)
parts = axes[1, 1].violinplot(data_list, showmeans=False, showmedians=False, 
                               showextrema=False)
for pc, color in zip(parts['bodies'], colors):
    pc.set_facecolor(color)
    pc.set_alpha(0.3)

# Box
bp = axes[1, 1].boxplot(data_list, patch_artist=True, widths=0.15, showfliers=False)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor('white')
    patch.set_edgecolor(color)
    patch.set_linewidth(1.5)

# Scatter (rain)
for i, data in enumerate(data_list):
    x = np.random.normal(i + 1, 0.03, len(data))
    axes[1, 1].scatter(x, data, alpha=0.2, s=5, c=colors[i])

axes[1, 1].set_xticks(range(1, len(labels) + 1))
axes[1, 1].set_xticklabels(labels)
axes[1, 1].set_title('Raincloud Plot')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.suptitle('Statistical Annotations', fontsize=16)
plt.tight_layout()
plt.savefig('output/box_violin_stats.png', dpi=150)
plt.close()

print("Statistical annotations saved")
print()

# =============================================================================
# 5. GROUPED BOX/VIOLIN PLOTS
# =============================================================================

print("=" * 60)
print("5. GROUPED PLOTS")
print("=" * 60)

# Two-factor data
np.random.seed(42)
n = 50
factors = {
    ('Treatment A', 'Male'): np.random.normal(5, 1, n),
    ('Treatment A', 'Female'): np.random.normal(4.5, 1, n),
    ('Treatment B', 'Male'): np.random.normal(7, 1.2, n),
    ('Treatment B', 'Female'): np.random.normal(6.5, 1.2, n),
    ('Control', 'Male'): np.random.normal(3, 0.8, n),
    ('Control', 'Female'): np.random.normal(2.8, 0.8, n),
}

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Grouped boxplot
treatments = ['Control', 'Treatment A', 'Treatment B']
genders = ['Male', 'Female']
positions = []
data_by_group = []
labels = []

for t in treatments:
    for g in genders:
        positions.append(len(data_by_group) + 1)
        data_by_group.append(factors[(t, g)])
        labels.append(f'{t}\n{g}')

colors_grouped = ['lightblue', 'lightpink'] * 3

bp = axes[0, 0].boxplot(data_by_group, positions=positions, labels=labels, 
                        patch_artist=True, widths=0.6, showfliers=False)
for patch, color in zip(bp['boxes'], colors_grouped):
    patch.set_facecolor(color)
axes[0, 0].set_title('Grouped Boxplot')
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Grouped violin
parts = axes[0, 1].violinplot(data_by_group, positions=positions, 
                               showmeans=True, showmedians=True)
for pc, color in zip(parts['bodies'], colors_grouped):
    pc.set_facecolor(color)
    pc.set_alpha(0.7)
axes[0, 1].set_xticks(positions)
axes[0, 1].set_xticklabels(labels, rotation=45)
axes[0, 1].set_title('Grouped Violin Plot')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Split violin (for gender comparison within treatment)
# Create split data
for i, t in enumerate(treatments):
    male_data = factors[(t, 'Male')]
    female_data = factors[(t, 'Female')]
    # Offset positions
    base_pos = i + 1
    # Male on left, female on right
    parts_m = axes[1, 0].violinplot([male_data], positions=[base_pos - 0.15], 
                                     vert=True, widths=0.3, showextrema=False)
    parts_f = axes[1, 0].violinplot([female_data], positions=[base_pos + 0.15], 
                                     vert=True, widths=0.3, showextrema=False)
    for pc in parts_m['bodies']:
        pc.set_facecolor('lightblue')
        pc.set_alpha(0.7)
    for pc in parts_f['bodies']:
        pc.set_facecolor('lightpink')
        pc.set_alpha(0.7)

axes[1, 0].set_xticks([1, 2, 3])
axes[1, 0].set_xticklabels(treatments)
axes[1, 0].legend([plt.Rectangle((0,0),1,1,fc='lightblue'), 
                   plt.Rectangle((0,0),1,1,fc='lightpink')], 
                  ['Male', 'Female'])
axes[1, 0].set_title('Split Violin (Male vs Female)')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Combined: box + violin + points
for i, (t, g) in enumerate([(t, g) for t in treatments for g in genders]):
    data = factors[(t, g)]
    pos = i + 1
    # Violin (half)
    parts = axes[1, 1].violinplot([data], positions=[pos], widths=0.5, 
                                   showmeans=False, showmedians=False, showextrema=False)
    for pc in parts['bodies']:
        pc.set_facecolor(colors_grouped[i])
        pc.set_alpha(0.3)
    # Box
    bp = axes[1, 1].boxplot([data], positions=[pos], widths=0.15, 
                             patch_artist=True, showfliers=False)
    for patch in bp['boxes']:
        patch.set_facecolor('white')
        patch.set_edgecolor(colors_grouped[i])
        patch.set_linewidth(1.5)
    # Points
    x = np.random.normal(pos, 0.03, len(data))
    axes[1, 1].scatter(x, data, alpha=0.2, s=8, c=colors_grouped[i])

axes[1, 1].set_xticks(range(1, len(labels) + 1))
axes[1, 1].set_xticklabels(labels, rotation=45)
axes[1, 1].set_title('Combined: Violin + Box + Points')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.suptitle('Grouped Box/Violin Plots', fontsize=16)
plt.tight_layout()
plt.savefig('output/box_violin_grouped.png', dpi=150)
plt.close()

print("Grouped plots saved")
print()

# =============================================================================
# SUMMARY
# =============================================================================

print("=" * 60)
print("BOX & VIOLIN PLOTS COMPLETE")
print("=" * 60)
print("""
Key Concepts:
1. Box plots: boxplot() with notch, whis, showmeans, custom styling
2. Violin plots: violinplot() with bw_method, showmedians
3. Customization: colors, whiskers, outliers, notches
4. Annotations: statistics, significance brackets, quartile lines
5. Combined: violin + box + strip/raincloud plots
6. Grouped: two-factor designs with split violins

Next: Pie charts, 3D plots, contour plots
""")