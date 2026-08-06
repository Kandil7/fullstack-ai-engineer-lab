# FastAPI — 26: Pydantic v2 Deep

Companion exercise: `26-pydantic-v2-deep.py`

---

## Topic Overview

Pydantic v2 is the data-validation layer beneath every FastAPI endpoint. Its
Rust core (`pydantic-core`) makes validation 5–50x faster than v1 for large
schemas, and its validator API has been rebuilt around `field_validator`,
`model_validator`, and `TypeAdapter`. This topic goes past the basics — past
just declaring `BaseModel` subclasses — into the machinery that decides whether
your API's contract is enforced or merely decorative: field constraints,
validation order, computed fields, strict mode, aliases, and configuration.

The mental model: a Pydantic model is a **schema** that (1) coerces and
validates input, (2) holds state, and (3) serializes output. Understanding
validation order — which hook runs when, in which mode — is what separates
schemas that catch bad data at the edge from schemas that silently mangle it.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Replace hand-written validation with `Field` constraints.
2. Use `field_validator` with `mode="before"` and `mode="after"`.
3. Enforce cross-field invariants with `model_validator`.
4. Add derived output values with `computed_field`.
5. Control coercion with strict mode and `model_config`.
6. Validate non-model types with `TypeAdapter`.
7. Rename fields in JSON output with serialization aliases.
8. Predict when validation errors are raised and what 422 looks like.

## Prerequisites

| Need | Where |
|---|---|
| Request bodies | `05-request-body.py` |
| Response models | `06-response-model.py` |
| Error handling | `23-exception-handling.py` |

## 1. Field Constraints — Declarative Validation

`Field(min_length=..., gt=..., ...)` turns constraints into the schema itself —
the same constraints appear in OpenAPI docs, and validation happens before your
handler runs.

```python
class Product(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    price: float = Field(gt=0, le=10_000)
    stock: int = Field(ge=0)
    tags: list[str] = Field(default_factory=list, max_length=10)
```

Output:
```
# Product(name="GPU", price=2500.0, stock=4) — valid
# Product(name="X", price=-1, stock=0) -> ValidationError: name too short
```

`default_factory` matters: never use a mutable default (`tags=[]`); a fresh
list per instance is what you want.

## 2. field_validator — Per-Field Logic

Per-field hooks run before or after type coercion:

```python
class Order(BaseModel):
    email: str
    qty: int = Field(gt=0)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v:
            raise ValueError("email must contain @")
        return v

    @field_validator("qty", mode="before")
    @classmethod
    def coerce_qty(cls, v):
        if isinstance(v, str):
            v = v.strip()
        return v
```

Output:
```
# Order(email="  A@B.com ", qty="3") -> email "a@b.com", qty 3 (int)
```

- `mode="before"`: sees raw input (str "3"), good for normalization/coercion.
- `mode="after"` (default): sees the coerced value (int 3), good for range/business rules.

## 3. model_validator — Cross-Field Invariants

When a rule spans fields, use `model_validator(mode="after")`:

```python
class Booking(BaseModel):
    start: int
    end: int

    @model_validator(mode="after")
    def check_range(self) -> "Booking":
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self
```

Output:
```
# Booking(start=10, end=14) — valid
# Booking(start=14, end=10) -> ValidationError
```

`mode="after"` receives the fully-built model, so you can validate against
already-processed fields. (There is also `mode="before"` over raw dicts, and
`mode="wrap"` for the rare cases that need both.)

## 4. computed_field — Derived Output Values

Values that should appear in serialized output but never be accepted as input:

```python
class Invoice(BaseModel):
    unit_price: float
    qty: int
    tax_rate: float = 0.2

    @computed_field
    @property
    def total(self) -> float:
        return round(self.unit_price * self.qty * (1 + self.tax_rate), 2)
```

Output:
```
# Invoice(unit_price=10.0, qty=3).total -> 36.0
# model_dump() includes "total" without requiring it as input
```

## 5. Strict Mode — No Silent Coercion

By default Pydantic coerces ("42" -> 42, True -> 1). For contracts where that
is dangerous — an ID field that must be an integer, a token that must be a
string — turn it off:

```python
class StrictId(BaseModel):
    model_config = ConfigDict(strict=True)
    user_id: int

# StrictId(user_id="42") -> ValidationError (rejected, not coerced)
```

Output:
```
# ValidationError: Input should be a valid integer, got a string
```

Use strict mode at API boundaries where type confusion is a real risk.

## 6. TypeAdapter — Validating Non-Model Types

Not everything is a model. A list of IDs, a bare string, a dict — wrap with
`TypeAdapter`:

```python
IntList = TypeAdapter(list[int])
IntList.validate_python([1, 2, 3])      # [1, 2, 3]
IntList.validate_python([1, "x"])       # ValidationError
```

Output:
```
# [1, 2, 3]
# ValidationError: Input should be a valid integer, got a string
```

## 7. Serialization Aliases — JSON Names Differ from Python

Legacy clients or external specs often use names that differ from Python
conventions:

```python
class LegacyAPI(BaseModel):
    user_id: int
    user_name: str = Field(serialization_alias="userName")

LegacyAPI(user_id=1, user_name="ada").model_dump(by_alias=True)
# -> {"user_id": 1, "userName": "ada"}
```

Output:
```
# {'user_id': 1, 'userName': 'ada'}
```

## 8. Common Mistakes to Avoid

### Mistake 1: Mutable default values
```python
# WRONG — one list shared by every instance
class Bad(BaseModel):
    tags: list[str] = []
# CORRECT
class Good(BaseModel):
    tags: list[str] = Field(default_factory=list)
```

### Mistake 2: Raising wrong exception types in validators
```python
# WRONG — ValidationError is raised by Pydantic, not by you
def v(cls, x):
    raise RuntimeError("bad")
# CORRECT — raise ValueError/AssertionError inside validators
```

### Mistake 3: Forgetting mode for coercion-style validators
```python
# WRONG — 'after' sees int 3, strip() fails with AttributeError
@field_validator("qty")
def coerce(cls, v): return v.strip()
# CORRECT — mode="before" sees the raw string
```

### Mistake 4: Validating with if/raise inside the handler
```python
# WRONG — business rules checked in the endpoint, bypassing the schema
# CORRECT — encode the rule in the model; the edge rejects bad data
```

### Mistake 5: Ignoring strict mode at security boundaries
```python
# WRONG — user_id="1" coerces silently, masking client bugs
# CORRECT — ConfigDict(strict=True) where type identity matters
```

## 9. Best Practices

1. Encode every constraint in the schema, not in the handler.
2. Use `default_factory` for all mutable defaults.
3. Raise `ValueError` inside validators; never catch `ValidationError` in handlers.
4. Prefer `mode="before"` for input normalization, `mode="after"` for rules.
5. Use `model_validator(mode="after")` for cross-field invariants.
6. Use `computed_field` for derived output; keep inputs explicit.
7. Use strict mode at identity-sensitive boundaries.
8. Use `TypeAdapter` for lists/dicts you don't want as full models.
9. Set `extra="forbid"` to reject unexpected fields where strictness pays.
10. Keep one model per contract; compose with inheritance, don't duplicate.

## 10. Complexity and Cost

| Operation | Cost | Notes |
|---|---|---|
| Field validation (v2) | O(fields) per parse | Rust core: ~5–50x faster than v1 |
| Strict mode | same | No coercion overhead added |
| Validators | O(validators) per parse | User code — keep them light |
| TypeAdapter on lists | O(n) | Linear in list length |
| model_dump serialization | O(fields) | Aliases add tiny constant cost |

The v2 speedup matters most on high-throughput endpoints parsing large payloads
— hundreds of fields x thousands of requests/sec.

## 11. AI Engineering Relevance

**Where this shows up:** every ML/LLM API boundary. Structured outputs from
LLMs (`09-genai/03-structured-output`) are validated with Pydantic schemas;
feature vectors, prediction requests, and eval-suite configs are all models.

| Concept here | Used for |
|---|---|
| Field constraints | Validating LLM JSON outputs against a schema |
| Strict mode | Rejecting malformed structured outputs instead of coercing |
| TypeAdapter | Validating lists of embeddings, token counts, costs |
| Cross-field validators | Checking start<end, model<budget invariants in configs |
| Aliases | Mapping provider-specific field names to your contract |

**Scale note:** at high QPS, validation is no longer free — the v2 Rust core
is why production FastAPI services validate every request without measurable
overhead.

## 12. Summary

| Concept | Description |
|---|---|
| Field constraints | Declarative per-field rules |
| field_validator | Per-field hooks, before/after coercion |
| model_validator | Cross-field invariants |
| computed_field | Derived output, not input |
| Strict mode | Reject coercion at boundaries |
| TypeAdapter | Validate non-model types |
| Aliases | Different JSON names on the wire |

## Quick Reference

| Task | Idiom |
|---|---|
| Constrain a field | `Field(min_length=3, gt=0, max_length=10)` |
| Normalize input | `@field_validator("f", mode="before")` |
| Cross-field rule | `@model_validator(mode="after")` |
| Derived output | `@computed_field @property` |
| Reject coercion | `model_config = ConfigDict(strict=True)` |
| Non-model validation | `TypeAdapter(list[int])` |
| Rename in JSON | `Field(serialization_alias="x")` + `model_dump(by_alias=True)` |

## Next Steps

Next: **[27 — API Versioning](27-api-versioning-lecture.md)** — evolving your contract without breaking clients.

Continues in: **[09-genai — 03 Structured Output](../../09-genai/lectures/03-structured-output-lecture.md)** — Pydantic as the LLM output contract.

Official docs: <https://docs.pydantic.dev/latest/>
