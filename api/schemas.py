from pydantic import BaseModel
from datetime import date

class KPI(BaseModel):
    order_date: date
    daily_revenue: float
    daily_orders: int
    aov: float

class Insight(BaseModel):
    order_date: date
    insight: str
    confidence: str
