# Lab 01: The Rosetta Frequency

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/devomh/comp3084-2026/blob/main/lab01/lab01.ipynb)

## Case Brief

### The Situation
Intelligence has intercepted a series of digital documents from an unknown source. Most appear to be standard literature, likely public domain texts used as cover. However, one file—designated **"Mystery Artifact"**—is of unknown origin and requires immediate analysis.

### Your Mission
You are a **Linguistic Forensics Officer** tasked with developing a specialized software tool capable of:
1. Extracting "linguistic fingerprints" from text documents through letter frequency analysis
2. Classifying unknown documents based on their frequency patterns
3. Distinguishing between natural language text and source code artifacts

### The Tool
You will engineer a reusable Python class system—not a one-off script—that can be deployed for future investigations. The system must be robust enough to handle:
- Multiple text encodings (UTF-8, Latin-1)
- Various file types (natural text, source code)
- Large documents (thousands of lines)

---

## Chain of Custody

### Evidence Files
The following digital assets are located in the `data/` directory:

1. **`english.txt`** - Control Sample A (English literature)
2. **`spanish.txt`** - Control Sample B (Spanish literature)
3. **`artifact.py`** - The Mystery Artifact (origin unknown)
4. **`corrupt.txt`** - Damaged evidence with encoding anomalies

### Prerequisites
- Python 3.8 or higher
- Basic understanding of classes and objects (review `concepts.md` if needed)
- A text editor or IDE (VS Code recommended)
- Terminal access (Linux/macOS/Git Bash on Windows)

### Technical Environment
```bash
# Verify Python version
python3 --version

# Navigate to lab directory
cd lab01

# List evidence files
ls -lh data/
```

---

## Investigation Phases

### Phase 1: Field Work (30 minutes)
**Objective:** Conduct initial reconnaissance on the evidence files using command-line tools.

Before writing any code, you must understand your data. Use the following terminal commands:

1. **File Inspection:**
   ```bash
   ls -lh data/          # Check file sizes
   file data/*           # Identify file types
   ```

2. **Content Preview:**
   ```bash
   head -n 10 data/english.txt    # First 10 lines
   tail -n 10 data/spanish.txt    # Last 10 lines
   wc -l data/artifact.py         # Count lines
   ```

3. **The Encoding Trap:**
   Try opening `data/corrupt.txt` with a Python script:
   ```python
   with open('data/corrupt.txt', 'r', encoding='utf-8') as f:
       content = f.read()
       print(content)
   ```
   **What happens? Why does it fail?** Document this in your lab notebook.

**Deliverable:** Written observations about:
- Approximate file sizes
- Language/content type of each file
- The encoding error encountered with `corrupt.txt`

---

### Phase 2: The Build - TextAnalyzer Class (90 minutes)
**Objective:** Construct the core forensic tool as a reusable Python class.

#### Class Specification: `TextAnalyzer`

**Attributes (State):**
- `self.filepath` - Path to the evidence file
- `self.content` - The raw text content
- `self.frequency_map` - Dictionary storing character frequencies

**Methods (Behavior):**

1. **`__init__(self, filepath)`**
   - Constructor that initializes the analyzer with a file path
   - Sets up empty content and frequency map

2. **`load_file(self)`**
   - Opens and reads the file safely
   - Handles potential `FileNotFoundError`
   - **Critical:** Must try UTF-8 first, fallback to Latin-1 if needed

3. **`clean_content(self)`**
   - Removes numbers, punctuation, and whitespace
   - Converts all text to lowercase
   - Keeps only alphabetic characters (a-z)

4. **`calculate_frequency(self)`**
   - Iterates through cleaned content
   - Populates `self.frequency_map` with character counts
   - Example: `{'a': 105, 'b': 23, 'c': 47, ...}`

5. **`report(self)`**
   - Prints analysis results:
     - Filename
     - Total character count
     - Top 5 most frequent letters with counts
     - Frequency percentage for top letter

**Implementation Strategy:**
```python
class TextAnalyzer:
    def __init__(self, filepath):
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
analyzer = TextAnalyzer('data/english.txt')

# Run the analysis pipeline
analyzer.load_file()
analyzer.clean_content()
analyzer.calculate_frequency()
analyzer.report()
```

**Deliverable:** A working `analyzer.py` file containing the `TextAnalyzer` class.

---

### Phase 3: Critical Incident - CodeAnalyzer Subclass (45 minutes)
**Objective:** Handle the specialized case where the artifact is source code, not natural text.

#### The Problem
Running `TextAnalyzer` on `artifact.py` produces misleading results. The frequency is skewed by:
- Programming keywords (`def`, `return`, `class`, `self`, `import`)
- Syntax characters (`(`, `)`, `:`, `_`)

These mask the true linguistic pattern of the variable names and comments.

#### The Solution: Inheritance
Create a **`CodeAnalyzer`** class that inherits from `TextAnalyzer` but overrides the `clean_content()` method to:
1. Remove single-line comments (`#` to end of line)
2. Strip common Python keywords
3. Remove syntax-specific characters

**Class Specification: `CodeAnalyzer`**
```python
class CodeAnalyzer(TextAnalyzer):
    def clean_content(self):
        # Your specialized cleaning logic
        # Should remove Python-specific noise
        pass
```

**The Revelation:**
After cleaning, analyze `artifact.py` with `CodeAnalyzer`. Compare the top letters with your control samples. What do you discover about the artifact's origin?

**Deliverable:**
- Updated `analyzer.py` with `CodeAnalyzer` class
- Short written analysis: "The artifact was authored by someone who speaks _______ because _______"

---

## Submission Requirements

Your final submission must include:

### 1. Code Files
```
lab01/
├── analyzer.py        # Both TextAnalyzer and CodeAnalyzer classes
└── main.py           # Script that runs analysis on all data files
```

**`main.py` Requirements:**
- Instantiate analyzers for all four evidence files
- Use appropriate analyzer type (`TextAnalyzer` or `CodeAnalyzer`)
- Print clearly labeled results for each file

### 2. Documentation
Create a `submission.md` file containing:

**Section A: Observations (Phase 1)**
- Command outputs and file inspection notes
- Explanation of the encoding error

**Section B: Analysis Results (Phase 2)**
- Top 5 letter frequencies for each control sample
- Comparison: English vs Spanish frequency patterns

**Section C: Critical Incident Report (Phase 3)**
- Frequency analysis of the artifact before and after using `CodeAnalyzer`
- Conclusion about the artifact's linguistic origin
- Explanation of why inheritance was necessary

**Section D: AI Usage Appendix (if applicable)**
If you used AI tools, document:
1. **Tool Used:** (e.g., "GitHub Copilot", "ChatGPT")
2. **Methodology:** What specific problem did you ask AI to help with?
3. **The Prompt:** Copy the most representative query
4. **The Output:** What did the AI suggest?
5. **Human Value-Add:** How did you verify, modify, or correct the AI's suggestion?

**Note:** AI should NOT write the core class logic. Acceptable uses:
- Explaining encoding concepts
- Debugging `UnicodeDecodeError` messages
- Suggesting regex patterns for text cleaning

---

## Evaluation Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **Phase 1** | 10 | Correct file inspection, encoding error documented |
| **Phase 2** | 50 | `TextAnalyzer` class fully functional, handles encodings |
| **Phase 3** | 30 | `CodeAnalyzer` correctly identifies artifact language |
| **Documentation** | 10 | Clear observations, proper AI attribution if used |
| **Total** | 100 | |

**Bonus (+10):** Implement a method to automatically detect the language (English/Spanish) by comparing frequency distributions to reference patterns.

---

## Tips for Success

1. **Test Incrementally:** Don't write all methods at once. Test each method individually.

2. **Debug with Small Files:** If your analyzer fails, create a tiny test file (3-4 lines) to debug.

3. **Print Debug Info:** Add temporary print statements inside methods to verify logic.
   ```python
   def clean_content(self):
       print(f"Before cleaning: {len(self.content)} chars")
       # cleaning logic
       print(f"After cleaning: {len(self.content)} chars")
   ```

4. **Read Error Messages:** If you get `UnicodeDecodeError`, the error message tells you which byte failed. Look up that byte value.

5. **Verify Inheritance:** After creating `CodeAnalyzer`, verify you can still call `load_file()` and `report()` without rewriting them.

---

## Academic Integrity Reminder

You are the **Senior Engineer** responsible for this code. Submitting code you cannot explain violates the course's integrity policy. If you use AI assistance, you must:
- Be able to explain every line of code
- Document AI usage in the appendix
- Demonstrate that you verified and understood the AI's suggestions

**The Verifier Principle:** In the age of generative AI, the most valuable skill is the ability to **audit and validate** code, not just generate it.

---

## Resources

- **Concepts Reference:** See [`concepts.md`](concepts.md) for detailed explanations
- **Lab Notebook:** Use [`lab01.md`](lab01.md) for guided exercises
- **Python Documentation:** [File I/O](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- **Encoding Guide:** [Unicode HOWTO](https://docs.python.org/3/howto/unicode.html)

---

## Questions?

If you encounter issues:
1. Re-read the relevant section in `concepts.md`
2. Test your code with simpler inputs
3. Ask a classmate (collaboration on concepts is encouraged)
4. Consult the instructor during lab hours

**Remember:** The goal is not just to complete the assignment, but to understand how to build reusable, maintainable software systems.

Good luck, Officer.
