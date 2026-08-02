# Memory and Context — Glossary 16

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Context Budget | Memory | Window minus reserved output tokens |
| Long-Term Memory | Memory | Retrievable persistent conversation history |
| Rolling Summary | Memory | A compressed, updated digest of old turns |
| Short-Term Memory | Memory | The recent verbatim message list |
| Stateless | Model | No state persists between calls |
| Token Budget | Cost | The token allowance for a request |
| Truncation | Failure | Dropping content because the window overflowed |

## Detailed Definitions
### Context Budget
**Definition**: The tokens available after reserving output; the design
constraint for memory policies.
**Related**: Token Budget

### Long-Term Memory
**Definition**: Past exchanges stored in an index and retrieved on demand.
**Related**: Short-Term Memory

### Rolling Summary
**Definition**: A digest of aged-out turns, updated as the conversation grows.
**Related**: Long-Term Memory

### Short-Term Memory
**Definition**: The recent turns included verbatim in the request.
**Related**: Rolling Summary

### Stateless
**Definition**: Each API call is independent; the model retains nothing.
**Related**: Long-Term Memory

### Token Budget
**Definition**: The window size minus output reservation; what memory may use.
**Related**: Context Budget

### Truncation
**Definition**: Losing content when the total exceeds the window.
**Related**: Token Budget

## Key Concepts Summary
### The Hierarchy
- Recent verbatim, old summarized, facts retrieved

### The Rule
- Budget = window − output; never overflow

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Stateless — ___
2. Rolling summary — ___
3. Long-term memory — ___
4. Budget — ___
5. Short-term memory — ___

**Answers:** 1-c, 2-e, 3-a, 4-b, 5-d where a=retrieved history, b=window minus
output, c=no persistence, d=recent verbatim turns, e=compressed digest.
