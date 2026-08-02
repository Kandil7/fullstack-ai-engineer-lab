# MLOps — 06: Docker for ML

## Topic Overview

Docker containers are the standard unit of ML deployment: they package the
model artifact, its exact runtime environment (Python version, system
libraries, dependencies), and the serving code into a single immutable image
that runs identically anywhere — a laptop, a CI runner, a Kubernetes pod, an
edge box. Docker is what makes the reproducibility contract from Lecture 01
*enforceable*: the image *is* the pinned environment.

For ML engineers, Docker solves three specific problems: (1) **environment
drift** — the image built today is the exact env that serves tomorrow; (2)
**portability** — CPU training, GPU training, and CPU serving can share one
codebase with different images; (3) **isolation & scale** — Kubernetes and
cloud serving platforms (SageMaker, Vertex) are container-native: your model
*must* be a container to be served at scale.

The core mental model: a **Dockerfile** is a recipe; `docker build` executes it
into an **image** (immutable); `docker run` starts a **container** (a running
instance). Images are layered and cached — layer order is the #1 performance
and correctness lever.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Write a Dockerfile that packages a trained model + FastAPI serving app
2. Explain image layering and order layers for cache efficiency
3. Use multi-stage builds to keep images small (train vs serve)
4. Handle GPU images (`nvidia/cuda` base, `--gpus all`)
5. Build, tag, and push images; debug with `docker logs`, `docker exec`
6. Distinguish CPU vs GPU image strategies
7. Apply the 12-factor principles (config via env, stateless) to ML containers

## Prerequisites

| Need | Where |
|---|---|
| Model packaging | `08-mlops/lectures/05-model-packaging-lecture.md` |
| FastAPI basics | `05-web-frameworks/fastapi/` |
| Reproducibility | `08-mlops/lectures/01-reproducibility-lecture.md` |
| Shell basics | `00-core-foundations/git-linux/` |

## 1. The Dockerfile as a Reproducible Recipe

A minimal serving image: Python 3.11 slim, install the pinned deps, copy the
packaged model and the serving code, expose the port, and start the server.

```dockerfile
# Multi-stage build: builder compiles, runner serves (small final image)
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS runner
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY model/ /app/model/          # the packaged artifact
COPY serve.py /app/serve.py
ENV MODEL_PATH=/app/model
EXPOSE 8000
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]
```

Output (conceptually):
```
Successfully built 5f2c9a1b
Successfully tagged churn-serve:latest
```

The image pins: Python version (3.11-slim), deps (requirements.txt), model
artifact (model/), and serving entrypoint — the whole reproducibility story in
one immutable object.

## 2. Layer Ordering and the Cache

Every `RUN`, `COPY`, and `ENV` creates a **layer**. Docker caches layers;
unchanged earlier layers are reused. The rule: **put things that change least
often first**. Dependencies change rarely; model artifacts change every
retraining; code changes constantly.

```dockerfile
# GOOD order: deps (rare change) → model (occasional) → code (constant)
COPY requirements.txt .
RUN pip install -r requirements.txt     # cached unless reqs change
COPY model/ .                           # cached unless model changes
COPY serve.py .                         # always rebuilt
```

Output (conceptually):
```
CACHED  → pip install layer (fast)
CACHED  → model layer
BUILD   → serve.py layer
```

Wrong order (code first, deps last) invalidates the pip layer on every code
edit — a 5-minute build becomes a 25-minute build.

## 3. Multi-Stage Builds: Train vs Serve

A serving image should be **small**: no compilers, no training code, no dev
deps. Multi-stage builds separate "build environment" from "runtime
environment". The classic ML pattern: build the model in a fat training image,
copy only the artifact + minimal runtime into a slim serving image.

```dockerfile
FROM python:3.11 AS train
COPY requirements-train.txt .
RUN pip install -r requirements-train.txt
COPY train.py .
RUN python train.py --out /model/model.pkl     # artifact built here

FROM python:3.11-slim AS serve
COPY --from=train /model/ /model/
COPY requirements-serve.txt .
RUN pip install -r requirements-serve.txt
COPY serve.py .
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0"]
```

Output (conceptually):
```
serve image size: 420MB  (vs 2.1GB if train deps shipped)
```

This is why "keep the model out of the training codebase" is operationalized:
the serve image contains only what predictions need.

## 4. GPU Images

GPU inference/training needs the CUDA runtime inside the container, plus the
NVIDIA container toolkit on the host. Base image choice matters:

```dockerfile
# GPU inference image
FROM nvidia/cuda:12.1-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y --no-install-recommends python3.11 python3-pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY model.onnx /model/
COPY serve.py .
CMD ["python", "serve.py"]
```

Output (conceptually):
```
docker run --gpus all churn-gpu:latest   → GPU visible inside container
```

**Key rule:** training images use `nvidia/cuda:12.1-devel-ubuntu22.04`
(compilers + headers), serving images use `-runtime-` (just the runtime) —
that alone saves gigabytes.

## 5. Config and Secrets: 12-Factor for ML

Containers are stateless and configured by **environment variables** — never
hardcode paths, endpoints, or secrets in the image (secrets get baked into
layers and leak).

```python
import os
MODEL_PATH = os.environ.get("MODEL_PATH", "/model/model.pkl")
DB_URL = os.environ["DATABASE_URL"]   # from the orchestration layer, not the image
```

Output (conceptually):
```
docker run -e DATABASE_URL=postgres://... -e MODEL_PATH=/model/model.pkl churn-serve
```

The same image promotes through staging → production with different env vars —
no rebuild needed. This is the 12-factor "config in environment" rule, which
is what makes one image deployable anywhere.

## 6. Local Development and Debugging

The dev loop: `docker build` → `docker run` → `docker logs` → `docker exec`
into the container to inspect. Health checks keep orchestrators honest.

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" \
  || exit 1
```

Output (conceptually):
```
docker ps                → container healthy (state: healthy)
docker logs churn        → uvicorn access logs
docker exec -it churn bash   → shell inside the container
```

## Every Use Case

- **Model serving endpoints**: one image per model version, deployed on
  Kubernetes or a serving platform.
- **Batch scoring jobs**: cron/K8s Job containers running the same image.
- **Training at scale**: GPU training images with pinned CUDA + frameworks.
- **CI/CD**: run the smoke tests in the same image that will serve — parity.
- **Edge deployment**: same image (or a slimmed variant) on edge hardware.
- **Experimentation environments**: reproduce a researcher's exact env as an
  image ("here's the image that produced these results").
- **Multi-team ML platforms**: a standard base image with pinned versions is
  the platform team's control point.
- **Disaster recovery**: an image is an immutable snapshot — restore any
  historical serving state by running its image.

## Real-World Use Cases for AI Engineers

- **Fintech model rollout**: the champion model ships as a Docker image tagged
  with the model version + git SHA. The platform team promotes that exact
  image to production; a bad release is a rollback to the previous image tag —
  not a rebuild. The audit trail is the image registry history.
- **E-commerce latency**: the ranking model is a slim ONNX-serve image (~400MB
  vs 2GB) that scales to hundreds of pods; multi-stage builds keep rollout
  time under a minute instead of ten.
- **Healthcare edge inference**: the sepsis model image (with the ONNX runtime)
  runs on hospital edge boxes; the hospital's IT department accepts the image
  as a versioned, signed artifact — reproducibility for regulatory review.
- **GPU training farm**: a team of researchers shares one GPU training image
  with pinned CUDA 12.1 + PyTorch; "works in the research image" is the
  universal repro story, and `--gpus all` is the only difference per machine.
- **RAG service**: the retrieval service, the embedder, and the LLM gateway
  each deploy as separate images; upgrades are per-image tag flips with
  per-service health checks.

## Common Mistakes to Avoid

### Mistake 1: Installing deps after copying code
```
# WRONG — pip layer invalidated on every code change
COPY . .
RUN pip install -r requirements.txt
# CORRECT
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### Mistake 2: Shipping the training image to production
Training images carry compilers + training data — huge and risky. Multi-stage
builds to a slim runtime image.

### Mistake 3: Baking secrets into the image
`ENV API_KEY=...` persists in layers and leaks. Pass secrets at runtime.

### Mistake 4: `pip install` without pins in the image
The image is only reproducible if the requirements are pinned (Lecture 01).

### Mistake 5: Ignoring the user / running as root
Run as a non-root user (`USER 1000`) — containers run as root by default.

### Mistake 6: No healthcheck
Orchestrators can't restart what they can't observe. Add `HEALTHCHECK`.

### Mistake 7: Pulling the wrong base for GPU
`cuda:12.1-devel` in serving (2GB+ of compilers) instead of `-runtime`.

## Best Practices

1. Pin base image tags and every pip dep
2. Order layers: deps → model → code (least-to-most changing)
3. Use multi-stage builds; keep the serving image small
4. Use `-runtime-` CUDA images for serving, `-devel-` for training
5. Pass config and secrets via environment, never baked in
6. Add a `HEALTHCHECK` endpoint the image exposes
7. Tag images with model version + git SHA for traceability
8. Run as a non-root user
9. Test the image in CI before promoting (smoke the same image)
10. Keep the model artifact out of the build context; COPY only what's needed

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Build from cold cache | 5–25 min | layers ≤ sum | multi-stage + cached layers |
| Rebuild after code change | 1–3 min | O(changed layers) | good layer order (deps cached) |
| Push image to registry | O(size) | O(size) | slim images, ONNX runtime |
| GPU image | — | 3–6 GB | `-runtime-` instead of `-devel-` |

## AI Engineering Relevance

**Where this shows up:** every model that reaches a server, edge device, or
batch job; every CI promotion gate; every serving platform integration.

| Concept here | Used for |
|---|---|
| Image = pinned env | reproducibility enforcement |
| Multi-stage | small, safe serving images |
| GPU images | training and GPU inference at scale |
| 12-factor config | one image, any environment |

**Scale note:** at 100+ model versions, the image registry IS the deploy
catalog — each tag a reproducible snapshot. Image size directly controls
rollout speed: 400MB vs 2GB is the difference between seconds and minutes of
cluster rollout time.

## Practice Exercises

### Exercise 1: Read a Dockerfile (Easy)
Given a Dockerfile with layers out of order, reorder them for cache
efficiency and explain the reason for each move.

### Exercise 2: Multi-Stage Plan (Medium)
Write a multi-stage Dockerfile for a sklearn model: training stage builds the
artifact, serving stage serves it with only runtime deps. State the expected
final image size difference.

### Exercise 3: Healthcheck + Config (Medium)
Extend a serving app so the image reads `MODEL_PATH` and `PORT` from env vars
and exposes `/health`; write the Dockerfile `HEALTHCHECK` and the `docker run`
command with `-e` flags.

### Exercise 4: Image Audit (Hard)
Given a bloated Dockerfile (training deps + secrets + root user + no pins),
rewrite it to satisfy: slim runtime, pinned deps, non-root, env config, health
check — and list each fix's security/size impact.

## Summary

| Concept | Description |
|---|---|
| Image | immutable, layered snapshot of the env |
| Layer order | cache efficiency = deps → model → code |
| Multi-stage | train fat, serve slim |
| GPU images | `-runtime-` serve, `-devel-` train |
| 12-factor | env config, stateless, one image anywhere |

Docker turns the reproducibility contract into an enforceable object: the image
either contains the exact environment or it doesn't, and it ships as one
immutable unit. For ML, it is also the on-ramp to every container-native
serving platform.

## Quick Reference

| Task | Idiom |
|---|---|
| Build image | `docker build -t churn-serve:1.2.0 .` |
| Run container | `docker run -p 8000:8000 churn-serve:1.2.0` |
| GPU run | `docker run --gpus all churn-gpu:latest` |
| Inspect | `docker logs <id>`, `docker exec -it <id> bash` |
| Env config | `docker run -e MODEL_PATH=/model/model.pkl ...` |

## Next Steps

Next: **[07 Model Serving](07-model-serving-lecture.md)** — exposing the
packaged, containerized model as a production HTTP endpoint.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://docs.docker.com/build/building/multi-stage/,
https://docs.docker.com/engine/reference/run/#runtime-constraints-on-resources
