"""
Pandas Plotting
W3Schools: https://www.w3schools.com/python/pandas_plotting.asp

Pandas integrates with matplotlib to provide built-in plotting.
This covers line plots, area plots, and other visualization types.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import tempfile

# ---------------------------------------------------------------------------
# Example 1: Line plot
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Line Plot")
print("=" * 60)

np.random.seed(42)
dates = pd.date_range("2024-01-01", periods=12, freq="ME")
df_stock = pd.DataFrame({
    "Date": dates,
    "Stock_A": np.cumsum(np.random.randn(12)) + 100,
    "Stock_B": np.cumsum(np.random.randn(12)) + 100,
    "Stock_C": np.cumsum(np.random.randn(12)) + 100,
}).set_index("Date")

print("Stock data:")
print(df_stock.round(2))
print()

fig, ax = plt.subplots(figsize=(10, 5))
df_stock.plot(ax=ax, marker="o", linewidth=2)
ax.set_title("Stock Price Trends")
ax.set_ylabel("Price ($)")
ax.grid(True, alpha=0.3)
ax.legend()
path1 = os.path.join(tempfile.gettempdir(), "pandas_ex24_line.png")
fig.savefig(path1, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path1}")
print()

# ---------------------------------------------------------------------------
# Example 2: Area plot
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Area Plot (Stacked)")
print("=" * 60)

df_area = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Electronics": [120, 130, 145, 160, 170, 180],
    "Clothing": [80, 85, 90, 95, 100, 110],
    "Food": [200, 210, 195, 220, 230, 240],
    "Home": [60, 65, 70, 75, 80, 85],
}).set_index("Month")

print("Monthly sales:")
print(df_area)
print()

fig, ax = plt.subplots(figsize=(10, 5))
df_area.plot.area(ax=ax, alpha=0.7, stacked=True)
ax.set_title("Sales by Category (Area Chart)")
ax.set_ylabel("Revenue ($K)")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper left")
path2 = os.path.join(tempfile.gettempdir(), "pandas_ex24_area.png")
fig.savefig(path2, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path2}")
print()

# ---------------------------------------------------------------------------
# Example 3: Box plot
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Box Plot")
print("=" * 60)

df_box = pd.DataFrame({
    "Q1": np.random.normal(70, 15, 100),
    "Q2": np.random.normal(75, 10, 100),
    "Q3": np.random.normal(68, 20, 100),
    "Q4": np.random.normal(80, 12, 100),
})

print("Quarterly score statistics:")
print(df_box.describe().round(1))
print()

fig, ax = plt.subplots(figsize=(8, 5))
df_box.plot.box(ax=ax, patch_artist=True,
                boxprops=dict(facecolor="lightblue", color="steelblue"),
                medianprops=dict(color="red", linewidth=2))
ax.set_title("Score Distribution by Quarter")
ax.set_ylabel("Score")
ax.grid(True, alpha=0.3, axis="y")
path3 = os.path.join(tempfile.gettempdir(), "pandas_ex24_box.png")
fig.savefig(path3, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path3}")
print()

# ---------------------------------------------------------------------------
# Example 4: Combined dashboard
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Multi-Panel Dashboard")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Line plot
df_stock.plot(ax=axes[0, 0], marker="o")
axes[0, 0].set_title("Stock Trends")
axes[0, 0].grid(True, alpha=0.3)

# Panel 2: Bar chart
df_area.sum().plot.bar(ax=axes[0, 1], color=plt.cm.Set2.colors)
axes[0, 1].set_title("Total Sales by Category")
axes[0, 1].set_ylabel("Revenue ($K)")

# Panel 3: Box plot
df_box.plot.box(ax=axes[1, 0], patch_artist=True,
                boxprops=dict(facecolor="lightyellow"))
axes[1, 0].set_title("Score Distribution")

# Panel 4: Histogram
data = np.random.normal(75, 15, 500)
axes[1, 1].hist(data, bins=25, color="steelblue", edgecolor="white", alpha=0.8)
axes[1, 1].set_title("Score Distribution (Histogram)")
axes[1, 1].set_xlabel("Score")
axes[1, 1].set_ylabel("Frequency")
axes[1, 1].grid(True, alpha=0.3, axis="y")

plt.suptitle("Analytics Dashboard", fontsize=16, fontweight="bold", y=1.01)
plt.tight_layout()
path4 = os.path.join(tempfile.gettempdir(), "pandas_ex24_dashboard.png")
fig.savefig(path4, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path4}")
print()

# ---------------------------------------------------------------------------
# Example 5: Subplots with twin axes
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Dual-Axis Plot")
print("=" * 60)

df_dual = pd.DataFrame({
    "Month": pd.date_range("2024-01-01", periods=6, freq="ME"),
    "Revenue": [100, 120, 110, 140, 160, 175],
    "Profit_Margin": [0.15, 0.18, 0.12, 0.20, 0.22, 0.25],
}).set_index("Month")

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(df_dual.index, df_dual["Revenue"], width=20, color="steelblue", alpha=0.7, label="Revenue")
ax1.set_ylabel("Revenue ($K)", color="steelblue")
ax1.tick_params(axis="y", labelcolor="steelblue")

ax2 = ax1.twinx()
ax2.plot(df_dual.index, df_dual["Profit_Margin"], color="coral", marker="o", linewidth=2, label="Margin")
ax2.set_ylabel("Profit Margin", color="coral")
ax2.tick_params(axis="y", labelcolor="coral")
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.0%}"))

ax1.set_title("Revenue vs Profit Margin")
fig.tight_layout()
path5 = os.path.join(tempfile.gettempdir(), "pandas_ex24_dual_axis.png")
fig.savefig(path5, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path5}")
print()
print("Done!")
