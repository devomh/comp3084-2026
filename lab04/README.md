# Lab 04: Matrix Vision

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/devomh/comp3084-2026/blob/main/lab04/lab04.ipynb)

## Case Brief

### The Situation

A digital forensics unit has intercepted a set of surveillance images suspected
of containing hidden intelligence. Standard visual inspection reveals nothing
unusual — but intelligence analysts believe an adversary is using steganography
to embed secret messages inside ordinary-looking photographs. Your team has been
brought in to build a custom image analysis toolkit and decode whatever is hidden.

### Your Mission

You are a **Computer Vision Analyst** tasked with building an image processing
toolkit from scratch and using it to expose a concealed message. You will:

1. Load surveillance images as NumPy arrays and understand their structure.
2. Build five image filters using only raw array mathematics — no high-level
   image processing libraries allowed.
3. Decode a secret message hidden inside a surveillance photo using LSB
   steganography.

### The Stakes

The intercepted `stego_image.png` may contain operational intelligence. The
filters you build will also serve as the forensic enhancement tools used to
examine the images under different conditions. Every function must be correct —
one bad implementation could mean a missed clue or a false lead.

---

## Chain of Custody

### Technical Requirements

- Completion of Lab 02 (binary data, bytes, bitwise operations)
- Completion of Lab 03 (Python classes, file I/O, serialization)
- Python 3.8 or higher
- Python libraries: `numpy`, `Pillow`, `matplotlib`

```bash
pip install numpy Pillow matplotlib
```

**Library Constraints (strictly enforced):**

- **Pillow** — only `Image.open()` and `Image.fromarray().save()`
- **Matplotlib** — only `imshow()` and `plt.show()`
- **All image processing** must use raw NumPy array operations
- **No OpenCV, scikit-image, or scipy** in student code

### Evidence Files (Provided)

Located in the [`data/`](data/) directory:

1. **`surveillance_a.png`** — Primary test image for filter development
2. **`surveillance_b.png`** — Secondary image for comparison
3. **`stego_image.png`** — Suspected carrier of hidden intelligence
4. **`reference/grayscale_ref.png`** — Verification reference for grayscale output

```bash
# Verify the evidence files are present
ls data/
# Expected: surveillance_a.png  surveillance_b.png  stego_image.png  reference/
```

---

## Investigation Phases

Open [`lab04.md`](lab04.md) (or [`lab04.ipynb`](lab04.ipynb) in Jupyter/Colab) for
the guided exercises. Consult [`concepts.md`](concepts.md) for technical background.

### Phase 1: Field Work — Understanding Images as Arrays (25 min)

**Objective:** Learn how a digital image maps to a NumPy array.

- Load `surveillance_a.png` and `surveillance_b.png` as NumPy arrays
- Inspect shape, dtype, min/max values, and individual pixel values
- Visualize both images side-by-side using Matplotlib
- Extract and display each RGB channel independently

**Key insight:** A color image is a 3D array of shape `(H, W, 3)` where each
pixel stores `[Red, Green, Blue]` values in the range 0–255.

---

### Phase 2: The Build — Manual Image Filters (80 min)

**Objective:** Implement five forensic image filters in [`image_filters.py`](image_filters.py)
using only NumPy operations.

#### Part A: Grayscale Conversion (15 min)

Implement `to_grayscale()` using the **luminosity formula**:

```
gray = 0.2989 × R + 0.5870 × G + 0.1140 × B
```

Weights reflect human eye sensitivity — we perceive green most strongly and
blue least. Verify your result against `data/reference/grayscale_ref.png`.

#### Part B: Color Inversion (10 min)

Implement `invert()` using:

```
inverted = 255 - original
```

This single vectorized operation works on both color and grayscale arrays.

#### Part C: Brightness & Contrast Adjustment (15 min)

Implement `adjust_brightness_contrast()` using:

```
adjusted = clip(alpha × pixel + beta, 0, 255)
```

⚠️ **uint8 overflow warning:** `np.uint8(200) + np.uint8(100) = 44` (wraps!).
Always convert to `float64` before arithmetic, then clip and cast back.

#### Part D: Thresholding (15 min)

Implement `threshold()` to convert a grayscale image to pure black-and-white:

```
binary[y, x] = 255 if gray[y, x] > threshold else 0
```

Use a boolean mask and multiply by 255 — no loops needed.

#### Part E: Box Blur — Convolution (25 min)

Implement `box_blur()` using a sliding-window convolution. Each pixel becomes
the mean of its `kernel_size × kernel_size` neighborhood:

```python
# Pad edges, then slide kernel across every pixel
padded = np.pad(img.astype(np.float64), pad, mode='reflect')
for y in range(h):
    for x in range(w):
        result[y, x] = padded[y:y+k, x:x+k].mean()
```

For detailed convolution theory and kernel diagrams, see [`concepts.md`](concepts.md).

---

### Phase 3: Critical Incident — Steganography (35 min)

**Objective:** Expose the hidden message in `data/stego_image.png`.

Intelligence has confirmed the adversary is using **Least Significant Bit (LSB)
steganography**: the message is encoded in the lowest bit of each Red channel
pixel — a change of ±1 that is invisible to the human eye.

**Encoding protocol (declassified):**

1. The message is hidden in the LSBs of the **Red channel only**
2. The first **32 pixels** encode the message length as a 32-bit integer (MSB first)
3. The remaining pixels encode the message as **ASCII characters** (8 bits each, MSB first)

Implement `extract_lsb_message()` in [`steganography.py`](steganography.py):

```python
red_channel = img[:, :, 0].flatten()
lsbs = red_channel & 1                    # Extract LSBs with bitwise AND
# Read 32-bit length header, then decode character bytes
```

For detailed bitwise operation explanations and worked examples, see the
**Bitwise Operations** and **Steganography** sections in [`concepts.md`](concepts.md).

**Bonus — LSB Encoder (+10 pts):** Implement `encode_lsb_message()` as the
reverse operation. Verify with a round-trip test: encode a message, decode it,
confirm it matches exactly.

---

## Wrap-Up

After completing all phases, run [`main.py`](main.py) to produce a combined
filter showcase and steganography decode report:

```bash
python main.py
```

This script applies all five filters to `surveillance_a.png`, displays them in
a 2×3 grid, and prints the decoded message from `stego_image.png`. If all panels
render correctly and the message is readable, your investigation is complete.

**Before you leave:**

- Complete all sections of [`submission.md`](submission.md), including the
  decoded message, capacity analysis, and reflection questions.
- Ensure `image_filters.py`, `steganography.py`, and `main.py` all run without errors.
- Include your AI Usage Appendix if applicable.

---

## Submission Requirements

### 1. Code Files

- [`image_filters.py`](image_filters.py) — All 5 filter functions implemented
- [`steganography.py`](steganography.py) — LSB message extraction working
- [`main.py`](main.py) — Demo script runs without errors

### 2. Output Files

Generated during the investigation:

- `data/surveillance_a_filters.png` — 2×3 filter showcase
- `data/stego_analysis.png` — LSB layer visualization

### 3. Documentation

Complete [`submission.md`](submission.md) with:

- Image properties table (shape, dtype, min/max for both surveillance images)
- Decoded hidden message
- Capacity analysis (image dimensions, total Red pixels, max message length)
- Answers to all four reflection questions

---

## Evaluation Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **Image Loading & Inspection** | 10 | Shape, dtype, min/max recorded; both images visualized |
| **Grayscale Conversion** | 15 | Correct luminosity weights; exact match with reference |
| **Color Inversion** | 10 | Single vectorized operation; double-inversion round-trip passes |
| **Brightness/Contrast** | 10 | Float conversion, clip applied; no uint8 overflow |
| **Thresholding** | 10 | Boolean mask approach; output contains only 0 and 255 |
| **Box Blur** | 15 | Correct padding and sliding window; works on color and grayscale |
| **Steganography Decode** | 20 | Hidden message correctly extracted and recorded |
| **Visualization** | 10 | All filter outputs displayed and compared side-by-side |
| **Total** | **100** | |

**Bonus:** LSB Encoder (+10), Otsu Threshold (+5), Edge Detection (+5).

---

## Tips for Success

1. **Read the Field Manual first:** [`concepts.md`](concepts.md) covers NumPy
   arrays, broadcasting, convolution theory, and bitwise operations with worked
   examples. Understanding the concepts before coding will save time.

2. **Watch out for uint8 overflow:** This is the most common bug in this lab.
   Before any arithmetic operation on pixel values, cast to `float64`. After
   clipping, cast back to `uint8`.

3. **Test incrementally:** After implementing each filter, immediately test it
   and verify the output before moving on:
   ```python
   gray = to_grayscale(img)
   print(gray.shape, gray.dtype)  # Should be (H, W), uint8
   ```

4. **Use the reference image:** The provided `data/reference/grayscale_ref.png`
   lets you verify your grayscale implementation before proceeding:
   ```python
   ref = np.array(Image.open('data/reference/grayscale_ref.png'))
   print(np.array_equal(gray, ref))  # Should be True
   ```

5. **Visualize the LSB layer early:** Before decoding the message, extract and
   display the Red channel LSBs — structured patterns in the upper rows confirm
   the data is there:
   ```python
   lsb_layer = (stego[:, :, 0] & 1) * 255
   plt.imshow(lsb_layer, cmap='gray')
   ```

6. **Debug binary extraction by hand:** If decoding produces garbage, print
   the first 40 LSBs and verify the length header manually before debugging
   the character extraction loop.

---

## Academic Integrity Reminder

Image analysis and steganography are core digital forensics skills. You must:

- Understand every filter you implement and be able to explain the math behind it
- Be able to explain how LSB steganography works at the bit level
- Document any AI assistance used in the AI Usage Appendix

**Remember:** In a real forensic investigation, presenting results you cannot
explain or verify is inadmissible. Build it, understand it, own it.

---

## Resources

- **Field Manual:** [`concepts.md`](concepts.md) — NumPy, convolution, bitwise
  operations, and steganography theory
- **Lab Notebook:** [`lab04.md`](lab04.md) — Guided exercises with boilerplate
  code and expected outputs
- **Python `numpy` documentation:** [numpy.org/doc](https://numpy.org/doc/)
- **Pillow documentation:** [pillow.readthedocs.io](https://pillow.readthedocs.io/)
- **Matplotlib `imshow`:** [matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html)

---

## Questions?

If you encounter issues:

1. Re-read the relevant section in [`concepts.md`](concepts.md)
2. Check for uint8 overflow — convert to `float64` before arithmetic
3. Print intermediate values and shapes to isolate where the problem is
4. Verify round-trips: apply a filter, check shape and dtype, visualize the output

**Remember:** The goal is to think like a forensic analyst — every pixel tells
a story, and the tools you build determine what stories you can read.
