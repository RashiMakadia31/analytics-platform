from fastapi import APIRouter
from orchestration.full_pipeline import run_full_pipeline

router = APIRouter()

@router.post("/pipeline/run")
def run_pipeline():
    run()
    return {"status": "pipeline executed successfully"}
