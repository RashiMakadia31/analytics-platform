from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db import get_db
import pandas as pd
import traceback

router = APIRouter()

@router.get("/insights")
def get_insights(db: Session = Depends(get_db)):
    try:
        df = pd.read_sql(
            "SELECT order_date, insight, confidence FROM executive_insights ORDER BY order_date DESC",
            db.bind
        )
        return df.to_dict(orient="records")

    except Exception as e:
        print("INSIGHTS ERROR:")
        traceback.print_exc()
        return {
            "error": "insights_failed",
            "details": str(e)
        }
