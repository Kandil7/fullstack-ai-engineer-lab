"""
Pandas Visualization: Built-in plotting with Matplotlib
=======================================================

Quick data visualization directly from pandas DataFrames.
"""

import os
os.environ.setdefault("MPLBACKEND", "Agg")  # never open a GUI window

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False
    print("[skip] seaborn not installed — pip install seaborn")

np.random.seed(42)

# =============================================================================
# 1. SETUP & BASIC PLOTS
# =============================================================================

print("=" * 60)
print("1. BASIC PANDAS PLOTTING")
print("=" * 60)

# Create sample data
df = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=100, freq='D'),
    'sales': np.random.randn(100).cumsum() + 100,
    'visitors': np.random.poisson(50, 100),
    'conversion_rate': np.random.beta(2, 8, 100) * 100,
    'channel': np.random.choice(['Organic', 'Paid', 'Social', 'Email'], 100),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
    'device': np.random.choice(['Desktop', 'Mobile', 'Tablet'], 100)
})

# Set style
plt.style.use('seaborn-v0_8-whitegrid')

# Basic line plot
ax = df['sales'].plot(figsize=(10, 4), title='Daily Sales', color='steelblue')
ax.set_ylabel('Sales ($)')
plt.tight_layout()
plt.savefig('output/sales_line.png', dpi=150)
plt.close()

# Multiple lines
df[['sales', 'visitors']].plot(figsize=(10, 4), title='Sales vs Visitors')
plt.savefig('output/multi_line.png', dpi=150)
plt.close()

print("Basic plots created and saved to output/")
print()

# =============================================================================
# 2. PLOT KINDS
# =============================================================================

print("=" * 60)
print("2. PLOT KINDS")
print("=" * 60)

# Bar plot
channel_sales = df.groupby('channel')['sales'].mean().sort_values(ascending=False)
ax = channel_sales.plot(kind='bar', figsize=(8, 5), title='Avg Sales by Channel', color='coral')
ax.set_ylabel('Average Sales ($)')
plt.tight_layout()
plt.savefig('output/bar_plot.png', dpi=150)
plt.close()

# Horizontal bar
ax = channel_sales.plot(kind='barh', figsize=(8, 5), title='Avg Sales by Channel (Horizontal)', color='teal')
ax.set_xlabel('Average Sales ($)')
plt.tight_layout()
plt.savefig('output/barh_plot.png', dpi=150)
plt.close()

# Histogram
ax = df['sales'].plot(kind='hist', bins=20, figsize=(8, 5), title='Sales Distribution', alpha=0.7, edgecolor='black')
ax.set_xlabel('Sales ($)')
plt.tight_layout()
plt.savefig('output/histogram.png', dpi=150)
plt.close()

# Density (KDE)
ax = df['sales'].plot(kind='kde', figsize=(8, 5), title='Sales Density', linewidth=2)
plt.tight_layout()
plt.savefig('output/kde.png', dpi=150)
plt.close()

# Box plot
ax = df.boxplot(column='sales', by='channel', figsize=(10, 6))
plt.title('Sales by Channel')
plt.suptitle('')  # Remove default title
plt.xlabel('Channel')
plt.ylabel('Sales ($)')
plt.tight_layout()
plt.savefig('output/boxplot.png', dpi=150)
plt.close()

# Scatter plot
ax = df.plot(kind='scatter', x='visitors', y='sales', c='conversion_rate', 
             colormap='viridis', figsize=(8, 6), title='Sales vs Visitors')
plt.tight_layout()
plt.savefig('output/scatter.png', dpi=150)
plt.close()

# Hexbin (for large datasets)
large_df = pd.DataFrame({
    'x': np.random.randn(5000),
    'y': np.random.randn(5000)
})
ax = large_df.plot(kind='hexbin', x='x', y='y', gridsize=30, figsize=(8, 6), 
                   title='Hexbin Plot', colormap='Blues')
plt.tight_layout()
plt.savefig('output/hexbin.png', dpi=150)
plt.close()

# Pie chart
device_counts = df['device'].value_counts()
ax = device_counts.plot(kind='pie', figsize=(6, 6), title='Device Distribution', 
                        autopct='%1.1f%%', startangle=90)
plt.ylabel('')
plt.tight_layout()
plt.savefig('output/pie.png', dpi=150)
plt.close()

# Area plot
df.set_index('date')[['sales', 'visitors']].plot.area(figsize=(10, 5), title='Cumulative Sales & Visitors', alpha=0.5)
plt.tight_layout()
plt.savefig('output/area.png', dpi=150)
plt.close()

print("All plot kinds demonstrated and saved")
print()

# =============================================================================
# 3. SUBPLOTS & MULTIPLE AXES
# =============================================================================

print("=" * 60)
print("3. SUBPLOTS & MULTIPLE AXES")
print("=" * 60)

# Subplots from DataFrame
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Top-left: Line
df.set_index('date')['sales'].plot(ax=axes[0, 0], title='Sales Over Time', color='blue')
axes[0, 0].set_ylabel('Sales')

# Top-right: Histogram
df['sales'].plot(kind='hist', ax=axes[0, 1], bins=15, title='Sales Distribution', alpha=0.7)

# Bottom-left: Box plot
df.boxplot(column='sales', by='channel', ax=axes[1, 0])
axes[1, 0].set_title('Sales by Channel')

# Bottom-right: Scatter
df.plot.scatter(x='visitors', y='sales', ax=axes[1, 1], title='Sales vs Visitors')

plt.suptitle('Dashboard Overview', fontsize=16)
plt.tight_layout()
plt.savefig('output/subplots.png', dpi=150)
plt.close()

# Subplots with plot method
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
df.groupby('channel')['sales'].mean().plot(kind='bar', ax=axes[0, 0], title='Avg Sales by Channel')
df.groupby('region')['sales'].sum().plot(kind='pie', ax=axes[0, 1], title='Sales by Region', autopct='%1.1f%%')
df.groupby('device')['conversion_rate'].mean().plot(kind='barh', ax=axes[1, 0], title='Conversion by Device')
df.set_index('date').resample('W')['sales'].sum().plot(ax=axes[1, 1], title='Weekly Sales')

plt.tight_layout()
plt.savefig('output/subplots2.png', dpi=150)
plt.close()

print("Subplot examples created")
print()

# =============================================================================
# 4. GROUPBY PLOTTING
# =============================================================================

print("=" * 60)
print("4. GROUPBY PLOTTING")
print("=" * 60)

# Multiple lines by group
fig, ax = plt.subplots(figsize=(10, 6))
for channel in df['channel'].unique():
    subset = df[df['channel'] == channel].set_index('date')
    subset['sales'].rolling(7).mean().plot(ax=ax, label=channel, alpha=0.8)
ax.set_title('7-Day Rolling Avg Sales by Channel')
ax.legend()
plt.tight_layout()
plt.savefig('output/groupby_lines.png', dpi=150)
plt.close()

# Grouped bar
pivot = df.pivot_table(values='sales', index='channel', columns='device', aggfunc='mean')
pivot.plot(kind='bar', figsize=(10, 6), title='Avg Sales by Channel & Device')
plt.xlabel('Channel')
plt.ylabel('Avg Sales ($)')
plt.tight_layout()
plt.savefig('output/grouped_bar.png', dpi=150)
plt.close()

# Stacked bar
pivot.plot(kind='bar', stacked=True, figsize=(10, 6), title='Stacked: Sales by Channel & Device')
plt.tight_layout()
plt.savefig('output/stacked_bar.png', dpi=150)
plt.close()

print("GroupBy plotting examples created")
print()

# =============================================================================
# 5. ADVANCED CUSTOMIZATION
# =============================================================================

print("=" * 60)
print("5. ADVANCED CUSTOMIZATION")
print("=" * 60)

fig, ax = plt.subplots(figsize=(12, 6))

# Plot with custom styling
df.set_index('date')['sales'].plot(
    ax=ax,
    color='#2E86AB',
    linewidth=2,
    alpha=0.8,
    label='Daily Sales'
)

# Add rolling average
df.set_index('date')['sales'].rolling(7).mean().plot(
    ax=ax,
    color='#A23B72',
    linewidth=3,
    label='7-Day MA'
)

# Add confidence band
rolling_mean = df.set_index('date')['sales'].rolling(7).mean()
rolling_std = df.set_index('date')['sales'].rolling(7).std()
ax.fill_between(rolling_mean.index, 
                rolling_mean - 2*rolling_std, 
                rolling_mean + 2*rolling_std,
                color='#A23B72', alpha=0.1, label='±2σ')

# Customize
ax.set_title('Sales with 7-Day Moving Average & Confidence Band', fontsize=14, fontweight='bold')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Sales ($)', fontsize=12)
ax.legend(loc='upper left', framealpha=0.9)
ax.grid(True, alpha=0.3)

# Annotate
ax.annotate('Peak', xy=('2023-03-15', 150), xytext=('2023-02-15', 160),
            arrowprops=dict(arrowstyle='->', color='red'), fontsize=12)

plt.tight_layout()
plt.savefig('output/customized.png', dpi=150)
plt.close()

# Twin axes
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.set_xlabel('Date')
ax1.set_ylabel('Sales ($)', color='tab:blue')
df.set_index('date')['sales'].plot(ax=ax1, color='tab:blue', label='Sales')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Visitors', color='tab:orange')
df.set_index('date')['visitors'].plot(ax=ax2, color='tab:orange', label='Visitors', alpha=0.7)
ax2.tick_params(axis='y', labelcolor='tab:orange')

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.title('Sales vs Visitors (Dual Axis)')
plt.tight_layout()
plt.savefig('output/twin_axes.png', dpi=150)
plt.close()

print("Advanced customization examples created")
print()

# =============================================================================
# 6. INTEGRATION WITH SEABORN
# =============================================================================

print("=" * 60)
print("6. SEABORN INTEGRATION")
print("=" * 60)

if not HAS_SEABORN:
    print("[skip] seaborn not installed — seaborn section skipped (pip install seaborn)")
else:
    # Seaborn works directly with pandas DataFrames
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Pairplot (subset for speed; sample(200, replace=True) because df has 100 rows)
    sns.pairplot(df[['sales', 'visitors', 'conversion_rate', 'channel']].sample(200, replace=True),
                 hue='channel', diag_kind='kde', corner=True)
    plt.savefig('output/pairplot.png', dpi=150)
    plt.close()

    # Violin plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(data=df, x='channel', y='sales', ax=ax, palette='Set2')
    ax.set_title('Sales Distribution by Channel (Violin)')
    plt.tight_layout()
    plt.savefig('output/violin.png', dpi=150)
    plt.close()

    # Swarm plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.swarmplot(data=df, x='channel', y='sales', ax=ax, palette='Set2', size=4)
    ax.set_title('Sales by Channel (Swarm)')
    plt.tight_layout()
    plt.savefig('output/swarm.png', dpi=150)
    plt.close()

    # Heatmap
    corr = df[['sales', 'visitors', 'conversion_rate']].corr()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, ax=ax,
                square=True, cbar_kws={'shrink': 0.8})
    ax.set_title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig('output/heatmap.png', dpi=150)
    plt.close()

    print("Seaborn integration examples created")
    print()

# =============================================================================
# 7. SAVING & EXPORTING
# =============================================================================

print("=" * 60)
print("7. SAVING & EXPORTING")
print("=" * 60)

# Save with high DPI
fig, ax = plt.subplots(figsize=(10, 6))
df.set_index('date')['sales'].plot(ax=ax, title='High Quality Export')
plt.tight_layout()
plt.savefig('output/high_dpi.png', dpi=300, bbox_inches='tight')
plt.savefig('output/high_dpi.pdf', bbox_inches='tight')  # Vector format
plt.close()

# Save with transparent background
fig, ax = plt.subplots(figsize=(8, 6))
df['sales'].plot(kind='hist', ax=ax, bins=20, alpha=0.7)
plt.savefig('output/transparent.png', dpi=150, transparent=True)
plt.close()

# Save multiple figures to PDF
from matplotlib.backends.backend_pdf import PdfPages
with PdfPages('output/multi_page.pdf') as pdf:
    for i, col in enumerate(['sales', 'visitors', 'conversion_rate']):
        fig, ax = plt.subplots(figsize=(8, 5))
        df[col].plot(kind='hist', ax=ax, bins=20, title=f'{col} Distribution')
        pdf.savefig(fig)
        plt.close()

print("Export examples created (PNG, PDF, transparent)")
print()

# =============================================================================
# 8. PLOTTING WITH CATEGORICAL DATA
# =============================================================================

print("=" * 60)
print("8. PLOTTING WITH CATEGORICAL DATA")
print("=" * 60)

# Categorical data with order
df['channel'] = pd.Categorical(df['channel'], categories=['Organic', 'Paid', 'Social', 'Email'], ordered=True)
df['device'] = pd.Categorical(df['device'], categories=['Desktop', 'Tablet', 'Mobile'], ordered=True)

# Ordered bar plot respects category order
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
df.groupby('channel')['sales'].mean().plot(kind='bar', ax=axes[0], title='Ordered by Channel Priority')
df.groupby('device')['conversion_rate'].mean().plot(kind='bar', ax=axes[1], title='Ordered by Device Size')
plt.tight_layout()
plt.savefig('output/categorical_order.png', dpi=150)
plt.close()

print("Categorical plotting preserves order")
print()

# =============================================================================
# 9. INTERACTIVE PLOTTING (PLOTLY)
# =============================================================================

print("=" * 60)
print("9. INTERACTIVE PLOTTING (PLOTLY - CONCEPT)")
print("=" * 60)

plotly_example = """
# Install: pip install plotly
import plotly.express as px

# Interactive line
fig = px.line(df, x='date', y='sales', color='channel', title='Interactive Sales')
fig.show()

# Interactive scatter
fig = px.scatter(df, x='visitors', y='sales', color='channel', size='conversion_rate',
                 hover_data=['date', 'region'], title='Interactive Scatter')
fig.show()

# Interactive bar
fig = px.bar(df.groupby('channel')['sales'].mean().reset_index(), 
             x='channel', y='sales', title='Interactive Bar')
fig.show()

# Save as HTML
fig.write_html('output/interactive.html')
"""
print(plotly_example)

print("\n" + "=" * 60)
print("END OF VISUALIZATION")
print("=" * 60)