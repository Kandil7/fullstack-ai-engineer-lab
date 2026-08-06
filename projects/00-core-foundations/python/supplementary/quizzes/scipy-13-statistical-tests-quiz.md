# SciPy 13 — Statistical Tests Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1.** A p-value of 0.03 from a two-sample t-test means:

- A) There is a 3% chance the null hypothesis is true
- B) Under H0, data at least this extreme would occur 3% of the time
- C) The effect is 3% likely to be a real improvement
- D) The probability of a Type II error is 3%

**E2.** Which test is the rank-based (non-parametric) sibling of the paired t-test?

- A) `mannwhitneyu`
- B) `wilcoxon`
- C) `f_oneway`
- D) `chi2_contingency`

**E3 (code-output).** What prints?
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
a = rng.normal(size=50)
print(stats.ttest_ind(a, a).pvalue)
```

- A) `nan`
- B) `1.0`
- C) `0.5`
- D) `0.0`

**E4.** Which function checks whether data looks normally distributed?

- A) `stats.normaltest`
- B) `stats.ttest_1samp`
- C) `stats.pearsonr`
- D) `stats.describe`

**E5.** `stats.mannwhitneyu(a, b)` is preferred over `stats.ttest_ind(a, b)` when:

- A) the sample sizes are exactly equal
- B) the data is skewed or ordinal — the normality assumption fails
- C) there are three or more groups
- D) the data is paired

**E6 (code-output).** What prints?
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
x = rng.normal(size=300)
y = 2.0 * x + rng.normal(scale=0.3, size=300)
r, p = stats.pearsonr(x, y)
print(round(r, 2), p < 0.05)
```

- A) `0.99`, `True`
- B) `0.50`, `False`
- C) `2.00`, `True`
- D) `0.99`, `False`

---

## Medium

**M1.** You run 20 independent tests at alpha = 0.05 under the null. The expected number of false positives is:

- A) 0 — alpha prevents them
- B) exactly 1
- C) about 1 (≈20 × 0.05), with ~64% chance of at least one
- D) 20 × 0.05² = 0.05

**M2 (code-output).** What prints?
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
g1 = rng.normal(size=50)
g2 = rng.normal(size=50)
g3 = rng.normal(loc=2.0, size=50)
F, p = stats.f_oneway(g1, g2, g3)
print(p < 0.05, F > 0)
```

- A) `True`, `True`
- B) `True`, `False`
- C) `False`, `True`
- D) `False`, `False`

**M3.** `np.unique(observed, return_counts=True)` returns:

- A) `(counts, values)` — counts first
- B) `(values, counts)` — values first
- C) `(values, counts, indices)` — three arrays
- D) `counts` only

**M4 (code-output).** What prints?
```python
import numpy as np
pvals = np.array([0.01, 0.5, 0.001])
print(np.minimum(1.0, pvals * 3))
```

- A) `[0.03 1.5  0.003]`
- B) `[0.03 1.   0.003]`
- C) `[0.01 0.5  0.001]`
- D) `[0.03 0.5  0.003]`

**M5.** Cohen's d = 0.8 means:

- A) 80% of the observations differ between groups
- B) the group means are 0.8 pooled standard deviations apart — a large effect
- C) the p-value must be below 0.8
- D) the sample size needed is 80

**M6 (code-output).** What prints?
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(3)
u1 = rng.exponential(scale=1.0, size=100)
u2 = rng.exponential(scale=1.0, size=100)
U, p = stats.mannwhitneyu(u1, u2, alternative="two-sided")
print(p > 0.05)
```

- A) `True`
- B) `False`
- C) `nan`
- D) raises — equal scales are invalid

**M7.** Why does `ttest_rel` beat `ttest_ind` on paired data?

- A) It doubles the sample size
- B) It tests the differences, removing between-subject variance
- C) It always uses more assumptions, so it is stricter
- D) It is faster — the differences are smaller numbers

**M8 (code-output).** What prints?
```python
import numpy as np
from scipy import stats
table = np.array([[120, 80], [70, 130]])
chi2, p, dof, expected = stats.chi2_contingency(table)
print(round(chi2, 1), p < 0.01, dof)
```

- A) `24.1`, `True`, `1`
- B) `24.1`, `True`, `3`
- C) `5.0`, `False`, `1`
- D) `24.1`, `True`, `2`

**M9.** A normality test on n = 100,000 samples returns p = 1e-9. The correct interpretation:

- A) The t-test is definitely invalid — abandon parametric tests
- B) With huge n, trivial deviations become significant; check a histogram/QQ plot and effect size before panicking
- C) The data is exactly normal — p is a type error
- D) Switch to chi-square immediately

---

## Hard

**H1.** Which pair of actions correctly addresses the multiple-comparisons problem in feature screening (500 features)?

- A) Use alpha = 0.05 per feature; reject individually
- B) Apply Benjamini-Hochberg to the 500 p-values; report FDR-controlled discoveries
- C) Divide alpha by the number of *significant* results
- D) Run Bonferroni, but only on features with p < 0.01 first

**H2 (code-output).** What prints?
```python
import numpy as np
p = np.array([0.01, 0.04, 0.05])
order = np.argsort(p)
adj = p[order] * 3 / np.arange(1, 4)
adj = np.minimum.accumulate(adj[::-1])[::-1]
print(adj)
```

- A) `[0.03 0.06 0.05]`
- B) `[0.03 0.05 0.05]`
- C) `[0.01 0.04 0.05]`
- D) `[0.03 0.12 0.15]`

**H3.** You compare two models on 1000 questions (paired per-question scores, skewed differences). The right test and correction:

- A) `ttest_ind` on the two score arrays — scores are large so CLT applies
- B) `wilcoxon` on the paired scores, no correction needed (one test)
- C) `mannwhitneyu` on the two score arrays — non-parametric and paired
- D) `ttest_rel` — the differences are skewed so the t is invalid anyway

**H4.** Power analysis says n = 63/group for d = 0.5 at power 0.8. You can only afford 30/group. What should you do?

- A) Run the experiment; the p-value will still be correct — significance is unaffected by power
- B) Reconsider the effect size, increase the measurement precision, or accept the low power; report the power honestly
- C) Lower alpha to 0.01 to compensate
- D) Run 30/group but use a one-tailed test — it doubles power for free

**H5 (code-output).** What prints?
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(4)
before = rng.normal(100.0, 20.0, 200)
after = before + rng.normal(0.3, 2.0, 200)
p_rel = stats.ttest_rel(before, after).pvalue
p_ind = stats.ttest_ind(before, after).pvalue
print(p_rel < 0.05, p_ind < 0.05)
```

- A) `True`, `True`
- B) `True`, `False`
- C) `False`, `False`
- D) `False`, `True`

---

## Answer Key

**E1 — B.** The p-value is P(data at least this extreme | H0). It assumes H0 and says nothing about H0's probability, effect size, or Type II error.
*Distractors:* A inverts the conditional (the classic crime); C confuses probability with likelihood of improvement; D conflates p with beta.

**E2 — B.** `wilcoxon` is the rank-based paired test; Mann-Whitney is the *independent* two-sample rank test.
*Distractors:* A is unpaired; C is ANOVA (3+ groups); D is for count tables.

**E3 — B.** Identical arrays → t = 0 → p = 1.0 exactly (no evidence of difference).
*Distractors:* A would come from zero variance (that's `nan` territory in a different formulation); C is the probability of heads; D would mean "always different".

**E4 — A.** `normaltest` (D'Agostino) checks normality; `shapiro` is the other one.
*Distractors:* B is a mean test; C is correlation; D is descriptive stats.

**E5 — B.** Mann-Whitney works on ranks — no normality assumption — the right choice for skewed/ordinal data.
*Distractors:* A is irrelevant (t handles unequal n); C describes ANOVA/Kruskal; D describes `ttest_rel`/`wilcoxon`.

**E6 — A.** r ≈ 0.99 for y = 2x + small noise; p is astronomically small.
*Distractors:* B is the no-correlation case; C returns the slope (2.0) as if it were r; D contradicts p for r = 0.99 at n = 300.

**M1 — C.** Expected false positives ≈ k·alpha = 1; P(at least one) = 1 − 0.95²⁰ ≈ 64%.
*Distractors:* A denies the math; B forgets it's an expectation; D misapplies the formula.

**M2 — A.** One shifted group → F large, p tiny; F is always ≥ 0 for real data.
*Distractors:* B/C/D break one or both facts.

**M3 — B.** `np.unique(x, return_counts=True)` → `(values, counts)` — swapping them silently feeds values into `chisquare` (a real bug class from the lecture).
*Distractors:* A reverses the order; C is `return_index` territory; D drops the values.

**M4 — B.** Bonferroni: p × k, capped at 1: 0.5×3 = 1.5 → 1.0.
*Distractors:* A forgets the cap; C is the raw p-values; D caps the wrong entry.

**M5 — B.** Cohen's d is mean difference / pooled std; 0.8 is the conventional "large" threshold.
*Distractors:* A misreads it as a proportion; C confuses d with alpha; D confuses d with n.

**M6 — A.** Same scale → no evidence of shift → p large (> 0.05). Deterministic with the seed.
*Distractors:* B would need a real shift; C would need degenerate data; D is false — equal scales are perfectly valid input.

**M7 — B.** The paired test reduces the problem to one-sample on differences, cancelling between-subject variance.
*Distractors:* A is false (n is the same); C inverts the assumption story; D is nonsense.

**M8 — A.** chi² = 24.07, p ≈ 9e-7, df = (2−1)(2−1) = 1.
*Distractors:* B/C/D miscompute df or chi² (df for a 2×2 table is always 1).

**M9 — B.** Shapiro-style tests at huge n flag trivial deviations; the CLT makes the t-test robust anyway. Judge severity with a histogram/QQ plot and effect size.
*Distractors:* A overreacts; C is wrong — p < 0.05 rejects exact normality, which is fine to reject; D is the wrong tool for this question.

**H1 — B.** BH controls the false discovery rate — exactly the screening scenario. Bonferroni (A is raw screening, C is circular, D is p-hacking-by-prefiltering) would kill real discoveries at 500 tests.
*Distractors:* A is the uncorrected factory; C divides by the number of *rejections* (circular); D pre-filters then corrects (bias).

**H2 — B.** BH: [0.03, 0.06, 0.05] → monotone-enforced from the right → [0.03, 0.05, 0.05].
*Distractors:* A is the pre-monotonicity values; C is raw; D is the unscaled 3/rank variant.

**H3 — B.** Paired design + skewed diffs → `wilcoxon`; one test needs no correction.
*Distractors:* A ignores pairing and skew; C is unpaired; D chooses a parametric test the data doesn't support.

**H4 — B.** Underpowered experiments waste money and produce noise; the honest options are bigger effect (better measurement), accepting low power with disclosure, or not running.
*Distractors:* A confuses validity with power; C makes it worse; D is p-hacking territory (one-tailed is only legitimate when pre-registered).

**H5 — B.** Large between-subject variance (20.0) hides the small true effect (0.3) in the unpaired test; the paired test sees the clean 0.3-difference signal.
*Distractors:* A misses the variance story; C/D contradict the paired result.

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 13](03-libraries/scipy/lectures/13-statistical-tests-lecture.md) ·
[Glossary 13](03-libraries/scipy/lectures/13-statistical-tests-glossary.md) ·
[Challenge 13](03-libraries/scipy/challenges/13-statistical-tests/README.md)
