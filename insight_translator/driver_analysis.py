def identify_driver(curr_row, prev_row):
    drivers = []

    if curr_row["daily_orders"] < prev_row["daily_orders"]:
        drivers.append("order_volume_decline")

    if curr_row["aov"] < prev_row["aov"]:
        drivers.append("lower_average_order_value")

    if not drivers:
        drivers.append("mixed_or_external_factors")

    return drivers
