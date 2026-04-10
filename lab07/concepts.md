# Lab 07 Field Manual: The Needle in the Haystack

**Distributed Thinking with MapReduce and PySpark**

This document is your technical reference for Lab 07. It explains what
MapReduce is, why distributed computation exists, how Spark organizes work into
partitions, and where the expensive part of the job usually happens.

The most important section is the toy example. You should be able to follow it
with pencil and paper. If you cannot manually simulate Map, Shuffle, and
Reduce, then PySpark will feel like a black box instead of a system you can
reason about.

---

## Setup

Run this cell first if you want the Mermaid diagrams in a notebook view.

```python
!pip install -q mermaid-py
```

```python
from mermaid import Mermaid
```

---

## Why MapReduce Exists

On a tiny dataset, one computer can read every record and do the whole job.
When the dataset becomes too large, that approach breaks down:

- One machine may not have enough memory
- One CPU core may take too long
- Reading everything sequentially may be too slow

MapReduce solves this by splitting the work into a pattern:

1. **Map** - Each worker processes its own local chunk of data and emits
   `(key, value)` pairs
2. **Shuffle** - The system regroups all identical keys together
3. **Reduce** - Each grouped key is aggregated into a final answer

```python
Mermaid("""
flowchart LR
    A["Input data<br/>split into chunks"] --> B["Map<br/>emit (key, value)"]
    B --> C["Shuffle<br/>group identical keys"]
    C --> D["Reduce<br/>combine grouped values"]
    D --> E["Final result"]

    style B fill:#e1f5ff
    style C fill:#ffe1e1
    style D fill:#90EE90
""")
```

---

## Bridge from pandas: You Already Know This Pattern

In Lab 06, you learned `groupby()` — the split-apply-combine pattern:

~~~python
# Lab 06 — pandas groupby
df.groupby('account_id')['amount'].sum()
~~~

That single line does three things:

1. **Split** the DataFrame into groups (one per `account_id`)
2. **Apply** the `sum()` function to each group
3. **Combine** the results into a new Series

MapReduce is exactly the same idea, but designed for data that is too large to
fit on one machine:

| Step | pandas (Lab 06) | MapReduce (Lab 07) |
|---|---|---|
| **Split** | `groupby('account_id')` | **Map** — each worker emits `(key, value)` pairs |
| **Regroup** | pandas handles this internally | **Shuffle** — the system moves all identical keys to the same place |
| **Combine** | `.sum()`, `.mean()`, `.count()` | **Reduce** — each grouped key is aggregated |

The biggest difference is that pandas does all of this on one machine in one
process. MapReduce does it across many machines (or simulated workers), so
the system must physically **move data** during the shuffle step. That data
movement is the expensive part that does not exist in pandas.

```python
Mermaid("""
flowchart LR
    subgraph "Lab 06 — pandas"
        A1["df.groupby('key')"] --> B1[".sum()"]
    end
    subgraph "Lab 07 — MapReduce"
        A2["Map<br/>emit (key, value)"] --> B2["Shuffle<br/>regroup by key"]
        B2 --> C2["Reduce<br/>combine values"]
    end

    style A1 fill:#90EE90
    style A2 fill:#e1f5ff
    style B2 fill:#ffe1e1
    style C2 fill:#90EE90
""")
```

If you understood `groupby()` in Lab 06, you already understand the *logic* of
MapReduce. The new part is understanding *where the data moves* when it cannot
all live on one machine.

---

## Toy Example 1: WordCount by Hand

Let us manually count words in three tiny lines:

```text
Line 1: alert login failed
Line 2: alert payment failed
Line 3: login succeeded alert
```

### Step 1: Map

Each mapper reads one line and emits `(word, 1)` for every word:

| Input | Mapper Output |
|---|---|
| `alert login failed` | `(alert, 1)`, `(login, 1)`, `(failed, 1)` |
| `alert payment failed` | `(alert, 1)`, `(payment, 1)`, `(failed, 1)` |
| `login succeeded alert` | `(login, 1)`, `(succeeded, 1)`, `(alert, 1)` |

If we put all emitted pairs together, we get:

```text
(alert,1) (login,1) (failed,1)
(alert,1) (payment,1) (failed,1)
(login,1) (succeeded,1) (alert,1)
```

### Step 2: Shuffle

The shuffle step groups identical keys together:

| Key | Grouped Values |
|---|---|
| `alert` | `[1, 1, 1]` |
| `login` | `[1, 1]` |
| `failed` | `[1, 1]` |
| `payment` | `[1]` |
| `succeeded` | `[1]` |

This is the part students often skip mentally. Do not skip it. The shuffle is
where the system must move data so that all `alert` pairs end up together, all
`login` pairs end up together, and so on.

### Step 3: Reduce

Now each reducer sums its grouped values:

| Key | Reduce Operation | Result |
|---|---|---|
| `alert` | `1 + 1 + 1` | `3` |
| `login` | `1 + 1` | `2` |
| `failed` | `1 + 1` | `2` |
| `payment` | `1` | `1` |
| `succeeded` | `1` | `1` |

Final answer:

```text
alert: 3
login: 2
failed: 2
payment: 1
succeeded: 1
```

### Visual Flow

```python
Mermaid("""
flowchart TD
    A["alert login failed"] --> A1["(alert,1) (login,1) (failed,1)"]
    B["alert payment failed"] --> B1["(alert,1) (payment,1) (failed,1)"]
    C["login succeeded alert"] --> C1["(login,1) (succeeded,1) (alert,1)"]

    A1 --> S["Shuffle by key"]
    B1 --> S
    C1 --> S

    S --> R1["alert -> [1,1,1] -> 3"]
    S --> R2["login -> [1,1] -> 2"]
    S --> R3["failed -> [1,1] -> 2"]
    S --> R4["payment -> [1] -> 1"]
    S --> R5["succeeded -> [1] -> 1"]

    style S fill:#ffe1e1
""")
```

---

## Toy Example 2: Suspicious Transactions by Account

MapReduce is not just for text. It works whenever you can define a key and a
combine rule.

Suppose we have these already-flagged suspicious transactions:

| Transaction | Account | Why suspicious? |
|---|---|---|
| T01 | A102 | amount > 10000 |
| T02 | A105 | off-hours |
| T03 | A102 | off-hours |
| T04 | A102 | amount > 10000 |
| T05 | A110 | amount > 10000 |
| T06 | A105 | amount > 10000 |

### Map

Emit `(account_id, 1)` for each suspicious transaction:

```text
(A102,1) (A105,1) (A102,1) (A102,1) (A110,1) (A105,1)
```

### Shuffle

Group by account:

```text
A102 -> [1, 1, 1]
A105 -> [1, 1]
A110 -> [1]
```

### Reduce

Sum each group:

```text
A102 -> 3 suspicious transactions
A105 -> 2 suspicious transactions
A110 -> 1 suspicious transaction
```

This is exactly the same pattern as WordCount. Only the key changed:

- WordCount key: `word`
- Risk-analysis key: `account_id`

---

## Spark: A Distributed Engine for MapReduce-Like Work

PySpark lets you express these patterns across many partitions.

### `local[4]` - A Simulated Cluster

When you create a session like this:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[4]") \
    .appName("COMP3084_Lab07") \
    .getOrCreate()
```

you are not using four separate computers. You are asking Spark to simulate
four worker threads on one machine. That is enough to practice partitioning,
shuffling, and distributed reasoning.

### Driver vs Workers

```python
Mermaid("""
flowchart LR
    D["Driver program<br/>your notebook"] --> W1["Worker / partition 1"]
    D --> W2["Worker / partition 2"]
    D --> W3["Worker / partition 3"]
    D --> W4["Worker / partition 4"]

    style D fill:#ffe1e1
    style W1 fill:#e1f5ff
    style W2 fill:#e1f5ff
    style W3 fill:#e1f5ff
    style W4 fill:#e1f5ff
""")
```

- **Driver**: builds the plan and asks for results
- **Workers**: execute tasks on partitions

---

## Partitions: The Real Unit of Work

Spark does not usually think "one file, one job." It thinks "many partitions,
many tasks."

If an RDD has 4 partitions, then up to 4 tasks can run at once in `local[4]`
mode.

```python
rdd = spark.sparkContext.parallelize(range(20), 4)
print(rdd.getNumPartitions())  # 4
print(rdd.glom().collect())    # show each partition's local data
```

`glom()` is useful because it lets you inspect which records landed in each
partition.

---

## RDDs vs DataFrames

Spark offers two main data structures. Both represent distributed collections
of data split across partitions, but they differ in how much structure they
expose.

### RDD — Resilient Distributed Dataset

An **RDD** is a distributed list. Each element can be anything: a string, a
number, a tuple, a dictionary. There is no schema — Spark does not know what
is inside each element until your code looks at it.

Think of it as a **Python list that has been split across multiple workers**.
Each worker holds a chunk (partition), and operations like `map()` and
`filter()` run independently on each chunk.

```python
# A Python list — everything on one machine
words = ["alert", "login", "failed", "alert"]

# An RDD — the same data, but distributed across partitions
rdd = spark.sparkContext.parallelize(["alert", "login", "failed", "alert"], 2)
# Partition 0: ["alert", "login"]
# Partition 1: ["failed", "alert"]
```

The key differences from a regular Python list:

| Python list | RDD |
|---|---|
| Lives in one process | Split across partitions (workers) |
| Operations execute immediately | Operations are lazy (build a plan) |
| You write `for` loops | You write `map()`, `filter()`, `reduce()` |
| Limited by one machine's memory | Can scale across a cluster |

### Spark DataFrame — A Distributed Table

A **Spark DataFrame** is the distributed version of the pandas DataFrame you
used in Lab 06. It is a table with named columns, where each column has a
specific type (string, integer, float, etc.).

```python
# Lab 06 — pandas DataFrame (one machine)
import pandas as pd
pdf = pd.read_csv("data/transactions_small.csv")

# Lab 07 — Spark DataFrame (distributed across partitions)
sdf = spark.read.option("header", True).option("inferSchema", True) \
           .csv("data/transactions_small.csv")
```

Both give you a table with rows and columns. The difference is that the Spark
DataFrame is split across partitions, so operations like `groupBy()` may
trigger a shuffle.

| pandas DataFrame (Lab 06) | Spark DataFrame (Lab 07) |
|---|---|
| Lives in one process's memory | Split across partitions |
| `df.groupby('col').sum()` | `df.groupBy('col').agg(F.sum('col'))` |
| Operations execute immediately | Operations are lazy |
| Great for data that fits in memory | Designed for data too large for one machine |
| Columns accessed with `df['col']` | Columns accessed with `df['col']` or `F.col('col')` |

### When to Use Which

| Structure | Best for in this lab | Why |
|---|---|---|
| **RDD** | Classic WordCount | Feels close to pure MapReduce; you control every `(key, value)` pair |
| **DataFrame** | Transaction analysis by account | Schema-aware, tabular, SQL-like aggregation — same mental model as pandas |

In general, prefer DataFrames when your data is tabular (rows and columns) and
RDDs when your data is unstructured (raw text, arbitrary objects).

---

## Quick Refresher: Lambda Functions

Every RDD operation in this lab uses **lambda functions** — small, anonymous
functions written in one line. If you are still getting comfortable with them,
here is the pattern:

```python
# A regular function
def double(x):
    return x * 2

# The same thing as a lambda
double = lambda x: x * 2

# Both work the same way
print(double(5))  # 10
```

The syntax is: `lambda arguments: expression`. There is no `return` keyword —
the expression *is* the return value. You will see three forms in this lab:

| Lambda | What It Does |
|---|---|
| `lambda line: line.split()` | Takes one string, returns a list of words |
| `lambda word: (word, 1)` | Takes one word, returns a `(key, value)` tuple |
| `lambda a, b: a + b` | Takes two numbers, returns their sum |

Lambdas are just a compact way to pass a small function to `map()`, `filter()`,
or `reduceByKey()` without having to define and name a separate function.

---

## Spark in Action: Code Examples

### RDD Example — WordCount Pipeline

```python
lines = spark.sparkContext.textFile("data/incident_report.txt")
counts = (lines
          .flatMap(lambda line: line.split())
          .map(lambda word: (word, 1))
          .reduceByKey(lambda a, b: a + b))
```

Here is what each line does:

| Line | What It Does |
|---|---|
| `textFile(...)` | Reads the file and creates one element per line |
| `.flatMap(lambda line: line.split())` | Splits each line into words and **flattens** them into one big list |
| `.map(lambda word: (word, 1))` | Wraps each word into a `(key, value)` pair |
| `.reduceByKey(lambda a, b: a + b)` | Groups identical keys and sums their values (the shuffle happens here) |

### `flatMap` vs `map` — The Key Difference

This is a common point of confusion. Both apply a function to every element,
but they differ in how they handle the output:

- **`map`** produces exactly **one output per input**.
- **`flatMap`** produces **zero or more outputs per input**, then flattens
  them into a single list.

~~~python
# Suppose our RDD contains two lines:
lines = ["alert login", "payment failed"]

# map: one input → one output (a list inside a list)
lines.map(lambda line: line.split())
# Result: [["alert", "login"], ["payment", "failed"]]
#          ↑ nested — two lists of two words each

# flatMap: one input → many outputs, flattened
lines.flatMap(lambda line: line.split())
# Result: ["alert", "login", "payment", "failed"]
#          ↑ flat — four individual words
~~~

We need `flatMap` here because `split()` produces multiple words from one line,
and we want all the words in a single flat sequence — not a list of lists.

### DataFrame Example — Transaction Aggregation

```python
from pyspark.sql import functions as F

df = spark.read.option("header", True).option("inferSchema", True).csv("data/transactions_small.csv")
summary = (df.groupBy("account_id")
             .agg(F.count("*").alias("tx_count"),
                  F.sum("amount").alias("total_amount")))
```

| Line | What It Does | pandas Equivalent |
|---|---|---|
| `spark.read.option(...).csv(...)` | Reads CSV into a Spark DataFrame | `pd.read_csv(...)` |
| `.groupBy("account_id")` | Groups rows by account | `df.groupby('account_id')` |
| `F.count("*").alias("tx_count")` | Counts rows per group, names the column | `('tx_id', 'count')` in `.agg()` |
| `F.sum("amount").alias("total_amount")` | Sums amounts per group, names the column | `('amount', 'sum')` in `.agg()` |

Notice how similar this is to the pandas `groupby().agg()` pattern from Lab 06.
The main difference is syntax: Spark uses `F.count()`, `F.sum()` instead of
string-based aggregation names.

---

## Lazy Evaluation: Spark Builds a Plan First

Most Spark operations are **lazy**:

- `map()`
- `filter()`
- `flatMap()`
- `select()`
- `groupBy()`

They describe what should happen, but do not immediately execute it.

Work begins when you call an **action**:

- `collect()`
- `count()`
- `take()`
- `show()`

Think of transformations as building a recipe and actions as actually cooking
the meal.

### What This Looks Like in Practice

```python
rdd = spark.sparkContext.parallelize(["alert login", "payment failed"])

# This does NOT execute anything — it just builds a plan
mapped = rdd.flatMap(lambda line: line.split())
print(mapped)
# Output: PythonRDD[1] at RDD at PythonRDD.scala:53
# ↑ Not your words! Just a description of the plan.

# This EXECUTES the plan and returns actual data
print(mapped.collect())
# Output: ['alert', 'login', 'payment', 'failed']
# ↑ Now the work actually happened.
```

If you call `print()` on a transformation and see an object description instead
of your data, that is normal — Spark has not run the computation yet. Call an
action like `collect()` to trigger it.

---

## Shuffle: The Expensive Part

The shuffle is the step where data must move so identical keys meet each other.
That is why it is usually the most expensive stage.

### Why Shuffle Is Expensive — A Concrete Example

Imagine your text is split across two partitions:

```text
Partition 0: "alert login failed"
Partition 1: "login succeeded alert"
```

After the **map** step, each partition has its own local pairs:

```text
Partition 0: (alert,1) (login,1) (failed,1)
Partition 1: (login,1) (succeeded,1) (alert,1)
```

Notice that `alert` appears in **both** partitions. So does `login`. To add
them up, the system must **move data across partitions** so that all `alert`
pairs end up together and all `login` pairs end up together:

```python
Mermaid("""
flowchart TD
    subgraph "Before Shuffle"
        P0["Partition 0<br/>(alert,1) (login,1) (failed,1)"]
        P1["Partition 1<br/>(login,1) (succeeded,1) (alert,1)"]
    end

    P0 -->|"alert,1 moves"| R0["Reducer for alert<br/>[1, 1] → 2"]
    P0 -->|"login,1 moves"| R1["Reducer for login<br/>[1, 1] → 2"]
    P0 -->|"failed,1 stays"| R2["Reducer for failed<br/>[1] → 1"]
    P1 -->|"alert,1 moves"| R0
    P1 -->|"login,1 moves"| R1
    P1 -->|"succeeded,1 stays"| R3["Reducer for succeeded<br/>[1] → 1"]

    style P0 fill:#e1f5ff
    style P1 fill:#e1f5ff
    style R0 fill:#ffe1e1
    style R1 fill:#ffe1e1
    style R2 fill:#90EE90
    style R3 fill:#90EE90
""")
```

In pandas on one machine, this regrouping is just an internal rearrangement in
memory. In a distributed system, it means **sending data over the network**
between machines. That is why shuffle-heavy jobs are slow.

### Operations That Cause a Shuffle

- `reduceByKey()`
- `groupByKey()`
- `groupBy()`
- joins
- some sorts

The map stage can often run independently inside each partition. The shuffle
requires coordination across partitions.

### `reduceByKey` vs `groupByKey` — Why It Matters

Both `reduceByKey` and `groupByKey` group data by key and cause a shuffle, but
they move very different amounts of data.

**`groupByKey`** collects *all* values for each key into a list, then sends
them across the network. It does no combining before the shuffle:

```text
Partition 0: (alert,1) (alert,1) (login,1)
Partition 1: (alert,1) (login,1)

   ──── shuffle all 5 pairs ────>

alert → [1, 1, 1]  then sum → 3
login → [1, 1]     then sum → 2
```

**`reduceByKey`** combines values *locally within each partition first*, then
shuffles only the partial results:

```text
Partition 0: (alert,1) (alert,1) (login,1)
   local combine → (alert,2) (login,1)        ← only 2 pairs to send

Partition 1: (alert,1) (login,1)
   local combine → (alert,1) (login,1)        ← only 2 pairs to send

   ──── shuffle 4 pairs instead of 5 ────>

alert → 2 + 1 = 3
login → 1 + 1 = 2
```

On this toy example the difference is small. On a real dataset with millions of
records, `reduceByKey` can move dramatically less data across the network
because it pre-aggregates inside each partition before shuffling.

**Rule of thumb:** If your reduce operation is associative and commutative
(like addition, max, or min), always prefer `reduceByKey` over `groupByKey`.

---

## Data Skew

What if one key dominates the data?

Example:

```text
A999 -> 90% of all suspicious transactions
all other accounts -> remaining 10%
```

Even if you have 4 partitions, one partition may end up doing most of the work
for `A999`. That imbalance is called **data skew**.

Symptoms:

- One task runs much longer than the others
- The cluster appears underutilized
- A "distributed" job still feels slow

This is why inspecting partition balance matters.

---

## Bonus Reference: Adding Conditional Columns

This section covers `withColumn` and `F.when().otherwise()`. These are **not
required for the main lab exercises** — they are used in Bonus B. If you are
not attempting the bonus, you can skip this section.

In Lab 06, you created new columns and applied conditions like this:

~~~python
# Lab 06 — pandas: conditional column
import numpy as np
df['size'] = np.where(df['poblacion'] > 50000, 'Large', 'Small')
~~~

In Spark, you cannot assign to a column with `=` because the DataFrame is
distributed. Instead, you use `.withColumn()` to produce a new DataFrame with
the column added:

~~~python
# Spark: conditional column with F.when().otherwise()
df = df.withColumn(
    "size",
    F.when(F.col("poblacion") > 50000, "Large")
     .otherwise("Small")
)
~~~

| Spark Syntax | What It Does | pandas Equivalent |
|---|---|---|
| `F.col("amount")` | Refers to a column by name | `df['amount']` |
| `df.withColumn("new", expr)` | Returns a new DataFrame with the column added | `df['new'] = expr` |
| `F.when(condition, value)` | If condition is true, use this value | `np.where(condition, value, ...)` |
| `.otherwise(value)` | If no `when` matched, use this fallback | The third argument of `np.where` |

---

## Quick Reference Summary

| Concept | Key Point |
|---------|-----------|
| **MapReduce** | Split work into Map (emit key-value pairs), Shuffle (regroup by key), Reduce (aggregate) |
| **Map** | Each worker processes its local chunk and emits `(key, value)` pairs |
| **Shuffle** | The system moves data so all identical keys end up together — the expensive step |
| **Reduce** | Each grouped key is aggregated into a final answer (sum, count, etc.) |
| **SparkSession** | Entry point to Spark; `local[4]` simulates 4 worker threads |
| **RDD** | Resilient Distributed Dataset — a distributed Python list with no schema |
| **Spark DataFrame** | A distributed table with named, typed columns — like a pandas DataFrame split across partitions |
| **Partition** | A chunk of data that one worker processes; more partitions = more parallelism |
| **Lazy evaluation** | Transformations build a plan; actions execute it |
| **Transformation** | `map()`, `flatMap()`, `filter()`, `select()`, `groupBy()` — does not execute |
| **Action** | `collect()`, `count()`, `take()`, `show()` — triggers execution |
| **`flatMap`** | Like `map`, but flattens the output — one input can produce many outputs |
| **`reduceByKey`** | Groups identical keys and combines their values (triggers a shuffle) |
| **`groupByKey`** | Collects all values per key into a list — shuffles more data than `reduceByKey` |
| **`reduceByKey` vs `groupByKey`** | `reduceByKey` pre-aggregates locally before shuffling; always prefer it for sum/max/min |
| **`glom()`** | Inspect which records landed in each partition |
| **`withColumn`** | Returns a new DataFrame with a column added — Spark equivalent of `df['col'] = ...` |
| **`F.when().otherwise()`** | Conditional column values — Spark equivalent of `np.where()` |
| **`F.col()`** | Refers to a column by name inside Spark expressions |
| **Lambda function** | `lambda x: expr` — a compact anonymous function passed to `map()`, `filter()`, etc. |
| **Data skew** | When one key dominates, one partition does most of the work |

### Key Method Quick Reference

| Method | Purpose | pandas Equivalent |
|--------|---------|-------------------|
| `spark.sparkContext.parallelize(data, n)` | Create an RDD from a Python list with n partitions | — |
| `spark.sparkContext.textFile(path)` | Read a text file as an RDD (one element per line) | — |
| `spark.read.csv(path)` | Read a CSV into a Spark DataFrame | `pd.read_csv(path)` |
| `rdd.map(func)` | Apply func to each element, one output per input | `series.apply(func)` |
| `rdd.flatMap(func)` | Apply func, flatten results into one list | — |
| `rdd.filter(func)` | Keep elements where func returns True | `df[mask]` |
| `rdd.reduceByKey(func)` | Group by key, combine values with func | `df.groupby(key).sum()` |
| `rdd.collect()` | Return all elements to the driver as a Python list | `df.values.tolist()` |
| `rdd.take(n)` | Return first n elements | `df.head(n)` |
| `rdd.count()` | Count elements | `len(df)` |
| `rdd.getNumPartitions()` | How many partitions the RDD has | — |
| `rdd.glom().collect()` | Show each partition's contents | — |
| `rdd.groupByKey()` | Group by key, collect all values into a list (less efficient) | `df.groupby(key).agg(list)` |
| `df.groupBy(col)` | Group Spark DataFrame rows by column | `df.groupby(col)` |
| `df.agg(F.sum(col))` | Aggregate with Spark SQL functions | `df.agg({'col': 'sum'})` |
| `df.withColumn(name, expr)` | Add or replace a column | `df['name'] = expr` |
| `F.when(cond, val).otherwise(val)` | Conditional column value | `np.where(cond, val, val)` |
| `F.col("name")` | Reference a column by name | `df['name']` |
| `df.printSchema()` | Show column names and types | `df.dtypes` |
| `df.show()` | Print the first 20 rows | `print(df.head(20))` |
| `df.repartition(n)` | Redistribute data into n partitions | — |

---

## Practical Questions You Should Be Able to Answer

By the end of the lab, you should be able to answer:

1. What key did my mapper emit?
2. Which operation caused the shuffle?
3. Why did Spark need to move data at that point?
4. How many partitions did I use?
5. Were the partitions balanced or skewed?
6. Why is `reduceByKey()` usually better than manually collecting everything to
   Python and aggregating there?

If you can answer those clearly, you are thinking like the cluster instead of
just calling cluster-shaped functions.
