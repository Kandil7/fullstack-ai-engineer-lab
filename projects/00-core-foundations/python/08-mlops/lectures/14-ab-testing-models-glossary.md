# A/B Testing Models — Glossary 14

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| A/B Test | Experiment | Controlled split of traffic between models |
| Blast Radius | Deployment | The scope of impact if something fails |
| Canary | Deployment | A small % of traffic to a new model |
| Guardrail | Experiment | A metric that can veto a rollout |
| Pre-Registration | Experiment | Declaring rules before running |
| Shadow | Deployment | Running in parallel, logging only |
| Significance | Statistics | Confidence a difference is not noise |
| Traffic Split | Experiment | Routing % of users to each arm |
| z-test | Statistics | Test of difference in proportions |

## Detailed Definitions
### A/B Test
**Definition**: Splitting traffic between control and treatment to measure a
difference with statistics.
**Related**: Traffic Split

### Blast Radius
**Definition**: The extent of damage if a change fails (shadow = none, full
rollout = everything).
**Related**: Canary

### Canary
**Definition**: Routing a small % of traffic to the new model before wider
rollout.
**Related**: Blast Radius

### Guardrail
**Definition**: A metric (latency, error rate) that must hold; can veto a
target-metric win.
**Related**: Pre-Registration

### Pre-Registration
**Definition**: Declaring sample size, significance, and stopping rules before
the experiment starts.
**Related**: Significance

### Shadow
**Definition**: Running the new model on live traffic without affecting users;
logging only.
**Related**: Blast Radius

### Significance
**Definition**: Statistical confidence that an observed difference is real.
**Related**: z-test

### Traffic Split
**Definition**: The % of users routed to each arm, bucketed deterministically.
**Related**: A/B Test

### z-test
**Definition**: A test on proportions; |z| > 1.96 ~ p < 0.05.
**Related**: Significance

## Key Concepts Summary
### The Ladder
- Shadow (no impact) -> Canary (small %) -> A/B (50/50) -> Rollout (100%)

### The Rules
- Pre-register before running
- Guardrails can veto
- Deterministic bucketing per user

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Canary — ___
2. Shadow — ___
3. Guardrail — ___
4. Pre-registration — ___
5. z-test — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=proportion test, b=small % of
traffic, c=parallel logging only, d=veto metric, e=rules set in advance.
