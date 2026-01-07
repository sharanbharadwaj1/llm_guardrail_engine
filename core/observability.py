import json
import time
from pathlib import Path
import datetime

RUNS_DIR = Path("runs")
RUNS_DIR.mkdir(exist_ok=True)


def write_run_artifact(data: dict):
    # ts = int(time.time() * 1000)
    ts = datetime.datetime.fromtimestamp(time.time()).strftime("%Y%m%d_%H%M%S_%f")

    print(f"Writing run artifact at timestamp: {ts}, time:{time.time()}")
    path = RUNS_DIR / f"run_{ts}.json"
    def serialize(obj):
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        return str(obj)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=serialize)

    return path
