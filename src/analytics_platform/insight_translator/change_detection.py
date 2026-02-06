def detect_change(curr, prev, threshold=0.05):
    """
    Detects direction and magnitude of change.
    """
    if prev == 0:
        return "no_baseline", 0

    pct_change = (curr - prev) / prev

    if abs(pct_change) < threshold:
        return "stable", pct_change
    elif pct_change > 0:
        return "increase", pct_change
    else:
        return "decrease", pct_change
