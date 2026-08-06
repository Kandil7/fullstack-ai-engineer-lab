# Challenge 13: Statistical Tests — Choose, Correct, Report

Three tiers that mirror real evaluation work: Bronze picks the
right test for the data, Silver applies multiple-comparison
corrections, Gold runs a complete A/B report — test choice,
effect size, and verdict in one call.

## 🥉 Bronze — Choose the Test (~15 min)

**Task:** Implement `test_groups(a, b)` that runs a Shapiro-Wilk
normality check on both groups and returns `(statistic, p, name)`:
`("t", ...)` when both groups look normal, `("u", ...)` for
Mann-Whitney otherwise.

**Signature:**
```python
def test_groups(a: np.ndarray, b: np.ndarray) -> tuple[float, float, str]:
```

| Input | Expected |
|---|---|
| seeded normal vs normal | name `"t"`, p ≈ t-test p |
| seeded exponential vs exponential | name `"u"`, p ≈ Mann-Whitney p |
| seeded normal vs shifted normal | name `"t"` |
| identical arrays | p == 1.0 |

**Constraints:** n ≤ 2000 per group (Shapiro limit). **No Python
loops or comprehensions.**

---

## 🥈 Silver — Correct the p-values (~35 min)

**Task:** Implement `multiple_comparisons(pvals, method)` with
`method in {"bonferroni", "fdr_bh"}` returning the corrected
p-values (capped at 1).

**Signature:**
```python
def multiple_comparisons(pvals: np.ndarray, method: str) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `[0.01, 0.5, 0.001]`, `"bonferroni"` | `[0.03, 1.0, 0.003]` |
| `[0.01, 0.04, 0.05]`, `"fdr_bh"` | `[0.03, 0.05, 0.05]` |
| 50 uniform p-values, either method | all in [0, 1], none ≤ 1/k raw-screening artifacts |
| unknown method | raises `ValueError` |

**Constraints:** k ≤ 10⁵. **No Python loops or comprehensions.**
The BH output must be monotone non-decreasing when sorted.

---

## 🥇 Gold — A/B Report (~75 min)

**Task:** Implement `ab_report(control, treatment, paired=False)`
returning `(p_value, effect_size, test_name, decision)`:

- `paired=True` → `ttest_rel` if the *differences* pass Shapiro,
  else `wilcoxon`; effect size = `mean(diff)/std(diff)`.
- `paired=False` → t-test if both groups pass Shapiro, else
  Mann-Whitney; effect size = Cohen's d (pooled std).
- `decision` is `"significant"` when `p < 0.05`, else
  `"not significant"`.

**Signature:**
```python
def ab_report(control: np.ndarray, treatment: np.ndarray,
              paired: bool = False) -> tuple[float, float, str, str]:
```

| Input | Expected |
|---|---|
| seeded normal, shift 1.0, n=80, unpaired | `"t"`, significant, \|d\| > 0.5 |
| seeded skewed (exponential), shift 1.4 | `"u"`, significant |
| identical arrays | `"t"`, p == 1.0, `"not significant"` |
| paired normal diff 0.5 | `"ttest_rel"`, significant |
| paired exponential diffs | `"wilcoxon"` |

**Constraints:** n ≤ 2000. **No Python loops or comprehensions.**
`paired=True` must use the difference-based normality check, not
the raw groups'.

**Follow-up:** which of the four verdicts changes if you switch
`paired`? Why does the paired design find effects the unpaired
one misses? (Answer: between-subject variance is removed; the
paired t is a one-sample test on differences.)

---

## Running

```bash
pytest 03-libraries/scipy/challenges/13-statistical-tests/test_challenge.py -v
```

```text
collected ... items  (all tests pass against solution.py;
                      starter.py raises NotImplementedError by design)
```

## Test File Structure

```
challenges/13-statistical-tests/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Correctness + edge cases + deterministic seeds
```
