# Lab 06: The Data Lake

**Concepts**: [![Open Concepts In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/devomh/comp3084-2026/blob/main/lab06/concepts.ipynb)

**Lab06**: [![Open Lab Notebook In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/devomh/comp3084-2026/blob/main/lab06/lab06.ipynb)

## Case Brief

### The Situation

The Municipal Intelligence Division has received a priority tasking: analyze
public datasets from Puerto Rico's open data sources to support city planning
decisions. The raw data — spreadsheets with mixed types (strings, numbers,
dates, categories) — is useless without the ability to slice, filter, sort,
and summarize it. Standard spreadsheet tools cannot handle the volume or
complexity of the analysis required.

Additionally, analysts have flagged a resource consumption dataset where one
municipality shows a pattern that deviates significantly from its peers.
Something is wrong in the data, and it is your job to find it.

### Your Mission

You are an **Urban Data Analyst** tasked with building an analytical toolkit
using pandas to transform raw government data into actionable intelligence.
You will:

1. Load CSV datasets into DataFrames and inspect their structure.
2. Select, filter, and sort data using `.loc`, `.iloc`, and boolean masks.
3. Group and aggregate data to reveal regional patterns.
4. Create visualizations that communicate findings clearly.
5. Detect a statistical anomaly in municipal resource consumption data.

### The Stakes

City planners are waiting for your analysis. Every filter you write, every
groupby you compute, and every chart you generate feeds directly into
infrastructure decisions affecting 3.2 million residents. The anomaly in the
consumption data could indicate fraud, data corruption, or a genuine crisis —
your statistical evidence must be airtight.

---

## Chain of Custody

### Technical Requirements

- Completion of Lab 04 and Lab 05 (NumPy arrays, vectorized operations)
- Python 3.8 or higher
- Python libraries: `pandas`, `numpy`, `matplotlib`

```bash
pip install pandas numpy matplotlib
```

**Library Constraints (strictly enforced):**

- **`pandas`** — All DataFrame/Series operations
- **`numpy`** — Supporting array operations
- **`matplotlib`** — `plot()`, `bar()`, `hist()`, `subplots()`, axis labels and titles
- **No `seaborn`, `plotly`, `polars`, `openpyxl`**, or any other data library

### Evidence Files (Provided)

Located in the [`data/`](data/) directory:

1. **`municipios_stats.csv`** — Primary municipal statistics (78 municipalities,
   6 columns: name, region, population, area, income, poverty rate)
2. **`consumo_municipal.csv`** — Monthly energy consumption per municipality
   (936 rows: 78 municipalities x 12 months, with one planted anomaly)

```bash
# Verify the evidence files are present
ls data/
# Expected: municipios_stats.csv  consumo_municipal.csv
```

---

## Investigation Phases

Open [`lab06.md`](lab06.md) (or [`lab06.ipynb`](lab06.ipynb) in Jupyter/Colab) for
the guided exercises. Consult [`concepts.md`](concepts.md) for technical background.

### Phase 1: First Contact with the Data (30 min)

**Objective:** Load CSV data into DataFrames and understand their structure.

- Load CSV files using `pd.read_csv()`
- Inspect shape, dtypes, columns, and memory usage with `.info()`
- Compute summary statistics with `.describe()`
- Understand the difference between a Series (1D) and a DataFrame (2D)

**Key insight:** A DataFrame is a dictionary of Series — each column has its
own dtype. This is what makes it "heterogeneous," unlike a NumPy array where
every element shares the same type.

---

### Phase 2: Slicing & Filtering — The Scalpel (45 min)

**Objective:** Master precise data access and conditional filtering.

#### Part A: loc and iloc — Precision Access (15 min)

Select specific rows and columns by label (`.loc`) or position (`.iloc`):

```
df.loc[row_label, col_name]     # Label-based (like a dictionary lookup)
df.iloc[row_index, col_index]   # Position-based (like NumPy indexing)
```

#### Part B: Boolean Filtering — The Mask (15 min)

Filter rows based on conditions, exactly like NumPy boolean indexing:

```python
mask = df['poblacion'] > 50000
big_cities = df[mask]
```

Combine conditions with `&` (AND), `|` (OR), `~` (NOT).

#### Part C: Sorting — Establishing Order (15 min)

Sort by one or more columns using `.sort_values()`, extract top-N records,
and rank entries with `.rank()`.

---

### Phase 3: Grouping & Aggregation — The Analyst's Lens (45 min)

**Objective:** Use the split-apply-combine pattern to reveal regional trends.

#### Part A: groupby — Split-Apply-Combine (20 min)

Group by a categorical column and compute summaries (`.sum()`, `.mean()`,
`.count()`, `.agg()`).

#### Part B: Reindexing — New Labels (15 min)

Change row labels with `.set_index()` and `.reset_index()` to enable
natural lookups by municipality name.

#### Part C: Adding Computed Columns (10 min)

Derive new columns from existing ones: population density, size categories.

---

### Phase 4: Visualization Dashboard (20 min)

**Objective:** Create a multi-panel summary visualization of the dataset.

Build a 2x2 dashboard with:
- Top 10 municipalities by population (bar chart)
- Total population by region (bar chart)
- Population distribution (histogram)
- Municipality size categories (bar chart)

---

### Phase 5: Critical Incident — "The Anomaly in the Data Lake" (30 min)

**Objective:** Detect and explain a statistical outlier in consumption data.

**The Escalation:** Analysts have flagged the energy consumption dataset —
one municipality's per-capita consumption is far outside the expected range.

1. **Load** the consumption dataset and compute annual totals per municipality.
2. **Normalize** by population to get per-capita consumption.
3. **Compute z-scores** to identify statistical outliers.
4. **Isolate** the anomalous municipality and present evidence.
5. **Visualize** the anomaly against the population-wide distribution.

---

## Wrap-Up

After completing all phases, verify every cell runs from top to bottom
without errors.

**Before you leave:**

- Complete all sections of [`submission.md`](submission.md), including the
  anomaly findings and reflection questions.
- Ensure all notebook cells run without errors from top to bottom.
- Include your AI Usage Appendix if applicable.

---

## Submission Requirements

### 1. Notebook

- [`lab06.ipynb`](lab06.ipynb) — All cells implemented and run without errors,
  top to bottom

### 2. Documentation

Complete [`submission.md`](submission.md) with:

- Dataset properties table (shape, dtypes, column summary)
- Anomaly findings from the Critical Incident
- Answers to all reflection questions

---

## Evaluation Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **Loading & Inspection** | 10 | Correct shape, dtypes, describe output reported |
| **Column/Row Selection** | 10 | Correct use of loc/iloc, Series vs DataFrame distinction |
| **Boolean Filtering** | 15 | Correct masks with &/\|/~, meaningful filters applied |
| **Sorting & Ranking** | 10 | Correct sort_values, rank, top-N extraction |
| **Grouping & Aggregation** | 15 | Correct groupby with multiple aggregations |
| **Reindexing & Computed Columns** | 10 | set_index/reset_index, derived columns (density, categories) |
| **Visualization Dashboard** | 10 | Multi-panel figure with proper labels and titles |
| **Critical Incident** | 20 | Anomaly detected, evidence presented, findings written |
| **Total** | **100** | |

**Bonus:**

| Component | Points | Criteria |
|-----------|--------|----------|
| Multi-level groupby | +5 | Group by two columns simultaneously |
| Custom agg functions | +5 | Use `.agg()` with lambda or named aggregation |
| Interactive exploration | +5 | Use `.query()` method for readable filtering |
| Cross-tab analysis | +5 | Use `pd.crosstab()` for frequency tables |

---

## Tips for Success

1. **Read the Field Manual first:** [`concepts.md`](concepts.md) covers
   DataFrames vs arrays, indexing, groupby, and the bridge from NumPy to
   pandas with worked examples and diagrams.

2. **Remember the NumPy bridge:** Every pandas operation has a NumPy parallel.
   Boolean masks work the same way — `df[mask]` is just like `arr[mask]`.
   If you get stuck, think about how you would do it with arrays first.

3. **Series vs DataFrame:** A single bracket `df['col']` returns a Series
   (1D). Double brackets `df[['col']]` return a DataFrame (2D). Know which
   one you need.

4. **Test incrementally:** After every filter, groupby, or transformation,
   print the shape and head to verify it worked:
   ```python
   result = df.groupby('region')['poblacion'].sum()
   print(result.shape)
   print(result)
   ```

5. **Watch for SettingWithCopyWarning:** When modifying a filtered DataFrame,
   use `.loc` to ensure you are editing the original, not a copy.

6. **Parentheses in boolean masks:** Always wrap conditions in parentheses
   when combining with `&` or `|`:
   ```python
   mask = (df['pop'] > 50000) & (df['region'] == 'Metro')  # correct
   ```

---

## Resources

- **Field Manual:** [`concepts.md`](concepts.md) — DataFrames, Series,
  indexing, groupby, and the NumPy-to-pandas bridge
- **Lab Notebook:** [`lab06.md`](lab06.md) — Guided exercises with boilerplate
  code and expected outputs
- **pandas documentation:** [pandas.pydata.org/docs](https://pandas.pydata.org/docs/)
- **Matplotlib `bar`:** [matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html)

---

## Questions?

If you encounter issues:

1. Re-read the relevant section in [`concepts.md`](concepts.md)
2. Check for parentheses in boolean masks — missing parens is the #1 error
3. Print `.shape`, `.dtypes`, and `.head()` at every step to isolate problems
4. Verify column names match exactly (case-sensitive, no extra spaces)

**Remember:** The goal is to think like an urban data analyst — every row
tells a story, and the tools you build determine what stories you can find.
