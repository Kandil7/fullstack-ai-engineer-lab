"""
Unit tests for Machine Learning examples.
"""

import pytest
import numpy as np

# Skip ML tests if sklearn not available
sklearn = pytest.importorskip("sklearn")


class TestMLExamples:
    """Test ML examples."""

    def test_getting_started_imports(self):
        """Test that ML getting started imports work."""
        from ml.getting_started import X, y

        assert X.shape == (100, 1)
        assert y.shape == (100,)

    def test_ml_types(self):
        """Test ML type definitions."""
        from ml.getting_started import ml_types

        assert "Supervised Learning" in ml_types
        assert "Unsupervised Learning" in ml_types
        assert "Reinforcement Learning" in ml_types

    def test_workflow_steps(self):
        """Test ML workflow steps."""
        from ml.getting_started import workflow_steps

        assert len(workflow_steps) == 7
        assert "1. Collect Data" in workflow_steps[0]
        assert "7. Deploy Model" in workflow_steps[6]

    def test_iris_dataset(self):
        """Test Iris dataset loading."""
        from ml.getting_started import iris

        assert iris.data.shape == (150, 4)
        assert iris.target.shape == (150,)
        assert list(iris.target_names) == ["setosa", "versicolor", "virginica"]

    def test_knn_model(self):
        """Test k-NN model training."""
        from ml.getting_started import knn, X_train, X_test, y_train, y_test
        from sklearn.metrics import accuracy_score

        preds = knn.predict(X_test)
        accuracy = accuracy_score(y_test, preds)
        # Should get reasonable accuracy on Iris
        assert accuracy > 0.8

    def test_numerical_data(self):
        """Test numerical data array."""
        from ml.getting_started import numerical_data

        assert numerical_data.shape == (3, 3)

    def test_categorical_encoding(self):
        """Test categorical encoding."""
        from ml.getting_started import le, categories, encoded

        assert list(encoded) == [0, 1, 2, 0, 1]  # Depends on LabelEncoder fit order
        assert set(le.classes_) == {"bird", "cat", "dog"}

    def test_libraries(self):
        """Test library imports."""
        from ml.getting_started import libraries

        assert "NumPy" in libraries
        assert "Pandas" in libraries
        assert "Scikit-learn" in libraries
        assert "Matplotlib" in libraries
        assert "Seaborn" in libraries


class TestMLModels:
    """Test specific ML models."""

    @pytest.mark.parametrize(
        "model_file",
        [
            "02-data-mining.py",
            "03-data-set.py",
            "04-clean-data.py",
            "05-linear-regression.py",
            "06-polynomial-regression.py",
            "07-r-squared.py",
            "08-multiple-regression.py",
            "09-scale.py",
            "10-train-test.py",
            "11-decision-tree.py",
            "12-confusion-matrix.py",
            "13-correlation.py",
            "14-linear-regression-example.py",
            "15-logistic-regression.py",
            "16-k-means.py",
            "17-hierarchical-clustering.py",
            "18-pca.py",
            "19-naive-bayes.py",
            "20-random-forest.py",
            "21-svm.py",
            "22-cross-validation.py",
            "23-k-nearest-neighbors.py",
        ],
    )
    def test_ml_model_runs(self, model_file):
        """Test that ML model files execute without errors."""
        import subprocess
        import sys
        from pathlib import Path

        file_path = Path(__file__).parent.parent.parent / "ml" / model_file
        if not file_path.exists():
            pytest.skip(f"File {model_file} not found")

        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=file_path.parent,
        )

        assert result.returncode == 0, f"Failed to run {model_file}: {result.stderr}"
