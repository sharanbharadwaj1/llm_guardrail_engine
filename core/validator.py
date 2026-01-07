from pydantic import ValidationError
from schemas.summary import SummaryOutput
from core.errors import FailureType
from schemas.summary import SummaryOutput
import json

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
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as e:
        return False, FailureType.INVALID_JSON, str(e)

    try:
        parsed = SummaryOutput.model_validate(data)
        return True, FailureType.NONE, parsed
    except ValidationError as e:
        return False, FailureType.SCHEMA_VIOLATION, str(e)
