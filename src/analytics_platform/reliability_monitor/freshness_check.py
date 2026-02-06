from datetime import date
import pandas as pd

def check_freshness(df, date_col="order_date", max_days_delay=2):
    # Convert to datetime64 and ignore invalids
    dates = pd.to_datetime(df[date_col], errors="coerce")
    dates = dates.dropna()

    if dates.empty:
        return {
            "latest_date": None,
            "delay_days": None,
            "status": "FAIL",
            "reason": "No valid dates found"
        }

    latest_ts = dates.max()
    latest_date = latest_ts.date()
    today = date.today()

    delay = (today - latest_date).days

    return {
        "latest_date": str(latest_date),
        "delay_days": delay,
        "status": "PASS" if delay <= max_days_delay else "FAIL"
    }
