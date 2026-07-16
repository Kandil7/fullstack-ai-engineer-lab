"""
Exercise 02: Deployment & the fastai Stack
===========================================
Goal: build data with the DataBlock API, clean it WITH a trained model,
export a Learner, run single-image inference, and serve it via a Gradio app.

Prerequisites:
    pip install fastai==2.7.18 gradio==4.44.0

GPU note: fine_tune() is much faster on a GPU. On CPU keep epochs small, or
run on a free Kaggle/Paperspace GPU as the fast.ai course recommends.
"""

from __future__ import annotations

from pathlib import Path

from fastai.vision.all import (
    DataBlock,
    ImageBlock,
    CategoryBlock,
    Resize,
    RandomResizedCrop,
    RandomSplitter,
    aug_transforms,
    get_image_files,
    parent_label,
    vision_learner,
    resnet18,
    error_rate,
    ClassificationInterpretation,
    load_learner,
)


# ---------------------------------------------------------------------------
# 1. Build DataLoaders with the DataBlock API
# ---------------------------------------------------------------------------

def build_dataloaders(path: Path, batch_size: int = 32):
    """Assemble a DataBlock and return its DataLoaders.

    Demonstrates the six DataBlock arguments and presizing.
    """
    block = DataBlock(
        blocks=(ImageBlock, CategoryBlock),          # x=image, y=category
        get_items=get_image_files,                   # list input files
        splitter=RandomSplitter(valid_pct=0.2, seed=42),  # reproducible split
        get_y=parent_label,                          # label = parent folder
        item_tfms=Resize(460),                       # presize step 1 (CPU)
        batch_tfms=aug_transforms(size=224, min_scale=0.75),  # step 2 (GPU)
    )
    dls = block.dataloaders(path, bs=batch_size)
    # EXERCISE: call dls.show_batch(max_n=6) and confirm dls.vocab is correct.
    return dls


# ---------------------------------------------------------------------------
# 2. Inspect augmentation (item_tfms vs batch_tfms)
# ---------------------------------------------------------------------------

def build_augmented_dataloaders(path: Path):
    """Use RandomResizedCrop so one image yields many augmented views."""
    block = DataBlock(
        blocks=(ImageBlock, CategoryBlock),
        get_items=get_image_files,
        splitter=RandomSplitter(valid_pct=0.2, seed=42),
        get_y=parent_label,
        item_tfms=RandomResizedCrop(224, min_scale=0.3),  # aggressive crops
        batch_tfms=aug_transforms(),                       # rotate/warp/flip
    )
    dls = block.dataloaders(path)
    # EXERCISE: dls.train.show_batch(max_n=4, nrows=1, unique=True)
    #           to view the SAME image augmented four different ways.
    return dls


# ---------------------------------------------------------------------------
# 3. Train a quick baseline model
# ---------------------------------------------------------------------------

def train_quick_model(dls, epochs: int = 2):
    """Fine-tune resnet18 briefly — enough to guide data cleaning."""
    learn = vision_learner(dls, resnet18, metrics=error_rate)
    learn.fine_tune(epochs)
    return learn


# ---------------------------------------------------------------------------
# 4. Clean data WITH the model (plot_top_losses)
# ---------------------------------------------------------------------------

def find_noisy_data(learn) -> None:
    """Surface the most-confident mistakes — the likely mislabeled images."""
    interp = ClassificationInterpretation.from_learner(learn)
    interp.plot_confusion_matrix()
    interp.plot_top_losses(6, nrows=2)
    # EXERCISE: in a notebook, run:
    #     from fastai.vision.widgets import ImageClassifierCleaner
    #     cleaner = ImageClassifierCleaner(learn)
    #     cleaner
    # then apply cleaner.delete()/cleaner.change() to fix the data and retrain.


# ---------------------------------------------------------------------------
# 5. Export the Learner for deployment
# ---------------------------------------------------------------------------

def export_model(learn, filename: str = "model.pkl") -> Path:
    """Pickle model + transforms into a single deployable file."""
    learn.export(filename)
    return learn.path / filename


# ---------------------------------------------------------------------------
# 6. Single-image inference from an exported model
# ---------------------------------------------------------------------------

def classify_image(pkl_path: str, img_path: str) -> dict[str, float]:
    """Load an exported learner and return {class: probability} for one image."""
    inf = load_learner(pkl_path)                 # CPU-friendly, load once
    pred_class, pred_idx, probs = inf.predict(img_path)
    print(f"Predicted: {pred_class} ({float(probs[pred_idx]):.2%})")
    # EXERCISE: map every vocab entry to its probability using zip().
    return {cls: float(p) for cls, p in zip(inf.dls.vocab, probs)}


# ---------------------------------------------------------------------------
# 7. Serve the model with a Gradio Interface
# ---------------------------------------------------------------------------

def launch_gradio_app(pkl_path: str = "model.pkl") -> None:
    """Wrap the exported learner in a Gradio web app.

    On Hugging Face Spaces this same code runs as app.py.
    """
    import gradio as gr  # imported lazily so the file loads without gradio

    learn = load_learner(pkl_path)               # load once at startup
    labels = learn.dls.vocab

    def predict(img) -> dict[str, float]:
        _, _, probs = learn.predict(img)
        return {labels[i]: float(probs[i]) for i in range(len(labels))}

    demo = gr.Interface(
        fn=predict,
        inputs=gr.Image(type="pil"),
        outputs=gr.Label(num_top_classes=3),
        title="fastai Image Classifier",
    )
    demo.launch()
    # EXERCISE: add `examples=[...]` and describe the steps to host on Spaces
    #           (push app.py + model.pkl + requirements.txt to a Space repo).


# ---------------------------------------------------------------------------
# 8. Main Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the training -> clean -> export -> inference pipeline.

    Set DATA_PATH to a folder of per-class subfolders of images.
    """
    print("fastai Deployment Exercise")
    print("=" * 60)

    data_path = Path("data")  # EXERCISE: point this at your own dataset
    if not data_path.exists():
        print(f"No dataset at {data_path!r}. Add per-class image folders first.")
        return

    dls = build_dataloaders(data_path)
    learn = train_quick_model(dls, epochs=2)
    find_noisy_data(learn)
    pkl = export_model(learn, "model.pkl")
    print(f"Exported to {pkl}")

    # EXERCISE: pick a test image and inspect the probability dict.
    # print(classify_image("model.pkl", "test.jpg"))

    # EXERCISE: uncomment to serve locally.
    # launch_gradio_app("model.pkl")


if __name__ == "__main__":
    main()
