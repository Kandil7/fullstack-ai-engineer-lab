"""
07-machine-learning — 35: Explainability — Why Did the Model Say That?
======================================================================
Topics: permutation importance, partial dependence, LIME-style local
        surrogate models, global vs local explanations, the limits of
        explanations

Why this matters for AI/backend engineering:
    Regulators, users, and your own debugging need answers to "why?".
    Global methods (which features matter overall) and local methods (why
    THIS prediction) answer different questions. This exercise builds both
    from first principles — no black-box package needed.

Run:      python 35-explainability.py
Verify:   python 35-explainability.py --verify
Reference: https://scikit-learn.org/stable/modules/inspection.html
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance, partial_dependence
from sklearn.linear_model import Ridge
from sklearn.metrics import roc_auc_score

rng = np.random.RandomState(0)
X, y = make_classification(n_samples=3000, n_features=20, n_informative=6,
                           n_redundant=6, random_state=0)
feature_names = [f"f{i}" for i in range(20)]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

rf = RandomForestClassifier(n_estimators=100, random_state=0).fit(Xtr, ytr)

# ============================================================
# 1. Global: permutation importance (model-agnostic)
# ============================================================
pi = permutation_importance(rf, Xte, yte, n_repeats=10, random_state=0)
order = np.argsort(pi.importances_mean)[::-1]
print("Example 1: permutation importance (global)")
for i in order[:6]:
    print(f"  {feature_names[i]:>4}: {pi.importances_mean[i]:+.4f} +/- {pi.importances_std[i]:.4f}")
print("  -> break a feature and watch AUC drop; drop = importance")

# ============================================================
# 2. Global: partial dependence — how a feature drives predictions
# ============================================================
pd_res = partial_dependence(rf, Xte, [0], kind="average")
values_key = "grid_values" if "grid_values" in pd_res else "values"
print("\nExample 2: partial dependence on f0")
print(f"  f0 values      : {np.round(pd_res[values_key][0][:5], 2)}")
print(f"  avg prediction : {np.round(pd_res['average'][0][:5], 3)}")
print("  -> as f0 rises, average prediction moves up/down = the effect")

# ============================================================
# 3. Local: LIME-style explanation from first principles
# ============================================================
def lime_local_explanation(model, X_instance: np.ndarray, X_background: np.ndarray, n_samples: int = 500, seed: int = 0):
    """Perturb the instance, fit a linear surrogate, return feature weights."""
    r = np.random.RandomState(seed)
    noise = r.normal(0, np.std(X_background, axis=0), size=(n_samples, X_instance.shape[0]))
    X_pert = np.clip(X_instance + noise, X_background.min(0), X_background.max(0))
    # distance-based weights (RBF kernel)
    dist = np.linalg.norm(X_pert - X_instance, axis=1)
    kernel_w = np.exp(-(dist ** 2) / (2 * (np.median(dist) + 1e-9) ** 2))
    # local labels: the model's own probability
    y_local = model.predict_proba(X_pert)[:, 1]
    surrogate = Ridge(alpha=1.0).fit(X_pert, y_local, sample_weight=kernel_w)
    return surrogate.coef_, surrogate.intercept_


instance = Xte[0]
weights, bias = lime_local_explanation(rf, instance, Xte)
top = np.argsort(np.abs(weights))[::-1][:4]
print("\nExample 3: local explanation (LIME-style) for one prediction")
print(f"  true label {yte[0]}, predicted P=1 {rf.predict_proba([instance])[0][1]:.3f}")
for i in top:
    direction = "PUSHES toward 1" if weights[i] > 0 else "PUSHES toward 0"
    print(f"  f{i:>2} = {instance[i]:+.3f}  weight {weights[i]:+.3f}  ({direction})")

# ============================================================
# 4. Global vs local — different questions
# ============================================================
print("\nExample 4: global vs local")
print("  GLOBAL: 'income is the 2nd most important feature overall'")
print("  LOCAL : 'this loan was denied because income=40k and age=22'")
print("  Both are needed; neither substitutes for the other.")

# ============================================================
# 5. The limits of explanations
# ============================================================
print("\n" + "=" * 60)
print("Limits of explanations:")
print("- Permutation importance can be fooled by collinear features")
print("- Local surrogates are approximations of a black box")
print("- Correlations in data show up as 'importance' even if spurious")
print("- Explanations describe, they do not guarantee causality")
print("- Always pair explanation with data-quality review")
print("=" * 60)


def _verify() -> None:
    assert len(pi.importances_mean) == 20
    assert np.isfinite(pd_res["average"][0]).all()
    assert np.isfinite(weights).all() and len(weights) == 20
    assert 0 <= rf.predict_proba([instance])[0][1] <= 1
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
