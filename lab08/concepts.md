# Lab 08 Field Manual: The Query Room

**Declarative Analysis with SQL, SQLite, and JupySQL**

This document is your technical reference for Lab 08. It explains what SQL is,
why declarative querying is a different mental model from the pandas and
PySpark code you have already written, and how to run queries directly from
a Jupyter cell with JupySQL.

You will learn every concept on a **tiny toy database** (6 students, 20
grades) that fits in your head. Every concept shows a runnable query. A
handful of concepts also include a short practice question — try to write
the query before you peek at the answer. When you are done here, open
[`lab08.md`](lab08.md) and apply the same ideas to a real dataset.

---

## Setup

Run these cells first. They install JupySQL, connect to an **in-memory**
SQLite database, and create the two toy tables.

```python
!pip install -q jupysql pandas matplotlib mermaid-py
```

```python
from mermaid import Mermaid

%load_ext sql
%config SqlMagic.autopandas = False
%config SqlMagic.feedback = False
%config SqlMagic.displaycon = False
%config SqlMagic.displaylimit = 30
%sql sqlite://
```

The empty path after `sqlite://` means *in-memory database* — nothing is
written to disk, and when the kernel restarts the tables are gone.

### Build the toy database

```python
%%sql
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS grades;

CREATE TABLE students (
    id   INTEGER PRIMARY KEY,
    name TEXT    NOT NULL,
    gpa  REAL,
    dob  TEXT
);

INSERT INTO students (id, name, gpa, dob) VALUES
    (1, 'Ana García',    3.85, '2003-05-14'),
    (2, 'Bruno Torres',  3.10, '2004-11-02'),
    (3, 'Carla Méndez',  3.95, '2002-08-21'),
    (4, 'Diego Ruiz',    2.75, '2005-03-09'),
    (5, 'Elena Vargas',  3.50, '2003-12-30'),
    (6, 'Félix Otero',   NULL, '2006-01-18');

CREATE TABLE grades (
    student_id INTEGER,
    exam       TEXT,
    score      INTEGER
);

INSERT INTO grades (student_id, exam, score) VALUES
    (1, 'Exam1', 88), (1, 'Exam2', 92), (1, 'Exam3', 95), (1, 'Exam4', 90),
    (2, 'Exam1', 72), (2, 'Exam2', 68), (2, 'Exam3', 75), (2, 'Exam4', 70),
    (3, 'Exam1', 96), (3, 'Exam2', 94), (3, 'Exam3', 98), (3, 'Exam4', 97),
    (4, 'Exam1', 65), (4, 'Exam2', 70), (4, 'Exam3', 60),
    (5, 'Exam1', 80), (5, 'Exam2', 85), (5, 'Exam3', 82), (5, 'Exam4', 88),
    (99, 'Exam1', 55);
```

Two deliberate oddities live inside these tables:

- **Félix (id=6)** has `gpa IS NULL` and no grades at all — he just enrolled.
- **One grade row** points at `student_id = 99`, who does not exist in
  `students` (an **orphan row**).

These are the seeds for the `IS NULL` and `LEFT JOIN` lessons later on.

Peek at the data:

```python
%sql SELECT * FROM students;
```

```python
%sql SELECT * FROM grades LIMIT 8;
```

---

## Why SQL, and Why Now

By the end of Lab 07 you had answered analytical questions two different
ways: with `df.groupby(...)` in pandas (one machine, one process) and with
`rdd.reduceByKey(...)` or `df.groupBy(...)` in PySpark (many workers, one
shuffle). Both were **imperative** — you described the *steps* the machine
should take.

SQL is **declarative**. You describe the *answer* you want, and the database
engine chooses the plan. `SELECT student_id, AVG(score) FROM grades GROUP
BY student_id` does not tell SQLite how to group rows, which index to use,
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
| Average score per student | `df.groupby('student_id')['score'].mean()` | `df.groupBy('student_id').avg('score')` | `SELECT student_id, AVG(score) FROM grades GROUP BY student_id` |
| Top 3 students by GPA | `df.nlargest(3, 'gpa')` | `df.orderBy(F.desc('gpa')).limit(3)` | `SELECT * FROM students ORDER BY gpa DESC LIMIT 3` |
| Student ranking via intermediate result | `avg = df.groupby(...).mean(); avg.merge(students, ...)` | `avg = df.groupBy(...).agg(...); avg.join(students, ...)` | `WITH avg AS (...) SELECT ... FROM avg JOIN students ...` |

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
    A["Question:<br/>average score per student"] --> B["pandas:<br/>groupby('student_id').mean()"]
    A --> C["PySpark:<br/>groupBy('student_id').avg('score')"]
    A --> D["SQL:<br/>GROUP BY student_id"]
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

## 1. `SELECT ... FROM ...` — Projection

Projects columns out of a table. The list after `SELECT` decides what
columns come back.

```python
%%sql
SELECT name, gpa FROM students;
```

The pandas equivalent is `df[['name', 'gpa']]`. Use `SELECT *` when you
want every column — handy for exploration, avoided in production because
column order then depends on the schema.

---

## 2. `WHERE` — Filter Rows

`WHERE` keeps only rows that satisfy a predicate. It runs on **one row at
a time**, before any grouping, so it cannot reference an aggregate like
`AVG(...)`.

### Numeric comparison

```python
%%sql
SELECT name, gpa
FROM students
WHERE gpa > 3.5;
```

### String pattern with `LIKE`

`%` matches any sequence of characters, `_` matches exactly one.

```python
%%sql
SELECT name
FROM students
WHERE name LIKE 'A%';
```

### Range with `BETWEEN` (dates work too)

SQLite stores dates as ISO text (`'YYYY-MM-DD'`), which sorts and compares
correctly.

```python
%%sql
SELECT name, dob
FROM students
WHERE dob BETWEEN '2003-01-01' AND '2004-12-31'
ORDER BY dob;
```

### `IN` — membership

```python
%%sql
SELECT name, gpa
FROM students
WHERE id IN (1, 3, 5);
```

### `IS NULL` — missing values

`NULL` is not equal to anything, not even to itself. `gpa = NULL` returns
zero rows; you must use `IS NULL` / `IS NOT NULL`.

```python
%%sql
SELECT name
FROM students
WHERE gpa IS NULL;
```

<!-- #region -->
> **Practice 1.** Write a query that returns the `name` and `gpa` of every
> student whose GPA is **at least 3.0**. How many rows do you get, and why
> is Félix *not* in the result?
>
> <details><summary>Answer</summary>
>
> ```sql
> SELECT name, gpa FROM students WHERE gpa >= 3.0;
> ```
>
> Four rows: Ana, Bruno, Carla, Elena. Félix is excluded because his
> `gpa` is `NULL`, and `NULL >= 3.0` is itself `NULL` (not true) — `WHERE`
> only keeps rows where the predicate evaluates to true.
>
> </details>

<!-- #endregion -->

---

## 3. `ORDER BY` and `LIMIT` — Sort and Cap

`ORDER BY` sorts the final result set; `LIMIT n` keeps the first *n* rows
after sorting. You can sort by multiple columns, and each column can have
its own direction.

```python
%%sql
SELECT name, gpa
FROM students
WHERE gpa IS NOT NULL
ORDER BY gpa DESC, name ASC
LIMIT 3;
```

The pandas equivalent is `df.dropna(subset=['gpa']).sort_values(['gpa','name'], ascending=[False, True]).head(3)`.

---

## 4. `DISTINCT` — Deduplicate

`SELECT DISTINCT` removes duplicate rows from the result.

```python
%%sql
SELECT DISTINCT exam FROM grades ORDER BY exam;
```

Useful when a column has a small set of repeated values and you want the
vocabulary (here: the four exam names, plus whatever the orphan row
brings).

---

## 5. Scalar Subquery

A **scalar subquery** is a `SELECT` that returns exactly one value. You
can drop it anywhere an expression is allowed — including inside `WHERE`.

```python
%%sql
SELECT name, gpa
FROM students
WHERE gpa > (SELECT AVG(gpa) FROM students);
```

The inner `SELECT` computes the class-average GPA once; the outer query
compares each student's GPA against it. Without a scalar subquery, you
would have to compute the average in Python first and then paste a literal
number into the SQL — brittle and non-portable.

<!-- #region -->

> **Practice 2.** Write a query that returns every student whose GPA is
> **below** the class average. Hint: the inner subquery does not change.
>
> <details><summary>Answer</summary>
>
> ```sql
> SELECT name, gpa
> FROM students
> WHERE gpa < (SELECT AVG(gpa) FROM students);
> ```
>
> Two rows: Bruno and Diego. Félix is excluded (same `NULL` reason as
> Practice 1).
>
> </details>

<!-- #endregion -->

---

## 6. `GROUP BY` and Aggregates

`GROUP BY` collapses rows that share a key into one row per group. The
`SELECT` list can then use **aggregate functions** that summarize each
group: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.

```python
%%sql
SELECT student_id,
       COUNT(*)   AS n_exams,
       AVG(score) AS avg_score,
       MIN(score) AS min_score,
       MAX(score) AS max_score
FROM grades
GROUP BY student_id
ORDER BY avg_score DESC;
```

The pandas equivalent is `df.groupby('student_id')['score'].agg(['count','mean','min','max'])`.

Notice that `student_id = 99` (the orphan) gets its own group — `GROUP BY`
does not care whether the key points to a real student. That is a
foreshadowing of the `LEFT JOIN` lesson.

---

## 7. `WHERE` vs `HAVING` — The Critical Distinction

`WHERE` filters **rows before grouping**. `HAVING` filters **groups after
aggregation**. The same condition can belong in either place, but only
one is correct for any given question.

### `HAVING`: keep groups whose aggregate matches a condition

"Which students have an average score above 80?"

```python
%%sql
SELECT student_id, AVG(score) AS avg_score
FROM grades
GROUP BY student_id
HAVING AVG(score) > 80
ORDER BY avg_score DESC;
```

### `WHERE`: keep rows whose value matches a condition, *then* group

"Counting only exams the student passed (score > 80), how many such exams
did each student have?"

```python
%%sql
SELECT student_id, COUNT(*) AS n_passed
FROM grades
WHERE score > 80
GROUP BY student_id
ORDER BY n_passed DESC;
```

Both queries look similar, but they answer **different questions**:

- `HAVING AVG(score) > 80` — the student's overall average must exceed 80.
- `WHERE score > 80` — we throw away individual exams below 80, then count
  what's left per student.

### Why you cannot put an aggregate in `WHERE`

~~~sql
-- Intentionally wrong:
SELECT student_id, AVG(score)
FROM grades
WHERE AVG(score) > 80          -- error: aggregate in WHERE
GROUP BY student_id;
~~~

`WHERE` runs once per input row, before grouping has happened — so
`AVG(score)` is not yet defined. SQLite raises
`misuse of aggregate function AVG()`. Move the condition to `HAVING`
(which runs after aggregation) to fix it.

<!-- #region -->

> **Practice 3.** Write a query that returns the **student_id and average
> score** of students whose **worst exam** was still above 70. Which
> clause — `WHERE` or `HAVING` — carries the `MIN(score) > 70`
> condition?
>
> <details><summary>Answer</summary>
>
> ```sql
> SELECT student_id, AVG(score) AS avg_score
> FROM grades
> GROUP BY student_id
> HAVING MIN(score) > 70
> ORDER BY avg_score DESC;
> ```
>
> `HAVING`, because `MIN(score)` is an aggregate — it only has a value
> *after* the group is formed. Two students qualify: Ana and Carla.
>
> </details>

<!-- #endregion -->

---

## 8. `JOIN ... ON ...` — Combine Tables

`JOIN` stitches rows from two tables together when a condition holds. The
`ON` clause makes the matching rule **explicit**.

```python
%%sql
SELECT s.name, g.exam, g.score
FROM students s
INNER JOIN grades g ON s.id = g.student_id
ORDER BY s.name, g.exam
LIMIT 10;
```

The pandas equivalent is
`pd.merge(students, grades, left_on='id', right_on='student_id', how='inner')`.

The `s` and `g` after the table names are **aliases** — shorthand so you
do not have to repeat `students.name` / `grades.score` everywhere.

---

## 9. `INNER` vs `LEFT JOIN`

The most common join confusion.

- **`INNER JOIN`** keeps only rows that match in *both* tables. Unmatched
  rows on either side vanish.
- **`LEFT JOIN`** keeps every row on the left, filling the right side with
  `NULL` when nothing matches.

```python
Mermaid("""
flowchart TD
    subgraph "INNER JOIN students  grades"
        A1["student id=1 (Ana)"] -->|match| B1["4 grade rows<br/>kept"]
        A2["student id=6 (Félix)"] -.->|no grades<br/>dropped| X1["(gone)"]
        G1["grade row<br/>student_id=99"] -.->|no student<br/>dropped| X2["(gone)"]
    end
    subgraph "LEFT JOIN students  grades"
        A3["student id=1 (Ana)"] -->|match| B3["4 grade rows<br/>kept"]
        A4["student id=6 (Félix)"] -->|no grades| B4["kept, exam/score=NULL"]
    end

    style A1 fill:#e1f5ff
    style A2 fill:#e1f5ff
    style A3 fill:#e1f5ff
    style A4 fill:#e1f5ff
    style G1 fill:#e1f5ff
    style X1 fill:#ffe1e1
    style X2 fill:#ffe1e1
    style B1 fill:#90EE90
    style B3 fill:#90EE90
    style B4 fill:#ffe4b5
""")
```

### Demo: `INNER JOIN` silently drops Félix and the orphan

```python
%%sql
SELECT COUNT(*) AS inner_rows
FROM students s
INNER JOIN grades g ON s.id = g.student_id;
```

You will get 19 rows: the 20 grade rows minus the orphan, Félix
contributing zero. Neither Félix nor the orphan produced an error; the
join simply omitted them.

### Demo: `LEFT JOIN` preserves Félix

```python
%%sql
SELECT s.name, g.exam, g.score
FROM students s
LEFT JOIN grades g ON s.id = g.student_id
WHERE s.name = 'Félix Otero';
```

One row comes back — with `NULL` for `exam` and `score`. Félix is
visible; the inner join would have hidden him entirely.

### The orphan probe: `LEFT JOIN ... WHERE ... IS NULL`

To find rows in `grades` whose `student_id` does not match any student,
flip the join direction and filter for the unmatched side:

```python
%%sql
SELECT g.student_id, g.exam, g.score
FROM grades g
LEFT JOIN students s ON g.student_id = s.id
WHERE s.id IS NULL;
```

This is the standard **integrity probe**. When you suspect foreign-key
rot, run it before trusting any `INNER JOIN`.

<!-- #region -->

> **Practice 4.** Write a query that returns the `name` of every student
> who has **no grades at all**. Hint: `LEFT JOIN` from `students` to
> `grades`, then filter for the unmatched side.
>
> <details><summary>Answer</summary>
>
> ```sql
> SELECT s.name
> FROM students s
> LEFT JOIN grades g ON s.id = g.student_id
> WHERE g.student_id IS NULL;
> ```
>
> One row: Félix Otero. The `LEFT JOIN` keeps every student, including
> those with no matching grade rows; the `WHERE ... IS NULL` filter then
> keeps only the students whose right side came back empty.
>
> </details>

<!-- #endregion -->

### When `INNER JOIN` Lies

`INNER JOIN` drops unmatched rows *without telling you*. If your fact
table has a row whose foreign key points nowhere, the inner join will
silently hide it. Your sum will be wrong. Your count will be wrong. No
error will appear.

**Rule of thumb:** when you are not certain every row on the "many" side
has a match on the "one" side, run the `LEFT JOIN ... WHERE ... IS NULL`
probe first to see what is missing.

---

## 10. CTEs (`WITH`) — Compute Once, Reference Twice

A **Common Table Expression** is a named subquery defined at the top of a
statement. It lets you break a complicated query into readable pieces
instead of nesting subqueries three deep.

```python
%%sql
WITH avg_by_student AS (
    SELECT student_id, AVG(score) AS avg_score
    FROM grades
    GROUP BY student_id
)
SELECT s.name, a.avg_score
FROM avg_by_student a
JOIN students s ON a.student_id = s.id
ORDER BY a.avg_score DESC
LIMIT 3;
```

The CTE named `avg_by_student` computes the per-student average once; the
outer query joins it to `students` and ranks the top 3. The pandas
mental model: `avg = df.groupby('student_id')['score'].mean(); avg.merge(students, ...).nlargest(3, 'avg_score')`.

```python
Mermaid("""
flowchart LR
    A["grades<br/>(20 rows)"] --> B["WITH avg_by_student<br/>GROUP BY student_id"]
    B --> C["avg_by_student<br/>(6 rows,<br/>one per student_id)"]
    C --> D["JOIN students"]
    M["students<br/>(6 rows)"] --> D
    D --> E["ORDER BY avg_score DESC<br/>LIMIT 3"]

    style B fill:#e1f5ff
    style C fill:#ffe4b5
    style D fill:#ffe1e1
    style E fill:#90EE90
""")
```

Without the CTE, you would either nest the subquery inline (unreadable
once the query grows) or rank raw fact rows before aggregating (wrong).

<!-- #region -->

> **Practice 5.** Rewrite the CTE query above so that instead of the top
> 3 students, it returns **students whose average score is above the
> overall class average score**. You will need *two* aggregates: one in
> the CTE (per student) and one in the outer query (across all grades).
>
> <details><summary>Answer</summary>
>
> ```sql
> WITH avg_by_student AS (
>     SELECT student_id, AVG(score) AS avg_score
>     FROM grades
>     GROUP BY student_id
> )
> SELECT s.name, a.avg_score
> FROM avg_by_student a
> JOIN students s ON a.student_id = s.id
> WHERE a.avg_score > (SELECT AVG(score) FROM grades)
> ORDER BY a.avg_score DESC;
> ```
>
> Three rows: Carla, Ana, and Elena. The scalar subquery
> `(SELECT AVG(score) FROM grades)` computes the class-wide average once
> and the outer `WHERE` compares each student's CTE-derived average
> against it.
>
> </details>

<!-- #endregion -->

---

## JupySQL Crash-Course

JupySQL is the Jupyter extension that adds the `%sql` and `%%sql` magics
you have been using all along.

| Syntax | What it does |
|---|---|
| `%load_ext sql` | Load the extension (run once per kernel) |
| `%sql sqlite:///path/to/file.db` | Connect to a file-backed database |
| `%sql sqlite://` | Connect to an in-memory database (this file uses this) |
| `%sql SELECT ...` | Run a one-line query; result renders as a table |
| `%%sql` (cell magic) | Run a multi-line query; the rest of the cell is SQL |
| `result << SELECT ...` | Capture the query result into a Python variable |
| `result.DataFrame()` | Convert a captured result to a pandas DataFrame |

Capture example — the `<<` operator:

```python
%sql top << SELECT name, gpa FROM students WHERE gpa IS NOT NULL ORDER BY gpa DESC LIMIT 3;
```

```python
top.DataFrame()
```

Use `<<` whenever you want to plot the result, pass it into Python logic,
or compare it to a pandas DataFrame from an earlier lab. Plain `%sql` or
`%%sql` without capture is fine when you just want to *look*.

---

## Quick Reference Summary

| Concept | Key Point |
|---------|-----------|
| **Declarative vs imperative** | SQL describes the answer; the engine picks the plan |
| **`SELECT`** | Projects columns; the "what do I want back" list |
| **`WHERE`** | Filters rows *before* grouping; cannot use aggregates |
| **`IS NULL`** | The only correct way to test for missing values (not `= NULL`) |
| **`LIKE`** | Pattern match; `%` = any sequence, `_` = one character |
| **`BETWEEN a AND b`** | Inclusive range; works for numbers and ISO dates |
| **`IN (...)`** | Membership check against a fixed list |
| **`ORDER BY`** | Sorts the final result set; can sort by multiple columns |
| **`LIMIT`** | Keeps the first N rows after ordering |
| **`DISTINCT`** | Deduplicate rows in the result |
| **`GROUP BY`** | Collapses rows that share a key |
| **`HAVING`** | Filters groups *after* aggregation; can use aggregates |
| **Scalar subquery** | A `SELECT` that returns one value, usable inside `WHERE` |
| **`INNER JOIN`** | Keeps only matching rows on both sides |
| **`LEFT JOIN`** | Keeps every row on the left; `NULL` for unmatched right side |
| **`ON` clause** | The explicit matching condition of a join |
| **Orphan row** | A foreign-key value with no matching parent — silently dropped by `INNER JOIN` |
| **CTE (`WITH`)** | Named subquery at the top of a statement; compose without nesting |
| **`%sql` / `%%sql`** | JupySQL line and cell magics for running queries |
| **`<<` capture** | Saves a query result into a Python variable |

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

By the end of this field manual, you should be able to answer:

1. How does a `GROUP BY ... HAVING ...` query differ from a `WHERE ...
   GROUP BY ...` query? When would the same condition be wrong in one
   clause but right in the other?
2. Why does `WHERE gpa = NULL` return zero rows, and what do you write
   instead?
3. What silent failure mode does `INNER JOIN` have that `LEFT JOIN` does
   not? How do you detect an orphan row?
4. Why is a CTE cleaner than a deeply nested subquery for multi-step work?
5. What does the `<<` operator in JupySQL do, and when would you use it
   instead of a plain `%%sql` query?

If you can answer those clearly, you are thinking in SQL instead of
translating every query back into pandas in your head.

**Next step:** open [`lab08.md`](lab08.md) and apply these ideas to a
real municipal dataset.
