"""Entrypoint for running Jarvis Core as a background service.

Run with: python -m jarvis_core.service.main
"""

import uvicorn

from jarvis_core.config.loader import load_config
from jarvis_core.observability.logging import get_logger, setup_logging
from jarvis_core.permissions.store import PermissionStore
from jarvis_core.plugins.loader import discover_plugins
from jarvis_core.plugins.registry import PluginRegistry
from jarvis_core.service.app import create_app
from jarvis_core.storage.db import get_connection


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

    return create_app(permission_store, plugin_registry), config


def run() -> None:
    app, config = build_app()
    uvicorn.run(app, host=config.service.host, port=config.service.port)


if __name__ == "__main__":
    run()
