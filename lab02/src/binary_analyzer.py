# binary_analyzer.py
"""
Lab 02: The Hex Detective
Binary forensics analysis toolkit.

This module provides tools for:
- Analyzing binary files and detecting file types
- Extracting embedded strings from binary data
- Repairing corrupted file headers

Reference Implementation
"""


class BinaryAnalyzer:
    """
    A forensic tool for analyzing binary files.
    Identifies file types by magic signatures and extracts embedded data.
    """

    def __init__(self, filepath):
        """
        Initialize the analyzer with a file path.

        Args:
            filepath (str): Path to the binary file to analyze
        """
        self.filepath = filepath
        self.data = b''
        self.file_type = 'Unknown'

        # Magic signature database
        self.magic_db = {
            b'\x89PNG\r\n\x1a\n': 'PNG',
            b'\xff\xd8\xff': 'JPEG',
            b'GIF87a': 'GIF',
            b'GIF89a': 'GIF',
            b'%PDF': 'PDF',
            b'PK\x03\x04': 'ZIP',
            b'\x7fELF': 'ELF (Linux Executable)',
            b'MZ': 'PE/EXE (Windows Executable)',
            b'RIFF': 'RIFF (WAV/AVI)',
            b'ID3': 'MP3 (ID3 Tag)',
            b'\xff\xfb': 'MP3 (Frame Sync)',
            b'SQLite format 3': 'SQLite Database',
            b'<!DOCTYPE': 'HTML',
            b'<?xml': 'XML',
        }

    def load_file(self):
        """
        Load the file content in binary mode.
        Handles FileNotFoundError and PermissionError gracefully.
        """
        try:
            with open(self.filepath, 'rb') as f:
                self.data = f.read()
            print(f"Loaded {len(self.data)} bytes from {self.filepath}")
        except FileNotFoundError:
            print(f"Error: File not found: {self.filepath}")
            self.data = b''
        except PermissionError:
            print(f"Error: Permission denied: {self.filepath}")
            self.data = b''

    def get_header(self, num_bytes=16):
        """
        Return the first N bytes as a formatted hex string.

        Args:
            num_bytes (int): Number of bytes to return

        Returns:
            str: Hex representation of the header bytes
        """
        header = self.data[:num_bytes]
        return header.hex(' ')

    def detect_type(self):
        """
        Detect file type by comparing header to known magic signatures.

        Returns:
            str: Detected file type or 'Unknown'
        """
        # Sort signatures by length (longest first) to match most specific
        sorted_sigs = sorted(
            self.magic_db.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )

        for signature, file_type in sorted_sigs:
            if self.data.startswith(signature):
                self.file_type = file_type
                return self.file_type

        # Check if it might be plain text
        if self._is_likely_text():
            self.file_type = 'Text/ASCII'
            return self.file_type

        self.file_type = 'Unknown'
        return self.file_type

    def _is_likely_text(self, sample_size=512):
        """
        Check if the file appears to be plain text.

        Args:
            sample_size (int): Number of bytes to sample

        Returns:
            bool: True if file appears to be text
        """
        sample = self.data[:sample_size]
        if not sample:
            return False

        # Count printable ASCII characters
        printable = sum(1 for b in sample if 32 <= b <= 126 or b in (9, 10, 13))
        ratio = printable / len(sample)

        return ratio > 0.85  # 85% printable suggests text

    def extract_strings(self, min_length=4):
        """
        Extract printable ASCII strings from binary data.

        Args:
            min_length (int): Minimum string length to extract

        Returns:
            list: List of extracted strings
        """
        strings = []
        current_string = []

        for byte in self.data:
            if 32 <= byte <= 126:
                current_string.append(chr(byte))
            else:
                if len(current_string) >= min_length:
                    strings.append(''.join(current_string))
                current_string = []

        # Don't forget the last string
        if len(current_string) >= min_length:
            strings.append(''.join(current_string))

        return strings

    def hexdump(self, start=0, length=256):
        """
        Generate a formatted hex dump of the data.

        Args:
            start (int): Starting offset
            length (int): Number of bytes to dump

        Returns:
            str: Formatted hex dump string
        """
        lines = []
        chunk_size = 16

        end = min(start + length, len(self.data))
        data_slice = self.data[start:end]

        for i in range(0, len(data_slice), chunk_size):
            chunk = data_slice[i:i + chunk_size]
            offset = start + i

            # Format offset
            offset_str = f'{offset:08x}'

            # Format hex bytes
            hex_bytes = ' '.join(f'{b:02x}' for b in chunk)
            hex_bytes = hex_bytes.ljust(chunk_size * 3 - 1)

            # Format ASCII representation
            ascii_repr = ''.join(
                chr(b) if 32 <= b < 127 else '.'
                for b in chunk
            )

            lines.append(f'{offset_str}  {hex_bytes}  |{ascii_repr}|')

        return '\n'.join(lines)

    def report(self):
        """
        Print a comprehensive analysis report.
        """
        print("=" * 60)
        print(f"Binary Analysis Report: {self.filepath}")
        print("=" * 60)

        # File info
        print(f"\nFile Size: {len(self.data)} bytes")
        print(f"Detected Type: {self.file_type}")

        # Header bytes
        print(f"\nHeader (first 16 bytes):")
        print(f"  Hex: {self.get_header(16)}")

        # First bytes as ASCII (if printable)
        header = self.data[:16]
        ascii_header = ''.join(chr(b) if 32 <= b < 127 else '.' for b in header)
        print(f"  ASCII: {ascii_header}")

        # Extracted strings (first 5)
        strings = self.extract_strings(min_length=6)
        if strings:
            print(f"\nExtracted Strings (first 5 of {len(strings)}):")
            for s in strings[:5]:
                # Truncate long strings
                display = s[:50] + '...' if len(s) > 50 else s
                print(f"  - {display}")
        else:
            print("\nNo significant strings found.")

        # Hex dump preview
        print(f"\nHex Dump (first 64 bytes):")
        print(self.hexdump(0, 64))

        print("\n" + "=" * 60)


class FileRepairer:
    """
    A forensic tool for repairing corrupted file headers.
    """

    # Known file signatures
    SIGNATURES = {
        'PNG': bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]),
        'JPEG': bytes([0xFF, 0xD8, 0xFF, 0xE0]),
        'GIF': b'GIF89a',
        'PDF': b'%PDF-1.4',
        'ZIP': bytes([0x50, 0x4B, 0x03, 0x04]),
    }

    def __init__(self, filepath):
        """
        Initialize the repairer with a file path.

        Args:
            filepath (str): Path to the corrupted file
        """
        self.filepath = filepath
        self.data = None
        self.load_file()

    def load_file(self):
        """Load file as mutable bytearray."""
        try:
            with open(self.filepath, 'rb') as f:
                self.data = bytearray(f.read())
            print(f"Loaded {len(self.data)} bytes from {self.filepath}")
        except FileNotFoundError:
            print(f"Error: File not found: {self.filepath}")
            self.data = bytearray()
        except PermissionError:
            print(f"Error: Permission denied: {self.filepath}")
            self.data = bytearray()

    def diagnose(self, file_type='PNG'):
        """
        Compare file header to expected signature.

        Args:
            file_type (str): Expected file type (PNG, JPEG, etc.)

        Returns:
            list: List of (index, expected, actual) tuples for corrupted bytes
        """
        if file_type not in self.SIGNATURES:
            print(f"Unknown file type: {file_type}")
            print(f"Supported types: {', '.join(self.SIGNATURES.keys())}")
            return []

        signature = self.SIGNATURES[file_type]
        corrupted_bytes = []

        print(f"\nDiagnosis for {file_type}:")
        print(f"  Expected: {signature.hex(' ')}")
        print(f"  Actual:   {self.data[:len(signature)].hex(' ')}")
        print()

        for i, expected in enumerate(signature):
            actual = self.data[i] if i < len(self.data) else None
            if actual != expected:
                corrupted_bytes.append((i, expected, actual))
                actual_str = f'{actual:02x}' if actual is not None else 'N/A'
                print(f"  Byte {i}: {actual_str} should be {expected:02x}")

        if not corrupted_bytes:
            print("  No corruption detected in header!")

        return corrupted_bytes

    def repair(self, file_type='PNG', output_path=None):
        """
        Repair the file header and write to output.

        Args:
            file_type (str): Expected file type
            output_path (str): Where to write repaired file (optional)

        Returns:
            bool: True if repair successful
        """
        if file_type not in self.SIGNATURES:
            print(f"Unknown file type: {file_type}")
            return False

        if not self.data:
            print("No data loaded to repair")
            return False

        if output_path is None:
            # Generate output path by inserting '_repaired' before extension
            base, ext = self.filepath.rsplit('.', 1) if '.' in self.filepath else (self.filepath, '')
            output_path = f"{base}_repaired.{ext}" if ext else f"{self.filepath}_repaired"

        signature = self.SIGNATURES[file_type]

        # Patch the header
        print(f"\nPatching header with {file_type} signature...")
        for i, byte in enumerate(signature):
            if i < len(self.data):
                old_byte = self.data[i]
                self.data[i] = byte
                if old_byte != byte:
                    print(f"  Byte {i}: {old_byte:02x} -> {byte:02x}")

        # Write repaired file
        try:
            with open(output_path, 'wb') as f:
                f.write(self.data)
            print(f"\nRepaired file written to: {output_path}")
            return True
        except PermissionError:
            print(f"Error: Cannot write to {output_path}")
            return False

    def verify(self, filepath):
        """
        Verify a file by checking its magic signature.

        Args:
            filepath (str): Path to file to verify

        Returns:
            str: Detected file type or 'Unknown'
        """
        try:
            with open(filepath, 'rb') as f:
                header = f.read(16)
        except FileNotFoundError:
            return 'File not found'
        except PermissionError:
            return 'Permission denied'

        # Check against known signatures
        for file_type, signature in self.SIGNATURES.items():
            if header.startswith(signature):
                return file_type

        return 'Unknown'

    def auto_repair(self, output_path=None):
        """
        Attempt to identify the most likely file type and repair automatically.
        Uses heuristics to guess the intended file type.

        Args:
            output_path (str): Where to write repaired file

        Returns:
            tuple: (success: bool, detected_type: str)
        """
        # Look for partial signatures or hints
        header = bytes(self.data[:16])

        # Check for partial PNG (has 0x89 at start but corrupted PNG)
        if self.data[0] == 0x89 or b'IHDR' in header or b'IDAT' in self.data[:1000]:
            print("Detected likely PNG structure")
            success = self.repair('PNG', output_path)
            return success, 'PNG'

        # Check for JPEG markers (often have FF somewhere)
        if b'\xff\xd9' in self.data[-2:]:  # JPEG end marker
            print("Detected likely JPEG structure (end marker found)")
            success = self.repair('JPEG', output_path)
            return success, 'JPEG'

        # Check for PDF content
        if b'%%EOF' in self.data or b'/Type' in self.data:
            print("Detected likely PDF structure")
            success = self.repair('PDF', output_path)
            return success, 'PDF'

        # Check for ZIP structure
        if b'PK' in self.data[:100]:
            print("Detected likely ZIP structure")
            success = self.repair('ZIP', output_path)
            return success, 'ZIP'

        print("Could not auto-detect file type")
        return False, 'Unknown'


# Simple test when run directly
if __name__ == "__main__":
    print("BinaryAnalyzer Module")
    print("=" * 40)
    print("Classes available:")
    print("  - BinaryAnalyzer: Analyze binary files")
    print("  - FileRepairer: Repair corrupted headers")
    print()
    print("Usage:")
    print("  from binary_analyzer import BinaryAnalyzer, FileRepairer")
    print()
    print("  analyzer = BinaryAnalyzer('file.bin')")
    print("  analyzer.load_file()")
    print("  analyzer.detect_type()")
    print("  analyzer.report()")
