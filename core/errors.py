from enum import Enum


class FailureType(str, Enum):
    INVALID_JSON = "invalid_json"
    SCHEMA_VIOLATION = "schema_violation"
    LLM_EXECUTION_ERROR = "llm_execution_error"
    REPAIR_EXHAUSTED_INVALID_DATA = "repair_exhausted"
    UNKNOWN = "unknown"
    NONE = "none" 
