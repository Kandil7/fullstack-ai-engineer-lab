# Matplotlib 24 — Saving and Export Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1 (code-output).** What prints?
```python
print(6 * 150, 4 * 150)
```

- A) `900 600`
- B) `600 400`
- C) `6 4`
- D) `150 150`

**E2.** SVG is:

- A) vector — drawing commands, sharp at any zoom
- B) raster — pixels like PNG
- C) a video format
- D) a compressed CSV

**E3 (code-output).** What prints?
```python
import struct
with open("fig.png", "rb") as fh:
    head = fh.read(8)
print(head[:4] == b"\x89PNG")
```

- A) `True`
- B) `False`
- C) `b'PNG'`
- D) raises `UnicodeDecodeError`

**E4.** `bbox_inches="tight"` in `savefig`:

- A) crops the canvas to the drawn artists
- B) enlarges the canvas to include margins
- C) compresses the file
- D) rounds the DPI up

**E5 (code-output).** What prints?
```python
import struct
with open("fig.png", "rb") as fh:
    data = fh.read(33)
w, h = struct.unpack(">II", data[16:24])
print(w, h)
```
(`fig.png` is a 6×4 inch figure saved at 150 dpi)

- A) `900 600`
- B) `600 900`
- C) `6 4`
- D) `150 150`

**E6.** `matplotlib.use("Agg")` must be called:

- A) before `import matplotlib.pyplot as plt`
- B) after every `savefig`
- C) only in notebooks
- D) once per figure

---

## Medium

**M1.** The PNG signature is:

- A) `\x89PNG\r\n\x1a\n` (8 bytes)
- B) `PNG` (3 bytes)
- C) `\x89PNG` (4 bytes)
- D) `BM` (2 bytes)

**M2 (code-output).** What prints?
```python
with open("fig.png", "rb") as fh:
    data = fh.read(26)
print(data[12:16])
print(data[25])
```
(`fig.png` was saved with `transparent=True`)

- A) `b'IHDR'` `6`
- B) `b'IDAT'` `6`
- C) `b'IHDR'` `2`
- D) `b'IHDR'` `8`

**M3.** Color type 6 in a PNG IHDR chunk means:

- A) RGBA — an alpha channel is present
- B) RGB — no transparency
- C) grayscale
- D) 6-bit depth

**M4.** Why does a PNG blur when zoomed but an SVG does not?

- A) PNG stores a fixed pixel grid; SVG stores drawing commands
  re-rendered at any scale
- B) PNG is compressed; SVG is not
- C) SVG stores more colors
- D) PNG is always low resolution

**M5 (code-output).** What prints?
```python
print(6 * 100, 4 * 100)
```

- A) `600 400`
- B) `900 600`
- C) `100 100`
- D) `6 4`

**M6 (code-output).** What prints?
```python
with open("fig.svg", "r", encoding="utf-8") as fh:
    head = fh.read(200)
print("<svg" in head)
```

- A) `True`
- B) `False`
- C) `b'<svg'`
- D) raises `UnicodeDecodeError`

**M7.** Saving before `plt.show()` (in scripts) is important because:

- A) interactive backends may clear the canvas after show
- B) show() deletes the file
- C) savefig is slower after show
- D) it is not important at all

**M8.** `png_dimensions(path)` reads the IHDR chunk because:

- A) width/height live at fixed offsets after the signature — O(1),
  no image library
- B) PNG stores dimensions in a database
- C) it is the only way to open a PNG
- D) matplotlib requires it

**M9.** `transparent=True` is used when:

- A) compositing the figure onto a colored slide/dark dashboard
- B) making the plot invisible
- C) hiding the axes
- D) reducing the file size to zero

---

## Hard

**H1 (code-output).** What prints?
```python
import struct
def dims(path):
    with open(path, "rb") as fh:
        data = fh.read(33)
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    return struct.unpack(">II", data[16:24])
fig.savefig("loose.png", dpi=100)
fig.savefig("tight.png", dpi=100, bbox_inches="tight")
wl, hl = dims("loose.png")
wt, ht = dims("tight.png")
print(wt <= wl and ht <= hl)
print((wt, ht) != (wl, hl))
```

- A) `True` `True`
- B) `True` `False`
- C) `False` `True`
- D) `False` `False`

**H2.** "Tight and loose can be equal" — when?

- A) when no artist exceeds the default canvas, the recomputed bbox
  matches the original
- B) never — tight always crops
- C) when the DPI is 100
- D) when the figure is a square

**H3.** Asserting `png_dimensions(path) == (900, 600)` in CI proves:

- A) the export contract (inches × dpi) was honored — the file itself
  is the source of truth
- B) the plot is beautiful
- C) the data is correct
- D) matplotlib is installed

**H4.** For an audit-ready model card, prefer:

- A) SVG/PDF — labels stay selectable/searchable text
- B) PNG at 72 dpi
- C) JPEG
- D) screenshots

**H5.** The reproducible-export recipe is:

- A) Agg backend + fixed figsize/dpi + fixed seed
- B) Agg backend only
- C) any backend + `plt.show()`
- D) saving twice and keeping the larger file

---

## Answer Key

**E1 — A.** 6 × 150 = 900, 4 × 150 = 600 — the inches × dpi contract.
*Distractors:* B is 100 dpi; C is inches; D is DPI alone.

**E2 — A.** SVG stores drawing commands — vector.
*Distractors:* B is PNG; C/D are unrelated.

**E3 — A.** PNG files start with the 8-byte signature
`\x89PNG\r\n\x1a\n`; comparing the first 4 bytes to `b"\x89PNG"` is
True.
*Distractors:* B inverts; C prints bytes not a bool; D is a decode
error, not a bytes comparison.

**E4 — A.** Tight recomputes the bbox from the artists and crops.
*Distractors:* B is the default; C is compression; D is DPI.

**E5 — A.** 6×4 in at 150 dpi → 900×600, read straight from the
header (big-endian).
*Distractors:* B swaps; C is inches; D is DPI alone.

**E6 — A.** `matplotlib.use("Agg")` must precede the pyplot import.
*Distractors:* B/C/D misplace it.

**M1 — A.** The 8-byte signature identifies a PNG.
*Distractors:* B/C truncate; D is BMP.

**M2 — A.** Bytes 12-16 are the first chunk type `IHDR`; byte 25 is
the color type — 6 (RGBA) for a transparent save.
*Distractors:* B is the data chunk; C is the opaque type; D is an
invalid type.

**M3 — A.** Color type 6 = RGBA with an alpha channel.
*Distractors:* B is type 2; C is type 0; D confuses bit depth.

**M4 — A.** Raster = fixed pixels; vector = re-rendered commands.
*Distractors:* B/C/D are false.

**M5 — A.** 100 dpi → 600×400 px — blurry in print; use ≥300.
*Distractors:* B is 150 dpi; C/D are nonsense.

**M6 — A.** SVG documents contain `<svg` in the header text.
*Distractors:* B inverts; C is bytes; D is false (read as text).

**M7 — A.** Interactive backends may clear the canvas after show —
save first.
*Distractors:* B/C/D are false.

**M8 — A.** Width/height are at fixed offsets — O(1) header parse.
*Distractors:* B/C/D are false.

**M9 — A.** Transparency lets the figure composite onto any
background.
*Distractors:* B/C/D are false.

**H1 — A.** Tight must be ≤ loose in both dimensions AND different on
an edge-hugging figure — the verified crop contract.
*Distractors:* B says equal; C/D break one condition.

**H2 — A.** When no artist overflows the canvas, the tight bbox equals
the original — the crop is conditional.
*Distractors:* B/C/D invent unconditional rules.

**H3 — A.** The file header is the ground truth for the export
contract.
*Distractors:* B/C/D are aesthetic/data claims, not verifiable here.

**H4 — A.** Vector keeps labels selectable/searchable — governance
value.
*Distractors:* B/C/D degrade text.

**H5 — A.** Agg + fixed figsize/dpi + fixed seed = identical exports
across machines.
*Distractors:* B is incomplete; C adds interactivity; D is a
superstition.

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 24](03-libraries/matplotlib/lectures/24-saving-and-export-lecture.md) ·
[Glossary 24](03-libraries/matplotlib/lectures/24-saving-and-export-glossary.md) ·
[Challenge 24](03-libraries/matplotlib/challenges/24-saving-and-export/README.md)
