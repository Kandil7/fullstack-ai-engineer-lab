"""
Matplotlib 3D Scatter Plots - W3Schools Exercises
====================================================
3D scatter visualization and point cloud techniques.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Exercise 1: Basic 3D Scatter ─────────────────────────────────────────────
def exercise_01():
    """Create a simple 3D scatter plot."""
    np.random.seed(42)
    n = 100
    x = np.random.randn(n)
    y = np.random.randn(n)
    z = np.random.randn(n)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x, y, z, s=40, c="steelblue", alpha=0.7)
    ax.set_title("Exercise 1: Basic 3D Scatter")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig(os.path.join(OUTPUT_DIR, "18_exercise_01.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Color-Mapped 3D Scatter ──────────────────────────────────────
def exercise_02():
    """Use color to represent a 4th dimension in 3D scatter."""
    np.random.seed(42)
    n = 200
    x = np.random.randn(n) * 2
    y = np.random.randn(n) * 2
    z = np.sin(x) + np.cos(y)
    colors = x**2 + y**2

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    sc = ax.scatter(x, y, z, c=colors, cmap="plasma", s=30, alpha=0.8)
    fig.colorbar(sc, ax=ax, shrink=0.5, label="x² + y²")
    ax.set_title("Exercise 2: Color-Mapped 3D Scatter")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig(os.path.join(OUTPUT_DIR, "18_exercise_02.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: 3D Scatter Clusters ──────────────────────────────────────────
def exercise_03():
    """Visualize distinct clusters in 3D space."""
    np.random.seed(42)
    centers = [(2, 2, 2), (-2, -2, 2), (2, -2, -2), (-2, 2, -2)]
    labels_true = []
    all_x, all_y, all_z = [], [], []

    for i, (cx, cy, cz) in enumerate(centers):
        n = 50
        all_x.extend(np.random.randn(n) * 0.5 + cx)
        all_y.extend(np.random.randn(n) * 0.5 + cy)
        all_z.extend(np.random.randn(n) * 0.5 + cz)
        labels_true.extend([i] * n)

    colors = plt.cm.Set1(np.linspace(0, 1, len(centers)))

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    for i in range(len(centers)):
        mask = np.array(labels_true) == i
        ax.scatter(np.array(all_x)[mask], np.array(all_y)[mask],
                   np.array(all_z)[mask], s=30, alpha=0.7, label=f"Cluster {i+1}",
                   color=colors[i])
    ax.legend()
    ax.set_title("Exercise 3: 3D Cluster Visualization")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig(os.path.join(OUTPUT_DIR, "18_exercise_03.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: 3D Scatter on Surface ────────────────────────────────────────
def exercise_04():
    """Plot 3D scatter points sampled from a surface."""
    np.random.seed(42)
    n = 300
    x = np.random.uniform(-3, 3, n)
    y = np.random.uniform(-3, 3, n)
    z = np.sin(np.sqrt(x**2 + y**2)) + np.random.randn(n) * 0.1

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x, y, z, c=z, cmap="viridis", s=25, alpha=0.7)
    ax.set_title("Exercise 4: Points Sampled from Surface")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig(os.path.join(OUTPUT_DIR, "18_exercise_04.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: 3D Scatter with Size Variation ───────────────────────────────
def exercise_05():
    """Vary marker size in 3D to encode another dimension."""
    np.random.seed(42)
    n = 150
    x = np.random.randn(n)
    y = np.random.randn(n)
    z = x * y
    sizes = np.abs(z) * 100 + 10

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    sc = ax.scatter(x, y, z, s=sizes, c=z, cmap="RdYlGn", alpha=0.6, edgecolors="gray",
                    linewidth=0.3)
    fig.colorbar(sc, ax=ax, shrink=0.5, label="z = x·y")
    ax.set_title("Exercise 5: Variable Size 3D Scatter")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig(os.path.join(OUTPUT_DIR, "18_exercise_05.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll 3D Scatter exercises completed!")
