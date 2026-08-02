# GenAI — 20: Evaluation Frameworks

## Topic Overview

An evaluation framework is the systematic harness for grading every component
of an LLM system — prompts (L5), retrieval (L10), agents (L14), guardrails
(L19), models, and whole pipelines — on your data, with your criteria,
before and after every change. It is the unifying practice of Phase 9: the
eval harness is how "this feels better" becomes "this scores 0.88 vs 0.84 on
the frozen set," and how regressions get caught in CI (Phase 8 L12 pattern)
instead of by users.

The framework has four parts:

1. **Datasets**: frozen, representative, versioned — with gold labels or
   checkable properties (L5).
2. **Evaluators**: scoring functions — exact match, rubric/LLM-judge, metric
   computation (retrieval L10, groundedness L9, guardrail catch-rate L19).
3. **Runner**: runs candidates (prompt/model/config) over the datasets and
   produces a report.
4. **Gates**: CI integration — regressions block merges; improvements ship.

Tools: **DeepEval**, **Ragas** (RAG-specific), **LangSmith evaluation**,
**promptfoo**, or a hand-rolled harness. The framework is the *infrastructure*
of LLM quality — this lecture teaches the architecture and the discipline.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Design an eval suite: datasets, evaluators, and the score report
2. Build evaluators: exact-match, rubric (LLM-judge), retrieval metrics, guardrail metrics
3. Run an A/B eval of two configurations and read the report
4. Use LLM-as-judge safely (calibration, reference, sampling)
5. Set CI gates (no regression) for every change
6. Track quality over time (leaderboards per dataset)
7. Extend the framework to RAG, agents, and guardrails

## Prerequisites

| Need | Where |
|---|---|
| Prompt evaluation | `09-genai/lectures/05-prompt-evaluation-lecture.md` |
| Retrieval metrics | `09-genai/lectures/10-retrieval-quality-lecture.md` |
| Guardrails | `09-genai/lectures/19-guardrails-and-safety-lecture.md` |
| CI gates (Phase 8) | `08-mlops/lectures/12-ci-cd-for-ml-lecture.md` |

## 1. The Framework Architecture

```python
@dataclass
class EvalCase:
    input: str
    expected: str | None = None      # gold, for exact/rubric scoring
    gold_sources: list[str] | None = None   # for retrieval scoring
    should_block: bool | None = None # for guardrail scoring
    metadata: dict = field(default_factory=dict)

@dataclass
class EvalResult:
    suite: str
    config: str                      # prompt/model/version being scored
    scores: dict[str, float]
    cases: list[dict]                # per-case detail for debugging
```

Output:
```
EvalCase(input='refund policy?', expected='...', gold_sources=['refunds.pdf'])
→ EvalResult(suite='support', config='prompt_v3', scores={'accuracy': 0.88})
```

**The design principle:** datasets + evaluators are separate from the
runner — the same suite scores any candidate (prompt, model, config),
because the suite is the *referee*, not a team.

## 2. Evaluators: The Scoring Functions

| Evaluator | Used for | Notes |
|---|---|---|
| exact_match | classification/extraction | gold labels required |
| partial_match | lists/sets | Jaccard / containment |
| rubric (LLM-judge) | open-ended (summary, generation) | calibrated + referenced |
| groundedness | RAG answers | claims must cite context (L9) |
| retrieval metrics | search stage (L10) | recall@k, MRR |
| guardrail metrics | safety layers (L19) | catch rate + FP rate |

```python
def exact_match_evaluator(case: EvalCase, output: str) -> float:
    return 1.0 if output.strip() == (case.expected or "").strip() else 0.0

def groundedness_evaluator(case: EvalCase, output: str, context: str) -> float:
    """Each claim in the output must appear (or cite) the provided context."""
    claims = extract_claims(output)
    if not claims:
        return 0.0
    return sum(1 for c in claims if c in context) / len(claims)
```

Output:
```
exact: 1.0 / 0.0 per case; groundedness: 0.92 — each evaluator scores its
own criterion; the report merges them.
```

## 3. LLM-as-Judge Done Right

The most misused evaluator. The safe pattern:

1. **Reference-optional rubric** — the judge gets the criteria, not just vibes
2. **Calibration** — periodically compare judge scores vs human scores on a sample
3. **Determinism** — temperature 0, fixed rubric, log the judge's raw output
4. **Sampling** — judge a subset; humans review the edges

```python
RUBRIC = """Score 1-5 on: (1) faithfulness to the source, (2) completeness,
(3) clarity. 5 = excellent, 1 = poor."""

def judge_scores(judge_fn, output: str, reference: str) -> dict[str, int]:
    prompt = (f"{RUBRIC}\n\nSource:\n{reference}\n\nOutput:\n{output}\n\n"
              f"JSON: {{\"faithfulness\": int, \"completeness\": int, \"clarity\": int}}")
    import json
    return json.loads(judge_fn(prompt))     # L3 structured output mandatory
```

Output:
```
{'faithfulness': 5, 'completeness': 4, 'clarity': 4} — parseable, auditable.
```

**The golden rule:** never ship an LLM-judge without calibration evidence —
judge-human agreement on a sample is the judge's own eval.

## 4. Running and Reading the Report

```python
def run_suite(suite: list[EvalCase], candidate_fn, evaluators: dict) -> EvalResult:
    """Score a candidate over a suite; return the aggregate report."""
    agg = {name: [] for name in evaluators}
    details = []
    for case in suite:
        output = candidate_fn(case.input)
        row = {"input": case.input, "output": output}
        for name, ev in evaluators.items():
            s = ev(case, output) if "context" not in ev.__code__.co_varnames \
                else ev(case, output, case.metadata.get("context", ""))
            agg[name].append(s)
            row[name] = s
        details.append(row)
    return EvalResult(suite=suite.name, config=candidate_fn.config,
                      scores={k: round(sum(v)/len(v), 3) for k, v in agg.items()},
                      cases=details)
```

Output:
```
EvalResult(suite='support', config='prompt_v3',
           scores={'accuracy': 0.88, 'groundedness': 0.92}, cases=[...])
```

**Read the cases, not just the score:** the per-case detail is the debugger —
a 0.88 accuracy with 5 specific failures names exactly what to fix.

## 5. A/B and the CI Gate

The decision loop (L5 extended to the whole framework):

```python
def compare_and_gate(baseline: EvalResult, candidate: EvalResult,
                     keys: list[str], tol: float = 0.02) -> dict:
    deltas = {k: round(candidate.scores[k] - baseline.scores[k], 3) for k in keys}
    regressed = {k: d for k, d in deltas.items() if d < -tol}
    return {"deltas": deltas, "pass": not regressed, "regressions": regressed}

print(compare_and_gate(base_prompt, cand_prompt, ["accuracy", "groundedness"]))
```

Output:
```
{'deltas': {'accuracy': 0.03, 'groundedness': -0.04}, 'pass': False,
 'regressions': {'groundedness': -0.04}}   → CI blocks the change
```

**The gate rule:** a candidate that regresses *any* tracked criterion on the
frozen suite is blocked — even if the headline metric improved.

## 6. Tracking Quality Over Time

Eval results are a time series: quality per suite per config over releases.
This is the "leaderboard" that makes regressions visible and improvements
attributable:

```python
def quality_trend(results: list[EvalResult]) -> dict[str, list[float]]:
    """Series of headline scores per suite, ordered by time."""
    series = {}
    for r in sorted(results, key=lambda x: x.metadata.get("ts", 0)):
        series.setdefault(r.suite, []).append(r.scores.get("accuracy", 0.0))
    return series
```

Output:
```
{'support': [0.84, 0.86, 0.85, 0.88], 'rag': [0.72, 0.78, 0.81]}
→ a regression between releases shows as a dip — investigate, don't ignore.
```

## Every Use Case

- **Prompt/model/config changes**: the A/B + gate loop.
- **RAG systems**: retrieval + generation scored separately (L10 + L9).
- **Agents**: completion rate + step efficiency (L14).
- **Guardrails**: attack suites catch rate + false-positive rate (L19).
- **Model selection**: same suite, different models, cost-quality table.
- **Regression protection**: every change runs the suite in CI.
- **Production monitoring**: sampled traces (L17) scored by the suite.
- **Compliance**: eval evidence as the quality assurance record.

## Real-World Use Cases for AI Engineers

- **RAG service at a fintech**: one suite (20 Q&A with gold sources +
  groundedness evaluator) runs in CI. A chunking change raised recall but
  dropped groundedness — the suite's *multi-criterion* report caught the
  trade, and the change was blocked (L7 → L10 discipline in action).
- **Support classifier**: the exact-match suite (500 frozen tickets) is the
  referee for every prompt change — the gate blocked 3 regressions in a
  quarter that would have shipped silently.
- **Agent platform**: completion-rate + step-efficiency suites gate agent
  changes; a "more capable" agent that took 2x the steps was rejected on
  efficiency — the suite made cost a first-class quality axis (L18).
- **Guardrail rollout**: the attack suite (L19) scored the new moderation
  layer: catch rate 0.97, false-positive rate 0.01 — the numbers, not
  vibes, approved the rollout.
- **Model upgrade**: same suite across old vs new model — the quality-cost
  table (new model +5% groundedness at 1.5x cost) drove the decision. The
  eval framework is the company's LLM quality bureau.

## Common Mistakes to Avoid

### Mistake 1: Gold labels from the model
Self-labeled gold measures nothing. Human labels (or validated LLM-assist).

### Mistake 2: Judge without calibration
An uncalibrated LLM-judge is a noisy opinion. Calibrate against humans.

### Mistake 3: Single-metric evals
Accuracy alone hides groundedness/safety/cost regressions. Multi-criterion.

### Mistake 4: No CI gate
Eval suites that never gate are reports, not protection.

### Mistake 5: Overfitting the frozen suite
The suite is a referee, not a training target. Refresh periodically + watch
production (L17).

### Mistake 6: Small, stale datasets
20 cases can't measure a 2% change; stale cases drift from reality. Size +
refresh.

### Mistake 7: Ignoring per-case details
The score hides which cases failed. Read the cases.

## Best Practices

1. Frozen, versioned, representative datasets with human-labeled gold
2. Multi-criterion suites (accuracy, groundedness, safety, cost)
3. Calibrate LLM-judges against human scores on a sample
4. Gate every change in CI (no regressions on any tracked criterion)
5. Track quality over time per suite (leaderboards)
6. Refresh datasets on a schedule; watch production for drift
7. Read per-case details, not just aggregates
8. Score components separately (retrieval, generation, guardrails)
9. Log eval configs + results (audit + attribution — L17 synergy)
10. Make eval evidence part of compliance records

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Exact-match suite (500 cases) | seconds | O(1) | — |
| LLM-judge suite (500 cases) | minutes + $ | O(1) | sample 10% |
| Retrieval suite | ms per case | O(1) | — |
| CI gate per change | minutes | O(1) | subset suite per PR, full nightly |

## AI Engineering Relevance

**Where this shows up:** the quality infrastructure of every LLM system. The
eval framework is how GenAI engineering becomes engineering — measured,
gated, and auditable.

| Concept here | Used for |
|---|---|
| Datasets | the frozen referees |
| Evaluators | criteria as functions |
| A/B + gates | decisions with numbers |
| Leaderboards | quality over time |
| LLM-judge | calibrated opinion at scale |

**Scale note:** at 20 features × 10 changes/week, the CI-gated suite is the
only way to keep quality from drifting — each change is measured before it
ships. The framework's value compounds with system size: it is the quality
bureau for the whole LLM platform.

## Practice Exercises

### Exercise 1: Suite + Exact Eval (Easy)
Build `EvalCase`/`EvalResult` and an exact-match evaluator; score a 5-case
suite by hand and verify the aggregate.

### Exercise 2: Multi-Evaluator Report (Medium)
Add a groundedness evaluator; score a mixed suite and assert the report
contains both scores per config.

### Exercise 3: Gate Logic (Medium)
Implement `compare_and_gate` and test: improvement passes, single-criterion
regression blocks, tie passes.

### Exercise 4: Full Framework (Hard)
Build `run_suite` + `compare_and_gate` + `quality_trend` over 3 configs × a
10-case suite; assert the winner is promoted, the regression is blocked, and
the trend series is correct.

## Summary

| Concept | Description |
|---|---|
| Datasets | frozen referees with gold labels |
| Evaluators | criteria as scoring functions |
| Runner + report | aggregate + per-case detail |
| A/B + gates | measured decisions, blocked regressions |
| Leaderboards | quality over time |
| LLM-judge | calibrated, sampled opinion |

The evaluation framework is the quality infrastructure of GenAI: frozen
datasets, functional evaluators, CI-gated comparisons, and quality tracking.
It converts every "feels better" into a number, every change into a measured
candidate, and every regression into a blocked merge — the discipline that
makes LLM engineering engineering.

## Quick Reference

| Task | Idiom |
|---|---|
| Score a change | run frozen suite → compare scores |
| Gate | block any criterion regression |
| Judge open-ended | calibrated LLM-judge, sampled |
| Track | leaderboard per suite over time |
| Debug | read per-case details |

## Next Steps

Next: **[21 Fine-Tuning](21-fine-tuning-lecture.md)** — going beyond prompts:
adapting the model to your task and domain.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://docs.confident-ai.com/, https://docs.ragas.io/
