# Lecture 11: Let's Build the GPT Tokenizer — A Complete Guide to Tokenization in LLMs

## Topic Overview

In October 2025, fast.ai published "Let's Build the GPT Tokenizer" — a text-and-code adaptation of Andrej Karpathy's famous 2-hour-13-minute YouTube tutorial, transformed into a structured book chapter using the Solveit platform (Lecture 10). This lecture covers the complete guide to tokenization in Large Language Models (LLMs).

**Tokenization is the bridge between human language and neural network math.** Every LLM — from GPT-2 to GPT-4 to Claude — converts text into sequences of integers (tokens) before processing them. The seemingly simple choice of *how* to do this conversion shapes everything about model behavior: spelling ability, multilingual performance, arithmetic capability, and even context window utilization.

Understanding tokenization is essential because **many model quirks trace directly to the tokenizer, not the neural network.** Poor spelling? The model works on tokens, not characters. Trouble with non-English languages? The tokenizer was trained on English-dominated data. Can't reverse a string easily? Tokens don't align with characters.

**Duration:** 3–4 hours  
**Difficulty:** Intermediate  
**Prerequisites:** Lecture 01 (Getting Started), Lecture 05 (From-Scratch Model), basic Python

---

## Learning Objectives

By the end of this lecture you will be able to:

1. **Explain** why raw text cannot be fed directly into a neural network and why tokenization is necessary.
2. **Implement** character-level encoding and decoding as a baseline.
3. **Describe** the Byte Pair Encoding (BPE) algorithm and its role in modern LLM tokenizers.
4. **Trace** how a GPT tokenizer converts text → BPE tokens → integer sequences and back.
5. **Identify** common model behaviors that are caused by tokenization, not the neural network itself.
6. **Analyze** the trade-offs between vocabulary size, sequence length, and encoding efficiency.
7. **Compare** the GPT-2, GPT-4, and SentencePiece tokenizer architectures.
8. **Debug** tokenization edge cases: whitespace handling, Unicode normalization, and special tokens.

---

## Key Concepts

### 1. Why Tokenization Matters

LLMs cannot process raw text. They operate on sequences of integers (tokens), where each token represents an index into a fixed-size vocabulary. The tokenizer's job is to provide a **deterministic, invertible mapping** between text and token IDs.

The tokenizer is the **only non-learned component of the LLM pipeline** — it is hand-designed with specific rules and heuristics. This means **all of its quirks and limitations are inherited by the model.**

```text
Raw text: ──▶ Tokenizer ──▶ Token IDs ──▶ Embedding ──▶ Transformer ──▶ ...
                ▲
                │
            Hand-designed rules
            (not learned from data)
```

#### Common behavior sources rooted in tokenization:

- **Poor spelling:** Text "hellooo" vs "hello" produces completely different token sequences, making the model appear bad at spelling.
- **Non-English performance:** Tokenizers are trained on primarily English text, so words in other languages get fragmented into many tokens, using up context budget and reducing performance.
- **String reversal:** The model cannot reverse a string because tokens have no notion of character order within a token.
- **Simple arithmetic:** Numbers are tokenized inconsistently (e.g., "380" might be one token, but "381" might be two), making arithmetic unreliable.
- **Trailing whitespace:** "hello" and "hello " (with a space) tokenize differently, which can produce confusing behavior.

### 2. From Characters to Bytes: The Encoding Problem

The Unicode standard defines roughly 150,000 characters — too many for a practical vocabulary. The standard encoding UTF-8 maps each Unicode character to 1–4 bytes and is backward-compatible with ASCII.

```python
# A single Unicode character can be 1-4 bytes in UTF-8
text = "hello"
bytes = text.encode("utf-8")
print(list(bytes))  # [104, 101, 108, 108, 111]  — one byte per ASCII char

text = "héllo"
bytes = text.encode("utf-8")
print(list(bytes))  # [104, 195, 169, 108, 108, 111]  — 'é' is 2 bytes

text = "🌍"
bytes = text.encode("utf-8")
print(list(bytes))  # [240, 159, 140, 141]  — emoji is 4 bytes
```

If we tokenize at the byte level, our vocabulary is only 256 tokens — but every text becomes a very long sequence, which is inefficient for the transformer's context window.

#### The trade-off:

| Approach | Vocabulary | Sequence Length | Problems |
|----------|-----------|----------------|----------|
| Character-level | ~150,000 (Unicode) | ~same as text length | Huge vocabulary, unstable |
| Byte-level | 256 | ~1-4x text length | Very long sequences, wastes context |
| Word-level | ~100,000+ | ~short sequences | Huge vocabulary, OOV words |
| **Subword (BPE)** | **~50,000** | **~1.3x word-level** | **Best balance** |

### 3. Byte Pair Encoding (BPE)

**Byte Pair Encoding** is the algorithm used by GPT-2, GPT-3, GPT-4, and many other LLMs. It finds the optimal middle ground between byte-level and word-level tokenization.

#### How BPE works:

1. **Start** with a vocabulary of all individual bytes (256 tokens).
2. **Count** the frequency of every adjacent pair of tokens in your training corpus.
3. **Merge** the most frequent pair into a new token, adding it to the vocabulary.
4. **Repeat** until the vocabulary reaches the desired size (e.g., 50,257 for GPT-2).

```text
Training corpus: "aaabdaaabac"

Step 0: tokens = [a, a, a, b, d, a, a, a, b, a, c]
         pair frequencies: aa=5, ab=3, bd=1, da=1, ac=1

Step 1: merge "aa" → Z
        tokens = [Z, Z, b, d, Z, Z, b, a, c]
        pair frequencies: ZZ=2, Zb=2, bd=1, dZ=1, Zb=2, ba=1, ac=1

Step 2: merge "Zb" → Y
        tokens = [Z, Z, Y, d, Z, Z, Y, a, c]
        ...

This continues until the vocabulary reaches the target size.
```

#### BPE in practice:

BPE naturally compresses common substrings (like "tion", "ing", "the") into single tokens, while rare words remain as multiple tokens. This gives a good balance:

```text
Common:     "hello" → [hello]           (1 token)
            "world" → [world]           (1 token)

Rare:       "supercalifragilistic" → [sup, er, cal, ifrag, il, istic]  (~6 tokens)

Numbers:    "100" → [100]               (1 token)
            "1001" → [100, 1]           (2 tokens — depends on training data)
```

#### The GPT-2 tokenizer (tiktoken):

OpenAI's `tiktoken` library implements BPE with some important details:

- **Vocabulary size:** 50,257 tokens (50,256 BPE merges + 1 special `<|endoftext|>` token)
- **Byte-level:** operates on UTF-8 bytes, not characters — so it can encode any Unicode string
- **Regex pre-tokenization:** splits text into words using a GPT-specific regex pattern before applying BPE within each word. This prevents merges across word boundaries, keeping common words intact.

```python
import tiktoken

enc = tiktoken.get_encoding("gpt2")
tokens = enc.encode("hello world")
print(tokens)       # [31373, 995]  — two tokens
print(enc.decode(tokens))  # "hello world"

# GPT-4 uses "cl100k_base" with a different pre-tokenization regex
enc_gpt4 = tiktoken.get_encoding("cl100k_base")
tokens_gpt4 = enc_gpt4.encode("hello world")
print(tokens_gpt4)  # [15339, 1917]
```

### 4. Pre-Tokenization: The Regex Step

Before BPE, GPT tokenizers split text into "words" using a carefully designed regular expression. This regex encodes many design decisions:

```python
import regex

# GPT-2's pre-tokenization pattern (simplified)
GPT2_SPLIT_PATTERN = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

def gpt2_pretokenize(text: str) -> list[str]:
    """Split text into 'words' that become the units for BPE."""
    return regex.findall(GPT2_SPLIT_PATTERN, text)


# Examples:
# "hello world" → ["hello", " world"]     (space belongs to the *next* word)
# "I'm learning" → ["I", "'m", " learning"]
# "123 abc!" → ["123", " abc", "!"]
```

Key design choices encoded in the regex:

- **Space before words:** Spaces are attached to the *following* word, not the preceding one. This means "hello world" and "hello  world" (two spaces) tokenize differently.
- **Numbers are separate:** Digit sequences are isolated so the model can learn arithmetic.
- **Contractions split:** "don't" → ["don", "'t"], making it easier for the model to handle grammatical variations.

### 5. Special Tokens

LLMs reserve specific token IDs for special purposes:

| Token | ID (GPT-2) | Purpose |
|-------|-----------|---------|
| `<|endoftext|>` | 50256 | Marks end of text / separator between documents |
| `<|startoftext|>` | (varies) | Some models use this (e.g., CLIP) |
| `<pad>` | (varies) | Padding for batch processing |
| Extras | 50257+ | May be added for fine-tuning tasks |

### 6. How Other Tokenizers Differ

| Model | Tokenizer | Vocab Size | Pre-tokenization | Special Features |
|-------|-----------|------------|-----------------|------------------|
| GPT-2 | BPE (tiktoken) | 50,257 | Regex + byte-level | The original GPT approach |
| GPT-4 | BPE (cl100k_base) | 100,256 | Improved regex | Better multilingual, more tokens |
| LLaMA | SentencePiece (BPE) | 32,000 | Byte-level, no regex | Does not require pre-tokenization |
| T5 | SentencePiece (Unigram) | 32,000 | Whitespace-based | Unigram LM instead of BPE |
| BERT | WordPiece | 30,000 | Whitespace + punctuation | Greedy longest-match-first |

**SentencePiece** (used by LLaMA and T5) is notable because it does not require pre-tokenization — it treats the raw byte stream directly, making it language-agnostic. It also handles whitespace by replacing spaces with `▁` (a special underscore character).

### 7. Tokenization as a Source of Model Behavior

Understanding the tokenizer helps explain many observed LLM behaviors:

```text
BEHAVIOR: The model is bad at spelling "hippopotamus" backward.
CAUSE:    The word is tokenized as [hipp, op, ot, amus] — the model
          sees 4 tokens with no knowledge of character ordering within each.

BEHAVIOR: The model handles French poorly compared to English.
CAUSE:    French words get split into 2-3× more tokens than English
          equivalents, consuming the context budget faster.

BEHAVIOR: "3.14" and "3,14" produce different answers to math questions.
CAUSE:    Different tokenization of the decimal separator.

BEHAVIOR: The model cannot reliably count characters in a string.
CAUSE:    The model operates on tokens, which have variable length in characters.
```

---

## Code Examples

### Example 1: Building a Character-Level Tokenizer

A minimal tokenizer for educational purposes — this is what BPE improves upon.

```python
"""Character-level tokenizer — the simplest possible approach."""

from __future__ import annotations


class CharTokenizer:
    """Tokenize text at the character level.

    This is NOT what GPT uses — it's the baseline that BPE improves upon.
    Vocabulary grows with the number of unique characters in the training text.
    """

    def __init__(self, text: str) -> None:
        chars = sorted(set(text))
        self.vocab_size = len(chars)
        self._stoi: dict[str, int] = {c: i for i, c in enumerate(chars)}
        self._itos: dict[int, str] = {i: c for c, i in self._stoi.items()}

    def encode(self, text: str) -> list[int]:
        """Convert text to a sequence of integer token IDs."""
        return [self._stoi[c] for c in text]

    def decode(self, ids: list[int]) -> str:
        """Convert a sequence of token IDs back to text."""
        return "".join(self._itos[i] for i in ids)


# Usage:
tokenizer = CharTokenizer("hello world")
print(tokenizer.encode("world"))   # [5, 4, 6, 3, 2]
print(tokenizer.decode([5, 4, 6, 3, 2]))  # "world"
```

### Example 2: Implementing BPE from Scratch

A simplified implementation that shows the core merge logic.

```python
"""Minimal BPE implementation for educational purposes."""

from __future__ import annotations

from collections import Counter
from typing import Dict, List, Tuple


class BPE:
    """Byte Pair Encoding tokenizer.

    This is a simplified version of what GPT-2 uses.
    The real GPT tokenizer adds regex pre-tokenization and byte-level encoding.
    """

    def __init__(self, vocab_size: int = 300) -> None:
        self.vocab_size = vocab_size
        self.merges: dict[tuple[int, int], int] = {}
        self._vocab: dict[int, bytes] = {}

    def _get_stats(self, ids: list[int]) -> Counter:
        """Count adjacent pairs."""
        pairs = Counter()
        for pair in zip(ids, ids[1:]):
            pairs[pair] += 1
        return pairs

    def _merge(self, ids: list[int], pair: tuple[int, int], new_idx: int) -> list[int]:
        """Replace all occurrences of ``pair`` with ``new_idx``."""
        merged: list[int] = []
        i = 0
        while i < len(ids):
            if i < len(ids) - 1 and (ids[i], ids[i+1]) == pair:
                merged.append(new_idx)
                i += 2
            else:
                merged.append(ids[i])
                i += 1
        return merged

    def train(self, text: str) -> None:
        """Learn BPE merges from training text."""
        ids = list(text.encode("utf-8"))  # start with raw bytes
        self._vocab = {i: bytes([i]) for i in range(256)}
        next_idx = 256

        while len(self._vocab) < self.vocab_size:
            stats = self._get_stats(ids)
            if not stats:
                break
            (most_common_pair, _), = stats.most_common(1)
            self.merges[most_common_pair] = next_idx
            self._vocab[next_idx] = self._vocab[most_common_pair[0]] + self._vocab[most_common_pair[1]]
            ids = self._merge(ids, most_common_pair, next_idx)
            next_idx += 1

    def encode(self, text: str) -> list[int]:
        """Encode text into token IDs using learned merges."""
        ids = list(text.encode("utf-8"))
        while len(ids) >= 2:
            stats = self._get_stats(ids)
            # Find the earliest mergeable pair
            pair = min(stats.keys(), key=lambda p: self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break
            ids = self._merge(ids, pair, self.merges[pair])
        return ids

    def decode(self, ids: list[int]) -> str:
        """Decode token IDs back to text."""
        return b"".join(self._vocab[i] for i in ids).decode("utf-8", errors="replace")


# Usage:
bpe = BPE(vocab_size=300)
bpe.train("aaabdaaabac" * 100)
encoded = bpe.encode("aaabdaaabac")
print(f"Encoded: {encoded}")
print(f"Decoded: {bpe.decode(encoded)}")
```

### Example 3: Real Tokenization with tiktoken

Using OpenAI's actual tokenizer to explore token behavior.

```python
"""Exploring tokenization with OpenAI's tiktoken library."""

from __future__ import annotations

import tiktoken


def explore_tokenizer(name: str = "gpt2") -> None:
    """Explore how different texts are tokenized."""
    enc = tiktoken.get_encoding(name)

    examples = [
        "hello world",
        "hello  world",
        "Hello, World!",
        "hippopotamus",
        "supercalifragilisticexpialidocious",
        "1234567890",
        "3.14159",
        "I don't know",
        "你好世界",
        "🌍🌎🌏",
        "    leading spaces",
        "trailing spaces   ",
    ]

    print(f"Tokenizer: {name}")
    print(f"Vocab size: {enc.n_vocab}")
    print()

    for text in examples:
        tokens = enc.encode(text)
        decoded = [enc.decode_single_token_bytes(t) for t in tokens]
        print(f"Input:      {text!r}")
        print(f"Tokens:     {tokens}")
        print(f"Bytes:      {decoded}")
        print(f"Decoded:    {enc.decode(tokens)!r}")
        print(f"N tokens:   {len(tokens)}")
        print()


if __name__ == "__main__":
    explore_tokenizer("gpt2")
    print("=" * 60)
    explore_tokenizer("cl100k_base")
```

### Example 4: Counting Tokens (Context Window Budget)

Understanding how many tokens different texts consume is crucial for LLM application development.

```python
"""Analyze token counts for different types of content."""

from __future__ import annotations

import tiktoken


def token_budget_analysis() -> None:
    """Show how different content types consume the context budget."""
    enc = tiktoken.get_encoding("cl100k_base")

    samples = {
        "Short English sentence": "The quick brown fox jumps over the lazy dog.",
        "Long English paragraph": (
            "Machine learning is a method of data analysis that automates "
            "analytical model building. It is a branch of artificial intelligence "
            "based on the idea that systems can learn from data, identify patterns, "
            "and make decisions with minimal human intervention. " * 5
        ),
        "Code snippet": 'def hello(name: str) -> str:\n    return f"Hello, {name}!"\n\nprint(hello("world"))',
        "Chinese text": "机器学习是数据分析的一种方法，它自动化了分析模型的构建过程。" * 10,
        "Mixed content": "Python 是一种优秀的编程语言。Machine learning is fun! 2024年。",
    }

    print(f"{'Content Type':<35} {'Chars':>6} {'Tokens':>7} {'Ratio':>7}")
    print("-" * 55)

    for label, text in samples.items():
        tokens = enc.encode(text)
        ratio = len(tokens) / len(text)
        print(f"{label:<35} {len(text):>6} {len(tokens):>7} {ratio:.3f}")


if __name__ == "__main__":
    token_budget_analysis()
```

---

## Common Mistakes to Avoid

### Mistake 1: Assuming Tokens = Characters

```python
# BAD: assuming one token = one character for string operations
text = "hello world"
tokens = enc.encode(text)
# tokens = [31373, 995] — 2 tokens for 11 characters!

# GOOD: always check token count separately from character count
n_tokens = len(enc.encode(text))
n_chars = len(text)
print(f"{n_tokens} tokens for {n_chars} characters (ratio: {n_tokens/n_chars:.2f})")
```

### Mistake 2: Using the Wrong Tokenizer for a Model

```python
# BAD: using GPT-2 tokenizer with a GPT-4 model
enc = tiktoken.get_encoding("gpt2")
gpt4_tokens = enc.encode("hello")  # Wrong! GPT-4 uses cl100k_base

# GOOD: match the tokenizer to the model
# GPT-4, GPT-3.5-turbo → "cl100k_base"
# GPT-2 → "gpt2"
# text-davinci-003 → "p50k_base"
enc = tiktoken.get_encoding("cl100k_base")  # For GPT-4
```

### Mistake 3: Assuming Tokenization Is Consistent Across Models

```python
# Each model family has its own tokenizer — never assume they match.
gpt2 = tiktoken.get_encoding("gpt2")
gpt4 = tiktoken.get_encoding("cl100k_base")

text = "The quick brown fox jumps over the lazy dog."
tokens_gpt2 = gpt2.encode(text)
tokens_gpt4 = gpt4.encode(text)

print(f"GPT-2: {len(tokens_gpt2)} tokens: {tokens_gpt2}")
print(f"GPT-4: {len(tokens_gpt4)} tokens: {tokens_gpt4}")
# Different lengths and different token IDs!
```

### Mistake 4: Not Accounting for Special Tokens in the Budget

```python
# BAD: forgetting that special tokens consume context budget
prompt = "Translate to French: Hello"
messages = [
    {"role": "system", "content": "You are a translator."},
    {"role": "user", "content": prompt},
]
# The message format adds overhead tokens (roles, markers, etc.)

# GOOD: always count the *actual* tokenized payload
enc = tiktoken.get_encoding("cl100k_base")
full_payload = str(messages)  # In practice, the library handles this
tokens = enc.encode(full_payload)
print(f"Prompt tokens: {len(tokens)}")  # More than just len(enc.encode(prompt))
```

---

## Best Practices

1. **Always use the correct tokenizer** for your model — mismatched tokenizers produce garbage output.
2. **Count tokens before sending prompts** using `tiktoken` or the model provider's tokenizer to stay within the context window.
3. **Be aware of tokenization effects on pricing** — LLM APIs charge per token, so understanding token counts helps control costs.
4. **Plan for multilingual content** — non-English text uses 2-3× more tokens than English, reducing effective context size.
5. **Strip trailing whitespace** before tokenization to avoid unexpected token splits.
6. **Test tokenization of edge cases** — numbers, code, special characters, and whitespace variations often behave unexpectedly.
7. **Consider tokenization when designing prompts** — prefer common words and consistent formatting to minimize token usage.
8. **Use `tiktoken`'s `encode_single_token_bytes` for debugging** to see exactly what each token represents.
9. **Remember that token IDs are model-specific** — never reuse token IDs between different models.
10. **Understand the regex pre-tokenization rules** for your specific tokenizer — they encode assumptions about what constitutes a "word."

---

## Practice Exercises

### Exercise 1: Character-Level Baseline

Implement the `CharTokenizer` class and encode a paragraph of text. Compare the vocabulary size and sequence length to the BPE-based `tiktoken` encoding.

### Exercise 2: Implement BPE

Build the `BPE` class from the code examples and train it on a small corpus (e.g., the text of a news article). Inspect which pairs were merged first and what the resulting tokens represent.

### Exercise 3: Cross-Tokenizer Comparison

Download three different tokenizers (GPT-2, GPT-4, LLaMA via SentencePiece) and compare how they tokenize the same text. Which produces the fewest tokens? The most?

### Exercise 4: Tokenization Debugging

Find three examples where tokenization causes the model to behave unexpectedly (e.g., poor arithmetic, bad spelling, different token counts for similar inputs). Explain each case in terms of the tokenizer's behavior.

### Exercise 5: Build a Token Counter

Write a function that takes a text and a model name and returns the token count, character count, compression ratio, and estimated cost (using the model's per-token pricing).

### Exercise 6: Multi-Language Analysis

Compare token counts for the same message translated into 5 different languages. Which language uses the most tokens per character? Why?

---

## Summary

1. **Tokenization is the bridge between text and neural networks** — and it is the only hand-designed, non-learned component of the LLM pipeline.
2. **Many LLM quirks** (poor spelling, bad arithmetic, multilingual weakness) trace back to the tokenizer, not the neural network.
3. **Byte Pair Encoding (BPE)** is the algorithm behind GPT-2, GPT-3, GPT-4, and many other LLMs: it iteratively merges the most frequent adjacent byte pairs to build a vocabulary of ~50,000–100,000 tokens.
4. **Pre-tokenization regex** splits text into "words" before BPE, encoding design choices about spaces, numbers, contractions, and punctuation.
5. **Different models use different tokenizers** — GPT-2 (50k vocab), GPT-4 (100k vocab), LLaMA (SentencePiece, 32k) — and they are not interchangeable.
6. **Token count = cost and context** — understanding how your text tokenizes helps you control API costs and stay within context windows.
7. **Whitespace, Unicode, numbers, and code** each have specific tokenization behaviors that can surprise you if you do not test them.
8. **Building a BPE tokenizer from scratch** is the best way to understand this critical but often overlooked component of modern LLMs.

**Next:** Return to the Data Ethics module to connect these technical insights with ethical considerations about how tokenization choices affect model performance across languages and communities.

---

## References

- Karpathy, A. (2025). "Let's build the GPT Tokenizer." *Via fast.ai/Solveit.* [YouTube](https://www.youtube.com/watch?v=zduSFxRajkE)
- OpenAI. (2022). `tiktoken` — A fast BPE tokeniser for use with OpenAI's models. [GitHub](https://github.com/openai/tiktoken)
- Sennrich, R., Haddow, B., & Birch, A. (2016). "Neural Machine Translation of Rare Words with Subword Units." *ACL 2016.* [BPE paper](https://aclanthology.org/P16-1162/)
- Karpathy, A. "Neural Networks: Zero to Hero" series. [karpathy.ai](https://karpathy.ai/zero-to-hero.html)
