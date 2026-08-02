# GenAI — 05: Prompt Evaluation

## Topic Overview

Prompt evaluation is the practice of measuring whether a prompt (or model
configuration) actually improves quality — on *your* data, against *your*
criteria — before you ship it. It is the answer to the #1 problem in LLM
engineering: "the new prompt feels better" is not a measurement, and
benchmarks (MMLU, HumanEval) do not predict performance on your customer
support tickets. Evaluation turns prompt iteration from guesswork into an
engineering loop: define criteria → build an eval set → score → iterate →
ship only measured improvements.

The core tooling: a **frozen eval set** of representative inputs with expected
behavior, a **scoring method** (exact-match, rubric-based, LLM-as-judge, or
human review), and a **leaderboard** that compares prompt/model/temperature
configurations. The loop is the same as CI for code (Lecture 12 of Phase 8):
every prompt change is a candidate; only measured wins are merged.

Why this matters: prompts degrade silently — a model update changes behavior,
a new edge case arrives, an instruction reads differently than intended.
Without evaluation, quality drift is invisible until users complain. With it,
every prompt version has a number, and regressions are caught in CI.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Define measurable criteria for a task (accuracy, format, safety, groundedness)
2. Build a representative frozen eval set (with edge cases)
3. Score outputs: exact/partial match, rubric, LLM-as-judge
4. Run an A/B comparison of two prompt versions and decide with numbers
5. Detect overfitting to the eval set (and refresh it)
6. Integrate eval as a CI gate for prompt changes
7. Measure what matters for RAG/agents (groundedness, tool correctness) — the pattern extends

## Prerequisites

| Need | Where |
|---|---|
| Prompt engineering | `09-genai/lectures/04-prompt-engineering-lecture.md` |
| Structured output | `09-genai/lectures/03-structured-output-lecture.md` |
| Python | `01-core-python/` |
| Phase 8 CI gates | `08-mlops/lectures/12-ci-cd-for-ml-lecture.md` |

## 1. Define Criteria Before You Measure

You cannot evaluate without a definition of "good." For every task, name the
criteria:

| Task | Criteria |
|---|---|
| Classification | accuracy, per-class precision/recall |
| Extraction | field-level correctness, schema validity (L3) |
| Summarization | faithfulness, completeness, conciseness |
| Q&A (RAG) | groundedness (no invented facts), answer correctness, citations |
| Generation | rubric: tone, structure, adherence to constraints |
| Safety | refusal rate on harmful inputs, leakage rate (L19) |

The criteria become the eval set's labels and the scoring functions.

## 2. Build the Eval Set

A frozen eval set is the referee both prompt versions agree to. Design rules:

- **Representative**: real production inputs (sample a week of traffic)
- **Edge cases**: empty input, huge input, adversarial, rare formats
- **Expected behavior**: golden outputs or rubric-checkable properties
- **Frozen**: versioned; model/prompt changes never rewrite it

```python
EVAL_SET = [
    # (input, expected_label)
    ("The app crashed three times today.", "Negative"),
    ("Love the new dashboard!", "Positive"),
    ("", "Neutral"),                       # edge: empty
    ("Billing " * 2000, "Neutral"),        # edge: huge
]
```

Output:
```
5-10% edge cases, 90% representative — the set that catches regressions.
```

**Golden outputs** (human-written) are the gold standard for accuracy tasks;
**checkable properties** (is it valid JSON? does it cite a source?) work where
exact output is not fixed.

## 3. Scoring: From Exact Match to LLM-as-Judge

### Exact / partial match
```python
def accuracy(preds: list[str], gold: list[str]) -> float:
    return sum(p == g for p, g in zip(preds, gold)) / len(preds)

print(accuracy(["Positive", "Negative", "Neutral"], ["Positive", "Positive", "Neutral"]))
```

Output:
```
0.6667
```

### LLM-as-judge
For open-ended tasks (summaries, generation), a judge LLM scores against a
rubric. This is a *reliability risk* — the judge itself drifts and has biases —
so it is used with a reference and sampled human review:

```python
def judge_score(judge_fn, output: str, rubric: str) -> int:
    """1-5 rubric score from a judge LLM call."""
    resp = judge_fn(f"{rubric}\n\nOutput: {output}\n\nScore (1-5):")
    try:
        return int(resp.strip())
    except ValueError:
        return 0   # judge format drift → score 0 and log it
```

Output:
```
4   (judge's rubric score; logged with the raw response for audit)
```

**Judging the judge:** periodically check judge agreement with human scores
on a sample; if agreement drops, recalibrate the judge prompt or revert to
human review.

## 4. The A/B Loop: Prompt v1 vs v2

The engineering loop: run both versions on the same frozen set, compare,
decide with numbers:

```python
def compare(prompt_a, prompt_b, eval_set, score_fn) -> dict:
    a = [score_fn(prompt_a(x)) for x in eval_set]
    b = [score_fn(prompt_b(x)) for x in eval_set]
    return {
        "a": round(sum(a) / len(a), 3),
        "b": round(sum(b) / len(b), 3),
        "delta": round(sum(b) / len(b) - sum(a) / len(a), 3),
        "verdict": "ship B" if sum(b) > sum(a) else "keep A",
    }

print(compare(lambda t: "Positive", lambda t: "Negative",
              [("x", "Positive")] * 100, lambda p: 1.0 if p == "Positive" else 0.0))
```

Output:
```
{'a': 1.0, 'b': 0.0, 'delta': -1.0, 'verdict': 'keep A'}
```

**Statistically honest version:** sample-size math from Phase 8 Lecture 14
applies — a 1% delta on 20 samples is noise; run enough cases or use paired
significance tests before claiming a win.

## 5. Overfitting to the Eval Set

Prompt optimization can overfit the eval set exactly like a model overfits
training data — the v14 prompt scores 99% on the set and collapses on real
traffic. Defenses:

1. **Hold out a refresh set** you evaluate on monthly
2. **Refresh the eval set** from live traffic periodically (new edge cases)
3. **Watch production metrics** (L17) — the eval leaderboard is a proxy; real
   outcomes (resolution rate, user satisfaction) are the truth
4. **Limit iteration churn**: every prompt revision should improve measured
   quality on an *unchanged* set, then be re-checked on fresh data

## 6. Evaluation as a CI Gate

The strongest pattern (Phase 8 Lecture 12 applied to prompts): prompt changes
go through CI with the eval as a gate — a candidate must not regress the
frozen set:

```python
def prompt_ci_gate(candidate_metrics: dict, baseline_metrics: dict,
                   key: str = "accuracy", min_delta: float = 0.0) -> tuple[bool, str]:
    regress = candidate_metrics[key] < baseline_metrics[key] - min_delta
    return (not regress,
            f"{key}: {candidate_metrics[key]:.3f} vs baseline {baseline_metrics[key]:.3f}")

print(prompt_ci_gate({"accuracy": 0.88}, {"accuracy": 0.91}))
```

Output:
```
(False, 'accuracy: 0.880 vs baseline 0.910')  → CI fails, prompt not merged
```

Every prompt change is then a *candidate* that must pass the gate — the same
discipline as code, applied to the fuzzy artifact.

## Every Use Case

- **Prompt versioning**: A/B every prompt change on a frozen set.
- **Model selection**: same eval set, different models — choose by measured quality + cost.
- **Temperature tuning**: eval at temperature 0 vs 0.5 to justify the knob.
- **RAG component eval**: retrieval quality (L10) and answer groundedness (L9) scored separately.
- **Agent evaluation**: tool-call correctness and task completion (L14, L24).
- **LLM-as-judge calibration**: scoring the judges themselves.
- **Regression protection**: CI gate on prompt/model changes.
- **Compliance evidence**: eval scores recorded for audit (how was quality assured?).

## Real-World Use Cases for AI Engineers

- **Support-ticket classifier**: a v2 prompt "feels better" — the engineer
  runs it on 500 frozen tickets: 82% vs 79% (n=500, paired test p=0.04). The
  measured win ships; the eval set is refreshed monthly with new ticket
  formats so the classifier never silently degrades.
- **Legal summarization**: rubric-based judge (faithfulness, completeness)
  scored prompt versions; the team found v3's extra constraint hurt
  completeness — the eval caught a regression the "feel" missed.
- **RAG answer grounding**: groundedness eval (each claim must cite a
  retrieved chunk) gated the chunking change (L7): the new chunker raised
  recall but *dropped* groundedness — the eval prevented a quality regression
  that pure retrieval metrics would have hidden.
- **LLM-as-judge at a platform company**: the platform team maintains judge
  prompts and calibrates them against human labels monthly; 15 teams share
  the eval infrastructure — prompt quality is a platform service, not a
  per-team guess.
- **Compliance (healthcare)**: every prompt/model release logs its eval
  scores; the audit trail answers "how do you know quality was maintained?"
  with numbers, not assertions.

## Common Mistakes to Avoid

### Mistake 1: No eval set
"Feels better" shipping — quality drift is invisible until users complain.

### Mistake 2: Eval set that matches training data
The set must be *frozen and representative*, never the same inputs the prompt
was iterated on.

### Mistake 3: Tiny sample, strong claims
20 samples cannot detect a 2% difference. Use enough cases or significance
tests.

### Mistake 4: Trusting the judge without calibration
LLM-as-judge drifts and biases. Check judge-human agreement; sample human
review.

### Mistake 5: Single metric
Accuracy alone misses groundedness, safety, format. Score the criteria that
matter.

### Mistake 6: Never refreshing the set
The world changes; the eval set must too (with versioning + changelog).

### Mistake 7: Overfitting
Prompt churn to win the eval → collapse on live traffic. Refresh + production
metrics are the counterweight.

## Best Practices

1. Define criteria before measuring — a task without criteria is unevaluable
2. Build a frozen, representative eval set with edge cases
3. Prefer exact/golden scoring; use LLM-as-judge only with calibration
4. Run A/B comparisons with adequate sample size
5. Make eval a CI gate for every prompt/model change
6. Track multiple criteria (accuracy, groundedness, safety, format)
7. Refresh the eval set on a schedule; version it like code
8. Watch production metrics — eval is a proxy, reality is the truth
9. Log eval results with the prompt version (audit + attribution)
10. Calibrate judges against human review periodically

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Exact-match eval (1k cases) | seconds | O(1) | — |
| LLM-as-judge (1k cases) | minutes + $ | O(1) | sample 10% + exact metrics |
| Judge calibration | hours monthly | O(1) | — |
| CI gate per change | minutes | O(1) | run on a 200-case subset per PR |

## AI Engineering Relevance

**Where this shows up:** every prompt/model/temperature change you will ever
ship. Evaluation is the measurement layer that makes prompt engineering an
engineering discipline.

| Concept here | Used for |
|---|---|
| Frozen eval set | the agreed referee |
| Scoring | from exact match to calibrated judges |
| A/B compare | measured wins, not feelings |
| CI gate | regressions blocked before merge |

**Scale note:** at 1M calls/day, a 1% measured improvement is a real business
win; a 1% silent regression is a real incident. The eval harness is how the
numbers stay visible either way.

## Practice Exercises

### Exercise 1: Accuracy (Easy)
Write `accuracy(preds, gold)` and test ties, all-correct, all-wrong.

### Exercise 2: Eval Set Design (Medium)
Given a support-ticket task, design a 20-case eval set (15 representative, 5
edge) and state the criteria + scoring method for each of the 5 edge cases.

### Exercise 3: A/B Compare (Medium)
Implement `compare(prompt_a, prompt_b, eval_set, score_fn)` and assert the
verdict flips when B's scores exceed A's; add a paired-significance check
(`scipy.stats.wilcoxon`) that reports p.

### Exercise 4: CI Gate (Hard)
Build `prompt_ci_gate` + a mini harness: version A (baseline), candidate B
worse on 3 of 4 criteria — assert the gate fails and the report names the
regressed criteria.

## Summary

| Concept | Description |
|---|---|
| Criteria | define "good" before measuring |
| Eval set | frozen, representative, with edge cases |
| Scoring | exact/rubric/LLM-judge, calibrated |
| A/B loop | measured decisions |
| CI gate | regressions blocked at merge |

Prompt evaluation converts "the prompt feels better" into "the prompt scores
88% vs 84% on the frozen set, p=0.04." It is the measurement layer that makes
prompt engineering engineering — and it protects production from the silent
quality drift that plagues every LLM system.

## Quick Reference

| Task | Idiom |
|---|---|
| Score accuracy | `sum(p==g)/len` |
| Judge open-ended | LLM-as-judge with rubric + calibration |
| Compare versions | frozen set, paired significance |
| Gate in CI | candidate must not regress baseline |
| Refresh | monthly, versioned, changelogged |

## Next Steps

Next: **[06 Embeddings](06-embeddings-lecture.md)** — the numerical
representation of text that powers retrieval and RAG.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://platform.openai.com/docs/guides/evaluation
