import random
import uuid
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import text
from db.connection import engine

BASE_PRICE = 1200
REGIONS = ["North", "South", "East", "West"]
PRODUCTS = ["SKU-1", "SKU-2", "SKU-3"]

def generate_orders(
    run_time_minutes=1,
    history_days=14,
    anomaly_rate=0.18,
    null_rate=0.12,
    rule_break_rate=0.08,
    seed=None,
):
    """
    Generate semi-realistic orders with controlled noise and anomalies.

    history_days: spreads orders across recent days to enable KPI anomaly detection.
    anomaly_rate: valid-but-extreme values (spikes/dips) to trigger KPI anomalies.
    null_rate: missing values to trigger completeness checks.
    rule_break_rate: invalid values (negative price, zero quantity) to trigger rules.
    seed: optional for reproducibility during demos.
    """
    if seed is not None:
        random.seed(seed)

    now = datetime.utcnow()
    orders = []

    history_days = max(1, int(history_days))
    total_orders = run_time_minutes * random.randint(20, 40)

    event_days = set()
    outage_days = set()
    if history_days >= 7:
        event_days = {
            (now - timedelta(days=random.randint(1, history_days - 1))).date()
            for _ in range(2)
        }
    if history_days >= 5:
        outage_days = {
            (now - timedelta(days=random.randint(1, history_days - 1))).date()
        }

    last_order_id = None

    for _ in range(total_orders):
        order_time = now - timedelta(
            days=random.randint(0, history_days - 1),
            minutes=random.randint(0, 24 * 60 - 1),
        )

        # Business logic
        weekday = order_time.weekday()
        base_multiplier = 1.0

        # Weekend surge
        if weekday >= 5:
            base_multiplier *= 1.3

        # Promotion window (simulate events)
        if order_time.hour in [12, 13, 20]:
            base_multiplier *= random.choice([1.8, 2.2, 1.0])

        # Campaign spike days
        if order_time.date() in event_days:
            base_multiplier *= random.choice([1.0, 2.5, 3.0])

        # Partial outage days
        if order_time.date() in outage_days and random.random() < 0.6:
            base_multiplier *= 0.4

        # Rare outage
        if random.random() < 0.03:
            base_multiplier *= 0.3

        price = round(BASE_PRICE * base_multiplier * random.uniform(0.8, 1.2), 2)
        quantity = random.choice([1, 1, 2, 3])
        order_id = str(uuid.uuid4())
        region = random.choice(REGIONS)
        product_id = random.choice(PRODUCTS)
        order_date = order_time.date()

        # Anomalies (valid but extreme)
        if random.random() < anomaly_rate:
            anomaly_type = random.choice(["price_spike", "bulk_order", "price_drop"])
            if anomaly_type == "price_spike":
                price = round(price * random.uniform(3, 6), 2)
            elif anomaly_type == "bulk_order":
                quantity = random.choice([10, 25, 50])
            else:
                price = round(price * random.uniform(0.1, 0.3), 2)

        # Missing values (completeness failures)
        if random.random() < null_rate:
            region = None
        if random.random() < null_rate:
            price = None
        if random.random() < null_rate:
            order_date = None

        # Rule breaks (business rule failures)
        if random.random() < rule_break_rate:
            price = -abs(price) if price is not None else -BASE_PRICE
        if random.random() < rule_break_rate:
            quantity = random.choice([0, -1, -5])

        # Misc. data issues (not fatal but noisy)
        if random.random() < (rule_break_rate / 2):
            product_id = "SKU-XXX"
        if last_order_id and random.random() < (rule_break_rate / 3):
            order_id = last_order_id

        last_order_id = order_id

        orders.append({
            "order_id": order_id,
            "order_date": order_date,
            "region": region,
            "product_id": product_id,
            "quantity": quantity,
            "price": price,
        })

    return pd.DataFrame(orders)


def push_orders_to_db(df):
    df.to_sql(
        "orders_cleaned",
        engine,
        if_exists="append",
        index=False
    )


if __name__ == "__main__":
    df = generate_orders()
    push_orders_to_db(df)
    print(f"{len(df)} orders generated")
