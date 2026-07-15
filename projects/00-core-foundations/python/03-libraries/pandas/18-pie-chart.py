"""
Pie Chart
W3Schools: https://www.w3schools.com/python/pandas_plotting_pie.asp

A pie chart shows proportions of a whole. Useful for categorical data.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import tempfile

# ---------------------------------------------------------------------------
# Example 1: Basic pie chart
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Basic Pie Chart")
print("=" * 60)

df = pd.DataFrame({
    "Language": ["Python", "JavaScript", "Java", "C#", "Go"],
    "Popularity": [30, 25, 20, 15, 10],
})
print("Language Popularity:")
print(df)
print()

fig, ax = plt.subplots(figsize=(7, 7))
df.set_index("Language")["Popularity"].plot.pie(
    ax=ax, autopct="%1.1f%%", startangle=90, colors=plt.cm.Set2.colors
)
ax.set_title("Programming Language Popularity")
ax.set_ylabel("")  # Remove default ylabel
path1 = os.path.join(tempfile.gettempdir(), "pandas_ex18_pie1.png")
fig.savefig(path1, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path1}")
print()

# ---------------------------------------------------------------------------
# Example 2: Exploded pie chart
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Exploded Pie Chart")
print("=" * 60)

df2 = pd.DataFrame({
    "OS": ["Windows", "macOS", "Linux", "Other"],
    "Market_Share": [72, 15, 8, 5],
})

fig, ax = plt.subplots(figsize=(7, 7))
df2.set_index("OS")["Market_Share"].plot.pie(
    ax=ax,
    autopct="%1.1f%%",
    startangle=140,
    explode=[0.05, 0, 0, 0],  # Slightly explode Windows
    colors=["#4472C4", "#A5A5A5", "#FFC000", "#70AD47"],
    shadow=True,
)
ax.set_title("Desktop OS Market Share")
ax.set_ylabel("")
path2 = os.path.join(tempfile.gettempdir(), "pandas_ex18_pie2.png")
fig.savefig(path2, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path2}")
print()

# ---------------------------------------------------------------------------
# Example 3: Multiple pie charts (subplots)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Side-by-Side Pie Charts")
print("=" * 60)

df3 = pd.DataFrame({
    "Category": ["Rent", "Food", "Transport", "Entertainment", "Savings"],
    "Year1": [35, 25, 15, 10, 15],
    "Year2": [30, 20, 10, 15, 25],
})

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

df3.set_index("Category")["Year1"].plot.pie(
    ax=axes[0], autopct="%1.1f%%", startangle=90, colors=plt.cm.Pastel1.colors
)
axes[0].set_title("Year 1 Budget")
axes[0].set_ylabel("")

df3.set_index("Category")["Year2"].plot.pie(
    ax=axes[1], autopct="%1.1f%%", startangle=90, colors=plt.cm.Pastel1.colors
)
axes[1].set_title("Year 2 Budget")
axes[1].set_ylabel("")

plt.suptitle("Budget Allocation Comparison", fontsize=14, y=1.02)
plt.tight_layout()
path3 = os.path.join(tempfile.gettempdir(), "pandas_ex18_pie3.png")
fig.savefig(path3, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path3}")
print()

# ---------------------------------------------------------------------------
# Example 4: Donut chart (pie with inner circle)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Donut Chart")
print("=" * 60)

df4 = pd.DataFrame({
    "Status": ["Completed", "In Progress", "Pending", "Cancelled"],
    "Count": [45, 20, 25, 10],
})

fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    df4["Count"],
    labels=df4["Status"],
    autopct="%1.1f%%",
    startangle=90,
    colors=["#2ecc71", "#3498db", "#f39c12", "#e74c3c"],
    pctdistance=0.85,
)
# Draw a white circle in the center to create a donut
centre_circle = plt.Circle((0, 0), 0.60, fc="white")
ax.add_artist(centre_circle)
ax.set_title("Task Status Distribution")
# Add total in center
total = df4["Count"].sum()
ax.text(0, 0, f"Total\n{total}", ha="center", va="center", fontsize=16, fontweight="bold")
path4 = os.path.join(tempfile.gettempdir(), "pandas_ex18_pie4.png")
fig.savefig(path4, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path4}")
print()

# ---------------------------------------------------------------------------
# Example 5: Pie from value_counts
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Pie from value_counts()")
print("=" * 60)

orders = pd.DataFrame({
    "product": np.random.choice(
        ["Espresso", "Latte", "Cappuccino", "Americano", "Mocha"],
        size=200,
        p=[0.15, 0.30, 0.25, 0.20, 0.10],
    )
})

vc = orders["product"].value_counts()
print("Order counts:")
print(vc)
print()

fig, ax = plt.subplots(figsize=(7, 7))
vc.plot.pie(ax=ax, autopct="%1.1f%%", startangle=140, colors=plt.cm.Set3.colors)
ax.set_title("Coffee Orders")
ax.set_ylabel("")
path5 = os.path.join(tempfile.gettempdir(), "pandas_ex18_pie5.png")
fig.savefig(path5, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path5}")
print()
print("Done!")
