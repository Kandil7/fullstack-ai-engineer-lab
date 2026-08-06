"""Challenge 13: Statistical Tests — starter template.

Implement the three functions below. Read README.md for the
behavior contract and I/O tables.
"""

import numpy as np


def test_groups(a: np.ndarray, b: np.ndarray) -> tuple[float, float, str]:
    """Return (statistic, p, name) — 't' if both groups are normal, else 'u'."""
    raise NotImplementedError


def multiple_comparisons(pvals: np.ndarray, method: str) -> np.ndarray:
    """Correct p-values by 'bonferroni' or 'fdr_bh'."""
    raise NotImplementedError


def ab_report(control: np.ndarray, treatment: np.ndarray,
              paired: bool = False) -> tuple[float, float, str, str]:
    """Return (p, effect_size, test_name, decision)."""
    raise NotImplementedError
