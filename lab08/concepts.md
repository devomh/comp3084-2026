# Lab 08 Field Manual: The Query Room

**Declarative Analysis with SQL, SQLite, and JupySQL**

This document is your technical reference for Lab 08. It explains what SQL is,
why declarative querying is a different mental model from the pandas and
PySpark code you have already written, and how the JupySQL extension lets you
run queries directly from a Jupyter cell.

The most important section is the three-dialects comparison table. You should
be able to look at a canonical question (for example, "total population per
region") and write it in pandas, PySpark, and SQL. If you can, the tooling
stops being the puzzle and the question takes center stage.

---

## Setup

Run this cell first if you want the Mermaid diagrams in a notebook view.

```python
!pip install -q mermaid-py
```

```python
from mermaid import Mermaid
```

---

## Why SQL, and Why Now

By the end of Lab 07 you had answered analytical questions two different
ways: with `df.groupby(...)` in pandas (one machine, one process) and with
`rdd.reduceByKey(...)` or `df.groupBy(...)` in PySpark (many workers, one
shuffle). Both were **imperative** — you described the *steps* the machine
should take.

SQL is **declarative**. You describe the *answer* you want, and the database
engine chooses the plan. `SELECT region, SUM(poblacion) FROM municipio GROUP
BY region` does not tell SQLite how to group the rows, which index to use,
or in which order to scan the table. SQLite decides. You only stated *what*
you wanted.

This is not a cosmetic difference. Once you can express a question as SQL,
any database — SQLite, Postgres, DuckDB, BigQuery — can answer it without
you rewriting the logic. The query is portable because the *plan* is the
engine's problem, not yours.

---

## Bridge from pandas and PySpark: One Idea, Three Dialects

The single most important table in this lab:

| Question | pandas (Lab 06) | PySpark (Lab 07) | SQL (Lab 08) |
|---|---|---|---|
| Total population per region | `df.groupby('region')['poblacion'].sum()` | `df.groupBy('region').sum('poblacion')` | `SELECT region, SUM(poblacion) FROM municipio GROUP BY region` |
| Top 10 municipalities by population | `df.nlargest(10, 'poblacion')` | `df.orderBy(F.desc('poblacion')).limit(10)` | `SELECT * FROM municipio ORDER BY poblacion DESC LIMIT 10` |
| Per-capita consumption, flagging outliers | `groupby + z-score` in Python | `groupBy` + window function | `WITH annual AS (...) SELECT ... ORDER BY kwh_per_cap DESC` |

The three expressions are **the same operation in three dialects**. What
changes between them:

- **pandas** fits the data in one process's memory and runs immediately.
- **PySpark** distributes the work across partitions and decides when to
  shuffle.
- **SQL** pushes the entire problem to a database engine and lets it pick
  the execution plan.

If you understood `groupby()` in Lab 06, you already understand the *logic*
of `GROUP BY`. The new part is the vocabulary — and the fact that you no
longer describe the plan, only the answer.

```python
Mermaid("""
flowchart LR
    A["Question:<br/>total population per region"] --> B["pandas:<br/>groupby('region').sum()"]
    A --> C["PySpark:<br/>groupBy('region').sum('poblacion')"]
    A --> D["SQL:<br/>GROUP BY region"]
    B --> E["one machine,<br/>one process"]
    C --> F["many workers,<br/>explicit shuffle"]
    D --> G["engine picks<br/>the plan"]

    style A fill:#ffe1e1
    style B fill:#e1f5ff
    style C fill:#e1f5ff
    style D fill:#90EE90
""")
```

---

## The Four SQL Clauses of Interest

Almost every query in this lab is some combination of four clauses.

### `SELECT ... FROM ...`

Projects columns out of a table.

```sql
SELECT nombre, poblacion FROM municipio;
```

The pandas equivalent is `df[['nombre', 'poblacion']]`. The list after
`SELECT` is the **projection** — what columns come back.

### `WHERE`

Filters rows *before* grouping.

```sql
SELECT nombre FROM municipio WHERE poblacion > 50000;
```

The pandas equivalent is `df[df['poblacion'] > 50000]['nombre']`. `WHERE`
acts on individual rows; it cannot reference an aggregate like `SUM(...)`.

### `GROUP BY` and `HAVING`

`GROUP BY` collapses rows that share a key; `HAVING` filters the *groups*
after aggregation.

```sql
SELECT region_id, AVG(poblacion) AS avg_pop
FROM municipio
GROUP BY region_id
HAVING AVG(poblacion) > 30000;
```

The pandas equivalent is
`df.groupby('region_id')['poblacion'].mean().loc[lambda s: s > 30000]`.

**Critical distinction:** `WHERE` runs on rows; `HAVING` runs on groups.
The same condition can belong in either place, but only one is correct:

- `WHERE poblacion > 30000` — keep individual municipios above 30k, *then*
  group.
- `HAVING AVG(poblacion) > 30000` — group first, keep regions whose average
  exceeds 30k.

These return different answers. Pay attention to which one your question is
asking.

### `JOIN ... ON ...`

Combines rows from two tables when a condition holds.

```sql
SELECT m.nombre, r.nombre AS region
FROM municipio m
INNER JOIN region r ON m.region_id = r.id;
```

The pandas equivalent is `pd.merge(municipio_df, region_df, left_on='region_id',
right_on='id')`. SQL makes the join condition **explicit** in the `ON` clause
— there is no ambiguity about which column matches which.

---

## INNER vs LEFT JOIN

The most common join confusion in this lab.

- **`INNER JOIN`** keeps only rows that match in *both* tables. Unmatched
  rows on either side vanish.
- **`LEFT JOIN`** keeps every row on the left, filling the right side with
  `NULL` when nothing matches.

```python
Mermaid("""
flowchart TD
    subgraph "INNER JOIN"
        A1["consumo row<br/>municipio_id=42"] -->|match| B1["municipio id=42<br/>kept"]
        A2["consumo row<br/>municipio_id=999"] -.->|no match<br/>dropped| X1["(gone)"]
    end
    subgraph "LEFT JOIN"
        A3["consumo row<br/>municipio_id=42"] -->|match| B3["municipio id=42<br/>kept"]
        A4["consumo row<br/>municipio_id=999"] -->|no match| B4["kept, municipio=NULL"]
    end

    style A1 fill:#e1f5ff
    style A2 fill:#e1f5ff
    style A3 fill:#e1f5ff
    style A4 fill:#e1f5ff
    style X1 fill:#ffe1e1
    style B1 fill:#90EE90
    style B3 fill:#90EE90
    style B4 fill:#ffe4b5
""")
```

### When `INNER JOIN` Lies

`INNER JOIN` drops unmatched rows *without telling you*. If your fact table
has a row whose foreign key points nowhere (the orphan row in Exercise 4.3),
the inner join will silently hide it. Your sum will be wrong. Your count
will be wrong. No error will appear.

**Rule of thumb:** when you are not certain every row on the "many" side
has a match on the "one" side, run the `LEFT JOIN ... WHERE ... IS NULL`
probe first to see what is missing.

---

## CTEs (`WITH`): Compute Once, Reference Twice

A **Common Table Expression** is a named subquery defined at the top of a
statement. It lets you break a complicated query into readable pieces.

```sql
WITH annual AS (
    SELECT municipio_id, SUM(consumo_kwh) AS total_kwh
    FROM consumo
    GROUP BY municipio_id
)
SELECT m.nombre, a.total_kwh
FROM annual a
JOIN municipio m ON a.municipio_id = m.id
ORDER BY a.total_kwh DESC
LIMIT 10;
```

The CTE named `annual` computes the per-municipio total once; the outer
query then joins it to `municipio` and ranks it. Without the CTE, you
would either nest the subquery inline (unreadable) or rank raw fact rows
before aggregating (wrong).

```python
Mermaid("""
flowchart LR
    A["consumo<br/>(937 rows)"] --> B["WITH annual<br/>GROUP BY municipio_id"]
    B --> C["annual<br/>(78 rows,<br/>total per muni)"]
    C --> D["JOIN municipio"]
    M["municipio<br/>(78 rows)"] --> D
    D --> E["ORDER BY<br/>kwh_per_cap DESC<br/>LIMIT 10"]

    style B fill:#e1f5ff
    style C fill:#ffe4b5
    style D fill:#ffe1e1
    style E fill:#90EE90
""")
```

The pandas mental model: `annual = df.groupby('municipio_id')['kwh'].sum();
result = annual.merge(municipio, ...)`.

---

## JupySQL Crash-Course

JupySQL is a Jupyter extension that adds SQL cell magics.

| Syntax | What it does |
|---|---|
| `%load_ext sql` | Load the extension (run once per kernel) |
| `%sql sqlite:///data/municipios.db` | Connect to a database |
| `%sql SELECT ...` | Run a one-line query; result renders as a table |
| `%%sql` (cell magic) | Run a multi-line query; the rest of the cell is SQL |
| `result << SELECT ...` | Capture the query result into a Python variable |
| `result.DataFrame()` | Convert a captured result to a pandas DataFrame |
| `%sqlplot bar --table result --column x y` | Draw a bar chart from a captured result |

Full example:

```python
%load_ext sql
%config SqlMagic.autopandas = False
%sql sqlite:///data/municipios.db
```

```python
%%sql
SELECT nombre, poblacion
FROM municipio
ORDER BY poblacion DESC
LIMIT 5;
```

```python
top << SELECT nombre, poblacion FROM municipio ORDER BY poblacion DESC LIMIT 10;
%sqlplot bar --table top --column nombre poblacion
```

---

## Quick Reference Summary

| Concept | Key Point |
|---------|-----------|
| **Declarative vs imperative** | SQL describes the answer; the engine picks the plan |
| **`SELECT`** | Projects columns; the "what do I want back" list |
| **`WHERE`** | Filters rows *before* grouping; cannot use aggregates |
| **`GROUP BY`** | Collapses rows that share a key |
| **`HAVING`** | Filters groups *after* aggregation; can use aggregates |
| **`ORDER BY`** | Sorts the final result set |
| **`LIMIT`** | Keeps the first N rows after ordering |
| **`LIKE '%ue%'`** | Pattern match; `%` is any sequence of characters |
| **`DISTINCT`** | Deduplicate rows in the result |
| **Scalar subquery** | A `SELECT` that returns one value, usable inside `WHERE` |
| **`INNER JOIN`** | Keeps only matching rows on both sides |
| **`LEFT JOIN`** | Keeps every row on the left; `NULL` for unmatched right side |
| **`ON clause`** | The explicit matching condition of a join |
| **Orphan row** | A foreign-key value with no matching parent — silently dropped by `INNER JOIN` |
| **CTE (`WITH`)** | Named subquery at the top of a statement; compose without nesting |
| **`%sql` / `%%sql`** | JupySQL line and cell magics for running queries |
| **`<<` capture** | Saves a query result into a Python variable |
| **`%sqlplot`** | One-line chart from a captured result |

### Key Clause Quick Reference

| Clause | Purpose | pandas Equivalent |
|--------|---------|-------------------|
| `SELECT col1, col2 FROM t` | Project columns | `df[['col1', 'col2']]` |
| `WHERE cond` | Filter rows | `df[cond]` |
| `ORDER BY col DESC` | Sort | `df.sort_values('col', ascending=False)` |
| `LIMIT n` | First n rows | `df.head(n)` |
| `GROUP BY col` | Split rows by key | `df.groupby('col')` |
| `HAVING agg(col) > x` | Filter groups | `.loc[lambda s: s > x]` |
| `INNER JOIN t2 ON a=b` | Keep matched rows only | `pd.merge(df1, df2, on='a', how='inner')` |
| `LEFT JOIN t2 ON a=b` | Keep all left-side rows | `pd.merge(df1, df2, on='a', how='left')` |
| `WITH x AS (...)` | Named subquery | `x = df.groupby(...); ...` |
| `COUNT(*)` | Row count per group | `.count()` / `.size()` |
| `SUM(col)` | Sum per group | `.sum()` |
| `AVG(col)` | Mean per group | `.mean()` |
| `MIN(col)` / `MAX(col)` | Min / max per group | `.min()` / `.max()` |

---

## Practical Questions You Should Be Able to Answer

By the end of the lab, you should be able to answer:

1. How does a `GROUP BY ... HAVING ...` query differ from a `WHERE ...
   GROUP BY ...` query?
2. What silent failure mode does `INNER JOIN` have that `LEFT JOIN` does
   not?
3. Why is a CTE cleaner than a nested subquery for multi-step work?
4. If you were given the Vieques per-capita question from scratch, would
   you reach for pandas, PySpark, or SQL first? Why?
5. What does the `<<` operator in JupySQL do, and when would you use it
   instead of a plain `%sql` query?

If you can answer those clearly, you are thinking in SQL instead of
translating every query back into pandas in your head.
