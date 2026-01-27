def check_business_rules(df):
    issues = []

    if (df["price"] < 0).any():
        issues.append("Negative price detected")

    if (df["quantity"] <= 0).any():
        issues.append("Invalid quantity detected")

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues
    }
