"""
Lab 04: Main demo script.
Applies all filters and decodes the steganographic message.
"""
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from image_filters import to_grayscale, invert, adjust_brightness_contrast, threshold, box_blur
from steganography import extract_lsb_message


def demonstrate_filters(img, title="surveillance_a"):
    """Apply and display all filters on the given image."""
    gray = to_grayscale(img)
    inv = invert(img)
    bright = adjust_brightness_contrast(img, alpha=1.4, beta=30)
    thresh = threshold(gray, 128)
    blurred = box_blur(img, kernel_size=5)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(f"Matrix Vision — {title}", fontsize=16)

    panels = [
        (axes[0, 0], img,     "Original"),
        (axes[0, 1], gray,    "Grayscale (Luminosity)"),
        (axes[0, 2], inv,     "Inverted"),
        (axes[1, 0], bright,  "Brightness +30, Contrast x1.4"),
        (axes[1, 1], thresh,  "Threshold (128)"),
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


def demonstrate_steganography():
    """Decode and display the hidden message."""
    stego = np.array(Image.open('data/stego_image.png'))
    message = extract_lsb_message(stego)

    print("=" * 60)
    print("  STEGANOGRAPHY DECODE RESULT")
    print("=" * 60)
    print(f"  Message length: {len(message)} characters")
    print(f"  Decoded message: \"{message}\"")
    print("=" * 60)

    # Visualize LSB layer
    lsb_layer = (stego[:, :, 0] & 1) * 255
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(stego)
    axes[0].set_title("Stego Image (looks normal)")
    axes[0].axis('off')
    axes[1].imshow(lsb_layer, cmap='gray')
    axes[1].set_title("Red Channel LSBs (hidden data)")
    axes[1].axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Load test image
    img = np.array(Image.open('data/surveillance_a.png'))
    print(f"Loaded: shape={img.shape}, dtype={img.dtype}")

    demonstrate_filters(img)
    demonstrate_steganography()

    print("\nAll demonstrations complete.")
