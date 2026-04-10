# Lab 07: The Needle in the Haystack -- Lab Notebook
**Distributed Analysis with MapReduce and PySpark**

---

## Introduction

Welcome to the Security Operations Center. You are now working as a
**Distributed Forensics Analyst**. The datasets in front of you are no longer
comfortable single-file exercises. They are the kind of workloads that force
you to think about partitions, grouping by key, and where the expensive data
movement begins.

Your mission has three parts:

1. **Understand** MapReduce by walking through a toy example manually
2. **Build** a distributed WordCount pipeline on text evidence using PySpark
3. **Summarize** transaction activity by account and explain how the work is
   distributed

**Constraints:** You may use `pyspark`, `matplotlib`, and built-in Python. Do
not use `pandas` for the core analytics pipeline.

**Reference:** Consult [`concepts.md`](concepts.md) for the full explanation of
MapReduce, partitions, shuffle, data skew, and the manual toy example.

---

## Setup

Run this cell first. Every later cell depends on these imports.

```python
!pip install -q pyspark
```

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import matplotlib.pyplot as plt
import re
```

```python
spark = SparkSession.builder \
    .master("local[4]") \
    .appName("COMP3084_Lab07_The_Needle_in_the_Haystack") \
    .getOrCreate()

sc = spark.sparkContext
print("Spark session started.")
print("Default parallelism:", sc.defaultParallelism)
```

```python
def show_partition_sizes(rdd, label="RDD"):
    """Print the number of records in each partition."""
    partition_sizes = rdd.glom().map(len).collect()
    print(f"{label} partition sizes: {partition_sizes}")
    print(f"Total records: {sum(partition_sizes)}")


def normalize_word(word):
    """Lowercase and remove non-letter characters."""
    return re.sub(r"[^a-z]", "", word.lower())
```

---

## Phase 1: Manual MapReduce - Think Like the Cluster

Before touching Spark, we will simulate the MapReduce pattern with a toy
example. This is the part you should be able to explain on paper.

### Exercise 1.1: WordCount by Hand

```python
toy_lines = [
    "alert login failed",
    "alert payment failed",
    "login succeeded alert"
]

for i, line in enumerate(toy_lines, start=1):
    print(f"Line {i}: {line}")
```

**Task:** In [`submission.md`](submission.md), manually write:

- the emitted `(word, 1)` pairs for each line
- the grouped keys after shuffle
- the final reduced counts

Now reproduce the same logic in plain Python.

```python
# Map step: emit (word, 1) pairs
mapped_pairs = []
for line in toy_lines:
    for word in line.split():
        mapped_pairs.append((word, 1))

mapped_pairs
```

```python
# Shuffle step: group values by key
grouped = {}
for word, value in mapped_pairs:
    grouped.setdefault(word, []).append(value)

grouped
```

```python
# Reduce step: sum each group
reduced = {word: sum(values) for word, values in grouped.items()}
reduced
```

**Reflection:** Which stage required records from different input lines to meet
each other?

---

### Exercise 1.2: Suspicious Transactions by Hand

MapReduce also works on tabular data. In this tiny example, the key is
`account_id` instead of `word`.

```python
toy_suspicious_accounts = ["A102", "A105", "A102", "A102", "A110", "A105"]
[(account, 1) for account in toy_suspicious_accounts]
```

**Task:** Group these manually by account and compute the suspicious transaction
count for each one. Record the result in [`submission.md`](submission.md).

```python
toy_grouped = {}
for account in toy_suspicious_accounts:
    toy_grouped.setdefault(account, []).append(1)

toy_grouped
```

```python
toy_reduced = {account: sum(values) for account, values in toy_grouped.items()}
toy_reduced
```

---

## Phase 2: Distributed WordCount with PySpark

Now we move from manual reasoning to distributed execution.

### Exercise 2.1: Load the Text Evidence as an RDD

```python
lines_rdd = sc.textFile("data/incident_report.txt", minPartitions=4)

print("Number of partitions:", lines_rdd.getNumPartitions())
print("First 5 lines:")
for line in lines_rdd.take(5):
    print("-", line)
```

```python
show_partition_sizes(lines_rdd, "incident_report.txt")
```

**Question:** Are the lines distributed evenly across partitions? Record your
observation in [`submission.md`](submission.md).

---

### Exercise 2.2: Build the WordCount Pipeline

We will ignore common stop words and words shorter than 6 characters.

```python
stop_words = {
    "the", "and", "from", "with", "were", "into", "after", "during",
    "their", "there", "while", "under", "about", "again", "across",
    "a", "an", "of", "to", "in", "for", "on", "at", "by"
}
```

```python
# Step 1: Split each line into words
raw_words = lines_rdd.flatMap(lambda line: line.split())

# Step 2: Normalize each word
normalized_words = raw_words.map(normalize_word)

# Step 3: Filter out blanks, stop words, and short words
filtered_words = normalized_words.filter(
    lambda word: word and word not in stop_words and len(word) >= 6
)

filtered_words.take(20)
```

```python
# Step 4: Emit (word, 1) pairs
word_pairs = filtered_words.map(lambda word: (word, 1))

word_pairs.take(10)
```

```python
# Step 5: Reduce by key to count frequencies
word_counts = word_pairs.reduceByKey(lambda a, b: a + b)

top_10_words = word_counts.takeOrdered(10, key=lambda pair: -pair[1])
top_10_words
```

**Checkpoint:** Your result should be a list of `(word, count)` tuples ordered
from most frequent to least frequent.

---

### Exercise 2.3: Inspect the Post-Map Partitions

```python
show_partition_sizes(filtered_words, "filtered_words")
show_partition_sizes(word_pairs, "word_pairs")
```

Now inspect actual partition contents.

```python
word_pair_partitions = word_pairs.glom().collect()
for i, part in enumerate(word_pair_partitions):
    print(f"Partition {i}:")
    print(part[:10])
    print()
```

**Question:** Before reduction, do repeated keys such as `suspicious` or
`gateway` appear in multiple partitions? Why does that matter?

---

### Exercise 2.4: Where Does the Shuffle Happen?

Spark hides the physical network work from you, but you can still reason about
the boundary in the code.

**Question:** Which line below is the shuffle boundary?

```python
raw_words = lines_rdd.flatMap(lambda line: line.split())
normalized_words = raw_words.map(normalize_word)
filtered_words = normalized_words.filter(lambda word: word and word not in stop_words and len(word) >= 6)
word_pairs = filtered_words.map(lambda word: (word, 1))
word_counts = word_pairs.reduceByKey(lambda a, b: a + b)
```

Write your answer in [`submission.md`](submission.md) and explain why.

---

## Phase 3: Critical Incident - Transaction Analysis by Account

The text pipeline counted words by grouping on `word`. Now we apply the same
grouping logic to transaction data — but this time the key is `account_id`.

The core question is simple: **Which accounts have the most transactions, and
which moved the most money?**

### Exercise 3.1: Load the CSV with Spark

```python
tx = (spark.read
      .option("header", True)
      .option("inferSchema", True)
      .csv("data/transactions_small.csv"))

tx.printSchema()
tx.show(truncate=False)
```

```python
print("Row count:", tx.count())
print("Distinct accounts:", tx.select("account_id").distinct().count())
```

Take a moment to look at the schema and the data. Notice the columns:
`transaction_id`, `account_id`, `amount`, `transaction_type`, `hour`.

---

### Exercise 3.2: Aggregate by Account

This is the same MapReduce pattern you used for WordCount, applied to tabular
data. In WordCount the key was `word`; here the key is `account_id`.

```python
# Group by account_id and compute:
# - tx_count: how many transactions this account made
# - total_amount: total dollars moved by this account
# - max_amount: the single largest transaction
account_summary = (
    tx
    .groupBy("account_id")
    .agg(
        F.count("*").alias("tx_count"),
        F.sum("amount").alias("total_amount"),
        F.max("amount").alias("max_amount")
    )
    .orderBy(F.col("total_amount").desc())
)

account_summary.show(truncate=False)
```

**Question:** Which account moved the most total money? Which had the most
transactions? Are they the same account?

---

### Exercise 3.3: Inspect Partitions

Let us see how the transaction data is distributed across partitions before and
after the groupBy.

```python
# Before grouping: how is the raw data distributed?
show_partition_sizes(tx.rdd, "transactions (before groupBy)")
```

```python
# After grouping: how is the result distributed?
show_partition_sizes(account_summary.rdd, "account_summary (after groupBy)")
```

**Question:** Did the number of records per partition change after the groupBy?
Why does that make sense — what happened during the shuffle?

---

### Exercise 3.4: Present the Findings

Create a bar chart showing the top 5 accounts by total amount moved.

```python
top_5 = account_summary.limit(5).collect()

labels = [row["account_id"] for row in top_5]
totals = [row["total_amount"] for row in top_5]

plt.figure(figsize=(10, 5))
plt.bar(labels, totals, color="steelblue")
plt.title("Top 5 Accounts by Total Transaction Amount")
plt.xlabel("Account ID")
plt.ylabel("Total Amount ($)")
plt.tight_layout()
plt.savefig("data/top_accounts.png", dpi=150)
plt.show()
```

**Task:** In [`submission.md`](submission.md), identify which account stands out
and explain what the groupBy revealed.

---

## Phase 4: Optional Bonus

### Bonus A: Force a Skewed Example

Create an artificial RDD in which one key dominates almost everything, then
inspect the partition sizes.

```python
skewed = sc.parallelize(
    ["A999"] * 40 + ["A101", "A102", "A103", "A104"],
    4
)

show_partition_sizes(skewed, "skewed key RDD")
skewed.glom().collect()
```

**Question:** Why can a job still feel slow even when multiple partitions exist?

### Bonus B: Add a Risk Flag

Using `F.when().otherwise()`, add a column that flags transactions where
`amount > 10000` as `"HIGH"` and everything else as `"NORMAL"`. Then count how
many `HIGH` transactions each account has.

```python
# Your code here
```

---

## Wrap-Up

You have now:

1. Simulated MapReduce manually on a toy example
2. Built a distributed WordCount pipeline with PySpark RDDs
3. Loaded tabular data into a Spark DataFrame
4. Grouped transactions by account using the same MapReduce pattern
5. Inspected partition sizes before and after a shuffle

Before submitting:

- [ ] All analysis cells were run and interpreted
- [ ] Notebook runs from top to bottom without errors
- [ ] `data/top_accounts.png` was generated
- [ ] [`submission.md`](submission.md) is complete

```python
spark.stop()
print("Spark session stopped.")
```
