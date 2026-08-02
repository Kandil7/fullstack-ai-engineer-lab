# MLOps — 10: Data Validation

## Topic Overview

Data validation is checking that the data entering your pipelines, training
jobs, and serving endpoints **matches its contract** — schema, types, ranges,
uniqueness, and distributions — and failing fast with a clear message when it
doesn't. In production ML, bad data is the #1 cause of silent model
degradation: the model keeps serving, but the inputs drifted off the training
distribution and the predictions are quietly wrong. Validation is the tripwire
that catches corruption at the boundary instead of letting it poison the model.

The standard tool is **pandera** (schema validation for pandas DataFrames,
with statistical checks) alongside **Great Expectations** (data profiling and
expectation suites) and **TensorFlow Data Validation** (TFDV) for
training-serving skew detection. All three implement the same idea: *declare a
contract, run every dataset against it, fail loudly on violation.* Validation
is a first-class pipeline stage (Lecture 09) with its own DAG node.

Why this matters for an AI engineer: validation is cheap insurance. A 30-second
validation stage at every boundary (ingest, feature store, model input, batch
output) prevents the multi-day incidents that happen when bad data reaches a
model silently. The three boundaries every ML system needs: **raw ingest**,
**training data**, and **serving input** (training-serving skew).

## Learning Objectives

By the end of this lecture, you will be able to:
1. Declare a DataFrame schema with pandera (types, nullability, ranges)
2. Add statistical checks: allowed values, min/max, uniqueness, distribution shape
3. Validate at ingest, train, and serve boundaries
4. Detect training-serving skew (feature distribution drift at serving)
5. Build a validation failure report that an engineer can act on
6. Decide fail-fast vs quarantine-and-alert policies per stage
7. Version validation rules with the pipeline (rules change = new dataset version)

## Prerequisites

| Need | Where |
|---|---|
| pandas basics | `03-libraries/pandas/` |
| Data versioning | `08-mlops/lectures/03-data-versioning-lecture.md` |
| Pipeline orchestration | `08-mlops/lectures/09-pipeline-orchestration-lecture.md` |
| Statistics basics | `07-machine-learning/` |

## 1. Schema Validation with Pandera

The basic contract: column names, dtypes, nullability. This alone catches the
most common failure modes — a column renamed by a source change, an int
becoming a float, a column going all-null.

```python
import pandera as pa

schema = pa.DataFrameSchema(
    columns={
        "customer_id": pa.Column(int, unique=True),
        "tenure": pa.Column(float, nullable=False),
        "churn": pa.Column(int, pa.Check.isin([0, 1])),
    },
    strict=True,   # reject unknown columns
)

try:
    schema.validate(df)
    print("PASS: schema valid")
except pa.errors.SchemaError as e:
    print("FAIL:", e)
```

Output (conceptually):
```
PASS: schema valid
```

`strict=True` is the discipline-setting flag: unknown columns are a signal of
a changed source, and you want to know immediately.

## 2. Statistical Checks: Beyond Types

Types are the floor; ranges and distributions are the real tripwires. Pandera
checks cover: value ranges (age in [0, 120]), allowed sets, uniqueness, and
distributional checks (mean/std drift vs a reference).

```python
schema = pa.DataFrameSchema(
    columns={
        "amount": pa.Column(float, pa.Check.in_range(0.0, 100_000.0)),
        "status": pa.Column(str, pa.Check.isin(["APPROVED", "DECLINED"])),
        "txn_id": pa.Column(str, unique=True),
    },
)
```

Output (conceptually):
```
PASS: amount in range, statuses valid, txn_ids unique
```

A check that fails is a **signal**, not just an error: amount > 100k might be
a data bug *or* a real business change — the validation report should carry
counts and sample values so an engineer can triage.

## 3. The Three Validation Boundaries

| Boundary | What to validate | Failure policy |
|---|---|---|
| Raw ingest | schema, nulls, duplicates, encoding | quarantine + alert |
| Training data | ranges, distributions, class balance | fail-fast (block training) |
| Serving input | same schema + feature ranges as training | reject request / alert on drift |

Training-serving skew is the nastiest: the serving input differs from training
in distribution (e.g. a feature that was ≤0.5 at train time now arrives as
3.0). TFDV computes statistics at serving and compares to the training
statistics, flagging drift beyond a threshold.

```python
def check_serving_skew(ref_stats: dict, live_stats: dict, threshold: float = 0.1) -> list[str]:
    """Flag features whose live distribution drifted from training."""
    flags = []
    for feat, ref in ref_stats.items():
        drift = abs(live_stats[feat]["mean"] - ref["mean"]) / max(abs(ref["mean"]), 1e-9)
        if drift > threshold:
            flags.append(f"{feat}: drift {drift:.2%}")
    return flags

print(check_serving_skew({"amount": {"mean": 50.0}}, {"amount": {"mean": 300.0}}))
```

Output (conceptually):
```
['amount: drift 500.00%']
```

## 4. Validation Reports: Fail Loudly, Triagable

A good validation failure is *actionable*: it names the rule, the failing
rows, and a sample. Never log "validation failed" with no details.

```python
def summarize_failures(schema, df) -> dict:
    """Return a human-actionable failure summary."""
    report = {"total_rows": len(df), "violations": {}}
    for col, col_schema in schema.columns.items():
        invalid = ~df[col].map(lambda v: _satisfies(col_schema.checks, v))
        if invalid.any():
            report["violations"][col] = {
                "count": int(invalid.sum()),
                "samples": df.loc[invalid, col].head(5).tolist(),
            }
    return report
```

Output (conceptually):
```
{'total_rows': 10000, 'violations': {'amount': {'count': 34,
  'samples': [120000.0, 250000.0, ...]}}}
```

## 5. Policies: Fail-Fast vs Quarantine-and-Alert

Different boundaries deserve different policies:

- **Fail-fast (blocking)**: training input fails → stop training. Never train
  on corrupt data; the pipeline retries after the source is fixed.
- **Quarantine + alert**: ingest failures quarantine bad rows to a dead-letter
  table and alert — the pipeline continues with the good rows, and the
  quarantine is investigated in parallel.
- **Reject (serving)**: a serving request that violates the schema is rejected
  with a clear error; a *distributional* drift is alerted, not rejected
  (rejecting real users' data is itself a production decision).

```python
def quarantine_bad_rows(df, schema, dead_letter_path: str):
    valid = schema.validate(df, lazy=True)          # collect ALL failures
    bad = df.loc[valid.failure_cases.index]
    bad.to_csv(dead_letter_path, index=False)
    return df.drop(index=bad.index)
```

Output (conceptually):
```
34 bad rows quarantined to outputs/quarantine/2026-08-02.csv; pipeline continues
```

## Every Use Case

- **Ingest pipelines**: catching source-format changes before they spread.
- **Training gates**: never training on schema-violating or drifted data.
- **Serving skew detection**: TFDV-style monitoring of live vs train statistics.
- **Feature store**: validating computed features before serving them.
- **Batch output**: validating scoring output (no NaNs, probabilities in [0,1])
  before it reaches downstream systems.
- **LLM structured output (Phase 9)**: validating that an LLM's JSON output
  matches the declared schema before it is used — the same pandera/JSON-schema
  idea applied to model output.
- **Data migration**: validating after a warehouse migration that the data
  contract still holds.
- **Regulatory**: demonstrating that production data met quality gates (audit
  evidence).

## Real-World Use Cases for AI Engineers

- **Fintech transaction ingest**: a source changed a currency code from ISO to
  internal codes; validation flagged 2% of rows as `status` violations and
  quarantined them, alerting the team *before* the fraud model ingested
  garbage — a silent-data incident averted in minutes.
- **E-commerce training gate**: a schema check blocked a training run whose
  `price` feature had 40% nulls after a catalog migration; without the gate,
  the retrained ranking model would have shipped with corrupted features —
  the fail-fast policy protected production from a bad retrain.
- **Serving skew at a bank**: TFDV flagged `income` mean drift of 40% between
  training and live data after a policy change; the team rebuilt the training
  data rather than trusting a model that had silently started seeing
  out-of-distribution inputs.
- **RAG ingestion (Phase 9)**: chunk validation — empty chunks, oversized
  chunks, lost metadata — gates document ingestion; a corrupt PDF batch is
  quarantined, not embedded into the index.
- **Healthcare**: a clinical data feed's validation report is part of the
  quality review; any schema violation pauses the pipeline and pages the
  data owner.

## Common Mistakes to Avoid

### Mistake 1: Type-only validation
```
# WRONG — dtypes fine, but values are garbage
# (validate ranges, uniqueness, distributions too)
```

### Mistake 2: Failing on all-null vs empty column
An empty column can be "genuinely empty" — distinguish schema violations
(nullability) from statistical anomalies (empty with non-null contract).

### Mistake 3: No boundary between train and serve checks
Training failures and serving skew need different policies; one blunt check
fits neither.

### Mistake 4: Logging "validation failed" without details
Reports must carry rule, counts, and samples to be triageable.

### Mistake 5: Validating only at ingest
Corruption happens at every boundary — schema drift can appear between stages.

### Mistake 6: Ignoring versioned rules
Validation rules change; a fixed ruleset silently becomes stale. Version rules
with the pipeline (a rules change should produce a new dataset version).

## Best Practices

1. Validate at every boundary: ingest, train, serve, output
2. Use schema (types/nullability) + statistical (range/unique/distribution) checks together
3. Fail-fast for training; quarantine-and-alert for ingest
4. Make failure reports actionable: rule, counts, sample values
5. Detect training-serving skew with distribution drift thresholds
6. Version validation rules with the pipeline
7. Alert the owning team with run IDs on every gate failure
8. Validate LLM structured output against the declared schema (Phase 9)
9. Automate the checks in CI with the same schema object
10. Keep reference statistics from a validated, frozen training snapshot

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Validate 10M rows | seconds | O(n) | sample-based checks for distributions |
| Full schema check | O(n cols) | O(1) | — |
| Distribution drift | O(n) stats | O(1) | streaming quantiles |
| Quarantine write | O(bad rows) | O(bad) | dead-letter table |

## AI Engineering Relevance

**Where this shows up:** every pipeline boundary, every retraining gate, every
serving endpoint — validation is the tripwire between "data problem" and
"model incident".

| Concept here | Used for |
|---|---|
| Schema contract | catching source changes early |
| Statistical checks | catching drift before it poisons training |
| Train/serve skew | the #1 silent degradation cause |
| Quarantine policy | keep the pipeline alive while triaging |

**Scale note:** at petabyte scale, validate in streaming or sampled passes;
at any scale, a 30-second gate at the boundary is cheaper than a 3-day
incident. Validation cost is linear; the cost of *not* validating grows
quadratically with the number of downstream consumers.

## Practice Exercises

### Exercise 1: Schema Gate (Easy)
Define a pandera-style schema for a 3-column frame (id unique, amount in
[0, 1e6], status in a set) and write `validate_or_raise(df, schema)` that
raises a clear message on violation.

### Exercise 2: Skew Detector (Medium)
Implement `check_serving_skew(ref_stats, live_stats, threshold)` (section 3)
and assert it flags a 40% mean drift but not a 5% one.

### Exercise 3: Quarantine Policy (Medium)
Write `quarantine_bad_rows(df, schema, dead_letter_path)` that writes bad rows
to a dead-letter CSV and returns the clean frame; assert good rows are
preserved and bad rows are in the file.

### Exercise 4: Validation Report (Hard)
Build `summarize_failures` that returns per-column violation counts + samples,
and a `triage(rule, count)` helper that classifies a failure as `fix-source`
vs `review-biz-change` based on the rule type.

## Summary

| Concept | Description |
|---|---|
| Schema contract | types, nullability, names |
| Statistical checks | ranges, uniqueness, distributions |
| Boundaries | ingest / train / serve / output |
| Train-serve skew | the silent degradation tripwire |
| Policies | fail-fast, quarantine, reject |

Data validation is the cheapest incident-prevention an ML system can buy: a
declared contract plus a gate at every boundary catches the corruptions,
drifting features, and source changes that would otherwise poison models
silently. It turns "bad data disaster" into "actionable report".

## Quick Reference

| Task | Idiom |
|---|---|
| Declare schema | `pa.DataFrameSchema(columns={...})` |
| Validate | `schema.validate(df)` / `lazy=True` for all failures |
| Skew check | compare live mean/std vs frozen training stats |
| Quarantine | write bad rows to dead-letter, continue with good |
| Fail-fast | raise on training-input violation |

## Next Steps

Next: **[11 Monitoring and Drift](11-monitoring-and-drift-lecture.md)** —
watching production models for degradation after deployment.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://pandera.readthedocs.io/, https://greatexpectations.io/,
https://www.tensorflow.org/tfx/data_validation
