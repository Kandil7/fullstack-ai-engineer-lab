# Lecture 03: Agent Memory

## 🎯 Topic Overview

**Memory** is what allows agents to learn from past experiences, maintain context across interactions, and make increasingly informed decisions. Without memory, every interaction starts from scratch — the agent cannot remember what worked, what failed, or what the user prefers.

This lecture covers:
- Types of memory (short-term, long-term, episodic, semantic)
- Memory architectures and storage mechanisms
- Retrieval strategies for relevant memories
- Memory consolidation and summarization
- Building agents with persistent memory

---

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. **Distinguish** between different memory types and their use cases
2. **Design** memory architectures for various agent applications
3. **Implement** short-term memory using conversation buffers
4. **Build** long-term memory with vector stores and databases
5. **Implement** memory retrieval strategies for relevant context
6. **Build** memory consolidation systems for summarization
7. **Handle** memory limits and context window constraints
8. **Design** memory systems that preserve important information

---

## 🧩 Key Concepts

### 1. Memory Taxonomy

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Memory Types                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐    ┌─────────────────────┐        │
│  │    SHORT-TERM       │    │    LONG-TERM         │        │
│  │  (Working Memory)   │    │  (Persistent)        │        │
│  ├─────────────────────┤    ├─────────────────────┤        │
│  │ • Current context   │    │ • Past interactions  │        │
│  │ • Recent messages   │    │ • Learned facts      │        │
│  │ • Active task       │    │ • User preferences   │        │
│  │ • Scratchpad        │    │ • World knowledge    │        │
│  └─────────────────────┘    └─────────────────────┘        │
│                                                             │
│  ┌─────────────────────┐    ┌─────────────────────┐        │
│  │    EPISODIC         │    │    SEMANTIC          │        │
│  │  (Experience)       │    │  (Knowledge)         │        │
│  ├─────────────────────┤    ├─────────────────────┤        │
│  │ • Specific events   │    │ • General facts      │        │
│  │ • Timestamps        │    │ • Relationships      │        │
│  │ • Outcomes          │    │ • Rules/concepts     │        │
│  │ • Emotional context │    │ • Procedures         │        │
│  └─────────────────────┘    └─────────────────────┘        │
│                                                             │
│  ┌─────────────────────┐    ┌─────────────────────┐        │
│  │    PROCEDURAL       │    │    SENSORY           │        │
│  │  (How-to)           │    │  (Perception)        │        │
│  ├─────────────────────┤    ├─────────────────────┤        │
│  │ • Action sequences  │    │ • Current input      │        │
│  │ • Skills            │    │ • Environment state  │        │
│  │ • Motor patterns    │    │ • Sensor readings    │        │
│  │ • Learned behaviors │    │ • Tool outputs       │        │
│  └─────────────────────┘    └─────────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Memory Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Memory Architecture                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   Input                                                      │
│     │                                                        │
│     ▼                                                        │
│  ┌────────────────────────────────────────┐                 │
│  │         Sensory Buffer                 │                 │
│  │    (Raw input, temporary storage)      │                 │
│  └──────────────────┬─────────────────────┘                 │
│                     │                                        │
│                     ▼                                        │
│  ┌────────────────────────────────────────┐                 │
│  │         Working Memory                 │◄── LLM Context  │
│  │    (Current task, recent context)      │     Window      │
│  └────────┬───────────────┬───────────────┘                 │
│           │               │                                  │
│           ▼               ▼                                  │
│  ┌─────────────┐  ┌─────────────┐                          │
│  │ Short-term  │  │  Long-term  │                          │
│  │   Store     │  │    Store    │                          │
│  │ (Buffer)    │  │ (Vector DB) │                          │
│  └──────┬──────┘  └──────┬──────┘                          │
│         │                │                                   │
│         ▼                ▼                                   │
│  ┌────────────────────────────────────────┐                 │
│  │         Memory Manager                │                 │
│  │  • Consolidation                       │                 │
│  │  • Retrieval                           │                 │
│  │  • Forgetting                          │                 │
│  └────────────────────────────────────────┘                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 💻 Code Examples

### Example 1: Complete Memory System

```python
"""
Complete Agent Memory System
Implements short-term, long-term, and retrieval mechanisms.
"""
import json
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
import hashlib


@dataclass
class MemoryEntry:
    """A single memory item."""
    content: Any
    timestamp: float
    memory_type: str  # "short_term", "long_term", "episodic", "semantic"
    importance: float = 0.5  # 0-1 scale
    access_count: int = 0
    last_accessed: float = 0.0
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "timestamp": self.timestamp,
            "memory_type": self.memory_type,
            "importance": self.importance,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MemoryEntry":
        return cls(**data)


class ShortTermMemory:
    """
    Working memory with limited capacity.
    
    Features:
    - Fixed-size buffer (FIFO)
    - Priority-based eviction
    - Summarization when full
    """
    
    def __init__(self, max_size: int = 20):
        self.max_size = max_size
        self.buffer: deque = deque(maxlen=max_size)
        self.importance_queue: List[MemoryEntry] = []
    
    def add(self, content: Any, importance: float = 0.5, 
            metadata: dict = None) -> MemoryEntry:
        """Add item to working memory."""
        entry = MemoryEntry(
            content=content,
            timestamp=time.time(),
            memory_type="short_term",
            importance=importance,
            metadata=metadata or {}
        )
        
        self.buffer.append(entry)
        self._maintain_size()
        
        return entry
    
    def get_recent(self, n: int = 5) -> List[MemoryEntry]:
        """Get most recent n items."""
        return list(self.buffer)[-n:]
    
    def get_by_importance(self, min_importance: float = 0.7) -> List[MemoryEntry]:
        """Get items above importance threshold."""
        return [m for m in self.buffer if m.importance >= min_importance]
    
    def _maintain_size(self):
        """Evict low-importance items when buffer is full."""
        if len(self.buffer) < self.max_size:
            return
        
        # Find least important item to evict
        min_importance = float('inf')
        min_idx = 0
        
        for i, entry in enumerate(self.buffer):
            if entry.importance < min_importance:
                min_importance = entry.importance
                min_idx = i
        
        # Only evict if importance is low
        if min_importance < 0.3:
            # Move to long-term before evicting
            evicted = self.buffer[min_idx]
            self.buffer.remove(evicted)
            return evicted
    
    def summarize(self) -> str:
        """Create a summary of current working memory."""
        if not self.buffer:
            return "Working memory is empty."
        
        summaries = []
        for entry in self.buffer:
            content = str(entry.content)[:100]
            summaries.append(f"[{entry.memory_type}] {content}")
        
        return "\n".join(summaries)


class LongTermMemory:
    """
    Persistent memory with vector-based retrieval.
    
    Features:
    - Vector embeddings for semantic search
    - Importance-based retention
    - Automatic consolidation from short-term
    """
    
    def __init__(self, embedding_model=None):
        self.memories: List[MemoryEntry] = []
        self.embeddings: List[List[float]] = []
        self.embedding_model = embedding_model
    
    def store(self, content: Any, importance: float = 0.5,
              memory_type: str = "long_term", 
              metadata: dict = None) -> MemoryEntry:
        """Store a memory in long-term storage."""
        entry = MemoryEntry(
            content=content,
            timestamp=time.time(),
            memory_type=memory_type,
            importance=importance,
            metadata=metadata or {}
        )
        
        self.memories.append(entry)
        
        # Generate embedding if model available
        if self.embedding_model:
            embedding = self._embed(str(content))
            self.embeddings.append(embedding)
        
        return entry
    
    def retrieve(self, query: str, top_k: int = 5,
                min_importance: float = 0.0) -> List[MemoryEntry]:
        """
        Retrieve relevant memories.
        
        Uses semantic search if embeddings available,
        otherwise falls back to keyword matching.
        """
        if self.embedding_model and self.embeddings:
            return self._semantic_search(query, top_k, min_importance)
        else:
            return self._keyword_search(query, top_k, min_importance)
    
    def _semantic_search(self, query: str, top_k: int,
                        min_importance: float) -> List[MemoryEntry]:
        """Vector-based semantic search."""
        query_embedding = self._embed(query)
        
        # Calculate similarities
        similarities = []
        for i, mem_embedding in enumerate(self.embeddings):
            sim = self._cosine_similarity(query_embedding, mem_embedding)
            similarities.append((sim, i))
        
        # Sort by similarity
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        # Return top results
        results = []
        for sim, idx in similarities[:top_k]:
            entry = self.memories[idx]
            if entry.importance >= min_importance:
                entry.access_count += 1
                entry.last_accessed = time.time()
                results.append(entry)
        
        return results
    
    def _keyword_search(self, query: str, top_k: int,
                       min_importance: float) -> List[MemoryEntry]:
        """Simple keyword-based search."""
        query_terms = query.lower().split()
        
        scored = []
        for entry in self.memories:
            if entry.importance < min_importance:
                continue
            
            content_str = str(entry.content).lower()
            score = sum(1 for term in query_terms if term in content_str)
            if score > 0:
                scored.append((score, entry))
        
        scored.sort(reverse=True, key=lambda x: x[0])
        
        results = []
        for score, entry in scored[:top_k]:
            entry.access_count += 1
            entry.last_accessed = time.time()
            results.append(entry)
        
        return results
    
    def _embed(self, text: str) -> List[float]:
        """Generate embedding for text."""
        # Placeholder - in production use real embedding model
        import hashlib
        hash_val = hashlib.md5(text.encode()).hexdigest()
        return [float(int(hash_val[i:i+2], 16)) / 255 
                for i in range(0, 32, 2)]
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between vectors."""
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)
    
    def consolidate(self, entries: List[MemoryEntry], 
                   max_memories: int = 1000):
        """
        Consolidate memories - keep important ones, remove old/unused.
        """
        if len(self.memories) <= max_memories:
            return
        
        # Sort by importance and recency
        self.memories.sort(
            key=lambda e: (e.importance, e.last_accessed),
            reverse=True
        )
        
        # Keep top memories
        self.memories = self.memories[:max_memories]
        if self.embeddings:
            self.embeddings = self.embeddings[:max_memories]


class EpisodicMemory:
    """
    Memory for specific events and experiences.
    
    Stores complete episodes with:
    - What happened
    - When it happened
    - What the outcome was
    - What was learned
    """
    
    def __init__(self):
        self.episodes: List[Dict] = []
    
    def record_episode(self, goal: str, actions: List[Dict],
                      outcome: str, lesson_learned: str = None) -> Dict:
        """Record a complete episode."""
        episode = {
            "id": len(self.episodes),
            "timestamp": time.time(),
            "goal": goal,
            "actions": actions,
            "outcome": outcome,
            "lesson_learned": lesson_learned,
            "success": "success" in outcome.lower()
        }
        self.episodes.append(episode)
        return episode
    
    def get_similar_episodes(self, goal: str, 
                           n: int = 3) -> List[Dict]:
        """Find episodes with similar goals."""
        scored = []
        goal_words = set(goal.lower().split())
        
        for episode in self.episodes:
            episode_words = set(episode["goal"].lower().split())
            overlap = len(goal_words & episode_words)
            scored.append((overlap, episode))
        
        scored.sort(reverse=True, key=lambda x: x[0])
        return [ep for _, ep in scored[:n]]
    
    def get_success_patterns(self) -> List[Dict]:
        """Extract patterns from successful episodes."""
        successful = [ep for ep in self.episodes if ep["success"]]
        
        # Find common action patterns
        patterns = {}
        for episode in successful:
            for action in episode["actions"]:
                tool = action.get("tool", "unknown")
                if tool not in patterns:
                    patterns[tool] = {"count": 0, "outcomes": []}
                patterns[tool]["count"] += 1
                patterns[tool]["outcomes"].append(episode["outcome"])
        
        return patterns
    
    def get_failure_lessons(self) -> List[str]:
        """Extract lessons from failed episodes."""
        failed = [ep for ep in self.episodes if not ep["success"]]
        return [ep["lesson_learned"] for ep in failed 
                if ep.get("lesson_learned")]


class AgentMemory:
    """
    Complete memory system combining all memory types.
    
    This is the memory interface agents use.
    """
    
    def __init__(self, short_term_size: int = 20,
                 embedding_model=None):
        self.short_term = ShortTermMemory(max_size=short_term_size)
        self.long_term = LongTermMemory(embedding_model=embedding_model)
        self.episodic = EpisodicMemory()
    
    def remember(self, content: Any, memory_type: str = "short_term",
                importance: float = 0.5, metadata: dict = None):
        """Store a memory in appropriate location."""
        if memory_type == "short_term":
            return self.short_term.add(content, importance, metadata)
        else:
            return self.long_term.store(content, importance, 
                                       memory_type, metadata)
    
    def recall(self, query: str, scope: str = "all",
              top_k: int = 5) -> List[Any]:
        """Retrieve memories relevant to query."""
        results = []
        
        if scope in ("all", "short_term"):
            # Search short-term (simple text matching)
            recent = self.short_term.get_recent(top_k)
            results.extend(recent)
        
        if scope in ("all", "long_term"):
            long_term_results = self.long_term.retrieve(query, top_k)
            results.extend(long_term_results)
        
        return results
    
    def record_experience(self, goal: str, actions: List[Dict],
                         outcome: str, lesson: str = None):
        """Record an experience for future learning."""
        self.episodic.record_episode(goal, actions, outcome, lesson)
    
    def get_context(self, current_goal: str) -> str:
        """
        Build context string for LLM from memory.
        
        Includes:
        - Recent conversation
        - Relevant past experiences
        - Learned lessons
        """
        parts = []
        
        # Recent context
        recent = self.short_term.get_recent(5)
        if recent:
            parts.append("Recent context:")
            for mem in recent:
                parts.append(f"- {str(mem.content)[:100]}")
        
        # Relevant past experiences
        similar = self.episodic.get_similar_episodes(current_goal, n=3)
        if similar:
            parts.append("\nSimilar past experiences:")
            for ep in similar:
                parts.append(f"- Goal: {ep['goal']}")
                parts.append(f"  Outcome: {ep['outcome'][:100]}")
        
        # Learned lessons
        lessons = self.episodic.get_failure_lessons()
        if lessons:
            parts.append("\nLessons learned from failures:")
            for lesson in lessons[:3]:
                parts.append(f"- {lesson}")
        
        return "\n".join(parts)
    
    def consolidate(self):
        """Consolidate memories - move important short-term to long-term."""
        important = self.short_term.get_by_importance(min_importance=0.7)
        for entry in important:
            self.long_term.store(
                entry.content,
                importance=entry.importance,
                memory_type="consolidated",
                metadata=entry.metadata
            )


# === Usage Example ===

# Create memory system
memory = AgentMemory(short_term_size=10)

# Add memories
memory.remember("User prefers Celsius temperatures", 
               memory_type="short_term", importance=0.8)
memory.remember("User is working on a weather app",
               memory_type="short_term", importance=0.6)

# Record an experience
memory.record_experience(
    goal="Calculate weather statistics",
    actions=[
        {"tool": "get_weather", "input": "Paris"},
        {"tool": "calculate", "input": "mean([22, 24, 21])"}
    ],
    outcome="Successfully calculated 3-day average",
    lesson="Using list of temperatures works well for averages"
)

# Get context for new task
context = memory.get_context("Calculate weather for London")
print(context)

# Recall memories
relevant = memory.recall("temperature")
for mem in relevant:
    print(f"Memory: {str(mem.content)[:80]}")
```

---

## ⚠️ Common Mistakes to Avoid

### Mistake 1: Storing Everything
```python
# ❌ BAD: Storing every interaction
def bad_remember(observation):
    memory.store(observation)  # Grows unbounded!

# ✅ GOOD: Only store important information
def good_remember(observation, importance_threshold=0.3):
    importance = calculate_importance(observation)
    if importance >= importance_threshold:
        memory.store(observation, importance=importance)
```

### Mistake 2: No Memory Retrieval Strategy
```python
# ❌ BAD: Retrieving everything
all_memories = memory.get_all()
context = "\n".join(str(m) for m in all_memories)  # Too much!

# ✅ GOOD: Targeted retrieval
relevant = memory.retrieve(query=current_task, top_k=5)
context = format_memories(relevant)
```

### Mistake 3: Ignoring Memory Decay
```python
# ❌ BAD: Old memories stay forever with same importance
def store_forever(content):
    memory.store(content, importance=0.9)  # Never decays

# ✅ GOOD: Implement importance decay
def store_with_decay(content, base_importance=0.9):
    entry = memory.store(content, importance=base_importance)
    # Schedule importance reduction over time
    schedule_decay(entry, decay_rate=0.1, period="week")
```

### Mistake 4: Not Consolidating
```python
# ❌ BAD: Short-term fills up, important info lost
memory = ShortTermMemory(max_size=10)
for i in range(100):
    memory.add(f"Important fact {i}")  # Only last 10 kept!

# ✅ GOOD: Consolidate important items
memory = AgentMemory()
for i in range(100):
    importance = calculate_importance(f"Fact {i}")
    memory.remember(f"Fact {i}", importance=importance)
memory.consolidate()  # Move important items to long-term
```

---

## ✅ Best Practices

1. **Prioritize Memories**: Assign importance scores based on relevance
2. **Implement Retrieval**: Don't just store — retrieve relevant memories
3. **Consolidate Regularly**: Move important short-term items to long-term
4. **Limit Context**: Respect LLM context window limits
5. **Track Access Patterns**: Frequently accessed memories may be more important
6. **Handle Privacy**: Be careful with sensitive information in memory
7. **Implement Forgetting**: Allow old, unused memories to decay
8. **Log Memory Operations**: Track what's stored and retrieved for debugging

---

## 🏋️ Practice Exercises

### Exercise 1: Build a Conversation Memory
Create a memory system that:
- Stores conversation history
- Summarizes old conversations
- Retrieves relevant past discussions

### Exercise 2: Preference Learning
Build a system that:
- Learns user preferences from interactions
- Updates preferences based on feedback
- Uses preferences to personalize responses

### Exercise 3: Experience Replay
Implement:
- Recording of complete agent experiences
- Pattern extraction from successful runs
- Learning from failed attempts

---

## 📝 Summary

| Memory Type | Purpose | Storage | Retention |
|-------------|---------|---------|-----------|
| **Short-term** | Current context | Buffer | Limited |
| **Long-term** | Persistent facts | Vector DB | Extended |
| **Episodic** | Past experiences | Database | Varies |
| **Semantic** | General knowledge | Knowledge base | Permanent |
| **Procedural** | How-to knowledge | Code/skills | Permanent |

**Key Takeaways:**
1. Different memory types serve different purposes
2. Retrieval is as important as storage
3. Consolidation prevents information loss
4. Memory limits require careful management
5. Privacy considerations are essential

---

## 🔗 Next Lecture

In **Lecture 04: ReAct Pattern**, we'll explore the Reasoning + Acting pattern that combines thinking and tool use.
