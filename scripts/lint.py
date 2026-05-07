import subprocess
import tomllib
from pathlib import Path

project_root = Path(__file__).parent


def run_lint():
    config_path = project_root / "pixi.toml"
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    autoflake_cfg = config.get("tool", {}).get("autoflake", {})

    cmd = ["autoflake"]
    for key, value in autoflake_cfg.items():
        if key == "exclude" and isinstance(value, list):
            cmd.append(f"--exclude={','.join(value)}")
        elif value is True:
            cmd.append(f"--{key.replace('_', '-')}")
        elif value is not False:
            if isinstance(value, bool):
                continue
            cmd.append(f"--{key.replace('_', '-')}={value}")

    cmd.append(".")
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)

    subprocess.run(["black", "."])
    subprocess.run(["isort", "."])


if __name__ == "__main__":
    run_lint()