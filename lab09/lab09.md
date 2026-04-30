# Lab 09: The Public Dashboard — Lab Guide

**Interactive Dashboards with Streamlit, SQLite, and Matplotlib**

---

## Introduction

Welcome back to the Municipal Intelligence Division. You are now a
**Dashboard Architect / Public Intelligence Officer**. The `municipios.db`
database you built in Lab 08 has everything the Regional Planning Council
needs — but they cannot run a Jupyter notebook. Your mission is to wrap
that database in a web application that any planner can use by opening a
URL in a browser.

Your mission has five parts:

1. **Run** a Streamlit app in Colab and understand the re-run model
2. **Connect** the app to `municipios.db` with cached resources and
   parameterized queries
3. **Wire** sidebar widgets to those queries so every filter change
   updates the data
4. **Add** two matplotlib charts that re-render with every interaction
5. **Deploy** the finished app to Streamlit Community Cloud

**Constraints:** `streamlit`, `pandas`, `matplotlib`, and `sqlite3` only.
No `seaborn`, `plotly`, `st.bar_chart`, or f-string interpolation of user
input into SQL queries.

**Reference:** Consult [`concepts.md`](concepts.md) for the full
explanation of the re-run model, caching, parameterized queries, and
deployment.

---

## Setup

Run these cells once at the start of the lab, in order. Do not skip any.

```python
# Cell 1 — Clone the course repository
!git clone https://github.com/devomh/comp3084-2026.git
```

```python
# Cell 2 — Move into the lab directory (all later paths are relative here)
import os
os.chdir("comp3084-2026/lab09")
```

```python
# Cell 3 — Install Streamlit
!pip install -q streamlit
```

```python
# Cell 4 — Get the localtunnel password (copy the IP address printed here)
!wget -q -O - ipv4.icanhazip.com
```

After Cell 4, keep the printed IP address handy — you will paste it into
the localtunnel "Endpoint IP" box every time you view the app.

---

## Phase 1: Hello, Dashboard

**Goal:** Run a Streamlit app in Colab via localtunnel; understand the
re-run model.

### Exercise 1.1: The Minimal App

Create `app.py` with the `%%writefile` magic and launch it:

```python
%%writefile app.py
import streamlit as st

st.set_page_config(page_title="Municipal Intelligence Dashboard", layout="wide")
st.title("Municipal Intelligence Dashboard")
st.write("Dashboard is running.")
```

```python
# Cell 5 — Launch (keep this cell running for the duration of the lab)
!streamlit run app.py & sleep 3 && npx localtunnel --port 8501
```

When Cell 5 prints `your url is: https://some-words.loca.lt`:

1. Click the link.
2. On the "Friendly Reminder" page, paste the IP from Cell 4 into the
   **Endpoint IP** box and click Submit.
3. The dashboard appears.

**Record the IP address in [`submission.md`](submission.md)** — you will
need it again if Cell 5 is restarted.

### Exercise 1.2: The Re-Run Model

Update the `%%writefile` cell and restart the tunnel to observe the
re-run model:

```python
%%writefile app.py
import streamlit as st

st.set_page_config(page_title="Municipal Intelligence Dashboard", layout="wide")
st.title("Municipal Intelligence Dashboard")

n = st.sidebar.slider("Top N municipalities", 5, 20, 10)
st.write(f"You selected: {n}")
```

Stop Cell 5 (click the stop button) and re-run it. A new `loca.lt` URL
will appear. Open it and move the slider.

The value updates without pressing any button. **This is the re-run
model:** every widget interaction re-executes `app.py` from the first
line to the last. Every variable is recreated. Every `st.write` renders
again. The slider's new value is available on line 7 because line 6 ran
before line 7.

### Exercise 1.3: The Empty-State Constraint

Add a text input and observe what the app renders before the user types
anything:

```python
%%writefile app.py
import streamlit as st

st.set_page_config(page_title="Municipal Intelligence Dashboard", layout="wide")
st.title("Municipal Intelligence Dashboard")

n = st.sidebar.slider("Top N municipalities", 5, 20, 10)
search = st.sidebar.text_input("Search by name (substring)")

st.write(f"Slider value: {n}")
st.write(f"Search term: '{search}'")
```

Restart the tunnel and observe: when `search` is empty (the initial
state), the app still renders — it does not crash. The app must handle
every valid state a widget can be in, including the initial empty state.
This is a design constraint you will apply in Phase 3.

**Deliverable:** A running `app.py` via localtunnel that responds to two
widgets. No database yet.

---

## Phase 2: The Data Layer

**Goal:** Connect to `municipios.db` with cached resources and
parameterized queries.

### Exercise 2.1: Open the Connection (Once)

The `@st.cache_resource` decorator runs the function body **once per
session**, not once per re-run. Without it, a new SQLite connection would
open on every slider move.

```python
%%writefile app.py
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Municipal Intelligence Dashboard", layout="wide")


@st.cache_resource
def get_connection():
    return sqlite3.connect("data/municipios.db", check_same_thread=False)


con = get_connection()

st.title("Municipal Intelligence Dashboard")
st.write(f"Database tables: {pd.read_sql('SELECT name FROM sqlite_master WHERE type=?', con, params=['table'])['name'].tolist()}")
```

Restart the tunnel. The `st.write` line should print
`['region', 'municipio', 'demografia', 'consumo']`.

### Exercise 2.2: Load Static Reference Data

Region names do not change during the session — they are good candidates
for `@st.cache_data`. The leading underscore on `_con` tells Streamlit
not to try to hash the connection object.

```python
%%writefile app.py
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Municipal Intelligence Dashboard", layout="wide")


@st.cache_resource
def get_connection():
    return sqlite3.connect("data/municipios.db", check_same_thread=False)


@st.cache_data
def load_regions(_con):
    return pd.read_sql("SELECT id, nombre FROM region ORDER BY nombre", _con)


con = get_connection()
regions = load_regions(con)

st.title("Municipal Intelligence Dashboard")
st.write("Regions loaded:", regions["nombre"].tolist())
```

Expected output: `['Central', 'Este', 'Metro', 'Norte', 'Oeste', 'Sur']`.

### Exercise 2.3: The First Parameterized Query

Wire a multiselect to a `WHERE IN` query. The widget returns a Python
list; `params=selected` passes that list safely to the database driver —
no f-string interpolation of user values.

```python
%%writefile app.py
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Municipal Intelligence Dashboard", layout="wide")


@st.cache_resource
def get_connection():
    return sqlite3.connect("data/municipios.db", check_same_thread=False)


@st.cache_data
def load_regions(_con):
    return pd.read_sql("SELECT id, nombre FROM region ORDER BY nombre", _con)


con = get_connection()
regions = load_regions(con)

st.title("Municipal Intelligence Dashboard")

# --- Sidebar ---
st.sidebar.header("Filters")
selected = st.sidebar.multiselect(
    "Filter by region",
    regions["nombre"].tolist(),
    default=regions["nombre"].tolist(),
)

# --- Query ---
placeholders = ",".join("?" * len(selected))
df = pd.read_sql(
    f"SELECT m.nombre, r.nombre AS region, m.poblacion, m.area_km2 "
    f"FROM municipio m JOIN region r ON m.region_id = r.id "
    f"WHERE r.nombre IN ({placeholders}) "
    f"ORDER BY m.poblacion DESC",
    con, params=selected
)

st.dataframe(df)
```

Restart the tunnel. Deselect one region — the table updates immediately.

### Exercise 2.4: The `st.stop()` Guard

What happens if you deselect *all* regions? Try it. The `placeholders`
string becomes `""`, the SQL becomes `WHERE r.nombre IN ()`, and SQLite
raises a syntax error that renders as a red stack trace in the browser.

Fix it by adding the guard **before** the query:

```python
if not selected:
    st.warning("Select at least one region from the sidebar.")
    st.stop()
```

Place this block immediately after the `selected = st.sidebar.multiselect(...)` line. `st.stop()` halts
execution — nothing below it renders. Deselect all regions again. You
should now see a yellow warning box, not a stack trace.

**Checkpoint — `app.py` at the end of Phase 2:**

```python
%%writefile app.py
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Municipal Intelligence Dashboard", layout="wide")


@st.cache_resource
def get_connection():
    return sqlite3.connect("data/municipios.db", check_same_thread=False)


@st.cache_data
def load_regions(_con):
    return pd.read_sql("SELECT id, nombre FROM region ORDER BY nombre", _con)


con = get_connection()
regions = load_regions(con)

st.title("Municipal Intelligence Dashboard")
st.markdown("_Explore Puerto Rico's 78 municipalities — filter by region, rank by population, and search by name._")

st.sidebar.header("Filters")
selected = st.sidebar.multiselect(
    "Filter by region",
    regions["nombre"].tolist(),
    default=regions["nombre"].tolist(),
)

if not selected:
    st.warning("Select at least one region from the sidebar.")
    st.stop()

placeholders = ",".join("?" * len(selected))
df = pd.read_sql(
    f"SELECT m.nombre, r.nombre AS region, m.poblacion, m.area_km2 "
    f"FROM municipio m JOIN region r ON m.region_id = r.id "
    f"WHERE r.nombre IN ({placeholders}) "
    f"ORDER BY m.poblacion DESC",
    con, params=selected
)

st.dataframe(df)
```

**Deliverable:** A running app that filters municipalities by region,
shows a live table, and handles the empty-filter case gracefully.

---

## Phase 3: Layout and Filters

**Goal:** Add the remaining sidebar widgets and build the KPI row.

### Exercise 3.1: Add the Top-N Slider and Search Input

Both widgets were previewed in Phase 1. Place them after the multiselect
in the sidebar block:

```python
top_n = st.sidebar.slider("Top N municipalities", min_value=5, max_value=20, value=10)
search = st.sidebar.text_input("Search by name (substring)")
```

### Exercise 3.2: The Ranking Query

The slider value becomes a SQL `LIMIT` parameter. Append `top_n` to the
`params` list — it is the last `?` in the query:

```python
df_top = pd.read_sql(
    f"SELECT m.nombre, r.nombre AS region, m.poblacion "
    f"FROM municipio m JOIN region r ON m.region_id = r.id "
    f"WHERE r.nombre IN ({placeholders}) "
    f"ORDER BY m.poblacion DESC LIMIT ?",
    con, params=selected + [top_n]
)
```

Note: `selected + [top_n]` is just Python list concatenation. The
`placeholders` string still covers only the `selected` values; `[top_n]`
adds one more `?` for the `LIMIT` clause.

### Exercise 3.3: The Text Search Query

Add this **at the bottom of `app.py`**, after the raw data section you
will build shortly. The `LIKE ?` pattern is the SQL equivalent of
`.str.contains()` from Lab 06.

```python
if search:
    df_search = pd.read_sql(
        "SELECT m.nombre, r.nombre AS region, m.poblacion, m.area_km2 "
        "FROM municipio m JOIN region r ON m.region_id = r.id "
        "WHERE m.nombre LIKE ?",
        con, params=[f"%{search}%"]
    )
    st.subheader(f"Search results for '{search}'")
    if len(df_search) == 0:
        st.info("No municipalities match your search.")
    else:
        st.dataframe(df_search, use_container_width=True)
```

The conditional `if search:` means the section only renders when the
user has typed something — matching the empty-state constraint from
Exercise 1.3.

### Exercise 3.4: The KPI Row

`st.columns(3)` splits the main area into three equal columns. Each
column receives its own `st.metric` call.

```python
col1, col2, col3 = st.columns(3)
col1.metric("Municipalities shown", len(df))
col2.metric("Total population", f"{df['poblacion'].sum():,}")
col3.metric(
    "Largest municipality",
    df.iloc[0]["nombre"] if len(df) > 0 else "—",
)
```

Place this **after the guard and after all three queries are fetched**,
and **before any headers or plots**.

**Checkpoint — `app.py` at the end of Phase 3:**

```python
%%writefile app.py
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Municipal Intelligence Dashboard", layout="wide")


@st.cache_resource
def get_connection():
    return sqlite3.connect("data/municipios.db", check_same_thread=False)


@st.cache_data
def load_regions(_con):
    return pd.read_sql("SELECT id, nombre FROM region ORDER BY nombre", _con)


con = get_connection()
regions = load_regions(con)

st.title("Municipal Intelligence Dashboard")
st.markdown("_Explore Puerto Rico's 78 municipalities — filter by region, rank by population, and search by name._")

# --- Sidebar ---
st.sidebar.header("Filters")
selected = st.sidebar.multiselect(
    "Filter by region",
    regions["nombre"].tolist(),
    default=regions["nombre"].tolist(),
)
top_n = st.sidebar.slider("Top N municipalities", min_value=5, max_value=20, value=10)
search = st.sidebar.text_input("Search by name (substring)")

# --- Guard ---
if not selected:
    st.warning("Select at least one region from the sidebar.")
    st.stop()

# --- Queries ---
placeholders = ",".join("?" * len(selected))

df = pd.read_sql(
    f"SELECT m.nombre, r.nombre AS region, m.poblacion, m.area_km2 "
    f"FROM municipio m JOIN region r ON m.region_id = r.id "
    f"WHERE r.nombre IN ({placeholders}) "
    f"ORDER BY m.poblacion DESC",
    con, params=selected
)

df_top = pd.read_sql(
    f"SELECT m.nombre, r.nombre AS region, m.poblacion "
    f"FROM municipio m JOIN region r ON m.region_id = r.id "
    f"WHERE r.nombre IN ({placeholders}) "
    f"ORDER BY m.poblacion DESC LIMIT ?",
    con, params=selected + [top_n]
)

df_region = pd.read_sql(
    f"SELECT r.nombre AS region, SUM(m.poblacion) AS total_pop "
    f"FROM municipio m JOIN region r ON m.region_id = r.id "
    f"WHERE r.nombre IN ({placeholders}) "
    f"GROUP BY r.nombre ORDER BY total_pop DESC",
    con, params=selected
)

# --- KPI Row ---
col1, col2, col3 = st.columns(3)
col1.metric("Municipalities shown", len(df))
col2.metric("Total population", f"{df['poblacion'].sum():,}")
col3.metric(
    "Largest municipality",
    df.iloc[0]["nombre"] if len(df) > 0 else "—",
)

# --- Raw Data ---
st.header("Raw Data")
st.dataframe(df, use_container_width=True)

# --- Search Results ---
if search:
    df_search = pd.read_sql(
        "SELECT m.nombre, r.nombre AS region, m.poblacion, m.area_km2 "
        "FROM municipio m JOIN region r ON m.region_id = r.id "
        "WHERE m.nombre LIKE ?",
        con, params=[f"%{search}%"]
    )
    st.subheader(f"Search results for '{search}'")
    if len(df_search) == 0:
        st.info("No municipalities match your search.")
    else:
        st.dataframe(df_search, use_container_width=True)
```

**Deliverable:** Sidebar with three widgets; main area with a KPI row,
a raw data table, and a conditional search section.

---

## Phase 4: The Plots

**Goal:** Add two matplotlib charts that re-render whenever a filter
changes.

**Rule:** Every plot must use a fresh `fig, ax = plt.subplots(...)` and
must call `plt.close(fig)` immediately after `st.pyplot(fig)`. Do not
use `plt.show()` — it has no effect in Streamlit.

### Exercise 4.1: Top N by Population (Horizontal Bar)

Insert this block **between the KPI row and the Raw Data section**:

```python
import matplotlib.pyplot as plt

st.header(f"Top {top_n} Municipalities by Population")
fig, ax = plt.subplots(figsize=(10, 4))
ax.barh(df_top["nombre"][::-1], df_top["poblacion"][::-1], color="steelblue")
ax.set_xlabel("Population")
ax.set_title(f"Top {top_n} by Population ({', '.join(selected)})")
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)
```

The `[::-1]` slice reverses the DataFrame order so the highest-ranked
municipality appears at the top of the horizontal bar chart (matplotlib
draws bars bottom-to-top by default).

### Exercise 4.2: Population by Region (Vertical Bar)

Insert this block after Plot 1, still before Raw Data:

```python
st.header("Population by Region")
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.bar(df_region["region"], df_region["total_pop"], color="darkorange")
ax2.set_ylabel("Total Population")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
st.pyplot(fig2)
plt.close(fig2)
```

This answers the same question as Lab 06 Phase 3A (`groupby('region')['poblacion'].sum()`) and Lab 08
Exercise 3.1 (`GROUP BY r.nombre`) — now with a sidebar filter that
restricts which regions appear.

### Exercise 4.3: Observation

Move the region multiselect. Observe that **both charts update
simultaneously** — not because they are linked, but because the entire
script re-ran and both plot blocks executed again with the new `selected`
value.

Answer in [`submission.md`](submission.md): What triggers the re-render?
Which Python objects are recreated on each widget change?

**Final `app.py` — the submitted file:**

```python
%%writefile app.py
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Municipal Intelligence Dashboard", layout="wide")


@st.cache_resource
def get_connection():
    return sqlite3.connect("data/municipios.db", check_same_thread=False)


@st.cache_data
def load_regions(_con):
    return pd.read_sql("SELECT id, nombre FROM region ORDER BY nombre", _con)


con = get_connection()
regions = load_regions(con)

st.title("Municipal Intelligence Dashboard")
st.markdown(
    "_Explore Puerto Rico's 78 municipalities — filter by region, "
    "rank by population, and search by name._"
)

# --- Sidebar ---
st.sidebar.header("Filters")
selected = st.sidebar.multiselect(
    "Filter by region",
    regions["nombre"].tolist(),
    default=regions["nombre"].tolist(),
)
top_n = st.sidebar.slider("Top N municipalities", min_value=5, max_value=20, value=10)
search = st.sidebar.text_input("Search by name (substring)")

# --- Guard ---
if not selected:
    st.warning("Select at least one region from the sidebar.")
    st.stop()

# --- Queries ---
placeholders = ",".join("?" * len(selected))

df = pd.read_sql(
    f"SELECT m.nombre, r.nombre AS region, m.poblacion, m.area_km2 "
    f"FROM municipio m JOIN region r ON m.region_id = r.id "
    f"WHERE r.nombre IN ({placeholders}) "
    f"ORDER BY m.poblacion DESC",
    con, params=selected
)

df_top = pd.read_sql(
    f"SELECT m.nombre, r.nombre AS region, m.poblacion "
    f"FROM municipio m JOIN region r ON m.region_id = r.id "
    f"WHERE r.nombre IN ({placeholders}) "
    f"ORDER BY m.poblacion DESC LIMIT ?",
    con, params=selected + [top_n]
)

df_region = pd.read_sql(
    f"SELECT r.nombre AS region, SUM(m.poblacion) AS total_pop "
    f"FROM municipio m JOIN region r ON m.region_id = r.id "
    f"WHERE r.nombre IN ({placeholders}) "
    f"GROUP BY r.nombre ORDER BY total_pop DESC",
    con, params=selected
)

# --- KPI Row ---
col1, col2, col3 = st.columns(3)
col1.metric("Municipalities shown", len(df))
col2.metric("Total population", f"{df['poblacion'].sum():,}")
col3.metric(
    "Largest municipality",
    df.iloc[0]["nombre"] if len(df) > 0 else "—",
)

# --- Plot 1: Top N by Population ---
st.header(f"Top {top_n} Municipalities by Population")
fig, ax = plt.subplots(figsize=(10, 4))
ax.barh(df_top["nombre"][::-1], df_top["poblacion"][::-1], color="steelblue")
ax.set_xlabel("Population")
ax.set_title(f"Top {top_n} by Population ({', '.join(selected)})")
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# --- Plot 2: Population by Region ---
st.header("Population by Region")
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.bar(df_region["region"], df_region["total_pop"], color="darkorange")
ax2.set_ylabel("Total Population")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

# --- Raw Data ---
st.header("Raw Data")
st.dataframe(df, use_container_width=True)

# --- Search Results ---
if search:
    df_search = pd.read_sql(
        "SELECT m.nombre, r.nombre AS region, m.poblacion, m.area_km2 "
        "FROM municipio m JOIN region r ON m.region_id = r.id "
        "WHERE m.nombre LIKE ?",
        con, params=[f"%{search}%"]
    )
    st.subheader(f"Search results for '{search}'")
    if len(df_search) == 0:
        st.info("No municipalities match your search.")
    else:
        st.dataframe(df_search, use_container_width=True)
```

**Deliverable:** Two charts that correctly re-render when sidebar filters
change; `plt.close(fig)` present after each `st.pyplot`.

---

## Phase 5: Permanent Deployment

**Goal:** Produce a `*.streamlit.app` URL that persists after the Colab
session ends.

The localtunnel URL from Phases 1–4 disappears when Cell 5 is stopped.
The Regional Planning Council cannot bookmark a URL that vanishes. This
phase fixes that.

### Exercise 5.1: Download `app.py`

In Colab's file browser (left panel → folder icon), navigate to
`comp3084-2026/lab09/` and right-click `app.py` → **Download**.

Verify the downloaded file matches the Phase 4 final checkpoint above.

### Exercise 5.2: Verify No Absolute Paths

Open the downloaded `app.py` in any text editor. Search for `/content`.
If you find it, replace it with the relative path `data/municipios.db`.

This is the most common cloud deployment failure. Streamlit Cloud does not
have a `/content/` directory.

### Exercise 5.3: Confirm `requirements.txt`

The [`requirements.txt`](requirements.txt) committed to this repo
already contains:

```
streamlit
pandas
matplotlib
```

`sqlite3` is Python's standard library — do not add it here.

### Exercise 5.4: Confirm the Repository Structure

Before pushing, verify the following files exist in the `lab09/` directory
of the course repo (or your own fork):

```
lab09/
├── app.py
├── requirements.txt
└── data/
    └── municipios.db
```

`municipios.db` must be committed. Streamlit Cloud clones the repo and
does not run any build script.

### Exercise 5.5: Deploy on Streamlit Community Cloud

1. Log in at **streamlit.io/cloud** with your GitHub account.
2. Click **New app**.
3. Select the repository (`devomh/comp3084-2026` or your fork) and
   the main branch.
4. Set **Main file path** to `lab09/app.py`.
5. Click **Deploy**. Watch the build log for errors.
6. Once the build finishes, copy the `*.streamlit.app` URL.
7. Paste the URL into [`submission.md`](submission.md).

### Exercise 5.6: Smoke Test

Open the `*.streamlit.app` URL in a **private/incognito browser tab**
(no GitHub login, no IP password):

- [ ] Page loads without error
- [ ] Both charts render with all six regions selected (the default)
- [ ] Deselecting two regions updates both charts and the KPI row
- [ ] Deselecting all regions shows the warning (not a stack trace)
- [ ] Typing "San" in the search box returns results
- [ ] Typing "xyz" in the search box shows the "No municipalities" info
      message

Document the smoke test results in [`submission.md`](submission.md).

**Deliverable:** A permanent `*.streamlit.app` URL that the instructor
can visit without any local setup or IP password.

---

## Wrap-Up

You have now:

1. Run a Streamlit app in Colab via localtunnel
2. Connected it to a SQLite database with cached resources
3. Wired three sidebar widgets to parameterized SQL queries
4. Built a KPI row and two matplotlib charts that re-render on every
   filter change
5. Deployed the app to Streamlit Community Cloud

Before submitting:

- [ ] Live `*.streamlit.app` URL pasted into `submission.md`
- [ ] Both charts re-render when region filter changes
- [ ] Search input returns results and handles empty result gracefully
- [ ] `st.stop()` guard present
- [ ] No absolute paths in `app.py`
- [ ] Smoke test passed and documented
- [ ] Reflection prompts answered in `submission.md`

**Reflection prompts:**

1. What is the re-run model, and why does it require `@st.cache_resource`
   for the database connection?
2. Why does the app call `st.stop()` when no regions are selected, rather
   than letting the query run?
3. The "total population per region" question was answered in Lab 06
   (`groupby`), Lab 08 (`GROUP BY`), and now Lab 09 (parameterized SQL
   in Streamlit). What does each layer add that the previous one lacked?
4. What four changes would you make to `app.py` to start your final
   project with a different dataset?
