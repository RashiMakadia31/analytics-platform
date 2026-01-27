import pandas as pd
from db.connection import engine

def compute_daily_kpis():
    df = pd.read_sql("SELECT * FROM orders_cleaned", engine)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["revenue"] = df["quantity"] * df["price"]

    kpis = (
        df.groupby("order_date")
        .agg(
            daily_revenue=("revenue", "sum"),
            daily_orders=("order_id", "nunique")
        )
        .reset_index()
    )

    kpis["aov"] = kpis["daily_revenue"] / kpis["daily_orders"]

    kpis.to_sql(
        "daily_kpis",
        engine,
        if_exists="replace",
        index=False
    )

    print("daily_kpis table updated:", len(kpis))
    return kpis
