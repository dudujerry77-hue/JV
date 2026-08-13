"""Layered config loading: defaults -> YAML file -> environment overrides.

Never put secrets here -- see .jarvis/decisions.md D-0012. This layer is
for structural configuration (ports, paths, log level) only.
"""

import os
from pathlib import Path
from typing import Any

import yaml

from jarvis_core.config.schema import JarvisConfig

ENV_PREFIX = "JARVIS_"
DEFAULT_CONFIG_ENV_VAR = "JARVIS_CONFIG_PATH"


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _load_yaml_file(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


def _env_overrides() -> dict[str, Any]:
    """Flat JARVIS_SECTION__FIELD=value overrides, e.g. JARVIS_SERVICE__PORT=9000."""
    overrides: dict[str, Any] = {}
    for key, raw_value in os.environ.items():
        if not key.startswith(ENV_PREFIX) or key == DEFAULT_CONFIG_ENV_VAR:
            continue
        path = key[len(ENV_PREFIX) :].lower().split("__")
        node = overrides
        for part in path[:-1]:
            node = node.setdefault(part, {})
        node[path[-1]] = raw_value
    return overrides


def load_config(config_path: str | Path | None = None) -> JarvisConfig:
    """Load config with precedence: env overrides > file > schema defaults."""
    raw_path = config_path or os.environ.get(DEFAULT_CONFIG_ENV_VAR, "")
    resolved_path = Path(raw_path) if raw_path else None
    file_data = _load_yaml_file(resolved_path) if resolved_path else {}
    merged = _deep_merge(file_data, _env_overrides())
    return JarvisConfig(**merged)
