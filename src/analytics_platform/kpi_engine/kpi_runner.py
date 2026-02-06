from kpi_engine.compute_kpis import compute_daily_kpis
from kpi_engine.kpi_health_score import compute_kpi_health

from reliability_monitor.reliability_runner import run_reliability_checks

def run_kpi_pipeline():
    reliability_report = run_reliability_checks()
    kpi_health = compute_kpi_health(reliability_report)

    daily_kpis = compute_daily_kpis()

    print("\nKPI HEALTH SCORE:", kpi_health)
    return daily_kpis, kpi_health

if __name__ == "__main__":
    run_kpi_pipeline()
