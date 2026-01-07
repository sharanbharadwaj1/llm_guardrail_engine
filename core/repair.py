from requests import JSONDecodeError
from core.executor import call_llm
from core.validator import validate_summary
from core.errors import FailureType
from pydantic import ValidationError


def repair_with_retries(prompt: str, role, max_retries: int = 2):
    retries = 0
    last_failure = None

    while retries <= max_retries:
        try:
            output = call_llm(prompt, role)
            # return validate_output(output, retries)
            valid, failure_type, result = validate_summary(output)

            if valid:

                return {
                    "status": "valid",
                    "output": result,
                    "retries": retries,
                    "failure_type": failure_type
                }
            last_failure = failure_type
            print(f"Validation failed: {failure_type}, Output:{output},CHECK 1")

        except ValidationError as e:
            last_failure = "SCHEMA_VIOLATION"
        except JSONDecodeError:
            last_failure = "INVALID_JSON"
                
        retries += 1
        prompt = repair_prompt(prompt, last_failure)

    return {
        "status": "failed",
        "failure_type": "REPAIR_EXHAUSTED",
        "retries": retries,
        "output": None,
    }


# def repair_with_retries(prompt: str, role,max_retries: int = 2):


    

#     last_error = None
#     last_failure_type = None

#     for attempt in range(max_retries + 1):
#         try:
#             output = call_llm(prompt,role)
#         except Exception as e:
#             print(f"LLM execution error: {FailureType.LLM_EXECUTION_ERROR}")
#             return {
#                 "status": "failed",
#                 "failure_type": FailureType.LLM_EXECUTION_ERROR,
#                 "error": str(e),
#                 "retries": attempt
#             }

#         valid, failure_type, result = validate_summary(output)

#         if valid:
#             return {
#                 "status": "valid",
#                 "output": result,
#                 "retries": attempt,
#                 "failure_type": None
#             }

#         last_error = result
#         last_failure_type = failure_type

#         # prompt = (
#         #     "The previous output was invalid.\n"
#         #     f"Failure type: {failure_type}\n"
#         #     f"Error: {last_error}\n\n"
#         #     "Return ONLY valid JSON matching the schema."
#         # )
#         prompt = repair_prompt(prompt, last_failure_type)

#     return {
#         "status": "failed",
#         "failure_type": FailureType.REPAIR_EXHAUSTED_INVALID_DATA,
#         "error": last_error,
#         "retries": max_retries
#     }


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
