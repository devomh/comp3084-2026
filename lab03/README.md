# Lab 03: The Time Capsule

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/devomh/comp3084-2026/blob/main/lab03/lab03.ipynb)

## Case Brief

### The Situation
You've been contracted by a small indie game studio to architect their save system. Their RPG has entered beta testing, and disaster has struck: players are losing hundreds of hours of progress due to save corruption, crashes during writes, and incompatible save formats across platforms.

The studio needs a **robust persistence layer** that can:
- Save character state reliably across sessions
- Support multiple serialization formats for different scenarios
- Verify data integrity to detect corruption immediately

### Your Mission
You are a **Data Persistence Architect** tasked with designing and implementing a production-grade save system. You will:

1. Build a `Character` class representing complex game state
2. Implement save/load functionality using **four serialization formats** (Custom Text, JSON, Binary, and Pickle)
3. Compare trade-offs: file size, readability, portability, security
4. Implement **checksum validation** to detect file corruption

### The Stakes
A player named "ElvenArcher92" has reported a corrupted save file after a power outage. They have 127 hours invested in their character "Legolas" and are threatening to abandon the game if the data can't be recovered. You must first implement a way to detect such corruption automatically using checksums.

---

## Chain of Custody

### Technical Requirements
- Completion of Lab 01 (OOP fundamentals) and Lab 02 (Binary I/O)
- Python 3.8 or higher
- Understanding of file I/O (`'rb'`, `'wb'`, text mode)
- Basic knowledge of data structures (lists, dictionaries, tuples)

### Evidence Files (Provided)
Located in the `data/` directory:

1. **`corrupted.json`** - Truncated save file (power failure during write)
2. **`corrupted_syntax.json`** - Save with JSON syntax errors
3. **`valid_reference.json`** - Known-good JSON save file for comparison
4. **`valid_reference.txt`** - Known-good custom text save file for comparison

### Technical Environment
```bash
# Navigate to lab directory
cd lab03

# Create data directory for saves
mkdir -p data

# Verify Python version
python3 --version  # Should be 3.8+
```

---

## Investigation Phases

### Phase 1: Field Work - Understanding Serialization (20 minutes)

**Objective:** Understand why persistence is necessary and inspect different data layouts.

#### Exercise 1.1: The Volatile Memory Problem (5 mins)
Run this demonstration to understand why persistence is necessary:

```python
# Create a character in memory
class Character:
    def __init__(self, name):
        self.name = name
        self.level = 1

hero = Character("Aragorn")
hero.level = 50
print(f"{hero.name} is level {hero.level}")

# Close program... all data is LOST
```

**Question:** How can we preserve `hero` across program executions?

#### Exercise 1.2: Format Research (10 mins)
Review these four serialization methods:

1. **Custom Text** - Simple key=value pairs (easiest to implement, good starting point)
2. **JSON** - Universal text format (cross-language, web-friendly, industry standard)
3. **Binary (`struct`)** - Fixed-size binary format for maximum efficiency and forensic control
4. **Pickle** - Python's native object serialization (convenient but carries security risks)

#### Exercise 1.3: CLI File Inspection (5 mins)
Examine the provided sample save files:

```bash
# View JSON saves
cat data/valid_reference.json

# View as hex (notice the structure and padding)
xxd data/valid_reference.json | head -n 10

# Extract strings from binary files (once generated)
strings data/hero.bin
```

---

### Phase 2: The Build - Character Save System (85 minutes)

**Objective:** Implement a complete `Character` class with multiple save/load methods.

#### Part A: Character Class Design (15 minutes)

Build a class representing an RPG character. A **boilerplate class** with `to_dict()` and `from_dict()` helper methods is provided in the lab notebook to speed up this process.

**Required Attributes:** `name`, `level`, `health`, `max_health`, `mana`, `max_mana`, `position` (tuple), `inventory` (list), `gold`, `experience`.

---

#### Part B: Serialization Method 1 - Custom Text Format (10 minutes)

**Objective:** Implement the simplest possible persistence format using key=value pairs.

This format is easy to read, easy to debug, and provides a gentle introduction before moving to structured formats. Near-complete boilerplate is provided in the lab notebook.

**Format:**
```
[CHARACTER]
name=Aragorn
level=50
health=5000
max_health=5000
mana=2500
max_mana=2500
position=42,17
gold=10000
experience=99999
[INVENTORY]
Sword
Shield
Potion
```

---

#### Part C: Serialization Method 2 - JSON (20 minutes)

**Objective:** Use JSON for universal, web-friendly serialization.

**Notes:**
- JSON doesn't support tuples natively. You must convert `position` to a list when saving and back to a tuple when loading.
- Wrap the character data inside a `"character"` key to match the structure in `data/valid_reference.json`.

```python
import json

def save_json(self, filepath):
    """Save character to JSON format."""
    # TODO: Wrap character dict inside {"character": ...}, use json.dump()
    pass

@classmethod
def load_json(cls, filepath):
    """Load character from JSON format."""
    # TODO: Use json.load(), extract data['character'], reconstruct object
    pass
```

---

#### Part D: Serialization Method 3 - Binary Format (35 minutes)

**Objective:** Use Python's `struct` module for compact binary saves. This is a core forensic skill.

**Binary Layout:**
- Bytes 0-31: Name (32-byte string, null-padded)
- Bytes 32-71: 10 Integers (level, health, max_h, mana, max_m, x, y, gold, exp, inv_count)

```python
import struct

def save_binary(self, filepath):
    """Save character to binary format using struct."""
    # TODO: Pack fixed-size header and write inventory
    pass

@classmethod
def load_binary(cls, filepath):
    """Load character from binary format."""
    # TODO: Unpack header and read variable-length inventory
    pass
```

---

#### Part E: Serialization Method 4 - Pickle (5 mins)

**Objective:** Observe Python's native serialization and inspect what it stores.

Pickle serializes entire Python objects automatically — no manual conversion needed. After saving, use `strings` and `xxd` to inspect the `.pkl` file and observe that class/attribute names are visible in the raw binary.

⚠️ **SECURITY WARNING:** Never unpickle data from untrusted sources! Pickle can execute arbitrary code during deserialization.

---

### Phase 3: Critical Incident - Data Integrity (30 minutes)

**Objective:** Build a system to detect and recover from corrupted character saves.

#### Part A: Checksum Implementation (20 minutes)

Add MD5 integrity verification to your JSON save system. If the file is modified or truncated, the checksum will fail, preventing the game from loading corrupt data.

```python
import hashlib

def save_json_with_checksum(self, filepath):
    # 1. Generate JSON string
    # 2. Calculate MD5 hash
    # 3. Save hash with data
    pass
```

---

## Format Comparison & Wrap-up (15 minutes)

After implementing the formats, complete the comparison analysis:

| Criterion | Custom Text | JSON | Binary (struct) | Pickle |
|-----------|-------------|------|-----------------|--------|
| **File Size** | Largest | Medium | Smallest | Small |
| **Human Readable** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Cross-Language** | ✅ Yes | ✅ Yes | ⚠️ Partial | ❌ No |
| **Security** | ✅ Safe | ✅ Safe | ✅ Safe | ❌ Dangerous |

---

## Submission Requirements

### 1. Code Files (starter files provided)
- `character.py` (Complete `Character` class with all save/load methods)
- `main.py` (Demonstration script that saves/loads in all four formats)

### 2. Output Files
Generated save files in the `data/` directory:
- `hero.txt` (Custom text format)
- `hero.json` (JSON format)
- `hero.bin` (Binary format)
- `hero.pkl` (Pickle format)

### 3. Documentation
Create `submission.md` with your format comparison and reflections on data integrity.

---

## Evaluation Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **Character Class** | 15 | Complete implementation with all attributes and helper methods |
| **Custom Text Format** | 10 | Key=value save/load with correct parsing |
| **JSON Format** | 20 | Valid JSON serialization, tuple handling, proper structure |
| **Binary Format (struct)** | 25 | Proper struct packing/unpacking (Core Skill) |
| **Pickle Format** | 5 | Basic pickle implementation with security awareness |
| **Checksum Validation** | 15 | MD5 integrity checking with correct wrapper pattern |
| **Documentation** | 10 | Format comparison, reflections, clear observations |
| **Total** | **100** | |

---

## Tips for Success

1. **Start Simple:** The custom text format is a warm-up. Get it working first, then build up to JSON and binary.

2. **Use `to_dict()` and `from_dict()`:** These helper methods on your Character class will make every serialization format easier to implement.

3. **Test Incrementally:** After implementing each format, immediately test a save/load round-trip:
   ```python
   hero = Character("TestHero", 10)
   hero.save_json("data/test.json")
   loaded = Character.load_json("data/test.json")
   print(hero.name == loaded.name)  # Should be True
   ```

4. **Print Debug Info:** When binary isn't working, print the raw bytes:
   ```python
   with open("data/hero.bin", "rb") as f:
       print(f.read(72).hex(' '))
   ```

5. **Compare File Sizes:** Use `os.path.getsize()` after implementing all formats to see the trade-offs in practice.

6. **Binary Mode is Crucial:** Use `'rb'`/`'wb'` for binary and pickle files, `'r'`/`'w'` for text and JSON.

---

## Academic Integrity Reminder

Data persistence is a foundational skill in computer forensics. You must:
- Understand every serialization method you implement
- Be able to explain why each format handles data differently
- Document any AI assistance used

**Remember:** In forensics, data integrity is everything. The systems you build today are the same principles used to preserve digital evidence in real investigations.

---

## Resources

- **Concepts Reference:** See [`concepts.md`](concepts.md) for detailed explanations of each format
- **Lab Notebook:** Use [`lab03.md`](lab03.md) for guided exercises with boilerplate code
- **Python `json` Module:** [json Documentation](https://docs.python.org/3/library/json.html)
- **Python `struct` Module:** [struct Documentation](https://docs.python.org/3/library/struct.html)
- **Python `hashlib` Module:** [hashlib Documentation](https://docs.python.org/3/library/hashlib.html)

---

## Questions?

If you encounter issues:
1. Re-read the relevant section in `concepts.md`
2. Check your file modes (`'w'` vs `'wb'`, `'r'` vs `'rb'`)
3. Use `xxd` or `cat` to inspect your output files
4. Verify round-trip: save, load, compare all attributes

**Remember:** The goal is to think like a data architect—design for reliability, verify for integrity.

