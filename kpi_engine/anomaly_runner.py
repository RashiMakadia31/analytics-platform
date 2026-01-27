import pandas as pd
from db.connection import engine
from kpi_engine.anomaly_detection import detect_anomalies

def run_kpi_anomalies():
    df = pd.read_sql("SELECT * FROM daily_kpis ORDER BY order_date", engine)

    for kpi in ["daily_revenue", "daily_orders", "aov"]:
        df = detect_anomalies(df, kpi)

    anomalies = []

    for _, row in df.iterrows():
        for kpi in ["daily_revenue", "daily_orders", "aov"]:
            anomalies.append({
                "order_date": row["order_date"],
                "kpi_name": kpi,
                "is_anomaly": bool(row[f"{kpi}_anomaly"])
            })

    pd.DataFrame(anomalies).to_sql(
        "kpi_anomalies",
        engine,
        if_exists="replace",
        index=False
    )

    print("kpi_anomalies table updated")
