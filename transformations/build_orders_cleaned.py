import pandas as pd
from db.connection import engine

RAW = "data/raw/olist/"

def build_orders_cleaned():
    orders = pd.read_csv(RAW + "olist_orders_dataset.csv")
    items = pd.read_csv(RAW + "olist_order_items_dataset.csv")
    customers = pd.read_csv(RAW + "olist_customers_dataset.csv")

    orders = orders[["order_id", "customer_id", "order_purchase_timestamp"]]
    orders.rename(columns={"order_purchase_timestamp": "order_date"}, inplace=True)

    customers = customers[["customer_id", "customer_state"]]
    customers.rename(columns={"customer_state": "region"}, inplace=True)

    items = items[["order_id", "product_id", "price"]]
    items["quantity"] = 1

    df = (
        orders.merge(customers, on="customer_id", how="left")
              .merge(items, on="order_id", how="inner")
    )

    df["order_date"] = pd.to_datetime(df["order_date"]).dt.date
    df = df[["order_id", "order_date", "region", "product_id", "quantity", "price"]]

    # 🔥 WRITE TO POSTGRES
    df.to_sql(
        "orders_cleaned",
        engine,
        if_exists="replace",
        index=False
    )

    print("orders_cleaned table refreshed:", len(df))

if __name__ == "__main__":
    build_orders_cleaned()
