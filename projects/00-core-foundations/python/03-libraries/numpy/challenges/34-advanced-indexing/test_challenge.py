"""Challenge 34: Advanced Indexing — correctness, edge cases, memory.

Run from the module root:
    python -m pytest 03-libraries/numpy/challenges/34-advanced-indexing/test_challenge.py -v
"""

import ast
import importlib.util
import os
import tracemalloc

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
solution = _load("solution_34", os.path.join(HERE, "solution.py"))
starter = _load("starter_34", os.path.join(HERE, "starter.py"))


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


def _call_peak(fn, *args):
    tracemalloc.start()
    result = fn(*args)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak


# ---------------------------------------------------------------- bronze

def test_bronze_basic_top2():
    scores = np.array([5.0, 1.0, 9.0, 2.0, 7.0])
    idx = solution.top_k_indices(scores, 2)
    assert set(idx.tolist()) == {2, 4}


def test_bronze_matches_full_sort_large():
    rng = np.random.default_rng(42)
    scores = rng.normal(size=100_000)
    idx = solution.top_k_indices(scores, 10)
    assert set(idx.tolist()) == set(np.argsort(scores)[-10:].tolist())


def test_bronze_ties_any_winner():
    scores = np.array([3.0, 3.0, 3.0])
    idx = solution.top_k_indices(scores, 2)
    assert idx.size == 2 and set(idx.tolist()).issubset({0, 1, 2})


def test_bronze_k_equals_n():
    scores = np.array([1.0, 5.0, 3.0, 2.0, 4.0])
    idx = solution.top_k_indices(scores, 5)
    assert set(idx.tolist()) == {0, 1, 2, 3, 4}


def test_bronze_k_zero_returns_empty():
    idx = solution.top_k_indices(np.array([1.0, 2.0]), 0)
    assert idx.size == 0


def test_bronze_memory_linear():
    rng = np.random.default_rng(1)
    scores = rng.normal(size=1_000_000)          # 8 MB
    _, peak = _call_peak(solution.top_k_indices, scores, 10)
    assert peak < 4 * 8 * scores.size            # index buffer(s) only


def test_bronze_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- silver

def test_silver_small_exact_buckets():
    v = np.array([0.0, 0.1, 0.5, 0.9, 1.0])
    labels = solution.quantile_buckets(v, 5)
    assert np.array_equal(labels, [0, 1, 2, 3, 4])


def test_silver_uniform_balance():
    rng = np.random.default_rng(0)
    v = rng.uniform(0.0, 1.0, size=10_000)
    labels = solution.quantile_buckets(v, 5)
    _, counts = np.unique(labels, return_counts=True)
    assert counts.shape == (5,)
    assert np.all(counts > 0.9 * 10_000 / 5)
    assert np.all(counts < 1.1 * 10_000 / 5)


def test_silver_normal_range_and_balance():
    rng = np.random.default_rng(2)
    v = rng.normal(size=10_000)
    labels = solution.quantile_buckets(v, 10)
    assert labels.min() == 0 and labels.max() == 9
    _, counts = np.unique(labels, return_counts=True)
    assert counts.shape == (10,)
    assert np.all(counts > 0.9 * 1000) and np.all(counts < 1.1 * 1000)


def test_silver_degenerate_data_single_bucket():
    v = np.array([1.0, 1.0, 1.0, 1.0])
    labels = solution.quantile_buckets(v, 4)
    assert np.all(labels == labels[0])


def test_silver_boundary_value_lands_after_edge():
    v = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    labels = solution.quantile_buckets(v, 5)
    # edges at 0.25/0.5/0.75 -> side="right": equal values go up a bucket
    assert labels[0] == 0 and labels[1] == 1
    assert labels[2] == 2 and labels[3] == 3 and labels[4] == 4


def test_silver_memory_ok():
    rng = np.random.default_rng(3)
    v = rng.uniform(size=1_000_000)
    _, peak = _call_peak(solution.quantile_buckets, v, 20)
    assert peak < 6 * v.nbytes


def test_silver_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- gold

def _gold_data(seed=42, n=5000, d=32):
    rng = np.random.default_rng(seed)
    return rng.normal(size=(n, d))


def test_gold_finds_exact_copy_row():
    X = _gold_data()
    query = X[123].copy()
    idx = solution.retrieve_nearest(X, query, 5)
    assert 123 in idx.tolist()


def test_gold_matches_full_sort_reference():
    rng = np.random.default_rng(7)
    X = _gold_data(seed=1)
    query = rng.normal(size=X.shape[1])
    k = 20
    idx = solution.retrieve_nearest(X, query, k)
    dist = np.linalg.norm(X - query, axis=1)
    truth = set(np.argsort(dist)[:k].tolist())
    assert set(idx.tolist()) == truth


def test_gold_duplicates_both_may_appear():
    X = np.vstack([np.zeros(8), np.zeros(8), np.ones(8)])
    idx = solution.retrieve_nearest(X, np.zeros(8), 2)
    # both zero rows are distance-0 ties; either is a valid winner
    assert idx.size == 2
    assert 2 not in idx.tolist()  # the ones-row is strictly farther


def test_gold_k_exceeds_n():
    X = _gold_data(n=10, d=4)
    idx = solution.retrieve_nearest(X, np.zeros(4), 100)
    assert idx.size == 10
    assert set(idx.tolist()) == set(range(10))


def test_gold_k_zero_returns_empty():
    X = _gold_data(n=10, d=4)
    idx = solution.retrieve_nearest(X, np.zeros(4), 0)
    assert idx.size == 0


def test_gold_memory_bounded():
    X = _gold_data(seed=3, n=5000, d=32)         # 1.28 MB float64
    query = np.zeros(X.shape[1])
    _, peak = _call_peak(solution.retrieve_nearest, X, query, 20)
    assert peak < 3 * X.nbytes + 32 * X.shape[0]


def test_gold_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- starter

def test_starter_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        starter.top_k_indices(np.array([1.0, 2.0, 3.0]), 2)
    with pytest.raises(NotImplementedError):
        starter.quantile_buckets(np.array([0.0, 0.5, 1.0]), 4)
    with pytest.raises(NotImplementedError):
        starter.retrieve_nearest(np.eye(3), np.zeros(3), 2)
