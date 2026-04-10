# Lab 07: The Needle in the Haystack

**Concepts**: [![Open Concepts In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/devomh/comp3084-2026/blob/main/lab07/concepts.ipynb)

**Lab07**: [![Open Lab Notebook In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/devomh/comp3084-2026/blob/main/lab07/lab07.ipynb)

## Case Brief

### The Situation

The Security Operations Center has captured a growing mountain of evidence:
incident reports, authentication logs, and transaction records. The problem is
no longer writing a loop over one file. The problem is thinking like a
distributed system. When the dataset gets large enough, the question changes
from "Can I solve it?" to "How do I split the work so the machine cluster can
solve it with me?"

Your task is to build a distributed analysis workflow that can process text
evidence, summarize transaction activity by account, and explain how the
computation is divided across partitions.

### Your Mission

You are a **Distributed Forensics Analyst** tasked with:

1. Understanding the MapReduce pattern by working through a toy example by hand
2. Launching a local PySpark session that simulates a small cluster
3. Building a distributed word-count pipeline on incident text
4. Summarizing transaction activity by account using PySpark DataFrames
5. Inspecting partitions to reason about where the shuffle happens

### The Stakes

If your reasoning about distributed computation is wrong, the code may still
"work" on small data while collapsing on real workloads. This lab is about more
than counting words or summing transactions. It is about learning when a
computation shuffles data, why that is expensive, and how to design a pipeline
that scales instead of stalling.

---

## Chain of Custody

### Technical Requirements

- Completion of Lab 06 (DataFrames, filtering, aggregation)
- Python 3.8 or higher
- Python libraries: `pyspark`, `matplotlib`

```bash
pip install pyspark matplotlib
```

**Library Constraints (strictly enforced):**

- **`pyspark`** - Core distributed processing engine for this lab
- **`matplotlib`** - Final chart for presenting account findings
- **Built-in Python** - Small helper logic, printing, and manual examples
- **No `pandas` for the core analysis pipeline**
- **No external big-data services** - run everything through local Spark

### Evidence Files (Provided)

Located in the [`data/`](data/) directory:

1. **`incident_report.txt`** - Short text corpus for the distributed word-count
   investigation
2. **`transactions_small.csv`** - Synthetic financial transactions for the
   transaction analysis phase

These are intentionally small so you can debug quickly. The same pipeline
should scale to larger files after it works on the sample evidence.

```bash
# Verify the evidence files are present
ls data/
# Expected: incident_report.txt  transactions_small.csv
```

---

## Investigation Phases

Open [`lab07.md`](lab07.md) (or [`lab07.ipynb`](lab07.ipynb) in Jupyter/Colab)
for the guided exercises. Consult [`concepts.md`](concepts.md) for technical
background.

### Phase 1: Manual MapReduce - Think Like the Cluster (25 min)

**Objective:** Understand Map, Shuffle, and Reduce before using Spark.

You will:

- Work through a tiny word-count example by hand
- Identify what each mapper emits as `(key, value)` pairs
- Group identical keys together during the shuffle step
- Sum grouped values during reduce
- Repeat the same reasoning on suspicious transactions per account

**Key insight:** MapReduce is not a special magic command. It is a disciplined
way to break a large job into independent local work, regroup the results by
key, and then aggregate them.

### Phase 2: Distributed WordCount with PySpark (45 min)

**Objective:** Build the classic MapReduce pipeline on text evidence.

You will:

- Start a `SparkSession` in `local[4]` mode to simulate 4 worker cores
- Read `data/incident_report.txt` as an RDD
- Normalize and tokenize text
- Ignore stop words and words shorter than 6 characters
- Count word frequencies with `flatMap()`, `map()`, and `reduceByKey()`
- Inspect partition contents with `glom()`

**Key insight:** `reduceByKey()` is a distributed version of "group identical
keys, then combine their values."

### Phase 3: Critical Incident - Transaction Analysis by Account (40 min)

**Objective:** Apply the same MapReduce grouping pattern to transaction data.

You will:

1. Load a transaction CSV into a Spark DataFrame
2. Group by `account_id` and compute counts, totals, and maximums
3. Inspect partition sizes before and after the groupBy
4. Create a bar chart of the top 5 accounts by total amount

**Key insight:** `groupBy("account_id")` is the same pattern as WordCount —
only the key changed. The shuffle still happens, and the data still moves.

---

## Wrap-Up

After completing all phases, verify the notebook runs from top to bottom
without errors and that you can answer the following:

- What exactly did the map step emit?
- When did the shuffle happen?
- Which account moved the most money?
- Did the partition sizes change after the groupBy?

**Before you leave:**

- Complete all sections of [`submission.md`](submission.md), including the
  manual MapReduce tables and the account findings
- Ensure all notebook cells run without errors from top to bottom
- Include your AI Usage Appendix if applicable

---

## Submission Requirements

### 1. Notebook

- [`lab07.ipynb`](lab07.ipynb) - All cells implemented and run without errors,
  top to bottom

### 2. Output Files

Generated during the investigation:

- `data/top_accounts.png` - Bar chart of the top 5 accounts by total amount

### 3. Documentation

Complete [`submission.md`](submission.md) with:

- Manual MapReduce walkthrough for the toy example
- Top 10 words from the distributed word count
- Account summary findings from the transaction analysis
- Answers to all reflection questions

---

## Evaluation Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **Manual MapReduce** | 20 | Correct map, shuffle, and reduce reasoning on toy examples |
| **Spark Setup** | 10 | Session starts correctly; partition count inspected |
| **Distributed WordCount** | 25 | Correct normalization, filtering, and word-frequency pipeline |
| **Partition Inspection** | 10 | Meaningful use of `glom()` or partition reasoning |
| **Aggregation by Account** | 20 | Correct groupBy with counts and totals; findings explained |
| **Visualization** | 15 | Clear bar chart with labels and ranking |
| **Total** | **100** | |

**Bonus:**

| Component | Points | Criteria |
|-----------|--------|----------|
| Data skew experiment | +5 | Demonstrates an intentionally unbalanced key distribution |
| Risk flag with `F.when` | +5 | Adds a HIGH/NORMAL flag and counts HIGH transactions per account |

---

## Tips for Success

1. **Start small and visible:** Read the toy example in [`concepts.md`](concepts.md)
   first. If you cannot explain MapReduce by hand, Spark code will feel opaque.

2. **Separate transformations from actions:** In Spark, code like `map()` and
   `filter()` builds a plan. Work does not happen until an action such as
   `collect()`, `count()`, `take()`, or `show()` is executed.

3. **Watch for shuffle boundaries:** Operations that regroup by key such as
   `reduceByKey()` or `groupBy()` are usually where the expensive data movement
   begins.

4. **Inspect partitions on purpose:** The cluster cannot think for you. Use
   `getNumPartitions()` and `glom()` to observe how your data is actually
   distributed.

5. **Treat the sample files as debugging evidence:** Get the logic correct on
   the small files before talking about "big data."

---

## Resources

- PySpark Quick Start:
  [SparkSession docs](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.builder.getOrCreate.html)
- RDD Programming Guide:
  [Spark RDD docs](https://spark.apache.org/docs/latest/rdd-programming-guide.html)
- Spark SQL DataFrames:
  [DataFrame docs](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html)

## Questions?

If your pipeline works but you cannot explain where the shuffle happens, you are
not done. The code artifact is only part of the investigation; your explanation
is the real evidence.
