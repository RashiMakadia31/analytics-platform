from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db import get_db
from api.schemas import Insight
from typing import List
import pandas as pd

router = APIRouter()

@router.get("/insights", response_model=List[Insight])
def get_insights(db: Session = Depends(get_db)):
    df = pd.read_sql(
        "SELECT * FROM executive_insights ORDER BY order_date DESC",
        db.bind
    )
    return df.to_dict(orient="records")
