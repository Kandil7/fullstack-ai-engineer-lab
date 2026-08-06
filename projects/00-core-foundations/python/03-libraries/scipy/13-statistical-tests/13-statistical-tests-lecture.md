# SciPy 13 — Statistical Tests: hypothesis testing beyond the t-test

## Topic Overview

"Model B is 2% better" is a claim, not a fact, until a hypothesis
test has put a number on the probability that the difference is
noise. This lecture builds the decision framework of
`scipy.stats`: when to run a t-test vs Mann-Whitney vs ANOVA vs
chi-square, how to check the assumptions each one makes, how to
correct for running many tests at once, and how to report effect
size and power so a p-value actually means something. It extends
the basics already covered in SciPy 04 (descriptive stats,
one/two-sample/paired t-tests, correlation) into the full menu of
tests you will reach for in A/B analysis, model evaluation, and
feature selection.

## Learning Objectives

By the end of this lecture you will be able to:

1. State the null hypothesis, interpret a p-value, and avoid the
   three classic misinterpretations of it.
2. Choose between parametric (t, ANOVA) and non-parametric
   (Mann-Whitney, Kruskal, Wilcoxon) tests based on data
   properties.
3. Run chi-square goodness-of-fit and contingency tests on count
   data.
4. Check normality assumptions with `shapiro`/`normaltest`.
5. Correct p-values for multiple comparisons (Bonferroni vs
   Benjamini-Hochberg) and implement both in a few lines.
6. Report Cohen's d and compute required sample sizes from power
   targets.

## Prerequisites

- SciPy 04 (statistics basics: t-tests, correlation).
- NumPy 30 (vectorization) and 32 (dtypes) — test inputs are
  arrays; seeds make them reproducible.
- A working definition of the normal distribution.

---

## Key Concepts

### 1. The workflow — hypothesis, p-value, decision, honestly

Every test follows the same shape:

1. **Null hypothesis H0:** "no effect" (means equal, variables
   independent, distribution fits).
2. **Test statistic:** a number computed from the data (t, F, U,
   chi², W).
3. **p-value:** P(statistic this extreme | H0 is true). The
   probability of seeing what you saw *if there is no effect*.
4. **Decision:** `p < alpha` (usually 0.05) → reject H0 → there
   is evidence of an effect.

The three classic p-value crimes:

- **"p is the probability H0 is true"** — wrong; p assumes H0.
- **"p < 0.05 proves the effect"** — it quantifies evidence; it
  does not prove causation or magnitude.
- **"p = 0.04 is meaningfully different from p = 0.06"** — the
  threshold is a convention, not a cliff. Report the number.

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(42)
a = rng.normal(size=60)
b = rng.normal(loc=0.5, size=60)
t, p = stats.ttest_ind(a, b)
print(f"t={t:.3f} p={p:.4f} significant={p < 0.05}")
```

**Errors:** rejecting H0 when true = Type I (false positive,
rate = alpha); failing to reject when false = Type II (rate =
beta; power = 1 − beta). Both matter — Section 9.

---

### 2. The t-test family — and the assumptions they silently make

| Test | Question | Assumption |
|---|---|---|
| `ttest_1samp` | mean equals a value? | data ~ normal |
| `ttest_ind` | two groups' means differ? | each group ~ normal; Welch version tolerates unequal variance |
| `ttest_rel` | paired before/after means differ? | *differences* ~ normal |

`ttest_ind` defaults to **Welch's** test (`equal_var=False`) —
no pooled-variance assumption, the safe default. `ttest_rel`
compares matched units (same user before/after), removing
between-subject variance — far more powerful than an independent
test on the same data.

```python
before = rng.normal(loc=100.0, scale=10.0, size=40)
after = before + rng.normal(loc=4.0, scale=5.0, size=40)
print(stats.ttest_rel(before, after))      # significant
```

**Assumption check:** if the data (or the paired differences)
look non-normal — skewed, bounded, heavy-tailed — switch to the
non-parametric column (Sections 4).

---

### 3. ANOVA — three or more groups without p-value inflation

`stats.f_oneway(*groups)` tests whether k group means are equal,
as one F-statistic. Running pairwise t-tests instead inflates the
family-wise error (k=4 groups → 6 tests → ~26% chance of at
least one false positive at alpha=0.05).

```python
g1 = rng.normal(size=50); g2 = rng.normal(size=50)
g3 = rng.normal(size=50); g4 = rng.normal(loc=1.5, size=50)
print(stats.f_oneway(g1, g2, g3))       # p large: no effect
print(stats.f_oneway(g1, g2, g3, g4))   # p ~ 1e-15: effect
```

ANOVA only says "some group differs" — post-hoc tests (Tukey,
not in `scipy.stats`) identify *which*. The non-parametric
k-group alternative is `stats.kruskal` (Kruskal-Wallis H).

---

### 4. Non-parametric two-sample — Mann-Whitney U

`stats.mannwhitneyu(a, b)` tests whether one group tends to
produce larger values, using ranks instead of means. Assumption:
the values are ordinal and the distributions have the same
shape — **no normality required**. This is the right tool for
latency, revenue, and other skewed/bounded data where t-tests
misbehave.

```python
u1 = rng.exponential(scale=1.0, size=80)
u2 = rng.exponential(scale=1.3, size=80)
print(stats.mannwhitneyu(u1, u2, alternative="two-sided"))
```

Paired rank test: `stats.wilcoxon(before, after,
method="approx")` — the non-parametric sibling of `ttest_rel`.

**Cost:** U is O(n log n)-ish (rank-based), fine up to large
samples; the p-value switches to a normal approximation for big
n, which is why large datasets often prefer it over t.

---

### 5. Chi-square — statistics on counts, not measurements

Two families:

- **Goodness of fit** — `stats.chisquare(observed)`: does the
  count distribution match expectation (uniform by default, or
  `f_exp`)?

```python
_, obs = np.unique(rng.integers(1, 7, size=600), return_counts=True)
print(stats.chisquare(obs))          # fair die: p large
```

- **Independence / contingency** — `stats.chi2_contingency(
  table)`: are two categorical variables independent? `table[i,
  j]` = count of row-category i × column-category j; returns
  (chi², p, dof, expected-table).

```python
table = np.array([[120, 80], [70, 130]])
print(stats.chi2_contingency(table))  # p ~ 1e-6: association
```

**Watch:** counts must be actual counts (not fractions);
expected cell counts below ~5 make the chi² approximation shaky
(Fisher's exact test is the small-n alternative).

---

### 6. Normality tests — checking the gate before the t-test

`stats.shapiro(x)` (W, n < 5000, strongest small-sample power)
and `stats.normaltest(x)` (D'Agostino: combines skew and
kurtosis). Both return (statistic, p); `p < 0.05` → reject
normality.

```python
print(stats.shapiro(rng.normal(size=300)))    # p ~ 0.4: normal
print(stats.shapiro(rng.uniform(size=300)))   # p ~ 1e-8: not normal
```

**Engineering judgment:** with large n (thousands+), even tiny
deviations become "significant" — normality tests flag
distributions that are functionally fine for a t-test (CLT).
Use them as a *tripwire*, then look at a histogram/QQ plot to
judge severity. When in doubt on bounded/skewed data, the
non-parametric test is never a wrong answer.

---

### 7. Correlation significance — r without p is a rumor

`stats.pearsonr(x, y)` → (r, p) for linear association;
`stats.spearmanr(x, y)` → (rho, p) for monotonic (rank)
association. A high r on 5 points is noise; p encodes how
surprising r is given n.

```python
x = rng.normal(size=200)
y = 3.0 * x + rng.normal(scale=0.5, size=200)
print(stats.pearsonr(x, y))     # r ~ 0.99, p ~ 1e-150
```

Spearman survives outliers and non-linearity that Pearson
doesn't — check both when exploring features.

---

### 8. Multiple comparisons — the silent p-value factory

Run 20 tests at alpha=0.05 under H0: expect **one false
positive** by chance. Correct before reporting:

- **Bonferroni:** `p_corrected = min(1, p · k)`. Controls the
  family-wise error rate; simple, conservative — with many
  correlated tests it throws away real discoveries.
- **Benjamini-Hochberg (FDR):** sort p-values, scale by
  `k / rank`, enforce monotonicity. Controls the *false
  discovery rate* — the expected proportion of false positives
  among rejections. The standard for feature selection and
  genome-wide-style screens.

Both are a few lines (scipy.stats no longer ships
`multipletests`; statsmodels does):

```python
def bonferroni(pvals):
    p = np.asarray(pvals, dtype=float)
    return np.minimum(1.0, p * p.size)

def benjamini_hochberg(pvals):
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p)
    adj = p[order] * p.size / np.arange(1, p.size + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]   # monotone
    out = np.empty_like(adj)
    out[order] = np.minimum(adj, 1.0)
    return out
```

In the example data, raw screening flags 4 of 10 tests; after
Bonferroni only 1 survives, BH keeps 2 — the power difference in
one line.

---

### 9. Effect size and power — the numbers that actually decide

A significant p-value with a tiny effect is a common but useless
finding at scale (n = 1M makes everything "significant").

- **Cohen's d** = `(m1 − m2) / pooled_std` — the effect in
  standard-deviation units; 0.2 small, 0.5 medium, 0.8 large.
- **Power** = 1 − beta: the probability of detecting an effect
  of size d at sample size n. Power analysis answers "how many
  users do I need before the experiment is worth running?"

Per-group sample size for a two-sample t-test (normal
approximation, equal n):

```python
from scipy import stats as st

def sample_size_t2(d, alpha=0.05, power=0.8):
    za2 = st.norm.ppf(1 - alpha / 2)
    zb = st.norm.ppf(power)
    return 2.0 * (za2 + zb) ** 2 / d ** 2

print(sample_size_t2(0.5))     # ~63 per group
```

d=0.5 needs ~63/group; d=0.2 needs ~393; halving the effect
quadruples the sample — the economics of experiments are set by
effect size, not by p-value thresholds.

---

## Common Mistakes to Avoid

1. **Interpreting p backwards** — p is not P(H0); it is
   P(data | H0).
2. **Running t-tests on skewed data** — check normality or use
   Mann-Whitney/Kruskal from the start.
3. **Pairwise t-tests for 3+ groups** — ANOVA first; post-hoc
   only after.
4. **Forgetting the `method="approx"` on `wilcoxon`** with ties
   or large n (warnings, or exact mode blowup).
5. **Chi-square on proportions** — it needs counts; and expected
   cells < 5 invalidate the approximation.
6. **Uncorrected multiple tests** — 20 screens at 0.05 ≈ one
   guaranteed phantom discovery.
7. **`np.unique(x, return_counts=True)` unpacking** — it returns
   `(values, counts)`, in that order. Swapping them feeds the
   *values* into `chisquare` and every result is silently wrong.
8. **Power-1% significance theater** — report d, and compute n
   *before* running the experiment.
9. **Normality tests on huge n** — they reject everything;
   judge effect size and look at the histogram.

---

## Best Practices

- **Report the p-value, not just the verdict** — and give d when
  p is significant.
- **Fix the seed** (`np.random.default_rng(seed)`) so every test
  run is reproducible — the whole point of the exercise files.
- **Precompute the test menu** before looking at data: is the
  question about means (t/ANOVA), ranks (U/Kruskal/Wilcoxon), or
  counts (chi²)? Is the design paired or independent?
- **Apply BH when screening many features**, Bonferroni when the
  number of tests is small and false positives are expensive.
- **Check assumptions on the *actual* data** — the same dataset
  can justify t on one column and Mann-Whitney on another.
- **Use Welch's t-test by default** (scipy's default) — no
  equal-variance assumption to defend.

---

## Complexity and Cost

| Test | Function | Cost | Notes |
|---|---|---|---|
| 1-sample t | `ttest_1samp` | O(n) | normality assumed |
| independent t | `ttest_ind` | O(n) | Welch by default |
| paired t | `ttest_rel` | O(n) | differences ~ normal |
| Mann-Whitney | `mannwhitneyu` | O(n log n) | ranks; no normality |
| Wilcoxon | `wilcoxon` | O(n log n) | paired ranks |
| ANOVA | `f_oneway` | O(n·k) | 3+ groups |
| Kruskal-Wallis | `kruskal` | O(n log n) | non-parametric ANOVA |
| Chi-square GOF | `chisquare` | O(k) | counts only |
| Contingency | `chi2_contingency` | O(cells) | expected ≥ 5 |
| Shapiro | `shapiro` | O(n) | n < 5000 |
| Pearson/Spearman | `pearsonr`/`spearmanr` | O(n)/O(n log n) | linear vs rank |
| Corrections | manual (Section 8) | O(k log k) | bonferroni / BH |
| Power/sample size | manual (Section 9) | O(1) | `norm.ppf` based |

---

## AI Engineering Relevance

- **A/B testing of model/feature changes**: `ttest_ind` on
  metric deltas; Mann-Whitney when the metric is skewed (latency,
  revenue). Power analysis decides the holdout size *before* the
  deployment.
- **Model evaluation claims**: "our RAG system answers 6% more
  correctly" is a paired design (`ttest_rel` or `wilcoxon` on
  per-question scores) — not a t-test on aggregate numbers.
- **Feature selection**: screen hundreds of features with
  `pearsonr`/`spearmanr`, then apply **BH correction** — the raw
  p-values would hand you dozens of phantom features.
- **Data quality**: `chisquare` on category distributions detects
  drift between training and serving data; `chi2_contingency`
  flags biased sampling.
- **Class balance / label sanity**: `np.unique(..., return_counts
  =True)` + `chisquare` is the standard imbalance check.
- **Evaluation pipelines**: deterministic seeds + fixed test data
  make every experiment reproducible and comparable.

---

## Practice Exercises

1. Generate `N(0,1)` vs `N(1,1)` samples (n=50 each, fixed seed);
   run `ttest_ind` and confirm p < 0.01; then run
   `mannwhitneyu` and compare verdicts.
2. Create paired before/after data with a small true effect;
   show `ttest_rel` finds it while `ttest_ind` on the same two
   arrays (unpaired) does not — and explain why.
3. Build a 3×3 contingency table with a planted association;
   verify `chi2_contingency` p < 0.05 and that the returned
   `expected` table matches `outer(row_sums, col_sums) / total`.
4. Implement Bonferroni and BH; generate 50 p-values under H0
   (uniform); show raw screening finds ~2.5 "significant" on
   average while both corrections find ~0 — the multiple-
   comparisons problem in miniature.
5. Compute the sample size for d=0.3 at power=0.8, then
   `power_t2(n)` on the result — confirm the inversion returns
   0.8.

---

## Summary

- Every test = H0 → statistic → p-value → decision; p is
  P(data | H0), nothing else.
- Parametric tests assume normality; skewed/bounded data → the
  rank-based column (U, Kruskal, Wilcoxon).
- 3+ groups → ANOVA (`f_oneway`); counts → chi-square
  (`chisquare`, `chi2_contingency`).
- Normality checks are tripwires, not oracles.
- Many tests → correct (Bonferroni for few/expensive, BH for
  screening).
- Significance is not magnitude: report Cohen's d and size the
  experiment with power analysis first.

## Quick Reference

```python
from scipy import stats as st
import numpy as np

# means
st.ttest_1samp(x, popmean=0.0)          # one sample
st.ttest_ind(a, b)                       # Welch by default
st.ttest_rel(before, after)              # paired

# 3+ groups
st.f_oneway(g1, g2, g3)                  # parametric
st.kruskal(g1, g2, g3)                   # rank-based

# non-parametric two-sample / paired
st.mannwhitneyu(a, b)                    # independent ranks
st.wilcoxon(before, after, method="approx")

# counts
st.chisquare(obs)                        # goodness of fit
st.chi2_contingency(table)               # independence

# assumptions + correlation
st.shapiro(x)                            # normality (n < 5000)
st.pearsonr(x, y); st.spearmanr(x, y)    # correlation + p

# corrections (implement: Section 8) and power (Section 9)
p_corr = bonferroni(pvals)               # min(1, p * k)
p_bh = benjamini_hochberg(pvals)
n = sample_size_t2(d=0.5, power=0.8)     # ~63 per group
```

## Next Steps

- SciPy 14 (optimization-advanced): use statistical tests to
  compare optimizer solutions on noisy objectives.
- SciPy 16 (distance and similarity): `pdist`/`cdist` give you
  the pairwise distances that feed nearest-neighbor retrieval —
  pair with the retrieval challenge from NumPy 34.
- Revisit SciPy 04 to see the descriptive layer underneath this
  lecture's tests.
