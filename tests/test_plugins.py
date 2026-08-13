from jarvis_core.plugins.loader import discover_plugins
from jarvis_core.plugins.manifest import PluginManifest
from jarvis_core.plugins.registry import PluginRegistry

VALID_MANIFEST = """
name: example-plugin
version: "0.1.0"
description: A test plugin.
permissions:
  - NETWORK
"""

INVALID_MANIFEST = """
version: "0.1.0"
"""  # missing required 'name' and 'description'


def test_discover_plugins_empty_dir_returns_no_results(tmp_path):
    result = discover_plugins(tmp_path)
    assert result.manifests == []
    assert result.errors == {}


def test_discover_plugins_missing_dir_returns_no_results(tmp_path):
    result = discover_plugins(tmp_path / "does-not-exist")
    assert result.manifests == []
    assert result.errors == {}


def test_discover_valid_plugin(tmp_path):
    plugin_dir = tmp_path / "example-plugin"
    plugin_dir.mkdir()
    (plugin_dir / "plugin.yaml").write_text(VALID_MANIFEST)

    result = discover_plugins(tmp_path)

    assert len(result.manifests) == 1
    assert result.manifests[0].name == "example-plugin"
    assert result.errors == {}


def test_invalid_plugin_is_isolated_not_fatal(tmp_path):
    good_dir = tmp_path / "good-plugin"
    good_dir.mkdir()
    (good_dir / "plugin.yaml").write_text(VALID_MANIFEST)

    bad_dir = tmp_path / "bad-plugin"
    bad_dir.mkdir()
    (bad_dir / "plugin.yaml").write_text(INVALID_MANIFEST)

    result = discover_plugins(tmp_path)

    assert len(result.manifests) == 1
    assert result.manifests[0].name == "example-plugin"
    assert "bad-plugin" in result.errors


def test_directory_without_manifest_is_skipped(tmp_path):
    (tmp_path / "not-a-plugin").mkdir()

    result = discover_plugins(tmp_path)

    assert result.manifests == []
    assert result.errors == {}


def test_registry_register_and_list():
    registry = PluginRegistry()
    manifest = PluginManifest(name="p1", version="1.0.0", description="desc")

    registry.register(manifest)

    assert registry.get("p1") is manifest
    assert registry.list_plugins() == [manifest]
