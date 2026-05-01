# Lab 09: The Public Dashboard

**Field Manual**: [concepts.md](https://github.com/devomh/comp3084-2026/blob/main/lab09/concepts.md)

**Live App**: [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/devomh/comp3084-2026/main/lab09/app_demo.py)

## Case Brief

### The Situation

The Municipal Intelligence Division has been asked to present its findings
to the Regional Planning Council — a group of decision-makers who do not
know Python and cannot run a notebook. Last semester you loaded the data
(Lab 06), distributed the computation (Lab 07), and archived everything
into a SQL database (Lab 08). Today you finish the job.

Your mission: turn `data/municipios.db` into a public-facing dashboard
that any planner can open in a browser, filter by region, search by name,
and read without touching code.

The dashboard must be live on the internet before the briefing. You have
one lab session to build it and ship it.

### Your Mission

You are a **Dashboard Architect / Public Intelligence Officer** tasked with:

1. Running a Streamlit app locally and understanding the re-run model
2. Connecting the app to `municipios.db` with parameterized SQL queries
3. Wiring sidebar widgets to those queries so every filter change
   re-renders the data
4. Laying out KPI metrics and two matplotlib charts
5. Deploying the finished app to Streamlit Community Cloud for a
   permanent public URL

### The Stakes

Any planner on the Council can open your URL and filter by their own
region. If your query uses f-string interpolation instead of `params=`,
a malicious user could rewrite your SQL. If your app uses an absolute
path, it will crash the moment you deploy it to the cloud. If you forget
to commit the database file, the deployed app will open to a
`FileNotFoundError`. The technical details of this lab are not
bureaucratic — they are the difference between a dashboard that ships and
one that does not.

---

## Chain of Custody

### Technical Requirements

- Python 3.9+ with pip
- A GitHub account with a **public** repository
- Completion of Lab 08 (you must understand the `municipios.db` schema)

### Evidence Files (Provided)

Located in the [`data/`](data/) directory:

| File | Description |
|---|---|
| `data/municipios.db` | SQLite database from Lab 08 — 4 tables, 78 municipalities |

The database is committed to the repo. You do not need to run any build
script to start the lab.

### Library Constraints (strictly enforced)

| Library | Allowed usage |
|---|---|
| `streamlit` | UI, widgets, layout, plot rendering |
| `pandas` | `pd.read_sql` to receive query results |
| `matplotlib` | `fig, ax = plt.subplots(...)` pattern only |
| `sqlite3` | DB connection inside `@st.cache_resource` only |
| **Not allowed** | `seaborn`, `plotly`, `st.bar_chart`, `altair`, `pd.read_sql` in place of queries |

---

## Local Execution Model

Streamlit is a web server. Running `streamlit run app.py` starts it on
`http://localhost:8501`. Every time you save `app.py`, Streamlit offers
to rerun — click **Rerun** in the browser banner (or press `R`).

**Setup (run once from the `lab09/` directory):**

```bash
pip install -r requirements.txt
```

Then create `app.py` by following [`lab09.md`](lab09.md) and launch it:

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Investigation Phases

Open [`lab09.md`](lab09.md) for the complete step-by-step guide.
Consult [`concepts.md`](concepts.md) for technical background.

### Phase 1: Hello, Dashboard (20 min)

**Objective:** Understand the re-run model.

You will write a three-line app, launch it locally, add a sidebar slider,
and observe that moving the slider updates the displayed value without any
button press. That automatic re-execution is the central concept of this
lab.

### Phase 2: The Data Layer (30 min)

**Objective:** Connect to the database with cached resources and
parameterized queries.

You will:
- Open a connection with `@st.cache_resource` (runs once per session)
- Load region names with `@st.cache_data` (cached DataFrame)
- Build the first parameterized `WHERE IN` query driven by a multiselect
- Add the `st.stop()` guard for the empty-filter edge case

**Key insight:** `params=selected` is not the same as interpolating
`selected` into the SQL string. One is safe; the other is a security
vulnerability.

### Phase 3: Layout and Filters (30 min)

**Objective:** Wire all three sidebar widgets to queries; build the KPI
row.

You will add the top-N slider and the text search input, incorporate
them into queries, and display three `st.metric` cards whose values
change when filters change.

**Key insight:** `st.stop()` is what separates a graceful "no regions
selected" warning from a cryptic SQL syntax error.

### Phase 4: The Plots (30 min)

**Objective:** Add two matplotlib charts that re-render with every
filter change.

You will produce a horizontal bar chart of the top-N municipalities and
a vertical bar chart of per-region totals, both fed by already-fetched
DataFrames. You will call `plt.close(fig)` after each `st.pyplot` to
prevent figure accumulation across re-runs.

**Key insight:** Every `fig` object must be explicitly closed. Without
`plt.close`, Streamlit accumulates open figures in memory with each
widget interaction.

### Phase 5: Permanent Deployment (25 min)

**Objective:** Produce a `*.streamlit.app` URL that is accessible from
anywhere, not just your local machine.

You will verify `requirements.txt`, confirm the database is committed,
push to a public GitHub repo, and deploy on Streamlit Community Cloud.
The final smoke test must pass in a private/incognito browser tab (no
login required).

---

## Wrap-Up

After completing all phases, you should be able to answer:

- What triggers a full top-to-bottom re-run of `app.py`?
- Why does the connection need `@st.cache_resource` but the region list
  only needs `@st.cache_data`?
- Why does `localhost:8501` disappear when you close your terminal, but
  the `streamlit.app` URL stays up?
- What four changes would you make to `app.py` to start your final
  project?

**Before submitting:**

- [ ] Live `*.streamlit.app` URL pasted into `submission.md`
- [ ] Both charts re-render when region filter changes
- [ ] Search input returns results and handles the empty-result case
- [ ] `st.stop()` guard present
- [ ] No absolute paths in `app.py` — use `"data/municipios.db"`
- [ ] `data/municipios.db` committed to the repo
- [ ] Reflection prompts answered in `submission.md`
- [ ] AI Usage Appendix included if applicable

---

## Submission Requirements

### 1. App

- [`app.py`](app.py) — complete Streamlit dashboard, runs without
  errors on Streamlit Cloud

### 2. Documentation

Complete [`submission.md`](submission.md) with:

- Live Streamlit Cloud URL
- Smoke test evidence (screenshot or description)
- Answers to the four wrap-up reflection prompts

---

## Evaluation Rubric

| Component | Points | Criteria |
|---|---|---|
| **Phase 1 — Streamlit basics** | 10 | App runs locally; re-run model explained correctly |
| **Phase 2 — Data layer** | 15 | `@st.cache_resource` connection; `params=` queries; `st.stop()` guard present |
| **Phase 3 — Layout and filters** | 20 | All three widgets wired to queries; KPI row renders correct values |
| **Phase 4 — Plots** | 20 | Two matplotlib plots re-render on filter change; `plt.close(fig)` present; no `plt.show()` |
| **Phase 5 — Deployment** | 25 | Permanent `*.streamlit.app` URL works without login; no absolute paths; DB committed |
| **Reflection** | 10 | All four wrap-up questions answered with specific references to code |
| **Total** | **100** | |

**Bonus (+5):** Add a `delta=` argument to each `st.metric`. Compute
the difference between the currently filtered value and the all-regions
baseline and pass it as `delta=`. Both the metric and the colored
arrow must render correctly when regions are filtered.

---

## Tips for Success

1. **The re-run model is not optional background.** Widgets do not call
   callbacks — they return values. Every widget change re-runs the
   entire script. Once you understand this, caching and `st.stop()` are
   obvious; without it, they seem arbitrary.

2. **Edit `app.py` directly in your editor.** Save the file and click
   **Rerun** in the browser. Keep only one copy — do not duplicate it.

3. **Test the empty-filter case before Phase 5.** Deselect all regions.
   The app should show a warning and stop — not a red stack trace. If
   you see a stack trace, your `st.stop()` guard is missing or in the
   wrong place.

4. **The absolute-path trap is real.** If your connection string is
   `sqlite3.connect("/home/yourname/lab09/data/municipios.db")`, your
   Streamlit Cloud deploy will fail with `FileNotFoundError`. Use
   `"data/municipios.db"` — relative to wherever `app.py` lives.

5. **Use `layout="wide"` in `st.set_page_config`.** Without it, charts
   will be narrow and the KPI row will wrap. This one setting makes the
   difference between a dashboard that looks professional and one that
   looks like a notebook printout.

---

## Resources

- Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
- `st.cache_resource` vs `st.cache_data`:
  [docs.streamlit.io/develop/concepts/architecture/caching](https://docs.streamlit.io/develop/concepts/architecture/caching)
- Streamlit Community Cloud deployment guide:
  [docs.streamlit.io/deploy/streamlit-community-cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud)
