# Quiz 07: Collaborative Filtering

## Topic Overview
This quiz covers collaborative filtering and embeddings as taught in fast.ai
lesson 7 using MovieLens: the sparse ratings matrix, latent factors, the dot
product, embeddings as differentiable one-hot lookups, bias terms, the sigmoid
`y_range`, weight decay, embedding interpretation (bias ranking and PCA), and
the cold-start problem.

---

## Questions

### Question 1
**In collaborative filtering, what does the user × item ratings matrix look like in practice?**

- A) Completely filled with ratings
- B) Mostly empty (sparse), with only a small fraction of cells observed
- C) A square matrix that is always symmetric
- D) A matrix of item descriptions

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** No user rates every item, so the vast majority of cells are unobserved. The recommendation task is exactly to predict those empty cells from the sparse set of known ratings.
</details>

---

### Question 2
**What are "latent factors" in a collaborative filtering model?**

- A) Hand-labeled genre tags applied to each movie
- B) Learned hidden vectors describing user taste and item attributes, discovered by SGD
- C) The timestamps of each rating
- D) The number of users who rated an item

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Each user and each item is represented as a vector of latent factors. These are not assigned by humans; gradient descent learns values that best reconstruct the observed ratings. Their meaning (e.g. "sci-fi-ness") is emergent.
</details>

---

### Question 3
**How is a predicted rating computed from a user vector and a movie vector in the basic model?**

- A) The Euclidean distance between them
- B) The cosine of the angle between them only
- C) Their dot product (element-wise multiply, then sum)
- D) The concatenation of the two vectors

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** The dot product multiplies matching factors and sums them. Aligned factors (both strong, same sign) increase the score; opposing signs decrease it. This scores how well the user's taste matches the movie's attributes.
</details>

---

### Question 4
**Why is an embedding described as "just matrix multiplication by a one-hot vector"?**

- A) Because embeddings store one-hot vectors internally
- B) Because indexing row i of a weight matrix equals multiplying that matrix by a one-hot vector that is 1 at position i
- C) Because embeddings can only represent binary data
- D) Because one-hot vectors are faster than embeddings

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Selecting a row by index is mathematically identical to multiplying the matrix by a one-hot vector. An embedding does the selection directly (much cheaper) while remaining differentiable, so gradients update the selected rows during training.
</details>

---

### Question 5
**Why add per-user and per-movie bias terms to the dot-product model?**

- A) To make the model train faster
- B) To capture baselines — generous raters and universally liked/disliked movies — that a pure interaction cannot express
- C) To reduce the number of latent factors needed to zero
- D) To normalize the embeddings to unit length

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A bias is a scalar added per user and per movie. It models a movie being loved regardless of taste, or a user who rates everything high, which a factor interaction alone struggles to represent cleanly. Bias terms improve accuracy cheaply.
</details>

---

### Question 6
**In fastai, why is `y_range` often set to `(0, 5.5)` rather than `(0, 5.0)` for 0–5 ratings?**

- A) Because ratings can legally exceed 5.0
- B) Because a sigmoid asymptotes and never reaches its ceiling, so headroom is needed to actually predict 5.0
- C) Because 5.5 makes the loss smaller by definition
- D) It is arbitrary and has no effect

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Predictions pass through `sigmoid(x) * (hi - lo) + lo`. The sigmoid approaches but never hits 1, so `hi` must sit above the true maximum for real 5.0 ratings to be reachable.
</details>

---

### Question 7
**What problem does weight decay (L2 regularization) address in collaborative filtering, and how?**

- A) Slow training; it increases the learning rate
- B) Overfitting; it adds a penalty proportional to the sum of squared weights, discouraging large weights
- C) Data leakage; it removes duplicate ratings
- D) Cold-start; it creates embeddings for new users

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** With enough factors, collab models can memorize training ratings. Weight decay adds `wd * (weights**2).sum()` to the loss (equivalently nudging gradients by `2*wd*weight`), favoring smaller weights and smoother, more general solutions. `wd≈0.1` is a common value.
</details>

---

### Question 8
**What does the fastai `collab_learner(dls, n_factors=50, y_range=(0, 5.5))` call set up?**

- A) A random forest recommender
- B) A model with user/movie embeddings, bias terms, and a sigmoid output range, wrapped in a trainable Learner
- C) A raw PyTorch training loop with no model
- D) Only the data loaders

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `collab_learner` builds the embedding-dot-bias model (user/movie factor embeddings + bias + sigmoid `y_range`) and returns a `Learner` ready for `fine_tune`. `n_factors` sets the latent dimensionality.
</details>

---

### Question 9
**How can the learned embeddings be interpreted after training?**

- A) They cannot be interpreted at all
- B) The movie-bias vector ranks universally liked/disliked films, PCA on the movie factors reveals emergent axes, and factor distance finds similar movies
- C) Only by retraining with different seeds
- D) By reading the raw timestamps

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The bias term isolates "good/bad regardless of taste." PCA projects the 50-D factor matrix onto a few interpretable components (e.g. blockbuster ↔ arthouse). Nearest neighbors in factor space are similar movies.
</details>

---

### Question 10
**What is the cold-start (bootstrapping) problem, and why does pure collaborative filtering struggle with it?**

- A) Models train slowly on cold hardware; use a GPU
- B) A brand-new user or item has no ratings, so its embedding row was never trained; fixes include mean/bias defaults, onboarding questions, or a metadata model
- C) Ratings drift over time as tastes change
- D) The sigmoid range is set incorrectly

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Collaborative filtering learns only from interactions. A new user/item has none, so its embedding is untrained and predictions are unreliable. Common mitigations: fall back to global mean + bias, collect a few onboarding ratings, or use a content/metadata model until interactions accrue.
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
| 8 | Easy | | |
| 9 | Medium | | |
| 10 | Hard | | |

**Score:** ____/10

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 6 | B |
| 2 | B | 7 | B |
| 3 | C | 8 | B |
| 4 | B | 9 | B |
| 5 | B | 10 | B |

---

*Generated for fast.ai Deep Learning Lab — Quiz 07 of 09*
