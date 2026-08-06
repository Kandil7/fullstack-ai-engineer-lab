"""
Matplotlib Plotting Markers & Line Styles - W3Schools Exercises
================================================================
Comprehensive exercises on line and marker customization.
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


# ── Exercise 1: Marker Styles ────────────────────────────────────────────────
def exercise_01():
    """Demonstrate all common Matplotlib marker types."""
    markers = ["o", "s", "^", "D", "v", "P", "*", "X", "p", "h"]
    x = np.linspace(0, 2 * np.pi, len(markers))

    plt.figure(figsize=(10, 6))
    for i, m in enumerate(markers):
        plt.plot(x[i], i, marker=m, markersize=15, linestyle="none", label=m)
    plt.yticks(range(len(markers)), markers)
    plt.title("Exercise 1: Marker Styles")
    plt.xlabel("x")
    plt.legend(title="Marker", ncol=2)
    plt.savefig(OUTPUT_DIR / "03_exercise_01.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Line Styles ──────────────────────────────────────────────────
def exercise_02():
    """Demonstrate all line style options."""
    styles = ["-", "--", "-.", ":"]
    labels = ["solid", "dashed", "dash-dot", "dotted"]
    x = np.linspace(0, 10, 100)

    plt.figure(figsize=(8, 5))
    for style, label in zip(styles, labels):
        plt.plot(x, np.sin(x * (styles.index(style) + 1)), linestyle=style,
                 linewidth=2, label=label)
    plt.legend()
    plt.title("Exercise 2: Line Styles")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig(OUTPUT_DIR / "03_exercise_02.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Line Width and Color ─────────────────────────────────────────
def exercise_03():
    """Control line width and named color strings."""
    x = np.linspace(0, 2 * np.pi, 100)
    widths = [0.5, 1.0, 2.0, 3.0, 5.0]
    colors = ["red", "orange", "green", "blue", "purple"]

    plt.figure(figsize=(8, 5))
    for w, c in zip(widths, colors):
        plt.plot(x, np.sin(x) * w, linewidth=w, color=c, label=f"w={w}")
    plt.legend()
    plt.title("Exercise 3: Line Width & Color")
    plt.savefig(OUTPUT_DIR / "03_exercise_03.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Combined Marker + Line Styling ───────────────────────────────
def exercise_04():
    """Combine markers with different line styles for publication-quality plots."""
    categories = ["Control", "Treatment A", "Treatment B", "Treatment C"]
    x = np.arange(1, 11)
    np.random.seed(42)
    data = [np.cumsum(np.random.randn(10) * 0.5 + i * 0.3) for i in range(4)]
    markers = ["o", "s", "^", "D"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

    plt.figure(figsize=(10, 6))
    for cat, d, m, c in zip(categories, data, markers, colors):
        plt.plot(x, d, marker=m, color=c, markersize=8, linewidth=2,
                 markerfacecolor="white", markeredgewidth=2, label=cat)
    plt.legend()
    plt.title("Exercise 4: Publication-Quality Plot")
    plt.xlabel("Time Point")
    plt.ylabel("Cumulative Value")
    plt.grid(True, alpha=0.3)
    plt.savefig(OUTPUT_DIR / "03_exercise_04.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Scatter-Like Plot with plot() ────────────────────────────────
def exercise_05():
    """Use plot() with markers only (no line) to create scatter-style display."""
    np.random.seed(7)
    x = np.random.randn(50)
    y = np.random.randn(50)
    sizes = np.abs(np.random.randn(50)) * 300 + 50

    plt.figure(figsize=(8, 8))
    plt.plot(x, y, "o", markersize=8, color="teal", alpha=0.6)
    plt.title("Exercise 5: Scatter-Like with plot()")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axhline(y=0, color="gray", linestyle="--", alpha=0.5)
    plt.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    plt.savefig(OUTPUT_DIR / "03_exercise_05.png", dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Plotting exercises completed!")
