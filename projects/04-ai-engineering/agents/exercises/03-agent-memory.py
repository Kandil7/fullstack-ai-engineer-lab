"""
=============================================================
EXERCISE 03: Agent Memory Systems
=============================================================
Topic: Working, Short-Term, and Long-Term Memory for Agents

Learning Objectives:
- Implement working memory (in-context)
- Build short-term memory with eviction policies
- Create long-term memory with vector similarity search
- Design memory retrieval strategies
- Manage conversation history effectively
- Implement summary-based compression

Prerequisites:
- Python 3.10+
- numpy (pip install numpy)
=============================================================
"""

import json
import time
import math
import uuid
import hashlib
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from datetime import datetime, timedelta
from collections import deque
import heapq


# ============================================================
# SECTION 1: Working Memory (In-Context)
# ============================================================

@dataclass
class MemoryEntry:
    """A single memory entry with metadata."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    content: str = ""
    role: str = "user"          # "user", "assistant", "system", "tool"
    timestamp: datetime = field(default_factory=datetime.now)
    importance: float = 0.5     # 0.0 to 1.0
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)
    embedding: list[float] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "role": self.role,
            "timestamp": self.timestamp.isoformat(),
            "importance": self.importance,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat(),
            "metadata": self.metadata,
        }

    def touch(self):
        """Mark as accessed (updates recency)."""
        self.access_count += 1
        self.last_accessed = datetime.now()


class WorkingMemory:
    """
    Working memory: the agent's immediate context window.
    Manages what the LLM can "see" right now.
    """

    def __init__(self, max_tokens_estimate: int = 4000, max_messages: int = 50):
        self.max_tokens_estimate = max_tokens_estimate
        self.max_messages = max_messages
        self.messages: list[MemoryEntry] = []
        self.system_prompt: str = ""
        self._token_cache: dict[str, int] = {}

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 chars for English)."""
        if text in self._token_cache:
            return self._token_cache[text]
        tokens = max(1, len(text) // 4)
        self._token_cache[text] = tokens
        return tokens

    def current_token_count(self) -> int:
        """Estimate total tokens in working memory."""
        total = self.estimate_tokens(self.system_prompt)
        for msg in self.messages:
            total += self.estimate_tokens(msg.content)
            total += 4  # Overhead for role/formatting
        return total

    def add(self, content: str, role: str = "user", importance: float = 0.5, **kwargs):
        """Add a message to working memory."""
        entry = MemoryEntry(
            content=content,
            role=role,
            importance=importance,
            **kwargs
        )
        self.messages.append(entry)
        self._enforce_limits()

    def _enforce_limits(self):
        """Evict messages when over limits."""
        # First limit: max messages count
        if len(self.messages) > self.max_messages:
            # Keep system messages and most recent
            system_msgs = [m for m in self.messages if m.role == "system"]
            non_system = [m for m in self.messages if m.role != "system"]
            # Keep most recent non-system messages
            keep_count = self.max_messages - len(system_msgs)
            self.messages = system_msgs + non_system[-keep_count:]

        # Second limit: token estimate
        while self.current_token_count() > self.max_tokens_estimate and len(self.messages) > 2:
            # Find least important message to evict
            non_system = [m for m in self.messages if m.role != "system"]
            if not non_system:
                break
            # Evict lowest importance (or oldest if tied)
            min_importance = min(non_system, key=lambda m: (m.importance, m.timestamp))
            self.messages.remove(min_importance)

    def get_context(self, last_n: int = None) -> list[dict]:
        """Get formatted context for LLM."""
        context = []
        if self.system_prompt:
            context.append({"role": "system", "content": self.system_prompt})
        msgs = self.messages if last_n is None else self.messages[-last_n:]
        for msg in msgs:
            context.append({"role": msg.role, "content": msg.content})
        return context

    def search(self, query: str, top_k: int = 5) -> list[MemoryEntry]:
        """Simple keyword search in working memory."""
        scored = []
        query_lower = query.lower()
        for msg in self.messages:
            # Simple relevance scoring
            content_lower = msg.content.lower()
            score = 0
            for word in query_lower.split():
                if word in content_lower:
                    score += 1
            if score > 0:
                scored.append((score, msg))
        scored.sort(key=lambda x: (-x[0], -x[1].timestamp.timestamp()))
        return [msg for _, msg in scored[:top_k]]

    def get_stats(self) -> dict:
        """Get working memory statistics."""
        return {
            "messages": len(self.messages),
            "estimated_tokens": self.current_token_count(),
            "max_tokens": self.max_tokens_estimate,
            "utilization": round(self.current_token_count() / self.max_tokens_estimate, 2),
            "roles": {role: sum(1 for m in self.messages if m.role == role)
                      for role in set(m.role for m in self.messages)},
        }


# ============================================================
# SECTION 2: Short-Term Memory (Buffer-Based)
# ============================================================

class ShortTermMemory:
    """
    Short-term memory: recent interactions stored with timestamps.
    Supports eviction by time, count, or importance.
    """

    def __init__(self, max_entries: int = 100, ttl_seconds: int = 3600):
        self.max_entries = max_entries
        self.ttl_seconds = ttl_seconds
        self.entries: list[MemoryEntry] = []
        self._access_order: deque = deque()

    def store(self, content: str, role: str = "user", importance: float = 0.5, **metadata):
        """Store a memory entry."""
        entry = MemoryEntry(
            content=content,
            role=role,
            importance=importance,
            metadata=metadata,
        )
        self.entries.append(entry)
        self._access_order.append(entry.id)
        self._evict()

    def retrieve(self, memory_id: str) -> Optional[MemoryEntry]:
        """Retrieve a specific memory by ID."""
        for entry in self.entries:
            if entry.id == memory_id:
                entry.touch()
                return entry
        return None

    def search_recent(self, query: str, top_k: int = 5) -> list[MemoryEntry]:
        """Search recent memories by keyword relevance."""
        scored = []
        query_words = set(query.lower().split())
        for entry in self.entries:
            content_words = set(entry.content.lower().split())
            overlap = len(query_words & content_words)
            if overlap > 0:
                # Combine relevance with recency
                recency_score = 1.0 / (1.0 + (datetime.now() - entry.timestamp).total_seconds() / 300)
                final_score = overlap * 0.7 + recency_score * 0.3 + entry.importance * 0.2
                scored.append((final_score, entry))
        scored.sort(key=lambda x: -x[0])
        return [entry for _, entry in scored[:top_k]]

    def search_by_importance(self, min_importance: float = 0.7, top_k: int = 10) -> list[MemoryEntry]:
        """Get the most important memories."""
        important = [e for e in self.entries if e.importance >= min_importance]
        important.sort(key=lambda e: -e.importance)
        return important[:top_k]

    def _evict(self):
        """Evict old entries based on TTL and max count."""
        now = datetime.now()
        # Remove expired entries
        self.entries = [
            e for e in self.entries
            if (now - e.timestamp).total_seconds() < self.ttl_seconds
        ]
        # If still over limit, remove least important
        if len(self.entries) > self.max_entries:
            self.entries.sort(key=lambda e: (e.importance, e.timestamp))
            self.entries = self.entries[-self.max_entries:]

    def get_conversation_history(self, last_n: int = 20) -> list[dict]:
        """Get formatted conversation history."""
        recent = self.entries[-last_n:]
        return [{"role": e.role, "content": e.content} for e in recent]

    def compress(self, keep_recent: int = 10) -> list[MemoryEntry]:
        """
        Compress memory by summarizing older entries.
        Returns the compressed entries (removed from main store).
        """
        if len(self.entries) <= keep_recent:
            return []

        old_entries = self.entries[:-keep_recent]
        self.entries = self.entries[-keep_recent:]

        # Create summary entry
        summary_parts = []
        for entry in old_entries:
            summary_parts.append(f"[{entry.role}]: {entry.content[:100]}")

        summary = MemoryEntry(
            content=f"Previous conversation summary ({len(old_entries)} messages): " +
                    "; ".join(summary_parts[:5]),
            role="system",
            importance=0.8,
            metadata={"type": "summary", "original_count": len(old_entries)},
        )
        self.entries.insert(0, summary)
        return old_entries


# ============================================================
# SECTION 3: Long-Term Memory (Vector Store)
# ============================================================

class SimpleVectorStore:
    """
    Simple in-memory vector store using cosine similarity.
    In production, use ChromaDB, Pinecone, or Weaviate.
    """

    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        self.vectors: list[dict] = []  # {"id", "vector", "metadata"}

    @staticmethod
    def simple_embed(text: str, dimension: int = 128) -> list[float]:
        """
        Simple deterministic embedding (NOT for production).
        Maps text to a fixed-size vector using hashing.
        """
        # Create a deterministic seed from text
        seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
        import random
        rng = random.Random(seed)
        vector = [rng.gauss(0, 1) for _ in range(dimension)]
        # Normalize
        norm = math.sqrt(sum(v * v for v in vector))
        if norm > 0:
            vector = [v / norm for v in vector]
        return vector

    @staticmethod
    def cosine_similarity(a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def add(self, content: str, metadata: dict = None, id: str = None):
        """Add a vector to the store."""
        vector = self.simple_embed(content, self.dimension)
        entry_id = id or str(uuid.uuid4())[:8]
        self.vectors.append({
            "id": entry_id,
            "vector": vector,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
        })

    def search(self, query: str, top_k: int = 5, threshold: float = 0.0) -> list[dict]:
        """Search for similar content using cosine similarity."""
        query_vector = self.simple_embed(query, self.dimension)
        scored = []
        for entry in self.vectors:
            sim = self.cosine_similarity(query_vector, entry["vector"])
            if sim >= threshold:
                scored.append((sim, entry))
        scored.sort(key=lambda x: -x[0])
        return [
            {
                "id": entry["id"],
                "content": entry["content"],
                "score": round(score, 4),
                "metadata": entry["metadata"],
            }
            for score, entry in scored[:top_k]
        ]

    def delete(self, entry_id: str) -> bool:
        """Delete an entry by ID."""
        for i, entry in enumerate(self.vectors):
            if entry["id"] == entry_id:
                self.vectors.pop(i)
                return True
        return False

    def update(self, entry_id: str, content: str, metadata: dict = None):
        """Update an existing entry."""
        for entry in self.vectors:
            if entry["id"] == entry_id:
                entry["content"] = content
                entry["vector"] = self.simple_embed(content, self.dimension)
                if metadata:
                    entry["metadata"].update(metadata)
                return True
        return False

    def get_stats(self) -> dict:
        """Get store statistics."""
        return {
            "total_entries": len(self.vectors),
            "dimension": self.dimension,
            "memory_estimate_kb": round(len(self.vectors) * self.dimension * 8 / 1024, 2),
        }


# ============================================================
# SECTION 4: Hierarchical Memory System
# ============================================================

class HierarchicalMemory:
    """
    Complete memory system with working, short-term, and long-term layers.
    Implements automatic promotion/demotion between layers.
    """

    def __init__(self):
        self.working = WorkingMemory(max_tokens_estimate=4000, max_messages=30)
        self.short_term = ShortTermMemory(max_entries=200, ttl_seconds=7200)
        self.long_term = SimpleVectorStore(dimension=128)
        self._promotion_threshold = 3  # Access count to promote
        self._demotion_threshold = timedelta(hours=1)

    def store(self, content: str, role: str = "user", importance: float = 0.5, **metadata):
        """Store information in the appropriate memory layer."""
        # Always add to working memory
        self.working.add(content, role=role, importance=importance, **metadata)
        # Also add to short-term
        self.short_term.store(content, role=role, importance=importance, **metadata)

        # High-importance items go directly to long-term
        if importance >= 0.8:
            self.long_term.add(content, metadata={**metadata, "role": role, "importance": importance})

    def retrieve(self, query: str, layers: list[str] = None) -> dict:
        """Retrieve information from all memory layers."""
        layers = layers or ["working", "short_term", "long_term"]
        results = {}

        if "working" in layers:
            results["working"] = self.working.search(query, top_k=3)

        if "short_term" in layers:
            results["short_term"] = self.short_term.search_recent(query, top_k=5)

        if "long_term" in layers:
            results["long_term"] = self.long_term.search(query, top_k=5)

        return results

    def _promote_memories(self):
        """Promote frequently accessed short-term memories to long-term."""
        for entry in self.short_term.entries:
            if entry.access_count >= self._promotion_threshold:
                self.long_term.add(
                    entry.content,
                    metadata={"role": entry.role, "importance": entry.importance}
                )

    def get_context_for_llm(self, query: str = "", max_tokens: int = 3000) -> list[dict]:
        """
        Build the optimal context window for an LLM call.
        Combines working memory with relevant long-term memories.
        """
        context = []

        # Add working memory (most recent)
        working_ctx = self.working.get_context()
        context.extend(working_ctx)

        # If we have a query, retrieve relevant long-term memories
        if query:
            long_term_results = self.long_term.search(query, top_k=3, threshold=0.1)
            if long_term_results:
                context.append({
                    "role": "system",
                    "content": "Relevant memories:\n" + "\n".join(
                        f"- {r['content'][:200]}" for r in long_term_results
                    )
                })

        return context

    def consolidate(self):
        """
        Consolidate memory: compress short-term, promote important items,
        clean up expired entries.
        """
        # Compress old short-term entries
        self.short_term.compress(keep_recent=20)

        # Promote frequently accessed items
        self._promote_memories()

        # Clean up working memory
        self.working._enforce_limits()

    def get_stats(self) -> dict:
        """Get complete memory statistics."""
        return {
            "working_memory": self.working.get_stats(),
            "short_term_memory": {
                "entries": len(self.short_term.entries),
                "max_entries": self.short_term.max_entries,
            },
            "long_term_memory": self.long_term.get_stats(),
        }


# ============================================================
# SECTION 5: Conversation History Manager
# ============================================================

class ConversationManager:
    """
    Manages conversation history with intelligent compression
    and retrieval strategies.
    """

    def __init__(self, max_history: int = 100, compression_threshold: int = 50):
        self.max_history = max_history
        self.compression_threshold = compression_threshold
        self.history: list[MemoryEntry] = []
        self.summaries: list[str] = []
        self._total_tokens = 0

    def add_message(self, role: str, content: str, importance: float = 0.5):
        """Add a message to conversation history."""
        entry = MemoryEntry(content=content, role=role, importance=importance)
        self.history.append(entry)

        # Auto-compress if over threshold
        if len(self.history) > self.compression_threshold:
            self.compress_old()

    def compress_old(self):
        """Compress old messages into summaries."""
        keep_recent = self.max_history // 2
        if len(self.history) <= keep_recent:
            return

        old_messages = self.history[:-keep_recent]
        self.history = self.history[-keep_recent:]

        # Create summary
        summary = self._create_summary(old_messages)
        self.summaries.append(summary)

    def _create_summary(self, messages: list[MemoryEntry]) -> str:
        """Create a summary of old messages (heuristic-based)."""
        user_msgs = [m for m in messages if m.role == "user"]
        assistant_msgs = [m for m in messages if m.role == "assistant"]

        topics = set()
        for msg in user_msgs:
            # Extract potential topics (first few words)
            words = msg.content.split()[:5]
            topics.update(w.lower() for w in words if len(w) > 3)

        summary = (
            f"Conversation covered {len(messages)} messages. "
            f"Topics discussed: {', '.join(list(topics)[:5])}. "
            f"User asked about: {user_msgs[0].content[:100] if user_msgs else 'various topics'}."
        )
        return summary

    def get_context(self, max_tokens: int = 4000, include_summaries: bool = True) -> list[dict]:
        """Build context window with optional summaries."""
        context = []

        # Add summaries if available
        if include_summaries and self.summaries:
            summary_text = "Previous conversation context:\n" + "\n".join(
                f"- {s}" for s in self.summaries[-3:]
            )
            context.append({"role": "system", "content": summary_text})

        # Add recent messages
        token_count = sum(len(m.content) // 4 for m in context)
        for msg in reversed(self.history):
            msg_tokens = len(msg.content) // 4
            if token_count + msg_tokens > max_tokens:
                break
            context.insert(-len([c for c in context if c["role"] != "system"]) or len(context),
                          {"role": msg.role, "content": msg.content})
            token_count += msg_tokens

        return context

    def search(self, query: str, top_k: int = 5) -> list[MemoryEntry]:
        """Search conversation history by relevance."""
        query_words = set(query.lower().split())
        scored = []
        for entry in self.history:
            content_words = set(entry.content.lower().split())
            overlap = len(query_words & content_words)
            if overlap > 0:
                score = overlap + entry.importance * 2
                scored.append((score, entry))
        scored.sort(key=lambda x: -x[0])
        return [entry for _, entry in scored[:top_k]]

    def get_stats(self) -> dict:
        """Get conversation statistics."""
        return {
            "total_messages": len(self.history),
            "summaries": len(self.summaries),
            "estimated_tokens": sum(len(m.content) // 4 for m in self.history),
        }


# ============================================================
# SECTION 6: Memory Retrieval Strategies
# ============================================================

class RetrievalStrategy:
    """Different strategies for retrieving relevant memories."""

    @staticmethod
    def recent(memories: list[MemoryEntry], top_k: int = 5) -> list[MemoryEntry]:
        """Most recent memories."""
        return sorted(memories, key=lambda m: m.timestamp, reverse=True)[:top_k]

    @staticmethod
    def important(memories: list[MemoryEntry], top_k: int = 5) -> list[MemoryEntry]:
        """Most important memories by importance score."""
        return sorted(memories, key=lambda m: m.importance, reverse=True)[:top_k]

    @staticmethod
    def frequent(memories: list[MemoryEntry], top_k: int = 5) -> list[MemoryEntry]:
        """Most frequently accessed memories."""
        return sorted(memories, key=lambda m: m.access_count, reverse=True)[:top_k]

    @staticmethod
    def relevant(memories: list[MemoryEntry], query: str, top_k: int = 5) -> list[MemoryEntry]:
        """Most relevant memories by keyword matching."""
        query_words = set(query.lower().split())
        scored = []
        for mem in memories:
            content_words = set(mem.content.lower().split())
            overlap = len(query_words & content_words)
            if overlap > 0:
                scored.append((overlap, mem))
        scored.sort(key=lambda x: -x[0])
        return [mem for _, mem in scored[:top_k]]

    @staticmethod
    def combined(memories: list[MemoryEntry], query: str, top_k: int = 5) -> list[MemoryEntry]:
        """Combined scoring: relevance + recency + importance."""
        now = datetime.now()
        scored = []
        query_words = set(query.lower().split())

        for mem in memories:
            content_words = set(mem.content.lower().split())
            relevance = len(query_words & content_words) / max(len(query_words), 1)
            recency = 1.0 / (1.0 + (now - mem.timestamp).total_seconds() / 3600)
            importance = mem.importance
            frequency = min(mem.access_count / 10.0, 1.0)

            combined_score = (
                relevance * 0.4 +
                recency * 0.2 +
                importance * 0.3 +
                frequency * 0.1
            )
            scored.append((combined_score, mem))

        scored.sort(key=lambda x: -x[0])
        return [mem for _, mem in scored[:top_k]]


# ============================================================
# SECTION 7: Running the Exercises
# ============================================================

def exercise_1_working_memory():
    """Exercise 3.1: Working memory operations."""
    print("\n" + "=" * 60)
    print("EXERCISE 3.1: Working Memory")
    print("=" * 60)

    wm = WorkingMemory(max_tokens_estimate=500, max_messages=10)
    wm.system_prompt = "You are a helpful assistant."

    messages = [
        ("user", "What is machine learning?", 0.6),
        ("assistant", "Machine learning is a subset of AI that learns from data.", 0.7),
        ("user", "How does deep learning differ?", 0.6),
        ("assistant", "Deep learning uses neural networks with many layers.", 0.7),
        ("user", "What are transformers?", 0.5),
        ("assistant", "Transformers are attention-based architectures for sequence processing.", 0.7),
    ]

    for role, content, importance in messages:
        wm.add(content, role=role, importance=importance)
        print(f"  Added [{role}]: {content[:50]}...")

    print(f"\n  Stats: {json.dumps(wm.get_stats(), indent=4)}")

    # Search
    results = wm.search("neural networks")
    print(f"\n  Search 'neural networks':")
    for r in results:
        print(f"    [{r.role}]: {r.content[:60]}...")


def exercise_2_short_term_memory():
    """Exercise 3.2: Short-term memory with eviction."""
    print("\n" + "=" * 60)
    print("EXERCISE 3.2: Short-Term Memory")
    print("=" * 60)

    stm = ShortTermMemory(max_entries=5, ttl_seconds=60)

    # Add entries
    entries = [
        ("Hello, how are you?", "user", 0.5),
        ("I'm doing well, thanks!", "assistant", 0.6),
        ("What's the weather?", "user", 0.7),
        ("It's sunny today.", "assistant", 0.6),
        ("Tell me a joke", "user", 0.4),
        ("Why did the AI cross the road?", "assistant", 0.5),
        ("To optimize its path!", "assistant", 0.8),
    ]

    for content, role, importance in entries:
        stm.store(content, role=role, importance=importance)
        print(f"  Stored [{role}] (imp={importance}): {content[:40]}...")

    print(f"\n  Total entries: {len(stm.entries)}")

    # Search
    results = stm.search_recent("weather sunny")
    print(f"\n  Search 'weather sunny':")
    for r in results:
        print(f"    [{r.role}]: {r.content[:50]}...")

    # Compression
    print(f"\n  Compressing...")
    compressed = stm.compress(keep_recent=3)
    print(f"  Compressed {len(compressed)} entries")
    print(f"  Remaining: {len(stm.entries)} entries")


def exercise_3_vector_store():
    """Exercise 3.3: Vector store operations."""
    print("\n" + "=" * 60)
    print("EXERCISE 3.3: Vector Store (Long-Term Memory)")
    print("=" * 60)

    store = SimpleVectorStore(dimension=64)

    # Add documents
    documents = [
        "Python is a versatile programming language for data science and web development.",
        "Machine learning algorithms learn patterns from data without explicit programming.",
        "Neural networks are inspired by biological brain structure.",
        "Transformers use self-attention mechanisms for natural language processing.",
        "RAG systems combine retrieval with generation for accurate responses.",
        "Vector databases enable similarity search for semantic retrieval.",
        "Fine-tuning adapts pre-trained models to specific domains.",
        "Prompt engineering is the art of crafting effective LLM inputs.",
    ]

    print("  Adding documents:")
    for i, doc in enumerate(documents):
        store.add(doc, metadata={"index": i, "topic": "AI"})
        print(f"    [{i}] {doc[:60]}...")

    print(f"\n  Store stats: {store.get_stats()}")

    # Search
    queries = ["How do neural networks work?", "Finding similar content", "Language models"]
    for query in queries:
        results = store.search(query, top_k=3)
        print(f"\n  Search '{query}':")
        for r in results:
            print(f"    Score {r['score']}: {r['content'][:60]}...")


def exercise_4_hierarchical_memory():
    """Exercise 3.4: Hierarchical memory system."""
    print("\n" + "=" * 60)
    print("EXERCISE 3.4: Hierarchical Memory System")
    print("=" * 60)

    memory = HierarchicalMemory()

    # Store interactions
    interactions = [
        ("user", "I'm building a RAG system", 0.6),
        ("assistant", "Great! RAG combines retrieval and generation.", 0.7),
        ("user", "What vector DB should I use?", 0.7),
        ("assistant", "ChromaDB is good for prototyping, Pinecone for production.", 0.8),
        ("user", "How do I chunk documents?", 0.6),
        ("assistant", "Use overlapping windows of 500-1000 tokens with 200 token overlap.", 0.9),
        ("user", "What about embeddings?", 0.5),
        ("assistant", "text-embedding-3-small is a good balance of cost and quality.", 0.8),
    ]

    for role, content, importance in interactions:
        memory.store(content, role=role, importance=importance)
        print(f"  Stored [{role}] (imp={importance}): {content[:50]}...")

    print(f"\n  Memory Stats: {json.dumps(memory.get_stats(), indent=4)}")

    # Retrieve across layers
    query = "vector database recommendations"
    results = memory.retrieve(query)
    print(f"\n  Retrieval for '{query}':")
    for layer, layer_results in results.items():
        print(f"  {layer}: {len(layer_results)} results")

    # Get LLM context
    context = memory.get_context_for_llm(query="RAG system")
    print(f"\n  LLM Context ({len(context)} messages):")
    for msg in context:
        print(f"    [{msg['role']}]: {msg['content'][:60]}...")


def exercise_5_conversation_manager():
    """Exercise 3.5: Conversation history management."""
    print("\n" + "=" * 60)
    print("EXERCISE 3.5: Conversation History Manager")
    print("=" * 60)

    manager = ConversationManager(max_history=20, compression_threshold=15)

    # Simulate a long conversation
    conversation = [
        ("user", "Tell me about Python", 0.5),
        ("assistant", "Python is a high-level programming language.", 0.6),
        ("user", "What about decorators?", 0.7),
        ("assistant", "Decorators modify function behavior using @ syntax.", 0.8),
        ("user", "How do generators work?", 0.6),
        ("assistant", "Generators use yield to produce values lazily.", 0.7),
        ("user", "What is async/await?", 0.6),
        ("assistant", "Async/await enables cooperative concurrency in Python.", 0.8),
        ("user", "Tell me about metaclasses", 0.5),
        ("assistant", "Metaclasses are classes of classes that control class creation.", 0.7),
        ("user", "What are descriptors?", 0.5),
        ("assistant", "Descriptors define __get__, __set__, __delete__ for attribute access.", 0.7),
        ("user", "How about context managers?", 0.6),
        ("assistant", "Context managers use __enter__/__exit__ for resource management.", 0.8),
    ]

    for role, content, importance in conversation:
        manager.add_message(role, content, importance)

    print(f"  Stats: {json.dumps(manager.get_stats(), indent=4)}")

    # Get context
    context = manager.get_context(max_tokens=500)
    print(f"\n  Context ({len(context)} messages):")
    for msg in context:
        prefix = "[SUMMARY] " if msg["role"] == "system" and "Previous" in msg["content"] else ""
        print(f"    {prefix}[{msg['role']}]: {msg['content'][:60]}...")

    # Search
    results = manager.search("decorators Python")
    print(f"\n  Search 'decorators Python':")
    for r in results:
        print(f"    [{r.role}]: {r.content[:60]}...")


def exercise_6_retrieval_strategies():
    """Exercise 3.6: Memory retrieval strategies."""
    print("\n" + "=" * 60)
    print("EXERCISE 3.6: Retrieval Strategies")
    print("=" * 60)

    # Create test memories
    memories = [
        MemoryEntry(content="Python is great for data science", importance=0.8, access_count=10),
        MemoryEntry(content="Machine learning requires large datasets", importance=0.7, access_count=5),
        MemoryEntry(content="Deep learning uses neural networks", importance=0.9, access_count=15),
        MemoryEntry(content="NLP processes natural language text", importance=0.6, access_count=3),
        MemoryEntry(content="Computer vision analyzes images", importance=0.5, access_count=2),
        MemoryEntry(content="Reinforcement learning uses rewards", importance=0.7, access_count=7),
    ]

    query = "machine learning neural networks"

    print("  Testing different retrieval strategies:\n")

    # Recent
    results = RetrievalStrategy.recent(memories, top_k=3)
    print("  1. Recent Strategy:")
    for r in results:
        print(f"     {r.content[:50]}... (accessed: {r.access_count}x)")

    # Important
    results = RetrievalStrategy.important(memories, top_k=3)
    print("\n  2. Important Strategy:")
    for r in results:
        print(f"     {r.content[:50]}... (importance: {r.importance})")

    # Frequent
    results = RetrievalStrategy.frequent(memories, top_k=3)
    print("\n  3. Frequent Strategy:")
    for r in results:
        print(f"     {r.content[:50]}... (accessed: {r.access_count}x)")

    # Relevant
    results = RetrievalStrategy.relevant(memories, query, top_k=3)
    print(f"\n  4. Relevant Strategy (query: '{query}'):")
    for r in results:
        print(f"     {r.content[:50]}...")

    # Combined
    results = RetrievalStrategy.combined(memories, query, top_k=3)
    print(f"\n  5. Combined Strategy (query: '{query}'):")
    for r in results:
        print(f"     {r.content[:50]}... (imp={r.importance}, acc={r.access_count})")


def exercise_7_memory_patterns():
    """Exercise 3.7: Common memory patterns."""
    print("\n" + "=" * 60)
    print("EXERCISE 3.7: Common Memory Patterns")
    print("=" * 60)

    print("\n  Pattern 1: Sliding Window Memory")
    print("  " + "-" * 40)

    class SlidingWindowMemory:
        def __init__(self, window_size: int = 5):
            self.window = deque(maxlen=window_size)

        def add(self, item: str):
            self.window.append(item)

        def get_context(self) -> list[str]:
            return list(self.window)

    sw = SlidingWindowMemory(3)
    for i in range(5):
        sw.add(f"Message {i}")
        print(f"    Added msg {i}: {sw.get_context()}")

    print("\n  Pattern 2: Importance-Weighted Memory")
    print("  " + "-" * 40)

    class ImportanceMemory:
        def __init__(self, capacity: int = 100):
            self.capacity = capacity
            self.entries: list[MemoryEntry] = []

        def add(self, content: str, importance: float):
            entry = MemoryEntry(content=content, importance=importance)
            self.entries.append(entry)
            if len(self.entries) > self.capacity:
                # Remove lowest importance
                self.entries.sort(key=lambda e: e.importance)
                self.entries.pop(0)

        def get_top(self, n: int = 5) -> list[MemoryEntry]:
            return sorted(self.entries, key=lambda e: -e.importance)[:n]

    im = ImportanceMemory(5)
    for i, (content, imp) in enumerate([
        ("Low importance note", 0.2),
        ("Critical error message", 0.9),
        ("Routine update", 0.3),
        ("Key decision", 0.8),
        ("Minor detail", 0.1),
    ]):
        im.add(content, imp)
        print(f"    Added '{content[:20]}...' (imp={imp}): {len(im.entries)} entries")

    print(f"\n  Top entries:")
    for e in im.get_top(3):
        print(f"    {e.content[:40]}... (imp={e.importance})")

    print("\n  Pattern 3: Episodic Memory (Event Sequences)")
    print("  " + "-" * 40)

    class EpisodicMemory:
        def __init__(self):
            self.episodes: list[dict] = []

        def record_event(self, event: str, context: dict = None):
            self.episodes.append({
                "event": event,
                "context": context or {},
                "timestamp": datetime.now().isoformat(),
                "episode_id": len(self.episodes),
            })

        def recall_by_context(self, key: str, value: str) -> list[dict]:
            return [ep for ep in self.episodes if ep["context"].get(key) == value]

        def recall_recent(self, n: int = 5) -> list[dict]:
            return self.episodes[-n:]

    em = EpisodicMemory()
    em.record_event("Started coding session", {"project": "rag-app", "language": "python"})
    em.record_event("Fixed bug in parser", {"project": "rag-app", "language": "python"})
    em.record_event("Deployed to production", {"project": "rag-app", "environment": "prod"})
    em.record_event("Wrote tests", {"project": "rag-app", "language": "python"})

    print(f"    Total episodes: {len(em.episodes)}")
    print(f"    Python episodes: {len(em.recall_by_context('language', 'python'))}")
    print(f"    Recent episodes: {[e['event'] for e in em.recall_recent(2)]}")


# ============================================================
# Main: Run all exercises
# ============================================================

if __name__ == "__main__":
    print("╔" + "═" * 58 + "╗")
    print("║  EXERCISE 03: Agent Memory Systems                        ║")
    print("║  Working, Short-Term, Long-Term Memory                     ║")
    print("╚" + "═" * 58 + "╝")

    exercises = [
        ("3.1", "Working Memory", exercise_1_working_memory),
        ("3.2", "Short-Term Memory", exercise_2_short_term_memory),
        ("3.3", "Vector Store", exercise_3_vector_store),
        ("3.4", "Hierarchical Memory", exercise_4_hierarchical_memory),
        ("3.5", "Conversation Manager", exercise_5_conversation_manager),
        ("3.6", "Retrieval Strategies", exercise_6_retrieval_strategies),
        ("3.7", "Memory Patterns", exercise_7_memory_patterns),
    ]

    for num, name, func in exercises:
        try:
            func()
        except Exception as e:
            print(f"\n  [ERROR in {num}: {name}] {e}")

    print("\n" + "=" * 60)
    print("  All exercises completed!")
    print("=" * 60)

    print("""
KEY TAKEAWAYS:
1. Working memory = what the LLM sees right now (context window)
2. Short-term memory stores recent interactions with TTL
3. Long-term memory uses vector similarity for semantic retrieval
4. Hierarchical systems promote/demote memories automatically
5. Compression summarizes old conversations to save context
6. Retrieval strategies: recency, importance, frequency, relevance
7. Combined scoring gives the best retrieval results
""")
