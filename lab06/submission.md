# Lab 06 Submission: The Data Lake

**Student Name:** [Your Name]
**Date:** [Date]

## Section A: Dataset Loading & Inspection

### Municipal Statistics (`municipios_stats.csv`)

| Property | Value |
|----------|-------|
| Shape (rows, cols) | |
| Columns | |
| Numeric columns | |
| Text columns | |
| Memory usage | |

### Consumption Data (`consumo_municipal.csv`)

| Property | Value |
|----------|-------|
| Shape (rows, cols) | |
| Columns | |
| Date range | |
| Number of unique municipalities | |

### Summary Statistics

- Median population across municipalities: ______
- Population range (min - max): ______
- Column with highest variance: ______

## Section B: Selection & Filtering

### loc vs iloc
- [ ] Extracted population of 10th municipality using both `.loc` and `.iloc`
- [ ] Verified both return the same value
- [ ] Understand the difference: `.loc` uses labels, `.iloc` uses positions

### Boolean Filtering
- [ ] Created mask for population > 50,000
- [ ] Combined conditions with `&` (AND)
- [ ] Combined conditions with `|` (OR)
- [ ] Used `~` (NOT) for negation
- [ ] Found municipalities with population between 20,000 and 60,000

Number of municipalities with pop > 50,000: ______
Number of municipalities with pop between 20,000 and 60,000: ______

### Sorting & Ranking
- [ ] Sorted by population (descending)
- [ ] Sorted by multiple columns (region + population)
- [ ] Ranked municipalities by population
- Top 3 by population: ______
- Bottom 3 by population: ______

## Section C: Grouping & Aggregation

### groupby Results

| Region | Total Population | Mean Population | Number of Municipalities |
|--------|-----------------|-----------------|-------------------------|
| Central | | | |
| Este | | | |
| Metro | | | |
| Norte | | | |
| Oeste | | | |
| Sur | | | |

- Region with most municipalities: ______
- Region with highest total population: ______
- Region with highest average population: ______

### Reindexing
- [ ] Set index to municipality name
- [ ] Looked up Humacao's population using `.loc`
- [ ] Reset index back to default

Population of Humacao: ______

### Computed Columns
- [ ] Created `densidad` (population density) column
- [ ] Created `tamano` (size category) column

Size category distribution:

| Category | Count |
|----------|-------|
| Pequeño (< 20,000) | |
| Mediano (20,000 - 50,000) | |
| Grande (50,000 - 100,000) | |
| Metrópoli (> 100,000) | |

## Section D: Visualization Dashboard

- [ ] Panel 1: Top 10 municipalities by population (horizontal bar)
- [ ] Panel 2: Total population by region (bar chart)
- [ ] Panel 3: Population distribution (histogram)
- [ ] Panel 4: Size category counts (bar chart)
- [ ] All panels have proper titles, axis labels, and formatting
- [ ] `plt.suptitle()` with overall dashboard title

## Section E: Critical Incident — Anomaly Detection

### Anomalous Municipality
**Name:** ______

### Evidence

| Metric | Anomalous Municipality | Population Average |
|--------|----------------------|-------------------|
| Annual consumption (kWh) | | |
| Per-capita consumption (kWh/person) | | |
| Z-score | | |

### Findings
[Write 2-3 sentences explaining what makes this municipality anomalous,
what metric you used to detect it, and what might explain the anomaly.]

### Visualization
- [ ] Bar chart comparing anomaly vs regional average
- [ ] Clear annotations explaining the deviation

## Section F: Reflections

1. What is the difference between a pandas Series and a DataFrame? How does
   this relate to selecting a single column vs multiple columns?

2. Why must you wrap boolean conditions in parentheses when combining them
   with `&` or `|`? What error do you get if you forget?

3. Explain the split-apply-combine pattern of `groupby` in your own words.
   Give an example from this lab.

4. What is a z-score and why is it useful for anomaly detection? What
   threshold did you use and why?

## Section G: Bonus (if attempted)

### Multi-level groupby
- [ ] Grouped by two columns simultaneously
- [ ] Meaningful aggregation computed

### Custom agg functions
- [ ] Used `.agg()` with lambda or named aggregation

### Interactive exploration
- [ ] Used `.query()` method for readable filtering

### Cross-tab analysis
- [ ] Used `pd.crosstab()` for frequency tables

## Section H: AI Usage (if applicable)

### Tool Used
[Name of AI tool]

### Methodology
[How did you use it? What was your approach?]

### The Prompt
[Paste the prompt you used]

### The Output
[Paste the AI's response]

### Human Value-Add
[What did you change, verify, or learn from the AI's output?]
