"""Challenge 13: Statistical Tests — correctness and edge cases.

Run from the module root:
    python -m pytest 03-libraries/scipy/challenges/13-statistical-tests/test_challenge.py -v
"""

import ast
import importlib.util
import os

import numpy as np
import pytest
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Unique module names per challenge dir: several test files share the
# filenames solution.py/starter.py, and sys.modules caching would make
# the first import win when pytest runs multiple challenge dirs at once.
solution = _load("solution_13", os.path.join(HERE, "solution.py"))
starter = _load("starter_13", os.path.join(HERE, "starter.py"))


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


def _normal(n=200, shift=0.0, seed=42):
    return np.random.default_rng(seed).normal(loc=shift, size=n)


def _skewed(n=200, scale=1.0, seed=7):
    return np.random.default_rng(seed).exponential(scale=scale, size=n)


# ---------------------------------------------------------------- bronze

def test_bronze_normal_groups_use_t():
    a, b = _normal(), _normal(seed=1)
    stat, p, name = solution.test_groups(a, b)
    assert name == "t"
    ref = stats.ttest_ind(a, b)
    assert abs(stat - ref.statistic) < 1e-9
    assert abs(p - ref.pvalue) < 1e-9


def test_bronze_skewed_groups_use_u():
    a, b = _skewed(), _skewed(scale=1.4)
    stat, p, name = solution.test_groups(a, b)
    assert name == "u"
    ref = stats.mannwhitneyu(a, b, alternative="two-sided")
    assert abs(stat - ref.statistic) < 1e-9


def test_bronze_normal_shift_detected():
    a, b = _normal(), _normal(shift=1.5)
    stat, p, name = solution.test_groups(a, b)
    assert name == "t"
    assert p < 0.01


def test_bronze_identical_arrays_p_one():
    a = _normal()
    stat, p, name = solution.test_groups(a, a)
    assert name == "t"
    assert p == 1.0


def test_bronze_mixed_normality():
    # one normal, one skewed -> Mann-Whitney even though a is normal
    a, b = _normal(), _skewed()
    _, _, name = solution.test_groups(a, b)
    assert name == "u"


def test_bronze_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- silver

def test_silver_bonferroni_known():
    out = solution.multiple_comparisons(np.array([0.01, 0.5, 0.001]),
                                        "bonferroni")
    assert np.allclose(out, [0.03, 1.0, 0.003])


def test_silver_bh_known():
    out = solution.multiple_comparisons(np.array([0.01, 0.04, 0.05]),
                                        "fdr_bh")
    assert np.allclose(out, [0.03, 0.05, 0.05])


def test_silver_bh_monotone_when_sorted():
    rng = np.random.default_rng(0)
    p = np.sort(rng.uniform(size=50))
    out = solution.multiple_comparisons(p, "fdr_bh")
    assert np.all(np.diff(out) >= -1e-12)
    assert out.min() >= 0.0 and out.max() <= 1.0


def test_silver_random_bonferroni_equals_manual():
    rng = np.random.default_rng(1)
    p = rng.uniform(size=30)
    out = solution.multiple_comparisons(p, "bonferroni")
    assert np.allclose(out, np.minimum(1.0, p * 30))


def test_silver_rejects_unknown_method():
    with pytest.raises(ValueError):
        solution.multiple_comparisons(np.array([0.1, 0.2]), "holm")


def test_silver_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- gold

def test_gold_unpaired_normal_report():
    a, b = _normal(n=80), _normal(n=80, shift=1.0)
    p, effect, name, decision = solution.ab_report(a, b)
    assert name == "t"
    assert decision == "significant"
    assert abs(effect) > 0.5  # sign follows control - treatment; magnitude matters


def test_gold_unpaired_skewed_report():
    a, b = _skewed(n=80), _skewed(n=80, scale=1.4)
    p, effect, name, decision = solution.ab_report(a, b)
    assert name == "u"
    assert decision == "significant"


def test_gold_identical_not_significant():
    a = _normal(n=80)
    p, effect, name, decision = solution.ab_report(a, a)
    assert name == "t"
    assert p == 1.0
    assert decision == "not significant"
    assert abs(effect) < 0.3


def test_gold_paired_normal_uses_rel():
    rng = np.random.default_rng(5)
    before = rng.normal(100.0, 10.0, 100)
    after = before + rng.normal(0.5, 3.0, 100)
    p, effect, name, decision = solution.ab_report(before, after, paired=True)
    assert name == "ttest_rel"
    assert decision == "significant"
    assert effect > 0.0


def test_gold_paired_skewed_diffs_use_wilcoxon():
    rng = np.random.default_rng(6)
    before = rng.normal(100.0, 10.0, 100)
    after = before + rng.exponential(3.0, 100)      # skewed diffs
    p, effect, name, decision = solution.ab_report(before, after, paired=True)
    assert name == "wilcoxon"
    assert decision == "significant"


def test_gold_paired_finds_what_unpaired_misses():
    # large between-subject variance hides a small true effect unpaired
    rng = np.random.default_rng(8)
    before = rng.normal(100.0, 20.0, 120)
    after = before + rng.normal(0.4, 2.0, 120)
    p_paired, _, name_p, _ = solution.ab_report(before, after, paired=True)
    p_unpaired, _, name_u, _ = solution.ab_report(before, after, paired=False)
    assert name_p == "ttest_rel"
    assert p_paired < 0.05
    assert name_u == "t"
    assert p_unpaired > 0.05


def test_gold_no_python_loops():
    _assert_no_python_loops(solution)


# ---------------------------------------------------------------- starter

def test_starter_raises_not_implemented():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([1.0, 2.0, 4.0])
    with pytest.raises(NotImplementedError):
        starter.test_groups(a, b)
    with pytest.raises(NotImplementedError):
        starter.multiple_comparisons(np.array([0.1, 0.2]), "bonferroni")
    with pytest.raises(NotImplementedError):
        starter.ab_report(a, b)
