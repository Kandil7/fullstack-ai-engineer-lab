"""
Matplotlib Markers - W3Schools Exercises
==========================================
Deep dive into marker customization.
"""
import matplotlib
matplotlib.use('Agg')

import matplotlib
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import os
OUTPUT_DIR = pathlib.Path(os.path.dirname(__file__)) / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Exercise 1: Marker Reference Chart ───────────────────────────────────────
def exercise_01():
    """Create a visual reference chart of all basic marker types."""
    markers = {
        "o": "circle", "s": "square", "^": "triangle_up",
        "v": "triangle_down", "D": "diamond", "P": "plus_filled",
        "*": "star", "X": "x_filled", "p": "pentagon", "h": "hexagon",
    }
    positions = np.arange(len(markers))

    plt.figure(figsize=(12, 6))
    plt.plot(positions, [0] * len(markers), " ")
    for i, (m, name) in enumerate(markers.items()):
        plt.plot(i, 0, marker=m, markersize=20, color="steelblue")
        plt.annotate(name, (i, 0), textcoords="offset points", xytext=(0, -30),
                     ha="center", fontsize=9)
    plt.title("Exercise 1: Marker Reference Chart")
    plt.yticks([])
    plt.xticks([])
    plt.ylim(-1, 1)
    plt.savefig("../../../outputs/matplotlib/04_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Marker Face and Edge Colors ──────────────────────────────────
def exercise_02():
    """Customize markerfacecolor, markeredgecolor, and markeredgewidth."""
    x = np.arange(5)
    y = [1, 3, 2, 5, 4]

    configs = [
        {"mfc": "red", "mec": "black", "mew": 2},
        {"mfc": "yellow", "mec": "green", "mew": 3},
        {"mfc": "cyan", "mec": "purple", "mew": 1},
        {"mfc": "white", "mec": "blue", "mew": 4},
    ]

    plt.figure(figsize=(10, 5))
    for i, cfg in enumerate(configs):
        plt.subplot(1, 4, i + 1)
        plt.plot(x, y, "o", markersize=15, markerfacecolor=cfg["mfc"],
                 markeredgecolor=cfg["mec"], markeredgewidth=cfg["mew"])
        plt.title(f"mfc={cfg['mfc']}\nmec={cfg['mec']}\nmew={cfg['mew']}", fontsize=9)
        plt.ylim(0, 6)
    plt.suptitle("Exercise 2: Marker Face/Edge Colors", fontsize=13)
    plt.tight_layout()
    plt.savefig("../../../outputs/matplotlib/04_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Marker Size Variation ────────────────────────────────────────
def exercise_03():
    """Show how marker size affects visual weight."""
    np.random.seed(10)
    x = np.random.randn(30)
    y = np.random.randn(30)
    sizes = np.random.choice([20, 80, 200, 500], size=30)

    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, s=sizes, c=x + y, cmap="coolwarm", alpha=0.7,
                edgecolors="black", linewidth=0.5)
    plt.colorbar(label="x + y")
    plt.title("Exercise 3: Variable Marker Sizes")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("../../../outputs/matplotlib/04_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Markers Every N Points ───────────────────────────────────────
def exercise_04():
    """Show markers only at every N-th point on a dense line."""
    x = np.linspace(0, 4 * np.pi, 200)
    y = np.sin(x)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(x, y, "o", markersize=2, color="blue")
    plt.title("All points (cluttered)")

    plt.subplot(1, 2, 2)
    plt.plot(x, y, "-", color="blue")
    plt.plot(x[::10], y[::10], "o", color="red", markersize=6, label="every 10th")
    plt.legend()
    plt.title("Line + Sparse Markers")

    plt.suptitle("Exercise 4: Sparse Markers")
    plt.tight_layout()
    plt.savefig("../../../outputs/matplotlib/04_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Custom Marker via Path ───────────────────────────────────────
def exercise_05():
    """Use matplotlib.path for a custom marker shape."""
    from matplotlib.path import Path
    import matplotlib.patches as patches

    verts = [(0, 0), (0.5, 1), (1, 0), (0.5, 0.2), (0, 0)]
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    custom_path = Path(verts, codes)

    fig, ax = plt.subplots(figsize=(8, 6))
    patch = patches.PathPatch(custom_path, facecolor="coral", edgecolor="black", lw=2)
    ax.add_patch(patch)
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_aspect("equal")
    ax.set_title("Exercise 5: Custom Path Marker Shape")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    plt.savefig("../../../outputs/matplotlib/04_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Markers exercises completed!")
