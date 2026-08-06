"""
Matplotlib Labels - W3Schools Exercises
=========================================
Title, xlabel, ylabel, and text customization.
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


# ── Exercise 1: Basic Labels ─────────────────────────────────────────────────
def exercise_01():
    """Add title and axis labels to a plot."""
    x = [1, 2, 3, 4, 5]
    y = [10, 24, 36, 40, 55]

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker="o", linewidth=2)
    plt.title("Student Exam Scores")
    plt.xlabel("Exam Number")
    plt.ylabel("Score")
    plt.savefig(OUTPUT_DIR / "06_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Font Size & Style ────────────────────────────────────────────
def exercise_02():
    """Customize font sizes and styles for all text elements."""
    x = np.linspace(0, 10, 50)
    y = np.sin(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, linewidth=2)

    plt.title("Exercise 2: Font Customization", fontsize=18, fontweight="bold", color="navy")
    plt.xlabel("Time (s)", fontsize=14, fontstyle="italic")
    plt.ylabel("Amplitude", fontsize=14, fontfamily="serif")
    plt.tick_params(axis="both", labelsize=11)
    plt.savefig(OUTPUT_DIR / "06_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Grid Labels on a Bar Chart ───────────────────────────────────
def exercise_03():
    """Labels on a bar chart with proper spacing."""
    fruits = ["Apples", "Bananas", "Cherries", "Dates", "Elderberries"]
    counts = [25, 40, 30, 55, 20]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(fruits, counts, color=["#e74c3c", "#f1c40f", "#e91e63",
                                           "#8d6e63", "#7e57c2"])
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 str(count), ha="center", fontweight="bold")
    plt.title("Fruit Inventory")
    plt.xlabel("Fruit Type")
    plt.ylabel("Count")
    plt.savefig(OUTPUT_DIR / "06_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Mathematical Notation in Labels ──────────────────────────────
def exercise_04():
    """Use LaTeX-style formatting in titles and labels."""
    x = np.linspace(-2, 2, 200)

    plt.figure(figsize=(10, 5))
    plt.plot(x, np.exp(-x**2), label=r"$e^{-x^2}$", linewidth=2)
    plt.plot(x, 1 / (1 + x**2), label=r"$\frac{1}{1+x^2}$", linewidth=2, linestyle="--")
    plt.legend(fontsize=14)
    plt.title(r"Exercise 4: LaTeX Labels ($\sigma = 1$)", fontsize=14)
    plt.xlabel(r"$x$", fontsize=12)
    plt.ylabel(r"$f(x)$", fontsize=12)
    plt.savefig(OUTPUT_DIR / "06_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Multi-line Title with Text Box ───────────────────────────────
def exercise_05():
    """Create a multi-line title and use figtext for footnotes."""
    x = np.arange(1, 7)
    y1 = [20, 35, 30, 35, 27, 30]
    y2 = [25, 32, 34, 38, 31, 35]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y1, marker="o", label="Team A")
    ax.plot(x, y2, marker="s", label="Team B")

    ax.set_title("Quarterly Performance\nTeam A vs Team B", fontsize=14)
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Units Sold")
    ax.legend()

    fig.text(0.5, 0.01, "Source: Internal Report Q1-Q2 2024", ha="center",
             fontsize=9, fontstyle="italic", color="gray")
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(OUTPUT_DIR / "06_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Labels exercises completed!")
