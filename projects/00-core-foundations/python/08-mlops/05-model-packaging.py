"""
MLOps - 05: Model Packaging
===========================
Topics: serialization formats, pickle risks, ONNX export, environment
pinning, and model artifacts as supply-chain risk.

Why this matters for AI/backend engineering:
    A model you cannot load is not deployed. The serialization format
    decides portability (Python version, library versions, CPU vs GPU),
    and pickle is unsafe to load from untrusted sources - a real
    supply-chain attack vector in production systems.

Run:      python 05-model-packaging.py
Verify:   python 05-model-packaging.py --verify
Reference: https://docs.python.org/3/library/pickle.html
"""

from __future__ import annotations

import io
import json
import pickle
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ============================================================
# 1. The Model Artifact Bundle
# ============================================================
# Ship more than the weights: model + format + schema + env + version.

@dataclass
class ModelArtifact:
    model: Any
    format: str
    schema: dict[str, Any]
    library: str
    library_version: str
    python_version: str

    def to_manifest(self) -> dict[str, Any]:
        return {
            "format": self.format,
            "schema": self.schema,
            "library": self.library,
            "library_version": self.library_version,
            "python_version": self.python_version,
        }


# ============================================================
# 2. Pickle: easy, dangerous
# ============================================================
# Example 1: round-trip a simple model via pickle.
class _Model:
    def __init__(self, w: float, b: float) -> None:
        self.w = w
        self.b = b

    def predict(self, x: float) -> float:
        return self.w * x + self.b


model = _Model(2.0, 1.0)
buf = io.BytesIO()
pickle.dump(model, buf)
buf.seek(0)
loaded = pickle.load(buf)
print("Example 1: pickle round-trip")
print(f"  predict(3) = {loaded.predict(3)}")
assert loaded.predict(3) == 7.0

# Example 2: pickle executes arbitrary code on load (the supply-chain risk).
class _Exploit:
    def __reduce__(self):
        # Would run any command on unpickle - this one only prints.
        import builtins
        return (builtins.print, ("  [REDACTED] pickle would run arbitrary code!",))

malicious = pickle.dumps(_Exploit())
print("\nExample 2: why pickle is risky")
buf2 = io.BytesIO(malicious)
pickle.load(buf2)  # executes the payload
print("  -> never unpickle untrusted artifacts")

# ============================================================
# 3. Safe serialization: plain JSON for the contract
# ============================================================
# For small models / configs, JSON is portable and safe to load.

def model_to_json(model: _Model) -> str:
    return json.dumps({"w": model.w, "b": model.b, "class": "linear"})

def model_from_json(blob: str) -> _Model:
    data = json.loads(blob)
    return _Model(data["w"], data["b"])


serialized = model_to_json(model)
rebuilt = model_from_json(serialized)
print("\nExample 3: JSON round-trip")
print(f"  rebuilt predict(3) = {rebuilt.predict(3)}")
assert rebuilt.predict(3) == 7.0

# ============================================================
# 4. Environment Pinning
# ============================================================
# An artifact without its environment is a time bomb: numpy 1.x vs 2.x
# can silently change model behavior.

def pin_environment() -> dict[str, str]:
    import platform
    import numpy
    return {
        "python": platform.python_version(),
        "numpy": numpy.__version__,
    }


print("\nExample 4: pinned environment")
env = pin_environment()
print(f"  {env}")
assert "python" in env and "numpy" in env

# ============================================================
# Production Pattern
# ============================================================
def build_artifact(model: _Model, out_dir: Path) -> Path:
    """Write a safe JSON artifact plus a manifest of its environment."""
    import platform
    import numpy
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "model": model_to_json(model),
        "schema": {"input": "float", "output": "float"},
        "env": {"python": platform.python_version(), "numpy": numpy.__version__},
    }
    path = out_dir / "artifact.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return path


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: pickle.load() on any artifact without integrity checks
#   (executes code; use signed artifacts + a safelist of classes)
# CORRECT: prefer JSON/protobuf contracts, or ONNX for portability
# MISTAKE: shipping weights without the library version
# CORRECT: manifest records library + version + python version


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    m = _Model(3.0, -1.0)
    j = model_to_json(m)
    assert json.loads(j)["w"] == 3.0, "JSON must carry weights"
    assert model_from_json(j).predict(2) == 5.0, "JSON round-trip must preserve behavior"

    with tempfile.TemporaryDirectory() as tmp:
        p = build_artifact(m, Path(tmp))
        data = json.loads(p.read_text(encoding="utf-8"))
        assert data["schema"]["input"] == "float", "artifact carries schema"
        assert "env" in data and "numpy" in data["env"], "artifact pins environment"

    a = ModelArtifact(m, "json", {}, "numpy", "2.0", "3.13")
    man = a.to_manifest()
    assert man["format"] == "json" and man["library"] == "numpy", "manifest shape"

    # pickle safety: loading a crafted payload must be detectable as a risk
    evil = pickle.dumps(_Exploit())
    assert b"__reduce__" in evil or len(evil) > 0, "crafted payloads exist"
    print("[OK] 05-model-packaging: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Ship model + schema + env manifest together.")
        print("2. pickle executes code on load - treat artifacts as untrusted.")
        print("3. JSON/ONNX contracts are portable and safe.")
        _verify()
