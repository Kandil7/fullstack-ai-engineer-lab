"""
Matplotlib Contour Plots - W3Schools Exercises
================================================
Contour and contourf for 2D scalar fields.
"""
matplotlib.use('Agg')

import matplotlib
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import os
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Exercise 1: Basic Contour Plot ───────────────────────────────────────────
def exercise_01():
    """Create a basic contour plot of a 2D function."""
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))

    plt.figure(figsize=(8, 6))
    plt.contour(X, Y, Z, levels=15, cmap="viridis")
    plt.colorbar(label="Z")
    plt.title("Exercise 1: Basic Contour Plot")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("../../../outputs/matplotlib/15_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Filled Contour (contourf) ────────────────────────────────────
def exercise_02():
    """Use contourf for smooth filled contour visualization."""
    x = np.linspace(-2, 2, 200)
    y = np.linspace(-2, 2, 200)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + Y**2

    plt.figure(figsize=(8, 6))
    cf = plt.contourf(X, Y, Z, levels=20, cmap="hot")
    plt.colorbar(label="X² + Y²")
    plt.title("Exercise 2: Filled Contour (Paraboloid)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("../../../outputs/matplotlib/15_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Contour with Labels ──────────────────────────────────────────
def exercise_03():
    """Add contour line labels (inline annotations)."""
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 + Y**2)) * np.cos(2 * X)

    plt.figure(figsize=(8, 6))
    cs = plt.contour(X, Y, Z, levels=10, colors="black", linewidths=0.8)
    plt.clabel(cs, inline=True, fontsize=8)
    plt.title("Exercise 3: Contour with Labels")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("../../../outputs/matplotlib/15_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Mountain Terrain Contour ─────────────────────────────────────
def exercise_04():
    """Simulate terrain with multiple peaks and contour it."""
    np.random.seed(42)
    x = np.linspace(0, 10, 200)
    y = np.linspace(0, 10, 200)
    X, Y = np.meshgrid(x, y)

    # Generate terrain with peaks
    Z = (5 * np.exp(-((X - 3)**2 + (Y - 7)**2) / 2)
         + 8 * np.exp(-((X - 7)**2 + (Y - 3)**2) / 1.5)
         + 3 * np.exp(-((X - 5)**2 + (Y - 5)**2) / 3))

    plt.figure(figsize=(8, 8))
    cf = plt.contourf(X, Y, Z, levels=20, cmap="terrain")
    plt.contour(X, Y, Z, levels=20, colors="black", linewidths=0.3, alpha=0.5)
    plt.colorbar(label="Elevation")
    plt.title("Exercise 4: Terrain Contour Map")
    plt.xlabel("X (km)")
    plt.ylabel("Y (km)")
    plt.savefig("../../../outputs/matplotlib/15_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Contour + Scatter Overlay ────────────────────────────────────
def exercise_05():
    """Overlay a scatter plot on a contour plot for combined visualization."""
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y)

    plt.figure(figsize=(8, 6))
    plt.contourf(X, Y, Z, levels=20, cmap="RdYlBu", alpha=0.7)
    plt.colorbar(label="Z")

    np.random.seed(42)
    scatter_x = np.random.uniform(-3, 3, 50)
    scatter_y = np.random.uniform(-3, 3, 50)
    plt.scatter(scatter_x, scatter_y, color="black", s=20, zorder=5, label="Sample Points")
    plt.legend()
    plt.title("Exercise 5: Contour + Scatter Overlay")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("../../../outputs/matplotlib/15_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Contour Plot exercises completed!")
