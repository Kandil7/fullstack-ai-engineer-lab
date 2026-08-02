# Data Validation — Glossary 10

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Baseline | Validation | Expected distribution statistics for comparison |
| Column Rule | Validation | Type/null/range contract for one column |
| Contract | Validation | The declared requirements for data |
| Distribution Check | Validation | Comparing a distribution to its baseline |
| Fail Fast | Validation | Stopping at the first violation |
| Null Rate | Validation | Fraction of missing values in a column |
| Schema | Validation | The structural definition of the data |
| Tolerance | Validation | Allowed deviation from a baseline |

## Detailed Definitions
### Baseline
**Definition**: Reference statistics (mean, std, null rate) captured from
healthy data.
**Related**: Distribution Check

### Column Rule
**Definition**: A per-column contract: dtype, nullable, min_value, max_value.
```python
ColumnRule("age", dtype=int, min_value=0, max_value=120)
```
**Related**: Contract

### Contract
**Definition**: The full set of rules data must satisfy before use.
**Related**: Column Rule

### Distribution Check
**Definition**: Comparing current data to a baseline to catch shifts schema
checks cannot.
**Related**: Baseline

### Fail Fast
**Definition**: Validating at the boundary and stopping with a clear error,
before expensive downstream work.
**Related**: Contract

### Null Rate
**Definition**: The fraction of None/missing values in a column; a spike is a
source-break warning.
**Related**: Distribution Check

### Schema
**Definition**: The declared structure of the data: columns and their types.
**Related**: Contract

### Tolerance
**Definition**: How far current statistics may deviate from baseline before
alerting.
**Related**: Baseline

## Key Concepts Summary
### Two Layers of Validation
- Schema: types, nulls, ranges
- Distribution: means, null rates, shifts

### The Rule
- Fail the pipeline, not the model

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Contract — ___
2. Baseline — ___
3. Null rate — ___
4. Fail fast — ___
5. Tolerance — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=allowed deviation, b=set of rules,
c=reference statistics, d=fraction missing, e=stop at boundary.
