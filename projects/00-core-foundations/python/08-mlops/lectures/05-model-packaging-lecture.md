# MLOps — 05: Model Packaging

## Topic Overview

Model packaging is the art of turning a trained artifact (weights, scalers,
preprocessing steps) into a **self-contained, deployable unit**: something that
can be loaded, versioned, and served on any machine — without the training
codebase, without ad-hoc glue, and without "it works in the notebook"
surprises. A model that exists only as `model.pt` plus a folder of notebook
cells is not deployable; a packaged model is *one artifact that knows how to
predict*.

The canonical Python answer is **joblib/Pickle** for sklearn-style pipelines
and **torch.save / ONNX / TensorFlow SavedModel** for deep learning — but
"packaging" is more than a serialization format. It is a **contract**: the
artifact carries its input/output schema, its dependencies, and its
preprocessing, so that any serving layer can load it and call `predict()`
without knowing how it was trained. MLflow codifies this with `mlflow.pyfunc`
(the universal Python model flavor): every framework gets wrapped in a single
`load_model(path).predict(data)` interface.

Why this matters for an AI engineer: packaging mistakes are the most common
source of "works in dev, explodes in prod" failures — missing scaler, wrong
feature order, a categorical encoding that never got saved, a Python version
mismatch. Packaging is where the model stops being *research* and starts being
*software*.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Serialize a trained sklearn pipeline with joblib (including the preprocessor!)
2. Package a deep-learning model with torch.save / ONNX export
3. Build a `pyfunc` wrapper so any model exposes one `predict(data)` interface
4. Define and validate the model's input/output signature
5. Capture the dependency environment alongside the artifact (conda/pip + Python version)
6. Detect and fix the classic "missing preprocessor" packaging bug
7. Choose between pickle, ONNX, and SavedModel based on the deployment target

## Prerequisites

| Need | Where |
|---|---|
| sklearn pipelines | `07-machine-learning/` lectures |
| Model registry | `08-mlops/lectures/04-model-registry-lecture.md` |
| Environment capture | `08-mlops/lectures/01-reproducibility-lecture.md` |
| NumPy/pandas basics | `03-libraries/` |

## 1. The Packaging Contract

A packaged model must answer four questions at load time:
1. **What is the input schema?** (feature names, dtypes, order)
2. **How do I predict?** (one interface, e.g. `predict(df)`)
3. **What dependencies do I need?** (versions, Python version)
4. **Where is the artifact?** (self-contained or referenced)

The classic failure: training loads raw data → fits `StandardScaler` → fits a
classifier, but only saves the classifier. The served model receives raw
features and silently predicts garbage. **The preprocessor is part of the
model** — package the whole pipeline.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000)),
])
# fit on X_train, y_train ...
# package the WHOLE pipeline:
import joblib
joblib.dump(pipe, "churn_model.pkl")
```

Output (conceptually):
```
['churn_model.pkl']  (contains scaler + classifier together)
```

## 2. Serialization Formats by Framework

| Framework | Format | Strengths | Watch out for |
|---|---|---|---|
| sklearn | `joblib.dump` | whole pipelines, fast | only Python, version-sensitive |
| PyTorch | `torch.save(state_dict)` | research standard | load with the same class definitions |
| PyTorch → serving | `torch.jit.script` / `torch.export` | no Python needed at serving | graph tracing pitfalls |
| Universal | **ONNX** | framework-agnostic, C++/mobile/web runtimes | opset mismatches, dynamic shapes |
| TensorFlow | `SavedModel` | production-native, TF Serving | heavyweight dependency |

The AI engineer's rule of thumb: **pickle/joblib for Python-only serving,
ONNX when you need performance or portability (mobile, edge, other languages),
SavedModel when the infra is already TF-centric.**

```python
# ONNX export — portable, no Python needed at serving time
import onnx
import onnxruntime as ort

# exported = onnx.ModelProto (from torch.onnx.export or sklearn-onnx)
sess = ort.InferenceSession("churn_model.onnx")
pred = sess.run(None, {"X": X_numpy.astype("float32")})
```

Output (conceptually):
```
[[0.12], [0.87], ...]  (class probabilities from the ONNX runtime)
```

## 3. The Universal Interface: `pyfunc`

MLflow's `pyfunc` flavor makes every model — sklearn, torch, keras, ONNX,
even a raw function — expose the same two methods: `load_model(path)` and
`model.predict(data)`. This is the interface contract that lets serving layers,
batch jobs, and CI all talk to any model without framework-specific code.

```python
import mlflow.pyfunc

class ChurnWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        import joblib
        self._pipe = joblib.load(context.artifacts["model_pkl"])

    def predict(self, context, model_input):
        # model_input is a pandas DataFrame
        return self._pipe.predict_proba(model_input)[:, 1]

mlflow.pyfunc.save_model(
    "churn_pyfunc", python_model=ChurnWrapper(),
    artifacts={"model_pkl": "churn_model.pkl"},
)
loaded = mlflow.pyfunc.load_model("churn_pyfunc")
print(loaded.predict(df_new).head())
```

Output (conceptually):
```
0    0.88
1    0.12
2    0.54
Name: 0, dtype: float64
```

## 4. Input/Output Signature: The Schema Contract

A packaged model that does not declare its schema is a footgun: a feature-order
mismatch between training and serving is silent garbage. Declare the signature
at packaging time and validate at load time.

```python
from mlflow.models import ModelSignature
from mlflow.types import ColSpec, DataType, Schema

signature = ModelSignature(
    inputs=Schema([
        ColSpec(DataType.double, "tenure"),
        ColSpec(DataType.double, "monthly_charges"),
        ColSpec(DataType.long, "contract_type_code"),
    ]),
    outputs=Schema([ColSpec(DataType.double, "churn_probability")]),
)
```

Output (conceptually):
```
inputs: [tenure: double, monthly_charges: double, contract_type_code: long]
outputs: [churn_probability: double]
```

A signature check at serving time catches the "you sent me the columns in the
wrong order" class of bug *before* it reaches users. This is the same idea as
schema validation in data pipelines (Lecture 10 in this phase) applied to the
model boundary.

## 5. Dependency Capture: The Environment Around the Artifact

The artifact is half the package; the **environment** is the other half.
`conda_env` or `pip_requirements` recorded with the artifact pin the exact
versions the model needs. Without them, the artifact loads on your machine and
fails (or silently changes behavior) on the serving box.

```yaml
# conda.yaml shipped with the artifact
channels: [defaults]
dependencies:
  - python=3.11
  - pip
  - pip:
    - scikit-learn==1.3.2
    - joblib==1.3.2
    - numpy==1.24.4
```

Output (conceptually):
```
A serving container built from this env reproduces the training env.
```

## 6. Versioning and Cache: The Model File as a Content-Addressed Object

A packaged model should be treated like any other artifact: hashed,
immutably stored, and cached at the serving layer. The same content-addressing
from Lecture 03 applies to `model.pkl`: `sha256(model bytes)` is the model's
identity, and the serving layer caches by hash so the same model is never
loaded twice.

```python
import hashlib

def model_sha256(path: str) -> str:
    return f"sha256:{hashlib.sha256(open(path,'rb').read()).hexdigest()[:16]}"
```

Output (conceptually):
```
sha256:5f8b2c4d...
```

## Every Use Case

- **REST inference endpoints**: the artifact + pyfunc wrapper behind FastAPI/Flask.
- **Batch scoring**: same packaged model, offline jobs — identical predictions
  to the online endpoint (consistency guarantee).
- **MLflow/serving platforms**: SageMaker, Vertex, Databricks all consume
  registered packaged models.
- **Edge/embedded inference**: ONNX → mobile, browser (ONNX Runtime Web), IoT.
- **CI/CD gates**: load the packaged model in CI and assert its signature and
  a golden-output test before promotion.
- **Multi-team reuse**: a packaged model is a shareable, consumable artifact —
  other teams call it without your training code.
- **Experimentation → production parity**: the exact same artifact that won the
  leaderboard is what gets served — no re-training, no re-wrapping.

## Real-World Use Cases for AI Engineers

- **Fraud model at a fintech**: the winning XGBoost pipeline is packaged
  *including* the one-hot encoder and the custom feature transformers. When a
  data scientist later trains a variant, the artifact is what moves through
  staging; serving never re-runs training code — eliminating the classic
  "retrained silently on serving box" incident.
- **Recommendation latency**: an ONNX export of a PyTorch ranking model runs
  in 3ms on the serving cluster instead of 25ms via Python — a 8x latency win
  with byte-identical predictions after a golden test.
- **Healthcare device edge case**: a sepsis-prediction model must run on a
  hospital edge box with no Python. The ONNX artifact runs in the C++ runtime;
  the packaging step (with its golden test) is what the hospital's IT audit
  accepts.
- **LLM serving**: LoRA adapters are packaged as artifacts with their base
  model version and tokenizer; serving loads adapter+base as one unit (Phase 9).
- **Startup velocity**: one ML engineer packages a churn model as pyfunc; the
  backend team integrates it in an afternoon without learning sklearn.

## Common Mistakes to Avoid

### Mistake 1: Saving the classifier, not the pipeline
```
# WRONG — the scaler is lost; served inputs are unnormalized
joblib.dump(clf, "model.pkl")
# CORRECT — package preprocessor + model together
joblib.dump(Pipeline([("scaler", scaler), ("clf", clf)]), "model.pkl")
```

### Mistake 2: No signature declared
Feature-order mismatches are silent. Declare inputs/outputs at packaging time.

### Mistake 3: No dependency pinning
`pip install sklearn` in the serving container lands a new version → behavior
drift. Ship the conda/pip env with the artifact.

### Mistake 4: Pickling with local classes
A custom class defined in a notebook cannot be unpickled elsewhere. Use
library classes or register the class in a shared module.

### Mistake 5: Ignoring Python-version compatibility
joblib/pickle files are generally loadable across minor versions but break
across majors. Pin the Python version in the env record.

### Mistake 6: Not testing the packaged artifact
You validated `pipe.predict` in the notebook — validate the *packaged*
artifact with a golden-output test before shipping.

## Best Practices

1. Package the whole preprocessing pipeline, never the bare model
2. Declare the input/output signature at packaging time
3. Ship the dependency environment with the artifact
4. Use pyfunc-style universal interfaces for serving portability
5. Use ONNX for edge/mobile/cross-language targets; pickle for Python-only
6. Test the packaged artifact (golden outputs) in CI, not just the training code
7. Treat the packaged model as immutable and content-addressed
8. Pin Python version + library versions in the env record
9. Keep the artifact small: quantize/compress where latency matters
10. Log the packaged artifact into the registry, not the raw weights only

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| joblib.dump a 200MB model | O(n) | O(n) | compress with `compress=3` |
| Load artifact at startup | O(n) | O(n) | lazy-load + LRU cache by sha256 |
| ONNX export | minutes (once) | O(n) | — |
| Signature validation | O(1) per call | O(1) | validate once at load |
| Golden-output test | O(n) | O(1) | sample 100 rows, not full data |

## AI Engineering Relevance

**Where this shows up:** every model that crosses the training → serving
boundary; every edge deployment; every CI promotion gate.

| Concept here | Used for |
|---|---|
| Whole-pipeline packaging | dev/prod prediction parity |
| Signature | schema check at the model boundary |
| Dependency env | reproduce the training env at serving |
| ONNX/pyfunc | one interface for every framework |

**Scale note:** a serving cluster reloading a 200MB model per pod per deploy is
wasteful — package once, hash, and have pods pull the shared artifact from a
content-addressed store. At 1M predictions/sec, the packaging decision (ONNX
vs Python) is the difference between 3ms and 25ms per call — 22ms × 1M = a lot
of latency budget.

## Practice Exercises

### Exercise 1: Package a Pipeline (Easy)
Fit a `Pipeline(scaler + LogisticRegression)` on synthetic data, `joblib.dump`
it, reload in a *fresh* process, and assert predictions match the in-memory fit.

### Exercise 2: Signature Validation (Medium)
Define an input schema (2 numeric, 1 categorical column); write
`validate_input(df) -> bool` that returns True only when the df has exactly the
declared columns/dtypes; assert it rejects a shuffled-column DataFrame.

### Exercise 3: Golden-Output Test (Hard)
Train a model, package it, then write `golden_test(artifact, samples)` that
predicts on a frozen 100-row sample, saves the outputs, and on re-run asserts
byte-identical outputs. Prove the artifact is deterministic and version-stable.

### Exercise 4: ONNX Round-Trip (Hard, optional)
Export a small model to ONNX, run it with `onnxruntime`, and assert the
probabilities match the original within 1e-4 — demonstrating the portability
contract.

## Summary

| Concept | Description |
|---|---|
| Packaging contract | schema + predict interface + env + artifact |
| Whole pipeline | preprocessor and model travel together |
| pyfunc | one `predict()` interface for every framework |
| Signature | schema validation at the model boundary |
| ONNX | portable, fast, framework-agnostic |

Packaging is where a model stops being research and becomes software. The
discipline of shipping the *whole* pipeline, with its schema and environment,
is what eliminates the entire class of "works in the notebook" failures.

## Quick Reference

| Task | Idiom |
|---|---|
| Package sklearn | `joblib.dump(pipeline, "m.pkl")` |
| Package PyTorch | `torch.save(model.state_dict(), "m.pt")` |
| Portable export | ONNX export → `onnxruntime.InferenceSession` |
| Universal wrapper | `mlflow.pyfunc.save_model(...)` |
| Declare schema | `ModelSignature(inputs=Schema([...]), outputs=...)` |

## Next Steps

Next: **[06 Docker for ML](06-docker-for-ml-lecture.md)** — containerizing the
packaged model and its environment into a deployable image.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://scikit-learn.org/stable/model_persistence.html,
https://onnxruntime.ai/, https://mlflow.org/docs/latest/python_api/mlflow.pyfunc.html
