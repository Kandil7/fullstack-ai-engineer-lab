# Lecture 07: Collaborative Filtering

## Topic Overview

Collaborative filtering answers a deceptively simple question: *given a giant,
mostly-empty table of who liked what, what will someone like next?* fast.ai
lesson 7 uses the **MovieLens** dataset to build a movie recommender — and in
doing so introduces one of the most important ideas in all of deep learning:
the **embedding**. You will learn to represent each user and each movie as a
small vector of *learned latent factors*, predict a rating as the **dot
product** of those vectors, and then discover that an embedding is nothing more
than a differentiable lookup into a weight matrix. That single realization —
"an embedding is just matrix multiplication by a one-hot vector" — is the bridge
between this recommender and the embeddings that power NLP, RAG, and the lab's
own `embeddings/` and RAG projects.

**Duration:** 3-4 hours  
**Difficulty:** Intermediate  
**Prerequisites:** Lectures 01-05 (training loop, SGD, from-scratch models, `nn.Module`)

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Frame** recommendation as filling in a sparse user × item ratings matrix
2. **Explain** latent factors and why a dot product captures taste-to-attribute match
3. **Describe** an embedding as a lookup table equivalent to one-hot matrix multiply
4. **Build** a MovieLens recommender with `CollabDataLoaders` and `collab_learner`
5. **Implement** a `DotProduct` model from scratch as an `nn.Module` using `nn.Embedding`
6. **Add** user and movie **bias** terms and a sigmoid `y_range` to bound predictions
7. **Apply** **weight decay** (L2 regularization) to stop collab models overfitting
8. **Interpret** learned embeddings via PCA, movie similarity, and the bias term, and reason about the **cold-start** problem

---

## Key Concepts

### 1. The Recommendation Problem: A Mostly-Empty Matrix

Imagine every user as a row and every movie as a column. Each filled cell is a
rating. The overwhelming majority of cells are **empty** — no one watches
everything. Recommendation = predicting the empty cells.

```
            Toy Story  Alien  Casablanca  Fargo
   User 1      5.0       ?        4.0       ?
   User 2       ?       4.5        ?       3.0
   User 3      4.0       ?         ?        ?     <- predict the "?"
   User 4       ?       5.0       2.0       ?
```

A dataset with 1,000 users and 1,000 movies has 1,000,000 cells but perhaps
only ~50,000 ratings. The task: learn structure from the known cells that
generalizes to the unknown ones.

```python
from fastai.collab import *
from fastai.tabular.all import *

path = untar_data(URLs.ML_100k)
ratings = pd.read_csv(
    path / "u.data",
    delimiter="\t",
    header=None,
    names=["user", "movie", "rating", "timestamp"],
)
ratings.head()
```

### 2. Latent Factors

We describe each movie by a small vector of hidden ("latent") attributes and
each user by a vector of the *same length* expressing their taste along those
same attributes. We do **not** hand-label these factors — SGD discovers them.

```
Movie "Alien"  ->  [ 0.98  -0.90   0.72 ]   (sci-fi, not-romance, action)
User  "Alice"  ->  [ 0.90   0.10   0.85 ]   (loves sci-fi, neutral romance, loves action)
                       │       │       │
                    factor1 factor2 factor3   (meaning is emergent, not assigned)
```

If a user's factors align with a movie's factors, the predicted rating is high.
The number of factors is a hyperparameter (`n_factors`, often 50).

### 3. The Dot Product Captures "Match"

The predicted rating is the **dot product** of the user vector and the movie
vector: multiply element-wise, then sum.

```python
import torch

user  = torch.tensor([0.90, 0.10, 0.85])   # taste
movie = torch.tensor([0.98, -0.90, 0.72])  # attributes

prediction = (user * movie).sum()   # dot product
# 0.90*0.98 + 0.10*(-0.90) + 0.85*0.72 = 1.404
```

A large positive product on a factor means "user wants this AND movie has it"
(or "user dislikes AND movie lacks it") — both are good matches. Opposite signs
subtract. Summing across factors yields an overall compatibility score. This is
**matrix factorization**: the full ratings matrix ≈ (users matrix) × (movies
matrixᵀ).

### 4. Embeddings = A Lookup Table = One-Hot Matrix Multiply

We store all user vectors in one matrix and all movie vectors in another. To
get user 42's vector we *index* row 42. That index step is an **embedding**.

The key insight: **indexing into a matrix is identical to multiplying that
matrix by a one-hot vector** — but indexing is fast and, crucially, we can
compute gradients through it, so the lookup table is learnable.

```
one-hot for user #2      embedding matrix (3 users x 3 factors)
[0, 1, 0]        @        [[ 0.1,  0.4, -0.2],     =  [ 0.9, 0.1, 0.85]
                          [ 0.9,  0.1,  0.85],  <---- row 2 selected
                          [-0.3,  0.6,  0.05]]

  Multiplying by a one-hot vector == picking a row.
  nn.Embedding does the pick directly, and backprop flows into that row only.
```

```python
emb = torch.nn.Embedding(num_embeddings=3, embedding_dim=3)
idx = torch.tensor([2])          # want row 2
vec = emb(idx)                   # differentiable lookup, shape (1, 3)
```

### 5. Bias Terms

Some users rate everything high; some movies are loved regardless of genre. A
pure dot product can't express "universally good" because it must go through a
factor interaction. So we add a **bias** scalar per user and per movie.

```
prediction = dot(user_factors, movie_factors)
           + user_bias[user]      # this user's baseline generosity
           + movie_bias[movie]    # this movie's baseline appeal
```

The movie-bias term is interpretable on its own: a high movie bias means "people
like this even if it doesn't match their usual taste."

### 6. Bounding Predictions with `y_range` (Sigmoid)

Ratings live in [0, 5]. Predictions should too. fastai squashes the raw output
through a **sigmoid** scaled to a range. Note the trick: the top is set slightly
**above** the max (e.g. `5.5`) because sigmoid asymptotes and never quite
reaches its ceiling — the extra headroom lets the model actually hit 5.0.

```python
def sigmoid_range(x, lo, hi):
    return torch.sigmoid(x) * (hi - lo) + lo

# collab_learner uses y_range=(0, 5.5) so real 5.0 ratings are reachable
```

### 7. Weight Decay (L2 Regularization)

Collaborative models overfit easily: with enough factors they can memorize the
training ratings. **Weight decay** adds a penalty proportional to the sum of
squared weights to the loss, discouraging large weights and forcing smoother,
more general solutions.

```
loss = mse(predictions, targets) + wd * (weights ** 2).sum()

# Equivalently, it nudges each gradient:  grad += 2 * wd * weights
```

In fastai you pass `wd` to `fit`/`fine_tune`. Typical collab values: `0.1`.
Diagram of the effect:

```
no weight decay:   train loss ↓↓↓   valid loss ↓ then ↑  (overfit)
with weight decay: train loss ↓     valid loss ↓ and stays low (generalizes)
```

### 8. Interpreting Embeddings & the Cold-Start Problem

Once trained, the embeddings are *meaningful*:

- **Movie bias** ranks universally loved vs. universally disliked films.
- **PCA** on the movie-factor matrix projects 50 dimensions down to 2-3
  interpretable axes (e.g. an emergent "blockbuster ↔ arthouse" axis).
- **Distance** between two movie vectors finds similar movies.

```
PCA of movie factors (2 components):

  arthouse  ●Casablanca      ●Fargo
            │
   ─────────┼───────────────────────►  factor 1
            │         ●Toy Story
 blockbuster│                 ●Star Wars
```

**Cold-start / bootstrapping:** a brand-new user or movie has *no* ratings, so
its embedding row was never trained. Solutions: default to the mean/bias, ask a
few onboarding questions, or use a metadata model (genre, demographics) until
enough interactions accrue.

---

## Code Examples

### Example 1: MovieLens Recommender with fastai in ~10 lines

```python
"""End-to-end MovieLens recommender using the fastai collab API."""
from fastai.collab import CollabDataLoaders, collab_learner
from fastai.data.external import untar_data, URLs
import pandas as pd

path = untar_data(URLs.ML_100k)
ratings = pd.read_csv(
    path / "u.data",
    delimiter="\t",
    header=None,
    names=["user", "movie", "rating", "timestamp"],
)

# Build DataLoaders directly from the DataFrame.
dls = CollabDataLoaders.from_df(
    ratings,
    user_name="user",
    item_name="movie",
    rating_name="rating",
    bs=64,
)

# A collab_learner wires up embeddings + bias + sigmoid range for us.
learn = collab_learner(dls, n_factors=50, y_range=(0, 5.5))
learn.fine_tune(5, wd=0.1)          # weight decay to curb overfitting

# Predict a rating for one (user, movie) pair.
dl = learn.dls.test_dl(pd.DataFrame({"user": [1], "movie": [100]}))
preds, _ = learn.get_preds(dl=dl)
print(f"Predicted rating: {preds.item():.2f}")
```

### Example 2: The DotProduct Model From Scratch

```python
"""Reimplement what collab_learner does, as a plain nn.Module."""
import torch
from torch import nn


def create_params(size: tuple[int, ...]) -> nn.Parameter:
    """A learnable embedding matrix initialized with small random values."""
    return nn.Parameter(torch.zeros(*size).normal_(0, 0.01))


class DotProductBias(nn.Module):
    """Matrix factorization with user/movie factors AND bias terms."""

    def __init__(
        self,
        n_users: int,
        n_movies: int,
        n_factors: int,
        y_range: tuple[float, float] = (0, 5.5),
    ) -> None:
        super().__init__()
        # Two embedding matrices of latent factors...
        self.user_factors = nn.Embedding(n_users, n_factors)
        self.movie_factors = nn.Embedding(n_movies, n_factors)
        # ...and two bias vectors (one scalar per user / per movie).
        self.user_bias = nn.Embedding(n_users, 1)
        self.movie_bias = nn.Embedding(n_movies, 1)
        self.y_range = y_range

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x[:, 0] = user index, x[:, 1] = movie index (a mini-batch).
        users = self.user_factors(x[:, 0])
        movies = self.movie_factors(x[:, 1])
        # Element-wise product, summed over factors = per-row dot product.
        res = (users * movies).sum(dim=1, keepdim=True)
        res += self.user_bias(x[:, 0]) + self.movie_bias(x[:, 1])
        # Bound predictions to a sensible rating range via sigmoid.
        lo, hi = self.y_range
        return torch.sigmoid(res) * (hi - lo) + lo


# Train it with fastai's Learner (same data, our model).
from fastai.collab import CollabDataLoaders
from fastai.learner import Learner
from fastai.losses import MSELossFlat

# (dls built as in Example 1)
# n_users = len(dls.classes["user"]); n_movies = len(dls.classes["movie"])
# model = DotProductBias(n_users, n_movies, 50)
# learn = Learner(dls, model, loss_func=MSELossFlat())
# learn.fit_one_cycle(5, 5e-3, wd=0.1)
```

### Example 3: Interpreting the Learned Embeddings

```python
"""Read meaning out of a trained collab model: bias ranking, PCA, similarity."""
import torch

# Assume `learn` is a trained collab_learner; grab the movie index->title map.
movies = learn.dls.classes["movie"]  # list of movie ids/titles

# --- (a) Bias reveals universally liked / disliked movies -----------------
movie_bias = learn.model.movie_bias.weight.squeeze()
worst = movie_bias.argsort()[:5]
best = movie_bias.argsort(descending=True)[:5]
print("Universally liked (high bias):", [movies[i] for i in best])
print("Universally disliked (low bias):", [movies[i] for i in worst])

# --- (b) PCA of movie factors: emergent interpretable axes ----------------
factors = learn.model.movie_factors.weight        # (n_movies, n_factors)
factors = factors - factors.mean(dim=0)            # center for PCA
u, s, v = torch.pca_lowrank(factors, q=3)
movie_pca = factors @ v[:, :3]                     # project to 3 components
# movie_pca[:, 0] often sorts blockbuster <-> arthouse.

# --- (c) Similar movies via distance in factor space ----------------------
def similar_movies(idx: int, k: int = 5) -> list:
    """Return the k movies whose factor vectors are closest to `idx`."""
    dists = torch.norm(factors - factors[idx], dim=1)
    nearest = dists.argsort()[1 : k + 1]           # skip itself at position 0
    return [movies[i] for i in nearest]

print("Similar to movie 0:", similar_movies(0))
```

---

## Common Mistakes to Avoid

### 1. Forgetting the Bias Term
```python
# BAD: pure dot product cannot express "universally good/bad" cleanly
res = (users * movies).sum(dim=1)          # no baseline for user/movie

# GOOD: add per-user and per-movie bias so baselines are learnable
res = (users * movies).sum(dim=1, keepdim=True)
res += self.user_bias(uidx) + self.movie_bias(midx)
```

### 2. Setting `y_range` to the Exact Rating Max
```python
# BAD: sigmoid asymptotes; the model can never actually output 5.0
learn = collab_learner(dls, n_factors=50, y_range=(0, 5.0))

# GOOD: leave headroom so real max ratings are reachable
learn = collab_learner(dls, n_factors=50, y_range=(0, 5.5))
```

### 3. Skipping Weight Decay (Overfitting)
```python
# BAD: collab models memorize training ratings; valid loss climbs
learn.fine_tune(5)                          # wd defaults may be too low here

# GOOD: regularize so learned factors generalize
learn.fine_tune(5, wd=0.1)                  # penalize large weights
```

---

## Best Practices

1. **Start with `collab_learner`** before writing a model from scratch — it
   already wires embeddings, bias, and `y_range` correctly.
2. **Use `n_factors≈50`** as a sane default; tune it only after a baseline works.
3. **Always set `y_range` slightly above the true max** (e.g. `(0, 5.5)`).
4. **Tune weight decay first** (`wd≈0.1`) when the validation loss diverges.
5. **Initialize embeddings small** (`normal_(0, 0.01)`) for stable early training.
6. **Include bias terms** — they carry real signal and improve accuracy cheaply.
7. **Interpret the bias vector** to sanity-check the model against known hits/flops.
8. **Run PCA on factors** to confirm the model learned meaningful structure.
9. **Plan for cold-start** explicitly (defaults, onboarding, or a metadata model).
10. **Remember embeddings are universal** — the same lookup-table idea reappears
    in NLP, tabular categories, and the lab's RAG/embeddings projects.

---

## Practice Exercises

### Exercise 1: Baseline Recommender
Load MovieLens 100k with `CollabDataLoaders.from_df` and train a
`collab_learner` for 5 epochs. Report the final validation loss and predict a
rating for a chosen (user, movie) pair.

### Exercise 2: Dot Product Without Bias
Implement a `DotProduct` `nn.Module` (no bias) using `nn.Embedding`. Train it and
compare its validation loss to the biased version. Explain the gap.

### Exercise 3: Add Bias and `y_range`
Extend Exercise 2 with user/movie bias and a sigmoid `y_range=(0, 5.5)`. Show
that both changes improve validation loss.

### Exercise 4: Regularization Sweep
Train the model at `wd ∈ {0.0, 0.01, 0.1, 1.0}`. Plot train vs. validation loss
and identify the value that best controls overfitting.

### Exercise 5: Embedding Interpretation
From a trained model, print the 10 highest- and lowest-bias movies, run PCA on
the movie factors, and write a one-sentence interpretation of the first
principal component.

---

## Summary

Collaborative filtering turns a sparse ratings matrix into predictions by
learning **latent factors**:

1. **Users and movies** are each represented as vectors of learned factors.
2. **The dot product** of a user and movie vector scores their compatibility.
3. **Embeddings** are learnable lookup tables — equivalent to multiplying a
   weight matrix by a one-hot vector, made differentiable.
4. **Bias terms** capture per-user generosity and per-movie universal appeal.
5. **`y_range` + sigmoid** bound predictions; leave headroom above the max.
6. **Weight decay** (L2) is the primary defense against overfitting.
7. **Trained embeddings are interpretable** via bias ranking, PCA, and distance —
   and the same idea powers embeddings everywhere else in deep learning.

**Next lecture:** Convolutions (CNNs) — how convolutional networks *see* images,
built up from a single hand-computed convolution to a full CNN.
