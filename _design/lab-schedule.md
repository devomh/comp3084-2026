# COMP3084 Lab Schedule: The Case Log

This document outlines the 12-week schedule of investigations for COMP3084. Each investigation is mapped to the course syllabus and designed to build forensic and architectural depth.

## 1. Weekly Investigations (Syllabus Mapping)

### Phase 1: The File System & Forensics (Weeks 1-3)

**Week 1: The Rosetta Frequency (Syllabus: I - Sequential Files)**
*   **Theme**: Cryptography & Linguistics.
*   **Task**: Read large text corpuses (Project Gutenberg books). Calculate letter frequency.
*   **AI Role**: (Optional) Ask AI to generate regex patterns for cleaning text or to explain historical cipher distributions.
*   **Critical Incident**: Identify the language of a mystery file based solely on frequency analysis (Spanish vs. English vs. French vs. Python code).

**Week 2: The Hex Detective (Syllabus: II - File Examination)**
*   **Theme**: Reverse Engineering.
*   **Task**: Use CLI tools (`hexdump`, `strings`, `grep`) and Python to inspect binary files.
*   **AI Role**: (Optional) Upload a snippet of a binary header and ask AI to hypothesize the file format.
*   **Critical Incident**: You are given a "corrupt" PNG file header. Fix the hex bytes using a hex editor/python script so the image displays again.

**Week 3: The Time Capsule (Syllabus: III & IV - Persistence & Serialization)**
*   **Theme**: Save States & RPGs.
*   **Task**: Create a simple Text RPG character class. Implement `save()` and `load()` methods using: 1. Custom text format, 2. Binary (`struct`), 3. JSON, 4. Pickle.
*   **AI Role**: (Optional) Compare the file sizes and readability of the different formats.
*   **Critical Incident**: "Data Recovery". Recover a corrupted user profile from a partial JSON dump and verify its integrity using a checksum algorithm.

### Phase 2: Big Data & Processing (Weeks 4-7)

**Week 4: The Needle in the Haystack (Syllabus: IV - MapReduce)**
*   **Theme**: Distributed Thinking.
*   **Task**: Simulate a MapReduce job on a single machine using Python generators. Process a massive log file (1GB+) to count error codes.
*   **AI Role**: (Optional) Generate the massive dummy log file. Optimize the mapping function.
*   **Critical Incident**: The "Risk Analysis". Correlate IP addresses with error codes to find a "hacker" in the logs.

**Week 5: Matrix Vision (Syllabus: V - Vectors & Homogeneous Data)**
*   **Theme**: Computer Vision Basics.
*   **Task**: Load an image as a NumPy array. Apply manual filters (grayscale, inversion, thresholding) without using image libraries (only array math).
*   **AI Role**: (Optional) Explain the matrix math behind a "blur" convolution.
*   **Critical Incident**: "Steganography". Use boolean masking to reveal a hidden message encoded in the least significant bits of the pixel values.

**Week 6: Digital Waves (Syllabus: VI - Digital Signals)**
*   **Theme**: Audio Engineering.
*   **Task**: Read raw audio (WAV) files. Visualize the waveform. Change the volume, speed up, or reverse the audio by manipulating the raw bytes.
*   **AI Role**: (Optional) Help write the code to convert stereo to mono by averaging channels.
*   **Critical Incident**: "The Ghost Voice". Isolate a specific frequency or remove high-pitch noise from a "dirty" recording.

**Week 7: The Data Lake (Syllabus: VII - Heterogeneous Tables)**
*   **Theme**: Urban Data Science.
*   **Task**: Use Pandas to load real data from `data.pr.gov` (e.g., energy consumption or crime stats). Filter, sort, and re-index.
*   **AI Role**: (Optional) "Data Assistant" - ask AI to generate the Pandas one-liners for complex groupings.
*   **Critical Incident**: Find the anomaly. Which municipality had the weirdest power consumption pattern?

### Phase 3: Advanced Analysis (Weeks 8-11)

**Week 8: The Data Janitor (Syllabus: VIII - Cleaning)**
*   **Theme**: Dirty Data Warfare.
*   **Task**: You are given a "cursed" dataset (mixed dates, typos, duplicates, nulls). Build a pipeline to clean it. Use Edit Distance (Levenshtein) to fuzzy match strings.
*   **AI Role**: (Optional) Generate a script to detect common data entry errors.
*   **Critical Incident**: Reconcile two lists of names that are spelled slightly differently (e.g., "Juan Perez" vs "J. Perez").

**Week 9: The Mashup (Syllabus: IX - Indexing & Combining)**
*   **Theme**: Correlation != Causation.
*   **Task**: Join two unrelated datasets (e.g., "Weather in PR" and "Ice Cream Sales"). Use multi-indexing.
*   **AI Role**: (Optional) Suggest potential correlations to investigate.
*   **Critical Incident**: "The Missing Link". Reconstruct a timeline of events by joining fragments from three different log files.

**Week 10: The Stock Market Oracle (Syllabus: X - Time Series)**
*   **Theme**: Financial Tech.
*   **Task**: Load time-series data. Resample (daily to monthly). Calculate rolling averages. Visualize with Matplotlib.
*   **AI Role**: (Optional) Explain the difference between a simple moving average and an exponential one.
*   **Critical Incident**: Detect "flash crashes". Write an algorithm that triggers an alert when the value drops X% within Y minutes.

**Week 11: The Spam Filter (Syllabus: XI - Sparse Matrices)**
*   **Theme**: NLP & Text Mining.
*   **Task**: Build a Bag-of-Words model from a set of emails. Store it in a Sparse Matrix. Find the most common n-grams.
*   **AI Role**: (Optional) Generate a list of "spammy" words to test against.
*   **Critical Incident**: Calculate the "distance" between two emails to see if they are templates of the same spam campaign.

### Phase 4: The Final Frontier (Week 12+)

**Week 12: Mission Control (Syllabus: XII - Final Project/GUI)**
*   **Theme**: The Dashboard.
*   **Task**: Integrate previous concepts. Build a GUI (using a Python framework compatible with the syllabus goals, e.g., Tkinter, PyQt, or a web-based dashboard like Streamlit if flexible) that loads a file, processes it (cleaning/analysis), and displays charts.
*   **Project**: "The Inspector". A tool where a user drops a dataset, and the tool automatically attempts to identify columns, clean data, and produce a summary report.
