from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db import get_db
import pandas as pd

router = APIRouter()

@router.get("/insights")
def get_insights(db: Session = Depends(get_db)):
    try:
        df = pd.read_sql(
            "SELECT * FROM executive_insights ORDER BY order_date DESC",
            db.bind
        )
    except Exception:
        # DB/table exists but query failed
        return []

    if df.empty:
        # THIS IS A VALID BUSINESS STATE
        return []

    return df.to_dict(orient="records")
