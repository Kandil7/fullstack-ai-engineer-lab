# Probability Calibration — Glossary

> Companion reference for the **Probability Calibration** lecture.

## Concepts

- **Calibration**: Among predictions of probability p, fraction p are actually true.
- **Reliability diagram**: Binned predicted vs actual positive rate; the diagonal = perfect calibration.
- **Brier score**: Mean squared error of predicted probabilities — lower is better.
- **Miscalibration**: Systematic bias — 0.8 predictions are really 0.55.
- **Downstream decisions**: Auto-approvals, queuing, pricing, routing that act on probabilities.

## Methods

- **Platt scaling**: Fit a logistic (sigmoid) mapping raw scores → calibrated probabilities; smooth, parametric.
- **Isotonic regression**: Non-parametric monotone fit; more flexible, needs more data.
- **`CalibratedClassifierCV(estimator, method="sigmoid"|"isotonic", cv=5)`**: sklearn wrapper adding calibration.
- **`calibration_curve(y, proba, n_bins)`**: Compute reliability diagram data.
- **Held-out rule**: Calibrate on validation data — never training data.

## Metrics

- **`brier_score_loss`**: Calibration-focused metric.
- **`log_loss`**: Rewards calibrated probabilities.
- **`mean_predicted` / `fraction_positive`**: The reliability diagram axes.

## Real-World Patterns

- **Auto-approval**: calibrate, then act on thresholds with trustworthy probabilities.
- **Risk scoring**: calibrated P(default) feeds pricing engines.
- **Ensemble scores**: model-average probabilities are often miscalibrated — recalibrate after blending.
