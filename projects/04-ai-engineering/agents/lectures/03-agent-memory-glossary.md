# Glossary: Agent Memory

> Terms defined in alphabetical order. Each entry includes: definition, example usage, code snippet, and related terms.

---

## Quick Reference Table

| Term | One-Line Definition | See Also |
|------|---------------------|----------|
| Buffer | Fixed-size temporary storage for recent items | Short-term Memory |
| Cache | Fast storage for frequently accessed data | Memory, Retrieval |
| Consolidation | Moving important short-term memories to long-term | Memory, Storage |
| Context Window | Maximum tokens LLM can process at once | Memory, Limits |
| Decay | Gradual reduction of memory importance over time | Forgetting |
| Embedding | Vector representation of text for similarity search | Vector, Semantic |
| Episodic Memory | Memory of specific events and experiences | Memory, Experience |
| Forgetting | Intentional removal of unimportant memories | Decay, Consolidation |
| Index | Data structure for fast memory retrieval | Search, Vector |
| Long-term Memory | Persistent storage across sessions | Memory, Storage |
| Memory | System for storing and retrieving agent knowledge | Context, Recall |
| Recall | Retrieving relevant memories for current context | Retrieval, Search |
| Retrieval | Process of finding relevant memories | Search, Recall |
| Semantic Memory | General knowledge and facts | Memory, Knowledge |
| Sensory Memory | Brief storage of raw perceptual input | Buffer, Input |
| Short-term Memory | Limited-capacity working memory | Buffer, Working Memory |
| Summarization | Condensing memories into shorter representations | Consolidation |
| Vector | Numerical representation for semantic search | Embedding, Similarity |
| Working Memory | Active, currently relevant information | Short-term, Context |

---

## B

### Buffer

**Definition:** A temporary storage area with fixed capacity that holds the most recent items. When the buffer is full, older items are evicted (FIFO) or replaced based on priority.

**Example:**
```python
from collections import deque

class Buffer:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.items = deque(maxlen=max_size)
    
    def add(self, item):
        """Add item to buffer. Evicts oldest if full."""
        self.items.append(item)
    
    def get_recent(self, n: int = None):
        """Get last n items, or all if n is None."""
        items = list(self.items)
        return items[-n:] if n else items
    
    def is_full(self) -> bool:
        return len(self.items) >= self.max_size

# Usage
buffer = Buffer(max_size=5)
for i in range(10):
    buffer.add(f"item_{i}")

print(buffer.get_recent(3))  # ['item_7', 'item_8', 'item_9']
```

**Related terms:** Short-term Memory, Queue, Eviction

---

## C

### Cache

**Definition:** Fast storage layer that stores frequently accessed data to avoid expensive recomputation or retrieval. In agent memory, caches can store embeddings, search results, or LLM responses.

**Example:**
```python
from typing import Any, Optional
import time

class MemoryCache:
    def __init__(self, ttl_seconds: int = 300, max_size: int = 100):
        self.cache = {}
        self.ttl = ttl_seconds
        self.max_size = max_size
        self.access_times = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache if valid."""
        if key in self.cache:
            if time.time() - self.access_times[key] < self.ttl:
                return self.cache[key]
            else:
                # Expired
                del self.cache[key]
                del self.access_times[key]
        return None
    
    def set(self, key: str, value: Any):
        """Store item in cache."""
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        
        self.cache[key] = value
        self.access_times[key] = time.time()
    
    def _evict_oldest(self):
        """Remove oldest item from cache."""
        if self.access_times:
            oldest_key = min(self.access_times, key=self.access_times.get)
            del self.cache[oldest_key]
            del self.access_times[oldest_key]

# Usage
cache = MemoryCache(ttl_seconds=60)
cache.set("weather_paris", {"temp": 22, "condition": "sunny"})
result = cache.get("weather_paris")
```

**Related terms:** TTL, Eviction, Memory

---

### Consolidation

**Definition:** The process of moving important memories from short-term to long-term storage, often involving summarization or compression. Consolidation prevents information loss when working memory capacity is exceeded.

**Example:**
```python
class MemoryConsolidator:
    def __init__(self, short_term, long_term, importance_threshold=0.7):
        self.short_term = short_term
        self.long_term = long_term
        self.threshold = importance_threshold
    
    def consolidate(self):
        """Move important short-term items to long-term."""
        for entry in self.short_term.get_by_importance(self.threshold):
            # Store in long-term
            self.long_term.store(
                content=entry.content,
                importance=entry.importance,
                memory_type="consolidated",
                metadata={"source": "short_term", 
                         "original_time": entry.timestamp}
            )
    
    def summarize_and_consolidate(self):
        """Summarize short-term items before consolidating."""
        items = self.short_term.get_by_importance(self.threshold)
        
        if items:
            # Create summary
            summary = self._create_summary(items)
            
            # Store summary in long-term
            self.long_term.store(
                content=summary,
                importance=max(m.importance for m in items),
                memory_type="summary"
            )
    
    def _create_summary(self, items):
        """Create a summary of memory items."""
        contents = [str(item.content) for item in items]
        return f"Summary of {len(items)} items: " + "; ".join(contents[:5])

# Usage
consolidator = MemoryConsolidator(short_term_memory, long_term_memory)
consolidator.consolidate()
```

**Related terms:** Summarization, Short-term Memory, Long-term Memory

---

### Context Window

**Definition:** The maximum number of tokens (text units) an LLM can process in a single request. Memory systems must respect this limit by selecting only the most relevant information to include.

**Example:**
```python
class ContextManager:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.reserved_tokens = 500  # For response
    
    def build_context(self, system_prompt: str, 
                     memories: list,
                     current_query: str) -> list:
        """Build context that fits within token limit."""
        messages = [{"role": "system", "content": system_prompt}]
        available_tokens = self.max_tokens - self.reserved_tokens
        
        # Estimate tokens for system prompt
        available_tokens -= self._estimate_tokens(system_prompt)
        
        # Add most relevant memories
        for memory in memories:
            mem_tokens = self._estimate_tokens(str(memory.content))
            if available_tokens - mem_tokens > 0:
                messages.append({
                    "role": "system",
                    "content": f"Memory: {memory.content}"
                })
                available_tokens -= mem_tokens
        
        # Add current query
        messages.append({"role": "user", "content": current_query})
        
        return messages
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough estimate of token count."""
        return len(text.split()) // 3

# Usage
manager = ContextManager(max_tokens=4000)
context = manager.build_context(
    system_prompt="You are a helpful assistant.",
    memories=retrieved_memories,
    current_query="What should I wear today?"
)
```

**Related terms:** Token, Memory, Prompt

---

## D

### Decay

**Definition:** The gradual reduction of a memory's importance over time. Decaying memories eventually become candidates for forgetting, ensuring the memory system doesn't become cluttered with stale information.

**Example:**
```python
import time
import math

class ImportanceDecay:
    def __init__(self, half_life_days: float = 30):
        self.half_life = half_life_days * 86400  # Convert to seconds
    
    def calculate_decayed_importance(self, original_importance: float,
                                    created_at: float,
                                    last_accessed: float = None) -> float:
        """Calculate importance with time decay."""
        reference_time = last_accessed or time.time()
        age = reference_time - created_at
        
        # Exponential decay
        decay_factor = math.exp(-0.693 * age / self.half_life)
        
        return original_importance * decay_factor
    
    def apply_decay(self, memory_entry):
        """Apply decay to a memory entry."""
        memory_entry.importance = self.calculate_decayed_importance(
            original_importance=memory_entry.importance,
            created_at=memory_entry.timestamp,
            last_accessed=memory_entry.last_accessed
        )
        return memory_entry

# Usage
decay = ImportanceDecay(half_life_days=30)
old_memory = MemoryEntry(
    content="Old fact",
    timestamp=time.time() - 86400 * 60,  # 60 days ago
    importance=1.0
)

decayed = decay.apply_decay(old_memory)
print(f"Original: 1.0, After 60 days: {decayed.importance:.2f}")
# Original: 1.0, After 60 days: 0.25
```

**Related terms:** Forgetting, Importance, Half-life

---

## E

### Embedding

**Definition:** A dense vector representation of text that captures semantic meaning. Embeddings enable similarity-based memory retrieval — finding memories that are conceptually related, not just keyword-matched.

**Example:**
```python
from typing import List
import numpy as np

class TextEmbedder:
    def __init__(self, model_name: str = "default"):
        self.model_name = model_name
        self.dimension = 384  # Example dimension
    
    def embed(self, text: str) -> List[float]:
        """Generate embedding for text."""
        # Placeholder - in production use real model
        # e.g., sentence-transformers, OpenAI embeddings
        import hashlib
        hash_val = hashlib.md5(text.encode()).hexdigest()
        embedding = [float(int(hash_val[i:i+2], 16)) / 255 
                    for i in range(0, min(32, self.dimension * 2), 2)]
        return embedding
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        return [self.embed(text) for text in texts]
    
    def similarity(self, embedding1: List[float], 
                  embedding2: List[float]) -> float:
        """Calculate cosine similarity between embeddings."""
        dot = sum(a * b for a, b in zip(embedding1, embedding2))
        norm1 = sum(a * a for a in embedding1) ** 0.5
        norm2 = sum(b * b for b in embedding2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

# Usage
embedder = TextEmbedder()
emb1 = embedder.embed("The weather is sunny today")
emb2 = embedder.embed("It's a beautiful day outside")

sim = embedder.similarity(emb1, emb2)
print(f"Similarity: {sim:.2f}")  # Should be high (similar meaning)
```

**Related terms:** Vector, Semantic Search, Similarity

---

### Episodic Memory

**Definition:** Memory of specific events and experiences, including what happened, when it happened, and what the outcome was. Episodic memory enables agents to learn from past experiences.

**Example:**
```python
from dataclasses import dataclass
from typing import List, Dict
import time

@dataclass
class Episode:
    """A single recorded experience."""
    id: str
    timestamp: float
    goal: str
    actions_taken: List[Dict]
    outcome: str
    success: bool
    metadata: Dict = None

class EpisodicMemoryStore:
    def __init__(self):
        self.episodes: List[Episode] = []
    
    def record(self, goal: str, actions: List[Dict], 
              outcome: str) -> Episode:
        """Record a new episode."""
        episode = Episode(
            id=f"ep_{len(self.episodes)}",
            timestamp=time.time(),
            goal=goal,
            actions_taken=actions,
            outcome=outcome,
            success="success" in outcome.lower()
        )
        self.episodes.append(episode)
        return episode
    
    def retrieve_similar(self, goal: str, n: int = 3) -> List[Episode]:
        """Find episodes with similar goals."""
        def similarity_score(ep):
            goal_words = set(goal.lower().split())
            ep_words = set(ep.goal.lower().split())
            return len(goal_words & ep_words)
        
        scored = [(similarity_score(ep), ep) for ep in self.episodes]
        scored.sort(reverse=True, key=lambda x: x[0])
        return [ep for _, ep in scored[:n]]
    
    def get_successful_patterns(self) -> Dict:
        """Extract patterns from successful episodes."""
        successful = [ep for ep in self.episodes if ep.success]
        
        patterns = {}
        for ep in successful:
            for action in ep.actions_taken:
                tool = action.get("tool", "unknown")
                patterns[tool] = patterns.get(tool, 0) + 1
        
        return patterns

# Usage
store = EpisodicMemoryStore()
store.record(
    goal="Find restaurant recommendation",
    actions=[{"tool": "search", "input": "restaurants near me"}],
    outcome="Found 3 restaurants"
)
```

**Related terms:** Experience, Episode, Learning

---

## F

### Forgetting

**Definition:** The intentional removal of memories that are no longer relevant or important. Forgetting prevents memory overload and ensures the agent focuses on current, relevant information.

**Example:**
```python
import time

class ForgettingStrategy:
    def __init__(self, strategy: str = "importance"):
        self.strategy = strategy
    
    def should_forget(self, memory_entry, context: dict = None) -> bool:
        """Determine if a memory should be forgotten."""
        if self.strategy == "importance":
            return memory_entry.importance < 0.2
        
        elif self.strategy == "age":
            age_days = (time.time() - memory_entry.timestamp) / 86400
            return age_days > 30 and memory_entry.importance < 0.5
        
        elif self.strategy == "access":
            # Forgotten if never accessed in last 7 days
            days_since_access = (time.time() - memory_entry.last_accessed) / 86400
            return days_since_access > 7 and memory_entry.access_count < 3
        
        elif self.strategy == "context":
            # Forget if not relevant to current context
            if context:
                return not self._is_relevant(memory_entry, context)
            return False
        
        return False
    
    def _is_relevant(self, memory, context):
        """Check if memory is relevant to context."""
        # Simple keyword matching
        context_words = set(str(context).lower().split())
        memory_words = set(str(memory.content).lower().split())
        overlap = len(context_words & memory_words)
        return overlap > 0

# Usage
forgetter = ForgettingStrategy(strategy="importance")
memories_to_keep = [m for m in all_memories 
                   if not forgetter.should_forget(m)]
```

**Related terms:** Decay, Importance, Cleanup

---

## L

### Long-term Memory

**Definition:** Persistent storage for information that needs to survive across sessions and interactions. Long-term memory typically uses databases or vector stores and supports semantic retrieval.

**Example:**
```python
from typing import Any, List, Optional
import json

class LongTermMemoryStore:
    def __init__(self, storage_path: str = "memory.json"):
        self.storage_path = storage_path
        self.memories = []
        self._load()
    
    def _load(self):
        """Load memories from disk."""
        try:
            with open(self.storage_path, 'r') as f:
                self.memories = json.load(f)
        except FileNotFoundError:
            self.memories = []
    
    def _save(self):
        """Persist memories to disk."""
        with open(self.storage_path, 'w') as f:
            json.dump(self.memories, f, indent=2)
    
    def store(self, key: str, value: Any, 
             importance: float = 0.5) -> None:
        """Store a memory."""
        memory = {
            "key": key,
            "value": value,
            "importance": importance,
            "created_at": time.time(),
            "access_count": 0
        }
        self.memories.append(memory)
        self._save()
    
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a memory by key."""
        for memory in self.memories:
            if memory["key"] == key:
                memory["access_count"] += 1
                self._save()
                return memory["value"]
        return None
    
    def search(self, query: str, top_k: int = 5) -> List[Any]:
        """Search memories by keyword."""
        query_words = set(query.lower().split())
        
        scored = []
        for memory in self.memories:
            key_words = set(memory["key"].lower().split())
            value_words = set(str(memory["value"]).lower().split())
            all_words = key_words | value_words
            
            overlap = len(query_words & all_words)
            if overlap > 0:
                score = overlap * memory["importance"]
                scored.append((score, memory["value"]))
        
        scored.sort(reverse=True, key=lambda x: x[0])
        return [value for _, value in scored[:top_k]]
    
    def get_important(self, min_importance: float = 0.7) -> List:
        """Get high-importance memories."""
        return [m for m in self.memories 
                if m["importance"] >= min_importance]

# Usage
ltm = LongTermMemoryStore()
ltm.store("user_prefers_celsius", True, importance=0.8)
ltm.store("project_deadline", "2024-03-01", importance=0.9)
```

**Related terms:** Persistent Storage, Database, Vector Store

---

## M

### Memory

**Definition:** The system that stores and retrieves information an agent needs to remember. Memory encompasses all storage mechanisms from temporary buffers to persistent databases.

**Example:**
```python
class AgentMemorySystem:
    """Complete memory system for an agent."""
    
    def __init__(self):
        self.working = []  # Current context
        self.episodic = []  # Past experiences
        self.semantic = {}  # Facts and knowledge
    
    def remember(self, content, memory_type="working"):
        """Store information in appropriate memory."""
        if memory_type == "working":
            self.working.append({
                "content": content,
                "timestamp": time.time()
            })
        elif memory_type == "episodic":
            self.episodic.append({
                "content": content,
                "timestamp": time.time(),
                "outcome": None
            })
        elif memory_type == "semantic":
            key = content.get("key", str(content))
            self.semantic[key] = content
    
    def recall(self, query, memory_types=None):
        """Retrieve relevant memories."""
        types = memory_types or ["working", "episodic", "semantic"]
        results = []
        
        if "working" in types:
            results.extend(self.working[-10:])  # Recent working memory
        
        if "episodic" in types:
            results.extend(self.episodic[-5:])  # Recent episodes
        
        if "semantic" in types:
            # Search semantic memory
            for key, value in self.semantic.items():
                if query.lower() in key.lower():
                    results.append(value)
        
        return results
    
    def forget(self, condition):
        """Remove memories matching condition."""
        self.working = [m for m in self.working if not condition(m)]
        self.episodic = [m for m in self.episodic if not condition(m)]

# Usage
memory = AgentMemorySystem()
memory.remember("User asked about weather", "working")
memory.remember({"type": "fact", "content": "Paris is in France"}, "semantic")
```

**Related terms:** Storage, Recall, Retrieval

---

## R

### Recall

**Definition:** The process of retrieving relevant memories from storage based on a query or current context. Recall can be triggered explicitly (user asks) or implicitly (agent needs information).

**Example:**
```python
class MemoryRecaller:
    def __init__(self, memory_store):
        self.store = memory_store
    
    def recall_for_context(self, context: str, 
                          top_k: int = 5) -> list:
        """Recall memories relevant to current context."""
        # Multiple recall strategies
        
        # 1. Temporal recall (recent memories)
        temporal = self.store.get_recent(top_k)
        
        # 2. Semantic recall (similar memories)
        semantic = self.store.search_by_similarity(context, top_k)
        
        # 3. Associative recall (related memories)
        associative = self.store.find_associated(context, top_k)
        
        # Combine and deduplicate
        all_memories = temporal + semantic + associative
        seen = set()
        unique = []
        for mem in all_memories:
            mem_id = id(mem)
            if mem_id not in seen:
                seen.add(mem_id)
                unique.append(mem)
        
        return unique[:top_k]
    
    def recall_with_importance(self, context: str,
                              min_importance: float = 0.5) -> list:
        """Recall only important memories."""
        all_memories = self.recall_for_context(context)
        return [m for m in all_memories 
                if m.importance >= min_importance]

# Usage
recaller = MemoryRecaller(long_term_memory)
relevant = recaller.recall_for_context("What should I cook for dinner?")
```

**Related terms:** Retrieval, Search, Query

---

### Retrieval

**Definition:** The process of finding and extracting relevant information from memory storage. Retrieval strategies include keyword search, semantic search, and hybrid approaches.

**Example:**
```python
from typing import List

class MemoryRetriever:
    def __init__(self, memories: List, embeddings: List = None):
        self.memories = memories
        self.embeddings = embeddings
    
    def retrieve(self, query: str, strategy: str = "hybrid",
                top_k: int = 5) -> List:
        """Retrieve memories using specified strategy."""
        if strategy == "keyword":
            return self._keyword_retrieve(query, top_k)
        elif strategy == "semantic":
            return self._semantic_retrieve(query, top_k)
        elif strategy == "hybrid":
            return self._hybrid_retrieve(query, top_k)
        return []
    
    def _keyword_retrieve(self, query: str, top_k: int) -> List:
        """Simple keyword matching."""
        query_words = set(query.lower().split())
        
        scored = []
        for mem in self.memories:
            content_words = set(str(mem.content).lower().split())
            score = len(query_words & content_words)
            if score > 0:
                scored.append((score, mem))
        
        scored.sort(reverse=True, key=lambda x: x[0])
        return [mem for _, mem in scored[:top_k]]
    
    def _semantic_retrieve(self, query: str, top_k: int) -> List:
        """Vector-based semantic search."""
        if not self.embeddings:
            return self._keyword_retrieve(query, top_k)
        
        query_emb = self._embed(query)
        similarities = []
        
        for i, mem_emb in enumerate(self.embeddings):
            sim = self._cosine_sim(query_emb, mem_emb)
            similarities.append((sim, self.memories[i]))
        
        similarities.sort(reverse=True, key=lambda x: x[0])
        return [mem for _, mem in similarities[:top_k]]
    
    def _hybrid_retrieve(self, query: str, top_k: int) -> List:
        """Combine keyword and semantic results."""
        keyword_results = self._keyword_retrieve(query, top_k)
        semantic_results = self._semantic_retrieve(query, top_k)
        
        # Merge results with score boosting
        seen = {}
        for mem in keyword_results + semantic_results:
            if id(mem) in seen:
                seen[id(mem)]["score"] += 1
            else:
                seen[id(mem)] = {"mem": mem, "score": 1}
        
        ranked = sorted(seen.values(), 
                       key=lambda x: x["score"], 
                       reverse=True)
        return [item["mem"] for item in ranked[:top_k]]
    
    def _embed(self, text):
        """Placeholder for embedding generation."""
        import hashlib
        h = hashlib.md5(text.encode()).hexdigest()
        return [int(h[i:i+2], 16) / 255 for i in range(0, 32, 2)]
    
    def _cosine_sim(self, a, b):
        """Cosine similarity."""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0
```

**Related terms:** Search, Query, Similarity

---

## S

### Semantic Memory

**Definition:** Memory that stores general knowledge, facts, and concepts (as opposed to specific experiences). Semantic memory enables agents to answer factual questions and apply learned knowledge.

**Example:**
```python
class SemanticMemory:
    def __init__(self):
        self.facts = {}
        self.concepts = {}
        self.relationships = {}
    
    def learn_fact(self, subject: str, predicate: str, obj: str):
        """Learn a new fact (subject-predicate-object triple)."""
        key = f"{subject}:{predicate}"
        self.facts[key] = {
            "subject": subject,
            "predicate": predicate,
            "object": obj,
            "confidence": 1.0,
            "learned_at": time.time()
        }
        
        # Update relationships
        if subject not in self.relationships:
            self.relationships[subject] = []
        self.relationships[subject].append({
            "predicate": predicate,
            "object": obj
        })
    
    def query(self, subject: str = None, 
             predicate: str = None) -> list:
        """Query facts from semantic memory."""
        results = []
        for key, fact in self.facts.items():
            if subject and fact["subject"] != subject:
                continue
            if predicate and fact["predicate"] != predicate:
                continue
            results.append(fact)
        return results
    
    def get_related(self, concept: str) -> list:
        """Get all concepts related to given concept."""
        return self.relationships.get(concept, [])
    
    def learn_concept(self, name: str, definition: str,
                     examples: list = None):
        """Learn a new concept."""
        self.concepts[name] = {
            "definition": definition,
            "examples": examples or [],
            "learned_at": time.time()
        }

# Usage
sem_memory = SemanticMemory()
sem_memory.learn_fact("Paris", "is_capital_of", "France")
sem_memory.learn_fact("France", "is_in", "Europe")

results = sem_memory.query(subject="Paris")
print(results)  # [{'subject': 'Paris', 'predicate': 'is_capital_of', 'object': 'France'}]
```

**Related terms:** Knowledge, Facts, Concepts

---

### Summarization

**Definition:** The process of condensing longer text or multiple memories into shorter, more manageable representations. Summarization helps fit more information within context window limits.

**Example:**
```python
class MemorySummarizer:
    def __init__(self, llm_caller=None):
        self.llm = llm_caller
    
    def summarize_memories(self, memories: list, 
                          max_length: int = 500) -> str:
        """Summarize a list of memories."""
        contents = [str(m.content) for m in memories]
        combined = "\n".join(f"- {c}" for c in contents)
        
        if self.llm:
            return self._llm_summarize(combined, max_length)
        else:
            return self._extractive_summarize(combined, max_length)
    
    def _llm_summarize(self, text: str, max_length: int) -> str:
        """Use LLM for abstractive summarization."""
        prompt = f"""Summarize the following in under {max_length} words:
        
{text}

Summary:"""
        return self.llm(prompt)
    
    def _extractive_summarize(self, text: str, 
                             max_length: int) -> str:
        """Simple extractive summarization."""
        sentences = text.split(". ")
        summary = ""
        for sentence in sentences:
            if len(summary) + len(sentence) < max_length:
                summary += sentence + ". "
            else:
                break
        return summary.strip()

# Usage
summarizer = MemorySummarizer()
context_summary = summarizer.summarize_memories(recent_memories)
```

**Related terms:** Compression, Consolidation, Context

---

## Quick Reference: Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Memory System Flow                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Input ──► Sensory Buffer ──► Working Memory               │
│                                     │                       │
│                 ┌───────────────────┼───────────────────┐   │
│                 ▼                   ▼                   ▼   │
│           ┌──────────┐       ┌──────────┐       ┌──────────┐
│           │ Short-term│       │ Episodic │       │ Semantic │
│           │  Buffer   │       │  Memory  │       │  Memory  │
│           └────┬─────┘       └────┬─────┘       └────┬─────┘
│                │                  │                   │      │
│                └──────────────────┼───────────────────┘      │
│                                  ▼                          │
│                          ┌──────────────┐                  │
│                          │  Retrieval   │                  │
│                          │   System     │                  │
│                          └──────┬───────┘                  │
│                                 │                           │
│                                 ▼                           │
│                          ┌──────────────┐                  │
│                          │   Context    │                  │
│                          │   Window     │──► LLM           │
│                          └──────────────┘                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**[← Back to Lecture 03](./03-agent-memory-lecture.md)** | **[Next: Lecture 04 →](./04-react-pattern-glossary.md)**
