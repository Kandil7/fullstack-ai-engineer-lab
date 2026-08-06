"""
Correlation
W3Schools: https://www.w3schools.com/python/pandas_dataframe_corr.asp

Correlation measures the linear relationship between two variables.
Values range from -1 (perfect negative) to +1 (perfect positive).
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import tempfile

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

np.random.seed(42)
n = 200

# Create correlated data
study_hours = np.random.uniform(1, 10, n)
exam_score = 40 + 5 * study_hours + np.random.normal(0, 8, n)
sleep_hours = np.random.uniform(4, 9, n)
gpa = 1.0 + 0.3 * study_hours - 0.1 * sleep_hours + np.random.normal(0, 0.5, n)

df = pd.DataFrame({
    "study_hours": study_hours.round(1),
    "exam_score": exam_score.round(1),
    "sleep_hours": sleep_hours.round(1),
    "gpa": gpa.round(2),
    "age": np.random.randint(18, 25, n),
})

print("Sample data (first 5 rows):")
print(df.head())
print()

# ---------------------------------------------------------------------------
# Example 1: Correlation matrix
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Correlation Matrix")
print("=" * 60)

corr = df.corr().round(3)
print("Full correlation matrix:")
print(corr)
print()

# ---------------------------------------------------------------------------
# Example 2: Pairwise correlation
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Pairwise Correlation")
print("=" * 60)

print("exam_score correlations:")
exam_corr = df.corr()["exam_score"].drop("exam_score").sort_values(ascending=False)
print(exam_corr.round(3))
print()

print("Strongest positive correlation: study_hours + exam_score =", 
      df["study_hours"].corr(df["exam_score"]).round(3))
print("Weakest correlation: age + exam_score =",
      df["age"].corr(df["exam_score"]).round(3))
print()

# ---------------------------------------------------------------------------
# Example 3: Correlation heatmap
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Correlation Heatmap")
print("=" * 60)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=45, ha="right")
ax.set_yticklabels(corr.columns)

# Add text annotations
for i in range(len(corr)):
    for j in range(len(corr)):
        color = "white" if abs(corr.values[i, j]) > 0.5 else "black"
        ax.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center", color=color, fontsize=10)

plt.colorbar(im, label="Correlation Coefficient")
ax.set_title("Correlation Heatmap")
plt.tight_layout()
path3 = os.path.join(tempfile.gettempdir(), "pandas_ex23_heatmap.png")
fig.savefig(path3, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path3}")
print()

# ---------------------------------------------------------------------------
# Example 4: Scatter matrix
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Scatter Matrix")
print("=" * 60)

from pandas.plotting import scatter_matrix

fig, axes = plt.subplots(1, 1, figsize=(10, 8))
scatter_matrix(df[["study_hours", "exam_score", "sleep_hours", "gpa"]],
               alpha=0.4, ax=axes, diagonal="hist", color="steelblue")
plt.suptitle("Scatter Matrix", y=1.02, fontsize=14)
plt.tight_layout()
path4 = os.path.join(tempfile.gettempdir(), "pandas_ex23_scatter_matrix.png")
fig.savefig(path4, dpi=100, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path4}")
print()

# ---------------------------------------------------------------------------
# Example 5: Different correlation methods
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Different Correlation Methods")
print("=" * 60)

print("Pearson (default – linear):")
print(df[["study_hours", "exam_score"]].corr(method="pearson").round(3))
print()

print("Spearman (rank-based – monotonic):")
print(df[["study_hours", "exam_score"]].corr(method="spearman").round(3))
print()

print("Kendall (concordant/discordant pairs):")
print(df[["study_hours", "exam_score"]].corr(method="kendall").round(3))
print()

# Demonstrate with non-linear data
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x) + np.random.normal(0, 0.1, 100)
df_nonlinear = pd.DataFrame({"x": x, "y": y})

print("Non-linear data (sin wave):")
print(f"  Pearson:  {df_nonlinear.corr(method='pearson').iloc[0,1]:.3f}")
print(f"  Spearman: {df_nonlinear.corr(method='spearman').iloc[0,1]:.3f}")
print()

print("Done!")
