from fastapi import FastAPI
from pydantic import BaseModel, Field
from engine import run_engine
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from core.observability import write_run_artifact


app = FastAPI(
    title="LLM Guardrails Engine",
    description="Schema-enforced, repairable, confidence-scored LLM outputs",
    version="1.0.0"
)


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=20)


@app.post("/generate-summary")
def generate_summary(req: SummaryRequest):
    result = run_engine(req.text)

    return {
        "status": result["status"],
        "output": result.get("output"),
        "confidence": result["confidence"],
        "retries": result["retries"],
        "failure_type": result.get("failure_type"),
        "latency_ms": result["latency_ms"],
    }





@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    failure_type = "SCHEMA_VIOLATION"
    for err in errors:
        if err.get("type") == "json_invalid":
            failure_type = "INVALID_INPUT_JSON"
            artifact = {
                "status": "failed",
                "failure_type": failure_type,
                "confidence": 0.0,
                "retries": 0,
                "latency_ms": 0,
            }
            print("Writing validation error artifact")
            write_run_artifact(artifact)
            break




    return JSONResponse(
        status_code=400,
        content={
            "status": "failed",
            "failure_type": failure_type,
            "confidence": 0.0,
            "retries": 0,
            "output": None
        }
    )
