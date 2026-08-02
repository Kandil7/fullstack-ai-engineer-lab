# Monitoring and Drift — Glossary 11

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Concept Drift | Monitoring | The relationship P(Y\|X) changed |
| Data Drift | Monitoring | The input distribution P(X) changed |
| Delayed Label | Monitoring | Ground truth that arrives late |
| KS Statistic | Statistics | Max gap between cumulative distributions |
| Proxy Metric | Monitoring | An observable used before labels arrive |
| PSI | Statistics | Bucketed divergence between distributions |
| Reference Baseline | Monitoring | The distribution a model was validated on |
| Shift | Monitoring | A measured change in a distribution |

## Detailed Definitions
### Concept Drift
**Definition**: The mapping from inputs to outputs changed - the task itself
moved.
**Example response**: re-examine features and labels.
**Related**: Data Drift

### Data Drift
**Definition**: The input feature distribution changed while the relationship
stayed the same.
**Example response**: retrain on recent data.
**Related**: Concept Drift

### Delayed Label
**Definition**: Ground truth that arrives days/weeks after the prediction
(e.g. fraud confirmation).
**Related**: Proxy Metric

### KS Statistic
**Definition**: The maximum vertical gap between two empirical CDFs; larger =
more shifted.
**Related**: PSI

### Proxy Metric
**Definition**: An immediately observable signal (null rate, volume, prediction
distribution) used until true labels arrive.
**Related**: Delayed Label

### PSI
**Definition**: Population Stability Index: buckets both distributions and sums
`(r-c)*log(r/c)`. <0.1 stable, >0.25 alert.
**Related**: KS Statistic

### Reference Baseline
**Definition**: The distribution the model was trained/validated on; drift is
measured against it.
**Related**: Data Drift

### Shift
**Definition**: A statistically measured change in a distribution.
**Related**: PSI

## Key Concepts Summary
### Drift Types
- Data drift: P(X) changed -> retrain
- Concept drift: P(Y|X) changed -> re-examine the task

### Alert Rules
- PSI < 0.1 stable | 0.1-0.25 investigate | > 0.25 alert

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Data drift — ___
2. Concept drift — ___
3. PSI — ___
4. Proxy metric — ___
5. Delayed label — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=late ground truth, b=P(X) changed,
c=P(Y|X) changed, d=bucketed divergence, e=observable-before-labels.
