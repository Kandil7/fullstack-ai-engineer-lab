"""Challenge 14: Optimization Advanced — correctness and edge cases.

Run from the module root:
    python -m pytest 03-libraries/scipy/challenges/14-optimization-advanced/test_challenge.py -v
"""

import ast
import importlib.util
import os

import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Unique module names per challenge dir: several test files share the
# filenames solution.py/starter.py, and sys.modules caching would make
# the first import win when pytest runs multiple challenge dirs at once.
solution = _load("solution_14", os.path.join(HERE, "solution.py"))
starter = _load("starter_14", os.path.join(HERE, "starter.py"))


# ---------------------------------------------------------------- helpers

def _assert_no_python_loops(mod):
    for name in ("starter", "solution"):
        tree = ast.parse(
            open(os.path.join(HERE, name + ".py"), encoding="utf-8").read()
        )
        banned = [
            n
            for n in ast.walk(tree)
            if isinstance(
                n, (ast.For, ast.While, ast.ListComp, ast.DictComp,
                    ast.SetComp, ast.GeneratorExp)
            )
        ]
        assert not banned, f"{name}.py contains Python loops/comprehensions"


def _outlier_line(seed=42):
    rng = np.random.default_rng(seed)
    x = np.linspace(0.0, 10.0, 25)
    y = 2.0 * x + 1.0 + rng.normal(scale=0.3, size=x.size)
    y[-7:] += 40.0
    return x, y


# ---------------------------------------------------------------- bronze

def test_bronze_clamped_at_upper_bound():
    x = solution.minimize_box(lambda z: (z - 5.0) ** 2, 0.0, 0.0, 2.0)
    assert np.isclose(x, 2.0, atol=1e-4)


def test_bronze_interior_optimum():
    x = solution.minimize_box(lambda z: (z - 0.3) ** 2, 0.0, 0.0, 2.0)
    assert np.isclose(x, 0.3, atol=1e-4)


def test_bronze_zero_at_bounds():
    x = solution.minimize_box(lambda z: z ** 2, 1.0, -1.0, 1.0)
    assert np.isclose(x, 0.0, atol=1e-4)


def test_bronze_clamped_at_lower_bound():
    x = solution.minimize_box(lambda z: (z + 3.0) ** 2, 0.0, 0.0, 2.0)
    assert np.isclose(x, 0.0, atol=1e-4)


def test_bronze_result_inside_box_always():
    rng = np.random.default_rng(0)
    for _ in range(10):
        lo, hi = sorted(rng.uniform(-5.0, 5.0, size=2))
        x = solution.minimize_box(
            lambda z: np.sin(3.0 * z) + z ** 2, (lo + hi) / 2, lo, hi)
        assert lo - 1e-4 <= x <= hi + 1e-4


def test_bronze_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- silver

def test_silver_clean_line_linear_loss():
    x = np.linspace(0.0, 10.0, 25)
    y = 2.0 * x + 1.0
    slope, intercept = solution.fit_robust_line(x, y, "linear")
    assert abs(slope - 2.0) < 0.1
    assert abs(intercept - 1.0) < 0.1


def test_silver_cauchy_survives_outliers():
    x, y = _outlier_line()
    slope, intercept = solution.fit_robust_line(x, y, "cauchy")
    assert abs(slope - 2.0) < 0.3


def test_silver_linear_fails_on_outliers():
    x, y = _outlier_line()
    slope, _ = solution.fit_robust_line(x, y, "linear")
    assert abs(slope - 2.0) > 0.5


def test_silver_huber_stalls_with_extreme_outliers():
    """Lecture lesson: only cauchy recovers from +40 outliers.

    huber (like soft_l1) stalls in a bad basin near slope 7.2 --
    deterministic for this fixed data, so we assert it does NOT
    recover, proving why cauchy is the reliable choice.
    """
    x, y = _outlier_line()
    slope, intercept = solution.fit_robust_line(x, y, "huber")
    assert isinstance(slope, float) and isinstance(intercept, float)
    assert abs(slope - 2.0) > 1.0


def test_silver_unknown_loss_raises():
    x = np.linspace(0.0, 1.0, 5)
    with pytest.raises(ValueError):
        solution.fit_robust_line(x, x, "fake")


def test_silver_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- gold

def test_gold_two_assets_high_mu_wins():
    """Tangency portfolio: w ~ (mu - rf)/sum(mu - rf) = [0.727, 0.273].

    Not all-in on asset 1 -- mixing cuts volatility and raises Sharpe.
    """
    mu = np.array([0.10, 0.05])
    cov = np.array([[0.04, 0.0], [0.0, 0.04]])
    w = solution.allocate_weights(mu, cov, risk_free=0.02)
    assert abs(w[0] - 0.727) < 0.01
    assert abs(w[1] - 0.273) < 0.01


def test_gold_swapped_mu_flips_allocation():
    mu = np.array([0.05, 0.10])
    cov = np.array([[0.04, 0.0], [0.0, 0.04]])
    w = solution.allocate_weights(mu, cov, risk_free=0.02)
    assert abs(w[0] - 0.273) < 0.01
    assert abs(w[1] - 0.727) < 0.01


def test_gold_equal_returns_split():
    mu = np.array([0.08, 0.08])
    cov = np.array([[0.04, 0.0], [0.0, 0.04]])
    w = solution.allocate_weights(mu, cov, risk_free=0.02)
    assert abs(w.sum() - 1.0) < 1e-6
    assert np.all(w >= -1e-6) and np.all(w <= 1.0 + 1e-6)


def test_gold_three_assets_constraints_and_sharpe():
    rng = np.random.default_rng(7)
    mu = rng.uniform(0.03, 0.12, size=3)
    cov = np.diag(rng.uniform(0.01, 0.08, size=3))
    w = solution.allocate_weights(mu, cov, risk_free=0.02)
    assert abs(w.sum() - 1.0) < 1e-6
    assert np.all(w >= -1e-6) and np.all(w <= 1.0 + 1e-6)
    sharpe_w = (mu @ w - 0.02) / np.sqrt(w @ cov @ w)
    for unit in np.eye(3):
        sharpe_unit = (mu @ unit - 0.02) / np.sqrt(unit @ cov @ unit)
        assert sharpe_w >= sharpe_unit - 1e-6


def test_gold_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- starter

def test_starter_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        starter.minimize_box(lambda z: z ** 2, 0.0, -1.0, 1.0)
    with pytest.raises(NotImplementedError):
        starter.fit_robust_line(np.array([0.0, 1.0]), np.array([0.0, 1.0]),
                                "cauchy")
    with pytest.raises(NotImplementedError):
        starter.allocate_weights(np.array([0.1, 0.05]),
                                 np.eye(2) * 0.04, 0.02)
