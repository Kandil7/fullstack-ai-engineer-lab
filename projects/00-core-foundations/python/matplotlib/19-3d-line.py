"""
Matplotlib 3D Line Plots - W3Schools Exercises
================================================
3D line plotting and parametric curves.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Exercise 1: Basic 3D Line ────────────────────────────────────────────────
def exercise_01():
    """Plot a simple helix in 3D space."""
    t = np.linspace(0, 4 * np.pi, 500)
    x = np.cos(t)
    y = np.sin(t)
    z = t

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(x, y, z, linewidth=2, color="blue")
    ax.set_title("Exercise 1: Helix (3D Line)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig(os.path.join(OUTPUT_DIR, "19_exercise_01.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 01 saved")


# ── Exercise 2: Color-Changing 3D Line ───────────────────────────────────────
def exercise_02():
    """Use scatter with very small markers connected by lines for color gradient."""
    t = np.linspace(0, 6 * np.pi, 1000)
    x = np.cos(t) * (1 + 0.5 * np.cos(3 * t))
    y = np.sin(t) * (1 + 0.5 * np.cos(3 * t))
    z = np.sin(3 * t)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    # Use scatter with connected segments
    for i in range(len(t) - 1):
        color = plt.cm.hsv(i / len(t))
        ax.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=color, linewidth=1.5)
    ax.set_title("Exercise 2: Color-Changing 3D Curve")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig(os.path.join(OUTPUT_DIR, "19_exercise_02.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 02 saved")


# ── Exercise 3: Lissajous Curve ──────────────────────────────────────────────
def exercise_03():
    """Plot a 3D Lissajous curve with different frequencies."""
    t = np.linspace(0, 2 * np.pi, 1000)
    a, b, c = 3, 2, 5
    delta = np.pi / 4

    x = np.sin(a * t + delta)
    y = np.sin(b * t)
    z = np.sin(c * t)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(x, y, z, linewidth=1.5, color="purple")
    ax.set_title(f"Exercise 3: Lissajous (a={a}, b={b}, c={c})")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig(os.path.join(OUTPUT_DIR, "19_exercise_03.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 03 saved")


# ── Exercise 4: Multiple 3D Lines ────────────────────────────────────────────
def exercise_04():
    """Plot multiple 3D trajectories for comparison."""
    np.random.seed(42)
    t = np.linspace(0, 10, 300)
    colors = ["red", "green", "blue"]

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    for i, c in enumerate(colors):
        x = np.cumsum(np.random.randn(300) * 0.1)
        y = np.cumsum(np.random.randn(300) * 0.1)
        z = np.cumsum(np.random.randn(300) * 0.1) + i * 2
        ax.plot(x, y, z, color=c, linewidth=1.5, label=f"Path {i+1}")

    ax.legend()
    ax.set_title("Exercise 4: Multiple 3D Trajectories")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig(os.path.join(OUTPUT_DIR, "19_exercise_04.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 04 saved")


# ── Exercise 5: Parametric Torus ─────────────────────────────────────────────
def exercise_05():
    """Plot a parametric torus curve in 3D."""
    theta = np.linspace(0, 2 * np.pi, 500)
    phi = np.linspace(0, 2 * np.pi, 500)

    # Single torus curve (a single ring)
    R, r = 2, 0.5
    x = (R + r * np.cos(phi)) * np.cos(theta)
    y = (R + r * np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(x, y, z, linewidth=1, color="teal")
    ax.set_title("Exercise 5: Torus Curve")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_box_aspect([1, 1, 0.4])
    plt.savefig(os.path.join(OUTPUT_DIR, "19_exercise_05.png"), dpi=100, bbox_inches="tight")
    plt.close()
    print("[OK] Exercise 05 saved")


if __name__ == "__main__":
    exercise_01()
    exercise_02()
    exercise_03()
    exercise_04()
    exercise_05()
    print("\nAll 3D Line exercises completed!")
