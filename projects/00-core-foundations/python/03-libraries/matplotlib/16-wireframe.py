"""
Matplotlib Wireframe Plots - W3Schools Exercises
==================================================
3D wireframe surface visualization.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Exercise 1: Basic Wireframe ──────────────────────────────────────────────
def exercise_01():
    """Create a simple wireframe plot of a paraboloid."""
    x = np.linspace(-3, 3, 30)
    y = np.linspace(-3, 3, 30)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + Y**2

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_wireframe(X, Y, Z, rstride=3, cstride=3, linewidth=0.8)
    ax.set_title("Exercise 1: Basic Wireframe (z = x² + y²)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig(os.path.join(OUTPUT_DIR, "16_exercise_01.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Wireframe with Custom Stride ─────────────────────────────────
def exercise_02():
    """Compare different stride values for wireframe density."""
    x = np.linspace(-3, 3, 50)
    y = np.linspace(-3, 3, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))

    strides = [(2, 2), (5, 5), (10, 10)]
    fig = plt.figure(figsize=(15, 4))

    for i, (rs, cs) in enumerate(strides, 1):
        ax = fig.add_subplot(1, 3, i, projection="3d")
        ax.plot_wireframe(X, Y, Z, rstride=rs, cstride=cs, linewidth=0.6, color="steelblue")
        ax.set_title(f"rstride={rs}, cstride={cs}")

    fig.suptitle("Exercise 2: Wireframe Density Comparison", fontsize=13)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "16_exercise_02.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Wireframe Color Mapping ──────────────────────────────────────
def exercise_03():
    """Color a surface by height using a colormap with a colorbar."""
    x = np.linspace(-2, 2, 40)
    y = np.linspace(-2, 2, 40)
    X, Y = np.meshgrid(x, y)
    Z = np.cos(X) * np.sin(Y) * 3

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    # A wireframe has no scalar array for a colorbar, so use a surface plot
    surf = ax.plot_surface(X, Y, Z, cmap="coolwarm")
    fig.colorbar(surf, ax=ax, shrink=0.5, label="Z value")
    ax.set_title("Exercise 3: Color-Mapped Surface")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig(os.path.join(OUTPUT_DIR, "16_exercise_03.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Saddle Point Wireframe ───────────────────────────────────────
def exercise_04():
    """Visualize a saddle surface (hyperbolic paraboloid)."""
    x = np.linspace(-3, 3, 40)
    y = np.linspace(-3, 3, 40)
    X, Y = np.meshgrid(x, y)
    Z = X**2 - Y**2

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_wireframe(X, Y, Z, rstride=4, cstride=4, linewidth=0.8, color="darkgreen")
    ax.set_title("Exercise 4: Saddle Surface (z = x² - y²)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=25, azim=135)
    plt.savefig(os.path.join(OUTPUT_DIR, "16_exercise_04.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Wireframe with Projected Contour ─────────────────────────────
def exercise_05():
    """Combine wireframe with a contour projection on the base plane."""
    x = np.linspace(-3, 3, 40)
    y = np.linspace(-3, 3, 40)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 + Y**2)) * 5

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_wireframe(X, Y, Z, rstride=3, cstride=3, linewidth=0.7, alpha=0.8, color="blue")
    ax.contour(X, Y, Z, zdir="z", offset=ax.get_zlim()[0], cmap="viridis", alpha=0.6)
    ax.set_title("Exercise 5: Wireframe + Base Contour")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig(os.path.join(OUTPUT_DIR, "16_exercise_05.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Wireframe exercises completed!")
