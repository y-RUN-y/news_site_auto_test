import tomllib
from pathlib import Path

# 项目根路径，统一在此定义
project_root = Path(__file__).resolve().parent.parent


def load_config():
    with open(project_root / "pixi.toml", mode="rb") as f:
        data = tomllib.load(f)
    return data["tool"]


config = load_config()
