import shutil
from pathlib import Path

project_root = Path(__file__).parent

targets = ["screenshots", "report", "test_log.log"]
for target in targets:
    path = project_root / target
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        print(f"Removed: {target}")
