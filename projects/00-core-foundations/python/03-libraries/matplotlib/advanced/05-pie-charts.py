"""
Matplotlib Pie Charts and Polar Plots
======================================
"""

import pathlib
import matplotlib.pyplot as plt
OUTPUT_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "outputs" / "matplotlib"
import pathlib
import numpy as np

# =============================================================================
# 1. BASIC PIE CHART
# =============================================================================

print("=" * 60)
print("1. BASIC PIE CHART")
print("=" * 60)

labels = ['Product A', 'Product B', 'Product C', 'Product D', 'Others']
sizes = [35, 25, 20, 15, 5]
colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Basic pie
axes[0, 0].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
axes[0, 0].set_title('Basic Pie Chart')

# With explode
explode = (0.1, 0, 0, 0, 0)  # explode 1st slice
axes[0, 1].pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', 
               colors=colors, shadow=True)
axes[0, 1].set_title('Exploded Slice')

# Donut chart
axes[1, 0].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors,
               wedgeprops=dict(width=0.5, edgecolor='w'))
axes[1, 0].set_title('Donut Chart (wedgeprops)')

# Nested pie (two levels)
inner_labels = ['A', 'B', 'C', 'D', 'E']
inner_sizes = [15, 20, 10, 5, 5]
outer_labels = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5']
outer_sizes = [35, 25, 20, 15, 5]

axes[1, 1].pie(outer_sizes, labels=outer_labels, autopct='%1.1f%%',
               radius=1, colors=plt.cm.Set2(np.linspace(0, 1, 5)),
               wedgeprops=dict(width=0.3, edgecolor='w'))
axes[1, 1].pie(inner_sizes, labels=inner_labels, autopct='%1.1f%%',
               radius=0.7, colors=plt.cm.Set3(np.linspace(0, 1, 5)),
               wedgeprops=dict(width=0.3, edgecolor='w'))
axes[1, 1].set_title('Nested Pie Chart')

plt.suptitle('Pie Chart Variations', fontsize=16)
plt.tight_layout()
plt.savefig("../../../outputs/matplotlib/pie_basic.png", dpi=150)
plt.close()

print("Basic pie charts saved")
print()

# =============================================================================
# 2. PIE CHART CUSTOMIZATION
# =============================================================================

print("=" * 60)
print("2. PIE CHART CUSTOMIZATION")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Custom text properties
axes[0, 0].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors,
               textprops={'fontsize': 12, 'fontweight': 'bold', 'color': 'white'},
               pctdistance=0.85)
axes[0, 0].set_title('Custom Text Properties')

# Custom autopct function
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return f'{pct:.1f}%\n({val})'
    return my_autopct

axes[0, 1].pie(sizes, labels=labels, autopct=make_autopct(sizes), colors=colors)
axes[0, 1].set_title('Custom autopct with Values')

# Start angle and rotation
axes[1, 0].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors,
               startangle=90, counterclock=False)
axes[1, 0].set_title('startangle=90, counterclock=False')

# Legend instead of labels
wedges, texts, autotexts = axes[1, 1].pie(sizes, autopct='%1.1f%%', colors=colors,
                                           labeldistance=1.15)
axes[1, 1].legend(wedges, labels, title="Products", loc="center left", 
                  bbox_to_anchor=(1, 0, 0.5, 1))
axes[1, 1].set_title('Legend Instead of Labels')

plt.suptitle('Pie Chart Customizations', fontsize=16)
plt.tight_layout()
plt.savefig("../../../outputs/matplotlib/pie_custom.png", dpi=150)
plt.close()

print("Customized pie charts saved")
print()

# =============================================================================
# 3. POLAR PLOTS
# =============================================================================

print("=" * 60)
print("3. POLAR PLOTS")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(12, 10), subplot_kw={'projection': 'polar'})

# Basic polar line
theta = np.linspace(0, 2*np.pi, 100)
r = 1 + 0.5 * np.sin(4*theta)
axes[0, 0].plot(theta, r, 'b-', linewidth=2)
axes[0, 0].set_title('Polar Line: r = 1 + 0.5*sin(4θ)')
axes[0, 0].grid(True)

# Polar scatter
np.random.seed(42)
theta_scatter = np.random.uniform(0, 2*np.pi, 100)
r_scatter = np.random.uniform(0, 2, 100)
colors_scatter = np.random.rand(100)
sc = axes[0, 1].scatter(theta_scatter, r_scatter, c=colors_scatter, cmap='hsv', alpha=0.6)
axes[0, 1].set_title('Polar Scatter')
plt.colorbar(sc, ax=axes[0, 1])

# Polar bar chart
categories = ['A', 'B', 'C', 'D', 'E', 'F']
values = [3, 7, 2, 5, 8, 4]
theta_bars = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
bars = axes[1, 0].bar(theta_bars, values, width=0.8, bottom=0.5, 
                      color=plt.cm.viridis(np.linspace(0, 1, len(categories))), 
                      edgecolor='white', alpha=0.8)
axes[1, 0].set_xticks(theta_bars)
axes[1, 0].set_xticklabels(categories)
axes[1, 0].set_title('Polar Bar Chart')

# Rose diagram (wind rose style)
wind_dirs = np.array([0, 45, 90, 135, 180, 225, 270, 315])
wind_speeds = np.array([5, 3, 8, 2, 6, 4, 7, 3])
wind_dirs_rad = np.deg2rad(wind_dirs)
width = np.deg2rad(30)

axes[1, 1].bar(wind_dirs_rad, wind_speeds, width=width, bottom=0.5,
               color=plt.cm.coolwarm(np.linspace(0, 1, len(wind_dirs))), 
               edgecolor='white', alpha=0.8)
axes[1, 1].set_theta_zero_location('N')
axes[1, 1].set_theta_direction(-1)
axes[1, 1].set_xticks(np.deg2rad([0, 45, 90, 135, 180, 225, 270, 315]))
axes[1, 1].set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
axes[1, 1].set_title('Wind Rose Diagram')
axes[1, 1].grid(True)

plt.suptitle('Polar Plots', fontsize=16)
plt.tight_layout()
plt.savefig("../../../outputs/matplotlib/polar_plots.png", dpi=150)
plt.close()

print("Polar plots saved")
print()

# =============================================================================
# 4. RADAR / SPIDER CHARTS
# =============================================================================

print("=" * 60)
print("4. RADAR / SPIDER CHARTS")
print("=" * 60)

# Skills data
categories = ['Python', 'ML/DL', 'Statistics', 'SQL', 'Cloud', 'MLOps', 'Communication']
N = len(categories)

person_a = [9, 7, 8, 6, 5, 4, 7]
person_b = [6, 9, 7, 8, 7, 6, 5]
person_c = [7, 6, 9, 7, 6, 5, 8]

# Compute angles
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # Close the loop

# Close the data
for data in [person_a, person_b, person_c]:
    data += data[:1]

fig, axes = plt.subplots(1, 2, figsize=(14, 6), subplot_kw={'projection': 'polar'})

# Multiple series
for data, label, color in zip([person_a, person_b, person_c], 
                               ['Person A', 'Person B', 'Person C'],
                               ['blue', 'red', 'green']):
    axes[0].plot(angles, data, 'o-', linewidth=2, label=label, color=color)
    axes[0].fill(angles, data, alpha=0.15, color=color)

axes[0].set_xticks(angles[:-1])
axes[0].set_xticklabels(categories)
axes[0].set_ylim(0, 10)
axes[0].set_title('Skill Comparison Radar Chart', pad=20)
axes[0].legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
axes[0].grid(True)

# Single series with annotations
angles2 = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles2 += angles2[:1]

axes[1].plot(angles2, person_a, 'o-', linewidth=2, color='navy')
axes[1].fill(angles2, person_a, alpha=0.25, color='navy')
axes[1].set_xticks(angles2[:-1])
axes[1].set_xticklabels(categories)
axes[1].set_ylim(0, 10)

# Add value labels
for angle, value, cat in zip(angles2[:-1], person_a[:-1], categories):
    axes[1].text(angle, value + 0.5, str(value), ha='center', va='center',
                 fontweight='bold', color='navy')

axes[1].set_title('Person A Skills with Values', pad=20)
axes[1].grid(True)

plt.suptitle('Radar / Spider Charts', fontsize=16)
plt.tight_layout()
plt.savefig("../../../outputs/matplotlib/radar_charts.png", dpi=150)
plt.close()

print("Radar charts saved")
print()

# =============================================================================
# SUMMARY
# =============================================================================

print("=" * 60)
print("PIE & POLAR COMPLETE")
print("=" * 60)
print("""
Key Concepts:
1. Pie: pie() with autopct, explode, shadow, wedgeprops
2. Donut: wedgeprops=dict(width=0.5)
3. Nested: Multiple pie() calls with different radii
4. Custom: textprops, custom autopct function, startangle
5. Polar: projection='polar' for line, scatter, bar
6. Wind rose: bar with theta zero at North
7. Radar: polar line with fill, closed polygon

Next: 3D plots, animations, embeddings
""")