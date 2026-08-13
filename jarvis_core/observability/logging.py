"""Structured logging foundation.

Implements the "logs" requirement from .jarvis/observability_spec.md.
Every subsystem should log through get_logger(__name__) rather than
printing or creating its own handlers, so log output stays centralized and
consistent.
"""

import logging
from logging.handlers import RotatingFileHandler

from jarvis_core.config.schema import JarvisConfig

ROOT_LOGGER_NAME = "jarvis"
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"

_configured = False


def setup_logging(config: JarvisConfig) -> None:
    """Idempotent: safe to call once at service startup."""
    global _configured
    if _configured:
        return

    log_file = config.resolved_log_file()
    log_file.parent.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger(ROOT_LOGGER_NAME)
    root.setLevel(config.logging.level.upper())
    root.handlers.clear()

    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=5_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    _configured = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"{ROOT_LOGGER_NAME}.{name}")
