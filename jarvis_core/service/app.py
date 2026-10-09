"""Jarvis Core's local HTTP API -- see .jarvis/decisions.md D-0011.

Loopback-only by construction (the caller is responsible for binding to
127.0.0.1 -- see main.py). This is how a separate UI (Mission Control,
Settings, future chat client) observes and drives Jarvis Core; it is not a
public service.
"""

import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from jarvis_core import __version__
from jarvis_core.credentials.store import (
    SUPPORTED_PROVIDERS,
    CredentialStore,
)
from jarvis_core.permissions.store import PermissionStore
from jarvis_core.plugins.registry import PluginRegistry

CURRENT_PHASE = "Phase 1 - Foundation"


class KeyPayload(BaseModel):
    provider: str = Field(..., description="groq or google")
    key: str = Field(..., min_length=1, description="API key value")


def create_app(
    permission_store: PermissionStore,
    plugin_registry: PluginRegistry,
    credential_store: CredentialStore | None = None,
) -> FastAPI:
    app = FastAPI(title="Jarvis Core", version=__version__)
    started_at = time.monotonic()
    credentials = credential_store or CredentialStore()

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
            "keys": credentials.status(),
        }

    @app.get("/settings/keys/status")
    def keys_status() -> dict:
        """Whether each AI provider key is set. Never returns the key values."""
        return {"keys": credentials.status()}

    @app.post("/settings/keys")
    def save_key(payload: KeyPayload) -> dict:
        provider = payload.provider.lower().strip()
        if provider not in SUPPORTED_PROVIDERS:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Unsupported provider {provider!r}. "
                    f"Supported: {', '.join(SUPPORTED_PROVIDERS)}"
                ),
            )
        try:
            credentials.set_key(provider, payload.key)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
        return {"ok": True, "provider": provider, "saved": True}

    @app.delete("/settings/keys/{provider}")
    def delete_key(provider: str) -> dict:
        provider = provider.lower().strip()
        if provider not in SUPPORTED_PROVIDERS:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Unsupported provider {provider!r}. "
                    f"Supported: {', '.join(SUPPORTED_PROVIDERS)}"
                ),
            )
        try:
            credentials.delete_key(provider)
        except RuntimeError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
        return {"ok": True, "provider": provider, "deleted": True}

    return app
