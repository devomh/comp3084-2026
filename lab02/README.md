# Lab 02: The Hex Detective

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/devomh/comp3084-2026/blob/main/lab02/lab02.ipynb)

## Case Brief

### The Situation
A routine security audit has uncovered a cache of suspicious files on a seized storage device. The files have no extensions, corrupted headers, or have been intentionally obfuscated. Standard forensic tools report them as "data" or fail to process them entirely.

### Your Mission
You are a **Reverse Engineering Specialist** tasked with developing expertise in binary forensics. You will learn to:
1. Examine files at the byte level using hex analysis tools
2. Identify file types by their "magic signatures" rather than extensions
3. Repair corrupted binary files by patching damaged headers
4. Build reusable Python tools for automated binary analysis

### The Stakes
One file in particular—designated **"corrupted.png"**—is believed to contain critical evidence, but image viewers refuse to open it. Your task is to diagnose the corruption and restore the file.

---

## Chain of Custody

### Evidence Files
The following digital assets are located in the `data/` directory:

1. **`unknown_a.bin`** - Unidentified binary file #1
2. **`unknown_b.bin`** - Unidentified binary file #2
3. **`unknown_c.bin`** - Unidentified binary file #3
4. **`corrupted.png`** - Damaged image file (will not open)
5. **`hidden_message.bin`** - Binary file with suspected embedded data

### Reference Materials
- **`data/reference/original.png`** - An uncorrupted reference image for comparison

### Prerequisites
- Completion of Lab 01 (OOP and File I/O fundamentals)
- Python 3.8 or higher
- Terminal access with `xxd` or `hexdump` available
- Basic understanding of hexadecimal (review `concepts.md` if needed)

### Technical Environment
```bash
# Verify tools are available
which xxd || which hexdump
which strings
which file

# Navigate to lab directory
cd lab02

# List evidence files
ls -lh data/
```

---

## Investigation Phases

### Phase 1: Field Work - CLI Binary Forensics (45 minutes)
**Objective:** Master command-line tools for binary file inspection.

Before writing code, use terminal tools to gather intelligence on the evidence files.

#### Exercise 1.1: Initial Reconnaissance
```bash
# Identify file types (may fail on some files)
file data/*

# Check file sizes
ls -lh data/
```

**Record:** Which files does `file` successfully identify? Which ones return "data"?

#### Exercise 1.2: Hex Examination
```bash
# View first 64 bytes of each unknown file
xxd -l 64 data/unknown_a.bin
xxd -l 64 data/unknown_b.bin
xxd -l 64 data/unknown_c.bin
```

**Questions:**
1. What magic bytes do you see at the start of `unknown_a.bin`?
2. What magic bytes do you see at the start of `unknown_b.bin`?
3. Does `unknown_c.bin` have recognizable magic bytes?

#### Exercise 1.3: String Extraction
```bash
# Extract printable strings
strings data/unknown_c.bin
strings data/hidden_message.bin
```

**Questions:**
1. What content is hidden in `unknown_c.bin`?
2. Can you find the secret messages in `hidden_message.bin`?

#### Exercise 1.4: The Corrupted File
```bash
# Compare corrupted vs reference
xxd -l 16 data/corrupted.png
xxd -l 16 data/reference/original.png
```

**Critical Finding:** What bytes are different between the corrupted and original files?

**Deliverable:** Written observations documenting your findings for each file.

---

### Phase 2: The Build - BinaryAnalyzer Class (75 minutes)
**Objective:** Construct a Python class for automated binary file analysis.

#### Class Specification: `BinaryAnalyzer`

**Attributes (State):**
- `self.filepath` - Path to the evidence file
- `self.data` - Raw bytes read from the file
- `self.file_type` - Detected file type string
- `self.magic_db` - Dictionary of known magic signatures

**Methods (Behavior):**

1. **`__init__(self, filepath)`**
   - Constructor that initializes the analyzer with a file path
   - Loads the magic signature database

2. **`load_file(self)`**
   - Opens and reads file in binary mode (`'rb'`)
   - Handles `FileNotFoundError`
   - Stores raw bytes in `self.data`

3. **`get_header(self, num_bytes=16)`**
   - Returns the first N bytes as a formatted hex string
   - Useful for quick inspection

4. **`detect_type(self)`**
   - Compares file header against known magic signatures
   - Sets `self.file_type` and returns the detected type
   - Returns "Unknown" if no match found

5. **`extract_strings(self, min_length=4)`**
   - Finds and returns printable ASCII sequences
   - Mimics the `strings` command functionality

6. **`hexdump(self, start=0, length=256)`**
   - Generates a formatted hex dump view
   - Includes offset, hex bytes, and ASCII representation

7. **`report(self)`**
   - Prints comprehensive analysis summary:
     - Filename and size
     - Detected file type
     - First 16 bytes (hex)
     - Sample extracted strings

**Implementation Template:**
```python
class BinaryAnalyzer:
    def __init__(self, filepath):
        # Initialize magic signature database
        self.magic_db = {
            b'\x89PNG\r\n\x1a\n': 'PNG',
            b'\xff\xd8\xff': 'JPEG',
            # Add more signatures...
        }
        # Your code here
        pass

    def load_file(self):
        # Your code here
        pass

    # ... other methods
```

**Testing Your Class:**
```python
# Create an instance
analyzer = BinaryAnalyzer('data/unknown_a.bin')

# Run the analysis pipeline
analyzer.load_file()
detected = analyzer.detect_type()
print(f"Detected type: {detected}")
analyzer.report()
```

**Deliverable:** A working `binary_analyzer.py` file containing the `BinaryAnalyzer` class.

---

### Phase 3: Critical Incident - File Repair (45 minutes)
**Objective:** Repair a PNG file with a corrupted header.

#### The Problem
The file `data/corrupted.png` has been tampered with. The PNG magic signature has been partially overwritten, causing image viewers and the `file` command to fail.

**Expected PNG signature:**
```
89 50 4E 47 0D 0A 1A 0A
```

#### The Task
Create a `FileRepairer` class (or extend `BinaryAnalyzer`) that:

1. **Diagnoses** the corruption by comparing to expected signatures
2. **Patches** the incorrect bytes with correct values
3. **Writes** the repaired file to a new location
4. **Verifies** the repair was successful

**Class Specification: `FileRepairer`**
```python
class FileRepairer:
    def __init__(self, filepath):
        # Your code here
        pass

    def diagnose(self, expected_signature):
        """Compare file header to expected signature, report differences."""
        pass

    def repair(self, expected_signature, output_path):
        """Patch the header and write to output_path."""
        pass

    def verify(self, output_path):
        """Confirm the repair worked (check with magic bytes)."""
        pass
```

**Testing Your Repair:**
```python
# Attempt repair
repairer = FileRepairer('data/corrupted.png')
repairer.diagnose(PNG_SIGNATURE)
repairer.repair(PNG_SIGNATURE, 'data/repaired.png')
repairer.verify('data/repaired.png')
```

```bash
# Verify with file command
file data/corrupted.png    # Should say "data"
file data/repaired.png     # Should say "PNG image data..."
```

**Deliverable:**
- Updated `binary_analyzer.py` with `FileRepairer` class
- Successfully repaired `data/repaired.png` that opens in image viewers

---

## Submission Requirements

### 1. Code Files
```
lab02/
├── binary_analyzer.py    # BinaryAnalyzer and FileRepairer classes
└── main.py              # Script that analyzes all evidence files
```

**`main.py` Requirements:**
- Analyze all five evidence files in `data/`
- Use `BinaryAnalyzer` to detect file types
- Use `FileRepairer` to fix `corrupted.png`
- Print clearly labeled results

### 2. Documentation
Create a `submission.md` file containing:

**Section A: CLI Reconnaissance (Phase 1)**
- Command outputs showing file identification
- Magic bytes observed for each file
- Strings extracted from binary files

**Section B: BinaryAnalyzer Results (Phase 2)**
- Analysis output for each evidence file
- File types detected vs actual types

**Section C: File Repair Report (Phase 3)**
- Diagnosis of corrupted.png (which bytes were wrong)
- Steps taken to repair
- Verification that repair succeeded

**Section D: AI Usage Appendix (if applicable)**
Follow the standard AI documentation format from Lab 01.

---

## Evaluation Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **Phase 1** | 15 | Correct CLI usage, magic bytes identified |
| **Phase 2** | 45 | `BinaryAnalyzer` class fully functional |
| **Phase 3** | 30 | `FileRepairer` successfully repairs PNG |
| **Documentation** | 10 | Clear observations, proper attribution |
| **Total** | 100 | |

**Bonus (+10):** Implement support for repairing multiple file types (JPEG, GIF, PDF).

---

## Tips for Success

1. **Start with CLI:** Before writing Python, understand what the command-line tools show you.

2. **Use the Reference File:** Compare `corrupted.png` to `reference/original.png` to see exactly what changed.

3. **Test Incrementally:** Build and test each method before moving to the next.

4. **Print Debug Info:**
   ```python
   def detect_type(self):
       header = self.data[:16]
       print(f"Header bytes: {header.hex(' ')}")
       # ... rest of method
   ```

5. **Binary Mode is Crucial:** Always use `'rb'` when opening binary files.

6. **Verify Your Repairs:** After patching, always check with the `file` command.

---

## Academic Integrity Reminder

Binary analysis requires hands-on learning. You must:
- Understand every byte manipulation you perform
- Be able to explain the hex values and their meanings
- Document any AI assistance used

**Remember:** In forensics, every byte tells a story. Your job is to understand that story.

---

## Resources

- **Concepts Reference:** See [`concepts.md`](concepts.md) for detailed explanations
- **Lab Notebook:** Use [`lab02.md`](lab02.md) for guided exercises
- **Magic Bytes Database:** [File Signatures (Wikipedia)](https://en.wikipedia.org/wiki/List_of_file_signatures)
- **Python Bytes:** [Python Bytes Documentation](https://docs.python.org/3/library/stdtypes.html#bytes)

---

## Questions?

If you encounter issues:
1. Re-read the relevant section in `concepts.md`
2. Use `xxd` to verify what bytes you're reading
3. Compare against the reference files in `data/reference/`

**Remember:** The goal is to think like a forensic analyst—question everything, verify everything.
