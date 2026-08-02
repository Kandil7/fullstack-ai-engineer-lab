# Document Processing — Glossary 08

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Boilerplate | Cleaning | Repeated page furniture: nav, footer, banners |
| Cleaner | Pipeline | Function removing noise from extracted text |
| Deduplication | Cleaning | Removing repeated lines from extracted text |
| Encoding | Reading | The character map used to decode bytes to text |
| Loader | Pipeline | Function converting a file to text |
| Mojibake | Failure | Garbled text from wrong encoding |
| OCR | Reading | Extracting text from scanned images |
| Typed Error | Failure | An error class naming the specific problem |

## Detailed Definitions
### Boilerplate
**Definition**: Navigation, footers, banners - page furniture with no content
value.
**Related**: Cleaner

### Cleaner
**Definition**: A stage that strips tags, boilerplate, duplicates, and stray
whitespace from extracted text.
**Related**: Loader

### Deduplication
**Definition**: Collapsing repeated lines (common in PDF text layers) before
embedding.
**Related**: Cleaner

### Encoding
**Definition**: The mapping (UTF-8, latin-1, ...) from bytes to characters.
**Related**: Mojibake

### Loader
**Definition**: A function that takes a file path and returns clean text,
raising typed errors on failure.
**Related**: Cleaner

### Mojibake
**Definition**: Text garbled by decoding bytes with the wrong encoding.
**Related**: Encoding

### OCR
**Definition**: Optical character recognition; extracting text from scans.
**Related**: Loader

### Typed Error
**Definition**: An exception subclass naming the failure (e.g.
UnsupportedTypeError) for precise handling.
**Related**: Loader

## Key Concepts Summary
### The Chain
- Load → clean → dedupe → normalize → chunk

### The Rules
- Fail loudly, never silently
- Read with explicit encodings

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Boilerplate — ___
2. Loader — ___
3. Dedupe — ___
4. Mojibake — ___
5. Typed error — ___

**Answers:** 1-c, 2-b, 3-e, 4-a, 5-d where a=garbled by wrong encoding,
b=file-to-text function, c=page furniture, d=named failure class, e=remove
repeated lines.
