import yaml
from pathlib import Path

class Policy:
    def __init__(self, path: str = "policy.yaml"):
        self.raw = yaml.safe_load(Path(path).read_text())

    @property
    def min_confidence(self) -> float:
        return self.raw["confidence"]["minimum"]

    @property
    def retries_fast(self) -> int:
        return self.raw["retries"]["fast_model"]

    @property
    def retries_strong(self) -> int:
        return self.raw["retries"]["strong_model"]

    @property
    def escalation_failures(self) -> set:
        return set(self.raw["escalation"]["failure_types"])
