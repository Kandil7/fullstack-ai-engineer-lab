"""Challenge 22: Styling and Themes — tests for all three tiers.

Run from the module root:
    python -m pytest 03-libraries/matplotlib/challenges/22-styling-and-themes/test_challenge.py -v
"""

from __future__ import annotations

import importlib.util
import os

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


solution = _load("solution_22", os.path.join(HERE, "solution.py"))
starter = _load("starter_22", os.path.join(HERE, "starter.py"))


@pytest.fixture(autouse=True)
def _clean_figures():
    plt.close("all")
    yield
    plt.close("all")


# ---------------------------------------------------------------- bronze

def test_bronze_rcparams_applied():
    solution.apply_dpi_defaults()
    assert plt.rcParams["figure.dpi"] == 120
    assert plt.rcParams["savefig.dpi"] == 150
    assert plt.rcParams["font.size"] == 11
    assert plt.rcParams["axes.grid"] is True


def test_bronze_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.apply_dpi_defaults()


# ---------------------------------------------------------------- silver

def test_silver_exact_set():
    assert solution.uniform_maps() == ["cividis", "inferno", "magma", "plasma", "viridis"]


def test_silver_jet_rejected():
    result = solution.uniform_maps()
    assert "jet" not in result, "jet must not pass the PU policy"


def test_silver_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.uniform_maps()


# ---------------------------------------------------------------- gold

def _noisy_parabola():
    rng = np.random.default_rng(42)
    x = np.linspace(0, 10, 200)
    y = (x - 4.0) ** 2 + 0.5 * rng.normal(size=x.size)
    return x, y


def test_gold_single_annotation():
    x, y = _noisy_parabola()
    ax = solution.annotate_minimum(x, y)
    assert len(ax.texts) == 1, "exactly one text artist"


def test_gold_xy_is_argmin():
    x, y = _noisy_parabola()
    ax = solution.annotate_minimum(x, y)
    i_min = int(np.argmin(y))
    ann = ax.texts[0]
    assert ann.xy == (x[i_min], y[i_min]), "annotation must point at the argmin"
    assert ann.xy[0] == pytest.approx(x[i_min])
    assert ann.xy[1] == pytest.approx(y[i_min])


def test_gold_uses_annotate():
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    fn = source.split("def uniform_maps")[1]
    assert "annotate(" in fn, "must use ax.annotate"


def test_gold_starter_raises():
    x, y = _noisy_parabola()
    with pytest.raises(NotImplementedError):
        starter.annotate_minimum(x, y)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
