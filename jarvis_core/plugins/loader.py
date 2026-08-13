"""Plugin discovery -- see .jarvis/plugin_spec.md.

A malformed plugin must not take down Core (.jarvis/failure_recovery.md
self-healing table: "Plugin crashed -> isolate plugin"). Discovery
collects per-plugin errors instead of raising on the first bad manifest.
"""

from dataclasses import dataclass, field
from pathlib import Path

import yaml
from pydantic import ValidationError

from jarvis_core.observability.logging import get_logger
from jarvis_core.plugins.manifest import PluginManifest

logger = get_logger("plugins")

MANIFEST_FILENAMES = ("plugin.yaml", "plugin.yml", "plugin.json")


@dataclass
class DiscoveryResult:
    manifests: list[PluginManifest] = field(default_factory=list)
    errors: dict[str, str] = field(default_factory=dict)


def _find_manifest_file(plugin_dir: Path) -> Path | None:
    for filename in MANIFEST_FILENAMES:
        candidate = plugin_dir / filename
        if candidate.is_file():
            return candidate
    return None


def discover_plugins(plugins_dir: Path) -> DiscoveryResult:
    result = DiscoveryResult()

    if not plugins_dir.is_dir():
        return result

    for entry in sorted(plugins_dir.iterdir()):
        if not entry.is_dir():
            continue

        manifest_file = _find_manifest_file(entry)
        if manifest_file is None:
            continue

        try:
            raw = yaml.safe_load(manifest_file.read_text(encoding="utf-8")) or {}
            manifest = PluginManifest(**raw)
        except (ValidationError, yaml.YAMLError, OSError) as exc:
            logger.warning("failed to load plugin manifest %s: %s", manifest_file, exc)
            result.errors[str(entry.name)] = str(exc)
            continue

        result.manifests.append(manifest)

    return result
