from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db import get_db
from api.schemas import KPI
from typing import List
import pandas as pd

router = APIRouter()

@router.get("/kpis/latest", response_model=KPI)
def get_latest_kpi(db: Session = Depends(get_db)):
    df = pd.read_sql(
        "SELECT * FROM daily_kpis ORDER BY order_date DESC LIMIT 1",
        db.bind
    )
    return df.iloc[0].to_dict()

@router.get("/kpis/history", response_model=List[KPI])
def get_kpi_history(db: Session = Depends(get_db)):
    df = pd.read_sql(
        "SELECT * FROM daily_kpis ORDER BY order_date",
        db.bind
    )
    return df.to_dict(orient="records")
