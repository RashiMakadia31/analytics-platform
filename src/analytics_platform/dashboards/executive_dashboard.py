import streamlit as st
import pandas as pd
import os
from pandas.errors import EmptyDataError

st.set_page_config(page_title="Executive Analytics Dashboard", layout="wide")
st.title("📊 Executive Analytics Dashboard")

# --- Load KPIs (this file is never empty) ---
kpis = pd.read_csv("data/analytics/daily_kpis.csv")
latest = kpis.sort_values("order_date").iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Daily Revenue", f"{latest['daily_revenue']:.2f}")
col2.metric("Daily Orders", int(latest["daily_orders"]))
col3.metric("AOV", f"{latest['aov']:.2f}")

st.divider()

# --- Load Insights SAFELY ---
INSIGHTS_FILE = "data/analytics/executive_insights.csv"

try:
    if os.path.exists(INSIGHTS_FILE):
        insights = pd.read_csv(INSIGHTS_FILE)
    else:
        insights = pd.DataFrame(columns=["date", "insight"])
except EmptyDataError:
    insights = pd.DataFrame(columns=["date", "insight"])

# --- Display Insights ---
st.subheader("🚨 Key Business Insights")

if insights.empty:
    st.success("No significant anomalies detected. KPIs are within expected ranges.")
else:
    for _, row in insights.iterrows():
        st.warning(row["insight"])

st.divider()

# --- KPI Trends ---
st.subheader("📈 KPI Trends")
st.line_chart(
    kpis.set_index("order_date")[["daily_revenue", "daily_orders"]]
)
