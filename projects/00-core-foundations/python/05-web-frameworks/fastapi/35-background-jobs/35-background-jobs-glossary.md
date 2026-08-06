# Background Jobs — Glossary 35

Companion lecture: `35-background-jobs-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| 202 Accepted | HTTP | Response indicating the work was accepted, not finished |
| BackgroundTasks | Mechanism | FastAPI's in-process fire-and-forget tasks |
| Broker | Durability | The store (Redis/RabbitMQ) persisting queued jobs |
| Dead-letter queue | Reliability | Where permanent failures are parked for inspection |
| Durable queue | Reliability | Broker-persisted jobs surviving restarts |
| Idempotent task | Reliability | A task safe to run more than once |
| Job ID | Observability | The identifier clients use to track a job |
| Poison message | Failure | A job that can never succeed |
| Progress reporting | Observability | Job state (queued/running/done) exposed to clients |
| Queue depth | Monitoring | The number of pending jobs — the leading indicator |
| Retry | Reliability | Re-executing a failed job, usually with backoff |
| Backoff | Reliability | Increasing wait between retries, with jitter |
| Worker | Scale | A separate process executing queue jobs |
| Transient failure | Failure | A temporary error worth retrying |
| Permanent failure | Failure | An error retrying cannot fix |
| Celery | Tooling | The full-featured Python distributed task queue |
| RQ/ARQ | Tooling | Simpler Redis-backed queues |
| Beat | Tooling | Celery's scheduler for periodic jobs |

## Detailed Definitions

### 202 Accepted
**Definition**: The HTTP status returned when work is accepted but not yet
done; clients pair it with a job_id to track progress.
**Related**: Job ID

### BackgroundTasks
**Definition**: FastAPI's mechanism for running functions after the response —
in-process, non-durable, no retries.
**Example**:
```python
background.add_task(send_email, "a@b.com")
```
**Related**: Durable queue

### Broker
**Definition**: The persistent store (Redis, RabbitMQ) that holds queued jobs
so they survive worker restarts — the source of durability.
**Related**: Durable queue

### Dead-letter queue
**Definition**: The queue receiving jobs that exhausted their retries —
parked for inspection instead of blocking the queue or vanishing.
**Related**: Poison message

### Durable queue
**Definition**: A job system where messages persist in a broker and are
processed by workers with retries — for work you cannot afford to lose.
**Related**: Broker, BackgroundTasks

### Idempotent task
**Definition**: A task whose repeated execution produces the same result —
what makes retries safe.
**Related**: Retry

### Job ID
**Definition**: The identifier returned on submission so clients can poll
status — the contract of the 202 pattern.
**Related**: 202 Accepted

### Poison message
**Definition**: A job that can never succeed (bad payload, permanent bug);
handled by max_retries then the DLQ.
**Related**: Dead-letter queue

### Progress reporting
**Definition**: Exposing job state (queued/running/done, maybe percentage)
via a status endpoint or SSE.
**Related**: Job ID

### Queue depth
**Definition**: The number of pending jobs — the leading indicator of
ingestion problems; monitor and alert on it.
**Related**: Monitoring

### Retry
**Definition**: Re-executing a failed job, bounded by max_retries, for
transient failures.
**Related**: Backoff

### Backoff
**Definition**: The increasing wait between retries (exponential + jitter)
that prevents retry storms.
**Related**: Retry

### Worker
**Definition**: A separate process that consumes queue jobs — independently
scalable and isolated from the API.
**Related**: Durable queue

### Transient failure
**Definition**: A temporary error (network blip, lock) worth retrying.
**Related**: Permanent failure

### Permanent failure
**Definition**: An error retrying cannot fix; the job is dead-lettered.
**Related**: Poison message

### Celery
**Definition**: The full-featured Python distributed task queue — brokers,
beat scheduling, rich retries, and a large ecosystem.
**Related**: Durable queue

### RQ/ARQ
**Definition**: Simpler Redis-backed queues (RQ synchronous, ARQ async) —
durable with far less machinery than Celery.
**Related**: Durable queue

### Beat
**Definition**: Celery's scheduler process for periodic/cron jobs.
**Related**: Celery

## Key Concepts Summary

### The decision rule
- BackgroundTasks: disposable work (emails, thumbnails) — in-memory, no retry.
- Durable queue: anything you cannot lose on restart.
- Test: "can I afford to lose this job?"

### The durable contract
- Broker persistence -> survives restarts.
- Retry transient failures with backoff; DLQ permanent ones.
- 202 + job_id for progress; workers for scale.

### The discipline
- Idempotent tasks make retries safe.
- Monitor queue depth; alert on DLQ growth.
- Timeout every task; test failure paths.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. FastAPI's in-process fire-and-forget tasks — ___
2. Broker-persisted jobs surviving restarts — ___
3. Where permanent failures are parked — ___
4. A job that can never succeed — ___
5. The status returned when work is accepted — ___
6. A separate process executing queue jobs — ___
7. A temporary error worth retrying — ___
8. The number of pending jobs — ___

**Answers:** 1-BackgroundTasks, 2-durable queue, 3-dead-letter queue,
4-poison message, 5-202 Accepted, 6-worker, 7-transient failure, 8-queue depth
