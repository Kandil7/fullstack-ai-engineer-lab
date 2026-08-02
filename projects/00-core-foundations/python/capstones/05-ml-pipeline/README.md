# 🤖 Project 05: ML Pipeline

An end-to-end machine learning pipeline that trains multiple classifiers on the Iris dataset and compares performance.

## What This Project Practices

| Skill | Phase | Details |
|-------|-------|---------|
| scikit-learn | Phase 7 | Model training, evaluation, preprocessing |
| Pandas | Phase 3 | Results DataFrame, sorting |
| Matplotlib | Phase 3 | Bar charts, feature importance |
| Data Splitting | Phase 7 | train_test_split with stratification |
| Cross-Validation | Phase 7 | 5-fold CV evaluation |
| Model Comparison | Phase 7 | Multiple classifiers, metrics comparison |
| Feature Scaling | Phase 7 | StandardScaler |

## How to Run

```bash
# Install dependencies
pip install scikit-learn pandas matplotlib

# Run the pipeline
python projects/05-ml-pipeline/main.py
```

## What It Does

1. **Loads** the Iris dataset (3 classes, 4 features, 150 samples)
2. **Splits** data into train/test (80/20 stratified)
3. **Scales** features with StandardScaler
4. **Trains** 4 classifiers: Logistic Regression, Decision Tree, Random Forest, SVM
5. **Evaluates** with accuracy, precision, recall, F1-score, and 5-fold CV
6. **Visualizes** performance comparison and feature importance
7. **Reports** the best model

## Example Output

```
         Model  Accuracy  Precision  Recall  F1-Score  CV Mean  CV Std
0  Random Forest    0.9667     0.9689  0.9667    0.9667   0.9583  0.0589
1          SVM     0.9667     0.9689  0.9667    0.9667   0.9583  0.0589
2      Decision Tree    0.9333     0.9359  0.9333    0.9333   0.9214  0.0807
3  Logistic Regression    0.9000     0.9037  0.9000    0.9000   0.9214  0.0807
```
