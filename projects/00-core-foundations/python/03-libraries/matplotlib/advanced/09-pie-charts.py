"""
Matplotlib Pie Charts - W3Schools Exercises
=============================================
Pie chart creation and customization.
"""
matplotlib.use('Agg')

import matplotlib
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import os
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Exercise 1: Basic Pie Chart ──────────────────────────────────────────────
def exercise_01():
    """Create a simple pie chart with labels."""
    sizes = [35, 25, 20, 15]
    labels = ["Python", "JavaScript", "Java", "Others"]

    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title("Exercise 1: Basic Pie Chart")
    plt.savefig("../../../outputs/matplotlib/12_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Exploded Pie ─────────────────────────────────────────────────
def exercise_02():
    """Explode one or more slices for emphasis."""
    sizes = [40, 25, 20, 10, 5]
    labels = ["Product A", "Product B", "Product C", "Product D", "Product E"]
    explode = (0.1, 0, 0, 0, 0)  # only explode first slice
    colors = plt.cm.Set3(np.linspace(0, 1, len(sizes)))

    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, explode=explode, colors=colors,
            autopct="%1.1f%%", shadow=True, startangle=90)
    plt.title("Exercise 2: Exploded Pie Chart")
    plt.savefig("../../../outputs/matplotlib/12_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Nested Pie Chart ─────────────────────────────────────────────
def exercise_03():
    """Create a donut chart (pie with a hole)."""
    sizes = [30, 25, 20, 15, 10]
    labels = ["A", "B", "C", "D", "E"]
    colors = plt.cm.Paired(np.linspace(0, 1, len(sizes)))

    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%",
            pctdistance=0.85, startangle=90)
    # Draw a white circle at the center to create donut
    centre_circle = plt.Circle((0, 0), 0.50, fc="white")
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title("Exercise 3: Donut Chart")
    plt.savefig("../../../outputs/matplotlib/12_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Pie Chart with Custom Colors ─────────────────────────────────
def exercise_04():
    """Use hex colors for a branded pie chart."""
    sizes = [45, 30, 15, 10]
    labels = ["Electronics", "Clothing", "Food", "Books"]
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]

    plt.figure(figsize=(7, 7))
    wedges, texts, autotexts = plt.pie(
        sizes, labels=labels, colors=colors, autopct="%1.1f%%",
        startangle=140, textprops={"fontsize": 12}
    )
    for t in autotexts:
        t.set_fontweight("bold")
    plt.title("Exercise 4: Custom Colors Pie", fontsize=14)
    plt.savefig("../../../outputs/matplotlib/12_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Side-by-Side Pie Charts ──────────────────────────────────────
def exercise_05():
    """Compare two pie charts side by side (e.g., year-over-year)."""
    labels = ["Desktop", "Mobile", "Tablet"]
    data_2023 = [45, 40, 15]
    data_2024 = [35, 50, 15]
    colors = ["#3498db", "#e74c3c", "#2ecc71"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    ax1.pie(data_2023, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax1.set_title("2023 Traffic")

    ax2.pie(data_2024, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax2.set_title("2024 Traffic")

    fig.suptitle("Exercise 5: Year-over-Year Comparison", fontsize=14)
    plt.tight_layout()
    plt.savefig("../../../outputs/matplotlib/12_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Pie Chart exercises completed!")
