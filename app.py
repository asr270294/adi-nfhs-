import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------
# Page config
# ------------------------------------------------
st.set_page_config(
    page_title="NFHS India Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 National Family Health Survey (NFHS) Dashboard")
st.caption("Health • Nutrition • Women • Sanitation • Social Indicators")

# ------------------------------------------------
# Load data
# ------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("All India National Family Health Survey.xlsx")
    df = df.dropna(how="all")
    return df

df = load_data()

# first 3 columns are identifiers
id_cols = ["India/States/UTs", "Survey", "Area"]
indicator_cols = [c for c in df.columns if c not in id_cols]

# ------------------------------------------------
# Sidebar filters
# ------------------------------------------------
st.sidebar.header("🔎 Filters")

state = st.sidebar.selectbox("State / UT", sorted(df[id_cols[0]].unique()))
survey = st.sidebar.selectbox("Survey Round", sorted(df[id_cols[1]].unique()))
area = st.sidebar.selectbox("Area", sorted(df[id_cols[2]].unique()))
indicator = st.sidebar.selectbox("Indicator", sorted(indicator_cols))

# ------------------------------------------------
# Filtered record
# ------------------------------------------------
filtered = df[
    (df[id_cols[0]] == state) &
    (df[id_cols[1]] == survey) &
    (df[id_cols[2]] == area)
]

value = filtered[indicator].iloc[0]

# ------------------------------------------------
# KPI cards
# ------------------------------------------------
c1, c2, c3 = st.columns(3)

c1.metric("📍 State", state)
c2.metric("📊 Survey", survey)
c3.metric("📈 Value (%)", round(float(value), 2))

st.divider()

# ------------------------------------------------
# State comparison
# ------------------------------------------------
st.subheader("📊 State Comparison")

co
