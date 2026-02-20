# Lab 04: Matrix Vision -- Lab Notebook
**Image Processing & Steganography with NumPy Arrays**

---

## Introduction

Welcome to the Digital Forensics Image Analysis Division. You have been assigned the role of **Computer Vision Analyst** on a high-priority case. A set of surveillance images has been intercepted, and intelligence suggests they may contain hidden data encoded using steganography -- the practice of concealing messages within ordinary-looking images.

Your mission is threefold:

1. **Understand** how digital images are represented as numerical arrays.
2. **Build** a custom image processing toolkit using only raw NumPy operations -- no high-level image processing libraries.
3. **Decode** a hidden message embedded in the least significant bits of pixel values.

**Constraints:** You may use Pillow (`PIL`) only for loading and saving images. You may use Matplotlib only for visualization. All image processing must be implemented with raw NumPy array operations. No OpenCV, scikit-image, or scipy.

**Reference:** Consult [`concepts.md`](concepts.md) for detailed background on NumPy arrays, image representation, convolution theory, and bitwise operations.

---

## Phase 1: Field Work (Understanding Images as Arrays)

Before we can analyze surveillance footage, we need to understand how a computer represents an image. At its core, every digital image is a grid of numbers -- a matrix. A color image is a 3D array of shape `(height, width, 3)`, where each pixel holds three values: Red, Green, and Blue, each ranging from 0 to 255.

---

### Exercise 1.1: Loading an Image as a NumPy Array

Our first task is to load a surveillance image into memory and inspect its structure. We use Pillow only to read the file from disk, then immediately convert it to a NumPy array for all subsequent work.

```python
from PIL import Image
import numpy as np

# Load the primary surveillance image
img = np.array(Image.open('data/surveillance_a.png'))

# Inspect the array structure
print(f"Shape: {img.shape}")           # (height, width, channels)
print(f"Dtype: {img.dtype}")           # Data type of each element
print(f"Min: {img.min()}, Max: {img.max()}")  # Value range
print(f"Pixel at (0,0): {img[0, 0]}")  # First pixel [R, G, B]
print(f"Total pixels: {img.shape[0] * img.shape[1]}")
```

<details>
<summary>Expected Output</summary>

```
Shape: (300, 300, 3)
Dtype: uint8
Min: 0, Max: 255
Pixel at (0,0): [40 40 60]
Total pixels: 90000
```

The shape tells us the image is 300 pixels tall, 300 pixels wide, and has 3 color channels. The dtype `uint8` means unsigned 8-bit integers (range 0-255). The pixel at position (0,0) is the top-left corner.
</details>

**Task:** Now load `surveillance_b.png` and record its properties. How does it compare to `surveillance_a.png`?

```python
# TODO: Load surveillance_b.png and inspect its properties
img_b = np.array(Image.open('data/surveillance_b.png'))
print(f"Shape: {img_b.shape}")
print(f"Dtype: {img_b.dtype}")
print(f"Min: {img_b.min()}, Max: {img_b.max()}")
print(f"Pixel at (0,0): {img_b[0, 0]}")
```

---

### Exercise 1.2: Visualizing with Matplotlib

Numbers alone do not tell the whole story. We need to see what the surveillance images actually look like. Matplotlib's `imshow()` function can render a NumPy array as an image.

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].imshow(img)
axes[0].set_title("Surveillance A")
axes[0].axis('off')

axes[1].imshow(img_b)
axes[1].set_title("Surveillance B")
axes[1].axis('off')

plt.tight_layout()
plt.show()
```

**Key pattern to remember:** This `plt.subplots()` / `imshow()` / `axis('off')` / `tight_layout()` / `show()` pattern is the standard way to display images throughout this lab. You will use it repeatedly.

---

### Exercise 1.3: Channel Isolation

A color image has three layers stacked on top of each other: Red, Green, and Blue. We can extract each channel independently using array slicing on the third dimension.

```python
# Extract individual channels
red_channel   = img[:, :, 0]  # All rows, all columns, channel 0 (Red)
green_channel = img[:, :, 1]  # All rows, all columns, channel 1 (Green)
blue_channel  = img[:, :, 2]  # All rows, all columns, channel 2 (Blue)

print(f"Red channel shape: {red_channel.shape}")    # (300, 300) -- 2D!
print(f"Green channel shape: {green_channel.shape}")
print(f"Blue channel shape: {blue_channel.shape}")
```

```python
# Visualize each channel as a grayscale image
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(red_channel, cmap='gray')
axes[0].set_title("Red Channel")
axes[0].axis('off')

axes[1].imshow(green_channel, cmap='gray')
axes[1].set_title("Green Channel")
axes[1].axis('off')

axes[2].imshow(blue_channel, cmap='gray')
axes[2].set_title("Blue Channel")
axes[2].axis('off')

plt.tight_layout()
plt.show()
```

<details>
<summary>Expected Output</summary>

```
Red channel shape: (300, 300)
Green channel shape: (300, 300)
Blue channel shape: (300, 300)
```

Each channel is a 2D array. When displayed with `cmap='gray'`, bright areas indicate high values in that channel and dark areas indicate low values. For example, the red square in `surveillance_a.png` should appear bright in the Red channel and dark in the Green and Blue channels.
</details>

**Question:** A single channel is a 2D array with values 0-255. When displayed, why does it appear as grayscale rather than colored? What is Matplotlib actually doing when you pass `cmap='gray'`?

---

## Phase 2: The Build (Manual Image Filters)

Now that we understand how images are structured as arrays, it is time to build our forensic image processing toolkit. Implement each filter function directly in the cell provided, then run the test cell immediately below to verify your result.

---

### Part A: Grayscale Conversion (15 mins)

**Objective:** Convert a color image to grayscale using the luminosity method.

**The Science:** The human eye does not perceive all colors equally. We are most sensitive to green light, moderately sensitive to red, and least sensitive to blue. The standard luminosity formula accounts for this:

```
gray = 0.2989 * R + 0.5870 * G + 0.1140 * B
```

This produces a perceptually accurate grayscale image -- much better than a simple average of the three channels.

**Task:** Implement the `to_grayscale()` function in the cell below.

```python
def to_grayscale(img):
    """Convert RGB image to grayscale using luminosity method.

    Args:
        img: NumPy array of shape (H, W, 3), dtype uint8

    Returns:
        NumPy array of shape (H, W), dtype uint8
    """
    # Hint: Use array slicing for each channel, apply weights,
    #       sum them, and convert back to uint8.
    # Remember: multiplying a uint8 array by a float automatically
    #           promotes to float64 -- but you must cast back at the end. Use method .astype(np.uint8)
    # TODO: Implement
    pass
```

**Test your implementation:**

```python
gray = to_grayscale(img)
print(f"Input shape:  {img.shape}")    # (300, 300, 3)
print(f"Output shape: {gray.shape}")   # (300, 300)
print(f"Output dtype: {gray.dtype}")   # uint8
print(f"Output range: {gray.min()} - {gray.max()}")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(img)
axes[0].set_title("Original (Color)")
axes[0].axis('off')
axes[1].imshow(gray, cmap='gray')
axes[1].set_title("Grayscale (Luminosity)")
axes[1].axis('off')
plt.tight_layout()
plt.show()
```

**Verification:** Compare your result against the Pillow built-in conversion and the provided reference image. Your values should match within +/-1 (rounding differences are acceptable).

```python
# Compare against PIL's grayscale conversion
pil_gray = np.array(Image.open('data/surveillance_a.png').convert('L'))
difference = np.abs(gray.astype(int) - pil_gray.astype(int))
print(f"Max difference from PIL: {difference.max()}")
print(f"Mean difference from PIL: {difference.mean():.4f}")

# Compare against the provided reference
ref_gray = np.array(Image.open('data/reference/grayscale_ref.png'))
exact_match = np.array_equal(gray, ref_gray)
print(f"Exact match with reference: {exact_match}")
```

<details>
<summary>Expected Output</summary>

```
Max difference from PIL: 1
Mean difference from PIL: 0.2xxx
Exact match with reference: True
```

A max difference of 1 from PIL is normal -- it is caused by different rounding strategies. Your output should be an exact match with the reference image since it uses the same formula.
</details>

---

### Part B: Color Inversion (10 mins)

**Objective:** Create a photographic negative by computing the complement of each pixel value.

**The Math:** For any pixel value in the range [0, 255], the inversion is simply:

```
inverted = 255 - original
```

Black (0) becomes white (255). White (255) becomes black (0). Red (255, 0, 0) becomes cyan (0, 255, 255). Every color maps to its complement.

**Task:** Implement the `invert()` function in the cell below.

```python
def invert(img):
    """Invert all pixel values (create a negative).

    Args:
        img: NumPy array of shape (H, W, 3) or (H, W), dtype uint8

    Returns:
        NumPy array with same shape, dtype uint8
    """
    # Hint: This is a single NumPy operation thanks to broadcasting.
    # NumPy will apply the subtraction to every element in the array.
    # TODO: Implement
    pass
```

**Test your implementation:**

```python
inv = invert(img)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(img)
axes[0].set_title("Original")
axes[0].axis('off')
axes[1].imshow(inv)
axes[1].set_title("Inverted (Negative)")
axes[1].axis('off')
plt.tight_layout()
plt.show()

# Verification: inverting twice should return the original
double_inv = invert(inv)
print(f"Double inversion matches original: {np.array_equal(double_inv, img)}")
```

**Question:** The `invert()` function works on both color images (shape `(H, W, 3)`) and grayscale images (shape `(H, W)`) without any code change. Why? What NumPy feature makes this possible?

---

### Part C: Brightness & Contrast Adjustment (15 mins)

**Objective:** Adjust image brightness and contrast using a linear transformation.

**The Math:** Each pixel is transformed by:

```
adjusted = clip(alpha * pixel + beta, 0, 255)
```

- `alpha` controls **contrast**: 1.0 = no change, >1.0 = more contrast, <1.0 = less contrast.
- `beta` controls **brightness**: 0 = no change, >0 = brighter, <0 = darker.
- `clip` ensures values stay within the valid [0, 255] range.

**CRITICAL WARNING -- uint8 Overflow:**

Before implementing, you must understand a dangerous property of `uint8` arithmetic. Run this code:

```python
# Demonstration: uint8 overflow wraps around!
a = np.uint8(200)
b = np.uint8(100)
print(f"200 + 100 = {a + b}")   # Expected: 300. Actual: 44!
print(f"  Why? 300 - 256 = 44 (wraps around)")

# This WILL corrupt your images if you don't convert to float first!
c = np.uint8(10)
d = np.uint8(50)
print(f"10 - 50 = {c - d}")     # Expected: -40. Actual: 216!
```

<details>
<summary>Expected Output</summary>

```
200 + 100 = 44
  Why? 300 - 256 = 44 (wraps around)
10 - 50 = 216
```

The `uint8` type can only hold values 0-255. Arithmetic that exceeds this range silently wraps around, producing incorrect results. The fix: always convert to `float64` before doing arithmetic, then clip and cast back to `uint8`.
</details>

**Task:** Implement `adjust_brightness_contrast()` in the cell below.

```python
def adjust_brightness_contrast(img, alpha=1.0, beta=0):
    """Adjust brightness and contrast.

    Args:
        img: NumPy array, dtype uint8
        alpha: Contrast multiplier (1.0 = no change, >1 = more contrast)
        beta: Brightness offset (0 = no change, >0 = brighter)

    Returns:
        NumPy array with same shape, dtype uint8
    """
    # Step 1: Convert to float64 to avoid uint8 overflow. Use method .astype(np.float64)
    # Step 2: Apply the formula: alpha * pixel + beta
    # Step 3: Clip values to [0, 255]
    # Step 4: Convert back to uint8
    # TODO: Implement
    pass
```

**Test your implementation:**

```python
bright = adjust_brightness_contrast(img, alpha=1.4, beta=30)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(img)
axes[0].set_title("Original")
axes[0].axis('off')
axes[1].imshow(bright)
axes[1].set_title("Brightness +30, Contrast x1.4")
axes[1].axis('off')
plt.tight_layout()
plt.show()

# Verify no overflow occurred
print(f"Output dtype: {bright.dtype}")
print(f"Output range: {bright.min()} - {bright.max()}")
```

---

### Part D: Thresholding (15 mins)

**Objective:** Convert a grayscale image into a pure black-and-white (binary) image using a threshold value.

**The Concept:** Thresholding is one of the simplest forms of image segmentation. Every pixel above the threshold becomes white (255), and every pixel at or below becomes black (0). This separates the "foreground" from the "background."

```
binary[y, x] = 255 if gray[y, x] > threshold else 0
```

**Task:** Implement `threshold()` in the cell below.

```python
def threshold(gray_img, thresh=128):
    """Apply binary thresholding to a grayscale image.

    Args:
        gray_img: NumPy array of shape (H, W), dtype uint8
        thresh: Threshold value (0-255)

    Returns:
        NumPy array of shape (H, W), dtype uint8, values are 0 or 255
    """
    # Hint: A boolean comparison like (gray_img > thresh) produces a
    # True/False array. Multiplying by 255 converts True to 255 and
    # False to 0. Don't forget to cast to uint8!
    # TODO: Implement
    pass
```

**Test your implementation:**

```python
# First, convert to grayscale, then threshold
gray = to_grayscale(img)
binary = threshold(gray, thresh=128)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(gray, cmap='gray')
axes[0].set_title("Grayscale")
axes[0].axis('off')
axes[1].imshow(binary, cmap='gray')
axes[1].set_title("Threshold (128)")
axes[1].axis('off')
plt.tight_layout()
plt.show()

# Verify output contains only 0 and 255
unique_values = np.unique(binary)
print(f"Unique values in output: {unique_values}")
```

<details>
<summary>Expected Output</summary>

```
Unique values in output: [  0 255]
```

The binary image should contain exactly two values: 0 (black) and 255 (white). If you see other values, check your implementation.
</details>

**Experiment:** Try different threshold values (64, 128, 192) and observe how the segmentation changes. What threshold best separates the shapes from the background in `surveillance_a.png`?

---

### Part E: Box Blur -- Convolution (25 mins)

**Objective:** Implement a box blur filter using manual convolution with nested loops.

**The Concept:** A box blur replaces each pixel with the average of its neighborhood. For a 3x3 kernel, that means averaging the pixel and its 8 neighbors:

```
kernel = [[1/9, 1/9, 1/9],
          [1/9, 1/9, 1/9],
          [1/9, 1/9, 1/9]]
```

For a detailed explanation of how convolution works step-by-step, including why kernels must be odd-sized and how to handle edge pixels, see the **Convolution** section in [`concepts.md`](concepts.md).

**Task:** Implement `box_blur()` in the cell below.

```python
def box_blur(img, kernel_size=3):
    """Apply box blur using manual convolution.

    Args:
        img: NumPy array of shape (H, W) or (H, W, 3), dtype uint8
        kernel_size: Size of the square kernel (must be odd)

    Returns:
        NumPy array with same shape, dtype uint8
    """
    assert kernel_size % 2 == 1, "Kernel size must be odd"
    pad = kernel_size // 2

    # For color images, blur each channel independently
    if img.ndim == 3:
        return np.stack([box_blur(img[:, :, c], kernel_size)
                         for c in range(img.shape[2])], axis=-1)

    # Pad edges with reflected values to handle border pixels
    padded = np.pad(img.astype(np.float64), pad, mode='reflect')
    h, w = img.shape
    result = np.zeros((h, w), dtype=np.float64)

    # Slide the kernel over every pixel
    for y in range(h):
        for x in range(w):
            # Extract the neighborhood around pixel (y, x)
            neighborhood = padded[y:y + kernel_size, x:x + kernel_size]
            # The new pixel value is the mean of the neighborhood
            result[y, x] = neighborhood.mean()

    return np.clip(result, 0, 255).astype(np.uint8)
```

**Note:** The nested-loop approach above is intentionally written for clarity, not speed. A 300x300 image with a 5x5 kernel requires 300 * 300 * 25 = 2,250,000 operations. Real image processing libraries use optimized C code or FFT-based convolution for performance. For this lab, correctness matters more than speed.

**Test your implementation:**

```python
blurred_3 = box_blur(img, kernel_size=3)
blurred_5 = box_blur(img, kernel_size=5)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(img)
axes[0].set_title("Original")
axes[0].axis('off')
axes[1].imshow(blurred_3)
axes[1].set_title("Box Blur (3x3)")
axes[1].axis('off')
axes[2].imshow(blurred_5)
axes[2].set_title("Box Blur (5x5)")
axes[2].axis('off')
plt.tight_layout()
plt.show()

print(f"Original - sharp edges visible")
print(f"3x3 blur - slightly smoothed")
print(f"5x5 blur - noticeably smoothed")
```

**Question:** What happens to edges and fine details as you increase the kernel size? Why does a larger kernel produce a stronger blur?

---

### Filter Showcase

Now that all five filters are implemented, let us apply them all to `surveillance_a.png` and display the results in a single figure. This serves as both a visual summary and a verification that all your implementations work correctly.

```python
# Load the image
img = np.array(Image.open('data/surveillance_a.png'))

# Apply all filters
gray = to_grayscale(img)
inv = invert(img)
bright = adjust_brightness_contrast(img, alpha=1.4, beta=30)
binary = threshold(gray, thresh=128)
blurred = box_blur(img, kernel_size=5)

# Display in a 2x3 grid
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle("Matrix Vision -- Filter Showcase", fontsize=16)

panels = [
    (axes[0, 0], img,     "Original"),
    (axes[0, 1], gray,    "Grayscale (Luminosity)"),
    (axes[0, 2], inv,     "Inverted"),
    (axes[1, 0], bright,  "Brightness +30, Contrast x1.4"),
    (axes[1, 1], binary,  "Threshold (128)"),
    (axes[1, 2], blurred, "Box Blur (5x5)"),
]

for ax, data, label in panels:
    if data.ndim == 2:
        ax.imshow(data, cmap='gray')
    else:
        ax.imshow(data)
    ax.set_title(label)
    ax.axis('off')

plt.tight_layout()
plt.show()
```

If all six panels render correctly, your filter toolkit is complete. Proceed to Phase 3.

---

## Phase 3: Critical Incident -- Steganography

**ESCALATION NOTICE:** Intelligence has confirmed that the intercepted surveillance images contain hidden data. Analysis suggests the adversary is using **Least Significant Bit (LSB) steganography** to transmit secret messages. The message is invisible to the human eye because modifying the lowest bit of a pixel value (e.g., changing 214 to 215) produces an imperceptible color change.

Your task is to understand the encoding technique and decode the hidden message from `data/stego_image.png`.

For detailed background on binary numbers, bitwise operations, and the steganography protocol, consult the relevant sections in [`concepts.md`](concepts.md).

---

### Part A: Understanding LSB Encoding (10 mins)

**The Core Insight:** Every pixel value (0-255) is stored as 8 binary bits. The **Most Significant Bit** (MSB, bit 7) is worth 128 -- changing it produces a dramatic color shift. The **Least Significant Bit** (LSB, bit 0) is worth only 1 -- changing it is invisible to the eye.

```
Original pixel:  11010110  (214)
Modified pixel:  11010111  (215)  <-- LSB changed from 0 to 1
Difference: 1 out of 255 (0.4%) -- INVISIBLE
```

This means we can "hide" one bit of secret data in every pixel by writing our data into the LSB. To store a byte (8 bits) of information, we need 8 pixels.

**Demonstration:** Let us extract and visualize the LSB layer of our surveillance images.

```python
# Load both a normal image and the suspected stego image
normal_img = np.array(Image.open('data/surveillance_a.png'))
stego_img  = np.array(Image.open('data/stego_image.png'))

# Extract the LSB of every pixel in the Red channel
normal_lsb = (normal_img[:, :, 0] & 1) * 255  # Bitwise AND with 1, scale to visible
stego_lsb  = (stego_img[:, :, 0] & 1) * 255

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(normal_lsb, cmap='gray')
axes[0].set_title("LSB Layer: surveillance_a (Normal)")
axes[0].axis('off')
axes[1].imshow(stego_lsb, cmap='gray')
axes[1].set_title("LSB Layer: stego_image (Suspect)")
axes[1].axis('off')
plt.tight_layout()
plt.show()
```

**Question:** Examine the two LSB layers carefully. Does the normal image's LSB layer look like random noise? What about the stego image -- can you see any patterns in the top rows where data might be encoded?

---

### Part B: Decoding the Hidden Message (25 mins)

**Objective:** Extract the secret message from `data/stego_image.png`.

**The Encoding Protocol (Declassified):**

1. The message is hidden in the LSBs of the **Red channel only**.
2. The first **32 pixels** encode the message length as a 32-bit unsigned integer (MSB first).
3. The remaining pixels encode the message as **ASCII characters** (8 bits per character, MSB first).

The three helper functions below are already implemented. Read them carefully --
you will need to call them in the right order to build `extract_lsb_message()`.

```python
# Helper functions -- already implemented, do not modify

def assemble(bits):
    """Reconstruct an integer from a sequence of bits (MSB first).

    Args:    bits -- sequence of 0s and 1s
    Returns: int
    """
    value = 0
    for bit in bits:
        value = (value << 1) | int(bit)
    return value

def bits_to_symbol(bits):
    """Convert 8 bits (MSB first) to a single ASCII character.

    Args:    bits -- sequence of exactly 8 values (0 or 1)
    Returns: str (one character)
    """
    return chr(assemble(bits))

def scan(channel):
    """Extract the least significant bit from every element of a 2D array.

    Args:    channel -- 2D NumPy array (H, W), dtype uint8
    Returns: 1D NumPy array of 0s and 1s
    """
    return channel.flatten() & 1
```

**Task:** Using the helpers above, complete `extract_lsb_message()` by filling
in each blank. Each step tells you *what* to do -- you must identify *which
helper* to call and *which arguments* to pass.

```python
def extract_lsb_message(img):
    """Extract a hidden message from the LSBs of the Red channel.

    Args:
        img: NumPy array of shape (H, W, 3), dtype uint8

    Returns:
        str: The decoded hidden message
    """
    # Step 1: Get a flat 1D array of LSBs from the Red channel.
    #         Which helper? Which channel index?
    lsbs = ___(___)

    # Step 2: The first 32 LSBs encode the message length as an integer.
    #         Which helper? Which slice of lsbs?
    msg_length = ___(___)

    # Step 3: Each character occupies 8 consecutive LSBs after the 32-bit header.
    #         Which helper? How do you slice lsbs for the i-th character?
    message = ''
    for i in range(msg_length):
        message += ___(lsbs[___ : ___])

    return message
```

**Test your implementation:**

```python
stego_img = np.array(Image.open('data/stego_image.png'))
message = extract_lsb_message(stego_img)

print("=" * 60)
print("  STEGANOGRAPHY DECODE RESULT")
print("=" * 60)
print(f"  Message length: {len(message)} characters")
print(f"  Decoded message: \"{message}\"")
print("=" * 60)
```

If your implementation is correct, the decoded message will be readable English text. Record this message in your `submission.md` file.

**Capacity Analysis:** How much data could this image hold?

```python
h, w = stego_img.shape[:2]
total_red_pixels = h * w
usable_bits = total_red_pixels - 32  # subtract header
max_chars = usable_bits // 8
print(f"Image dimensions: {h} x {w}")
print(f"Total Red channel pixels: {total_red_pixels}")
print(f"Maximum message length: {max_chars} characters ({max_chars} bytes)")
```

---

### Part C: Encoding a Message (Bonus)

**Objective:** Write the reverse function -- hide your own message inside an image.

If you can decode, you should be able to encode. Implement the `encode_lsb_message()` function in the cell below that takes an image and a message string, and returns a new image with the message hidden in the Red channel LSBs.

```python
def encode_lsb_message(img, message):
    """Hide a message in the LSBs of the Red channel.

    Args:
        img: NumPy array of shape (H, W, 3), dtype uint8
        message: str to hide (ASCII only)

    Returns:
        NumPy array (modified copy) with message encoded in LSBs
    """
    # TODO: Implement the reverse of extract_lsb_message
    # 1. Make a copy of the image (don't modify the original)
    # 2. Convert message length to 32-bit binary (MSB first)
    # 3. Convert each character to 8-bit binary (MSB first)
    # 4. For each bit, clear the LSB of the target Red pixel,
    #    then set it to the desired bit: (pixel & 0xFE) | bit
    # 5. Return the modified image
    pass
```

**Test the round-trip:** Encode a message, then decode it. The result should match.

```python
# Use a clean image as the carrier
carrier = np.array(Image.open('data/surveillance_a.png'))
secret = "Testing 123 -- this message is hidden in plain sight!"

# Encode
encoded_img = encode_lsb_message(carrier, secret)

# Verify the image looks unchanged
print(f"Max pixel difference: {np.abs(carrier.astype(int) - encoded_img.astype(int)).max()}")

# Decode
recovered = extract_lsb_message(encoded_img)
print(f"Original:  \"{secret}\"")
print(f"Recovered: \"{recovered}\"")
print(f"Match: {secret == recovered}")
```

<details>
<summary>Expected Output</summary>

```
Max pixel difference: 1
Original:  "Testing 123 -- this message is hidden in plain sight!"
Recovered: "Testing 123 -- this message is hidden in plain sight!"
Match: True
```

The maximum pixel difference should be 1 (only the LSB changes). The recovered message should be an exact match.
</details>

---

## Wrap-Up

Congratulations, Analyst. You have successfully completed the Matrix Vision investigation.

**What you accomplished today:**

1. **Loaded and inspected** digital images as NumPy arrays, understanding that a color image is a 3D matrix of shape `(H, W, 3)` with `uint8` values.
2. **Implemented five image filters** from scratch using only array math: grayscale conversion, color inversion, brightness/contrast adjustment, binary thresholding, and box blur convolution.
3. **Discovered the uint8 overflow trap** and learned why type casting to float is essential before arithmetic operations on pixel data.
4. **Decoded a hidden steganographic message** using bitwise operations on the least significant bits of pixel values.
5. **Visualized** all results using Matplotlib for side-by-side comparison and verification.

**Before you leave:**

- Complete all sections of [`submission.md`](submission.md), including the decoded message, capacity analysis, and reflection questions.
- Ensure all notebook cells run without errors from top to bottom.
- Include your AI Usage Appendix if applicable.

**Looking ahead:** The array manipulation and vectorized operations you practiced today form the foundation for processing large-scale data. In upcoming labs, you will apply similar patterns to audio signals, streaming data, and more.

---
