"""
Matplotlib Introduction - W3Schools Exercises
==============================================
Getting started with Matplotlib: basic plotting and configuration.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Exercise 1: Simple Line Plot ─────────────────────────────────────────────
def exercise_01():
    """Plot a basic sine curve to verify Matplotlib is working."""
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y)
    plt.title("Exercise 1: Simple Sine Wave")
    plt.xlabel("x")
    plt.ylabel("sin(x)")
    plt.savefig(os.path.join(OUTPUT_DIR, "01_exercise_01.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Multiple Lines ───────────────────────────────────────────────
def exercise_02():
    """Plot sin(x) and cos(x) on the same figure."""
    x = np.linspace(0, 2 * np.pi, 100)
    y_sin = np.sin(x)
    y_cos = np.cos(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y_sin, label="sin(x)")
    plt.plot(x, y_cos, label="cos(x)")
    plt.legend()
    plt.title("Exercise 2: Sin and Cos")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig(os.path.join(OUTPUT_DIR, "01_exercise_02.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Figure and Axes (OO API) ─────────────────────────────────────
def exercise_03():
    """Use the object-oriented interface to create a figure with two axes."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    x = np.linspace(-3, 3, 200)
    ax1.plot(x, x ** 2, color="blue")
    ax1.set_title("y = x²")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")

    ax2.plot(x, x ** 3, color="red")
    ax2.set_title("y = x³")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")

    plt.suptitle("Exercise 3: OO Interface", fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "01_exercise_03.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Configuring Style ────────────────────────────────────────────
def exercise_04():
    """Explore available Matplotlib styles and apply one."""
    available = plt.style.available
    print(f"  Available styles ({len(available)}): {available[:5]} ...")

    plt.style.use("ggplot")
    x = np.linspace(0, 10, 50)
    plt.figure(figsize=(8, 5))
    plt.plot(x, np.sin(x), linewidth=2, label="sin")
    plt.plot(x, np.cos(x), linewidth=2, label="cos")
    plt.legend()
    plt.title("Exercise 4: ggplot Style")
    plt.savefig(os.path.join(OUTPUT_DIR, "01_exercise_04.png"), dpi=100, bbox_inches="tight")
    plt.style.use("default")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Custom Colors and Line Styles ────────────────────────────────
def exercise_05():
    """Demonstrate custom line colors, widths, and styles."""
    x = np.linspace(0, 2 * np.pi, 100)

    plt.figure(figsize=(8, 5))
    plt.plot(x, np.sin(x), color="#2ecc71", linewidth=2, linestyle="-", label="solid")
    plt.plot(x, np.sin(x + 0.5), color="#e74c3c", linewidth=2, linestyle="--", label="dashed")
    plt.plot(x, np.sin(x + 1.0), color="#3498db", linewidth=2, linestyle=":", label="dotted")
    plt.plot(x, np.sin(x + 1.5), color="#f39c12", linewidth=2, linestyle="-.", label="dash-dot")

    plt.legend()
    plt.title("Exercise 5: Line Styles & Colors")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig(os.path.join(OUTPUT_DIR, "01_exercise_05.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Introduction exercises completed!")
