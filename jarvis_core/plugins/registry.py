"""In-memory registry of validated plugin manifests for this run."""

from jarvis_core.plugins.manifest import PluginManifest


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, PluginManifest] = {}

    def register(self, manifest: PluginManifest) -> None:
        self._plugins[manifest.name] = manifest

    def get(self, name: str) -> PluginManifest | None:
        return self._plugins.get(name)

    def list_plugins(self) -> list[PluginManifest]:
        return list(self._plugins.values())
