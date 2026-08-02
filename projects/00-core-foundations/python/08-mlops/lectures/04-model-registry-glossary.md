# Model Registry — Glossary 04

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Archived | Registry | Stage for replaced or retired models |
| Gate | Registry | A threshold a promotion must clear |
| Promotion | Registry | Moving a model to a later stage |
| Production | Registry | The stage where a model serves live traffic |
| Registry | MLOps | Version control + lifecycle for models |
| Rollback | Registry | Re-promoting an archived model after regression |
| Signature | Registry | The declared input/output schema of a model |
| Stage | Registry | Lifecycle position of a model version |
| Staging | Registry | Pre-production validation stage |
| Version | Registry | Monotonic identifier for a model incarnation |

## Detailed Definitions
### Archived
**Definition**: The final stage; a model replaced in Production or retired.
**Related**: Stage, Rollback

### Gate
**Definition**: A declared threshold - accuracy >= 0.90, latency <= 100ms -
that promotion to a stage must satisfy.
**Example**:
```python
GATES = {"Production": {"accuracy": (0.90, "min")}}
```
**Related**: Promotion

### Promotion
**Definition**: The act of moving a model from one stage to the next, with
gates checked and an owner recorded.
**Related**: Stage, Gate

### Production
**Definition**: The stage where the model serves real traffic; exactly one
model per name can occupy it.
**Related**: Stage

### Registry
**Definition**: The system managing model versions, stages, signatures, and
promotion history.
**Related**: Version, Stage

### Rollback
**Definition**: Forced re-promotion of an archived model when the current one
regresses; bypasses gates but is logged.
**Related**: Archived, Promotion

### Signature
**Definition**: The declared input/output schema, enabling contract checks at
serving time.
**Related**: Version

### Stage
**Definition**: Lifecycle position: None, Staging, Production, Archived.
**Related**: Promotion

### Staging
**Definition**: The validation stage between registration and Production.
**Related**: Stage

### Version
**Definition**: An auto-incremented integer identifying one incarnation of a
model name.
**Related**: Registry

## Key Concepts Summary
### Lifecycle
- None -> Staging -> Production -> Archived
- One model per name per stage

### Promotion Rules
- Gates must pass for normal promotion
- Rollbacks are forced but logged
- Every transition records who and why

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Gate — ___
2. Rollback — ___
3. Production — ___
4. Signature — ___
5. Version — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=monotonic identifier, b=promotion
threshold, c=re-promoting an archived model, d=live-traffic stage, e=input/
output schema.
