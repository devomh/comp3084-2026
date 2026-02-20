"""Generate test images for Lab 04.

Dependencies: numpy, Pillow (only).
No scipy, OpenCV, or other image processing libraries required.
"""
from PIL import Image, ImageDraw
import numpy as np


def _get_font(size=16):
    """Try to load a TrueType font, fall back to Pillow's default bitmap font.

    The default bitmap font is tiny but always available.
    On most systems, at least one of the TrueType paths below will exist.
    """
    from PIL import ImageFont
    # Common font paths across platforms
    font_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",   # Debian/Ubuntu
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",               # Arch
        "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf",  # Fedora
        "/System/Library/Fonts/Helvetica.ttc",                     # macOS
        "C:\\Windows\\Fonts\\arial.ttf",                           # Windows
    ]
    for path in font_candidates:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    # Fall back to default (small but functional)
    return ImageFont.load_default()


def create_surveillance_a():
    """Create a test image with varied features for filter testing.

    Contains: red square, green circle, blue triangle, gradient bar, text.
    Size: 300x300 RGB.
    """
    img = Image.new('RGB', (300, 300), (40, 40, 60))
    draw = ImageDraw.Draw(img)

    # Geometric shapes for contrast testing
    draw.rectangle([20, 20, 140, 140], fill=(200, 50, 50))    # Red square
    draw.ellipse([160, 20, 280, 140], fill=(50, 200, 50))     # Green circle
    draw.polygon([(150, 160), (90, 280), (210, 280)], fill=(50, 50, 200))  # Blue triangle

    # Gradient bar along the bottom
    for x in range(300):
        gray = int(x / 300 * 255)
        draw.line([(x, 285), (x, 299)], fill=(gray, gray, gray))

    # Text labels (uses TrueType if available, falls back to bitmap)
    font = _get_font(18)
    draw.text((10, 150), "COMP3084", fill=(255, 255, 255), font=font)
    draw.text((10, 175), "MATRIX VISION", fill=(200, 200, 0), font=font)

    img.save('data/surveillance_a.png')
    print("Created: data/surveillance_a.png (300x300 RGB)")
    return img


def create_surveillance_b():
    """Create a second test image with smooth gradients and noise.

    Contains: R/G/B gradients with random noise overlay.
    Size: 300x300 RGB.
    """
    np.random.seed(3084)
    y, x = np.mgrid[0:300, 0:300]
    r = np.clip(x * 255 // 300, 0, 255).astype(np.uint8)
    g = np.clip(y * 255 // 300, 0, 255).astype(np.uint8)
    b = np.clip(255 - (x + y) * 255 // 600, 0, 255).astype(np.uint8)
    img_array = np.stack([r, g, b], axis=-1)

    # Add random noise (int16 to avoid uint8 overflow)
    noise = np.random.randint(-20, 20, img_array.shape)
    img_array = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    Image.fromarray(img_array).save('data/surveillance_b.png')
    print("Created: data/surveillance_b.png (300x300 RGB)")
    return img_array


def _manual_box_blur(arr, radius=2):
    """Simple box blur using only NumPy (no scipy).

    Blurs a 2D or 3D uint8 array by averaging each pixel's neighborhood.
    Uses cumulative sums for O(1)-per-pixel performance.

    Args:
        arr: NumPy array of shape (H, W) or (H, W, C), dtype uint8.
        radius: Half-size of the blur kernel (kernel is 2*radius+1 square).

    Returns:
        Blurred array with same shape and dtype.
    """
    arr_f = arr.astype(np.float64)

    # If 3D (color), blur each channel independently
    if arr_f.ndim == 3:
        return np.stack([_manual_box_blur(arr_f[:, :, c], radius)
                         for c in range(arr_f.shape[2])], axis=-1).astype(np.uint8)

    # 2D case: cumulative sum approach (summed area table)
    h, w = arr_f.shape
    padded = np.pad(arr_f, radius, mode='reflect')
    # Prepend a row and column of zeros for proper inclusion-exclusion
    padded = np.pad(padded, ((1, 0), (1, 0)), mode='constant', constant_values=0)
    cs = np.cumsum(np.cumsum(padded, axis=0), axis=1)
    k = 2 * radius + 1
    # Inclusion-exclusion on the summed area table
    blurred = (cs[k:k+h, k:k+w] - cs[:h, k:k+w] - cs[k:k+h, :w] + cs[:h, :w]) / (k * k)
    return np.clip(blurred, 0, 255).astype(np.uint8)


# ─── Steganography constants ───
STEGO_HIDDEN_MESSAGE = (
    "CASE-7742: Rendezvous at Grid Reference 42-17. "
    "Bring the cipher key. - Control"
)
"""The exact message hidden inside stego_image.png.
Used by generate_test_images.py for encoding and by the answer key for verification.
Students must extract this string to complete Phase 3."""


def create_stego_image(message=STEGO_HIDDEN_MESSAGE):
    """Create an image with a hidden LSB steganographic message.

    Encoding protocol (must match extract_lsb_message):
      1. Red channel only.
      2. First 32 pixels → message length as 32-bit integer (MSB first).
      3. Next len(message)*8 pixels → ASCII characters (8 bits each, MSB first).

    Size: 200x200 RGB.
    Capacity: 200*200 = 40,000 Red pixels → 40,000 bits → 5,000 bytes max.

    No scipy dependency — uses _manual_box_blur() for smoothing.
    """
    np.random.seed(42)
    base = np.random.randint(60, 200, (200, 200, 3), dtype=np.uint8)

    # Smooth the random noise to look like a real photograph
    # (uses the manual box blur above — no scipy needed)
    base = _manual_box_blur(base, radius=2)

    # --- Encode message in Red channel LSBs ---
    red = base[:, :, 0].flatten()

    msg_bytes = message.encode('ascii')
    msg_length = len(msg_bytes)

    # Capacity check
    total_bits = 32 + msg_length * 8
    assert total_bits <= len(red), (
        f"Message too long: needs {total_bits} bits but image has {len(red)} Red pixels"
    )

    # Encode length as 32-bit integer (MSB first)
    length_bits = [(msg_length >> (31 - i)) & 1 for i in range(32)]

    # Encode each character as 8 bits (MSB first)
    msg_bits = []
    for byte_val in msg_bytes:
        for i in range(7, -1, -1):
            msg_bits.append((byte_val >> i) & 1)

    all_bits = length_bits + msg_bits

    # Set LSBs: clear bit 0 then set to desired value
    for i, bit in enumerate(all_bits):
        red[i] = (red[i] & 0xFE) | bit

    base[:, :, 0] = red.reshape(200, 200)
    Image.fromarray(base).save('data/stego_image.png')
    print(f"Created: data/stego_image.png (200x200 RGB, hidden: {msg_length} chars)")
    return base


def create_grayscale_reference():
    """Create reference grayscale of surveillance_a for student verification.

    Uses the same luminosity formula students must implement:
        gray = 0.2989 * R + 0.5870 * G + 0.1140 * B

    Students compare their to_grayscale() output against this file.
    """
    img = np.array(Image.open('data/surveillance_a.png'))
    gray = (0.2989 * img[:, :, 0]
          + 0.5870 * img[:, :, 1]
          + 0.1140 * img[:, :, 2])
    gray = np.clip(gray, 0, 255).astype(np.uint8)

    Image.fromarray(gray, mode='L').save('data/reference/grayscale_ref.png')
    print("Created: data/reference/grayscale_ref.png")


if __name__ == "__main__":
    import os
    os.makedirs('data/reference', exist_ok=True)

    # Generate in order (grayscale_ref depends on surveillance_a)
    create_surveillance_a()
    create_surveillance_b()
    create_stego_image()
    create_grayscale_reference()

    # Print verification summary
    print("\n--- Verification ---")
    print(f"Stego hidden message ({len(STEGO_HIDDEN_MESSAGE)} chars):")
    print(f"  \"{STEGO_HIDDEN_MESSAGE}\"")
    print("\nTest image generation complete!")
