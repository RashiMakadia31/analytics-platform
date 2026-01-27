import pandas as pd
from db.connection import engine

from reliability_monitor.schema_check import check_schema
from reliability_monitor.completeness_check import check_completeness
from reliability_monitor.freshness_check import check_freshness
from reliability_monitor.business_rules import check_business_rules

def run_reliability_checks():
    df = pd.read_sql("SELECT * FROM orders_cleaned", engine)

    return {
        "schema": check_schema(df),
        "completeness": check_completeness(df),
        "freshness": check_freshness(df),
        "business_rules": check_business_rules(df)
    }
