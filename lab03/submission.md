# Lab 03 Submission: The Time Capsule

**Student Name:** [Your Name]
**Date:** [Date]

## Section A: Format Implementation

### Custom Text Format
- [ ] `save_text()` implemented (provided)
- [ ] `load_text()` implemented (parsing key=value pairs)
- [ ] Correctly parses position from comma-separated string
- [ ] Correctly converts numeric fields from strings
- [ ] File size: _____ bytes

### JSON Format
- [ ] `save_json()` implemented
- [ ] `load_json()` implemented
- [ ] Handled tuple conversion (position)
- [ ] File size: _____ bytes

### Binary Format (struct)
- [ ] `save_binary()` implemented
- [ ] `load_binary()` implemented
- [ ] Fixed-size header (32s10i)
- [ ] Variable-length inventory
- [ ] File size: _____ bytes

### Pickle Format
- [ ] `save_pickle()` implemented
- [ ] `load_pickle()` implemented
- [ ] File size: _____ bytes

---

## Section B: Data Integrity

### Checksum Validation
- [ ] MD5 calculation implemented
- [ ] Integrity check catches modifications
- [ ] Verified on `valid_reference.json`

---

## Section C: Format Comparison

| Format | Size (bytes) | Human Readable | Best Use Case |
|--------|--------------|----------------|---------------|
| Custom Text |         |                |               |
| JSON   |              |                |               |
| Binary |              |                |               |
| Pickle |              |                |               |

**Analysis:**
Which format would you choose for a production game save system and why?

---

## Section D: Reflections

1. Why does the `struct` module require a "format string" like `'32s10i'`?
2. What are the security risks of using `pickle` for player-shared save files?
3. How does a checksum protect the game from "cheating" by manually editing save files?

---

## Section E: AI Usage Appendix (if applicable)
[Standard AI usage disclosure]
