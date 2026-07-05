"""
Histogram
W3Schools: https://www.w3schools.com/python/pandas_plotting_hist.asp

A histogram is an approximate representation of the distribution of
numerical data. It groups data into bins and shows frequency.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import tempfile

# ---------------------------------------------------------------------------
# Example 1: Basic histogram
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Basic Histogram")
print("=" * 60)

np.random.seed(42)
df = pd.DataFrame({
    "age": np.random.normal(35, 10, 500).astype(int),
})

print("Age statistics:")
print(df["age"].describe().round(1))
print()

fig, ax = plt.subplots(figsize=(8, 5))
df["age"].plot.hist(bins=20, ax=ax, color="steelblue", edgecolor="white", alpha=0.8)
ax.set_title("Age Distribution")
ax.set_xlabel("Age")
ax.set_ylabel("Frequency")
ax.grid(True, alpha=0.3, axis="y")
path1 = os.path.join(tempfile.gettempdir(), "pandas_ex17_hist1.png")
fig.savefig(path1, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path1}")
print()

# ---------------------------------------------------------------------------
# Example 2: Multiple histograms on one plot
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Overlaid Histograms")
print("=" * 60)

df2 = pd.DataFrame({
    "score_A": np.random.normal(70, 15, 200),
    "score_B": np.random.normal(60, 20, 200),
})

print("Score A stats:", df2["score_A"].describe().round(1).to_dict())
print("Score B stats:", df2["score_B"].describe().round(1).to_dict())
print()

fig, ax = plt.subplots(figsize=(8, 5))
df2["score_A"].hist(bins=25, ax=ax, alpha=0.6, color="steelblue", label="Score A")
df2["score_B"].hist(bins=25, ax=ax, alpha=0.6, color="coral", label="Score B")
ax.set_title("Score Distributions")
ax.set_xlabel("Score")
ax.set_ylabel("Frequency")
ax.legend()
ax.grid(True, alpha=0.3, axis="y")
path2 = os.path.join(tempfile.gettempdir(), "pandas_ex17_hist2.png")
fig.savefig(path2, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path2}")
print()

# ---------------------------------------------------------------------------
# Example 3: Histogram with custom bins
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Custom Bin Ranges")
print("=" * 60)

df3 = pd.DataFrame({
    "salary": np.random.lognormal(11, 0.5, 500).round(0),
})

# Define specific bins
bins = [0, 30000, 50000, 75000, 100000, 150000, 300000]
labels = ["<30K", "30-50K", "50-75K", "75-100K", "100-150K", "150K+"]
df3["salary_range"] = pd.cut(df3["salary"], bins=bins, labels=labels)

print("Salary range distribution:")
print(df3["salary_range"].value_counts().sort_index())
print()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: raw histogram
df3["salary"].plot.hist(bins=30, ax=axes[0], color="steelblue", edgecolor="white")
axes[0].set_title("Salary Distribution (Raw)")
axes[0].set_xlabel("Salary ($)")
axes[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

# Right: binned bar chart
df3["salary_range"].value_counts().sort_index().plot.bar(
    ax=axes[1], color="steelblue", edgecolor="white"
)
axes[1].set_title("Salary Range Distribution (Binned)")
axes[1].set_xlabel("Salary Range")
axes[1].set_ylabel("Count")

plt.tight_layout()
path3 = os.path.join(tempfile.gettempdir(), "pandas_ex17_hist3.png")
fig.savefig(path3, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path3}")
print()

# ---------------------------------------------------------------------------
# Example 4: Histogram by group
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Histogram by Group")
print("=" * 60)

df4 = pd.DataFrame({
    "score": np.concatenate([
        np.random.normal(75, 10, 100),  # Class A
        np.random.normal(65, 15, 100),  # Class B
    ]),
    "class": ["A"] * 100 + ["B"] * 100,
})

fig, ax = plt.subplots(figsize=(8, 5))
for label, group in df4.groupby("class"):
    group["score"].hist(bins=20, ax=ax, alpha=0.5, label=f"Class {label}")
ax.set_title("Score Distribution by Class")
ax.set_xlabel("Score")
ax.set_ylabel("Frequency")
ax.legend()
ax.grid(True, alpha=0.3, axis="y")
path4 = os.path.join(tempfile.gettempdir(), "pandas_ex17_hist4.png")
fig.savefig(path4, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path4}")
print()

# ---------------------------------------------------------------------------
# Example 5: KDE plot (density estimate)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Density Plot (KDE)")
print("=" * 60)

fig, ax = plt.subplots(figsize=(8, 5))
df4.groupby("class")["score"].plot.kde(ax=ax, legend=True)
ax.set_title("Score Density by Class")
ax.set_xlabel("Score")
ax.set_ylabel("Density")
ax.grid(True, alpha=0.3)
path5 = os.path.join(tempfile.gettempdir(), "pandas_ex17_hist5.png")
fig.savefig(path5, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path5}")
print()
print("Done!")
