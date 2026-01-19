from pydantic import ValidationError
from schemas.summary import SummaryOutput
from core.errors import FailureType
from schemas.summary import SummaryOutput
import json
from core.semantic_validator import validate_semantics


# def validate_summary(raw_text: str):
#     """
#     Returns: (is_valid: bool, parsed | error)
#     """
#     try:
#         parsed = SummaryOutput.model_validate_json(raw_text)
#         return True, parsed
#     except ValidationError as e:
#         return False, str(e)

def validate_summary(raw_text: str):
    score = 0.0
    try:
        data = json.loads(raw_text)
        # if raw_text:
        #     ok, score = validate_semantics(raw_text, parsed.summary)
        #     if not ok:
        #         return False, FailureType.SEMANTIC_MISMATCH, {
        #             "semantic_score": score
        #         }
    except json.JSONDecodeError as e:
        return False, FailureType.INVALID_JSON, str(e),score

    try:
        parsed = SummaryOutput.model_validate(data)
        if parsed.summary and raw_text:
            ok, score = validate_semantics(raw_text, parsed.summary)
            if not ok:
                return False, FailureType.SEMANTIC_MISMATCH, {
                    "semantic_score": score
                }
        return True, FailureType.NONE, parsed,score
    except ValidationError as e:
        return False, FailureType.SCHEMA_VIOLATION, str(e),score
    
    # 2) Semantic validation (NEW)
    # try:

    #     if raw_text:
    #         ok, score = validate_semantics(raw_text, parsed.summary)
    #         if not ok:
    #             return False, FailureType.SEMANTIC_MISMATCH, {
    #                 "semantic_score": score
    #             }

    #     return True, None, parsed
