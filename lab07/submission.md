# Lab 07 Submission: The Needle in the Haystack

**Student Name:** [Your Name]
**Date:** [Date]

## Section A: Manual MapReduce

### Toy WordCount

#### Map Output
[Write the emitted `(word, 1)` pairs here]

#### Shuffle Groups
[Write the grouped keys and value lists here]

#### Reduce Output
[Write the final counts here]

### Toy Suspicious Transactions

#### Map Output
[Write the emitted `(account_id, 1)` pairs here]

#### Shuffle Groups
[Write the grouped keys and value lists here]

#### Reduce Output
[Write the suspicious transaction count per account here]

---

## Section B: Spark Setup and Partitions

- [ ] Spark session started successfully
- [ ] Verified default parallelism
- [ ] Checked partition count for the text RDD
- [ ] Inspected partition sizes with `glom()`

### Partition Observations

- Initial text partitions: ______
- Initial partition sizes: ______

---

## Section C: Distributed WordCount

### Top 10 Words

| Rank | Word | Count |
|------|------|-------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |
| 7 | | |
| 8 | | |
| 9 | | |
| 10 | | |

### Reflection

1. Which line of code caused the shuffle in your WordCount pipeline?
2. Before the shuffle, did repeated keys appear in multiple partitions? Why does
   that matter?

---

## Section D: Transaction Analysis by Account

- [ ] Loaded `transactions_small.csv` with Spark
- [ ] Grouped transactions by `account_id`
- [ ] Computed transaction count, total amount, and max amount per account

### Account Summary

| Account | Tx Count | Total Amount | Max Amount |
|---------|----------|--------------|------------|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

### Findings

1. Which account moved the most total money?
2. Which account had the most transactions?
3. Did the partition sizes change after the groupBy? Why?

---

## Section E: Visualization

- [ ] Generated `data/top_accounts.png`
- [ ] Chart shows the top 5 accounts by total amount
- [ ] Axes and title are clear

---

## Section F: Reflections

1. Why is the shuffle step usually more expensive than the map step?

2. What is data skew, and how could it hurt performance on a larger dataset?

---

## Section G: Bonus (if attempted)

### Data Skew Experiment
- [ ] Built an intentionally skewed key distribution
- [ ] Explained why one key can dominate runtime

### Risk Flag
- [ ] Added a `HIGH`/`NORMAL` flag using `F.when().otherwise()`
- [ ] Counted `HIGH` transactions per account

---

## Section H: AI Usage (if applicable)

### Tool Used
[Name of AI tool]

### Methodology
[How did you use it? What was your approach?]

### The Prompt
[Paste the prompt you used]

### The Output
[Summarize what the AI gave you]

### Human Value-Add
[What did you verify, correct, or improve?]
