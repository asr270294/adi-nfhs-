import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# Page settings
# -------------------------------------------------
st.set_page_config(
    page_title="NFHS Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 National Family Health Survey (NFHS) Dashboard")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("All India National Family Health Survey5.xlsx")
    df = df.dropna(how="all")
    return df

df = load_data()

# -------------------------------------------------
# Identify columns
# -------------------------------------------------
state_col = "India/States/UTs"
survey_col = "Survey"
area_col = "Area"

indicator_cols = [
    c for c in df.columns
    if c not in [state_col, survey_col, area_col]
]

# -------------------------------------------------
# Sidebar filters
# -------------------------------------------------
st.sidebar.header("🔎 Filters")

state = st.sidebar.selectbox("State / UT", sorted(df[state_col].unique()))
survey = st.sidebar.selectbox("Survey Round", sorted(df[survey_col].unique()))
area = st.sidebar.selectbox("Area Type", sorted(df[area_col].unique()))
indicator = st.sidebar.selectbox("Indicator", sorted(indicator_cols))

# -------------------------------------------------
# Filter data
# -------------------------------------------------
filtered = df[
    (df[state_col] == state) &
    (df[survey_col] == survey) &
    (df[area_col] == area)
]

if filtered.empty:
    st.warning("No data available for selected filters")
    st.stop()

value = float(filtered[indicator].iloc[0])

# -------------------------------------------------
# KPI Section
# -------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("State", state)
c2.metric("Survey", survey)
c3.metric("Area", area)
c4.metric("Value (%)", round(value, 2))

st.divider()

# -------------------------------------------------
# Tabs
# -------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Comparison", "📈 Trend", "📋 Table"])

# -------------------------------------------------
# Tab 1 – State comparison
# -------------------------------------------------
with tab1:
    compare_df = df[
        (df[survey_col] == survey) &
        (df[area_col] == area)
    ][[state_col, indicator]]

    fig = px.bar(
        compare_df.sort_values(indicator, ascending=False),
        x=state_col,
        y=indicator,
        title=f"{indicator} across States"
    )

    fig.update_layout(xaxis_tickangle=-60)
    st.plotly_chart(fig, use_container_width=True)


# -------------------------------------------------
# Tab 2 – Trend across surveys
# -------------------------------------------------
with tab2:
    trend_df = df[
        (df[state_col] == state) &
        (df[area_col] == area)
    ][[survey_col, indicator]]

    fig2 = px.line(
        trend_df,
        x=survey_col,
        y=indicator,
        markers=True,
        title=f"{indicator} trend for {state}"
    )

    st.plotly_chart(fig2, use_container_width=True)


# -------------------------------------------------
# Tab 3 – Table + download
# -------------------------------------------------
with tab3:
    st.dataframe(compare_df.sort_values(indicator, ascending=False), use_container_width=True)

    csv = compare_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        csv,
        "nfhs_data.csv",
        "text/csv"
    )
