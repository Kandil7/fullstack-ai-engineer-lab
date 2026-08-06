"""Challenge 24: Saving and Export — tests for all three tiers.

Run from the module root:
    python -m pytest 03-libraries/matplotlib/challenges/24-saving-and-export/test_challenge.py -v
"""

from __future__ import annotations

import importlib.util
import os
import struct

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution_24", os.path.join(HERE, "solution.py"))
starter = _load("starter_24", os.path.join(HERE, "starter.py"))


def _plain_fig(figsize=(6, 4)):
    fig, ax = plt.subplots(figsize=figsize)
    x = np.linspace(0, 10, 200)
    ax.plot(x, np.sin(x))
    return fig


def _edge_hugging_fig(figsize=(6, 4)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot([0, 1, 2], [0, 3, 1])
    ax.set_title("A title that reaches the top edge")
    ax.set_ylabel("y label hugging the left edge")
    return fig


@pytest.fixture(autouse=True)
def _close_figures():
    plt.close("all")
    yield
    plt.close("all")


def _parse_header(path):
    with open(path, "rb") as fh:
        data = fh.read(33)
    return struct.unpack(">II", data[16:24])


# ---------------------------------------------------------------- bronze

def test_bronze_dpi_contract(tmp_path):
    fig = _plain_fig(figsize=(6, 4))
    w, h = solution.save_fig_png(fig, str(tmp_path / "a.png"), 150)
    assert (w, h) == (900, 600), "6in x 4in @ 150dpi must be 900x600"


def test_bronze_file_is_png(tmp_path):
    fig = _plain_fig()
    path = str(tmp_path / "b.png")
    solution.save_fig_png(fig, path, 100)
    with open(path, "rb") as fh:
        assert fh.read(8) == b"\x89PNG\r\n\x1a\n", "must be a real PNG"


def test_bronze_matches_own_parser(tmp_path):
    fig = _plain_fig(figsize=(5, 4))
    path = str(tmp_path / "c.png")
    result = solution.save_fig_png(fig, path, 110)
    assert result == _parse_header(path)


def test_bronze_starter_raises(tmp_path):
    with pytest.raises(NotImplementedError):
        starter.save_fig_png(_plain_fig(), str(tmp_path / "x.png"), 100)


# ---------------------------------------------------------------- silver

def test_silver_png_report(tmp_path):
    fig = _plain_fig(figsize=(4, 3))
    path = str(tmp_path / "opaque.png")
    fig.savefig(path, dpi=100)
    report = solution.export_report(path)
    assert report["format"] == "png"
    assert report["width"] == 400 and report["height"] == 300


def test_silver_transparent_has_alpha(tmp_path):
    fig = _plain_fig(figsize=(4, 3))
    path = str(tmp_path / "transparent.png")
    fig.savefig(path, dpi=100, transparent=True)
    report = solution.export_report(path)
    assert report["format"] == "png"
    assert report["has_alpha"] is True, "RGBA channel must be present"


def test_silver_svg_report(tmp_path):
    fig = _plain_fig(figsize=(4, 3))
    path = str(tmp_path / "vector.svg")
    fig.savefig(path)
    report = solution.export_report(path)
    assert report["format"] == "svg"
    assert report["width"] is None


def test_silver_starter_raises(tmp_path):
    path = str(tmp_path / "x.png")
    _plain_fig().savefig(path, dpi=100)
    with pytest.raises(NotImplementedError):
        starter.export_report(path)


# ---------------------------------------------------------------- gold

def test_gold_tight_crops_edge_figure(tmp_path):
    fig = _edge_hugging_fig()
    assert solution.tight_crops(
        fig, str(tmp_path / "loose.png"), str(tmp_path / "tight.png"), 100
    ) is True


def test_gold_files_differ(tmp_path):
    fig = _edge_hugging_fig()
    loose, tight = str(tmp_path / "loose.png"), str(tmp_path / "tight.png")
    solution.tight_crops(fig, loose, tight, 100)
    assert _parse_header(loose) != _parse_header(tight), \
        "cropping must change the exported pixels"


def test_gold_header_based():
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    assert "struct.unpack" in source, "must parse the PNG header"
    assert "bbox_inches" in source, "must use bbox_inches='tight'"


def test_gold_starter_raises(tmp_path):
    with pytest.raises(NotImplementedError):
        starter.tight_crops(_edge_hugging_fig(), str(tmp_path / "l.png"), str(tmp_path / "t.png"), 100)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
