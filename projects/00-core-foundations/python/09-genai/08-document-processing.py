"""
GenAI - 08: Document Processing
================================
Topics: PDF/HTML/Markdown extraction, layout preservation, tables, OCR,
cleaning, and garbage-in-garbage-retrieved.

Why this matters for AI/backend engineering:
    RAG quality is bounded by ingestion quality. If extraction mangles
    tables, drops headings, or keeps boilerplate, the retriever searches
    garbage. Document processing is where pipelines are won or lost.

Run:      python 08-document-processing.py
Verify:   python 08-document-processing.py --verify
Reference: https://docs.python.org/3/library/html.parser.html
"""

from __future__ import annotations

import html as html_lib
import re
import sys
from dataclasses import dataclass


# ============================================================
# 1. HTML to Text
# ============================================================
# Strip tags, keep structure (headings/paragraphs), unescape entities.
# Naive regex tag-stripping corrupts content with '<' in code or math.

def html_to_text(html: str) -> str:
    """Convert HTML to readable text, preserving headings and paragraphs."""
    # mark headings with newlines so structure survives
    html = re.sub(r"<(h[1-6])[^>]*>", lambda m: "\n## ", html, flags=re.I)
    html = re.sub(r"</h[1-6]>", "\n", html, flags=re.I)
    html = re.sub(r"<(p|div|li|br)[^>]*>", "\n", html, flags=re.I)
    html = re.sub(r"<[^>]+>", "", html)  # remove remaining tags
    text = html_lib.unescape(html)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


# Example 1: HTML extraction
sample_html = ("<html><body><h1>Pricing</h1><p>Plans start at "
               "<b>$10</b>/mo &amp; include API access.</p></body></html>")
text = html_to_text(sample_html)
print("Example 1: HTML extraction")
print(f"  {text!r}")
assert "Pricing" in text and "$10" in text and "&" in text, "tags stripped, entities decoded"

# ============================================================
# 2. Markdown Structure
# ============================================================
# Headings carry semantic structure - keep them as metadata, not text
# soup. Splitting by heading yields natural, structure-aware chunks.

def split_by_headings(md: str) -> list[dict]:
    """Split markdown into (heading, body) sections.

    Text before the first heading is treated as preamble and dropped;
    content without any headings produces no sections.
    """
    sections: list[dict] = []
    current: dict | None = None
    for line in md.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            if current is not None:
                sections.append({
                    "heading": current["heading"],
                    "body": "\n".join(current["body"]).strip(),
                })
            current = {"heading": m.group(2), "body": []}
        elif current is not None:
            current["body"].append(line)
    if current is not None:
        sections.append({"heading": current["heading"],
                         "body": "\n".join(current["body"]).strip()})
    return sections


# Example 2: heading-based sections
md_doc = "# Installation\n\nRun pip install.\n\n## Config\n\nSet the key.\n\n# Usage\n\nCall it."
sections = split_by_headings(md_doc)
print("\nExample 2: markdown sections")
for s in sections:
    print(f"  [{s['heading']}] -> {s['body'][:30]}")
assert len(sections) == 3, "three sections"
assert sections[0]["heading"] == "Installation"

# ============================================================
# 3. Cleaning Noise
# ============================================================
# Boilerplate (nav, footers, cookies) and repeated text pollute the
# index. Detect and drop junk lines by heuristic.

BOILERPLATE_PATTERNS = [
    r"cookie",
    r"sign up",
    r"all rights reserved",
    r"privacy policy",
    r"©\s*\d{4}",
]


def clean_document(text: str) -> str:
    """Drop boilerplate lines and collapse whitespace."""
    kept = []
    for line in text.splitlines():
        low = line.lower()
        if any(re.search(p, low) for p in BOILERPLATE_PATTERNS):
            continue
        kept.append(line.strip())
    return re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip()


# Example 3: cleaning
noisy = ("Welcome to our site! Please sign up for our newsletter.\n"
         "The API accepts JSON payloads.\n"
         "Copyright 2026 Example Corp. All rights reserved.\n"
         "Use POST /v1/predict.")
cleaned = clean_document(noisy)
print("\nExample 3: cleaning")
print(f"  cleaned: {cleaned!r}")
assert "sign up" not in cleaned and "Copyright" not in cleaned
assert "API accepts JSON" in cleaned

# ============================================================
# 4. Tables
# ============================================================
# Tables lose meaning as plain text. Convert them to a readable,
# searchable form (pipe-delimited) rather than concatenated cells.

def table_to_text(header: list[str], rows: list[list[str]]) -> str:
    """Render a table as a markdown-ish block for retrieval."""
    lines = [" | ".join(header), " | ".join(["---"] * len(header))]
    lines.extend(" | ".join(row) for row in rows)
    return "\n".join(lines)


# Example 4: tables survive retrieval
header = ["model", "accuracy", "latency_ms"]
rows = [["rf", "0.94", "5"], ["gbdt", "0.96", "8"]]
table_text = table_to_text(header, rows)
print("\nExample 4: table handling")
print(f"  {table_text.splitlines()[0]}")
assert "rf" in table_text and "0.96" in table_text and "accuracy" in table_text

# ============================================================
# Production Pattern
# ============================================================
# The ingestion pipeline: extract -> structure -> clean -> attach
# metadata. Test each stage against a fixture corpus.

@dataclass
class ProcessedDocument:
    title: str
    content: str
    sections: list[dict]


def process_markdown(source: str, title: str) -> ProcessedDocument:
    sections = split_by_headings(source)
    full = clean_document(source)
    return ProcessedDocument(title=title, content=full, sections=sections)


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: regex tag-stripping on HTML (breaks < in code/math)
# MISTAKE: flattening tables to cell soup (unsearchable)
# MISTAKE: indexing boilerplate (nav/footers) with real content
# MISTAKE: no cleaning step - garbage goes straight into the index


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    t = html_to_text("<p>A &amp; B</p>")
    assert t == "A & B", "entities decoded"

    secs = split_by_headings("# A\nx\n## B\ny")
    assert len(secs) == 2 and secs[0]["heading"] == "A", "headings split"

    c = clean_document("Keep this.\nSign up for updates.")
    assert "Sign up" not in c and "Keep this." in c, "boilerplate dropped"

    tbl = table_to_text(["a", "b"], [["1", "2"]])
    assert "a | b" in tbl and "1 | 2" in tbl, "table rendered"

    pd = process_markdown("# T\n\nBody\n\n## S\n\nMore", "doc")
    assert pd.title == "doc" and len(pd.sections) == 2, "processing pipeline"

    assert split_by_headings("no headings here") == [], "no headings -> no sections"
    print("[OK] 08-document-processing: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Extract with structure (headings, not tag soup).")
        print("2. Clean boilerplate before indexing.")
        print("3. Render tables so retrieval can find their cells.")
        _verify()
