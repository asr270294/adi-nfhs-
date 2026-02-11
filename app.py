import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="NFHS Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 National Family Health Survey (NFHS) Dashboard")
st.markdown("Interactive dashboard for NFHS-3 and NFHS-4 indicators")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("All India National Family Health Survey4.xlsx")
    return df

df = load_data()

# -----------------------------
# Clean Data
# -----------------------------
# Remove "Note of :" columns
df = df[[col for col in df.columns if not col.startswith("Note of")]]

# Convert wide to long format
id_cols = ["India/States/UTs", "Survey", "Area"]
value_cols = [col for col in df.columns if col not in id_cols]

df_long = df.melt(
    id_vars=id_cols,
    value_vars=value_cols,
    var_name="Indicator",
    value_name="Value"
)

# Remove missing values
df_long = df_long.dropna(subset=["Value"])

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

state = st.sidebar.selectbox(
    "Select State/UT",
    sorted(df_long["India/States/UTs"].unique())
)

survey = st.sidebar.selectbox(
    "Select Survey",
    sorted(df_long["Survey"].unique())
)

area = st.sidebar.selectbox(
    "Select Area",
    sorted(df_long["Area"].unique())
)

indicator = st.sidebar.selectbox(
    "Select Indicator",
    sorted(df_long["Indicator"].unique())
)

# -----------------------------
# Filtered Data
# -----------------------------
filtered_df = df_long[
    (df_long["India/States/UTs"] == state) &
    (df_long["Survey"] == survey) &
    (df_long["Area"] == area) &
    (df_long["Indicator"] == indicator)
]

# -----------------------------
# KPI Display
# -----------------------------
st.subheader("📌 Selected Indicator Value")

if not filtered_df.empty:
    value = filtered_df["Value"].values[0]
    st.metric(label=indicator, value=round(value, 2))
else:
    st.warning("No data available for selected filters.")

# -----------------------------
# State Comparison Chart
# -----------------------------
st.subheader("📊 State-wise Comparison")

comparison_df = df_long[
    (df_long["Survey"] == survey) &
    (df_long["Area"] == area) &
    (df_long["Indicator"] == indicator)
]

fig = px.bar(
    comparison_df,
    x="India/States/UTs",
    y="Value",
    title=f"{indicator} ({survey} - {area})",
)

fig.update_layout(xaxis_tickangle=-90)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Data Table
# -----------------------------
st.subheader("📋 Data Table")
st.dataframe(comparison_df.sort_values("Value", ascending=False))
