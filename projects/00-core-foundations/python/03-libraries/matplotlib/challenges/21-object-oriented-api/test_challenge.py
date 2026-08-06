"""Challenge 21: The Object-Oriented API — tests for all three tiers.

Run from the module root:
    python -m pytest 03-libraries/matplotlib/challenges/21-object-oriented-api/test_challenge.py -v
"""

from __future__ import annotations

import importlib.util
import os

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution_21", os.path.join(HERE, "solution.py"))
starter = _load("starter_21", os.path.join(HERE, "starter.py"))


@pytest.fixture(autouse=True)
def _close_figures():
    """Every test starts and ends with zero open figures."""
    plt.close("all")
    yield
    plt.close("all")


# ---------------------------------------------------------------- bronze

def test_bronze_returns_fig_ax():
    fig, ax = solution.explicit_line_plot()
    assert isinstance(fig, plt.Figure)
    assert isinstance(ax, plt.Axes)


def test_bronze_single_line():
    fig, ax = solution.explicit_line_plot()
    assert len(ax.lines) == 1, "exactly one line artist expected"
    assert ax.get_title() != "", "a title must be set"


def test_bronze_no_state_machine_plot():
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    fn = source.split("def mosaic_layout")[0]
    assert "plt.plot(" not in fn, "must plot through ax, not plt.*"


def test_bronze_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.explicit_line_plot()


# ---------------------------------------------------------------- silver

def test_silver_has_exact_keys():
    axd = solution.mosaic_layout()
    assert set(axd) == {"loss", "grad", "hist"}


def test_silver_all_axes():
    axd = solution.mosaic_layout()
    assert all(isinstance(a, plt.Axes) for a in axd.values())
    assert len(axd["loss"].lines) == 1, "loss panel must hold one line"
    assert len(axd["grad"].lines) == 1, "grad panel must hold one line"


def test_silver_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.mosaic_layout()


# ---------------------------------------------------------------- gold

def test_gold_returns_true():
    assert solution.shared_x_propagates() is True


def test_gold_closes_figures():
    solution.shared_x_propagates()
    assert len(plt.get_fignums()) == 0, "figure must be closed"


def test_gold_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.shared_x_propagates()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
