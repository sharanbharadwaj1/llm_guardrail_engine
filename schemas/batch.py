from pydantic import BaseModel
from typing import List, Optional, Any
from fastapi import APIRouter
import time

from engine import run_engine

router = APIRouter()

class BatchItem(BaseModel):
    """
    One independent unit of work in a batch request.
    """
    id: str
    text: str


class BatchResult(BaseModel):
    """
    Result for a single batch item.
    Failure isolation is enforced at this level.
    """
    id: str
    index: int
    status: str                    # valid | failed
    output: Optional[Any]
    failure_type: Optional[str]
    confidence: float
    retries: int
    latency_ms: int
    model_role: Optional[str]


class BatchResponse(BaseModel):
    """
    Aggregated batch response.
    Order is NOT guaranteed unless index is used.
    """
    results: List[BatchResult]


@router.post("/generate-summary/batch", response_model=BatchResponse)
def generate_summary_batch(items: List[BatchItem]):
    results = []

    for index, item in enumerate(items):
        start = time.time()

        try:
            result = run_engine(item.text)

            latency_ms = int((time.time() - start) * 1000)

            results.append(
                BatchResult(
                    id=item.id,
                    index=index,
                    status=result["status"],
                    output=result.get("output"),
                    failure_type=result.get("failure_type"),
                    confidence=result.get("confidence", 0.0),
                    retries=result.get("retries", 0),
                    latency_ms=latency_ms,
                    model_role=result.get("model_role"),
                )
            )

        except Exception as e:
            latency_ms = int((time.time() - start) * 1000)

            results.append(
                BatchResult(
                    id=item.id,
                    index=index,
                    status="failed",
                    output=None,
                    failure_type="INTERNAL_ERROR",
                    confidence=0.0,
                    retries=0,
                    latency_ms=latency_ms,
                    model_role=None,
                )
            )

    return BatchResponse(results=results)
