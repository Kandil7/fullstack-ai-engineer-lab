# Glossary: Data Ethics

## Quick Reference Table

| Term | Definition | Example / Cue |
|------|-----------|---------------|
| Feedback loop | System outputs re-enter as future inputs | Recommender trained on its own clicks |
| Runaway feedback loop | A loop that self-amplifies without correction | Predictive policing concentrating patrol |
| Goodhart's Law | A measure targeted stops being a good measure | Optimizing watch-time breaks it as a signal |
| Historical bias | Data faithfully encodes an unequal world | Hiring model learns past discrimination |
| Representation bias | Training data under-represents some groups | Face dataset mostly light-skinned faces |
| Measurement bias | Features/labels are noisy proxies | "Arrests" used as a stand-in for "crime" |
| Aggregation bias | One model wrongly applied across distinct groups | Single clinical model across populations |
| Evaluation/deployment bias | Benchmark or context mismatches deployment | Validated on one group, deployed on all |
| Disaggregated evaluation | Metrics reported per subgroup, not aggregate | Per-group FPR/FNR table |
| Fairness | Distribution of benefits/harms across groups | Demographic parity vs. error-rate balance |
| Proxy variable | A stand-in feature for the real target | Healthcare cost used for health need |
| Recourse | A real path to contest and correct a decision | Working appeals process for a denial |
| Accountability | A named party answerable for outcomes | Not "the algorithm decided" |
| Automation bias | Over-trusting automated output | Rubber-stamping model decisions |
| Human-in-the-loop | An empowered human reviewing/overriding output | Reviewer with time, context, override |
| Model card | Doc of a model's use, data, and disaggregated metrics | Ships with the model |
| Datasheet for datasets | Doc of a dataset's origin, composition, use | Motivation, collection, recommended use |
| Data provenance | Known origin, license, and meaning of data | "Where did this come from and how?" |
| Informed consent | Permission given with understanding of use | Opt-in with clear purpose |

---

## Detailed Definitions

### Feedback loop

**Definition:** A dynamic in which a system's outputs influence the world in a
way that becomes future input to the same system. ML systems are prone to this
because they are retrained on data their own predictions helped generate.

## Example

```text
predict "engaging" ─► show more of it ─► users watch more of it
        ▲                                          │
        └──────────── retrain on the new clicks ───┘
```

The metric (clicks) can rise while the thing you cared about (user well-being,
information quality) falls.

**Related Terms:** runaway feedback loop, Goodhart's Law, proxy variable
- The loop is not a bug; it is inherent to systems retrained on their outputs.
- Mitigation: monitor second-order effects over time, not just launch metrics.

---

### Runaway feedback loop

**Definition:** A feedback loop with positive gain and no correcting force, so a
small initial difference is amplified each cycle into a large disparity.

## Example

Two districts have equal true crime, but district A starts with more patrol.
More patrol → more observed arrests in A → next cycle sends even more patrol to
A. Patrol share diverges toward A regardless of the underlying reality.

**Related Terms:** feedback loop, measurement bias, Goodhart's Law
- The system measures *its own past actions*, not ground truth.
- Predictive policing is the canonical illustration fast.ai uses.

---

### Goodhart's Law

**Definition:** "When a measure becomes a target, it ceases to be a good
measure." Once you optimize a proxy directly, agents (or models) game it and it
stops tracking what you cared about.

## Example

Engagement is a reasonable *signal* of value — until a recommender optimizes it
directly, at which point extreme/provocative content wins because it maximizes
the number, not the value.

**Related Terms:** proxy variable, feedback loop, fairness
- Pair any target metric with guardrail metrics that detect gaming.
- Never let a single metric become the sole objective.

---

### Historical bias

**Definition:** Bias that exists because the data faithfully reflects a world
that is already unequal. It is present even with perfect sampling and perfect
measurement.

## Example

A résumé-screening model trained on who a company hired in the past learns and
reproduces whatever discrimination shaped those past decisions.

**Related Terms:** representation bias, measurement bias, fairness
- You cannot fix historical bias by collecting "more" of the same data.
- Requires deciding what the world *should* be, not just what it *was*.

---

### Representation bias

**Definition:** Bias arising when the training data under-represents part of the
population the model will serve, so the model learns those groups poorly.

## Example

A facial-analysis training set dominated by lighter-skinned faces yields far
higher error on darker-skinned faces — the disparity at the core of the "Gender
Shades" findings (Buolamwini & Gebru, 2018).

**Related Terms:** evaluation bias, disaggregated evaluation, aggregation bias
- Detectable by comparing subgroup sizes and subgroup error rates.
- Fix by sampling the deployment population, not the convenient one.

---

### Measurement bias

**Definition:** Bias introduced when the features or labels you record are noisy
or systematically skewed proxies for the concept you actually care about.

## Example

Using *number of arrests* to represent *crime* measures policing activity, not
crime. Using *healthcare spending* to represent *health need* under-measures
need for groups on whom less was historically spent.

**Related Terms:** proxy variable, historical bias, feedback loop
- Always ask: what does this label/feature literally measure?
- Central to the Obermeyer et al. (2019) health-algorithm case.

---

### Aggregation bias

**Definition:** Bias that appears when a single model is applied to distinct
subpopulations for which the correct input-output relationship differs, so the
model fits none of them well.

## Example

A one-size-fits-all clinical model can misfit populations whose disease
presents differently, even if each group had adequate data.

**Related Terms:** representation bias, evaluation bias, disaggregated evaluation
- Sometimes the right fix is group-specific models or features.
- Only visible if you evaluate per group.

---

### Evaluation / deployment bias

**Definition:** Bias from evaluating a model on a benchmark or population that
does not match where and how it is actually deployed.

## Example

A model validated only on adults is deployed for children; or a benchmark
over-weights an easy subgroup, so headline accuracy overstates field
performance.

**Related Terms:** representation bias, aggregation bias, model card
- The model card's "intended use" and "out-of-scope" fields guard against this.

---

### Disaggregated evaluation

**Definition:** The practice of computing and reporting metrics separately for
each meaningful subgroup instead of collapsing everything into one aggregate
number.

## Example

```python
import numpy as np

def per_group_fnr(y_true, y_pred, groups):
    out = {}
    for g in np.unique(groups):
        m = groups == g
        fn = np.sum((y_true[m] == 1) & (y_pred[m] == 0))
        tp = np.sum((y_true[m] == 1) & (y_pred[m] == 1))
        out[g] = fn / max(fn + tp, 1)
    return out
```

**Related Terms:** fairness, evaluation bias, model card
- A 95% aggregate can hide a 70% subgroup.
- Which gap matters depends on the cost of a false positive vs. false negative.

---

### Fairness

**Definition:** A property concerning how a model's benefits and harms are
distributed across groups. There are multiple formal, often mutually
incompatible, definitions.

## Example

*Demographic parity* (equal selection rates) and *equalized odds* (equal
error rates) usually cannot both hold at once; you must choose and justify.

**Related Terms:** disaggregated evaluation, proxy variable, accountability
- There is no single "fair" — fairness is a choice you must defend.
- State which definition you optimized and why.

---

### Proxy variable

**Definition:** A feature used as a stand-in for a target concept that is hard to
measure directly. Danger arises when the proxy diverges from the target,
especially unevenly across groups.

## Example

`healthcare_cost` as a proxy for `health_need`; `clicks` as a proxy for `value`;
`arrests` as a proxy for `crime`.

**Related Terms:** measurement bias, Goodhart's Law, fairness
- Removing a protected attribute does not remove bias if a proxy encodes it.
- Name every proxy explicitly during design review.

---

### Recourse

**Definition:** A meaningful, usable mechanism by which a person affected by an
algorithmic decision can understand it, contest it, and get an error corrected.

## Example

A loan applicant denied by a model can see the reasons, submit a correction, and
have a human re-review — within a bounded, published timeframe.

**Related Terms:** accountability, human-in-the-loop, data provenance
- Requires logging inputs, decisions, and reasons *before* launch.
- Absent recourse, errors become permanent for the people they hit.

---

### Accountability

**Definition:** The condition that a specific, identifiable party is answerable
for a system's outcomes and cannot deflect responsibility onto "the algorithm."

## Example

A benefits agency names an official responsible for wrongful automated denials,
with a duty to fix them — not "the system did it."

**Related Terms:** recourse, human-in-the-loop, model card
- "I only followed the spec" is not accountability.
- Pair with recourse: someone must own the appeals path.

---

### Automation bias

**Definition:** The documented human tendency to over-trust automated outputs
and to defer to them even when they conflict with the person's own judgment.

## Example

A caseworker approves 200 model decisions per hour with no context and is
penalized for overriding — the "human in the loop" launders errors rather than
catching them.

**Related Terms:** human-in-the-loop, accountability, fairness
- A reviewer who cannot realistically override is not a safeguard.
- Never present model output as objective truth.

---

### Human-in-the-loop

**Definition:** A design in which a human reviews, and can override, automated
decisions. It is only effective when the human is genuinely empowered.

## Example

An empowered reviewer sees inputs, reasons, and the model's uncertainty; has
enough time per case; can override without penalty; and their overrides feed
back into improving the model.

**Related Terms:** automation bias, recourse, accountability
- Empowerment (time, context, uncertainty, penalty-free override) is the point.
- Otherwise automation bias dominates.

---

### Model card

**Definition:** A short, standardized document (Mitchell et al., 2019) reporting
a model's intended use, out-of-scope uses, training/evaluation data, and
disaggregated performance and limitations.

## Example

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ModelCard:
    name: str
    intended_use: str
    out_of_scope_uses: str
    disaggregated_metrics: dict[str, dict[str, float]]
```

**Related Terms:** datasheet for datasets, disaggregated evaluation, evaluation bias
- Treat it as a code artifact that ships with the model.
- Immutability (frozen) keeps a faithful record per version.

---

### Datasheet for datasets

**Definition:** A standardized document (Gebru et al.) describing a dataset's
motivation, composition, collection process, preprocessing, recommended uses,
and limitations.

## Example

A datasheet answers: Why was this collected? Who is in it? How were labels
obtained? What uses are discouraged?

**Related Terms:** data provenance, model card, informed consent
- Undocumented data is a liability you cannot reason about.
- Written by data creators; read by data consumers.

---

### Data provenance

**Definition:** Documented knowledge of where data came from, how it was
collected, under what license or consent, and what it does and does not
represent.

## Example

"These images were licensed from source X under license Y, collected in region
Z in 2021, and exclude minors." vs. "we scraped it from somewhere."

**Related Terms:** datasheet for datasets, informed consent, measurement bias
- Provenance gaps surface later as legal and bias problems.
- Prefer known-origin, minimized data.

---

### Informed consent

**Definition:** Permission obtained from people whose data is used, given with a
genuine understanding of how the data will be collected and used.

## Example

An opt-in checkbox with a clear, specific purpose statement — not a buried
clause repurposing data for a use the person never anticipated.

**Related Terms:** data provenance, privacy, datasheet for datasets
- Availability of data is not permission to use it.
- Practice data minimization: collect only what you need.

---

## Summary

Data ethics for engineers is a set of habits, not a checklist you pass once.
**Feedback loops** and **Goodhart's Law** explain how optimizing a single metric
produces harm; the **bias taxonomy** (historical, representation, measurement,
aggregation, evaluation) names where harm enters; **disaggregated evaluation**
is how you see it; **fairness** definitions force an explicit, defended choice;
**recourse** and **accountability** give affected people a way out and name who
owns the outcome; an **empowered human-in-the-loop** counters **automation
bias**; and **provenance, consent, datasheets, and model cards** make the whole
practice documentable and durable. Report by subgroup, name your proxies, and
ask who is harmed if you are wrong.
