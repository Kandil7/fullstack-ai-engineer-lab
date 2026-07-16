"""
Practice Problems — Module 03: Vector Embeddings (NO SOLUTIONS)
================================================================
Solve these yourself! No hints, no solutions.

Run: python 03-vector-embeddings-practice.py
Select a problem number to see the description.

Categories:
  EASY (20 XP):   Problems 1-5
  MEDIUM (50 XP): Problems 6-10
  HARD (100 XP):  Problems 11-15

Prerequisites:
    pip install openai sentence-transformers numpy python-dotenv
"""

import numpy as np


# ============================================================
# EASY PROBLEMS (20 XP)
# ============================================================

# Problem 1: Cosine Similarity
# Write a function that computes the cosine similarity between two vectors.
# cosine_sim(a, b) = (a · b) / (||a|| * ||b||)
# Handle the edge case where either vector has zero magnitude (return 0.0).
def problem_01():
    pass  # Write your code here


# Problem 2: Dot Product Similarity
# Write a function that computes the dot product of two vectors.
# This is the simplest similarity metric. Return the scalar value.
def problem_02():
    pass  # Write your code here


# Problem 3: Euclidean Distance
# Write a function that computes the Euclidean distance between two vectors.
# distance(a, b) = sqrt(sum((a_i - b_i)^2))
# Return a non-negative float.
def problem_03():
    pass  # Write your code here


# Problem 4: Vector Normalizer
# Write a function that normalizes a vector to unit length (L2 norm).
# normalized = v / ||v||
# Handle zero vectors by returning the zero vector unchanged.
def problem_04():
    pass  # Write your code here


# Problem 5: Similarity Ranker
# Write a function that takes a query vector and a list of document vectors,
# computes cosine similarity for each, and returns the indices sorted by
# similarity (highest first). Return a list of (index, score) tuples.
def problem_05():
    pass  # Write your code here


# ============================================================
# MEDIUM PROBLEMS (50 XP)
# ============================================================

# Problem 6: Embedding Cache
# Build an EmbeddingCache class that:
# - Stores embeddings in memory (dict)
# - Uses a hash of the input text as the key
# - Has get(text) → vector or None
# - Has set(text, vector) to store
# - Has a size() method
# - Has a clear() method
# - Supports hit rate tracking (hits vs misses)
class EmbeddingCache:
    def __init__(self):
        pass  # Write your code here

    def get(self, text: str):
        pass  # Write your code here

    def set(self, text: str, embedding: list[float]):
        pass  # Write your code here

    def size(self) -> int:
        pass  # Write your code here

    def clear(self):
        pass  # Write your code here

    def hit_rate(self) -> float:
        pass  # Write your code here


# Problem 7: Batch Embedder with Rate Limiting
# Write a function that embeds a list of texts using OpenAI's API,
# but respects rate limits:
# - Process in batches of 20
# - Wait 1 second between batches
# - Return all embeddings in order
# - Track total API calls made
def problem_07():
    pass  # Write your code here


# Problem 8: Semantic Search Engine
# Build a SemanticSearch class that:
# - Stores documents with their embeddings
# - Has an add(text, embedding) method
# - Has a search(query_embedding, k=5) → top-k results
# - Returns results with text, score, and rank
# - Supports filtering by metadata (e.g., source="wiki")
class SemanticSearch:
    def __init__(self):
        pass  # Write your code here

    def add(self, text: str, embedding: list[float], metadata: dict = None):
        pass  # Write your code here

    def search(self, query_embedding: list[float], k: int = 5, filters: dict = None):
        pass  # Write your code here


# Problem 9: Dimensionality Reducer
# Write a function that reduces embedding dimensions using PCA.
# 1. Take a matrix of embeddings (N x D)
# 2. Compute the top-K principal components
# 3. Project embeddings onto those components
# 4. Return the reduced embeddings (N x K)
# Do NOT use sklearn — implement PCA from scratch using numpy.
def problem_09():
    pass  # Write your code here


# Problem 10: Similarity Threshold Filter
# Write a function that takes a query embedding and document embeddings,
# computes similarities, and returns only documents above a threshold.
# Also implement "diversity" mode: after selecting the top document,
# exclude documents too similar to already-selected ones (MMR algorithm).
def problem_10():
    pass  # Write your code here


# ============================================================
# HARD PROBLEMS (100 XP)
# ============================================================

# Problem 11: Embedding Quality Evaluator
# Write a function that evaluates embedding quality:
# 1. Take a set of (text, expected_cluster) pairs
# 2. Generate embeddings for all texts
# 3. Compute intra-cluster similarity (avg similarity within same cluster)
# 4. Compute inter-cluster similarity (avg similarity across different clusters)
# 5. Return a quality score: intra / inter (higher is better)
def problem_11():
    pass  # Write your code here


# Problem 12: Hybrid Search Engine
# Build a HybridSearch class that combines:
# - Semantic search (cosine similarity on embeddings)
# - Keyword search (BM25-style term matching)
# - Weighted fusion: score = α * semantic_score + (1-α) * keyword_score
# - Support for tuning α (alpha) parameter
# - Index that supports add and search
class HybridSearch:
    def __init__(self, alpha: float = 0.7):
        pass  # Write your code here

    def add(self, text: str, embedding: list[float]):
        pass  # Write your code here

    def search(self, query: str, query_embedding: list[float], k: int = 5):
        pass  # Write your code here


# Problem 13: Hierarchical Navigable Small World (HNSW)
# Implement a simplified HNSW index:
# - Build a graph where nodes are embeddings
# - Each node connects to its M nearest neighbors
# - Search starts at a random entry point
# - Greedy search navigates to closer neighbors
# - Return top-k nearest embeddings
# Use numpy for distance calculations. M=10, ef_search=10.
def problem_13():
    pass  # Write your code here


# Problem 14: Embedding Interpolation
# Write a function that "interpolates" between two embeddings:
# - Takes two embeddings and a weight (0.0 to 1.0)
# - Returns the weighted average: result = w * a + (1-w) * b
# - Also write a "midpoint" function that finds the embedding
#   exactly between two others
# - Test: verify midpoint is equidistant from both inputs
def problem_14():
    pass  # Write your code here


# Problem 15: Streaming Vector Store
# Build a VectorStore class that:
# - Supports add, search, delete, and update operations
# - Uses an in-memory numpy array for the vectors
# - Supports batch operations (add_many, search_many)
# - Has persistence (save_to_disk, load_from_disk) using JSON
# - Tracks insertions and deletions (tombstones)
# - Has a compaction method that rebuilds the index
class VectorStore:
    def __init__(self, dimension: int = 1536):
        pass  # Write your code here

    def add(self, id: str, vector: list[float], metadata: dict = None):
        pass  # Write your code here

    def search(self, query: list[float], k: int = 5):
        pass  # Write your code here

    def delete(self, id: str):
        pass  # Write your code here

    def update(self, id: str, vector: list[float], metadata: dict = None):
        pass  # Write your code here

    def add_many(self, items: list[dict]):
        pass  # Write your code here

    def save_to_disk(self, path: str):
        pass  # Write your code here

    def load_from_disk(self, path: str):
        pass  # Write your code here

    def compact(self):
        pass  # Write your code here


# ============================================================
# MAIN — Run to see problem descriptions
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Module 03: Vector Embeddings — Practice Problems")
    print("=" * 60)
    print()

    problems = {
        1: ("Cosine Similarity", "Easy", 20),
        2: ("Dot Product Similarity", "Easy", 20),
        3: ("Euclidean Distance", "Easy", 20),
        4: ("Vector Normalizer", "Easy", 20),
        5: ("Similarity Ranker", "Easy", 20),
        6: ("Embedding Cache", "Medium", 50),
        7: ("Batch Embedder with Rate Limiting", "Medium", 50),
        8: ("Semantic Search Engine", "Medium", 50),
        9: ("Dimensionality Reducer (PCA)", "Medium", 50),
        10: ("Similarity Threshold Filter (MMR)", "Medium", 50),
        11: ("Embedding Quality Evaluator", "Hard", 100),
        12: ("Hybrid Search Engine", "Hard", 100),
        13: ("HNSW Index", "Hard", 100),
        14: ("Embedding Interpolation", "Hard", 100),
        15: ("Streaming Vector Store", "Hard", 100),
    }

    total_xp = sum(p[2] for p in problems.values())
    print(f"Total Problems: {len(problems)}")
    print(f"Total XP: {total_xp}")
    print()

    for num, (name, diff, xp) in problems.items():
        print(f"  [{num:2d}] {name:<45} {diff:<8} +{xp} XP")

    print()
    print("Select a problem number to see its full description.")
    print("Solve each function by replacing 'pass' with your implementation.")
    print("No solutions are provided — figure it out yourself!")
    print("=" * 60)
