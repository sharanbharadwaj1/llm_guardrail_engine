import asyncio
import time
from schemas.batch import BatchItem, BatchResult, BatchResponse
from core.errors import FailureType
from engine import run_engine
from fastapi import APIRouter
from typing import List

router = APIRouter()


BATCH_TIMEOUT_SECONDS = 30

async def run_batch(items):
    tasks = [
        asyncio.create_task(run_item(item, index=i))
        for i, item in enumerate(items)
    ]

    done, pending = await asyncio.wait(
        tasks,
        timeout=BATCH_TIMEOUT_SECONDS
    )

    results = []

    # Completed tasks
    for task in done:
        try:
            results.append(task.result())
        except Exception:
            results.append(
                BatchResult(
                    id="unknown",
                    index=-1,
                    status="failed",
                    output=None,
                    failure_type=FailureType.INTERNAL_ERROR,
                    confidence=0.0,
                    retries=0,
                    latency_ms=0,
                    model_role=None,
                )
            )

    # Timed-out tasks
    for task in pending:
        task.cancel()
        results.append(
            BatchResult(
                id="unknown",
                index=-1,
                status="failed",
                output=None,
                failure_type=FailureType.TIMEOUT,
                confidence=0.0,
                retries=0,
                latency_ms=BATCH_TIMEOUT_SECONDS * 1000,
                model_role=None,
            )
        )

    return results




# Global semaphore (important: NOT inside function)
MAX_CONCURRENCY = 5
semaphore = asyncio.Semaphore(MAX_CONCURRENCY)


async def run_item(item: BatchItem, index: int) -> BatchResult:
    async with semaphore:
        start = time.time()

        try:
            # run sync engine in thread to avoid blocking event loop
            result = await asyncio.to_thread(run_engine, item.text)

            latency_ms = int((time.time() - start) * 1000)

            return BatchResult(
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

        except Exception:
            latency_ms = int((time.time() - start) * 1000)

            return BatchResult(
                id=item.id,
                index=index,
                status="failed",
                output=None,
                failure_type=FailureType.INTERNAL_ERROR,
                confidence=0.0,
                retries=0,
                latency_ms=latency_ms,
                model_role=None,
            )
