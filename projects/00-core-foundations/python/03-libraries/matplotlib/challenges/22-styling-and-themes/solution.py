"""
Challenge 22: Styling and Themes — Reference Solution
=======================================================
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")   # MUST precede pyplot import: headless tests

import matplotlib.pyplot as plt
import numpy as np

# Canonical perceptually-uniform, colorblind-safe colormaps.
PERCEPTUALLY_UNIFORM = {"viridis", "plasma", "inferno", "magma", "cividis"}


def apply_dpi_defaults() -> None:
    """Set figure.dpi, savefig.dpi, font.size, axes.grid.

    Why this approach: rcParams are read at figure *creation*, so the
    defaults must be applied before any figure exists — this function
    is the "configure once at startup" pattern.
    """
    plt.rcParams["figure.dpi"] = 120
    plt.rcParams["savefig.dpi"] = 150
    plt.rcParams["font.size"] = 11
    plt.rcParams["axes.grid"] = True


def uniform_maps() -> list[str]:
    """Return the canonical perceptually-uniform colormaps, sorted.

    Why this approach: the set literal documents the policy ("these
    five are approved"), and the sorted list makes the output
    deterministic for tests and style audits alike.
    """
    return sorted(PERCEPTUALLY_UNIFORM)


def annotate_minimum(x: np.ndarray, y: np.ndarray) -> plt.Axes:
    """Plot and annotate the minimum; return the axes.

    Why this approach: the annotation is a pure function of the data —
    recompute i_min, re-call annotate, and the label tracks a new
    minimum automatically.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y, alpha=0.8)
    i_min = int(np.argmin(y))
    ax.annotate(
        "observed min",
        xy=(x[i_min], y[i_min]),
        xytext=(7.0, float(y.max())),
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "tab:red"},
    )
    ax.set_title("Annotated minimum")
    return ax
