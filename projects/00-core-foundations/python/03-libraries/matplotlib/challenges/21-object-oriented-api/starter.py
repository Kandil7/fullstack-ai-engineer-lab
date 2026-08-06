"""
Challenge 21: The Object-Oriented API — Starter Code
======================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")   # MUST precede pyplot import: headless tests

import matplotlib.pyplot as plt
import numpy as np


def explicit_line_plot() -> tuple[plt.Figure, plt.Axes]:
    """One line on explicit fig/ax; return both."""
    raise NotImplementedError


def mosaic_layout() -> dict[str, plt.Axes]:
    """Named 2x2 mosaic: loss spans top, grad + hist below."""
    raise NotImplementedError


def shared_x_propagates() -> bool:
    """True iff sharex joins the panels (limits propagate)."""
    raise NotImplementedError
