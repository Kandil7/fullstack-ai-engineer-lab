# LLM Observability — Glossary 17

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Error Rate | Signal | Fraction of calls that failed |
| Latency | Signal | Time from request to response |
| p95 | Signal | The latency below which 95% of calls fall |
| Redaction | Safety | Removing secrets/PII before logging |
| Refusal Rate | Signal | Fraction of outputs that decline to answer |
| Regression Signal | Signal | A metric that flags quality drops |
| Request ID | Tracing | A unique identifier per call |
| Trace | Tracing | The full record of one request's life |

## Detailed Definitions
### Error Rate
**Definition**: Failed calls / total; integration health.
**Related**: Trace

### Latency
**Definition**: Time-to-response for a call; UX metric.
**Related**: p95

### p95
**Definition**: The latency that 95% of calls stay under; catches tail risk.
**Related**: Latency

### Redaction
**Definition**: Masking secrets and personal data before storing logs.
**Related**: Trace

### Refusal Rate
**Definition**: Outputs declining to answer / total; flags over-guardrailing.
**Related**: Regression Signal

### Regression Signal
**Definition**: A derived metric (refusals, length, errors) that flags drops.
**Related**: Refusal Rate

### Request ID
**Definition**: A unique ID linking a complaint to its trace.
**Related**: Trace

### Trace
**Definition**: The structured record: prompt, model, latency, tokens, output.
**Related**: Request ID

## Key Concepts Summary
### The Pillars
- Trace everything, aggregate the signals

### The Signals
- Latency, tokens, refusals, errors, hit rate

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Trace — ___
2. p95 — ___
3. Redaction — ___
4. Refusal rate — ___
5. Request ID — ___

**Answers:** 1-d, 2-b, 3-e, 4-c, 5-a where a=unique call ID, b=tail latency,
c=decline share, d=full call record, e=secrets masking.
