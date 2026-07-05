"""
Matplotlib Scatter Plot - W3Schools Exercises
===============================================
Scatter plot customization and techniques.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Exercise 1: Basic Scatter ────────────────────────────────────────────────
def exercise_01():
    """Create a simple scatter plot with random data."""
    np.random.seed(42)
    x = np.random.randn(50)
    y = np.random.randn(50)

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y)
    plt.title("Exercise 1: Basic Scatter Plot")
    plt.xlabel("X values")
    plt.ylabel("Y values")
    plt.savefig(os.path.join(OUTPUT_DIR, "09_exercise_01.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Size and Color Mapping ───────────────────────────────────────
def exercise_02():
    """Map point size and color to additional dimensions."""
    np.random.seed(10)
    n = 100
    x = np.random.randn(n)
    y = 2 * x + np.random.randn(n)
    sizes = np.abs(np.random.randn(n)) * 200 + 30
    colors = x + y

    plt.figure(figsize=(8, 6))
    sc = plt.scatter(x, y, s=sizes, c=colors, cmap="viridis", alpha=0.7,
                     edgecolors="black", linewidth=0.5)
    plt.colorbar(sc, label="x + y value")
    plt.title("Exercise 2: Size & Color Mapping")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig(os.path.join(OUTPUT_DIR, "09_exercise_02.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Categorical Scatter ──────────────────────────────────────────
def exercise_03():
    """Scatter plot with categorical x-axis and jittered y values."""
    np.random.seed(42)
    categories = ["Control", "Drug A", "Drug B", "Drug C"]
    data = [np.random.normal(50 + i * 5, 10, 30) for i in range(4)]
    colors = ["#3498db", "#e74c3c", "#2ecc71", "#9b59b6"]

    plt.figure(figsize=(8, 6))
    for i, (cat, vals, col) in enumerate(zip(categories, data, colors)):
        jitter = np.random.uniform(-0.1, 0.1, len(vals))
        plt.scatter(np.full(len(vals), i) + jitter, vals, color=col,
                    alpha=0.6, edgecolors="black", linewidth=0.5, label=cat)

    plt.xticks(range(len(categories)), categories)
    plt.ylabel("Response")
    plt.title("Exercise 3: Categorical Scatter (Jittered)")
    plt.legend()
    plt.savefig(os.path.join(OUTPUT_DIR, "09_exercise_03.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Bubble Chart ─────────────────────────────────────────────────
def exercise_04():
    """Create a bubble chart representing 4 dimensions of data."""
    np.random.seed(7)
    countries = ["USA", "China", "India", "Brazil", "Germany", "UK", "Japan", "France"]
    gdp = [21.4, 14.3, 2.9, 1.8, 3.8, 2.8, 5.1, 2.7]  # trillion $
    life_expectancy = [78.9, 76.9, 69.7, 75.9, 81.0, 81.3, 84.6, 82.7]
    population = [331, 1412, 1380, 213, 83, 67, 126, 67]  # millions
    colors = plt.cm.Set2(np.linspace(0, 1, len(countries)))

    plt.figure(figsize=(10, 7))
    for i, c in enumerate(countries):
        plt.scatter(gdp[i], life_expectancy[i], s=population[i] / 5,
                    color=colors[i], alpha=0.7, edgecolors="black", linewidth=1)
        plt.annotate(c, (gdp[i], life_expectancy[i]), fontsize=9,
                     textcoords="offset points", xytext=(10, 5))

    plt.title("Exercise 4: Bubble Chart (GDP vs Life Expectancy)")
    plt.xlabel("GDP (Trillion $)")
    plt.ylabel("Life Expectancy (years)")
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(OUTPUT_DIR, "09_exercise_04.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Scatter with Regression Line ─────────────────────────────────
def exercise_05():
    """Scatter plot with a fitted linear regression line."""
    np.random.seed(42)
    x = np.random.uniform(0, 10, 80)
    y = 2.5 * x + 5 + np.random.randn(80) * 3

    # Fit line
    coeffs = np.polyfit(x, y, 1)
    poly = np.poly1d(coeffs)
    x_line = np.linspace(0, 10, 100)

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, alpha=0.6, edgecolors="black", linewidth=0.5)
    plt.plot(x_line, poly(x_line), color="red", linewidth=2,
             label=f"y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}")
    plt.legend(fontsize=12)
    plt.title("Exercise 5: Scatter with Regression Line")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(OUTPUT_DIR, "09_exercise_05.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Scatter Plot exercises completed!")
