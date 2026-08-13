import os

from jarvis_core.config.loader import load_config
from jarvis_core.config.schema import JarvisConfig


def test_defaults_when_no_file_or_env(tmp_path, monkeypatch):
    monkeypatch.delenv("JARVIS_CONFIG_PATH", raising=False)
    for key in list(os.environ):
        if key.startswith("JARVIS_"):
            monkeypatch.delenv(key, raising=False)

    config = load_config()

    assert config.service.host == "127.0.0.1"
    assert config.service.port == 8756


def test_yaml_file_overrides_defaults(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("service:\n  port: 9999\n")

    config = load_config(config_file)

    assert config.service.port == 9999
    assert config.service.host == "127.0.0.1"  # untouched default


def test_env_overrides_file_and_defaults(tmp_path, monkeypatch):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("service:\n  port: 9999\n")
    monkeypatch.setenv("JARVIS_SERVICE__PORT", "7000")

    config = load_config(config_file)

    assert config.service.port == 7000


def test_resolved_paths_are_under_data_dir(tmp_path):
    config = JarvisConfig(data_dir=str(tmp_path))

    assert config.resolved_db_path() == tmp_path / "jarvis.db"
    assert config.resolved_log_file() == tmp_path / "logs" / "jarvis.log"
    assert config.resolved_plugins_dir() == tmp_path / "plugins"
