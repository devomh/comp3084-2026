# Lab 03 Notebook: The Time Capsule
**Data Persistence & Save System Implementation**

---

## Introduction

This notebook guides you through building a production-grade save system for an RPG game. You will implement four different serialization formats (Custom Text, JSON, Binary, and Pickle), compare their trade-offs, and develop a data integrity system using checksums.

---

## Phase 1: Field Work - Understanding Serialization

### Exercise 1.1: The Volatile Memory Problem

**Demonstration:** Run this code to understand why persistence is necessary.

```python
# Character exists only in RAM
class SimpleCharacter:
    def __init__(self, name, level):
        self.name = name
        self.level = level

hero = SimpleCharacter("Aragorn", 50)
print(f"{hero.name} is level {hero.level}")

# What happens when the program ends?
# Everything is LOST!
```

**Task:** Close Python and restart. Try to access `hero`. What happens?

**Question:** How can we preserve the character's state between program runs?

---

### Exercise 1.2: Format Comparison Research

Review the characteristics of the four serialization formats:

| Format | Human Readable? | Cross-Language? | File Size | Security |
|--------|-----------------|-----------------|-----------|----------|
| Custom Text | ✅ Yes | ✅ Yes | Largest | ✅ Safe |
| JSON | ✅ Yes | ✅ Yes | Medium | ✅ Safe |
| Binary (struct) | ❌ No | ⚠️ Partial | Smallest | ✅ Safe |
| Pickle | ❌ No | ❌ No | Small | ❌ Risky |

---

### Exercise 1.3: Inspect Sample Files

Inspect the provided sample data files using your terminal. Record your observations below.

```bash
# View JSON structure
cat data/valid_reference.json

# View as hex
xxd data/valid_reference.json | head -n 10

# Check file sizes
ls -la data/

# View corrupted file (notice what's wrong)
cat data/corrupted.json
```

**Observation Table:** Record what you find.

| Command | What did you observe? |
|---------|----------------------|
| `cat data/valid_reference.json` | |
| `xxd data/valid_reference.json \| head -n 10` | |
| `cat data/corrupted.json` | |
| `cat data/corrupted_syntax.json` | |

---

## Phase 2: The Build - Character Save System

### Part A: Character Class

Use this boilerplate to start. Note the `to_dict()` and `from_dict()` helper methods — these will make every serialization format easier to implement.

```python
class Character:
    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self.health = 100 * level
        self.max_health = 100 * level
        self.mana = 50 * level
        self.max_mana = 50 * level
        self.position = (0, 0)
        self.inventory = []
        self.gold = 100
        self.experience = 0

    def __repr__(self):
        return f"Character(name='{self.name}', level={self.level})"

    def display_stats(self):
        print(f"--- {self.name} (LVL {self.level}) ---")
        print(f"HP: {self.health}/{self.max_health} | MP: {self.mana}/{self.max_mana}")
        print(f"Pos: {self.position} | Gold: {self.gold}")
        print(f"Items: {', '.join(self.inventory) if self.inventory else 'None'}")

    def to_dict(self):
        """Convert character state to a plain dictionary.
        Useful for JSON and checksum serialization."""
        return {
            'name': self.name,
            'level': self.level,
            'health': self.health,
            'max_health': self.max_health,
            'mana': self.mana,
            'max_mana': self.max_mana,
            'position': list(self.position),  # tuple → list for JSON
            'inventory': self.inventory.copy(),
            'gold': self.gold,
            'experience': self.experience
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Character from a dictionary.
        Handles list → tuple conversion for position."""
        character = cls(data['name'], data['level'])
        character.health = data['health']
        character.max_health = data['max_health']
        character.mana = data['mana']
        character.max_mana = data['max_mana']
        character.position = tuple(data['position'])  # list → tuple
        character.inventory = data['inventory'].copy()
        character.gold = data['gold']
        character.experience = data['experience']
        return character
```

**Test your class:**
```python
hero = Character("Aragorn", 50)
hero.gold = 10000
hero.inventory = ["Sword", "Shield", "Potion"]
hero.position = (42, 17)
hero.display_stats()

# Test to_dict / from_dict round-trip
data = hero.to_dict()
clone = Character.from_dict(data)
print(f"Round-trip OK: {hero.name == clone.name and hero.gold == clone.gold}")
```

---

### Part B: Serialization Method 1 - Custom Text Format

**Goal:** Implement the simplest persistence format using key=value pairs.

The `save_text()` method is provided below. Your task is to implement `load_text()` which parses the file back into a `Character` object.

**The save method (provided):**

```python
def save_text(self, filepath):
    """Save character to custom text format."""
    with open(filepath, 'w') as f:
        f.write("[CHARACTER]\n")
        f.write(f"name={self.name}\n")
        f.write(f"level={self.level}\n")
        f.write(f"health={self.health}\n")
        f.write(f"max_health={self.max_health}\n")
        f.write(f"mana={self.mana}\n")
        f.write(f"max_mana={self.max_mana}\n")
        f.write(f"position={self.position[0]},{self.position[1]}\n")
        f.write(f"gold={self.gold}\n")
        f.write(f"experience={self.experience}\n")
        f.write("[INVENTORY]\n")
        for item in self.inventory:
            f.write(f"{item}\n")
```

**The load method (your task):**

```python
@classmethod
def load_text(cls, filepath):
    """Load character from custom text format."""
    with open(filepath, 'r') as f:
        lines = f.readlines()

    data = {}
    inventory = []
    section = None

    for line in lines:
        line = line.strip()
        if line == "[CHARACTER]":
            section = "character"
            continue
        elif line == "[INVENTORY]":
            section = "inventory"
            continue

        if section == "character" and '=' in line:
            key, value = line.split('=', 1)
            data[key] = value
        elif section == "inventory" and line:
            inventory.append(line)

    # TODO: Build the Character object from data and inventory
    # Hints:
    #   - Convert numeric fields: int(data['level'])
    #   - Parse position: data['position'].split(',') → tuple of ints
    #   - Set inventory from the inventory list
    pass
```

**Test it:**
```python
hero.save_text("data/hero.txt")
loaded = Character.load_text("data/hero.txt")
print(f"Name match: {hero.name == loaded.name}")
print(f"Level match: {hero.level == loaded.level}")
print(f"Inventory match: {hero.inventory == loaded.inventory}")
```

---

### Part C: Serialization Method 2 - JSON

**Goal:** Implement `save_json` and `load_json` using the `to_dict()` / `from_dict()` helpers.

**Challenge:** Remember that JSON converts your `position` tuple into a list. The `to_dict()` and `from_dict()` helpers already handle this conversion for you.

Your JSON file should use a `"character"` wrapper key to match the structure in `data/valid_reference.json`:

```json
{
  "character": {
    "name": "Aragorn",
    "level": 50,
    ...
  }
}
```

```python
import json

def save_json(self, filepath):
    """Save character to JSON format."""
    # Hint: Wrap self.to_dict() inside {"character": ...}
    #       then use json.dump() with indent=2
    # TODO: Implement
    pass

@classmethod
def load_json(cls, filepath):
    """Load character from JSON format."""
    # Hint: Use json.load(), extract data['character'],
    #       then use cls.from_dict() to reconstruct
    # TODO: Implement
    pass
```

**Test it:**
```python
hero.save_json("data/hero.json")
loaded = Character.load_json("data/hero.json")
print(f"Name match: {hero.name == loaded.name}")
print(f"Position match: {hero.position == loaded.position}")
```

**Inspect the output and compare to the reference:**
```bash
cat data/hero.json
cat data/valid_reference.json
```

---

### Part D: Serialization Method 3 - Binary Format (struct)

**Goal:** Implement compact binary saving. This is a core forensic skill for the course.

**Binary Layout:**
```
Offset  Size  Field          Format
------  ----  -----          ------
0       32    Name           32s (null-padded string)
32      4     Level          i
36      4     Health         i
40      4     Max Health     i
44      4     Mana           i
48      4     Max Mana       i
52      4     Position X     i
56      4     Position Y     i
60      4     Gold           i
64      4     Experience     i
68      4     Inv Count      i
72      ...   Inventory      variable-length strings
```

**Header format string:** `'32s10i'` — one 32-byte string followed by ten 4-byte integers = **72 bytes total**.

```python
import struct

HEADER_FORMAT = '32s10i'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)  # 72 bytes

def save_binary(self, filepath):
    """Save character to binary format using struct."""
    with open(filepath, 'wb') as f:
        # Prepare name as 32-byte null-padded bytes
        name_bytes = self.name.encode('utf-8')[:32].ljust(32, b'\x00')

        # Pack the fixed-size header
        header = struct.pack(HEADER_FORMAT,
            name_bytes,
            self.level, self.health, self.max_health,
            self.mana, self.max_mana,
            self.position[0], self.position[1],
            self.gold, self.experience,
            len(self.inventory)
        )
        f.write(header)

        # Write each inventory item as: length (4 bytes) + string bytes
        for item in self.inventory:
            item_bytes = item.encode('utf-8')
            f.write(struct.pack('i', len(item_bytes)))
            f.write(item_bytes)

@classmethod
def load_binary(cls, filepath):
    """Load character from binary format."""
    with open(filepath, 'rb') as f:
        # Read and unpack the fixed-size header
        header_data = f.read(HEADER_SIZE)
        fields = struct.unpack(HEADER_FORMAT, header_data)

        name = fields[0].rstrip(b'\x00').decode('utf-8')
        level, health, max_health, mana, max_mana, x, y, gold, experience, inv_count = fields[???]

        character = cls(???, ???)
        # TODO: Assign the remaining character attributes (health, max_health,
        #       mana, max_mana, position, gold, experience)

        for _ in range(???):
            n = struct.unpack('i', f.read(???))[0]
            item = f.read(???).decode('utf-8')
            character.inventory.append(item)

        return character
```

**Test it:**
```python
hero.save_binary("data/hero.bin")
loaded = Character.load_binary("data/hero.bin")
print(f"Name match: {hero.name == loaded.name}")
print(f"Gold match: {hero.gold == loaded.gold}")
```

**Inspect the binary output:**
```bash
xxd data/hero.bin | head -n 10
strings data/hero.bin
```

---

### Part E: Serialization Method 4 - Pickle

Observe how Python's native `pickle` module handles the entire object automatically — no manual field-by-field conversion needed.

```python
import pickle

def save_pickle(self, filepath):
    """Save character using pickle."""
    with open(filepath, 'wb') as f:
        pickle.dump(self, f)

@classmethod
def load_pickle(cls, filepath):
    """Load character from pickle file."""
    with open(filepath, 'rb') as f:
        return pickle.load(f)
```

⚠️ **SECURITY WARNING:** Never unpickle data from untrusted sources! Pickle can execute arbitrary code during deserialization.

**Test it:**
```python
hero.save_pickle("data/hero.pkl")
loaded = Character.load_pickle("data/hero.pkl")
print(f"Name match: {hero.name == loaded.name}")
print(f"Gold match: {hero.gold == loaded.gold}")
```

**Forensic exercise:** Inspect the pickle file with CLI tools. Notice that Python class and attribute names are visible in the raw binary — this is useful for forensic analysis but also reveals why pickle is insecure.

```bash
xxd data/hero.pkl | head -n 20
strings data/hero.pkl
```

**Questions:**
1. What class/attribute names can you spot in the `strings` output?
2. Why is pickle convenient but dangerous? When would you use it vs JSON?

---

## Phase 3: Critical Incident - Data Integrity

Before implementing checksums, experience the problem firsthand. Try loading the corrupted save files that "ElvenArcher92" reported:

```python
import json

# Try loading the truncated file
try:
    with open("data/corrupted.json", "r") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"corrupted.json failed: {e}")

# Try loading the syntax-error file
try:
    with open("data/corrupted_syntax.json", "r") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"corrupted_syntax.json failed: {e}")
```

**Observation:** Both files fail silently with different error messages. Without a checksum, a *subtly* corrupted file (e.g., one changed number) would load successfully with wrong data and the player would never know. That's what checksums prevent.

### Part A: Checksum Implementation

**Goal:** Use MD5 to verify that a save file hasn't been tampered with or corrupted.

The key insight is the **wrapper pattern**: compute the checksum on the character data *only*, then store both the data and checksum in an outer wrapper dictionary. This avoids the circular problem of checksumming data that already contains the checksum.

```python
import hashlib
import json

def save_json_with_checksum(self, filepath):
    """Save character to JSON with MD5 integrity checksum."""
    # 1. Get character data as a dictionary
    char_data = self.to_dict()

    # 2. Convert to a stable JSON string (sort_keys ensures consistency)
    json_str = json.dumps(char_data, indent=2, sort_keys=True)

    # 3. Compute MD5 checksum of the character data string
    checksum = hashlib.md5(json_str.encode('utf-8')).hexdigest()

    # 4. Create wrapper with checksum + character data
    wrapper = {
        'checksum': checksum,
        'character': char_data
    }

    # 5. Write wrapper to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(wrapper, f, indent=2)

    print(f"Saved with checksum: {checksum}")
```

**Now implement the verification side:**

```python
@classmethod
def load_json_with_checksum(cls, filepath):
    """Load character from JSON and verify checksum integrity."""
    with open(filepath, 'r', encoding='utf-8') as f:
        wrapper = json.load(f)

    # TODO: Recompute the checksum on wrapper['character']
    # 1. Get char_data from wrapper['character']
    # 2. Convert to JSON string using same parameters (indent=2, sort_keys=True)
    # 3. Compute MD5 of that string
    # 4. Compare with wrapper['checksum']
    # 5. If mismatch: raise ValueError("Checksum mismatch! File may be corrupted.")
    # 6. If OK: use cls.from_dict(char_data) to reconstruct
    pass
```

**Test it:**
```python
# Save with checksum
hero.save_json_with_checksum("data/hero_checked.json")

# Load and verify (should succeed)
loaded = Character.load_json_with_checksum("data/hero_checked.json")
print(f"Loaded OK: {loaded.name}")

# Now manually edit data/hero_checked.json (change gold value)
# Try loading again — should raise ValueError!
```

---

## Phase 4: Comparison & Wrap-up

Save the same character using all four formats and compare the results.

**Verification script:**

```python
import os

# Create a test character
hero = Character("Aragorn", 50)
hero.gold = 10000
hero.inventory = ["Sword", "Shield", "Potion"]
hero.position = (42, 17)
hero.experience = 99999

# Save in all formats
hero.save_text("data/hero.txt")
hero.save_json("data/hero.json")
hero.save_binary("data/hero.bin")
hero.save_pickle("data/hero.pkl")

# Compare file sizes
formats = {
    'Custom Text': 'data/hero.txt',
    'JSON':        'data/hero.json',
    'Binary':      'data/hero.bin',
    'Pickle':      'data/hero.pkl'
}

print("\n--- File Size Comparison ---")
for name, path in formats.items():
    size = os.path.getsize(path)
    print(f"{name:15s}: {size:5d} bytes")

# Verify round-trip for each format
print("\n--- Round-Trip Verification ---")
loaded_text = Character.load_text("data/hero.txt")
loaded_json = Character.load_json("data/hero.json")
loaded_bin  = Character.load_binary("data/hero.bin")
loaded_pkl  = Character.load_pickle("data/hero.pkl")

for label, loaded in [("Text", loaded_text), ("JSON", loaded_json),
                       ("Binary", loaded_bin), ("Pickle", loaded_pkl)]:
    match = (loaded.name == hero.name and loaded.level == hero.level
             and loaded.gold == hero.gold)
    print(f"{label:8s} round-trip: {'PASS' if match else 'FAIL'}")
```

**Record your findings in `submission.md`.**
