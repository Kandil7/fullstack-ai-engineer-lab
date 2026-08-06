"""
Matplotlib Histograms - W3Schools Exercises
=============================================
Histogram creation and distribution visualization.
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


# ── Exercise 1: Basic Histogram ──────────────────────────────────────────────
def exercise_01():
    """Create a simple histogram of normally distributed data."""
    np.random.seed(42)
    data = np.random.randn(1000)

    plt.figure(figsize=(8, 5))
    plt.hist(data, bins=30, color="steelblue", edgecolor="black")
    plt.title("Exercise 1: Basic Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.savefig("../../../outputs/matplotlib/11_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Normalized Histogram ─────────────────────────────────────────
def exercise_02():
    """Show probability density instead of raw counts."""
    np.random.seed(42)
    data = np.random.randn(500) * 2 + 5

    plt.figure(figsize=(8, 5))
    plt.hist(data, bins=40, density=True, color="coral", edgecolor="black", alpha=0.7)
    # Overlay the true PDF
    x = np.linspace(-2, 12, 200)
    pdf = (1 / (2 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - 5) / 2) ** 2)
    plt.plot(x, pdf, "k--", linewidth=2, label="True PDF")
    plt.legend()
    plt.title("Exercise 2: Normalized Histogram")
    plt.xlabel("Value")
    plt.ylabel("Density")
    plt.savefig("../../../outputs/matplotlib/11_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Overlapping Histograms ───────────────────────────────────────
def exercise_03():
    """Compare two distributions with overlapping histograms."""
    np.random.seed(42)
    group_a = np.random.normal(60, 10, 200)
    group_b = np.random.normal(70, 12, 200)

    plt.figure(figsize=(8, 5))
    plt.hist(group_a, bins=30, alpha=0.6, label="Group A", color="blue", edgecolor="black")
    plt.hist(group_b, bins=30, alpha=0.6, label="Group B", color="red", edgecolor="black")
    plt.legend()
    plt.title("Exercise 3: Overlapping Histograms")
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.savefig("../../../outputs/matplotlib/11_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Histogram with KDE Overlay ───────────────────────────────────
def exercise_04():
    """Show histogram with a kernel density estimation curve."""
    np.random.seed(42)
    data = np.random.gamma(2, 2, 500)

    from scipy.stats import gaussian_kde
    kde = gaussian_kde(data)
    x_kde = np.linspace(0, data.max(), 200)

    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.hist(data, bins=30, density=True, alpha=0.6, color="lightgreen", edgecolor="black")
    ax2 = ax1.twinx()
    ax2.plot(x_kde, kde(x_kde), color="darkgreen", linewidth=2, label="KDE")
    ax2.set_ylabel("Density (KDE)")

    ax1.set_title("Exercise 4: Histogram + KDE")
    ax1.set_xlabel("Value")
    ax1.set_ylabel("Frequency (normalized)")
    ax2.legend(loc="upper right")
    plt.savefig("../../../outputs/matplotlib/11_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: 2D Histogram (Hexbin) ────────────────────────────────────────
def exercise_05():
    """Use hexbin for a 2D histogram of correlated data."""
    np.random.seed(42)
    n = 1000
    x = np.random.randn(n)
    y = 0.8 * x + np.random.randn(n) * 0.5

    plt.figure(figsize=(8, 6))
    hb = plt.hexbin(x, y, gridsize=25, cmap="YlOrRd", mincnt=1)
    plt.colorbar(hb, label="Count")
    plt.title("Exercise 5: 2D Hexbin Histogram")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("../../../outputs/matplotlib/11_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Histogram exercises completed!")
