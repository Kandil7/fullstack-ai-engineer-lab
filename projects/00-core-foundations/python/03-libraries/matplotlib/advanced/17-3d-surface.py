"""
Matplotlib 3D Surface Plots - W3Schools Exercises
====================================================
Advanced 3D surface rendering and visualization.
"""
matplotlib.use('Agg')

import matplotlib
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import os
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Exercise 1: 3D Surface with Plotly-style Colors ──────────────────────────
def exercise_01():
    """Create a vibrant surface plot with a smooth colormap."""
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.cos(X**2 + Y**2)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="coolwarm", edgecolor="none", antialiased=True)
    ax.set_title("Exercise 1: Vibrant Surface Plot")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig("../../../outputs/matplotlib/20_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Surface with Contour Projections ─────────────────────────────
def exercise_02():
    """Add contour projections on all three coordinate planes."""
    x = np.linspace(-3, 3, 80)
    y = np.linspace(-3, 3, 80)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, alpha=0.5, cmap="viridis", edgecolor="none")
    ax.contour(X, Y, Z, zdir="z", offset=-2, cmap="viridis", alpha=0.5)
    ax.contour(X, Y, Z, zdir="x", offset=-4, cmap="viridis", alpha=0.5)
    ax.contour(X, Y, Z, zdir="y", offset=4, cmap="viridis", alpha=0.5)
    ax.set_title("Exercise 2: Surface with Contour Projections")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_zlim(-2, 2)
    plt.savefig("../../../outputs/matplotlib/20_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Monkey Saddle Surface ────────────────────────────────────────
def exercise_03():
    """Visualize the monkey saddle surface z = x³ - 3xy²."""
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = X**3 - 3 * X * Y**2

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="RdBu_r", edgecolor="none",
                           antialiased=True, alpha=0.8)
    fig.colorbar(surf, ax=ax, shrink=0.5, label="Z")
    ax.set_title("Exercise 3: Monkey Saddle (z = x³ - 3xy²)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig("../../../outputs/matplotlib/20_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Surface with View Angles ─────────────────────────────────────
def exercise_04():
    """Show the same surface from multiple viewing angles."""
    x = np.linspace(-3, 3, 60)
    y = np.linspace(-3, 3, 60)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1 * (X**2 + Y**2))

    views = [(30, 45), (30, 135), (60, 225), (10, 315)]
    fig = plt.figure(figsize=(12, 10))

    for i, (elev, azim) in enumerate(views, 1):
        ax = fig.add_subplot(2, 2, i, projection="3d")
        ax.plot_surface(X, Y, Z, cmap="plasma", edgecolor="none", alpha=0.8)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(f"elev={elev}°, azim={azim}°", fontsize=9)

    fig.suptitle("Exercise 4: Same Surface, Different Views", fontsize=13)
    plt.tight_layout()
    plt.savefig("../../../outputs/matplotlib/20_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Surface Plot with Colorbar and Labels ────────────────────────
def exercise_05():
    """Publication-quality surface plot with full labeling."""
    x = np.linspace(-2, 2, 150)
    y = np.linspace(-2, 2, 150)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-X**2 - Y**2) * np.cos(3 * X) * np.sin(3 * Y)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none",
                           antialiased=True, alpha=0.9)
    cbar = fig.colorbar(surf, ax=ax, shrink=0.5, pad=0.1, label="f(x,y)")
    ax.set_title(r"Exercise 5: Publication-Quality Surface ($e^{-r^2}\cos(3x)\sin(3y)$)",
                 fontsize=12, pad=15)
    ax.set_xlabel("X", fontsize=10)
    ax.set_ylabel("Y", fontsize=10)
    ax.set_zlabel("Z", fontsize=10)
    ax.tick_params(labelsize=8)
    plt.savefig("../../../outputs/matplotlib/20_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll 3D Surface exercises completed!")
