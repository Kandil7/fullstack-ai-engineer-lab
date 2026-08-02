# Feature Stores — Glossary 13

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| As-of Join | Features | Joining features valid at an event's timestamp |
| Feature | ML | A measurable input property used by a model |
| Feature Store | MLOps | Shared feature definitions + storage |
| Lookahead | Features | Using future data in training (leakage) |
| Offline Store | Features | Historical batch store for training |
| Online Store | Features | Current-value low-latency store for serving |
| Point-in-Time | Features | Correctness rule: no future values |
| Skew | MLOps | Training/serving feature divergence |

## Detailed Definitions
### As-of Join
**Definition**: Joining each event with feature values valid at its timestamp.
```python
features.as_of("u1", "spend_7d", 150.0)
```
**Related**: Point-in-Time

### Feature
**Definition**: A measurable property (spend_7d, age, country) fed to a model.
**Related**: Feature Store

### Feature Store
**Definition**: A system holding feature definitions and values, shared by
training and serving.
**Related**: Offline Store, Online Store

### Lookahead
**Definition**: Using a feature value computed after the label time - a form
of leakage that inflates offline metrics.
**Related**: Point-in-Time

### Offline Store
**Definition**: The historical, batch-accessible feature store for training.
**Related**: Feature Store

### Online Store
**Definition**: The low-latency, current-value store for serving.
**Related**: Feature Store

### Point-in-Time
**Definition**: The rule that feature values must be as-of the event time -
never future values.
**Related**: As-of Join

### Skew
**Definition**: Training and serving computing a feature differently, making
the deployed model see different inputs.
**Related**: Feature Store

## Key Concepts Summary
### Two Stores, One Definition
- Offline for training, online for serving
- Both read the same feature definitions

### The Cardinal Rule
- Join as-of event time - never look ahead

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Skew — ___
2. Lookahead — ___
3. As-of join — ___
4. Online store — ___
5. Offline store — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=training store, b=train/serve
divergence, c=future data in training, d=join at event time, e=serving store.
