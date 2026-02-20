"""
Lab 04: LSB Steganography
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
    # Step 1: Flatten the Red channel to a 1D array
    red_channel = img[:, :, 0].flatten()

    # Step 2: Extract LSBs using bitwise AND
    lsbs = red_channel & 1

    # Step 3: Read the first 32 bits as message length
    length_bits = lsbs[:32]
    # TODO: Convert 32 bits to integer
    # Hint: Iterate through bits, shift and accumulate
    #   msg_length = 0
    #   for bit in length_bits:
    #       msg_length = (msg_length << 1) | bit

    # Step 4: Read the message bits (after the 32-bit header)
    # TODO: Group bits into 8-bit chunks, convert each to ASCII char
    # Hint: for i in range(msg_length):
    #           byte_bits = lsbs[32 + i*8 : 32 + (i+1)*8]
    #           char_value = 0
    #           for bit in byte_bits:
    #               char_value = (char_value << 1) | bit
    #           message += chr(char_value)

    # Step 5: Return the decoded message
    pass


def encode_lsb_message(img, message):
    """Hide a message in the LSBs of the Red channel (Bonus).

    Args:
        img: NumPy array of shape (H, W, 3), dtype uint8
        message: str to hide (ASCII only)

    Returns:
        NumPy array (modified copy) with message encoded in LSBs
    """
    # TODO: Implement the reverse of extract_lsb_message
    # 1. Convert message length to 32-bit binary
    # 2. Convert each character to 8-bit binary
    # 3. Set LSBs of Red channel pixels accordingly
    # 4. Return modified image
    pass
