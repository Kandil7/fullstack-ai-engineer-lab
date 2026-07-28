# Phases 7–9 — ML, MLOps, and GenAI

> **Phase 7 current:** 23 exercises, 23 lectures. **23/23 pass ✅** — clean, but
> shallow relative to the target role.
> **Phases 8 and 9 do not exist.** They are planned in `EXPANSION_PLAN.md` and
> never built.
>
> These three phases are what make the title "AI Engineer" true. Measured
> repo-wide: `torch` **0** files (though PyTorch **is installed**), `openai` **0**,
> `anthropic` **0**, `mlflow` **0**, `drift` **0**, `onnx` **0**, `quantiz` **0**.

---

## PART A — Phase 7: Machine Learning (`07-machine-learning/`)

### A.1 Current state

All 23 files pass. Coverage is the classical sklearn surface:

| Range | Topics |
|---|---|
01–04 | Getting started, data mining, datasets, cleaning |
05–08 | Linear, polynomial, R², multiple regression |
09–10 | Scaling, train/test split |
11–13 | Decision tree, confusion matrix, correlation |
14–15 | Regression example, logistic regression |
16–18 | K-means, hierarchical clustering, PCA |
19–23 | Naive Bayes, random forest, SVM, cross-validation, KNN |

**Strength:** the algorithm inventory is reasonable and everything runs.
**Weakness:** it teaches `model.fit(X, y)` without teaching *why the number is
wrong* — the actual work of an ML engineer.

### A.2 Gaps

| Gap | Consequence |
|---|---|
No leakage discussion | The most common and most expensive ML bug ships undetected |
No gradient boosting | XGBoost/LightGBM win most tabular problems; absent |
No pipelines | `Pipeline`/`ColumnTransformer` absent → leakage becomes near-inevitable |
No proper validation strategy | `train_test_split` only; no stratification, grouping, or time-series CV |
Metrics shallow | Accuracy-centric; no PR-AUC, calibration, or threshold selection |
No imbalanced handling | Real-world classification is imbalanced |
No feature engineering topic | The highest-leverage activity in tabular ML |
No explainability | SHAP/permutation importance absent |
No deep learning | `torch` installed, used in 0 files |
No experiment tracking | Nothing on reproducibility |

### A.3 New topics 24–40

**Rigor and correctness (24–29)**

| # | Topic | Concepts |
|---|---|---|
24 | `24-sklearn-pipelines.py` ⭐ | `Pipeline`, `ColumnTransformer`, `FeatureUnion`; fit on train only; custom transformers; **pipelines as leakage prevention** |
25 | `25-data-leakage.py` ⭐ | Target leakage; train-test contamination; scaling before split; temporal leakage; group leakage; duplicate rows across splits; **a worked example where accuracy goes 0.99 → 0.71 once fixed** |
26 | `26-validation-strategies.py` | K-fold, stratified, group, `TimeSeriesSplit`; nested CV for tuning; train/val/test discipline; **when CV lies** |
27 | `27-metrics-deep.py` | Precision/recall tradeoff; ROC-AUC vs PR-AUC (**and when ROC misleads on imbalance**); F-beta; log loss; **threshold selection as a business decision**; regression metrics; multi-class averaging |
28 | `28-calibration.py` | Probability calibration; Platt scaling; isotonic regression; reliability diagrams; **why an uncalibrated model breaks downstream decisions** |
29 | `29-imbalanced-learning.py` | Class weights; resampling (SMOTE/ADASYN); threshold moving; **why accuracy is useless at 1% positive**; evaluation under imbalance |

**Modeling depth (30–35)**

| # | Topic | Concepts |
|---|---|---|
30 | `30-gradient-boosting.py` ⭐ | XGBoost/LightGBM/CatBoost; boosting intuition; key hyperparameters; early stopping; categorical handling; **why GBDTs beat neural nets on tabular data** |
31 | `31-feature-engineering.py` | Numeric transforms; encoding (one-hot, ordinal, target, hashing); interactions; binning; date features; text features; **fit encoders on train only** |
32 | `32-feature-selection.py` | Filter/wrapper/embedded; RFE; `SelectFromModel`; multicollinearity and VIF; permutation importance; stability |
33 | `33-hyperparameter-tuning.py` | Grid vs random vs Bayesian; Optuna; pruning; search-space design; **tuning inside CV, not outside** |
34 | `34-ensembling.py` | Voting, stacking, blending; out-of-fold predictions; diversity; when ensembling is not worth the complexity |
35 | `35-explainability.py` | Permutation importance; SHAP (values, plots, interpretation); LIME; partial dependence; global vs local; **the limits of explanations** |

**Deep learning (36–40)** — PyTorch is installed and unused

| # | Topic | Concepts |
|---|---|---|
36 | `36-pytorch-tensors.py` | Tensors; dtypes; devices; autograd and the computation graph; `no_grad`; **broadcasting shared with NumPy** |
37 | `37-pytorch-training-loop.py` | `nn.Module`; `Dataset`/`DataLoader`; loss, optimizer, scheduler; the canonical loop; overfitting a single batch as a **debugging first step** |
38 | `38-neural-network-basics.py` | Layers, activations, initialization; backprop intuition; vanishing/exploding gradients; regularization; batch norm and dropout |
39 | `39-transfer-learning.py` | Pretrained models; freezing vs fine-tuning; feature extraction; learning-rate schedules; small-data strategy |
40 | `40-transformers-from-scratch.py` ⭐ | Attention mechanism implemented directly; Q/K/V; multi-head; positional encoding; the block; why attention scales quadratically; **the foundation for everything in Phase 9** |

---

## PART B — Phase 8: MLOps (`08-mlops/`) — NEW

Measured: `mlflow` 0, `Dockerfile` 0, `drift` 0, `feature store` 0, `onnx` 0.
None of this exists.

| # | Topic | Concepts |
|---|---|---|
01 | `01-reproducibility.py` | Seeds everywhere; deterministic ops; environment capture; data versioning; **why "it worked on my machine" is a production incident** |
02 | `02-experiment-tracking.py` | MLflow tracking; params/metrics/artifacts; run comparison; nested runs; W&B alternative; what to log and what not to |
03 | `03-data-versioning.py` | DVC; content-addressed storage; dataset lineage; large-file handling; linking data version to model version |
04 | `04-model-registry.py` | MLflow Model Registry; stages; versioning; signatures; promotion gates; rollback |
05 | `05-model-packaging.py` | Serialization formats; `pickle` risks; ONNX export; TorchScript; environment pinning; **model artifacts as supply-chain risk** |
06 | `06-docker-for-ml.py` | Multi-stage builds; CUDA base images; layer caching for large deps; image size; GPU passthrough; reproducible builds |
07 | `07-model-serving.py` | FastAPI serving; load-at-startup; **dynamic batching**; async inference; concurrency vs memory; latency budget |
08 | `08-inference-optimization.py` | Quantization (int8, fp16); pruning; distillation; ONNX Runtime; batching tradeoffs; **measured latency/accuracy curve** |
09 | `09-pipeline-orchestration.py` | Prefect/Airflow; DAGs; retries; scheduling; backfills; idempotent tasks; failure handling |
10 | `10-data-validation.py` | Pandera/Great Expectations; schema contracts; distribution checks; **fail the pipeline, not the model** |
11 | `11-monitoring-and-drift.py` ⭐ | Data drift vs concept drift; PSI, KS test; embedding drift; performance monitoring with delayed labels; alerting thresholds; Evidently |
12 | `12-ci-cd-for-ml.py` | Testing ML code; testing *models* (behavioral tests); training in CI; model approval gates; deployment automation |
13 | `13-feature-stores.py` | Offline vs online; **point-in-time correctness** (training/serving skew); Feast; when a feature store is overkill |
14 | `14-ab-testing-models.py` | Shadow, canary, A/B; traffic splitting; statistical significance; guardrail metrics; **when to stop an experiment** |
15 | `15-cost-optimization.py` | GPU vs CPU economics; spot instances; autoscaling to zero; batch vs real-time; caching; **cost per 1k predictions** |
16 | `16-case-study-e2e.py` | End to end: validate → train → track → register → serve → monitor → retrain |

---

## PART C — Phase 9: GenAI / LLM Engineering (`09-genai/`) — NEW

Measured: `openai` 0, `anthropic` 0, `prompt` 4 (incidental), `embedding` 1.
This is the phase most directly tied to the stated goal, and it is entirely absent.

### C.1 Foundations (01–05)

| # | Topic | Concepts |
|---|---|---|
01 | `01-llm-fundamentals.py` | Tokenization (BPE) and why token ≠ word; context windows; autoregressive generation; temperature/top-p/top-k; **why the same prompt gives different answers**; cost per token |
02 | `02-api-clients.py` | Anthropic and OpenAI SDKs; messages format; system prompts; streaming; **retries on 429/503 with backoff**; timeouts; token counting before sending |
03 | `03-structured-output.py` ⭐ | JSON mode; tool/function calling as structured extraction; Pydantic schema validation; **retry-on-invalid loops**; when to use a grammar |
04 | `04-prompt-engineering.py` | Zero/few-shot; chain of thought; role and format control; delimiters; **prompt versioning as code**; systematic iteration over guesswork |
05 | `05-prompt-evaluation.py` | Golden datasets; regression tests for prompts; LLM-as-judge and its biases; pairwise comparison; **the eval loop before optimizing** |

### C.2 RAG (06–12) — the core competency

| # | Topic | Concepts |
|---|---|---|
06 | `06-embeddings.py` | Embedding models; dimensionality; normalization; cosine similarity; batching; **caching embeddings**; model selection and the cost of migrating |
07 | `07-chunking-strategies.py` ⭐ | Fixed, recursive, semantic, structural chunking; overlap; **chunk size vs retrieval quality, measured**; metadata attachment; table and code handling |
08 | `08-document-processing.py` | PDF/HTML/Markdown extraction; layout preservation; tables; OCR; cleaning; **garbage in, garbage retrieved** |
09 | `09-rag-baseline.py` | The minimal correct pipeline: ingest → chunk → embed → store → retrieve → generate; citations; **build the baseline before optimizing** |
10 | `10-retrieval-quality.py` ⭐ | Recall@k, MRR, NDCG; building a labeled eval set; failure analysis; **retrieval quality dominates generation quality** |
11 | `11-advanced-retrieval.py` | Hybrid dense+sparse; RRF; query expansion; HyDE; multi-query; parent-document; small-to-big; **measured lift per technique** |
12 | `12-reranking.py` | Cross-encoders; latency vs quality; two-stage retrieval; k tuning; cost per query |

### C.3 Agents and tools (13–16)

| # | Topic | Concepts |
|---|---|---|
13 | `13-tool-calling.py` | Tool schemas from type hints; execution loop; parallel tools; error handling; **validating model-chosen arguments** |
14 | `14-agent-patterns.py` | ReAct; plan-and-execute; reflection; **loop limits and budget caps**; state management; when an agent is the wrong architecture |
15 | `15-multi-agent.py` | Orchestrator/worker; handoffs; shared state; LangGraph-style state machines; cost multiplication risk |
16 | `16-memory-and-context.py` | Conversation history management; summarization; context-window budgeting; **retrieval as memory**; sliding windows |

### C.4 Production (17–22)

| # | Topic | Concepts |
|---|---|---|
17 | `17-llm-observability.py` ⭐ | Tracing a request through retrieval and generation; token/cost/latency per call; prompt and response logging with PII care; Langfuse/Phoenix |
18 | `18-caching-and-cost.py` | Exact and semantic caching; prompt caching; batching; **model routing by task difficulty**; cost per conversation; measured savings |
19 | `19-guardrails-and-safety.py` | **Prompt injection** — the defining security problem; input/output validation; PII detection; refusal handling; jailbreak resistance; content filtering |
20 | `20-evaluation-frameworks.py` | RAGAS metrics (faithfulness, relevance); custom evaluators; regression suites in CI; human review loops; **shipping without eval is guessing** |
21 | `21-fine-tuning.py` | When fine-tuning beats prompting (and when it does not); LoRA/QLoRA; dataset prep (**JSONL**); SFT vs DPO; evaluation; serving adapters |
22 | `22-local-models.py` | Ollama/llama.cpp; quantized GGUF; VRAM math; throughput vs quality; **when local beats API** on cost and privacy |

### C.5 Capstones (23–25)

| # | Topic |
|---|---|
23 | `23-case-study-rag-service.py` — production RAG API with citations, hybrid retrieval, caching, eval, observability |
24 | `24-case-study-agent.py` — tool-using agent with budget caps, retries, tracing |
25 | `25-case-study-extraction.py` — high-volume structured extraction with validation and cost controls |

---

## PART D — Standards for These Phases

### D.1 Determinism without network access

The hardest constraint: LLM and ML content must be CI-verifiable offline.

```python
# Tier 1 — pure logic: always test for real
def _verify() -> None:
    chunks = chunk_text("a" * 1000, size=300, overlap=50)
    assert all(len(c) <= 300 for c in chunks), "no chunk may exceed size"
    assert len(chunks) == 4, "1000 chars at 300/50 overlap → 4 chunks"
    # reconstruct-ability: overlap must not lose content
    assert "".join(c[:250] for c in chunks).startswith("a" * 250)

# Tier 2 — API calls: mock by default, live only when a key is present
def _verify_llm() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("[skip] no API key — set ANTHROPIC_API_KEY for live checks")
        return
    ...
```

**Rules**
- Chunking, prompt templating, token counting, schema validation, retry logic,
  cost calculation, and RAG scoring are **pure functions** — always tested
- Live API calls are opt-in via env var, never required for CI
- ML training uses tiny synthetic datasets with fixed seeds; assert on shapes,
  monotonic loss decrease, and pipeline correctness — **never on exact accuracy**
- Assert *leakage prevention* structurally: that the scaler saw only training rows

### D.2 Model and provider guidance

Use current models. Per the repo's existing conventions, prefer the latest Claude
models for examples (`claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5-20251001`),
and show provider-agnostic abstractions so a learner can swap backends. Route by
task difficulty in `18-caching-and-cost.py`.

### D.3 Cost transparency

Every GenAI topic states its cost model: tokens in/out, cache-hit rate, cost per
1k requests. This is the discipline the role requires and it is absent from most
tutorials.

---

## E — Deliverables

| Item | Count |
|---|---|
Phase 7 new topics `24`–`40` | 17 |
Phase 7 `_verify()` retrofits | 23 |
Phase 8 `08-mlops/` | 16 |
Phase 9 `09-genai/` | 25 |
New lecture+glossary pairs | 116 |
Challenges | 58 dirs |
Quizzes | ~18 |
Interview guides | ~10 |

---

## F — Sequencing

| Step | Work | Depends on |
|---|---|---|
| 1 | Phase 7 `_verify()` retrofits (23) | Tier 0 |
| 2 | **`24-sklearn-pipelines` + `25-data-leakage`** | step 1 — highest value in Phase 7 |
| 3 | `26`–`29` (validation, metrics, calibration, imbalance) | step 2 |
| 4 | `30`–`35` (GBDT, features, tuning, explainability) | step 3 |
| 5 | `36`–`40` (PyTorch → transformers) | Phase 3 NumPy `29`–`34` |
| 6 | Phase 8 `01`–`08` (reproducibility → inference opt) | step 4; Phase 5 Docker |
| 7 | Phase 8 `09`–`16` (orchestration → e2e) | step 6 |
| 8 | Phase 9 `01`–`05` (foundations) | step 5 (`40-transformers`) |
| 9 | Phase 9 `06`–`12` (RAG) | Phase 4 vector-stores; step 8 |
| 10 | Phase 9 `13`–`16` (agents) | step 9 |
| 11 | Phase 9 `17`–`22` (production) | Phase 5 observability; step 10 |
| 12 | Phase 9 `23`–`25` (capstones) | step 11 |

**Critical path to the goal:** Phase 3 NumPy → Phase 7 `40-transformers` →
Phase 9 foundations → Phase 4 vector stores → Phase 9 RAG. This chain is what
turns the curriculum into AI-engineer training.

---

## G — Exit Criteria

**Phase 7**
- [ ] 40 topics, all passing `_verify()`
- [ ] Leakage taught with a worked before/after example
- [ ] Pipelines used throughout, not bare `fit`
- [ ] Metrics beyond accuracy; calibration and thresholds covered
- [ ] Gradient boosting present
- [ ] PyTorch used (from 0 files) through attention implemented from scratch

**Phase 8**
- [ ] 16 topics; a model goes train → register → serve → monitor
- [ ] Experiment tracking, data versioning, drift detection working
- [ ] Docker image builds and serves
- [ ] Cost per 1k predictions computed

**Phase 9**
- [ ] 25 topics; a complete RAG service with citations and eval
- [ ] Retrieval quality measured (recall@k, NDCG), not assumed
- [ ] Structured output with validation and retry
- [ ] Prompt injection defenses covered
- [ ] Observability: tokens, cost, latency traced per request
- [ ] All pure logic CI-tested offline; live calls opt-in

---

*Phases 7–9 of [00-MASTER-PLAN.md](00-MASTER-PLAN.md). Depends on Phase 3 (NumPy), Phase 4 (vector stores), Phase 5 (serving, observability).*
