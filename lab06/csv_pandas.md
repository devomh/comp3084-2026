---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.4
  kernelspec:
    display_name: Python 3
    name: python3
---

<!-- #region -->
# CSV Files and pandas

## What is a CSV file?

**CSV** stands for **Comma-Separated Values**. It is one of the simplest and
most widely used formats for storing and exchanging tabular data (data organized
in rows and columns).

A CSV file is just a **plain text file** where:

- The **first line** (header) contains the column names, separated by commas
- Each **subsequent line** is a row of data, with values separated by commas
- Each row has the **same number of fields** as the header

Example:
```
municipio,region,poblacion
San Juan,Metro,318441
Ponce,Sur,126327
```

**Why CSV is everywhere:**

- It is **human-readable** — you can open it in any text editor
- It is **universal** — every spreadsheet program (Excel, Google Sheets),
  database, and programming language can read and write CSV
- It is **lightweight** — no special formatting, no binary encoding, just text
- It is the **default export format** for open data portals, government
  datasets, scientific data, and APIs worldwide

**Limitations:**

- No data types — everything is stored as text (the reader must convert numbers)
- No standard for special characters (commas inside values, line breaks, encoding)
- No metadata — column types, units, or descriptions must be documented separately
<!-- #endregion -->

<!-- #region -->
# Part 1: Exploring a CSV file manually

Before using any library, let's understand CSV files by parsing one with pure
Python. This builds intuition for what tools like pandas do automatically.

We will work with `municipios_stats.csv`, a dataset of Puerto Rico's 78
municipalities.
<!-- #endregion -->

```python
# Step 1: Read the file
# Use open() with mode 'r' to read the file 'municipios_stats.csv'
# Store the entire file content in a variable called `content`
# Hint: use the `with` statement and f.read()

```

```python
# Step 2: Explore the raw content
# Display the content variable to see what the raw CSV text looks like
# Notice: it is one long string with \n (newline) characters separating rows

```

```python
# Step 3: Split into lines
# Convert the content string into a list of lines using .split('\n')
# Store the result in a variable called `lines`
# Print how many lines there are using len()

```

```python
# Step 4: Separate the header from the data
# The first line (lines[0]) contains the column names — store it in `columns`
# Display `columns` to see the header row
# Hint: what separator does CSV use between column names?

```

```python
# Step 5: Extract the data rows
# All lines after the first are data rows — store them in `data` (lines[1:])
# Use a for loop to print each data line
# Notice how each line follows the same structure as the header

```

```python
# Step 6: Extract a single column
# Extract the municipio names (first field of each line) into a list
# Steps:
#   1. Create an empty list called `municipios`
#   2. Loop through each line in `data`
#   3. Skip empty lines (if line == '')
#   4. Split the line by comma and take the first element [0]
#   5. Append it to the list
# Print the resulting list

```

```python
# Step 7: Generalize — write a function
# Convert your previous code into a reusable function:
#   def get_column(data, col):
# Parameters:
#   data: list of data lines (strings)
#   col: column position (integer, 0-based)
# Returns: a list of values (strings) from that column
# Remember to skip empty lines

```

```python
# Step 8: Test your function
# Use get_column to extract the municipio column (position 0)
# Print the result — it should match your earlier list

```

```python
# Step 9: Compute a column total
# Use get_column to extract the poblacion column (position 2)
# Problem: the values come back as strings — convert them to integers
# Hint: use a list comprehension [int(p) for p in poblacion]
# Then use an accumulator (total = 0, loop and add) to compute the sum
# Print the total population of all municipalities

```

```python
# Step 10: Count by category
# Use get_column to extract the region column (position 1)
# Count how many municipalities belong to each region using a dictionary:
#   1. Create an empty dictionary `conteo`
#   2. Loop through the region values
#   3. For each region, increment its count: conteo[r] = conteo.get(r, 0) + 1
# Print the dictionary
# Bonus: print each region and its count on a separate line

```

```python
# Step 11: List unique regions
# From the region column, print each unique region name (no repetitions)
# Hint: you can use a set, or track the "current" region and only print
# when it changes (the data is grouped by region in the CSV)

```

<!-- #region -->
# Part 2: pandas — From manual work to one-liners

In Part 1, you wrote loops, split strings, converted types, and built
accumulators by hand. This is valuable for understanding the CSV format, but
it is slow, error-prone, and does not scale.

**pandas** is Python's most important library for data analysis. It provides
the **DataFrame** — a table structure where:

- Each **column** has a name and its own data type (text, integer, float)
- Each **row** has an index (label) for fast lookups
- Built-in methods replace manual loops: loading, filtering, sorting, grouping,
  and plotting all happen in one line

Think of a DataFrame as an **upgraded dictionary of lists**, where every list
(column) is the same length, and pandas keeps them aligned by row.

**Key idea:** A DataFrame is *heterogeneous* — unlike NumPy arrays where every
element must be the same type, each column in a DataFrame can have a different
type (strings, integers, floats, categories).

**Import convention:**

```python
import pandas as pd
```
<!-- #endregion -->

```python
# Step 1: Import pandas
# Import the pandas library with the standard alias `pd`

```

```python
# Step 2: Load the CSV into a DataFrame
# Use pd.read_csv() to load 'municipios_stats.csv' into a variable called `df`
# pandas automatically:
#   - Parses the header row into column names
#   - Detects data types (strings, integers, floats)
#   - Assigns a numeric index (0, 1, 2, ...) to each row
# Display df to see the table

```

```python
# Step 3: Inspect the shape
# Print df.shape — this returns a tuple (rows, columns)
# How many municipalities are in the dataset?
# How many columns (variables) does each municipality have?

```

```python
# Step 4: Check column names and types
# Print df.columns to see all column names
# Print df.dtypes to see the data type of each column
# Notice: pandas detected which columns are text (object),
#         which are integers (int64), and which are floats (float64)
# Compare this to Part 1 where everything was a string!

```

```python
# Step 5: Get a compact summary with .info()
# Call df.info() — this prints column names, non-null counts,
# data types, and memory usage in one output
# This is the first thing you should run on any new dataset

```

```python
# Step 6: Statistical summary with .describe()
# Call df.describe() — this returns count, mean, std, min,
# 25%, 50% (median), 75%, max for all numeric columns
# Question: What is the median population? Which column has the highest std?

```

```python
# Step 7: Preview rows
# Use df.head() to see the first 5 rows
# Use df.tail() to see the last 5 rows
# You can pass a number: df.head(10) for the first 10

```

<!-- #region -->
## Replicating the manual work with pandas

Now let's redo everything from Part 1 — but using pandas. Notice how each
manual operation becomes a single expression.
<!-- #endregion -->

```python
# Step 8: Extract a single column (replaces Step 6 from Part 1)
# Select the 'municipio' column: df['municipio']
# This returns a Series (a labeled 1D array — like a list with an index)
# Print its type with type() and its shape with .shape
# Compare: in Part 1 you wrote a loop + split + append. Here it's one expression.

```

```python
# Step 9: Compute a column total (replaces Step 9 from Part 1)
# Select the 'poblacion' column and call .sum() on it
# No type conversion needed — pandas already knows it's int64
# Print the total
# Compare: in Part 1 you converted strings to int, then used an accumulator loop

```

```python
# Step 10: Count by category (replaces Step 10 from Part 1)
# Use df['region'].value_counts() to count municipalities per region
# This returns a Series with regions as the index and counts as values
# Compare: in Part 1 you wrote a loop with dict.get()

```

```python
# Step 11: List unique values (replaces Step 11 from Part 1)
# Use df['region'].unique() to get an array of unique region names
# Or use df['region'].nunique() to get just the count
# Compare: in Part 1 you tracked changes manually or used a set

```

<!-- #region -->
## Going further: things pandas makes easy

The following operations would be very difficult with manual CSV parsing but
are straightforward with pandas.
<!-- #endregion -->

```python
# Step 12: Filter rows with a condition (Boolean filtering)
# Find all municipalities with population greater than 50,000
# Create a boolean mask: mask = df['poblacion'] > 50000
# Apply it: df[mask] — this returns only rows where the condition is True
# Print how many municipalities match using len()
# Hint: this is the same boolean indexing pattern from NumPy (Lab 04)

```

```python
# Step 13: Sort the data
# Sort all municipalities by population in descending order
# Use df.sort_values('poblacion', ascending=False)
# Display the top 10 using .head(10)
# Which municipality has the largest population? The smallest?

```

```python
# Step 14: Group and aggregate
# Compute the total population per region using:
#   df.groupby('region')['poblacion'].sum()
# This splits the data by region, sums population within each group,
# and combines the results into a new Series
# Which region has the highest total population?

```

```python
# Step 15: Multiple aggregations
# Use .agg() to compute multiple statistics per region in one call:
#   df.groupby('region')['poblacion'].agg(['sum', 'mean', 'count'])
# This returns a DataFrame with sum, mean, and count as columns
# Which region has the most municipalities? The highest average population?

```

<!-- #region -->
## Reflection: What did we gain? What did we lose?

Take a moment to compare both approaches:

| | Manual (Part 1) | pandas (Part 2) |
|---|---|---|
| **Loading** | `open()` + `.read()` + `.split('\n')` | `pd.read_csv()` |
| **Type handling** | Everything is a string — you convert manually | Automatic detection (int64, float64, object) |
| **Column access** | `.split(',')[i]` on every line | `df['column_name']` |
| **Aggregation** | Loops + accumulators + dictionaries | `.sum()`, `.mean()`, `.value_counts()` |
| **Filtering** | Manual if/continue logic | Boolean masks in one expression |
| **Grouping** | Nested loops + dictionary bookkeeping | `.groupby()` in one line |

**What we gained with pandas:**
- Speed of writing: operations that took 5-10 lines become one expression
- Safety: no manual type conversion, no off-by-one errors on column indices
- Expressiveness: code reads like a description of what you want, not how to do it

**What we lost:**
- Transparency: pandas hides the mechanics — if something goes wrong, debugging
  requires understanding what happens inside `.read_csv()` or `.groupby()`
- Control: pandas makes decisions for you (type inference, index assignment,
  missing value handling) that may not always be what you expect

**The takeaway:** Part 1 was not wasted effort. Understanding the manual process
is what lets you reason about what pandas does under the hood — and diagnose
problems when the automatic approach breaks down.
<!-- #endregion -->
