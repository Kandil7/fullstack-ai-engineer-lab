"""
Matplotlib — 24: Saving and Export
======================================
Topics: savefig DPI; vector vs raster; bbox_inches="tight"; transparent
backgrounds; the Agg backend for headless CI; figure size and
reproducibility.

Why this matters for AI/backend engineering:
    Reports and model cards are rendered headless in CI, then embedded in
    docs, papers, and slides. If your savefig settings are wrong, a 6x4
    figure silently becomes a 0.2 MP blur or an SVG that overflows a page.
    Knowing the PNG header layout lets you VERIFY what you exported, which
    is exactly the kind of artifact assertion CI should run.

Run:      python 24-saving-and-export.py
Verify:   python 24-saving-and-export.py --verify
Reference: https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.savefig
"""

from __future__ import annotations

import os
import struct
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # MUST precede pyplot import: headless CI rendering

import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parents[2] / "outputs" / "matplotlib"
os.makedirs(OUT_DIR, exist_ok=True)

rng = np.random.default_rng(42)


def png_dimensions(path: Path) -> tuple[int, int]:
    """Read (width, height) pixels from a PNG header (IHDR chunk).

    Layout: 8-byte signature, 4-byte length, 4-byte 'IHDR', then
    width (4 bytes BE), height (4 bytes BE). O(1), no image library.
    """
    with open(path, "rb") as fh:
        data = fh.read(33)
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "file must be a PNG"
    assert data[12:16] == b"IHDR", "first chunk must be IHDR"
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def png_has_alpha(path: Path) -> bool:
    """True if the PNG color type is 6 (RGBA), i.e. transparency stored."""
    with open(path, "rb") as fh:
        data = fh.read(26)
    return data[25] == 6


# ============================================================
# 1. DPI: the contract between inches and pixels
# ============================================================
# A figure is sized in INCHES; dpi converts to pixels at export time.
# figsize=(6, 4) at dpi=150 -> exactly 900 x 600 px. This is how you can
# assert that CI exported what the spec demanded.

def save_known_size() -> Path:
    """Save a 6x4 inch figure at 150 dpi; returns the artifact path."""
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.linspace(0, 10, 200)
    ax.plot(x, np.sin(x))
    ax.set_title("DPI contract: 6in x 4in @ 150dpi")
    path = OUT_DIR / "24-dpi.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


# ============================================================
# 2. Vector vs raster: SVG keeps text as text
# ============================================================
# Raster (PNG) stores pixels: zoom in and it blurs. Vector (SVG/PDF)
# stores drawing commands: infinitely sharp, and labels remain selectable
# text. Papers and dashboards use vector; thumbnails use raster.

def save_vector_and_raster() -> tuple[Path, Path]:
    """Export the same figure as SVG and PNG side by side."""
    fig, ax = plt.subplots(figsize=(6, 4))
    t = np.linspace(0, 4 * np.pi, 400)
    ax.plot(t, np.sin(t) * np.exp(-t / 10), label="damped")
    ax.legend()
    ax.set_title("Same figure: SVG vs PNG")
    svg_path = OUT_DIR / "24-vector.svg"
    png_path = OUT_DIR / "24-raster.png"
    fig.savefig(svg_path)
    fig.savefig(png_path, dpi=120)
    plt.close(fig)
    return svg_path, png_path


# ============================================================
# 3. bbox_inches="tight": crop the whitespace
# ============================================================
# Default saving keeps the full figure canvas, so labels near the edge can
# be clipped. "tight" recomputes the bounding box from the artists, which
# is the standard for embedding figures in reports.

def save_tight_and_loose() -> tuple[Path, Path]:
    """Save loose and tight variants; tight should crop the canvas."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([0, 1, 2], [0, 3, 1])
    ax.set_title("A title that reaches the top edge")
    ax.set_ylabel("y label hugging the left edge")
    loose = OUT_DIR / "24-loose.png"
    tight = OUT_DIR / "24-tight.png"
    fig.savefig(loose, dpi=100)
    fig.savefig(tight, dpi=100, bbox_inches="tight")
    plt.close(fig)
    return loose, tight


# ============================================================
# 4. Transparent background: compositing onto slides/dashboards
# ============================================================
# transparent=True drops the facecolor from the raster so the figure can
# sit on a colored slide or a dark dashboard without a white box.

def save_transparent() -> Path:
    """Save a PNG with an alpha channel (color type 6 in IHDR)."""
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot([1, 2, 3], [1, 4, 2])
    ax.set_title("Transparent background")
    path = OUT_DIR / "24-transparent.png"
    fig.savefig(path, dpi=100, transparent=True)
    plt.close(fig)
    return path


# ============================================================
# 5. Agg backend and reproducibility: identical bytes per run
# ============================================================
# The Agg backend renders to memory with no window server, which is why
# CI can run on a bare container. Combined with fixed figsize and dpi,
# the same script on any machine produces the same pixel dimensions.

def save_reproducible() -> Path:
    """Export a canonical artifact used to prove byte-level determinism."""
    fig, ax = plt.subplots(figsize=(5, 4))
    rng2 = np.random.default_rng(7)
    ax.hist(rng2.normal(size=500), bins=20)
    ax.set_title("Reproducible artifact")
    path = OUT_DIR / "24-reproducible.png"
    fig.savefig(path, dpi=110)
    plt.close(fig)
    return path


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: calling savefig after plt.show() (interactive backends clear)
#   plt.show()
#   fig.savefig("late.png")     # may be blank
# CORRECT: save BEFORE show, or never call show in scripts
#
# MISTAKE: exporting 6x4 at default 100 dpi for print
#   fig.savefig("fig.png")      # 600x400 px -> blurry in a paper
# CORRECT: fig.savefig("fig.png", dpi=300)
#
# MISTAKE: relying on GUI backends in tests
#   import matplotlib.pyplot as plt   # may open a window on dev machines
# CORRECT: matplotlib.use("Agg") before the pyplot import


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    path = save_known_size()
    w, h = png_dimensions(path)
    assert (w, h) == (900, 600), \
        f"6in x 4in @ 150dpi must be 900x600 px, got {w}x{h}"

    svg_path, png_path = save_vector_and_raster()
    assert svg_path.exists() and svg_path.stat().st_size > 1000, \
        "SVG artifact must exist and be non-trivial"
    assert png_path.exists() and png_path.stat().st_size > 1000, \
        "PNG artifact must exist and be non-trivial"
    with open(svg_path, "r", encoding="utf-8") as fh:
        svg_head = fh.read(200)
    assert "<svg" in svg_head, "vector export must produce an SVG document"

    loose, tight = save_tight_and_loose()
    w_loose, h_loose = png_dimensions(loose)
    w_tight, h_tight = png_dimensions(tight)
    assert w_tight <= w_loose and h_tight <= h_loose, \
        "bbox_inches='tight' must not enlarge the canvas"
    assert (w_tight, h_tight) != (w_loose, h_loose), \
        "tight cropping must change the pixel dimensions here"

    trans = save_transparent()
    assert png_has_alpha(trans), \
        "transparent=True must write an RGBA (color type 6) PNG"

    repro = save_reproducible()
    w_r, h_r = png_dimensions(repro)
    assert (w_r, h_r) == (550, 440), \
        f"5in x 4in @ 110dpi must be 550x440 px, got {w_r}x{h_r}"

    print("[OK] 24-saving-and-export: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        save_known_size()
        save_vector_and_raster()
        save_tight_and_loose()
        save_transparent()
        save_reproducible()
        print("\n--- Summary ---")
        print("1. pixels = inches * dpi; assert the header to prove it")
        print("2. SVG/PDF are vector; PNG is raster; pick per artifact")
        print("3. bbox_inches='tight' crops; transparent writes RGBA")
        _verify()   # always runs, so plain execution is also a test
