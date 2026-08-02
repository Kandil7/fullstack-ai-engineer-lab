"""
Matplotlib Box Plots - W3Schools Exercises
============================================
Box plot creation for statistical data visualization.
"""
matplotlib.use('Agg')

import matplotlib
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import os
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Exercise 1: Basic Box Plot ───────────────────────────────────────────────
def exercise_01():
    """Create a simple box plot from random data."""
    np.random.seed(42)
    data = [np.random.normal(50, 10, 100) for _ in range(4)]

    plt.figure(figsize=(8, 5))
    plt.boxplot(data, tick_labels=["A", "B", "C", "D"])
    plt.title("Exercise 1: Basic Box Plot")
    plt.ylabel("Value")
    plt.savefig(OUTPUT_DIR / "13_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Horizontal Box Plot ──────────────────────────────────────────
def exercise_02():
    """Create horizontal box plots for better label readability."""
    np.random.seed(42)
    categories = ["Control", "Low Dose", "Medium Dose", "High Dose"]
    data = [np.random.normal(50 + i * 8, 10 + i * 2, 80) for i in range(4)]

    plt.figure(figsize=(8, 5))
    plt.boxplot(data, tick_labels=categories, orientation="horizontal", patch_artist=True,
                boxprops=dict(facecolor="lightblue"))
    plt.title("Exercise 2: Horizontal Box Plot")
    plt.xlabel("Response")
    plt.savefig(OUTPUT_DIR / "13_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Box Plot with Custom Colors ──────────────────────────────────
def exercise_03():
    """Customize box colors, whisker caps, and median styles."""
    np.random.seed(42)
    data = [np.random.normal(i, 1, 100) for i in range(5)]
    labels = ["μ=0", "μ=1", "μ=2", "μ=3", "μ=4"]
    colors = plt.cm.Pastel1(np.linspace(0, 1, 5))

    plt.figure(figsize=(8, 5))
    bp = plt.boxplot(data, tick_labels=labels, patch_artist=True, notch=True)

    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
    for median in bp["medians"]:
        median.set_color("red")
        median.set_linewidth(2)
    for whisker in bp["whiskers"]:
        whisker.set_linestyle("--")
    for cap in bp["caps"]:
        cap.set_linewidth(2)

    plt.title("Exercise 3: Custom Colored Box Plot")
    plt.ylabel("Value")
    plt.savefig(OUTPUT_DIR / "13_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Box Plot vs Violin Plot ──────────────────────────────────────
def exercise_04():
    """Compare box plots with violin plots side by side."""
    np.random.seed(42)
    data = [np.random.normal(50 + i * 5, 8, 100) for i in range(4)]
    labels = ["Group 1", "Group 2", "Group 3", "Group 4"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    bp = ax1.boxplot(data, tick_labels=labels, patch_artist=True)
    colors = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
    ax1.set_title("Box Plot")

    parts = ax2.violinplot(data, showmeans=True, showmedians=True)
    for pc in parts["bodies"]:
        pc.set_facecolor("lightblue")
        pc.set_alpha(0.7)
    ax2.set_xticks(range(1, len(labels) + 1))
    ax2.set_xticklabels(labels)
    ax2.set_title("Violin Plot")

    fig.suptitle("Exercise 4: Box vs Violin", fontsize=14)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "13_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Box Plot with Outlier Detection ──────────────────────────────
def exercise_05():
    """Show box plot with visible outliers and flier markers."""
    np.random.seed(42)
    data = np.random.normal(50, 10, 100)
    # Inject outliers
    outliers = np.array([10, 15, 85, 90, 95])
    full_data = np.concatenate([data, outliers])

    plt.figure(figsize=(8, 5))
    bp = plt.boxplot([full_data], tick_labels=["Data"], patch_artist=True,
                     flierprops=dict(marker="D", markerfacecolor="red", markersize=8))
    bp["boxes"][0].set_facecolor("lightyellow")
    plt.title("Exercise 5: Box Plot with Outliers")
    plt.ylabel("Value")
    plt.text(1.15, 95, "← Outliers", color="red", fontsize=10)
    plt.savefig(OUTPUT_DIR / "13_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Box Plot exercises completed!")
