from openai import BaseModel
from core.repair import repair_with_retries,repair_prompt
from core.confidence import compute_confidence
from pathlib import Path
from prompts.summary import prompt_summary
from core.observability import write_run_artifact
import time
from json import JSONDecodeError
import json
from core.models import ModelRole
from core.policy import Policy


# PROMPT_PATH = Path("prompts/summary.py")
CONFIDENCE_THRESHOLD = 0.6
ESCALATE_ON_FAILURES = {"SCHEMA_VIOLATION", "REPAIR_EXHAUSTED"}


def run_engine(text: str):
    start = time.time()
    policy = Policy()
    base_prompt = prompt_summary.replace("{{TEXT}}", text)

    # 1️⃣ Try FAST model
    # fast_result = repair_with_retries(base_prompt, role=ModelRole.FAST)
    
    role = ModelRole.FAST
    max_retries = (
    policy.retries_fast
    if role == ModelRole.FAST
    else policy.retries_strong
    )

    fast_result = repair_with_retries(base_prompt, role=ModelRole.FAST, max_retries=max_retries)


    print(f"Fast result: {fast_result}")

    fast_confidence = compute_confidence(
        retries=fast_result.get("retries", 0),
        success=fast_result["status"] == "valid",
        failure_type=fast_result.get("failure_type"),
    )

    # 2️⃣ Decide escalation
    # should_escalate = (
    #     fast_result["status"] != "valid"
    #     or fast_confidence < CONFIDENCE_THRESHOLD
    #     or fast_result.get("failure_type") in ESCALATE_ON_FAILURES
    # )
    should_escalate = (
    fast_result["status"] != "valid"
    or (
        policy.raw["escalation"]["confidence_below_threshold"]
        and fast_confidence < policy.min_confidence
    )
    or fast_result.get("failure_type") in policy.escalation_failures
)

    

    if not should_escalate:
        latency_ms = int((time.time() - start) * 1000)
        
        artifact = {
            "status": fast_result["status"],
            "output": fast_result.get("output"),
            "failure_type": str(fast_result.get("failure_type")),
            "retries": fast_result.get("retries"),
            "confidence": fast_confidence,
            "latency_ms": latency_ms,
            "model_role": "FAST",
            "policy": policy.raw
        }
        if isinstance(fast_result.get("output"), BaseModel):
            # output = fast_result.get("output").model_dump()
            artifact = {
            "status": fast_result["status"],
            "output": (
                fast_result["output"].model_dump()
                if hasattr(fast_result["output"], "model_dump")
                else fast_result["output"]
            ),
            "failure_type": str(fast_result.get("failure_type")),
            "retries": fast_result.get("retries"),
            "confidence": fast_confidence,
            "latency_ms": latency_ms,
            "model_role": "FAST"
            }


        write_run_artifact(artifact)

        return {
                "status": fast_result["status"],
                "output": fast_result.get("output"),
                "failure_type": fast_result.get("failure_type"),
                "confidence": fast_confidence,
                "retries": fast_result.get("retries"),
                "latency_ms": latency_ms,
                "model_role": "FAST"
            }

    # 3️⃣ Escalate to STRONG model
    strong_result = repair_with_retries(base_prompt, role=ModelRole.STRONG)

    strong_confidence = compute_confidence(
        retries=strong_result.get("retries", 0),
        success=strong_result["status"] == "valid",
        failure_type=strong_result.get("failure_type"),
    )

    latency_ms = int((time.time() - start) * 1000)
    artifact = {
        "status": strong_result["status"],
        "output": strong_result.get("output"),
        "failure_type": str(strong_result.get("failure_type")),
        "retries": strong_result.get("retries"),
        "confidence": strong_confidence,
        "latency_ms": latency_ms,
        "model_role": "STRONG",
        "policy": policy.raw
    }
    write_run_artifact(artifact)

    return {
                "status": strong_result["status"],
                "output": strong_result.get("output"),
                "failure_type": strong_result.get("failure_type"),
                "confidence": strong_confidence,
                "retries": strong_result.get("retries"),
                "latency_ms": latency_ms,
                "model_role": "STRONG"
            }


# def run_engine(text: str):
#     start = time.time()
#     base_prompt = prompt_summary.replace("{{TEXT}}", text)
#     try:
#         result = repair_with_retries(base_prompt)
#     # except Exceptions as e:
#     #     failure_type = result["msg"]
#     #     prompt = repair_prompt(prompt, failure_type)
#     #     retries += 1
#     # except ValidationError as e:
#     #     failure_type = "SCHEMA_VIOLATION"
#         # prompt = repair_prompt(prompt, failure_type)
#         # retries += 1
#     except json.JSONDecodeError as e:
#         failure_type = "INVALID_JSON"
#         prompt = repair_prompt(prompt, failure_type)
#         retries += 1

    
    
#     confidence = compute_confidence(
#         retries=result.get("retries", 0),
#         success=result["status"] == "valid"
#     )

#     # return {
#     #     "status": result["status"],
#     #     "output": result.get("output"),
#     #     "confidence": confidence,
#     #     "retries": result.get("retries")
#     # }
# #     return {
# #     "status": result["status"],
# #     "output": result.get("output"),
# #     "failure_type": result.get("failure_type"),
# #     "confidence": confidence,
# #     "retries": result.get("retries")
# # }
#     latency_ms = int((time.time() - start) * 1000)

#     artifact = {
#         "status": result["status"],
#         "failure_type": str(result.get("failure_type")),
#         "retries": result.get("retries"),
#         "confidence": confidence,
#         "latency_ms": latency_ms,
#     }

#     write_run_artifact(artifact)

#     return {
#         **artifact,
#         "output": result.get("output"),
#     }


