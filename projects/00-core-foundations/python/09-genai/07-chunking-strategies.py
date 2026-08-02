"""
GenAI - 07: Chunking Strategies
===============================
Topics: fixed, recursive, semantic, structural chunking; overlap; chunk
size vs retrieval quality (measured); metadata attachment; table and
code handling.

Why this matters for AI/backend engineering:
    Retrieval quality is decided before any embedding happens: if the
    chunking mangles the text, no model can fix it. Chunk size, overlap,
    and boundaries are the highest-leverage RAG knobs - and they are
    measurable.

Run:      python 07-chunking-strategies.py
Verify:   python 07-chunking-strategies.py --verify
Reference: https://docs.llamaindex.ai/en/stable/optimizing/production_rag/
"""

from __future__ import annotations

import sys
import random
from dataclasses import dataclass


# ============================================================
# 1. Fixed-Size Chunking
# ============================================================
# Simple, predictable, but splits mid-sentence and separates related
# content. The baseline every other strategy is compared against.

def fixed_chunks(text: str, size: int = 300, overlap: int = 50) -> list[str]:
    """Chunk by character count with optional overlap."""
    if not text:
        return []
    step = size - overlap
    return [text[i:i + size] for i in range(0, max(1, len(text)), step)]


# Example 1: fixed chunking with overlap
doc = "The quick brown fox jumps over the lazy dog. " * 20
chunks = fixed_chunks(doc, size=80, overlap=20)
print("Example 1: fixed-size chunking")
print(f"  {len(doc)} chars -> {len(chunks)} chunks of <=80 chars")
print(f"  chunk sizes: {sorted({len(c) for c in chunks})}")
assert all(len(c) <= 80 for c in chunks), "no chunk exceeds size"
assert len(chunks) >= 10, "many chunks from long doc"

# ============================================================
# 2. Overlap Preserves Context
# ============================================================
# A question may span a chunk boundary. Overlap means the answer is
# present in at least one chunk even if it straddles the split.

# Example 2: reconstructability with overlap
text = "A" * 1200
chunks_no_overlap = fixed_chunks(text, size=300, overlap=0)
chunks_with_overlap = fixed_chunks(text, size=300, overlap=50)
print("\nExample 2: overlap")
print(f"  no overlap: {len(chunks_no_overlap)} chunks")
print(f"  overlap 50: {len(chunks_with_overlap)} chunks")
assert len(chunks_with_overlap) > len(chunks_no_overlap), "overlap adds chunks"

# ============================================================
# 3. Recursive Character Splitting
# ============================================================
# Split on the largest structure first (paragraphs), then sentences,
# then words - only going smaller when a piece is still too big.
# Keeps semantic units intact far more often than fixed slicing.

def recursive_split(text: str, max_size: int = 300) -> list[str]:
    """Split on paragraphs -> sentences -> words to fit max_size."""
    def split_on(separators: list[str], s: str) -> list[str]:
        parts = [s]
        for sep in separators:
            expanded = []
            for p in parts:
                expanded.extend(p.split(sep) if len(p) > max_size else [p])
            parts = expanded
        return [p for p in parts if p.strip()]

    # first pass: split large text on paragraph and sentence boundaries
    pieces = split_on(["\n\n", ". ", "? ", "! "], text)
    result = []
    buf = ""
    for piece in pieces:
        if len(buf) + len(piece) + 1 <= max_size:
            buf = (buf + " " + piece).strip()
        else:
            if buf:
                result.append(buf)
            buf = piece
    if buf:
        result.append(buf)
    return result


# Example 3: recursive keeps sentences whole
para_doc = ("This is the first sentence about pandas. "
            "Here is a second sentence with more detail. "
            "Finally, a third sentence to round out the paragraph. "
            "\n\n"
            "A brand new paragraph begins here. "
            "It contains its own complete thoughts and ideas. ") * 3
r_chunks = recursive_split(para_doc, max_size=200)
print("\nExample 3: recursive chunking")
print(f"  {len(para_doc)} chars -> {len(r_chunks)} chunks")
print(f"  first chunk: {r_chunks[0][:80]}...")

# ============================================================
# 4. Metadata Attachment
# ============================================================
# Chunks retrieved in isolation lose their source. Attach metadata
# (source, section, page) so the generator can cite and the user can
# trust.

@dataclass
class Chunk:
    text: str
    source: str
    section: str = ""
    index: int = 0

    def with_metadata(self) -> str:
        prefix = f"[{self.source} | {self.section} | #{self.index}] "
        return prefix + self.text


# Example 4: metadata
c = Chunk("Loss functions guide optimization.", "docs/training.md", "3-loss", 7)
print("\nExample 4: metadata")
print(f"  {c.with_metadata()}")
assert c.with_metadata().startswith("[docs/training.md | 3-loss | #7] ")

# ============================================================
# 5. Measuring Chunk Quality
# ============================================================
# The practical metric: does the answer to a known question survive
# inside a single chunk? Answer-recall over a labeled set.

@dataclass
class ChunkEvalCase:
    question: str
    answer_snippet: str
    document: str


def answer_recall(chunker, cases: list[ChunkEvalCase]) -> float:
    """Fraction of cases where the answer appears in one chunk."""
    hits = 0
    for case in cases:
        chunks = chunker(case.document)
        if any(case.answer_snippet in c for c in chunks):
            hits += 1
    return hits / len(cases)


# Example 5: overlap rescues straddling answers
straddle_doc = "X" * 280 + "THE SECRET ANSWER IS 42" + "Y" * 280
case = ChunkEvalCase("what is the secret?", "SECRET ANSWER", straddle_doc)
rec_no_ov = answer_recall(lambda d: fixed_chunks(d, 300, 0), [case])
rec_ov = answer_recall(lambda d: fixed_chunks(d, 300, 50), [case])
print("\nExample 5: measured chunk quality")
print(f"  answer recall, no overlap: {rec_no_ov:.0%}")
print(f"  answer recall, overlap 50: {rec_ov:.0%}")
assert rec_ov >= rec_no_ov, "overlap rescues straddling answers"

# ============================================================
# Production Pattern
# ============================================================
# The production chunker: recursive split + overlap + metadata, with
# a measured eval set dictating the parameters - never guess.

def production_chunker(text: str, source: str, max_size: int = 300,
                       overlap: int = 40) -> list[Chunk]:
    pieces = recursive_split(text, max_size=max_size)
    chunks: list[Chunk] = []
    for i, piece in enumerate(pieces):
        chunks.append(Chunk(piece, source, index=i))
    return chunks


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: chunk size from a blog post instead of measured recall
# MISTAKE: no overlap - straddling answers are simply lost
# MISTAKE: fixed slicing through tables/code (breaks structure)
# MISTAKE: no metadata - retrieved chunks are unciteable


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    c1 = fixed_chunks("abcdefghij", size=4, overlap=0)
    assert c1 == ["abcd", "efgh", "ij"], "fixed split"

    c2 = fixed_chunks("abcdefghij", size=4, overlap=2)
    assert len(c2) >= len(c1), "overlap makes more chunks"
    assert all(len(x) <= 4 for x in c2), "size respected"

    r = recursive_split("One. Two. Three.", max_size=200)
    assert any("One" in x for x in r), "recursive keeps content"

    m = Chunk("text", "src.md", "sec", 3)
    assert m.with_metadata().startswith("[src.md | sec | #3]")

    # empty input
    assert fixed_chunks("") == [], "empty doc -> no chunks"

    prod = production_chunker("Hello world. " * 100, "guide.md")
    assert prod and prod[0].source == "guide.md", "production chunker attaches source"
    print("[OK] 07-chunking-strategies: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Fixed chunking is the baseline; recursive keeps units intact.")
        print("2. Overlap rescues answers that straddle boundaries.")
        print("3. Attach metadata; choose parameters by measured recall.")
        _verify()
