"""
Scatter Plot
W3Schools: https://www.w3schools.com/python/pandas_plotting_scatter.asp

Scatter plots show the relationship between two numerical variables.
Pandas has built-in plotting via matplotlib.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import os
import tempfile

# ---------------------------------------------------------------------------
# Example 1: Basic scatter plot
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Basic Scatter Plot")
print("=" * 60)

np.random.seed(42)
n = 50
df = pd.DataFrame({
    "height": np.random.normal(170, 10, n),
    "weight": np.random.normal(70, 12, n),
})

print("Data (first 5 rows):")
print(df.head())
print()

fig, ax = plt.subplots(figsize=(8, 5))
df.plot.scatter(x="height", y="weight", ax=ax, alpha=0.7, color="steelblue")
ax.set_title("Height vs Weight")
ax.set_xlabel("Height (cm)")
ax.set_ylabel("Weight (kg)")
ax.grid(True, alpha=0.3)
path1 = os.path.join(tempfile.gettempdir(), "pandas_ex16_scatter1.png")
fig.savefig(path1, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path1}")
print()

# ---------------------------------------------------------------------------
# Example 2: Scatter with color and size
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Scatter with Color and Size")
print("=" * 60)

n = 100
df2 = pd.DataFrame({
    "x": np.random.uniform(0, 10, n),
    "y": np.random.uniform(0, 10, n),
    "size": np.random.randint(10, 200, n),
    "category": np.random.choice(["A", "B", "C"], n),
})

print("Data (first 5 rows):")
print(df2.head())
print()

fig, ax = plt.subplots(figsize=(8, 5))
colors = {"A": "red", "B": "green", "C": "blue"}
for cat, group in df2.groupby("category"):
    ax.scatter(
        group["x"], group["y"],
        s=group["size"],
        alpha=0.5,
        label=cat,
        color=colors[cat],
    )
ax.set_title("Scatter with Varying Size and Color")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend()
ax.grid(True, alpha=0.3)
path2 = os.path.join(tempfile.gettempdir(), "pandas_ex16_scatter2.png")
fig.savefig(path2, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path2}")
print()

# ---------------------------------------------------------------------------
# Example 3: Scatter with trend line
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Scatter with Trend Line")
print("=" * 60)

np.random.seed(0)
x = np.linspace(0, 10, 80)
y = 2.5 * x + np.random.normal(0, 3, 80)

df3 = pd.DataFrame({"x": x, "y": y})
print("Correlation:", df3["x"].corr(df3["y"]).round(3))
print()

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df3["x"], df3["y"], alpha=0.6, color="steelblue", label="Data")

# Trend line
z = np.polyfit(df3["x"], df3["y"], 1)
p = np.poly1d(z)
ax.plot(df3["x"], p(df3["x"]), "r--", linewidth=2, label=f"Trend: y={z[0]:.2f}x+{z[1]:.2f}")

ax.set_title("Scatter with Linear Trend Line")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend()
ax.grid(True, alpha=0.3)
path3 = os.path.join(tempfile.gettempdir(), "pandas_ex16_scatter3.png")
fig.savefig(path3, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path3}")
print()

# ---------------------------------------------------------------------------
# Example 4: Pandas built-in scatter plot
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Pandas .plot.scatter()")
print("=" * 60)

df4 = pd.DataFrame({
    "GDP_per_capita": [45000, 55000, 38000, 62000, 35000, 48000, 52000],
    "Life_Expectancy": [78, 81, 74, 83, 72, 79, 80],
    "Population": [330, 67, 83, 126, 1400, 230, 67],
    "Country": ["USA", "UK", "France", "Japan", "India", "Brazil", "Germany"],
})

fig, ax = plt.subplots(figsize=(8, 5))
df4.plot.scatter(
    x="GDP_per_capita",
    y="Life_Expectancy",
    s=df4["Population"] / 10,  # Scale population for marker size
    alpha=0.7,
    color="darkblue",
    ax=ax,
)
for _, row in df4.iterrows():
    ax.annotate(
        row["Country"],
        (row["GDP_per_capita"], row["Life_Expectancy"]),
        fontsize=8, ha="center", va="bottom",
    )
ax.set_title("GDP per Capita vs Life Expectancy")
ax.set_xlabel("GDP per Capita ($)")
ax.set_ylabel("Life Expectancy (years)")
ax.grid(True, alpha=0.3)
path4 = os.path.join(tempfile.gettempdir(), "pandas_ex16_scatter4.png")
fig.savefig(path4, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path4}")
print()
print("Done!")
