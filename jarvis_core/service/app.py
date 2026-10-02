"""Jarvis Core's local HTTP API -- see .jarvis/decisions.md D-0011.

Loopback-only by construction (service.host is validated in
jarvis_core/config/schema.py -- see main.py). This is how a separate UI
(Mission Control, future chat client) observes and drives Jarvis Core; it
is not a public service.
"""

import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from jarvis_core import __version__
from jarvis_core.ai.provider import AIProviderError
from jarvis_core.ai.router import AIRouter, CostCeilingExceeded
from jarvis_core.permissions.checker import PermissionDenied
from jarvis_core.permissions.store import PermissionStore
from jarvis_core.plugins.registry import PluginRegistry

CURRENT_PHASE = "Phase 3 - Multi-AI Brain"


class AICompleteRequest(BaseModel):
    prompt: str


def create_app(
    permission_store: PermissionStore,
    plugin_registry: PluginRegistry,
    ai_router: AIRouter | None = None,
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
            "ai_router_configured": ai_router is not None,
        }

    @app.post("/ai/complete")
    def ai_complete(request: AICompleteRequest) -> dict:
        if ai_router is None:
            raise HTTPException(
                status_code=503, detail="no AI provider is configured for this run"
            )
        try:
            response = ai_router.complete(request.prompt)
        except PermissionDenied as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from exc
        except CostCeilingExceeded as exc:
            raise HTTPException(status_code=402, detail=str(exc)) from exc
        except AIProviderError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

        return {
            "text": response.text,
            "model": response.model,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
        }

    return app
