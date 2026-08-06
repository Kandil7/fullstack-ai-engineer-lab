"""
Matplotlib Grid - W3Schools Exercises
=======================================
Grid line customization and styling.
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


# ── Exercise 1: Basic Grid ───────────────────────────────────────────────────
def exercise_01():
    """Enable a basic grid on a line plot."""
    x = np.linspace(0, 10, 50)
    y = np.sin(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, linewidth=2)
    plt.grid(True)
    plt.title("Exercise 1: Basic Grid")
    plt.xlabel("x")
    plt.ylabel("sin(x)")
    plt.savefig("../../../outputs/matplotlib/07_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Grid Customization ───────────────────────────────────────────
def exercise_02():
    """Customize grid color, linewidth, and alpha."""
    x = np.linspace(0, 2 * np.pi, 100)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x, np.sin(x), "b-", linewidth=2)
    plt.grid(True, color="gray", linestyle="--", linewidth=0.5, alpha=0.5)
    plt.title("Subtle Grid")

    plt.subplot(1, 2, 2)
    plt.plot(x, np.cos(x), "r-", linewidth=2)
    plt.grid(True, color="navy", linestyle="-", linewidth=1, alpha=0.3)
    plt.title("Prominent Grid")

    plt.suptitle("Exercise 2: Grid Customization")
    plt.tight_layout()
    plt.savefig("../../../outputs/matplotlib/07_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Axis-Specific Grid ───────────────────────────────────────────
def exercise_03():
    """Enable grid on only x or y axis."""
    x = np.arange(1, 8)
    y = [20, 35, 30, 35, 27, 30, 32]

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(x, y, marker="o", linewidth=2)
    plt.grid(axis="x", color="lightblue", linestyle="--")
    plt.title("X-axis Grid Only")

    plt.subplot(1, 2, 2)
    plt.plot(x, y, marker="s", linewidth=2, color="orange")
    plt.grid(axis="y", color="lightgreen", linestyle=":")
    plt.title("Y-axis Grid Only")

    plt.suptitle("Exercise 3: Axis-Specific Grid")
    plt.tight_layout()
    plt.savefig("../../../outputs/matplotlib/07_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Major & Minor Grids ──────────────────────────────────────────
def exercise_04():
    """Use both major and minor grid lines."""
    x = np.linspace(0, 10, 200)
    y = np.sin(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, linewidth=2)
    plt.minorticks_on()
    plt.grid(which="major", color="gray", linestyle="-", linewidth=0.8, alpha=0.7)
    plt.grid(which="minor", color="lightgray", linestyle=":", linewidth=0.5, alpha=0.5)
    plt.title("Exercise 4: Major & Minor Grids")
    plt.xlabel("x")
    plt.ylabel("sin(x)")
    plt.savefig("../../../outputs/matplotlib/07_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Grid on Scatter Plot ─────────────────────────────────────────
def exercise_05():
    """Apply grid styling appropriate for scatter plots."""
    np.random.seed(42)
    x = np.random.randn(100)
    y = 0.8 * x + np.random.randn(100) * 0.3

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, alpha=0.6, edgecolors="black", linewidth=0.5)
    plt.axhline(y=0, color="red", linestyle="--", linewidth=0.8, alpha=0.5)
    plt.axvline(x=0, color="red", linestyle="--", linewidth=0.8, alpha=0.5)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.title("Exercise 5: Scatter Plot with Grid")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig("../../../outputs/matplotlib/07_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Grid exercises completed!")
