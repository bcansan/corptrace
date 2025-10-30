import os
from pathlib import Path


def load_env() -> None:
    env_path = Path(".env")
    if not env_path.exists():
        return
    with env_path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.strip().startswith("#"):
                continue
            key, _, value = line.strip().partition("=")
            if key and value:
                os.environ.setdefault(key, value)
