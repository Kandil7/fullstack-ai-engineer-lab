"""Challenge 16: Distance and Similarity — correctness, memory, edges.

Run from the module root:
    python -m pytest 03-libraries/scipy/challenges/16-distance-and-similarity/test_challenge.py -v
"""

import ast
import importlib.util
import os
import tracemalloc

import numpy as np
import pytest
from scipy.spatial.distance import cdist

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Unique module names per challenge dir: several test files share the
# filenames solution.py/starter.py, and sys.modules caching would make
# the first import win when pytest runs multiple challenge dirs at once.
solution = _load("solution_16", os.path.join(HERE, "solution.py"))
starter = _load("starter_16", os.path.join(HERE, "starter.py"))


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


def _rand(seed, *shape):
    return np.random.default_rng(seed).normal(size=shape)


# ---------------------------------------------------------------- bronze

def test_bronze_top1_known():
    Q = np.array([[0.0, 0.0]])
    X = np.array([[1.0, 0.0], [0.0, 3.0]])
    dist, idx = solution.nearest_brute(Q, X, k=1)
    assert idx.shape == (1, 1) and idx[0, 0] == 0
    assert np.isclose(dist[0, 0], 1.0)


def test_bronze_top3_shapes_sorted():
    rng = np.random.default_rng(0)
    Q = rng.normal(size=(2, 3))
    X = rng.normal(size=(5, 3))
    dist, idx = solution.nearest_brute(Q, X, k=3)
    assert dist.shape == (2, 3) and idx.shape == (2, 3)
    assert np.all(np.diff(dist, axis=1) >= -1e-12), "rows must be sorted"
    assert np.all(idx < 5)


def test_bronze_cosine_metric_range():
    rng = np.random.default_rng(1)
    Q = rng.normal(size=(3, 4))
    X = rng.normal(size=(10, 4))
    dist, idx = solution.nearest_brute(Q, X, k=2, metric="cosine")
    assert np.all(dist >= 0.0) and np.all(dist <= 2.0 + 1e-9)


def test_bronze_k_too_large_raises():
    with pytest.raises(ValueError):
        solution.nearest_brute(np.zeros((1, 2)), np.zeros((4, 2)), k=5)


def test_bronze_equals_cdist_directly():
    rng = np.random.default_rng(2)
    Q = rng.normal(size=(4, 5))
    X = rng.normal(size=(20, 5))
    dist, idx = solution.nearest_brute(Q, X, k=6)
    expected_idx = np.argsort(cdist(Q, X), axis=1)[:, :6]
    assert np.array_equal(idx, expected_idx)


# ---------------------------------------------------------------- silver

def test_silver_cosine_orthogonal():
    assert np.isclose(solution.cosine_pair(np.array([1.0, 0.0]),
                                           np.array([0.0, 1.0])), 1.0)


def test_silver_cosine_scale_invariant():
    assert np.isclose(solution.cosine_pair(np.array([1.0, 0.0]),
                                           np.array([5.0, 0.0])), 0.0)


def test_silver_cosine_matches_scipy():
    rng = np.random.default_rng(3)
    u = rng.normal(size=6)
    v = rng.normal(size=6)
    assert np.isclose(solution.cosine_pair(u, v),
                      cdist([u], [v], "cosine")[0, 0], atol=1e-12)


def test_silver_cosine_zero_norm_raises():
    with pytest.raises(ValueError):
        solution.cosine_pair(np.zeros(3), np.ones(3))
    with pytest.raises(ValueError):
        solution.cosine_pair(np.ones(3), np.zeros(3))


def test_silver_normalized_topk_equals_cosine_topk():
    rng = np.random.default_rng(4)
    Q = rng.normal(size=(5, 20))
    X = rng.normal(size=(50, 20))
    got = solution.normalized_topk(Q, X, k=5)
    Qn = Q / np.linalg.norm(Q, axis=1, keepdims=True)
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    expected = np.argsort(cdist(Qn, Xn, "euclidean"), axis=1)[:, :5]
    assert np.array_equal(got, expected)


def test_silver_spread_low_dim():
    rng = np.random.default_rng(5)
    V = rng.normal(size=(2000, 2))
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    assert abs(solution.spread(V) - 0.7071) < 0.05


def test_silver_spread_high_dim():
    rng = np.random.default_rng(6)
    V = rng.normal(size=(2000, 128))
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    assert abs(solution.spread(V) - 0.0884) < 0.02


# ---------------------------------------------------------------- gold

def test_gold_kd_exact_vs_brute():
    rng = np.random.default_rng(7)
    pts = rng.uniform(size=(500, 2))
    q = rng.uniform(size=(3, 2))
    dist, idx = solution.fast_neighbors(pts, q, k=3)
    expected_dist = np.sort(cdist(q, pts), axis=1)[:, :3]
    assert np.allclose(dist, expected_dist, atol=1e-12)


def test_gold_kd_large_memory_guard():
    """50k points, 1000 queries at d=2: cdist would need ~400 MB."""
    rng = np.random.default_rng(8)
    pts = rng.normal(size=(50000, 2))
    q = rng.normal(size=(1000, 2))
    tracemalloc.start()
    solution.fast_neighbors(pts, q, k=3)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak < 10e6, f"kd path densified: peak={peak / 1e6:.1f} MB"


def test_gold_kd_k_too_large_raises():
    with pytest.raises(ValueError):
        solution.fast_neighbors(np.zeros((10, 2)), np.zeros((1, 2)), k=11)


def test_gold_spread_ratio_2_128():
    r = solution.spread_ratio(2, 128)
    assert r > 4.0, f"expected ~8 (sqrt(128/2)), got {r:.2f}"


def test_gold_spread_ratio_8_32():
    r = solution.spread_ratio(8, 32)
    assert r > 1.5, f"expected ~2 (sqrt(32/8)), got {r:.2f}"


def test_gold_spread_ratio_deterministic():
    r1 = solution.spread_ratio(2, 128, seed=42)
    r2 = solution.spread_ratio(2, 128, seed=42)
    assert r1 == r2


def test_gold_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- starter

def test_starter_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        starter.nearest_brute(np.zeros((1, 2)), np.zeros((3, 2)), k=1)
    with pytest.raises(NotImplementedError):
        starter.cosine_pair(np.ones(2), np.ones(2))
    with pytest.raises(NotImplementedError):
        starter.normalized_topk(np.zeros((1, 2)), np.zeros((3, 2)), k=1)
    with pytest.raises(NotImplementedError):
        starter.spread(np.ones((4, 2)))
    with pytest.raises(NotImplementedError):
        starter.fast_neighbors(np.zeros((3, 2)), np.zeros((1, 2)), k=1)
    with pytest.raises(NotImplementedError):
        starter.spread_ratio(2, 128)
