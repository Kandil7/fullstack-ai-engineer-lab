# Challenge 24: Saving and Export

## 🥉 Bronze — DPI Contract (~15 min)

**Task:** Save a figure at a known DPI and return its actual pixel
dimensions, parsed from the PNG header.

**Signature:**
```python
def save_fig_png(fig: plt.Figure, path: str, dpi: int) -> tuple[int, int]:
```

**Requirements:**
- `fig.savefig(path, dpi=dpi)`; parse the IHDR chunk with `struct`
  (8-byte signature, `IHDR`, then `width, height` big-endian)
- Return `(width, height)`

| Input (6x4 inch fig, dpi=150) | Expected |
|-------|----------|
| any figure | `(900, 600)` |

**Constraints:** header parsing only — no `PIL`, no matplotlib reads.
Must assert the 8-byte PNG signature.

---

## 🥈 Silver — Export Report (~35 min)

**Task:** Detect the file format from the header and report the export
metadata.

**Signature:**
```python
def export_report(path: str) -> dict[str, object]:
```

**Requirements:**
- PNG (8-byte `\x89PNG\r\n\x1a\n` signature): width/height from the
  IHDR chunk; `has_alpha` = color type 6 (RGBA channel present)
- SVG (starts with `<?xml ... <svg ...`): `"format": "svg"` with
  `width`/`height`/`has_alpha` all `None`
- Return `{"format": ..., "width": ..., "height": ..., "has_alpha": ...}`

| Input | Expected |
|-------|----------|
| 4x3 inch PNG @ 100 dpi | `format "png"`, `width 400`, `height 300` |
| SVG export of same figure | `format "svg"`, `width None` |

**Constraints:** header-based detection only — no PIL, no
matplotlib reads.
**Version note:** matplotlib ≥3.10 writes RGBA PNGs (color type 6)
even for opaque saves, so `has_alpha` reports the *channel*, not
background transparency. To prove real transparency you would need to
decode the IDAT pixels — beyond header scope.

---

## 🥇 Gold — Tight Cropping Verdict (~75 min)

**Task:** Save a figure both loose and with `bbox_inches="tight"`, and
verify the tight export actually cropped the canvas.

**Signature:**
```python
def tight_crops(fig: plt.Figure, loose_path: str, tight_path: str, dpi: int) -> bool:
```

**Requirements:**
- Save both variants at the same `dpi`
- Return True iff `tight <= loose` in **both** dimensions and the two
  are **not equal** in at least one dimension (i.e., cropping happened)

| Input (fig with a title hugging the top edge) | Expected |
|-------|----------|
| 6x4 fig @ 100 dpi | `True` |

**Constraints:** must parse headers, not guess; must not rely on
`fig.get_size_inches()`.
**Follow-up:** why can tight and loose be *equal* on some figures?
(Answer: when no artist exceeds the default canvas, the recomputed
bbox equals the original — the crop only shows when labels reach the
edges.)

---

## Running

```bash
python -m pytest 03-libraries/matplotlib/challenges/24-saving-and-export/test_challenge.py -v
```

## Test File Structure

```
challenges/24-saving-and-export/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
