# Lab 06: The Data Lake -- Lab Notebook
**Urban Data Analysis with pandas DataFrames**

---

## Introduction

Welcome to the Municipal Intelligence Division. You have been assigned the role of **Urban Data Analyst** on a priority case. City planners need actionable insights from Puerto Rico's municipal data — raw spreadsheets with mixed types (strings, numbers, categories) that are useless without the ability to slice, filter, sort, and summarize.

Your mission is threefold:

1. **Understand** how tabular data is represented as a pandas DataFrame — the heterogeneous evolution of the NumPy arrays you mastered in Labs 04-05.
2. **Build** an analytical toolkit using selection, filtering, grouping, and visualization to extract patterns from municipal data.
3. **Detect** a statistical anomaly in resource consumption data that could indicate fraud, data corruption, or a genuine crisis.

**Constraints:** You may use `pandas`, `numpy`, and `matplotlib`. No `seaborn`, `plotly`, `polars`, `openpyxl`, or any other data library.

**Reference:** Consult [`concepts.md`](concepts.md) for detailed background on DataFrames vs arrays, indexing, groupby, and how every pandas operation maps to a NumPy operation you already know.

---

## Setup

Run this cell first. Every code cell in this notebook depends on these imports.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

---

## Phase 1: First Contact with the Data

Before we can analyze municipal data, we need to understand its structure. Unlike the homogeneous NumPy arrays from Labs 04-05, a DataFrame stores **heterogeneous** data — each column has its own type. A municipality name is text, a population is an integer, and a poverty rate is a float, all in the same table.

---

### Exercise 1.1: Loading a CSV into a DataFrame

Our first task is to load a dataset and inspect its dimensions and structure. The `pd.read_csv()` function parses a CSV file and returns a DataFrame.

```python
# Load the municipal statistics dataset
df = pd.read_csv('data/municipios_stats.csv')

# Inspect the structure
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"\nColumn types:")
print(df.dtypes)
print(f"\nFirst 5 rows:")
df.head()
```

<details>
<summary>Expected Output</summary>

```
Shape: (78, 6)
Columns: ['municipio', 'region', 'poblacion', 'area_km2', 'ingreso_mediano', 'tasa_pobreza']

Column types:
municipio           object
region              object
poblacion            int64
area_km2           float64
ingreso_mediano      int64
tasa_pobreza       float64
```

The shape `(78, 6)` tells us there are 78 municipalities and 6 columns. Notice that dtypes are **heterogeneous** — `object` (text), `int64` (integers), and `float64` (decimals) coexist in the same table. This is impossible in a NumPy array.
</details>

**Task:** Use `.info()` to get a compact summary of the dataset, including non-null counts and memory usage.

```python
# TODO: Display the full info summary
df.info()
```

**Discovery Task:** How many municipalities are in the dataset? Which columns are numeric and which are text? Record your answers in [`submission.md`](submission.md).

---

### Exercise 1.2: Statistical Summary

The `.describe()` method computes summary statistics for all numeric columns: count, mean, std, min, 25%, 50% (median), 75%, max.

```python
# Summary statistics for numeric columns
df.describe()
```

**Questions:**
- What is the median population across municipalities? (Look at the 50% row)
- Which numeric column has the highest standard deviation?
- What is the range (max - min) of population?

---

### Exercise 1.3: Series vs DataFrame

Understanding the return type of column selection is critical. A single bracket returns a **Series** (1D), while double brackets return a **DataFrame** (2D).

```python
# Series (1D) — like arr[:, i] in NumPy
pop = df['poblacion']
print(f"Type: {type(pop)}")
print(f"Shape: {pop.shape}")
print(f"Dtype: {pop.dtype}")
```

```python
# DataFrame (2D) — like arr[:, [i, j]] in NumPy
subset = df[['municipio', 'poblacion']]
print(f"Type: {type(subset)}")
print(f"Shape: {subset.shape}")
```

<details>
<summary>Expected Output</summary>

```
Type: <class 'pandas.core.series.Series'>
Shape: (78,)
Dtype: int64

Type: <class 'pandas.core.frame.DataFrame'>
Shape: (78, 2)
```

Key difference: `df['col']` → Series (1D), `df[['col1', 'col2']]` → DataFrame (2D).
</details>

**Connection to NumPy:** A Series is like `arr[:, i]` — a single column. A DataFrame subset is like `arr[:, [i, j]]` — multiple columns.

---

## Phase 2: Slicing & Filtering — The Scalpel

Now that we can load and inspect data, we move to precise data access. These tools let you extract exactly the rows and columns you need — the analytical equivalent of a surgeon's scalpel.

---

### Part A: loc and iloc — Precision Access

There are two accessors for selecting rows and columns:

- **`.loc`** — by **label** (column name, row label). Slicing is **inclusive**.
- **`.iloc`** — by **position** (integer index, like NumPy). Slicing is **exclusive**.

```python
# .loc — label-based
print("loc[0, 'municipio']:", df.loc[0, 'municipio'])
print("\nloc[0:4, specific columns]:")
df.loc[0:4, ['municipio', 'poblacion']]
```

```python
# .iloc — position-based (like NumPy)
print("iloc[0, 0]:", df.iloc[0, 0])
print("\niloc[:5, :3] (first 5 rows, first 3 columns):")
df.iloc[:5, :3]
```

<details>
<summary>Key Difference</summary>

```
df.loc[0:4]   → rows 0, 1, 2, 3, 4  (inclusive — 5 rows)
df.iloc[0:4]  → rows 0, 1, 2, 3     (exclusive — 4 rows, like NumPy)
```
</details>

**Exercise:** Extract the population of the 10th municipality (index 9) using both `.loc` and `.iloc`. Verify they return the same value.

```python
# TODO: Get population of the 10th municipality using .loc
pop_loc = None  # Replace with your code

# TODO: Get population of the 10th municipality using .iloc
pop_iloc = None  # Replace with your code

print(f"Using .loc:  {pop_loc}")
print(f"Using .iloc: {pop_iloc}")
print(f"Same value?  {pop_loc == pop_iloc}")
```

---

### Part B: Boolean Filtering — The Mask

Boolean filtering works **exactly** like NumPy boolean indexing from Lab 04. The pattern is:

1. Create a boolean mask (Series of True/False)
2. Apply the mask to the DataFrame

```python
# Step 1: Create a boolean mask
mask = df['poblacion'] > 50000
print("Mask (first 10):")
print(mask.head(10))
print(f"\nMunicipalities with pop > 50,000: {mask.sum()}")
```

```python
# Step 2: Apply the mask
big_cities = df[mask]
print(f"\n{len(big_cities)} municipalities with population > 50,000:")
big_cities[['municipio', 'poblacion', 'region']]
```

**Combining Conditions:**

```python
# AND: & (both conditions must be true)
# Always wrap each condition in parentheses!
mask_metro_big = (df['poblacion'] > 30000) & (df['region'] == 'Metro')
metro_big = df[mask_metro_big]
print(f"Metro municipalities with pop > 30,000: {len(metro_big)}")
metro_big[['municipio', 'poblacion']]
```

```python
# OR: | (either condition)
mask_or = (df['poblacion'] > 100000) | (df['municipio'] == 'Humacao')
df[mask_or][['municipio', 'poblacion']]
```

```python
# NOT: ~ (invert)
mask_not_metro = ~(df['region'] == 'Metro')
non_metro = df[mask_not_metro]
print(f"Non-Metro municipalities: {len(non_metro)}")
```

**Exercise:** Find all municipalities with population between 20,000 and 60,000.

```python
# TODO: Create a mask for population between 20,000 and 60,000
# Hint: Combine two conditions with &
mask_mid = None  # Replace with your code

mid_pop = df[mask_mid]
print(f"Municipalities with pop between 20k and 60k: {len(mid_pop)}")
mid_pop[['municipio', 'poblacion', 'region']].head(10)
```

---

### Part C: Sorting — Establishing Order

Sorting lets you rank and extract top/bottom records.

```python
# Sort by population (largest first)
df_sorted = df.sort_values('poblacion', ascending=False)
print("Top 5 municipalities by population:")
df_sorted[['municipio', 'poblacion']].head()
```

```python
# Sort by multiple columns: region (A-Z), then population (high to low) within each
df_multi = df.sort_values(['region', 'poblacion'], ascending=[True, False])
df_multi[['municipio', 'region', 'poblacion']].head(15)
```

```python
# Rank municipalities by population
df['pop_rank'] = df['poblacion'].rank(ascending=False).astype(int)
print("Top 5 and Bottom 5 by rank:")
print(df.sort_values('pop_rank')[['municipio', 'poblacion', 'pop_rank']].head())
print()
print(df.sort_values('pop_rank')[['municipio', 'poblacion', 'pop_rank']].tail())
```

**Visualization — Top 10 Bar Chart:**

```python
top10 = df.sort_values('poblacion', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top10['municipio'], top10['poblacion'], color='steelblue')
ax.set_xlabel('Population')
ax.set_title('Top 10 Municipalities by Population')
ax.invert_yaxis()  # Largest on top
plt.tight_layout()
plt.show()
```

**Exercise:** Which municipality is ranked #1? Which is last (#78)? Record in [`submission.md`](submission.md).

---

## Phase 3: Grouping & Aggregation — The Analyst's Lens

Grouping is the most powerful single-table operation in pandas. It replaces what would otherwise require manual loops in NumPy with a concise split-apply-combine pattern.

---

### Part A: groupby — Split-Apply-Combine

The `groupby()` method divides the DataFrame into groups based on a column, applies an aggregation function to each group, and combines the results.

```python
# Total population per region
region_pop = df.groupby('region')['poblacion'].sum()
print("Total population by region:")
print(region_pop)
```

```python
# Multiple aggregations at once
region_stats = df.groupby('region')['poblacion'].agg(['sum', 'mean', 'count'])
print("\nRegion statistics:")
region_stats
```

```python
# Named aggregation — custom column names
region_summary = df.groupby('region').agg(
    total_pop=('poblacion', 'sum'),
    avg_pop=('poblacion', 'mean'),
    num_municipios=('municipio', 'count'),
    avg_income=('ingreso_mediano', 'mean')
)
print("\nRegion summary:")
region_summary
```

**Visualization — Population by Region:**

```python
region_pop_sorted = df.groupby('region')['poblacion'].sum().sort_values()

fig, ax = plt.subplots(figsize=(10, 5))
region_pop_sorted.plot.barh(ax=ax, color='darkorange')
ax.set_title('Total Population by Region')
ax.set_xlabel('Population')
plt.tight_layout()
plt.show()
```

**Exercise:** Which region has the most municipalities? Which has the highest total population? Record in [`submission.md`](submission.md).

---

### Part B: Reindexing — New Labels, New Perspective

Setting a meaningful column as the index allows dictionary-like lookups.

```python
# Set municipality name as the index
df_indexed = df.set_index('municipio')

# Now look up by name
print("Humacao's data:")
print(df_indexed.loc['Humacao'])
```

```python
# Look up multiple municipalities
selected = df_indexed.loc[['San Juan', 'Ponce', 'Mayagüez']]
print("\nSelected municipalities:")
selected[['region', 'poblacion', 'ingreso_mediano']]
```

```python
# Reset back to default integer index
df_reset = df_indexed.reset_index()
print(f"\nAfter reset_index, shape: {df_reset.shape}")
print(f"Columns: {list(df_reset.columns)}")
```

**Exercise:** Set the index to municipality name. Look up the population of Humacao directly using `.loc`. Record the value in [`submission.md`](submission.md).

---

### Part C: Adding Computed Columns

Create new columns derived from existing ones.

```python
# Population density (people per km²)
df['densidad'] = df['poblacion'] / df['area_km2']
print("Top 5 by density:")
df.nlargest(5, 'densidad')[['municipio', 'poblacion', 'area_km2', 'densidad']]
```

```python
# Categorical classification by population size
df['tamano'] = pd.cut(
    df['poblacion'],
    bins=[0, 20000, 50000, 100000, float('inf')],
    labels=['Pequeño', 'Mediano', 'Grande', 'Metrópoli']
)

print("Municipality size distribution:")
print(df['tamano'].value_counts().sort_index())
```

<details>
<summary>Expected Output (approximate)</summary>

```
Municipality size distribution:
Pequeño       ~25
Mediano       ~38
Grande        ~11
Metrópoli      ~4
```

Most municipalities are small or medium-sized. Only a few exceed 100,000 residents.
</details>

**Exercise:** How many municipalities fall in each category? Record in [`submission.md`](submission.md).

---

## Phase 4: Visualization Dashboard

**Goal:** Create a multi-panel summary visualization of the dataset.

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Top 10 by population (horizontal bar)
top10 = df.nlargest(10, 'poblacion')
axes[0, 0].barh(top10['municipio'], top10['poblacion'], color='steelblue')
axes[0, 0].set_title('Top 10 Municipalities by Population')
axes[0, 0].invert_yaxis()
axes[0, 0].set_xlabel('Population')

# Panel 2: Population by region (bar chart)
region_pop = df.groupby('region')['poblacion'].sum().sort_values()
region_pop.plot.barh(ax=axes[0, 1], color='darkorange')
axes[0, 1].set_title('Total Population by Region')
axes[0, 1].set_xlabel('Population')

# Panel 3: Population distribution (histogram)
axes[1, 0].hist(df['poblacion'], bins=20, color='steelblue', edgecolor='white')
axes[1, 0].set_title('Population Distribution')
axes[1, 0].set_xlabel('Population')
axes[1, 0].set_ylabel('Count')

# Panel 4: Size category counts (bar chart)
size_counts = df['tamano'].value_counts().sort_index()
colors = ['#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
size_counts.plot.bar(ax=axes[1, 1], color=colors)
axes[1, 1].set_title('Municipalities by Size Category')
axes[1, 1].set_ylabel('Count')
axes[1, 1].tick_params(axis='x', rotation=45)

plt.suptitle('Puerto Rico Municipal Analysis Dashboard', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

**Checkpoint:** You should see four well-labeled panels. If any panel is missing data or labels, fix it before proceeding.

---

## Phase 5: Critical Incident — "The Anomaly in the Data Lake"

**The Escalation:** Intelligence analysts have flagged a dataset of municipal energy consumption. One municipality shows a pattern that deviates significantly from its peers. Your mission: find it, prove it, and explain it.

---

### Step 1: Load & Inspect the Consumption Data

```python
consumo = pd.read_csv('data/consumo_municipal.csv')

print(f"Shape: {consumo.shape}")
print(f"Columns: {list(consumo.columns)}")
print(f"Unique municipalities: {consumo['municipio'].nunique()}")
print(f"Date range: {consumo['mes'].min()} to {consumo['mes'].max()}")
print(f"\nFirst 5 rows:")
consumo.head()
```

<details>
<summary>Expected Output</summary>

```
Shape: (936, 3)
Columns: ['municipio', 'mes', 'consumo_energia_kwh']
Unique municipalities: 78
Date range: 2024-01 to 2024-12
```

936 rows = 78 municipalities x 12 months.
</details>

---

### Step 2: Compute Annual Totals

Group by municipality to get the total annual consumption for each.

```python
# Total annual consumption per municipality
annual = consumo.groupby('municipio')['consumo_energia_kwh'].sum()
print(f"Annual consumption — shape: {annual.shape}")
print("\nTop 5 by total consumption:")
print(annual.sort_values(ascending=False).head())
```

---

### Step 3: Normalize by Population (Per-Capita)

Raw consumption totals are misleading — larger municipalities naturally consume more. We need **per-capita** values to make a fair comparison.

```python
# Load population data using set_index for direct lookups
stats = pd.read_csv('data/municipios_stats.csv').set_index('municipio')

# TODO: Compute per-capita annual consumption
# For each municipality in 'annual':
#   per_capita = annual_kwh / population
#
# Hint: stats.loc[municipio_name, 'poblacion'] gives the population
#       Or use: per_capita = annual / stats['poblacion']
#       (pandas aligns by index automatically!)

per_capita = None  # Replace with your code

print("Top 10 by per-capita annual consumption (kWh/person):")
print(per_capita.sort_values(ascending=False).head(10))
```

<details>
<summary>Expected Output (approximate)</summary>

```
Top 10 by per-capita annual consumption (kWh/person):
Vieques      ~14.5    ← THIS IS THE ANOMALY
Salinas       ~4.3
Utuado        ~4.3
...
```

One municipality should stand out dramatically — its per-capita consumption is roughly 3-4x higher than any other.
</details>

---

### Step 4: Detect the Anomaly with Z-Scores

A **z-score** measures how many standard deviations a value is from the mean. Values with |z| > 2 are unusual; |z| > 3 is extreme.

```python
# TODO: Compute z-scores for per-capita consumption
# z = (value - mean) / std
#
# mean = per_capita.mean()
# std = per_capita.std()
# z_scores = (per_capita - mean) / std

z_scores = None  # Replace with your code

# Flag outliers (|z| > 2)
outliers = z_scores[z_scores.abs() > 2]
print(f"Outliers (|z| > 2): {len(outliers)}")
print(outliers)
```

<details>
<summary>Expected Output</summary>

```
Outliers (|z| > 2): 1
Vieques    ~7.2
```

Only one municipality should be flagged as an outlier, with a very high z-score.
</details>

```python
# Identify the anomalous municipality
anomaly_name = z_scores.abs().idxmax()
anomaly_z = z_scores[anomaly_name]
anomaly_consumption = per_capita[anomaly_name]
avg_consumption = per_capita.mean()

print(f"\n--- ANOMALY DETECTED ---")
print(f"Municipality: {anomaly_name}")
print(f"Per-capita consumption: {anomaly_consumption:.1f} kWh/person")
print(f"Population average: {avg_consumption:.1f} kWh/person")
print(f"Z-score: {anomaly_z:.1f}")
print(f"Ratio to average: {anomaly_consumption / avg_consumption:.1f}x")
```

---

### Step 5: Present the Evidence

Create a visualization that clearly shows the anomaly.

```python
# TODO: Create a bar chart comparing the anomalous municipality
# against the overall distribution
#
# Option A: Bar chart of top 15 per-capita consumers
# Option B: Histogram with the anomaly marked
# Option C: Both in a 2-panel figure

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel 1: Top 15 per-capita consumers
top15 = per_capita.sort_values(ascending=False).head(15)
colors = ['crimson' if name == anomaly_name else 'steelblue'
          for name in top15.index]
axes[0].barh(top15.index, top15.values, color=colors)
axes[0].set_title('Top 15 Per-Capita Energy Consumption')
axes[0].set_xlabel('Annual kWh per Person')
axes[0].invert_yaxis()

# Panel 2: Z-score distribution
axes[1].hist(z_scores, bins=20, color='steelblue', edgecolor='white')
axes[1].axvline(x=anomaly_z, color='crimson', linewidth=2, linestyle='--',
                label=f'{anomaly_name} (z={anomaly_z:.1f})')
axes[1].axvline(x=2, color='orange', linewidth=1, linestyle=':',
                label='z = 2 threshold')
axes[1].axvline(x=-2, color='orange', linewidth=1, linestyle=':')
axes[1].set_title('Z-Score Distribution')
axes[1].set_xlabel('Z-Score')
axes[1].set_ylabel('Count')
axes[1].legend()

plt.suptitle('Critical Incident: Energy Consumption Anomaly',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()
```

---

### Step 6: Write Your Findings

**Task:** Complete the Critical Incident section of [`submission.md`](submission.md):

1. Which municipality is the anomaly?
2. What metric did you use to detect it (raw consumption, per-capita, z-score)?
3. How far from normal is it (z-score, ratio to average)?
4. What might explain the anomaly? (Consider: data entry error, unreported industrial activity, military installations, tourism infrastructure on a small island, etc.)

---

## Wrap-Up

Congratulations, analyst. You have:

1. **Loaded** CSV data into pandas DataFrames and understood the heterogeneous structure.
2. **Selected** rows and columns with `.loc` and `.iloc`, bridging from NumPy position-based indexing to label-based access.
3. **Filtered** data using boolean masks — the same pattern from Lab 04, now applied to tabular rows.
4. **Sorted** and **ranked** municipalities by population and other metrics.
5. **Grouped** data by region using `groupby` — the split-apply-combine pattern that replaces manual loops.
6. **Created** computed columns (density, size categories) and **reindexed** for natural lookups.
7. **Visualized** findings in a multi-panel dashboard.
8. **Detected** a statistical anomaly using per-capita normalization and z-scores.

Every operation has a NumPy parallel:

| pandas Operation | NumPy Equivalent | What's New |
|---|---|---|
| `df['col']` | `arr[:, i]` | Named columns |
| `df[mask]` | `arr[mask]` | Same pattern |
| `df.sort_values()` | `arr[np.argsort()]` | By column name |
| `df.groupby().sum()` | Manual loop | Automatic split-apply-combine |
| `df.set_index()` | — | Meaningful row labels |

### Before You Leave

- [ ] Complete all sections of [`submission.md`](submission.md)
- [ ] Ensure all notebook cells run without errors from top to bottom
- [ ] Verify the anomaly is correctly identified and explained
- [ ] Include the AI Usage Appendix if applicable

### Looking Ahead

The DataFrame skills you practiced here — selection, filtering, grouping, aggregation — are the foundation of all data analysis. In Lab 09, you will extend these skills to **multi-table operations** (merging, joining) when data lives across multiple files. For now, you have mastered the single-table toolkit.
