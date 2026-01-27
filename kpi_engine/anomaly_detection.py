import pandas as pd

def detect_anomalies(
    df,
    kpi_col,
    window=7,
    z_threshold=3
):
    """
    Flags anomalies using rolling mean and std deviation.
    """

    df = df.copy()

    df[f"{kpi_col}_rolling_mean"] = (
        df[kpi_col].rolling(window=window, min_periods=3).mean()
    )

    df[f"{kpi_col}_rolling_std"] = (
        df[kpi_col].rolling(window=window, min_periods=3).std()
    )

    df[f"{kpi_col}_zscore"] = (
        (df[kpi_col] - df[f"{kpi_col}_rolling_mean"])
        / df[f"{kpi_col}_rolling_std"]
    )

    df[f"{kpi_col}_anomaly"] = df[f"{kpi_col}_zscore"].abs() > z_threshold

    return df
