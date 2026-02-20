"""
Lab 04 Reference Implementation: LSB Steganography
"""
import numpy as np


def extract_lsb_message(img):
    """Extract a hidden message from the LSBs of the Red channel.

    Protocol:
      - Bits are in the Red channel (index 0) only.
      - First 32 pixels: message length as 32-bit integer (MSB first).
      - Next length*8 pixels: ASCII characters (8 bits each, MSB first).

    Args:
        img: NumPy array of shape (H, W, 3), dtype uint8

    Returns:
        str: The decoded hidden message
    """
    # Step 1: Flatten the Red channel
    red_channel = img[:, :, 0].flatten()

    # Step 2: Extract all LSBs
    lsbs = red_channel & 1

    # Step 3: Read 32-bit length header
    msg_length = 0
    for bit in lsbs[:32]:
        msg_length = (msg_length << 1) | int(bit)

    # Step 4: Read message characters
    message = ''
    for i in range(msg_length):
        byte_bits = lsbs[32 + i * 8 : 32 + (i + 1) * 8]
        char_value = 0
        for bit in byte_bits:
            char_value = (char_value << 1) | int(bit)
        message += chr(char_value)

    return message


def encode_lsb_message(img, message):
    """Hide a message in the LSBs of the Red channel.

    Args:
        img: NumPy array of shape (H, W, 3), dtype uint8
        message: str to hide (ASCII only)

    Returns:
        NumPy array (modified copy) with message encoded in LSBs
    """
    result = img.copy()
    red = result[:, :, 0].flatten()

    msg_bytes = message.encode('ascii')
    msg_length = len(msg_bytes)

    # Capacity check
    total_bits = 32 + msg_length * 8
    if total_bits > len(red):
        raise ValueError(
            f"Message too long: needs {total_bits} bits, "
            f"image has {len(red)} Red pixels"
        )

    # Build bit stream: 32-bit length header + message bits
    all_bits = []

    # Length header (32 bits, MSB first)
    for i in range(31, -1, -1):
        all_bits.append((msg_length >> i) & 1)

    # Message body (8 bits per char, MSB first)
    for byte_val in msg_bytes:
        for i in range(7, -1, -1):
            all_bits.append((byte_val >> i) & 1)

    # Write bits into Red channel LSBs
    for i, bit in enumerate(all_bits):
        red[i] = (red[i] & 0xFE) | bit

    result[:, :, 0] = red.reshape(result.shape[0], result.shape[1])
    return result
