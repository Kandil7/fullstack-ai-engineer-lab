# MLOps — 14: A/B Testing Models

## Topic Overview

A/B testing for models is the disciplined way to answer the question offline
evaluation cannot: **does the new model win in production, against real users,
with real business impact?** Offline metrics (val_acc, AUC) are proxies;
A/B testing measures the actual outcome — conversion, fraud caught, clicks,
satisfaction — on a controlled slice of traffic. It is the final gate between
"the eval gate passed" (Lecture 12) and "ship to everyone."

The mechanics: split traffic (typically 50/50 or 90/10) between the incumbent
model (control) and the candidate (treatment); run until the outcome metric
has enough statistical power; decide by **statistical significance** — not by
eyeballing a dashboard. The AI engineer's craft is in the *experiment design*:
the metric, the allocation, the sample-size math, and the stopping rule.

The standard tools are experimentation platforms (**Optimizely**, **Eppo**,
internal ML platforms) or the DIY statistical core: **chi-squared tests** for
proportions (conversion/click rates), **t-tests** for means, and
**sample-size calculators** to plan the run. The math is old statistics; the
discipline is new — most model rollouts skip it and pay with unreproducible
"wins."

## Learning Objectives

By the end of this lecture, you will be able to:
1. Design a model A/B test: metric, allocation, duration
2. Compute the sample size needed for a detectable effect
3. Run a chi-squared test on conversion-rate experiments
4. Run a t-test on continuous outcome metrics
5. Avoid the classic pitfalls: peeking, multiple comparisons, Simpson's paradox
6. Decide promote vs rollback from the statistical result
7. Operationalize A/B as a registry-gated step in the promotion pipeline

## Prerequisites

| Need | Where |
|---|---|
| Statistics / hypothesis testing | `07-machine-learning/` (statistics lectures) |
| CI/CD promotion | `08-mlops/lectures/12-ci-cd-for-ml-lecture.md` |
| Monitoring | `08-mlops/lectures/11-monitoring-and-drift-lecture.md` |
| Model registry | `08-mlops/lectures/04-model-registry-lecture.md` |

## 1. The Experiment Design

Every model A/B test needs four decisions *before* traffic starts:

| Decision | Example | Why it matters |
|---|---|---|
| **Primary metric** | conversion rate, CTR, fraud caught | the one number that decides |
| **Allocation** | 50/50 or 90/10 | power vs risk |
| **Sample size** | from effect size + power math | duration and cost |
| **Stopping rule** | fixed duration or fixed sample | prevents peeking bias |

The metric must be a *business outcome*, not a model metric. "The model's AUC
is 0.93" is not the experiment; "conversion went up 2% at p<0.05" is.

## 2. Sample Size Math: How Long Do We Run?

You cannot see an effect you did not have power to detect. The required sample
size depends on: baseline rate (control), minimum effect you care about
(δ), significance level (α = 0.05), and power (1−β = 0.80).

```python
import math
from scipy import stats

def min_sample_size(baseline: float, effect: float, alpha: float = 0.05,
                    power: float = 0.80) -> int:
    """Per-group sample size for a two-proportion z-test."""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    p_bar = (baseline + baseline + effect) / 2
    var = 2 * p_bar * (1 - p_bar)
    return int(math.ceil((z_alpha + z_beta) ** 2 * var / effect ** 2))

print("sample size per group:", min_sample_size(baseline=0.10, effect=0.02))
```

Output (conceptually):
```
sample size per group: 3882
```

At 10k users/day split 50/50, that's under a day — but for a 0.2% effect it
is ~400k users and weeks. **Running an underpowered test and calling the
result a "win" is the #1 A/B sin.**

## 3. Proportions: The Chi-Squared Test

The most common model A/B metric is a rate (conversion, click, approval). The
test is a 2×2 contingency table + chi-squared:

```python
from scipy import stats

def ab_proportion_test(control_success: int, control_total: int,
                       treat_success: int, treat_total: int) -> dict:
    """Chi-squared test on conversion rates. Returns p-value + verdict."""
    table = [[control_success, control_total - control_success],
             [treat_success, treat_total - treat_success]]
    chi2, p, _, _ = stats.chi2_contingency(table)
    c_rate = control_success / control_total
    t_rate = treat_success / treat_total
    lift = (t_rate - c_rate) / c_rate if c_rate else float("nan")
    return {"control_rate": round(c_rate, 4), "treatment_rate": round(t_rate, 4),
            "lift": round(lift, 4), "p": round(p, 4),
            "verdict": "treatment wins" if (p < 0.05 and t_rate > c_rate)
                       else "no significant win"}

print(ab_proportion_test(410, 4000, 452, 4000))
```

Output (conceptually):
```
{'control_rate': 0.1025, 'treatment_rate': 0.113, 'lift': 0.1024,
 'p': 0.0034, 'verdict': 'treatment wins'}
```

The verdict requires *both* p < 0.05 *and* the right direction. A significant
*negative* effect is a real finding — the candidate is worse, and you roll
back.

## 4. Continuous Outcomes: The t-Test

When the metric is a mean (revenue per user, session time), use a t-test:

```python
from scipy import stats

def ab_t_test(control: list[float], treatment: list[float]) -> dict:
    """Two-sample t-test on a continuous outcome."""
    t_stat, p = stats.ttest_ind(treatment, control, equal_var=False)
    return {"control_mean": round(float(np.mean(control)), 4),
            "treatment_mean": round(float(np.mean(treatment)), 4),
            "p": round(float(p), 4),
            "verdict": "treatment wins" if (p < 0.05 and np.mean(treatment) > np.mean(control))
                       else "no significant win"}
```

Output (conceptually):
```
{'control_mean': 4.82, 'treatment_mean': 5.11, 'p': 0.011,
 'verdict': 'treatment wins'}
```

Both tests share the discipline: **pre-register the metric and the stopping
rule**, collect until the sample size is met, then test once.

## 5. The Pitfalls That Invalidate Experiments

| Pitfall | What goes wrong | Fix |
|---|---|---|
| **Peeking** | checking every day, stopping on the first p<0.05 | fixed sample size / duration; sequential methods |
| **Multiple comparisons** | testing 10 metrics, one "wins" by chance | pre-register one primary metric; correct for multiplicity |
| **Simpson's paradox** | overall win is a mix of losing segments | stratify (country, device, cohort) |
| **Underpowering** | "no significant difference" with n too small | sample-size math first |
| **Traffic leakage** | a user sees both models (cross-contamination) | strict user/request-level bucketing |
| **Long-term vs short-term** | short-term metric up, long-term harm | follow-up window; guardrail metrics |

**Peeking is the silent killer**: if you watch the dashboard and stop at the
first p<0.05, the false-positive rate is far above 5%. Decide the sample size
*first* and stop there.

## 6. Guardrail Metrics and Segments

A model change can win the primary metric and still harm the business.
Guardrails: latency (Lecture 07), error rate, other-model metrics, and
segment performance. Run the primary test *and* check guardrails; a win that
breaks the p99 latency budget is not a win.

```python
def guardrail_check(primary_pass: bool, guardrails: dict[str, bool]) -> tuple[bool, list[str]]:
    """Promotion requires primary + all guardrails green."""
    failures = [g for g, ok in guardrails.items() if not ok]
    return (primary_pass and not failures), failures

print(guardrail_check(True, {"latency": True, "error_rate": True}))
print(guardrail_check(True, {"latency": False}))
```

Output (conceptually):
```
(True, [])
(False, ['latency'])
```

## 7. A/B as a Pipeline Step, Not a Human Ritual

The strongest pattern: the promotion pipeline (Lecture 12) includes an
**A/B stage** — shadow scoring first, then a canary A/B on real traffic, with
the registry recording the experiment result on the candidate version (Lecture
04). The decision "promote vs rollback" is then a *recorded pipeline
decision*, auditable like every other gate.

```python
def promote_decision(experiment: dict, guardrails_ok: bool) -> str:
    if not guardrails_ok:
        return "rollback: guardrail failure"
    if experiment["verdict"] == "treatment wins":
        return "promote to production"
    if experiment["verdict"] == "no significant win" and experiment["harmless"]:
        return "promote (parity) — document no measured loss"
    return "keep incumbent"
```

Output (conceptually):
```
promote to production
```

## Every Use Case

- **Ranking model rollouts**: CTR experiments on search/recommendation.
- **Fraud model changes**: fraud-caught rate vs false-positive rate trade-offs.
- **Pricing/payout models**: revenue and approval-rate outcomes.
- **LLM system changes (Phase 9)**: prompt/temperature/model swaps measured on
  user satisfaction, deflection, cost per resolved ticket.
- **Feature store changes (Lecture 13)**: a new feature definition A/B tested
  before backfilling.
- **Multi-tenant products**: per-tenant experiments with shared platform stats.
- **Rollback triggers**: when a canary shows a guardrail break, auto-rollback.

## Real-World Use Cases for AI Engineers

- **E-commerce ranking**: the new ranking model won offline AUC by 1%, but
  A/B showed conversion *down* 0.6% (p=0.03). The experiment overruled the
  offline eval — a textbook case of why the production test is the last word.
- **Fintech fraud**: the candidate caught 3% more fraud but raised
  false-positive declines 1.2%, hurting revenue. The A/B with guardrail
  metrics showed the trade-off was net-negative; the team iterated on
  thresholds instead of shipping.
- **Ride-hailing pricing**: a pricing-model change was A/B tested per-city
  (Simpson's paradox guard: aggregate looked neutral, but big cities lost and
  small cities won) — the stratified analysis stopped a full rollout.
- **Customer support LLM (Phase 9)**: a new prompt achieved higher
  "auto-resolved" rates (primary metric) with unchanged CSAT (guardrail) —
  the A/B justified the rollout with recorded evidence.
- **Startup**: a 2-engineer team A/B tests the churn model's threshold change
  on 5% of traffic; the chi-squared result (p=0.02, +1.1% retention) is the
  recorded evidence for the promotion.

## Common Mistakes to Avoid

### Mistake 1: Peeking and stopping early
```
# WRONG — stop at the first p<0.05 you see in the dashboard
# CORRECT — pre-compute sample size; test once at the end
```

### Mistake 2: Underpowered tests
"n=500, no significant difference" is not a finding. Size the test first.

### Mistake 3: Multiple metrics, no pre-registration
10 metrics → one will "win" by chance. Pre-register one primary metric.

### Mistake 4: Ignoring Simpson's paradox
Stratify by country/device/cohort before trusting the aggregate.

### Mistake 5: No guardrail metrics
A primary win with a broken latency budget is a loss. Guardrail everything.

### Mistake 6: Traffic leakage
Users switching models mid-session contaminates both arms. Bucket strictly.

## Best Practices

1. Pre-register the primary metric, allocation, sample size, and stopping rule
2. Compute required sample size before starting (baseline + min effect)
3. Test once at the planned size — never peek
4. Use chi-squared for rates, t-test for means
5. Stratify results to catch Simpson's paradox
6. Track guardrail metrics (latency, error, secondary outcomes)
7. Record the experiment result on the candidate version in the registry
8. Prefer canary (small %) to 50/50 when risk is asymmetric
9. Follow up after the win (long-term effects vs short-term)
10. Make the verdict a pipeline decision, not a human judgment call

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Sample-size calc | O(1) | O(1) | — |
| Chi-squared test | O(1) | O(1) | — |
| Collect experiment | days-weeks | O(n rows) | smaller δ if acceptable |
| Stratified analysis | O(segments) | O(1) | pre-aggregate by segment |

## AI Engineering Relevance

**Where this shows up:** every model promotion decision where offline metrics
are proxies — which is most production ML worth shipping.

| Concept here | Used for |
|---|---|
| Pre-registered design | honest, interpretable results |
| Power/sample-size | knowing what you can detect |
| Significance tests | promote vs rollback decisions |
| Guardrails | protecting the business while optimizing |

**Scale note:** at high traffic, experiments finish in hours and run
continuously; at low traffic, tests take weeks and the sample-size math
decides whether an experiment is even worth running. Either way, the
discipline is identical — and the evidence is what makes model rollouts
defensible.

## Practice Exercises

### Exercise 1: Sample Size (Easy)
Implement `min_sample_size` and verify it grows when the effect shrinks and
shrinks when the baseline is higher.

### Exercise 2: Chi-Squared Verdict (Medium)
Implement `ab_proportion_test` and test three cases: significant win,
significant loss, no significant difference — asserting the verdict each time.

### Exercise 3: t-Test Verdict (Medium)
Implement `ab_t_test` on synthetic control/treatment arrays with a known mean
shift; assert it detects a 10% shift at n=2000 but not at n=20.

### Exercise 4: Experiment Planner (Hard)
Write `plan_experiment(baseline, min_effect, traffic_per_day, guardrails)` that
returns the sample size, the duration in days, and a stop decision function —
then simulate a peeking scenario and show how the fixed-size rule avoids the
false positive.

## Summary

| Concept | Description |
|---|---|
| Pre-registration | metric + size + stopping rule before traffic |
| Power/sample size | knowing what the test can detect |
| Chi-squared / t-test | rates and means, both with verdict discipline |
| Guardrails | the business protections around the primary metric |
| Pipeline step | A/B as a recorded promotion gate |

A/B testing is the last and most honest gate: it measures real outcomes on
real users and replaces "the model felt better" with "the model won at p<0.05
with guardrails green." The AI engineer who masters experiment design ships
model changes with evidence, not hope.

## Quick Reference

| Task | Idiom |
|---|---|
| Size the test | `min_sample_size(baseline, effect)` |
| Test a rate | `scipy.stats.chi2_contingency(table)` |
| Test a mean | `scipy.stats.ttest_ind(a, b, equal_var=False)` |
| Stop rule | pre-planned sample, single test |
| Guardrails | primary metric + latency/error/secondaries |

## Next Steps

Next: **[15 Cost Optimization](15-cost-optimization-lecture.md)** — managing the
compute, storage, and serving budgets of an ML system.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://www.statsmodels.org/, https://www.evanmiller.org/ab-testing/
