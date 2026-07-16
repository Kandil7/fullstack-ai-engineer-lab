# Glossary: GPT Tokenizer — Tokenization in LLMs

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| Tokenization | Converting text into sequences of integers for neural network processing | The bridge between human language and model math |
| Token | A unit of text represented by a single integer ID | Common words are 1 token; rare words are many |
| Byte Pair Encoding (BPE) | Algorithm that iteratively merges frequent adjacent byte pairs to build a vocabulary | GPT-2 / GPT-3 / GPT-4 use this |
| Vocabulary | The set of all tokens a model can recognize | GPT-2: 50,257; GPT-4: ~100,256 |
| Pre-tokenization | Splitting text into "words" using regex before applying BPE | Encodes assumptions about spaces, numbers, contractions |
| UTF-8 | Standard encoding mapping Unicode characters to 1-4 bytes | GPT tokenizers operate on UTF-8 bytes |
| Special Token | Reserved token ID with a specific semantic meaning | `<\|endoftext\|>`, `<\|startoftext\|>` |
| Context Window | Maximum number of tokens a model can process at once | GPT-4: 8,192 / 32,128 / 128,000 tokens |
| Subword | A token that is smaller than a word but larger than a byte | The "subword" in subword tokenization |
| Unigram LM | Alternative to BPE that uses a language model to find optimal tokenization | Used by T5, some SentencePiece variants |
| SentencePiece | A language-agnostic tokenizer that does not require pre-tokenization | Used by LLaMA, T5 |
| WordPiece | Greedy longest-match-first tokenization algorithm | Used by BERT |
| tiktoken | OpenAI's fast BPE tokenization library | Source of truth for OpenAI model tokenizers |
| Byte-level BPE | BPE applied to raw UTF-8 bytes rather than characters | Can encode any Unicode string |

---

## Detailed Definitions

### Tokenization

**Definition:** The process of converting raw text into a sequence of integers (token IDs) that a neural network can process. The tokenizer provides a deterministic, invertible mapping between text and token IDs.

## Example

```python
"hello world" → [31373, 995]  (GPT-2 tokenizer)
```

**Related Terms:** Token, Byte Pair Encoding, Vocabulary

- The only non-learned component of the LLM pipeline.
- All tokenizer limitations are inherited by the model.
- Different models require different tokenizers.

---

### Token

**Definition:** A unit of text represented by a single integer ID in the model's vocabulary. A token can be a whole word, a subword, a single character, or part of a byte sequence depending on the vocabulary.

## Example

```python
"hello" → [31373]  (1 token — common word)
"supercalifragilistic" → [sup, er, cal, ifrag, il, istic]  (6 tokens — rare word)
```

**Related Terms:** Tokenization, Vocabulary, Subword

- Common words are typically single tokens.
- Rare words are split into multiple tokens.
- The number of tokens determines context budget usage.

---

### Byte Pair Encoding (BPE)

**Definition:** An algorithm that starts with a vocabulary of individual bytes (256 tokens) and iteratively merges the most frequent adjacent pair, adding the merged pair as a new token. Repeats until the vocabulary reaches the desired size.

## Example

```text
Training: "aaabdaaabac"
Step 0: [a, a, a, b, d, a, a, a, b, a, c]
Step 1: merge "aa" → Z: [Z, Z, b, d, Z, Z, b, a, c]
Step 2: merge "Zb" → Y: [Z, Z, Y, d, Z, Z, Y, a, c]
...
```

**Related Terms:** Tokenization, Vocabulary, Subword

- Used by: GPT-2, GPT-3, GPT-4, many other LLMs.
- Finds optimal balance between byte-level and word-level tokenization.
- Naturally compresses common substrings into single tokens.

---

### Vocabulary

**Definition:** The complete set of token IDs a model can recognize and generate. Each token has a learned embedding vector that maps it into the model's internal representation space.

## Example

```python
# GPT-2: 50,257 tokens (50,256 BPE merges + 1 special token)
# GPT-4: ~100,256 tokens (improved coverage for code and multilingual text)
# LLaMA: 32,000 tokens (SentencePiece, byte-level)
```

**Related Terms:** Token, Tokenization, Embedding

- Larger vocabulary = more parameters in the embedding layer.
- Must be matched exactly between training and inference.
- Vocabulary can be extended with new tokens for fine-tuning.

---

### Pre-tokenization

**Definition:** The step before BPE that splits text into "words" using a regular expression. Each "word" then receives BPE merges independently, preventing merges across word boundaries.

## Example

```python
# GPT-2 pattern splits on spaces, punctuation, numbers:
"hello world!" → ["hello", " world", "!"]
"I'm #1" → ["I", "'m", " #", "1"]
```

**Related Terms:** Tokenization, Byte Pair Encoding

- The regex encodes design decisions about what constitutes a word.
- Spaces are attached to the *following* word, not the preceding one.
- This is why "hello" and "hello " tokenize differently.

---

### UTF-8

**Definition:** A variable-width encoding for Unicode characters that uses 1-4 bytes per character. ASCII characters take 1 byte; extended Latin, Greek, etc., take 2 bytes; most CJK characters take 3 bytes; emoji and some rare characters take 4 bytes.

## Example

```python
'a' → 1 byte:  [97]
'é' → 2 bytes: [195, 169]
'中' → 3 bytes: [228, 184, 173]
'🌍' → 4 bytes: [240, 159, 140, 141]
```

**Related Terms:** Tokenization, Byte-level BPE

- GPT tokenizers operate on UTF-8 byte representations.
- Multilingual text uses more bytes per character, thus more tokens.

---

### Special Token

**Definition:** Reserved token IDs with specific semantic meaning, such as marking boundaries, padding sequences, or controlling generation behavior.

## Example

```python
# GPT-2 special tokens:
<|endoftext|>  → ID 50256

# GPT-4 also uses:
<|im_start|>   → marks start of a message
<|im_end|>     → marks end of a message
```

**Related Terms:** Tokenization, Vocabulary, Context Window

- Special tokens count toward the context budget.
- The model learns embeddings for special tokens during training.
- Mismatched special tokens cause generation errors.

---

### Context Window

**Definition:** The maximum number of tokens a model can process in a single forward pass, including both prompt and generated tokens. Determined by the position encoding and attention mechanism.

## Example

```python
# GPT-4 variants:
gpt_4_8k:   8,192  tokens
gpt_4_32k:  32,768 tokens
gpt_4_128k: 128,000 tokens  (GPT-4 Turbo)
```

**Related Terms:** Token, Tokenization

- Total = prompt tokens + completion tokens must fit in the window.
- Multilingual and code content uses more tokens per semantic unit.
- Hitting the limit causes truncation or errors.

---

### Subword

**Definition:** A token that is smaller than a word but larger than a single character or byte. Subword tokenization (like BPE) finds the optimal granularity by learning which substrings are most common.

## Example

```text
"unbelievable" → ["un", "believ", "able"]
"tokenization" → ["token", "ization"]
```

**Related Terms:** Byte Pair Encoding, WordPiece, Unigram LM

- The key insight of modern tokenization.
- Balances vocabulary size against sequence length.
- Rare words are kept as byte sequences; common ones are merged.

---

### Unigram LM

**Definition:** A tokenization algorithm that uses a language model to find the most likely tokenization of a text. Unlike BPE (which is deterministic and greedy), Unigram scores all possible tokenizations and picks the one with the highest probability.

**Related Terms:** Byte Pair Encoding, SentencePiece, Subword

- Used by T5 and some SentencePiece configurations.
- More flexible than BPE but more complex.
- Can produce multiple valid tokenizations for the same text.

---

### SentencePiece

**Definition:** A language-agnostic tokenization library (Google, 2018) that treats text as a raw byte stream without requiring pre-tokenization. It can use either BPE or Unigram LM as its algorithm.

## Example

```python
# SentencePiece represents spaces as underscores:
text = "hello world"
# SentencePiece tokens: ["▁hello", "▁world"]
```

**Related Terms:** Unigram LM, Byte Pair Encoding, Pre-tokenization

- Used by LLaMA, T5, and many other open models.
- No dependency on language-specific pre-tokenization regex.
- Handles any Unicode text without modification.

---

### WordPiece

**Definition:** A greedy tokenization algorithm (used by BERT) that builds a vocabulary from the most frequent substrings, then tokenizes new text by finding the longest vocabulary match starting from each position.

**Related Terms:** Byte Pair Encoding, Subword, Pre-tokenization

- Used by BERT and its variants.
- Greedy longest-match-first differs from BPE's frequency-based merging.
- Requires a separate pre-tokenization step (whitespace + punctuation).

---

### tiktoken

**Definition:** OpenAI's fast BPE tokenization library, written in Rust with Python bindings. It is the canonical implementation of the GPT-2, GPT-3, and GPT-4 tokenizers.

## Example

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer
tokens = enc.encode("hello world")
```

**Related Terms:** Byte Pair Encoding, Tokenization, Vocabulary

- Much faster than Python-only implementations.
- Includes encoder/decoder for all OpenAI tokenizers.
- The source of truth for token counting in OpenAI API usage.

---

### Byte-level BPE

**Definition:** BPE applied to raw UTF-8 bytes rather than Unicode characters or codepoints. This allows the tokenizer to handle any possible Unicode string without having to know about Unicode structure.

**Related Terms:** Byte Pair Encoding, UTF-8, SentencePiece

- Guarantees no out-of-vocabulary (OOV) tokens.
- All strings can be represented, even those with characters not seen during training.
- More efficient than character-level but less efficient than word-level.

---

## Summary

1. **Tokenization** converts text to integer sequences — it is the only hand-designed component in the LLM pipeline.
2. **BPE** builds a vocabulary of ~50k–100k tokens by iteratively merging frequent byte pairs.
3. **Pre-tokenization** regex splits text into words before BPE, encoding design choices about spaces, numbers, and punctuation.
4. **UTF-8** byte representation means any Unicode text can be tokenized, but multilingual text uses more tokens.
5. **Special tokens** and **context windows** constrain how many tokens can be processed at once.
6. **Different architectures** (BPE, Unigram LM, WordPiece, SentencePiece) encode different design trade-offs.
7. **`tiktoken`** is the reference implementation for OpenAI's tokenizers.
8. **Tokenization affects model behavior, cost, and capability** — understanding it is essential for LLM application development.
