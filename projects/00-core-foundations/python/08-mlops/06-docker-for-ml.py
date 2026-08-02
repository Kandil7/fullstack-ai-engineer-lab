"""
MLOps - 06: Docker for ML
==========================
Topics: multi-stage builds, CUDA base images, layer caching, image size,
GPU passthrough, reproducible builds. Teaches the *design* of a Dockerfile
through the artifacts it produces - no Docker daemon required.

Why this matters for AI/backend engineering:
    Training and serving environments drift. Containers pin the OS, the
    Python version, the CUDA stack, and the libraries so a model behaves
    identically on a laptop and in production. Image size and layer order
    are cost and CI-speed decisions.

Run:      python 06-docker-for-ml.py
Verify:   python 06-docker-for-ml.py --verify
Reference: https://docs.docker.com/build/building/multi-stage/
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


# ============================================================
# 1. Layer Model
# ============================================================
# Every Dockerfile instruction creates a layer. Cache invalidation
# propagates: change line 2 and everything below rebuilds. So put
# slow-changing steps (base image, pip install) BEFORE fast-changing
# steps (your code).

@dataclass
class Layer:
    instruction: str
    size_mb: float
    change_frequency: str  # "rare" | "often"
    cache_hit: bool = True


def order_layers(layers: list[Layer]) -> list[Layer]:
    """Reorder instructions: rarest-changing first (best cache reuse).

    Tie-break by instruction type so base images (FROM) always precede
    dependency installs (RUN pip) which precede application code (COPY).
    """
    rank = {"rare": 0, "often": 1}
    type_rank = {"FROM": 0, "RUN pip": 1, "RUN": 2, "COPY": 3, "CMD": 4, "ENTRYPOINT": 4}

    def key(l: Layer) -> tuple[int, int]:
        inst = l.instruction
        t = next((tk for tk in type_rank if inst.startswith(tk)), 5)
        return (rank[l.change_frequency], t)

    return sorted(layers, key=key)


# Example 1: bad vs good instruction order
bad = [
    Layer("COPY app/ ./app/", 5.0, "often"),
    Layer("RUN pip install -r requirements.txt", 900.0, "rare"),
    Layer("FROM python:3.13-slim", 150.0, "rare"),
]
good = order_layers(bad)
print("Example 1: layer ordering (rare-changing first)")
for l in good:
    print(f"  [{l.instruction}]  size={l.size_mb}MB  changes={l.change_frequency}")
assert good[0].instruction.startswith("FROM"), "base image must be first"
assert good[1].instruction.startswith("RUN pip"), "pip install before copying code"

# ============================================================
# 2. Multi-Stage Builds
# ============================================================
# Build stage installs the compiler toolchain; the runtime stage copies
# only the artifacts. The result: a small, clean serving image.

@dataclass
class BuildPlan:
    stages: list[str]

    def runtime_size_mb(self) -> float:
        # The runtime stage excludes build-time deps.
        return sum(s.size_mb for s in self.stages if s.kind == "runtime")


@dataclass
class Stage:
    name: str
    kind: str  # "build" | "runtime"
    size_mb: float


# Example 2: multi-stage shrinks the image
stages = [
    Stage("builder", "build", 1200.0),   # compilers, cuda toolkit
    Stage("runtime", "runtime", 480.0),  # only runtime libs + artifacts
]
plan = BuildPlan(stages)
print("\nExample 2: multi-stage size")
print(f"  build stage: 1200MB (not shipped)")
print(f"  runtime stage: {plan.runtime_size_mb()}MB (this is what ships)")
assert plan.runtime_size_mb() == 480.0

# ============================================================
# 3. GPU Passthrough
# ============================================================
# Training images need the CUDA runtime AND the driver's userspace libs.
# nvidia/cuda base image + --gpus all at runtime.

@dataclass
class GPUCapability:
    cuda_in_image: bool
    driver_present_on_host: bool

    def can_train_on_gpu(self) -> bool:
        return self.cuda_in_image and self.driver_present_on_host


# Example 3: GPU readiness
cap = GPUCapability(cuda_in_image=True, driver_present_on_host=True)
print("\nExample 3: GPU passthrough")
print(f"  CUDA in image: {cap.cuda_in_image}")
print(f"  driver on host: {cap.driver_present_on_host}")
print(f"  can train on GPU: {cap.can_train_on_gpu()}")
assert cap.can_train_on_gpu()

# ============================================================
# 4. Dependencies and Reproducibility
# ============================================================
# Pin exact versions in requirements, not ranges. "numpy>=1.26" is a
# different image every week.

def freeze_requirements() -> list[str]:
    return ["numpy==2.1.3", "pandas==2.2.3", "scikit-learn==1.5.2", "torch==2.5.1"]


# Example 4: pinned deps
deps = freeze_requirements()
print("\nExample 4: pinned requirements")
for d in deps:
    print(f"  {d}")
assert all("==" in d for d in deps), "exact pins, not ranges"

# ============================================================
# Production Pattern
# ============================================================
# The canonical serving Dockerfile, expressed as data.

SERVING_DOCKERFILE = """# --- builder: compile what we need, then throw it away ---
FROM python:3.13-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# --- runtime: only what ships ---
FROM python:3.13-slim
COPY --from=builder /install /usr/local
COPY app/ ./app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""


def validate_dockerfile(dockerfile: str) -> tuple[bool, list[str]]:
    """Cheap static checks on a Dockerfile's structure."""
    issues: list[str] = []
    lines = [l.strip() for l in dockerfile.splitlines() if l.strip()]
    if not any(l.startswith("FROM") for l in lines):
        issues.append("missing FROM base image")
    if not any(l.startswith("COPY") for l in lines):
        issues.append("nothing copied into the image")
    if not any(l.startswith("CMD") or l.startswith("ENTRYPOINT") for l in lines):
        issues.append("no CMD/ENTRYPOINT - image is not runnable")
    return (not issues, issues)


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: pip install AFTER COPY app/ -> every code change rebuilds deps
# MISTAKE: unpinned ranges -> non-reproducible images
# MISTAKE: shipping the 1.2GB build stage to production


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    layers = [
        Layer("COPY app/", 5.0, "often"),
        Layer("FROM base", 150.0, "rare"),
        Layer("RUN pip install", 900.0, "rare"),
    ]
    ordered = order_layers(layers)
    assert ordered[0].instruction.startswith("FROM"), "base image first"
    assert ordered[-1].instruction.startswith("COPY app"), "code last"

    plan = BuildPlan([Stage("b", "build", 1000.0), Stage("r", "runtime", 300.0)])
    assert plan.runtime_size_mb() == 300.0, "runtime size excludes build stage"

    assert GPUCapability(True, True).can_train_on_gpu()
    assert not GPUCapability(True, False).can_train_on_gpu(), "missing driver blocks GPU"

    ok, issues = validate_dockerfile(SERVING_DOCKERFILE)
    assert ok, f"canonical Dockerfile must validate: {issues}"
    bad_ok, bad_issues = validate_dockerfile("RUN echo hi")
    assert not bad_ok and bad_issues, "invalid Dockerfile must be flagged"

    assert all("==" in d for d in freeze_requirements()), "deps pinned"
    print("[OK] 06-docker-for-ml: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Rare-changing layers first for cache hits.")
        print("2. Multi-stage: build big, ship small.")
        print("3. Pin exact versions; GPU needs CUDA image + host driver.")
        _verify()
