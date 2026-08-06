# Pydantic v2 Deep — Glossary 26

Companion lecture: `26-pydantic-v2-deep-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Coercion | Validation | Automatic type conversion (str "1" -> int 1) |
| computed_field | Model | Derived property present in output but not accepted as input |
| ConfigDict | Model | Model-level configuration (strict, extra, etc.) |
| default_factory | Model | Callable producing a fresh mutable default per instance |
| extra="forbid" | Model | Reject unexpected fields instead of ignoring them |
| Field | Validation | Declarative per-field constraints and metadata |
| field_validator | Validation | Per-field hook running before or after coercion |
| model_config | Model | The ConfigDict attached to a model class |
| model_dump | Serialization | Convert a model to a dict (optionally by_alias) |
| model_validator | Validation | Whole-model hook for cross-field invariants |
| pydantic-core | Engine | The Rust validation core of v2 |
| Serialization alias | Serialization | The JSON field name used on output |
| Strict mode | Validation | Reject coercion: types must match exactly |
| TypeAdapter | Validation | Validate non-model types like list[int] |
| ValidationError | Validation | Raised when input violates the schema |
| Validator | Validation | A function enforcing rules on field/model values |
| mode="before" | Validation | Validator runs on raw input before type coercion |
| mode="after" | Validation | Validator runs on the coerced value |

## Detailed Definitions

### Coercion
**Definition**: Pydantic's default behavior of converting input to the declared
type — "42" becomes 42, True becomes 1. Disabled per model with strict mode.
**Example**:
```python
class Item(BaseModel):
    qty: int
Item(qty="3")   # qty == 3 (int)
```
**Related**: Strict mode

### computed_field
**Definition**: A property decorated `@computed_field` that appears in
serialization output but is never required or accepted as input.
**Example**:
```python
@computed_field
@property
def total(self) -> float:
    return self.price * self.qty
```
**Related**: model_dump

### ConfigDict
**Definition**: The typed dict used to configure a model class — strict mode,
extra-field handling, and more.
**Example**:
```python
model_config = ConfigDict(strict=True, extra="forbid")
```
**Related**: model_config, Strict mode

### default_factory
**Definition**: The callable given to `Field(default_factory=...)` that creates
a fresh mutable default (list, dict) per instance — avoids the shared-mutable
bug.
**Example**:
```python
tags: list[str] = Field(default_factory=list)
```
**Related**: Field

### extra="forbid"
**Definition**: A config option that rejects unknown input fields with a
ValidationError instead of silently ignoring them.
**Related**: ConfigDict

### Field
**Definition**: The function declaring per-field constraints, defaults, and
metadata (`min_length`, `gt`, `description`, ...).
**Example**:
```python
price: float = Field(gt=0, le=10_000)
```
**Related**: field_validator

### field_validator
**Definition**: A per-field hook: `@field_validator("field")` with `mode`
"before" (raw input) or "after" (coerced value).
**Example**:
```python
@field_validator("email")
@classmethod
def normalize(cls, v: str) -> str:
    return v.strip().lower()
```
**Related**: model_validator

### model_config
**Definition**: The class attribute assigning a `ConfigDict` to a model.
**Related**: ConfigDict

### model_dump
**Definition**: Serializes a model instance to a dict; `by_alias=True` uses
serialization aliases as keys.
**Example**:
```python
inv.model_dump(by_alias=True)
```
**Related**: Serialization alias

### model_validator
**Definition**: A whole-model hook for rules spanning multiple fields;
`mode="after"` runs on the fully built model.
**Example**:
```python
@model_validator(mode="after")
def check_range(self):
    if self.end <= self.start:
        raise ValueError("end must be after start")
    return self
```
**Related**: field_validator

### pydantic-core
**Definition**: The Rust implementation of validation in v2, making it 5–50x
faster than the pure-Python v1.
**Related**: Coercion

### Serialization alias
**Definition**: The JSON key used for a field on output, set with
`Field(serialization_alias=...)`; activated by `model_dump(by_alias=True)`.
**Related**: model_dump

### Strict mode
**Definition**: Model config rejecting coercion — input types must match the
declared types exactly.
**Example**:
```python
model_config = ConfigDict(strict=True)
# StrictId(user_id="42") -> ValidationError
```
**Related**: Coercion

### TypeAdapter
**Definition**: Validates non-model types (lists, dicts, primitives) without
wrapping them in a model.
**Example**:
```python
IntList = TypeAdapter(list[int])
IntList.validate_python([1, 2, 3])
```
**Related**: ValidationError

### ValidationError
**Definition**: The exception raised when input violates the schema; FastAPI
turns it into a 422 response with a `detail` list.
**Related**: Validator

### Validator
**Definition**: A function enforcing rules on a field or the whole model;
raises ValueError/AssertionError to signal failure.
**Related**: field_validator, model_validator

### mode="before"
**Definition**: Validator mode running on the raw input before type coercion —
right place for normalization and string cleanup.
**Related**: mode="after"

### mode="after"
**Definition**: Validator mode running on the coerced value — right place for
business rules on final values.
**Related**: mode="before"

## Key Concepts Summary

### Validation order
- Input -> field validators (mode="before") -> coercion -> field validators
  (mode="after") -> model validators (mode="after").
- Raise ValueError inside validators; Pydantic converts it to ValidationError.

### Config control
- strict=True rejects coercion; extra="forbid" rejects unknown fields.
- default_factory for mutable defaults.
- computed_field for derived output.

### Edge types
- TypeAdapter for list[int] and similar.
- Serialization aliases + by_alias for wire-format naming.
- The Rust core makes all of it cheap at scale.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Rust validation core of v2 — ___
2. Hook running on raw input before coercion — ___
3. Derived property in output, not input — ___
4. Rejecting coercion entirely — ___
5. Callable producing a fresh mutable default — ___
6. Cross-field rule hook — ___
7. JSON name used on output — ___
8. Validation of list[int] without a model — ___

**Answers:** 1-pydantic-core, 2-mode="before", 3-computed_field, 4-strict mode,
5-default_factory, 6-model_validator, 7-serialization alias, 8-TypeAdapter
