# Quiz 04: Natural Language (NLP)

## Topic Overview

This quiz covers fast.ai lesson 4: fine-tuning a pretrained transformer with
🤗 Hugging Face Transformers on the U.S. Patent Phrase-to-Phrase Matching task.
It tests transfer learning for text, tokenization and numericalization, the
`datasets` + `Trainer` pipeline, metric selection (Pearson correlation), and —
most importantly — validation/test discipline and the overfitting/underfitting
trade-off. Understanding these ideas is what turns a model that *looks* good
into one that actually generalizes.

---

## Questions

### Question 1 — Easy

**Why do we fine-tune a pretrained language model instead of training a text
model from scratch?**

- A) Pretrained models are always smaller
- B) The pretrained model already encodes language, so fine-tuning needs far less data, time, and compute
- C) Training from scratch is impossible with transformers
- D) Fine-tuning removes the need for a validation set

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation:** A pretrained model has already learned grammar, facts, and word
relationships from a huge corpus. Fine-tuning (transfer learning) reuses those
representations, so a small labeled dataset and a few minutes of GPU time can
beat a from-scratch model trained for days.

</details>

---

### Question 2 — Easy

**What does tokenization do?**

- A) Encrypts the text for privacy
- B) Splits raw text into tokens (often subwords) the model can consume
- C) Converts the model's output back into text
- D) Removes stop words from the input

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation:** Tokenization splits text into tokens. Modern transformers use
subword tokenization (BPE / WordPiece) so any word — even unseen ones — can be
represented as a sequence of known pieces.

</details>

---

### Question 3 — Medium

**Why do transformers use subword (BPE / WordPiece) tokenization rather than
splitting on whole words?**

- A) It makes the vocabulary infinitely large
- B) It guarantees no word is fully unknown — rare words split into known pieces
- C) It removes the need for special tokens
- D) It only works for English

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation:** Whole-word vocabularies explode in size and still hit unknown
words. Subword schemes keep a fixed vocabulary of frequent pieces; common words
stay whole while rare words split into known subwords, so any input can be
represented.

</details>

---

### Question 4 — Medium

**What is numericalization?**

- A) Rounding the model's predictions to integers
- B) Mapping tokens to their integer IDs using the tokenizer's vocabulary
- C) Normalizing pixel values
- D) Converting labels to one-hot vectors

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation:** After tokenization, numericalization looks each token up in the
vocabulary to produce `input_ids` (integers). The model also receives an
`attention_mask` marking real tokens vs padding. It never sees raw text.

</details>

---

### Question 5 — Medium

**In the Patent task, how is the "how similar are these two phrases given a
context?" problem framed for the model?**

- A) As two separate models, one per phrase
- B) By serializing anchor, target, and context into a single input string and predicting one score
- C) By clustering the phrases with k-means
- D) By training a separate tokenizer per context

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation:** All fields are folded into one string (e.g.
`"TEXT1: <context>; TEXT2: <target>; ANC1: <anchor>"`) so the transformer can
attend across them, and the similarity `score` is predicted as a single value
(regression with `num_labels=1`).

</details>

---

### Question 6 — Medium

**Which Hugging Face pieces make up the standard fine-tuning pipeline used in
this lesson?**

- A) `AutoTokenizer`, `Dataset.from_pandas`/`.map`, `AutoModelForSequenceClassification`, `TrainingArguments`, `Trainer`
- B) `Pipeline`, `Tokenizer`, `Estimator`, `GridSearchCV`
- C) `DataBlock`, `DataLoaders`, `vision_learner`, `fine_tune`
- D) `Sequential`, `Dense`, `compile`, `fit`

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation:** `AutoTokenizer` tokenizes, `Dataset.from_pandas` + `.map`
builds and tokenizes the dataset, `AutoModelForSequenceClassification` adds the
head, `TrainingArguments` configures training, and `Trainer` runs the loop.
Option C is the fastai *vision* API, not the Transformers text pipeline.

</details>

---

### Question 7 — Medium

**The competition is scored by Pearson correlation. What does optimizing the
WRONG metric risk?**

- A) Nothing — any metric converges to the same model
- B) A model that scores well on your metric but fails the real objective (e.g. high accuracy on imbalanced data yet useless)
- C) The tokenizer producing wrong IDs
- D) Slower training only

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation:** The metric defines success. Optimizing accuracy on a skewed
target can yield a model that always predicts the majority class — high accuracy,
zero value. You must optimize the metric that reflects the true goal (Pearson
`r` here).

</details>

---

### Question 8 — Hard

**Why is a purely random train/validation split dangerous for the Patent data,
where the same `anchor` appears in many rows?**

- A) Random splits are always slower to compute
- B) The same anchor can land in both splits, so the model memorizes it and validation looks better than real performance
- C) Random splits change the vocabulary
- D) It causes the tokenizer to crash

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation:** When groups (anchors) leak across the split, the model sees the
same anchor in training and validation, inflating the validation score. A
grouped split (e.g. `GroupShuffleSplit` on `anchor`) keeps each anchor on one
side so validation reflects unseen anchors — like the real test set.

</details>

---

### Question 9 — Hard

**On Kaggle, what plays the role of the true test set, and how should you treat
it?**

- A) The training CSV — retrain on it repeatedly
- B) The private leaderboard — it is scored once at the end and must not be tuned on
- C) The public leaderboard — tune every hyperparameter against it
- D) The validation set — it is the same thing as the test set

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation:** The validation set (≈ public LB) is used repeatedly during
development, so you can overfit to it. The private leaderboard is the untouched
test set that gives the honest final estimate. Treat it as sacred — never tune
against it.

</details>

---

### Question 10 — Hard

**You fine-tune a transformer and see training loss keep dropping while
validation Pearson starts falling after epoch 3. What is happening and what
should you do?**

- A) Underfitting — train for many more epochs
- B) Overfitting — stop earlier (fewer epochs), add data, or regularize
- C) The metric is broken — switch to accuracy
- D) The learning rate is too small — raise it 100x

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation:** Diverging curves — train error falling while validation error
rises — is the classic overfitting signature on the right side of the U-shaped
curve. Fine-tuned transformers overfit fast, so reduce epochs (stop around the
validation peak), add data, or apply regularization such as weight decay.

</details>

---

## Answer Key

| Question | Answer | Difficulty | Concept |
|----------|--------|------------|---------|
| 1 | B | Easy | Transfer learning for text |
| 2 | B | Easy | Tokenization |
| 3 | B | Medium | Subword / BPE / WordPiece |
| 4 | B | Medium | Numericalization |
| 5 | B | Medium | Framing similarity as one input/score |
| 6 | A | Medium | datasets + Trainer pipeline |
| 7 | B | Medium | Metric selection (wrong metric danger) |
| 8 | B | Hard | Validation leakage / grouped split |
| 9 | B | Hard | Test set = Kaggle private LB |
| 10 | B | Hard | Overfitting / U-shaped curve |

**Scoring:**
- 9-10 correct: Excellent — you understand fine-tuning and, crucially, validation discipline.
- 7-8 correct: Solid — revisit metric choice and grouped splits.
- 5-6 correct: Review the lecture's validation and overfitting sections.
- 0-4 correct: Re-read Lecture 04 and rerun the exercise before moving on.

**Next:** Lecture 05 (From-Scratch Model) rebuilds the neural network under these
abstractions — tensors, matrix multiply, ReLU, and the forward pass.
