"""Challenge 23: ML Visualization — tests for all three tiers.

Run from the module root:
    python -m pytest 03-libraries/matplotlib/challenges/23-ml-visualization/test_challenge.py -v
"""

from __future__ import annotations

import importlib.util
import os

import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution_23", os.path.join(HERE, "solution.py"))
starter = _load("starter_23", os.path.join(HERE, "starter.py"))


def _roc_inputs() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(42)
    n = 1000
    y_true = np.concatenate([np.zeros(700), np.ones(300)]).astype(int)
    y_score = np.concatenate([
        rng.normal(0.0, 1.0, 700), rng.normal(2.2, 1.0, 300)
    ])
    return y_true, y_score


def _confusion_inputs() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(42)
    y_true = rng.integers(0, 3, 300)
    y_pred = np.clip(y_true + rng.choice([-1, 0, 0, 0, 1], 300), 0, 2)
    return y_true, y_pred


# ---------------------------------------------------------------- bronze

def test_bronze_endpoints():
    y_true, y_score = _roc_inputs()
    fpr, tpr = solution.roc_endpoints(y_true, y_score)
    assert fpr[0] == 0.0 and tpr[0] == 0.0, "ROC must start at (0, 0)"
    assert abs(fpr[-1] - 1.0) < 1e-12 and abs(tpr[-1] - 1.0) < 1e-12, \
        "ROC must end at (1, 1)"


def test_bronze_monotonic():
    y_true, y_score = _roc_inputs()
    fpr, tpr = solution.roc_endpoints(y_true, y_score)
    assert np.all(np.diff(fpr) >= 0), "FPR must be monotonic"
    assert np.all(np.diff(tpr) >= 0), "TPR must be monotonic"


def test_bronze_deterministic():
    y_true, y_score = _roc_inputs()
    a = solution.roc_endpoints(y_true, y_score)
    b = solution.roc_endpoints(y_true, y_score)
    assert np.array_equal(a[0], b[0]) and np.array_equal(a[1], b[1])


def test_bronze_starter_raises():
    y_true, y_score = _roc_inputs()
    with pytest.raises(NotImplementedError):
        starter.roc_endpoints(y_true, y_score)


# ---------------------------------------------------------------- silver

def test_silver_shape():
    y_true, y_pred = _confusion_inputs()
    report = solution.confusion_stats(y_true, y_pred)
    assert report["shape"] == (3, 3), "3 classes -> 3x3 matrix"


def test_silver_diagonal_positive():
    y_true, y_pred = _confusion_inputs()
    report = solution.confusion_stats(y_true, y_pred)
    assert report["diagonal"] > 0, "some correct predictions expected"


def test_silver_perfect_predictions():
    y_true = np.array([0, 1, 2, 1, 0, 2])
    report = solution.confusion_stats(y_true, y_true.copy())
    assert report["shape"] == (3, 3)
    assert report["diagonal"] == len(y_true), "perfect -> all on diagonal"


def test_silver_starter_raises():
    y_true, y_pred = _confusion_inputs()
    with pytest.raises(NotImplementedError):
        starter.confusion_stats(y_true, y_pred)


# ---------------------------------------------------------------- gold

def test_gold_verdict_true():
    assert solution.learning_curve_improves() is True


def test_gold_deterministic():
    assert solution.learning_curve_improves() is solution.learning_curve_improves()


def test_gold_checks_train_above_val():
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    fn = source.split("def learning_curve_improves")[1]
    assert "train >= valid" in fn or "train >=" in fn, \
        "verdict must include the train >= validation condition"


def test_gold_starter_raises():
    with pytest.raises(NotImplementedError):
        starter.learning_curve_improves()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
