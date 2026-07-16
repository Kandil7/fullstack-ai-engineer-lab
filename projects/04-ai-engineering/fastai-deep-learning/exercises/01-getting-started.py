"""
================================================================================
 Module 01 — Getting Started (fast.ai Lesson 1)
================================================================================
Goal: Train and evaluate a cats-vs-dogs image classifier the fast.ai way —
train first, understand later — then predict and interpret its mistakes.

Prerequisites:
    pip install "fastai>=2.7,<3.0"

Note:
    A GPU (Kaggle, Paperspace Gradient, or Google Colab) is strongly
    recommended — CNN training on CPU is impractically slow. The code is
    written to be READABLE without a GPU or the dataset present: the heavy
    blocks are guarded under main() / `if __name__ == "__main__"`, and the
    `# EXERCISE:` prompts tell you what to implement or run yourself.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from fastai.vision.all import (
    DataLoaders,
    ImageDataLoaders,
    Learner,
    ClassificationInterpretation,
    Resize,
    URLs,
    error_rate,
    accuracy,
    get_image_files,
    resnet18,
    resnet34,
    untar_data,
    vision_learner,
)


# ------------------------------------------------------------------------------
# 1. Configuration
# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class TrainConfig:
    """Immutable knobs for the Lesson 1 pipeline."""

    valid_pct: float = 0.2      # fraction held out for validation
    seed: int = 42              # reproducible train/valid split
    img_size: int = 224         # square resize applied to every image
    batch_size: int = 64        # images per training step
    epochs: int = 1             # fine_tune unfrozen epochs
    metrics: tuple = field(default_factory=lambda: (error_rate, accuracy))


# ------------------------------------------------------------------------------
# 2. Labelling
# ------------------------------------------------------------------------------
def is_cat(fname: str) -> bool:
    """Return True for cat images.

    In the Oxford-IIIT Pets dataset, cat breeds are capitalised while dog
    breeds are lowercase, so the first character of the filename is the label.
    """
    return fname[0].isupper()


# ------------------------------------------------------------------------------
# 3. Build the DataLoaders
# ------------------------------------------------------------------------------
def build_dataloaders(cfg: TrainConfig) -> DataLoaders:
    """Download PETS and construct a cat-vs-dog DataLoaders."""
    path = untar_data(URLs.PETS) / "images"
    return ImageDataLoaders.from_name_func(
        path,
        get_image_files(path),
        valid_pct=cfg.valid_pct,
        seed=cfg.seed,
        label_func=is_cat,
        item_tfms=Resize(cfg.img_size),
        bs=cfg.batch_size,
    )
    # EXERCISE: call dls.show_batch(max_n=6) in a notebook to verify that the
    # images and their True/False cat labels actually line up.


# ------------------------------------------------------------------------------
# 4. Build and fine-tune the Learner (transfer learning)
# ------------------------------------------------------------------------------
def train_classifier(
    dls: DataLoaders,
    cfg: TrainConfig,
    arch: Callable = resnet34,
) -> Learner:
    """Create a pretrained ResNet learner and fine-tune it.

    vision_learner attaches a fresh head (sized to our 2 classes) onto a
    ResNet body pretrained on ImageNet. fine_tune trains the head first with
    the body frozen, then unfreezes and trains everything.
    """
    learn = vision_learner(dls, arch, metrics=list(cfg.metrics))
    learn.fine_tune(cfg.epochs)
    return learn
    # EXERCISE: swap `arch=resnet18` and `arch=resnet50` and compare the
    # error_rate against the training time for each.


# ------------------------------------------------------------------------------
# 5. Predict on a single image
# ------------------------------------------------------------------------------
def predict_image(learn: Learner, image_path: str) -> tuple[str, float]:
    """Return the predicted label and its confidence for one image."""
    pred_class, pred_idx, probs = learn.predict(image_path)
    confidence = float(probs[pred_idx])
    return str(pred_class), confidence
    # EXERCISE: download any cat or dog photo and confirm the prediction and
    # confidence look reasonable.


# ------------------------------------------------------------------------------
# 6. Interpret mistakes
# ------------------------------------------------------------------------------
def interpret(learn: Learner, k: int = 9) -> ClassificationInterpretation:
    """Build an interpretation object and plot diagnostics."""
    interp = ClassificationInterpretation.from_learner(learn)
    interp.plot_confusion_matrix(figsize=(6, 6))
    interp.plot_top_losses(k, nrows=3)
    return interp
    # EXERCISE: identify which images the model was most confidently WRONG
    # about. Are they mislabelled, ambiguous, or genuinely hard?


# ------------------------------------------------------------------------------
# 7. Report the validation metric (never the training metric!)
# ------------------------------------------------------------------------------
def report(learn: Learner) -> None:
    """Print the validation loss and error rate."""
    loss, err = learn.validate()[:2]
    print(f"validation loss = {loss:.4f}")
    print(f"error_rate      = {err:.4f}  (accuracy = {1 - err:.2%})")
    # EXERCISE: explain in one sentence why measuring on the TRAINING set
    # instead would be misleading (hint: overfitting).


# ------------------------------------------------------------------------------
# 8. Orchestration
# ------------------------------------------------------------------------------
def main() -> None:
    """Run the full Lesson 1 pipeline. Requires a GPU + internet for the data."""
    cfg = TrainConfig()
    dls = build_dataloaders(cfg)
    learn = train_classifier(dls, cfg, arch=resnet34)
    report(learn)

    # EXERCISE: uncomment once you have a test image and a trained learner.
    # label, conf = predict_image(learn, "mystery_pet.jpg")
    # print(f"{label} ({conf:.2%})")
    # interpret(learn)


if __name__ == "__main__":
    # Wrapped so importing this module never triggers a multi-GB download.
    main()
