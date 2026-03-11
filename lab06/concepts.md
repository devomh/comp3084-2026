# Lab 06 Field Manual: The Data Lake

**Tabular Data Processing & Analysis**

This document is your technical reference for Lab 06. It covers the foundational
concepts you will need to understand before and during the lab exercises: how
tabular data differs from homogeneous arrays, how pandas DataFrames work
internally, and how every pandas operation maps to a **NumPy operation** you
already know from Labs 04-05.

Throughout this guide, we will use **Puerto Rico municipal data** as our
building blocks. Instead of abstract examples, you will work with real
municipality names, populations, and regions — all using the same vectorized
thinking from your previous labs.

---

## Setup

Run this cell first. Every code cell in this document depends on these imports.

```python
!pip install -q mermaid-py
```

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mermaid import Mermaid
```

---

## From Arrays to Tables

### The NumPy Limitation

In Labs 04-05, you worked with NumPy arrays. These are powerful but have one
critical limitation: **every element must be the same type**.

```python
# NumPy: all elements must be the same dtype
arr = np.array([["San Juan", 318441, 123.9],
                ["Ponce",    126327, 297.8]])
print(arr.dtype)  # <U32 — everything became a string!
print(arr)
```

NumPy coerced the numbers into strings to maintain a uniform dtype. You
cannot do math on the "numbers" because they are actually text:

```python
# This does NOT work as expected
try:
    print(arr[:, 1].sum())  # Error or wrong result — these are strings!
except TypeError as e:
    print(f"Error: {e}")
```

### The pandas Solution

A pandas DataFrame solves this by storing **each column independently**, with
its own dtype:

```python
df = pd.DataFrame({
    'municipio': ['San Juan', 'Ponce'],
    'poblacion': [318441, 126327],
    'area_km2':  [123.9, 297.8]
})
print(df.dtypes)
print(df)
```

```
municipio     object   (text)
poblacion      int64   (integer)
area_km2     float64   (decimal)
```

Each column is a separate NumPy array with its own type. The DataFrame is a
**container** that keeps them aligned by row index.

### The Bridge: NumPy to pandas

```python
Mermaid("""
flowchart LR
    A["NumPy ndarray<br/>(homogeneous)"] -->|"one dtype for all"| B["Every element<br/>same type"]
    C["pandas DataFrame<br/>(heterogeneous)"] -->|"one dtype per column"| D["Each column<br/>has its own type"]
    A -.->|"evolution"| C

    style A fill:#e1f5ff
    style C fill:#90EE90
""")
```

Every pandas operation has a NumPy equivalent you already know:

| pandas Operation | NumPy Parallel | What's New |
|---|---|---|
| `df['col']` (column select) | `arr[:, i]` (column slice) | Columns have **names**, not just indices |
| `df.loc[mask]` (boolean filter) | `arr[mask]` (boolean indexing) | Filter by **conditions on any column** |
| `df.sort_values('col')` | `arr[np.argsort(arr[:, i])]` | Sort by named column, stable |
| `df.groupby('col').sum()` | Manual loop + accumulation | Automatic split-apply-combine |
| `df.dtypes` | `arr.dtype` (single type) | **Each column has its own type** |
| `df.set_index('col')` | — | Row labels become meaningful |

---

## What Is a DataFrame?

### Internal Structure

A DataFrame is essentially a **dictionary of Series** (columns), where each
Series is a labeled 1D array:

```python
Mermaid("""
block-beta
    columns 4
    A["municipio<br/>(object)"] B["region<br/>(object)"] C["poblacion<br/>(int64)"] D["area_km2<br/>(float64)"]
    E["San Juan"] F["Metro"] G["318441"] H["123.9"]
    I["Ponce"] J["Sur"] K["126327"] L["297.8"]
    M["Humacao"] N["Este"] O["50653"] P["114.9"]
    Q["DataFrame: dict of Series, each with its own dtype"]:4

    style A fill:#ffe1e1
    style B fill:#ffe1e1
    style C fill:#e1f5ff
    style D fill:#e1f5ff
""")
```

### Key Properties

```python
df = pd.read_csv('data/municipios_stats.csv')

print(f"Shape: {df.shape}")           # (rows, columns) — same as NumPy!
print(f"Columns: {list(df.columns)}") # Column names (Index object)
print(f"Index: {df.index}")           # Row labels (default: 0, 1, 2, ...)
print(f"\nDtypes:\n{df.dtypes}")      # Each column's type
```

### .info() — The One-Stop Summary

```python
df.info()
```

This shows column names, non-null counts, dtypes, and memory usage in one
compact output. It is the first thing you should run on any new dataset.

### .describe() — Statistical Summary

```python
df.describe()
```

Returns count, mean, std, min, 25%, 50% (median), 75%, max for all numeric
columns. Non-numeric columns are excluded.

---

## Series vs DataFrame

This is the most important distinction to internalize.

### Series: A Single Column (1D)

A Series is a labeled 1D array — like a NumPy array with an index:

```python
pop = df['poblacion']        # Single brackets → Series
print(type(pop))             # <class 'pandas.core.series.Series'>
print(pop.shape)             # (78,)
print(pop.dtype)             # int64
```

**NumPy equivalent:** `arr[:, i]` — selecting one column from a 2D array.

### DataFrame: Multiple Columns (2D)

Double brackets return a DataFrame (a subset of columns):

```python
subset = df[['municipio', 'poblacion']]  # Double brackets → DataFrame
print(type(subset))                       # <class 'pandas.core.frame.DataFrame'>
print(subset.shape)                       # (78, 2)
```

**NumPy equivalent:** `arr[:, [i, j]]` — selecting multiple columns.

### Visual Comparison

```python
Mermaid("""
flowchart LR
    A["df['poblacion']"] -->|"Single brackets"| B["Series<br/>shape (78,)<br/>1D"]
    C["df[['municipio', 'poblacion']]"] -->|"Double brackets"| D["DataFrame<br/>shape (78, 2)<br/>2D"]

    style B fill:#e1f5ff
    style D fill:#90EE90
""")
```

### Quick Rule

| Syntax | Returns | Analogous To |
|--------|---------|--------------|
| `df['col']` | Series | `arr[:, i]` |
| `df[['a', 'b']]` | DataFrame | `arr[:, [i, j]]` |
| `df.col` | Series | `arr[:, i]` (attribute access) |

---

## Row Selection: loc vs iloc

pandas provides two main accessors for selecting rows and columns:

### .loc — Label-Based (like a dictionary)

```python
df.loc[0, 'municipio']                     # Single cell by label
df.loc[0:4, ['municipio', 'poblacion']]    # Rows 0-4, specific columns
df.loc[mask, 'poblacion']                  # Filtered rows, one column
```

**Important:** `.loc` slicing is **inclusive** on both ends. `df.loc[0:4]`
returns rows 0, 1, 2, 3, **and 4** (5 rows).

### .iloc — Position-Based (like NumPy)

```python
df.iloc[0, 0]           # First row, first column (by position)
df.iloc[:5, :3]         # First 5 rows, first 3 columns
df.iloc[-1]             # Last row
```

**Important:** `.iloc` slicing is **exclusive** on the end, just like NumPy
and Python. `df.iloc[0:4]` returns rows 0, 1, 2, **3** (4 rows).

### Comparison

```python
Mermaid("""
flowchart TD
    A["Need to select rows/columns?"]
    A -->|"By name or label"| B[".loc[row_label, col_name]"]
    A -->|"By position number"| C[".iloc[row_index, col_index]"]
    B --> D["Inclusive slicing<br/>loc[0:4] → 5 rows"]
    C --> E["Exclusive slicing<br/>iloc[0:4] → 4 rows"]

    style B fill:#e1f5ff
    style C fill:#ffe1e1
""")
```

### When the Index Is Meaningful

When you set a column as the index (e.g., municipality names), `.loc` becomes
even more powerful:

```python
df_indexed = df.set_index('municipio')
df_indexed.loc['Humacao']                          # All data for Humacao
df_indexed.loc[['San Juan', 'Ponce', 'Mayagüez']]  # Multiple municipalities
```

---

## Boolean Filtering — The Mask

Boolean filtering works exactly like NumPy boolean indexing from Lab 04.
The pattern is always the same:

1. Create a boolean mask (a Series of True/False)
2. Apply the mask to the DataFrame

### Creating Masks

```python
# Single condition
mask = df['poblacion'] > 50000
print(mask.head())       # Series of True/False values
print(mask.sum())        # Count of True values
```

### Applying Masks

```python
big_cities = df[mask]               # or: df.loc[mask]
print(f"Cities with pop > 50,000: {len(big_cities)}")
```

### Combining Conditions

```python
# AND: & (both conditions must be true)
mask = (df['poblacion'] > 30000) & (df['region'] == 'Metro')

# OR: | (either condition)
mask = (df['poblacion'] > 100000) | (df['municipio'] == 'San Juan')

# NOT: ~ (invert)
mask = ~(df['region'] == 'Metro')   # All non-Metro municipalities
```

**Critical syntax rule:** Always use parentheses around each condition when
combining with `&` or `|`. Without them, Python's operator precedence causes
errors:

```python
# WRONG — will raise an error
# mask = df['poblacion'] > 30000 & df['region'] == 'Metro'

# CORRECT — parentheses around each condition
mask = (df['poblacion'] > 30000) & (df['region'] == 'Metro')
```

### NumPy Bridge

| pandas | NumPy | What Changed |
|--------|-------|--------------|
| `df['pop'] > 50000` | `arr[:, i] > 50000` | Named column instead of index |
| `df[mask]` | `arr[mask]` | Identical pattern |
| `(cond1) & (cond2)` | `(cond1) & (cond2)` | Identical pattern |

---

## Sorting

### sort_values — Sort by Column

```python
# Sort by population, largest first
df_sorted = df.sort_values('poblacion', ascending=False)
df_sorted.head()

# Sort by multiple columns: region first, then population within each region
df_sorted = df.sort_values(['region', 'poblacion'], ascending=[True, False])
```

### rank — Assign Ranks

```python
df['pop_rank'] = df['poblacion'].rank(ascending=False)
# Rank 1 = highest population
```

### nlargest / nsmallest — Quick Top/Bottom N

```python
top5 = df.nlargest(5, 'poblacion')     # Top 5 by population
bottom5 = df.nsmallest(5, 'poblacion') # Bottom 5 by population
```

---

## Groupby — Split-Apply-Combine

This is the single most important pandas concept. It replaces what would
otherwise require manual loops in NumPy.

### The Pattern

```python
Mermaid("""
flowchart LR
    A["DataFrame<br/>(78 rows)"] -->|"Split"| B["Groups<br/>by region"]
    B -->|"Apply"| C["sum() per group"]
    C -->|"Combine"| D["Result<br/>(6 rows)"]

    style A fill:#e1f5ff
    style D fill:#90EE90
""")
```

1. **Split:** Divide the DataFrame into groups based on a column's values
2. **Apply:** Compute a function (sum, mean, count, etc.) within each group
3. **Combine:** Assemble the results back into a DataFrame or Series

### Basic Usage

```python
# Total population per region
region_pop = df.groupby('region')['poblacion'].sum()
print(region_pop)
```

### Multiple Aggregations

```python
# Multiple stats at once
region_stats = df.groupby('region')['poblacion'].agg(['sum', 'mean', 'count'])
print(region_stats)
```

### Named Aggregation (Custom)

```python
region_summary = df.groupby('region').agg(
    total_pop=('poblacion', 'sum'),
    avg_pop=('poblacion', 'mean'),
    num_municipios=('municipio', 'count'),
    avg_income=('ingreso_mediano', 'mean')
)
print(region_summary)
```

### NumPy Comparison

What would have required this in NumPy:

```python
# NumPy approach (manual, error-prone)
regions = np.unique(arr[:, region_col])
for r in regions:
    mask = arr[:, region_col] == r
    total = arr[mask, pop_col].astype(int).sum()
    print(f"{r}: {total}")
```

Becomes a single line in pandas:

```python
df.groupby('region')['poblacion'].sum()
```

---

## Reindexing

### set_index — Use a Column as Row Labels

```python
df_indexed = df.set_index('municipio')

# Now look up by municipality name directly
df_indexed.loc['Humacao']
df_indexed.loc['Humacao', 'poblacion']
```

### reset_index — Go Back to Default

```python
df_reset = df_indexed.reset_index()
# 'municipio' becomes a regular column again
```

### Why Reindex?

Setting a meaningful index enables natural, dictionary-like lookups. In the
Critical Incident, you will use this to look up population values by
municipality name without needing a merge operation.

---

## Computed Columns

### Creating New Columns

```python
# Population density
df['densidad'] = df['poblacion'] / df['area_km2']

# Per-capita income (just an example)
df['income_per_capita'] = df['ingreso_mediano'] / df['poblacion']
```

### Categorical Classification with pd.cut

```python
df['tamano'] = pd.cut(
    df['poblacion'],
    bins=[0, 20000, 50000, 100000, float('inf')],
    labels=['Pequeño', 'Mediano', 'Grande', 'Metrópoli']
)
print(df['tamano'].value_counts())
```

This divides the population into bins and labels each municipality accordingly.
Bins are: 0-20k (Pequeño), 20k-50k (Mediano), 50k-100k (Grande), 100k+
(Metrópoli).

---

## Visualization from DataFrames

pandas integrates directly with Matplotlib. Every Series and DataFrame has
a `.plot()` method:

### Bar Charts

```python
# From a groupby result
region_pop = df.groupby('region')['poblacion'].sum().sort_values()
region_pop.plot.barh(color='steelblue', figsize=(10, 5))
plt.xlabel('Population')
plt.title('Total Population by Region')
plt.tight_layout()
plt.show()
```

### Histograms

```python
df['poblacion'].plot.hist(bins=20, color='steelblue', edgecolor='white')
plt.xlabel('Population')
plt.ylabel('Count')
plt.title('Distribution of Municipal Populations')
plt.tight_layout()
plt.show()
```

### Multi-Panel Dashboards

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: bar chart
top10 = df.nlargest(10, 'poblacion')
axes[0, 0].barh(top10['municipio'], top10['poblacion'], color='steelblue')
axes[0, 0].set_title('Top 10 by Population')
axes[0, 0].invert_yaxis()

# ... fill remaining panels ...

plt.suptitle('Dashboard Title', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

---

## Anomaly Detection with Z-Scores

### What Is a Z-Score?

A z-score measures how many **standard deviations** a value is from the mean:

$$z = \frac{x - \mu}{\sigma}$$

where $\mu$ is the mean and $\sigma$ is the standard deviation.

| Z-Score | Interpretation |
|---------|----------------|
| 0 | Exactly at the mean |
| 1.0 | One std above the mean |
| -1.0 | One std below the mean |
| > 2.0 | Unusually high (top ~2.5%) |
| > 3.0 | Extremely unusual (top ~0.1%) |

### Computing Z-Scores in pandas

```python
mean = series.mean()
std = series.std()
z_scores = (series - mean) / std

# Flag outliers
outliers = z_scores[z_scores.abs() > 2]
```

### Why Z-Scores for Anomaly Detection?

Raw values can be misleading. A municipality consuming 100,000 kWh might seem
like a lot, but if it has 300,000 residents, that is low per-capita. By
normalizing to per-capita consumption and then computing z-scores, we get a
fair comparison across all municipalities regardless of size.

---

## Quick Reference Summary

| Concept | Key Point |
|---------|-----------|
| **DataFrame** | Dictionary of Series (columns), each with its own dtype |
| **Series** | Labeled 1D array — one column of a DataFrame |
| **Heterogeneous** | Unlike NumPy, each column can have a different type |
| **`.loc`** | Label-based selection (inclusive slicing) |
| **`.iloc`** | Position-based selection (exclusive slicing, like NumPy) |
| **Boolean mask** | `df[df['col'] > val]` — same pattern as NumPy |
| **`&` `|` `~`** | Combine masks — always use parentheses around conditions |
| **`.sort_values()`** | Sort by one or more columns |
| **`.rank()`** | Assign ranks within a column |
| **`.groupby()`** | Split-apply-combine: group → aggregate → result |
| **`.agg()`** | Multiple or custom aggregations in one call |
| **`.set_index()`** | Make a column the row index for natural lookups |
| **`.reset_index()`** | Restore default integer index |
| **`pd.cut()`** | Bin numeric data into categories |
| **`.describe()`** | Summary statistics for all numeric columns |
| **`.info()`** | Compact summary: columns, dtypes, non-null counts |
| **Z-score** | `(x - mean) / std` — measures how unusual a value is |
| **`.plot()`** | Direct Matplotlib integration from DataFrames/Series |

### Key Method Quick Reference

| Method | Purpose | Example |
|--------|---------|---------|
| `pd.read_csv(path)` | Load CSV into DataFrame | `df = pd.read_csv('data/file.csv')` |
| `df.head(n)` | First n rows | `df.head()` |
| `df.shape` | (rows, cols) tuple | `print(df.shape)` |
| `df.dtypes` | Column types | `print(df.dtypes)` |
| `df.info()` | Full summary | `df.info()` |
| `df.describe()` | Numeric stats | `df.describe()` |
| `df['col']` | Select column (Series) | `pop = df['poblacion']` |
| `df[['a','b']]` | Select columns (DataFrame) | `sub = df[['municipio','poblacion']]` |
| `df.loc[r, c]` | Select by label | `df.loc[0, 'municipio']` |
| `df.iloc[r, c]` | Select by position | `df.iloc[0, 0]` |
| `df[mask]` | Boolean filter | `df[df['pop'] > 50000]` |
| `df.sort_values(col)` | Sort rows | `df.sort_values('pop', ascending=False)` |
| `df.nlargest(n, col)` | Top N rows | `df.nlargest(10, 'poblacion')` |
| `df.groupby(col)` | Group rows | `df.groupby('region')['pop'].sum()` |
| `df.set_index(col)` | Set row labels | `df.set_index('municipio')` |
| `pd.cut(s, bins)` | Bin values | `pd.cut(df['pop'], bins=[...])` |
