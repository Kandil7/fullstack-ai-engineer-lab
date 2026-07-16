# Lecture 09: Data Ethics

## Topic Overview

fast.ai's data-ethics bonus lesson (taught largely by Rachel Thomas, co-founder
of fast.ai and founding director of the USF Center for Applied Data Ethics)
argues a blunt point: **the engineer who builds a system shares responsibility
for what it does in the world**. "I was just implementing the spec" is not a
defense. This lecture translates that stance into concrete engineering practice:
recognizing feedback loops, naming the kinds of bias that creep into data and
models, evaluating models *by subgroup* instead of by a single aggregate number,
and running a real pre-deployment checklist before you ship.

Unlike the rest of Part 1, there is almost no model training here. The "code" is
the code you write to **audit** a model — disaggregated metrics, feedback-loop
simulations, and machine-readable documentation (model cards, datasheets).

**Duration:** 2-3 hours
**Difficulty:** All levels
**Prerequisites:** Lecture 01

---

## Learning Objectives

By the end of this lecture you will be able to:

1. Explain why engineers, not just product owners or executives, are
   accountable for the systems they build.
2. Identify **feedback loops** in a system and predict how a metric can run away
   (Goodhart's Law).
3. Distinguish **historical, representation, measurement, aggregation,** and
   **evaluation/deployment** bias, and locate each in a real case.
4. Compute and interpret **disaggregated metrics** (per-subgroup error rates)
   instead of relying on a single aggregate score.
5. Design **recourse** and **accountability** mechanisms so people can contest
   and correct algorithmic decisions.
6. Recognize **automation bias** and place a meaningful human in the loop.
7. Reason about **privacy, consent, and data provenance** when sourcing data.
8. Apply practical tools — **datasheets for datasets, model cards, and a
   pre-deployment ethics checklist** — using the Markkula "ethics as a practice"
   lenses (consequentialist, rights, justice).

---

## Key Concepts

### 1. You are responsible for what you build

fast.ai opens the ethics lesson by rejecting the idea that ethics is someone
else's job — the legal team's, the policy team's, or "the business's." If you
write the code, you made choices: what data to use, what to optimize, what to
ship, and what edge cases to ignore. Those choices have consequences for real
people.

A recurring historical warning in the lesson: engineers who defended their work
by saying they *only followed the specification* have, across many domains, been
complicit in serious harm. The point is not to induce paralysis but to install a
habit: **before you build, ask who is affected, and after you build, ask who was
harmed if it is wrong.**

> Rachel Thomas frames the useful question as: *"What could go wrong? Who could
> be hurt? And what will we do about it?"* Ask it during design, not during the
> post-mortem.

This lesson does not claim engineers are *solely* responsible. Responsibility is
shared across a system — but "shared" never means "not mine."

### 2. Feedback loops and runaway metrics (Goodhart's Law)

A **feedback loop** occurs when a system's outputs re-enter as future inputs. ML
systems are especially prone to this because they are *retrained on data their
own predictions helped produce*.

Two well-known examples fast.ai discusses:

- **Recommendation systems amplifying extreme content.** A system optimized for
  watch-time or engagement learns that provocative or extreme content keeps
  people watching. It recommends more of it, which trains users toward more
  extreme consumption, which produces more engagement data confirming the
  strategy. YouTube's recommender has been cited (including by its own
  researchers and outside reporting) as a case where optimizing a single
  engagement metric produced unintended radicalization dynamics. Describe this
  carefully: the effect is real and documented in reporting and research, but it
  is contested in magnitude and is a system-level phenomenon, not a single bug.
- **Predictive policing.** A model trained on historical *arrest* data sends
  more officers to already-policed neighborhoods. More officers produce more
  arrests there, which becomes new training data, which further concentrates
  policing. The model is not measuring crime; it is measuring *past police
  activity* and then amplifying it.

The underlying principle is **Goodhart's Law**: *"When a measure becomes a
target, it ceases to be a good measure."* Engagement is a fine signal until you
optimize it directly; then the system games it. The mitigation is to (a) expect
loops, (b) monitor second-order effects, and (c) never let one metric become the
sole objective.

```text
        ┌───────────────────────────────────────────────┐
        │              RUNAWAY FEEDBACK LOOP             │
        │                                                │
        │   model predicts ──► action taken in world     │
        │        ▲                       │               │
        │        │                       ▼               │
        │   retrain on ◄──── new data reflects the action│
        │   biased data       (not ground truth)         │
        └───────────────────────────────────────────────┘
        The metric goes up. The thing you cared about may not.
```

### 3. The taxonomy of bias

"Bias" is not one thing. fast.ai (drawing on Suresh & Guttag's framework)
separates several sources, and the fix differs for each:

- **Historical bias.** The world the data came from is already unequal, so even
  perfectly measured, perfectly sampled data encodes that inequality. Example: a
  hiring model trained on who was hired in the past learns past discrimination.
- **Representation bias.** The training population under-represents some groups.
  The dataset does not reflect who the model will serve.
- **Measurement bias.** The features or labels are noisy proxies for what you
  actually care about — you measure "arrests" and call it "crime," or measure
  "healthcare cost" and call it "health need."
- **Aggregation bias.** A single model is applied to distinct groups for which
  the right relationship differs, so it fits none of them well (e.g., a
  one-size-fits-all clinical model across populations with different disease
  presentation).
- **Evaluation / deployment bias.** The model is evaluated on a benchmark that
  does not match deployment, or is deployed in a context it was never validated
  for.

Two cases fast.ai grounds this in, described carefully:

- **Facial-analysis disparities ("Gender Shades," Buolamwini & Gebru, 2018).**
  Commercial gender-classification systems had far higher error rates on
  darker-skinned women than on lighter-skinned men — an aggregate accuracy
  figure hid enormous subgroup disparities. This is *representation* and
  *evaluation* bias made visible only by disaggregation.
- **A healthcare risk-prediction algorithm (Obermeyer et al., 2019).** A widely
  used system used *past healthcare spending* as a proxy for *health need*.
  Because less money was historically spent on Black patients at equal levels of
  illness, the algorithm systematically under-referred them to extra care. This
  is textbook *measurement bias* via a **proxy variable** — no protected
  attribute was in the model, yet the outcome was racially disparate.

The lesson's takeaway: you cannot debug bias you refuse to look for, and a
single aggregate metric is designed *not* to show it.

### 4. Disaggregated evaluation

The single most actionable engineering habit in this lesson: **never report one
aggregate metric. Break error rates down by subgroup.** A model that is 95%
accurate overall can be 99% accurate for the majority group and 70% for a
minority group — and the aggregate will look great while the product fails the
people it is failing.

Disaggregated evaluation means computing your confusion-matrix-derived rates
(false-positive rate, false-negative rate, precision, recall) *separately* for
each meaningful group, and comparing.

```python
import numpy as np
import pandas as pd

def disaggregated_error_rates(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    groups: np.ndarray,
) -> pd.DataFrame:
    """Per-group confusion-matrix rates. Report these, not one number."""
    rows = []
    for g in np.unique(groups):
        m = groups == g
        yt, yp = y_true[m], y_pred[m]
        tp = int(np.sum((yt == 1) & (yp == 1)))
        tn = int(np.sum((yt == 0) & (yp == 0)))
        fp = int(np.sum((yt == 0) & (yp == 1)))
        fn = int(np.sum((yt == 1) & (yp == 0)))
        rows.append({
            "group": g,
            "n": int(m.sum()),
            "accuracy": (tp + tn) / max(m.sum(), 1),
            "fpr": fp / max(fp + tn, 1),   # false-positive rate
            "fnr": fn / max(fn + tp, 1),   # false-negative rate
        })
    return pd.DataFrame(rows)
```

If your `fpr`/`fnr` columns diverge across groups, your "95% accurate" model is
distributing its mistakes unequally. Which disparity matters depends on what a
false positive vs. a false negative *costs a person* — a false positive on a
fraud model freezes an innocent person's account; a false negative on a disease
screen misses a sick patient.

### 5. Diverse teams and "who is harmed if this is wrong?"

A homogeneous team tends not to *notice* the failure modes that hit people
unlike themselves. fast.ai repeatedly connects the facial-analysis and other
failures to teams that never had a reason to test on the affected groups.
Diversity here is not only a fairness goal, it is an **error-detection
mechanism**: more perspectives find more of the ways a system breaks.

The practical prompt to institutionalize: for every feature, ask **"who is
harmed if this is wrong, and how badly?"** Write the answer down. If nobody on
the team can answer, that is itself a finding.

### 6. Recourse and accountability

When an algorithm makes a consequential decision about a person, that person
must be able to **understand, contest, and correct** it. fast.ai cites cases
where automated systems cut people off from benefits, credit, or employment with
no working appeals path — and where the errors were both common and hard to
reverse (e.g., buggy automated eligibility systems denying benefits to people
who qualified, and credit decisions people could neither see nor dispute).

**Recourse** = the affected person has a real mechanism to fix a wrong decision.
**Accountability** = a specific, identifiable party is answerable for the
outcome and cannot hide behind "the algorithm did it." Designing for recourse
means logging inputs and decisions, exposing reasons, and building an appeals
path *before* launch — not bolting one on after a scandal.

### 7. Humans in the loop and automation bias

Adding a human reviewer is often proposed as the safeguard — but it only works
if the human is empowered and skeptical. **Automation bias** is the documented
human tendency to over-trust automated output and to defer to it even against
their own judgment. A "human in the loop" who rubber-stamps model output at 200
cases an hour is not a safeguard; they are laundering the model's errors with a
signature.

Treating model output as **objective truth** is the core mistake. Models emit
probabilities shaped by their training data; they are not oracles. Real
human-in-the-loop design gives the reviewer time, context, the ability to
override without penalty, and visibility into model uncertainty.

### 8. Privacy, consent, and data provenance; ethics as a practice

- **Privacy & consent.** Just because data is *available* does not mean it is
  *permitted*. Scraping, purchasing, or repurposing data beyond what people
  consented to is an ethical (and often legal) problem. Prefer **informed
  consent** and data minimization — collect only what you need.
- **Data provenance.** Know where your data came from, how it was collected,
  under what license, and what it does and does not represent. Undocumented data
  is a liability you cannot reason about.

fast.ai points to concrete tooling to make this routine rather than heroic:

- **Datasheets for datasets** (Gebru et al.) — a standard document describing a
  dataset's motivation, composition, collection, and recommended uses.
- **Model cards** (Mitchell et al.) — a short document reporting a model's
  intended use, training data, and **disaggregated** performance and limits.
- **Ethical-risk checklists** run *before* deployment.

The Markkula Center's framing (which fast.ai adopts) treats **ethics as an
ongoing practice**, not a one-time gate, examined through complementary lenses:

- **Consequentialist:** what are the likely outcomes, and for whom?
- **Rights:** whose rights (privacy, dignity, due process) are at stake?
- **Justice:** are benefits and harms distributed fairly across groups?

No single lens is sufficient; run all three.

---

## Code Examples

### Example 1: A fairness / bias-audit helper

A small, dependency-light auditor you can drop into an evaluation pipeline. It
computes per-group rates and flags disparities against a tolerance.

```python
from __future__ import annotations

import numpy as np
import pandas as pd


def audit_fairness(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    groups: np.ndarray,
    tolerance: float = 0.10,
) -> tuple[pd.DataFrame, list[str]]:
    """Compute per-group rates and flag gaps larger than ``tolerance``.

    Returns a per-group metrics table and a list of human-readable warnings.
    """
    records: list[dict[str, float]] = []
    for g in np.unique(groups):
        mask = groups == g
        yt, yp = y_true[mask], y_pred[mask]
        tp = int(np.sum((yt == 1) & (yp == 1)))
        tn = int(np.sum((yt == 0) & (yp == 0)))
        fp = int(np.sum((yt == 0) & (yp == 1)))
        fn = int(np.sum((yt == 1) & (yp == 0)))
        records.append({
            "group": g,
            "n": int(mask.sum()),
            "selection_rate": float(np.mean(yp == 1)),
            "fpr": fp / max(fp + tn, 1),
            "fnr": fn / max(fn + tp, 1),
        })

    table = pd.DataFrame(records)
    warnings: list[str] = []
    for metric in ("selection_rate", "fpr", "fnr"):
        gap = float(table[metric].max() - table[metric].min())
        if gap > tolerance:
            hi = table.loc[table[metric].idxmax(), "group"]
            lo = table.loc[table[metric].idxmin(), "group"]
            warnings.append(
                f"{metric} gap {gap:.2f} > {tolerance:.2f} "
                f"(highest: {hi}, lowest: {lo})"
            )
    return table, warnings
```

The `selection_rate` gap is a demographic-parity check; the `fpr`/`fnr` gaps are
error-rate-balance checks. These fairness definitions can conflict — you usually
cannot satisfy all of them at once, so you must *choose and justify* which
matters for your use case.

### Example 2: A model card as a dataclass

Make documentation a code artifact that lives with the model, not a wiki page
that rots.

```python
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ModelCard:
    """Minimal model card (after Mitchell et al., 2019)."""

    name: str
    version: str
    intended_use: str
    out_of_scope_uses: str
    training_data: str
    evaluation_data: str
    disaggregated_metrics: dict[str, dict[str, float]]
    ethical_considerations: str
    caveats: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [
            f"# Model Card: {self.name} (v{self.version})",
            f"**Intended use:** {self.intended_use}",
            f"**Out-of-scope:** {self.out_of_scope_uses}",
            f"**Training data:** {self.training_data}",
            f"**Evaluation data:** {self.evaluation_data}",
            "## Disaggregated metrics",
        ]
        for group, metrics in self.disaggregated_metrics.items():
            pretty = ", ".join(f"{k}={v:.3f}" for k, v in metrics.items())
            lines.append(f"- **{group}:** {pretty}")
        lines.append(f"## Ethical considerations\n{self.ethical_considerations}")
        if self.caveats:
            lines.append("## Caveats")
            lines.extend(f"- {c}" for c in self.caveats)
        return "\n".join(lines)
```

Because it is `frozen=True`, a card is immutable once built — a new model
version yields a new card rather than silently overwriting the old record.

### Example 3: A pre-deployment ethics checklist as data

```python
ETHICS_CHECKLIST: list[str] = [
    "Who benefits from this system, and who could be harmed if it is wrong?",
    "Have we evaluated metrics disaggregated by every meaningful subgroup?",
    "What proxy variables are we using, and what do they really measure?",
    "Is there a feedback loop? What happens to the metric over time?",
    "Can an affected person understand, contest, and correct a decision?",
    "Who is accountable by name if this causes harm?",
    "Is the human reviewer empowered to override — with time and context?",
    "Do we have consent and known provenance for all training data?",
    "Have we written a datasheet and a model card?",
    "Have we examined this via consequentialist, rights, and justice lenses?",
]


def run_checklist(answers: dict[str, str]) -> list[str]:
    """Return unanswered checklist items — a non-empty list blocks launch."""
    return [q for q in ETHICS_CHECKLIST if not answers.get(q, "").strip()]
```

---

## Common Mistakes to Avoid

**Mistake 1 — Reporting one aggregate metric.**

```python
# BAD: hides subgroup failure entirely
accuracy = (y_pred == y_true).mean()
print(f"Model is {accuracy:.1%} accurate. Ship it.")

# GOOD: look at each group's error rates before deciding
table, warnings = audit_fairness(y_true, y_pred, groups, tolerance=0.10)
print(table)
if warnings:
    raise SystemExit("Disparity detected:\n" + "\n".join(warnings))
```

**Mistake 2 — Treating a proxy as the target.**

```text
BAD:  "We predict healthcare *cost*, which obviously means health *need*."
GOOD: "Cost is a proxy. Historically, less was spent on some groups at equal
       illness, so cost under-measures their need. We validate need directly
       and audit outcomes by group."
```

**Mistake 3 — "Human in the loop" as a rubber stamp.**

```text
BAD:  Reviewer approves 200 model decisions/hour, no context, penalized for
      overriding. Automation bias guarantees the model's errors pass through.
GOOD: Reviewer sees inputs, reasons, and model uncertainty; has time per case;
      can override without penalty; overrides are logged and fed back to
      improve the model and the appeals path.
```

---

## Best Practices

1. **Report disaggregated metrics by default.** One aggregate number is a red
   flag, not a result.
2. **Ask "who is harmed if this is wrong?" at design time** and write down the
   answer for every feature.
3. **Name proxy variables explicitly** and interrogate the gap between the proxy
   and the thing you actually care about.
4. **Assume feedback loops exist** and monitor second-order effects over time,
   not just launch-day metrics.
5. **Resist single-metric optimization** (Goodhart's Law); pair any target with
   guardrail metrics that catch gaming.
6. **Build recourse before launch:** logging, explanations, and a working
   appeals path.
7. **Assign named accountability;** "the algorithm decided" is not an answer.
8. **Empower the human in the loop** with time, context, uncertainty, and a
   penalty-free override.
9. **Document with datasheets and model cards** as code artifacts that ship with
   the model.
10. **Run the pre-deployment ethics checklist** through consequentialist,
    rights, and justice lenses — and treat ethics as an ongoing practice, not a
    one-time sign-off.

---

## Practice Exercises

1. **Disaggregate a confusion matrix.** Given `y_true`, `y_pred`, and a `group`
   array, compute accuracy, FPR, and FNR per group. Identify which group the
   model fails and argue whether the FPR or FNR gap matters more for a lending
   decision vs. a disease screen.

2. **Simulate a runaway feedback loop.** Model "predictive policing": start with
   equal true crime rates across two districts but unequal initial patrol.
   Each round, allocate patrol proportional to *last round's arrests*, and let
   observed arrests depend on patrol. Plot patrol share over 20 rounds and
   explain the divergence in terms of Goodhart's Law.

3. **Spot the bias type.** For five short scenarios (a hiring model, a scraped
   face dataset, a cost-as-need health model, a benchmark/deployment mismatch,
   an under-sampled dialect in ASR), label each as historical, representation,
   measurement, aggregation, or evaluation bias, and justify.

4. **Write a model card.** Use the `ModelCard` dataclass to document a small
   classifier you trained in an earlier lecture, including at least two
   disaggregated metric groups and three honest caveats. Render it to Markdown.

5. **Run the checklist for real.** Take a project you have actually built (or the
   Gradio app from Lecture 02) and answer all ten `ETHICS_CHECKLIST` items in
   writing. Which questions could you *not* answer? Those are your gaps.

---

## Summary

Ethics is not a compliance layer bolted on at the end — it is engineering. You
are responsible for what you build; feedback loops and runaway metrics
(Goodhart's Law) mean well-intentioned single-metric optimization can cause real
harm; bias comes in distinct flavors (historical, representation, measurement,
aggregation, evaluation) that each demand different fixes; and the antidote
starts with **disaggregated evaluation** — never trust one aggregate number.
Around the model, build **recourse and accountability**, an **empowered human in
the loop** (guarding against automation bias), and disciplined handling of
**privacy, consent, and provenance**. Make it routine with **datasheets, model
cards, and a pre-deployment checklist** examined through consequentialist,
rights, and justice lenses.

**Next lecture:** This completes **Part 1** of the fast.ai mirror. From here,
fast.ai continues into **Part 2 — "From Deep Learning Foundations to Stable
Diffusion,"** which builds generative diffusion models from the ground up. In
this lab, carry the ethics habits forward into the applied tracks: the
`agents/` track (where autonomous action multiplies the stakes of a wrong
decision) and the `ai-automation/` RAG track (where data provenance, consent,
and disaggregated evaluation of retrieval quality apply directly). Ship
responsibly.
