"""
Matplotlib Area Plots - W3Schools Exercises
=============================================
Area (filled line) chart creation and stacked areas.
"""
matplotlib.use('Agg')

import matplotlib
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import os
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Exercise 1: Basic Area Plot ──────────────────────────────────────────────
def exercise_01():
    """Create a simple filled area plot."""
    x = np.arange(1, 11)
    y = [15, 25, 35, 30, 40, 55, 50, 60, 55, 70]

    plt.figure(figsize=(8, 5))
    plt.fill_between(x, y, alpha=0.4, color="steelblue")
    plt.plot(x, y, color="navy", linewidth=2)
    plt.title("Exercise 1: Basic Area Plot")
    plt.xlabel("Month")
    plt.ylabel("Revenue ($)")
    plt.savefig("../../../outputs/matplotlib/14_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Stacked Area Plot ────────────────────────────────────────────
def exercise_02():
    """Create a stacked area plot showing composition over time."""
    months = np.arange(1, 7)
    labels = ["Product A", "Product B", "Product C"]
    data = np.array([
        [20, 25, 30, 35, 40, 45],
        [15, 20, 18, 22, 25, 28],
        [10, 12, 15, 18, 20, 22],
    ])
    colors = ["#3498db", "#e74c3c", "#2ecc71"]

    plt.figure(figsize=(8, 5))
    plt.stackplot(months, *data, labels=labels, colors=colors, alpha=0.7)
    plt.legend(loc="upper left")
    plt.title("Exercise 2: Stacked Area Plot")
    plt.xlabel("Month")
    plt.ylabel("Units Sold")
    plt.savefig("../../../outputs/matplotlib/14_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Area Between Two Curves ──────────────────────────────────────
def exercise_03():
    """Fill the area between two curves to show difference/interval."""
    x = np.linspace(0, 2 * np.pi, 100)
    upper = np.sin(x) + 0.5
    lower = np.sin(x) - 0.5

    plt.figure(figsize=(8, 5))
    plt.plot(x, np.sin(x), color="blue", linewidth=2, label="sin(x)")
    plt.fill_between(x, lower, upper, alpha=0.3, color="blue", label="±0.5 band")
    plt.legend()
    plt.title("Exercise 3: Confidence Band (fill_between)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig("../../../outputs/matplotlib/14_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Conditional Fill ─────────────────────────────────────────────
def exercise_04():
    """Use fill_between with where parameter to color above/below zero."""
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, color="black", linewidth=2)
    plt.fill_between(x, y, 0, where=(y >= 0), color="green", alpha=0.4, label="Positive")
    plt.fill_between(x, y, 0, where=(y < 0), color="red", alpha=0.4, label="Negative")
    plt.axhline(y=0, color="gray", linestyle="--", linewidth=0.8)
    plt.legend()
    plt.title("Exercise 4: Conditional Fill")
    plt.xlabel("x")
    plt.ylabel("sin(x)")
    plt.savefig("../../../outputs/matplotlib/14_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Streamgraph-Style ────────────────────────────────────────────
def exercise_05():
    """Create a baseline-shifted stacked area (streamgraph style)."""
    np.random.seed(42)
    n_points = 50
    x = np.arange(n_points)
    n_series = 5
    raw = np.random.rand(n_points, n_series) * 10

    # Smooth the data
    from scipy.ndimage import uniform_filter1d
    smoothed = uniform_filter1d(raw, size=5, axis=0)

    plt.figure(figsize=(10, 6))
    colors = plt.cm.tab10(np.linspace(0, 1, n_series))
    plt.stackplot(x, *smoothed.T, colors=colors, alpha=0.8,
                  labels=[f"Series {i+1}" for i in range(n_series)])
    plt.legend(loc="upper left", ncol=2)
    plt.title("Exercise 5: Streamgraph-Style Area Plot")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.savefig("../../../outputs/matplotlib/14_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Area Plot exercises completed!")
