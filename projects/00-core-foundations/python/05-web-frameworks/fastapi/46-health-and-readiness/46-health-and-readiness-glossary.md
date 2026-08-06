# Health & Readiness — Glossary 46

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Drain | Shutdown | Letting in-flight requests finish before exit |
| Grace period | Shutdown | The window allowed for draining before SIGKILL |
| In-flight | Concept | Requests currently executing |
| Liveness | Probe | "Is the process alive?" — crash → restart |
| Orchestrator | Platform | K8s/ECS/Nomad — decides restarts from probes |
| Probe | Mechanism | The endpoint the orchestrator polls |
| Readiness | Probe | "Can it serve traffic?" — deps → route or stop |
| SIGKILL | Signal | Uncatchable kill after the grace period |
| SIGTERM | Signal | The polite shutdown request → drain first |
| Startup | Probe | "Is it still warming up?" — gates traffic |
| Termination grace | Shutdown | The orchestrator's drain allowance |
| 503 | Status | Not ready yet — stop routing, don't kill |

## Detailed Definitions

### Drain
**Definition**: The shutdown phase letting in-flight requests finish
before the process exits — refusing new work while completing old.
**Related**: Grace period

### Grace period
**Definition**: The window the orchestrator allows for draining
(`terminationGracePeriod`) before SIGKILL. A service that drains slowly
gets killed anyway.
**Related**: SIGKILL

### In-flight
**Definition**: Requests currently executing — what draining protects.
**Related**: Drain

### Liveness
**Definition**: The probe answering "is the process alive?" — process-only
checks; 500 means restart. Must never depend on external services.
**Related**: Readiness

### Orchestrator
**Definition**: The platform (Kubernetes, ECS, Nomad) polling probes and
deciding restarts, routing, and shutdown.
**Related**: Probe

### Probe
**Definition**: An HTTP endpoint the orchestrator polls periodically —
liveness, readiness, or startup.
**Related**: Liveness

### Readiness
**Definition**: The probe answering "can it serve traffic?" — dependency
checks; 503 stops routing but keeps the process alive to recover.
**Related**: Liveness

### SIGKILL
**Definition**: The uncatchable force-kill the orchestrator sends when the
grace period expires — the deadline draining must beat.
**Related**: Grace period

### SIGTERM
**Definition**: The polite shutdown signal — the service's cue to stop
accepting, drain, and exit.
**Related**: Drain

### Startup
**Definition**: The probe answering "is it still warming up?" — gates
traffic until cold-start work (model load) completes.
**Related**: Probe

### Termination grace
**Definition**: The orchestrator-configured allowance for a pod to shut
down gracefully before SIGKILL.
**Related**: Grace period

### 503
**Definition**: "Not ready" — the orchestrator stops routing; the process
is not dead and must not be restarted.
**Related**: Readiness

## Key Concepts Summary

### The three probes
- liveness: process alive → restart on 500.
- readiness: dependencies OK → route or stop routing.
- startup: warmed up → gate traffic until yes.

### The shutdown sequence
- SIGTERM → stop accepting → drain in-flight → exit within grace.
- SIGKILL after grace — drain fast or be killed anyway.

### The incident-prevention rule
- Never let readiness failures kill the process (that is liveness's job).
- Never let liveness depend on external services.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Is the process alive? — ___
2. Can it serve traffic? — ___
3. Still warming up? — ___
4. Letting in-flight work finish — ___
5. The force-kill after grace — ___
6. The polite shutdown signal — ___
7. Requests currently executing — ___
8. Stop routing, don't kill — ___

**Answers:** 1-liveness, 2-readiness, 3-startup probe, 4-drain, 5-SIGKILL,
6-SIGTERM, 7-in-flight, 8-503
