"""Exercise 06: Random Forests & Tabular (fast.ai lesson 6).

Goal:
    Build intuition for decision trees and random forests on a small,
    Titanic-like tabular dataset -- all on CPU, no downloads. You will:
      1. Synthesize a tabular dataset and split it.
      2. Overfit a single decision tree, then rein it in with max_leaf_nodes.
      3. Train a random forest and read its OOB score (free validation).
      4. Watch the diminishing-returns curve of n_estimators.
      5. Rank feature importance and prune low-importance columns.

    Fill in every block marked "# EXERCISE:". Run the file to check your work.

Prerequisites:
    scikit-learn, pandas, numpy
        pip install scikit-learn pandas numpy
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

RANDOM_STATE = 42


def make_titanic_like(n: int = 800, seed: int = 0) -> pd.DataFrame:
    """Synthesize a small Titanic-flavored dataframe (no download needed)."""
    rng = np.random.default_rng(seed)
    sex = rng.integers(0, 2, n)  # 0 female, 1 male
    pclass = rng.integers(1, 4, n)  # 1..3
    age = rng.normal(30.0, 14.0, n).clip(0.5, 80.0)
    fare = rng.gamma(2.0, 15.0, n)
    logit = 1.6 - 2.3 * sex - 0.9 * (pclass - 1) - 0.02 * age + 0.01 * fare
    prob = 1.0 / (1.0 + np.exp(-logit))
    survived = (rng.random(n) < prob).astype(int)
    return pd.DataFrame(
        {
            "Sex": sex,
            "Pclass": pclass,
            "Age": age.round(1),
            "Fare": fare.round(2),
            "Survived": survived,
        }
    )


def part_1_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Part 1: build the dataset and a train/validation split."""
    print("\n" + "=" * 60)
    print("PART 1: Build and split the dataset")
    print("=" * 60)
    df = make_titanic_like()
    features = df.drop(columns="Survived")
    target = df["Survived"]

    # EXERCISE: split into train/validation (25% valid, RANDOM_STATE).
    # Replace the four None values below with train_test_split(...).
    x_train, x_valid, y_train, y_valid = (None, None, None, None)

    assert x_train is not None, "TODO: call train_test_split"
    print(f"train rows: {len(x_train)}  valid rows: {len(x_valid)}")
    return x_train, x_valid, y_train, y_valid


def part_2_overfit_tree(
    x_train: pd.DataFrame,
    x_valid: pd.DataFrame,
    y_train: pd.Series,
    y_valid: pd.Series,
) -> None:
    """Part 2: overfit a deep tree, then constrain it."""
    print("\n" + "=" * 60)
    print("PART 2: A single tree overfits; bound it")
    print("=" * 60)

    deep = DecisionTreeClassifier(random_state=RANDOM_STATE).fit(x_train, y_train)
    print(f"deep  train={deep.score(x_train, y_train):.3f} "
          f"valid={deep.score(x_valid, y_valid):.3f}")

    # EXERCISE: build a constrained tree with max_leaf_nodes=8 and fit it.
    small: DecisionTreeClassifier | None = None

    assert small is not None, "TODO: create + fit a max_leaf_nodes=8 tree"
    print(f"small train={small.score(x_train, y_train):.3f} "
          f"valid={small.score(x_valid, y_valid):.3f}")
    print("Expect: deep train ~1.0 but lower valid (overfit); small closes the gap.")


def part_3_forest_oob(
    x_train: pd.DataFrame,
    x_valid: pd.DataFrame,
    y_train: pd.Series,
    y_valid: pd.Series,
) -> RandomForestClassifier:
    """Part 3: train a random forest and read its OOB score."""
    print("\n" + "=" * 60)
    print("PART 3: Random forest + out-of-bag validation")
    print("=" * 60)

    # EXERCISE: create a RandomForestClassifier with n_estimators=200,
    # min_samples_leaf=5, max_features="sqrt", oob_score=True, n_jobs=-1,
    # random_state=RANDOM_STATE, then fit on the training data.
    rf: RandomForestClassifier | None = None

    assert rf is not None, "TODO: create + fit the RandomForestClassifier"
    print(f"valid acc: {rf.score(x_valid, y_valid):.3f}")
    print(f"OOB  acc : {rf.oob_score_:.3f}  (free validation)")
    return rf


def part_4_n_estimators_curve(
    x_train: pd.DataFrame, y_train: pd.Series
) -> None:
    """Part 4: observe diminishing returns as trees are added."""
    print("\n" + "=" * 60)
    print("PART 4: n_estimators diminishing-returns curve")
    print("=" * 60)

    # EXERCISE: for each n in the list, fit a forest with that many trees and
    # print its OOB score. You should see the score climb fast then plateau.
    for n in (1, 5, 20, 50, 100, 200):
        rf = RandomForestClassifier(
            n_estimators=n,
            min_samples_leaf=5,
            oob_score=True,
            n_jobs=-1,
            random_state=RANDOM_STATE,
        )
        # EXERCISE: fit rf on (x_train, y_train), then read rf.oob_score_.
        score: float | None = None

        assert score is not None, "TODO: fit rf and set score = rf.oob_score_"
        print(f"n={n:>3}  oob={score:.3f}")


def part_5_feature_importance(
    rf: RandomForestClassifier,
    x_train: pd.DataFrame,
    x_valid: pd.DataFrame,
    y_train: pd.Series,
    y_valid: pd.Series,
) -> None:
    """Part 5: rank features and prune the low-importance ones."""
    print("\n" + "=" * 60)
    print("PART 5: Feature importance + pruning")
    print("=" * 60)

    # EXERCISE: build a pandas Series of rf.feature_importances_ indexed by
    # x_train.columns and sort it descending.
    importance: pd.Series | None = None

    assert importance is not None, "TODO: build the importance Series"
    print(importance.round(3).to_string())

    keep = importance[importance > 0.05].index.tolist()
    slim = RandomForestClassifier(
        n_estimators=200,
        min_samples_leaf=5,
        n_jobs=-1,
        random_state=RANDOM_STATE,
    ).fit(x_train[keep], y_train)
    print(f"kept columns: {keep}")
    print(f"full acc: {rf.score(x_valid, y_valid):.3f}  "
          f"slim acc: {slim.score(x_valid[keep], y_valid):.3f}")
    print("Expect: similar accuracy with fewer columns -> simpler model.")


def main() -> None:
    x_train, x_valid, y_train, y_valid = part_1_data()
    part_2_overfit_tree(x_train, x_valid, y_train, y_valid)
    rf = part_3_forest_oob(x_train, x_valid, y_train, y_valid)
    part_4_n_estimators_curve(x_train, y_train)
    part_5_feature_importance(rf, x_train, x_valid, y_train, y_valid)
    print("\nAll parts complete. Compare your numbers with the lecture.")


if __name__ == "__main__":
    main()
