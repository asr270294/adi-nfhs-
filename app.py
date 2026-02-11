import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="NFHS India Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 National Family Health Survey (NFHS) Dashboard")
st.markdown("Interactive health & socio-economic indicators across India")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("All India National Family Health Survey1.xlsx")
    return df

df = load_data()

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------
st.sidebar.header("🔎 Filters")

state = st.sidebar.selectbox(
    "State / UT",
    sorted(df["India/States/UTs"].unique())
)

survey = st.sidebar.selectbox(
    "Survey Round",
    sorted(df["Survey"].unique())
)

area = st.sidebar.selectbox(
    "Area",
    sorted(df["Area"].unique())
)

indicator_cols = df.columns[3:]

indicator = st.sidebar.selectbox(
    "Indicator",
    sorted(indicator_cols)
)

# ---------------------------------------------------
# Filtered data
# ---------------------------------------------------
filtered = df[
    (df["India/States/UTs"] == state) &
    (df["Survey"] == survey) &
    (df["Area"] == area)
]

value = filtered[indicator].values[0]

# ---------------------------------------------------
# KPI Section
# ---------------------------------------------------
col1, col2 = st.columns([1, 3])

with col1:
    st.metric("Selected Value (%)", round(value, 2))

with col2:
    st.subheader(indicator)

st.divider()

# ---------------------------------------------------
# State Comparison Chart
# ---------------------------------------------------
st.subheader("📈 State Comparison")

compare_df = df[
    (df["Survey"] == survey) &
    (df["Area"] == area)
][["India/States/UTs", indicator]]

fig = px.bar(
    compare_df.sort_values(indicator, ascending=False),
    x="India/States/UTs",
    y=indicator,
    title=f"{indicator} across States",
)

fig.update_layout(xaxis_tickangle=-60)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Trend Across Surveys
# ---------------------------------------------------
st.subheader(f"📉 Trend for {state}")

trend_df = df[
    (df["India/States/UTs"] == state) &
    (df["Area"] == area)
][["Survey", indicator]]

trend_fig = px.line(
    trend_df,
    x="Survey",
    y=indicator,
    markers=True
)

st.plotly_chart(trend_fig, use_container_width=True)

# ---------------------------------------------------
# Data Table
# ---------------------------------------------------
st.subheader("📋 Data Table")
st.dataframe(compare_df.sort_values(indicator, ascending=False))

# ---------------------------------------------------
# Download option
# ---------------------------------------------------
csv = compare_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download CSV",
    csv,
    "nfhs_data.csv",
    "text/csv"
)
