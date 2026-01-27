from fastapi import FastAPI
from api.routes import health, kpis, insights, pipeline

app = FastAPI(title="Analytics Reliability Platform API")

@app.get("/")
def root():
    return {
        "message": "Analytics Platform API is running",
        "docs": "/docs",
        "health": "/health"
    }

app.include_router(health.router)
app.include_router(kpis.router)
app.include_router(insights.router)
app.include_router(pipeline.router)
