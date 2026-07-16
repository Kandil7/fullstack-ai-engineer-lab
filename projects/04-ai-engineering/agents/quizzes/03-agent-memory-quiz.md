# Quiz 03: Agent Memory

> **Topic Overview**: Memory systems enable agents to retain and recall information across interactions. This quiz covers different memory types (short-term, long-term, episodic, semantic), vector stores, context window management, memory retrieval strategies, and patterns for building agents that learn and adapt from past experiences.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 20 |
| Correct Answers | 0 |
| Score | 0% |
| Difficulty Rating | — |

---

## Questions

### Question 1 — Easy

**What is the primary purpose of memory in an AI agent?**

- A) To increase the agent's processing speed
- B) To enable the agent to retain and recall information across interactions
- C) To reduce the cost of API calls
- D) To encrypt the agent's communications

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Memory enables agents to retain context, learn from past interactions, maintain state across sessions, and make more informed decisions by recalling relevant historical information.

</details>

---

### Question 2 — Easy

**Which type of memory stores information about recent interactions within a single session?**

- A) Long-term memory
- B) Short-term / working memory
- C) Semantic memory
- D) Procedural memory

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Short-term (or working) memory stores information relevant to the current session or recent context. In LLMs, this is typically managed through the context window, which holds the current conversation history.

</details>

---

### Question 3 — Easy

**What is the "context window" in LLM-based agents?**

- A) A GUI window displaying the agent's output
- B) The maximum amount of text the LLM can process in a single forward pass
- C) A window for viewing source code
- D) The agent's configuration panel

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The context window is the maximum number of tokens an LLM can process in a single request. It includes the system prompt, conversation history, tool results, and any other text. Information beyond the context window is inaccessible to the model.

</details>

---

### Question 4 — Easy

**What is "semantic memory" in the context of AI agents?**

- A) Memory about specific past events
- B) General knowledge and facts about the world
- C) Memory of physical movements
- D) Memory of emotional states

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Semantic memory stores general knowledge, facts, concepts, and relationships about the world. For an AI agent, this might include knowledge about programming languages, company policies, or domain-specific information retrieved from a knowledge base.

</details>

---

### Question 5 — Medium

**What is "episodic memory" and how does it differ from semantic memory?**

- A) Episodic memory stores facts; semantic memory stores experiences
- B) Episodic memory stores specific past experiences and events; semantic memory stores general knowledge
- C) They are the same thing with different names
- D) Episodic memory is faster to access than semantic memory

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Episodic memory stores specific experiences and events (e.g., "yesterday the user asked about database optimization"). Semantic memory stores general knowledge and facts (e.g., "PostgreSQL supports JSON queries"). Both are important for agents to function effectively.

</details>

---

### Question 6 — Medium

**What is "vector similarity search" and why is it used for agent memory?**

- A) Searching for text strings using exact matching
- B) Finding similar information by comparing high-dimensional vector embeddings of text
- C) A method for encrypting memory data
- D) A technique for compressing memory storage

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Vector similarity search converts text into high-dimensional embeddings and finds semantically similar content by computing distance metrics (cosine similarity, dot product). This enables agents to retrieve relevant information even when the query doesn't exactly match stored content.

</details>

---

### Question 7 — Medium

**Which of the following is a common strategy for managing limited context windows?**

- A) Ignore old messages entirely
- B) Summarize older conversations and keep only recent messages in full detail
- C) Increase the context window by buying more expensive hardware
- D) Only process every other message

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A common strategy is to maintain full recent messages while summarizing older ones. This preserves important context from earlier in the conversation while freeing up context window space for new interactions. This is called "sliding window with summarization."

</details>

---

### Question 8 — Medium

**What is a "vector store" in the context of agent memory?**

- A) A traditional SQL database
- B) A specialized database that stores and indexes vector embeddings for efficient similarity search
- C) A file system for storing text files
- D) A caching layer for API responses

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Vector stores (like Pinecone, Weaviate, Chroma, Qdrant) are specialized databases that store vector embeddings and provide efficient similarity search capabilities. They enable agents to retrieve semantically relevant information from large knowledge bases.

</details>

---

### Question 9 — Medium

**What is "retrieval-augmented generation" (RAG) in the context of agent memory?**

- A) A method for generating new training data
- B) A pattern where the agent retrieves relevant information from a knowledge base before generating a response
- C) A technique for augmenting the agent's physical capabilities
- D) A method for generating vector embeddings

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: RAG combines retrieval and generation: the agent first retrieves relevant documents or information from a knowledge base, then uses this context to generate a more informed and accurate response. This extends the agent's knowledge beyond what's in its training data.

</details>

---

### Question 10 — Medium

**What is the "lost in the middle" problem with LLM context windows?**

- A) Information at the beginning and end of the context is attended to more than information in the middle
- B) The LLM forgets information after 10 messages
- C) The context window randomly drops messages
- D) Long contexts cause the LLM to crash

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Research shows LLMs attend more to information at the beginning and end of the context window, with middle content receiving less attention. This "lost in the middle" effect means critical information should be positioned at the start or end of the context for best retrieval.

</details>

---

### Question 11 — Hard

**What is "knowledge distillation" in the context of agent memory?**

- A) Filtering out irrelevant information from memory
- B) Extracting and compressing knowledge from a large model or knowledge base into a smaller, more efficient format
- C) Distilling water for the agent's hardware cooling
- D) Translating knowledge between different languages

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Knowledge distillation in agent memory involves extracting the most important knowledge from a large source (model or knowledge base) and compressing it into a smaller, more efficient format. This can be used to create focused knowledge bases for specific domains.

</details>

---

### Question 12 — Hard

**What is "memory consolidation" in agent systems?**

- A) The process of backing up memory to disk
- B) The process of organizing, prioritizing, and pruning stored memories to maintain efficiency and relevance
- C) Merging two agents' memories together
- D) Encrypting memory for security

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Memory consolidation is the process of reviewing stored memories, removing outdated or irrelevant information, merging similar entries, and reorganizing for efficient retrieval. This prevents memory bloat and ensures the agent maintains a high-quality, relevant knowledge base.

</details>

---

### Question 13 — Hard

**What is "hierarchical memory" and why is it useful for agents?**

- A) Memory organized in a tree structure for different levels of abstraction
- B) Memory that only stores hierarchical data structures
- C) Memory that requires admin privileges to access
- D) Memory that processes data in parallel

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Hierarchical memory organizes information at multiple levels of abstraction—from detailed specific memories at the bottom to abstract summaries at the top. This enables efficient retrieval at different granularities and helps agents manage large volumes of information.

</details>

---

### Question 14 — Hard

**What is the "retrieval bottleneck" in RAG-based agent systems?**

- A) The agent can't retrieve any information
- B) The retrieval step becomes the performance bottleneck when the knowledge base is very large or retrieval is slow
- C) The agent retrieves too much information
- D) The context window is too small for retrieved information

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

</details>

**Explanation**: The retrieval bottleneck occurs when the retrieval step (searching vector stores, ranking results) becomes the performance bottleneck. As knowledge bases grow, retrieval latency increases, potentially making it the slowest part of the agent pipeline.

</details>

---

### Question 15 — Hard

**What is "memory-augmented planning" in AI agents?**

- A) Using memory to enhance the agent's planning capabilities by recalling successful strategies from past experiences
- B) Adding more memory to the agent's hardware
- C) Planning memory allocation in advance
- D) Using memory to replace the planning module entirely

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Memory-augmented planning uses stored experiences, past strategies, and outcomes to inform future planning decisions. The agent recalls what worked and what failed in similar situations, enabling more effective and efficient planning.

</details>

---

### Question 16 — Easy

**What is "conversation history" in agent memory?**

- A) A log of all API calls made
- B) The sequence of user and assistant messages in a conversation
- C) A database of user profiles
- D) The agent's source code history

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Conversation history is the sequence of user and assistant messages in a conversation. It serves as the agent's short-term memory, providing context for understanding the current interaction and maintaining coherent dialogue.

</details>

---

### Question 17 — Medium

**Which of the following is NOT a common vector store?**

- A) Pinecone
- B) Chroma
- C) Weaviate
- D) Apache Spark

<details>
<summary>Reveal Answer</summary>

**Correct Answer: D**

**Explanation**: Apache Spark is a distributed data processing framework, not a vector store. Pinecone, Chroma, Weaviate, and Qdrant are all purpose-built vector databases designed for storing and querying vector embeddings.

</details>

---

### Question 18 — Medium

**What is "chunking" in the context of RAG memory systems?**

- A) Breaking large documents into smaller, manageable pieces for embedding and retrieval
- B) Deleting unnecessary data from memory
- C) Compressing memory into smaller files
- D) Organizing files into directories

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Chunking is the process of splitting large documents into smaller segments (chunks) for embedding and retrieval. Proper chunking is critical for RAG quality—too large and retrieval is imprecise; too small and context is lost.

</details>

---

### Question 19 — Hard

**What is the "memory recall accuracy" metric in agent evaluation?**

- A) How fast the agent recalls information
- B) The percentage of relevant memories successfully retrieved for a given query
- C) How much memory the agent uses
- D) The number of memories stored

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Memory recall accuracy measures the percentage of relevant memories that are successfully retrieved for a given query. It's analogous to "recall" in information retrieval—it measures whether the agent can find the information it needs when it needs it.

</details>

---

### Question 20 — Easy

**What is "persistent memory" vs "ephemeral memory" in agents?**

- A) Persistent memory is fast; ephemeral memory is slow
- B) Persistent memory survives across sessions; ephemeral memory is lost when the session ends
- C) Persistent memory stores text; ephemeral memory stores images
- D) They are the same thing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Persistent memory is stored outside the context window (in databases, files, or vector stores) and survives across sessions. Ephemeral memory exists only within the current context window and is lost when the session ends. Most agent systems need both.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Easy |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Medium |
| 9 | B | Medium |
| 10 | A | Medium |
| 11 | B | Hard |
| 12 | B | Hard |
| 13 | A | Hard |
| 14 | B | Hard |
| 15 | A | Hard |
| 16 | B | Easy |
| 17 | D | Medium |
| 18 | A | Medium |
| 19 | B | Hard |
| 20 | B | Easy |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 18-20 | Expert | Excellent memory systems knowledge |
| 14-17 | Proficient | Strong understanding; explore advanced patterns |
| 10-13 | Developing | Good foundation; practice implementing memory |
| 6-9 | Beginner | Review memory concepts and RAG patterns |
| 0-5 | Novice | Start with basic memory concepts |

---

**Previous Quiz**: [02 - Tool Calling](02-tool-calling-quiz.md) | **Next Quiz**: [04 - ReAct Pattern](04-react-pattern-quiz.md)
