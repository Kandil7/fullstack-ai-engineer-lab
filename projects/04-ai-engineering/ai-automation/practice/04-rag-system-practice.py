"""
Practice Problems — Module 04: RAG Systems (NO SOLUTIONS)
==========================================================
Solve these yourself! No hints, no solutions.

Run: python 04-rag-system-practice.py
Select a problem number to see the description.

Categories:
  EASY (20 XP):   Problems 1-5
  MEDIUM (50 XP): Problems 6-10
  HARD (100 XP):  Problems 11-15

Prerequisites:
    pip install openai numpy python-dotenv
"""

from dataclasses import dataclass, field
from typing import Any


# ============================================================
# EASY PROBLEMS (20 XP)
# ============================================================

# Problem 1: Fixed-Size Chunker
# Write a function that splits text into chunks of a fixed character size.
# - chunk_text(text, chunk_size=500) → list of strings
# - Each chunk should be approximately chunk_size characters
# - The last chunk may be shorter
# - Split at the nearest word boundary (space) to avoid cutting words
def problem_01():
    pass  # Write your code here


# Problem 2: Sentence Chunker
# Write a function that splits text into chunks by sentence boundaries.
# - Use regex to split on sentence-ending punctuation (. ! ?)
# - Merge sentences into chunks up to a max_characters limit
# - Preserve the original sentence punctuation
def problem_02():
    pass  # Write your code here


# Problem 3: Document Loader
# Write a function that loads a text file and returns a list of dicts:
# [{"content": str, "source": str, "line_start": int, "line_end": int}]
# Support loading .txt and .md files.
# For .md files, split by ## headings as separate documents.
def problem_03():
    pass  # Write your code here


# Problem 4: Metadata Extractor
# Write a function that extracts metadata from a text chunk:
# - word_count: number of words
# - char_count: number of characters
# - has_code: True if the chunk contains code (backticks or common keywords)
# - language: detect if it's English, Spanish, or code
# Return a metadata dict.
def problem_04():
    pass  # Write your code here


# Problem 5: Query Preprocessor
# Write a function that preprocesses a search query:
# - Lowercase
# - Remove stop words (the, a, an, is, are, was, were, in, on, at, to, for, of)
# - Remove special characters
# - Collapse multiple spaces
# Return the cleaned query string.
def problem_05():
    pass  # Write your code here


# ============================================================
# MEDIUM PROBLEMS (50 XP)
# ============================================================

# Problem 6: Recursive Text Splitter
# Write a recursive chunking function that:
# 1. Tries to split by paragraphs first (\n\n)
# 2. If a paragraph is too long, split by sentences
# 3. If a sentence is too long, split by words
# 4. Merges small pieces up to chunk_size
# This is the strategy LangChain uses.
def problem_06():
    pass  # Write your code here


# Problem 7: Chunk Deduplicator
# Write a function that deduplicates chunks:
# - Compute a content hash (SHA-256) for each chunk
# - Remove exact duplicates
# - Also remove near-duplicates (cosine similarity > 0.95)
# - Return deduplicated chunks and the number removed
def problem_07():
    pass  # Write your code here


# Problem 8: Context Window Manager
# Write a function that fits retrieved chunks into an LLM context window:
# - Takes a list of scored chunks and a max_token_limit
# - Estimates tokens (1 token ≈ 4 chars)
# - Adds chunks in score order until the limit is reached
# - Returns the selected chunks and total tokens used
# - Always includes the top-1 chunk even if it exceeds the limit
def problem_08():
    pass  # Write your code here


# Problem 9: RAG Prompt Builder
# Write a function that constructs a RAG prompt:
# - Takes a user query and a list of context chunks
# - Builds a prompt with clear instructions: "Answer based ONLY on the context"
# - Includes source references [1], [2], etc.
# - If no context is relevant, says "I don't have information about that"
# - Returns the formatted prompt string
def problem_09():
    pass  # Write your code here


# Problem 10: Retrieval Scorer
# Write a function that scores retrieval quality:
# - Takes a query, retrieved documents, and ground-truth relevant docs
# - Computes: precision@5, recall@5, MRR, and a combined score
# - The combined score = 0.3*precision + 0.3*recall + 0.4*MRR
# - Returns a dict with all metrics
def problem_10():
    pass  # Write your code here


# ============================================================
# HARD PROBLEMS (100 XP)
# ============================================================

# Problem 11: Reranker
# Write a Reranker class that:
# - Takes initial retrieval results (from vector search)
# - Uses cross-attention scoring (simulate with a simple scoring function)
# - Considers query-document relevance AND document diversity
# - Implements MMR (Maximal Marginal Relevance) for diversity
# - Returns reranked results
class Reranker:
    def __init__(self, lambda_param: float = 0.5):
        pass  # Write your code here

    def rerank(self, query: str, documents: list[str],
               embeddings: list[list[float]], top_k: int = 5):
        pass  # Write your code here


# Problem 12: Citation Generator
# Write a function that adds citations to a generated answer:
# - Takes the answer text and the source chunks used
# - Detects factual claims in the answer
# - Matches claims to source chunks
# - Adds [Source N] citations after each claim
# - Returns the cited answer and a list of sources
def problem_12():
    pass  # Write your code here


# Problem 13: Hallucination Detector
# Write a function that detects hallucinations in a RAG answer:
# - Takes the answer, context chunks, and the original query
# - For each sentence in the answer, checks if it's supported by context
# - Uses a simple heuristic: sentence contains a key phrase from context
# - Returns a report: {sentence, supported: bool, evidence: str}
# - Computes hallucination rate: unsupported_sentences / total_sentences
def problem_13():
    pass  # Write your code here


# Problem 14: Incremental Indexer
# Build an IncrementalIndexer class that:
# - Maintains an index of documents and their embeddings
# - Supports add(new_docs), remove(doc_ids), update(doc_ids, new_docs)
# - Tracks which documents have changed since last index rebuild
# - Has a should_rebuild() method (rebuild after N changes)
# - Has a rebuild() method that re-embeds changed documents
# - Supports snapshot/restore for versioning
class IncrementalIndexer:
    def __init__(self, rebuild_threshold: int = 10):
        pass  # Write your code here

    def add(self, documents: list[dict]):
        pass  # Write your code here

    def remove(self, doc_ids: list[str]):
        pass  # Write your code here

    def update(self, doc_ids: list[str], new_docs: list[dict]):
        pass  # Write your code here

    def should_rebuild(self) -> bool:
        pass  # Write your code here

    def rebuild(self):
        pass  # Write your code here

    def snapshot(self) -> dict:
        pass  # Write your code here

    def restore(self, snapshot: dict):
        pass  # Write your code here


# Problem 15: Complete RAG Pipeline
# Build a complete RAGPipeline class that:
# - Ingests documents (chunk → embed → store)
# - Retrieves relevant chunks for a query
# - Reranks results
# - Generates an answer with citations
# - Evaluates quality (hallucination check)
# - Returns a full RAGResponse with answer, sources, metrics
# - Supports streaming the answer generation
# - Tracks latency and token usage throughout
class RAGPipeline:
    def __init__(self):
        pass  # Write your code here

    def ingest(self, documents: list[dict]):
        pass  # Write your code here

    def query(self, question: str, top_k: int = 5) -> dict:
        pass  # Write your code here

    def stream_answer(self, question: str):
        pass  # Write your code here

    def evaluate(self, test_cases: list[dict]) -> dict:
        pass  # Write your code here

    def get_metrics(self) -> dict:
        pass  # Write your code here


# ============================================================
# MAIN — Run to see problem descriptions
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Module 04: RAG Systems — Practice Problems")
    print("=" * 60)
    print()

    problems = {
        1: ("Fixed-Size Chunker", "Easy", 20),
        2: ("Sentence Chunker", "Easy", 20),
        3: ("Document Loader", "Easy", 20),
        4: ("Metadata Extractor", "Easy", 20),
        5: ("Query Preprocessor", "Easy", 20),
        6: ("Recursive Text Splitter", "Medium", 50),
        7: ("Chunk Deduplicator", "Medium", 50),
        8: ("Context Window Manager", "Medium", 50),
        9: ("RAG Prompt Builder", "Medium", 50),
        10: ("Retrieval Scorer", "Medium", 50),
        11: ("Reranker (MMR)", "Hard", 100),
        12: ("Citation Generator", "Hard", 100),
        13: ("Hallucination Detector", "Hard", 100),
        14: ("Incremental Indexer", "Hard", 100),
        15: ("Complete RAG Pipeline", "Hard", 100),
    }

    total_xp = sum(p[2] for p in problems.values())
    print(f"Total Problems: {len(problems)}")
    print(f"Total XP: {total_xp}")
    print()

    for num, (name, diff, xp) in problems.items():
        print(f"  [{num:2d}] {name:<40} {diff:<8} +{xp} XP")

    print()
    print("Select a problem number to see its full description.")
    print("Solve each function by replacing 'pass' with your implementation.")
    print("No solutions are provided — figure it out yourself!")
    print("=" * 60)
