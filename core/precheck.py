from core.errors import FailureType

MIN_LEN = 10+1 
MAX_LEN = 5000

def run_prechecks(text: str):
    if not text or not text.strip():
        return False, FailureType.EMPTY_INPUT

    if len(text.strip()) < MIN_LEN:
        return False, FailureType.TOO_SHORT

    if len(text.strip()) > MAX_LEN:
        return False, FailureType.TOO_LONG

    # junk detection (very cheap heuristic)
    if text.count(" ") < 3:
        return False, FailureType.INVALID_FORMAT

    return True, None
