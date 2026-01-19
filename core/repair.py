from requests import JSONDecodeError
from core.executor import call_llm
from core.validator import validate_summary
from core.errors import FailureType
from pydantic import ValidationError
from core.observability import write_run_artifact

def repair_with_retries(prompt: str, role,  max_retries: int = 2):
    retries = 0
    last_failure = None
    
    
    while retries <= max_retries:
        try:
            print("LLM call attempt made")
            output = call_llm(prompt, role)
            # return validate_output(output, retries)
            valid, failure_type, result,score = validate_summary(output)

            if valid:

                return {
                    "status": "valid",
                    "output": result,
                    "retries": retries,
                    "failure_type": failure_type,
                    "semantic_score": score
                }
            last_failure = failure_type
            print(f"Validation failed: {failure_type}, Output:{output},CHECK 1")

        except ValidationError as e:
            last_failure = "SCHEMA_VIOLATION"
        except JSONDecodeError:
            last_failure = "INVALID_JSON"
        except RuntimeError as e:
            failure_type = str(e)

            failure_type = str(e)

            # 🔴 HARD STOP failures
            if failure_type in {
                FailureType.LLM_AUTH_FAILURE,
                FailureType.LLM_QUOTA_EXCEEDED,
                FailureType.LLM_PROVIDER_UNAVAILABLE,

            }:
                last_failure = failure_type
                artifact = {
                    "status": "Hard Stop failure Occured during LLM call",
                    "failure_type": last_failure,
                    "retries": retries,
                    "output": None,
                    "message": "LLM authentication failed"
                }

                write_run_artifact(artifact)

                return {
                    "status": "failed",
                    "failure_type": last_failure,
                    "retries": retries,
                    "output": None,
                }

                
                
            last_failure = failure_type
                
        retries += 1
        prompt = repair_prompt(prompt, last_failure)

    return {
        "status": "failed",
        "failure_type": "REPAIR_EXHAUSTED",
        "retries": retries,
        "output": None,
    }




def repair_prompt(original_prompt: str, failure_type: str) -> str:

    REPAIR_STRATEGIES = {
    "INVALID_JSON": (
        "Your previous response was not valid JSON. "
        "Return ONLY valid JSON. "
        "Do not include explanations, markdown, or extra text."
    ),

    "SCHEMA_VIOLATION": (
        "Your response did not match the required schema. "
        "Ensure all required fields are present and correctly typed. "
        "Follow the schema exactly."
    ),

    "EMPTY_OUTPUT": (
        "Your previous response was empty or incomplete. "
        "Provide a complete and concise response that satisfies the task."
    ),
}
    instruction = REPAIR_STRATEGIES.get(
        failure_type,
        "Fix the issues in your previous response."
    )

    return (
        original_prompt
        + "\n\n### REPAIR INSTRUCTIONS\n"
        + instruction
    )
