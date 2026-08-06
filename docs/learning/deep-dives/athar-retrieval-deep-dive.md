# Deep Dive: Athar RAG Retrieval Optimization

**Last updated:** 2026-08-06

**Context:** Optimizing retrieval quality for domain-specific RAG systems, with emphasis on
Arabic and multilingual content retrieval challenges.

---

## 1. Query Understanding

### Query Expansion
Users rarely ask questions in the optimal form for retrieval. Query understanding
transforms raw user input into something the retrieval system can work with.

**Techniques:**
- **Query rewriting:** rephrase vague queries for clarity
  - "that thing with the tokens" → "JWT token refresh mechanism"
- **Query decomposition:** break complex questions into sub-queries
  - "How does auth work and what's the refresh strategy?"
  - → Sub-query 1: "authentication flow JWT"
  - → Sub-query 2: "refresh token rotation strategy"
- **HyDE (Hypothetical Document Embeddings):** generate a hypothetical answer, embed it,
  use that for retrieval — often better than embedding the question directly

### Arabic-Specific Query Challenges
- **Diacritics (tashkeel):** users rarely type full diacritics
  - Query: "المصادقة" vs indexed: "اَلْمُصَادَقَة"
  - Fix: normalize by stripping diacritics during indexing and query time
- **Dialectal variation:** Egyptian "أكاونت" vs MSA "حساب" vs English "account"
  - Fix: multilingual embeddings + synonym expansion
- **Right-to-left mixing:** Arabic text with embedded English terms
  - "auth service المصادقة" — tokenizer may split incorrectly
  - Fix: language-aware tokenization, test with mixed-language queries
- **Morphological richness:** one Arabic root produces many forms
  - root ك-ت-ب: كتب، يكتب، مكتوب، كتاب،كاتب،كتابة
  - Fix: Arabic stemming (Khoj/Stemmer) or morphological analysis before embedding

### Query Classification
Not all queries need the same retrieval strategy:
- **Factual:** "What is the JWT expiry time?" → exact retrieval
- **Explanatory:** "How does caching work?" → broad semantic retrieval
- **Exploratory:** "Tell me about the system" → diverse multi-chunk retrieval
- **Specific:** "POST /auth/login request format" → keyword-heavy retrieval

---

## 2. Metadata Filtering

### Why Metadata Matters
Pure vector similarity is not enough. Metadata filters narrow the search space before
(or after) similarity computation, dramatically improving precision.

### Filter Design Patterns
```python
# Temporal filter: only recent documents
Filter(must=[
    FieldCondition(key="updated_at", range=Gte(gte="2024-01-01"))
])

# Language filter: Arabic content only
Filter(must=[
    FieldCondition(key="language", match=MatchValue(value="ar"))
])

# Source authority filter: official docs over blog posts
Filter(must=[
    FieldCondition(key="source_type", match=MatchValue(value="official"))
])

# Combined filter: Arabic + recent + official
Filter(must=[
    FieldCondition(key="language", match=MatchValue(value="ar")),
    FieldCondition(key="updated_at", range=Gte(gte="2024-01-01")),
    FieldCondition(key="source_type", match=MatchValue(value="official")),
])
```

### Filter Placement Strategy
- **Pre-filter (recommended):** reduces vector search space → faster + more relevant
- **Post-filter:** retrieve top-k then filter → may return fewer results
- **Faceted filtering:** combine hard filters (must) with soft preferences (should)

### Metadata Schema Best Practices
```json
{
  "language": "ar",           // ISO 639-1
  "source_type": "official",  // official | blog | forum | code
  "domain": "auth",           // functional domain
  "updated_at": "2024-06-15",
  "version": "2.1",
  "content_type": "text",     // text | code | table | faq
  "authority_score": 0.9,     // 0-1 ranking of source reliability
  "reading_level": "advanced" // beginner | intermediate | advanced
}
```

---

## 3. Multi-Turn Retrieval

### Conversation-Aware Retrieval
In multi-turn conversations, each query depends on previous context. Naive retrieval
on the latest query alone misses the full intent.

**Example:**
```
Turn 1: "How does JWT work?"        → retrieves JWT docs
Turn 2: "And the refresh part?"      → needs context from Turn 1
Turn 3: "What about token theft?"    → needs both Turn 1 + Turn 2
```

### Strategies
1. **Query rewriting with context:** prepend conversation history to the query
   ```
   "And the refresh part?" + context "JWT discussion"
   → "JWT token refresh mechanism and rotation strategy"
   ```

2. **State tracking:** maintain a conversation state object
   ```python
   conversation_state = {
       "topic": "authentication",
       "subtopics": ["JWT", "refresh tokens"],
       "depth": "intermediate",
       "asked_so_far": ["jwt_basics", "refresh_flow"]
   }
   ```

3. **Hybrid approach:** combine current query embedding with conversation
   summary embedding for broader retrieval

### Arabic Multi-Turn Considerations
- Arabic conversation often uses pronouns referencing earlier context
  - "كيف يعمل؟" (How does it work?) — "it" is ambiguous without context
- Diacritics may change across turns as user types more carefully
- Code-switching between Arabic and English is common in technical discussions

---

## 4. Domain-Specific Evaluation

### Beyond Generic Metrics
Standard RAGAs metrics are a starting point. Domain-specific evaluation requires
custom metrics tailored to the content and use case.

### Arabic RAG Evaluation Metrics

**Morphological Recall**
```
= (answers using correct Arabic morphological forms) / (total answers)
Measures: does the system handle Arabic word forms correctly?
```

**Code-Switch Quality**
```
= (answers correctly mixing Arabic + English) / (total mixed-language answers)
Measures: does retrieval handle bilingual queries?
```

**Diacritics Robustness**
```
= (correct retrieval regardless of diacritics) / (total queries)
Measures: is the system insensitive to diacritics variation?
```

### Domain-Specific Test Sets
For each domain, create:
- **50 factual questions** with known answers
- **20 edge cases** (ambiguous, multi-topic, out-of-scope)
- **10 adversarial queries** (injection attempts, misleading questions)
- **10 multilingual queries** (Arabic, English, mixed)

### Evaluation Pipeline
```
1. Load domain-specific test set
2. Run each query through RAG pipeline
3. Score: retrieval relevance, answer faithfulness, language quality
4. Human review of 10% sample for calibration
5. Compare against baseline metrics
6. Regression gate: fail if any metric drops >5%
```

---

## 5. Retrieval Optimization Playbook

### Quick Wins
1. **Add reranking** — 100ms cost, 15-20% relevance improvement
2. **Implement hybrid search** — catches keyword misses
3. **Enrich metadata** — every chunk gets source, section, language
4. **Normalize Arabic text** — strip diacritics, normalize alef/ya variants

### Medium-Term Improvements
1. **Semantic chunking** — topic-aware splits improve coherence
2. **Multi-query retrieval** — decompose complex questions
3. **Conversation-aware retrieval** — track topic across turns
4. **A/B test chunking strategies** — measure with eval dataset

### Advanced Techniques
1. **HyDE** — generate hypothetical answer, embed that instead of query
2. **Query routing** — classify query type, route to specialized retrieval
3. **Adaptive top-k** — retrieve more chunks for complex questions, fewer for simple
4. **Relevance feedback** — use click/feedback data to retrain retrieval

---

## 6. Monitoring & Continuous Improvement

### Key Metrics to Track
```
Retrieval precision@5:  target > 0.7
Retrieval recall@20:    target > 0.9
Faithfulness:           target > 0.85
End-to-end latency:     target < 3s
Hallucination rate:     target < 5%
```

### Feedback Loop
```
User query → RAG response → User feedback (thumbs up/down)
    ↓
Log: query, retrieved chunks, answer, feedback
    ↓
Weekly review: analyze negative feedback patterns
    ↓
Improvement: adjust chunking, prompt, or retrieval strategy
    ↓
Re-evaluate with eval dataset → deploy if improved
```

---

## Self-Check

Can you explain:
- Why Arabic stemming improves retrieval quality?
- How HyDE works and when to use it?
- The difference between pre-filtering and post-filtering in Qdrant?
- How multi-turn retrieval maintains conversation context?
- The quick wins vs advanced techniques for retrieval optimization?

---

## ملخص عربي (Arabic Summary)

نظرة معمقة في تحسين استرداد RAG لأنظمة المجالات المتخصصة: فهم الاستعلام، تصفية
البيانات الوصفية، الاسترداد متعدد الجولات، التقييم خارج المعايير العامة، وطرق التحسين
المنطقية. يشمل تحديات اللغة العربية: التجريد الصوتي، التنوع اللهجي، خلط اللغات،
والتحليل الصرفي.
