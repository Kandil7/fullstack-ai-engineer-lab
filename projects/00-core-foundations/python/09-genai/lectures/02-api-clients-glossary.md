# API Clients — Glossary 02

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Assistant Message | API | Prior model output in the conversation |
| Backoff | Reliability | Increasing delay between retries |
| Fake Client | Testing | Deterministic stand-in returning scripted responses |
| Jitter | Reliability | Randomness added to backoff to desync clients |
| Rate Limit | API | Server cap on requests; 429 response |
| Retry | Reliability | Re-attempting a failed request |
| System Message | API | Instructions setting model behavior |
| Timeout | Reliability | Max time to wait for a response |

## Detailed Definitions
### Assistant Message
**Definition**: A message with the assistant role; the model's prior output.
**Related**: System Message

### Backoff
**Definition**: Waiting longer between successive retries, usually exponential.
**Related**: Jitter

### Fake Client
**Definition**: A client that returns scripted responses, enabling offline dev
and deterministic tests.
**Related**: Timeout

### Jitter
**Definition**: Random variation in retry delay to prevent synchronized retry
storms.
**Related**: Backoff

### Rate Limit
**Definition**: A server-imposed cap on requests, signaled with HTTP 429.
**Related**: Retry

### Retry
**Definition**: Re-issuing a failed request, on transient errors only.
**Related**: Backoff

### System Message
**Definition**: Top-of-conversation instructions that set behavior and tone.
**Related**: Assistant Message

### Timeout
**Definition**: The maximum wait time for a connect or read before giving up.
**Related**: Retry

## Key Concepts Summary
### The Rules
- Retry 429/5xx/timeouts; never 4xx
- Backoff needs jitter
- Fake clients make dev deterministic

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Backoff — ___
2. Jitter — ___
3. 429 — ___
4. System message — ___
5. Fake client — ___

**Answers:** 1-c, 2-e, 3-a, 4-b, 5-d where a=rate limited, b=behavior
instructions, c=increasing delay, d=scripted stand-in, e=desync randomness.
