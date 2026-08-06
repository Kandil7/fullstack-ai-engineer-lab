# Pandas for ML — Glossary 43 (pandas)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| feature engineering | Pattern | Turning raw mixed-type data into numeric model input |
| `get_dummies` | Method | One-hot expansion; drifts when categories differ |
| column drift | Concept | Train/serve column sets differ; shape errors at predict |
| `reindex(fill_value=0)` | Method | The drift fix: align to a reference column list |
| leakage | Concept | Using future/test information in training |
| `StandardScaler` | Transformer | Centers/scales by fit-learned mean and std |
| fit-on-train | Rule | Transformers learn statistics from train only |
| time-based split | Pattern | Chronological cutoff for time-ordered data |
| column contract | Concept | The ordered feature-name list saved with the model |
| `.to_numpy()` | Method | The pandas -> numpy handoff |
| `ColumnTransformer` | Transformer | Routes columns to different transformers |
| `OneHotEncoder` | Transformer | sklearn one-hot with `handle_unknown` options |
| `train_test_split` | Function | Random split; wrong for time-ordered data |
| target variable | Concept | `y` — the column being predicted; never used to build X |

## Detailed Definitions

### column contract
**Definition**: The ordered list of feature names that defines the matrix
shape — saved next to the model and used to reindex serving-time frames.
**Related**: column drift, `.to_numpy()`

### column drift
**Definition**: When train and test/serve have different column sets —
usually from `get_dummies` on categories that appear in only one set.
Fixes: `reindex(columns=train_columns, fill_value=0)`.
**Related**: `get_dummies`, column contract

### `ColumnTransformer`
**Definition**: A sklearn object that applies different transformers to
different columns and concatenates results — the replayable way to handle
mixed numeric/categorical frames.
**Example**:
```python
ColumnTransformer([
    ("scale", StandardScaler(), ["amount"]),
    ("onehot", OneHotEncoder(drop="first"), ["region"]),
])
```
**Related**: `StandardScaler`, `OneHotEncoder`

### feature engineering
**Definition**: The pandas pass that converts raw columns into numeric
features: date arithmetic, flags, interactions, polynomial terms —
vectorized with `.assign`.
**Related**: column contract

### fit-on-train
**Definition**: The rule that every transformer learns its parameters from
the training split only; test and serving data are *transformed*, never
fitted. Violations are leakage.
**Related**: leakage, `StandardScaler`

### `get_dummies`
**Definition**: Expands a categorical column into one 0/1 column per value.
Simple and fast; produces column drift unless aligned to a fixed list.
**Example**:
```python
pd.get_dummies(df, prefix="plan")
```
**Complexity**: O(n x categories).
**Related**: `OneHotEncoder`, column drift

### leakage
**Definition**: Using information in training that would not be available
at prediction time — test statistics in scalers, future values in features,
random splits on time data. Inflates validation; fails in production.
**Related**: fit-on-train, time-based split

### `OneHotEncoder`
**Definition**: sklearn's one-hot encoder; supports `handle_unknown`,
`drop="first"`, and lives inside `ColumnTransformer` — the drift-safe
alternative to `get_dummies`.
**Related**: `get_dummies`, `ColumnTransformer`

### `reindex(fill_value=0)`
**Definition**: Aligns a frame to a reference index/column list, filling
missing entries with a value — the drift fix for test dummies.
**Example**:
```python
test_d.reindex(columns=train_d.columns, fill_value=0)
```
**Related**: column drift

### `StandardScaler`
**Definition**: Centers (subtract mean) and scales (divide by std) a
numeric matrix using statistics learned at `fit` time. Must be fit on train
only.
**Example**:
```python
scaler = StandardScaler().fit(X_train)
X_test_scaled = scaler.transform(X_test)
```
**Related**: fit-on-train, leakage

### target variable
**Definition**: The column being predicted (`y`). The hard rule: `y` may
never be used to build features — a leakage subclass.
**Related**: feature engineering, leakage

### time-based split
**Definition**: Splitting at a timestamp cutoff: train on the past, test on
the future. Required when data is time-ordered; random splits leak.
**Related**: leakage

### `.to_numpy()`
**Definition**: Converts a DataFrame/Series to a numpy array — the handoff
sklearn consumes. `dtype=` stabilizes the matrix dtype.
**Example**:
```python
X = df[feature_names].to_numpy(dtype=float)
```
**Related**: column contract

### `train_test_split`
**Definition**: sklearn's random splitter. Correct for i.i.d. data; wrong
for time-ordered data — use a cutoff instead.
**Related**: time-based split

## Key Concepts Summary

### The three contracts
- Split first, then engineer and fit per split
- Fit on train only; transform test and serving
- Keep the column contract (names + order) with the model

### Encoding
- `get_dummies` drifts; reindex to train columns
- `OneHotEncoder` inside `ColumnTransformer` for serving
- High-cardinality columns need target/hash encoding — not one-hot

### Handoff
- `.to_numpy(dtype=float)` at the last moment
- Assert `X.shape == (n, len(names))` before fitting

## Practice Terms

Match each term to its definition (answers at the bottom).

1. leakage — ___
2. fit-on-train — ___
3. column drift — ___
4. column contract — ___
5. `get_dummies` — ___
6. `reindex(fill_value=0)` — ___
7. time-based split — ___
8. `.to_numpy()` — ___

A. Train/serve column sets differ
B. Test statistics leaking into training
C. The feature-name list saved with the model
D. Transformers learn from train only
E. One-hot expansion that can drift
F. The pandas -> numpy handoff
G. Aligns test columns to a reference list
H. Chronological cutoff for time-ordered data

**Answers:** 1-B, 2-D, 3-A, 4-C, 5-E, 6-G, 7-H, 8-F
