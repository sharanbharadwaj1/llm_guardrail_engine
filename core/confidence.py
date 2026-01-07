from core.errors import FailureType


def compute_confidence(retries: int, success: bool, failure_type=None) -> float:
    confidence = 1.0

    confidence -= 0.2 * retries

    if not success:
        confidence -= 0.5

    if failure_type == FailureType.REPAIR_EXHAUSTED_INVALID_DATA:
        confidence -= 0.2

    return round(max(confidence, 0.0), 2)
