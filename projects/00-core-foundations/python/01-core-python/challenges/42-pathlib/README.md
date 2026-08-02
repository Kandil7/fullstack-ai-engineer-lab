# Challenge 42: pathlib — Modern Path Handling

## 🥉 Bronze — Path Builder (~15 min)

**Task:** Implement a function that constructs standardized checkpoint paths for ML experiments.

**Signature:**
```python
def checkpoint_path(
    base_dir: Path,
    model_name: str,
    epoch: int,
    metric_name: str,
    metric_value: float,
) -> Path:
```

**Requirements:**
- Path format: `{base_dir}/{model_name}/epoch_{epoch:04d}_{metric_name}_{metric_value:.4f}.pt`
- Must use `/` operator exclusively (no string concatenation)
- Return a `Path` object

| Input | Expected |
|-------|----------|
| `Path("/models"), "bert", 1, "acc", 0.9234` | `Path("/models/bert/epoch_0001_acc_0.9234.pt")` |
| `Path("runs"), "resnet50", 42, "loss", 0.1234` | `Path("runs/resnet50/epoch_0042_loss_0.1234.pt")` |

**Constraints:** n ≤ 100. Any correct approach passes.

---

## 🥈 Silver — Checkpoint Finder (~35 min)

**Task:** Implement a function that finds the latest checkpoint in a directory based on modification time.

**Signature:**
```python
def find_latest_checkpoint(checkpoint_dir: Path) -> Path | None:
```

**Requirements:**
- Return the most recently modified `.pt` file
- Return `None` if directory doesn't exist or has no `.pt` files
- Handle permission errors gracefully (return `None`)
- Use `stat().st_mtime` for modification time

**Constraints:** n ≤ 10⁴ files. An O(n²) solution will time out.

| Scenario | Expected |
|----------|----------|
| Dir with `model_1.pt` (mtime 100), `model_2.pt` (mtime 200) | Returns path to `model_2.pt` |
| Empty directory | `None` |
| Non-existent directory | `None` |
| No `.pt` files | `None` |

---

## 🥇 Gold — Dataset Walker (~75 min)

**Task:** Implement an efficient dataset statistics collector for image classification datasets.

**Signature:**
```python
def dataset_stats(root: Path) -> dict[str, int]:
```

**Requirements:**
- Dataset structure: `root/class_name/*.{jpg,jpeg,png}`
- Return `{class_name: image_count}` for each subdirectory
- Must stream results — **never materialize full file list** (memory ≤ 50 MB for 1M files)
- Handle 100k+ files efficiently
- Case-insensitive extension matching

**Constraints:** 10⁷ files, memory ≤ 50 MB. Must be single-pass.

| Input Structure | Expected Output |
|-----------------|-----------------|
| `root/cat/img1.jpg`, `root/cat/img2.png`, `root/dog/img3.jpeg` | `{"cat": 2, "dog": 1}` |

**Follow-up:** What breaks first at 10⁹ files? (Answer: filesystem inode limits, single-directory entry limits, stat() syscall overhead)

---

## Running

```bash
pytest challenges/42-pathlib/test_challenge.py -v
```

## Test File Structure

```
challenges/42-pathlib/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```