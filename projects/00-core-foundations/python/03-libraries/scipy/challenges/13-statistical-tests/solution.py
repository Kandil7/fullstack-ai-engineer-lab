"""Challenge 13: Statistical Tests — reference solution.

Normality-gated test selection, Bonferroni/BH corrections, and a
full A/B report. No Python loops anywhere.
"""

import numpy as np
from scipy import stats


def test_groups(a: np.ndarray, b: np.ndarray) -> tuple[float, float, str]:
    """Return (statistic, p, name) — 't' if both groups are normal, else 'u'."""
    pa = stats.shapiro(a).pvalue
    pb = stats.shapiro(b).pvalue
    if pa >= 0.05 and pb >= 0.05:
        stat, p = stats.ttest_ind(a, b)
        return float(stat), float(p), "t"
    stat, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    return float(stat), float(p), "u"


def multiple_comparisons(pvals: np.ndarray, method: str) -> np.ndarray:
    """Correct p-values by 'bonferroni' or 'fdr_bh'."""
    p = np.asarray(pvals, dtype=float)
    k = p.size
    if method == "bonferroni":
        return np.minimum(1.0, p * k)
    if method == "fdr_bh":
        order = np.argsort(p)
        adj = p[order] * k / np.arange(1, k + 1)
        adj = np.minimum.accumulate(adj[::-1])[::-1]
        corrected = np.empty_like(adj)
        corrected[order] = np.minimum(adj, 1.0)
        return corrected
    raise ValueError(f"unknown method: {method!r}")


def _cohen_d(g1: np.ndarray, g2: np.ndarray) -> float:
    n1, n2 = g1.size, g2.size
    vp = ((n1 - 1) * g1.var(ddof=1) + (n2 - 1) * g2.var(ddof=1)) / (n1 + n2 - 2)
    return float((g1.mean() - g2.mean()) / np.sqrt(vp))


def ab_report(control: np.ndarray, treatment: np.ndarray,
              paired: bool = False) -> tuple[float, float, str, str]:
    """Return (p, effect_size, test_name, decision)."""
    if paired:
        diffs = treatment - control
        if stats.shapiro(diffs).pvalue >= 0.05:
            stat, p = stats.ttest_rel(control, treatment)
            name = "ttest_rel"
        else:
            stat, p = stats.wilcoxon(control, treatment, method="approx")
            name = "wilcoxon"
        effect = float(diffs.mean() / diffs.std(ddof=1))
    else:
        pa = stats.shapiro(control).pvalue
        pb = stats.shapiro(treatment).pvalue
        if pa >= 0.05 and pb >= 0.05:
            stat, p = stats.ttest_ind(control, treatment)
            name = "t"
        else:
            stat, p = stats.mannwhitneyu(control, treatment,
                                         alternative="two-sided")
            name = "u"
        effect = _cohen_d(control, treatment)
    decision = "significant" if p < 0.05 else "not significant"
    return float(p), effect, name, decision
