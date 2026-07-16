"""
Bar Chart
W3Schools: https://www.w3schools.com/python/pandas_plotting_bar.asp

Bar charts compare quantities across categories. They are one of the most
common chart types for categorical data.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import tempfile

# ---------------------------------------------------------------------------
# Example 1: Simple vertical bar chart
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Vertical Bar Chart")
print("=" * 60)

df = pd.DataFrame({
    "Fruit": ["Apple", "Banana", "Cherry", "Date", "Elderberry"],
    "Sales": [450, 320, 280, 150, 90],
})

print("Fruit Sales:")
print(df)
print()

fig, ax = plt.subplots(figsize=(8, 5))
df.plot.bar(x="Fruit", y="Sales", ax=ax, color="steelblue", edgecolor="white")
ax.set_title("Fruit Sales")
ax.set_ylabel("Units Sold")
ax.set_xlabel("")
ax.grid(True, alpha=0.3, axis="y")
path1 = os.path.join(tempfile.gettempdir(), "pandas_ex19_bar1.png")
fig.savefig(path1, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path1}")
print()

# ---------------------------------------------------------------------------
# Example 2: Horizontal bar chart
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Horizontal Bar Chart")
print("=" * 60)

df2 = pd.DataFrame({
    "Language": ["Python", "JavaScript", "Java", "C++", "Go", "Rust"],
    "GitHub_Repos": [1500000, 1800000, 900000, 400000, 250000, 150000],
})

fig, ax = plt.subplots(figsize=(8, 5))
df2.plot.barh(x="Language", y="GitHub_Repos", ax=ax, color="coral", edgecolor="white")
ax.set_title("GitHub Repositories by Language")
ax.set_xlabel("Number of Repositories")
ax.set_ylabel("")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x/1e6:.1f}M"))
ax.grid(True, alpha=0.3, axis="x")
path2 = os.path.join(tempfile.gettempdir(), "pandas_ex19_bar2.png")
fig.savefig(path2, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path2}")
print()

# ---------------------------------------------------------------------------
# Example 3: Grouped bar chart
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Grouped Bar Chart")
print("=" * 60)

df3 = pd.DataFrame({
    "Q1": [120, 90, 150, 80],
    "Q2": [130, 110, 140, 95],
    "Q3": [145, 100, 160, 110],
    "Q4": [160, 125, 175, 130],
}, index=["Product A", "Product B", "Product C", "Product D"])

print("Quarterly Sales:")
print(df3)
print()

fig, ax = plt.subplots(figsize=(10, 5))
df3.plot.bar(ax=ax, edgecolor="white")
ax.set_title("Quarterly Sales by Product")
ax.set_ylabel("Units Sold")
ax.set_xlabel("")
ax.legend(title="Quarter")
ax.grid(True, alpha=0.3, axis="y")
plt.xticks(rotation=0)
path3 = os.path.join(tempfile.gettempdir(), "pandas_ex19_bar3.png")
fig.savefig(path3, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path3}")
print()

# ---------------------------------------------------------------------------
# Example 4: Stacked bar chart
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Stacked Bar Chart")
print("=" * 60)

df4 = pd.DataFrame({
    "Online": [60, 45, 70, 55],
    "In-Store": [40, 55, 30, 45],
    "Phone": [20, 15, 25, 20],
}, index=["Jan", "Feb", "Mar", "Apr"])

print("Sales by Channel:")
print(df4)
print()

fig, ax = plt.subplots(figsize=(8, 5))
df4.plot.bar(stacked=True, ax=ax, color=["#4472C4", "#ED7D31", "#A5A5A5"], edgecolor="white")
ax.set_title("Sales by Channel (Stacked)")
ax.set_ylabel("Units Sold")
ax.set_xlabel("Month")
ax.legend(title="Channel")
ax.grid(True, alpha=0.3, axis="y")
plt.xticks(rotation=0)
path4 = os.path.join(tempfile.gettempdir(), "pandas_ex19_bar4.png")
fig.savefig(path4, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path4}")
print()

# ---------------------------------------------------------------------------
# Example 5: Bar chart with value labels
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Bar Chart with Value Labels")
print("=" * 60)

df5 = pd.DataFrame({
    "Country": ["USA", "China", "Japan", "Germany", "UK"],
    "GDP_Trillion": [25.5, 18.3, 4.2, 4.1, 3.1],
})

fig, ax = plt.subplots(figsize=(8, 5))
bars = df5.plot.bar(x="Country", y="GDP_Trillion", ax=ax, color="#2ecc71", edgecolor="white", legend=False)
ax.set_title("GDP by Country (2024)")
ax.set_ylabel("GDP (Trillion USD)")
ax.set_xlabel("")
ax.grid(True, alpha=0.3, axis="y")

# Add value labels on bars
for bar in ax.patches:
    height = bar.get_height()
    ax.annotate(
        f"${height:.1f}T",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha="center", va="bottom", fontsize=9,
    )

plt.xticks(rotation=0)
path5 = os.path.join(tempfile.gettempdir(), "pandas_ex19_bar5.png")
fig.savefig(path5, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path5}")
print()
print("Done!")
