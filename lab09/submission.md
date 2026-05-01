# Lab 09 Submission: The Public Dashboard

**Student Name:** [Your Name]
**Date:** [Date]
**Live URL:** [paste your `*.streamlit.app` URL here]

---

## Section A: Setup and First Run (Phase 1)

### Re-Run Model (Exercise 1.2)

Describe in your own words what happened when you moved the slider:

[your answer]

Why does Streamlit re-execute the entire script on every widget
interaction, rather than only re-running the line that reads the widget?

[your answer — one or two sentences]

---

## Section B: Data Layer (Phase 2)

### Exercise 2.1 — Database Tables

Tables present in `data/municipios.db` (from the `sqlite_master` query):

[list them here]

### Exercise 2.3 — Parameterized Query

Paste the first working `pd.read_sql` call that filters by `selected`:

```python
[your query here]
```

Why is `params=selected` safer than interpolating `selected` into the
SQL string with an f-string?

[your answer]

### Exercise 2.4 — `st.stop()` Guard

What did the app display before you added the guard, when all regions
were deselected?

[your answer]

What does the app display after adding the guard?

[your answer]

---

## Section C: Layout and Filters (Phase 3)

### Exercise 3.2 — Ranking Query

Paste the `df_top` query, including the `params=` argument:

```python
[your query here]
```

Why is `top_n` appended to the params list rather than embedded directly
in the SQL string?

[your answer]

### Exercise 3.3 — Region Aggregate Query

Paste the `df_region` query:

```python
[your query here]
```

Why is this query placed in the `# --- Queries ---` block rather than
at the bottom of the file where the chart that uses it is rendered?

[your answer]

### Exercise 3.5 — KPI Row

With **all six regions** selected and `top_n = 10`:

| Metric | Value |
|---|---|
| Municipalities shown | |
| Total population | |
| Largest municipality | |

With **only Metro** selected and `top_n = 5`:

| Metric | Value |
|---|---|
| Municipalities shown | |
| Total population | |
| Largest municipality | |

---

## Section D: Plots (Phase 4)

### Exercise 4.1 — Top N Chart

Screenshot or description of the chart with all regions selected and
`top_n = 10`:

[description or note that screenshot is attached]

### Exercise 4.2 — Population by Region Chart

Screenshot or description of the chart with **only Norte and Central**
selected:

[description or note that screenshot is attached]

### Exercise 4.3 — Observation

What triggers the re-render of both charts simultaneously?

[your answer]

Which Python objects are recreated on each widget change? Which are not?
(Hint: think about what the cache decorators protect.)

[your answer]

---

## Section E: Deployment (Phase 5)

### Live URL

`*.streamlit.app` URL (must work without login):

[paste URL here]

### Smoke Test Results

| Test | Pass / Fail | Notes |
|---|---|---|
| Page loads without error | | |
| Both charts render (all regions selected) | | |
| Region filter updates charts and KPI row | | |
| Deselecting all regions shows warning, not stack trace | | |
| Search for "San" returns results | | |
| Search for "xyz" shows "No municipalities" info message | | |

### Absolute-Path Check

Does `app.py` use only relative paths (e.g. `data/municipios.db`)?
[ ] Yes — all paths are relative.
[ ] No — I found and fixed an absolute path before deploying.

---

## Section F: Wrap-Up Reflections

1. **The re-run model.** What is it, and why does it require
   `@st.cache_resource` for the database connection?

   [your answer]

2. **`st.stop()`.** Why does the app call `st.stop()` when no regions are
   selected, rather than letting the query run?

   [your answer]

3. **Three layers, same question.** The "total population per region"
   question was answered in Lab 06 (`groupby`), Lab 08 (`GROUP BY`), and
   now Lab 09 (parameterized SQL in Streamlit). What does each layer add
   that the previous one lacked?

   [your answer]

4. **Final project transition.** What four changes would you make to
   `app.py` to start your final project with a different dataset?

   [your answer]

---

## Section G: AI Usage (if applicable)

### Tool Used
[Name of AI tool]

### Methodology
[How did you use it?]

### The Prompt
[Paste the most representative prompt]

### The Output
[Summarize what the AI gave you — include any errors or hallucinations]

### Human Value-Add
[What did you verify, correct, or expand? How did you confirm it worked?]
