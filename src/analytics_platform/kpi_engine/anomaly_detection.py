import pandas as pd

def detect_anomalies(
    df,
    kpi_col,
    window=7,
    z_threshold=2.0,
    pct_threshold=0.35,
):
    """
    Flags anomalies using rolling mean and std deviation.
    """

    df = df.copy()

    if "order_date" in df.columns:
        df = df.sort_values("order_date")

    series = pd.to_numeric(df[kpi_col], errors="coerce")

    rolling_mean = series.rolling(window=window, min_periods=3).mean()
    rolling_std = series.rolling(window=window, min_periods=3).std()

    zscore = (series - rolling_mean) / rolling_std
    pct_change = series.pct_change()

    fallback = rolling_std.isna() | (rolling_std == 0)
    pct_anomaly = pct_change.abs() > pct_threshold

    df[f"{kpi_col}_rolling_mean"] = rolling_mean
    df[f"{kpi_col}_rolling_std"] = rolling_std
    df[f"{kpi_col}_zscore"] = zscore
    df[f"{kpi_col}_pct_change"] = pct_change
    df[f"{kpi_col}_anomaly"] = (zscore.abs() > z_threshold) | (fallback & pct_anomaly)

    return df
