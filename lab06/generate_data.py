"""Generate synthetic municipal datasets for Lab 06: The Data Lake.

Creates two CSV files in data/:
  - municipios_stats.csv   (78 rows, one per PR municipality)
  - consumo_municipal.csv  (78 x 12 = 936 rows, monthly energy consumption)

The municipios_stats data uses approximate values derived from US Census
and Puerto Rico Instituto de Estadisticas sources. Values are rounded and
lightly jittered to make the dataset synthetic while remaining demographically
plausible.

The consumo_municipal data models monthly energy consumption as proportional
to population, with seasonal variation and random noise. One municipality
(Vieques) is injected with anomalously high consumption to serve as the
Critical Incident detection target.

Dependencies: pandas, numpy
Usage: python generate_data.py
"""
import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(3084)

DATA_DIR = Path(__file__).parent / "data"

# ── All 78 municipalities of Puerto Rico ─────────────────────────────────
# (name, region, approx_population, area_km2)
#
# Regional classification follows a simplified 6-region scheme commonly
# used in PR planning contexts. Population figures are approximate,
# based on 2020 Census / Vintage 2024 estimates, rounded.
# Area figures are from the US Census Bureau TIGER/Line shapefiles.

MUNICIPIOS = [
    # ── Metro (10) ──
    ("San Juan",       "Metro",    318441,  123.9),
    ("Bayamón",        "Metro",    169269,  114.5),
    ("Carolina",       "Metro",    146937,  118.2),
    ("Guaynabo",       "Metro",     84214,   70.3),
    ("Trujillo Alto",  "Metro",     63674,   53.5),
    ("Toa Baja",       "Metro",     75227,   60.2),
    ("Toa Alta",       "Metro",     63927,  109.6),
    ("Cataño",         "Metro",     24888,   12.6),
    ("Canóvanas",      "Metro",     43335,   85.6),
    ("Loíza",          "Metro",     23072,   50.6),
    # ── Norte (11) ──
    ("Arecibo",        "Norte",     81966,  326.2),
    ("Barceloneta",    "Norte",     22585,   47.4),
    ("Camuy",          "Norte",     30982,  119.8),
    ("Dorado",         "Norte",     36141,   59.8),
    ("Florida",        "Norte",     11160,   39.3),
    ("Hatillo",        "Norte",     38648,  108.0),
    ("Manatí",         "Norte",     38235,  117.5),
    ("Morovis",        "Norte",     30577,  100.8),
    ("Quebradillas",   "Norte",     23140,   59.3),
    ("Vega Alta",      "Norte",     34973,   71.7),
    ("Vega Baja",      "Norte",     50023,  119.4),
    # ── Sur (12) ──
    ("Ponce",          "Sur",      126327,  297.8),
    ("Coamo",          "Sur",       37596,  202.2),
    ("Guayama",        "Sur",       37232,  168.3),
    ("Guayanilla",     "Sur",       17623,   66.4),
    ("Juana Díaz",     "Sur",       44423,  155.6),
    ("Peñuelas",       "Sur",       17977,  117.2),
    ("Salinas",        "Sur",       25430,  180.0),
    ("Santa Isabel",   "Sur",       21209,   88.3),
    ("Villalba",       "Sur",       21342,   92.5),
    ("Yauco",          "Sur",       33575,  176.6),
    ("Arroyo",         "Sur",       16926,   39.1),
    ("Patillas",       "Sur",       15509,  120.7),
    # ── Este (12) ──
    ("Humacao",        "Este",      50653,  114.9),
    ("Ceiba",          "Este",      10904,   74.5),
    ("Culebra",        "Este",       1714,   30.1),
    ("Fajardo",        "Este",      30476,   77.3),
    ("Juncos",         "Este",      37165,   68.5),
    ("Las Piedras",    "Este",      36110,   87.0),
    ("Luquillo",       "Este",      17665,   67.0),
    ("Maunabo",        "Este",      10321,   54.8),
    ("Naguabo",        "Este",      25070,  134.8),
    ("Río Grande",     "Este",      47292,  157.1),
    ("Vieques",        "Este",       8249,  135.3),
    ("Yabucoa",        "Este",      30426,  142.3),
    # ── Oeste (14) ──
    ("Mayagüez",       "Oeste",     67381,  201.4),
    ("Aguada",         "Oeste",     37516,   79.7),
    ("Aguadilla",      "Oeste",     52162,   94.1),
    ("Añasco",         "Oeste",     25480,  101.1),
    ("Cabo Rojo",      "Oeste",     47515,  182.4),
    ("Hormigueros",    "Oeste",     15267,   29.4),
    ("Isabela",        "Oeste",     39987,  143.3),
    ("Lajas",          "Oeste",     22156,  154.2),
    ("Las Marías",     "Oeste",      7874,  119.6),
    ("Maricao",        "Oeste",      4925,   95.5),
    ("Moca",           "Oeste",     33584,  130.5),
    ("Rincón",         "Oeste",     13656,   36.4),
    ("Sabana Grande",  "Oeste",     22147,   91.4),
    ("San Germán",     "Oeste",     30227,  141.1),
    # ── Central (19) ──
    ("Caguas",         "Central",  124606,  152.5),
    ("Aguas Buenas",   "Central",   24454,   77.5),
    ("Aibonito",       "Central",   22106,   81.2),
    ("Barranquitas",   "Central",   26563,   88.7),
    ("Cayey",          "Central",   42480,  134.6),
    ("Cidra",          "Central",   37104,   93.3),
    ("Comerío",        "Central",   17940,   72.0),
    ("Corozal",        "Central",   33117,  110.2),
    ("Gurabo",         "Central",   48593,   72.5),
    ("Naranjito",      "Central",   27349,   71.5),
    ("Orocovis",       "Central",   19688,  164.8),
    ("Ciales",         "Central",   15374,  172.0),
    ("Jayuya",         "Central",   13693,  115.1),
    ("Adjuntas",       "Central",   17185,  172.4),
    ("Lares",          "Central",   24473,  159.3),
    ("Utuado",         "Central",   26512,  297.9),
    ("San Sebastián",  "Central",   35068,  182.4),
    ("San Lorenzo",    "Central",   35286,  138.1),
    ("Guánica",        "Central",   13962,   96.1),
]

assert len(MUNICIPIOS) == 78, f"Expected 78 municipalities, got {len(MUNICIPIOS)}"

# The municipality that will have anomalous energy consumption
ANOMALY_MUNICIPIO = "Vieques"
ANOMALY_MULTIPLIER = 3.5  # consumption will be 3.5x what population predicts


def generate_municipios_stats():
    """Generate the primary municipal statistics CSV.

    Columns:
        municipio      (str)   - Municipality name
        region         (str)   - Geographic region
        poblacion      (int)   - Population estimate
        area_km2       (float) - Area in square kilometers
        ingreso_mediano (int)  - Median household income (USD)
        tasa_pobreza   (float) - Poverty rate (percentage, 0-100)

    Income and poverty are synthetically generated with realistic
    correlations: Metro municipalities tend to have higher income
    and lower poverty, rural/small municipalities the reverse.
    """
    rows = []
    # Base income/poverty by region (approximate PR Census ACS patterns)
    region_income_base = {
        "Metro":   24000,
        "Norte":   18000,
        "Sur":     16500,
        "Este":    17000,
        "Oeste":   17500,
        "Central": 16000,
    }
    region_poverty_base = {
        "Metro":   36.0,
        "Norte":   48.0,
        "Sur":     52.0,
        "Este":    50.0,
        "Oeste":   47.0,
        "Central": 53.0,
    }

    for nombre, region, pop, area in MUNICIPIOS:
        # Income: base + population bonus + noise
        base_income = region_income_base[region]
        pop_bonus = int(pop / 10000) * 500  # larger cities earn more
        noise = np.random.randint(-2000, 2000)
        ingreso = max(10000, base_income + pop_bonus + noise)

        # Poverty: base - population bonus + noise
        base_poverty = region_poverty_base[region]
        pop_reduction = pop / 50000 * 5  # larger cities have less poverty
        poverty_noise = np.random.uniform(-4.0, 4.0)
        pobreza = round(max(15.0, min(72.0,
            base_poverty - pop_reduction + poverty_noise)), 1)

        rows.append({
            "municipio":       nombre,
            "region":          region,
            "poblacion":       pop,
            "area_km2":        area,
            "ingreso_mediano": ingreso,
            "tasa_pobreza":    pobreza,
        })

    df = pd.DataFrame(rows)
    path = DATA_DIR / "municipios_stats.csv"
    df.to_csv(path, index=False)
    print(f"Created {path}: {df.shape[0]} rows x {df.shape[1]} cols")
    return df


def generate_consumo_municipal(stats_df):
    """Generate monthly energy consumption data with one anomaly.

    Model:
        base_kwh = population * 0.35  (per-capita monthly kWh, residential)
        seasonal  = 1.0 + 0.15 * sin(2pi * (month - 3) / 12)  (peak in summer)
        noise     = uniform(-0.05, +0.05) multiplicative
        consumption = base_kwh * seasonal * (1 + noise)

    Anomaly: Vieques gets multiplied by ANOMALY_MULTIPLIER, simulating
    an unexplained energy consumption spike (e.g., unreported industrial
    activity or data entry error — students must discover and explain).

    Columns:
        municipio            (str)   - Municipality name
        mes                  (str)   - Month in YYYY-MM format
        consumo_energia_kwh  (float) - Energy consumption in kWh
    """
    months = [f"2024-{m:02d}" for m in range(1, 13)]
    rows = []

    for _, row in stats_df.iterrows():
        nombre = row["municipio"]
        pop = row["poblacion"]
        base_kwh = pop * 0.35  # rough per-capita residential kWh

        for i, mes in enumerate(months):
            # Seasonal pattern: peak in June-August (months 6-8)
            seasonal = 1.0 + 0.15 * np.sin(2 * np.pi * (i + 1 - 3) / 12)
            noise = np.random.uniform(-0.05, 0.05)
            consumo = base_kwh * seasonal * (1 + noise)

            # Inject anomaly
            if nombre == ANOMALY_MUNICIPIO:
                consumo *= ANOMALY_MULTIPLIER

            rows.append({
                "municipio":           nombre,
                "mes":                 mes,
                "consumo_energia_kwh": round(consumo, 1),
            })

    df = pd.DataFrame(rows)
    path = DATA_DIR / "consumo_municipal.csv"
    df.to_csv(path, index=False)
    print(f"Created {path}: {df.shape[0]} rows x {df.shape[1]} cols")
    return df


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    stats = generate_municipios_stats()
    consumo = generate_consumo_municipal(stats)

    # Quick verification
    print(f"\n--- Verification ---")
    print(f"Municipalities: {stats.shape[0]}")
    print(f"Regions: {sorted(stats['region'].unique())}")
    print(f"Population range: {stats['poblacion'].min():,} - {stats['poblacion'].max():,}")
    print(f"Consumption rows: {consumo.shape[0]} (expected {78 * 12})")

    # Check anomaly is detectable
    annual = consumo.groupby("municipio")["consumo_energia_kwh"].sum()
    pop = stats.set_index("municipio")["poblacion"]
    per_capita = (annual / pop).sort_values(ascending=False)
    print(f"\nTop 5 per-capita annual consumption (kWh/person):")
    for muni, val in per_capita.head().items():
        flag = " *** ANOMALY" if muni == ANOMALY_MUNICIPIO else ""
        print(f"  {muni}: {val:.1f}{flag}")
    print(f"\nAll datasets generated successfully.")
