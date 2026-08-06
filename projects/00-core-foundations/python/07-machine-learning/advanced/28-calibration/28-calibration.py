"""
07-machine-learning — 28: Probability Calibration — Trustworthy Numbers
======================================================================
Topics: why raw model probabilities lie, Platt scaling (sigmoid),
        isotonic regression, reliability diagrams, calibration curves,
        why an uncalibrated model breaks downstream decisions

Why this matters for AI/backend engineering:
    If your model says 0.80 but only 0.55 of those predictions are true, any
    downstream system that acts on probabilities (auto-approval, queuing,
    risk scoring, cost optimization) makes systematically wrong decisions.
    Calibration is how you make probability = truth.

Run:      python 28-calibration.py
Verify:   python 28-calibration.py --verify
Reference: https://scikit-learn.org/stable/modules/calibration.html
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss, log_loss

rng = np.random.RandomState(0)

# SVC is chosen because its raw decision_function is NOT a probability.
X, y = make_classification(n_samples=3000, n_features=10, n_informative=6,
                           n_redundant=2, weights=[0.7, 0.3], random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.4, random_state=0)

# ============================================================
# 1. Uncalibrated model — confident but wrong
# ============================================================
svc = SVC(probability=True, random_state=0).fit(Xtr, ytr)
raw_proba = svc.predict_proba(Xte)[:, 1]

print("Example 1: raw SVC probabilities")
print(f"  Brier score (lower=better): {brier_score_loss(yte, raw_proba):.4f}")
print(f"  log loss                  : {log_loss(yte, raw_proba):.4f}")

# ============================================================
# 2. Reliability curve — the truth about your probabilities
# ============================================================
fraction_positive, mean_predicted = calibration_curve(yte, raw_proba, n_bins=5)
print("\nExample 2: reliability diagram (bin: predicted -> actual)")
for pred, actual in zip(mean_predicted, fraction_positive):
    marker = "OK " if abs(pred - actual) < 0.08 else "BIAS"
    print(f"  predicted {pred:.2f} -> actual {actual:.2f}  [{marker}]")

# ============================================================
# 3. Platt scaling — sigmoid fit to (score, label)
# ============================================================
platt = CalibratedClassifierCV(svc, method="sigmoid", cv=5)
platt.fit(Xtr, ytr)
platt_proba = platt.predict_proba(Xte)[:, 1]
print("\nExample 3: Platt scaling (sigmoid)")
print(f"  Brier score: {brier_score_loss(yte, platt_proba):.4f}")
print(f"  log loss   : {log_loss(yte, platt_proba):.4f}")

# ============================================================
# 4. Isotonic regression — non-parametric monotone fit
# ============================================================
iso = CalibratedClassifierCV(svc, method="isotonic", cv=5)
iso.fit(Xtr, ytr)
iso_proba = iso.predict_proba(Xte)[:, 1]
print("\nExample 4: isotonic regression")
print(f"  Brier score: {brier_score_loss(yte, iso_proba):.4f}")
print(f"  log loss   : {log_loss(yte, iso_proba):.4f}")

# ============================================================
# 5. Why calibration matters downstream
# ============================================================
# Cost-aware decision: auto-refund orders when P(return) < 0.2.
# With the calibrated model, exactly the 20% lowest-risk orders are chosen.
decisions_raw = raw_proba < 0.2
decisions_iso = iso_proba < 0.2
# Expected return rate among auto-approved (actual positive rate)
actual_rate_raw = yte[decisions_raw].mean() if decisions_raw.sum() else np.nan
actual_rate_iso = yte[decisions_iso].mean() if decisions_iso.sum() else np.nan
print("\nExample 5: downstream cost decision")
print(f"  auto-approve share: raw {decisions_raw.mean():.2f}  calibrated {decisions_iso.mean():.2f}")
print(f"  actual return rate among approved: raw {actual_rate_raw:.2f}  calib {actual_rate_iso:.2f}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Raw model scores are often NOT probabilities (SVC, boosting, NN)")
print("- Reliability diagrams reveal systematic bias by bin")
print("- Platt (sigmoid) for smooth calibration, isotonic for flexible")
print("- Calibrate on a HELD-OUT set, never on the training data")
print("- Uncalibrated probabilities break downstream cost decisions")
print("=" * 60)


def _verify() -> None:
    b_raw = brier_score_loss(yte, raw_proba)
    b_platt = brier_score_loss(yte, platt_proba)
    # Calibration should not degrade (often improves) Brier on this data
    assert b_platt <= b_raw + 0.01, "Platt should not be much worse than raw"
    assert len(mean_predicted) == len(fraction_positive) == 5
    assert 0.0 <= iso_proba.min() and iso_proba.max() <= 1.0
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
