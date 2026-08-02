# GenAI — 03: Structured Output

## Topic Overview

Structured output is the practice of forcing an LLM to return
**schema-valid, machine-parseable data** — JSON, or constrained text — instead
of free-form prose. LLMs natively emit text; production systems consume JSON.
The gap between them is the source of most "LLM integration" pain: unclosed
braces, hallucinated keys, wrong types, extra commentary around the JSON.
Structured output closes that gap with three escalating techniques:
(1) prompting with a schema, (2) JSON mode, and (3) **constrained/grammar
decoding** (used by providers like OpenAI's `response_format` and by local
engines like vLLM/Outlines that literally mask illegal tokens during
generation).

Why this matters: nearly every production LLM feature is downstream of
structured output — extraction (L25), function/tool calling (L13), evaluation
(L20), agent state machines (L14), and RAG answer synthesis. A system that
cannot reliably get valid JSON out of the model cannot be reliable at all.
This lecture gives you the full ladder, plus validation so that whatever the
model emits, the program never crashes on it.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Prompt for JSON with an explicit schema (the baseline technique)
2. Use JSON mode / `response_format` for guaranteed-valid JSON
3. Use constrained decoding (OpenAI structured outputs, Outlines, vLLM guided) for guaranteed schema compliance
4. Validate and repair model JSON with pydantic
5. Handle the failure modes: prose-wrapped JSON, wrong keys, nested errors
6. Choose the right rung of the ladder for reliability vs flexibility
7. Apply the same discipline to other constrained outputs (CSV, enums)

## Prerequisites

| Need | Where |
|---|---|
| LLM fundamentals | `09-genai/lectures/01-llm-fundamentals-lecture.md` |
| API clients | `09-genai/lectures/02-api-clients-lecture.md` |
| pydantic | `05-web-frameworks/fastapi/` |
| JSON | `01-core-python/` |

## 1. Rung 1: Prompting with a Schema

The baseline: tell the model exactly what JSON to emit. Works reasonably, but
is *soft* — the model may comply or not. It is the floor, never the ceiling.

```python
PROMPT = """Extract the following fields as JSON only (no prose):
{"name": str, "age": int, "is_subscribed": bool, "plan": "free"|"pro"}
Text: John Doe, 34 years old, pays monthly for pro."""

# response: {"name": "John Doe", "age": 34, "is_subscribed": true, "plan": "pro"}
```

Output:
```
{"name": "John Doe", "age": 34, "is_subscribed": true, "plan": "pro"}
```

Weaknesses: models add "Here is the JSON:" wrappers, wrap in markdown fences,
or drift the keys. Never trust rung 1 alone in production.

## 2. Rung 2: JSON Mode

JSON mode (OpenAI `response_format={"type": "json_object"}`, Anthropic's
structured output variants) guarantees the *format* is valid JSON — not that it
matches your schema.

```python
from openai import OpenAI

client = OpenAI()
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system",
         "content": "Output JSON. Schema: {\"name\": str, \"age\": int, \"plan\": str}"},
        {"role": "user", "content": "Extract: Jane, 28, on the pro plan."},
    ],
    response_format={"type": "json_object"},
)
import json
data = json.loads(resp.choices[0].message.content)
print(data)
```

Output:
```
{'name': 'Jane', 'age': 28, 'plan': 'pro'}
```

JSON mode eliminates "it's not valid JSON" — but `age` could still be `"28"`
(a string), keys could be missing, and the model could invent fields. Format
guaranteed, *schema not*. Validate anyway.

## 3. Rung 3: Constrained Decoding (Schema-Guaranteed)

Constrained/structured decoding masks illegal tokens *during generation*, so
the output is **provably schema-valid** — impossible to violate. OpenAI's
Structured Outputs (`response_format` with a JSON schema) does this server-side;
local engines (Outlines, vLLM guided decoding, guidance) do it with a local
grammar.

```python
from openai import OpenAI

client = OpenAI()
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user",
               "content": "Extract: Bob, 41, on the free plan."}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "user_extract",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "plan": {"type": "string", "enum": ["free", "pro"]},
                },
                "required": ["name", "age", "plan"],
                "additionalProperties": False,
            },
        },
    },
)
print(resp.choices[0].message.content)
```

Output:
```
{"name": "Bob", "age": 41, "plan": "free"}
```

The schema *constrains the token stream*: `age` cannot be a string, `plan`
cannot leave the enum, extra keys are impossible. This is the reliability
ceiling — the choice when a malformed response has real cost.

## 4. Rung 4: Validate and Repair (The Safety Net)

Whatever the rung, **validate** the output with pydantic — and repair when
feasible. This is the AI engineer's iron rule: never trust the model's output;
always check it at the boundary.

```python
from pydantic import BaseModel, Field, ValidationError
import json

class UserExtract(BaseModel):
    name: str
    age: int = Field(ge=0, le=120)
    plan: str = Field(pattern="^(free|pro)$")

def safe_parse(raw: str) -> UserExtract:
    """Parse + validate; raise a clear error on any mismatch."""
    try:
        data = json.loads(raw)
        return UserExtract.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"model output failed validation: {e}") from e
```

Output:
```
UserExtract(name='Bob', age=41, plan='free')
# {"age": "41"}        → ValidationError (string not int) → clear ValueError
# {"plan": "enterprise"} → ValidationError (not in enum) → clear ValueError
```

Validation turns "the model said something weird" into a *typed, catchable,
loggable* event. Downstream code never sees raw model text.

## 5. Repair Strategies: When Validation Fails

Even with all rungs, output can fail. The repair ladder:

```python
def extract_with_repair(client, text: str, schema, *, max_repairs=2):
    """Validate → on failure, re-prompt the model with the error."""
    raw = client.complete(text)          # rung 1-3 call
    for _ in range(max_repairs):
        try:
            return schema.model_validate(json.loads(raw))
        except (json.JSONDecodeError, ValidationError):
            # give the model its own error as feedback — a repair loop
            raw = client.complete(
                f"Your previous JSON was invalid. Fix it.\nPrevious: {raw}\n"
                f"Schema: {schema.schema()}")
    raise ValueError("could not repair model output")
```

Output:
```
attempt 1: {"age": "41"}  → invalid → re-prompt with error
attempt 2: {"age": 41}    → valid ✓
```

The repair loop uses the model's own output as input — a cheap, effective
self-correction. Cap repairs (cost) and log the repair rate (quality signal).

## 6. Constrained Non-JSON Outputs

The same discipline applies to CSV, enums, and structured text:
- Enums/classification: prompt + constrain to allowed values; validate membership.
- CSV: prompt for header + rows; validate parse; never parse raw.
- Dates/numbers: validate format + range.
- Tables: JSON-mode with an array schema, validated by pydantic.

```python
VALID = {"approve", "reject", "escalate"}
def classify_verdict(raw: str) -> str:
    v = raw.strip().lower()
    if v not in VALID:
        raise ValueError(f"verdict '{raw}' not in {VALID}")
    return v
```

Output:
```
"APPROVE" → "approve" ✓ ; "maybe" → ValueError (not in allowed set)
```

## Every Use Case

- **Document extraction**: invoices, claims, contracts → structured records (L25).
- **Tool/function calling**: the arguments to tools must be valid JSON (L13).
- **Evaluation**: LLM-as-judge scores must be parseable (L20).
- **Database inserts**: extracted fields go straight into rows — schema-validated.
- **Agent state machines**: the next action is a constrained enum (L14).
- **Data pipelines**: LLM enrichment outputs feed pandas — validated first.
- **Forms/UI**: extracted values populate structured UI state.
- **RAG answers with sources**: answer + citation list as JSON (L9, L23).
- **Multi-step workflows**: each step's output validates before the next runs.

## Real-World Use Cases for AI Engineers

- **Insurance claims extraction**: a claims processor must get `{claimant,
  policy_no, date, amount, diagnosis}` from medical PDFs. Rung 3 (structured
  outputs) + pydantic validation means the *system* — not a reviewer — catches
  every malformed extraction; repair loops fix the rest. The claims database
  never receives unvalidated data.
- **E-commerce catalog enrichment**: an LLM generates product attributes
  (color enum, size enum, price range). Schema-guaranteed output + validation
  means bad attributes are blocked before they reach the catalog search index.
- **Financial data extraction**: an analyst tool extracts
  `{company, revenue, currency, fiscal_period}` from earnings releases —
  constrained decoding prevents "revenue" from being a string or the currency
  leaving ISO 4217. Bad extractions are logged as a repair-rate metric.
- **Agent tool calling (fintech)**: the agent's tool arguments
  (`transfer(amount, account)`) are generated as structured output and
  validated *before execution* — a malformed amount never reaches the
  transfer API.
- **LLM evaluation harness**: every judge response (score + reason) is
  schema-validated; a judge that drifts format is flagged in the eval
  pipeline (L20) instead of silently corrupting results.

## Common Mistakes to Avoid

### Mistake 1: Trusting rung 1 (prompt-only) in production
"Output JSON" is a request, not a guarantee. Use JSON mode or constrained
decoding.

### Mistake 2: No validation
Even JSON mode can emit wrong types. Always pydantic-validate at the boundary.

### Mistake 3: Catching errors silently
A swallowed ValidationError hides the model's drift. Log the raw output and
the error — it's your quality signal.

### Mistake 4: Infinite repair loops
Repair is bounded and logged. Cap repairs to bound cost.

### Mistake 5: Parsing text with fragile regex
`json.loads` on the *whole* response; never regex-scrape JSON out of prose.

### Mistake 6: Forgetting additionalProperties
Without `additionalProperties: False`, the model can invent keys. Constrain.

### Mistake 7: Unbounded string fields
A `str` field accepts anything; use enums, patterns, and length bounds where
possible.

## Best Practices

1. Start at the highest reliable rung you can (constrained decoding > JSON mode > prompt)
2. Validate everything at the boundary with pydantic
3. Use strict schemas: required fields, enums, additionalProperties: false
4. Log raw outputs + validation failures (the repair-rate is a quality metric)
5. Cap repair loops and bound cost
6. Never let raw model text reach downstream code
7. Use enums and patterns instead of open strings
8. Test the extraction with known-bad inputs in CI
9. Treat schema changes as versioned contracts
10. Monitor extraction reliability per field (L17, L20)

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| JSON mode | same as normal | — | — |
| Constrained decoding | same or slightly more | — | — |
| Validation | µs | O(1) | pydantic |
| Repair loop | +1 call per repair | — | better schema/prompt first |

Constrained decoding adds negligible latency (the token mask is computed
per-step) but removes entire classes of failure. Cost is usually *lower* —
fewer invalid outputs to repair.

## AI Engineering Relevance

**Where this shows up:** every LLM output that a program consumes — which is
almost all of them. Structured output is the reliability foundation of the
entire GenAI phase.

| Concept here | Used for |
|---|---|
| Rungs 1-3 | escalating guarantees of valid output |
| pydantic validation | the safety net at the boundary |
| Repair loops | self-correcting extraction |
| Logged failures | quality monitoring signals |

**Scale note:** at 100k extractions/day, a 2% format-failure rate is 2,000
broken records daily. Structured output + validation + repair is what turns
that into a logged, measured, near-zero operational event.

## Practice Exercises

### Exercise 1: Parse and Validate (Easy)
Write `safe_parse(raw, schema)` using pydantic; test valid JSON, string-int,
missing-key, and extra-key cases — each raises a clear ValueError.

### Exercise 2: Repair Loop (Medium)
Implement `extract_with_repair` with a mock client that fails once with wrong
types then succeeds; assert it repairs and that the repair count is capped.

### Exercise 3: Enum Constraint (Medium)
Write `classify_verdict(raw, valid)` (section 6) and test case-insensitivity
and out-of-set rejection.

### Exercise 4: Extraction Service (Hard)
Build a full extraction service: schema → constrained prompt → parse →
validate → repair → log metrics (success rate, repair rate). Test that a
malformed model output never escapes as raw text and that the success rate
report is correct.

## Summary

| Concept | Description |
|---|---|
| Rung 1: prompt | the soft baseline |
| Rung 2: JSON mode | format-guaranteed |
| Rung 3: constrained | schema-guaranteed |
| Validation | pydantic at the boundary |
| Repair | bounded self-correction |

LLMs emit text; systems need data. Structured output is the discipline that
bridges them — escalating guarantees from prompt to schema-enforced decoding,
with validation and bounded repair as the permanent safety net. Every reliable
GenAI system is built on this foundation.

## Quick Reference

| Task | Idiom |
|---|---|
| JSON mode | `response_format={"type": "json_object"}` |
| Strict schema | `response_format={"type": "json_schema", ...}` |
| Validate | `pydantic` model + `model_validate` |
| Repair | re-prompt with the model's own error |
| Never | regex-scrape JSON or trust unvalidated output |

## Next Steps

Next: **[04 Prompt Engineering](04-prompt-engineering-lecture.md)** — designing
the prompts that drive all of the above.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://platform.openai.com/docs/guides/structured-outputs,
https://docs.pydantic.dev/latest/
