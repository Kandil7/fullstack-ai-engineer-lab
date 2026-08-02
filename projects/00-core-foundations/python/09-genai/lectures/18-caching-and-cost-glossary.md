# Caching and Cost — Glossary 18

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Budget | Cost | A cap on tokens/calls per user or time |
| Degradation | Cost | Defined behavior when a budget is hit |
| Exact Cache | Caching | Serving identical requests from cache |
| Hit | Caching | A request served without a model call |
| Hit Rate | Caching | The share of requests served from cache |
| Input Tokens | Cost | Prompt/context tokens billed per call |
| Output Tokens | Cost | Generated answer tokens billed per call |
| Semantic Cache | Caching | Serving similar-meaning requests from cache |
| Threshold | Caching | The similarity cutoff for a semantic hit |

## Detailed Definitions
### Budget
**Definition**: A cap on tokens or calls protecting the bill.
**Related**: Degradation

### Degradation
**Definition**: The designed fallback (shorter context, refusal) at the cap.
**Related**: Budget

### Exact Cache
**Definition**: Keyed on the exact request; returns on identical text.
**Related**: Semantic Cache

### Hit
**Definition**: A request answered from cache at ~zero model cost.
**Related**: Hit Rate

### Hit Rate
**Definition**: `hits / total`; the health metric of a cache.
**Related**: Hit

### Input Tokens
**Definition**: The tokens of prompt, context, and history per call.
**Related**: Output Tokens

### Output Tokens
**Definition**: The tokens the model generates per call.
**Related**: Input Tokens

### Semantic Cache
**Definition**: Keyed on embedding similarity; returns on paraphrased repeats.
**Related**: Threshold

### Threshold
**Definition**: The similarity score above which a cache entry counts as a hit.
**Related**: Semantic Cache

## Key Concepts Summary
### The Levers
- Exact cache, semantic cache, budgets

### The Math
- Cost = misses × call cost; track the hit rate

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Hit rate — ___
2. Semantic cache — ___
3. Budget — ___
4. Input tokens — ___
5. Degradation — ___

**Answers:** 1-c, 2-e, 3-b, 4-a, 5-d where a=prompt tokens, b=usage cap, c=
cached share, d=behavior at cap, e=meaning-based caching.
