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

    count_and_delete_files_in_folder(folderpath =RUNS_DIR)
    return path

def count_and_delete_files_in_folder(folderpath):
    path = folderpath
    # Count only items that are files (not directories)
    count = sum(1 for entry in path.iterdir() if entry.is_file())
    # Delete oldest files if count exceeds 5
    sorted_files = sorted(path.iterdir(), key=lambda x: x.stat().st_mtime)
    for file in sorted_files:
        if file.is_file() and count>5:
            print(f"Deleting files to maintain folder size under limit. Current count: {count}")
            try:
                file.unlink()
                print(f'{file} is removed')
                count -= 1
                print(f"Updated count: {count}")
            except OSError as e:
                print(f'Error deleting {file}: {e}')
            else:
                break
    return count
