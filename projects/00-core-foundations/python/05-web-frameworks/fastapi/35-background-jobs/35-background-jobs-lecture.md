# FastAPI — 35: Background Jobs

Companion exercise: `35-background-jobs.py`

---

## Topic Overview

Some work should not make the client wait: emails, thumbnails, ingestion,
model inference, report generation. FastAPI's `BackgroundTasks` handles the
simple case — fire-and-forget after the response. But it has hard limits: the
work lives in process memory, so a crash or restart loses every pending task,
and there are no retries. When the work matters, you need a **durable queue**
(Celery, RQ, ARQ on Redis) with broker persistence, retries, and a dead-letter
queue.

This topic draws the line: BackgroundTasks for work you can afford to lose;
a durable queue for anything you cannot. And it builds a minimal durable-queue
with retry + DLQ semantics to make the contract concrete.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `BackgroundTasks` for fire-and-forget after a response.
2. State the limits: in-memory, lost on restart, no retries.
3. Explain why durable work needs a broker-backed queue.
4. Implement retry-with-backoff and dead-letter semantics.
5. Decide what belongs in BackgroundTasks vs a durable queue.
6. Design progress reporting for long jobs.
7. Recognize poison messages and how DLQs handle them.
8. Separate workers for scaling and isolation.

## Prerequisites

| Need | Where |
|---|---|
| FastAPI basics | `01-introduction.py` |
| Async concepts | `32-async-endpoints-deep.py` |
| Redis | `04-databases/redis/01-introduction.py` |

## 1. BackgroundTasks — Fire and Forget

```python
from fastapi import BackgroundTasks

def send_welcome_email(email: str): ...

@app.post("/signup", status_code=202)
def signup(email: str, background: BackgroundTasks):
    background.add_task(send_welcome_email, email)
    return {"status": "accepted", "email": email}
```

Output:
```
# 202 returned immediately; the email job runs after the response is sent
```

The response goes out first; the task executes after, in the same process.
Perfect for the case where the client should not wait and the work is
disposable.

## 2. The Hard Limits

```python
def background_tasks_limits():
    return [
        "In-memory only: a crash/restart loses every pending task",
        "No retries: if the task raises, it is gone",
        "No dedup, no priority, no visibility",
    ]
```

Output:
```
# In-memory only: a crash/restart loses every pending task
# No retries: if the task raises, it is gone
```

Three consequences: **loss** (restart kills pending work), **no retry** (a
transient failure silently drops the job), and **no observability** (nothing
to query for job state). These are acceptable only for work you can afford to
lose.

## 3. Durable Queues — The Broker Contract

Durable queues persist the message in a broker (Redis, RabbitMQ) so the job
survives restarts. The minimal contract, which the exercise implements:

```python
def enqueue(kind, payload) -> int:     # persists the job
def drain(max_retries) -> list:        # processes with retries
    # transient errors -> retry
    # permanent failures -> dead-letter queue
```

Output:
```
# enqueue flaky -> drain: retry, retry, done (transient failures recovered)
# enqueue poison -> drain: dead-lettered after max_retries
```

Real systems: Celery (full-featured), RQ (simple, Redis), ARQ (async, Redis).
They add durability, retries, priorities, scheduled jobs, and worker
processes.

## 4. Retries and the Dead-Letter Queue

- **Transient failure** (network blip, temporary lock): retry with backoff.
- **Permanent failure** (bad payload, bug): retrying is pointless — park it in
  the **DLQ** for inspection.
- Retry count and backoff policy belong to the job, not the worker's mood.

```python
if attempt >= max_retries:
    job["error"] = str(e)
    self._dlq.append(job)          # human/ops inspects later
else:
    self._queue.append(job)        # retry
```

Output:
```
# poison job -> {"status": "dead"} after max_retries; parked in the DLQ
```

The DLQ is the guarantee that a bad message neither blocks the queue forever
nor silently disappears.

## 5. Progress Reporting

Long jobs need status endpoints:

```python
@app.get("/jobs/{job_id}")
def job_status(job_id: int):
    return {"job_id": job_id, "status": store[job_id]}   # queued/running/done
```

Output:
```
# client polls -> queued -> running (42%) -> done
```

The store can be the broker, Redis, or the DB. Polling (or SSE from
`36-streaming-and-sse`) gives users and operators visibility.

## 6. When to Use Which

| Work | Tool |
|---|---|
| Welcome email, thumbnail, log flush | BackgroundTasks |
| Billing, ingestion, model inference, anything loss-sensitive | Durable queue |
| Long batch processing | Durable queue + separate workers |
| Scheduled/periodic | Celery beat / cron + queue |

The test: *can you afford to lose this job on a restart?* If no, it does not
belong in BackgroundTasks.

## 7. Common Mistakes to Avoid

### Mistake 1: Critical work in BackgroundTasks
```python
# WRONG — billing job in BackgroundTasks: restart loses the charge
# CORRECT — durable queue for anything you cannot lose
```

### Mistake 2: No retry policy
```python
# WRONG — one attempt, silent drop on transient failure
# CORRECT — retries with backoff; DLQ for permanent failures
```

### Mistake 3: Infinite retries on poison messages
```python
# WRONG — a bad payload retried forever blocks the queue
# CORRECT — max_retries then dead-letter
```

### Mistake 4: Heavy work inline in the request
```python
# WRONG — 30s report generation in the handler
# CORRECT — enqueue + status endpoint (202 pattern)
```

### Mistake 5: No observability
```python
# WRONG — jobs with no state, no queue length, no DLQ count
# CORRECT — status endpoint, metrics, DLQ alerting
```

## 8. Best Practices

1. BackgroundTasks for disposable work; durable queue for the rest.
2. Return 202 + job_id; let clients poll or subscribe.
3. Retry transient failures with exponential backoff and jitter.
4. Dead-letter permanent failures; alert on DLQ growth.
5. Store job state where operators can see it.
6. Idempotent tasks so retries are safe (see 30-idempotency-and-retries).
7. Keep workers separate for scale and isolation.
8. Timeout every task; no job runs forever.
9. Test failure paths: restart, retry, poison message.
10. Monitor queue depth — the leading indicator of ingestion problems.

## 9. Complexity and Cost

| Tool | Durability | Retries | Ops cost |
|---|---|---|---|
| BackgroundTasks | none (in-memory) | none | zero |
| RQ/ARQ (Redis) | broker-persisted | yes | Redis + worker |
| Celery | broker-persisted | rich | broker + workers + beat |

The durability you buy is a broker and workers to run — the price of not
losing jobs.

## 10. AI Engineering Relevance

**Where this shows up:** LLM pipelines are job-heavy — document ingestion,
embedding generation, fine-tuning runs, eval suites. These are exactly the
loss-sensitive workloads that need durable queues, not BackgroundTasks.

| Concept here | Used for |
|---|---|
| Durable queues | Document ingestion and embedding jobs |
| 202 + job_id | Async model-inference submission |
| Retries + DLQ | Provider-call failures in generation pipelines |
| Progress reporting | Fine-tuning and eval progress visibility |
| Worker separation | Dedicated GPU workers for inference jobs |

**Scale note:** an ingestion pipeline that loses jobs on deploy is a data
quality incident. Durable queues make restarts safe — the job reappears after
the worker comes back.

## 11. Summary

| Concept | Description |
|---|---|
| BackgroundTasks | In-process fire-and-forget; disposable work only |
| Durable queue | Broker-persisted jobs surviving restarts |
| Retries | Transient failures retried with backoff |
| DLQ | Permanent failures parked for inspection |
| 202 + job_id | The async-submission pattern |
| Workers | Separate processes for scale and isolation |

## 12. Quick Reference

| Task | Idiom |
|---|---|
| Fire-and-forget | `background.add_task(fn, *args)` |
| Durable submit | `202` + `job_id`; broker enqueue |
| Retry transient | backoff counter, re-enqueue < max_retries |
| Dead-letter | park after max_retries; alert on growth |
| Status | `GET /jobs/{id}` polling or SSE |
| Idempotency | tasks safe to replay (30-idempotency-and-retries) |

## Next Steps

Next: **[36 — Streaming and SSE](36-streaming-and-sse-lecture.md)** — pushing progress and tokens live.

Continues in: **[04-databases — Redis 07 Sessions and Queues](../../04-databases/redis/lectures/07-session-and-queues-lecture.md)** — Redis as the broker.

Official docs: <https://fastapi.tiangolo.com/tutorial/background-tasks/> · <https://docs.celeryq.dev/>
