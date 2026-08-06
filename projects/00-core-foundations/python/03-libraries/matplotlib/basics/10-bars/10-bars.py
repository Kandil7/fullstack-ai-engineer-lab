"""
Matplotlib Bar Charts - W3Schools Exercises
=============================================
Bar chart creation and customization.
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


# ── Exercise 1: Basic Bar Chart ──────────────────────────────────────────────
def exercise_01():
    """Create a simple vertical bar chart."""
    categories = ["A", "B", "C", "D", "E"]
    values = [23, 45, 56, 78, 32]

    plt.figure(figsize=(8, 5))
    plt.bar(categories, values, color="steelblue")
    plt.title("Exercise 1: Basic Bar Chart")
    plt.xlabel("Category")
    plt.ylabel("Value")
    plt.savefig(OUTPUT_DIR / "10_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Horizontal Bar Chart ─────────────────────────────────────────
def exercise_02():
    """Create a horizontal bar chart (barh) for ranked data."""
    languages = ["Python", "JavaScript", "Java", "C#", "TypeScript", "Go"]
    popularity = [28.1, 18.2, 15.5, 8.3, 7.5, 6.8]

    plt.figure(figsize=(8, 5))
    plt.barh(languages, popularity, color=plt.cm.viridis(np.linspace(0.2, 0.8, len(languages))))
    plt.title("Exercise 2: Horizontal Bar Chart")
    plt.xlabel("Popularity (%)")
    for i, v in enumerate(popularity):
        plt.text(v + 0.3, i, f"{v}%", va="center")
    plt.savefig(OUTPUT_DIR / "10_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Grouped Bar Chart ────────────────────────────────────────────
def exercise_03():
    """Side-by-side grouped bars for comparing series."""
    categories = ["Q1", "Q2", "Q3", "Q4"]
    product_a = [20, 35, 30, 35]
    product_b = [25, 32, 34, 20]
    x = np.arange(len(categories))
    width = 0.35

    plt.figure(figsize=(8, 5))
    plt.bar(x - width / 2, product_a, width, label="Product A", color="#3498db")
    plt.bar(x + width / 2, product_b, width, label="Product B", color="#e74c3c")
    plt.xticks(x, categories)
    plt.title("Exercise 3: Grouped Bar Chart")
    plt.ylabel("Sales")
    plt.legend()
    plt.savefig(OUTPUT_DIR / "10_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Stacked Bar Chart ────────────────────────────────────────────
def exercise_04():
    """Stack bars to show composition across categories."""
    categories = ["Jan", "Feb", "Mar", "Apr", "May"]
    online = [40, 45, 50, 55, 60]
    in_store = [60, 55, 50, 45, 40]

    plt.figure(figsize=(8, 5))
    plt.bar(categories, online, label="Online", color="#2ecc71")
    plt.bar(categories, in_store, bottom=online, label="In-Store", color="#e67e22")
    plt.title("Exercise 4: Stacked Bar Chart")
    plt.ylabel("Revenue ($)")
    plt.legend()
    plt.savefig(OUTPUT_DIR / "10_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Bar Chart with Error Bars ────────────────────────────────────
def exercise_05():
    """Add error bars to represent standard deviation."""
    methods = ["Method A", "Method B", "Method C", "Method D"]
    means = [78, 85, 72, 90]
    stds = [5, 8, 6, 4]
    colors = ["#3498db", "#2ecc71", "#e74c3c", "#9b59b6"]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(methods, means, color=colors, edgecolor="black", linewidth=0.8)
    plt.errorbar(methods, means, yerr=stds, fmt="none", ecolor="black", capsize=5, linewidth=2)

    for bar, mean in zip(bars, means):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 f"{mean}%", ha="center", fontweight="bold")

    plt.title("Exercise 5: Bar Chart with Error Bars")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0, 100)
    plt.savefig(OUTPUT_DIR / "10_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Bar Chart exercises completed!")
