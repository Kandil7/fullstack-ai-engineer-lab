"""
11 - GPT Tokenizer: Tokenization in LLMs
=========================================
Goal: Understand how LLMs convert text to token IDs and back. You will
implement a character-level tokenizer, a simplified BPE, and use OpenAI's
tiktoken library to explore real tokenization behavior.

You will:
  1. Build a character-level tokenizer (baseline).
  2. Implement BPE from scratch.
  3. Use tiktoken to explore GPT-2/GPT-4 tokenization.
  4. Analyze token counts and compression ratios across languages.
  5. Debug surprising tokenization behaviors.

Prerequisites:
  pip install tiktoken    (for parts 3-5; parts 1-2 use stdlib only)

Run:
  python 11-gpt-tokenizer.py
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Callable


# ============================================================
# 1. Character-Level Tokenizer (Baseline)
# ============================================================
class CharTokenizer:
    """The simplest possible tokenizer — one token per character.

    This is NOT what LLMs use, but it establishes the baseline that
    BPE improves upon. Every unique character in the training text
    becomes a vocabulary entry.
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
        """Convert token IDs back to text."""
        return "".join(self._itos[i] for i in ids)


# ============================================================
# 2. Simplified BPE Implementation
# ============================================================
class BPE:
    """A minimal Byte Pair Encoding tokenizer for educational purposes.

    This implements the core BPE algorithm: start with raw bytes,
    iteratively merge the most frequent adjacent pair, and build
    up a vocabulary of merged tokens.

    The REAL GPT tokenizer adds:
      - Regex pre-tokenization before BPE
      - Byte-level encoding (always works on UTF-8 bytes)
      - Special tokens for control
    """

    def __init__(self, vocab_size: int = 300) -> None:
        self.vocab_size = vocab_size
        self.merges: dict[tuple[int, int], int] = {}
        self._vocab: dict[int, bytes] = {}

    def _get_stats(self, ids: list[int]) -> Counter:
        """Count adjacent pair frequencies."""
        return Counter(zip(ids, ids[1:]))

    @staticmethod
    def _merge(ids: list[int], pair: tuple[int, int], new_idx: int) -> list[int]:
        """Replace all occurrences of ``pair`` with ``new_idx``."""
        merged: list[int] = []
        i = 0
        while i < len(ids):
            if i < len(ids) - 1 and (ids[i], ids[i + 1]) == pair:
                merged.append(new_idx)
                i += 2
            else:
                merged.append(ids[i])
                i += 1
        return merged

    def train(self, text: str) -> None:
        """Learn BPE merges from training text."""
        ids = list(text.encode("utf-8"))
        self._vocab = {i: bytes([i]) for i in range(256)}
        next_idx = 256

        while len(self._vocab) < self.vocab_size:
            stats = self._get_stats(ids)
            if not stats:
                break
            (pair, _), = stats.most_common(1)
            self.merges[pair] = next_idx
            self._vocab[next_idx] = self._vocab[pair[0]] + self._vocab[pair[1]]
            ids = self._merge(ids, pair, next_idx)
            next_idx += 1

    def encode(self, text: str) -> list[int]:
        """Encode text into token IDs using learned merges."""
        ids = list(text.encode("utf-8"))
        while len(ids) >= 2:
            stats = self._get_stats(ids)
            candidate_pairs = [p for p in stats if p in self.merges]
            if not candidate_pairs:
                break
            pair = min(candidate_pairs, key=lambda p: self.merges[p])
            ids = self._merge(ids, pair, self.merges[pair])
        return ids

    def decode(self, ids: list[int]) -> str:
        """Decode token IDs back to text."""
        return b"".join(self._vocab[i] for i in ids).decode("utf-8", errors="replace")


# ============================================================
# 3. Token Analysis Utilities
# ============================================================
def analyze_tokenization(
    text: str,
    encoder: Callable[[str], list[int]],
    decoder: Callable[[list[int]], str],
    name: str = "unknown",
) -> dict:
    """Analyze how text is tokenized: count tokens, check reconstruction."""
    tokens = encoder(text)
    reconstructed = decoder(tokens)
    n_tokens = len(tokens)
    n_chars = len(text)
    ratio = n_tokens / n_chars if n_chars > 0 else 0

    return {
        "name": name,
        "text": text,
        "n_chars": n_chars,
        "n_tokens": n_tokens,
        "compression_ratio": round(ratio, 4),
        "reconstructed_ok": text == reconstructed,
        "tokens": tokens,
    }


def compression_report(results: list[dict]) -> str:
    """Generate a report comparing tokenization across methods/languages."""
    lines = [f"{'Method':<20} {'Chars':>6} {'Tokens':>8} {'Ratio':>8} {'Match?':>8}", "=" * 50]
    for r in results:
        ok = "[OK]" if r["reconstructed_ok"] else "[FAIL]"
        lines.append(
            f"{r['name']:<20} {r['n_chars']:>6} {r['n_tokens']:>8} "
            f"{r['compression_ratio']:>8.4f} {ok:>8}"
        )
    return "\n".join(lines)


# ============================================================
# 4. GPT-2 Pre-tokenization Pattern
# ============================================================
# GPT-2 pre-tokenization uses Unicode property escapes (\p{L}, \p{N})
# which require the ``regex`` library. The pattern is stored as a source
# string so it can be compiled by whichever regex engine is available.
GPT2_PATTERN_SOURCE = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""


def gpt2_pretokenize(text: str) -> list[str]:
    """Simulate GPT-2's pre-tokenization regex step.

    Uses the ``regex`` library (which supports ``\\p{L}`` / ``\\p{N}``
    Unicode property escapes) if available; falls back to a simplified
    ASCII-only approximation with ``re`` otherwise.
    """
    try:
        import regex as _rx
        return _rx.findall(GPT2_PATTERN_SOURCE, text)
    except ImportError:
        # Fallback: ASCII-only approximation of the GPT-2 pattern
        _approx = re.compile(
            r"""'(?:[sdmt]|ll|ve|re)| ?[a-zA-Z]+| ?[0-9]+| ?[^\s\w]+|\s+(?!\S)|\s+""",
            re.UNICODE,
        )
        return _approx.findall(text)


# ============================================================
# 5. Main Demonstration
# ============================================================
def main() -> None:
    from random import Random
    rng = Random(42)
    sample_text = (
        "The quick brown fox jumps over the lazy dog! "
        "It was 2024, and AI had advanced significantly. "
        "Hello, World! Can't you see? I've been waiting. "
        "Numbers: 3.14159, 42, 1000000. "
        "Unicode: café, résumé, naïve, 🌍🌎🌏."
    )

    # ---- Part 1: Character-Level Baseline ----
    print("=" * 60)
    print("1. Character-Level Tokenizer (Baseline)")
    print("=" * 60)
    char_tokenizer = CharTokenizer(sample_text)
    char_tokens = char_tokenizer.encode(sample_text)
    char_decoded = char_tokenizer.decode(char_tokens)
    print(f"Vocabulary size: {char_tokenizer.vocab_size}")
    print(f"Tokens for sample: {len(char_tokens)} chars = {len(sample_text)}")
    print(f"Reconstruction OK: {sample_text == char_decoded}")
    print()

    # ---- Part 2: BPE from Scratch ----
    print("=" * 60)
    print("2. BPE from Scratch")
    print("=" * 60)
    training_text = sample_text * 20  # amplify patterns
    bpe = BPE(vocab_size=300)
    bpe.train(training_text)
    bpe_tokens = bpe.encode(sample_text)
    bpe_decoded = bpe.decode(bpe_tokens)
    print(f"Trained {len(bpe.merges)} merges (vocab={bpe.vocab_size})")
    print(f"Tokens for sample: {len(bpe_tokens)}")
    print(f"Reconstruction OK: {sample_text == bpe_decoded}")
    print(f"Compression: {len(bpe_tokens)} BPE tokens vs {len(sample_text.encode('utf-8'))} raw bytes")
    print()

    # Show the top 10 most common merges
    def _safe(s: str) -> str:
        """Sanitize string for terminal output (replace \ufffd)."""
        return s.replace("\ufffd", "[?]").replace("\u2192", "->")

    print("Top 10 learned merges:")
    sorted_merges = sorted(bpe.merges.items(), key=lambda x: x[1])[:10]
    for (a, b), idx in sorted_merges:
        a_str = _safe(bpe._vocab[a].decode("utf-8", errors="replace"))
        b_str = _safe(bpe._vocab[b].decode("utf-8", errors="replace"))
        merged = _safe(bpe._vocab[idx].decode("utf-8", errors="replace"))
        print(f"  {a_str!r} + {b_str!r} -> {merged!r}  (token ID {idx})")
    print()

    # ---- Part 3: Token Analysis (if tiktoken available) ----
    print("=" * 60)
    print("3. Real Tokenizer Analysis (tiktoken)")
    print("=" * 60)
    try:
        import tiktoken

        enc_gpt2 = tiktoken.get_encoding("gpt2")
        enc_gpt4 = tiktoken.get_encoding("cl100k_base")

        results = [
            analyze_tokenization(sample_text, char_tokenizer.encode, char_tokenizer.decode, "Char-level"),
            analyze_tokenization(sample_text, bpe.encode, bpe.decode, "DIY BPE"),
        ]

        if enc_gpt2:
            results.append(
                analyze_tokenization(sample_text, enc_gpt2.encode, lambda t: enc_gpt2.decode(t), "GPT-2")
            )
        if enc_gpt4:
            results.append(
                analyze_tokenization(sample_text, enc_gpt4.encode, lambda t: enc_gpt4.decode(t), "GPT-4")
            )

        print(compression_report(results))
        print()

        # Show how the GPT-2 tokenizer handles specific examples
        print("GPT-2 tokenization details:")
        for example in ["hello world", "I don't know", "3.14159", "cafe", "globe", "1000000"]:
            tokens = enc_gpt2.encode(example)
            decoded_bytes = [enc_gpt2.decode_single_token_bytes(t) for t in tokens]
            print(f"  {example!r:25s} -> {str(tokens):30s} -> {str(decoded_bytes)}")
        print()

        # Language comparison
        print("Token count by language (GPT-4 tokenizer):")
        languages = {
            "English": "The quick brown fox jumps over the lazy dog.",
            "Spanish": "El rápido zorro marrón salta sobre el perro perezoso.",
            "French": "Le renard brun rapide saute par-dessus le chien paresseux.",
            "German": "Der schnelle braune Fuchs springt über den faulen Hund.",
            "Chinese": "敏捷的棕色狐狸跳过了懒狗。",
            "Arabic": "الثعلب البني السريع يقفز فوق الكلب الكسول.",
            "Japanese": "素早い茶色の狐が怠け者の犬を飛び越える。",
        }
        for lang, text in languages.items():
            tokens = enc_gpt4.encode(text)
            ratio = len(tokens) / len(text)
            print(f"  {lang:<12} {len(text):>4} chars -> {len(tokens):>3} tokens (ratio: {ratio:.3f})")

    except ImportError:
        print("tiktoken not installed. Install with: pip install tiktoken")
        print("Skipping real tokenizer analysis.")
    print()

    # ---- Part 4: Pre-tokenization Demo ----
    print("=" * 60)
    print("4. GPT-2 Pre-tokenization Pattern")
    print("=" * 60)
    for example in ["hello world", "  hello world  ", "I'm learning! #1", "123-456-7890"]:
        pieces = gpt2_pretokenize(example)
        print(f"  {example!r:25s} -> {pieces}")
    print()

    # ---- Part 5: Exercise Prompts ----
    print("=" * 60)
    print("5. Exercises")
    print("=" * 60)
    print("""
EXERCISE 1 — BPE Training Data Sensitivity
  Train the BPE tokenizer on English-only text vs multilingual text.
  Compare the merge lists: which languages benefit from multilingual training?

EXERCISE 2 — Context Budget Calculator
  Write a function that takes a prompt and a model name, then returns:
    - Token count for the prompt
    - Percentage of context window used
    - Estimated cost (if you have pricing)
  Test it on prompts of different lengths and languages.

EXERCISE 3 — Tokenization Edge Cases
  Find 5 examples where tokenization behaves counterintuitively.
  For each, explain *why* the tokenizer produces that result.
  Hint: try numbers, whitespace, punctuation, and emoji combinations.

EXERCISE 4 — Custom Regex Exploration
  Modify the GPT2_PATTERN_SOURCE string. How do changes affect tokenization?
  Try: removing digit handling, changing space attachment, or adding
  new punctuation types.

EXERCISE 5 — Token ID Stability
  Train the same BPE tokenizer twice with the same text but different
  random seeds. Compare the resulting merge orders. Are they identical?
  What does this tell you about BPE's determinism?
""")


if __name__ == "__main__":
    main()
