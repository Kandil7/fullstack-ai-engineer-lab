"""
07-machine-learning — 31: Feature Engineering — The Highest-Leverage Work
=========================================================================
Topics: numeric transforms (log, clip), encoding (one-hot, ordinal, target,
        hashing), interactions, binning, date features, text features,
        ALWAYS fit encoders on train only

Why this matters for AI/backend engineering:
    Feature engineering is where tabular ML wins or loses. The model is the
    easy part; knowing how to turn raw logs into informative columns is the
    skill that separates engineers from notebook users. Every encoder must
    be fit on TRAIN data only — the same leakage rule as scaling.

Run:      python 31-feature-engineering.py
Verify:   python 31-feature-engineering.py --verify
Reference: https://scikit-learn.org/stable/modules/preprocessing.html
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import (
    StandardScaler, OneHotEncoder, OrdinalEncoder, PolynomialFeatures,
    KBinsDiscretizer,
)
from sklearn.compose import ColumnTransformer
from sklearn.metrics import roc_auc_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

rng = np.random.RandomState(0)
n = 2000

df = pd.DataFrame({
    "age": rng.randint(18, 80, n),
    "salary": np.exp(rng.randn(n) * 0.6 + 10.5),  # log-normal
    "plan": rng.choice(["free", "pro", "enterprise"], n, p=[0.6, 0.3, 0.1]),
    "city": rng.choice(["NYC", "SF", "CHI", "ATL"], n),
    "signup_ts": pd.date_range("2024-01-01", periods=n, freq="4h"),
    "bio": [" ".join(rng.choice(["python", "ml", "data", "backend", "cloud", "ai"],
                                 rng.randint(1, 5))) for _ in range(n)],
})
y = ((df["age"] > 45) & (df["plan"] != "free") | (df["salary"] > 40000)).astype(int)

Xtr, Xte, ytr, yte = train_test_split(df, y, test_size=0.3, random_state=0)
# Attach the target so groupby-based target encoding works on the frames
Xtr = Xtr.assign(y=ytr)
Xte = Xte.assign(y=yte)

# ============================================================
# 1. Numeric transforms — fix skew, add signal
# ============================================================
print("Example 1: numeric transforms")
print(f"  salary skew before log: {Xtr['salary'].skew():.2f}")
Xtr["salary_log"] = np.log1p(Xtr["salary"])
print(f"  salary skew after log : {Xtr['salary_log'].skew():.2f}")

# ============================================================
# 2. Binning — let the model split coarsely
# ============================================================
kb = KBinsDiscretizer(n_bins=5, encode="ordinal", strategy="quantile")
age_binned = kb.fit_transform(Xtr[["age"]])
print("\nExample 2: quantile binning")
print(f"  age -> {len(np.unique(age_binned))} bins (fitted on train)")

# ============================================================
# 3. Encoding strategies
# ============================================================
# One-hot (nominal)
ohe = OneHotEncoder(handle_unknown="ignore").fit(Xtr[["city"]])
print("\nExample 3: encodings")
print(f"  one-hot city -> {ohe.get_feature_names_out()}")

# Ordinal (plan has a natural order free < pro < enterprise)
ord_enc = OrdinalEncoder(categories=[["free", "pro", "enterprise"]])
plan_ord = ord_enc.fit_transform(Xtr[["plan"]])
print(f"  ordinal plan -> {plan_ord[:5].ravel()}")

# Target encoding — mean of target per category (fit on train!)
target_enc = Xtr.groupby("city")["y"].mean()
print(f"  target-encoded city (train means): {target_enc.round(3).to_dict()}")
# Apply with smoothing: (count*mean + prior) / (count + m)
prior = ytr.mean()
smooth = 10.0
def smooth_target(row_city, df_tr, df_te):
    counts = df_tr["city"].value_counts()
    means = df_tr.groupby("city")["y"].mean()
    out = df_te["city"].map(
        lambda c: (counts.get(c, 0) * means.get(c, prior) + smooth * prior)
                  / (counts.get(c, 0) + smooth)
    )
    return out
print(f"  smoothed target encoding sample: {smooth_target(None, Xtr, Xte).head(3).round(3).tolist()}")

# ============================================================
# 4. Interactions & polynomials
# ============================================================
poly = PolynomialFeatures(degree=2, include_bias=False)
inter = poly.fit_transform(Xtr[["age", "salary"]])
print("\nExample 4: interactions")
print(f"  2 features -> {inter.shape[1]} features (age, salary, age^2, age*salary, salary^2)")

# ============================================================
# 5. Date features — extract the signal
# ============================================================
Xtr["hour"] = Xtr["signup_ts"].dt.hour
Xtr["dow"] = Xtr["signup_ts"].dt.dayofweek
Xtr["month"] = Xtr["signup_ts"].dt.month
print("\nExample 5: date features")
print(f"  hour range {Xtr['hour'].min()}-{Xtr['hour'].max()}, dow 0-{Xtr['dow'].max()}, month 1-{Xtr['month'].max()}")

# ============================================================
# 6. Text features — TF-IDF for short bios
# ============================================================
tfidf = TfidfVectorizer(max_features=20)
bio_matrix = tfidf.fit_transform(Xtr["bio"])
print("\nExample 6: text features")
print(f"  bio text -> {bio_matrix.shape[1]} TF-IDF features")
print(f"  vocabulary: {list(tfidf.get_feature_names_out())}")

# ============================================================
# 7. Everything in one pipeline (leak-proof)
# ============================================================
from sklearn.pipeline import Pipeline  # noqa: E402

prep = ColumnTransformer([
    ("num", Pipeline([("poly", PolynomialFeatures(2, include_bias=False)),
                      ("scale", StandardScaler())]), ["age", "salary"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"]),
    ("ord", OrdinalEncoder(categories=[["free", "pro", "enterprise"]]), ["plan"]),
    ("txt", TfidfVectorizer(max_features=20), "bio"),
])
full = Pipeline([("prep", prep), ("clf", LogisticRegression(max_iter=500))])
full.fit(Xtr.drop(columns=["signup_ts", "y"]), ytr)
auc_full = roc_auc_score(yte, full.predict_proba(Xte.drop(columns=["signup_ts", "y"]))[:, 1])
print("\nExample 7: full engineered pipeline")
print(f"  AUC: {auc_full:.3f}")

# Baseline: no engineering
baseline = LogisticRegression(max_iter=500).fit(
    Xtr[["age", "salary"]].assign(salary=np.log1p(Xtr["salary"])), ytr)
auc_base = roc_auc_score(
    yte, baseline.predict_proba(Xte[["age", "salary"]].assign(salary=np.log1p(Xte["salary"])))[:, 1])
print(f"  baseline AUC (2 numeric cols): {auc_base:.3f}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Log transforms fix skew; binning adds robust granularity")
print("- One-hot for nominal, ordinal for ranked, target for high-card")
print("- Interactions capture joint effects (age x salary)")
print("- Date/time features: hour, dayofweek, month, lag, diff")
print("- Fit EVERY encoder on train only — or leak")
print("=" * 60)


def _verify() -> None:
    assert Xtr["salary"].skew() > Xtr["salary_log"].skew(), "log must reduce skew"
    assert inter.shape[1] == 5, "2 features -> 5 with degree-2 interactions"
    assert len(tfidf.get_feature_names_out()) <= 20
    assert auc_full > auc_base, "engineering should beat the raw baseline"
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
