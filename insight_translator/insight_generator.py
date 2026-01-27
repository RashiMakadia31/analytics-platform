def generate_insight(date, change_type, pct_change, drivers, revenue_impact, health_score):
    confidence = "high" if health_score >= 80 else "moderate"

    direction_word = {
        "increase": "increased",
        "decrease": "decreased",
        "stable": "remained stable"
    }.get(change_type, "changed")

    driver_text = ", ".join(drivers).replace("_", " ")

    insight = (
        f"On {date}, revenue {direction_word} by {abs(pct_change)*100:.1f}%. "
        f"The primary drivers were {driver_text}. "
        f"Estimated revenue impact was {revenue_impact:.2f}. "
        f"Data reliability confidence is {confidence}."
    )

    return insight
