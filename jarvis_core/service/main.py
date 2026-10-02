"""Entrypoint for running Jarvis Core as a background service.

Run with: python -m jarvis_core.service.main
"""

import uvicorn

from jarvis_core.ai.anthropic_provider import AnthropicProvider
from jarvis_core.ai.cost import CostTracker
from jarvis_core.ai.router import AIRouter
from jarvis_core.config.loader import load_config
from jarvis_core.observability.logging import get_logger, setup_logging
from jarvis_core.permissions.store import PermissionStore
from jarvis_core.plugins.loader import discover_plugins
from jarvis_core.plugins.registry import PluginRegistry
from jarvis_core.service.app import create_app
from jarvis_core.storage.db import get_connection

_PROVIDER_CLASSES = {
    "anthropic": AnthropicProvider,
}


def _build_ai_router(config, permission_store: PermissionStore, conn) -> AIRouter | None:
    """Build the configured AIRouter, or None if the configured provider
    isn't one we know how to construct yet (D-0015: only Anthropic exists
    as a concrete provider so far). Never raises -- a missing/unsupported
    provider means /ai/complete is unavailable, not that Core fails to
    start (D-0008's "never require payment merely to exist" extends to
    never requiring AI configuration merely to run)."""
    provider_class = _PROVIDER_CLASSES.get(config.ai.provider)
    if provider_class is None:
        return None

    cost_tracker = CostTracker(conn, monthly_ceiling_usd=config.ai.monthly_cost_ceiling_usd)
    return AIRouter(
        provider=provider_class(),
        model=config.ai.model,
        permission_store=permission_store,
        cost_tracker=cost_tracker,
        input_cost_per_1k_usd=config.ai.input_cost_per_1k_usd,
        output_cost_per_1k_usd=config.ai.output_cost_per_1k_usd,
    )


def build_app():
    config = load_config()
    setup_logging(config)
    logger = get_logger("service")

    conn = get_connection(config.resolved_db_path())
    permission_store = PermissionStore(conn)

    plugin_registry = PluginRegistry()
    discovery = discover_plugins(config.resolved_plugins_dir())
    for manifest in discovery.manifests:
        plugin_registry.register(manifest)
    for plugin_name, error in discovery.errors.items():
        logger.warning("plugin %s failed to load: %s", plugin_name, error)
    logger.info("loaded %d plugin(s)", len(discovery.manifests))

    ai_router = _build_ai_router(config, permission_store, conn)

    return create_app(permission_store, plugin_registry, ai_router), config


def run() -> None:
    app, config = build_app()
    uvicorn.run(app, host=config.service.host, port=config.service.port)


if __name__ == "__main__":
    run()
