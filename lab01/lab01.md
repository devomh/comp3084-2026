# Lab 01 Notebook: The Rosetta Frequency
**Linguistic Forensics Investigation**

---

## Introduction

This notebook guides you through building a text analysis system step-by-step. Each section includes exercises, code templates, and verification steps.

**Before you begin:**
- [ ] Read [`README.md`](README.md) for the full case briefing
- [ ] Review [`concepts.md`](concepts.md) for technical background
- [ ] Ensure all files in `data/` are present

---

## Phase 1: Field Work - Investigation

### Exercise 1.1: File Reconnaissance

Use terminal commands to gather intelligence on the evidence files.

**Task A: File Statistics**
```bash
# Run these commands and record the output
ls -lh data/
file data/*
```

**Record your observations:**
- Which file is the largest?
- What file types were detected?
- Are all files identified as "text"?

---

### Exercise 1.2: Content Preview

**Task B: Examine the first lines of each file**
```bash
head -n 5 data/english.txt
head -n 5 data/spanish.txt
head -n 5 data/artifact.py
```

**Questions:**
1. What language appears to be in `english.txt`?
2. What special characters do you notice in `spanish.txt`? (á, é, ñ?)
3. What type of content is in `artifact.py`?

---

### Exercise 1.3: The Encoding Trap

**Task C: Attempt to read the corrupt file**

Create a file called `test_encoding.py` and add this code:

```python
# test_encoding.py

# Attempt 1: Default encoding (UTF-8)
print("Attempting to read corrupt.txt with UTF-8...")
try:
    with open('data/corrupt.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
except UnicodeDecodeError as e:
    print(f"ERROR: {e}")

# Attempt 2: Latin-1 encoding
print("\nAttempting to read corrupt.txt with Latin-1...")
try:
    with open('data/corrupt.txt', 'r', encoding='latin-1') as f:
        content = f.read()
        print(content)
        print("SUCCESS: File read with Latin-1 encoding")
except UnicodeDecodeError as e:
    print(f"ERROR: {e}")
```

**Run it:**
```bash
python3 test_encoding.py
```

**Questions:**
1. What error message did you get with UTF-8?
2. Why did Latin-1 succeed?
3. What does this teach you about file encoding?

**Write your answers here:**

---

---

## Phase 2: The Build - TextAnalyzer Class

### Exercise 2.1: Class Constructor

Create a file called `analyzer.py` and start building the class.

> **Tip for Jupyter/Colab Users:** You can use the `%%writefile analyzer.py` magic command at the very top of the code cell to automatically save your code to a file.

```python
# analyzer.py

class TextAnalyzer:
    """
    A forensic tool for analyzing text files and extracting
    linguistic fingerprints through letter frequency analysis.
    """

    def __init__(self, filepath):
        """
        Initialize the analyzer with a file path.

        Args:
            filepath (str): Path to the text file to analyze
        """
        # TODO: Store the filepath
        # TODO: Initialize self.content as empty string
        # TODO: Initialize self.frequency_map as empty dictionary
        pass
```

**Your task:** Replace `pass` with actual implementation.

**Test your constructor:**
```python
# At the bottom of analyzer.py (temporary test)
if __name__ == "__main__":
    analyzer = TextAnalyzer('data/english.txt')
    print(f"Filepath: {analyzer.filepath}")
    print(f"Content: '{analyzer.content}'")
    print(f"Frequency map: {analyzer.frequency_map}")
```

**Expected output:**
```
Filepath: data/english.txt
Content: ''
Frequency map: {}
```

---

### Exercise 2.2: File Loading Method

Add the `load_file()` method to handle file reading with encoding safety.

```python
def load_file(self):
    """
    Load the file content with encoding detection.
    Tries UTF-8 first, falls back to Latin-1 if needed.
    """
    try:
        # TODO: Open file with UTF-8 encoding
        # TODO: Read content into self.content
        pass

    except FileNotFoundError:
        # TODO: Print error message
        # TODO: Set self.content to empty string
        pass

    except UnicodeDecodeError:
        # TODO: Try again with Latin-1 encoding
        # TODO: Read content into self.content
        pass
```

**Hint:** Use `with open(...) as f:` statements.

**Test your method:**
```python
if __name__ == "__main__":
    # Test with English file
    analyzer = TextAnalyzer('data/english.txt')
    analyzer.load_file()
    print(f"Loaded {len(analyzer.content)} characters")
    print(f"First 100 characters: {analyzer.content[:100]}")

    # Test with corrupt file
    analyzer2 = TextAnalyzer('data/corrupt.txt')
    analyzer2.load_file()
    print(f"\nCorrupt file loaded: {len(analyzer2.content)} characters")
```

---

### Exercise 2.3: Text Cleaning Method

Add the `clean_content()` method to prepare text for analysis.

```python
def clean_content(self):
    """
    Clean the content by:
    - Converting to lowercase
    - Removing all non-alphabetic characters (keep only a-z)
    """
    # TODO: Convert self.content to lowercase
    # TODO: Filter to keep only alphabetic characters
    # Hint: Use a list comprehension or filter with str.isalpha()
    pass
```

**Example approach:**
```python
# Option 1: List comprehension
cleaned = ''.join([char for char in self.content if char.isalpha()])

# Option 2: Filter function
cleaned = ''.join(filter(str.isalpha, self.content))
```

**Test your method:**
```python
if __name__ == "__main__":
    analyzer = TextAnalyzer('data/english.txt')
    analyzer.load_file()

    print(f"Before cleaning: {len(analyzer.content)} characters")
    print(f"Sample: {analyzer.content[:100]}")

    analyzer.clean_content()

    print(f"\nAfter cleaning: {len(analyzer.content)} characters")
    print(f"Sample: {analyzer.content[:100]}")
```

**Expected behavior:** Numbers, punctuation, spaces removed. All lowercase.

---

### Exercise 2.4: Frequency Calculation Method

Add the `calculate_frequency()` method to count letter occurrences.

```python
def calculate_frequency(self):
    """
    Count the frequency of each letter in the cleaned content.
    Populates self.frequency_map.
    """
    # TODO: Initialize frequency_map if needed
    # TODO: Loop through each character in self.content
    # TODO: Increment the count for each character
    # Hint: Use frequency_map.get(char, 0) + 1
    pass
```

**Test your method:**
```python
if __name__ == "__main__":
    analyzer = TextAnalyzer('data/english.txt')
    analyzer.load_file()
    analyzer.clean_content()
    analyzer.calculate_frequency()

    # Show first 10 entries
    items = list(analyzer.frequency_map.items())[:10]
    for letter, count in items:
        print(f"{letter}: {count}")
```

---

### Exercise 2.5: Reporting Method

Add the `report()` method to display analysis results.

```python
def report(self):
    """
    Print a formatted report of the analysis results.
    Shows:
    - Filename
    - Total character count
    - Top 5 most frequent letters
    """
    # TODO: Calculate total characters
    # TODO: Sort frequency_map by count (descending)
    # TODO: Get top 5
    # TODO: Print formatted output

    print("=" * 50)
    print(f"Analysis Report: {self.filepath}")
    print("=" * 50)

    # Your code here

    pass
```

**Hint for sorting:**
```python
sorted_items = sorted(
    self.frequency_map.items(),
    key=lambda x: x[1],
    reverse=True
)
top_5 = sorted_items[:5]
```

**Test your complete class:**
```python
if __name__ == "__main__":
    # Analyze English text
    analyzer = TextAnalyzer('data/english.txt')
    analyzer.load_file()
    analyzer.clean_content()
    analyzer.calculate_frequency()
    analyzer.report()
```

**Expected output format:**
```
==================================================
Analysis Report: data/english.txt
==================================================
Total characters: 15432
Top 5 letters:
  e: 1847 (11.97%)
  t: 1234 (8.00%)
  a: 1123 (7.28%)
  ...
```

---

### Exercise 2.6: Verify with Control Samples

Run your analyzer on both control samples:

```python
if __name__ == "__main__":
    print("CONTROL SAMPLE A: English")
    eng = TextAnalyzer('data/english.txt')
    eng.load_file()
    eng.clean_content()
    eng.calculate_frequency()
    eng.report()

    print("\n\nCONTROL SAMPLE B: Spanish")
    spa = TextAnalyzer('data/spanish.txt')
    spa.load_file()
    spa.clean_content()
    spa.calculate_frequency()
    spa.report()
```

**Record your findings:**
- What are the top 3 letters in English?
- What are the top 3 letters in Spanish?
- How are they different?

---

---

## Phase 3: Critical Incident - CodeAnalyzer

### Exercise 3.1: Analyze the Artifact (Before Cleaning)

First, run the standard `TextAnalyzer` on the artifact:

```python
if __name__ == "__main__":
    print("MYSTERY ARTIFACT (Standard Analysis):")
    artifact = TextAnalyzer('data/artifact.py')
    artifact.load_file()
    artifact.clean_content()
    artifact.calculate_frequency()
    artifact.report()
```

**Questions:**
1. What are the top 5 letters?
2. Do they match English or Spanish patterns?
3. Why might the results be misleading?

---

### Exercise 3.2: Build the CodeAnalyzer Subclass

Add this new class to `analyzer.py` (AFTER the TextAnalyzer class):

```python
import re  # Add at top of file

class CodeAnalyzer(TextAnalyzer):
    """
    Specialized analyzer for source code files.
    Inherits from TextAnalyzer but overrides cleaning logic
    to remove programming-specific noise.
    """

    def clean_content(self):
        """
        Clean source code by removing:
        - Comments (# to end of line)
        - Common Python keywords
        - Syntax characters
        Then apply standard text cleaning.
        """
        # TODO: Remove comments using regex
        # Pattern: r'#.*' removes from # to end of line

        # TODO: Remove Python keywords
        # Pattern: r'\b(def|class|return|import|if|else|for|while|self)\b'

        # TODO: Remove common syntax characters
        # You can remove: _ ( ) : " '

        # TODO: Apply the standard cleaning (lowercase, alpha only)
        # Hint: You can call the parent method or reuse the logic

        pass
```

**Implementation hints:**
```python
# Remove comments
self.content = re.sub(r'#.*', '', self.content)

# Remove keywords
keywords = r'\b(def|class|return|import|if|else|for|while|self|try|except|print|with|as|in|from)\b'
self.content = re.sub(keywords, '', self.content)

# Remove syntax characters
for char in ['_', '(', ')', ':', '"', "'", '{', '}', '[', ']']:
    self.content = self.content.replace(char, ' ')

# Apply standard cleaning (lowercase, alpha only)
self.content = self.content.lower()
self.content = ''.join(char for char in self.content if char.isalpha())
```

---

### Exercise 3.3: Analyze the Artifact (After Specialized Cleaning)

Test your new analyzer:

```python
if __name__ == "__main__":
    print("MYSTERY ARTIFACT (Code Analysis):")
    artifact = CodeAnalyzer('data/artifact.py')
    artifact.load_file()
    artifact.clean_content()
    artifact.calculate_frequency()
    artifact.report()
```

**Compare results:**
- What are the top 5 letters now?
- Do they match English or Spanish patterns better?
- What changed compared to standard analysis?

---

### Exercise 3.4: The Revelation

**Final Investigation Questions:**

1. **Language Identification:** Based on letter frequency, what language is the artifact written in?

2. **Evidence:** What specific frequency patterns support your conclusion?

3. **Inheritance Justification:** Why was inheritance useful here? Could you have achieved the same result without creating a subclass?

**Write your forensic report:**

```
FORENSIC REPORT: ARTIFACT.PY

Analysis Date: [Today's Date]
Analyst: [Your Name]

FINDINGS:
The mystery artifact exhibits the following linguistic characteristics:
- Top 5 letters: [list them]
- Frequency pattern matches: [English/Spanish]

CONCLUSION:
The artifact was authored by an individual who speaks [LANGUAGE] because
[explain your reasoning based on frequency analysis].

TECHNICAL NOTE:
The use of inheritance was essential because [explain why CodeAnalyzer
needed to override clean_content() while reusing other methods].
```

---

---

## Phase 4: Integration and Submission

### Exercise 4.1: Create main.py

Create a file called `main.py` that runs all analyses.

> **Tip for Jupyter/Colab Users:** You can use the `%%writefile main.py` magic command at the top of the cell to generate the file.

```python
# main.py
"""
Main execution script for Lab 01: The Rosetta Frequency
Runs analysis on all evidence files.
"""

from analyzer import TextAnalyzer, CodeAnalyzer

def main():
    print("=" * 70)
    print(" COMP3084 - Lab 01: Linguistic Forensics Analysis")
    print("=" * 70)
    print()

    # Analyze English control
    print("CONTROL SAMPLE A: English Literature")
    print("-" * 70)
    eng = TextAnalyzer('data/english.txt')
    eng.load_file()
    eng.clean_content()
    eng.calculate_frequency()
    eng.report()
    print()

    # Analyze Spanish control
    print("CONTROL SAMPLE B: Spanish Literature")
    print("-" * 70)
    spa = TextAnalyzer('data/spanish.txt')
    spa.load_file()
    spa.clean_content()
    spa.calculate_frequency()
    spa.report()
    print()

    # Analyze artifact with standard analyzer
    print("MYSTERY ARTIFACT: Standard Text Analysis")
    print("-" * 70)
    artifact_text = TextAnalyzer('data/artifact.py')
    artifact_text.load_file()
    artifact_text.clean_content()
    artifact_text.calculate_frequency()
    artifact_text.report()
    print()

    # Analyze artifact with code analyzer
    print("MYSTERY ARTIFACT: Specialized Code Analysis")
    print("-" * 70)
    artifact_code = CodeAnalyzer('data/artifact.py')
    artifact_code.load_file()
    artifact_code.clean_content()
    artifact_code.calculate_frequency()
    artifact_code.report()
    print()

    print("=" * 70)
    print(" Analysis Complete")
    print("=" * 70)

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
# Lab 01 Submission: The Rosetta Frequency

**Student Name:** [Your Name]
**Student ID:** [Your ID]
**Date:** [Submission Date]

---

## Section A: Phase 1 Observations

### File Inspection
[Paste your ls -lh and file command outputs]

### Encoding Investigation
[Describe the error you encountered with corrupt.txt and explain why it occurred]

---

## Section B: Phase 2 Analysis Results

### English Control Sample
- Top 5 letters: [list with percentages]
- Total characters analyzed: [number]

### Spanish Control Sample
- Top 5 letters: [list with percentages]
- Total characters analyzed: [number]

### Comparison
[Describe the key differences between English and Spanish frequency patterns]

---

## Section C: Phase 3 Critical Incident

### Standard Analysis of Artifact
- Top 5 letters: [list]

### Code Analysis of Artifact
- Top 5 letters: [list]

### Conclusion
[State which language the artifact is written in and provide evidence]

### Inheritance Justification
[Explain why creating a CodeAnalyzer subclass was the right design choice]

---

## Section D: AI Usage Appendix (if applicable)

**Did you use AI tools? [Yes/No]**

If yes, complete the following for each significant AI interaction:

### Interaction 1
- **Tool Used:** [e.g., ChatGPT, GitHub Copilot]
- **Methodology:** [What problem were you solving?]
- **The Prompt:** [Copy your query]
- **The Output:** [Summarize AI's response]
- **Human Value-Add:** [What did you change, verify, or correct?]

[Repeat for additional interactions]

---

## Section E: Reflection

1. What was the most challenging part of this lab?
2. What did you learn about object-oriented programming?
3. How does letter frequency analysis relate to real-world applications?

---
```

---

## Verification Checklist

Before submitting, ensure:

- [ ] `analyzer.py` contains both `TextAnalyzer` and `CodeAnalyzer` classes
- [ ] `main.py` runs without errors
- [ ] All four evidence files are analyzed
- [ ] `submission.md` is complete with all sections
- [ ] If AI was used, it is properly documented
- [ ] You can explain every line of code you wrote

---

## Bonus Challenge (+10 points)

Implement an automatic language detector:

```python
def detect_language(self):
    """
    Automatically detect if the text is English or Spanish
    by comparing frequency patterns to reference distributions.

    Returns:
        str: 'English', 'Spanish', or 'Unknown'
    """
    # Reference: In English, 'e' is most common
    # Reference: In Spanish, 'e' and 'a' are nearly equal, with 'a' often higher

    # Your implementation here
    pass
```

Add this method to `TextAnalyzer` and test it on your control samples.

---

## Congratulations!

You've completed the Rosetta Frequency investigation. You've learned how to:
- Build reusable classes with encapsulation
- Handle file I/O with encoding safety
- Use inheritance to specialize behavior
- Apply data structures (dictionaries) for analysis
- Think like a forensic data scientist

**Next Steps:** Review your code, ensure it's well-documented, and submit through the course portal.

---

**End of Notebook**
