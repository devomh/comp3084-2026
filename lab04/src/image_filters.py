"""
Lab 04 Reference Implementation: Image Filters
All filters use raw NumPy only — no OpenCV, scipy, or skimage.
"""
import numpy as np


def to_grayscale(img):
    """Convert RGB image to grayscale using luminosity method.

    Args:
        img: NumPy array of shape (H, W, 3), dtype uint8

    Returns:
        NumPy array of shape (H, W), dtype uint8
    """
    # Use float to avoid uint8 overflow during weighted sum
    gray = (0.2989 * img[:, :, 0]
          + 0.5870 * img[:, :, 1]
          + 0.1140 * img[:, :, 2])
    return np.clip(gray, 0, 255).astype(np.uint8)


def invert(img):
    """Invert all pixel values (create a negative).

    Args:
        img: NumPy array of shape (H, W, 3) or (H, W), dtype uint8

    Returns:
        NumPy array with same shape, dtype uint8
    """
    # Works on any shape thanks to NumPy broadcasting.
    # uint8 subtraction: 255 - 0 = 255, 255 - 255 = 0. No overflow possible
    # because both operands are in [0, 255].
    return np.uint8(255) - img


def adjust_brightness_contrast(img, alpha=1.0, beta=0):
    """Adjust brightness and contrast.

    Args:
        img: NumPy array, dtype uint8
        alpha: Contrast multiplier (1.0 = no change, >1 = more contrast)
        beta: Brightness offset (0 = no change, >0 = brighter)

    Returns:
        NumPy array with same shape, dtype uint8
    """
    # Convert to float FIRST to avoid uint8 overflow
    result = img.astype(np.float64) * alpha + beta
    return np.clip(result, 0, 255).astype(np.uint8)


def threshold(gray_img, thresh=128):
    """Apply binary thresholding to a grayscale image.

    Args:
        gray_img: NumPy array of shape (H, W), dtype uint8
        thresh: Threshold value (0-255)

    Returns:
        NumPy array of shape (H, W), dtype uint8, values are 0 or 255
    """
    # Boolean comparison → multiply by 255 to get binary image
    return ((gray_img > thresh) * 255).astype(np.uint8)


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

    # Handle color images by blurring each channel independently
    if img.ndim == 3:
        return np.stack([box_blur(img[:, :, c], kernel_size)
                         for c in range(img.shape[2])], axis=-1)

    # Pad edges with reflected values (avoids dark borders)
    padded = np.pad(img.astype(np.float64), pad, mode='reflect')
    h, w = img.shape
    result = np.zeros((h, w), dtype=np.float64)

    # Slide the kernel over every pixel (educational clarity over speed)
    for y in range(h):
        for x in range(w):
            neighborhood = padded[y:y + kernel_size, x:x + kernel_size]
            result[y, x] = neighborhood.mean()

    return np.clip(result, 0, 255).astype(np.uint8)
