# Lab 02 Notebook: The Hex Detective
**Binary Forensics Investigation**

---

## Introduction

This notebook guides you through binary file analysis step-by-step. You will learn to examine files at the byte level, identify file types by their signatures, and repair corrupted files.

**Before you begin:**
- [ ] Read [`README.md`](README.md) for the full case briefing
- [ ] Review [`concepts.md`](concepts.md) for technical background
- [ ] Ensure all files in `data/` are present
- [ ] Verify you have access to `xxd` or `hexdump` command

---

## Phase 1: Field Work - CLI Binary Forensics

### Exercise 1.1: Initial File Identification

Use the `file` command to identify file types.

**Task A: Run the file command on all evidence**
```bash
file data/*
```

**Record your observations:**
| File | `file` output |
|------|---------------|
| unknown_a.bin | |
| unknown_b.bin | |
| unknown_c.bin | |
| corrupted.png | |
| hidden_message.bin | |

**Questions:**
1. Which files did `file` successfully identify?
2. Which files returned "data" or an unexpected result?
3. Why might `corrupted.png` not be recognized as a PNG?

---

### Exercise 1.2: File Size Analysis

**Task B: Check file sizes**
```bash
ls -lh data/
```

**Record the sizes:**
| File | Size |
|------|------|
| unknown_a.bin | |
| unknown_b.bin | |
| unknown_c.bin | |
| corrupted.png | |
| hidden_message.bin | |

**Question:** Do any file sizes give hints about their content type?

---

### Exercise 1.3: Hex Dump Examination

Use `xxd` to view the first bytes of each file.

**Task C: Examine file headers**
```bash
# View first 64 bytes of each file
xxd -l 64 data/unknown_a.bin
xxd -l 64 data/unknown_b.bin
xxd -l 64 data/unknown_c.bin
xxd -l 64 data/corrupted.png
```

**Record the magic bytes (first 8-16 bytes) for each file:**

| File | First 8 bytes (hex) | Interpretation |
|------|---------------------|----------------|
| unknown_a.bin | | |
| unknown_b.bin | | |
| unknown_c.bin | | |
| corrupted.png | | |

**Reference - Common Magic Signatures:**
| File Type | Magic Bytes (Hex) |
|-----------|-------------------|
| PNG | 89 50 4E 47 0D 0A 1A 0A |
| JPEG | FF D8 FF |
| GIF | 47 49 46 38 |
| PDF | 25 50 44 46 |
| ZIP | 50 4B 03 04 |

**Questions:**
1. Based on magic bytes, what type is `unknown_a.bin`?
2. Based on magic bytes, what type is `unknown_b.bin`?
3. Does `unknown_c.bin` match any known signature?
4. What's wrong with the magic bytes in `corrupted.png`?

---

### Exercise 1.4: String Extraction

Use `strings` to find readable text in binary files.

**Task D: Extract strings from files**
```bash
# Extract strings from text-like binary
strings data/unknown_c.bin

# Extract strings from hidden message file
strings data/hidden_message.bin

# Try strings on image files (mostly noise, but interesting)
strings data/unknown_a.bin | head -n 10
```

**Questions:**
1. What is actually contained in `unknown_c.bin`?
2. What hidden messages did you find in `hidden_message.bin`?
3. Did you find any readable strings in the image files?

---

### Exercise 1.5: Comparing Corrupted vs Original

**Task E: Compare file headers**
```bash
# View the reference (uncorrupted) PNG header
xxd -l 16 data/reference/original.png

# View the corrupted PNG header
xxd -l 16 data/corrupted.png
```

**Side-by-side comparison:**
```
Original:  89 50 4E 47 0D 0A 1A 0A ...
Corrupted: ?? ?? ?? ?? ?? ?? ?? ?? ...
```

**Critical Finding:**
- Byte 1 is: ____ (should be 50, ASCII 'P')
- Byte 2 is: ____ (should be 4E, ASCII 'N')
- Byte 3 is: ____ (should be 47, ASCII 'G')

**Write your diagnosis:** What specific bytes need to be fixed?

---

---

## Phase 2: The Build - BinaryAnalyzer Class

### Exercise 2.1: Class Constructor and Magic Database

Create a file called `binary_analyzer.py` and start building the class.

> **Tip for Jupyter/Colab Users:** Use `%%writefile binary_analyzer.py` at the top of the cell.

```python
# binary_analyzer.py

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
        self.data = b''  # Raw bytes
        self.file_type = 'Unknown'

        # Magic signature database
        # Format: {signature_bytes: 'File Type Name'}
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
        }
```

**Your task:** Verify the constructor works.

**Test your constructor:**
```python
if __name__ == "__main__":
    analyzer = BinaryAnalyzer('data/unknown_a.bin')
    print(f"Filepath: {analyzer.filepath}")
    print(f"Data length: {len(analyzer.data)}")
    print(f"File type: {analyzer.file_type}")
    print(f"Magic DB entries: {len(analyzer.magic_db)}")
```

---

### Exercise 2.2: File Loading Method

Add the `load_file()` method to read binary data.

```python
def load_file(self):
    """
    Load the file content in binary mode.
    Handles FileNotFoundError gracefully.
    """
    try:
        # TODO: Open file in binary mode ('rb')
        # TODO: Read all bytes into self.data
        # Hint: with open(self.filepath, 'rb') as f:
        pass

    except FileNotFoundError:
        # TODO: Print error message
        # TODO: Set self.data to empty bytes
        pass

    except PermissionError:
        # TODO: Handle permission denied
        pass
```

**Implementation hint:**
```python
def load_file(self):
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
```

**Test your method:**
```python
if __name__ == "__main__":
    analyzer = BinaryAnalyzer('data/unknown_a.bin')
    analyzer.load_file()
    print(f"Loaded {len(analyzer.data)} bytes")
    print(f"First 16 bytes: {analyzer.data[:16]}")
```

---

### Exercise 2.3: Header Extraction Method

Add the `get_header()` method to view file headers.

```python
def get_header(self, num_bytes=16):
    """
    Return the first N bytes as a formatted hex string.

    Args:
        num_bytes (int): Number of bytes to return

    Returns:
        str: Hex representation of the header bytes
    """
    # TODO: Get the first num_bytes from self.data
    # TODO: Return as hex string with spaces between bytes
    # Hint: Use .hex(' ') for spaced hex output
    pass
```

**Test your method:**
```python
if __name__ == "__main__":
    analyzer = BinaryAnalyzer('data/unknown_a.bin')
    analyzer.load_file()
    print(f"Header: {analyzer.get_header(16)}")
```

**Expected output format:**
```
Header: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52
```

---

### Exercise 2.4: File Type Detection Method

Add the `detect_type()` method to identify files by magic bytes.

```python
def detect_type(self):
    """
    Detect file type by comparing header to known magic signatures.

    Returns:
        str: Detected file type or 'Unknown'
    """
    # TODO: Loop through self.magic_db
    # TODO: Check if self.data starts with each signature
    # TODO: Set self.file_type and return if match found
    # Hint: Use self.data.startswith(signature)

    # If no match found
    self.file_type = 'Unknown'
    return self.file_type
```

**Implementation approach:**
```python
def detect_type(self):
    for signature, file_type in self.magic_db.items():
        if self.data.startswith(signature):
            self.file_type = file_type
            return self.file_type

    self.file_type = 'Unknown'
    return self.file_type
```

**Test your method:**
```python
if __name__ == "__main__":
    for filename in ['unknown_a.bin', 'unknown_b.bin', 'unknown_c.bin']:
        analyzer = BinaryAnalyzer(f'data/{filename}')
        analyzer.load_file()
        file_type = analyzer.detect_type()
        print(f"{filename}: {file_type}")
```

---

### Exercise 2.5: String Extraction Method

Add the `extract_strings()` method to find readable text.

```python
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
        # Check if byte is printable ASCII (32-126)
        if 32 <= byte <= 126:
            current_string.append(chr(byte))
        else:
            # End of printable sequence
            if len(current_string) >= min_length:
                strings.append(''.join(current_string))
            current_string = []

    # Don't forget the last string
    if len(current_string) >= min_length:
        strings.append(''.join(current_string))

    return strings
```

**Test your method:**
```python
if __name__ == "__main__":
    analyzer = BinaryAnalyzer('data/hidden_message.bin')
    analyzer.load_file()
    strings = analyzer.extract_strings(min_length=8)
    print("Extracted strings:")
    for s in strings:
        print(f"  - {s}")
```

---

### Exercise 2.6: Hex Dump Method

Add the `hexdump()` method for formatted binary viewing.

```python
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
    chunk_size = 16  # Bytes per line

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
```

**Test your method:**
```python
if __name__ == "__main__":
    analyzer = BinaryAnalyzer('data/unknown_a.bin')
    analyzer.load_file()
    print(analyzer.hexdump(0, 64))
```

---

### Exercise 2.7: Report Method

Add the `report()` method to summarize analysis results.

```python
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

    # First few bytes as ASCII (if printable)
    header = self.data[:16]
    ascii_header = ''.join(chr(b) if 32 <= b < 127 else '.' for b in header)
    print(f"  ASCII: {ascii_header}")

    # Extracted strings (first 5)
    strings = self.extract_strings(min_length=6)
    if strings:
        print(f"\nExtracted Strings (first 5):")
        for s in strings[:5]:
            print(f"  - {s}")
    else:
        print("\nNo significant strings found.")

    print("\n" + "=" * 60)
```

**Test your complete class:**
```python
if __name__ == "__main__":
    analyzer = BinaryAnalyzer('data/unknown_a.bin')
    analyzer.load_file()
    analyzer.detect_type()
    analyzer.report()
```

---

### Exercise 2.8: Analyze All Evidence Files

Run your analyzer on all evidence files.

```python
if __name__ == "__main__":
    files = [
        'data/unknown_a.bin',
        'data/unknown_b.bin',
        'data/unknown_c.bin',
        'data/corrupted.png',
        'data/hidden_message.bin',
    ]

    for filepath in files:
        print(f"\n{'#' * 60}")
        analyzer = BinaryAnalyzer(filepath)
        analyzer.load_file()
        analyzer.detect_type()
        analyzer.report()
```

**Record your findings:**
| File | Detected Type | Actual Content |
|------|---------------|----------------|
| unknown_a.bin | | |
| unknown_b.bin | | |
| unknown_c.bin | | |
| corrupted.png | | |
| hidden_message.bin | | |

---

---

## Phase 3: Critical Incident - File Repair

### Exercise 3.1: Diagnose the Corruption

First, compare the corrupted file to the expected PNG signature.

```python
# PNG signature constant
PNG_SIGNATURE = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

# Load the corrupted file
with open('data/corrupted.png', 'rb') as f:
    corrupted_data = f.read()

print("Expected PNG signature:")
print(f"  {PNG_SIGNATURE.hex(' ')}")

print("\nCorrupted file header:")
print(f"  {corrupted_data[:8].hex(' ')}")

print("\nByte-by-byte comparison:")
for i in range(8):
    expected = PNG_SIGNATURE[i]
    actual = corrupted_data[i]
    status = "OK" if expected == actual else "CORRUPTED"
    print(f"  Byte {i}: expected {expected:02x}, got {actual:02x} - {status}")
```

**Record your findings:** Which bytes are corrupted?

---

### Exercise 3.2: Build the FileRepairer Class

Add a new class to `binary_analyzer.py` for file repair.

```python
class FileRepairer:
    """
    A forensic tool for repairing corrupted file headers.
    """

    # Known file signatures
    SIGNATURES = {
        'PNG': bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]),
        'JPEG': bytes([0xFF, 0xD8, 0xFF]),
        'GIF': b'GIF89a',
        'PDF': b'%PDF-1.',
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
            return []

        signature = self.SIGNATURES[file_type]
        corrupted_bytes = []

        print(f"\nDiagnosis for {file_type}:")
        print(f"Expected: {signature.hex(' ')}")
        print(f"Actual:   {self.data[:len(signature)].hex(' ')}")
        print()

        for i, expected in enumerate(signature):
            actual = self.data[i] if i < len(self.data) else None
            if actual != expected:
                corrupted_bytes.append((i, expected, actual))
                print(f"  Byte {i}: {actual:02x} should be {expected:02x}")

        if not corrupted_bytes:
            print("  No corruption detected!")

        return corrupted_bytes

    def repair(self, file_type='PNG', output_path=None):
        """
        Repair the file header and write to output.

        Args:
            file_type (str): Expected file type
            output_path (str): Where to write repaired file

        Returns:
            bool: True if repair successful
        """
        # TODO: Get the expected signature
        # TODO: Replace corrupted bytes with correct values
        # TODO: Write to output_path
        # TODO: Return True if successful
        pass

    def verify(self, filepath):
        """
        Verify a file by checking its magic signature.

        Args:
            filepath (str): Path to file to verify

        Returns:
            str: Detected file type or 'Unknown'
        """
        # TODO: Read the file header
        # TODO: Compare against known signatures
        # TODO: Return the detected type
        pass
```

**Your task:** Implement the `repair()` and `verify()` methods.

**Implementation hints for `repair()`:**
```python
def repair(self, file_type='PNG', output_path=None):
    if file_type not in self.SIGNATURES:
        print(f"Unknown file type: {file_type}")
        return False

    if output_path is None:
        output_path = self.filepath.replace('.', '_repaired.')

    signature = self.SIGNATURES[file_type]

    # Patch the header
    for i, byte in enumerate(signature):
        self.data[i] = byte

    # Write repaired file
    with open(output_path, 'wb') as f:
        f.write(self.data)

    print(f"Repaired file written to: {output_path}")
    return True
```

---

### Exercise 3.3: Repair the Corrupted PNG

Use your `FileRepairer` to fix `corrupted.png`.

```python
if __name__ == "__main__":
    # Create repairer instance
    repairer = FileRepairer('data/corrupted.png')

    # Diagnose the corruption
    corrupted_bytes = repairer.diagnose('PNG')

    # Perform the repair
    success = repairer.repair('PNG', 'data/repaired.png')

    if success:
        # Verify the repair
        result = repairer.verify('data/repaired.png')
        print(f"\nVerification: {result}")
```

**Verify with command line:**
```bash
# Before repair
file data/corrupted.png
# Expected: data

# After repair
file data/repaired.png
# Expected: PNG image data, 100 x 100, 8-bit/color RGB, non-interlaced
```

**Open the repaired image:**
```bash
# Linux
xdg-open data/repaired.png

# macOS
open data/repaired.png

# Windows (Git Bash)
start data/repaired.png
```

---

### Exercise 3.4: Document Your Repair

**Forensic Report:**
```
FORENSIC REPORT: CORRUPTED.PNG

Analysis Date: [Today's Date]
Analyst: [Your Name]

ORIGINAL STATE:
- File command output: data
- Header bytes: [list the corrupted bytes]

CORRUPTION IDENTIFIED:
- Byte 1: was 00, should be 50 (ASCII 'P')
- Byte 2: was 00, should be 4E (ASCII 'N')
- Byte 3: was 00, should be 47 (ASCII 'G')

REPAIR PERFORMED:
- Patched bytes 1-3 with correct PNG signature values
- Output written to: data/repaired.png

VERIFICATION:
- File command output: PNG image data, ...
- Image opens correctly: [Yes/No]

CONCLUSION:
The file header was deliberately corrupted to prevent identification.
The PNG signature bytes 'PNG' were replaced with null bytes (00 00 00).
After patching, the image is fully functional.
```

---

---

## Phase 4: Integration and Submission

### Exercise 4.1: Create main.py

Create a comprehensive analysis script.

> **Tip for Jupyter/Colab Users:** Use `%%writefile main.py` at the top of the cell.

```python
# main.py
"""
Main execution script for Lab 02: The Hex Detective
Analyzes all evidence files and repairs corrupted PNG.
"""

from binary_analyzer import BinaryAnalyzer, FileRepairer

def analyze_evidence():
    """Analyze all evidence files."""
    files = [
        'data/unknown_a.bin',
        'data/unknown_b.bin',
        'data/unknown_c.bin',
        'data/hidden_message.bin',
    ]

    print("=" * 70)
    print(" COMP3084 - Lab 02: Binary Forensics Analysis")
    print("=" * 70)

    for filepath in files:
        print(f"\n{'─' * 70}")
        analyzer = BinaryAnalyzer(filepath)
        analyzer.load_file()
        analyzer.detect_type()
        analyzer.report()

def repair_corrupted_file():
    """Repair the corrupted PNG file."""
    print("\n" + "=" * 70)
    print(" CRITICAL INCIDENT: File Repair")
    print("=" * 70)

    repairer = FileRepairer('data/corrupted.png')

    print("\n--- Diagnosis ---")
    repairer.diagnose('PNG')

    print("\n--- Repair ---")
    success = repairer.repair('PNG', 'data/repaired.png')

    if success:
        print("\n--- Verification ---")
        result = repairer.verify('data/repaired.png')
        print(f"Repaired file type: {result}")

def main():
    """Main entry point."""
    analyze_evidence()
    repair_corrupted_file()

    print("\n" + "=" * 70)
    print(" Analysis Complete")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Verify repaired.png opens correctly")
    print("  2. Run: file data/repaired.png")
    print("  3. Complete submission.md documentation")

if __name__ == "__main__":
    main()
```

**Run the complete analysis:**
```bash
python3 main.py
```

---

### Exercise 4.2: Document Your Work

Create a file called `submission.md` with the following sections:

```markdown
# Lab 02 Submission: The Hex Detective

**Student Name:** [Your Name]
**Student ID:** [Your ID]
**Date:** [Submission Date]

---

## Section A: CLI Reconnaissance (Phase 1)

### File Identification
[Paste your `file data/*` output]

### Hex Dump Observations
| File | Magic Bytes (Hex) | Identified As |
|------|-------------------|---------------|
| unknown_a.bin | | |
| unknown_b.bin | | |
| unknown_c.bin | | |
| corrupted.png | | |

### String Extraction
[List interesting strings found in hidden_message.bin]

---

## Section B: BinaryAnalyzer Results (Phase 2)

### Analysis Summary
| File | Size | Detected Type | Notes |
|------|------|---------------|-------|
| unknown_a.bin | | | |
| unknown_b.bin | | | |
| unknown_c.bin | | | |
| hidden_message.bin | | | |

### Code Quality
- All methods implemented: [Yes/No]
- Error handling included: [Yes/No]
- Tests pass: [Yes/No]

---

## Section C: File Repair Report (Phase 3)

### Diagnosis
The corrupted.png file had the following bytes damaged:
- Byte 1: [original] -> [expected]
- Byte 2: [original] -> [expected]
- Byte 3: [original] -> [expected]

### Repair Process
1. [Describe step 1]
2. [Describe step 2]
3. [Describe step 3]

### Verification
- `file data/corrupted.png` output: [paste]
- `file data/repaired.png` output: [paste]
- Image opens correctly: [Yes/No]

---

## Section D: AI Usage Appendix (if applicable)

**Did you use AI tools? [Yes/No]**

If yes, complete the following:

### Interaction 1
- **Tool Used:** [e.g., ChatGPT, GitHub Copilot]
- **Methodology:** [What problem were you solving?]
- **The Prompt:** [Copy your query]
- **The Output:** [Summarize AI's response]
- **Human Value-Add:** [What did you change, verify, or correct?]

---

## Section E: Reflection

1. What was the most challenging part of this lab?
2. How does understanding hex and magic bytes help in security?
3. What real-world applications can you think of for binary analysis?

---
```

---

## Verification Checklist

Before submitting, ensure:

- [ ] `binary_analyzer.py` contains both `BinaryAnalyzer` and `FileRepairer` classes
- [ ] `main.py` runs without errors
- [ ] All five evidence files are analyzed
- [ ] `corrupted.png` is successfully repaired
- [ ] `data/repaired.png` opens as a valid image
- [ ] `submission.md` is complete with all sections
- [ ] If AI was used, it is properly documented
- [ ] You can explain every byte manipulation you performed

---

## Bonus Challenge (+10 points)

Implement multi-format repair support:

```python
def auto_repair(self, output_path=None):
    """
    Attempt to identify and repair the file automatically.
    Tries each known signature and keeps the one that produces
    a valid file structure.
    """
    # Your implementation here
    pass
```

Or add a hex editor mode:

```python
def edit_byte(self, offset, new_value):
    """
    Manually edit a single byte at the given offset.

    Args:
        offset (int): Byte position to modify
        new_value (int): New byte value (0-255)
    """
    # Your implementation here
    pass
```

---

## Congratulations!

You've completed the Hex Detective investigation. You've learned how to:
- Examine binary files at the byte level
- Identify file types using magic signatures
- Use CLI tools for forensic analysis
- Build Python tools for binary manipulation
- Repair corrupted file headers

**Next Steps:** Review your code, ensure it's well-documented, and submit through the course portal.

---

**End of Notebook**
