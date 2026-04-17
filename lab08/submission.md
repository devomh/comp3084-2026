# Lab 08 Submission: The Query Room

**Student Name:** [Your Name]
**Date:** [Date]

## Section A: Schema (Phase 1)

### Tables present in `data/municipios.db`
[List the four table names returned by the `sqlite_master` query]

### Schema Diagram
[Draw the four tables and the foreign-key relationships between them.
ASCII art or a Mermaid diagram is fine. Show at minimum:
- `municipio.region_id → region.id`
- `demografia.municipio_id → municipio.id`
- `consumo.municipio_id → municipio.id` (note: no FK enforced — this is
  why the orphan row survives)]

```
[your diagram here]
```

---

## Section B: Filtering and Ranking (Phase 2)

### Exercise 2.1 — Count above 50k
- Count: ______
- Matches Lab 06 result? [ ] Yes [ ] No

### Exercise 2.2 — Metro region, 20k–60k
[Paste the result list]

### Exercise 2.3 — `LIKE '%ue%'`
[Paste the result list]

Anomaly municipality present: ______

### Exercise 2.4 — Top 10 by population
| Rank | Municipio | Población |
|------|-----------|-----------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |
| 7 | | |
| 8 | | |
| 9 | | |
| 10 | | |

---

## Section C: Aggregation (Phase 3)

### Exercise 3.1 — Total population per region
| Region | Total |
|--------|-------|
| | |
| | |
| | |
| | |
| | |
| | |

### Exercise 3.3 — `HAVING` vs `WHERE`
Regions with average municipal population > 30,000:

| Region | Average Population |
|--------|--------------------|
| | |

Error message returned when the condition was placed in `WHERE`:
```
[paste the error here]
```

Why `WHERE` cannot reference an aggregate (one sentence):
[your answer]

---

## Section D: Joins (Phase 4)

### Exercise 4.2 — Coastal vs Interior
| `costa` | `total_kwh` |
|---------|-------------|
| 0 (interior) | |
| 1 (coastal)  | |

Why is the interior total so much smaller than the coastal total?
[your answer — hint: count the coastal vs interior regions]

### Exercise 4.3 — Orphan row
Rows returned by the `LEFT JOIN ... WHERE m.id IS NULL` query:

| `municipio_id` | `mes` | `consumo_kwh` |
|----------------|-------|---------------|
| | | |

Number of rows `INNER JOIN` silently hid: ______

**Danger of trusting `INNER JOIN` when data integrity is unknown**
(2–3 sentences):
[your answer]

---

## Section E: Critical Incident — Re-finding Vieques (Phase 5)

### The CTE Query
```sql
[paste the CTE query from Exercise 5.1 here]
```

### Top 10 Per-Capita Annual kWh
| Municipio | Total kWh | Población | kWh per Cap |
|-----------|-----------|-----------|-------------|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

Top row (expected: Vieques with kwh_per_cap ≈ 14.5): ______

### Why the CTE form is cleaner than a nested subquery
[one sentence]

### Why Vieques stands out
[one sentence — you already know this from Lab 06]

---

## Section F: Wrap-Up Reflections

1. Which of the three tools (pandas / PySpark / SQL) would you reach
   for first for each canonical question, and why?
   [your answer]

2. Where did `HAVING` vs `WHERE` trip you up, if it did?
   [your answer]

3. What happened to the orphan row in your `INNER JOIN`?
   [your answer]

---

## Section G: Bonus (if attempted)

### Self-Join: Month-over-Month Change
[Paste the query and one insight it revealed]

---

## Section H: AI Usage (if applicable)

### Tool Used
[Name of AI tool]

### Methodology
[How did you use it? What was your approach?]

### The Prompt
[Paste the prompt you used]

### The Output
[Summarize what the AI gave you]

### Human Value-Add
[What did you verify, correct, or improve?]
