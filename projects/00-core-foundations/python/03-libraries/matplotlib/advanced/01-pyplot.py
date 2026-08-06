"""
Matplotlib Pyplot Module - W3Schools Exercises
===============================================
Understanding the pyplot module for quick plotting.
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


# ── Exercise 1: pyplot.plot() Basics ─────────────────────────────────────────
def exercise_01():
    """Use pyplot to draw a simple line from points."""
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    plt.figure(figsize=(8, 5))
    plt.plot(x, y)
    plt.title("Exercise 1: pyplot.plot()")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig("../../../outputs/matplotlib/02_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Markers with pyplot ──────────────────────────────────────────
def exercise_02():
    """Use markers to highlight data points."""
    x = np.arange(1, 8)
    y = [3, 1, 4, 1, 5, 9, 2]

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker="o", markersize=10, markerfacecolor="red",
             markeredgecolor="black", markeredgewidth=2)
    plt.title("Exercise 2: Markers")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.savefig("../../../outputs/matplotlib/02_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Linestyle & Color Shortcuts ──────────────────────────────────
def exercise_03():
    """Use shorthand notation for color, marker, and linestyle."""
    x = np.linspace(0, 10, 50)

    plt.figure(figsize=(8, 5))
    plt.plot(x, np.sin(x), "r-", label="r- (red solid)")
    plt.plot(x, np.cos(x), "g--", label="g-- (green dashed)")
    plt.plot(x, np.tan(x) / 5, "b:", label="b: (blue dotted)")
    plt.ylim(-2, 2)
    plt.legend()
    plt.title("Exercise 3: Shorthand Notation")
    plt.savefig("../../../outputs/matplotlib/02_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: plt.xlabel, plt.ylabel, plt.title ────────────────────────────
def exercise_04():
    """Set labels and title using pyplot functions."""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    sales = [150, 200, 180, 220, 250, 300]

    plt.figure(figsize=(8, 5))
    plt.plot(months, sales, marker="s", color="purple", linewidth=2)
    plt.title("Monthly Sales", fontsize=16, fontweight="bold")
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Revenue ($)", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.savefig("../../../outputs/matplotlib/02_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: plt.subplot() Quick Layout ───────────────────────────────────
def exercise_05():
    """Use plt.subplot() for a 2x2 grid of plots."""
    x = np.linspace(0, 2 * np.pi, 100)

    plt.figure(figsize=(10, 8))

    plt.subplot(2, 2, 1)
    plt.plot(x, np.sin(x), "r")
    plt.title("Sin")

    plt.subplot(2, 2, 2)
    plt.plot(x, np.cos(x), "g")
    plt.title("Cos")

    plt.subplot(2, 2, 3)
    plt.plot(x, np.tan(x), "b")
    plt.ylim(-5, 5)
    plt.title("Tan")

    plt.subplot(2, 2, 4)
    plt.plot(x, np.abs(np.sin(x)), "m")
    plt.title("|Sin|")

    plt.suptitle("Exercise 5: plt.subplot()", fontsize=14)
    plt.tight_layout()
    plt.savefig("../../../outputs/matplotlib/02_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Pyplot exercises completed!")
