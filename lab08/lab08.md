# Lab 08: The Query Room -- Lab Notebook
**Declarative Analysis with SQL, SQLite, and JupySQL**

---

## Introduction

Welcome back to the Municipal Intelligence Division. You are now a
**Municipal Data Analyst / SQL Investigator**. The datasets you worked with
in Lab 06 have been archived into a SQLite database: `data/municipios.db`.
Your new colleague cannot write pandas yet, but she needs the same answers
you produced last semester — in SQL.

Your mission has five parts:

1. **Open** the archive and inventory its schema
2. **Re-answer** Lab 06's filter and ranking questions in SQL
3. **Aggregate** with `GROUP BY`, and learn why `HAVING` is not the same
   as `WHERE`
4. **Combine** tables with `INNER JOIN` and `LEFT JOIN`, including a
   three-table join
5. **Re-find** the Vieques anomaly using a CTE (`WITH`) — the SQL form of
   an intermediate pandas DataFrame

**Constraints:** You may use `jupysql`, `pandas` (only for plot helpers),
and `matplotlib` (only inside the helper cell). Do not use `pd.read_sql`
or any ORM — the SQL must be visible on the page.

**Reference:** Consult [`concepts.md`](concepts.md) for the full explanation
of declarative vs imperative querying, `WHERE` vs `HAVING`, `INNER` vs
`LEFT JOIN`, and CTEs.

---

## Setup

Run these three cells first. Every later cell depends on them.

```python
!pip install -q jupysql pandas matplotlib
```

```python
%load_ext sql
%config SqlMagic.autopandas = False
%config SqlMagic.feedback = False
%config SqlMagic.displaycon = False
%sql sqlite:///data/municipios.db
```

```python
import matplotlib.pyplot as plt


def bar(df, x, y, title=None, highlight=None):
    """Simple bar chart. Highlighted row drawn in red, rest in steelblue."""
    colors = ['crimson' if str(v) == str(highlight) else 'steelblue' for v in df[x]]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df[x], df[y], color=colors)
    ax.set_xlabel(x); ax.set_ylabel(y)
    if title: ax.set_title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout(); plt.show()


def compare(df, x, y, group, title=None):
    """Grouped bar chart. `group` column controls color; `x` is the category axis."""
    fig, ax = plt.subplots(figsize=(8, 4))
    palette = {v: c for v, c in zip(sorted(df[group].unique()),
                                     ['steelblue', 'darkorange', 'seagreen', 'crimson'])}
    ax.bar([str(v) for v in df[x]], df[y], color=[palette[v] for v in df[group]])
    ax.set_xlabel(x); ax.set_ylabel(y)
    if title: ax.set_title(title)
    plt.tight_layout(); plt.show()
```

---

## Phase 1: The Archive Room

Before you query, you must know what is in the box.

### Exercise 1.1: List the Tables

```python
%%sql
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;
```

**Task:** Record the four table names in [`submission.md`](submission.md).

### Exercise 1.2: Inspect Each Table's Columns

`PRAGMA` is SQLite's introspection command — it is not portable SQL.
`PRAGMA table_info('t')` returns one row per column with its name, type,
nullability, default, and primary-key position. Other databases use
`information_schema.columns` (Postgres, MySQL) or `DESCRIBE t` for the
same purpose.

```python
%sql PRAGMA table_info('region');
```

```python
%sql PRAGMA table_info('municipio');
```

```python
%sql PRAGMA table_info('demografia');
```

```python
%sql PRAGMA table_info('consumo');
```

**Task:** In [`submission.md`](submission.md), draw the schema (ASCII art
or Mermaid) showing all four tables and the foreign-key relationships
between them.

### Exercise 1.3: Three Warm-Up `SELECT`s

```python
%sql SELECT * FROM municipio LIMIT 5;
```

```python
%sql SELECT * FROM region;
```

```python
%sql SELECT * FROM consumo LIMIT 5;
```

Capture a result into a Python variable using the `<<` operator:

```python
%sql sample << SELECT * FROM municipio LIMIT 5;
```

```python
type(sample)
```

```python
sample.DataFrame().head()
```

**Checkpoint:** `sample` should be a `ResultSet`, and
`sample.DataFrame()` should return a pandas DataFrame.

---

## Phase 2: Filtering and Ranking

Re-answering Lab 06 questions, this time in SQL.

### Exercise 2.1: Count Municipalities Above a Population Threshold

```python
%%sql
SELECT COUNT(*) AS n_big
FROM municipio
WHERE poblacion > 50000;
```

**Task:** Compare this count with your Lab 06 result. Record it in
[`submission.md`](submission.md).

### Exercise 2.2: Compound Condition with a Scalar Subquery

Find municipalities in the Metro region whose population is between
20,000 and 60,000. We use a **scalar subquery** to look up the Metro
region's id without hard-coding it.

```python
%%sql
SELECT nombre, poblacion
FROM municipio
WHERE poblacion BETWEEN 20000 AND 60000
  AND region_id = (SELECT id FROM region WHERE nombre = 'Metro')
ORDER BY poblacion DESC;
```

**Task:** Paste the result list into [`submission.md`](submission.md).

### Exercise 2.3: Pattern Match with `LIKE`

```python
%%sql
SELECT nombre
FROM municipio
WHERE nombre LIKE '%ue%'
ORDER BY nombre;
```

**Task:** Which well-known anomaly municipality appears in this list?

### Exercise 2.4: Top 10 by Population

```python
%sql top10 << SELECT nombre, poblacion FROM municipio ORDER BY poblacion DESC LIMIT 10;
```

```python
top10
```

```python
bar(top10.DataFrame(), 'nombre', 'poblacion',
    title='Top 10 municipalities by population')
```

**Verification:** your top 10 list must match the Lab 06
`df.nlargest(10, 'poblacion')` output.

---

## Phase 3: Aggregation

`GROUP BY` plus the `WHERE` vs `HAVING` distinction.

### Exercise 3.1: Total Population per Region

This is your first join: `municipio` to `region`.

```python
%%sql region_pop <<
SELECT r.nombre AS region, SUM(m.poblacion) AS total
FROM municipio m
JOIN region r ON m.region_id = r.id
GROUP BY r.nombre
ORDER BY total DESC;
```

```python
region_pop
```

```python
bar(region_pop.DataFrame(), 'region', 'total',
    title='Total population per region')
```

### Exercise 3.2: Multiple Aggregates at Once

```python
%%sql
SELECT r.nombre AS region,
       COUNT(*)        AS n,
       AVG(m.poblacion) AS avg_pop,
       MIN(m.poblacion) AS min_pop,
       MAX(m.poblacion) AS max_pop
FROM municipio m
JOIN region r ON m.region_id = r.id
GROUP BY r.nombre
ORDER BY avg_pop DESC;
```

### Exercise 3.3: `HAVING` vs `WHERE`

Find regions whose *average* municipal population exceeds 30,000.

```python
%%sql
SELECT r.nombre AS region, AVG(m.poblacion) AS avg_pop
FROM municipio m
JOIN region r ON m.region_id = r.id
GROUP BY r.nombre
HAVING AVG(m.poblacion) > 30000
ORDER BY avg_pop DESC;
```

Now try the same condition as a `WHERE` clause. **Type this query
into a new cell yourself** — the notebook does not run it for you
because it raises an error on purpose:

    -- Intentionally wrong: an aggregate inside WHERE.
    SELECT r.nombre AS region, AVG(m.poblacion) AS avg_pop
    FROM municipio m
    JOIN region r ON m.region_id = r.id
    WHERE AVG(m.poblacion) > 30000
    GROUP BY r.nombre;

**Task:** Run the wrong query in your own scratch cell, copy the error
message into [`submission.md`](submission.md), and explain in one
sentence why `WHERE` cannot reference an aggregate.

### Exercise 3.4: Histogram of Municipal Populations

```python
%sql popdist << SELECT poblacion FROM municipio;
```

```python
plt.figure(figsize=(8, 4))
plt.hist(popdist.DataFrame()['poblacion'], bins=20, color='steelblue')
plt.xlabel('poblacion'); plt.ylabel('count')
plt.title('Distribution of municipal populations')
plt.tight_layout(); plt.show()
```

---

## Phase 4: Joins

Two-table and three-table joins; `INNER` vs `LEFT`.

### Exercise 4.1: Two-Table INNER JOIN

Consumption rows with readable municipality names.

```python
%%sql
SELECT m.nombre, c.mes, c.consumo_kwh
FROM consumo c
INNER JOIN municipio m ON c.municipio_id = m.id
ORDER BY c.mes, m.nombre
LIMIT 20;
```

### Exercise 4.2: Three-Table INNER JOIN — Coastal vs Interior

Annual consumption split by coastal (`costa = 1`) vs interior
(`costa = 0`) regions.

```python
%%sql coast_v_interior <<
SELECT r.costa, SUM(c.consumo_kwh) AS total_kwh
FROM consumo c
JOIN municipio m ON c.municipio_id = m.id
JOIN region r   ON m.region_id    = r.id
GROUP BY r.costa;
```

```python
coast_v_interior
```

```python
compare(coast_v_interior.DataFrame(), 'costa', 'total_kwh', group='costa',
        title='Annual consumption: coastal (1) vs interior (0)')
```

**Task:** Why is the interior total so much smaller than the coastal
total? (Hint: re-read `concepts.md` and think about how many regions
are coastal vs interior.)

### Exercise 4.3: LEFT JOIN — Finding the Orphan

The inner join in Ex 4.1 quietly dropped some rows. Let's see which
ones by using a `LEFT JOIN` and filtering for the unmatched side.

```python
%%sql
SELECT c.municipio_id, c.mes, c.consumo_kwh, m.nombre
FROM consumo c
LEFT JOIN municipio m ON c.municipio_id = m.id
WHERE m.id IS NULL;
```

**Task:** How many rows does `INNER JOIN` silently hide? Answer in
[`submission.md`](submission.md) and write 2–3 sentences on the danger
of trusting an `INNER JOIN` when data integrity is unknown.

---

## Phase 5: Critical Incident — Re-finding Vieques

One CTE + aggregation + ranking, reproducing the Lab 06 anomaly.

### Exercise 5.1: The CTE Query

```python
%%sql anomaly <<
WITH annual AS (
    SELECT municipio_id, SUM(consumo_kwh) AS total_kwh
    FROM consumo
    WHERE municipio_id IN (SELECT id FROM municipio)
    GROUP BY municipio_id
)
SELECT m.nombre, a.total_kwh, m.poblacion,
       ROUND(a.total_kwh * 1.0 / m.poblacion, 2) AS kwh_per_cap
FROM annual a
JOIN municipio m ON a.municipio_id = m.id
ORDER BY kwh_per_cap DESC
LIMIT 10;
```

```python
anomaly
```

### Exercise 5.2: Visualize with Vieques Highlighted

```python
bar(anomaly.DataFrame(), 'nombre', 'kwh_per_cap',
    highlight='Vieques', title='Per-capita annual kWh (top 10)')
```

**Task:** In [`submission.md`](submission.md), copy the CTE query and
write one sentence on:

- Why Vieques stands out (you already know this from Lab 06)
- Why the CTE form (`WITH annual AS ...`) is cleaner than writing the
  subquery inline

---

## Phase 6: Optional Bonus

### Bonus: Month-over-Month Change via Self-Join

Join `consumo` to itself to compute the consumption delta between
consecutive months for each municipality.

```python
%%sql
SELECT m.nombre,
       c1.mes AS mes_actual,
       c1.consumo_kwh AS actual,
       c2.consumo_kwh AS anterior,
       ROUND(c1.consumo_kwh - c2.consumo_kwh, 1) AS delta
FROM consumo c1
JOIN consumo c2 ON c1.municipio_id = c2.municipio_id
              AND c1.mes = '2024-07' AND c2.mes = '2024-06'
JOIN municipio m ON c1.municipio_id = m.id
ORDER BY delta DESC
LIMIT 10;
```

**Task:** What single insight does the self-join reveal? Record it in
[`submission.md`](submission.md).

---

## Wrap-Up

You have now:

1. Opened a SQLite archive and recovered its schema
2. Re-expressed Lab 06 filter and ranking questions in SQL
3. Used `GROUP BY` with both `WHERE` and `HAVING`, and explained the
   difference
4. Combined two and three tables with `INNER JOIN`, and discovered an
   orphan row with `LEFT JOIN`
5. Re-identified the Vieques anomaly using a CTE

Before submitting:

- [ ] All analysis cells were run and interpreted
- [ ] Notebook runs from top to bottom without errors
- [ ] Schema diagram drawn in [`submission.md`](submission.md)
- [ ] The Phase 5 CTE query and its result are in the submission
- [ ] Reflection prompts answered

**Reflection prompts for submission.md:**

1. Which of the three tools (pandas / PySpark / SQL) would you reach
   for first for each canonical question, and why?
2. Where did `HAVING` vs `WHERE` trip you up, if it did?
3. What happened to the orphan row in your `INNER JOIN`?
