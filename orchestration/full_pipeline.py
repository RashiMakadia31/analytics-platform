from transformations.build_orders_cleaned import build_orders_cleaned
from reliability_monitor.reliability_runner import run_reliability_checks
from kpi_engine.compute_kpis import compute_daily_kpis
from kpi_engine.kpi_health_score import compute_kpi_health
from kpi_engine.anomaly_runner import run_kpi_anomalies
from insight_translator.insight_runner import run_insight_translation

def run_full_pipeline():
    print("STEP 1: Building cleaned data")
    build_orders_cleaned()

    print("\nSTEP 2: Running reliability checks")
    reliability_report = run_reliability_checks()

    print("\nSTEP 3: Computing KPIs")
    compute_daily_kpis()

    print("\nSTEP 4: Computing KPI health score")
    health_score = compute_kpi_health(reliability_report)
    print("KPI Health Score:", health_score)

    print("\nSTEP 5: Detecting KPI anomalies")
    run_kpi_anomalies()

    print("\nSTEP 6: Generating executive insights")
    run_insight_translation(health_score)

    print("\nPIPELINE COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    run_full_pipeline()
