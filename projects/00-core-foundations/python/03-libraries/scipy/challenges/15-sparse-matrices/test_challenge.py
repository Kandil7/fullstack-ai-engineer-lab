"""Challenge 15: Sparse Matrices — correctness, memory guards, edges.

Run from the module root:
    python -m pytest 03-libraries/scipy/challenges/15-sparse-matrices/test_challenge.py -v
"""

import ast
import importlib.util
import os
import tracemalloc

import numpy as np
import pytest
from scipy import sparse as sp

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Unique module names per challenge dir: several test files share the
# filenames solution.py/starter.py, and sys.modules caching would make
# the first import win when pytest runs multiple challenge dirs at once.
solution = _load("solution_15", os.path.join(HERE, "solution.py"))
starter = _load("starter_15", os.path.join(HERE, "starter.py"))


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


def _anchor_docs(n_each=1000, seed=7):
    """n_each docs per class; class A carries 'anchor_a', B 'anchor_b'."""
    rng = np.random.default_rng(seed)
    vocab = [f"w{i}" for i in range(5000)]
    docs = []
    for i in range(2 * n_each):
        toks = rng.choice(vocab, size=15, replace=True)
        toks = np.append(toks, "anchor_a" if i < n_each else "anchor_b")
        docs.append(" ".join(toks))
    return docs


# ---------------------------------------------------------------- bronze

def test_bronze_stats_coo():
    coo = sp.coo_matrix(
        (np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
         (np.array([0, 1, 2, 0, 3]), np.array([0, 1, 2, 2, 1]))),
        shape=(4, 3))
    s = solution.sparse_stats(coo)
    assert s["nnz"] == 5
    assert s["density"] == pytest.approx(5 / 12)
    assert s["bytes"] == 5 * 8 + 5 * 4 + 5 * 4          # data+idx+ptr
    assert s["shape"] == (4, 3)


def test_bronze_stats_counts_stored_zeros():
    coo = sp.coo_matrix((np.array([1.0, 0.0, 2.0]),
                         (np.array([0, 1, 2]), np.array([0, 1, 2]))),
                        shape=(3, 3))
    s = solution.sparse_stats(coo)
    assert s["nnz"] == 3, "explicit zeros count until eliminate_zeros()"


def test_bronze_stats_csc_matches_csr():
    coo = sp.coo_matrix(
        (np.array([1.0, 2.0, 3.0]),
         (np.array([0, 1, 2]), np.array([2, 0, 1]))), shape=(3, 3))
    assert solution.sparse_stats(coo.tocsr()) == \
        solution.sparse_stats(coo.tocsc())


def test_bronze_stats_round_trip_truth():
    rng = np.random.default_rng(0)
    coo = sp.random(50, 30, density=0.2, format="coo", random_state=0,
                    data_rvs=lambda k: rng.uniform(1.0, 2.0, size=k))
    s = solution.sparse_stats(coo)
    assert s["nnz"] == coo.nnz
    assert s["density"] == pytest.approx(0.2, abs=1e-6)
    assert s["bytes"] > 0 and s["shape"] == (50, 30)


# ---------------------------------------------------------------- silver

def test_silver_row_normalize_units():
    rng = np.random.default_rng(1)
    X = sp.random(5, 4, density=0.5, format="csr", random_state=1,
                  data_rvs=lambda k: rng.uniform(0.1, 1.0, size=k))
    Xn = solution.row_normalize_csr(X)
    l2 = np.asarray(Xn.power(2).sum(axis=1)).ravel() ** 0.5
    assert isinstance(Xn, sp.csr_matrix)
    assert np.allclose(l2, 1.0, atol=1e-9)
    assert Xn.nnz == X.nnz, "normalization must not densify"


def test_silver_row_normalize_zero_row_raises():
    X = sp.csr_matrix(np.array([[1.0, 0.0], [0.0, 0.0]]))
    with pytest.raises(ValueError):
        solution.row_normalize_csr(X)


def test_silver_row_normalize_accepts_csc():
    rng = np.random.default_rng(2)
    Xcsc = sp.random(4, 5, density=0.6, format="csc", random_state=2,
                     data_rvs=lambda k: rng.uniform(0.1, 1.0, size=k))
    Xn = solution.row_normalize_csr(Xcsc)
    l2 = np.asarray(Xn.power(2).sum(axis=1)).ravel() ** 0.5
    assert isinstance(Xn, sp.csr_matrix)
    assert np.allclose(l2, 1.0, atol=1e-9)


def test_silver_sparse_dot_matches_dense():
    rng = np.random.default_rng(3)
    A = sp.random(60, 50, density=0.1, format="csr", random_state=3,
                  data_rvs=lambda k: rng.uniform(0.0, 1.0, size=k))
    B = sp.random(50, 40, density=0.1, format="csr", random_state=4,
                  data_rvs=lambda k: rng.uniform(0.0, 1.0, size=k))
    C = solution.sparse_dot(A, B)
    assert isinstance(C, sp.csr_matrix)
    assert np.allclose(C.toarray(), A.toarray() @ B.toarray(), atol=1e-12)


def test_silver_sparse_dot_shape_mismatch_raises():
    A = sp.eye(3, format="csr")
    B = sp.eye(4, format="csr")
    with pytest.raises(ValueError):
        solution.sparse_dot(A, B)


# ---------------------------------------------------------------- gold

def test_gold_retrieval_anchor_a():
    docs = _anchor_docs()
    idx = solution.tfidf_retrieval(docs, "anchor_a", top_k=3)
    assert idx.dtype.kind == "i" and idx.shape == (3,)
    assert np.all(idx < 1000), "query 'anchor_a' must rank class A first"


def test_gold_retrieval_anchor_b():
    docs = _anchor_docs()
    idx = solution.tfidf_retrieval(docs, "anchor_b", top_k=3)
    assert np.all(idx >= 1000)


def test_gold_retrieval_ordering():
    docs = _anchor_docs()
    idx = solution.tfidf_retrieval(docs, "anchor_a", top_k=5)
    assert len(set(idx.tolist())) == 5, "indices must be distinct"


def test_gold_retrieval_memory_guard():
    """Corpus matrix is 2000x~5000 = 80 MB dense; peak must stay < 10 MB."""
    docs = _anchor_docs()
    tracemalloc.start()
    solution.tfidf_retrieval(docs, "anchor_a", top_k=3)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak < 10e6, f"retrieval densified the corpus: peak={peak / 1e6:.1f} MB"


def test_gold_spsolve_residual():
    n = 2000
    x = solution.solve_sparse_system(n)
    A = sp.diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(n, n), format="csr")
    assert np.max(np.abs(A @ x - np.ones(n))) < 1e-8


def test_gold_spsolve_closed_form():
    """x[i] = i * (n + 1 - i) / 2 for the tridiagonal L+2I."""
    n = 500
    x = solution.solve_sparse_system(n)
    expected = np.arange(1, n + 1) * (n + 1 - np.arange(1, n + 1)) / 2.0
    assert np.allclose(x, expected, rtol=1e-6)


def test_gold_spsolve_memory_guard():
    """Dense A at n=2000 is 32 MB; sparse solve must stay < 5 MB."""
    tracemalloc.start()
    solution.solve_sparse_system(2000)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak < 5e6, f"solve densified: peak={peak / 1e6:.2f} MB"


def test_gold_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- starter

def test_starter_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        starter.sparse_stats(sp.eye(3))
    with pytest.raises(NotImplementedError):
        starter.row_normalize_csr(sp.eye(3))
    with pytest.raises(NotImplementedError):
        starter.sparse_dot(sp.eye(3), sp.eye(3))
    with pytest.raises(NotImplementedError):
        starter.tfidf_retrieval(["a b", "c d"], "a")
    with pytest.raises(NotImplementedError):
        starter.solve_sparse_system(10)
