"""
Challenge 24: Saving and Export — Reference Solution
======================================================
"""

from __future__ import annotations

import struct

import matplotlib
matplotlib.use("Agg")   # MUST precede pyplot import: headless tests

import matplotlib.pyplot as plt


def _png_dimensions(path: str) -> tuple[int, int]:
    """Read (width, height) from the IHDR chunk; O(1), no image lib.

    Layout: 8-byte signature, 4-byte length, 4-byte 'IHDR', then
    width (4 bytes BE), height (4 bytes BE).
    """
    with open(path, "rb") as fh:
        data = fh.read(33)
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "file must be a PNG"
    assert data[12:16] == b"IHDR", "first chunk must be IHDR"
    return struct.unpack(">II", data[16:24])


def _png_color_type(path: str) -> int:
    """Byte 25 of the file: 2 = RGB, 6 = RGBA."""
    with open(path, "rb") as fh:
        data = fh.read(26)
    return data[25]


def save_fig_png(fig: plt.Figure, path: str, dpi: int) -> tuple[int, int]:
    """Save fig at dpi; return (width, height) from the PNG header.

    Why this approach: pixels = inches * dpi is a contract; asserting
    it against the file itself (not against matplotlib's memory) is
    what makes exports CI-verifiable.
    """
    fig.savefig(path, dpi=dpi)
    return _png_dimensions(path)


def export_report(path: str) -> dict[str, object]:
    """Detect format; return width/height/has_alpha for PNG, None for SVG.

    Why this approach: format detection from magic bytes is the
    CI-safe way to verify what was exported. For PNG, the IHDR chunk
    gives dimensions and color type 6 (RGBA) reports an alpha channel.
    Note: matplotlib >= 3.10 writes RGBA even for opaque saves, so
    has_alpha means "channel present", not "background transparent".
    """
    with open(path, "rb") as fh:
        head = fh.read(8)
    if head == b"\x89PNG\r\n\x1a\n":
        w, h = _png_dimensions(path)
        return {
            "format": "png",
            "width": w,
            "height": h,
            "has_alpha": _png_color_type(path) == 6,
        }
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read(200)
    if "<svg" in text:
        return {"format": "svg", "width": None, "height": None, "has_alpha": None}
    return {"format": "unknown", "width": None, "height": None, "has_alpha": None}


def tight_crops(fig: plt.Figure, loose_path: str, tight_path: str, dpi: int) -> bool:
    """Save loose + tight; True iff tight actually cropped the canvas.

    Why this approach: the verdict must come from the exported files,
    not from figure attributes — the same header parser used in CI.
    """
    fig.savefig(loose_path, dpi=dpi)
    fig.savefig(tight_path, dpi=dpi, bbox_inches="tight")
    w_loose, h_loose = _png_dimensions(loose_path)
    w_tight, h_tight = _png_dimensions(tight_path)
    cropped = (w_tight <= w_loose and h_tight <= h_loose)
    changed = (w_tight, h_tight) != (w_loose, h_loose)
    return bool(cropped and changed)
