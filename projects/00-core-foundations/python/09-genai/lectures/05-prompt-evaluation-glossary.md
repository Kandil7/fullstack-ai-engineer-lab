# Prompt Evaluation — Glossary 05

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Baseline | Evaluation | The pre-change score used for comparison |
| Exact Match | Metric | Score 1 only if output equals reference |
| Golden Set | Evaluation | Fixed (prompt, reference) pairs for regression |
| LLM-as-Judge | Metric | A model scoring open-ended output quality |
| Rubric | Metric | Scoring against defined criteria |
| Substring Match | Metric | Score 1 if reference appears in output |
| Suite Score | Evaluation | Aggregated score across a golden set |
| Regression | Evaluation | Detecting prompt-score drops over time |

## Detailed Definitions
### Baseline
**Definition**: The recorded score before a change; the only valid comparison.
**Related**: Suite Score

### Exact Match
**Definition**: Binary metric; 1 when output equals the reference exactly.
**Related**: Substring Match

### Golden Set
**Definition**: A curated set of prompts with reference outputs, used to
evaluate prompt versions.
**Related**: Regression

### LLM-as-Judge
**Definition**: Using a model to rate output quality per rubric or preference.
**Related**: Rubric

### Rubric
**Definition**: Defined criteria (e.g. 1-5 correctness, completeness) applied
to each output.
**Related**: LLM-as-Judge

### Substring Match
**Definition**: Binary metric; 1 when a required phrase appears in the output.
**Related**: Exact Match

### Suite Score
**Definition**: The aggregate (e.g. mean) of per-sample scores on a set.
**Related**: Baseline

### Regression
**Definition**: A drop in suite score after a change; caught by re-running.
**Related**: Golden Set

## Key Concepts Summary
### The Loop
- Baseline → change → re-score → keep if better

### The Rules
- Match metric to output type
- Golden sets rot; refresh them

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Golden set — ___
2. Exact match — ___
3. LLM-as-judge — ___
4. Baseline — ___
5. Regression — ___

**Answers:** 1-c, 2-b, 3-e, 4-a, 5-d where a=pre-change score, b=output equals
reference, c=fixed eval pairs, d=score drop, e=model rates quality.
