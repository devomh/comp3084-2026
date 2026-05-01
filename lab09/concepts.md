# Lab 09 Field Manual: The Public Dashboard

**Interactive Dashboards with Streamlit, SQLite, and Matplotlib**

This document is your technical reference for Lab 09. It explains what
Streamlit is, why it executes differently from a Jupyter notebook, and
how to connect widgets to SQL queries safely. Every concept is illustrated
with a small, self-contained example. When you are done here, open
[`lab09.md`](lab09.md) and apply the same ideas to `municipios.db`.

---

## Setup (concepts examples only)

The examples in this document can be run as a Streamlit app. Save any
example to a file and launch it locally:

```bash
# save the example, then:
streamlit run toy.py
```

Open `http://localhost:8501` in your browser.

---

## 1. The Re-Run Model

This is the one concept that has no parallel in Jupyter. When you move a
slider in Streamlit, **the entire `app.py` script executes again from the
top**. Every variable is recreated. Every query re-runs. Every chart is
redrawn.

Compare this to a Jupyter notebook, where you manually choose which cells
to re-run. In Streamlit you have no choice — a widget interaction always
triggers a complete re-execution.

### Why this matters

```python
import streamlit as st

st.title("Re-run counter")
n = st.sidebar.slider("Pick a number", 1, 10, 5)
st.write(f"You picked: {n}")
st.write("This line also re-executes every time.")
```

Every line from `import streamlit` to the last `st.write` runs when you
move the slider. There is no such thing as a "cell that stays cached"
unless you use the cache decorators described in Section 2.

### The execution order rule

Because the script runs top-to-bottom, **the order of your code is the
order of your UI**. A widget defined on line 10 returns its value to line
11. A `st.dataframe` on line 20 renders below everything defined before
it. You cannot reorder the rendered output without reordering the code.

```python
import streamlit as st

# This slider appears in the sidebar
top_n = st.sidebar.slider("Top N", 3, 10, 5)

# This text appears in the main area, after the slider is read
st.write(f"Showing top {top_n} results")
```

### Bridge from Lab 08

| Lab 08 (SQL notebook) | Lab 09 (Streamlit app) |
|---|---|
| Hard-coded `WHERE region_id = 3` | `st.sidebar.multiselect(...)` return value |
| `%%sql SELECT ...` | `pd.read_sql(query, con, params=[...])` |
| JupySQL result rendered in cell | `st.dataframe(df)` or `st.pyplot(fig)` |
| Re-run cell manually | Re-run triggered automatically on widget change |

---

## 2. Caching: `@st.cache_data` vs `@st.cache_resource`

Without caching, every widget interaction would:
- Open a new database connection
- Re-execute every query, including queries that fetch static data like
  region names

Streamlit provides two decorators that prevent redundant work.

### `@st.cache_resource` — for connections and shared objects

Use this for objects that are **expensive to create** and must be
**shared across all re-runs and all users**: database connections, ML
models, API clients.

```python
import sqlite3
import streamlit as st

@st.cache_resource
def get_connection():
    return sqlite3.connect("data/municipios.db", check_same_thread=False)

con = get_connection()
```

The function body runs **once per Streamlit session**. Every subsequent
call to `get_connection()` returns the same connection object. Without the
decorator, a new connection would open on every slider move.

`check_same_thread=False` is required because Streamlit may call your
functions from a thread other than the one that created the connection.

### `@st.cache_data` — for DataFrames and serializable results

Use this for **data that does not change during the session**: reference
tables, lookup lists, static aggregates.

```python
import pandas as pd

@st.cache_data
def load_regions(_con):
    return pd.read_sql("SELECT id, nombre FROM region ORDER BY nombre", _con)

regions = load_regions(con)
```

The leading underscore on `_con` tells Streamlit not to try to hash the
connection object (connections are not hashable). The returned DataFrame
is cached by the function's argument signature.

### When NOT to cache

Do **not** cache queries that depend on widget values — those must re-run
every time the widget changes. Only cache data that is static for the
entire session.

| Cached | Not cached |
|---|---|
| `load_regions()` — region names never change | `pd.read_sql(... WHERE region IN ?)` — depends on multiselect |
| `get_connection()` — open once, reuse | Any query whose `params` include a widget value |

---

## 3. Widget → Query → Render

Every interactive section of a Streamlit dashboard follows the same
three-step chain. Understanding this chain is understanding Streamlit.

```
Widget          →       Query           →       Render
-----------------------------------------------------------
st.sidebar          pd.read_sql(           st.dataframe(df)
  .multiselect(       query, con,            st.pyplot(fig)
  ...)               params=selected)       st.metric(...)
returns             returns                 renders
selected (list)     df (DataFrame)          in main area
```

### Concrete example

```python
import streamlit as st
import sqlite3
import pandas as pd

@st.cache_resource
def get_connection():
    return sqlite3.connect("data/municipios.db", check_same_thread=False)

con = get_connection()

# Step 1 — Widget: returns a Python list
top_n = st.sidebar.slider("Top N municipalities", 5, 20, 10)

# Step 2 — Query: list becomes a SQL parameter
df = pd.read_sql(
    "SELECT nombre, poblacion FROM municipio ORDER BY poblacion DESC LIMIT ?",
    con, params=[top_n]
)

# Step 3 — Render: DataFrame becomes a table on the page
st.dataframe(df)
```

Move the slider. The query re-runs with the new `top_n`. The table
re-renders with a different number of rows. Three steps, one cycle.

---

## 4. `st.stop()` — The Guard Pattern

When a filter widget produces an invalid state (for example, an empty
multiselect), the query downstream will fail with an SQL syntax error.
`st.stop()` halts script execution at that point and renders nothing
below it.

```python
selected = st.sidebar.multiselect(
    "Filter by region",
    ["Metro", "Norte", "Sur", "Este", "Oeste", "Central"],
    default=["Metro", "Norte", "Sur", "Este", "Oeste", "Central"],
)

if not selected:
    st.warning("Select at least one region from the sidebar.")
    st.stop()

# Nothing below this line runs when selected is empty.
# Without st.stop(), the next line would crash:
placeholders = ",".join("?" * len(selected))   # "?" * 0 = ""  → broken SQL
```

### When to use `st.stop()`

Use it whenever a widget value, if empty or out of range, would produce
a broken query or a meaningless chart. Place it **before the first query
that depends on that widget**. Everything rendered before `st.stop()`
remains visible; everything after it disappears.

---

## 5. Parameterized Queries — Why `params=` and Not f-Strings

The query below is correct:

```python
df = pd.read_sql(
    "SELECT nombre FROM municipio WHERE nombre LIKE ?",
    con,
    params=[f"%{search}%"]
)
```

This version is a security vulnerability:

```python
# WRONG — never do this
df = pd.read_sql(
    f"SELECT nombre FROM municipio WHERE nombre LIKE '%{search}%'",
    con
)
```

If a user types `%'; DROP TABLE municipio; --` into the search box, the
f-string version would execute that as a SQL statement. The `params=`
version passes the input as a **value**, not as SQL syntax — the database
driver escapes it automatically and it cannot alter the query structure.

### The `IN (?)` pattern for lists

SQLite's `?` placeholder is for a single value. For a list you need one
`?` per element:

```python
selected = ["Metro", "Norte"]
placeholders = ",".join("?" * len(selected))   # "?,?"
df = pd.read_sql(
    f"SELECT nombre FROM municipio "
    f"WHERE region_id IN (SELECT id FROM region WHERE nombre IN ({placeholders}))",
    con,
    params=selected
)
```

The f-string is used only to construct the placeholder pattern (`?,?`),
not to embed user values. The actual values go in `params=`.

---

## 6. `plt.close(fig)` — Memory Management Across Re-Runs

In a Jupyter notebook, each cell runs once. In Streamlit, the plot block
runs on every widget change. Without `plt.close`, each re-run creates a
new matplotlib `Figure` object and adds it to matplotlib's internal
registry. After 20 slider moves, there are 20 open figures in memory.
Streamlit will also emit a warning:

```
MatplotlibDeprecationWarning: ... too many open figures
```

The fix is one line after every `st.pyplot`:

```python
fig, ax = plt.subplots(figsize=(10, 4))
ax.barh(df["nombre"], df["poblacion"])
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)   # release the figure immediately after rendering
```

Do not call `plt.show()` — it has no effect in Streamlit and will produce
a blank popup if your environment intercepts it. `st.pyplot(fig)` is the
Streamlit equivalent.

---

## 7. Local vs Cloud

During development you run `streamlit run app.py` on your own machine.
The Streamlit server listens on port 8501 of **your machine**, so
`http://localhost:8501` works in your browser. The moment you close the
terminal the server stops and the URL is gone.

Streamlit Community Cloud is different. It clones your GitHub repository,
installs `requirements.txt`, and keeps the server running 24/7 at a
permanent public URL (`*.streamlit.app`). Anyone with the link can open
it — no local Python needed, no terminal to keep open.

### Ephemeral vs permanent

| Attribute | Local (`localhost:8501`) | Streamlit Cloud (`streamlit.app`) |
|---|---|---|
| Lifetime | Until you close the terminal | Persistent |
| Accessible to others | No — your machine only | Yes — public URL |
| Requires GitHub | No | Yes (public repo) |
| Purpose | Development and iteration | Production / submission |

Use `localhost` during the lab. Use Streamlit Cloud for submission.

---

## 8. Streamlit Cloud Deployment

Streamlit Community Cloud deploys a public GitHub repository. It clones
the repo, installs everything in `requirements.txt`, and runs
`streamlit run <your-app-file>`. There is no server to configure — the
only inputs are the repo URL, the branch, and the path to `app.py`.

### What must be in the repository

```
lab09/
├── app.py              ← entry point
├── requirements.txt    ← Python packages (no SQLite, it is stdlib)
└── data/
    └── municipios.db   ← must be committed; Cloud does not build it
```

### `requirements.txt`

```
streamlit
pandas
matplotlib
```

`sqlite3` is part of Python's standard library — it is not a package and
must not appear here.

### The absolute-path trap

If your connection string uses an absolute path tied to your local
machine:

```python
# Breaks on Cloud — absolute path only exists on your machine
sqlite3.connect("/home/yourname/lab09/data/municipios.db")
```

Streamlit Cloud will fail with `FileNotFoundError` because that path
does not exist on the Cloud server. Use a relative path instead:

```python
# Correct — works locally and on Cloud
sqlite3.connect("data/municipios.db")
```

Streamlit Cloud runs `app.py` from the directory it lives in, so
`"data/municipios.db"` resolves correctly as long as the `data/` folder
is in the same directory as `app.py`.

---

## Quick Reference

| Concept | Key point |
|---|---|
| Re-run model | Every widget interaction re-executes `app.py` top-to-bottom |
| `@st.cache_resource` | Run once per session; for connections and shared objects |
| `@st.cache_data` | Cache DataFrame results; re-runs when inputs change |
| `st.stop()` | Halts execution; use to guard against invalid widget states |
| `params=` | Pass widget values as SQL parameters, never via f-string |
| `plt.close(fig)` | Release figure after `st.pyplot`; prevents memory warnings |
| `localhost:8501` | Ephemeral; gone when you close the terminal |
| `streamlit.app` URL | Permanent; deployed from a public GitHub repo |
| Relative path | Use `"data/municipios.db"`, not an absolute system path |

### Streamlit API used in this lab

| Call | What it does |
|---|---|
| `st.set_page_config(layout="wide")` | Wide layout; call before any other `st.*` |
| `st.title(text)` | Large page title |
| `st.header(text)` | Section heading |
| `st.subheader(text)` | Sub-section heading |
| `st.markdown(text)` | Markdown-formatted text |
| `st.write(value)` | General-purpose output; renders text, numbers, or DataFrames |
| `st.sidebar.header(text)` | Section heading inside the sidebar panel |
| `st.sidebar.multiselect(label, options, default)` | Multi-select widget in sidebar |
| `st.sidebar.slider(label, min, max, value)` | Numeric slider in sidebar |
| `st.sidebar.text_input(label)` | Text input in sidebar |
| `st.columns(n)` | Split main area into n columns |
| `col.metric(label, value, delta)` | KPI card with optional colored delta |
| `st.dataframe(df)` | Scrollable table |
| `st.pyplot(fig)` | Render a matplotlib figure |
| `st.warning(text)` | Yellow warning box |
| `st.info(text)` | Blue info box |
| `st.stop()` | Halt script execution here |

---

## Practical Questions You Should Be Able to Answer

1. A classmate says "I moved the slider but the query didn't re-run."
   What is the most likely cause?
2. Why does `get_connection()` use `@st.cache_resource` while
   `load_regions()` uses `@st.cache_data`?
3. You add `@st.cache_data` to a function that takes `selected` (a list
   from a multiselect) as an argument. Will the cache return a stale
   result when `selected` changes? Why or why not?
4. A user types `'; DROP TABLE municipio; --` into the search box. If
   your query uses `params=[f"%{search}%"]`, what happens? If it uses
   an f-string, what happens?
5. Your app works perfectly locally but crashes on Streamlit Cloud with
   `FileNotFoundError`. What is the most likely cause?

If you can answer those clearly, you understand Streamlit well enough to
adapt `app.py` to your own final project dataset.

**Next step:** open [`lab09.md`](lab09.md) and build the dashboard.
