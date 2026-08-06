"""
35 - Background Jobs
======================
BackgroundTasks limits (lost on restart), durable jobs (Celery/RQ/ARQ),
retries and DLQs, progress reporting, when to use which.

Run:      python 35-background-jobs.py
Verify:   python 35-background-jobs.py --verify
Reference: https://fastapi.tiangolo.com/tutorial/background-tasks/
"""

from __future__ import annotations

import sys
import time

from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

app = FastAPI(title="Background Jobs Demo")

JOB_LOG: list[dict] = []


# ============================================================
# 1. BackgroundTasks — in-process, fire-and-forget, NON-durable
# ============================================================
def send_welcome_email(email: str) -> None:
    """Runs after the response is sent, in the same process."""
    time.sleep(0.01)
    JOB_LOG.append({"kind": "email", "to": email, "status": "sent"})


@app.post("/signup", status_code=202)
def signup(email: str, background: BackgroundTasks) -> dict:
    """The response returns immediately; the email job runs after."""
    background.add_task(send_welcome_email, email)
    return {"status": "accepted", "email": email}


# ============================================================
# 2. The hard truth: BackgroundTasks are lost on restart
# ============================================================
def background_tasks_limits() -> list[str]:
    return [
        "In-memory only: a crash/restart loses every pending task",
        "No retries: if the task raises, it is gone",
        "No dedup, no priority, no visibility",
        "Best for: emails, thumbnails, cache warming AFTER a response",
        "Wrong for: anything you cannot afford to lose",
    ]


# ============================================================
# 3. A minimal durable queue (in-memory, retry + DLQ semantics)
# ============================================================
class JobQueue:
    """Illustrates the durable-queue contract: enqueue, process, retry,
    dead-letter. Real systems use Celery/RQ/ARQ on Redis.

    Durability comes from the BROKER (Redis) persisting the message; this
    demo keeps the contract and swaps the broker for a list.
    """

    def __init__(self):
        self._queue: list[dict] = []
        self._dlq: list[dict] = []
        self._attempts: dict[int, int] = {}

    def enqueue(self, kind: str, payload: dict) -> int:
        job_id = len(self._queue) + len(self._dlq) + 1
        self._queue.append({"id": job_id, "kind": kind, "payload": payload})
        return job_id

    def drain(self, max_retries: int = 3) -> list[dict]:
        """Process everything, retrying failures up to max_retries,
        sending the finally-failed to the dead-letter queue."""
        results = []
        while self._queue:
            job = self._queue.pop(0)
            try:
                self._run(job)
                results.append({"id": job["id"], "status": "done"})
            except Exception as e:
                attempt = self._attempts.get(job["id"], 0) + 1
                self._attempts[job["id"]] = attempt
                if attempt >= max_retries:
                    job["error"] = str(e)
                    self._dlq.append(job)
                    results.append({"id": job["id"], "status": "dead"})
                else:
                    self._queue.append(job)     # retry
                    results.append({"id": job["id"], "status": "retry"})
        return results

    def _run(self, job: dict) -> None:
        if job["kind"] == "flaky":
            if self._attempts.get(job["id"], 0) < 2:
                raise ValueError("transient failure")
        JOB_LOG.append({"kind": job["kind"], "id": job["id"], "status": "processed"})


queue = JobQueue()


@app.post("/jobs", status_code=202)
def submit_job(kind: str) -> dict:
    """Durable-style enqueue: survives in the broker, retried, DLQ'd."""
    if kind not in ("email", "flaky", "report"):
        raise HTTPException(status_code=400, detail="Unknown job kind")
    job_id = queue.enqueue(kind, {})
    return {"status": "queued", "job_id": job_id}


# ============================================================
# 4. When to use which
# ============================================================
def choose_worker() -> str:
    return (
        "BackgroundTasks: fire-and-forget after a response (emails, logs) "
        "| Durable queue (Celery/RQ/ARQ): anything you cannot lose "
        "(billing, ingestion, model inference jobs) "
        "| Streaming/batches: dedicated workers scaled independently"
    )


# ============================================================
# Summary
# ============================================================
print("=" * 60)
print("Summary:")
print("- BackgroundTasks: in-process, lost on restart, no retries")
print("- Durable queue: broker-persisted, retried, DLQ for poison jobs")
print("- Retry semantics: transient errors retry, permanent go to DLQ")
print("- Scale: workers are a separate process/deployment")
print("=" * 60)
for line in background_tasks_limits():
    print(f"  - {line}")


def _verify() -> None:
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        r = client.post("/signup", params={"email": "a@b.com"})
        assert r.status_code == 202
        assert r.json()["status"] == "accepted"

        # Durable queue: enqueue + drain with retries and DLQ
        flaky_id = client.post("/jobs", params={"kind": "flaky"}).json()["job_id"]
        ok_id = client.post("/jobs", params={"kind": "email"}).json()["job_id"]
        bad_kind = client.post("/jobs", params={"kind": "nope"})
        assert bad_kind.status_code == 400

        # Drain: flaky fails twice then succeeds (retry), email succeeds
        results = queue.drain(max_retries=3)
        by_id = {r["id"]: r["status"] for r in results}
        assert by_id[flaky_id] == "done", "flaky job must succeed after retries"
        assert by_id[ok_id] == "done"

        # A permanently-failing job lands in the DLQ
        queue2 = JobQueue()
        # make every attempt fail by raising always: simulate with max_retries=1
        poisoned = queue2.enqueue("flaky", {})
        # force failure: monkeypatch _run to always raise
        def always_fail(job):
            raise RuntimeError("permanent")
        queue2._run = always_fail  # type: ignore[method-assign]
        results2 = queue2.drain(max_retries=2)
        assert any(r["id"] == poisoned and r["status"] == "dead" for r in results2)
        assert len(queue2._dlq) == 1, "poison job must be dead-lettered"

    assert "restart" in " ".join(background_tasks_limits()).lower()

    print("[OK] 35-background-jobs: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run("35-background-jobs:app", host="127.0.0.1", port=8000)
    else:
        _verify()
