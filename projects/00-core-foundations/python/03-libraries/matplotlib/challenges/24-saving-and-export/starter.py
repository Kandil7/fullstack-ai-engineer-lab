"""
Challenge 24: Saving and Export — Starter Code
===============================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")   # MUST precede pyplot import: headless tests

import matplotlib.pyplot as plt


def save_fig_png(fig: plt.Figure, path: str, dpi: int) -> tuple[int, int]:
    """Save fig at dpi; return (width, height) from the PNG header."""
    raise NotImplementedError


def export_report(path: str) -> dict[str, object]:
    """Detect format; return width/height/has_alpha for PNG, None for SVG."""
    raise NotImplementedError


def tight_crops(fig: plt.Figure, loose_path: str, tight_path: str, dpi: int) -> bool:
    """Save loose + tight; True iff tight actually cropped the canvas."""
    raise NotImplementedError
