"""
Matplotlib — 21: The Object-Oriented API
==============================================
Topics: fig/ax discipline; why the plt.* state machine breaks in scripts;
GridSpec; subplot_mosaic; shared axes.

Why this matters for AI/backend engineering:
    Any plot you ship (eval reports, monitoring dashboards, paper figures)
    must be drawn against explicit Figure/Axes objects. The plt.* state
    machine keeps a hidden "current axes" that leaks between cells, threads,
    and CI runs; one figure, one ax, and everything becomes inspectable,
    testable, and exportable at publication DPI.

Run:      python 21-object-oriented-api.py
Verify:   python 21-object-oriented-api.py --verify
Reference: https://matplotlib.org/stable/tutorials/intermediate/artists.html
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # MUST precede pyplot import: headless CI rendering

import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parents[2] / "outputs" / "matplotlib"
os.makedirs(OUT_DIR, exist_ok=True)

rng = np.random.default_rng(42)


# ============================================================
# 1. Figure and Axes: the explicit contract
# ============================================================
# A Figure is the canvas; an Axes is one plot region inside it. Everything
# you style lives on the Axes. Holding both explicitly means no hidden state:
# you can re-draw, re-style, and unit-test any panel in isolation.
# Complexity: O(1) memory per figure; each Axes holds its own artists.

def demo_fig_ax() -> tuple[plt.Figure, plt.Axes]:
    """Draw one line plot against explicit fig/ax objects."""
    fig, ax = plt.subplots(figsize=(6, 4))          # one fig, one ax
    x = np.linspace(0, 2 * np.pi, 100)
    ax.plot(x, np.sin(x), label="sin(x)")
    ax.set_title("Explicit fig/ax")
    ax.set_xlabel("x (rad)")
    ax.set_ylabel("sin(x)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "21-fig-ax.png", dpi=120)
    plt.close(fig)
    return fig, ax


# ============================================================
# 2. Why plt.* breaks in scripts
# ============================================================
# plt.plot() targets "the current axes". In a script or test runner that is
# implicit state: another call, a style change, or a context manager can
# silently retarget the next plot into a figure you thought you closed.
# The state machine is convenient in a notebook; in code you ship, it is a
# correctness hazard.

def demo_state_machine_hazard() -> None:
    """Show that plt.gca() follows global state, unlike an explicit ax."""
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    plt.sca(ax2)                                     # "set current axes"
    assert plt.gca() is ax2, "current axes must now be ax2"
    plt.sca(ax1)
    assert plt.gca() is ax1, "and back to ax1"
    plt.close(fig1)
    plt.close(fig2)
    print("gca() follows global state; explicit ax does not move")


# ============================================================
# 3. GridSpec: unequal grid layouts
# ============================================================
# GridSpec gives each row/column a relative width/height. The classic
# use: a wide top panel above a small bottom panel (e.g., raw signal
# above its spectrogram).

def demo_gridspec() -> plt.Figure:
    """Build a 2-row, 1-column layout with unequal row heights."""
    fig = plt.figure(figsize=(6, 5))
    gs = fig.add_gridspec(2, 1, height_ratios=(3, 1), hspace=0.35)

    ax_top = fig.add_subplot(gs[0])
    ax_bottom = fig.add_subplot(gs[1])

    t = np.linspace(0, 4, 400)
    ax_top.plot(t, np.sin(2 * np.pi * t), lw=1.5)
    ax_top.set_title("Signal")
    ax_bottom.fill_between(t, np.sign(np.sin(2 * np.pi * t)), step="mid",
                           alpha=0.5)
    ax_bottom.set_title("Step")
    fig.savefig(OUT_DIR / "21-gridspec.png", dpi=120)
    plt.close(fig)
    return fig


# ============================================================
# 4. subplot_mosaic: named panels (no positional bookkeeping)
# ============================================================
# Mosaic labels every panel with a letter/word and returns a dict of
# Axes keyed by that label. Layouts read like ASCII art, and you fetch
# panels by name instead of by (row, col) arithmetic.

def demo_mosaic() -> dict[str, plt.Axes]:
    """Build an 'A on top, B and C below' mosaic and return its axes dict."""
    fig, axd = plt.subplot_mosaic(
        [["loss", "loss"],
         ["grad", "hist"]],
        figsize=(8, 5),
        width_ratios=(2, 1),
    )
    epochs = np.arange(1, 31)
    axd["loss"].plot(epochs, 1.0 / np.sqrt(epochs), label="train")
    axd["loss"].set_title("Training loss")
    axd["grad"].plot(epochs, np.sin(epochs / 3.0), color="tab:orange")
    axd["grad"].set_title("Gradient norm")
    axd["hist"].hist(rng.normal(size=500), bins=20)
    axd["hist"].set_title("Weight histogram")
    fig.savefig(OUT_DIR / "21-mosaic.png", dpi=120)
    plt.close(fig)
    return axd


# ============================================================
# 5. Shared axes: one scale, many panels
# ============================================================
# sharex/sharey align tick ranges across panels, which makes comparisons
# honest. Shared axes are *joined*: setting the limits on one propagates.

def demo_shared_axes() -> tuple[plt.Axes, plt.Axes]:
    """Draw two panels sharing the x axis, and verify the join."""
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6, 5))
    x = np.linspace(0, 10, 200)
    ax1.plot(x, np.cos(x))
    ax2.plot(x, np.sin(x))
    ax1.set_xlim(2, 8)                     # propagates to ax2 via the join
    fig.savefig(OUT_DIR / "21-shared.png", dpi=120)
    plt.close(fig)
    return ax1, ax2


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: mixing interfaces
#   plt.plot(x, y)          # implicit, goes to "current" ax
#   ax.set_title("T")       # explicit, targets a different ax
# CORRECT:
#   fig, ax = plt.subplots()
#   ax.plot(x, y)
#   ax.set_title("T")
#
# MISTAKE: leaking figures in a loop (memory grows until close())
#   for i in range(100):
#       fig, ax = plt.subplots()   # never closed -> 100 open canvases
# CORRECT:
#   for i in range(100):
#       fig, ax = plt.subplots()
#       ...
#       plt.close(fig)


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    fig, ax = demo_fig_ax()
    assert isinstance(fig, plt.Figure), "subplots() must return a Figure"
    assert isinstance(ax, plt.Axes), "subplots() must return an Axes"
    assert len(ax.lines) == 1, "exactly one line on the explicit ax"

    fig_g = demo_gridspec()
    assert len(fig_g.axes) == 2, "GridSpec must produce two axes"

    axd = demo_mosaic()
    assert set(axd) == {"loss", "grad", "hist"}, \
        "mosaic keys must match the layout labels"
    assert all(isinstance(a, plt.Axes) for a in axd.values()), \
        "every mosaic panel must be a real Axes"

    ax1, ax2 = demo_shared_axes()
    assert ax1.get_shared_x_axes().joined(ax1, ax2), \
        "sharex=True must join the two x axes"

    png = OUT_DIR / "21-mosaic.png"
    assert png.exists() and png.stat().st_size > 1000, \
        "mosaic figure must be saved as a non-trivial PNG"

    demo_state_machine_hazard()
    print("[OK] 21-object-oriented-api: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        demo_fig_ax()
        demo_gridspec()
        demo_mosaic()
        demo_shared_axes()
        print("\n--- Summary ---")
        print("1. Hold fig/ax explicitly; the plt.* state machine is implicit")
        print("2. GridSpec controls relative sizes; mosaic names panels")
        print("3. sharex/sharey join axes so limits and scales stay aligned")
        _verify()   # always runs, so plain execution is also a test
