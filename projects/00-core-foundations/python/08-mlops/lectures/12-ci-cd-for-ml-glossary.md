# CI/CD for ML — Glossary 12

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Approval Gate | CI/CD | A human/policy decision to deploy |
| Behavioral Test | Testing | A test of a model's known behavior |
| CI Gate | CI/CD | The stage run that must all pass |
| Data Test | Testing | A test on input data quality |
| Golden Case | Testing | A locked input->output pair |
| Promotion | CI/CD | Moving a validated model to production |
| Regression | Testing | A behavior that used to work and now fails |

## Detailed Definitions
### Approval Gate
**Definition**: A separate step where a reviewer (or policy) approves
deployment - distinct from green CI.
**Related**: Promotion

### Behavioral Test
**Definition**: A test asserting the model's known behavior, e.g. a rule model
rejects negative income.
```python
assert rule_model_predict(16, 1e9) == "REJECT"
```
**Related**: Golden Case

### CI Gate
**Definition**: The ordered run of all test stages; any failure fails the
build.
**Related**: Behavioral Test

### Data Test
**Definition**: A test that input data satisfies its contract before training.
**Related**: CI Gate

### Golden Case
**Definition**: A (input, expected) pair locked into the test suite to catch
regressions.
**Related**: Regression

### Promotion
**Definition**: The act of shipping a validated model to production, gated and
approved.
**Related**: Approval Gate

### Regression
**Definition**: A behavior that previously worked and silently stopped working.
**Related**: Golden Case

## Key Concepts Summary
### The Test Trio
- Code tests (runs)
- Data tests (sane input)
- Behavioral tests (model contract)

### Gate vs Approval
- CI gate: safe
- Approval: wanted
- Both required for promotion

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Behavioral test — ___
2. Golden case — ___
3. CI gate — ___
4. Approval gate — ___
5. Regression — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=behavior that broke, b=model
behavior test, c=locked input->output pair, d=all-stages-run, e=human deploy
decision.
