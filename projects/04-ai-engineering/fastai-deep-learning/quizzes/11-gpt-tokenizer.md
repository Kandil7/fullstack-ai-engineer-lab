# Quiz 11: GPT Tokenizer — Tokenization in LLMs

## Topic Overview

This quiz covers LLM tokenization: why it matters, how Byte Pair Encoding (BPE) works, the role of pre-tokenization, handling of Unicode and special tokens, and how tokenization affects model behavior and cost.

---

## Questions

### Question 1

**Why do neural networks need tokenization?**

- A) Text is too large to store on disk
- B) Neural networks process sequences of integers, not raw text
- C) Tokenization makes text run faster
- D) It is an optional optimization for long documents

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** LLMs operate on sequences of integers (token IDs). The tokenizer provides the deterministic, invertible mapping between human language (text) and the format the neural network can process (integers). It is the only non-learned, hand-designed component of the pipeline.

</details>

---

### Question 2

**What is Byte Pair Encoding (BPE)?**

- A) A compression algorithm for images
- B) An algorithm that iteratively merges the most frequent adjacent byte pairs to build a vocabulary
- C) A method for encoding floating-point numbers
- D) A type of neural network architecture

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** BPE starts with all 256 individual byte values, counts the frequency of every adjacent pair in the training corpus, and merges the most frequent pair into a new token. It repeats this process until the vocabulary reaches the desired size (e.g., 50,257 for GPT-2).

</details>

---

### Question 3

**Why can't LLMs simply use a character-level tokenizer with the full Unicode character set?**

- A) Unicode has too many characters (~150,000), making the vocabulary impractically large
- B) Characters are not supported by modern hardware
- C) Character-level encoding is too slow
- D) Unicode is not standardized enough

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** The Unicode standard defines roughly 150,000 characters, and the character set continues to grow. A vocabulary this large would require an enormous embedding matrix and make training impractical. BPE finds the optimal balance between vocabulary size and sequence length.

</details>

---

### Question 4

**What does the GPT-2 pre-tokenization regex do?**

- A) It removes all punctuation from the text
- B) It splits text into "words" before BPE is applied, preventing merges across word boundaries
- C) It converts all text to lowercase
- D) It counts the number of tokens for billing

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The pre-tokenization regex divides text into units (words, numbers, punctuation) before BPE processing. BPE merges happen within each word independently, which prevents merges across word boundaries and keeps common words intact as single tokens. The regex also attaches spaces to the *following* word, which means whitespace affects tokenization.

</details>

---

### Question 5

**Why do LLMs often perform worse on non-English languages?**

- A) The model architecture is biased against non-English scripts
- B) Tokenizers are trained on primarily English text, so words in other languages get fragmented into more tokens
- C) Non-English languages are harder to learn
- D) There is no difference in performance across languages

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Tokenizer training data is typically English-dominated. Common English substrings like "tion" and "ing" become single tokens, while words in other languages lack these frequent substrings and must be represented as multiple tokens. More tokens per word means higher context budget consumption and often worse model performance.

</details>

---

### Question 6

**How many tokens does the GPT-2 vocabulary contain?**

- A) 1,024
- B) 10,000
- C) 50,257
- D) 1,000,000

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** GPT-2's vocabulary has 50,257 tokens: 50,256 from BPE merges, plus one special `<|endoftext|>` token (ID 50256). GPT-4 uses a larger vocabulary (~100,256) via the `cl100k_base` encoding with improved multilingual coverage.

</details>

---

### Question 7

**What reading of the following is TRUE about special tokens like `<|endoftext|>`?**

- A) They are optional and rarely used
- B) They count toward the context window budget
- C) They are invisible to the model
- D) They are only used during training, never during inference

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Special tokens are real token IDs with learned embeddings — they occupy positions in the context window and count toward the total token budget just like any other token. They carry semantic meaning (e.g., marking boundaries) that the model has learned during training.

</details>

---

### Question 8

**Why might a model struggle to reverse a string like "hello"?**

- A) The model was not trained on string reversal tasks
- B) Tokens do not align with characters — "hello" might be a single token, so the model has no knowledge of character ordering within it
- C) The training data explicitly excludes string operations
- D) String reversal requires more memory than the model has

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Common words like "hello" are often a single BPE token. The model sees this as one unit with no internal structure — it does not know which characters make up the token or in what order. This is why LLMs appear "bad at spelling" or string manipulation tasks.

</details>

---

### Question 9

**How does SentencePiece differ from the GPT-2 tokenizer?**

- A) SentencePiece is a character-level tokenizer
- B) SentencePiece does not require pre-tokenization — it operates directly on raw byte streams
- C) SentencePiece uses a smaller vocabulary
- D) There is no difference

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** SentencePiece (used by LLaMA, T5) treats text as a raw byte stream without requiring language-specific pre-tokenization. This makes it truly language-agnostic. It represents spaces using a special underscore character (`▁`) rather than GPT-2's approach of attaching spaces to the following word via regex.

</details>

---

### Question 10

**A sentence in English uses 10 tokens. The same sentence in Arabic might use 25 tokens. What is the practical consequence?**

- A) The Arabic version costs more per API call (token-based pricing)
- B) The Arabic version consumes more of the context window
- C) Both A and B are consequences
- D) There is no practical difference

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Both consequences apply. Token-based pricing means the Arabic version costs 2.5× more per query. It also consumes 2.5× more of the context window, leaving less room for the prompt, instructions, and response. This is a systemic inequity built into the tokenizer.

</details>

---

### Question 11

**What is `tiktoken`?**

- A) A TikTok API wrapper
- B) OpenAI's fast BPE tokenization library, the canonical implementation of GPT tokenizers
- C) A neural network architecture
- D) A dataset of tokenized texts

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `tiktoken` is OpenAI's open-source, Rust-based BPE tokenization library with Python bindings. It provides the canonical tokenizer implementations for GPT-2 (`gpt2`), GPT-3 (`p50k_base`), and GPT-4 (`cl100k_base`), and is the recommended way to count tokens for OpenAI API calls.

</details>

---

### Question 12

**Why might "3.14" and "3,14" produce different outputs from the same model in a math question?**

- A) The model is biased against commas
- B) The different decimal separators tokenize differently, leading to different model behavior
- C) Commas are not valid in numerical prompts
- D) There is no difference in behavior

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The period `.` and comma `,` are different characters that tokenize differently — one might merge with adjacent digits while the other does not. This changes the resulting token sequence, which changes how the model "sees" the number, which can produce different mathematical outputs.

</details>

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 7 | B |
| 2 | B | 8 | B |
| 3 | A | 9 | B |
| 4 | B | 10 | C |
| 5 | B | 11 | B |
| 6 | C | 12 | B |

---

*Generated for fast.ai Deep Learning — Quiz 11 (GPT Tokenizer).*
