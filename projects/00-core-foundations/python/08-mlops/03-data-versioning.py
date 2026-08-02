"""
MLOps - 03: Data Versioning
===========================
Topics: content-addressed storage, dataset lineage, large-file handling,
linking data version to model version.

Why this matters for AI/backend engineering:
    A model is meaningless without the exact data it was trained on.
    Versioning data by content (not filename) makes retraining, rollback,
    and audit possible. When a prediction is wrong, the first question is
    always "what data did this model see?"

Run:      python 03-data-versioning.py
Verify:   python 03-data-versioning.py --verify
Reference: https://docs.python.org/3/library/hashlib.html
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ============================================================
# 1. Content-Addressed Storage (CAS)
# ============================================================
# The dataset's name is its hash. If the content changes, the name
# changes - so a name always refers to exactly one dataset.

def sha256_file(path: Path, chunk_size: int = 1 << 16) -> str:
    """Streaming SHA-256 - works on large files without loading them."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


# Example 1: same content, same hash; different content, different hash
import tempfile
with tempfile.TemporaryDirectory() as tmp:
    p1 = Path(tmp) / "train.csv"
    p2 = Path(tmp) / "train-copy.csv"
    p1.write_text("a,b\n1,2\n3,4\n", encoding="utf-8")
    p2.write_text("a,b\n1,2\n3,4\n", encoding="utf-8")
    h1, h2 = sha256_file(p1), sha256_file(p2)
    print("Example 1: content addressing")
    print(f"  {p1.name}: {h1[:16]}...")
    print(f"  {p2.name}: {h2[:16]}...")
    assert h1 == h2, "identical bytes must hash identically"

    p2.write_text("a,b\n1,2\n3,4,EXTRA\n", encoding="utf-8")
    h3 = sha256_file(p2)
    print(f"  after edit: {h3[:16]}...")
    assert h1 != h3, "changed bytes must change the hash"

# ============================================================
# 2. Dataset Lineage
# ============================================================
# A manifest records how a dataset version was produced: raw sources,
# transforms, and parameters. Lineage lets you walk backwards.

@dataclass
class DatasetManifest:
    version: str
    name: str
    rows: int
    columns: list[str]
    source_hash: str
    transforms: list[str] = field(default_factory=list)
    params: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "name": self.name,
            "rows": self.rows,
            "columns": self.columns,
            "source_hash": self.source_hash,
            "transforms": self.transforms,
            "params": self.params,
        }


# Example 2: building a manifest
manifest = DatasetManifest(
    version="v3",
    name="customer_features",
    rows=120_000,
    columns=["age", "income", "spend", "label"],
    source_hash="a1b2c3d4",
    transforms=["dropna()", "onehot(country)", "clip(income, 0, 1e6)"],
    params={"train_frac": 0.8, "seed": 42},
)
print("\nExample 2: dataset manifest")
print(json.dumps(manifest.to_dict(), indent=2))
assert manifest.rows == 120_000 and manifest.version == "v3"

# ============================================================
# 3. Linking Data Version to Model Version
# ============================================================
# A model run must record WHICH data version it consumed. That single
# link is what makes "which model is deployed and on what data?"
# answerable in one query.

@dataclass
class ModelRecord:
    model_id: str
    data_version: str
    metrics: dict[str, float] = field(default_factory=dict)
    artifacts: list[str] = field(default_factory=list)


def train_on(manifest: DatasetManifest, params: dict[str, Any]) -> ModelRecord:
    """Stub: trains and records the data version it used."""
    return ModelRecord(
        model_id=f"model-{hashlib.sha256(manifest.version.encode()).hexdigest()[:8]}",
        data_version=manifest.version,
        metrics={"accuracy": 0.95, "latency_ms": 3.2},
        artifacts=[f"artifacts/{manifest.version}/model.pkl"],
    )


record = train_on(manifest, {"n_estimators": 200})
print("\nExample 3: model linked to data version")
print(f"  model_id={record.model_id}")
print(f"  trained_on={record.data_version}")
assert record.data_version == "v3", "model must record its data version"

# ============================================================
# Production Pattern
# ============================================================
# Store datasets under <root>/<dataset_name>/<sha256> so the filesystem
# itself is content-addressed, then reference the hash everywhere.

def store_dataset(root: Path, name: str, content: str) -> Path:
    """Write content to a CAS location, returning the stored path."""
    digest = hashlib.sha256(content.encode()).hexdigest()
    target = root / name / digest
    target.mkdir(parents=True, exist_ok=True)
    (target / "data.csv").write_text(content, encoding="utf-8")
    return target


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: versioning by filename or 'last_modified' timestamp
#   v1.csv overwritten by v2.csv but still called v1  -> WRONG
# CORRECT: version by content hash - a name can never silently change meaning
# MISTAKE: storing the whole dataset in git
# CORRECT: store the hash + manifest in git; blobs in object storage


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    import tempfile as _tf
    with _tf.TemporaryDirectory() as tmp:
        root = Path(tmp)
        p = store_dataset(root, "train", "x,y\n1,2\n")
        assert p.name == hashlib.sha256(b"x,y\n1,2\n").hexdigest(), "CAS path is the hash"
        # re-storing identical content resolves to the same path
        p2 = store_dataset(root, "train", "x,y\n1,2\n")
        assert p == p2, "same content must dedupe to same path"

    m = DatasetManifest("v1", "d", 10, ["a"], "h")
    d = m.to_dict()
    assert d["version"] == "v1" and d["rows"] == 10, "manifest serializes"
    rec = train_on(m, {"k": 1})
    assert rec.data_version == "v1", "model must link to data version"
    assert rec.model_id.startswith("model-"), "model ids are namespaced"
    print("[OK] 03-data-versioning: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Hash content, not names - CAS makes versions unambiguous.")
        print("2. Manifests capture lineage: sources, transforms, params.")
        print("3. Every model records the data version it trained on.")
        _verify()
