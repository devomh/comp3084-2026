# Lab 08: The Query Room

**Concepts**: [![Open Concepts In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/devomh/comp3084-2026/blob/main/lab08/concepts.ipynb)

**Lab08**: [![Open Lab Notebook In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/devomh/comp3084-2026/blob/main/lab08/lab08.ipynb)

## Case Brief

### The Situation

The Municipal Intelligence Division has archived last semester's investigation
into a SQLite database. One row per municipality, one row per region, one row
per monthly consumption reading. A new analyst has joined your team and cannot
write pandas yet — but she still needs answers to the same questions you
answered in Lab 06, and she needs them in SQL.

Your task is to translate the old questions into SQL, to answer two new ones
that require combining tables, and to re-discover the Vieques anomaly using a
CTE instead of a pandas pipeline.

### Your Mission

You are a **Municipal Data Analyst / SQL Investigator** tasked with:

1. Opening the archive (`data/municipios.db`) and inventorying its schema
2. Re-answering Lab 06 filter and ranking questions in SQL
3. Aggregating with `GROUP BY` and separating `WHERE` from `HAVING`
4. Combining tables with `INNER JOIN` (2 and 3 tables) and `LEFT JOIN`
5. Reproducing the Vieques per-capita-consumption anomaly with a CTE

### The Stakes

If your query is wrong but still returns rows, no error will tell you. SQL
lets you ask a precise question, but it will also *silently* answer the wrong
question if your `JOIN` drops rows, your `WHERE` runs before aggregation, or
your `HAVING` was supposed to be a `WHERE`. This lab is about reading your
own queries as carefully as you would read a witness statement.

---

## Chain of Custody

### Technical Requirements

- Completion of Lab 06 (DataFrames, groupby, anomaly detection)
- Completion of Lab 07 (distributed split-apply-combine mental model)
- Python 3.8 or higher
- Python libraries: `jupysql`, `pandas`, `matplotlib`

```bash
pip install jupysql pandas matplotlib
```

**Library Constraints (strictly enforced):**

- **`jupysql`** — Cell magics (`%sql`, `%%sql`) and result capture
- **`pandas`** — Only to receive query results for the inline plot helpers
- **`matplotlib`** — Allowed for the provided `bar`/`compare` helpers and
  the Phase 3 histogram; analysis should still happen in SQL, not pandas
- **No ORM** — no SQLAlchemy Core/ORM beyond the JupySQL connection string
- **No `pd.read_sql`** — the SQL must be visible on the page via `%sql` / `%%sql`

### Evidence Files (Provided)

Located in the [`data/`](data/) directory:

1. **`municipios.db`** — SQLite database with three tables (`region`,
   `municipio`, `consumo`) derived from the Lab 06 CSVs

The database is committed to the repo so you do not need to run
`build_db.py` to start the lab. If you do want to rebuild it:

```bash
# From the lab08/ directory
python build_db.py
```

This reads `../lab06/data/municipios_stats.csv` and
`../lab06/data/consumo_municipal.csv` and regenerates `data/municipios.db`
deterministically.

```bash
# Verify the database is present
ls data/
# Expected: municipios.db
```

---

## Investigation Phases

Open [`lab08.md`](lab08.md) (or [`lab08.ipynb`](lab08.ipynb) in Jupyter/Colab)
for the guided exercises. Consult [`concepts.md`](concepts.md) for technical
background.

### Phase 1: The Archive Room (20 min)

**Objective:** Open the database and inventory its schema.

You will:

- Load JupySQL and connect to `sqlite:///data/municipios.db`
- List all tables via `sqlite_master`
- Inspect each table's columns with `PRAGMA table_info(...)`

**Key insight:** Before you query, you must know what is in the box.

### Phase 2: Filtering and Ranking (30 min)

**Objective:** Re-answer Lab 06's filter questions in SQL.

You will:

- Count municipalities with `WHERE poblacion > 50000`
- Use a scalar subquery to filter by a named region
- Match names with `LIKE` (including a write-your-own `San%` prefix query)
- Rank the top 10 municipalities by population and plot them

**Key insight:** `SELECT ... WHERE ... ORDER BY ... LIMIT` is the same
operation as `df[df['col'] > x].nlargest(n, 'col')` in pandas.

### Phase 3: Aggregation (40 min)

**Objective:** Separate `WHERE` from `HAVING` and run multi-aggregate queries.

You will:

- Compute total population per region (first `JOIN` appears here)
- Write your own multi-aggregate query combining `COUNT`, `AVG`, `MIN`, `MAX`
- Use `HAVING` to filter *after* aggregation, plus a write-your-own
  `HAVING MAX(...) > 100000` query
- Plot a population histogram

**Key insight:** `WHERE` filters rows *before* grouping; `HAVING` filters
groups *after* aggregating. The order is not cosmetic.

### Phase 4: Joins (45 min)

**Objective:** Two-table and three-table joins; `INNER` vs `LEFT`.

You will:

1. Join `consumo` to `municipio` to get readable monthly reports
2. Chain a second join to `region` to answer coastal-vs-interior questions
3. Use `LEFT JOIN ... WHERE m.id IS NULL` to find an orphan row the
   `INNER JOIN` silently hid

**Key insight:** `INNER JOIN` drops unmatched rows without warning.
`LEFT JOIN` is how you *notice* what the inner join threw away.

### Phase 5: Critical Incident — Re-finding Vieques (30 min)

**Objective:** Use a CTE (`WITH`) to rank per-capita consumption and
reproduce the Lab 06 anomaly.

You will:

- Write a `WITH annual AS (...)` clause that sums consumption per
  municipio
- Join it to `municipio` and compute `kwh_per_cap`
- Order descending and plot the top 10 with Vieques highlighted
- Explain in one sentence why the CTE form is cleaner than a flat
  `GROUP BY`

**Key insight:** A CTE is "compute once, name it, then query the name."
It is the SQL equivalent of assigning an intermediate pandas DataFrame
to a variable.

---

## Wrap-Up

After completing all phases, verify the notebook runs from top to bottom
without errors and that you can answer the following:

- How many rows does `INNER JOIN` drop compared to `LEFT JOIN` on
  `consumo` ↔ `municipio`?
- When would a `HAVING` clause be wrong if expressed as a `WHERE`?
- Which of the three tools (pandas / PySpark / SQL) would you pick for
  the Vieques query, and why?

**Before you leave:**

- Complete all sections of [`submission.md`](submission.md), including
  the CTE query
- Ensure all notebook cells run without errors from top to bottom
- Include your AI Usage Appendix if applicable

---

## Submission Requirements

### 1. Notebook

- [`lab08.ipynb`](lab08.ipynb) — All cells implemented and run without
  errors, top to bottom

### 2. Documentation

Complete [`submission.md`](submission.md) with:

- Phase 2–4 query answers
- The Phase 5 CTE query (copy-pasted) and its top-10 result
- Answers to the three wrap-up reflection prompts

---

## Evaluation Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **Schema literacy (Phase 1)** | 10 | Tables correctly inventoried |
| **Filtering & ranking (Phase 2)** | 15 | Correct `WHERE`, `LIKE`, `ORDER BY`, `LIMIT`; results match Lab 06 |
| **Aggregation with HAVING (Phase 3)** | 20 | Correct `GROUP BY`; `HAVING` vs `WHERE` distinction explained |
| **Two-table joins (Ex 4.1–4.2)** | 20 | `INNER JOIN` on 2 and 3 tables; results explained |
| **LEFT JOIN & orphan reasoning (Ex 4.3)** | 10 | Orphan row found; danger of `INNER JOIN` explained |
| **Critical Incident CTE (Phase 5)** | 15 | Correct `WITH` clause; Vieques identified as top per-capita |
| **Reflection — three dialects** | 10 | Pandas / PySpark / SQL comparison in your own words |
| **Total** | **100** | |

---

## Tips for Success

1. **Read the schema before you query.** Phase 1 of the notebook exists
   for a reason. You cannot write a `JOIN` without knowing the foreign
   key column name.

2. **The query is the artifact on the page.** Plots are unscored. If
   your SQL is right and your chart is ugly, you earn full marks. If
   your chart is pretty and the SQL is wrong, you earn nothing.

3. **`INNER JOIN` lies by omission.** When you are unsure whether every
   row in the "many" side has a match in the "one" side, run a
   `LEFT JOIN ... WHERE ... IS NULL` *first* and look at what is
   missing.

4. **Verify against Lab 06.** You have already answered several of
   these questions in pandas. If your SQL result differs from your
   pandas result, the SQL is wrong — not pandas.

5. **Use `<<` to capture results.** The JupySQL `result << SELECT ...`
   syntax saves the output into a named variable you can convert to a
   DataFrame (`result.DataFrame()`) and pass to the `bar` / `compare`
   helpers.

---

## Resources

- JupySQL quick start:
  [JupySQL docs](https://jupysql.ploomber.io/en/latest/quick-start.html)
- SQLite syntax reference:
  [SQLite SELECT](https://www.sqlite.org/lang_select.html)
- Common Table Expressions — the `WITH` clause:
  [SQLite WITH](https://www.sqlite.org/lang_with.html)

## Questions?

If your query runs but returns the wrong number of rows, do not "just fix
it." Ask yourself: did the `JOIN` drop rows? Did the `GROUP BY` collapse
rows you needed? Did the `WHERE` run before the aggregation instead of
after? The query is usually answering a different question than the one
you meant to ask.
