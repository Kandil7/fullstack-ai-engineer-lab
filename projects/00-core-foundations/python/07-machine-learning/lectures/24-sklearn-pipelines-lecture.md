# sklearn Pipelines — Fit on Train Only

> **Topic 24 — ML rigor series.** `Pipeline`, `ColumnTransformer`, `FeatureUnion`,
> custom transformers — and why a pipeline is the #1 leakage-prevention tool in
> production ML.

Companion exercise: `24-sklearn-pipelines.py`

---

## 1. The Core Idea

A `Pipeline` bundles every preprocessing step and the final estimator into one
object with a single `fit` / `predict` interface:

```python
pipe = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression())])
pipe.fit(X_train, y_train)          # fit EVERY step on train only
pipe.predict(X_test)                # reuse fitted steps on test
```

Because each step is fit **inside** the pipeline, no test information can leak
into training transforms. Do the same thing by hand and you *will* eventually
fit a scaler or encoder on the full dataset.

## 2. ColumnTransformer — Different Recipes per Column Group

Real data mixes numerics and categoricals, each needing its own treatment:

```python
preprocessor = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler())]), ["age", "income"]),
    ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                      ("onehot", OneHotEncoder(handle_unknown="ignore"))]),
            ["plan", "region"]),
])
```

- Numeric columns: impute → scale.
- Categorical columns: impute → one-hot.
- Unseen categories in test are handled by `handle_unknown="ignore"`.

## 3. Custom Transformers — `BaseEstimator, TransformerMixin`

Production transforms (outlier clipping, custom text features) belong in
`fit`/`transform` classes so the pipeline can manage their lifecycle:

```python
class ClipOutliers(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.low_ = np.quantile(X, 0.01, axis=0)   # learned on TRAIN only
        self.high_ = np.quantile(X, 0.99, axis=0)
        return self

    def transform(self, X):
        return np.clip(X, self.low_, self.high_)
```

The moment it lives inside a `Pipeline`, the "fit on train, apply to all"
guarantee is automatic.

## 4. FeatureUnion — Parallel Feature Extraction

`FeatureUnion` runs several extractors in parallel and concatenates results —
for example, raw features **plus** engineered polynomials:

```python
FeatureUnion([
    ("raw", FunctionTransformer()),
    ("poly", FunctionTransformer(add_age_squared, validate=False)),
])
```

## 5. Tuning the Whole Pipeline

Grid-search the pipeline, not the model: parameter names use double-underscore
paths (`clf__n_estimators`, `prep__num__impute__strategy`). Because the CV
happens on the pipeline, transforms are refit inside every fold — no leakage,
honest scores.

## 6. Real-World Use Case — Loan Default Risk

```python
full = Pipeline([
    ("prep", ColumnTransformer([...])),
    ("clf", RandomForestClassifier(n_estimators=200, random_state=0)),
])
grid = GridSearchCV(full, {"clf__max_depth": [5, 10], "clf__n_estimators": [100, 200]}, cv=5)
grid.fit(X_train, y_train)                    # one object, no leakage
prob = grid.predict_proba(X_loan)             # deploy the whole pipeline
```

## Key Takeaways

1. Pipeline = one `fit`/`predict` unit for preprocess + model.
2. ColumnTransformer routes column groups to different recipes.
3. Custom transformers get train-only fitting for free inside a pipeline.
4. `FeatureUnion` composes parallel extractors.
5. Tune pipelines, never bare models.
