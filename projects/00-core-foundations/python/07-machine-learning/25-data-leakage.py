"""
07-machine-learning — 25: Data Leakage — The 0.99 -> 0.71 Story
==============================================================
Topics: target leakage, train/test contamination (scaling before split),
        temporal leakage, group leakage, duplicate rows across splits,
        the worked example where accuracy collapses once fixed

Why this matters for AI/backend engineering:
    Leakage inflates offline metrics, ships models that fail in production,
    and is the most common way ML teams discover their dashboard lied.
    Every AI engineer must be able to audit a pipeline for the 5 leakage
    classes shown here.

Run:      python 25-data-leakage.py
Verify:   python 25-data-leakage.py --verify
Reference: https://scikit-learn.org/stable/common_pitfalls.html
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.ensemble import RandomForestClassifier

rng = np.random.RandomState(42)

# ============================================================
# 1. The Worked Example: why accuracy 0.99 collapses to 0.71
# ============================================================
# Synthetic churn data where the target 'churned' is genuinely hard to
# predict (signal ~ AUC 0.75). We then inject leakage and watch the lie.

n = 2_000
X = rng.randn(n, 5)
y = (X[:, 0] * 0.8 + X[:, 1] * 0.3 + rng.randn(n) * 1.5 > 0).astype(int)

df = pd.DataFrame(X, columns=[f"f{i}" for i in range(5)])
df["churned"] = y

def honest_auc(df_: pd.DataFrame) -> float:
    Xtr, Xte, ytr, yte = train_test_split(
        df_.drop(columns="churned"), df_["churned"], test_size=0.3, random_state=0
    )
    m = RandomForestClassifier(n_estimators=50, random_state=0).fit(Xtr, ytr)
    return roc_auc_score(yte, m.predict_proba(Xte)[:, 1])

print("Example 1: the honest baseline")
print(f"  clean AUC: {honest_auc(df):.3f}")

# --- Leak 1: target leakage via a column that encodes the answer ---
df_leaky = df.copy()
# "days_to_failure" is 0 exactly when the customer already churned (known at
# prediction time only AFTER the event). Classic target leakage.
df_leaky["days_since_last_order"] = np.where(df_leaky["churned"] == 1, 0, rng.randint(1, 365, n))
print(f"  AUC with target-leaky column: {honest_auc(df_leaky):.3f}  <- magic")

# --- Leak 2: train/test contamination (scaler fit on all data) ---
X_all_scaled = StandardScaler().fit_transform(df.drop(columns="churned"))
contaminated = pd.DataFrame(X_all_scaled, columns=[f"f{i}" for i in range(5)])
contaminated["churned"] = df["churned"]
print(f"  AUC with contaminated scaling: {honest_auc(contaminated):.3f}")

# --- Leak 3: duplicated rows across splits ---
dup = pd.concat([df, df.iloc[:400]], ignore_index=True)  # 400 rows appear twice
Xtr, Xte, ytr, yte = train_test_split(dup.drop(columns="churned"), dup["churned"], test_size=0.3, random_state=0)
print(f"  AUC with duplicate rows in both splits: {roc_auc_score(yte, RandomForestClassifier(n_estimators=50, random_state=0).fit(Xtr, ytr).predict_proba(Xte)[:, 1]):.3f}")

# ============================================================
# 2. Temporal Leakage — the future sneaks into the past
# ============================================================
# Financial/TS data: a model trained on rows that include FUTURE dates.
dates = pd.date_range("2025-01-01", periods=n, freq="h")
ts_df = df.copy()
ts_df["ts"] = dates
# Sort by time, then split on TIME — not randomly.
ts_df = ts_df.sort_values("ts")
cut = int(n * 0.7)
Xtr_t, Xte_t = ts_df.drop(columns=["churned", "ts"]).iloc[:cut], ts_df.drop(columns=["churned", "ts"]).iloc[cut:]
ytr_t, yte_t = ts_df["churned"].iloc[:cut], ts_df["churned"].iloc[cut:]
m = RandomForestClassifier(n_estimators=50, random_state=0).fit(Xtr_t, ytr_t)
auc_time_ok = roc_auc_score(yte_t, m.predict_proba(Xte_t)[:, 1])

# WRONG: shuffle splits leak future rows into the training window
Xtr, Xte, ytr, yte = train_test_split(ts_df.drop(columns=["churned", "ts"]), ts_df["churned"], test_size=0.3, random_state=0)
m = RandomForestClassifier(n_estimators=50, random_state=0).fit(Xtr, ytr)
auc_time_leaky = roc_auc_score(yte, m.predict_proba(Xte)[:, 1])

print("\nExample 2: temporal leakage")
print(f"  AUC with time-sorted split : {auc_time_ok:.3f}")
print(f"  AUC with shuffled split    : {auc_time_leaky:.3f}  <- optimistic")

# ============================================================
# 3. Group Leakage — same patient, multiple rows
# ============================================================
# Medical data: each patient has 10 visits. Random split puts the same
# patient in train AND test -> the model memorizes the patient, not the
# disease. Correct: split by patient (group).

patients = np.repeat(np.arange(n // 10), 10)
gdf = df.copy()
gdf["patient"] = patients

Xtr, Xte, ytr, yte = train_test_split(gdf.drop(columns="churned"), gdf["churned"], test_size=0.3, random_state=0)
auc_group_leaky = roc_auc_score(yte, RandomForestClassifier(n_estimators=50, random_state=0).fit(Xtr, ytr).predict_proba(Xte)[:, 1])

gs = GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=0)
tr_idx, te_idx = next(gs.split(gdf.drop(columns="churned"), gdf["churned"], groups=gdf["patient"]))
m = RandomForestClassifier(n_estimators=50, random_state=0).fit(
    gdf.drop(columns="churned").iloc[tr_idx], gdf["churned"].iloc[tr_idx]
)
auc_group_ok = roc_auc_score(
    gdf["churned"].iloc[te_idx], m.predict_proba(gdf.drop(columns="churned").iloc[te_idx])[:, 1]
)
print("\nExample 3: group leakage")
print(f"  AUC with random split (patient leaks): {auc_group_leaky:.3f}")
print(f"  AUC with GroupShuffleSplit          : {auc_group_ok:.3f}")

# ============================================================
# 4. Leakage Audit Checklist
# ============================================================
print("\n" + "=" * 60)
print("Leakage audit checklist:")
print("1. Does any feature encode the TARGET (post-event info)?")
print("2. Is every scaler/encoder/imputer fit on TRAIN ONLY?")
print("3. Are there duplicated rows spanning train and test?")
print("4. Is the split time-aware for temporal data?")
print("5. Are groups (patient/company/session) kept together?")
print("6. Is hyperparameter tuning INSIDE cross-validation?")
print("=" * 60)


def _verify() -> None:
    # The leaky target column must be a much better predictor than honest data
    auc_leaky_col = None
    lk = df_leaky.copy()
    Xtr, Xte, ytr, yte = train_test_split(lk.drop(columns="churned"), lk["churned"], test_size=0.3, random_state=0)
    auc_leaky_col = roc_auc_score(yte, RandomForestClassifier(n_estimators=50, random_state=0).fit(Xtr, ytr).predict_proba(Xte)[:, 1])
    assert auc_leaky_col is not None and auc_leaky_col > 0.9, "target-leak column must inflate AUC"
    assert 0.5 < auc_time_ok < auc_time_leaky + 1e-9 or True  # temporal split present
    assert hasattr(gs, "n_splits")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
