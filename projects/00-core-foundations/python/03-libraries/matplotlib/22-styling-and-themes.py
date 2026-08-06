"""
Matplotlib — 22: Styling and Themes
======================================
Topics: rcParams; stylesheets; colormaps (perceptually uniform,
colorblind-safe; avoid jet); annotation; publication defaults.

Why this matters for AI/backend engineering:
    A model report is only trustworthy if every figure renders identically
    on every machine. rcParams and stylesheets make your visual identity
    deterministic, and perceptually-uniform colormaps are the difference
    between an honest loss heatmap and one that invents structure (jet
    is the classic offender). This is accessibility plus reproducibility
    in one API.

Run:      python 22-styling-and-themes.py
Verify:   python 22-styling-and-themes.py --verify
Reference: https://matplotlib.org/stable/tutorials/introductory/customizing.html
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # MUST precede pyplot import: headless CI rendering

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parents[2] / "outputs" / "matplotlib"
os.makedirs(OUT_DIR, exist_ok=True)

rng = np.random.default_rng(42)

# Canonical perceptually-uniform, colorblind-safe colormaps. These keep
# perceived lightness monotonic, so magnitude reads honestly for everyone.
PERCEPTUALLY_UNIFORM = {"viridis", "plasma", "inferno", "magma", "cividis"}


# ============================================================
# 1. rcParams: global defaults, set once, everywhere
# ============================================================
# rcParams are the process-wide style knobs. Set them at the top of a
# script (or in a matplotlibrc file) so every figure inherits the same
# fonts, sizes, and dpi. They are checked BEFORE any figure is created.

def set_publication_rcparams() -> None:
    """Apply publication-grade defaults to the whole process."""
    plt.rcParams["figure.dpi"] = 120
    plt.rcParams["savefig.dpi"] = 150
    plt.rcParams["font.size"] = 11
    plt.rcParams["axes.titlesize"] = 12
    plt.rcParams["axes.labelsize"] = 11
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.3
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False


# ============================================================
# 2. Stylesheets: one-line themes
# ============================================================
# plt.style.use() swaps a whole family of rcParams. Use a context manager
# to scope a style to a single figure instead of mutating global state.

def demo_stylesheets() -> None:
    """Render the same data under two named styles."""
    x = np.linspace(0, 10, 100)
    with plt.style.context("ggplot"):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, np.sin(x), lw=1.5)
        ax.set_title("ggplot style")
        fig.savefig(OUT_DIR / "22-style-ggplot.png", dpi=120)
        plt.close(fig)

    with plt.style.context("tableau-colorblind10"):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, np.cos(x), lw=1.5)
        ax.set_title("tableau-colorblind10 style")
        fig.savefig(OUT_DIR / "22-style-colorblind.png", dpi=120)
        plt.close(fig)


# ============================================================
# 3. Colormaps: perceptually uniform and colorblind-safe
# ============================================================
# Perceptually uniform: equal data steps map to equal perceived steps.
# Colorblind-safe: distinguishable under deuteranopia/protanopia.
# jet violates both: it is not uniform (banding invents contours) and its
# green/orange region is hostile to red-green colorblind readers.

def demo_colormaps() -> None:
    """Show the same data under viridis (good) and jet (bad)."""
    data = rng.normal(size=(50, 50))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.6))
    im1 = ax1.imshow(data, cmap="viridis")
    ax1.set_title("viridis: uniform, safe")
    fig.colorbar(im1, ax=ax1)

    im2 = ax2.imshow(data, cmap="jet")
    ax2.set_title("jet: banding, unsafe")
    fig.colorbar(im2, ax=ax2)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "22-colormaps.png", dpi=120)
    plt.close(fig)


def is_perceptually_uniform(cmap_name: str) -> bool:
    """Return True if the named colormap is in the canonical PU set."""
    return cmap_name in PERCEPTUALLY_UNIFORM


# ============================================================
# 4. Annotation: pointing the reader at the evidence
# ============================================================
# annotate() draws text plus an arrow to a data coordinate. In ML reports
# this is how you mark a plateau, an anomaly, or a chosen operating point.

def demo_annotation() -> plt.Axes:
    """Annotate the minimum of a noisy curve."""
    x = np.linspace(0, 10, 200)
    y = (x - 4.0) ** 2 + 0.5 * rng.normal(size=x.size)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y, lw=1.0, alpha=0.8)
    i_min = int(np.argmin(y))
    ax.annotate(
        "observed min", xy=(x[i_min], y[i_min]),
        xytext=(7.5, 30), fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "tab:red"},
    )
    ax.set_title("Annotated minimum")
    fig.savefig(OUT_DIR / "22-annotated.png", dpi=120)
    plt.close(fig)
    return ax


# ============================================================
# 5. Publication defaults end to end
# ============================================================
# The production pattern: set rcParams once, build with explicit ax,
# annotate the story, save at print dpi. The same script run on a laptop
# or in CI renders byte-for-byte-equivalent intent.

def demo_publication_figure() -> None:
    """Assemble the full publication pipeline."""
    set_publication_rcparams()
    fig, ax = plt.subplots(figsize=(6, 4))
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(t, np.sin(t), label="train", color="tab:blue")
    ax.plot(t, np.sin(t) * np.exp(-t / 8), label="valid", color="tab:orange")
    ax.set_xlabel("epoch")
    ax.set_ylabel("metric")
    ax.set_title("Decaying validation curve")
    ax.legend(loc="upper right")
    fig.savefig(OUT_DIR / "22-publication.png", dpi=150)
    plt.close(fig)


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: using jet/turbo/rainbow for continuous data
#   ax.imshow(gradients, cmap="jet")        # invents false contours
# CORRECT:
#   ax.imshow(gradients, cmap="viridis")    # honest magnitude
#
# MISTAKE: mutating global style without a scope
#   plt.style.use("dark_background")        # leaks into every later plot
# CORRECT:
#   with plt.style.context("dark_background"):
#       fig, ax = plt.subplots()
#
# MISTAKE: setting rcParams after figures exist
#   fig, ax = plt.subplots()
#   plt.rcParams["figure.dpi"] = 300        # too late for this figure
# CORRECT: set rcParams before any figure creation.


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    set_publication_rcparams()
    assert plt.rcParams["figure.dpi"] == 120, \
        "rcParams assignment must take effect immediately"
    assert plt.rcParams["axes.grid"] is True, \
        "rcParams grid default must be True after our setup"
    assert "ggplot" in plt.style.available, \
        "ggplot must be a registered stylesheet"

    cmap = plt.get_cmap("viridis")
    assert cmap.name == "viridis", "get_cmap must return the named map"
    assert is_perceptually_uniform("viridis"), \
        "viridis must be flagged perceptually uniform"
    assert not is_perceptually_uniform("jet"), \
        "jet must be flagged as NOT perceptually uniform"
    assert mcolors.is_color_like("tab:blue"), \
        "tab:blue must be a valid color spec"

    ax = demo_annotation()
    assert len(ax.texts) == 1, "annotate() must add exactly one text artist"

    demo_stylesheets()
    demo_colormaps()
    demo_publication_figure()

    png = OUT_DIR / "22-publication.png"
    assert png.exists() and png.stat().st_size > 1000, \
        "publication figure must be saved as a non-trivial PNG"
    print("[OK] 22-styling-and-themes: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        set_publication_rcparams()
        demo_stylesheets()
        demo_colormaps()
        demo_annotation()
        demo_publication_figure()
        print("\n--- Summary ---")
        print("1. rcParams set once at startup; stylesheets swap whole themes")
        print("2. Use perceptually uniform, colorblind-safe colormaps; avoid jet")
        print("3. annotate() tells the reader where the evidence is")
        _verify()   # always runs, so plain execution is also a test
