import pandas as pd
import yaml

def check_schema(df, schema_path="config/schema.yaml"):
    with open(schema_path, "r") as f:
        schema = yaml.safe_load(f)["orders_cleaned"]

    expected_cols = set(schema.keys())
    actual_cols = set(df.columns)

    missing = expected_cols - actual_cols
    extra = actual_cols - expected_cols

    return {
        "status": "PASS" if not missing and not extra else "FAIL",
        "missing_columns": list(missing),
        "extra_columns": list(extra)
    }
