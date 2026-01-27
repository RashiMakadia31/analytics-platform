from transformations.build_orders_cleaned import build_orders_cleaned
from reliability_monitor.reliability_runner import run_reliability_checks
from kpi_engine.compute_kpis import compute_daily_kpis
from kpi_engine.anomaly_runner import run_kpi_anomalies
from insight_translator.insight_runner import run_insight_translation
from kpi_engine.kpi_health_score import compute_kpi_health

def run_full_pipeline():
    build_orders_cleaned()          # uses Postgres
    report = run_reliability_checks()
    compute_kpis = compute_daily_kpis()
    health = compute_kpi_health(report)
    run_kpi_anomalies()
    run_insight_translation(health)

    return True
