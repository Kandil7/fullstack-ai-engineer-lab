"""
Matplotlib Line Plot - W3Schools Exercises
============================================
Focused exercises on line plotting techniques.
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


# ── Exercise 1: Simple Line with Data Points ─────────────────────────────────
def exercise_01():
    """Plot line from explicit x,y coordinates."""
    x = [0, 1, 2, 3, 4, 5]
    y = [0, 1, 4, 9, 16, 25]

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker="o", linewidth=2, color="darkblue")
    plt.title("Exercise 1: y = x²")
    plt.xlabel("x")
    plt.ylabel("x²")
    plt.savefig("../../../outputs/matplotlib/05_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Multiple Lines with Legend ────────────────────────────────────
def exercise_02():
    """Plot multiple exponential functions with legend."""
    x = np.linspace(0, 3, 100)
    bases = [0.5, 1.5, 2.0, 3.0]
    colors = ["blue", "green", "red", "purple"]

    plt.figure(figsize=(8, 5))
    for base, color in zip(bases, colors):
        plt.plot(x, base ** x, color=color, linewidth=2, label=f"{base}^x")
    plt.legend()
    plt.title("Exercise 2: Exponential Functions")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.ylim(0, 30)
    plt.savefig("../../../outputs/matplotlib/05_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Time Series Line Plot ────────────────────────────────────────
def exercise_03():
    """Simulate and plot a stock price time series."""
    np.random.seed(42)
    days = 365
    t = np.arange(days)
    price = 100 * np.exp(np.cumsum(np.random.randn(days) * 0.02))

    plt.figure(figsize=(12, 5))
    plt.plot(t, price, color="green", linewidth=1)
    plt.fill_between(t, price, alpha=0.1, color="green")
    plt.title("Exercise 3: Simulated Stock Price (365 Days)")
    plt.xlabel("Day")
    plt.ylabel("Price ($)")
    plt.grid(True, alpha=0.3)
    plt.savefig("../../../outputs/matplotlib/05_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Stepped Line Plot ────────────────────────────────────────────
def exercise_04():
    """Use drawstyle to create stepped (staircase) line plots."""
    x = np.arange(1, 8)
    y = [1, 3, 2, 5, 4, 7, 6]
    styles = ["default", "steps-pre", "steps-mid", "steps-post"]

    plt.figure(figsize=(10, 8))
    for i, ds in enumerate(styles, 1):
        plt.subplot(2, 2, i)
        plt.step(x, y, where="pre" if "pre" in ds else
                 ("mid" if "mid" in ds else "post" if "post" in ds else "pre"),
                 linewidth=2, color="teal")
        plt.plot(x, y, "o", color="red", markersize=6)
        plt.title(f"drawstyle: {ds}")
        plt.ylim(0, 8)
    plt.suptitle("Exercise 4: Stepped Line Plots", fontsize=13)
    plt.tight_layout()
    plt.savefig("../../../outputs/matplotlib/05_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Line with Annotations ────────────────────────────────────────
def exercise_05():
    """Plot a line and annotate key points."""
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, color="blue", linewidth=2)

    # Annotate the maximum
    max_idx = np.argmax(y)
    plt.annotate("Maximum", xy=(x[max_idx], y[max_idx]),
                 xytext=(x[max_idx] + 0.5, y[max_idx] + 0.3),
                 arrowprops=dict(arrowstyle="->", color="red"),
                 fontsize=11, color="red")

    # Annotate the minimum
    min_idx = np.argmin(y)
    plt.annotate("Minimum", xy=(x[min_idx], y[min_idx]),
                 xytext=(x[min_idx] + 0.5, y[min_idx] - 0.3),
                 arrowprops=dict(arrowstyle="->", color="orange"),
                 fontsize=11, color="orange")

    plt.title("Exercise 5: Line with Annotations")
    plt.xlabel("x")
    plt.ylabel("sin(x)")
    plt.savefig("../../../outputs/matplotlib/05_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Line Plot exercises completed!")
