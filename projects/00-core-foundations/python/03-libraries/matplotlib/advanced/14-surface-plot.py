"""
Matplotlib Surface Plots - W3Schools Exercises
================================================
3D surface rendering with shading and colormaps.
"""
matplotlib.use('Agg')

import matplotlib
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import os
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Exercise 1: Basic Surface Plot ───────────────────────────────────────────
def exercise_01():
    """Create a basic 3D surface plot."""
    x = np.linspace(-3, 3, 60)
    y = np.linspace(-3, 3, 60)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
    ax.set_title("Exercise 1: Basic Surface Plot")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig("../../../outputs/matplotlib/17_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Surface with Custom Colormap ─────────────────────────────────
def exercise_02():
    """Use a diverging colormap centered at zero."""
    x = np.linspace(-3, 3, 80)
    y = np.linspace(-3, 3, 80)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y) * 2

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="RdBu_r", edgecolor="none", antialiased=True)
    fig.colorbar(surf, ax=ax, shrink=0.5, label="Z")
    ax.set_title("Exercise 2: Diverging Colormap Surface")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig("../../../outputs/matplotlib/17_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Surface Lighting ─────────────────────────────────────────────
def exercise_03():
    """Apply lighting effects to a surface plot."""
    from matplotlib.colors import LightSource

    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.cos(X) * np.cos(Y) * 2

    ls = LightSource(azdeg=315, altdeg=45)
    rgb = ls.shade(Z, cmap=plt.cm.terrain, blend_mode="soft")

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, facecolors=rgb, edgecolor="none")
    ax.set_title("Exercise 3: Surface with Lighting")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig("../../../outputs/matplotlib/17_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Surface with Wireframe Overlay ───────────────────────────────
def exercise_04():
    """Combine a transparent surface with a wireframe."""
    x = np.linspace(-3, 3, 50)
    y = np.linspace(-3, 3, 50)
    X, Y = np.meshgrid(x, y)
    Z = X**2 * np.exp(-X**2 - Y**2) * 3

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, alpha=0.6, cmap="coolwarm", edgecolor="none")
    ax.plot_wireframe(X, Y, Z, rstride=5, cstride=5, linewidth=0.3, color="black", alpha=0.3)
    ax.set_title("Exercise 4: Surface + Wireframe Overlay")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig("../../../outputs/matplotlib/17_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Multiple Surfaces ────────────────────────────────────────────
def exercise_05():
    """Show two surfaces on the same axes for comparison."""
    x = np.linspace(-3, 3, 50)
    y = np.linspace(-3, 3, 50)
    X, Y = np.meshgrid(x, y)
    Z1 = X**2 + Y**2
    Z2 = 9 - (X**2 + Y**2)
    Z2 = np.clip(Z2, 0, None)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z1, cmap="Reds", alpha=0.6, edgecolor="none")
    ax.plot_surface(X, Y, Z2, cmap="Blues", alpha=0.6, edgecolor="none")
    ax.set_title("Exercise 5: Two Surfaces (Bowl + Dome)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig("../../../outputs/matplotlib/17_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Surface Plot exercises completed!")
