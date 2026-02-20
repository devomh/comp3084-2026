"""
Lab 04: Image Filters
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
    # Hint: Use array slicing for each channel, apply weights,
    #       sum them, and convert back to uint8
    # Luminosity weights: R=0.2989, G=0.5870, B=0.1140
    # TODO: Implement
    pass


def invert(img):
    """Invert all pixel values (create a negative).

    Args:
        img: NumPy array of shape (H, W, 3) or (H, W), dtype uint8

    Returns:
        NumPy array with same shape, dtype uint8
    """
    # Hint: This is a single NumPy operation thanks to broadcasting
    # TODO: Implement
    pass


def adjust_brightness_contrast(img, alpha=1.0, beta=0):
    """Adjust brightness and contrast.

    Args:
        img: NumPy array, dtype uint8
        alpha: Contrast multiplier (1.0 = no change, >1 = more contrast)
        beta: Brightness offset (0 = no change, >0 = brighter)

    Returns:
        NumPy array with same shape, dtype uint8
    """
    # Hint: Convert to float first to avoid overflow, apply formula,
    #       clip to [0, 255], then convert back to uint8
    # WARNING: uint8 overflow! 200 + 100 = 44 in uint8 (wraps around)
    # TODO: Implement
    pass


def threshold(gray_img, thresh=128):
    """Apply binary thresholding to a grayscale image.

    Args:
        gray_img: NumPy array of shape (H, W), dtype uint8
        thresh: Threshold value (0-255)

    Returns:
        NumPy array of shape (H, W), dtype uint8, values are 0 or 255
    """
    # Hint: Boolean comparison creates a mask, multiply by 255
    # TODO: Implement
    pass


def box_blur(img, kernel_size=3):
    """Apply box blur using manual convolution.

    Args:
        img: NumPy array of shape (H, W) or (H, W, 3), dtype uint8
        kernel_size: Size of the square kernel (must be odd)

    Returns:
        NumPy array with same shape, dtype uint8
    """
    # Strategy:
    # 1. Pad the image edges (to handle border pixels)
    # 2. For each pixel, compute the mean of its neighborhood
    # 3. Use nested loops for clarity (not performance)

    # Hint: np.pad() can add border pixels
    # TODO: Implement
    pass
