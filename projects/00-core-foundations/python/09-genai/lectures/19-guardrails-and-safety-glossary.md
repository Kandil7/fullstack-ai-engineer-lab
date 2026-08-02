# Guardrails and Safety — Glossary 19

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Allow | Policy | Pass a prompt/output through |
| Block | Policy | Reject a prompt/output entirely |
| False Positive | Testing | A legitimate item flagged by a guardrail |
| Injection | Threat | User data overriding the system prompt |
| Input Guardrail | Defense | Checks applied before the model |
| Output Guardrail | Defense | Checks applied before the user |
| Policy Code | Policy | A structured decision: ALLOW/REDACT/BLOCK + reason |
| Redact | Policy | Mask the offending part and pass the rest |
| Secret Leakage | Threat | Credentials or keys exposed in output |

## Detailed Definitions
### Allow
**Definition**: The policy decision to pass content unchanged.
**Related**: Block

### Block
**Definition**: The policy decision to reject content entirely.
**Related**: Allow

### False Positive
**Definition**: A guardrail flagging benign content; a tuning cost.
**Related**: Input Guardrail

### Injection
**Definition**: An attack where user text contains instructions that override
the system prompt.
**Related**: Input Guardrail

### Input Guardrail
**Definition**: Scans on prompts: secrets, blocked topics, injection patterns.
**Related**: Output Guardrail

### Output Guardrail
**Definition**: Scans on outputs: PII, secrets, out-of-scope content.
**Related**: Input Guardrail

### Policy Code
**Definition**: A structured decision (ALLOW/REDACT/BLOCK) with a reason, for
auditability.
**Related**: Redact

### Redact
**Definition**: Masking the offending portion while passing the rest.
**Related**: Policy Code

### Secret Leakage
**Definition**: The model echoing credentials it saw in context.
**Related**: Output Guardrail

## Key Concepts Summary
### The Layers
- Input checks → model → output checks → policy

### The Rule
- Test guardrails adversarially; trust nothing untested

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Injection — ___
2. Redact — ___
3. Block — ___
4. False positive — ___
5. Leakage — ___

**Answers:** 1-d, 2-b, 3-e, 4-c, 5-a where a=credential echo, b=mask offender,
c=benign flagged, d=instruction override, e=reject entirely.
