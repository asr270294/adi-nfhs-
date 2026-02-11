import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# Page setup
# ---------------------------------------------------
st.set_page_config(
    page_title="NFHS India Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 National Family Health Survey Dashboard")
st.caption("Interactive health & socio-economic indicators across India")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("All India National Family Health Survey5.xlsx")
    df = df.dropna(how="all")
    return df

df = load_data()

# Identify columns
id_cols = ["India/States/UTs", "Survey", "Area"]
indicator_cols = [c for c in df.columns if c not in id_cols]

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------
st.sidebar.header("🔎 Filters")

state = st.sidebar.selectbox("State / UT", sorted(df[id_cols[0]].unique()))
survey = st.sidebar.selectbox("Survey Round", sorted(df[id_cols[1]].unique()))
area = st.sidebar.selectbox("Area Type", sorted(df[id_cols[2]].unique()))
indicator = st.sidebar.selectbox("Indicator", sorted(indicator_cols))

# ---------------------------------------------------
# Filter
# ---------------------------------------------------
filtered = df[
    (df[id_cols[0]] == state) &
    (df[id_cols[1]] == survey) &
    (df[id_cols[2]] == area)
]

value = float(filtered[indicator].iloc[0])

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("State", state)
c2.metric("Survey", survey)
c3.metric("Area", area)
c4.metric("Value (%)", round(value, 2))

st.divider()

# ---------------------------------------------------
# Tabs layout
# ---------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 State Comparison", "📈 Trend", "📋 Table"])

# ------------------------
# Tab 1 – Comparison
# ------------------------
with tab1:
    compare_df = df[
        (df[id_cols[1]] == survey) &
        (df[id_cols[2]] == area)
    ][[id_cols[0], indicator]]

    fig = px.bar(
        compare_df.sort_values(indicator, ascending=False),
        x=id_cols[0],
        y=indicator,
        title=f"{indicator} across States"
    )

    fig.update_layout(xaxis_tickangle=-60)
    st.plotly_chart(fig, use_container_width=True)

# ------------------------
# Tab 2 – Trend
# ------------------------
with tab2:
    trend_df = df[
        (df[id_cols[0]] == state) &
        (df[id_cols[2]] == area)
    ][[id_cols[1], indicator]]

    trend_fig = px.line(
        trend_df,
        x=id_cols[1],
        y=indicator,
        markers=True,
        title=f"{indicator} trend for {state}"
    )

    st.plotly_chart(trend_fig, use_container_width=True)

# ------------------------
# Tab 3 – Table + Download
# ------------------------
with tab3:
    st.dataframe(compare_df.sort_values(indicator, ascending=False), use_container_width=True)

    csv = compare_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        csv,
        "nfhs_data.csv",
        "text/csv"
    )
