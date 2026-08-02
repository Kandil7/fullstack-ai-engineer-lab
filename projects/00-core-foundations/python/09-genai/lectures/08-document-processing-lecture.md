# GenAI — 08: Document Processing

## Topic Overview

Document processing is the ingestion pipeline that turns raw files (PDFs,
Word docs, HTML, markdown, images, code) into **clean, structured text that can
be chunked, embedded, and indexed** for retrieval. It is the unglamorous
foundation of every enterprise RAG system: garbage in, garbage embedded.
A pipeline that fails to parse a PDF correctly, keeps boilerplate, or loses
tables silently poisons retrieval quality — and the failures are often
invisible until answers are wrong.

The canonical pipeline:

```
ingest (read bytes) → parse (extract text) → clean (remove boilerplate)
→ normalize (encodings, whitespace) → structure (detect headings/tables)
→ chunk (L7) → embed (L6) → index (vector DB)
```

Each stage is versioned and validated (Phase 8 Lecture 10 discipline applied
to text): the ingestion pipeline is a data pipeline, and it deserves the same
gates. The two big families of tools: **parsers** (pdfplumber, PyMuPDF,
python-docx, BeautifulSoup, tika) and **frameworks** (Unstructured, LlamaHub,
Docling) that bundle parse+clean+chunk for common formats.

Why this matters: real-world documents are messy — scanned PDFs, complex
tables, nested headings, multi-column layouts, mixed languages. The AI
engineer's job is to make ingestion *lossless enough* that retrieval finds
what's actually in the documents. This lecture is the ingestion half of the
RAG story (retrieval and generation are L9–12).

## Learning Objectives

By the end of this lecture, you will be able to:
1. Parse common formats: PDF (text + tables), DOCX, HTML, markdown, plain text
2. Clean documents: boilerplate, headers/footers, whitespace, encoding
3. Extract structure: headings, tables, lists — and preserve it in chunks
4. Detect and handle scanned/image PDFs (OCR decision)
5. Validate ingestion output (empty pages, garbled text, missing tables)
6. Version the ingestion pipeline and its outputs (Phase 8 discipline)
7. Handle failure modes: encrypted PDFs, huge files, mixed encodings

## Prerequisites

| Need | Where |
|---|---|
| Chunking | `09-genai/lectures/07-chunking-strategies-lecture.md` |
| Embeddings | `09-genai/lectures/06-embeddings-lecture.md` |
| Data validation | `08-mlops/lectures/10-data-validation-lecture.md` |
| Versioning | `08-mlops/lectures/03-data-versioning-lecture.md` |

## 1. The Ingestion Pipeline

A single `ingest` function per format, all converging on one output: a list of
`Chunk` objects (L7) ready for embedding:

```python
def ingest_pipeline(source_path: str, chunk_strategy) -> list:
    """Parse → clean → structure → chunk. Returns Chunks with metadata."""
    raw = read_bytes(source_path)                 # 1. ingest
    text, tables = parse(source_path, raw)        # 2. parse (format-specific)
    cleaned = clean_text(text)                    # 3. clean
    structured = structure(cleaned, tables)       # 4. structure (headings, tables)
    chunks = chunk_strategy(structured, source_path)  # 5. chunk (L7)
    validate_chunks(chunks)                       # 6. gate (L10 discipline)
    return chunks
```

Output:
```
24 chunks from docs/guide.pdf, all with source/heading metadata, validated.
```

The contract: every format enters the pipeline and leaves as the *same* chunk
shape — so downstream embedding/indexing never cares what the source was.

## 2. Parsing PDFs: Text and Tables

PDFs are the hardest common format. Text extraction (pdfplumber/PyMuPDF)
handles most; tables need dedicated extraction; scanned PDFs need OCR.

```python
import pdfplumber

def parse_pdf_text(path: str) -> tuple[str, list]:
    """Extract text + tables from a PDF."""
    text_parts, tables = [], []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
            for tbl in page.extract_tables():
                tables.append([[c or "" for c in row] for row in tbl])
    return "\n\n".join(text_parts), tables
```

Output:
```
("Page 1 text...\n\nPage 2 text...", [ [['Q1','Revenue'],['Q1','$10M']] ])
```

**The table rule:** tables extracted separately and preserved (as markdown
tables or structured rows) — a table flattened into prose loses the column
structure that retrieval and Q&A depend on.

## 3. Scanned PDFs and OCR

If a PDF has no extractable text, it is scanned images — you need **OCR**
(Tesseract, PaddleOCR, or a vision model):

```python
def needs_ocr(text: str, sample: str = "") -> bool:
    """Scanned pages have no text layer."""
    return len(text.strip()) == 0

# OCR decision point in the pipeline:
# parse → if text empty → OCR → text
```

Output:
```
text layer present → skip OCR; text layer empty → OCR the page images.
```

**Decision guide:** text-based PDF → extract; scanned → OCR (costs time +
accuracy risk); mixed → per-page detection. OCR quality must be *validated*
(spot-check garbled text) — OCR errors propagate into embeddings silently.

## 4. Cleaning and Normalization

Raw extraction is dirty: headers/footers repeat, whitespace is erratic,
encodings mix, boilerplate (nav menus in HTML) pollutes the corpus.

```python
import re

def clean_text(text: str) -> str:
    """Normalize whitespace, drop page furniture, fix encoding artifacts."""
    text = re.sub(r"\s+", " ", text)                     # collapse whitespace
    text = re.sub(r"(?i)(page \d+ of \d+|\s+\d+\s*$)", "", text)  # page furniture
    text = text.replace("\u00a0", " ")                    # nbsp → space
    text = text.replace("\uFFFD", "")                     # replacement chars
    return text.strip()
```

Output:
```
"Billing Overview Billing Overview ..." → "Billing Overview ..."
```

Cleaning rules are **document-type specific** (a legal corpus keeps "Page X
of Y" as section context? usually not) — another reason the pipeline is
versioned and evaluated, not fixed forever.

## 5. Structure: Headings, Tables, and Chunk Metadata

Structure extraction feeds chunk metadata (L7) — heading-aware chunking, table
chunks, and section context:

```python
def structure(text: str) -> list[dict]:
    """Detect headings (markdown-style) and return (level, heading, body)."""
    sections, cur_heading, cur_body = [], "Untitled", []
    for line in text.split("\n"):
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            if cur_body:
                sections.append({"heading": cur_heading, "body": "\n".join(cur_body)})
            cur_heading = m.group(2)
            cur_body = []
        else:
            cur_body.append(line)
    if cur_body:
        sections.append({"heading": cur_heading, "body": "\n".join(cur_body)})
    return sections
```

Output:
```
[{'heading': 'Billing', 'body': 'Invoices are issued...'},
 {'heading': 'Refunds', 'body': 'Refunds take 3-5 days...'}]
```

Headings become chunk metadata — the citation anchor for answers and the
retrieval quality lever demonstrated in L7.

## 6. Validation Gates (Phase 8 Discipline)

Ingestion is a data pipeline — it needs gates (L10). Practical checks:

```python
def validate_chunks(chunks: list) -> None:
    """Gate: no empty chunks, no garbage, metadata present."""
    for c in chunks:
        if not c.text.strip():
            raise ValueError(f"empty chunk from {c.source}")
        if len(c.text) < 10:
            raise ValueError(f"suspiciously short chunk from {c.source}")
        if not c.heading:
            raise ValueError(f"chunk missing heading metadata from {c.source}")
```

Output:
```
PASS: 24 chunks validated (no empties, no garbage, all metadata present)
```

Additional gates: page-to-chunk coverage (every page produced chunks — no
silent drops), table detection rate (did tables survive?), and OCR spot-checks.
Fail → quarantine + alert (Phase 8 L10 policy), never silent.

## 7. Versioning and Incremental Ingestion

The pipeline and its outputs are versioned (Phase 8 L3): content-hash each
chunk/document, re-ingest only what changed, and gate pipeline changes with a
retrieval eval (L10). A parser update or cleaning-rule change is a *pipeline
version bump* with a re-index decision.

```python
def doc_hash(text: str) -> str:
    import hashlib
    return f"sha256:{hashlib.sha256(text.encode()).hexdigest()[:16]}"

# incremental: re-ingest only docs whose hash changed since the last index
changed = [p for p in all_docs if doc_hash(read(p)) != last_index.get(p)]
```

Output:
```
3 of 1,200 documents changed → re-ingest 3, re-embed 3, index updated.
```

## Every Use Case

- **Enterprise RAG**: support docs, policies, knowledge bases, wikis.
- **Legal**: contracts, filings, case law (PDF-heavy, table-light).
- **Healthcare**: clinical notes, research PDFs, reports.
- **Finance**: filings (10-Ks), prospectuses, invoices (tables!).
- **Code**: repos as retrieval corpora (structure-aware parsing).
- **Media**: articles, newsletters (HTML cleaning).
- **Academic**: papers (multi-column PDFs need layout-aware parsing).
- **Email/chat archives**: message-boundary parsing.
- **Regulatory**: audit-ready ingestion (versioned, validated, logged).

## Real-World Use Cases for AI Engineers

- **Insurance claims RAG**: the ingestion pipeline parses 40,000 claim PDFs
  (text + tables) into chunked, metadata-tagged records. The table-preserving
  parser (vs a naive one) is what makes "what was the claim amount?"
  answerable — the table gate caught a parser update that silently dropped
  every table.
- **Legal due diligence**: contracts parse sentence-chunked with headings;
  a scanned-historical-archives corpus goes through OCR with spot-check
  validation. The versioned pipeline means the diligence Q&A's answers are
  traceable to exact source clauses.
- **Financial filings**: 10-Ks are multi-column PDFs; layout-aware parsing
  preserves section structure ("Item 7" chunks carry their heading) — the
  analyst Q&A cites Item 7 correctly.
- **Support knowledge base**: HTML export of the help center is cleaned
  (nav boilerplate removed) and heading-structured — retrieval recall jumped
  after boilerplate removal, and the eval (L10) proved it.
- **RAG platform team**: ingestion is a shared service: format adapters +
  cleaning rules + gates per corpus; every corpus's pipeline version is
  recorded with its index manifest (L3) — a bad parser update can be
  reverted by pointing at the last-good pipeline version.

## Common Mistakes to Avoid

### Mistake 1: Assuming PDF text extraction "just works"
Scanned PDFs, multi-column, and embedded fonts all defeat naive extraction.
Detect + handle per case.

### Mistake 2: Flattening tables into prose
Column structure is information. Extract tables separately, preserve them.

### Mistake 3: No cleaning
Boilerplate and page furniture pollute embeddings and waste tokens.

### Mistake 4: No validation gates
Silent empty pages → silent retrieval gaps. Gate every ingestion run.

### Mistake 5: OCR without quality checks
OCR errors propagate silently into embeddings. Spot-check and measure.

### Mistake 6: Full re-ingest on every change
Re-ingest incrementally by content hash (Phase 8 L3).

### Mistake 7: Unversioned pipeline changes
A parser update that changes outputs is a version bump with eval + re-index
— not a silent code change.

## Best Practices

1. One pipeline contract: every format → Chunk objects with metadata
2. Parse text and tables separately; preserve both
3. Detect scanned PDFs; OCR with validation
4. Clean per document type (boilerplate, furniture, encoding)
5. Gate ingestion: no empty/garbled chunks, metadata present
6. Version the pipeline and its outputs; re-index only changed docs
7. Gate pipeline changes with a retrieval eval (L10)
8. Log per-source parse success + table-detection rates (L17)
9. Handle failures explicitly: encrypted, corrupt, huge files → quarantine + alert
10. Keep the raw source with the chunks (audit + re-processing)

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Parse text PDF | ms-page | O(n) | — |
| Table extraction | slow (pdfplumber) | O(n) | page-image heuristics |
| OCR (Tesseract) | seconds-page | O(n) | vision-LLM for hard cases |
| Clean + structure | O(n) | O(n) | — |
| Full re-index | hours for 1M docs | full store | incremental by hash |

## AI Engineering Relevance

**Where this shows up:** the ingestion stage of every RAG system. Garbage in,
garbage embedded — document processing quality is upstream of retrieval and
answer quality.

| Concept here | Used for |
|---|---|
| Parse + clean | lossless text from messy sources |
| Structure metadata | citations and heading-aware retrieval |
| Validation gates | no silent ingestion failures |
| Versioning | auditable, revertable pipelines |

**Scale note:** at 1M documents, ingestion is a batch pipeline with real
compute cost (OCR + embedding) — incremental re-ingestion and versioned
pipeline changes are what keep it economical and auditable.

## Practice Exercises

### Exercise 1: Cleaner (Easy)
Write `clean_text` handling: collapsed whitespace, page furniture, nbsp,
replacement chars. Test with a dirty sample and assert the clean output.

### Exercise 2: Table Extraction Shape (Medium)
Given a mock page table as a list of rows, write `table_to_markdown(rows)`
and `table_to_rows(rows)` — assert both preserve the structure losslessly.

### Exercise 3: Structure Detector (Medium)
Implement `structure(text)` (section 5) and assert headings map to the right
bodies, including nested levels.

### Exercise 4: Versioned Incremental Ingest (Hard)
Build `incremental_ingest(docs, last_index, parse_fn)` that: computes hashes,
re-ingests only changed docs, updates the index, and returns the delta — with
tests for add/change/no-change cases.

## Summary

| Concept | Description |
|---|---|
| Pipeline contract | formats → Chunk objects |
| Parse | text + tables, per-format |
| Clean/structure | boilerplate removal, heading metadata |
| OCR | scanned documents, validated |
| Gates + versioning | the Phase 8 discipline applied to text |

Document processing is the quiet foundation of enterprise RAG: parse, clean,
structure, and gate every document so that retrieval finds what's actually
there. The pipelines that do this well are versioned, validated, and
incremental — the ones that don't quietly poison every answer built on top.

## Quick Reference

| Task | Idiom |
|---|---|
| Parse PDF text | `pdfplumber.extract_text()` |
| Parse tables | `page.extract_tables()` → markdown |
| OCR scan | text-layer empty → Tesseract/vision |
| Clean | whitespace + furniture + encoding rules |
| Gate | no empty chunks, metadata present |
| Increment | re-ingest only hash-changed docs |

## Next Steps

Next: **[09 RAG Baseline](09-rag-baseline-lecture.md)** — putting it together:
retrieve context, generate grounded answers.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://unstructured.io/, https://pypi.org/project/pdfplumber/
