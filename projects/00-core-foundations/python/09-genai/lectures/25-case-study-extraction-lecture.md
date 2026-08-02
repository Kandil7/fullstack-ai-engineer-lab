# GenAI — 25: Case Study — Production Extraction Pipeline

## Topic Overview

This lecture is the third capstone: a complete, production-grade **document
extraction pipeline** — unstructured documents in, validated structured data
out — integrating the structured-output discipline (L3), document processing
(L8), evaluation (L20), and the Phase 8 assembly line (versioning L3,
validation L10, serving L7, monitoring L11, CI L12, cost L15). Extraction is
the quiet workhorse of enterprise GenAI: invoices, claims, contracts, and
forms converted into rows the business actually runs on.

The scenario: **"ClaimExtract"** — an insurance claims-processing pipeline
that reads claim PDFs and produces validated, schema-conformant records
(`claimant`, `policy_no`, `date`, `amount`, `diagnosis`, `status`) that flow
directly into the claims database. The companion exercise
(`25-case-study-extraction.py`) implements the core loop; this lecture is the
architect's tour — every decision measured, every layer a Lecture.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Design a production extraction pipeline: parse → extract → validate → repair → gate
2. Apply the structured-output ladder (L3) for schema-guaranteed fields
3. Build the repair loop (validation errors fed back to the model)
4. Validate and quarantine bad extractions (never corrupt the database)
5. Measure extraction quality (field accuracy, repair rate) and gate changes (L20)
6. Batch-process at scale with versioning, observability, and cost control
7. Trace a document from PDF to database row end to end

## Prerequisites

| Need | Where |
|---|---|
| Structured output | `09-genai/lectures/03-structured-output-lecture.md` |
| Document processing | `09-genai/lectures/08-document-processing-lecture.md` |
| Evaluation | `09-genai/lectures/20-evaluation-frameworks-lecture.md` |
| Phase 8 validation/CI | `08-mlops/lectures/10,12` |

## 1. The Architecture

```
[claim PDF] → [parse L8: text + tables] → [clean/structure]
     → [extract L3: structured output, schema-guaranteed]
     → [validate pydantic L3: types, ranges, enums]
     → [repair loop L3: errors → re-prompt with feedback (capped)]
     → [gate L10/L20: field accuracy, per-field confidence]
     → [write DB (validated rows)]  /  [quarantine + alert (bad rows)]
     → [trace L17 + metrics L11 + cost L15]
```

Every stage is a Lecture; the pipeline is the integration.

## 2. The Extraction Stage (L3)

The extraction prompt demands JSON matching a strict schema — the L3 ladder
(prompt → JSON mode → constrained decoding) applied for reliability:

```python
CLAIM_SCHEMA = {
    "type": "object",
    "properties": {
        "claimant": {"type": "string"},
        "policy_no": {"type": "string", "pattern": "^POL-\\d{6}$"},
        "date": {"type": "string", "format": "date"},
        "amount": {"type": "number", "minimum": 0},
        "diagnosis": {"type": "string"},
        "status": {"type": "string", "enum": ["OPEN", "REVIEW", "DENIED"]},
    },
    "required": [...], "additionalProperties": False,
}

def extract_claim(doc_text: str, llm_client) -> ClaimRecord:
    raw = llm_client.complete(
        EXTRACT_PROMPT.format(text=doc_text),
        response_format={"type": "json_schema",
                         "json_schema": {"name": "claim", "strict": True,
                                         "schema": CLAIM_SCHEMA}})
    return ClaimRecord.model_validate_json(raw)      # L3: validate at the boundary
```

Output:
```
ClaimRecord(claimant='Jane Doe', policy_no='POL-123456', date='2026-07-01',
            amount=2480.5, diagnosis='Knee injury', status='REVIEW')
```

## 3. The Repair Loop (L3)

Validation failures feed back to the model — a bounded, logged self-correction:

```python
def extract_with_repair(doc_text: str, llm_client, *, max_repairs=2) -> ClaimRecord:
    raw = llm_client.complete(EXTRACT_PROMPT.format(text=doc_text))
    for attempt in range(max_repairs + 1):
        try:
            return ClaimRecord.model_validate_json(raw)
        except (ValidationError, json.JSONDecodeError) as e:
            if attempt == max_repairs:
                raise ExtractionFailed(doc_id=..., error=str(e))
            raw = llm_client.complete(
                f"Your previous extraction was invalid: {e}\n"
                f"Fix ONLY the invalid fields. Document:\n{doc_text}")
    raise RuntimeError("unreachable")
```

Output:
```
attempt 1: {"amount": "2,480.5"} → invalid (string) → re-prompt with error
attempt 2: {"amount": 2480.5} → valid ✓
```

**The repair rate is a quality metric** (L20): a rising repair rate signals
the schema or the prompt is out of sync with the documents — monitored, not
ignored.

## 4. Validation and Quarantine: Never Corrupt the Database

The extraction pipeline's iron rule: **only validated rows reach the
database**; everything else is quarantined with a reason and alerted (Phase 8
L10 discipline applied to extraction):

```python
def process_batch(docs: list[Doc], llm_client) -> dict:
    good, bad = [], []
    for doc in docs:
        try:
            record = extract_with_repair(doc.text, llm_client)
            good.append(record)
        except (ValidationError, ExtractionFailed) as e:
            bad.append({"doc_id": doc.id, "reason": str(e)})
            alert_quarantine(doc.id, e)         # human review queue
    return {"accepted": len(good), "quarantined": len(bad),
            "quarantine_detail": bad}

report = process_batch(batch, client)
print(report)
```

Output:
```
{'accepted': 498, 'quarantined': 2, 'quarantine_detail':
 [{'doc_id': 'C-7731', 'reason': "amount failed range check"}, ...]}
```

**The discipline:** 2 quarantined out of 500 is a *success* — the system
caught them instead of letting bad rows into the claims database. The
quarantine queue is a human-review feature, not a failure.

## 5. Evaluation and the Ship Gate (L20)

Extraction quality is measured on a frozen golden set (documents with
human-verified fields); every prompt/schema change runs the gate:

```python
EVALUATORS = {
    "field_accuracy": lambda case, out: exact_match(case.expected, out),
    "schema_validity": lambda case, out: 1.0 if out else 0.0,
}

def extraction_ship_gate(candidate, suite) -> tuple[bool, dict]:
    report = run_suite(suite, candidate, EVALUATORS)          # L20
    ok = report.scores["field_accuracy"] >= BASELINE["field_accuracy"] - 0.01
    return ok, report.scores

print(extraction_ship_gate(candidate_extractor, GOLDEN_SUITE))
```

Output:
```
(True, {'field_accuracy': 0.986, 'schema_validity': 1.0})
— schema-valid 100%, field-accurate 98.6%; change ships.
```

**Per-field accuracy matters:** if `amount` is 99% and `diagnosis` is 91%,
the pipeline's weakest field is the quality ceiling — the report names it.

## 6. Batch Operations: Scale, Versioning, Cost

Production extraction is a batch pipeline — Phase 8 orchestration (L9) +
versioning (L3) + cost (L15):

| Concern | Practice |
|---|---|
| Versioning | documents + schema + prompt versions recorded per batch (L3) |
| Orchestration | batch DAG with retries + checkpointing (L9) |
| Cost | batch token budgets, caching identical docs, smaller model tiering (L18) |
| Observability | per-document traces: tokens, latency, cost, repair count (L17) |
| Monitoring | repair-rate and field-accuracy drift alerts (L11) |

```python
def batch_cost(records: list[dict], cost_per_m: float) -> float:
    total_tokens = sum(r["prompt_tokens"] + r["completion_tokens"]
                       for r in records)
    return round(total_tokens / 1e6 * cost_per_m, 2)
```

Output:
```
$18.40 for 500 claims — a line item on the L15 dashboard, not a surprise.
```

## Every Use Case

- **Insurance claims**: ClaimExtract's origin — PDFs to validated rows.
- **Invoice processing**: vendor, amount, due date → accounting system.
- **Contract review**: parties, dates, obligations → CLM database.
- **Medical intake**: referral letters → structured records (with guardrails, L19).
- **Forms/emails**: applications, inquiries → CRM rows.
- **Financial documents**: filings → structured facts for analysts.
- **HR documents**: resumes/CVs → structured profiles.
- **Any "unstructured → structured" workload**: the pattern is universal.

## Real-World Use Cases for AI Engineers

- **Insurance claims (ClaimExtract)**: 500 claims/hour with 98.6% field
  accuracy, 100% schema validity, and a quarantine queue for the 1-2% that
  need humans — the pipeline's *measured* quality is what the audit approved.
- **Accounts payable**: invoice extraction feeds the payment system; a
  wrong amount is a payment error — the range validation + repair loop + DB
  gate is the control that makes it safe.
- **Legal onboarding**: contract extraction (parties, dates, terms) fills the
  CLM; the schema version is part of the contract record — when the schema
  changed, the pipeline versioned the change and the audit trail held.
- **Healthcare admin**: referral letters → structured intake; the output gate
  (L19) blocks PII from leaking into logs, and the field-accuracy eval gates
  every prompt change.
- **Fintech document ops**: 1M documents/month through the batch pipeline;
  identical docs are cached (L18), the batch is checkpointed (L9), and the
  cost dashboard shows extraction at a per-document unit cost (L15).

## Common Mistakes to Avoid

### Mistake 1: Writing unvalidated extractions to the database
One bad row in a claims DB is an incident. Gate everything.

### Mistake 2: No repair loop
A single-pass extractor quarantines fixable documents. Repair (bounded).

### Mistake 3: Schema too loose
Open strings accept garbage (L3). Enums, patterns, ranges, required fields.

### Mistake 4: No per-field measurement
Aggregate accuracy hides a weak field. Track per-field accuracy (L20).

### Mistake 5: No versioning
Schema/prompt/document versions drift silently. Version per batch (L3).

### Mistake 6: No cost visibility
Batch extraction at scale is a real bill. Token budgets + dashboards (L15/L18).

### Mistake 7: Repair loops that never end
Unbounded repair burns cost. Cap repairs; quarantine the rest (L3).

## Best Practices

1. Apply the L3 ladder: constrained decoding ≥ JSON mode ≥ prompt
2. Validate at the boundary with pydantic; strict schemas (enums, ranges)
3. Repair bounded and logged; quarantine the rest with reasons
4. Only validated rows reach the database; quarantine + alert (L10)
5. Measure per-field accuracy + repair rate on a golden set (L20)
6. Gate every prompt/schema change in CI (L12)
7. Version documents, schema, and prompt per batch (L3)
8. Track tokens/cost per batch; cache identical docs (L15/L18)
9. Trace per document: tokens, latency, repairs (L17)
10. Monitor repair-rate and accuracy drift (L11)

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Parse one PDF | ms | O(n) | — |
| Extract + validate | 0.5-3s + tokens | O(1) | smaller model / JSON mode |
| Repair retry | +1 call | O(1) | better schema/prompt |
| Golden eval | per release | O(golden set) | subset in CI |
| Batch 500 docs | minutes | O(n) | parallelize (L9) |

## AI Engineering Relevance

**Where this shows up:** every enterprise unstructured→structured workload.
Extraction is the highest-volume, highest-trust GenAI application — the
discipline (schema, validation, repair, gates, versioning) is what lets it
run unattended at scale.

| Concept here | Used for |
|---|---|
| Structured output | schema-guaranteed fields |
| Validate + quarantine | the DB gate |
| Repair loop | self-correcting extraction |
| Per-field evals | measurable quality ceilings |
| Batch discipline | scale + versioning + cost |

**Scale note:** at 1M documents/month, batch orchestration (L9), caching
(L18), and per-batch cost (L15) are the operating economics; the golden eval +
quarantine queue are the quality and safety backbone. Extraction is the
production workhorse — it runs on the discipline of the whole phase.

## Practice Exercises

### Exercise 1: Schema + Validate (Easy)
Define a `ClaimRecord` pydantic model (with enums/ranges) and test valid,
invalid-type, and out-of-range cases.

### Exercise 2: Repair Loop (Medium)
Implement `extract_with_repair` with a mock client failing once; assert the
repair succeeds, the retry count is capped, and a persistent failure raises
`ExtractionFailed`.

### Exercise 3: Quarantine Gate (Medium)
Implement `process_batch` and assert: valid docs are accepted, invalid docs
are quarantined with reasons, and no invalid record reaches the "DB".

### Exercise 4: Per-Field Eval + Gate (Hard)
Build a 20-doc golden suite with per-field expected values; compute per-field
accuracy; implement `extraction_ship_gate` and assert a candidate regressing
`amount` accuracy is blocked.

## Summary

| Concept | Description |
|---|---|
| Structured output | schema-guaranteed fields (L3) |
| Repair loop | bounded self-correction |
| Validate + quarantine | the database gate |
| Per-field evals | measurable quality (L20) |
| Batch discipline | versioning, cost, traces |

ClaimExtract is the production extraction template: parse (L8), extract with
the L3 ladder, repair bounded, validate and quarantine at the gate, measure
per-field on a golden set, and run as a versioned, costed, traced batch. The
pipeline converts unstructured documents into *trusted* data — which is
exactly what enterprise GenAI is for.

## Quick Reference

| Task | Idiom |
|---|---|
| Extract | strict JSON schema + constrained decoding (L3) |
| Repair | feed validation errors back, capped |
| Gate | validated rows only; quarantine + alert |
| Measure | per-field accuracy on golden set (L20) |
| Operate | batch, versioned, costed, traced (L9/L15/L17) |

## Next Steps

This completes **Phase 9 — GenAI**. Return to the master program:
**[Master AI Engineering Roadmap](../../README.md)** or review the
**[Phase 8 MLOps recap](../../08-mlops/lectures/16-case-study-e2e-lecture.md)**.
Official docs: https://docs.pydantic.dev/latest/, https://platform.openai.com/docs/guides/structured-outputs
