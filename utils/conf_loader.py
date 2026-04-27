import tomllib


def load_config():
    with open("pyproject.toml", mode="rb") as f:
        data = tomllib.load(f)
    return data["tool"]


config = load_config()
