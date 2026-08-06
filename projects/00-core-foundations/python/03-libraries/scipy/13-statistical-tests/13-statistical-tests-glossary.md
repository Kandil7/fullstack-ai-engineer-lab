# Statistical Tests — Glossary 13

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Alpha (α) | Concept | Type-I error budget; the significance threshold, usually 0.05 |
| ANOVA | Test | One F-test that k group means are equal |
| Benjamini-Hochberg | Method | FDR correction: controls the proportion of false discoveries |
| Bonferroni | Method | p × k correction: family-wise error, conservative |
| Chi-square | Test | Count-data tests: goodness of fit and contingency |
| Cohen's d | Measure | Standardized effect size: mean diff / pooled std |
| Contingency table | Data | Counts of row×column categories for independence testing |
| Effect size | Concept | How big the effect is, independent of n |
| F-statistic | Statistic | ANOVA's test statistic: between-group / within-group variance |
| Family-wise error | Concept | Chance of ≥1 false positive across a set of tests |
| H0 | Concept | The null hypothesis: "no effect" |
| Mann-Whitney U | Test | Non-parametric two-sample test on ranks |
| p-value | Concept | P(data at least this extreme \| H0) |
| Paired design | Concept | Same units measured twice; removes between-subject variance |
| Power | Concept | 1 − β: probability of detecting a true effect |
| Shapiro-Wilk | Test | Normality test with strong small-sample power (n < 5000) |
| Type I error | Concept | False positive: rejecting a true H0 (rate = α) |
| Type II error | Concept | False negative: failing to reject a false H0 (rate = β) |
| Welch's t-test | Test | Two-sample t without the equal-variance assumption |
| Wilcoxon | Test | Non-parametric paired test (rank-based) |

## Detailed Definitions

### Alpha (α)
**Definition**: The Type-I error budget — the probability of a
false positive you tolerate. Conventionally 0.05; the decision
rule is `p < alpha`.

**Example**:
```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(42)
t, p = stats.ttest_ind(rng.normal(size=60), rng.normal(loc=0.5, size=60))
print(p < 0.05)     # decision
```

**Complexity**: —.
**Related**: p-value, Type I error

---

### ANOVA
**Definition**: `stats.f_oneway(*groups)` — one F-test asking
whether k group means are equal, avoiding the error inflation of
pairwise t-tests.

**Example**:
```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(0)
F, p = stats.f_oneway(rng.normal(size=50), rng.normal(size=50),
                      rng.normal(loc=1.5, size=50))
print(f"F={F:.3f} p={p:.2e}")
```

**Complexity**: O(n·k).
**Related**: F-statistic, Kruskal-Wallis (`kruskal`)

---

### Benjamini-Hochberg
**Definition**: False-discovery-rate correction: sort p-values,
scale by k/rank, enforce monotonicity. Controls the expected
proportion of false positives among rejections — the screening
default.

**Example**:
```python
import numpy as np

def benjamini_hochberg(pvals):
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p)
    adj = p[order] * p.size / np.arange(1, p.size + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    out = np.empty_like(adj)
    out[order] = np.minimum(adj, 1.0)
    return out

print(benjamini_hochberg(np.array([0.01, 0.04, 0.05])))
# [0.03 0.05 0.05]
```

**Complexity**: O(k log k) — the sort.
**Related**: Bonferroni, Family-wise error

---

### Bonferroni
**Definition**: The simplest multiple-comparison correction:
`p_corrected = min(1, p · k)`. Controls the family-wise error
rate; conservative when k is large.

**Example**:
```python
import numpy as np

pvals = np.array([0.01, 0.5, 0.001])
print(np.minimum(1.0, pvals * 3))    # [0.03 1.   0.003]
```

**Complexity**: O(k).
**Related**: Benjamini-Hochberg, Family-wise error

---

### Chi-square
**Definition**: Count-data tests. `stats.chisquare(obs)` tests
goodness of fit (uniform expected by default);
`stats.chi2_contingency(table)` tests independence of two
categorical variables.

**Example**:
```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(1)
_, obs = np.unique(rng.integers(1, 7, size=600), return_counts=True)
print(stats.chisquare(obs))          # fair die: p large

table = np.array([[120, 80], [70, 130]])
print(stats.chi2_contingency(table))  # p ~ 1e-6
```

**Complexity**: O(k) / O(cells).
**Related**: Contingency table

---

### Cohen's d
**Definition**: Standardized effect size:
`(m1 − m2) / pooled_std`. Conventions: 0.2 small, 0.5 medium,
0.8 large. The number that survives sample-size inflation.

**Example**:
```python
import numpy as np

def cohen_d(g1, g2):
    n1, n2 = g1.size, g2.size
    vp = ((n1 - 1) * g1.var(ddof=1) + (n2 - 1) * g2.var(ddof=1)) / (n1 + n2 - 2)
    return (g1.mean() - g2.mean()) / np.sqrt(vp)

rng = np.random.default_rng(2)
print(cohen_d(rng.normal(size=100), rng.normal(loc=0.5, size=100)))
```

**Complexity**: O(n).
**Related**: Effect size, Power

---

### Contingency table
**Definition**: `table[i, j]` = count of rows in category i and
column category j. The input to `chi2_contingency`; expected
counts under independence = `outer(row_sums, col_sums) / total`.

**Example**:
```python
import numpy as np
from scipy import stats

table = np.array([[120, 80], [70, 130]])
chi2, p, dof, expected = stats.chi2_contingency(table)
print(expected)      # [[100. 100.] [90. 110.]]
```

**Complexity**: O(cells).
**Related**: Chi-square

---

### Effect size
**Definition**: The magnitude of the difference in
standard-deviation units — independent of sample size. p-values
shrink with n; effect sizes don't. Report both.

**Example**:
```python
import numpy as np

d = 0.5  # medium effect
```

**Complexity**: —.
**Related**: Cohen's d, Power

---

### F-statistic
**Definition**: ANOVA's test statistic — ratio of between-group
variance to within-group variance. Large F (small p) means the
group means differ more than sampling noise explains.

**Example**:
```python
from scipy import stats

F, p = stats.f_oneway([1, 2, 3], [4, 5, 6])
print(F)          # large, p small
```

**Complexity**: —.
**Related**: ANOVA

---

### Family-wise error
**Definition**: The probability of at least one false positive
across a set of k tests. For independent tests at alpha:
`1 − (1 − alpha)^k` — 20 tests at 0.05 → ~64% chance of a
phantom discovery.

**Example**:
```python
k = 20
alpha = 0.05
print(1 - (1 - alpha) ** k)   # ~0.642
```

**Complexity**: O(1).
**Related**: Bonferroni, Benjamini-Hochberg

---

### H0
**Definition**: The null hypothesis — "no effect". Every test
computes how surprising the data is under H0; p is the surprise
meter. Reject H0 when p < alpha.

**Example**:
```python
# H0: the mean equals 50
from scipy import stats
print(stats.ttest_1samp([51, 52, 49, 50, 53], popmean=50))
```

**Complexity**: —.
**Related**: p-value, Alpha

---

### Mann-Whitney U
**Definition**: Non-parametric two-sample test: ranks instead of
means. Assumes ordinal data and same-shaped distributions — no
normality. The skewed-data replacement for `ttest_ind`.

**Example**:
```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(3)
U, p = stats.mannwhitneyu(rng.exponential(size=80),
                          rng.exponential(scale=1.3, size=80))
print(f"U={U:.0f} p={p:.4f}")
```

**Complexity**: O(n log n) — ranking.
**Related**: Wilcoxon, t-test

---

### p-value
**Definition**: The probability of observing data at least this
extreme, **assuming H0 is true**. Not P(H0); not the effect size;
not a proof.

**Example**:
```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(4)
_, p = stats.ttest_ind(rng.normal(size=60), rng.normal(size=60))
print(p)      # likely > 0.05: no effect found
```

**Complexity**: —.
**Related**: H0, Alpha

---

### Paired design
**Definition**: Same units measured twice (before/after, model A
vs B on the same questions). Removes between-subject variance —
`ttest_rel`/`wilcoxon` become far more powerful than their
unpaired siblings on the same data.

**Example**:
```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(5)
before = rng.normal(100, 10, 40)
after = before + rng.normal(4, 5, 40)
print(stats.ttest_rel(before, after))
```

**Complexity**: O(n).
**Related**: Wilcoxon, t-test

---

### Power
**Definition**: 1 − β — the probability of detecting an effect of
a given size at a given n. Power analysis computes the sample
size before the experiment: `n ≈ 2(z_{1−α/2} + z_β)² / d²`.

**Example**:
```python
from scipy import stats

z_alpha2 = stats.norm.ppf(1 - 0.05 / 2)
z_beta = stats.norm.ppf(0.8)
n = 2.0 * (z_alpha2 + z_beta) ** 2 / 0.5 ** 2
print(f"{n:.1f}")     # ~62.8 per group
```

**Complexity**: O(1).
**Related**: Effect size, Type II error

---

### Shapiro-Wilk
**Definition**: `stats.shapiro(x)` — the strongest normality test
at small n (n < 5000). Returns (W, p); `p < 0.05` rejects
normality.

**Example**:
```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(6)
print(stats.shapiro(rng.normal(size=300)))    # p ~ 0.4
print(stats.shapiro(rng.uniform(size=300)))   # p ~ 1e-8
```

**Complexity**: O(n).
**Related**: t-test assumptions

---

### Type I error
**Definition**: False positive — rejecting a true H0. Rate is
alpha by construction. The cost of a phantom discovery:
deploying a feature that does nothing.

**Example**:
```python
alpha = 0.05
print(alpha)      # the Type-I budget you choose
```

**Complexity**: —.
**Related**: Alpha, Type II error

---

### Type II error
**Definition**: False negative — failing to reject a false H0.
Rate is beta; power = 1 − beta. Costs a real discovery:
shipping nothing when the feature works.

**Example**:
```python
beta = 0.2
print(1 - beta)   # power 0.8
```

**Complexity**: —.
**Related**: Power, Type I error

---

### Welch's t-test
**Definition**: The two-sample t-test without the equal-variance
assumption — `ttest_ind`'s default (`equal_var=False`). The safe
default because unequal variances are the norm in real groups.

**Example**:
```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(7)
print(stats.ttest_ind(rng.normal(size=50), rng.normal(size=60)))
```

**Complexity**: O(n).
**Related**: t-test, Mann-Whitney U

---

### Wilcoxon
**Definition**: `stats.wilcoxon(x, y, method="approx")` — the
rank-based paired test, sibling of `ttest_rel` for
non-normal differences.

**Example**:
```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(8)
before = rng.normal(100, 10, 40)
after = before + rng.exponential(4, 40)     # skewed deltas
print(stats.wilcoxon(before, after, method="approx"))
```

**Complexity**: O(n log n).
**Related**: Paired design, Mann-Whitney U

## Key Concepts Summary

### The decision framework
- H0 → statistic → p-value → `p < alpha` decision.
- p is P(data | H0); report effect size alongside it.

### The test menu
- Means, normal data: t-tests, ANOVA.
- Skewed/ordinal data: Mann-Whitney, Kruskal, Wilcoxon.
- Counts: chisquare GOF, chi2_contingency.

### Assumptions and corrections
- Check normality (shapiro) before parametric tests.
- Correct for multiple tests: Bonferroni (few) or BH (screening).

### Sizing experiments
- Cohen's d for magnitude; sample_size_t2 for n before you run.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. p-value — ___
2. Welch's t-test — ___
3. Benjamini-Hochberg — ___
4. Power — ___
5. Type I error — ___
6. Cohen's d — ___

**Answers:**
1. c, 2. e, 3. a, 4. f, 5. b, 6. d

a. FDR correction controlling the proportion of false discoveries
b. Rejecting a true H0; rate is alpha
c. P(data at least this extreme | H0)
d. Standardized mean difference in standard-deviation units
e. Two-sample t without the equal-variance assumption
f. 1 − β: the probability of detecting a true effect

---

**Related docs:** [scipy.stats](https://docs.scipy.org/doc/scipy/reference/stats.html) ·
[Back to lecture](13-statistical-tests-lecture.md)
