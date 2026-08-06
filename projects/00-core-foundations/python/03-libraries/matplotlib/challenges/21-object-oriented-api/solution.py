"""
Challenge 21: The Object-Oriented API — Reference Solution
===========================================================
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")   # MUST precede pyplot import: headless tests

import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)


def explicit_line_plot() -> tuple[plt.Figure, plt.Axes]:
    """One line on explicit fig/ax; return both.

    Why this approach: holding fig and ax explicitly means no hidden
    "current axes" state — the caller can inspect, re-style, or test
    either object in isolation.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.linspace(0, 2 * np.pi, 100)
    ax.plot(x, np.sin(x))
    ax.set_title("Explicit fig/ax")
    return fig, ax


def mosaic_layout() -> dict[str, plt.Axes]:
    """Named 2x2 mosaic: loss spans top, grad + hist below.

    Why this approach: the repeated "loss" label creates the span, and
    the returned dict is keyed by name — no (row, col) arithmetic.
    """
    fig, axd = plt.subplot_mosaic(
        [["loss", "loss"],
         ["grad", "hist"]],
        figsize=(8, 5),
        width_ratios=(2, 1),
    )
    epochs = np.arange(1, 31)
    axd["loss"].plot(epochs, 1.0 / np.sqrt(epochs))
    axd["grad"].plot(epochs, np.sin(epochs / 3.0))
    axd["hist"].hist(rng.normal(size=500), bins=20)
    return axd


def shared_x_propagates() -> bool:
    """True iff sharex joins the panels (limits propagate).

    Why this approach: the join is a runtime property, not just a
    constructor argument — the API exposes it via
    get_shared_x_axes().joined(), and the xlim equality proves the
    propagation actually happened.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6, 5))
    x = np.linspace(0, 10, 200)
    ax1.plot(x, np.cos(x))
    ax2.plot(x, np.sin(x))
    ax1.set_xlim(2, 8)
    same_limits = all(
        abs(a - b) < 1e-9
        for a, b in zip(ax2.get_xlim(), ax1.get_xlim())
    )
    joined = ax1.get_shared_x_axes().joined(ax1, ax2)
    plt.close(fig)
    return bool(same_limits and joined)
