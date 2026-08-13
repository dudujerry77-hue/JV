"""Jarvis Core's local HTTP API -- see .jarvis/decisions.md D-0011.

Loopback-only by construction (the caller is responsible for binding to
127.0.0.1 -- see main.py). This is how a separate UI (Mission Control,
future chat client) observes and drives Jarvis Core; it is not a public
service.
"""

import time

from fastapi import FastAPI

from jarvis_core import __version__
from jarvis_core.permissions.store import PermissionStore
from jarvis_core.plugins.registry import PluginRegistry

CURRENT_PHASE = "Phase 1 - Foundation"


def create_app(
    permission_store: PermissionStore,
    plugin_registry: PluginRegistry,
) -> FastAPI:
    app = FastAPI(title="Jarvis Core", version=__version__)
    started_at = time.monotonic()

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.get("/status")
    def status() -> dict:
        grants = permission_store.list_grants()
        granted_count = sum(1 for g in grants if g["granted"])

        return {
            "phase": CURRENT_PHASE,
            "version": __version__,
            "uptime_seconds": round(time.monotonic() - started_at, 1),
            "plugins": [
                {"name": p.name, "version": p.version}
                for p in plugin_registry.list_plugins()
            ],
            "permissions": {
                "granted": granted_count,
                "total": len(grants),
            },
        }

    return app
