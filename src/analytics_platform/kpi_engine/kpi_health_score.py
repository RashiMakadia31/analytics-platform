def compute_kpi_health(reliability_report):
    weights = {
        "schema": 0.3,
        "completeness": 0.3,
        "freshness": 0.2,
        "business_rules": 0.2
    }

    score = 0

    if reliability_report["schema"]["status"] == "PASS":
        score += weights["schema"] * 100

    if all(v["status"] == "PASS" for v in reliability_report["completeness"].values()):
        score += weights["completeness"] * 100

    if reliability_report["freshness"]["status"] == "PASS":
        score += weights["freshness"] * 100

    if reliability_report["business_rules"]["status"] == "PASS":
        score += weights["business_rules"] * 100

    return round(score, 1)
