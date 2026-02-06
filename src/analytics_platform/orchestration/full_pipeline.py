from analytics_platform.transformations.build_orders_cleaned import build_orders_cleaned
from analytics_platform.reliability_monitor.reliability_runner import run_reliability_checks
from analytics_platform.kpi_engine.compute_kpis import compute_daily_kpis
from analytics_platform.kpi_engine.anomaly_runner import run_kpi_anomalies
from analytics_platform.insight_translator.insight_runner import run_insight_translation
from analytics_platform.kpi_engine.kpi_health_score import compute_kpi_health

def run_full_pipeline(use_live=False):
    if not use_live:
        build_orders_cleaned()          # uses Postgres
    report = run_reliability_checks()
    compute_kpis = compute_daily_kpis()
    health = compute_kpi_health(report)
    run_kpi_anomalies()
    run_insight_translation(health)

    return True
