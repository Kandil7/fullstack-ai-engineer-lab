"""
Matplotlib Subplots - W3Schools Exercises
===========================================
Creating multi-panel figure layouts.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Exercise 1: Basic 2x2 Subplots ──────────────────────────────────────────
def exercise_01():
    """Create a 2x2 grid of subplots with different functions."""
    x = np.linspace(0, 2 * np.pi, 100)
    funcs = [
        (np.sin, "sin(x)", "red"),
        (np.cos, "cos(x)", "blue"),
        (np.tan, "tan(x)", "green"),
        (lambda v: np.abs(np.sin(v)), "|sin(x)|", "purple"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for ax, (func, label, color) in zip(axes.flat, funcs):
        y = func(x)
        if "tan" in label:
            y = np.clip(y, -5, 5)
        ax.plot(x, y, color=color, linewidth=2)
        ax.set_title(label)
        ax.set_ylim(-3, 3) if "tan" not in label else ax.set_ylim(-5, 5)

    plt.suptitle("Exercise 1: 2x2 Subplots", fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "08_exercise_01.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Shared Axes ──────────────────────────────────────────────────
def exercise_02():
    """Create subplots that share x and y axes."""
    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    data = [np.sin(x) + np.random.randn(100) * 0.2 for _ in range(3)]

    fig, axes = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(8, 8))
    colors = ["steelblue", "coral", "seagreen"]
    for ax, d, c in zip(axes, data, colors):
        ax.plot(x, d, color=c, linewidth=1.5)
        ax.set_ylim(-2, 2)
        ax.grid(True, alpha=0.3)

    axes[0].set_title("Exercise 2: Shared Axes")
    axes[-1].set_xlabel("x")
    for i, ax in enumerate(axes):
        ax.set_ylabel(f"Signal {i+1}")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "08_exercise_02.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Uneven Subplot Layout ────────────────────────────────────────
def exercise_03():
    """Use GridSpec or subplot positioning for uneven layouts."""
    fig = plt.figure(figsize=(10, 7))
    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)

    ax1 = fig.add_subplot(gs[0, :])  # spans full top row
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])

    x = np.linspace(0, 2 * np.pi, 100)
    ax1.plot(x, np.sin(x), "b-", linewidth=2)
    ax1.set_title("Top: Full Width")

    ax2.bar(["A", "B", "C"], [5, 8, 3], color="orange")
    ax2.set_title("Bottom Left")

    ax3.pie([30, 25, 45], labels=["X", "Y", "Z"], autopct="%1.1f%%")
    ax3.set_title("Bottom Right")

    fig.suptitle("Exercise 3: Uneven Layout", fontsize=14)
    plt.savefig(os.path.join(OUTPUT_DIR, "08_exercise_03.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Inset Subplot ────────────────────────────────────────────────
def exercise_04():
    """Add an inset (zoomed) subplot within a main plot."""
    x = np.linspace(0, 10, 500)
    y = np.sin(x) * np.exp(-0.1 * x)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, linewidth=2)
    ax.set_title("Exercise 4: Inset Subplot (Zoom)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # Create inset
    ax_inset = fig.add_axes([0.55, 0.5, 0.3, 0.35])
    mask = (x >= 1) & (x <= 4)
    ax_inset.plot(x[mask], y[mask], color="red", linewidth=2)
    ax_inset.set_title("Zoomed In", fontsize=9)
    ax_inset.set_xlabel("x", fontsize=8)
    ax_inset.tick_params(labelsize=7)

    plt.savefig(os.path.join(OUTPUT_DIR, "08_exercise_04.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: 3x3 Subplot Grid ────────────────────────────────────────────
def exercise_05():
    """Create a 3x3 grid of small multiples showing different distributions."""
    np.random.seed(42)
    distributions = {
        "Normal": lambda n: np.random.randn(n),
        "Uniform": lambda n: np.random.uniform(size=n),
        "Exponential": lambda n: np.random.exponential(size=n),
        "Poisson": lambda n: np.random.poisson(5, size=n),
        "Binomial": lambda n: np.random.binomial(10, 0.5, size=n),
        "Gamma": lambda n: np.random.gamma(2, 2, size=n),
        "Beta": lambda n: np.random.beta(2, 5, size=n),
        "Chi-squared": lambda n: np.random.chisquare(3, size=n),
        "Log-normal": lambda n: np.random.lognormal(0, 1, size=n),
    }

    fig, axes = plt.subplots(3, 3, figsize=(12, 10))
    for ax, (name, sampler) in zip(axes.flat, distributions.items()):
        samples = sampler(500)
        ax.hist(samples, bins=30, color="steelblue", edgecolor="black", alpha=0.7)
        ax.set_title(name, fontsize=10)

    plt.suptitle("Exercise 5: Distribution Gallery", fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "08_exercise_05.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll Subplot exercises completed!")
