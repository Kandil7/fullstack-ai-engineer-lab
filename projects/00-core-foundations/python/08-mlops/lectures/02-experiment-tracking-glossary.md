# Experiment Tracking — Glossary 02

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Artifact | MLOps | A file produced by a run (model, plot, report) |
| Experiment | MLOps | A named group of related runs |
| Hyperparameter | ML | A configuration value set before training |
| Metric | MLOps | A measured outcome of a run (accuracy, loss) |
| Params | MLOps | The configuration inputs of a run |
| Run | MLOps | One training job: params + metrics + artifacts |
| Tag | MLOps | A key/value label on a run for grouping |
| Tracking | MLOps | The practice of recording every run |

## Detailed Definitions
### Artifact
**Definition**: A file a run produces - trained weights, a confusion-matrix
plot, a report. Artifacts are referenced by path, not embedded in the log.
**Example**:
```python
tracker.log_artifact(run, "artifacts/model.pkl")
```
**Complexity**: O(size) to store.
**Related**: Run, Model Registry

### Experiment
**Definition**: A named container grouping runs that explore one question.
**Related**: Run, Tag

### Hyperparameter
**Definition**: A configuration value chosen before training (learning rate,
tree depth) as opposed to learned parameters.
**Related**: Params

### Metric
**Definition**: A numeric outcome measured during or after training.
**Example**:
```python
tracker.log_metric(run, "val_accuracy", 0.94)
```
**Related**: Run, Params

### Params
**Definition**: The inputs of a run - hyperparameters and configuration.
**Related**: Hyperparameter, Run

### Run
**Definition**: The atomic unit of tracking: one training job with its config,
results, and files.
**Related**: Experiment, Metric, Artifact

### Tag
**Definition**: A key/value label (e.g. `team=data`), enabling queries across
runs.
**Related**: Experiment

### Tracking
**Definition**: The discipline of recording runs so comparisons, audits, and
promotions are evidence-based.
**Related**: Run, Experiment

## Key Concepts Summary
### The Run Formula
- Run = params (inputs) + metrics (outputs) + artifacts (files) + metadata

### Logging Rules
- Log before and during training, never only after
- Log hashes, not datasets
- Never log PII or absolute machine paths

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Run — ___
2. Metric — ___
3. Tag — ___
4. Artifact — ___
5. Experiment — ___

**Answers:** 1-b, 2-c, 3-e, 4-a, 5-d where a=file produced by a run, b=one
training job, c=measured outcome, d=group of runs, e=label for grouping.
