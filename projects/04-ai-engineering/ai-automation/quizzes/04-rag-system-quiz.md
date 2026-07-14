# Quiz 04: RAG System

## Topic Overview
This quiz covers Retrieval-Augmented Generation (RAG) systems, including document processing, chunking strategies, retrieval methods, re-ranking, citation generation, and evaluation metrics. Topics span the entire RAG pipeline from ingestion to generation.

---

## Questions

### Question 1
**What does RAG stand for in AI applications?**

- A) Random Access Generation
- B) Retrieval-Augmented Generation
- C) Recursive Algorithm for Grammar
- D) Resource-Aligned Generation

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** RAG stands for Retrieval-Augmented Generation. It's a technique that enhances LLM responses by first retrieving relevant documents from a knowledge base, then using that context to generate more accurate and grounded answers. RAG reduces hallucinations by grounding responses in factual, retrieved information.
</details>

---

### Question 2
**What is the primary benefit of RAG over using an LLM alone?**

- A) RAG is faster
- B) RAG reduces hallucinations by grounding responses in retrieved documents
- C) RAG requires less memory
- D) RAG works with any model

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** RAG's primary benefit is reducing hallucinations by providing the LLM with relevant, factual context from a knowledge base. Instead of relying solely on its training data, the model generates responses grounded in retrieved documents. This improves accuracy, enables working with private or recent data, and provides citations for verification.
</details>

---

### Question 3
**What is "chunking" in the context of RAG document processing?**

- A) Compressing documents into smaller files
- B) Splitting documents into smaller, manageable pieces for embedding and retrieval
- C) Converting documents to chunk-based databases
- D) Deleting irrelevant parts of documents

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Chunking splits long documents into smaller segments (chunks) that fit within embedding model context limits and improve retrieval granularity. Good chunking strategies balance chunk size (large enough for context, small enough for precision) and preserve semantic boundaries (paragraphs, sections, topics).
</details>

---

### Question 4
**What is the typical recommended chunk size for RAG systems?**

- A) 50-100 tokens
- B) 200-1000 tokens
- C) 5000-10000 tokens
- D) There is no standard

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Most RAG systems use chunks of 200-1000 tokens (roughly 150-750 words). This range provides enough context for meaningful embeddings while maintaining retrieval precision. Smaller chunks (200-400) work well for factual Q&A, while larger chunks (500-1000) are better for tasks requiring more context. The optimal size depends on your specific use case and embedding model.
</details>

---

### Question 5
**What is "overlap" in document chunking?**

- A) The redundancy between different document versions
- B) The overlapping text between adjacent chunks to preserve context
- C) The intersection of search results
- D) The overlap between embedding dimensions

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Chunk overlap ensures that adjacent chunks share some text (typically 10-20% of chunk size). This prevents information at chunk boundaries from being lost or split awkwardly. Overlap helps maintain context continuity across chunks, especially for concepts that span multiple paragraphs.
</details>

---

### Question 6
**What is "semantic chunking" vs "fixed-size chunking"?**

- A) Semantic chunking is faster; fixed-size is more accurate
- B) Semantic chunking splits by meaning/topics; fixed-size splits by token count
- C) Semantic chunking uses AI; fixed-size uses simple splitting
- D) They are the same thing

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Fixed-size chunking splits text at regular intervals (e.g., every 500 tokens), regardless of content structure. Semantic chunking analyzes the text's meaning and splits at natural boundaries like topic changes, paragraphs, or sections. Semantic chunking generally produces higher-quality retrievals but is more complex to implement.
</details>

---

### Question 7
**What is "re-ranking" in a RAG pipeline?**

- A) Re-embedding the query
- B) Reordering retrieved documents by relevance after initial retrieval
- C) Re-ranking the user's search history
- D) Reorganizing the vector database

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Re-ranking takes the initial set of retrieved documents (often from vector search) and reorders them using a more sophisticated relevance model. This second-pass ranking improves precision by using cross-encoders or learned models that can better assess query-document relevance than the initial retrieval method alone.
</details>

---

### Question 8
**What is "cross-encoder" re-ranking?**

- A) A re-ranking method that processes query and document together
- B) A method that uses two separate encoders for query and document
- C) A re-ranking method for multi-language queries
- D) A method that crosses embedding dimensions

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** Cross-encoders process the query and document together in a single forward pass, allowing deep interaction between query and document tokens. This produces more accurate relevance scores than bi-encoders (which encode query and document separately). However, cross-encoders are slower since they must process each query-document pair individually, making them suitable for re-ranking rather than initial retrieval.
</details>

---

### Question 9
**What is "metadata" in RAG document storage?**

- A) Data about the embedding model
- B) Structured information associated with each chunk (source, date, author, etc.)
- C) The embedding vector itself
- D) The raw document text

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Metadata provides structured information about each chunk, such as source file, page number, creation date, author, category, or custom attributes. Metadata enables filtering, citation generation, and improved retrieval by allowing the system to combine vector similarity with structured queries (e.g., "find similar chunks from 2024 in the finance category").
</details>

---

### Question 10
**What is "hybrid search" in RAG systems?**

- A) Using multiple RAG pipelines
- B) Combining vector similarity search with keyword-based search (BM25)
- C) Searching across multiple vector databases
- D) Using both cloud and on-premise search

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Hybrid search combines semantic vector search with traditional keyword search (like BM25). Vector search captures conceptual meaning, while keyword search handles exact matches (product codes, names, technical terms). Combining both methods provides more robust retrieval, especially for queries with both semantic and specific keyword components.
</details>

---

### Question 11
**What is "query expansion" in RAG retrieval?**

- A) Making the query longer by adding more words
- B) Generating additional related queries to improve recall
- C) Expanding the query to include all documents
- D) Converting the query to a different language

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Query expansion generates additional related queries from the original query to improve retrieval recall. Techniques include: generating synonyms, using the LLM to create alternative phrasings, or expanding with related concepts. Multiple queries are then used to retrieve documents, and results are merged, capturing relevant documents that the original query might miss.
</details>

---

### Question 12
**What is "context window stuffing" and why should it be avoided?**

- A) Adding too many documents to the LLM context window
- B) Compressing documents to fit in the context window
- C) Using too many tokens in the query
- D) Storing too much data in the vector database

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** Context window stuffing occurs when too many retrieved documents are added to the LLM's context, overwhelming it with information. This can degrade performance as the model struggles to identify the most relevant information. Best practices include limiting context to 3-5 most relevant chunks, using re-ranking to prioritize, and summarizing when necessary.
</details>

---

### Question 13
**What is "citation generation" in RAG systems?**

- A) Counting how many times documents are cited
- B) Automatically generating references to the source documents used in the response
- C) Creating citations for the RAG system itself
- D) Generating academic papers from retrieved documents

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Citation generation automatically tracks which retrieved documents were used in generating a response and creates proper references. This enables users to verify the AI's claims, builds trust, and provides transparency. Citations typically include document title, source, page number, and relevance score.
</details>

---

### Question 14
**What is the "context relevance" metric in RAG evaluation?**

- A) How many documents are retrieved
- B) How relevant the retrieved context is to the query
- C) How fast the retrieval process is
- D) How many tokens are in the context

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Context relevance measures how well the retrieved documents match the user's query. High context relevance means the retrieved documents contain information directly applicable to answering the query. This metric is typically evaluated using human judgments or automated metrics like ROUGE scores between queries and retrieved passages.
</details>

---

### Question 15
**What is "answer faithfulness" in RAG evaluation?**

- A) How faithful the system is to its training data
- B) Whether the generated answer is supported by the retrieved context
- C) How consistent the answers are across queries
- D) How faithful the system is to user preferences

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Answer faithfulness measures whether the generated response is grounded in and supported by the retrieved context. A faithful answer doesn't introduce information not present in the retrieved documents. This is crucial for factual accuracy and reducing hallucinations. Tools like RAGAS and DeepEval provide automated faithfulness scoring.
</details>

---

### Question 16
**What is "multimodal RAG"?**

- A) RAG that works with multiple languages
- B) RAG that retrieves and processes text, images, audio, and video
- C) RAG that uses multiple LLMs
- D) RAG that searches multiple databases

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Multimodal RAG extends traditional text-based RAG to handle multiple data types including images, audio, video, and documents (PDFs, slides). It requires specialized embedding models for each modality and fusion techniques to combine information across modalities. This is increasingly important as organizations have diverse content types.
</details>

---

### Question 17
**What is "incremental indexing" in RAG?**

- A) Indexing documents one at a time
- B) Adding new documents to the index without re-indexing everything
- C) Gradually improving the embedding model
- D) Incrementally increasing the chunk size

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Incremental indexing allows new documents to be added to the vector index without reprocessing the entire corpus. This is essential for production systems where knowledge bases are constantly updated. Efficient incremental indexing requires tracking which documents have been indexed and only processing new or changed content.
</details>

---

### Question 18
**What is "late interaction" in RAG retrieval models?**

- A) Re-ranking results after user feedback
- B) Models like ColBERT that compute token-level similarities after independent encoding
- C) Retrieving documents after the query is processed
- D) Interacting with the database after the response is generated

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Late interaction models (like ColBERT) encode query and document tokens independently, then compute fine-grained token-level similarities during retrieval. This captures more nuanced relationships than single-vector embeddings while maintaining the efficiency of bi-encoder architectures. Late interaction provides a middle ground between bi-encoders (fast but less precise) and cross-encoders (precise but slow).
</details>

---

### Question 19
**What is "RAG vs. fine-tuning" and when should you choose RAG?**

- A) RAG is always better than fine-tuning
- B) RAG is better for frequently updated knowledge; fine-tuning is better for behavior/style changes
- C) Fine-tuning is always better than RAG
- D) They are interchangeable

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** RAG is ideal when you need to access frequently changing information, private data, or want transparent citations. Fine-tuning is better when you need to change the model's behavior, style, or capabilities. Many production systems use both: fine-tuning for behavior and RAG for knowledge. RAG is generally faster to implement and easier to update.
</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Easy | | |
| 4 | Medium | | |
| 5 | Medium | | |
| 6 | Medium | | |
| 7 | Medium | | |
| 8 | Hard | | |
| 9 | Easy | | |
| 10 | Medium | | |
| 11 | Medium | | |
| 12 | Medium | | |
| 13 | Easy | | |
| 14 | Medium | | |
| 15 | Medium | | |
| 16 | Hard | | |
| 17 | Medium | | |
| 18 | Hard | | |
| 19 | Medium | | |

**Score:** ____/19

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | B | 8 | A | 15 | B |
| 2 | B | 9 | B | 16 | B |
| 3 | B | 10 | B | 17 | B |
| 4 | B | 11 | B | 18 | B |
| 5 | B | 12 | A | 19 | B |
| 6 | B | 13 | B | | |
| 7 | B | 14 | B | | |

---

*Generated for AI Automation Lab - Quiz 04 of 09*