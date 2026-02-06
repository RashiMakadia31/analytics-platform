import sys
import os

# --- HARD GUARANTEE that src/ is on PYTHONPATH ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))   # .../src/analytics_platform
SRC_DIR = os.path.dirname(CURRENT_DIR)                      # .../src
sys.path.insert(0, SRC_DIR)

import streamlit as st
import pandas as pd
from sqlalchemy import text

from analytics_platform.db.connection import engine
from analytics_platform.data_stimulation.live_order_generator import (
    generate_orders,
    push_orders_to_db,
)
from analytics_platform.orchestration.full_pipeline import run_full_pipeline


# -------------------------------------------------
# Streamlit config (MUST be first Streamlit call)
# -------------------------------------------------
st.set_page_config(
    page_title="Analytics Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Executive Analytics Dashboard")


# -------------------------------------------------
# Helpers (SAFE DB ACCESS)
# -------------------------------------------------
def safe_read_sql(query: str) -> pd.DataFrame:
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()


# -------------------------------------------------
# Sidebar – Data Simulation
# -------------------------------------------------
st.sidebar.header("Live Data Simulator")

minutes = st.sidebar.slider(
    "Generate data for last X minutes",
    min_value=1,
    max_value=60,
    value=5,
)

if st.sidebar.button("▶️ Generate Live Orders"):
    with st.spinner("Generating live business data..."):
        df = generate_orders(minutes)
        push_orders_to_db(df)
    st.sidebar.success(f"{len(df)} orders generated")
    st.session_state["has_live_data"] = True
    st.rerun()


# -------------------------------------------------
# Pipeline Trigger
# -------------------------------------------------
st.subheader("Pipeline Control")

if "has_live_data" not in st.session_state:
    st.session_state["has_live_data"] = False

use_live = st.checkbox(
    "Use live orders (skip raw rebuild)",
    value=st.session_state["has_live_data"],
)

if st.button("🚀 Run Analytics Pipeline"):
    with st.spinner("Running analytics pipeline..."):
        try:
            run_full_pipeline(use_live=use_live)
            st.success("Pipeline executed successfully")
        except Exception as e:
            st.error(f"Pipeline failed: {e}")


# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
st.header("Key Performance Indicators")

kpi_df = safe_read_sql("""
    SELECT *
    FROM daily_kpis
    ORDER BY order_date DESC
    LIMIT 1
""")

if not kpi_df.empty:
    kpi = kpi_df.iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Daily Revenue", f"₹{float(kpi['daily_revenue']):,.2f}")
    col2.metric("Daily Orders", int(kpi["daily_orders"]))
    col3.metric("AOV", f"₹{float(kpi['aov']):,.2f}")
else:
    st.info("No KPI data available yet.")


# -------------------------------------------------
# KPI TREND
# -------------------------------------------------
st.subheader("Revenue Trend")

history_df = safe_read_sql("""
    SELECT order_date, daily_revenue
    FROM daily_kpis
    ORDER BY order_date
""")

if not history_df.empty:
    history_df["order_date"] = pd.to_datetime(history_df["order_date"])
    st.line_chart(history_df.set_index("order_date"))
else:
    st.info("Not enough historical data to plot trends.")


# -------------------------------------------------
# EXECUTIVE INSIGHTS
# -------------------------------------------------
st.header("Executive Insights")

insights_df = safe_read_sql("""
    SELECT *
    FROM executive_insights
    ORDER BY order_date DESC
""")

if insights_df.empty:
    st.success("No significant anomalies detected 🎯")
else:
    for _, row in insights_df.iterrows():
        st.warning(row["insight"])
