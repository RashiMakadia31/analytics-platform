from datetime import date
import pandas as pd

def check_freshness(df, date_col="order_date", max_days_delay=2):
    # Explicitly convert to datetime
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce").dt.date

    latest_date = df[date_col].max()
    today = date.today()

    if latest_date is None:
        return {
            "latest_date": None,
            "delay_days": None,
            "status": "FAIL",
            "reason": "No valid dates found"
        }

    delay = (today - latest_date).days

    return {
        "latest_date": str(latest_date),
        "delay_days": delay,
        "status": "PASS" if delay <= max_days_delay else "FAIL"
    }
