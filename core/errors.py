from enum import Enum


class FailureType(str, Enum):
    INVALID_JSON = "invalid_json"
    SCHEMA_VIOLATION = "schema_violation"
    LLM_EXECUTION_ERROR = "llm_execution_error"
    REPAIR_EXHAUSTED_INVALID_DATA = "repair_exhausted"
    UNKNOWN = "unknown"
    NONE = "none" 

     # Level 2 additions
    EMPTY_INPUT = "EMPTY_INPUT"
    TOO_SHORT = "TOO_SHORT"
    TOO_LONG = "TOO_LONG"
    INVALID_FORMAT = "INVALID_FORMAT"

    #batch timeout
    TIMEOUT = "TIMEOUT"

    #LLM
    LLM_PROVIDER_ERROR = "LLM_PROVIDER_ERROR" or "INTERNAL_ERROR"
    LLM_AUTH_FAILURE = "LLM_AUTH_FAILURE" or "INTERNAL_ERROR"
