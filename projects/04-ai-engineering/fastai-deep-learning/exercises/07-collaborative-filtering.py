"""
Exercise 07: Collaborative Filtering
====================================
Goal: Build a MovieLens-style recommender the fast.ai way, then reimplement it
from scratch to internalize that an EMBEDDING is just a differentiable lookup
into a weight matrix. Covers latent factors, the dot product, bias terms,
sigmoid y_range, and weight decay.

Runs WITHOUT a GPU or the real MovieLens download: a tiny synthetic ratings
table keeps the mechanics visible. Swap in `CollabDataLoaders.from_df(...)`
for the real dataset.

Prerequisites:
    pip install torch          # fastai optional; the torch path always runs
"""

import torch
from torch import nn

# ---------------------------------------------------------------------------
# 1. A Tiny Synthetic Ratings Matrix
# ---------------------------------------------------------------------------

N_USERS: int = 6
N_MOVIES: int = 8
N_FACTORS: int = 4
Y_RANGE: tuple[float, float] = (0.0, 5.5)

# (user_idx, movie_idx, rating) triples — most of the 6x8 grid is unobserved.
RATINGS: list[tuple[int, int, float]] = [
    (0, 0, 5.0), (0, 1, 4.0), (0, 4, 1.0), (1, 1, 5.0), (1, 2, 4.0), (1, 5, 2.0),
    (2, 0, 4.0), (2, 3, 5.0), (2, 6, 1.0), (3, 2, 5.0), (3, 4, 4.0), (3, 7, 2.0),
    (4, 3, 4.0), (4, 5, 5.0), (4, 6, 3.0), (5, 0, 2.0), (5, 4, 5.0), (5, 7, 4.0),
]


def make_tensors() -> tuple[torch.Tensor, torch.Tensor]:
    """Return (x, y) where x is (N, 2) [user, movie] and y is (N, 1) ratings."""
    x = torch.tensor([[u, m] for (u, m, _) in RATINGS], dtype=torch.long)
    y = torch.tensor([[r] for (_, _, r) in RATINGS], dtype=torch.float32)
    return x, y


# ---------------------------------------------------------------------------
# 2. Embedding = One-Hot Matrix Multiply (the key insight)
# ---------------------------------------------------------------------------

def show_embedding_is_matmul() -> None:
    """Demonstrate that indexing an embedding == multiplying by a one-hot row."""
    weight = torch.tensor(
        [[0.1, 0.4], [0.9, 0.1], [-0.3, 0.6]], dtype=torch.float32
    )
    idx = 1
    one_hot = torch.zeros(3)
    one_hot[idx] = 1.0

    via_index = weight[idx]          # embedding lookup
    via_matmul = one_hot @ weight    # equivalent matrix multiply
    print(f"lookup:  {via_index.tolist()}")
    print(f"one-hot: {via_matmul.tolist()}")
    print(f"equal:   {torch.allclose(via_index, via_matmul)}")

    # EXERCISE: build nn.Embedding(3, 2), copy `weight` into `.weight.data`,
    #           and confirm emb(tensor([idx])) matches too.


# ---------------------------------------------------------------------------
# 3. DotProductBias Model From Scratch
# ---------------------------------------------------------------------------

class DotProductBias(nn.Module):
    """Matrix factorization with latent factors + per-entity bias + y_range."""

    def __init__(
        self,
        n_users: int,
        n_movies: int,
        n_factors: int,
        y_range: tuple[float, float] = Y_RANGE,
    ) -> None:
        super().__init__()
        self.user_factors = nn.Embedding(n_users, n_factors)
        self.movie_factors = nn.Embedding(n_movies, n_factors)
        self.user_bias = nn.Embedding(n_users, 1)
        self.movie_bias = nn.Embedding(n_movies, 1)
        self.y_range = y_range
        for emb in (self.user_factors, self.movie_factors):
            emb.weight.data.normal_(0.0, 0.01)
        self.user_bias.weight.data.zero_()
        self.movie_bias.weight.data.zero_()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        users = self.user_factors(x[:, 0])
        movies = self.movie_factors(x[:, 1])
        res = (users * movies).sum(dim=1, keepdim=True)
        res = res + self.user_bias(x[:, 0]) + self.movie_bias(x[:, 1])
        lo, hi = self.y_range
        return torch.sigmoid(res) * (hi - lo) + lo


# ---------------------------------------------------------------------------
# 4. A Minimal Training Loop With Weight Decay
# ---------------------------------------------------------------------------

def train(
    model: nn.Module,
    x: torch.Tensor,
    y: torch.Tensor,
    epochs: int = 400,
    lr: float = 0.05,
    wd: float = 0.1,
) -> list[float]:
    """Train with MSE loss + L2 weight decay; return the loss history."""
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=wd)
    loss_fn = nn.MSELoss()
    history: list[float] = []
    for _ in range(epochs):
        opt.zero_grad()
        preds = model(x)
        loss = loss_fn(preds, y)
        loss.backward()
        opt.step()
        history.append(float(loss.item()))
    return history

    # EXERCISE: rerun with wd=0.0 and wd=1.0; compare final loss and explain
    #           why lowest train loss can be misleading vs. a validation set.


# ---------------------------------------------------------------------------
# 5. Interpreting the Learned Embeddings
# ---------------------------------------------------------------------------

def interpret(model: DotProductBias) -> None:
    """Rank movies by bias and find similar movies via factor distance."""
    movie_bias = model.movie_bias.weight.detach().squeeze()
    best = movie_bias.argsort(descending=True)[:3].tolist()
    worst = movie_bias.argsort()[:3].tolist()
    print(f"Highest-bias movies (universally liked): {best}")
    print(f"Lowest-bias movies (universally disliked): {worst}")

    factors = model.movie_factors.weight.detach()
    dists = torch.norm(factors - factors[0], dim=1)
    print(f"Movies most similar to movie 0: {dists.argsort()[1:4].tolist()}")

    # EXERCISE: center `factors`, run torch.pca_lowrank(factors, q=2), project
    #           onto component 1, and print movies sorted along that axis.


# ---------------------------------------------------------------------------
# 6. Optional: The Real fast.ai Path (needs `fastai` + a download)
# ---------------------------------------------------------------------------

def fastai_reference() -> None:
    """Print the equivalent fast.ai high-level recipe (not executed here)."""
    recipe = """
    from fastai.collab import CollabDataLoaders, collab_learner
    from fastai.data.external import untar_data, URLs
    import pandas as pd
    path = untar_data(URLs.ML_100k)
    ratings = pd.read_csv(path/'u.data', delimiter='\\t', header=None,
                          names=['user', 'movie', 'rating', 'timestamp'])
    dls = CollabDataLoaders.from_df(ratings, bs=64)
    learn = collab_learner(dls, n_factors=50, y_range=(0, 5.5))
    learn.fine_tune(5, wd=0.1)"""
    print(recipe)

    # EXERCISE: run the recipe on Kaggle/Colab; compare its validation loss to
    #           your from-scratch model above.


# ---------------------------------------------------------------------------
# 7. Main Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    torch.manual_seed(42)
    print("=" * 60)
    print("COLLABORATIVE FILTERING FROM SCRATCH")
    print("=" * 60)
    print("\n[1] Embedding == one-hot matrix multiply")
    show_embedding_is_matmul()

    print("\n[2] Training DotProductBias with weight decay")
    x, y = make_tensors()
    model = DotProductBias(N_USERS, N_MOVIES, N_FACTORS)
    history = train(model, x, y)
    print(f"first loss: {history[0]:.3f}  ->  final loss: {history[-1]:.3f}")

    print("\n[3] Interpreting the learned embeddings")
    interpret(model)

    print("\n[4] The equivalent fast.ai recipe")
    fastai_reference()
    print("\nDone. Now work the EXERCISE TODOs above.")


if __name__ == "__main__":
    main()
