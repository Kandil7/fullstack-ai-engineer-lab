# Cost Optimization — Glossary 15

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Autoscaling | Cost | Scaling instances to demand, to zero if idle |
| Batch Processing | Cost | Running jobs in groups at lower per-item cost |
| Cache Hit | Cost | A repeat query served without a model call |
| Cost per 1k | Cost | The canonical prediction-cost unit |
| On-Demand | Cost | Reliable, pricier instances |
| Spot Instance | Cost | Cheap, interruptible instances |
| Throughput | Cost | Predictions per second |
| Utilization | Cost | Fraction of billed capacity actually used |

## Detailed Definitions
### Autoscaling
**Definition**: Adding/removing instances with demand; scaling to zero when
idle.
**Related**: Utilization

### Batch Processing
**Definition**: Grouping work (e.g. nightly) to amortize fixed costs.
**Related**: Throughput

### Cache Hit
**Definition**: Serving a repeat query from cache instead of running the model.
**Related**: Cost per 1k

### Cost per 1k
**Definition**: Dollars per 1000 predictions - the unit for comparing models
and architectures.
```python
cost_per_1k = instance_per_hour / (predictions_per_hr / 1000)
```
**Related**: Throughput

### On-Demand
**Definition**: Standard, reliable instances; cannot be interrupted.
**Related**: Spot Instance

### Spot Instance
**Definition**: Discounted (~70%) instances that can be reclaimed; fit for
interruptible training.
**Related**: On-Demand

### Throughput
**Definition**: Predictions per second; drives the denominator of cost per 1k.
**Related**: Cost per 1k

### Utilization
**Definition**: The fraction of paid capacity actually used; low utilization
is wasted money.
**Related**: Autoscaling

## Key Concepts Summary
### The Unit
- Optimize $/1k predictions, not $/hour

### The Levers
- Utilization, batching, caching, spot vs on-demand

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Cost per 1k — ___
2. Utilization — ___
3. Spot — ___
4. Cache hit — ___
5. Autoscaling — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=scale to demand, b=$ per 1000
predictions, c=capacity used, d=interruptible cheap instances, e=repeat query
served from cache.
