"""Build the SQLite database for Lab 08 from the Lab 06 CSVs.

Creates data/municipios.db with three tables:
    region      (6 rows, hand-curated)
    municipio   (78 rows, from municipios_stats.csv)
    consumo     (937 rows: 936 monthly readings + 1 orphan)

The orphan row (municipio_id=999) is inserted intentionally to give
students a LEFT JOIN teaching moment. Foreign keys are NOT enabled
on the consumo table so the orphan can survive.

Run from lab08/:
    python build_db.py

Dependencies: stdlib only (csv, sqlite3, pathlib).
"""
import csv
import sqlite3
from pathlib import Path

LAB08_DIR = Path(__file__).parent
DATA_DIR = LAB08_DIR / "data"
DB_PATH = DATA_DIR / "municipios.db"

STATS_CSV = LAB08_DIR / ".." / "lab06" / "data" / "municipios_stats.csv"
CONSUMO_CSV = LAB08_DIR / ".." / "lab06" / "data" / "consumo_municipal.csv"

REGIONS = [
    (1, "Metro",   1, "San Juan"),
    (2, "Norte",   1, "Arecibo"),
    (3, "Sur",     1, "Ponce"),
    (4, "Este",    1, "Humacao"),
    (5, "Oeste",   1, "Mayagüez"),
    (6, "Central", 0, "Utuado"),
]

ORPHAN_ROW = (999, "2024-06", 42000.0)

DDL = """
CREATE TABLE region (
    id              INTEGER PRIMARY KEY,
    nombre          TEXT    NOT NULL UNIQUE,
    costa           INTEGER NOT NULL CHECK (costa IN (0,1)),
    capital_region  TEXT    NOT NULL
);

CREATE TABLE municipio (
    id          INTEGER PRIMARY KEY,
    nombre      TEXT    NOT NULL UNIQUE,
    region_id   INTEGER NOT NULL REFERENCES region(id),
    poblacion   INTEGER NOT NULL,
    area_km2    REAL    NOT NULL
);

CREATE TABLE consumo (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    municipio_id    INTEGER NOT NULL,
    mes             TEXT    NOT NULL,
    consumo_kwh     REAL    NOT NULL
);

CREATE INDEX idx_consumo_municipio ON consumo(municipio_id);
"""


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(DDL)

    cur.executemany(
        "INSERT INTO region (id, nombre, costa, capital_region) VALUES (?, ?, ?, ?)",
        REGIONS,
    )

    region_by_name = {r[1]: r[0] for r in REGIONS}

    municipio_id_by_name = {}
    municipio_rows = []
    with open(STATS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            nombre = row["municipio"]
            region_id = region_by_name[row["region"]]
            municipio_id_by_name[nombre] = i
            municipio_rows.append((
                i, nombre, region_id,
                int(row["poblacion"]), float(row["area_km2"]),
            ))

    cur.executemany(
        "INSERT INTO municipio (id, nombre, region_id, poblacion, area_km2) "
        "VALUES (?, ?, ?, ?, ?)",
        municipio_rows,
    )

    consumo_rows = []
    with open(CONSUMO_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            muni_id = municipio_id_by_name[row["municipio"]]
            consumo_rows.append((
                muni_id, row["mes"], float(row["consumo_energia_kwh"]),
            ))

    cur.executemany(
        "INSERT INTO consumo (municipio_id, mes, consumo_kwh) VALUES (?, ?, ?)",
        consumo_rows,
    )
    cur.execute(
        "INSERT INTO consumo (municipio_id, mes, consumo_kwh) VALUES (?, ?, ?)",
        ORPHAN_ROW,
    )

    conn.commit()

    n_region = cur.execute("SELECT COUNT(*) FROM region").fetchone()[0]
    n_municipio = cur.execute("SELECT COUNT(*) FROM municipio").fetchone()[0]
    n_consumo = cur.execute("SELECT COUNT(*) FROM consumo").fetchone()[0]

    n_orphans = cur.execute(
        "SELECT COUNT(*) FROM consumo "
        "WHERE municipio_id NOT IN (SELECT id FROM municipio)"
    ).fetchone()[0]
    n_distinct_regions = cur.execute(
        "SELECT COUNT(DISTINCT region_id) FROM municipio"
    ).fetchone()[0]

    conn.close()

    print(f"Wrote {DB_PATH.relative_to(LAB08_DIR)}")
    print(f"  region:     {n_region} rows")
    print(f"  municipio:  {n_municipio} rows")
    print(f"  consumo:    {n_consumo} rows ({n_consumo - 1} + 1 orphan)")

    if n_orphans != 1:
        print(f"  ! expected 1 orphan, got {n_orphans}")
    if n_distinct_regions != 6:
        print(f"  ! expected 6 distinct regions, got {n_distinct_regions}")


if __name__ == "__main__":
    main()
