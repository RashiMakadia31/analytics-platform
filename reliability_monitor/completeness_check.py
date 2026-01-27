def check_completeness(df, threshold=0.05):
    results = {}

    for col in df.columns:
        null_ratio = df[col].isna().mean()
        results[col] = {
            "null_ratio": round(null_ratio, 3),
            "status": "FAIL" if null_ratio > threshold else "PASS"
        }

    return results
