from fastapi import APIRouter
from orchestration.full_pipeline import run_full_pipeline
import traceback

router = APIRouter()

@router.post("/pipeline/run")
def run_pipeline():
    try:
        run()
        return {"status": "pipeline executed successfully"}
    except Exception as e:
        print("PIPELINE ERROR:")
        traceback.print_exc()
        return {
            "status": "pipeline_failed",
            "error": str(e)
        }
