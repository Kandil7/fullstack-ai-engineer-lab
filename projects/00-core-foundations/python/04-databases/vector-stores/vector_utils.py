"""
Vector-store teaching utilities (numpy only)
=============================================
Deterministic helpers for the 04-databases/vector-stores/ exercises:

- `embed_text`: hashed bag-of-words embedding, so any string maps to the
  same vector on every run (fixed seed, no model download).
- similarity metrics: cosine, L2, dot
- brute-force kNN with recall@k evaluation
- synthetic corpus with metadata (cluster, tenant, tags) for filtering
- RAG chunking strategies (fixed, sentence, recursive)
- BM25 sparse scoring + Reciprocal Rank Fusion for hybrid search

faiss is intentionally NOT required: every algorithm here is implemented in
plain numpy + the standard library so the exercises run anywhere. A `faiss`
cross-check is guarded by try/except in the exercises that mention it.
"""

from __future__ import annotations

import hashlib
import math
import random
import re
from collections import Counter

import numpy as np

_SEED: int = 42


def seed_all(seed: int = _SEED) -> None:
    """Seed both random and numpy for reproducibility."""
    global _SEED
    _SEED = seed
    random.seed(seed)
    np.random.seed(seed)


seed_all()


# ----------------------------------------------------------------------
# deterministic embedding
# ----------------------------------------------------------------------
def embed_text(text: str, dim: int = 16) -> np.ndarray:
    """Hash a string into a fixed-dimension L2-normalized vector.

    Each token contributes to `dim` slots via md5 of the token; the sign and
    magnitude are also md5-derived, so the mapping is stable across runs and
    processes. This stands in for a real embedding model (sentence-transformers,
    OpenAI text-embedding-*) whose vectors we cannot compute offline.
    """
    vec = np.zeros(dim, dtype=np.float64)
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    if not tokens:
        tokens = ["<empty>"]
    for token in tokens:
        h = hashlib.md5(token.encode("utf-8")).digest()
        idx = int.from_bytes(h[:4], "little") % dim
        sign = 1.0 if h[4] % 2 == 0 else -1.0
        mag = 0.5 + (int.from_bytes(h[5:7], "little") % 100) / 100.0
        vec[idx] += sign * mag
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
    return vec


def embed_texts(texts: list[str], dim: int = 16) -> np.ndarray:
    """Embed a list of strings into a (n, dim) matrix."""
    return np.vstack([embed_text(t, dim=dim) for t in texts])


# ----------------------------------------------------------------------
# similarity metrics
# ----------------------------------------------------------------------
def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity in [-1, 1]. Higher is more similar."""
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def dot_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Dot-product similarity (for normalized embeddings == cosine)."""
    return float(np.dot(a, b))


def l2_dist(a: np.ndarray, b: np.ndarray) -> float:
    """Euclidean distance. Lower is more similar."""
    return float(np.linalg.norm(a - b))


# ----------------------------------------------------------------------
# brute-force kNN
# ----------------------------------------------------------------------
def brute_force_knn(queries: np.ndarray, corpus: np.ndarray, k: int = 5,
                    metric: str = "cosine") -> np.ndarray:
    """Exact kNN by exhaustive scan: O(n_queries * n_corpus * d).

    Returns an (n_queries, k) int array of corpus indices, best first.
    This is the correctness baseline every ANN index is compared against.
    """
    if metric == "cosine":
        norms = np.linalg.norm(corpus, axis=1, keepdims=True)
        qnorms = np.linalg.norm(queries, axis=1, keepdims=True)
        scores = (queries @ corpus.T) / (qnorms * norms.T + 1e-12)
        order = np.argsort(-scores, axis=1)[:, :k]
    elif metric == "l2":
        dists = np.linalg.norm(queries[:, None, :] - corpus[None, :, :], axis=2)
        order = np.argsort(dists, axis=1)[:, :k]
    else:  # dot
        scores = queries @ corpus.T
        order = np.argsort(-scores, axis=1)[:, :k]
    return order.astype(np.int64)


def recall_at_k(predicted: np.ndarray, truth: np.ndarray, k: int = 5) -> float:
    """Fraction of true top-k items present in the predicted top-k."""
    hits = 0
    total = 0
    for p, t in zip(predicted, truth):
        pset = set(p.tolist())
        total += min(k, len(t))
        hits += sum(1 for i in t[:k] if i in pset)
    return hits / total if total else 0.0


# ----------------------------------------------------------------------
# synthetic corpus with metadata
# ----------------------------------------------------------------------
def make_corpus(n: int = 200, dim: int = 16, n_clusters: int = 6,
                seed: int = _SEED) -> tuple[np.ndarray, list[dict]]:
    """Build a clustered synthetic corpus: (vectors, metadata list).

    Each metadata dict has: id, cluster (0..n_clusters-1), tenant (a/b),
    tags (subset of {'ml','db','web','ops'}), and a sample 'text'.
    Vectors within a cluster are near each other — the ground truth a
    vector store is expected to recover. Tag membership depends on
    i % 3 AND i // 6, tenant on (i // 2) % 2 — both vary WITHIN every
    cluster (filters aligned with clusters would be degenerate:
    all-or-nothing per cluster).
    """
    seed_all(seed)
    rng = np.random.default_rng(seed)
    centroids = rng.normal(size=(n_clusters, dim))
    centroids /= np.linalg.norm(centroids, axis=1, keepdims=True)
    vectors = np.zeros((n, dim))
    meta: list[dict] = []
    topic_texts = {
        0: "vector search retrieval reranking",
        1: "cache hit ratio latency throughput",
        2: "document schema index collection",
        3: "training loss gradient epoch batch",
        4: "deploy rollout canary rollback",
        5: "token budget prompt context window",
        6: "session auth token cookie expiry",
        7: "metric alert dashboard monitor",
    }
    for i in range(n):
        cluster = i % n_clusters
        v = centroids[cluster] + rng.normal(scale=0.18, size=dim)
        vectors[i] = v / np.linalg.norm(v)
        meta.append({
            "id": i,
            "cluster": cluster,
            "tenant": "a" if (i // 2) % 2 == 0 else "b",
            "tags": [t for t in ["ml", "db", "web", "ops"]
                     if (i % 3 + i // 6 + len(t)) % 3 == 0],
            "text": f"{topic_texts[cluster]} sample {i:03d}",
        })
    return vectors, meta


# ----------------------------------------------------------------------
# RAG chunking strategies
# ----------------------------------------------------------------------
def chunk_fixed(text: str, chunk_size: int = 40, overlap: int = 8) -> list[str]:
    """Fixed-size sliding-window chunks with overlap."""
    chunks: list[str] = []
    start = 0
    step = max(1, chunk_size - overlap)
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += step
    return chunks


def chunk_by_sentences(text: str, max_chars: int = 200) -> list[str]:
    """Sentence-boundary chunking: never split mid-sentence, merge while
    under max_chars, drop empty chunks."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks: list[str] = []
    current = ""
    for sent in sentences:
        if not sent:
            continue
        if current and len(current) + len(sent) + 1 > max_chars:
            chunks.append(current)
            current = sent
        else:
            current = f"{current} {sent}".strip() if current else sent
    if current:
        chunks.append(current)
    return chunks


def chunk_recursive(text: str, max_chars: int = 100,
                    separators: list[str] | None = None) -> list[str]:
    """Recursive character splitting: try the largest separator first,
    then smaller ones, until every piece fits under max_chars."""
    if separators is None:
        separators = ["\n\n", "\n", ". ", " "]
    if len(text) <= max_chars:
        return [text] if text.strip() else []
    for sep in separators:
        parts = text.split(sep)
        if len(parts) > 1:
            out: list[str] = []
            for p in parts:
                out.extend(chunk_recursive(p, max_chars, separators[separators.index(sep) + 1:]))
            return [c for c in out if c.strip()]
    # no separator helped — hard cut
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]


# ----------------------------------------------------------------------
# sparse retrieval (BM25-style) for hybrid search
# ----------------------------------------------------------------------
def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def bm25_scores(query: str, docs: list[str],
                k1: float = 1.2, b: float = 0.75) -> np.ndarray:
    """BM25-ish ranking of docs against a query. Higher = more relevant.

    Idle simplicity: idf from document frequency, tf with k1/b saturation.
    This is the 'sparse' arm of hybrid search (dense = embeddings).
    """
    q_tokens = tokenize(query)
    n = len(docs)
    doc_tokens = [tokenize(d) for d in docs]
    df: Counter[str] = Counter()
    for toks in doc_tokens:
        for t in set(toks):
            df[t] += 1
    avg_len = sum(len(t) for t in doc_tokens) / max(1, n)
    scores = np.zeros(n)
    for t in q_tokens:
        if df[t] == 0:
            continue
        idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
        for i, toks in enumerate(doc_tokens):
            tf = toks.count(t)
            if tf == 0:
                continue
            denom = tf + k1 * (1 - b + b * len(toks) / max(1.0, avg_len))
            scores[i] += idf * tf * (k1 + 1) / denom
    return scores


def rrf_fusion(rankings: list[list[int]], k: int = 60) -> list[int]:
    """Reciprocal Rank Fusion: combine several rankings into one.

    score(doc) = sum over rankers of 1 / (k + rank). k=60 is the standard
    constant from the original paper (Cormack et al., 2009).
    """
    scores: dict[int, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    return [doc_id for doc_id, _ in
            sorted(scores.items(), key=lambda kv: kv[1], reverse=True)]


# ----------------------------------------------------------------------
# ANN primitives used by multiple exercises
# ----------------------------------------------------------------------
def quantize_binary(vectors: np.ndarray) -> np.ndarray:
    """Binary quantization: +1 -> 1, -1 -> 0. 32x smaller, ~5-10% recall loss."""
    return (vectors > 0).astype(np.uint8)


def hamming_distance(x: np.ndarray, y: np.ndarray) -> int:
    return int(np.count_nonzero(x != y))


def asymmetric_distance(query_vec: np.ndarray, bq_corpus: np.ndarray) -> np.ndarray:
    """ADC-style approximate distance: query full-precision, corpus binarized."""
    bits = (bq_corpus.astype(np.int8) * 2 - 1)
    return np.asarray(-(query_vec @ bits.T) / bq_corpus.shape[1], dtype=np.float64)
