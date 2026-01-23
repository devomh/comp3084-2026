# COMP3084 Lab Guidelines: Field Operations Manual

## 1. Course Philosophy
**"From Code Monkey to Data Alchemist"**

This course treats software engineering and data science as a forensic discipline. You are not just writing code; you are an **Investigator** dissecting data evidence and an **Architect** building robust systems.

### Core Pillars
1.  **Forensic Mindset**: Data is treated as evidence. Every byte has a story, and code is the tool we use to uncover it.
2.  **Immersive Scenarios**: Labs are designed as "Field Investigations." You step into the role of a specialist solving context-rich, professional problems.
3.  **Sovereign Development**: We prioritize deep understanding. While we leverage modern tools, we maintain "Sovereignty" over our code—if you can't explain it or verify it, you don't own it.
4.  **Verification over Production**: In the era of high-speed generation, the most valuable skill is the ability to **audit** and **validate** results.

## 2. Technical Environment & Tooling
To ensure parity across different systems, the following environment is standard issue:
*   **Editor**: VS Code (Recommended extensions: Python, Jupyter, GitHub Copilot/Gemini).
*   **Operating Systems**:
    *   **Linux/macOS**: Native terminal.
    *   **Windows**: Must use **Git Bash**, **WSL**, or **xxd** (for hex examination) to ensure compatibility with Unix-style commands (`hexdump`, `strings`, `grep`).
*   **Data Safety**:
    *   **Tiered Data**: For massive datasets (1GB+), the instructor will provide `sample`, `medium`, and `massive` versions. Start with samples to preserve hardware performance.
    *   **Security**: Never run `pickle.load()` on files from untrusted sources.

## 3. The "Case Study" Protocol
Every lab follows a standardized template to maintain professional consistency:

1.  **Case Brief**: The objective and professional context.
2.  **Chain of Custody**: Intel on prerequisites, starter files, and setup.
3.  **Phase 1: Field Work (Investigation)**: Initial data exploration, probing, and discovery.
4.  **Phase 2: Implementation (The Build)**: Constructing the core logic or system.
5.  **Phase 3: Critical Incident (Bonus)**: A high-stakes escalation or edge case requiring advanced problem-solving.
6.  **Incident Report (Debrief)**: Final verification, documentation, and submission.

## 4. AI Usage Policy
AI is a powerful "Compiler" of natural language, but it can also lead to "Cognitive Atrophy." 

### General Rules
*   **Optional & Selective**: AI tools (Gemini, ChatGPT, Copilot) are **optional**. They are permitted only in labs specifically designated as "AI-Augmented."
*   **The Verifier Principle**: You are the **Senior Editor**. You are responsible for every line of code submitted. Submitting AI-generated code that you cannot explain is a violation of academic integrity.
*   **No Private Data**: Never upload student data, personal information, or full assignment descriptions to public LLMs.

### Socratic Interaction
When using AI for help, you are encouraged to treat it as a **Socratic Tutor**. Instead of asking for the solution, use prompts like:
> "I am working on [Topic]. Don't give me the code, but ask me a question that helps me realize the error in my logic regarding [Specific Problem]."

### The AI Appendix (Mandatory)
If AI tools are used in *any* capacity for a lab, an **AI Usage Appendix** must be appended to the submission (usually at the end of the `README.md`).

**Required Fields for the AI Log:**
1.  **Tool Used**: (e.g., Gemini 1.5 Pro, GitHub Copilot).
2.  **Methodology**: (e.g., "Used to debug a specific IndexError" or "Used to generate a regex").
3.  **The Prompt**: Copy the most representative instruction given to the AI.
4.  **The Output**: Describe what the AI delivered and if it contained any "hallucinations" or errors.
5.  **Human Value-Add**: **(Most Important)** Detail the changes, corrections, or expansions you made. How did you verify the logic?

## 5. Assessment & Defense
*   **Labs (60%)**: Completion of Phase 1 and 2.
*   **Critical Incidents (Bonus)**: Recognition for resolving high-complexity escalations.
*   **Oral Defense**: The instructor may perform "Interactive Defense" sessions where you must explain, justify, or modify your code in real-time. The artifact (the code) is the starting point; your understanding is the final grade.

## 6. Guidelines for the Instructor
*   **The "Gymnasium" Approach**: Design labs to be "Desirably Difficult." If it's too easy, there is no learning; if it's too hard without guidance, there is only frustration.
*   **The Forensic Twist**: Always include one "broken" or "anomalous" data point that forces students to move beyond the happy path.

## 7. Standard Field Kit (File Organization)
To ensure professional consistency and support both local and cloud workflows (e.g., Colab), every lab investigation must follow this standard directory structure:

### Directory Structure
```text
labXX/
├── README.md               # The Case File (Student-facing instructions & context)
├── concepts.md             # The "Field Manual" (Definitions + Mermaid UML diagrams)
├── labXX.md                # The Lab Notebook source (Text + Code blocks)
├── labXX.ipynb             # (Generated) The Colab-ready notebook
├── data/                   # The Evidence Locker (Forensic Assets)
│   ├── evidence_A.dat      # Control Sample
│   └── evidence_B.bin      # Mystery Artifact
└── src/                    # Reference Implementation (Solutions/Modules)
    ├── module.py           # The Python Module (Classes/Functions)
    └── main.py             # The Execution Script
```

### Document Roles & Workflow
1.  **`concepts.md` (The Field Manual)**: 
    *   Separates theory from execution.
    *   Provides high-level definitions (e.g., Encapsulation, MapReduce).
    *   Includes **Mermaid diagrams** (UML, Flowcharts) to visualize systems.
2.  **`labXX.md` (The Notebook Source)**:
    *   The "Source of Truth" for the guided investigation.
    *   Contains the narrative, instructions, and empty code cells.
    *   **Workflow**: Written in Markdown, then converted to `labXX.ipynb` (using `jupytext` or similar) for students to use in Jupyter/Colab.
3.  **`data/` (The Evidence Locker)**:
    *   Centralized repository for all raw data.
    *   Keeps the root directory clean and professional.
4.  **`src/` (The Arsenal)**:
    *   Contains the modular Python code (`.py`) developed during the lab.
    *   Reinforces the distinction between *analysis* (Notebook) and *software engineering* (Modules).
