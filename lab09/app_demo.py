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

# --- Guard: empty filter crashes the IN(...) query ---
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
    con,
    params=selected,
)

df_top = pd.read_sql(
    f"SELECT m.nombre, r.nombre AS region, m.poblacion "
    f"FROM municipio m JOIN region r ON m.region_id = r.id "
    f"WHERE r.nombre IN ({placeholders}) "
    f"ORDER BY m.poblacion DESC LIMIT ?",
    con,
    params=selected + [top_n],
)

df_region = pd.read_sql(
    f"SELECT r.nombre AS region, SUM(m.poblacion) AS total_pop "
    f"FROM municipio m JOIN region r ON m.region_id = r.id "
    f"WHERE r.nombre IN ({placeholders}) "
    f"GROUP BY r.nombre ORDER BY total_pop DESC",
    con,
    params=selected,
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

# --- Raw Data Preview ---
st.header("Raw Data")
st.dataframe(df, use_container_width=True)

# --- Search Results ---
if search:
    df_search = pd.read_sql(
        "SELECT m.nombre, r.nombre AS region, m.poblacion, m.area_km2 "
        "FROM municipio m JOIN region r ON m.region_id = r.id "
        "WHERE m.nombre LIKE ?",
        con,
        params=[f"%{search}%"],
    )
    st.subheader(f"Search results for '{search}'")
    if len(df_search) == 0:
        st.info("No municipalities match your search.")
    else:
        st.dataframe(df_search, use_container_width=True)
