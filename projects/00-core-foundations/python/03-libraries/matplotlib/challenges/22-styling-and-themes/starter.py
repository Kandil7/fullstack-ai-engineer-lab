"""
Challenge 22: Styling and Themes — Starter Code
=================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")   # MUST precede pyplot import: headless tests

import matplotlib.pyplot as plt
import numpy as np


def apply_dpi_defaults() -> None:
    """Set figure.dpi, savefig.dpi, font.size, axes.grid."""
    raise NotImplementedError


def uniform_maps() -> list[str]:
    """Return the canonical perceptually-uniform colormaps, sorted."""
    raise NotImplementedError


def annotate_minimum(x: np.ndarray, y: np.ndarray) -> plt.Axes:
    """Plot and annotate the minimum; return the axes."""
    raise NotImplementedError
