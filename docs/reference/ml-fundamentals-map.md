# ML Fundamentals Map — the deferred track

> **Status: deliberately deferred.** Not part of weeks 0–10 of the
> [active track](../roadmap/active-track-10-week.md). Scheduled as a sprint at week 11+
> (milestone A10) into
> [`projects/00-core-foundations/python/07-machine-learning/`](../../projects/00-core-foundations/python/07-machine-learning/).
> Source: planning conversation 2026-07-31, decomposed 2026-08-02.

## Why this is deferred, and the risk

The active track targets an **applied LLM/GenAI engineer** role: RAG, agents, production
concerns. Those roles rarely ask you to derive backpropagation.

The risk is real and worth naming. "AI Engineer" covers at least five distinct jobs — from
wiring a RAG pipeline over a hosted API to training models on GPU clusters — with a pay spread
that can reach 3× at the same nominal level. Deferring this material closes the
research-adjacent end of that range until the sprint is done.

Two situations should pull this material forward:

1. Interviews you are actually getting ask about fundamentals.
2. Postings you actually want list PyTorch, fine-tuning, or model training.

---

## 1. Mathematics — as much as is needed, no more

| Area | What is actually used |
| --- | --- |
| Linear algebra | vectors, matrices, dot product, matrix multiplication, eigenvalues |
| Calculus | derivatives, gradients, chain rule — the basis of backpropagation |
| Probability & statistics | distributions, Bayes, expectation, variance |
| Optimization | gradient descent and variants (SGD, Adam, RMSprop) |

The goal is understanding *why* an algorithm behaves as it does, not the ability to prove
theorems. Free and well-scoped: *Mathematics for Machine Learning*
(mml-book.github.io).

---

## 2. Core concepts

### Learning types

- **Supervised** — classification, regression (labels available)
- **Unsupervised** — clustering, dimensionality reduction
- **Semi- and self-supervised** — the basis of modern LLM pretraining
- **Reinforcement learning** — agent, reward, policy; relevant if RLHF comes up

### Project lifecycle

EDA → preprocessing → feature engineering → model selection and training → evaluation →
deployment → monitoring.

The last two are where AI engineers spend most of their time and where most courses stop.

---

## 3. Data preprocessing

- Missing values and outliers
- Encoding: one-hot, label, target
- Scaling: normalization, standardization
- Imbalanced data: SMOTE, class weights
- Train/validation/test split — and why the boundaries must not blur
- **Data leakage** — the most common serious mistake in applied ML. Understand it properly;
  it is also a frequent interview question.

---

## 4. Classical algorithms

Understand when each applies; don't memorize derivations.

| Family | Members |
| --- | --- |
| Linear | linear regression, logistic regression |
| Trees | decision trees, random forests |
| Boosting | XGBoost, LightGBM, CatBoost — still dominant on tabular data in production |
| Margin | SVM |
| Clustering | K-means, DBSCAN |
| Dimensionality | PCA |
| Instance-based | KNN |

---

## 5. Evaluation

- Classification: accuracy, precision, recall, F1, ROC-AUC, confusion matrix
- Regression: MAE, MSE, RMSE, R²
- Cross-validation (k-fold)
- Bias–variance trade-off
- Overfitting vs. underfitting; regularization (L1, L2, dropout)
- Learning curves — and how to read a model's problem off one

---

## 6. Deep learning

### Concepts

Forward pass and backpropagation · activation functions (ReLU, sigmoid, softmax) and when each
applies · loss functions (cross-entropy, MSE) · optimizers (SGD, Adam) · batch size, learning
rate, epochs and their interaction · regularization (dropout, batch norm, weight decay).

### Architectures

| Type | Domain | Priority here |
| --- | --- | --- |
| CNN | images — convolution, pooling | low |
| RNN / LSTM | sequences | low — historical context |
| **Transformer** | everything current — self-attention, multi-head attention, positional encoding | **high** |
| Autoencoder, GAN | generative | general awareness |

---

## 7. NLP and LLM theory

The part of this document most likely to appear in an interview for the target role.

- Tokenization — BPE, WordPiece
- Word embeddings (Word2Vec, GloVe) → contextual embeddings (BERT-style)
- **Attention mechanism in detail** — the highest-value item on this page
- Pretraining vs. fine-tuning; transfer learning
- Fine-tuning techniques: full, LoRA, QLoRA, PEFT
- RLHF — conceptual understanding
- LLM evaluation: perplexity, BLEU, ROUGE, LLM-as-judge

---

## 8. MLOps

Where applied ML meets engineering, and where AI engineers are differentiated from data
scientists.

- Model versioning — MLflow, DVC
- Experiment tracking — Weights & Biases, MLflow
- Serving — FastAPI, TorchServe, Triton
- Containerization and orchestration — Docker, Kubernetes
- CI/CD for ML pipelines
- Monitoring — data drift, model drift, post-deployment degradation
- A/B testing models

---

## Sprint plan (week 11+, A10)

Time-boxed. The aim is working code and the ability to discuss it, not coverage.

| Day | Work | Artifact |
| --- | --- | --- |
| 1 | scikit-learn pipeline end-to-end on a real dataset: preprocess → train → cross-validate → evaluate | `07-machine-learning/01-sklearn-pipeline.py` |
| 2 | Deliberately induce data leakage, measure the inflated score, then fix it | `07-machine-learning/02-data-leakage.py` |
| 3 | One PyTorch training loop written by hand — no Lightning, no Trainer | `07-machine-learning/03-pytorch-loop.py` |
| 4 | Self-attention implemented from scratch on a toy sequence | `07-machine-learning/04-attention.py` |
| 5 | Compare a gradient-boosting model against a neural net on tabular data; write up why one wins | `docs/learning/deep-dives/tabular-vs-nn.md` |

**Done when** you can explain backpropagation, data leakage, and self-attention at a
whiteboard without notes.

---

## Sources for the sprint

| Topic | Source |
| --- | --- |
| ML fundamentals | Google ML Crash Course · *Hands-On Machine Learning* (Géron) |
| Deep learning | fast.ai · Karpathy "Neural Networks: Zero to Hero" |
| Transformers | *The Illustrated Transformer* (Alammar) · *NLP with Transformers* (HF team) |
| Mathematics | *Mathematics for Machine Learning* (free) |
| Production ML | *Designing Machine Learning Systems* (Huyen) |

The repo already contains `projects/04-ai-engineering/fastai-deep-learning/` with 13 modules
and quizzes — start there rather than from scratch.

---

## Related

- [ADR-0004](../decisions/0004-adopt-10-week-ai-engineer-track.md) — where this deferral is recorded
- [`books-and-sources.md`](books-and-sources.md)
- [`interview-bank.md`](interview-bank.md)

*Extracted 2026-08-02 from `docs/plan/archive/Python-essentials-for-AI-engineers.md`*
