"""
Matplotlib Bar Charts: bar, barh, stacked, grouped
====================================================
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# =============================================================================
# 1. BASIC BAR CHARTS
# =============================================================================

print("=" * 60)
print("1. BASIC BAR CHARTS")
print("=" * 60)

categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Vertical bars
axes[0, 0].bar(categories, values, color='steelblue', edgecolor='black', linewidth=0.5)
axes[0, 0].set_title('Vertical Bar Chart')
axes[0, 0].set_ylabel('Value')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Horizontal bars
axes[0, 1].barh(categories, values, color='coral', edgecolor='black', linewidth=0.5)
axes[0, 1].set_title('Horizontal Bar Chart')
axes[0, 1].set_xlabel('Value')
axes[0, 1].grid(True, alpha=0.3, axis='x')

# Colored bars
colors = plt.cm.viridis(np.linspace(0, 1, len(categories)))
axes[1, 0].bar(categories, values, color=colors, edgecolor='black', linewidth=0.5)
axes[1, 0].set_title('Colored Bars (Viridis)')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# With value labels
bars = axes[1, 1].bar(categories, values, color='mediumseagreen', edgecolor='black')
for bar, val in zip(bars, values):
    axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    str(val), ha='center', va='bottom', fontweight='bold')
axes[1, 1].set_title('Bars with Value Labels')
axes[1, 1].grid(True, alpha=0.3, axis='y')
axes[1, 1].set_ylim(0, max(values) * 1.2)

plt.suptitle('Basic Bar Charts', fontsize=16)
plt.tight_layout()
plt.savefig('output/bar_basic.png', dpi=150)
plt.close()

print("Basic bar charts saved")
print()

# =============================================================================
# 2. GROUPED BAR CHARTS
# =============================================================================

print("=" * 60)
print("2. GROUPED BAR CHARTS")
print("=" * 60)

# Multi-series data
data = {
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Series 1': [23, 45, 56, 78, 32],
    'Series 2': [34, 32, 67, 45, 54],
    'Series 3': [45, 56, 34, 67, 76]
}
df = pd.DataFrame(data)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Method 1: Manual positioning
x = np.arange(len(df['Category']))
width = 0.25

axes[0, 0].bar(x - width, df['Series 1'], width, label='Series 1', color='skyblue')
axes[0, 0].bar(x, df['Series 2'], width, label='Series 2', color='lightcoral')
axes[0, 0].bar(x + width, df['Series 3'], width, label='Series 3', color='lightgreen')
axes[0, 0].set_xticks(x)
axes[0, 0].set_xticklabels(df['Category'])
axes[0, 0].set_title('Grouped Bars (Manual)')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Method 2: Pandas built-in
df.set_index('Category').plot(kind='bar', ax=axes[0, 1], width=0.8)
axes[0, 1].set_title('Grouped Bars (Pandas)')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Method 3: With error bars
np.random.seed(42)
errors = np.random.rand(5, 3) * 5
bar_positions = np.arange(len(df['Category']))
bar_width = 0.25

for i, (series, color) in enumerate(zip(['Series 1', 'Series 2', 'Series 3'], 
                                         ['skyblue', 'lightcoral', 'lightgreen'])):
    axes[1, 0].bar(bar_positions + (i - 1) * bar_width, df[series], bar_width,
                   label=series, color=color, yerr=errors[:, i], capsize=4)

axes[1, 0].set_xticks(bar_positions)
axes[1, 0].set_xticklabels(df['Category'])
axes[1, 0].set_title('Grouped Bars with Error Bars')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Method 4: Horizontal grouped
for i, (series, color) in enumerate(zip(['Series 1', 'Series 2', 'Series 3'], 
                                         ['skyblue', 'lightcoral', 'lightgreen'])):
    axes[1, 1].barh(bar_positions + (i - 1) * bar_width, df[series], bar_width,
                   label=series, color=color, xerr=errors[:, i], capsize=4)

axes[1, 1].set_yticks(bar_positions)
axes[1, 1].set_yticklabels(df['Category'])
axes[1, 1].invert_yaxis()
axes[1, 1].set_title('Horizontal Grouped Bars')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3, axis='x')

plt.suptitle('Grouped Bar Charts', fontsize=16)
plt.tight_layout()
plt.savefig('output/bar_grouped.png', dpi=150)
plt.close()

print("Grouped bar charts saved")
print()

# =============================================================================
# 3. STACKED BAR CHARTS
# =============================================================================

print("=" * 60)
print("3. STACKED BAR CHARTS")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Vertical stacked
bottom = np.zeros(len(df['Category']))
for series, color in zip(['Series 1', 'Series 2', 'Series 3'], 
                         ['skyblue', 'lightcoral', 'lightgreen']):
    axes[0, 0].bar(df['Category'], df[series], bottom=bottom, 
                   label=series, color=color)
    bottom += df[series].values

axes[0, 0].set_title('Vertical Stacked Bars')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Horizontal stacked
bottom = np.zeros(len(df['Category']))
for series, color in zip(['Series 1', 'Series 2', 'Series 3'], 
                         ['skyblue', 'lightcoral', 'lightgreen']):
    axes[0, 1].barh(df['Category'], df[series], left=bottom, 
                    label=series, color=color)
    bottom += df[series].values

axes[0, 1].set_title('Horizontal Stacked Bars')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3, axis='x')

# 100% Stacked (normalized)
df_norm = df.set_index('Category').div(df.set_index('Category').sum(axis=1), axis=0) * 100

bottom = np.zeros(len(df['Category']))
for series, color in zip(['Series 1', 'Series 2', 'Series 3'], 
                         ['skyblue', 'lightcoral', 'lightgreen']):
    axes[1, 0].bar(df['Category'], df_norm[series], bottom=bottom, 
                   label=series, color=color)
    bottom += df_norm[series].values

axes[1, 0].set_ylim(0, 100)
axes[1, 0].set_title('100% Stacked Bars (Percentage)')
axes[1, 0].set_ylabel('Percentage')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Diverging stacked (positive/negative)
diverging_data = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Positive': [20, 35, 30, 35, 27],
    'Negative': [-15, -25, -20, -30, -18]
})

axes[1, 1].bar(diverging_data['Category'], diverging_data['Positive'], 
               color='green', alpha=0.7, label='Positive')
axes[1, 1].bar(diverging_data['Category'], diverging_data['Negative'], 
               color='red', alpha=0.7, label='Negative')
axes[1, 1].axhline(y=0, color='black', linewidth=0.5)
axes[1, 1].set_title('Diverging Stacked Bars')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.suptitle('Stacked Bar Charts', fontsize=16)
plt.tight_layout()
plt.savefig('output/bar_stacked.png', dpi=150)
plt.close()

print("Stacked bar charts saved")
print()

# =============================================================================
# 4. ADVANCED BAR CUSTOMIZATION
# =============================================================================

print("=" * 60)
print("4. ADVANCED CUSTOMIZATION")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Gradient colors based on value
values = np.array([23, 45, 56, 78, 32])
norm = plt.Normalize(values.min(), values.max())
colors = plt.cm.RdYlGn(norm(values))

bars = axes[0, 0].bar(categories, values, color=colors, edgecolor='black')
# Colorbar
sm = plt.cm.ScalarMappable(cmap='RdYlGn', norm=norm)
sm.set_array([])
plt.colorbar(sm, ax=axes[0, 0], label='Value')
axes[0, 0].set_title('Gradient Colored Bars')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Patterned bars (hatching)
patterns = ['/', '\\', '|', '-', '+']
for cat, val, pat in zip(categories, values, patterns):
    axes[0, 1].bar(cat, val, color='white', edgecolor='black', 
                   hatch=pat, linewidth=1.5)
axes[0, 1].set_title('Hatched Bars')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Waterfall chart
waterfall_data = pd.DataFrame({
    'Category': ['Start', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'End'],
    'Value': [100, 20, -15, 30, -10, 25, -5, 0],  # Last is computed
    'Type': ['total', 'increase', 'decrease', 'increase', 'decrease', 
             'increase', 'decrease', 'total']
})

# Compute running total
running = 100
waterfall_data.loc[len(waterfall_data)-1, 'Value'] = running + waterfall_data['Value'][1:-1].sum()

colors_wf = ['gray' if t == 'total' else 'green' if v > 0 else 'red' 
             for t, v in zip(waterfall_data['Type'], waterfall_data['Value'])]

# Plot waterfall
bottoms = [0]
for i in range(1, len(waterfall_data)):
    if waterfall_data.iloc[i]['Type'] == 'total':
        bottoms.append(0)
    elif waterfall_data.iloc[i]['Value'] > 0:
        bottoms.append(running)
    else:
        bottoms.append(running + waterfall_data.iloc[i]['Value'])
    if waterfall_data.iloc[i]['Type'] != 'total':
        running += waterfall_data.iloc[i]['Value']

for i, (cat, val, typ, bot) in enumerate(zip(waterfall_data['Category'], 
                                              waterfall_data['Value'], 
                                              waterfall_data['Type'], bottoms)):
    if typ == 'total':
        axes[1, 0].bar(cat, val, bottom=0, color=colors_wf[i], edgecolor='black')
    else:
        axes[1, 0].bar(cat, val, bottom=bot, color=colors_wf[i], edgecolor='black')

axes[1, 0].set_title('Waterfall Chart')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Bar with confidence intervals
np.random.seed(42)
means = [10, 15, 12, 18, 14]
stds = [1.5, 2.0, 1.8, 2.2, 1.6]

bars = axes[1, 1].bar(categories, means, color='steelblue', edgecolor='black', 
                       yerr=stds, capsize=8, error_kw={'linewidth': 2})
# Color by significance
for bar, mean in zip(bars, means):
    if mean > 15:
        bar.set_color('darkgreen')
    elif mean < 12:
        bar.set_color('darkred')

axes[1, 1].set_title('Bars with Error Bars & Conditional Coloring')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.suptitle('Advanced Bar Customizations', fontsize=16)
plt.tight_layout()
plt.savefig('output/bar_advanced.png', dpi=150)
plt.close()

print("Advanced bar charts saved")
print()

# =============================================================================
# 5. REAL-WORLD EXAMPLE: SALES DASHBOARD
# =============================================================================

print("=" * 60)
print("5. REAL-WORLD EXAMPLE")
print("=" * 60)

# Monthly sales data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
sales_2022 = [45, 52, 48, 61, 55, 67, 72, 69, 75, 82, 78, 85]
sales_2023 = [52, 58, 62, 65, 70, 78, 82, 85, 88, 92, 90, 95]
target = [50, 55, 55, 60, 65, 70, 75, 75, 80, 85, 85, 90]

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Year comparison grouped
x = np.arange(len(months))
width = 0.35
axes[0, 0].bar(x - width/2, sales_2022, width, label='2022', color='lightblue', edgecolor='black')
axes[0, 0].bar(x + width/2, sales_2023, width, label='2023', color='darkblue', edgecolor='black')
axes[0, 0].set_xticks(x)
axes[0, 0].set_xticklabels(months, rotation=45)
axes[0, 0].set_title('Monthly Sales: 2022 vs 2023')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3, axis='y')

# 2. Actual vs Target (bullet chart style)
axes[0, 1].barh(range(len(months)), sales_2023, height=0.6, color='steelblue', label='Actual')
axes[0, 1].barh(range(len(months)), target, height=0.3, color='lightgray', label='Target', left=0)
axes[0, 1].set_yticks(range(len(months)))
axes[0, 1].set_yticklabels(months)
axes[0, 1].invert_yaxis()
axes[0, 1].set_title('Actual vs Target (Bullet Style)')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3, axis='x')

# 3. Cumulative with growth rate
cum_2022 = np.cumsum(sales_2022)
cum_2023 = np.cumsum(sales_2023)
growth = [(sales_2023[i] - sales_2022[i]) / sales_2022[i] * 100 for i in range(len(months))]

ax3 = axes[1, 0]
ax3.bar(months, cum_2023, color='lightgreen', alpha=0.7, label='Cumulative 2023', edgecolor='black')
ax3.plot(months, growth, 'ro-', linewidth=2, markersize=6, label='YoY Growth %')
ax3.set_ylabel('Cumulative Sales')
ax3_twin = ax3.twinx()
ax3_twin.set_ylabel('Growth %', color='red')
ax3_twin.tick_params(axis='y', labelcolor='red')
lines1, labels1 = ax3.get_legend_handles_labels()
lines2, labels2 = ax3_twin.get_legend_handles_labels()
ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax3.set_title('Cumulative Sales with Growth Rate')
ax3.tick_params(axis='x', rotation=45)

# 4. Category breakdown stacked
categories = ['Product A', 'Product B', 'Product C', 'Services']
cat_data = pd.DataFrame({
    'Product A': [15, 18, 16, 20, 19, 22, 24, 23, 25, 27, 26, 28],
    'Product B': [12, 14, 13, 15, 16, 18, 19, 20, 21, 22, 21, 23],
    'Product C': [10, 11, 10, 12, 11, 13, 14, 15, 15, 16, 15, 17],
    'Services': [15, 15, 15, 18, 19, 23, 25, 27, 27, 27, 28, 27]
}, index=months)

cat_data.plot(kind='bar', stacked=True, ax=axes[1, 1], colormap='Set2')
axes[1, 1].set_title('Sales by Category (Stacked)')
axes[1, 1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
axes[1, 1].tick_params(axis='x', rotation=45)
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.suptitle('Sales Dashboard - Bar Chart Examples', fontsize=16)
plt.tight_layout()
plt.savefig('output/bar_dashboard.png', dpi=150)
plt.close()

print("Sales dashboard saved")
print()

# =============================================================================
# SUMMARY
# =============================================================================

print("=" * 60)
print("BAR CHARTS COMPLETE")
print("=" * 60)
print("""
Key Concepts:
1. Basic: bar() vertical, barh() horizontal
2. Grouped: Multiple bars side-by-side (manual or pandas)
3. Stacked: bottom parameter for vertical, left for horizontal
4. 100% Stacked: Normalize to percentages
5. Diverging: Positive/negative bars from center
6. Advanced: Waterfall, gradient colors, hatching, error bars
6. Dashboard patterns: Year-over-year, actual vs target, cumulative

Next: Histograms, box plots, violin plots
""")