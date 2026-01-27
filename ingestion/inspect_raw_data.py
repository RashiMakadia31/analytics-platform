import pandas as pd

BASE_PATH = "data/raw/olist/"

files = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv"
}

for name, file in files.items():
    df = pd.read_csv(BASE_PATH + file)
    print(f"\n--- {name.upper()} ---")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print(df.head(2))
