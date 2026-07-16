# Glossary: Collaborative Filtering

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| Collaborative filtering | Recommending items from patterns in user-item interactions | Uses the crowd, not item content |
| Latent factor | A learned hidden attribute of a user or item | Discovered by SGD, not labeled |
| Embedding | A learnable lookup table of vectors indexed by id | = one-hot matrix multiply |
| Embedding matrix | The weight matrix an embedding indexes into | Rows = items, cols = factors |
| Dot product | Element-wise multiply then sum of two vectors | Scores user–item match |
| Matrix factorization | Approximating the ratings matrix as users × itemsᵀ | The core collab model |
| Bias | Per-user / per-movie scalar added to the score | Captures baseline appeal |
| One-hot vector | A vector that is 1 at one index, 0 elsewhere | Selecting a row = multiplying by it |
| Weight decay (L2) | Loss penalty on squared weights | Curbs overfitting |
| `y_range` / sigmoid range | Squashes output into a bounded rating range | Set top above true max |
| `CollabDataLoaders` | fastai loader for collab data from a DataFrame | `from_df(...)` |
| `collab_learner` | fastai factory for a ready collab model | `n_factors`, `y_range` |
| `nn.Embedding` | PyTorch differentiable lookup layer | Backprop flows to used rows |
| PCA | Projects factors to few interpretable axes | Reveals emergent structure |
| Cold-start | New user/item has no ratings to learn from | Needs defaults or metadata |

---

## Detailed Definitions

### Collaborative Filtering

**Definition:** A recommendation technique that predicts a user's preference for
an item based on the preferences of many users, rather than on the item's
content. "People who liked what you liked also liked X."

**Example:**
```python
from fastai.collab import CollabDataLoaders, collab_learner

dls = CollabDataLoaders.from_df(
    ratings, user_name="user", item_name="movie", rating_name="rating", bs=64
)
learn = collab_learner(dls, n_factors=50, y_range=(0, 5.5))
learn.fine_tune(5, wd=0.1)
```

**Related Terms:** Latent Factor, Matrix Factorization, Cold-start

**Key Points:**
- Learns from the interaction matrix, not item descriptions
- Works even with no metadata about users or items
- Struggles on brand-new users/items (cold-start)

---

### Latent Factor

**Definition:** A hidden, learned dimension describing a user's taste or an
item's attribute. The model discovers factors automatically via gradient
descent; humans never label what each factor "means."

**Example:**
```python
# n_factors is the length of each user/movie vector
learn = collab_learner(dls, n_factors=50)   # 50 latent factors per entity
```

**Related Terms:** Embedding, Dot Product, PCA

**Key Points:**
- More factors = more expressive, more prone to overfit
- Meaning is *emergent* (e.g. a factor may correlate with "sci-fi-ness")
- Users and items share the same factor space so they can be compared

---

### Embedding

**Definition:** A learnable lookup table that maps a discrete id (user, movie,
word) to a dense vector. Retrieving a vector is done by indexing, which is
mathematically equivalent to multiplying an embedding matrix by a one-hot
vector — but faster and differentiable.

**Example:**
```python
import torch

emb = torch.nn.Embedding(num_embeddings=1000, embedding_dim=50)
vec = emb(torch.tensor([42]))   # the vector for entity #42, shape (1, 50)
```

**Related Terms:** Embedding Matrix, One-Hot Vector, `nn.Embedding`

**Key Points:**
- The same construct powers NLP, tabular categories, and RAG
- Gradients flow only into the rows actually used in a batch
- Initialized small (e.g. `normal_(0, 0.01)`) for stable training

---

### Embedding Matrix

**Definition:** The 2-D weight tensor that an embedding indexes into. Shape is
`(num_entities, num_factors)`; each row is one entity's factor vector.

**Example:**
```python
# All movie factor vectors live in one matrix:
factors = learn.model.movie_factors.weight   # shape (n_movies, n_factors)
print(factors.shape)
```

**Related Terms:** Embedding, Matrix Factorization

**Key Points:**
- Rows = entities, columns = latent factors
- Learned jointly with the rest of the model
- Two matrices (users, items) plus two bias vectors form the collab model

---

### Dot Product

**Definition:** The sum of element-wise products of two equal-length vectors. In
collaborative filtering it scores how well a user's taste vector matches a
movie's attribute vector.

**Example:**
```python
import torch

user = torch.tensor([0.9, 0.1, 0.85])
movie = torch.tensor([0.98, -0.9, 0.72])
score = (user * movie).sum()   # 1.404
```

**Related Terms:** Latent Factor, Matrix Factorization, Bias

**Key Points:**
- Aligned signs add to the score; opposite signs subtract
- The whole model is (user factors · movie factors) + biases
- Equivalent to a row of the reconstructed ratings matrix

---

### Matrix Factorization

**Definition:** Approximating the large, sparse ratings matrix `R` as the
product of two smaller matrices — a user-factor matrix and an item-factor
matrix. Predicting a rating is reading one cell of that product.

**Example:**
```
R (users x movies)  ≈  U (users x factors)  @  Mᵀ (factors x movies)
rating[u, m]        ≈  dot(U[u], M[m])
```

**Related Terms:** Latent Factor, Dot Product, Embedding Matrix

**Key Points:**
- The classic pre-deep-learning collab method
- fastai's collab model is matrix factorization + bias + sigmoid range
- Factor count controls capacity

---

### Bias

**Definition:** A scalar added to the dot-product score — one per user and one
per item. It captures baselines a pure interaction cannot: generous raters and
universally loved/hated items.

**Example:**
```python
res = (users * movies).sum(dim=1, keepdim=True)
res += self.user_bias(uidx) + self.movie_bias(midx)
```

**Related Terms:** Dot Product, Embedding

**Key Points:**
- Movie bias alone ranks "good/bad regardless of taste"
- Cheap to add, reliably improves accuracy
- Implemented as an embedding with `embedding_dim=1`

---

### One-Hot Vector

**Definition:** A vector that is 1 at a single index and 0 everywhere else.
Multiplying an embedding matrix by a one-hot vector selects exactly one row —
the mathematical definition of an embedding lookup.

**Example:**
```python
import torch

onehot = torch.tensor([0.0, 1.0, 0.0])       # selects row 1
matrix = torch.tensor([[0.1, 0.4], [0.9, 0.1], [-0.3, 0.6]])
row = onehot @ matrix                         # tensor([0.9, 0.1])
```

**Related Terms:** Embedding, Embedding Matrix

**Key Points:**
- Explains *why* an embedding is "just" a matrix multiply
- Indexing is used in practice because it is far cheaper
- Makes the lookup differentiable and trainable

---

### Weight Decay (L2 Regularization)

**Definition:** A regularization technique that adds a penalty proportional to
the sum of squared weights to the loss, discouraging large weights and improving
generalization.

**Example:**
```python
# loss = mse(preds, targets) + wd * (weights ** 2).sum()
learn.fine_tune(5, wd=0.1)     # wd is the weight-decay strength
```

**Related Terms:** Overfitting, Latent Factor

**Key Points:**
- Collab models overfit quickly; `wd≈0.1` is a common starting point
- Equivalent to nudging each gradient by `2 * wd * weight`
- Keeps validation loss from climbing after it bottoms out

---

### `y_range` / Sigmoid Range

**Definition:** A bounded output range applied by pushing the raw model output
through a sigmoid scaled to `(lo, hi)`. Keeps predicted ratings inside a sensible
interval.

**Example:**
```python
def sigmoid_range(x, lo, hi):
    return torch.sigmoid(x) * (hi - lo) + lo

learn = collab_learner(dls, y_range=(0, 5.5))   # note 5.5, not 5.0
```

**Related Terms:** Bias, Dot Product

**Key Points:**
- Sigmoid asymptotes, so set `hi` above the true max to reach it
- Standard collab choice for 0–5 ratings is `(0, 5.5)`
- Turns an unbounded score into a valid rating

---

### `CollabDataLoaders`

**Definition:** The fastai data-loading class for collaborative filtering. Its
`from_df` constructor builds train/valid `DataLoaders` straight from a ratings
DataFrame.

**Example:**
```python
dls = CollabDataLoaders.from_df(
    ratings, user_name="user", item_name="movie",
    rating_name="rating", bs=64,
)
dls.show_batch()
```

**Related Terms:** `collab_learner`, Embedding

**Key Points:**
- Maps raw ids to contiguous indices for the embeddings
- `dls.classes["user"]` gives the id→index vocabulary
- Handles the train/validation split for you

---

### `collab_learner`

**Definition:** A fastai factory that returns a `Learner` wrapping a complete
collaborative-filtering model (embeddings, bias, and sigmoid range) ready to
train.

**Example:**
```python
learn = collab_learner(dls, n_factors=50, y_range=(0, 5.5))
learn.fine_tune(5, wd=0.1)
```

**Related Terms:** `CollabDataLoaders`, `nn.Embedding`, `y_range`

**Key Points:**
- Fastest path to a working recommender
- `n_factors` sets latent dimensionality
- Under the hood it is the `EmbeddingDotBias` module

---

### `nn.Embedding`

**Definition:** PyTorch's embedding layer — a differentiable lookup table
holding a `(num_embeddings, embedding_dim)` weight matrix, indexed by integer
ids.

**Example:**
```python
import torch
emb = torch.nn.Embedding(num_embeddings=943, embedding_dim=50)
batch = torch.tensor([0, 5, 5, 12])   # user ids
vectors = emb(batch)                   # shape (4, 50)
```

**Related Terms:** Embedding, One-Hot Vector, Embedding Matrix

**Key Points:**
- Building block for user_factors, movie_factors, and bias
- Backprop updates only the rows referenced in the batch
- `embedding_dim=1` makes a bias vector

---

### PCA

**Definition:** Principal Component Analysis — a linear technique that projects
high-dimensional data onto a few orthogonal axes capturing the most variance.
Used to interpret and visualize learned factor matrices.

**Example:**
```python
import torch
factors = learn.model.movie_factors.weight
factors = factors - factors.mean(dim=0)
u, s, v = torch.pca_lowrank(factors, q=3)
movie_pca = factors @ v[:, :3]        # 3 interpretable components
```

**Related Terms:** Latent Factor, Embedding Matrix

**Key Points:**
- Reveals emergent axes (e.g. blockbuster ↔ arthouse)
- Great sanity check that the model learned real structure
- Reduces 50-D factors to a 2-D/3-D plot

---

### Cold-Start / Bootstrapping

**Definition:** The problem of recommending for a brand-new user or item that has
no interaction history, so its embedding row was never trained.

**Example:**
```python
# A new user has no ratings -> fall back to global mean + item bias,
# or collect a few onboarding ratings, or use a metadata model first.
default_rating = ratings["rating"].mean()
```

**Related Terms:** Bias, Embedding, Collaborative Filtering

**Key Points:**
- Pure collaborative filtering cannot solve it alone
- Common fixes: mean/bias defaults, onboarding, metadata models
- Improves automatically as interactions accumulate

---

## Summary

Understanding these terms is essential for building recommenders and, more
broadly, for understanding embeddings everywhere:

1. **Collaborative filtering:** learn from the crowd's interactions
2. **Latent factors:** hidden, learned attributes of users and items
3. **Embedding / embedding matrix:** a differentiable lookup = one-hot multiply
4. **Dot product / matrix factorization:** score user–item compatibility
5. **Bias:** per-user/per-item baselines
6. **Weight decay:** the main defense against overfitting
7. **`y_range` / sigmoid:** bound predictions with headroom above the max
8. **`CollabDataLoaders` / `collab_learner` / `nn.Embedding`:** the fastai + torch tools
9. **PCA:** interpret the learned factors
10. **Cold-start:** the limit of pure collaborative filtering

**Next:** See Lecture 08 for convolutions and CNNs — how the same
"learned-parameters" idea builds networks that see images.
