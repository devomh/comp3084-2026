# COMP3084: Introduction to Programming and CS II

**University of Puerto Rico at Humacao**
**Spring 2026**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Course Description

This laboratory course introduces students to data processing, file I/O, and software engineering fundamentals through immersive, narrative-driven investigations. Students transform from "code monkeys" to "data alchemists" by treating data as evidence and applying forensic methodologies to real-world computational problems.

### Philosophy: The Forensic Approach

- **Investigators First**: Every lab is a "Field Investigation" where students are Linguistic Forensics Officers, Data Detectives, or Digital Archaeologists
- **Evidence-Based Learning**: Data files become crime scenes; every byte tells a story
- **Sovereign Development**: Students must understand and explain every line of code they submit
- **Verification over Production**: Auditing and validating results is prioritized over raw code generation

## Repository Structure

```
comp3084_2026-01/
├── 00_syllabus/           # Official course syllabi (Spanish)
├── _design/               # Course design documents and lab schedule
├── lab01/                 # Lab 01: The Rosetta Frequency
│   ├── README.md          # Case briefing
│   ├── concepts.md        # Technical reference
│   ├── lab01.md           # Guided notebook
│   ├── lab01.ipynb        # Jupyter notebook
│   └── data/              # Evidence files
├── lab02/                 # (Future) Lab 02: The Hex Detective
├── lab03/                 # (Future) Lab 03: The Time Capsule
└── ...                    # Additional labs (weeks 4-12)
```

## Labs Overview

### Phase 1: File System & Forensics (Weeks 1-3)
- **Lab 01**: The Rosetta Frequency - Linguistic fingerprinting through letter frequency analysis
- **Lab 02**: The Hex Detective - Binary file formats and data reconstruction
- **Lab 03**: The Time Capsule - File metadata and temporal analysis

### Phase 2: Big Data & Processing (Weeks 4-7)
- MapReduce patterns, computer vision, audio processing, and real-world datasets

### Phase 3: Advanced Analysis (Weeks 8-11)
- Data cleaning, indexing, time series, and sparse matrices

### Phase 4: The Final Frontier (Week 12+)
- Capstone GUI project integrating all concepts

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- VS Code (recommended) or any text editor
- Terminal access (Linux/macOS/Git Bash on Windows)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/devomh/comp3084-2026.git
cd comp3084-2026

# Navigate to first lab
cd lab01

# Read the case brief
cat README.md

# Start your investigation
python3 --version  # Verify Python installation
```

### Using Jupyter Notebooks

Each lab includes an interactive Jupyter notebook that can be opened directly in Google Colaboratory by clicking the badge in the lab's README.

## Learning Objectives

By the end of this course, students will be able to:

1. **Object-Oriented Programming**: Design and implement classes with inheritance and encapsulation
2. **File I/O Mastery**: Handle sequential files, binary formats, and encoding challenges
3. **Data Structures**: Apply appropriate data structures (lists, dictionaries, sets) to real problems
4. **Exception Handling**: Write robust code that gracefully handles errors
5. **Data Processing**: Transform, clean, and analyze large datasets
6. **Software Engineering**: Build reusable, maintainable, well-documented code

## AI Usage Policy

This course acknowledges the reality of generative AI while maintaining academic integrity:

- **Students are Senior Engineers**, not prompt writers - you own every line of code
- **AI is optional and selective** - only certain labs permit AI assistance
- **Mandatory documentation** - All AI usage must be documented in appendices
- **Verification is the skill** - The ability to audit and validate AI output is more valuable than generation

## Technical Environment

- **Languages**: Python 3.8+
- **Libraries**: Standard library (no heavy dependencies initially), progressing to NumPy, Pandas, Matplotlib
- **Tools**: Jupyter/Colab notebooks, Git, VS Code extensions (Python, Jupyter)
- **Operating Systems**: Linux/macOS native terminal; Windows via Git Bash or WSL

## Course Documents

- **Lab Schedule**: See [_design/lab-schedule.md](_design/lab-schedule.md) for the complete 12-week investigation timeline
- **Lab Guidelines**: See [_design/lab-guidelines.md](_design/lab-guidelines.md) for standards and protocols
- **Official Syllabus**: See [00_syllabus/](00_syllabus/) for formal course specifications (Spanish)

## Contributing

This course material is released under a Creative Commons Attribution 4.0 International License. Contributions, improvements, and adaptations are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear descriptions
4. Maintain the pedagogical approach and narrative style

## Academic Integrity

Students submitting code they cannot explain violate the course's integrity policy. **The Verifier Principle**: In the age of generative AI, the most valuable skill is the ability to audit and validate code, not just generate it.

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](LICENSE).

You are free to:
- **Share**: Copy and redistribute the material in any medium or format
- **Adapt**: Remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made
