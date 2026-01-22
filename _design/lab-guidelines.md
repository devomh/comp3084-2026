# COMP3084 Lab Guidelines: Advanced Programming & Data Science

## 1. Course Philosophy
**"From Code Monkey to Data Alchemist"**

This laboratory course is designed to bridge the gap between basic programming proficiency (COMP3081/3083) and professional software engineering/data science capability. We move beyond *how* to write a loop, to *why* and *what* we are computing.

### Core Pillars
1.  **Data-Centricity**: Almost every lab involves real, messy, or massive data. We stop using hardcoded variables and start ingesting the world.
2.  **Forensic Mindset**: We don't just read files; we dissect them. We treat data as evidence and code as the investigation tool.
3.  **Hands-On & Immersive**: Labs are designed as professional scenarios or "Field Investigations." Students step into the role of a specialist (e.g., Data Forensics Expert, Systems Architect) solving a specific, context-rich problem, rather than completing abstract exercises.
4.  **AI-Augmented Development**: We do not shun AI; we master it. Students will use AI (Gemini, Copilot, etc.) as a junior developer or pair programmer. The goal is not to have AI do the work, but to have AI accelerate the trivial so we can focus on the complex.


## 2. Technical Stack
*   **Primary Language**: Python (shifting from C++ emphasis in syllabus to modern Data Science standards, while respecting the syllabus topics).
*   **Environment**: VS Code with Dev Containers or Google Colab (for heavy data tasks).
*   **Version Control**: Git & GitHub (continuation from COMP3083).
*   **Libraries**: NumPy, Pandas, Matplotlib, SciPy, struct (binary), json, pickle.

## 3. Lab Structure: The "Case Study" Format
Each weekly lab (3 hours) follows this rhythm:

1.  **Briefing (20 mins)**: High-level concept + The "Case" objective.
2.  **The Investigation (1 hour)**: Guided exploration using CLI tools, hex editors, or basic scripts to understand the data/problem.
3.  **The Build (1 hour)**: Core coding task. Implementing the solution using the target concepts.
4.  **The "Critical Incident" (40 mins)**: A high-stakes professional challenge. Usually involves a corrupted file, a hidden edge case, or a critical system failure.
5.  **Debrief**: Review and commit.

---

## 4. Weekly Investigations (Syllabus Mapping)

### Phase 1: The File System & Forensics (Weeks 1-3)

**Week 1: The Rosetta Frequency (Syllabus: I - Sequential Files)**
*   **Theme**: Cryptography & Linguistics.
*   **Task**: Read large text corpuses (Project Gutenberg books). Calculate letter frequency.
*   **AI Role**: Ask AI to generate regex patterns for cleaning text or to explain historical cipher distributions.
*   **Critical Incident**: Identify the language of a mystery file based solely on frequency analysis (Spanish vs. English vs. French vs. Python code).

**Week 2: The Hex Detective (Syllabus: II - File Examination)**
*   **Theme**: Reverse Engineering.
*   **Task**: Use CLI tools (`hexdump`, `strings`, `grep`) and Python to inspect binary files.
*   **AI Role**: Upload a snippet of a binary header and ask AI to hypothesize the file format.
*   **Critical Incident**: You are given a "corrupt" PNG file header. Fix the hex bytes using a hex editor/python script so the image displays again.

**Week 3: The Time Capsule (Syllabus: III & IV - Persistence & Serialization)**
*   **Theme**: Save States & RPGs.
*   **Task**: Create a simple Text RPG character class. Implement `save()` and `load()` methods using: 1. Custom text format, 2. Binary (`struct`), 3. JSON, 4. Pickle.
*   **AI Role**: Compare the file sizes and readability of the different formats.
*   **Critical Incident**: "Data Recovery". Recover a corrupted user profile from a partial JSON dump and verify its integrity using a checksum algorithm.

### Phase 2: Big Data & Processing (Weeks 4-7)

**Week 4: The Needle in the Haystack (Syllabus: IV - MapReduce)**
*   **Theme**: Distributed Thinking.
*   **Task**: Simulate a MapReduce job on a single machine using Python generators. Process a massive log file (1GB+) to count error codes.
*   **AI Role**: Generate the massive dummy log file. Optimize the mapping function.
*   **Critical Incident**: The "Risk Analysis". Correlate IP addresses with error codes to find a "hacker" in the logs.

**Week 5: Matrix Vision (Syllabus: V - Vectors & Homogeneous Data)**
*   **Theme**: Computer Vision Basics.
*   **Task**: Load an image as a NumPy array. Apply manual filters (grayscale, inversion, thresholding) without using image libraries (only array math).
*   **AI Role**: Explain the matrix math behind a "blur" convolution.
*   **Critical Incident**: "Steganography". Use boolean masking to reveal a hidden message encoded in the least significant bits of the pixel values.

**Week 6: Digital Waves (Syllabus: VI - Digital Signals)**
*   **Theme**: Audio Engineering.
*   **Task**: Read raw audio (WAV) files. Visualize the waveform. Change the volume, speed up, or reverse the audio by manipulating the raw bytes.
*   **AI Role**: Help write the code to convert stereo to mono by averaging channels.
*   **Critical Incident**: "The Ghost Voice". Isolate a specific frequency or remove high-pitch noise from a "dirty" recording.

**Week 7: The Data Lake (Syllabus: VII - Heterogeneous Tables)**
*   **Theme**: Urban Data Science.
*   **Task**: Use Pandas to load real data from `data.pr.gov` (e.g., energy consumption or crime stats). Filter, sort, and re-index.
*   **AI Role**: "Data Assistant" - ask AI to generate the Pandas one-liners for complex groupings.
*   **Critical Incident**: Find the anomaly. Which municipality had the weirdest power consumption pattern?

### Phase 3: Advanced Analysis (Weeks 8-11)

**Week 8: The Data Janitor (Syllabus: VIII - Cleaning)**
*   **Theme**: Dirty Data Warfare.
*   **Task**: You are given a "cursed" dataset (mixed dates, typos, duplicates, nulls). Build a pipeline to clean it. Use Edit Distance (Levenshtein) to fuzzy match strings.
*   **AI Role**: Generate a script to detect common data entry errors.
*   **Critical Incident**: Reconcile two lists of names that are spelled slightly differently (e.g., "Juan Perez" vs "J. Perez").

**Week 9: The Mashup (Syllabus: IX - Indexing & Combining)**
*   **Theme**: Correlation != Causation.
*   **Task**: Join two unrelated datasets (e.g., "Weather in PR" and "Ice Cream Sales"). Use multi-indexing.
*   **AI Role**: Suggest potential correlations to investigate.
*   **Critical Incident**: "The Missing Link". Reconstruct a timeline of events by joining fragments from three different log files.

**Week 10: The Stock Market Oracle (Syllabus: X - Time Series)**
*   **Theme**: Financial Tech.
*   **Task**: Load time-series data. Resample (daily to monthly). Calculate rolling averages. Visualize with Matplotlib.
*   **AI Role**: Explain the difference between a simple moving average and an exponential one.
*   **Critical Incident**: Detect "flash crashes". Write an algorithm that triggers an alert when the value drops X% within Y minutes.

**Week 11: The Spam Filter (Syllabus: XI - Sparse Matrices)**
*   **Theme**: NLP & Text Mining.
*   **Task**: Build a Bag-of-Words model from a set of emails. Store it in a Sparse Matrix. Find the most common n-grams.
*   **AI Role**: Generate a list of "spammy" words to test against.
*   **Critical Incident**: Calculate the "distance" between two emails to see if they are templates of the same spam campaign.

### Phase 4: The Final Frontier (Week 12+)

**Week 12: Mission Control (Syllabus: XII - Final Project/GUI)**
*   **Theme**: The Dashboard.
*   **Task**: Integrate previous concepts. Build a GUI (using a Python framework compatible with the syllabus goals, e.g., Tkinter, PyQt, or a web-based dashboard like Streamlit if flexible) that loads a file, processes it (cleaning/analysis), and displays charts.
*   **Project**: "The Inspector". A tool where a user drops a dataset, and the tool automatically attempts to identify columns, clean data, and produce a summary report.

## 5. Assessment Strategy
*   **Labs (60%)**: Completion of the "Investigation" and "Build" phases.
*   **Critical Incidents (Bonus/Distinction)**: Successfully resolving the high-stakes challenge.
*   **Final Project (20%)**: "Mission Control" application.
*   **Exams (20%)**: Practical coding exams (open book/open AI).

## 6. Guidelines for the Instructor
*   **Don't lecture for 3 hours.** Lecture for 30 minutes, then circulate.
*   **Break things.** Give students broken files, bad data, and buggy code. They learn more from fixing than from creating from scratch.
*   **Embrace the "Magic".** When a library does something magical (like Pandas reading a CSV), stop and make them do it manually once (Week 1/2) so they appreciate the magic later.