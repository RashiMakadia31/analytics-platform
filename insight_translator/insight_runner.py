import pandas as pd
from db.connection import engine

from insight_translator.change_detection import detect_change
from insight_translator.driver_analysis import identify_driver
from insight_translator.insight_generator import generate_insight

def run_insight_translation(health_score):
    df = pd.read_sql("""
        SELECT k.order_date, k.daily_revenue, k.daily_orders, k.aov,
               a.is_anomaly
        FROM daily_kpis k
        JOIN kpi_anomalies a
          ON k.order_date = a.order_date
        WHERE a.kpi_name = 'daily_revenue'
        ORDER BY k.order_date
    """, engine)

    insights = []

    for i in range(1, len(df)):
        if not df.iloc[i]["is_anomaly"]:
            continue

        curr, prev = df.iloc[i], df.iloc[i-1]

        change, pct = detect_change(curr["daily_revenue"], prev["daily_revenue"])
        drivers = identify_driver(curr, prev)
        impact = curr["daily_revenue"] - prev["daily_revenue"]

        insights.append({
            "order_date": curr["order_date"],
            "insight": generate_insight(
                curr["order_date"], change, pct, drivers, impact, health_score
            ),
            "confidence": "high" if health_score >= 80 else "moderate"
        })

    pd.DataFrame(insights).to_sql(
        "executive_insights",
        engine,
        if_exists="replace",
        index=False
    )

    print("executive_insights table updated")
