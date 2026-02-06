CREATE TABLE IF NOT EXISTS orders_raw (
    order_id TEXT,
    order_date DATE,
    region TEXT,
    product_id TEXT,
    quantity INT,
    price NUMERIC
);

CREATE TABLE IF NOT EXISTS orders_cleaned (
    order_id TEXT,
    order_date DATE,
    region TEXT,
    product_id TEXT,
    quantity INT,
    price NUMERIC
);

CREATE TABLE IF NOT EXISTS daily_kpis (
    order_date DATE PRIMARY KEY,
    daily_revenue NUMERIC,
    daily_orders INT,
    aov NUMERIC
);

CREATE TABLE IF NOT EXISTS kpi_anomalies (
    order_date DATE,
    kpi_name TEXT,
    is_anomaly BOOLEAN
);

CREATE TABLE IF NOT EXISTS executive_insights (
    order_date DATE,
    insight TEXT,
    confidence TEXT
);
