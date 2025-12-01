from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml


class ConfigError(Exception):
    """Raised when the configuration file is invalid."""


def load_config(path: str | Path) -> Dict[str, Any]:
    """
    Load YAML configuration.

    Expected top-level keys:
      - excel_path
      - database_url
      - sheets
    """
    cfg_path = Path(path)
    if not cfg_path.exists():
        raise ConfigError(f"Config file not found: {cfg_path}")

    with cfg_path.open("r", encoding="utf8") as f:
        cfg = yaml.safe_load(f) or {}

    for key in ("excel_path", "database_url", "sheets"):
        if key not in cfg:
            raise ConfigError(f"Config missing required key: {key}")

    excel_path = Path(cfg["excel_path"])
    cfg["excel_path"] = excel_path

    sheets = cfg.get("sheets", {})
    if not isinstance(sheets, dict) or not sheets:
        raise ConfigError("'sheets' must be a non-empty mapping")

    return cfg
