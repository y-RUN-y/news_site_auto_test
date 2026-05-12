import subprocess
import sys
import tomllib
from pathlib import Path

# 将项目根目录添加到 Python 路径
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def run_lint():
    config_path = project_root / "pixi.toml"
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    autoflake_cfg = config.get("tool", {}).get("autoflake", {})

    cmd = ["autoflake"]
    exclude = list(autoflake_cfg.get("exclude", []))
    if ".pixi" not in exclude:
        exclude.append(".pixi")
    cmd.append(f"--exclude={','.join(exclude)}")
    for key, value in autoflake_cfg.items():
        if key == "exclude":
            continue
        elif value is True:
            cmd.append(f"--{key.replace('_', '-')}")
        elif value is not False:
            if isinstance(value, bool):
                continue
            cmd.append(f"--{key.replace('_', '-')}={value}")

    cmd.append(".")
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, shell=True)

    subprocess.run(["black", ".", "--exclude", ".pixi"], shell=True)
    subprocess.run(["isort", ".", "-s", ".pixi"], shell=True)


if __name__ == "__main__":
    run_lint()
