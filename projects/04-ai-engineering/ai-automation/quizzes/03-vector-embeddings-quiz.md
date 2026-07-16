# Quiz 03: Vector Embeddings

## Topic Overview
This quiz covers vector embeddings, their generation, storage, and use in semantic search and similarity matching. Topics include embedding models, vector dimensions, cosine similarity, vector databases, indexing strategies, and embedding optimization techniques.

---

## Questions

### Question 1
**What is a vector embedding in the context of machine learning?**

- A) A compressed image format
- B) A numerical representation of text, images, or other data in a high-dimensional space
- C) A type of neural network layer
- D) A database indexing structure

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Vector embeddings are dense, fixed-length numerical representations that capture the semantic meaning of data. Similar items are mapped to nearby points in the embedding space. These vectors enable semantic search, clustering, classification, and recommendation systems by mathematically representing relationships between concepts.
</details>

---

### Question 2
**What is "cosine similarity" used for in vector search?**

- A) Calculating the distance between API endpoints
- B) Measuring the angle between two vectors to determine semantic similarity
- C) Computing the cosine of the input text length
- D) Converting vectors to polar coordinates

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Cosine similarity measures the cosine of the angle between two vectors, producing a value between -1 and 1. A value of 1 means the vectors point in the same direction (most similar), 0 means they are orthogonal (unrelated), and -1 means they point in opposite directions. It's preferred over Euclidean distance for high-dimensional embeddings because it focuses on direction rather than magnitude.
</details>

---

### Question 3
**What is the typical dimensionality of modern text embedding models?**

- A) 3-10 dimensions
- B) 128-256 dimensions
- C) 384-1536 dimensions
- D) 10,000+ dimensions

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Modern text embedding models typically produce vectors with 384 to 1536 dimensions. For example, OpenAI's text-embedding-3-small uses 1536 dimensions, while sentence-transformers models often use 384 or 768 dimensions. The dimensionality balances expressiveness with storage and computation efficiency.
</details>

---

### Question 4
**What is "embedding normalization" and why is it important?**

- A) Converting embeddings to text format
- B) Scaling vectors to unit length for consistent similarity calculations
- C) Reducing the dimensionality of embeddings
- D) Converting embeddings between different models

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Embedding normalization scales vectors to unit length (L2 norm = 1). This ensures that cosine similarity can be computed using the dot product, which is computationally faster. Normalization also makes similarity scores more stable and comparable across different embedding models and dimensions.
</details>

---

### Question 5
**What is "dimensionality reduction" in the context of embeddings?**

- A) Deleting unnecessary embedding data
- B) Reducing the number of dimensions while preserving important relationships
- C) Converting embeddings to a different model
- D) Removing duplicate embeddings

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Dimensionality reduction techniques like PCA (Principal Component Analysis), t-SNE, or UMAP reduce the number of dimensions in embedding vectors while preserving the most important semantic relationships. This can reduce storage costs and improve computational efficiency while maintaining search accuracy.
</details>

---

### Question 6
**What is "embedding batching" and why is it useful?**

- A) Storing embeddings in batches on disk
- B) Processing multiple texts simultaneously to generate embeddings efficiently
- C) Grouping similar embeddings together
- D) Compressing embeddings into batches

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Embedding batching groups multiple text inputs into a single API call for processing. This is more efficient than calling the embedding API individually for each text because it reduces network overhead and leverages GPU parallelism. Most embedding APIs support batch sizes from 32 to 2048 texts per call.
</details>

---

### Question 7
**What is an "embedding cache" and when should you use one?**

- A) A database backup of embeddings
- B) A local storage layer that avoids redundant embedding computations
- C) A cache for API authentication tokens
- D) A temporary storage for embedding models

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** An embedding cache stores previously computed embeddings to avoid redundant API calls and computation. It's useful when: the same texts are repeatedly embedded, you're developing and testing prompts, or you want to reduce costs. The cache can use content hashing to detect unchanged texts and return cached embeddings.
</details>

---

### Question 8
**What is the difference between "dense" and "sparse" embeddings?**

- A) Dense embeddings are compressed; sparse embeddings are expanded
- B) Dense embeddings have all dimensions populated; sparse embeddings have mostly zeros
- C) Dense embeddings are for text; sparse embeddings are for images
- D) Dense embeddings are newer; sparse embeddings are outdated

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Dense embeddings use all dimensions with non-zero values (e.g., [0.1, -0.3, 0.7, ...]), while sparse embeddings have most dimensions as zero with only a few non-zero values. Dense embeddings capture semantic meaning well, while sparse embeddings (like BM25 or TF-IDF) are better for exact keyword matching. Hybrid approaches combine both for optimal results.
</details>

---

### Question 9
**What is "Approximate Nearest Neighbor" (ANN) search?**

- A) An exact search algorithm for vectors
- B) A search technique that trades perfect accuracy for much faster retrieval
- C) A method for finding the farthest vectors
- D) A technique for converting vectors to text

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** ANN algorithms (like HNSW, IVF, or LSH) find vectors that are approximately nearest to a query vector, trading perfect accuracy for significant speed improvements. For large-scale vector databases with millions or billions of vectors, exact nearest neighbor search is computationally infeasible. ANN algorithms can achieve 95-99% recall with 10-100x speedup.
</details>

---

### Question 10
**What is HNSW (Hierarchical Navigable Small World) in vector databases?**

- A) A compression algorithm for embeddings
- B) A graph-based indexing algorithm for efficient approximate nearest neighbor search
- C) A hash function for embedding storage
- D) A clustering algorithm for embedding organization

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** HNSW is a graph-based indexing algorithm that creates a multi-layer graph structure for efficient approximate nearest neighbor search. It builds a hierarchical network where higher layers provide "highway" connections for fast navigation, while lower layers provide fine-grained connections. HNSW offers excellent query performance and is used in most modern vector databases.
</details>

---

### Question 11
**What is "embedding fine-tuning"?**

- A) Adjusting the model's temperature parameter
- B) Specializing a pre-trained embedding model on domain-specific data
- C) Converting embeddings between different dimensions
- D) Reducing the learning rate during training

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Embedding fine-tuning takes a pre-trained embedding model and further trains it on domain-specific data. This improves embedding quality for specialized vocabularies, industries, or use cases. For example, fine-tuning on medical literature improves embeddings for healthcare applications. Techniques include contrastive learning and domain-adaptive pre-training.
</details>

---

### Question 12
**What is "metadata filtering" in vector search?**

- A) Filtering out metadata from embeddings
- B) Combining vector similarity search with structured metadata queries
- C) Using metadata to encrypt embeddings
- D) Removing metadata from search results

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Metadata filtering combines vector similarity search with structured queries on associated metadata (e.g., date, category, author, language). This enables more precise retrieval by first filtering candidates based on metadata criteria, then ranking by vector similarity. Most vector databases support this as a core feature.
</details>

---

### Question 13
**What is "embedding drift" and how does it affect vector search?**

- A) The slow degradation of embedding quality over time as data changes
- B) The movement of embedding vectors due to hardware errors
- C) The drift of the model's API endpoint
- D) The gradual increase in embedding dimensions

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** Embedding drift occurs when the underlying data distribution changes over time, making existing embeddings less representative. For example, new slang, terminology, or concepts may not be well-represented by older embeddings. This degrades search quality. Regular re-embedding, incremental updates, and monitoring embedding quality metrics help mitigate drift.
</details>

---

### Question 14
**What is "hybrid search" in the context of vector embeddings?**

- A) Using multiple embedding models
- B) Combining vector similarity search with keyword-based search
- C) Searching across multiple vector databases
- D) Using both CPU and GPU for search

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Hybrid search combines the semantic understanding of vector similarity search with the precision of keyword-based search (like BM25). This approach handles cases where exact keyword matches are important (e.g., product codes, names) while also capturing semantic meaning. Most production RAG systems use hybrid search for optimal retrieval quality.
</details>

---

### Question 15
**What is "quantization" in vector storage?**

- A) Converting vectors to quantum computing format
- B) Reducing the precision of embedding values to save storage space
- C) Quantifying the number of dimensions in a vector
- D) Converting vectors to integer coordinates

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Quantization reduces the precision of embedding values (e.g., from 32-bit float to 8-bit integer) to save storage space and improve search speed. Techniques include scalar quantization, product quantization, and binary quantization. While some accuracy is lost, modern quantization methods achieve minimal quality degradation with 4-8x storage reduction.
</details>

---

### Question 16
**Which of the following is NOT a common embedding model?**

- A) OpenAI text-embedding-3-small
- B) BERT (base embedding)
- C) GPT-4 (embedding variant)
- D) sentence-transformers all-MiniLM-L6-v2

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** GPT-4 is a generative language model, not an embedding model. OpenAI's embedding models are in the text-embedding family (ada, text-embedding-3-small/large). BERT produces contextual embeddings as part of its architecture, and sentence-transformers is specifically designed for generating sentence and paragraph embeddings.
</details>

---

### Question 17
**What is "embedding evaluation" and which metrics are commonly used?**

- A) Checking if embeddings are correctly formatted
- B) Measuring embedding quality using retrieval accuracy, similarity scores, and downstream task performance
- C) Counting the number of embeddings in a database
- D) Measuring embedding generation speed

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Embedding evaluation measures the quality and effectiveness of embeddings for specific tasks. Common metrics include: retrieval accuracy (precision@k, recall@k), clustering quality, semantic similarity correlations with human judgments, and performance on downstream tasks like classification or question answering.
</details>

---

### Question 18
**What is the "curse of dimensionality" in vector search?**

- A) The problem of having too many embedding models
- B) The degradation of distance metrics in high-dimensional spaces
- C) The difficulty of storing embeddings in high-dimensional arrays
- D) The complexity of visualizing high-dimensional data

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

</details>

</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Medium | | |
| 4 | Medium | | |
| 5 | Medium | | |
| 6 | Easy | | |
| 7 | Medium | | |
| 8 | Medium | | |
| 9 | Hard | | |
| 10 | Hard | | |
| 11 | Medium | | |
| 12 | Medium | | |
| 13 | Hard | | |
| 14 | Medium | | |
| 15 | Hard | | |
| 16 | Easy | | |
| 17 | Medium | | |
| 18 | Hard | | |

**Score:** ____/18

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | B | 7 | B | 13 | A |
| 2 | B | 8 | B | 14 | B |
| 3 | C | 9 | B | 15 | B |
| 4 | B | 10 | B | 16 | C |
| 5 | B | 11 | B | 17 | B |
| 6 | B | 12 | B | 18 | B |

---

*Generated for AI Automation Lab - Quiz 03 of 09*